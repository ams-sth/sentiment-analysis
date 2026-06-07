import { Navigate, useLocation, useNavigate } from "react-router-dom";
import Accordion from "../components/Accordion";
import ScoreBadge from "../components/ScoreBadge";
import SentimentCharts from "../components/SentimentCharts";
import type { CsvResult as CsvResultType } from "../types";

const MAX_PREVIEW = 100;

function sentimentColor(s: number) {
  if (s >= 0.05) return "text-emerald-400";
  if (s <= -0.05) return "text-rose-400";
  return "text-amber-400";
}

function exportResults(data: CsvResultType) {
  const lines: string[] = ["#,Review,Sentiment Score,Label"];
  for (let i = 0; i < data.table_data.length; i++) {
    const row = data.table_data[i];
    const label =
      row.sentiment >= 0.05 ? "Positive" : row.sentiment <= -0.05 ? "Negative" : "Neutral";
    lines.push(`${i + 1},"${row.review.replace(/"/g, '""')}",${row.sentiment},${label}`);
  }
  // UTF-8 BOM so Excel opens it correctly
  const blob = new Blob([`﻿${lines.join("\n")}`], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "sentiment_results.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 100);
}

export default function CsvResult() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const result = (state as { result?: CsvResultType } | null)?.result;

  if (!result) return <Navigate to="/" replace />;

  const avgSign = result.avg_sentiment > 0 ? "+" : "";
  const avgColor = sentimentColor(result.avg_sentiment);

  return (
    <div className="min-h-screen bg-zinc-950">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <button
            type="button"
            onClick={() => navigate("/")}
            className="text-slate-400 hover:text-white transition-colors text-sm"
          >
            ← Back
          </button>
          <h1 className="text-2xl font-bold text-white flex-1">CSV Analysis Report</h1>
          <button
            type="button"
            onClick={() => exportResults(result)}
            className="flex items-center gap-1.5 bg-white/10 hover:bg-white/15 text-white/70 hover:text-white text-sm px-3 py-1.5 rounded-xl border border-white/15 transition-colors"
          >
            ↓ Export CSV
          </button>
        </div>

        {/* Row-cap notice */}
        {result.total_rows_in_file > result.num_reviews && (
          <div className="mb-4 px-4 py-2.5 bg-amber-500/10 border border-amber-500/30 rounded-xl text-amber-300 text-sm">
            File has {result.total_rows_in_file.toLocaleString()} rows — analysed the first{" "}
            {result.num_reviews.toLocaleString()} for performance.
          </div>
        )}

        {/* Stats row */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          <div className="bg-white/5 rounded-2xl border border-white/10 p-5 text-center">
            <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Reviews Analysed</p>
            <p className="text-3xl font-bold text-white">{result.num_reviews.toLocaleString()}</p>
          </div>
          <div className="bg-white/5 rounded-2xl border border-white/10 p-5 text-center">
            <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Avg Score</p>
            <p className={`text-3xl font-bold ${avgColor}`}>
              {avgSign}
              {result.avg_sentiment.toFixed(4)}
            </p>
          </div>
          <div className="bg-white/5 rounded-2xl border border-white/10 p-5 text-center">
            <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Overall</p>
            <div className="mt-2">
              <ScoreBadge label={result.overall_sentiment} />
            </div>
          </div>
        </div>

        {/* Sections */}
        <div className="space-y-4">
          <Accordion title="Charts" defaultOpen>
            <SentimentCharts data={result} />
          </Accordion>

          <Accordion title={`Top Positive Comments (${result.positive_comments.length})`}>
            {result.positive_comments.length === 0 ? (
              <p className="text-slate-400 text-sm mt-4">No positive comments found.</p>
            ) : (
              <ol className="mt-4 space-y-4">
                {result.positive_comments.map((c, i) => (
                  <li key={c.comment} className="flex gap-3">
                    <span className="text-emerald-400 font-bold shrink-0 text-sm">{i + 1}.</span>
                    <div>
                      <p className="text-white/75 text-sm leading-relaxed">{c.comment}</p>
                      <span className="text-emerald-400 text-xs font-mono">
                        +{c.score.toFixed(4)}
                      </span>
                    </div>
                  </li>
                ))}
              </ol>
            )}
          </Accordion>

          <Accordion title={`Top Negative Comments (${result.negative_comments.length})`}>
            {result.negative_comments.length === 0 ? (
              <p className="text-slate-400 text-sm mt-4">No negative comments found.</p>
            ) : (
              <ol className="mt-4 space-y-4">
                {result.negative_comments.map((c, i) => (
                  <li key={c.comment} className="flex gap-3">
                    <span className="text-rose-400 font-bold shrink-0 text-sm">{i + 1}.</span>
                    <div>
                      <p className="text-white/75 text-sm leading-relaxed">{c.comment}</p>
                      <span className="text-rose-400 text-xs font-mono">{c.score.toFixed(4)}</span>
                    </div>
                  </li>
                ))}
              </ol>
            )}
          </Accordion>

          <Accordion title={`Full Data Table (${result.table_data.length} rows)`}>
            <div className="mt-4 overflow-x-auto max-h-80 overflow-y-auto rounded-xl">
              <table className="w-full text-sm">
                <thead className="sticky top-0 bg-slate-900/90 backdrop-blur-sm">
                  <tr>
                    <th className="text-left px-3 py-2 text-zinc-400 font-medium">#</th>
                    <th className="text-left px-3 py-2 text-zinc-400 font-medium">Review</th>
                    <th className="text-right px-3 py-2 text-zinc-400 font-medium">Score</th>
                  </tr>
                </thead>
                <tbody>
                  {result.table_data.map((row, i) => {
                    return (
                      <tr key={i} className="border-t border-white/5 hover:bg-white/5">
                        <td className="px-3 py-2 text-white/30 text-xs">{i + 1}</td>
                        <td className="px-3 py-2 text-white/70">{row.review}</td>
                        <td
                          className={`px-3 py-2 text-right font-mono text-xs ${sentimentColor(row.sentiment)}`}
                        >
                          {row.sentiment > 0 ? "+" : ""}
                          {row.sentiment.toFixed(4)}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </Accordion>

          <Accordion title={`Raw Data (${result.raw_data.length} rows)`}>
            <div className="mt-4 max-h-64 overflow-y-auto space-y-1.5">
              {result.raw_data.slice(0, MAX_PREVIEW).map((text, i) => {
                return (
                  <p key={i} className="text-white/55 text-sm py-1 border-b border-white/5">
                    <span className="text-zinc-600 font-mono text-xs mr-2">{i + 1}.</span>
                    {text}
                  </p>
                );
              })}
              {result.raw_data.length > MAX_PREVIEW && (
                <p className="text-slate-500 text-xs text-center pt-2">
                  … and {result.raw_data.length - MAX_PREVIEW} more rows
                </p>
              )}
            </div>
          </Accordion>

          <Accordion title={`Cleaned Data (${result.cleaned_data.length} rows)`}>
            <div className="mt-4 max-h-64 overflow-y-auto space-y-1.5">
              {result.cleaned_data.slice(0, MAX_PREVIEW).map((text, i) => {
                return (
                  <p
                    key={i}
                    className="text-white/55 text-sm py-1 border-b border-white/5 font-mono"
                  >
                    <span className="text-zinc-600 text-xs mr-2">{i + 1}.</span>
                    {text}
                  </p>
                );
              })}
              {result.cleaned_data.length > MAX_PREVIEW && (
                <p className="text-slate-500 text-xs text-center pt-2">
                  … and {result.cleaned_data.length - MAX_PREVIEW} more rows
                </p>
              )}
            </div>
          </Accordion>
        </div>
      </div>
    </div>
  );
}
