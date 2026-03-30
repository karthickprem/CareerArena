"use client";

import { useState, useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import type { MultiRoundStartResponse, InterviewPanelist, RoundConfig } from "@/lib/api";

export default function PanelRevealPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.id as string;

  const [panel, setPanel] = useState<InterviewPanelist[]>([]);
  const [roundPlan, setRoundPlan] = useState<RoundConfig[]>([]);
  const [revealedCount, setRevealedCount] = useState(0);
  const [allRevealed, setAllRevealed] = useState(false);

  const revealIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem(`panel_${sessionId}`);
    if (stored) {
      const data: MultiRoundStartResponse = JSON.parse(stored);
      setPanel(data.panel);
      setRoundPlan(data.round_plan.rounds);

      let count = 0;
      const interval = setInterval(() => {
        count++;
        setRevealedCount(count);
        if (count >= data.panel.length) {
          clearInterval(interval);
          setTimeout(() => setAllRevealed(true), 800);
        }
      }, 1000);
      revealIntervalRef.current = interval;

      return () => clearInterval(interval);
    }
  }, [sessionId]);

  const handleSkipReveal = () => {
    if (revealIntervalRef.current) {
      clearInterval(revealIntervalRef.current);
      revealIntervalRef.current = null;
    }
    setRevealedCount(panel.length);
    setAllRevealed(true);
  };

  const handleStartInterview = () => {
    router.push(`/interview/${sessionId}/round/1`);
  };

  return (
    <div className="min-h-screen bg-ca-bg flex flex-col items-center justify-center p-4 mesh-gradient">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-ca-border bg-ca-bg/50 text-xs text-ca-fg-muted mb-4">
          <span className="w-2 h-2 rounded-full bg-ca-accent animate-pulse" />
          Panel Generated
        </div>
        <h1 className="text-3xl font-bold text-ca-fg mb-2">
          Your Interview Panel
        </h1>
        <p className="text-ca-fg-secondary">
          {panel.length} interviewers, {roundPlan.length} rounds — each will
          interview you 1-on-1
        </p>
        {!allRevealed && panel.length > 0 && (
          <button
            onClick={handleSkipReveal}
            className="ca-btn ca-btn-ghost text-xs mt-2"
          >
            Skip animation
          </button>
        )}
      </motion.div>

      {/* Panel cards */}
      <div className="flex flex-wrap justify-center gap-8 mb-12 max-w-5xl">
        {panel.map((p, i) => {
          const round = roundPlan[i];
          const isRevealed = i < revealedCount;

          return (
            <AnimatePresence key={i}>
              {isRevealed && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.7, rotateY: 90 }}
                  animate={{ opacity: 1, scale: 1, rotateY: 0 }}
                  transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                  className="w-56"
                >
                  <div className="glass-card rounded-2xl p-6 text-center space-y-4 spotlight-glow card-glow">
                    {/* Avatar with glow */}
                    <div className="relative inline-block mx-auto">
                      <div
                        className="absolute inset-0 rounded-full blur-xl opacity-30"
                        style={{ backgroundColor: p.avatar_color || "#6366f1" }}
                      />
                      <div
                        className="relative w-20 h-20 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg"
                        style={{
                          background: `linear-gradient(135deg, ${p.avatar_color || "#6366f1"}, ${p.avatar_color || "#6366f1"}dd)`,
                        }}
                      >
                        {p.name
                          .split(" ")
                          .map((w) => w[0])
                          .join("")}
                      </div>
                    </div>

                    {/* Name & Role */}
                    <div>
                      <h3 className="font-semibold text-ca-fg">
                        {p.name}
                      </h3>
                      <p className="text-sm text-ca-fg-muted">{p.role}</p>
                    </div>

                    {/* Round info */}
                    {round && (
                      <div className="space-y-1.5">
                        <span className="inline-flex items-center gap-1.5 ca-badge ca-badge-accent text-xs">
                          Round {round.round_num}
                          {round.is_final ? " (Final)" : ""}
                        </span>
                        <p className="text-xs text-ca-fg-muted capitalize">
                          {round.round_type.replace("_", " ")}
                        </p>
                      </div>
                    )}

                    {/* Personality tag */}
                    {p.personality && (
                      <div className="pt-2 border-t border-ca-border/50">
                        <p className="text-xs text-ca-fg-muted capitalize">
                          {p.personality?.replace("_", " ")}
                        </p>
                      </div>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          );
        })}
      </div>

      {/* Round plan */}
      <AnimatePresence>
        {allRevealed && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className="max-w-2xl w-full space-y-6"
          >
            {/* Round timeline */}
            <div className="glass-card rounded-2xl p-6">
              <h2 className="text-sm font-semibold text-ca-fg mb-5 flex items-center gap-2">
                <svg className="w-4 h-4 text-ca-accent" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 0 1 0 3.75H5.625a1.875 1.875 0 0 1 0-3.75Z" />
                </svg>
                Interview Plan
              </h2>
              <div className="space-y-4">
                {roundPlan.map((round, i) => {
                  const interviewer = panel.find(
                    (p) => p.name === round.interviewer_name
                  );
                  return (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.15 }}
                      className="flex items-center gap-4"
                    >
                      <div
                        className="w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0 shadow-sm"
                        style={{
                          background: `linear-gradient(135deg, ${interviewer?.avatar_color || "#6366f1"}, ${interviewer?.avatar_color || "#6366f1"}cc)`,
                        }}
                      >
                        {round.round_num}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-ca-fg">
                          {round.interviewer_name}{" "}
                          <span className="text-ca-fg-muted font-normal">
                            ({round.interviewer_role})
                          </span>
                        </p>
                        <p className="text-xs text-ca-fg-muted">
                          {round.focus_areas.join(", ")}
                        </p>
                      </div>
                      <span className="text-xs text-ca-fg-muted whitespace-nowrap">
                        ~{round.max_questions} Qs
                      </span>
                    </motion.div>
                  );
                })}
              </div>
            </div>

            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              onClick={handleStartInterview}
              className="ca-btn ca-btn-primary w-full py-3.5 text-base shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/30 transition-shadow"
            >
              Start Round 1
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
              </svg>
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
