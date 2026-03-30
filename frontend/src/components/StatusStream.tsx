"use client";

import { useEffect, useState, useRef } from "react";
import { getSessionLogs, type SessionLog } from "@/lib/api";

interface Props {
  sessionId: string;
  status: string;
}

function categorizeLog(msg: string): { icon: string; color: string } {
  if (msg.includes("investigating")) return { icon: "🦑", color: "text-cyan-300/80" };
  if (msg.includes("posted")) return { icon: "📡", color: "text-green-300/80" };
  if (msg.includes("commented")) return { icon: "💬", color: "text-amber-300/80" };
  if (msg.includes("ADVERSARIAL")) return { icon: "🛡️", color: "text-orange-300" };
  if (msg.includes("DIRECTIVE")) return { icon: "🐙", color: "text-violet-300" };
  if (msg.includes("Convergence")) return { icon: "🧠", color: "text-cyan-300" };
  if (msg.includes("Cycle")) return { icon: "🔄", color: "text-violet-300/80" };
  if (msg.includes("→") && (msg.includes("OK") || msg.includes("FAIL")))
    return { icon: msg.includes("FAIL") ? "❌" : "✅", color: msg.includes("FAIL") ? "text-red-300" : "text-green-300" };
  if (msg.includes("Pipeline complete") || msg.includes("Simulation complete"))
    return { icon: "✨", color: "text-green-300" };
  if (msg.includes("Initial Sweep") || msg.includes("===")) return { icon: "🌊", color: "text-cyan-300" };
  return { icon: "·", color: "text-violet-300/40" };
}

export default function StatusStream({ sessionId, status }: Props) {
  const [logs, setLogs] = useState<SessionLog[]>([]);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (status !== "running") return;

    const poll = setInterval(async () => {
      try {
        const data = await getSessionLogs(sessionId);
        setLogs(data.logs || []);
      } catch {
        /* ignore */
      }
    }, 1500);

    return () => clearInterval(poll);
  }, [sessionId, status]);

  useEffect(() => {
    const container = scrollContainerRef.current;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }, [logs]);

  if (logs.length === 0) return null;

  return (
    <div className="mt-5 border-t border-violet-500/10 pt-4">
      <details className="group" open>
        <summary className="text-xs font-medium text-violet-300/50 cursor-pointer list-none flex items-center gap-2 hover:text-cyan-300/70 transition-colors">
          <span className="text-cyan-400/60 transition-transform duration-200 group-open:rotate-90" aria-hidden>▸</span>
          🐙 Tentacle Activity Log
          <span className="text-[10px] font-mono opacity-50">({logs.length})</span>
        </summary>
        <div
          ref={scrollContainerRef}
          className="mt-3 max-h-56 overflow-y-auto rounded-[var(--radius-md)] border border-violet-500/10 bg-[#020810]/80 p-3 space-y-1 font-mono text-[11px] leading-relaxed"
        >
          {logs.map((log, i) => {
            const { icon, color } = categorizeLog(log.msg);
            return (
              <div key={i} className={`${color} flex gap-2 animate-fade-in`}>
                <span className="shrink-0 w-5 text-center select-none">{icon}</span>
                <span className="text-[var(--foreground-subtle)]/80">{log.msg}</span>
              </div>
            );
          })}
        </div>
      </details>
    </div>
  );
}
