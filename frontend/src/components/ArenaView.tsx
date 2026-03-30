"use client";

import { useEffect, useState, useRef } from "react";
import { getArena, type ArenaPost, type ArenaComment } from "@/lib/api";
import AgentBadge from "./AgentBadge";
import ConfidenceMeter from "./ConfidenceMeter";

interface Props {
  sessionId: string;
  status?: string;
}

const TOPIC_COLORS: Record<string, string> = {
  compensation: "border-l-emerald-400",
  compensation_lead: "border-l-emerald-400",
  market_intel_lead: "border-l-sky-400",
  interview_coach_lead: "border-l-amber-400",
  skills_gap_lead: "border-l-violet-400",
  profile_analyst: "border-l-cyan-400",
  contrarian_challenge: "border-l-orange-400",
  contrarian: "border-l-orange-400",
  general: "border-l-violet-400/50",
};

function getTopicColor(topic: string): string {
  return TOPIC_COLORS[topic] || TOPIC_COLORS.general;
}

function CommentThread({ comment, allComments }: { comment: ArenaComment; allComments: ArenaComment[] }) {
  const [collapsed, setCollapsed] = useState(false);
  const replies = allComments.filter((c) => c.parent_comment_id === comment.comment_id);
  const isChallenge = comment.comment_type === "challenge";

  return (
    <div className="ml-3 sm:ml-4 mt-3">
      <div className={`pl-3 border-l-2 ${isChallenge ? "border-orange-500/30" : "border-violet-500/10"}`}>
        <div className="flex items-center gap-2 mb-1.5 flex-wrap">
          <AgentBadge agentType="sub" agentName={comment.agent_name} />
          {isChallenge && (
            <span className="text-[10px] px-2 py-0.5 rounded-md bg-orange-500/10 text-orange-300 font-bold uppercase tracking-wide border border-orange-500/20">
              🛡️ Challenge
            </span>
          )}
          {replies.length > 0 && (
            <button
              type="button"
              onClick={() => setCollapsed(!collapsed)}
              className="text-[10px] font-mono text-violet-300/40 hover:text-cyan-300"
            >
              {collapsed ? `[+${replies.length}]` : "[−]"}
            </button>
          )}
        </div>
        <p className="text-sm leading-relaxed text-[var(--foreground-subtle)] whitespace-pre-wrap">{comment.content}</p>
      </div>
      {!collapsed && replies.map((reply) => (
        <CommentThread key={reply.comment_id} comment={reply} allComments={allComments} />
      ))}
    </div>
  );
}

function PostCard({ post, isNew }: { post: ArenaPost; isNew: boolean }) {
  const [expanded, setExpanded] = useState(true);
  const [contentExpanded, setContentExpanded] = useState(false);
  const topLevelComments = post.comments.filter((c) => !c.parent_comment_id);
  const isContrarian = post.post_type === "challenge" || post.topic === "contrarian_challenge" || post.topic === "contrarian";
  const isLong = post.content.length > 600;
  const displayContent = isLong && !contentExpanded ? post.content.slice(0, 600) + "..." : post.content;

  return (
    <article
      className={`octopus-card overflow-hidden border-l-4 ${
        isContrarian ? "border-l-orange-400" : getTopicColor(post.topic)
      } ${isNew ? "animate-slide-up ring-1 ring-cyan-500/30" : "animate-fade-in"}`}
    >
      <div className="p-4 md:p-5">
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-3">
          <div className="flex items-center gap-2 flex-wrap">
            <AgentBadge
              agentType={post.agent_type}
              agentName={post.agent_name}
              isAdversarial={isContrarian}
            />
            <span className="text-[10px] px-2 py-0.5 rounded-md bg-violet-500/5 border border-violet-500/10 text-violet-300/60 font-mono">
              #{post.topic}
            </span>
            {post.post_type !== "analysis" && (
              <span className="text-[10px] px-2 py-0.5 rounded-md bg-cyan-500/5 border border-cyan-500/10 text-cyan-300/60">
                {post.post_type}
              </span>
            )}
            {isNew && (
              <span className="text-[10px] px-2 py-0.5 rounded-md bg-cyan-500/10 text-cyan-300 font-bold uppercase tracking-wide animate-biolum">
                New
              </span>
            )}
          </div>
          <div className="flex items-center gap-4 shrink-0">
            <ConfidenceMeter value={post.confidence} />
            {post.comments.length > 0 && (
              <button
                type="button"
                onClick={() => setExpanded(!expanded)}
                className="text-xs font-medium text-violet-300/40 hover:text-cyan-300 transition-colors"
              >
                {expanded ? "Collapse" : `${post.comments.length} replies`}
              </button>
            )}
          </div>
        </div>

        <div className="text-sm md:text-[15px] leading-relaxed text-[var(--foreground-subtle)] whitespace-pre-wrap break-words overflow-x-hidden">
          {displayContent}
        </div>

        {isLong && (
          <button
            type="button"
            onClick={() => setContentExpanded(!contentExpanded)}
            className="mt-2 text-xs font-medium text-cyan-400/70 hover:text-cyan-300 transition-colors"
          >
            {contentExpanded ? "Show less ↑" : "Read more ↓"}
          </button>
        )}

        <div className="flex items-center gap-4 mt-4 text-[11px] font-mono text-violet-300/30">
          <span>R{post.round_num}</span>
          {post.likes > 0 && <span className="text-cyan-400/50">▲ {post.likes}</span>}
          {post.dislikes > 0 && <span className="text-orange-400/50">▼ {post.dislikes}</span>}
          {post.comments.length > 0 && <span>{post.comments.length} replies</span>}
        </div>
      </div>

      {expanded && topLevelComments.length > 0 && (
        <div className="border-t border-violet-500/10 p-4 md:p-5 bg-violet-950/20">
          {topLevelComments.map((comment) => (
            <CommentThread key={comment.comment_id} comment={comment} allComments={post.comments} />
          ))}
        </div>
      )}
    </article>
  );
}

