"use client";

import { useState, useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  getInterviewForum,
  evaluateInterview,
  type ForumRound,
  type MultiRoundStartResponse,
  type InterviewPanelist,
} from "@/lib/api";

export default function ForumRevealPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.id as string;

  const [forumRounds, setForumRounds] = useState<ForumRound[]>([]);
  const [panel, setPanel] = useState<InterviewPanelist[]>([]);
  const [revealedRound, setRevealedRound] = useState(0);
  const [allRevealed, setAllRevealed] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isEvaluating, setIsEvaluating] = useState(false);

  useEffect(() => {
    const load = async () => {
      // Get panel info
      const panelStored = sessionStorage.getItem(`panel_${sessionId}`);
      if (panelStored) {
        const data: MultiRoundStartResponse = JSON.parse(panelStored);
        setPanel(data.panel);
      }

      // Try API first, fall back to sessionStorage
      try {
        const result = await getInterviewForum(sessionId);
        setForumRounds(result.rounds);
      } catch {
        const stored = sessionStorage.getItem(`forum_${sessionId}`);
        if (stored) {
          setForumRounds(JSON.parse(stored));
        }
      }

      setIsLoading(false);

      // Progressive reveal
      let round = 0;
      const interval = setInterval(() => {
        round++;
        setRevealedRound(round);
      }, 1500);
      revealIntervalRef.current = interval;

      return () => clearInterval(interval);
    };

    load();
  }, [sessionId]);

  const revealIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const handleRevealAll = () => {
    if (revealIntervalRef.current) {
      clearInterval(revealIntervalRef.current);
      revealIntervalRef.current = null;
    }
    setRevealedRound(forumRounds.length + 1);
    setAllRevealed(true);
  };

  const getColor = (name: string) => {
    const p = panel.find((p) => p.name === name);
    return p?.avatar_color || "#6366f1";
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "positive": return "border-l-green-500";
      case "negative": return "border-l-red-500";
      case "mixed": return "border-l-amber-500";
      default: return "border-l-gray-300";
    }
  };

  const getPostTypeLabel = (type: string) => {
    switch (type) {
      case "concern": return { label: "Concern", color: "bg-red-100 text-red-700" };
      case "praise": return { label: "Praise", color: "bg-green-100 text-green-700" };
      case "question": return { label: "Question", color: "bg-blue-100 text-blue-700" };
      case "strategy": return { label: "Strategy", color: "bg-purple-100 text-purple-700" };
      default: return { label: "Observation", color: "bg-gray-100 text-gray-700" };
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-ca-bg">
        <div className="border-b border-ca-border bg-ca-bg/80 backdrop-blur-xl sticky top-0 z-10">
          <div className="max-w-3xl mx-auto px-4 py-4 text-center">
            <div className="skeleton skeleton-text w-48 mx-auto h-6 mb-2" />
            <div className="skeleton skeleton-text w-72 mx-auto h-4" />
          </div>
        </div>
        <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="skeleton-card space-y-3">
              <div className="flex items-center gap-3">
                <div className="skeleton skeleton-avatar w-10 h-10" />
                <div className="skeleton skeleton-text w-32 h-4" />
              </div>
              <div className="skeleton skeleton-text w-full" />
              <div className="skeleton skeleton-text w-3/4" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-ca-bg">
      {/* Header */}
      <div className="border-b border-ca-border bg-ca-bg/80 backdrop-blur-xl sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-4 py-4 text-center">
          <h1 className="text-xl font-bold text-ca-fg">
            Behind the Scenes
          </h1>
          <p className="text-sm text-ca-fg-muted mt-1">
            What your interviewers said about you when you weren&apos;t listening
          </p>
          {!allRevealed && forumRounds.length > 0 && (
            <button
              onClick={handleRevealAll}
              className="ca-btn ca-btn-ghost text-xs mt-2"
            >
              Reveal All
            </button>
          )}
        </div>
      </div>

      {/* Forum timeline */}
      <div className="max-w-3xl mx-auto px-4 py-8">
        {forumRounds.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-ca-fg-muted">No forum posts yet.</p>
          </div>
        ) : (
          <div className="space-y-10">
            {forumRounds.map((round, ri) => {
              const isRevealed = ri < revealedRound;
              return (
                <motion.div
                  key={ri}
                  initial={{ opacity: 0, y: 20 }}
                  animate={isRevealed ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
                  transition={{ duration: 0.5 }}
                >
                  {/* Round marker */}
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-full bg-ca-accent flex items-center justify-center text-white font-bold text-sm">
                      R{round.round_num}
                    </div>
                    <div>
                      <h2 className="text-sm font-semibold text-ca-fg">
                        After Round {round.round_num}
                      </h2>
                      <p className="text-xs text-ca-fg-muted">
                        {round.posts?.length || 0} posts from the panel
                      </p>
                    </div>
                    <div className="flex-1 h-px bg-ca-border" />
                  </div>

                  {/* Posts */}
                  <div className="space-y-4 ml-5 border-l-2 border-ca-border pl-6">
                    {(round.posts || []).map((post, pi) => {
                      const agentName = post.agent_name || (post as any).agent_name;
                      const content = post.content || (post as any).content;
                      const postType = (post as any).post_type || "observation";
                      const sentiment = (post as any).sentiment || "neutral";
                      const typeInfo = getPostTypeLabel(postType);
                      const comments = (post as any).comments || (post as any).replies || [];

                      return (
                        <motion.div
                          key={pi}
                          initial={{ opacity: 0, x: -10 }}
                          animate={isRevealed ? { opacity: 1, x: 0 } : {}}
                          transition={{ delay: allRevealed ? 0 : pi * 0.3, duration: 0.3 }}
                          className={`ca-card border-l-4 ${getSentimentColor(sentiment)} p-4`}
                        >
                          {/* Post header */}
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                              <div
                                className="w-7 h-7 rounded-full flex items-center justify-center text-white text-xs font-bold"
                                style={{ backgroundColor: getColor(agentName) }}
                              >
                                {(agentName || "?")
                                  .split(" ")
                                  .map((w: string) => w[0])
                                  .join("")}
                              </div>
                              <div>
                                <span className="text-sm font-medium text-ca-fg">
                                  {agentName}
                                </span>
                                <span className="text-xs text-ca-fg-muted ml-1">
                                  ({(post as any).agent_type || (post as any).agent_role || ""})
                                </span>
                              </div>
                            </div>
                            <span className={`text-xs px-2 py-0.5 rounded-full ${typeInfo.color}`}>
                              {typeInfo.label}
                            </span>
                          </div>

                          {/* Post content */}
                          <p className="text-sm text-ca-fg leading-relaxed">
                            {content}
                          </p>

                          {/* Replies */}
                          {comments.length > 0 && (
                            <div className="mt-3 space-y-2 pl-4 border-l-2 border-ca-border/50">
                              {comments.map((reply: any, ci: number) => (
                                <div key={ci} className="text-sm">
                                  <span
                                    className="font-medium"
                                    style={{ color: getColor(reply.agent_name) }}
                                  >
                                    {reply.agent_name}
                                  </span>
                                  <span className="text-ca-fg-secondary ml-1">
                                    {reply.content}
                                  </span>
                                </div>
                              ))}
                            </div>
                          )}
                        </motion.div>
                      );
                    })}
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}

        {/* Actions */}
        <div className="mt-10 flex gap-3 justify-center">
          <button
            onClick={async () => {
              setIsEvaluating(true);
              try {
                const evaluation = await evaluateInterview(sessionId);
                sessionStorage.setItem(
                  `evaluation_${sessionId}`,
                  JSON.stringify(evaluation)
                );
                router.push(`/interview/${sessionId}/results`);
              } catch {
                // Evaluation may already exist — navigate anyway
                router.push(`/interview/${sessionId}/results`);
              }
            }}
            disabled={isEvaluating}
            className="ca-btn ca-btn-primary px-6 py-3"
          >
            {isEvaluating ? "Generating Scorecard..." : "View Scorecard"}
          </button>
          <button
            onClick={() => router.push("/screening")}
            className="ca-btn ca-btn-secondary px-6 py-3"
          >
            New Interview
          </button>
        </div>
      </div>
    </div>
  );
}
