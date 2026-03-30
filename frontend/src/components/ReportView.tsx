"use client";

import { useState } from "react";
import type { Report } from "@/lib/api";
import ConfidenceMeter from "./ConfidenceMeter";

interface Props {
  report: Report;
}

const SECTION_ICONS = ["🔍", "🎯", "📊", "💰", "🏢", "🚀", "⚖️", "🧬", "🛡️", "🌊"];

export default function ReportView({ report }: Props) {
  const [expandedSections, setExpandedSections] = useState<Set<number>>(
    new Set(report.sections.map((_, i) => i))
  );

  function toggleSection(index: number) {
    setExpandedSections((prev) => {
      const next = new Set(prev);
      if (next.has(index)) next.delete(index);
      else next.add(index);
      return next;
    });
  }

  return (
    <div className="space-y-6 animate-slide-up">
      {/* Executive summary — the brain's synthesis */}
      <div className="octopus-card p-6 md:p-8 bg-gradient-to-br from-violet-500/8 to-cyan-500/5 border-violet-500/15">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-2xl">🧠</span>
          <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-violet-300">Octopus Brain Synthesis</p>
        </div>
        <h2 className="text-xl md:text-2xl font-bold tracking-tight text-[var(--foreground)] mb-4">{report.title}</h2>
        <p className="text-sm md:text-base text-[var(--foreground-subtle)] leading-relaxed">{report.executive_summary}</p>
      </div>

      {/* Report sections — each arm's findings */}
      {report.sections.map((section, i) => (
        <div key={i} className="octopus-card overflow-hidden" style={{ animationDelay: `${i * 50}ms` }}>
          <button
            type="button"
            onClick={() => toggleSection(i)}
            className="w-full px-5 md:px-6 py-4 md:py-5 flex items-center justify-between gap-4 text-left hover:bg-violet-500/3 transition-colors"
          >
            <div className="flex items-center gap-3 min-w-0">
              <span className="text-lg shrink-0">{SECTION_ICONS[i % SECTION_ICONS.length]}</span>
              <div className="min-w-0">
                <h3 className="font-semibold text-base md:text-lg text-[var(--foreground)] tracking-tight truncate">
                  {section.heading}
                </h3>
              </div>
            </div>
            <div className="flex items-center gap-3 shrink-0">
              <ConfidenceMeter value={section.confidence} size="md" />
              <span className="text-violet-300/40 text-lg">{expandedSections.has(i) ? "▾" : "▸"}</span>
            </div>
          </button>

          {expandedSections.has(i) && (
            <div className="px-5 md:px-6 pb-6 border-t border-violet-500/10 pt-5 space-y-5">
              <p className="text-sm md:text-[15px] leading-[1.75] text-[var(--foreground-subtle)] whitespace-pre-wrap">
                {section.content}
              </p>

              {section.key_insights.length > 0 && (
                <div className="rounded-[var(--radius-md)] bg-cyan-500/5 border border-cyan-500/10 p-4">
                  <h4 className="text-[11px] font-semibold uppercase tracking-[0.18em] text-cyan-300 mb-3 flex items-center gap-2">
                    <span>💡</span> Key Insights
                  </h4>
                  <ul className="space-y-2.5">
                    {section.key_insights.map((insight, j) => (
                      <li key={j} className="text-sm flex gap-3 text-[var(--foreground-subtle)]">
                        <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 mt-2 shrink-0" aria-hidden />
                        <span>{insight}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {section.recommendations.length > 0 && (
                <div className="rounded-[var(--radius-md)] bg-violet-500/5 border border-violet-500/10 p-4">
                  <h4 className="text-[11px] font-semibold uppercase tracking-[0.18em] text-violet-300 mb-3 flex items-center gap-2">
                    <span>🎯</span> Recommendations
                  </h4>
                  <ul className="space-y-2.5">
                    {section.recommendations.map((rec, j) => (
                      <li key={j} className="text-sm flex gap-3 text-[var(--foreground-subtle)]">
                        <span className="text-violet-400 mt-0.5 shrink-0 font-mono">→</span>
                        <span>{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {section.caveats.length > 0 && (
                <div className="rounded-[var(--radius-md)] bg-amber-500/5 border border-amber-500/10 p-4">
                  <h4 className="text-[11px] font-semibold uppercase tracking-[0.18em] text-amber-300 mb-3 flex items-center gap-2">
                    <span>⚠️</span> Caveats
                  </h4>
                  <ul className="space-y-2.5">
                    {section.caveats.map((c, j) => (
                      <li key={j} className="text-sm flex gap-3 text-amber-200/80">
                        <span className="mt-0.5 shrink-0">•</span>
                        <span>{c}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      ))}

      {/* Key Recommendations — the brain's verdict */}
      {report.key_recommendations.length > 0 && (
        <div className="octopus-card p-6 md:p-8 border-cyan-500/20 bg-gradient-to-br from-cyan-500/8 to-violet-500/5">
          <div className="flex items-center gap-2 mb-5">
            <span className="text-xl">🐙</span>
            <h3 className="font-bold text-lg text-cyan-200 tracking-tight">The Octopus Recommends</h3>
          </div>
          <ol className="space-y-4">
            {report.key_recommendations.map((rec, i) => (
              <li key={i} className="text-sm md:text-[15px] flex gap-4 text-[var(--foreground-subtle)]">
                <span className="w-7 h-7 rounded-full bg-cyan-500/15 border border-cyan-500/25 flex items-center justify-center text-cyan-300 font-mono font-bold text-xs shrink-0 mt-0.5">
                  {i + 1}
                </span>
                <span className="leading-relaxed">{rec}</span>
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* Risk factors */}
      {report.risk_factors.length > 0 && (
        <div className="octopus-card p-6 md:p-8 border-orange-500/15 bg-gradient-to-br from-orange-500/5 to-red-500/3">
          <div className="flex items-center gap-2 mb-5">
            <span className="text-xl">🛡️</span>
            <h3 className="font-bold text-lg text-orange-300 tracking-tight">Risk Factors</h3>
          </div>
          <ul className="space-y-3">
            {report.risk_factors.map((risk, i) => (
              <li key={i} className="text-sm flex gap-3 text-orange-100/70">
                <span className="text-orange-400 font-bold shrink-0 mt-0.5">!</span>
                <span>{risk}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Next steps */}
      {report.next_steps.length > 0 && (
        <div className="octopus-card p-6 md:p-8 border-green-500/15 bg-gradient-to-br from-green-500/5 to-cyan-500/3">
          <div className="flex items-center gap-2 mb-5">
            <span className="text-xl">🚀</span>
            <h3 className="font-bold text-lg text-green-300 tracking-tight">Next Steps</h3>
          </div>
          <ul className="space-y-3">
            {report.next_steps.map((step, i) => (
              <li key={i} className="text-sm flex gap-3 text-[var(--foreground-subtle)]">
                <span className="text-green-400 shrink-0 mt-0.5">→</span>
                <span>{step}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {report.data_quality_note && (
        <p className="text-xs text-violet-300/30 text-center italic px-4 leading-relaxed">{report.data_quality_note}</p>
      )}
    </div>
  );
}
