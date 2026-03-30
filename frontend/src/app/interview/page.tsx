"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { startInterview } from "@/lib/api";

const PRESETS = [
  {
    key: "campus_placement",
    name: "Campus Placement",
    desc: "HR + Technical + Manager panel for campus hiring",
    panelSize: 3,
    icon: "🎓",
    recommended: true,
  },
  {
    key: "senior_tech",
    name: "Senior Tech Interview",
    desc: "Deep technical + leadership for experienced roles",
    panelSize: 3,
    icon: "💻",
  },
  {
    key: "stress_interview",
    name: "Stress Interview",
    desc: "High-pressure with deliberately challenging panelists",
    panelSize: 3,
    icon: "🔥",
  },
  {
    key: "upsc_board",
    name: "UPSC Board",
    desc: "Chairman + 2 board members — civil services simulation",
    panelSize: 3,
    icon: "🏛️",
  },
  {
    key: "hr_round",
    name: "HR Round",
    desc: "Behavioral STAR-method interview with one interviewer",
    panelSize: 1,
    icon: "🤝",
  },
  {
    key: "tech_deep_dive",
    name: "Tech Deep Dive",
    desc: "Two senior engineers on system design and coding",
    panelSize: 2,
    icon: "⚙️",
  },
];

const DIFFICULTIES = [
  { key: "practice", name: "Practice", desc: "Friendly, with hints" },
  { key: "realistic", name: "Realistic", desc: "Like the real thing" },
  { key: "stress_test", name: "Stress Test", desc: "Maximum pressure" },
];

