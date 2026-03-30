"""
Simulation Engine — MiroFish-aligned architecture for career intelligence.

Ported from Debug Arena's simulation.py with career domain adaptations.

Key capabilities:
- PARALLEL agent execution per round (ThreadPoolExecutor)
- SQLite-backed arena with personalized feeds
- ReAct-style tool use: agents CHOOSE which tools to call
- Agent memory: hypotheses and findings persist across rounds
- Adversarial agents: devil's advocate challenges emerging consensus
- Cognitive styles: bayesian, first_principles, contrarian, etc.
- Directive-driven orchestration via ReportAgent
"""

from __future__ import annotations

import json
import random
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from llm_client import LLMClient
from database import CareerDB
from arena import Arena
from tools import get_all_tools
from tools.base import Tool, ToolResult

COGNITIVE_STYLES = [
    {
        "name": "first_principles",
        "instruction": "You think from FIRST PRINCIPLES. Decompose every claim to its fundamentals. Don't accept 'it's always been this way' as evidence. Build analysis from data up — compensation structures, market dynamics, hiring patterns.",
    },
    {
        "name": "bayesian",
        "instruction": "You think like a BAYESIAN REASONER. Assign probabilities to claims, update them as evidence arrives. Say things like 'This shifts my estimate from X to Y because...' Be quantitative about uncertainty.",
    },
    {
        "name": "contrarian",
        "instruction": "You are a CONTRARIAN THINKER. When everyone converges on recommendation X, stress-test it. Ask: What if the opposite is true? What risk is everyone ignoring? You've seen too many career decisions where the obvious answer was wrong.",
    },
    {
        "name": "systems_thinker",
        "instruction": "You are a SYSTEMS THINKER. No career decision exists in isolation — trace the full impact: compensation vs growth vs stability vs learning. Ask: What second-order effects will this choice create in 2-3 years?",
    },
    {
        "name": "empiricist",
        "instruction": "You are a STRICT EMPIRICIST. Trust only MEASURED DATA — salary numbers, company metrics, hiring trends. Dismiss speculation unless backed by concrete data points. Your mantra: 'Show me the numbers.'",
    },
    {
        "name": "pattern_matcher",
        "instruction": "You think by PATTERN MATCHING across careers. For every situation, you recall similar patterns from other companies, roles, and career trajectories. Connect seemingly unrelated data points into actionable insights.",
    },
    {
        "name": "risk_analyst",
        "instruction": "You are a RISK ANALYST. For each recommendation, identify the downside scenarios. What could go wrong? What's the worst case? You ensure no one makes a decision without understanding the full risk profile.",
    },
    {
        "name": "growth_strategist",
        "instruction": "You are a GROWTH STRATEGIST. Focus on learning velocity, skill compounding, and long-term career trajectory. Short-term compensation matters less than the slope of the growth curve. Think in 5-year arcs.",
    },
]

AGENT_SYSTEM_PROMPT = """You are {agent_name}, a career intelligence analyst in a multi-agent debate forum.

## Your Profile
{persona}

## Your Role
Stance: {stance}
{stance_instruction}

## Your Cognitive Style
{cognitive_instruction}

## Focus Areas
{focus_areas}

## Your Current Hypotheses
{hypotheses}

## Key Findings from Previous Cycles
{memory}

## CRITICAL: Independent Thinking Rules
You are an expert analyst. Do NOT simply agree with popular opinions.
- READ every post and comment critically. Just because 3 agents agree doesn't make them right.
- FORM YOUR OWN CONCLUSION based on YOUR domain knowledge and YOUR research.
- If you see a flaw in the majority opinion, CALL IT OUT with evidence.
- If your evidence CONTRADICTS the consensus, present it boldly.
- If you genuinely agree, add NEW supporting evidence, don't just echo.
- CHALLENGE at least one claim from another agent with specific counter-evidence.

## Forum Interaction Rules
1. READ the forum feed carefully, including ALL comments.
2. DO NOT repeat points already made. If someone said what you want to say, LIKE their comment.
3. Reference other agents BY NAME (e.g. "Building on Market Analyst's point...", "I disagree with Comp Strategist...").
4. SPREAD comments across DIFFERENT posts. Don't pile onto the most-discussed thread.
5. LIKE comments you agree with. DISLIKE comments that are technically incorrect.
6. Only CREATE a new post if you have genuinely new information not in ANY existing post.
7. **CITE your sources**: use [Source: ToolName] tags when referencing research.
8. Stay in character as {agent_name}.{adversarial_instruction}"""

STANCE_INSTRUCTIONS = {
    "advocate": "You ADVOCATE for this career path. Present the strongest case with evidence, but honestly flag weaknesses.",
    "skeptic": "You are SKEPTICAL of the easy answers. Probe for hidden risks, unrealistic assumptions, and unstated trade-offs.",
    "investigating": "You are an INVESTIGATOR. Follow the evidence wherever it leads. Challenge weak claims, demand concrete data.",
    "specialist": "You have DEEP domain expertise. Contribute focused analysis within your specialty, connecting to the broader question.",
    "synthesizer": "You are a SYNTHESIZER. Connect dots between what others are saying. Identify contradictions and resolve them.",
}

