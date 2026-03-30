"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listSessions } from "@/lib/api";

interface Session {
  session_id: string;
  query: string;
  query_type: string;
  status: string;
  created_at: string;
}

const TYPE_LABELS: Record<string, string> = {
  PROFILE_REVIEW: "Resume review",
  CAREER_STRATEGY: "Career strategy",
  INTERVIEW_READINESS: "Interview check",
  SALARY_INTEL: "Salary intel",
  OFFER_COMPARISON: "Offer comparison",
  COMPANY_RESEARCH: "Company research",
  SKILL_PLANNING: "Skill planning",
  INTERVIEW_PREP: "Interview prep",
  NEGOTIATION: "Negotiation",
  GENERAL: "General",
};

const STATUS_STYLES: Record<string, string> = {
  completed: "ca-badge-success",
  running: "ca-badge-accent",
  error: "ca-badge-danger",
};

function ScorePill({ sessionId }: { sessionId: string }) {
  const [score, setScore] = useState<number | null>(null);

  useEffect(() => {
    try {
      const stored = sessionStorage.getItem(`evaluation_${sessionId}`);
      if (stored) {
        const data = JSON.parse(stored);
        if (data.overall) setScore(data.overall);
      }
    } catch { /* ignore */ }
  }, [sessionId]);

  if (score === null) {
    return (
      <svg className="w-4 h-4 text-ca-fg-muted group-hover:text-ca-accent transition-colors" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
      </svg>
    );
  }

  const color = score >= 7 ? "text-emerald-600 bg-emerald-50" : score >= 5 ? "text-amber-600 bg-amber-50" : "text-red-600 bg-red-50";
  return (
    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${color}`}>
      {score.toFixed(1)}/10
    </span>
  );
}

export default function HistoryPage() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await listSessions();
        setSessions(data.sessions);
      } catch {
        /* keep empty */
      } finally {
        setLoading(false);
      }
    }
    void load();
  }, []);

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight text-ca-fg mb-1">Your Sessions</h1>
        <p className="text-ca-fg-secondary text-sm">
          Every investigation and interview is preserved here.
        </p>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="skeleton-card">
              <div className="flex items-start gap-4">
                <div className="flex-1 min-w-0 space-y-2">
                  <div className="skeleton skeleton-text w-3/4 h-4" />
                  <div className="flex gap-2">
                    <div className="skeleton w-20 h-5 rounded-full" />
                    <div className="skeleton w-16 h-5 rounded-full" />
                  </div>
                </div>
                <div className="skeleton w-16 h-4" />
              </div>
            </div>
          ))}
        </div>
      ) : sessions.length === 0 ? (
        <div className="glass-card rounded-2xl p-14 text-center">
          <div className="w-16 h-16 rounded-full bg-ca-bg-secondary flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-ca-fg-muted" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
          </div>
          <p className="text-ca-fg font-medium mb-1">No sessions yet</p>
          <p className="text-sm text-ca-fg-muted mb-6 max-w-sm mx-auto">
            Start your first interview to see your history here.
          </p>
          <Link
            href="/screening"
            className="ca-btn ca-btn-primary inline-flex py-2.5 px-6"
          >
            Start Interview
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </Link>
        </div>
      ) : (
        <ul className="space-y-3 list-none p-0 m-0">
          {sessions.map((s) => (
            <li key={s.session_id}>
              <Link
                href={`/session/${s.session_id}`}
                className="group glass-card rounded-xl p-5 flex items-start gap-4 transition-all duration-200 hover:border-ca-accent/30 card-glow block"
              >
                <div className="min-w-0 flex-1 text-left">
                  <p className="text-sm font-medium text-ca-fg group-hover:text-ca-accent transition-colors leading-snug line-clamp-2">
                    {s.query}
                  </p>
                  <div className="flex flex-wrap items-center gap-2 mt-2.5">
                    <span className="ca-badge ca-badge-accent text-xs">
                      {TYPE_LABELS[s.query_type] || s.query_type}
                    </span>
                    <span className={`ca-badge text-xs ${STATUS_STYLES[s.status] || "ca-badge-accent"}`}>
                      {s.status}
                    </span>
                  </div>
                </div>
                <div className="flex flex-col items-end gap-2 shrink-0">
                  <span className="text-xs text-ca-fg-muted tabular-nums">
                    {new Date(s.created_at).toLocaleDateString(undefined, {
                      month: "short",
                      day: "numeric",
                      year: "numeric",
                    })}
                  </span>
                  <ScorePill sessionId={s.session_id} />
                </div>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
