"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { getSession, type SessionStatus } from "@/lib/api";
import ReportView from "@/components/ReportView";
import ArenaView from "@/components/ArenaView";
import StatusStream from "@/components/StatusStream";

type Tab = "report" | "arena";

export default function SessionPage() {
  const params = useParams();
  const sessionId = params.id as string;
  const [session, setSession] = useState<SessionStatus | null>(null);
  const [error, setError] = useState("");
  const [tab, setTab] = useState<Tab>("arena");
  const prevStatusRef = useRef<string>("");

  const fetchSession = useCallback(async () => {
    try {
      const data = await getSession(sessionId);
      setSession(data);

      if (prevStatusRef.current === "running" && data.status === "completed" && data.report) {
        setTab("report");
      }
      prevStatusRef.current = data.status;
      return data.status;
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load session");
      return "error";
    }
  }, [sessionId]);

  useEffect(() => {
    void fetchSession();
    const interval = setInterval(async () => {
      const status = await fetchSession();
      if (status === "completed" || status === "error") clearInterval(interval);
    }, 2000);
    return () => clearInterval(interval);
  }, [fetchSession]);

  if (error) {
    return (
      <div className="max-w-lg mx-auto text-center py-24 px-4">
        <div className="ca-card p-10">
          <div className="w-12 h-12 rounded-full bg-red-50 flex items-center justify-center mx-auto mb-4">
            <svg className="w-6 h-6 text-red-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
            </svg>
          </div>
          <p className="text-sm font-semibold text-red-600 mb-2">Something went wrong</p>
          <p className="text-ca-fg-muted mb-8 leading-relaxed">{error}</p>
          <Link href="/" className="ca-btn ca-btn-primary">
            Back to home
          </Link>
        </div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="flex flex-col items-center justify-center py-28 gap-4">
        <LoadingSpinner />
        <p className="text-sm text-ca-fg-muted">Loading session...</p>
      </div>
    );
  }

  const isRunning = session.status === "running";
  const isComplete = session.status === "completed";
  const hasPosts = (session.arena_stats?.total_posts ?? 0) > 0;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-6">
      {/* Header */}
      <div className="mb-8 md:mb-10">
        <Link href="/" className="inline-flex items-center gap-2 text-xs font-medium text-ca-fg-muted hover:text-ca-accent transition-colors mb-5">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
          </svg>
          New query
        </Link>

        <div className="flex flex-wrap items-center gap-2 mb-4">
          <StatusBadge status={session.status} />
          <span className="ca-badge ca-badge-accent">
            {session.query_type}
          </span>
          {session.companies.map((c) => (
            <span key={c} className="ca-badge" style={{ background: "var(--accent-light)", color: "var(--accent)" }}>
              {c}
            </span>
          ))}
        </div>

        <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-ca-fg leading-snug">
          {session.query}
        </h1>

        <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-4 text-xs text-ca-fg-muted font-mono">
          <span className="truncate max-w-full" title={session.session_id}>{session.session_id}</span>
          {session.elapsed_seconds != null && <span>{session.elapsed_seconds}s</span>}
          {session.arena_stats && (
            <>
              <span>{session.arena_stats.active_agents} agents</span>
              <span>{session.arena_stats.total_posts} posts</span>
              <span>{session.arena_stats.total_comments} comments</span>
            </>
          )}
        </div>
      </div>

      {/* Live status panel */}
      {isRunning && (
        <LivePanel sessionId={sessionId} status={session.status} arenaStats={session.arena_stats} />
      )}

      {/* Tabs */}
      {(isComplete || hasPosts || isRunning) && (
        <div className="inline-flex p-1 rounded-lg bg-ca-bg-secondary border border-ca-border mb-8" role="tablist">
          <TabButton active={tab === "arena"} onClick={() => setTab("arena")}>
            {isRunning && <span className="inline-block w-2 h-2 rounded-full bg-ca-accent mr-2 animate-pulse" aria-hidden />}
            Arena
            {session.arena_stats != null && (
              <span className="ml-2 text-[11px] opacity-50 tabular-nums">({session.arena_stats.total_posts})</span>
            )}
          </TabButton>
          <TabButton active={tab === "report"} onClick={() => setTab("report")}>
            Report
            {!session.report && isRunning && <span className="ml-2 text-[11px] opacity-40">synthesizing...</span>}
          </TabButton>
        </div>
      )}

      {tab === "report" && session.report && <ReportView report={session.report} />}
      {tab === "report" && !session.report && (
        <div className="ca-card p-12 text-center">
          {isRunning ? (
            <>
              <LoadingSpinner />
              <p className="text-sm text-ca-fg-muted max-w-sm mx-auto leading-relaxed mt-4">
                Agents are synthesizing findings. Watch the arena for live reasoning.
              </p>
              <button type="button" onClick={() => setTab("arena")} className="mt-6 text-sm font-medium text-ca-accent hover:text-ca-accent-hover transition-colors">
                Watch the arena
              </button>
            </>
          ) : (
            <p className="text-ca-fg-muted">No report available for this session.</p>
          )}
        </div>
      )}
      {tab === "arena" && <ArenaView sessionId={sessionId} status={session.status} />}
    </div>
  );
}

