import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import ProgressBar from "../components/ProgressBar";
import Spinner from "../components/Spinner";
import { analyzeCsvStream, analyzeText, previewCsv } from "../lib/api";

type CsvPhase =
  | { status: "idle" }
  | { status: "detecting" }
  | {
      status: "selecting";
      columns: string[];
      filename: string;
      recommended: string | null;
      selected: string;
    }
  | { status: "analyzing"; progress: number; message: string };

export default function Home() {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [text, setText] = useState("");
  const [textLoading, setTextLoading] = useState(false);
  const [csvPhase, setCsvPhase] = useState<CsvPhase>({ status: "idle" });
  const [error, setError] = useState<string | null>(null);

  const handleText = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    setTextLoading(true);
    setError(null);
    try {
      const result = await analyzeText(text.trim());
      navigate("/result", { state: { result } });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setTextLoading(false);
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setCsvPhase({ status: "detecting" });
    setError(null);
    try {
      const preview = await previewCsv(file);
      setCsvPhase({
        status: "selecting",
        columns: preview.columns,
        filename: preview.filename,
        recommended: preview.recommended,
        selected: preview.recommended ?? preview.columns[0] ?? "",
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to read CSV");
      setCsvPhase({ status: "idle" });
    }
  };

  const handleCsvAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (csvPhase.status !== "selecting") return;
    const { filename, selected } = csvPhase;
    setCsvPhase({ status: "analyzing", progress: 0, message: "Starting…" });
    setError(null);
    try {
      const result = await analyzeCsvStream(filename, selected, (progress, message) => {
        setCsvPhase({ status: "analyzing", progress, message });
      });
      navigate("/result/csv", { state: { result } });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setCsvPhase({ status: "idle" });
    }
  };

  const resetCsv = () => {
    setCsvPhase({ status: "idle" });
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="min-h-screen bg-zinc-950">
      {/* Hero */}
      <header className="text-center pt-20 pb-12 px-4">
        <div className="inline-flex items-center gap-2 bg-sky-500/10 text-sky-300 text-sm px-4 py-1.5 rounded-full ring-1 ring-sky-500/20 mb-6">
          VADER · NLTK · React
        </div>
        <h1 className="text-5xl font-bold text-white mb-4 tracking-tight">Sentiment Analysis</h1>
        <p className="text-slate-400 text-lg max-w-sm mx-auto">
          Understand the emotion behind any text — one sentence or an entire dataset.
        </p>
      </header>

      {/* Cards */}
      <main className="max-w-3xl mx-auto px-4 pb-20 grid gap-5 md:grid-cols-2">
        {/* Text form */}
        <form
          onSubmit={handleText}
          className="bg-white/5 backdrop-blur-sm rounded-2xl p-7 border border-white/10 flex flex-col gap-5 hover:border-white/20 transition-colors"
        >
          <div>
            <h2 className="text-lg font-semibold text-white mb-1">Analyze Text</h2>
            <p className="text-slate-400 text-sm">
              Paste any text and get an instant compound sentiment score.
            </p>
          </div>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type or paste text here…"
            required
            rows={5}
            className="w-full bg-white/5 text-white placeholder-white/25 rounded-xl px-4 py-3 border border-white/10 focus:outline-none focus:ring-2 focus:ring-sky-500/50 resize-none text-sm"
          />
          <button
            type="submit"
            disabled={textLoading || !text.trim()}
            className="flex items-center justify-center gap-2 bg-sky-600 hover:bg-sky-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold py-2.5 rounded-xl transition-colors text-sm"
          >
            {textLoading ? <Spinner size="sm" /> : null}
            {textLoading ? "Analyzing…" : "Analyze"}
          </button>
        </form>

        {/* CSV form */}
        <form
          onSubmit={handleCsvAnalyze}
          className="bg-white/5 backdrop-blur-sm rounded-2xl p-7 border border-white/10 flex flex-col gap-5 hover:border-white/20 transition-colors"
        >
          <div>
            <h2 className="text-lg font-semibold text-white mb-1">Analyze CSV</h2>
            <p className="text-slate-400 text-sm">
              Upload a CSV — we'll auto-detect the review column or let you pick one.
            </p>
          </div>

          {/* Always-hidden file input */}
          <input
            ref={fileInputRef}
            id="csv-file"
            type="file"
            accept=".csv"
            className="hidden"
            onChange={handleFileSelect}
          />

          {/* Idle: drop zone */}
          {csvPhase.status === "idle" && (
            <label
              htmlFor="csv-file"
              className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-white/20 rounded-xl cursor-pointer hover:border-purple-400/60 transition-colors group"
            >
              <p className="text-white/40 text-sm group-hover:text-white/60 transition-colors">
                Click to upload
              </p>
              <p className="text-slate-500 text-xs mt-1">.csv files only</p>
            </label>
          )}

          {/* Detecting: reading headers */}
          {csvPhase.status === "detecting" && (
            <div className="flex items-center justify-center h-32 gap-3">
              <Spinner size="sm" />
              <span className="text-white/40 text-sm">Reading columns…</span>
            </div>
          )}

          {/* Selecting: column picker */}
          {csvPhase.status === "selecting" && (
            <div className="space-y-3">
              <div className="flex items-center gap-2 bg-white/5 rounded-xl px-3 py-2">
                <span className="text-white/70 text-sm truncate flex-1">{csvPhase.filename}</span>
                <button
                  type="button"
                  onClick={resetCsv}
                  className="text-purple-400 hover:text-purple-300 text-xs shrink-0 transition-colors"
                >
                  Change
                </button>
              </div>
              <div>
                <p className="text-white/50 text-xs mb-1.5">Review column</p>
                <select
                  value={csvPhase.selected}
                  onChange={(e) => setCsvPhase({ ...csvPhase, selected: e.target.value })}
                  className="w-full bg-slate-800 text-white border border-white/10 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500/50"
                >
                  {csvPhase.columns.map((col) => (
                    <option key={col} value={col}>
                      {col}
                      {csvPhase.recommended === col ? " ★" : ""}
                    </option>
                  ))}
                </select>
                {csvPhase.recommended && (
                  <p className="text-white/30 text-xs mt-1.5">★ auto-detected review column</p>
                )}
              </div>
            </div>
          )}

          {/* Analyzing: progress bar */}
          {csvPhase.status === "analyzing" && (
            <div className="flex items-center py-6">
              <ProgressBar percent={csvPhase.progress} message={csvPhase.message} />
            </div>
          )}

          {/* Submit button — shown only while idle or selecting */}
          {(csvPhase.status === "idle" || csvPhase.status === "selecting") && (
            <button
              type="submit"
              disabled={csvPhase.status !== "selecting"}
              className="flex items-center justify-center gap-2 bg-sky-600 hover:bg-sky-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold py-2.5 rounded-xl transition-colors text-sm"
            >
              Analyze CSV
            </button>
          )}
        </form>
      </main>

      {/* Error toast */}
      {error && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 bg-rose-600 text-white text-sm px-5 py-3 rounded-xl shadow-xl ring-1 ring-rose-400/40">
          {error}
        </div>
      )}
    </div>
  );
}
