"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { InterviewEvaluation, getInterviewEvaluation, getSkillGapReport } from "@/lib/api";

// ─── Circular Score Ring ───
function ScoreRing({ score, maxScore = 10, size = 180, delay = 0.3 }: {
  score: number; maxScore?: number; size?: number; delay?: number;
}) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const radius = (size - 16) / 2;
  const circumference = 2 * Math.PI * radius;
  const pct = score / maxScore;
  const offset = circumference * (1 - pct);

  const color = score >= 7 ? "#10b981" : score >= 5 ? "#f59e0b" : "#ef4444";
  const bgGlow = score >= 7 ? "rgba(16, 185, 129, 0.15)" : score >= 5 ? "rgba(245, 158, 11, 0.15)" : "rgba(239, 68, 68, 0.15)";

  useEffect(() => {
    const timer = setTimeout(() => {
      const duration = 1500;
      const start = performance.now();
      const animate = (now: number) => {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        setAnimatedScore(score * eased);
        if (progress < 1) requestAnimationFrame(animate);
      };
      requestAnimationFrame(animate);
    }, delay * 1000);
    return () => clearTimeout(timer);
  }, [score, delay]);

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <div
        className="absolute inset-0 rounded-full blur-2xl opacity-50"
        style={{ background: bgGlow }}
      />
      <svg width={size} height={size} className="score-ring relative">
        <circle className="score-ring-track" cx={size / 2} cy={size / 2} r={radius} />
        <motion.circle
          className="score-ring-fill"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.5, delay, ease: [0.22, 1, 0.36, 1] }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-5xl font-bold" style={{ color }}>
          {animatedScore.toFixed(1)}
        </span>
        <span className="text-sm text-ca-fg-muted">/10</span>
      </div>
    </div>
  );
}

// ─── Animated Score Bar ───
function ScoreBar({ label, score, maxScore = 10, delay = 0 }: {
  label: string; score: number; maxScore?: number; delay?: number;
}) {
  const pct = (score / maxScore) * 100;
  const color = score >= 7 ? "from-emerald-400 to-emerald-500" : score >= 5 ? "from-amber-400 to-amber-500" : "from-red-400 to-red-500";

  return (
    <div className="flex items-center gap-3">
      <div className="w-40 text-sm text-ca-fg-secondary truncate">{label}</div>
      <div className="flex-1 h-2.5 bg-ca-bg-secondary rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full bg-gradient-to-r ${color}`}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.8, delay: 0.5 + delay * 0.1, ease: [0.22, 1, 0.36, 1] }}
        />
      </div>
      <div className="w-12 text-right text-sm font-semibold">{score.toFixed(1)}</div>
    </div>
  );
}

