"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { startScreening } from "@/lib/api";

export default function ScreeningPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleStart = async () => {
    setIsLoading(true);
    try {
      const result = await startScreening(name, resumeFile || undefined);
      sessionStorage.setItem(
        `screening_${result.session_id}`,
        JSON.stringify(result)
      );
      router.push(`/screening/${result.session_id}`);
    } catch (err) {
      console.error("Failed to start screening:", err);
      setError("Failed to start screening. Please check your connection and try again.");
      setIsLoading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) setResumeFile(file);
  };

  return (
    <div className="min-h-[calc(100vh-3.5rem)] bg-ca-bg flex items-center justify-center p-4 mesh-gradient">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-lg"
      >
        <div className="text-center mb-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center mx-auto mb-5 shadow-lg shadow-indigo-500/20"
          >
            <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
            </svg>
          </motion.div>
          <h1 className="text-3xl font-display font-extrabold text-ca-fg mb-2">
            Start Your Interview
          </h1>
          <p className="text-ca-fg-secondary max-w-sm mx-auto">
            We&apos;ll have a quick chat to understand your background, then set
            up a personalized interview panel for you.
          </p>
        </div>

        {error && (
          <div className="mb-4 px-4 py-3 bg-red-50 border border-red-200 rounded-xl flex items-center justify-between">
            <p className="text-sm text-red-700">{error}</p>
            <button onClick={() => setError(null)} className="text-red-500 hover:text-red-700 text-sm font-medium ml-4">
              Dismiss
            </button>
          </div>
        )}

        <div className="glass-card rounded-2xl p-7 space-y-6">
          <div>
            <label className="block text-sm font-medium text-ca-fg mb-2">
              Your Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g., Rahul Sharma"
              className="ca-input w-full"
              autoFocus
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-ca-fg mb-2">
              Resume (optional)
            </label>
            <div
              onClick={() => fileRef.current?.click()}
              onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
              onDragLeave={() => setIsDragOver(false)}
              onDrop={handleDrop}
              className={`rounded-xl border-2 border-dashed p-6 text-center cursor-pointer transition-all ${
                isDragOver
                  ? "border-ca-accent bg-ca-accent/5"
                  : resumeFile
                  ? "border-ca-success/50 bg-ca-success/5"
                  : "border-ca-border hover:border-ca-accent/50 hover:bg-ca-accent/5"
              }`}
            >
              {resumeFile ? (
                <div className="flex items-center justify-center gap-2">
                  <svg className="w-5 h-5 text-ca-success" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
                  <p className="text-ca-fg text-sm font-medium">
                    {resumeFile.name}
                  </p>
                </div>
              ) : (
                <>
                  <svg className="w-8 h-8 text-ca-fg-muted mx-auto mb-2" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
                  </svg>
                  <p className="text-ca-fg-muted text-sm">
                    Drop your resume here or <span className="text-ca-accent font-medium">browse</span>
                  </p>
                  <p className="text-xs text-ca-fg-muted mt-1">PDF, DOCX, or TXT</p>
                </>
              )}
              <input
                ref={fileRef}
                type="file"
                accept=".pdf,.txt,.doc,.docx"
                className="hidden"
                onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
              />
            </div>
          </div>

          <button
            onClick={handleStart}
            disabled={isLoading || !name.trim()}
            className="ca-btn ca-btn-primary w-full py-3.5 text-base shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/30 transition-shadow"
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-2">
                <div className="flex gap-1">
                  <span className="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
                Starting...
              </span>
            ) : (
              <>
                Start Interview
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
                </svg>
              </>
            )}
          </button>
        </div>

        <div className="flex items-center justify-center gap-4 mt-6 text-xs text-ca-fg-muted">
          <div className="flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
            3-5 min screening
          </div>
          <span className="text-ca-border">|</span>
          <div className="flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
            </svg>
            Personalized panel
          </div>
          <span className="text-ca-border">|</span>
          <div className="flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 0 0-2.455 2.456Z" />
            </svg>
            AI-powered
          </div>
        </div>
      </motion.div>
    </div>
  );
}
