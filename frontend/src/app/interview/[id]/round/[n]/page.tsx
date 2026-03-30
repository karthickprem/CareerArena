"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  startRound,
  submitRoundAnswer,
  endRound,
  type RoundStartResponse,
  type MultiRoundStartResponse,
  type InterviewPanelist,
  type RoundConfig,
} from "@/lib/api";
import { useTTS } from "@/hooks/useTTS";

interface Turn {
  speaker: string;
  role: string;
  content: string;
  type: "question" | "answer";
}

export default function RoundPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.id as string;
  const roundNum = parseInt(params.n as string);

  const [turns, setTurns] = useState<Turn[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<"loading" | "active" | "ending" | "transition">("loading");
  const [interviewer, setInterviewer] = useState<{ name: string; role: string; color: string }>({
    name: "", role: "", color: "#6366f1",
  });
  const [questionsAsked, setQuestionsAsked] = useState(0);
  const [maxQuestions, setMaxQuestions] = useState(8);
  const [totalRounds, setTotalRounds] = useState(3);
  const [roundType, setRoundType] = useState("");
  const [isFinal, setIsFinal] = useState(false);
  const [forumPosts, setForumPosts] = useState<
    { agent_name: string; agent_role: string; content: string; replies: { agent_name: string; content: string }[] }[]
  >([]);
  const [typingIndex, setTypingIndex] = useState<number | null>(null);

  const transcriptRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const tts = useTTS();

  // Load panel data and start round
  useEffect(() => {
    const init = async () => {
      // Get panel info from sessionStorage
      const panelStored = sessionStorage.getItem(`panel_${sessionId}`);
      if (panelStored) {
        const data: MultiRoundStartResponse = JSON.parse(panelStored);
        setTotalRounds(data.total_rounds);
        const round = data.round_plan.rounds.find((r) => r.round_num === roundNum);
        if (round) {
          const p = data.panel.find((p) => p.name === round.interviewer_name);
          setInterviewer({
            name: round.interviewer_name,
            role: round.interviewer_role,
            color: p?.avatar_color || "#6366f1",
          });
          setMaxQuestions(round.max_questions);
          setRoundType(round.round_type);
          setIsFinal(round.is_final);
        }
      }

      // Start the round via API
      try {
        const result: RoundStartResponse = await startRound(sessionId, roundNum);
        setInterviewer({
          name: result.interviewer_name,
          role: result.interviewer_role,
          color: interviewer.color,
        });
        setRoundType(result.round_type);
        setIsFinal(result.is_final);

        setTurns([{
          speaker: result.interviewer_name,
          role: result.interviewer_role,
          content: result.opening_message,
          type: "question",
        }]);
        setStatus("active");
        setQuestionsAsked(1);

        tts.speak(result.opening_message, result.interviewer_name);
      } catch (err) {
        console.error("Failed to start round:", err);
      }
    };

    init();
  }, [sessionId, roundNum]);

  // Auto-scroll
  useEffect(() => {
    if (transcriptRef.current) {
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
    }
  }, [turns]);

  const handleSubmit = useCallback(async () => {
    const text = input.trim();
    if (!text || isLoading || status !== "active") return;

    setInput("");
    setTurns((prev) => [...prev, {
      speaker: "You",
      role: "Candidate",
      content: text,
      type: "answer",
    }]);
    setIsLoading(true);

    try {
      const result = await submitRoundAnswer(sessionId, roundNum, text);
      setQuestionsAsked(result.questions_asked);

      if (result.is_round_complete) {
        // Round is done, trigger forum
        await handleEndRound();
      } else if (result.responses.length > 0) {
        const resp = result.responses[0];
        setTurns((prev) => [...prev, {
          speaker: resp.speaker,
          role: resp.role,
          content: resp.content,
          type: "question",
        }]);
        tts.speak(resp.content, resp.speaker);
      }
    } catch (err) {
      console.error("Answer submission error:", err);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  }, [input, isLoading, status, sessionId, roundNum, tts]);

  const handleEndRound = async () => {
    setStatus("ending");
    try {
      const result = await endRound(sessionId, roundNum);
      setForumPosts(result.forum_posts);
      setStatus("transition");

      // Store forum posts for the forum reveal page
      const existingForum = JSON.parse(
        sessionStorage.getItem(`forum_${sessionId}`) || "[]"
      );
      existingForum.push({
        round_num: roundNum,
        posts: result.forum_posts,
      });
      sessionStorage.setItem(`forum_${sessionId}`, JSON.stringify(existingForum));

      if (result.is_interview_complete) {
        setIsFinal(true);
      }
    } catch (err) {
      console.error("End round error:", err);
    }
  };

  const handleNextRound = () => {
    router.push(`/interview/${sessionId}/round/${roundNum + 1}`);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="min-h-screen bg-ca-bg flex flex-col">
      {/* Header */}
      <div className="border-b border-ca-border bg-ca-bg/80 backdrop-blur-xl sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div
                className="w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-bold"
                style={{ backgroundColor: interviewer.color }}
              >
                {interviewer.name
                  .split(" ")
                  .map((w) => w[0])
                  .join("")}
              </div>
              <div>
                <h1 className="text-sm font-semibold text-ca-fg">
                  {interviewer.name}
                </h1>
                <p className="text-xs text-ca-fg-muted">
                  {interviewer.role} &middot; Round {roundNum}/{totalRounds}
                  {isFinal ? " (Final)" : ""}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="text-xs text-ca-fg-muted capitalize">
                {roundType.replace("_", " ")}
              </span>
              <div className="flex items-center gap-1">
                <div className="w-16 h-1.5 bg-ca-border rounded-full overflow-hidden">
                  <div
                    className="h-full bg-ca-accent rounded-full transition-all"
                    style={{
                      width: `${(questionsAsked / maxQuestions) * 100}%`,
                    }}
                  />
                </div>
                <span className="text-xs text-ca-fg-muted">
                  {questionsAsked}/{maxQuestions}
                </span>
              </div>

              <button
                onClick={() => tts.toggleMute()}
                className="ca-btn ca-btn-ghost p-1.5"
                title={tts.isMuted ? "Unmute" : "Mute"}
              >
                {tts.isMuted ? (
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
                  </svg>
                ) : (
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Transcript */}
      <div
        ref={transcriptRef}
        className="flex-1 overflow-y-auto px-4 py-6 max-w-3xl mx-auto w-full"
        role="log"
        aria-label="Interview round transcript"
        aria-live="polite"
      >
        <div className="space-y-4">
          {turns.map((turn, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
              className={`flex ${
                turn.type === "answer" ? "justify-end" : "justify-start"
              }`}
            >
              {turn.type === "question" && (
                <div
                  className="w-7 h-7 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0 mr-2 mt-1"
                  style={{ backgroundColor: interviewer.color }}
                >
                  {turn.speaker[0]}
                </div>
              )}
              <div
                className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  turn.type === "answer"
                    ? "bubble-candidate"
                    : "bubble-interviewer"
                }`}
              >
                {turn.content}
              </div>
            </motion.div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div
                className="w-7 h-7 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0 mr-2 mt-1"
                style={{ backgroundColor: interviewer.color }}
              />
              <div className="bubble-interviewer rounded-2xl rounded-bl-sm px-4 py-3">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-ca-fg-muted rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-2 h-2 bg-ca-fg-muted rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-2 h-2 bg-ca-fg-muted rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Transition overlay */}
      {status === "transition" && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-20 flex items-center justify-center"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="ca-card p-8 max-w-lg mx-4 text-center space-y-6"
          >
            <h2 className="text-xl font-bold text-ca-fg">
              Round {roundNum} Complete
            </h2>

            {forumPosts.length > 0 && (
              <div className="space-y-3 text-left">
                <p className="text-sm text-ca-fg-muted text-center">
                  The panel is discussing your performance...
                </p>
                {forumPosts.slice(0, 3).map((post, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.8 }}
                    className="ca-card p-3"
                  >
                    <p className="text-xs font-semibold text-ca-fg mb-1">
                      {post.agent_name}
                      <span className="text-ca-fg-muted font-normal ml-1">
                        ({post.agent_role})
                      </span>
                    </p>
                    <p className="text-sm text-ca-fg-secondary line-clamp-3">
                      {post.content}
                    </p>
                  </motion.div>
                ))}
              </div>
            )}

            {forumPosts.length > 0 && !isFinal && (
              <button
                onClick={handleNextRound}
                className="ca-btn ca-btn-primary w-full py-3"
              >
                Continue to Round {roundNum + 1}
              </button>
            )}

            {isFinal && (
              <div className="space-y-3">
                <p className="text-sm text-ca-fg-muted">
                  All rounds complete! See the full behind-the-scenes
                  discussion.
                </p>
                <button
                  onClick={() =>
                    router.push(`/interview/${sessionId}/forum`)
                  }
                  className="ca-btn ca-btn-primary w-full py-3"
                >
                  See Forum Reveal
                </button>
              </div>
            )}
          </motion.div>
        </motion.div>
      )}

      {/* Ending overlay */}
      {status === "ending" && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-20 flex items-center justify-center">
          <div className="ca-card p-6 text-center">
            <svg className="animate-spin h-8 w-8 text-ca-accent mx-auto mb-3" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <p className="text-sm text-ca-fg">
              Panel is discussing your answers...
            </p>
          </div>
        </div>
      )}

      {/* Input */}
      {status === "active" && (
        <div className="border-t border-ca-border bg-ca-bg p-4">
          <div className="max-w-3xl mx-auto flex gap-3">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your answer..."
              rows={2}
              className="ca-input flex-1 resize-none"
              disabled={isLoading}
            />
            <div className="flex flex-col gap-2">
              <button
                onClick={handleSubmit}
                disabled={!input.trim() || isLoading}
                className="ca-btn ca-btn-primary px-4 flex-1"
              >
                Send
              </button>
              {questionsAsked >= maxQuestions - 1 && (
                <button
                  onClick={handleEndRound}
                  className="ca-btn ca-btn-secondary px-4 text-xs"
                >
                  End Round
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