// ─── Skeleton Loader ───
function ResultsSkeleton() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      <div className="text-center mb-8">
        <div className="skeleton skeleton-text w-48 mx-auto h-7 mb-3" />
        <div className="skeleton skeleton-text w-80 mx-auto" />
      </div>
      <div className="flex justify-center mb-8">
        <div className="skeleton skeleton-avatar w-44 h-44" />
      </div>
      <div className="skeleton-card">
        <div className="space-y-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="flex items-center gap-3">
              <div className="skeleton skeleton-text w-32" />
              <div className="skeleton flex-1 h-2.5 rounded-full" />
              <div className="skeleton skeleton-text w-10" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function ResultsPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [evaluation, setEvaluation] = useState<InterviewEvaluation | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"overview" | "panelists" | "actions" | "gaps">("overview");
  const [skillGap, setSkillGap] = useState<Awaited<ReturnType<typeof getSkillGapReport>> | null>(null);
  const [gapLoading, setGapLoading] = useState(false);

  useEffect(() => {
    const stored = sessionStorage.getItem(`evaluation_${id}`);
    if (stored) {
      setEvaluation(JSON.parse(stored));
      setLoading(false);
      sessionStorage.removeItem(`evaluation_${id}`);
      return;
    }

    getInterviewEvaluation(id)
      .then((data) => setEvaluation(data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <ResultsSkeleton />;

  if (!evaluation) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-20 text-center">
        <div className="w-16 h-16 rounded-full bg-ca-bg-secondary flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-ca-fg-muted" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
          </svg>
        </div>
        <p className="text-ca-fg-muted mb-4">No evaluation found for this interview.</p>
        <button onClick={() => router.push("/screening")} className="ca-btn ca-btn-primary inline-flex">Start New Interview</button>
      </div>
    );
  }

  const getVerdict = (score: number) => {
    if (score >= 8) return { text: "Excellent", desc: "You demonstrated strong skills across the board", tip: "Keep practicing to maintain your edge. Focus on perfecting your weaker dimensions." };
    if (score >= 7) return { text: "Good", desc: "Solid performance with room to grow", tip: "You're close to excellent. Review the action items below to level up." };
    if (score >= 5) return { text: "Getting There", desc: "You have a good foundation to build on", tip: "Focus on the high-priority action items. A few more practice sessions can make a big difference." };
    return { text: "Keep Practicing", desc: "Every expert was once a beginner", tip: "Don't be discouraged — this is practice. Work through the action items and try again. You'll see improvement quickly." };
  };

  const verdict = getVerdict(evaluation.overall);

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-6"
      >
        <h1 className="text-2xl font-bold mb-2">Interview Evaluation</h1>
        <p className="text-ca-fg-secondary max-w-xl mx-auto">{evaluation.summary}</p>
        <p className="text-xs text-ca-fg-muted mt-2 max-w-md mx-auto">
          This is AI-generated feedback to help you improve. Practice multiple times to track your progress.
        </p>
      </motion.div>

      {/* Score Ring */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1, duration: 0.5 }}
        className="flex flex-col items-center mb-8"
      >
        <ScoreRing score={evaluation.overall} />
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.8 }}
          className="mt-4 text-center"
        >
          <div className="text-lg font-semibold">{verdict.text}</div>
          <div className="text-sm text-ca-fg-muted">{verdict.desc}</div>
          <div className="text-xs text-ca-fg-muted mt-2 max-w-sm mx-auto leading-relaxed">
            {verdict.tip}
          </div>
        </motion.div>
      </motion.div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 border-b border-ca-border overflow-x-auto">
        {(["overview", "panelists", "actions", "gaps"] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => {
              setActiveTab(tab);
              if (tab === "gaps" && !skillGap && !gapLoading) {
                setGapLoading(true);
                getSkillGapReport(id)
                  .then(setSkillGap)
                  .catch(console.error)
                  .finally(() => setGapLoading(false));
              }
            }}
            className={`relative px-5 py-2.5 text-sm font-medium transition-colors whitespace-nowrap ${
              activeTab === tab
                ? "text-ca-fg"
                : "text-ca-fg-muted hover:text-ca-fg"
            }`}
          >
            {tab === "overview" ? "Score Breakdown" : tab === "panelists" ? "Panelist Feedback" : tab === "actions" ? "Action Items" : "Skill Gaps"}
            {activeTab === tab && (
              <motion.div
                layoutId="tab-indicator"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-ca-accent rounded-full"
              />
            )}
          </button>
        ))}
      </div>

      {/* Overview Tab */}
      {activeTab === "overview" && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass-card rounded-xl p-6 space-y-4"
        >
          {Object.entries(evaluation.dimensions).map(([dim, score], i) => (
            <ScoreBar
              key={dim}
              label={dim.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
              score={score}
              delay={i}
            />
          ))}
        </motion.div>
      )}

      {/* Panelists Tab */}
      {activeTab === "panelists" && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-6"
        >
          {Object.entries(evaluation.by_evaluator).map(([name, ev], i) => (
            <motion.div
              key={name}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="glass-card rounded-xl p-6"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-11 h-11 rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center text-white font-bold shadow-sm">
                  {name.charAt(0)}
                </div>
                <div>
                  <h3 className="font-semibold">{name}</h3>
                  <p className="text-sm text-ca-fg-muted">{ev.role}</p>
                </div>
                <div className="ml-auto">
                  <span
                    className={`ca-badge ${
                      ev.recommendation?.toLowerCase().includes("hire")
                        ? "ca-badge-success"
                        : ev.recommendation?.toLowerCase().includes("pass")
                        ? "ca-badge-danger"
                        : "ca-badge-warning"
                    }`}
                  >
                    {ev.recommendation || "Pending"}
                  </span>
                </div>
              </div>

              <p className="text-sm text-ca-fg-secondary mb-4 leading-relaxed">{ev.overall_impression}</p>

              {ev.key_observations && ev.key_observations.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-xs font-semibold text-ca-fg-muted uppercase tracking-wider">Key Observations</h4>
                  <ul className="space-y-1.5">
                    {ev.key_observations.map((obs, i) => (
                      <li key={i} className="text-sm text-ca-fg-secondary flex gap-2">
                        <span className="text-ca-accent mt-0.5 flex-shrink-0">
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                          </svg>
                        </span>
                        <span>{obs}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {ev.scores && Object.keys(ev.scores).length > 0 && (
                <div className="mt-4 pt-4 border-t border-ca-border/50 space-y-2">
                  <h4 className="text-xs font-semibold text-ca-fg-muted uppercase tracking-wider">Scores</h4>
                  {Object.entries(ev.scores).map(([dim, scoreData]) => (
                    <div key={dim} className="text-sm">
                      <div className="flex justify-between">
                        <span className="text-ca-fg-secondary">
                          {dim.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                        </span>
                        <span className="font-medium">
                          {typeof scoreData === "object" ? scoreData.score : scoreData}/10
                        </span>
                      </div>
                      {typeof scoreData === "object" && scoreData.feedback && (
                        <p className="text-xs text-ca-fg-muted mt-0.5">{scoreData.feedback}</p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Action Items Tab */}
      {activeTab === "actions" && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-4"
        >
          {evaluation.action_items && evaluation.action_items.length > 0 ? (
            evaluation.action_items.map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.08 }}
                className="glass-card rounded-xl p-5"
              >
                <div className="flex items-start gap-3">
                  <div
                    className={`w-7 h-7 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0 ${
                      item.priority === "high"
                        ? "bg-gradient-to-br from-red-400 to-red-500"
                        : item.priority === "medium"
                        ? "bg-gradient-to-br from-amber-400 to-amber-500"
                        : "bg-gradient-to-br from-emerald-400 to-emerald-500"
                    }`}
                  >
                    {i + 1}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-medium text-sm">{item.recommendation}</span>
                      <span className="ca-badge ca-badge-accent text-xs">
                        {item.area?.replace(/_/g, " ")}
                      </span>
                    </div>
                    {item.practice_tip && (
                      <p className="text-sm text-ca-fg-secondary leading-relaxed">{item.practice_tip}</p>
                    )}
                  </div>
                </div>
              </motion.div>
            ))
          ) : (
            <div className="text-center py-12">
              <div className="w-12 h-12 rounded-full bg-ca-bg-secondary flex items-center justify-center mx-auto mb-3">
                <svg className="w-6 h-6 text-ca-fg-muted" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                </svg>
              </div>
              <p className="text-ca-fg-muted">No specific action items generated.</p>
            </div>
          )}
        </motion.div>
      )}

      {/* Skill Gaps Tab */}
      {activeTab === "gaps" && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
          {gapLoading ? (
            <div className="text-center py-12">
              <div className="ca-spinner mx-auto mb-3" />
              <p className="text-ca-fg-muted text-sm">Analyzing skill gaps...</p>
            </div>
          ) : skillGap ? (
            <>
              {/* Readiness meter */}
              <div className="glass-card rounded-xl p-6 text-center">
                <h3 className="text-sm font-semibold text-ca-fg-muted uppercase tracking-wider mb-3">
                  Interview Readiness
                  {skillGap.target_company && ` for ${skillGap.target_company}`}
                </h3>
                <div className="text-4xl font-bold mb-2" style={{
                  color: skillGap.readiness_pct >= 70 ? "#10b981" : skillGap.readiness_pct >= 40 ? "#f59e0b" : "#ef4444"
                }}>
                  {skillGap.readiness_pct}%
                </div>
                <p className="text-sm text-ca-fg-secondary max-w-md mx-auto">{skillGap.overall_assessment}</p>
              </div>

              {/* Top Priorities */}
              {skillGap.top_priorities && skillGap.top_priorities.length > 0 && (
                <div className="glass-card rounded-xl p-6">
                  <h3 className="text-sm font-semibold text-ca-fg-muted uppercase tracking-wider mb-4">Top Priorities</h3>
                  <div className="space-y-3">
                    {skillGap.top_priorities.map((p, i) => (
                      <div key={i} className="flex items-start gap-3">
                        <div className="w-7 h-7 rounded-full bg-gradient-to-br from-red-400 to-red-500 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
                          {i + 1}
                        </div>
                        <div>
                          <span className="font-medium text-sm">{p.area?.replace(/_/g, " ").replace(/\b\w/g, (c: string) => c.toUpperCase())}</span>
                          <p className="text-sm text-ca-fg-secondary">{p.action}</p>
                          <p className="text-xs text-ca-fg-muted mt-0.5">{p.expected_improvement}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Gap Details */}
              {skillGap.gaps && skillGap.gaps.length > 0 && (
                <div className="glass-card rounded-xl p-6">
                  <h3 className="text-sm font-semibold text-ca-fg-muted uppercase tracking-wider mb-4">Dimension-by-Dimension</h3>
                  <div className="space-y-4">
                    {skillGap.gaps.map((g, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 8 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.05 }}
                        className={`p-4 rounded-lg border ${
                          g.severity === "critical_gap"
                            ? "border-red-500/30 bg-red-500/5"
                            : g.severity === "needs_work"
                            ? "border-amber-500/30 bg-amber-500/5"
                            : "border-emerald-500/30 bg-emerald-500/5"
                        }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium text-sm">
                            {g.dimension.replace(/_/g, " ").replace(/\b\w/g, (c: string) => c.toUpperCase())}
                          </span>
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-semibold">{g.current_score}/10</span>
                            <span className={`ca-badge text-xs ${
                              g.severity === "critical_gap" ? "ca-badge-danger" : g.severity === "needs_work" ? "ca-badge-warning" : "ca-badge-success"
                            }`}>
                              {g.severity === "critical_gap" ? "Critical" : g.severity === "needs_work" ? "Needs Work" : "Ready"}
                            </span>
                          </div>
                        </div>
                        <p className="text-sm text-ca-fg-secondary">{g.gap_description}</p>
                        {g.improvement_plan && g.severity !== "ready" && (
                          <div className="mt-2 pt-2 border-t border-ca-border/50">
                            <p className="text-xs text-ca-fg-muted font-medium uppercase mb-1">Improvement Plan</p>
                            <p className="text-sm text-ca-fg-secondary">{g.improvement_plan}</p>
                          </div>
                        )}
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-12">
              <p className="text-ca-fg-muted">Unable to load skill gap report.</p>
            </div>
          )}
        </motion.div>
      )}

      {/* Bottom CTA */}
      <div className="flex flex-col sm:flex-row justify-center gap-3 mt-10 pt-6 border-t border-ca-border">
        <button onClick={() => router.push("/screening")} className="ca-btn ca-btn-primary py-2.5 px-6 shadow-sm shadow-indigo-500/15">
          Try Another Interview
        </button>
        <button
          onClick={() => {
            if (typeof window !== "undefined" && navigator.clipboard) {
              navigator.clipboard.writeText(window.location.href);
            }
          }}
          className="ca-btn ca-btn-secondary py-2.5 px-6"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M7.217 10.907a2.25 2.25 0 1 0 0 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186 9.566-5.314m-9.566 7.5 9.566 5.314m0 0a2.25 2.25 0 1 0 3.935 2.186 2.25 2.25 0 0 0-3.935-2.186Zm0-12.814a2.25 2.25 0 1 0 3.933-2.185 2.25 2.25 0 0 0-3.933 2.185Z" />
          </svg>
          Share Results
        </button>
        <button onClick={() => router.push("/")} className="ca-btn ca-btn-secondary py-2.5 px-6">
          Back to Home
        </button>
      </div>
    </div>
  );
}
