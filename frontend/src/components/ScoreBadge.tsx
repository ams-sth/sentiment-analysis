import type { SentimentLabel } from "../types";

const styles: Record<SentimentLabel, string> = {
  Positive: "bg-emerald-500/20 text-emerald-300 ring-1 ring-emerald-500/40",
  Neutral: "bg-amber-500/20 text-amber-300 ring-1 ring-amber-500/40",
  Negative: "bg-rose-500/20 text-rose-300 ring-1 ring-rose-500/40",
};

export default function ScoreBadge({ label }: { label: SentimentLabel }) {
  return (
    <span className={`inline-block px-4 py-1 rounded-full text-sm font-semibold ${styles[label]}`}>
      {label}
    </span>
  );
}