ADVERSARIAL_INSTRUCTION = """

## CRITICAL: Devil's Advocate Role
You are the designated CHALLENGER. Your job is to:
- Question the emerging consensus and poke holes in recommendations
- Present ALTERNATIVE perspectives others may have overlooked
- Demand stronger evidence — "anecdotal data is not compensation data"
- Highlight risks, downsides, and assumptions others are making
- Be respectfully confrontational — back challenges with evidence
- When 3+ agents agree, dig deeper for flaws
You are NOT trying to be wrong. You are preventing GROUPTHINK."""

REACT_TOOL_PROMPT = """## Available Research Tools
{tool_descriptions}

## Arena Discussion
{feed_snippet}

## Your Current Hypotheses
{hypotheses}

Based on the arena discussion and your expertise as {agent_name}, decide which tools to call.
Think about:
1. What claims in the arena need verification with real data?
2. What salary/company/market data would strengthen your position?
3. What specific information would help answer the user's career question?

Choose 1-3 tool calls. Respond in JSON:
```json
{{
  "reasoning": "What I want to investigate and why",
  "tool_calls": [
    {{"tool": "tool_name", "args": {{"param": "value"}}, "purpose": "what I expect to find"}}
  ]
}}
```

Available tools: {tool_names}
If nothing specific to investigate, return empty tool_calls list."""

PHASE1_PROMPT = """## Arena Feed
{feed}

## Your Research Results (cite with [Source: ToolName])
{tool_results}

## Your Hypotheses from Previous Rounds
{hypotheses}

You have read the arena and researched with your tools.

THINK DEEPLY. Apply your cognitive style:
- What is everyone else MISSING?
- What assumption is the majority making that could be WRONG?
- What evidence from YOUR tools CONTRADICTS the popular recommendation?

Respond in JSON:
```json
{{
  "feed_analysis": "Critical analysis of key points. Who is RIGHT and WRONG and WHY?",
  "contrarian_take": "Strongest argument AGAINST the current consensus",
  "my_new_info": "New information from YOUR tools NOT already in the forum",
  "hypothesis_update": {{
    "current_hypothesis": "Your INDEPENDENT recommendation/conclusion",
    "confidence": "high|medium|low",
    "differs_from_majority": "How your view differs from others",
    "supporting_evidence": ["evidence 1 with [Source: tool]", "evidence 2"],
    "open_questions": ["What still needs investigation?"],
    "what_would_change_my_mind": "What evidence would change your recommendation?"
  }},
  "relevant_posts": [
    {{"post_id": 1, "agent": "name", "my_reaction": "agree|disagree|extend", "why": "reason"}}
  ],
  "relevant_comments": [
    {{"comment_id": 1, "agent": "name", "my_reaction": "agree|disagree", "why": "reason"}}
  ],
  "agents_to_follow": [],
  "search_forum_for": null,
  "should_comment_on": null,
  "should_reply_to_comment": null,
  "should_create_post": false
}}
```

Rules:
- You MUST disagree with at least ONE claim (with evidence).
- SPREAD attention: prefer posts with FEWER comments.
- PREFER should_reply_to_comment over should_comment_on for threaded discussions.
- Set should_create_post ONLY if you have genuinely new info."""

PHASE2_POST_PROMPT = """Write a NEW arena post sharing your unique findings.

Your research results:
{tool_results}

What others have said (summarize to avoid repeating):
{feed_summary}

Your current hypothesis:
{hypothesis}

Rules:
- Must contain information NOT in any existing post or comment
- Reference other agents by name where relevant
- **CITE sources** using [Source: ToolName] tags
- Include specific numbers, data points, company names
- Do NOT repeat what others said — add NEW information
- Write 150-300 words, specific and actionable

Respond with JSON:
```json
{{
  "content": "Your post text with [Source: ToolName] citations"
}}
```"""

PHASE2_COMMENT_PROMPT = """Write a COMMENT replying to Post #{post_id} by {post_author}.

The post:
{post_content}

Existing comments ({num_existing} total — DO NOT repeat):
{existing_comments}

Your research results (cite with [Source: ToolName]):
{tool_results}

Your current hypothesis:
{hypothesis}

Rules:
- There are {num_existing} comments. Read them. Do NOT repeat any point.
- Reference SPECIFIC commenters by name
- **CITE sources** using [Source: ToolName] tags
- If all your points are covered, respond with {{"content": ""}} to stay silent
- Write 80-150 words. Be concise.

Respond with JSON:
```json
{{
  "content": "Your comment text with [Source: ToolName] citations"
}}
```"""

PHASE2_REPLY_PROMPT = """Write a REPLY to Comment #{comment_id} by {comment_author} on Post #{post_id}.

The original post by {post_author}:
{post_content}

The comment you are replying to:
[{comment_author}] (Comment #{comment_id}): {comment_content}

Thread context:
{thread_context}

Your research results (cite with [Source: ToolName]):
{tool_results}

Your current hypothesis:
{hypothesis}

Rules:
- Address {comment_author}'s specific points
- CHALLENGE, EXTEND, or AGREE with supporting evidence
- **CITE sources** using [Source: ToolName] tags
- Be concise — 60-120 words.

Respond with JSON:
```json
{{
  "content": "Your reply text with [Source: ToolName] citations"
}}
```"""