function LivePanel({
  sessionId,
  status,
  arenaStats,
}: {
  sessionId: string;
  status: string;
  arenaStats: SessionStatus["arena_stats"];
}) {
  return (
    <div className="ca-card p-5 md:p-6 mb-8 bg-gradient-to-br from-indigo-500/5 to-emerald-500/5">
      <div className="flex items-center gap-3 mb-5">
        <div className="relative">
          <div className="w-10 h-10 rounded-full bg-ca-accent/10 flex items-center justify-center">
            <svg className="w-5 h-5 text-ca-accent animate-spin-slow" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 0 0-2.455 2.456Z" />
            </svg>
          </div>
          <span className="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-400 animate-pulse" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-ca-fg">Agents investigating</h3>
          <p className="text-xs text-ca-fg-muted mt-0.5">
            Agents are probing, debating, and synthesizing findings
          </p>
        </div>
      </div>

      {arenaStats && (
        <div className="grid grid-cols-3 gap-3 mb-4">
          <StatCard label="Active Agents" value={arenaStats.active_agents} />
          <StatCard label="Findings" value={arenaStats.total_posts} />
          <StatCard label="Debates" value={arenaStats.total_comments} />
        </div>
      )}

      <StatusStream sessionId={sessionId} status={status} />
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-lg px-3 py-3 text-center bg-ca-bg border border-ca-border">
      <div className="text-xl font-bold text-ca-accent tabular-nums">{value}</div>
      <div className="text-[10px] text-ca-fg-muted uppercase tracking-widest font-semibold mt-1">{label}</div>
    </div>
  );
}

function LoadingSpinner() {
  return (
    <div className="relative w-16 h-16 flex items-center justify-center">
      <div className="absolute inset-0 rounded-full border-2 border-ca-border border-t-ca-accent animate-spin" />
      <svg className="w-6 h-6 text-ca-accent" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
      </svg>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    running: "bg-indigo-50 text-indigo-600 border-indigo-200",
    completed: "bg-emerald-50 text-emerald-600 border-emerald-200",
    error: "bg-red-50 text-red-600 border-red-200",
    pending: "bg-amber-50 text-amber-600 border-amber-200",
  };

  return (
    <span className={`text-[11px] px-2.5 py-1 rounded-full font-semibold border uppercase tracking-wide ${styles[status] || styles.pending}`}>
      {status === "running" && <span className="inline-block w-1.5 h-1.5 rounded-full bg-indigo-500 mr-2 align-middle animate-pulse" aria-hidden />}
      {status}
    </span>
  );
}

function TabButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      role="tab"
      aria-selected={active}
      onClick={onClick}
      className={`px-5 py-2.5 rounded-md text-sm font-medium transition-all duration-200 flex items-center ${
        active
          ? "bg-ca-bg text-ca-fg shadow-sm border border-ca-border"
          : "text-ca-fg-muted hover:text-ca-fg border border-transparent"
      }`}
    >
      {children}
    </button>
  );
}
