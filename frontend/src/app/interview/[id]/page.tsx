"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  InterviewPanelist,
  InterviewTurn,
  InterviewStartResponse,
  submitInterviewAnswer,
  endInterview,
} from "@/lib/api";
import { useTTS } from "@/hooks/useTTS";

// ─── Typing effect component (click to skip) ───
function TypedMessage({
  text,
  speed = 30,
  onComplete,
}: {
  text: string;
  speed?: number;
  onComplete?: () => void;
}) {
  const [displayed, setDisplayed] = useState("");
  const [done, setDone] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    setDisplayed("");
    setDone(false);
    let i = 0;
    const words = text.split(" ");
    intervalRef.current = setInterval(() => {
      if (i < words.length) {
        setDisplayed((prev) => (prev ? prev + " " + words[i] : words[i]));
        i++;
      } else {
        if (intervalRef.current) clearInterval(intervalRef.current);
        setDone(true);
        onComplete?.();
      }
    }, speed);
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [text, speed]);

  const skipToEnd = () => {
    if (done) return;
    if (intervalRef.current) clearInterval(intervalRef.current);
    setDisplayed(text);
    setDone(true);
    onComplete?.();
  };

  return (
    <span onClick={skipToEnd} className={!done ? "cursor-pointer" : ""} title={!done ? "Click to skip" : ""}>
      {displayed}
      {!done && <span className="typing-cursor" />}
    </span>
  );
}