export default function ArenaView({ sessionId, status }: Props) {
  const [posts, setPosts] = useState<ArenaPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("all");
  const [newIds, setNewIds] = useState<Set<number>>(new Set());
  const isRunning = status === "running";
  const isInitialArenaLoadRef = useRef(true);
  const knownPostIdsRef = useRef<Set<number>>(new Set());

  useEffect(() => {
    isInitialArenaLoadRef.current = true;
    knownPostIdsRef.current = new Set();
    setLoading(true);

    async function load() {
      try {
        const data = await getArena(sessionId);
        const incoming = data.posts || [];
        setPosts(incoming);

        if (isInitialArenaLoadRef.current) {
          knownPostIdsRef.current = new Set(incoming.map((p) => p.post_id));
          isInitialArenaLoadRef.current = false;
        } else {
          const fresh = incoming.filter((p) => !knownPostIdsRef.current.has(p.post_id));
          if (fresh.length > 0) {
            setNewIds(new Set(fresh.map((p) => p.post_id)));
            knownPostIdsRef.current = new Set(incoming.map((p) => p.post_id));
            setTimeout(() => setNewIds(new Set()), 4000);
          }
        }
      } catch {
        /* ignore */
      } finally {
        setLoading(false);
      }
    }

    void load();

    if (isRunning) {
      const poll = setInterval(() => void load(), 3000);
      return () => clearInterval(poll);
    }
  }, [sessionId, isRunning]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16 gap-3">
        <div className="relative w-12 h-12 flex items-center justify-center">
          <div className="absolute inset-0 rounded-full border-2 border-violet-500/20 border-t-cyan-400 animate-spin" />
          <span className="text-lg">🐙</span>
        </div>
        <p className="text-sm text-violet-300/50">Tentacles reaching out...</p>
      </div>
    );
  }

  if (posts.length === 0) {
    return (
      <div className="octopus-card p-12 text-center bg-gradient-to-br from-violet-500/5 to-transparent">
        {isRunning ? (
          <>
            <div className="relative w-12 h-12 flex items-center justify-center mx-auto mb-4">
              <div className="absolute inset-0 rounded-full border-2 border-violet-500/20 border-t-cyan-400 animate-spin" />
              <span className="text-lg animate-swim">🐙</span>
            </div>
            <p className="text-sm font-medium text-[var(--foreground-subtle)] mb-1">Arms deploying...</p>
            <p className="text-xs text-violet-300/40 max-w-sm mx-auto leading-relaxed">
              The octopus is extending its tentacles. Findings and debates will stream in here.
            </p>
          </>
        ) : (
          <p className="text-sm text-violet-300/40">No arena activity for this session.</p>
        )}
      </div>
    );
  }

  const topics = Array.from(new Set(posts.map((p) => p.topic)));
  const filtered = filter === "all" ? posts : posts.filter((p) => p.topic === filter);

  return (
    <div className="space-y-5">
      {isRunning && (
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 font-medium text-cyan-300">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-biolum" aria-hidden />
            🐙 Live
          </span>
          <span className="text-violet-300/40">
            {posts.length} finding{posts.length !== 1 ? "s" : ""} — tentacles probing every few seconds
          </span>
        </div>
      )}

      <div className="flex items-center gap-2 flex-wrap">
        <FilterChip active={filter === "all"} onClick={() => setFilter("all")} count={posts.length}>
          All
        </FilterChip>
        {topics.map((topic) => (
          <FilterChip key={topic} active={filter === topic} onClick={() => setFilter(topic)} count={posts.filter((p) => p.topic === topic).length}>
            #{topic}
          </FilterChip>
        ))}
      </div>

      <div className="space-y-4">
        {filtered.map((post) => (
          <PostCard key={post.post_id} post={post} isNew={newIds.has(post.post_id)} />
        ))}
      </div>
    </div>
  );
}

function FilterChip({ active, onClick, count, children }: { active: boolean; onClick: () => void; count: number; children: React.ReactNode }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`text-xs px-3.5 py-1.5 rounded-full border font-medium transition-all duration-200 ${
        active
          ? "bg-violet-500/15 border-violet-500/30 text-cyan-200"
          : "border-violet-500/10 text-violet-300/40 hover:text-cyan-300/60 hover:border-violet-500/20"
      }`}
    >
      {children}{" "}
      <span className="tabular-nums opacity-60">({count})</span>
    </button>
  );
}