export default function InterviewSetupPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [preset, setPreset] = useState("campus_placement");
  const [role, setRole] = useState("");
  const [company, setCompany] = useState("");
  const [difficulty, setDifficulty] = useState("realistic");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleStart = async () => {
    setLoading(true);
    setError("");
    try {
      const result = await startInterview({ preset, role, company, difficulty });
      // Store the opening data in sessionStorage for the interview page
      sessionStorage.setItem(
        `interview_${result.session_id}`,
        JSON.stringify(result)
      );
      router.push(`/interview/${result.session_id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to start interview");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-12">
      {/* Progress */}
      <div className="flex items-center gap-2 mb-8">
        {[1, 2, 3].map((s) => (
          <div key={s} className="flex items-center gap-2 flex-1">
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all ${
                s <= step
                  ? "bg-gradient-to-br from-indigo-500 to-violet-500 text-white shadow-sm shadow-indigo-500/20"
                  : "bg-ca-bg-secondary text-ca-fg-muted border border-ca-border"
              }`}
            >
              {s < step ? (
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                </svg>
              ) : s}
            </div>
            <span className={`text-sm hidden sm:inline ${s <= step ? "text-ca-fg font-medium" : "text-ca-fg-muted"}`}>
              {s === 1 ? "Type" : s === 2 ? "Details" : "Difficulty"}
            </span>
            {s < 3 && (
              <div className={`flex-1 h-0.5 rounded-full transition-all ${s < step ? "bg-gradient-to-r from-indigo-500 to-violet-500" : "bg-ca-border"}`} />
            )}
          </div>
        ))}
      </div>

      {/* Step 1: Choose interview type */}
      {step === 1 && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <h1 className="text-2xl font-display font-extrabold mb-2">Choose interview type</h1>
          <p className="text-ca-fg-secondary mb-6">Select the format that matches your preparation goal</p>

          <div className="grid sm:grid-cols-2 gap-4">
            {PRESETS.map((p) => (
              <button
                key={p.key}
                onClick={() => setPreset(p.key)}
                className={`ca-card p-4 text-left transition-all rounded-xl ${
                  preset === p.key
                    ? "border-ca-accent ring-2 ring-ca-accent/20 shadow-sm shadow-indigo-500/10"
                    : "hover:border-ca-border-strong card-glow"
                }`}
              >
                <div className="flex items-start gap-3">
                  <span className="text-2xl">{p.icon}</span>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium">{p.name}</h3>
                      {(p as any).recommended && (
                        <span className="ca-badge ca-badge-success text-[10px]">Recommended</span>
                      )}
                    </div>
                    <p className="text-sm text-ca-fg-muted mt-1">{p.desc}</p>
                    <span className="ca-badge ca-badge-accent mt-2">{p.panelSize} panelist{p.panelSize > 1 ? "s" : ""}</span>
                  </div>
                </div>
              </button>
            ))}
          </div>

          <div className="flex justify-end mt-6">
            <button
              onClick={() => setStep(2)}
              className="ca-btn ca-btn-primary py-2 px-6"
            >
              Continue
            </button>
          </div>
        </motion.div>
      )}

      {/* Step 2: Role & Company */}
      {step === 2 && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <h1 className="text-2xl font-display font-extrabold mb-2">Interview details</h1>
          <p className="text-ca-fg-secondary mb-6">Optional — makes the interview more targeted and realistic</p>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1.5">Target Role</label>
              <input
                type="text"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder="e.g., Backend Developer, Product Manager, IAS Officer"
                className="ca-input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1.5">Company</label>
              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="e.g., TCS, Google, Flipkart, UPSC"
                className="ca-input"
              />
            </div>
          </div>

          <div className="flex justify-between mt-6">
            <button
              onClick={() => setStep(1)}
              className="ca-btn ca-btn-ghost"
            >
              Back
            </button>
            <button
              onClick={() => setStep(3)}
              className="ca-btn ca-btn-primary py-2 px-6"
            >
              Continue
            </button>
          </div>
        </motion.div>
      )}

      {/* Step 3: Difficulty & Launch */}
      {step === 3 && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <h1 className="text-2xl font-display font-extrabold mb-2">Set difficulty</h1>
          <p className="text-ca-fg-secondary mb-6">How challenging should the interview be?</p>

          <div className="grid sm:grid-cols-3 gap-4 mb-8">
            {DIFFICULTIES.map((d) => (
              <button
                key={d.key}
                onClick={() => setDifficulty(d.key)}
                className={`ca-card p-4 text-center transition-all rounded-xl ${
                  difficulty === d.key
                    ? "border-ca-accent ring-2 ring-ca-accent/20 shadow-sm shadow-indigo-500/10"
                    : "hover:border-ca-border-strong card-glow"
                }`}
              >
                <h3 className="font-medium">{d.name}</h3>
                <p className="text-sm text-ca-fg-muted mt-1">{d.desc}</p>
              </button>
            ))}
          </div>

          {/* Summary */}
          <div className="glass-card rounded-xl p-5 mb-6">
            <h3 className="font-medium mb-3">Interview Summary</h3>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="text-ca-fg-muted">Type</div>
              <div>{PRESETS.find((p) => p.key === preset)?.name}</div>
              <div className="text-ca-fg-muted">Role</div>
              <div>{role || "General"}</div>
              <div className="text-ca-fg-muted">Company</div>
              <div>{company || "Not specified"}</div>
              <div className="text-ca-fg-muted">Difficulty</div>
              <div>{DIFFICULTIES.find((d) => d.key === difficulty)?.name}</div>
              <div className="text-ca-fg-muted">Panel Size</div>
              <div>{PRESETS.find((p) => p.key === preset)?.panelSize} interviewers</div>
            </div>
          </div>

          {error && (
            <div className="ca-badge ca-badge-danger p-3 rounded-lg mb-4 w-full text-sm">
              {error}
            </div>
          )}

          <div className="flex justify-between">
            <button
              onClick={() => setStep(2)}
              className="ca-btn ca-btn-ghost"
            >
              Back
            </button>
            <button
              onClick={handleStart}
              disabled={loading}
              className="ca-btn ca-btn-primary py-2.5 px-8 shadow-lg shadow-indigo-500/20"
            >
              {loading ? (
                <>
                  <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Setting up panel...
                </>
              ) : (
                "Start Interview"
              )}
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
}