export default function InterviewSessionPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [panel, setPanel] = useState<InterviewPanelist[]>([]);
  const [turns, setTurns] = useState<InterviewTurn[]>([]);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<
    "loading" | "active" | "wrapping_up" | "evaluating" | "done"
  >("loading");
  const [turnCount, setTurnCount] = useState(0);
  const [maxTurns, setMaxTurns] = useState(30);
  const [coverage, setCoverage] = useState(0);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [typingTurnIndex, setTypingTurnIndex] = useState(-1);
  const [activeSpeaker, setActiveSpeaker] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const transcriptRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // ─── TTS (Google Cloud TTS Indian voices, Web Speech API fallback) ───
  const tts = useTTS();

  // Load initial data from sessionStorage
  useEffect(() => {
    const stored = sessionStorage.getItem(`interview_${id}`);
    if (stored) {
      const data: InterviewStartResponse = JSON.parse(stored);
      setPanel(data.panel);
      setMaxTurns(data.config.max_turns);
      sessionStorage.removeItem(`interview_${id}`);

      // Deliver opening turns sequentially with typing effect
      deliverTurnsSequentially(data.opening, 0);
    } else {
      setStatus("active");
    }

    // Start timer
    timerRef.current = setInterval(() => {
      setElapsedSeconds((s) => s + 1);
    }, 1000);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [id]);

  // Deliver turns one at a time with animation + voice
  const deliverTurnsSequentially = useCallback(
    (newTurns: InterviewTurn[], startIndex: number) => {
      if (newTurns.length === 0) {
        setStatus("active");
        return;
      }

      // Track pending turns for skip functionality
      pendingTurnsRef.current = [...newTurns];
      pendingStartIdxRef.current = startIndex;

      let i = 0;
      const deliverNext = () => {
        if (i < newTurns.length) {
          const turn = newTurns[i];
          pendingTurnsRef.current = newTurns.slice(i + 1);
          setActiveSpeaker(turn.speaker);
          setTurns((prev) => [...prev, turn]);
          setTypingTurnIndex(startIndex + i);

          // Trigger TTS for interviewer turns — wait for BOTH typing + audio
          typingDoneRef.current = false;
          audioDoneRef.current = false;
          const isInterviewerTurn =
            turn.speaker !== "You" && turn.speaker !== "Candidate";
          if (isInterviewerTurn) {
            tts.speak(turn.content, turn.speaker, () => {
              audioDoneRef.current = true;
              if (typingDoneRef.current) {
                deliverNextRef.current?.();
              }
            });
          } else {
            audioDoneRef.current = true;
          }

          i++;
        } else {
          setActiveSpeaker(null);
          setTypingTurnIndex(-1);
          setStatus("active");
          inputRef.current?.focus();
        }
      };

      // Deliver first immediately
      deliverNext();
      // The rest get delivered when typing completes (via onComplete)
      const checkAndDeliver = () => {
        if (i < newTurns.length) {
          setTimeout(() => {
            deliverNext();
          }, 500); // Brief pause between speakers
        } else {
          tts.stop();
          setActiveSpeaker(null);
          setTypingTurnIndex(-1);
          setStatus("active");
          inputRef.current?.focus();
        }
      };

      // Store the callback so TypedMessage can call it
      deliverNextRef.current = checkAndDeliver;
    },
    []
  );

  const deliverNextRef = useRef<(() => void) | null>(null);
  const typingDoneRef = useRef(false);
  const audioDoneRef = useRef(false);
  const pendingTurnsRef = useRef<InterviewTurn[]>([]);
  const pendingStartIdxRef = useRef(0);

  const handleSkipAll = useCallback(() => {
    tts.stop();
    // Add any remaining pending turns immediately
    const remaining = pendingTurnsRef.current;
    if (remaining.length > 0) {
      setTurns((prev) => [...prev, ...remaining]);
      pendingTurnsRef.current = [];
    }
    setActiveSpeaker(null);
    setTypingTurnIndex(-1);
    setStatus("active");
    deliverNextRef.current = null;
    inputRef.current?.focus();
  }, [tts]);

  const handleTypingComplete = useCallback(() => {
    typingDoneRef.current = true;
    if (audioDoneRef.current) {
      deliverNextRef.current?.();
    }
  }, []);

  // Auto-scroll only if user is near bottom
  const isNearBottomRef = useRef(true);
  const [showScrollBtn, setShowScrollBtn] = useState(false);

  const handleTranscriptScroll = useCallback(() => {
    if (!transcriptRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = transcriptRef.current;
    const nearBottom = scrollHeight - scrollTop - clientHeight < 100;
    isNearBottomRef.current = nearBottom;
    setShowScrollBtn(!nearBottom);
  }, []);

  const scrollToBottom = useCallback(() => {
    if (transcriptRef.current) {
      transcriptRef.current.scrollTo({ top: transcriptRef.current.scrollHeight, behavior: "smooth" });
    }
  }, []);

  useEffect(() => {
    if (transcriptRef.current && isNearBottomRef.current) {
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
    }
  }, [turns, typingTurnIndex]);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  const handleSubmitAnswer = useCallback(async () => {
    if (!answer.trim() || loading) return;

    const answerText = answer.trim();
    setAnswer("");
    setLoading(true);

    // Add candidate's answer immediately
    const candidateTurn: InterviewTurn = {
      turn_number: turns.length + 1,
      speaker: "You",
      speaker_role: "candidate",
      content: answerText,
      turn_type: "answer",
    };
    setTurns((prev) => [...prev, candidateTurn]);

    try {
      const result = await submitInterviewAnswer(id, answerText);
      const newTurns = result.responses;

      if (result.state?.orchestrator) {
        setTurnCount(result.state.orchestrator.turn_number);
        setCoverage(result.state.orchestrator.coverage);
      }

      if (result.state?.status === "wrapping_up") {
        setStatus("wrapping_up");
      }

      setLoading(false);

      // Deliver interviewer responses sequentially with typing
      if (newTurns.length > 0) {
        const startIdx = turns.length + 1; // after candidate turn
        deliverTurnsSequentially(newTurns, startIdx);
      }
    } catch (e) {
      console.error("Failed to submit answer:", e);
      setError("Failed to get a response. Please try again.");
      setLoading(false);
      inputRef.current?.focus();
    }
  }, [answer, loading, id, turns.length, deliverTurnsSequentially]);

  const handleEndInterview = async () => {
    setStatus("evaluating");
    setActiveSpeaker(null);
    tts.stop();

    try {
      const result = await endInterview(id);
      sessionStorage.setItem(
        `evaluation_${id}`,
        JSON.stringify(result.evaluation)
      );
      router.push(`/interview/${id}/results`);
    } catch (e) {
      console.error("Failed to end interview:", e);
      setError("Failed to end interview. Please try again.");
      setStatus("active");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmitAnswer();
    }
  };

  const getAvatarColor = (speaker: string) => {
    const panelist = panel.find((p) => p.name === speaker);
    return panelist?.avatar_color || "#6366f1";
  };

  const getInitial = (name: string) => name.charAt(0).toUpperCase();

  const progress = maxTurns > 0 ? (turnCount / maxTurns) * 100 : 0;

  const isInterviewer = (speaker: string) =>
    speaker !== "You" && speaker !== "Candidate";

  return (
    <div className="h-[calc(100vh-3.5rem)] flex flex-col">
      {/* Top bar */}
      <div className="border-b border-ca-border px-4 sm:px-6 py-3 flex items-center justify-between bg-ca-bg/80 backdrop-blur-xl">
        <div className="flex items-center gap-4">
          {/* Panel avatars */}
          <div className="flex items-center gap-3">
            {panel.map((p) => (
              <div
                key={p.name}
                className={`relative ${
                  activeSpeaker === p.name ? "avatar-speaking" : ""
                }`}
              >
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-bold transition-all duration-300 ${
                    activeSpeaker === p.name
                      ? "scale-110 ring-2 ring-offset-2 ring-offset-ca-bg"
                      : "opacity-70"
                  }`}
                  style={{
                    backgroundColor: p.avatar_color,
                    ...(activeSpeaker === p.name
                      ? { ringColor: p.avatar_color }
                      : {}),
                  }}
                  title={`${p.name} — ${p.role}`}
                >
                  {getInitial(p.name)}
                </div>
                {activeSpeaker === p.name && (
                  <div className="absolute -bottom-1 left-1/2 -translate-x-1/2">
                    <div className="speaking-indicator">
                      <span
                        style={{ background: p.avatar_color }}
                      />
                      <span
                        style={{ background: p.avatar_color }}
                      />
                      <span
                        style={{ background: p.avatar_color }}
                      />
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
          <div>
            <div className="text-sm font-medium">
              {activeSpeaker ? (
                <span>
                  <span className="text-ca-accent">{activeSpeaker}</span>
                  <span className="text-ca-fg-muted ml-1">is speaking...</span>
                </span>
              ) : (
                <span>Panel Interview</span>
              )}
            </div>
            <div className="flex items-center gap-3 text-xs text-ca-fg-muted">
              <span>
                Turn {turnCount}/{maxTurns}
              </span>
              <span>Coverage: {Math.round(coverage * 100)}%</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-sm font-mono text-ca-fg-muted">
            {formatTime(elapsedSeconds)}
          </span>

          {/* Mute/Unmute toggle */}
          <button
            onClick={tts.toggleMute}
            className="ca-btn ca-btn-ghost text-xs py-1.5 px-2"
            title={tts.isMuted ? "Unmute voices" : "Mute voices"}
          >
            {tts.isMuted ? (
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 9.75 19.5 12m0 0 2.25 2.25M19.5 12l2.25-2.25M19.5 12l-2.25 2.25m-10.5-6 4.72-3.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-3.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-3.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-3.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
              </svg>
            )}
          </button>

          <button
            onClick={handleEndInterview}
            disabled={status === "evaluating"}
            className="ca-btn ca-btn-secondary text-xs py-1.5 px-3"
          >
            {status === "evaluating" ? "Evaluating..." : "End Interview"}
          </button>
        </div>
      </div>

      {/* Progress bar */}
      <div className="ca-progress">
        <div
          className="ca-progress-bar"
          style={{ width: `${Math.min(progress, 100)}%` }}
        />
      </div>

      {/* Error banner */}
      {error && (
        <div className="px-4 sm:px-6 py-2 bg-red-50 border-b border-red-200 flex items-center justify-between">
          <p className="text-sm text-red-700">{error}</p>
          <button onClick={() => setError(null)} className="text-red-500 hover:text-red-700 text-sm font-medium ml-4">
            Dismiss
          </button>
        </div>
      )}

      {/* Transcript */}
      <div
        ref={transcriptRef}
        onScroll={handleTranscriptScroll}
        className="flex-1 overflow-y-auto px-4 sm:px-6 py-4 space-y-4 relative"
        role="log"
        aria-label="Interview transcript"
        aria-live="polite"
      >
        <AnimatePresence>
          {turns.map((turn, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`flex gap-3 ${
                !isInterviewer(turn.speaker) ? "justify-end" : ""
              }`}
            >
              {/* Interviewer avatar */}
              {isInterviewer(turn.speaker) && (
                <div className="flex flex-col items-center gap-1 flex-shrink-0">
                  <div
                    className={`relative w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-bold mt-1 transition-all duration-300 ${
                      activeSpeaker === turn.speaker && i === typingTurnIndex
                        ? "avatar-speaking"
                        : ""
                    }`}
                    style={{ backgroundColor: getAvatarColor(turn.speaker) }}
                  >
                    {getInitial(turn.speaker)}
                  </div>
                  {activeSpeaker === turn.speaker &&
                    i === typingTurnIndex && (
                      <div className="speaking-indicator">
                        <span
                          style={{
                            background: getAvatarColor(turn.speaker),
                          }}
                        />
                        <span
                          style={{
                            background: getAvatarColor(turn.speaker),
                          }}
                        />
                        <span
                          style={{
                            background: getAvatarColor(turn.speaker),
                          }}
                        />
                      </div>
                    )}
                </div>
              )}

              {/* Message bubble */}
              <div
                className={`max-w-[75%] ${
                  !isInterviewer(turn.speaker)
                    ? "bubble-candidate p-4"
                    : "bubble-interviewer p-4"
                }`}
              >
                {/* Speaker name + role */}
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="text-sm font-semibold">
                    {turn.speaker}
                  </span>
                  {isInterviewer(turn.speaker) && turn.speaker_role && (
                    <span className="text-xs text-ca-fg-muted">
                      {turn.speaker_role}
                    </span>
                  )}
                </div>

                {/* Message content — typed or static */}
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {i === typingTurnIndex && isInterviewer(turn.speaker) ? (
                    <TypedMessage
                      text={turn.content}
                      speed={40}
                      onComplete={handleTypingComplete}
                    />
                  ) : (
                    turn.content
                  )}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Loading indicator (waiting for backend) */}
        {loading && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex gap-3 items-center py-2"
          >
            <div className="w-10 h-10 rounded-full bg-ca-bg-secondary flex items-center justify-center">
              <div className="flex gap-1">
                <span className="w-1.5 h-1.5 bg-ca-accent rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-1.5 h-1.5 bg-ca-accent rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-1.5 h-1.5 bg-ca-accent rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
            <span className="text-sm text-ca-fg-muted">
              Panel is considering your response...
            </span>
          </motion.div>
        )}
      </div>

      {/* Scroll to bottom */}
      {showScrollBtn && (
        <div className="flex justify-center py-1">
          <button
            onClick={scrollToBottom}
            className="ca-btn ca-btn-ghost text-xs py-1 px-3 rounded-full border border-ca-border shadow-sm bg-ca-bg"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3" />
            </svg>
            New messages
          </button>
        </div>
      )}

      {/* Input area */}
      <div className="border-t border-ca-border px-4 sm:px-6 py-4 bg-ca-bg/80 backdrop-blur-xl">
        {status === "active" || status === "wrapping_up" ? (
          <div className="max-w-4xl mx-auto flex gap-3">
            <textarea
              ref={inputRef}
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                activeSpeaker
                  ? "Interviewer is speaking... (click Skip to respond)"
                  : status === "wrapping_up"
                  ? "Any final questions or comments?"
                  : "Type your answer... (Enter to send, Shift+Enter for new line)"
              }
              disabled={loading || !!activeSpeaker}
              rows={2}
              className="ca-input resize-none flex-1 min-h-[2.5rem] max-h-32"
            />
            {activeSpeaker && (
              <button
                onClick={handleSkipAll}
                className="ca-btn ca-btn-secondary self-end py-2.5 px-4 text-sm"
              >
                Skip
              </button>
            )}
            <button
              onClick={handleSubmitAnswer}
              disabled={loading || !answer.trim() || !!activeSpeaker}
              className="ca-btn ca-btn-primary self-end py-2.5 px-4"
              aria-label="Send answer"
            >
              {loading ? (
                <svg
                  className="animate-spin w-5 h-5"
                  viewBox="0 0 24 24"
                  fill="none"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                  />
                </svg>
              ) : (
                <svg
                  className="w-5 h-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={2}
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5"
                  />
                </svg>
              )}
            </button>
          </div>
        ) : status === "evaluating" ? (
          <div className="text-center py-3">
            <div className="flex items-center justify-center gap-3 text-ca-fg-muted">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-ca-accent rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 bg-ca-accent rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 bg-ca-accent rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
              <span className="text-sm font-medium">
                Panelists are evaluating your performance...
              </span>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
