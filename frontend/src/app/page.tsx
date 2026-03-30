"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence, useScroll, useTransform } from "framer-motion";
import ScrollReveal from "@/components/ScrollReveal";
import StaggerContainer, { itemVariants as staggerItemVariants } from "@/components/StaggerContainer";
import AnimatedCounter from "@/components/AnimatedCounter";
import HeroBackground from "@/components/HeroBackground";

// ─── Agents in the system ───
const agents = {
  screening: { name: "Kavitha", role: "Screening Agent", color: "#7c3aed", initial: "K" },
  tech: { name: "Arjun Mehta", role: "Tech Interviewer", color: "#2563eb", initial: "AM" },
  hr: { name: "Priya Sharma", role: "HR Lead", color: "#059669", initial: "PS" },
  manager: { name: "Meera Krishnan", role: "Hiring Manager", color: "#d97706", initial: "MK" },
};

// ─── Demo sequence: screening → forum → interview ───
type DemoStep =
  | { phase: "screening"; speaker: string; content: string }
  | { phase: "forum"; posts: { agent: keyof typeof agents; content: string; isReply?: boolean }[] }
  | { phase: "interview"; agent: keyof typeof agents; content: string; label: string }
  | { phase: "verdict"; result: string };

const demoSequence: DemoStep[] = [
  // 1. Screening
  {
    phase: "screening",
    speaker: "Kavitha",
    content: "Tell me about your strongest project and what technologies you used.",
  },
  // 2. Forum — agents discuss the candidate
  {
    phase: "forum",
    posts: [
      { agent: "screening", content: "Candidate has strong Node.js skills, built a 10K rps platform. Weak on system design theory." },
      { agent: "tech", content: "I'll probe the Redis architecture decisions. His caching approach needs deeper validation." },
      { agent: "hr", content: "Communication is confident. Will test team conflict scenarios in my round." },
    ],
  },
  // 3. Tech round
  {
    phase: "interview",
    agent: "tech",
    label: "Round 1 — Technical",
    content: "Walk me through how you'd design the caching layer if you had to handle 100K rps instead of 10K.",
  },
  // 4. Forum update after tech round
  {
    phase: "forum",
    posts: [
      { agent: "tech", content: "Good practical instincts but struggled with CAP theorem trade-offs. Score: 6.5/10" },
      { agent: "manager", content: "Noted. I'll focus on how he handles ambiguity in requirements — that's the real gap." },
    ],
  },
  // 5. HR round
  {
    phase: "interview",
    agent: "hr",
    label: "Round 2 — Behavioral",
    content: "Tell me about a time you disagreed with your team lead. How did you handle it?",
  },
  // 6. Final verdict
  {
    phase: "verdict",
    result: "Recommended for SDE-1 with mentorship plan for system design growth.",
  },
];

const features = [
  {
    title: "Screening Agent",
    description:
      "Kavitha profiles your skills, experience, and personality — then builds a customized interview panel just for you.",
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
      </svg>
    ),
    badge: "Step 1",
    color: "#7c3aed",
    gradient: "from-violet-500/10 to-purple-500/10",
  },
  {
    title: "Agent Forum",
    description:
      "Interviewers discuss your answers behind the scenes — sharing insights, adjusting questions, and building a complete picture together.",
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
      </svg>
    ),
    badge: "Unique",
    color: "#10b981",
    gradient: "from-emerald-500/10 to-teal-500/10",
  },
  {
    title: "Adaptive Interviews",
    description:
      "Each interviewer reads the forum before their round — so questions adapt based on what others discovered about you.",
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 0 0-2.455 2.456Z" />
      </svg>
    ),
    badge: "AI-Powered",
    color: "#f59e0b",
    gradient: "from-amber-500/10 to-orange-500/10",
  },
];

