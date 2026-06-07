import { Navigate, useLocation, useNavigate } from "react-router-dom";
import ScoreBadge from "../components/ScoreBadge";
import ScoreGauge from "../components/ScoreGauge";
import type { TextResult as TextResultType } from "../types";

function scoreColor(s: number) {
  if (s >= 0.05) return "text-emerald-400";
  if (s <= -0.05) return "text-rose-400";
  return "text-amber-400";
}

export default function TextResult() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const result = (state as { result?: TextResultType } | null)?.result;

  if (!result) return <Navigate to="/" replace />;

  const sign = result.score > 0 ? "+" : "";

  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center p-6">
      <div className="w-full max-w-lg">
        {/* Card */}
        <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-8">
          <h1 className="text-xl font-bold text-white mb-8">Analysis Result</h1>

          {/* Score */}
          <div className="text-center mb-6">
            <p className={`text-7xl font-black tracking-tight ${scoreColor(result.score)}`}>
              {sign}
              {result.score.toFixed(4)}
            </p>
            <div className="mt-3">
              <ScoreBadge label={result.label} />
            </div>
          </div>

          <ScoreGauge score={result.score} />

          {/* Input text */}
          <div className="mt-8">
            <p className="text-white/40 text-xs uppercase tracking-wider mb-2">Analyzed Text</p>
            <blockquote className="bg-white/5 rounded-xl px-5 py-4 text-white/70 text-sm italic border-l-4 border-sky-500/50 leading-relaxed">
              "{result.text}"
            </blockquote>
          </div>
        </div>

        <button
          type="button"
          onClick={() => navigate("/")}
          className="mt-4 w-full bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white font-medium py-3 rounded-xl transition-colors border border-white/10 text-sm"
        >
          ← Back to Home
        </button>
      </div>
    </div>
  );
}