@dataclass
class SimulationAgent:
    agent_id: str
    name: str
    persona: str
    agent_type: str
    tier: int = 2
    lead_type: str = ""
    company: str = ""
    entity_name: str = ""
    entity_type: str = ""
    entity_category: str = ""
    tools: List[str] = field(default_factory=list)
    is_adversarial: bool = False
    stance: str = "investigating"
    cognitive_style: dict = field(default_factory=dict)
    interested_topics: List[str] = field(default_factory=list)
    hypotheses: List[dict] = field(default_factory=list)
    memory: List[str] = field(default_factory=list)
    tool_citations: List[dict] = field(default_factory=list)
    system_prompt: str = ""
    evaluation_focus: str = ""
    heavyweight_role: str = ""
    direction: str = ""  # T1 screeners set this: STRONG/MODERATE/WEAK/RED_FLAG


class Simulation:
    """Career intelligence simulation engine — mirrors Debug Arena's Simulation class.

    Accepts EITHER:
      1. profiles + config (like debug_arena) — creates SimulationAgents from profile dicts
      2. pre-built SimulationAgent list (legacy)
    """

    def __init__(
        self,
        llm: LLMClient,
        db: CareerDB,
        session_id: str,
        agents: Optional[List[SimulationAgent]] = None,
        profiles: Optional[List[dict]] = None,
        config: Optional[dict] = None,
        graph: Optional[dict] = None,
        on_event: Optional[Callable] = None,
        focus_areas: str = "",
    ):
        self.llm = llm
        self.db = db
        self.arena = Arena(db)
        try:
            self.tools = get_all_tools()
        except Exception:
            self.tools = []
        self.tool_map = {t.name: t for t in self.tools}
        self.session_id = session_id
        self._on_event = on_event
        self.focus_areas = focus_areas
        self.config = config or {}
        self.graph = graph or {}

        if profiles and config:
            agent_config_map = {c["agent_id"]: c for c in config.get("agent_configs", [])}
            self.agents = []
            for p in profiles:
                ac = agent_config_map.get(p.get("user_id"), {})
                sa = SimulationAgent(
                    agent_id=str(p.get("user_id", p.get("agent_id", ""))),
                    name=p.get("name", "Unknown"),
                    persona=p.get("persona", p.get("bio", "")),
                    agent_type=p.get("agent_type", ac.get("entity_type", "sub")),
                    entity_name=p.get("entity_name", ac.get("entity_name", "")),
                    entity_type=p.get("entity_type", ac.get("entity_type", "")),
                    entity_category=p.get("entity_category", ""),
                    tools=p.get("tools", []),
                    is_adversarial=ac.get("is_adversarial", False),
                    stance=ac.get("stance", "investigating"),
                    interested_topics=p.get("interested_topics", ac.get("interested_topics", [])),
                )
                self.agents.append(sa)
        elif agents:
            self.agents = agents
        else:
            self.agents = []

        self._assign_adversarial_agents()
        self._assign_cognitive_styles()

        self.agent_map = {a.agent_id: a for a in self.agents}
        self._emit_lock = threading.Lock()
        self.should_stop = False
        self.sim_start_time = time.time()
        self.cycle_number = 0

    def _assign_adversarial_agents(self):
        if len(self.agents) < 3:
            return
        num_adversarial = max(1, len(self.agents) // 5)
        candidates = [a for a in self.agents if not a.is_adversarial]
        if candidates:
            chosen = random.sample(candidates, min(num_adversarial, len(candidates)))
            for agent in chosen:
                agent.is_adversarial = True

    def _assign_cognitive_styles(self):
        styles = list(COGNITIVE_STYLES)
        random.shuffle(styles)
        for i, agent in enumerate(self.agents):
            agent.cognitive_style = styles[i % len(styles)]

    def emit(self, event_type: str, data: Optional[dict] = None):
        if self._on_event:
            with self._emit_lock:
                self._on_event({"type": event_type, **(data or {})})

    def get_tier_agents(self, tier: int) -> List[SimulationAgent]:
        return [a for a in self.agents if a.tier == tier]

    def run_initial_sweep(self):
        """Phase 1: Seed initial posts, then ALL agents run in parallel — ReAct investigate + post."""
        self.emit("sim_start", {
            "agent_count": len(self.agents),
            "tool_count": len(self.tools),
            "adversarial_agents": [a.name for a in self.agents if a.is_adversarial],
        })

        if not self.agents:
            return

        self._seed_initial_posts()
        self.cycle_number = 0

        self.emit("cycle_start", {
            "cycle": 0,
            "phase": "initial_sweep",
            "active_count": len(self.agents),
            "active_agents": [a.name for a in self.agents],
        })

        self._run_round_parallel(self.agents, 0)

        stats = self.arena.get_stats(self.session_id)
        self.emit("cycle_end", {"cycle": 0, "phase": "initial_sweep", **stats})

    def _seed_initial_posts(self):
        """Seed forum with initial posts from config (Debug Arena Stage 3 output)."""
        event_config = self.config.get("event_config", {})
        initial_posts = event_config.get("initial_posts", [])
        if not initial_posts:
            return

        for post in initial_posts:
            agent_id = str(post.get("poster_agent_id", 0))
            agent = self.agent_map.get(agent_id)
            name = agent.name if agent else f"Agent_{agent_id}"
            content = post.get("content", "")
            if not content:
                continue

            self.arena.create_post(
                session_id=self.session_id,
                agent_id=agent_id,
                agent_name=name,
                agent_type=post.get("poster_type", "sub"),
                topic=self.focus_areas[:50] if self.focus_areas else "general",
                content=content,
                post_type="analysis",
                confidence=0.6,
                round_num=0,
            )
            self.emit("forum_post", {
                "round": 0, "post_id": 0,
                "agent_id": agent_id, "agent_name": name,
                "content": content[:100], "seed": True,
            })

    def run_tier1_sweep(self) -> Dict[str, Any]:
        """Run ONLY Tier 1 screeners — fast initial assessment.

        Returns activation signals for Tier 2.
        """
        tier1 = self.get_tier_agents(1)
        if not tier1:
            return {"activate_tier2": False, "signals": {}}

        self.emit("sim_start", {
            "agent_count": len(self.agents),
            "tier_counts": {
                "tier1": len(tier1),
                "tier2": len(self.get_tier_agents(2)),
                "tier3": len(self.get_tier_agents(3)),
            },
            "tool_count": len(self.tools),
            "adversarial_agents": [a.name for a in self.agents if a.is_adversarial],
        })

        self.cycle_number = 0
        self.emit("cycle_start", {
            "cycle": 0,
            "phase": "tier1_sweep",
            "tier": 1,
            "active_count": len(tier1),
            "active_agents": [a.name for a in tier1],
        })

        self._run_round_parallel(tier1, 0)

        stats = self.arena.get_stats(self.session_id)
        self.emit("cycle_end", {"cycle": 0, "phase": "tier1_sweep", **stats})

        return self._evaluate_tier1_signals(tier1)

    def _evaluate_tier1_signals(self, tier1_agents: List[SimulationAgent]) -> Dict[str, Any]:
        """Analyze Tier 1 screener outputs to determine Tier 2 activation.

        Mirrors btc_swarm's T1 alignment check.
        """
        from agent_factory import TIER2_ACTIVATION_PCT, TIER2_MIN_AGREE

        signals = {}
        positive_count = 0
        negative_count = 0
        total_with_signal = 0

        for agent in tier1_agents:
            hyp = self.db.get_latest_hypothesis(agent.agent_id, self.session_id)
            if hyp:
                content = hyp.get("content", "").lower()
                confidence = hyp.get("confidence", "medium")
                signals[agent.name] = {
                    "hypothesis": hyp.get("content", "")[:200],
                    "confidence": confidence,
                }
                total_with_signal += 1

                if confidence == "high" or any(w in content for w in ["strong", "recommend", "good fit", "solid"]):
                    positive_count += 1
                elif any(w in content for w in ["weak", "red flag", "concern", "risk", "poor", "gap"]):
                    negative_count += 1
                else:
                    positive_count += 0.5
                    negative_count += 0.5

        if total_with_signal == 0:
            return {"activate_tier2": True, "signals": signals, "reason": "no_signals_default_activate"}

        dominant = max(positive_count, negative_count)
        pct = dominant / total_with_signal if total_with_signal > 0 else 0

        activate = pct >= TIER2_ACTIVATION_PCT and dominant >= TIER2_MIN_AGREE

        if not activate and total_with_signal >= 3:
            activate = True

        self.emit("tier_activation", {
            "tier": 2,
            "activated": activate,
            "positive": positive_count,
            "negative": negative_count,
            "total": total_with_signal,
            "alignment_pct": round(pct, 2),
            "signals": {k: v["confidence"] for k, v in signals.items()},
        })

        return {
            "activate_tier2": activate,
            "signals": signals,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "alignment_pct": pct,
        }

    def run_tier2_specialists(self, cycle_num: int = 1) -> Dict[str, Any]:
        """Run Tier 2 specialist agents.

        Returns activation signals for Tier 3.
        """
        tier2 = self.get_tier_agents(2)
        if not tier2:
            return {"activate_tier3": False, "signals": {}}

        self.cycle_number = cycle_num
        self.emit("cycle_start", {
            "cycle": cycle_num,
            "phase": "tier2_specialists",
            "tier": 2,
            "active_count": len(tier2),
            "active_agents": [a.name for a in tier2],
        })

        self._run_round_parallel(tier2, cycle_num)

        stats = self.arena.get_stats(self.session_id)
        self.emit("cycle_end", {"cycle": cycle_num, "phase": "tier2_specialists", **stats})

        return self._evaluate_tier2_signals(tier2)

    def _evaluate_tier2_signals(self, tier2_agents: List[SimulationAgent]) -> Dict[str, Any]:
        """Analyze Tier 2 outputs to determine Tier 3 activation."""
        from agent_factory import TIER3_ACTIVATION_PCT, TIER3_MIN_AGREE

        signals = {}
        total_with_signal = 0
        agree_count = 0

        for agent in tier2_agents:
            hyp = self.db.get_latest_hypothesis(agent.agent_id, self.session_id)
            if hyp:
                signals[agent.name] = {
                    "hypothesis": hyp.get("content", "")[:200],
                    "confidence": hyp.get("confidence", "medium"),
                    "category": agent.entity_category,
                }
                total_with_signal += 1
                if hyp.get("confidence") in ("high", "medium"):
                    agree_count += 1

        if total_with_signal == 0:
            return {"activate_tier3": True, "signals": signals, "reason": "no_signals_default_activate"}

        pct = agree_count / total_with_signal if total_with_signal > 0 else 0
        activate = pct >= TIER3_ACTIVATION_PCT and agree_count >= TIER3_MIN_AGREE

        if not activate and total_with_signal >= 3:
            activate = True

        self.emit("tier_activation", {
            "tier": 3,
            "activated": activate,
            "agree_count": agree_count,
            "total": total_with_signal,
            "alignment_pct": round(pct, 2),
        })

        return {
            "activate_tier3": activate,
            "signals": signals,
            "agree_count": agree_count,
            "alignment_pct": pct,
        }

    def run_tier3_debate(self, cycle_num: int = 2, t1_summary: str = "", t2_summary: str = ""):
        """Run Tier 3 heavyweight debate and synthesis.

        Injects summaries from T1 and T2 into the debate context.
        """
        tier3 = self.get_tier_agents(3)
        if not tier3:
            return

        if t1_summary or t2_summary:
            extra_context = "\n\n## Prior Tier Analysis\n"
            if t1_summary:
                extra_context += f"### Tier 1 (Screeners) Summary:\n{t1_summary}\n\n"
            if t2_summary:
                extra_context += f"### Tier 2 (Specialists) Summary:\n{t2_summary}\n\n"
            for agent in tier3:
                agent.memory.append(extra_context)

        self.cycle_number = cycle_num
        self.emit("cycle_start", {
            "cycle": cycle_num,
            "phase": "tier3_debate",
            "tier": 3,
            "active_count": len(tier3),
            "active_agents": [a.name for a in tier3],
        })

        self._run_round_parallel(tier3, cycle_num)

        stats = self.arena.get_stats(self.session_id)
        self.emit("cycle_end", {"cycle": cycle_num, "phase": "tier3_debate", **stats})

    def build_tier_summary(self, tier: int) -> str:
        """Build a text summary of a tier's findings for feeding to next tier."""
        tier_agents = self.get_tier_agents(tier)
        if not tier_agents:
            return ""

        lines = []
        for agent in tier_agents:
            hyp = self.db.get_latest_hypothesis(agent.agent_id, self.session_id)
            findings = self.db.get_agent_memories(
                agent.agent_id, self.session_id, memory_type="finding", limit=3
            )

            agent_summary = f"**{agent.name}** ({agent.entity_category})"
            if hyp:
                agent_summary += f": {hyp['content'][:300]}"
                agent_summary += f" [confidence: {hyp.get('confidence', '?')}]"
            if findings:
                agent_summary += "\n  Key findings: " + "; ".join(f["content"][:150] for f in findings[:2])
            lines.append(agent_summary)

        return "\n".join(lines)

    def run_directed_cycle(self, directives: List[dict], cycle_num: int):
        """Phase 2+: Run ONLY the agents specified by orchestrator directives."""
        self.cycle_number = cycle_num

        target_names = list({d.get("target_agent", d.get("target_agent_name", "")) for d in directives})
        target_names = [n for n in target_names if n]

        active_agents = [a for a in self.agents if a.name in target_names]
        if not active_agents:
            return

        self.emit("cycle_start", {
            "cycle": cycle_num,
            "phase": "directed",
            "active_count": len(active_agents),
            "active_agents": [a.name for a in active_agents],
        })

        self._run_round_parallel(active_agents, cycle_num)

        stats = self.arena.get_stats(self.session_id)
        self.emit("cycle_end", {"cycle": cycle_num, "phase": "directed", **stats})

    def finalize(self):
        """Save agent memory and emit completion."""
        elapsed = time.time() - self.sim_start_time
        stats = self.arena.get_stats(self.session_id)
        self._save_agent_memory()
        self.emit("sim_complete", {"elapsed_s": round(elapsed, 1), "cycles": self.cycle_number, **stats})
        return self.arena

    def _run_round_parallel(self, active_agents: List[SimulationAgent], round_num: int):
        max_concurrent = min(30, len(active_agents))
        shuffled = list(active_agents)
        random.shuffle(shuffled)

        with ThreadPoolExecutor(max_workers=max_concurrent) as pool:
            futures = {
                pool.submit(self._run_agent_turn, agent, round_num): agent
                for agent in shuffled
            }
            for future in as_completed(futures):
                agent = futures[future]
                try:
                    future.result()
                except Exception as e:
                    self.emit("agent_error", {"agent_name": agent.name, "error": str(e)})

    def _run_agent_turn(self, agent: SimulationAgent, round_num: int):
        """Two-phase agent turn with ReAct investigation and memory."""
        keywords = [kw.lower() for kw in agent.interested_topics] if agent.interested_topics else None
        feed = self.arena.get_feed(self.session_id, agent.agent_id, agent_keywords=keywords)

        hypotheses_str = self._format_hypotheses(agent)
        memory_str = self._format_memory(agent)

        directive_str = ""
        pending = self.db.get_pending_directives(self.session_id, agent_id=agent.agent_id)
        if not pending:
            pending = self.db.get_pending_directives(self.session_id, agent_name=agent.name)
        if pending:
            directive_lines = ["\n## PRIORITY TASK FROM ORCHESTRATOR (you MUST address this)"]
            for d in pending[:3]:
                directive_lines.append(f"  >>> {d['task']}")
            directive_str = "\n".join(directive_lines)
            directive_str += "\n\nInvestigate this task using your tools and report findings. This takes priority."

        cognitive = agent.cognitive_style or COGNITIVE_STYLES[0]
        system_prompt = AGENT_SYSTEM_PROMPT.format(
            agent_name=agent.name,
            persona=agent.persona[:1200],
            stance=agent.stance,
            stance_instruction=STANCE_INSTRUCTIONS.get(agent.stance, STANCE_INSTRUCTIONS["investigating"]),
            cognitive_instruction=cognitive["instruction"],
            focus_areas=self.focus_areas or "General career investigation.",
            hypotheses=hypotheses_str,
            memory=memory_str + directive_str,
            adversarial_instruction=ADVERSARIAL_INSTRUCTION if agent.is_adversarial else "",
        )

        self.emit("agent_investigating", {
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "is_adversarial": agent.is_adversarial,
            "has_directive": bool(pending),
        })

        directive_feed = feed
        if pending:
            directive_context = "\n\n=== ORCHESTRATOR DIRECTIVE (PRIORITY) ===\n"
            for d in pending[:3]:
                directive_context += f"Task: {d['task']}\n"
            directive_context += "=== You MUST use tools to address this task ===\n"
            directive_feed = directive_context + feed

        tool_results_str = self._react_investigate(agent, directive_feed, round_num)

        if pending:
            snippet = tool_results_str[:500] if tool_results_str else "Agent completed turn"
            for d in pending[:3]:
                self.db.complete_directive(d["id"], snippet, round_num)

        feed_for_llm = feed[:6000]
        tool_ctx = tool_results_str[:4000] if tool_results_str else "No new research results."

        try:
            phase1 = self.llm.generate_json(
                prompt=PHASE1_PROMPT.format(
                    feed=feed_for_llm,
                    tool_results=tool_ctx,
                    hypotheses=hypotheses_str,
                ),
                system_prompt=system_prompt,
                temperature=0.4,
            )
        except Exception as e:
            self.emit("agent_silent", {
                "round": round_num, "agent_id": agent.agent_id,
                "agent_name": agent.name, "thinking": f"[LLM error: {str(e)[:80]}]",
            })
            return

        should_comment_on = phase1.get("should_comment_on")
        should_reply_to_comment = phase1.get("should_reply_to_comment")
        should_create_post = phase1.get("should_create_post", False)
        feed_analysis = phase1.get("feed_analysis", "")
        my_new_info = phase1.get("my_new_info", "")

        hyp_update = phase1.get("hypothesis_update", {})
        if hyp_update and hyp_update.get("current_hypothesis"):
            evidence = hyp_update.get("supporting_evidence", [])
            open_qs = hyp_update.get("open_questions", [])
            self.db.save_memory(
                self.session_id, agent.agent_id, agent.name, round_num, "hypothesis",
                hyp_update["current_hypothesis"],
                confidence=hyp_update.get("confidence", "medium"),
                evidence=evidence + [f"[open] {q}" for q in open_qs],
            )

        if my_new_info and len(my_new_info) > 20:
            self.db.save_memory(
                self.session_id, agent.agent_id, agent.name, round_num, "finding",
                f"[Round {round_num}] {my_new_info[:500]}",
            )

        search_query = phase1.get("search_forum_for")
        if search_query and isinstance(search_query, str) and len(search_query) > 2:
            search_result = self.arena.search_posts(self.session_id, search_query)
            if search_result and "No posts" not in search_result:
                self.db.save_memory(
                    self.session_id, agent.agent_id, agent.name, round_num, "search_result",
                    f"[Search: '{search_query}'] {search_result[:400]}",
                )

        for follow_name in phase1.get("agents_to_follow", [])[:3]:
            target = next((a for a in self.agents if a.name == follow_name), None)
            if target and target.agent_id != agent.agent_id:
                self.arena.follow_agent(agent.agent_id, target.agent_id, self.session_id,
                                        agent.name, round_num)

        for rp in phase1.get("relevant_posts", []):
            pid = rp.get("post_id")
            reaction = rp.get("my_reaction", "")
            if not pid:
                continue
            try:
                pid = int(pid)
            except (ValueError, TypeError):
                continue
            if reaction == "agree":
                self.arena.like_post(pid, self.session_id, agent.agent_id, agent.name, round_num)
            elif reaction == "disagree":
                self.arena.dislike_post(pid, self.session_id, agent.agent_id, agent.name, round_num)

        for rc in phase1.get("relevant_comments", []):
            cid = rc.get("comment_id")
            reaction = rc.get("my_reaction", "")
            if not cid:
                continue
            try:
                cid = int(cid)
            except (ValueError, TypeError):
                continue
            if reaction == "agree":
                self.arena.like_comment(cid, self.session_id, agent.agent_id, agent.name, round_num)
            elif reaction == "disagree":
                self.arena.dislike_comment(cid, self.session_id, agent.agent_id, agent.name, round_num)

        stats = self.arena.get_stats(self.session_id)
        has_enough_posts = stats["total_posts"] >= 3
        current_hypothesis = hyp_update.get("current_hypothesis", "") if hyp_update else ""

        if should_reply_to_comment and has_enough_posts:
            try:
                reply_cid = int(should_reply_to_comment)
                self._do_reply(agent, round_num, reply_cid, tool_results_str, system_prompt, current_hypothesis)
                return
            except (ValueError, TypeError):
                pass

        if should_comment_on and has_enough_posts:
            try:
                target_pid = int(should_comment_on)
                self._do_comment(agent, round_num, target_pid, tool_results_str, system_prompt, current_hypothesis)
            except (ValueError, TypeError):
                self._do_post(agent, round_num, tool_results_str, feed_analysis, system_prompt, current_hypothesis)
        elif should_create_post or not has_enough_posts:
            self._do_post(agent, round_num, tool_results_str, feed_analysis, system_prompt, current_hypothesis)
        elif tool_results_str and len(tool_results_str) > 100:
            self._do_post(agent, round_num, tool_results_str, feed_analysis, system_prompt, current_hypothesis)
        else:
            self.emit("agent_silent", {
                "round": round_num, "agent_id": agent.agent_id,
                "agent_name": agent.name, "thinking": feed_analysis[:200],
            })

    def _format_hypotheses(self, agent: SimulationAgent) -> str:
        latest = self.db.get_latest_hypothesis(agent.agent_id, self.session_id)
        if not latest:
            return "No hypotheses yet — this is your first round."
        lines = [f"Current hypothesis (confidence: {latest.get('confidence', '?')}): {latest['content']}"]
        try:
            ev = json.loads(latest.get("evidence", "[]"))
        except (json.JSONDecodeError, TypeError):
            ev = []
        if ev:
            lines.append("Evidence: " + "; ".join(str(e) for e in ev[:3]))
        return "\n".join(lines)

    def _format_memory(self, agent: SimulationAgent) -> str:
        findings = self.db.get_agent_memories(agent.agent_id, self.session_id, memory_type="finding", limit=5)
        search_results = self.db.get_agent_memories(agent.agent_id, self.session_id, memory_type="search_result", limit=3)
        memories = findings + search_results
        if not memories:
            return "No prior findings."
        memories.sort(key=lambda m: (m["round_num"], m["id"]))
        return "\n".join(m["content"][:300] for m in memories[-5:])

    def _react_investigate(self, agent: SimulationAgent, feed: str, round_num: int) -> str:
        if not self.tools:
            return ""

        available = [t for t in self.tools if t.name in agent.tools] if agent.tools else self.tools
        if not available:
            available = self.tools

        tool_descriptions = "\n".join(
            f"- **{t.name}**: {t.description} | Params: {', '.join(t.parameters.get('properties', {}).keys())}"
            for t in available
        )
        tool_names = ", ".join(t.name for t in available)

        try:
            plan = self.llm.generate_json(
                prompt=REACT_TOOL_PROMPT.format(
                    tool_descriptions=tool_descriptions,
                    feed_snippet=feed[:2000],
                    hypotheses=self._format_hypotheses(agent),
                    agent_name=agent.name,
                    tool_names=tool_names,
                ),
                system_prompt=f"You are {agent.name}. Choose which research tools to call. Output valid JSON.",
                temperature=0.3,
            )
        except Exception as e:
            self.emit("agent_error", {"agent_name": agent.name, "error": f"ReAct planning: {e}"})
            return ""

        tool_calls = plan.get("tool_calls", [])
        if not tool_calls:
            return ""

        results = []
        for tc in tool_calls[:3]:
            tool_name = tc.get("tool", "")
            args = tc.get("args", {})
            purpose = tc.get("purpose", "")

            tool = self.tool_map.get(tool_name)
            if not tool:
                continue

            args = self._normalize_tool_args(tool, args)

            try:
                r = tool.execute(**args)
                if r.success and r.data:
                    citation = f"[Source: {tool_name}] (Purpose: {purpose})\n{r.data}"
                    results.append(citation)
                    agent.tool_citations.append({
                        "tool": tool_name, "query": str(args),
                        "purpose": purpose, "result_snippet": r.data[:200],
                    })
                    self.db.save_memory(
                        self.session_id, agent.agent_id, agent.name, round_num, "tool_citation",
                        f"[{tool_name}] {purpose}: {r.data[:300]}",
                        source_tool=tool_name,
                    )
                    self.emit("tool_result", {
                        "agent_name": agent.name, "tool": tool_name,
                        "success": True, "snippet": r.data[:100],
                    })
                else:
                    self.emit("tool_result", {
                        "agent_name": agent.name, "tool": tool_name,
                        "success": False, "snippet": r.data[:100] if r.data else "No data",
                    })
            except Exception as e:
                self.emit("tool_result", {
                    "agent_name": agent.name, "tool": tool_name,
                    "success": False, "snippet": str(e)[:100],
                })

        return "\n\n---\n\n".join(results)

    def _normalize_tool_args(self, tool: Tool, args: dict) -> dict:
        schema = tool.parameters
        required = schema.get("required", [])
        properties = schema.get("properties", {})
        normalized = dict(args)
        present = set(normalized.keys())
        missing = [r for r in required if r not in present]
        if not missing:
            return normalized
        generic = [k for k in present if k not in properties]
        if generic and missing:
            for gk in generic:
                if missing:
                    normalized[missing.pop(0)] = normalized.pop(gk)
        return normalized

    def _do_post(self, agent, round_num, tool_results_str, feed_summary, system_prompt, hypothesis=""):
        try:
            result = self.llm.generate_json(
                prompt=PHASE2_POST_PROMPT.format(
                    tool_results=tool_results_str[:3000] if tool_results_str else "No specific research results.",
                    feed_summary=feed_summary[:1000] if feed_summary else "Arena is empty.",
                    hypothesis=hypothesis[:500] if hypothesis else "No specific hypothesis yet.",
                ),
                system_prompt=system_prompt,
                temperature=0.6,
            )
        except Exception as e:
            self.emit("agent_error", {"agent_name": agent.name, "error": f"Post LLM: {e}"})
            return

        content = result.get("content", "")
        if not content:
            return

        topic = "general"
        if agent.company:
            topic = agent.company.lower()
        elif agent.lead_type:
            topic = agent.lead_type

        new_post = self.arena.create_post(
            session_id=self.session_id,
            agent_id=agent.agent_id,
            agent_name=agent.name,
            agent_type=agent.agent_type,
            topic=topic,
            content=content,
            post_type="analysis" if not agent.is_adversarial else "challenge",
            confidence=0.7,
            round_num=round_num,
        )
        self.emit("forum_post", {
            "round": round_num, "post_id": new_post.post_id,
            "agent_id": agent.agent_id, "agent_name": agent.name,
            "content": content[:200], "is_adversarial": agent.is_adversarial,
        })

    def _do_comment(self, agent, round_num, post_id, tool_results_str, system_prompt, hypothesis=""):
        post = self.db.get_post(post_id)
        if not post:
            self._do_post(agent, round_num, tool_results_str, "", system_prompt, hypothesis)
            return

        existing = self.db.get_comments_for_post(post_id)
        num_existing = len(existing)
        existing_str = "\n".join(
            f"- [{c['agent_name']}] (Comment #{c['comment_id']}): {c['content'][:300]}"
            for c in existing[-8:]
        ) if existing else "(No comments yet.)"

        try:
            result = self.llm.generate_json(
                prompt=PHASE2_COMMENT_PROMPT.format(
                    post_id=post_id,
                    post_author=post["agent_name"],
                    post_content=post["content"][:1500],
                    num_existing=num_existing,
                    existing_comments=existing_str[:3000],
                    tool_results=tool_results_str[:2500] if tool_results_str else "No specific results.",
                    hypothesis=hypothesis[:500] if hypothesis else "No specific hypothesis yet.",
                ),
                system_prompt=system_prompt,
                temperature=0.6,
            )
        except Exception:
            return

        content = result.get("content", "")
        if not content:
            return

        comment = self.arena.create_comment(
            session_id=self.session_id, post_id=post_id,
            agent_id=agent.agent_id, agent_name=agent.name,
            content=content, comment_type="analysis", round_num=round_num,
        )
        if comment:
            self.emit("forum_comment", {
                "round": round_num, "post_id": post_id,
                "comment_id": comment.comment_id,
                "agent_name": agent.name, "content": content[:200],
            })

    def _do_reply(self, agent, round_num, comment_id, tool_results_str, system_prompt, hypothesis=""):
        target = self.db.get_comment(comment_id)
        if not target:
            return

        post = self.db.get_post(target["post_id"])
        if not post:
            return

        chain = self.db.get_thread_chain(comment_id)
        thread_lines = []
        for c in reversed(chain[1:]):
            thread_lines.append(f"[{c['agent_name']}] (Comment #{c['comment_id']}): {c['content'][:200]}")
        thread_context = "\n".join(thread_lines) if thread_lines else "(Top-level comment.)"

        try:
            result = self.llm.generate_json(
                prompt=PHASE2_REPLY_PROMPT.format(
                    comment_id=comment_id,
                    comment_author=target["agent_name"],
                    comment_content=target["content"][:1000],
                    post_id=target["post_id"],
                    post_author=post["agent_name"],
                    post_content=post["content"][:800],
                    thread_context=thread_context,
                    tool_results=tool_results_str[:2500] if tool_results_str else "No specific results.",
                    hypothesis=hypothesis[:500] if hypothesis else "No specific hypothesis.",
                ),
                system_prompt=system_prompt,
                temperature=0.6,
            )
        except Exception:
            return

        content = result.get("content", "")
        if not content:
            return

        reply = self.arena.create_comment(
            session_id=self.session_id, post_id=target["post_id"],
            agent_id=agent.agent_id, agent_name=agent.name,
            content=content, comment_type="reply", round_num=round_num,
            parent_comment_id=comment_id,
        )
        if reply:
            self.emit("forum_comment", {
                "round": round_num, "post_id": target["post_id"],
                "comment_id": reply.comment_id,
                "parent_comment_id": comment_id,
                "agent_name": agent.name, "content": content[:200],
            })

    def _save_agent_memory(self):
        for agent in self.agents:
            latest_hyp = self.db.get_latest_hypothesis(agent.agent_id, self.session_id)
            findings = self.db.get_agent_memories(agent.agent_id, self.session_id, memory_type="finding", limit=10)
            memory_data = {
                "hypotheses": [{"hypothesis": latest_hyp["content"], "confidence": latest_hyp.get("confidence")}] if latest_hyp else [],
                "memory": [f["content"] for f in findings],
                "tool_citations": agent.tool_citations,
                "is_adversarial": agent.is_adversarial,
            }
            self.db.set_meta(f"agent_memory_{agent.agent_id}", json.dumps(memory_data))
