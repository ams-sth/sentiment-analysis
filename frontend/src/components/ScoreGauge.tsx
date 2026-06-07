export default function ScoreGauge({ score }: { score: number }) {
  const pct = ((score + 1) / 2) * 100;

  const markerColor =
    score >= 0.05 ? "bg-emerald-400" : score <= -0.05 ? "bg-rose-400" : "bg-amber-400";

  return (
    <div className="mt-2">
      <div className="flex justify-between text-white/40 text-xs mb-2">
        <span>−1.0 Negative</span>
        <span>Neutral</span>
        <span>Positive +1.0</span>
      </div>
      <div className="relative h-2 rounded-full overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-rose-500/60 via-amber-400/60 to-emerald-500/60" />
        <div
          className={`absolute top-0 bottom-0 w-1 ${markerColor} rounded-full shadow-[0_0_6px_2px_rgba(255,255,255,0.4)]`}
          style={{ left: `calc(${pct}% - 2px)` }}
        />
      </div>
    </div>
  );
}
