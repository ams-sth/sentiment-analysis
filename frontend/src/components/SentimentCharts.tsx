import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { CsvResult } from "../types";

const PIE_COLORS: Record<string, string> = {
  Positive: "#34d399",
  Neutral: "#fbbf24",
  Negative: "#fb7185",
};

const tooltipStyle = {
  contentStyle: {
    background: "#18181b",
    border: "1px solid rgba(255,255,255,0.10)",
    borderRadius: 10,
  },
  itemStyle: { color: "#e4e4e7" },
  labelStyle: { color: "#7dd3fc" },
};

export default function SentimentCharts({ data }: { data: CsvResult }) {
  const pieData = [
    { name: "Positive", value: data.sentiment_breakdown.positive },
    { name: "Neutral", value: data.sentiment_breakdown.neutral },
    { name: "Negative", value: data.sentiment_breakdown.negative },
  ].filter((d) => d.value > 0);

  return (
    <div className="space-y-10">
      {/* Donut: sentiment breakdown */}
      <div>
        <p className="text-white/60 text-sm text-center mb-4 uppercase tracking-wider">
          Sentiment Breakdown
        </p>
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              innerRadius={70}
              outerRadius={110}
              paddingAngle={4}
              dataKey="value"
            >
              {pieData.map((entry) => (
                <Cell key={entry.name} fill={PIE_COLORS[entry.name] ?? "#94a3b8"} />
              ))}
            </Pie>
            <Tooltip {...tooltipStyle} />
            <Legend
              style={{ color: "#a1a1aa", fontSize: 13 }}
              formatter={(value: string) => <span style={{ color: "#a1a1aa" }}>{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Bar: score histogram */}
      <div>
        <p className="text-white/60 text-sm text-center mb-4 uppercase tracking-wider">
          Score Distribution
        </p>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data.score_histogram} margin={{ left: -10, right: 10, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
            <XAxis
              dataKey="range"
              tick={{ fill: "#94a3b8", fontSize: 10 }}
              angle={-45}
              textAnchor="end"
              interval={1}
            />
            <YAxis tick={{ fill: "#94a3b8", fontSize: 11 }} allowDecimals={false} />
            <Tooltip {...tooltipStyle} />
            <Bar dataKey="count" fill="#38bdf8" radius={[4, 4, 0, 0]} name="Reviews" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
