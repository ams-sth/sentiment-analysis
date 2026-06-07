interface Props {
  percent: number;
  message: string;
}

export default function ProgressBar({ percent, message }: Props) {
  return (
    <div className="w-full space-y-2">
      <div className="flex items-center justify-between gap-3 text-sm">
        <span className="text-white/55 truncate">{message}</span>
        <span className="text-purple-300 font-mono tabular-nums shrink-0">{percent}%</span>
      </div>
      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full bg-gradient-to-r from-sky-500 to-cyan-400 transition-all duration-300 ease-out"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
