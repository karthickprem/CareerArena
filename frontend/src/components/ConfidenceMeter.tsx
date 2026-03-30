interface Props {
  value: number | null;
  size?: "sm" | "md";
}

export default function ConfidenceMeter({ value, size = "sm" }: Props) {
  if (value === null || value === undefined) return null;
  const pct = Math.round(value * 100);
  const barClass =
    pct >= 80
      ? "bg-gradient-to-r from-cyan-400 to-green-300"
      : pct >= 60
      ? "bg-gradient-to-r from-violet-400 to-cyan-300"
      : "bg-gradient-to-r from-orange-400 to-amber-300";
  const w = size === "sm" ? "w-16" : "w-28";
  const h = size === "sm" ? "h-1.5" : "h-2";

  return (
    <div className="flex items-center gap-2" title={`Confidence: ${pct}%`}>
      <div className={`${w} ${h} rounded-full bg-violet-500/10 overflow-hidden ring-1 ring-violet-500/10`}>
        <div className={`h-full rounded-full ${barClass} transition-all duration-500 ease-out`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-[11px] font-mono text-violet-300/50 tabular-nums">{pct}%</span>
    </div>
  );
}
