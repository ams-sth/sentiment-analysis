export default function Spinner({ size = "md" }: { size?: "sm" | "md" }) {
  const cls = size === "sm" ? "w-4 h-4 border-2" : "w-8 h-8 border-4";
  return (
    <span
      className={`inline-block ${cls} border-white/30 border-t-white rounded-full animate-spin`}
    />
  );
}