const interviewTypes = [
  { name: "Campus Placement", desc: "Screening + Tech + HR + Manager panel", turns: 24, icon: "🎓" },
  { name: "Senior Tech", desc: "Deep system design + leadership assessment", turns: 30, icon: "💻" },
  { name: "Stress Interview", desc: "High-pressure with tough interviewers", turns: 24, icon: "🔥" },
  { name: "UPSC Board", desc: "Chairman + 2 board members", turns: 30, icon: "🏛️" },
  { name: "HR Round", desc: "Behavioral STAR interview", turns: 20, icon: "🤝" },
  { name: "Tech Deep Dive", desc: "Two senior engineers, coding focus", turns: 26, icon: "⚙️" },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] as [number, number, number, number] } },
};

// ─── Live Demo — Screening → Forum → Interview Flow ───
function LiveDemoPreview() {
  const [stepIdx, setStepIdx] = useState(-1);
  const [forumPostIdx, setForumPostIdx] = useState(-1); // for staggering forum posts

  useEffect(() => {
    const timers: ReturnType<typeof setTimeout>[] = [];
    let t = 800;

    const runSequence = () => {
      demoSequence.forEach((step, i) => {
        if (step.phase === "forum") {
          // Show forum container first
          timers.push(setTimeout(() => {
            setStepIdx(i);
            setForumPostIdx(-1);
          }, t));
          t += 400;
          // Stagger each forum post
          step.posts.forEach((_, postIdx) => {
            timers.push(setTimeout(() => setForumPostIdx(postIdx), t));
            t += 900;
          });
          t += 600;
        } else {
          timers.push(setTimeout(() => {
            setStepIdx(i);
            setForumPostIdx(-1);
          }, t));
          t += step.phase === "verdict" ? 3000 : 2800;
        }
      });
    };

    runSequence();

    // Loop
    const loopDelay = t + 2000;
    const loop = setInterval(() => {
      setStepIdx(-1);
      setForumPostIdx(-1);
      t = 800;
      runSequence();
    }, loopDelay);

    return () => {
      timers.forEach(clearTimeout);
      clearInterval(loop);
    };
  }, []);

  const currentStep = stepIdx >= 0 ? demoSequence[stepIdx] : null;

  return (
    <div className="glass-card rounded-2xl overflow-hidden shadow-lg demo-container">
      {/* Window chrome */}
      <div className="flex items-center gap-2 px-5 py-3 border-b border-ca-border/50">
        <span className="w-3 h-3 rounded-full bg-red-400" />
        <span className="w-3 h-3 rounded-full bg-yellow-400" />
        <span className="w-3 h-3 rounded-full bg-green-400" />
        <span className="ml-3 text-sm text-ca-fg-muted font-medium">
          CareerArena — Live Interview
        </span>
        <div className="ml-auto flex items-center gap-1 text-xs text-ca-fg-muted">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          Live
        </div>
      </div>

      {/* Phase indicator */}
      <div className="flex items-center gap-2 px-5 py-2.5 border-b border-ca-border/30 bg-ca-bg-secondary/50">
        {(["Screening", "Forum", "Interview", "Verdict"] as const).map((phase, i) => {
          const phaseMap = { Screening: "screening", Forum: "forum", Interview: "interview", Verdict: "verdict" };
          const isActive = currentStep?.phase === phaseMap[phase] ||
            (phase === "Interview" && currentStep?.phase === "interview") ||
            (phase === "Forum" && currentStep?.phase === "forum");
          const isPast = currentStep ? demoSequence.indexOf(currentStep) >
            demoSequence.findIndex(s => s.phase === phaseMap[phase]) : false;
          return (
            <div key={phase} className="flex items-center gap-2">
              {i > 0 && <div className={`w-4 h-px ${isPast || isActive ? "bg-ca-accent" : "bg-ca-border"}`} />}
              <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full transition-all duration-300 ${
                isActive
                  ? "bg-ca-accent/10 text-ca-accent"
                  : isPast
                  ? "text-ca-fg-muted"
                  : "text-ca-fg-muted/50"
              }`}>
                {phase}
              </span>
            </div>
          );
        })}
      </div>

      {/* Content area */}
      <div className="min-h-[300px] relative">
        <AnimatePresence mode="wait">
          {/* ── Screening Phase ── */}
          {currentStep?.phase === "screening" && (
            <motion.div
              key="screening"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
              className="p-5 space-y-4"
            >
              {/* Active agent spotlight */}
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div
                    className="w-12 h-12 rounded-full flex items-center justify-center text-white text-base font-bold spotlight-avatar"
                    style={{
                      backgroundColor: agents.screening.color,
                      boxShadow: `0 0 20px ${agents.screening.color}30`,
                    }}
                  >
                    {agents.screening.initial}
                  </div>
                  <div className="absolute -bottom-1 left-1/2 -translate-x-1/2">
                    <div className="speaking-indicator">
                      <span style={{ background: agents.screening.color }} />
                      <span style={{ background: agents.screening.color }} />
                      <span style={{ background: agents.screening.color }} />
                    </div>
                  </div>
                </div>
                <div>
                  <div className="text-sm font-semibold">{agents.screening.name}</div>
                  <div className="text-xs text-ca-fg-muted">{agents.screening.role}</div>
                </div>
              </div>
              {/* Message */}
              <div className="bubble-interviewer px-4 py-3 ml-2">
                <p className="text-sm leading-relaxed">{currentStep.content}</p>
              </div>
              {/* Candidate typing */}
              <div className="flex justify-end">
                <div className="bubble-candidate px-4 py-3 text-sm">
                  I built a microservices platform handling 10K rps using Node.js and Redis...
                </div>
              </div>
            </motion.div>
          )}

          {/* ── Forum Phase ── */}
          {currentStep?.phase === "forum" && (
            <motion.div
              key={`forum-${stepIdx}`}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.3 }}
              className="p-5"
            >
              <div className="flex items-center gap-2 mb-3">
                <div className="w-5 h-5 rounded bg-emerald-500/10 flex items-center justify-center">
                  <svg className="w-3 h-3 text-emerald-500" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242" />
                  </svg>
                </div>
                <span className="text-xs font-semibold text-emerald-600">Agent Forum</span>
                <span className="text-[10px] text-ca-fg-muted">— behind the scenes</span>
              </div>

              <div className="space-y-2.5">
                {currentStep.posts.map((post, i) => {
                  const agent = agents[post.agent];
                  return (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -12 }}
                      animate={i <= forumPostIdx ? { opacity: 1, x: 0 } : { opacity: 0, x: -12 }}
                      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
                      className="flex gap-2.5"
                    >
                      <div
                        className="w-7 h-7 rounded-full flex-shrink-0 flex items-center justify-center text-white text-[10px] font-bold mt-0.5"
                        style={{ backgroundColor: agent.color }}
                      >
                        {agent.initial}
                      </div>
                      <div className="flex-1 bg-ca-bg-secondary/80 border border-ca-border/50 rounded-lg px-3 py-2">
                        <div className="flex items-center gap-2 mb-0.5">
                          <span className="text-[11px] font-semibold">{agent.name}</span>
                          <span className="text-[10px] text-ca-fg-muted">{agent.role}</span>
                        </div>
                        <p className="text-xs text-ca-fg-secondary leading-relaxed">{post.content}</p>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>
          )}

          {/* ── Interview Phase ── */}
          {currentStep?.phase === "interview" && (
            <motion.div
              key={`interview-${stepIdx}`}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
              className="p-5 space-y-4"
            >
              {/* Round label */}
              <div className="flex items-center gap-2">
                <span className="ca-badge ca-badge-accent text-[10px]">{currentStep.label}</span>
                <span className="text-[10px] text-ca-fg-muted">Reading forum insights...</span>
              </div>
              {/* Active interviewer */}
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div
                    className="w-12 h-12 rounded-full flex items-center justify-center text-white text-base font-bold spotlight-avatar"
                    style={{
                      backgroundColor: agents[currentStep.agent].color,
                      boxShadow: `0 0 20px ${agents[currentStep.agent].color}30`,
                    }}
                  >
                    {agents[currentStep.agent].initial}
                  </div>
                  <div className="absolute -bottom-1 left-1/2 -translate-x-1/2">
                    <div className="speaking-indicator">
                      <span style={{ background: agents[currentStep.agent].color }} />
                      <span style={{ background: agents[currentStep.agent].color }} />
                      <span style={{ background: agents[currentStep.agent].color }} />
                    </div>
                  </div>
                </div>
                <div>
                  <div className="text-sm font-semibold">{agents[currentStep.agent].name}</div>
                  <div className="text-xs text-ca-fg-muted">{agents[currentStep.agent].role}</div>
                </div>
                {/* Other agents — dimmed, listening */}
                <div className="ml-auto flex items-center gap-1.5">
                  {Object.entries(agents)
                    .filter(([key]) => key !== currentStep.agent)
                    .map(([key, a]) => (
                      <div
                        key={key}
                        className="w-6 h-6 rounded-full flex items-center justify-center text-white text-[8px] font-bold opacity-25"
                        style={{ backgroundColor: a.color }}
                        title={`${a.name} — observing`}
                      >
                        {a.initial}
                      </div>
                    ))}
                </div>
              </div>
              {/* Question */}
              <div className="bubble-interviewer px-4 py-3 ml-2">
                <p className="text-sm leading-relaxed">{currentStep.content}</p>
              </div>
            </motion.div>
          )}

          {/* ── Verdict Phase ── */}
          {currentStep?.phase === "verdict" && (
            <motion.div
              key="verdict"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
              className="p-5 flex flex-col items-center justify-center min-h-[280px] text-center"
            >
              <div className="w-14 h-14 rounded-full bg-emerald-500/10 flex items-center justify-center mb-4">
                <svg className="w-7 h-7 text-emerald-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                </svg>
              </div>
              <p className="text-xs text-ca-fg-muted mb-2">Panel Consensus</p>
              <p className="text-sm font-medium text-ca-fg max-w-[260px] leading-relaxed">
                {currentStep.result}
              </p>
              {/* Agent avatars in agreement */}
              <div className="flex items-center gap-2 mt-4">
                {Object.values(agents).map((a) => (
                  <div
                    key={a.name}
                    className="w-8 h-8 rounded-full flex items-center justify-center text-white text-[10px] font-bold"
                    style={{ backgroundColor: a.color }}
                  >
                    {a.initial}
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {/* ── Initial state ── */}
          {!currentStep && (
            <motion.div
              key="initial"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="p-5 flex items-center justify-center min-h-[300px]"
            >
              <div className="text-center">
                <div className="flex items-center justify-center gap-3 mb-3">
                  {Object.values(agents).map((a) => (
                    <div
                      key={a.name}
                      className="w-10 h-10 rounded-full flex items-center justify-center text-white text-xs font-bold opacity-40"
                      style={{ backgroundColor: a.color }}
                    >
                      {a.initial}
                    </div>
                  ))}
                </div>
                <p className="text-xs text-ca-fg-muted">Assembling interview panel...</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default function HomePage() {
  const heroRef = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ["start start", "end start"],
  });
  const heroY = useTransform(scrollYProgress, [0, 1], [0, 80]);
  const heroOpacity = useTransform(scrollYProgress, [0, 0.8], [1, 0]);

  return (
    <div className="mesh-gradient animated-dots">
      {/* Hero */}
      <section ref={heroRef} className="relative max-w-6xl mx-auto px-4 sm:px-6 pt-16 sm:pt-24 pb-16">
        <HeroBackground />
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left: Copy */}
          <motion.div
            style={{ y: heroY, opacity: heroOpacity }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-ca-border bg-ca-bg/50 text-sm text-ca-fg-secondary mb-6 shimmer">
              <span className="w-2 h-2 rounded-full bg-ca-success animate-pulse" />
              Powered by Multi-Agent AI
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-display font-extrabold tracking-tight leading-[1.08] mb-6">
              AI interviewers that{" "}
              <span className="gradient-text-hero">talk to each other</span>
            </h1>

            <p className="text-lg text-ca-fg-secondary max-w-xl mb-8 leading-relaxed">
              A screening agent profiles you. Interview agents discuss your answers in a private forum.
              Each round adapts based on what the panel discovered — just like a real TCS, Infosys, or Wipro placement.
            </p>

            {/* Mobile demo — prominent, right after description */}
            <div className="lg:hidden mb-8">
              <div className="flex items-center gap-2 mb-3">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500" />
                </span>
                <span className="text-xs font-medium text-ca-fg-muted">See it in action</span>
              </div>
              <LiveDemoPreview />
              <p className="text-center text-[10px] text-ca-fg-muted mt-2">Auto-playing demo</p>
            </div>

            <div className="flex flex-col sm:flex-row items-start gap-3 mb-10">
              <a
                href="/screening"
                className="ca-btn ca-btn-primary text-base py-3 px-7 rounded-lg shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/30 transition-shadow"
              >
                Start Interview
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
                </svg>
              </a>
              <a
                href="/interview"
                className="ca-btn ca-btn-secondary text-base py-3 px-7 rounded-lg"
              >
                Quick Panel Interview
              </a>
            </div>

            {/* Stats */}
            <div className="flex items-center gap-6 sm:gap-8">
              <div>
                <div className="text-xl font-bold text-ca-fg"><AnimatedCounter target={8} suffix="+" /></div>
                <div className="text-xs text-ca-fg-muted">Agent Types</div>
              </div>
              <div>
                <div className="text-xl font-bold text-ca-fg"><AnimatedCounter target={10} suffix="+" /></div>
                <div className="text-xs text-ca-fg-muted">Company Profiles</div>
              </div>
              <div>
                <div className="text-xl font-bold text-ca-fg"><AnimatedCounter target={6} /></div>
                <div className="text-xs text-ca-fg-muted">Interview Formats</div>
              </div>
              <div>
                <div className="text-xl font-bold text-ca-fg">Real-time</div>
                <div className="text-xs text-ca-fg-muted">AI Responses</div>
              </div>
            </div>
          </motion.div>

          {/* Right: Live Demo */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.7 }}
            className="hidden lg:block"
          >
            <LiveDemoPreview />
          </motion.div>
        </div>

      </section>

      {/* Trust bar */}
      <ScrollReveal className="max-w-4xl mx-auto px-4 sm:px-6 pb-16">
        <div className="flex flex-col sm:flex-row items-center justify-center gap-6 sm:gap-10 py-5 px-6 rounded-2xl border border-ca-border/60 bg-ca-bg/50 backdrop-blur-sm">
          <div className="flex items-center gap-2 text-sm">
            <span className="w-8 h-8 rounded-full bg-indigo-500/10 flex items-center justify-center">
              <svg className="w-4 h-4 text-indigo-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
              </svg>
            </span>
            <span className="font-semibold text-ca-fg">500+</span>
            <span className="text-ca-fg-secondary">Mock Interviews</span>
          </div>
          <div className="hidden sm:block w-px h-6 bg-ca-border" />
          <div className="flex items-center gap-2 text-sm">
            <span className="w-8 h-8 rounded-full bg-emerald-500/10 flex items-center justify-center">
              <svg className="w-4 h-4 text-emerald-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
              </svg>
            </span>
            <span className="font-semibold text-ca-fg">50+</span>
            <span className="text-ca-fg-secondary">Students Practicing</span>
          </div>
          <div className="hidden sm:block w-px h-6 bg-ca-border" />
          <div className="flex items-center gap-2 text-sm">
            <span className="w-8 h-8 rounded-full bg-amber-500/10 flex items-center justify-center">
              <svg className="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a23.838 23.838 0 0 0-1.012 5.434c-.073.477.056.955.4 1.29a23.88 23.88 0 0 0 4.494 3.39c.343.22.757.287 1.14.173a23.907 23.907 0 0 0 3.48-1.486M4.26 10.147A48.354 48.354 0 0 1 12 4.28a48.354 48.354 0 0 1 7.74 5.867M12 4.28v.01" />
              </svg>
            </span>
            <span className="text-ca-fg-secondary">Built for Campus Placements</span>
          </div>
        </div>
      </ScrollReveal>

      {/* How it works — the flow */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 pb-20">
        <ScrollReveal>
          <h2 className="text-3xl font-display font-extrabold text-center mb-3">How it works</h2>
          <p className="text-ca-fg-secondary text-center mb-12 max-w-lg mx-auto">
            Not just Q&A — a full multi-agent system where interviewers coordinate behind the scenes
          </p>
        </ScrollReveal>

          <StaggerContainer className="grid sm:grid-cols-4 gap-6">
            {[
              {
                step: "1",
                title: "Screening",
                desc: "Kavitha understands your background, skills, and goals through a friendly conversation",
                color: "#7c3aed",
                icon: (
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                  </svg>
                ),
              },
              {
                step: "2",
                title: "Panel Created",
                desc: "Custom interviewers are generated based on YOUR profile — different for every candidate",
                color: "#2563eb",
                icon: (
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" />
                  </svg>
                ),
              },
              {
                step: "3",
                title: "Interview Rounds",
                desc: "Each interviewer conducts their round, posts feedback to the forum for others to see",
                color: "#059669",
                icon: (
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
                  </svg>
                ),
              },
              {
                step: "4",
                title: "Verdict",
                desc: "HR reads the full forum, conducts final round, and delivers the panel consensus",
                color: "#d97706",
                icon: (
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
                ),
              },
            ].map((s) => (
              <motion.div
                key={s.step}
                variants={staggerItemVariants}
                className="text-center"
              >
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-3 text-white shadow-lg"
                  style={{
                    backgroundColor: s.color,
                    boxShadow: `0 4px 14px ${s.color}25`,
                  }}
                >
                  {s.icon}
                </div>
                <div className="inline-flex items-center gap-1.5 text-xs text-ca-fg-muted mb-2">
                  <span
                    className="w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold text-white"
                    style={{ backgroundColor: s.color }}
                  >
                    {s.step}
                  </span>
                </div>
                <h3 className="text-sm font-semibold mb-1.5">{s.title}</h3>
                <p className="text-xs text-ca-fg-secondary leading-relaxed">{s.desc}</p>
              </motion.div>
            ))}
          </StaggerContainer>
      </section>

      {/* Features */}
      <section id="features" className="max-w-6xl mx-auto px-4 sm:px-6 pb-20 section-decoration-indigo">
        <ScrollReveal className="text-center mb-12">
          <h2 className="text-3xl font-display font-extrabold mb-3">What makes this different</h2>
          <p className="text-ca-fg-secondary max-w-xl mx-auto">
            Not just a chatbot asking questions — a coordinated panel of AI agents
          </p>
        </ScrollReveal>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid md:grid-cols-3 gap-6"
        >
          {features.map((f) => (
            <motion.div
              key={f.title}
              variants={itemVariants}
              className="feature-card p-6"
            >
              <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 bg-gradient-to-br ${f.gradient}`}>
                <div style={{ color: f.color }}>{f.icon}</div>
              </div>
              <div className="flex items-center gap-2 mb-2">
                <h3 className="text-lg font-semibold">{f.title}</h3>
                <span className="ca-badge ca-badge-accent text-xs">{f.badge}</span>
              </div>
              <p className="text-sm text-ca-fg-secondary leading-relaxed">{f.description}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="max-w-6xl mx-auto px-4 sm:px-6 pb-20">
        <ScrollReveal className="text-center mb-12">
          <h2 className="text-3xl font-display font-extrabold mb-3">Students who leveled up</h2>
          <p className="text-ca-fg-secondary max-w-xl mx-auto">
            Real results from students who practiced with CareerArena
          </p>
        </ScrollReveal>

        <StaggerContainer className="grid md:grid-cols-3 gap-6">
          {[
            {
              quote: "The panel interview simulation was exactly like my TCS Digital interview. The forum feature showed me how interviewers actually coordinate — I walked in prepared and got placed!",
              name: "Ananya Krishnan",
              college: "KPR Institute, Coimbatore",
              year: "2025 Batch",
              badge: "Placed at TCS Digital",
              badgeColor: "bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400",
              gradient: "from-violet-500 to-purple-500",
            },
            {
              quote: "My first mock score was 4/10. After practicing different interview types and getting specific feedback, I improved to 8.5/10 in just three weeks. The AI adapts to exactly where you're weak.",
              name: "Ravi Shankar M",
              college: "Hindusthan College, Coimbatore",
              year: "2025 Batch",
              badge: "Score: 4/10 to 8.5/10",
              badgeColor: "bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400",
              gradient: "from-blue-500 to-indigo-500",
            },
            {
              quote: "The stress interview mode prepared me for the hardest questions. When the actual Infosys panel asked tough follow-ups, I was calm and ready. Best preparation tool I've used.",
              name: "Divya Lakshmi S",
              college: "SNS College, Coimbatore",
              year: "2025 Batch",
              badge: "Placed at Infosys",
              badgeColor: "bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400",
              gradient: "from-emerald-500 to-teal-500",
            },
          ].map((t) => (
            <motion.div key={t.name} variants={staggerItemVariants} className="glass-card rounded-2xl p-6 relative">
              {/* Quote mark */}
              <svg className="absolute top-4 right-4 w-8 h-8 text-ca-accent/10" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10H14.017zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10H0z" />
              </svg>
              <p className="text-sm text-ca-fg-secondary leading-relaxed mb-5">&ldquo;{t.quote}&rdquo;</p>
              <div className="flex items-center gap-3">
                <div className={`w-10 h-10 rounded-full bg-gradient-to-br ${t.gradient} flex items-center justify-center text-white text-sm font-bold`}>
                  {t.name.split(" ").map(w => w[0]).join("").slice(0, 2)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-ca-fg">{t.name}</p>
                  <p className="text-xs text-ca-fg-muted">{t.college} &middot; {t.year}</p>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-ca-border/50">
                <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${t.badgeColor}`}>
                  {t.badge}
                </span>
              </div>
            </motion.div>
          ))}
        </StaggerContainer>
      </section>

      {/* Interview Types */}
      <section id="types" className="max-w-5xl mx-auto px-4 sm:px-6 pb-20 section-decoration-emerald">
        <ScrollReveal>
          <h2 className="text-3xl font-display font-extrabold text-center mb-3">Choose your interview type</h2>
          <p className="text-ca-fg-secondary text-center mb-10 max-w-lg mx-auto">
            Preset configurations for every scenario — from campus placement to UPSC board
          </p>
        </ScrollReveal>

          <StaggerContainer className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {interviewTypes.map((t) => (
              <motion.a
                key={t.name}
                variants={staggerItemVariants}
                href="/interview"
                className="type-card p-5 group cursor-pointer block"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{t.icon}</span>
                    <div>
                      <h3 className="font-semibold group-hover:text-ca-accent transition-colors">{t.name}</h3>
                      <p className="text-sm text-ca-fg-muted mt-0.5">{t.desc}</p>
                    </div>
                  </div>
                  <svg
                    className="w-4 h-4 text-ca-fg-muted opacity-0 type-card-arrow transition-all mt-1"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth={2}
                    stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
                  </svg>
                </div>
                <div className="flex items-center gap-2 mt-3 ml-11">
                  <span className="text-xs text-ca-fg-muted">{t.turns} turns max</span>
                </div>
              </motion.a>
            ))}
          </StaggerContainer>
      </section>

      {/* CTA */}
      <section id="cta" className="max-w-4xl mx-auto px-4 sm:px-6 pb-20 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.97 }}
          whileInView={{ opacity: 1, y: 0, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="relative rounded-2xl overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 via-violet-500 to-emerald-500" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,rgba(255,255,255,0.15),transparent_60%)]" />
          <div className="absolute inset-0 cta-dot-pattern" />
          <div className="relative p-8 sm:p-14">
            <h2 className="text-2xl sm:text-3xl font-display font-extrabold mb-3 text-white">Your placement journey starts here</h2>
            <p className="text-indigo-100 mb-8 max-w-lg mx-auto">
              Free to try. No sign-up needed. Practice as many times as you want and walk into your interview with confidence.
            </p>
            <a
              href="/screening"
              className="inline-flex items-center gap-2 bg-white text-indigo-600 font-semibold text-base py-3 px-8 rounded-lg hover:bg-indigo-50 transition-colors shadow-lg"
            >
              Start Interview
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
              </svg>
            </a>
          </div>
        </motion.div>
      </section>

    </div>
  );
}
