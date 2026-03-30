interface Props {
  agentType: string;
  agentName: string;
  isAdversarial?: boolean;
}

const TYPE_STYLES: Record<string, { bg: string; icon: string }> = {
  lead: { bg: "bg-violet-500/10 text-violet-300 border-violet-500/20", icon: "🐙" },
  sub: { bg: "bg-cyan-500/8 text-cyan-300 border-cyan-500/15", icon: "🦑" },
  contrarian: { bg: "bg-orange-500/10 text-orange-300 border-orange-500/20", icon: "🛡️" },
  orchestrator: { bg: "bg-violet-500/15 text-violet-200 border-violet-500/25", icon: "🧠" },
};

export default function AgentBadge({ agentType, agentName, isAdversarial }: Props) {
  const effectiveType = isAdversarial ? "contrarian" : agentType;
  const style = TYPE_STYLES[effectiveType] || TYPE_STYLES.lead;

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${style.bg}`}>
      <span className="text-[10px]">{style.icon}</span>
      {agentName}
    </span>
  );
}
