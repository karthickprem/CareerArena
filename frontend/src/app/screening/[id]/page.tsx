"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  submitScreeningAnswer,
  completeScreening,
  type ScreeningStartResponse,
  type ScreeningAnswerResponse,
} from "@/lib/api";
import { useTTS } from "@/hooks/useTTS";

interface ChatMessage {
  speaker: "agent" | "candidate";
  content: string;
  isTyping?: boolean;
}

export default function ScreeningChatPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.id as string;

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [coverage, setCoverage] = useState<Record<string, boolean>>({});
  const [coveragePct, setCoveragePct] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [isGeneratingPanel, setIsGeneratingPanel] = useState(false);
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");
  const [error, setError] = useState<string | null>(null);

  const transcriptRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const tts = useTTS();

  // Load initial data from sessionStorage
  useEffect(() => {
    const stored = sessionStorage.getItem(`screening_${sessionId}`);
    if (stored) {
      const data: ScreeningStartResponse = JSON.parse(stored);
      sessionStorage.removeItem(`screening_${sessionId}`);
      setMessages([{ speaker: "agent", content: data.message }]);
      setCoverage(data.coverage);
      tts.speak(data.message, "Kavitha");
    }
  }, [sessionId]);

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
  }, [messages]);

  const handleSubmit = useCallback(async () => {
    const text = input.trim();
    if (!text || isLoading || isComplete) return;

    setInput("");
    setMessages((prev) => [...prev, { speaker: "candidate", content: text }]);
    setIsLoading(true);

    try {
      const result: ScreeningAnswerResponse = await submitScreeningAnswer(
        sessionId,
        text
      );

      setMessages((prev) => [
        ...prev,
        { speaker: "agent", content: result.message },
      ]);
      setCoverage(result.coverage);
      setCoveragePct(result.coverage_pct);
      setIsComplete(result.is_complete);

      tts.speak(result.message, "Kavitha");
    } catch (err) {
      console.error("Screening answer error:", err);
      setError("Failed to get a response. Please try again.");
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  }, [input, isLoading, isComplete, sessionId, tts]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleGeneratePanel = async () => {
    setIsGeneratingPanel(true);
    try {
      const result = await completeScreening(sessionId, company, role, 3);
      sessionStorage.setItem(
        `panel_${result.session_id}`,
        JSON.stringify(result)
      );
      router.push(`/interview/${result.session_id}/panel`);
    } catch (err) {
      console.error("Panel generation error:", err);
      setError("Failed to generate panel. Please try again.");
      setIsGeneratingPanel(false);
    }
  };

  const coveredCount = Object.values(coverage).filter(Boolean).length;
  const totalDimensions = Object.keys(coverage).length || 8;

  return (
    <div className="min-h-screen bg-ca-bg flex flex-col">
      {/* Header */}
      <div className="border-b border-ca-border bg-ca-bg/80 backdrop-blur-xl sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-purple-500 flex items-center justify-center text-white text-sm font-medium">
              K
            </div>
            <div>
              <h1 className="text-sm font-semibold text-ca-fg">
                Kavitha - Screening
              </h1>
              <p className="text-xs text-ca-fg-muted">
                Getting to know you...
              </p>
            </div>
          </div>

          {/* Coverage bar */}
          <div className="flex items-center gap-2" title={Object.entries(coverage).map(([k, v]) => `${k.replace(/_/g, " ")}: ${v ? "covered" : "pending"}`).join("\n")}>
            <span className="text-xs text-ca-fg-muted hidden sm:inline">Profile</span>
            <div className="w-24 h-2 bg-ca-border rounded-full overflow-hidden">
              <div
                className="h-full bg-ca-accent rounded-full transition-all duration-500"
                style={{ width: `${(coveredCount / totalDimensions) * 100}%` }}
              />
            </div>
            <span className="text-xs text-ca-fg-muted">
              {Math.round((coveredCount / totalDimensions) * 100)}%
            </span>
          </div>
        </div>
      </div>

      {/* Error banner */}
      {error && (
        <div className="px-4 py-2 bg-red-50 border-b border-red-200 flex items-center justify-between max-w-3xl mx-auto w-full">
          <p className="text-sm text-red-700">{error}</p>
          <button onClick={() => setError(null)} className="text-red-500 hover:text-red-700 text-sm font-medium ml-4">
            Dismiss
          </button>
        </div>
      )}

      {/* Messages */}
      <div
        ref={transcriptRef}
        onScroll={handleTranscriptScroll}
        className="flex-1 overflow-y-auto px-4 py-6 max-w-3xl mx-auto w-full"
        role="log"
        aria-label="Screening conversation"
        aria-live="polite"
      >
        <div className="space-y-4">
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
              className={`flex ${
                msg.speaker === "candidate" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  msg.speaker === "candidate"
                    ? "bubble-candidate"
                    : "bubble-interviewer"
                }`}
              >
                {msg.content}
              </div>
            </motion.div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
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

      {/* Completion panel */}
      {isComplete && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="border-t border-ca-border bg-ca-bg p-4"
        >
          <div className="max-w-3xl mx-auto space-y-4">
            <p className="text-sm font-medium text-ca-fg text-center">
              Screening complete! Set up your interview:
            </p>
            <div className="flex gap-3">
              <input
                type="text"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder="Target role (e.g., SDE-1)"
                className="ca-input flex-1"
              />
              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="Company (e.g., TCS, Infosys)"
                className="ca-input flex-1"
              />
            </div>
            <p className="text-xs text-ca-fg-muted text-center">
              Leave blank for a general interview panel based on your profile
            </p>
            <button
              onClick={handleGeneratePanel}
              disabled={isGeneratingPanel}
              className="ca-btn ca-btn-primary w-full py-3"
            >
              {isGeneratingPanel ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Generating your panel...
                </span>
              ) : (
                "Generate Interview Panel"
              )}
            </button>
          </div>
        </motion.div>
      )}

      {/* Input */}
      {!isComplete && (
        <div className="border-t border-ca-border bg-ca-bg p-4">
          <div className="max-w-3xl mx-auto flex gap-3">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your answer..."
              rows={1}
              className="ca-input flex-1 resize-none"
              disabled={isLoading}
            />
            <button
              onClick={handleSubmit}
              disabled={!input.trim() || isLoading}
              className="ca-btn ca-btn-primary px-4"
              aria-label="Send message"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
