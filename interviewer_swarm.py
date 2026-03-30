"""
Interviewer Swarm — the multi-agent brain behind each interviewer.

Each interviewer in the panel is NOT a single LLM call. Instead, each is
backed by 8-10 debate agents in a mini-arena. The agents debate what to
ask, the orchestrator reads the forum, and synthesizes the best question.

Architecture:
  Candidate Answer
       │
       ▼
  ┌─────────────────────────────────────┐
  │  SWARM FORUM (mini-arena)           │
  │                                     │
  │  DepthProber: "Probe B-tree index"  │
  │  BSDetector: "They dropped buzzword"│
  │  EmpathyReader: "Getting nervous"   │
  │  DevilsAdvocate: "Actually strong"  │
  │  CrossReferrer: "Contradicts T2"    │
  │  ...8-10 agents debating...         │
  └──────────────┬──────────────────────┘
                 │
       ┌─────────▼─────────┐
       │ SWARM ORCHESTRATOR │
       │ Reads all posts,   │
       │ synthesizes ONE     │
       │ perfect question    │
       └─────────┬─────────┘
                 │
                 ▼
       Question + Confidence + Emotional Read

Reuses MiroFish patterns:
  - ThreadPoolExecutor for parallel agent execution (simulation.py)
  - Forum-based debate (arena.py)
  - Orchestrator reads forum + synthesizes (report_agent.py)
"""

from __future__ import annotations

import json
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from llm_client import LLMClient
from interviewer_personas import InterviewerPersona
from candidate_model import CandidateModel


# ═══════════════════════════════════════════════════════
# SWARM AGENT DEFINITIONS
# ═══════════════════════════════════════════════════════

@dataclass
class SwarmAgent:
    """A debate agent inside an interviewer's swarm."""
    agent_id: str
    name: str
    role: str  # e.g. "Depth Prober", "BS Detector", "Empathy Reader"
    instruction: str  # What this agent does and how it thinks
    is_adversarial: bool = False


# ─── Tech Interviewer's internal swarm ───

TECH_SWARM = [
    SwarmAgent(
        agent_id="tech_depth",
        name="Depth Prober",
        role="depth_prober",
        instruction=(
            "Your job is to find the BOUNDARY of the candidate's knowledge. "
            "If they said something confidently, propose a follow-up that goes ONE level deeper. "
            "For databases: if they know SQL, probe indexing. If they know indexing, probe query planning. "
            "Post the specific question that will reveal whether they TRULY know or are bluffing."
        ),
    ),
    SwarmAgent(
        agent_id="tech_system",
        name="System Thinker",
        role="system_thinker",
        instruction=(
            "Think about architecture and system design. When the candidate describes a project, "
            "identify the design decisions they made (or didn't mention). Propose questions about "
            "scalability, failure modes, trade-offs. 'What happens when this gets 100x traffic?' "
            "'Why not use X instead of Y?'"
        ),
    ),
    SwarmAgent(
        agent_id="tech_bs",
        name="BS Detector",
        role="bs_detector",
        instruction=(
            "Watch for buzzwords without substance. If the candidate says 'microservices' — "
            "did they actually build one or just read about it? If they say 'event-driven architecture' — "
            "can they explain backpressure? Propose questions that separate real experience from resume padding. "
            "Be specific: 'They said X — ask them to explain Y which anyone who actually used X would know.'"
        ),
    ),
    SwarmAgent(
        agent_id="tech_practical",
        name="Practical Eye",
        role="practical_experience",
        instruction=(
            "Focus on whether this person has BUILT things or just studied them. "
            "Look for passive voice ('the system was built') vs active ('I designed and deployed'). "
            "Propose questions about debugging stories, production incidents, deployment processes. "
            "Real builders have war stories. Textbook learners don't."
        ),
    ),
    SwarmAgent(
        agent_id="tech_cross",
        name="Cross Referrer",
        role="cross_referrer",
        instruction=(
            "Your job is to connect the current answer to PREVIOUS answers. "
            "Look for contradictions: 'Earlier they said they work alone, now they say team of 4.' "
            "Look for opportunities: 'They mentioned Redis in answer 2 — connect that to this database discussion.' "
            "Propose questions that test consistency and holistic understanding."
        ),
    ),
    SwarmAgent(
        agent_id="tech_empathy",
        name="Empathy Reader",
        role="empathy_reader",
        instruction=(
            "Read the candidate's EMOTIONAL state from their response patterns. "
            "Are they getting shorter answers? More hedge words? Losing confidence? "
            "Or are they warming up and getting more detailed? "
            "ADVISE the orchestrator: should we push harder or give them a confidence boost? "
            "If they're crumbling, suggest moving to a topic they're stronger on. "
            "If they're overconfident, suggest a harder challenge."
        ),
    ),
    SwarmAgent(
        agent_id="tech_benchmark",
        name="Industry Benchmarker",
        role="industry_benchmarker",
        instruction=(
            "Compare this candidate's knowledge level to what's ACTUALLY expected for their role/level. "
            "For a fresher at TCS: is this above or below average? For SDE-2 at Google: is this competitive? "
            "Calibrate the other agents — if they're pushing too hard for a junior role, say so. "
            "If the candidate is punching above their weight, flag that too."
        ),
    ),
    SwarmAgent(
        agent_id="tech_devil",
        name="Devil's Advocate",
        role="devils_advocate",
        instruction=(
            "Challenge the OTHER AGENTS. If Depth Prober says 'they're weak on databases', "
            "counter with evidence from the transcript. If BS Detector flags something, defend the candidate. "
            "Your job is to prevent pile-on and ensure FAIR assessment. "
            "But if the evidence really is damning, agree and add your own concerns."
        ),
        is_adversarial=True,
    ),
]


# ─── HR Interviewer's internal swarm ───

HR_SWARM = [
    SwarmAgent(
        agent_id="hr_authenticity",
        name="Authenticity Detector",
        role="authenticity_detector",
        instruction=(
            "Spot rehearsed vs genuine answers. YouTube-coached answers have telltale patterns: "
            "perfect STAR structure, generic 'weaknesses' that are actually strengths. "
            "Propose follow-ups that break the candidate out of rehearsed mode. "
            "'That sounds well-prepared — can you give me a DIFFERENT example, off the top of your head?'"
        ),
    ),
    SwarmAgent(
        agent_id="hr_motivation",
        name="Motivation Analyst",
        role="motivation_analyst",
        instruction=(
            "Assess WHY this person wants this role. Generic enthusiasm ('great company!') vs "
            "specific motivation ('I read about your data pipeline rewrite and...'). "
            "Propose questions that reveal genuine interest vs mass-applying. "
            "Also probe: is this a career step or are they just desperate?"
        ),
    ),
    SwarmAgent(
        agent_id="hr_culture",
        name="Culture Fit Agent",
        role="culture_fit",
        instruction=(
            "Listen for VALUES alignment. How do they talk about past managers? Past teams? "
            "Do they blame others or take ownership? Do they value collaboration or independence? "
            "Propose questions about conflict: 'Tell me about a disagreement with a teammate.' "
            "The HOW they describe it matters more than WHAT happened."
        ),
    ),
    SwarmAgent(
        agent_id="hr_redflags",
        name="Red Flag Agent",
        role="red_flag_detector",
        instruction=(
            "Watch for red flags: unexplained gaps, frequent job changes, badmouthing previous employers, "
            "inability to describe specific contributions, evasive about reasons for leaving. "
            "Don't be paranoid — not every gap is bad. But flag things worth probing. "
            "Propose GENTLE ways to ask about flags without putting the candidate on trial."
        ),
    ),
    SwarmAgent(
        agent_id="hr_empathy",
        name="Empathy Reader",
        role="empathy_reader",
        instruction=(
            "Read the emotional temperature. Is the candidate comfortable? Nervous? "
            "Opening up or shutting down? Watch for signs of interview fatigue. "
            "If they were strong early but fading now, suggest the orchestrator give them "
            "an easy question to rebuild confidence before the final assessment."
        ),
    ),
    SwarmAgent(
        agent_id="hr_growth",
        name="Growth Mindset Agent",
        role="growth_mindset",
        instruction=(
            "Assess learning ability and self-awareness. Do they know what they DON'T know? "
            "Can they describe how they learned something new? Do they take feedback well? "
            "Propose questions about failure: 'What's the biggest thing you got wrong and what did you learn?' "
            "Watch for deflection vs genuine reflection."
        ),
    ),
    SwarmAgent(
        agent_id="hr_stress",
        name="Stress Response Agent",
        role="stress_response",
        instruction=(
            "How does this candidate handle pressure? When challenged, do they get defensive, "
            "deflect, or engage thoughtfully? Rate their composure. "
            "If they haven't been tested yet, suggest a mildly challenging scenario. "
            "If they've already been stressed, assess their recovery."
        ),
    ),
    SwarmAgent(
        agent_id="hr_devil",
        name="Devil's Advocate",
        role="devils_advocate",
        instruction=(
            "Challenge the other agents' assessments. If Red Flag Agent flags a gap, "
            "maybe it was a sabbatical or caretaking — don't assume the worst. "
            "If Authenticity Detector says 'rehearsed', maybe the candidate is just well-prepared — "
            "that's a GOOD thing. Ensure fair, balanced assessment."
        ),
        is_adversarial=True,
    ),
]


# ─── VP / Leadership Interviewer's internal swarm ───

VP_SWARM = [
    SwarmAgent(
        agent_id="vp_ownership",
        name="Ownership Detector",
        role="ownership_detector",
        instruction=(
            "Does this person take OWNERSHIP or are they a task-executor? "
            "Look for: 'I was asked to do X' vs 'I identified the problem and proposed X'. "
            "Probe with: 'What would you have done differently?' 'How did you decide to do it that way?'"
        ),
    ),
    SwarmAgent(
        agent_id="vp_strategic",
        name="Strategic Thinker",
        role="strategic_thinker",
        instruction=(
            "Can this person think BEYOND their immediate task? Do they understand business context? "
            "Probe with ambiguous scenarios: 'The PM wants feature X but engineering capacity is limited. "
            "What do you do?' Look for trade-off thinking, not just 'I would work harder.'"
        ),
    ),
    SwarmAgent(
        agent_id="vp_impact",
        name="Impact Assessor",
        role="impact_assessor",
        instruction=(
            "Ask about OUTCOMES, not activities. 'You built X — what IMPACT did it have?' "
            "Watch for measurable results vs vague claims ('improved performance'). "
            "If they can't quantify impact, they probably weren't tracking it — that tells you something."
        ),
    ),
    SwarmAgent(
        agent_id="vp_empathy",
        name="Empathy Reader",
        role="empathy_reader",
        instruction=(
            "Read emotional dynamics from a leadership lens. How does the candidate respond "
            "when their ideas are challenged? Do they double down, listen, or capitulate? "
            "Leaders need conviction WITH openness. Flag which pattern you see."
        ),
    ),
    SwarmAgent(
        agent_id="vp_people",
        name="People Lens",
        role="people_management",
        instruction=(
            "How does this person work with PEOPLE? Listen for how they describe teammates, "
            "juniors, managers. Do they mentor? Do they give credit? Do they handle conflict constructively? "
            "Propose scenarios about team dynamics."
        ),
    ),
    SwarmAgent(
        agent_id="vp_devil",
        name="Devil's Advocate",
        role="devils_advocate",
        instruction=(
            "Some candidates are strong individual contributors, not leaders — and that's OK. "
            "Don't penalize them for not being a manager if the role doesn't require it. "
            "Challenge the other agents if they're setting the bar too high for the role level."
        ),
        is_adversarial=True,
    ),
]


# ─── UPSC Board's internal swarm ───

UPSC_SWARM = [
    SwarmAgent(
        agent_id="upsc_current",
        name="Current Affairs Analyst",
        role="current_affairs",
        instruction=(
            "Assess depth of current affairs knowledge. Not just 'do they know the news' but "
            "'can they analyze implications?' Propose questions connecting recent events to governance, "
            "policy, or the candidate's optional subject."
        ),
    ),
    SwarmAgent(
        agent_id="upsc_opinion",
        name="Opinion Tester",
        role="opinion_tester",
        instruction=(
            "UPSC boards test whether candidates have OPINIONS and can defend them. "
            "Propose opinion-based questions: 'Should India ban...?' 'Is the reservation policy...?' "
            "Then suggest a counter-argument to see if they can handle dissent."
        ),
    ),
    SwarmAgent(
        agent_id="upsc_ethics",
        name="Ethics Analyst",
        role="ethics",
        instruction=(
            "Civil servants face ethical dilemmas daily. Propose scenario-based ethics questions: "
            "'Your senior officer asks you to do something you believe is wrong. What do you do?' "
            "Look for nuance — not simplistic 'I would refuse' but understanding of practical realities."
        ),
    ),
    SwarmAgent(
        agent_id="upsc_india",
        name="India Awareness Agent",
        role="india_awareness",
        instruction=(
            "Assess understanding of India's diversity, challenges, and governance structure. "
            "Connect questions to the candidate's home state, optional subject, or work experience. "
            "'How is [issue] different in your state vs nationally?'"
        ),
    ),
    SwarmAgent(
        agent_id="upsc_empathy",
        name="Empathy Reader",
        role="empathy_reader",
        instruction=(
            "UPSC boards are respectful but probing. Read whether the candidate is handling "
            "the board's tone well. Are they being too deferential? Too argumentative? "
            "The ideal is confident but respectful. Advise the orchestrator."
        ),
    ),
    SwarmAgent(
        agent_id="upsc_devil",
        name="Devil's Advocate",
        role="devils_advocate",
        instruction=(
            "Challenge the board's assumptions. If other agents pile on a weak area, "
            "remind them that UPSC personality test is about personality — not just knowledge. "
            "A candidate who says 'I don't know but here's how I'd find out' deserves credit."
        ),
        is_adversarial=True,
    ),
]


# ─── Map interviewer roles to swarm profiles ───

SWARM_PROFILES: Dict[str, List[SwarmAgent]] = {
    "HR Lead": HR_SWARM,
    "Technical Lead": TECH_SWARM,
    "VP Engineering": VP_SWARM,
    "VP Eng": VP_SWARM,
    "Senior Director": VP_SWARM,
    "Domain Expert": TECH_SWARM,  # Adapts via persona context
    "Chairman": UPSC_SWARM,
    "Board Member (Current Affairs)": UPSC_SWARM,
    "Board Member (Domain)": UPSC_SWARM,
}


# ═══════════════════════════════════════════════════════
# SWARM FORUM (lightweight in-memory arena per turn)
# ═══════════════════════════════════════════════════════

@dataclass
class SwarmPost:
    """A single post in the swarm's internal debate forum."""
    agent_id: str
    agent_name: str
    role: str
    content: str
    timestamp: float = 0.0

    def to_text(self) -> str:
        return f"[{self.agent_name} ({self.role})]: {self.content}"


class SwarmForum:
    """In-memory forum for one turn's debate. Created fresh each turn."""

    def __init__(self):
        self.posts: List[SwarmPost] = []

    def add_post(self, agent_id: str, agent_name: str, role: str, content: str):
        self.posts.append(SwarmPost(
            agent_id=agent_id,
            agent_name=agent_name,
            role=role,
            content=content,
            timestamp=time.time(),
        ))

    def build_feed(self) -> str:
        if not self.posts:
            return "(No debate yet)"
        return "\n\n".join(p.to_text() for p in self.posts)

    def get_posts(self) -> List[SwarmPost]:
        return list(self.posts)


# ═══════════════════════════════════════════════════════
# INTERVIEWER SWARM
# ═══════════════════════════════════════════════════════

SWARM_AGENT_PROMPT = """You are {agent_name}, a specialist analyst inside an interviewer's mind.

YOUR ROLE: {role}
YOUR INSTRUCTION: {instruction}

The interviewer ({interviewer_name}, {interviewer_role}) just heard the candidate's answer.
Your job: analyze the answer from YOUR specific lens and post your analysis + recommended question to the forum.

## Candidate's Answer
{candidate_answer}

## Interview Transcript (recent)
{transcript}

## Candidate Model (what we know so far)
{candidate_model}

## Other Agents' Posts (read and respond to these)
{forum_feed}

Post your analysis and recommend what question the interviewer should ask next.
Be specific, concise (100-200 words). If you disagree with another agent, say so directly.

Respond in JSON:
```json
{{
  "analysis": "Your analysis of the candidate's answer from your specific lens",
  "recommended_question": "The specific question you think the interviewer should ask",
  "confidence": 0.0-1.0,
  "emotional_advisory": "If you're the Empathy Reader: advice on tone/difficulty adjustment. Otherwise: empty string",
  "flags": ["any red flags or notable observations"]
}}
```"""


SWARM_SYNTHESIZE_PROMPT = """You are {interviewer_name}, {interviewer_role}.

Your internal team of {num_agents} analysts just debated what you should ask next.
Read their debate and synthesize the ONE BEST question.

## Your Personality
{personality_brief}

## Analyst Debate Forum
{forum_feed}

## Emotional Advisory
{emotional_advisory}

## Candidate Model
{candidate_model}

## Coverage Gaps (dimensions NOT YET assessed)
{coverage_gaps}

RULES:
1. Pick the STRONGEST question from the debate — don't average them
2. Adjust tone based on the Empathy Reader's advice
3. Stay in character as {interviewer_name}
4. Ask exactly ONE question, under 150 words
5. If an analyst flagged a contradiction, you MUST address it
6. Reference previous answers when relevant

Respond in JSON:
```json
{{
  "question": "The final synthesized question you will ask",
  "turn_type": "follow_up | challenge | cross_reference | new_question | clarification",
  "confidence": 0.0-1.0,
  "reasoning": "Why this question, what you expect to learn",
  "emotional_calibration": "How you adjusted based on the emotional read"
}}
```"""


@dataclass
class SwarmOutput:
    """The output of a swarm's deliberation."""
    question: str
    turn_type: str
    confidence: float
    reasoning: str
    emotional_calibration: str
    debate_posts: List[SwarmPost]
    elapsed_seconds: float = 0.0


class InterviewerSwarm:
    """
    The multi-agent brain behind a single interviewer.

    Each call to think() runs a full debate cycle:
    1. All debate agents analyze the answer in PARALLEL
    2. Forum fills with diverse perspectives
    3. Orchestrator reads the debate and synthesizes one question
    """

    def __init__(
        self,
        llm: LLMClient,
        persona: InterviewerPersona,
        swarm_agents: Optional[List[SwarmAgent]] = None,
        on_event: Optional[Callable] = None,
    ):
        self.llm = llm
        self.persona = persona
        self.on_event = on_event or (lambda e: None)

        # Select swarm profile based on interviewer role
        if swarm_agents:
            self.agents = swarm_agents
        else:
            self.agents = list(SWARM_PROFILES.get(persona.role, TECH_SWARM))

        self.turn_count = 0

    def think(
        self,
        candidate_answer: str,
        transcript: str,
        candidate_model: CandidateModel,
        coverage_gaps: List[str],
    ) -> SwarmOutput:
        """
        Run the full swarm deliberation cycle.

        1. All agents debate in parallel (ThreadPoolExecutor)
        2. Orchestrator synthesizes from the forum
        3. Return the final question + metadata
        """
        start = time.time()
        self.turn_count += 1
        forum = SwarmForum()

        self.on_event({
            "type": "swarm_thinking",
            "interviewer": self.persona.name,
            "num_agents": len(self.agents),
        })

        # ── Step 1: All agents debate in PARALLEL ──
        model_summary = candidate_model.get_summary()
        emotional_read = candidate_model.get_emotional_read()

        with ThreadPoolExecutor(max_workers=min(10, len(self.agents))) as pool:
            futures = {
                pool.submit(
                    self._run_swarm_agent,
                    agent, candidate_answer, transcript,
                    model_summary, forum.build_feed(),
                ): agent
                for agent in self.agents
            }
            for future in as_completed(futures):
                agent = futures[future]
                try:
                    result = future.result()
                    if result:
                        forum.add_post(
                            agent_id=agent.agent_id,
                            agent_name=agent.name,
                            role=agent.role,
                            content=result,
                        )
                except Exception as e:
                    forum.add_post(
                        agent_id=agent.agent_id,
                        agent_name=agent.name,
                        role=agent.role,
                        content=f"[Error: {str(e)[:100]}]",
                    )

        self.on_event({
            "type": "swarm_debated",
            "interviewer": self.persona.name,
            "num_posts": len(forum.posts),
        })

        # ── Step 2: Extract emotional advisory from empathy agents ──
        emotional_advisory = ""
        for post in forum.posts:
            if post.role == "empathy_reader":
                emotional_advisory += f"{post.agent_name}: {post.content}\n"
        if not emotional_advisory:
            emotional_advisory = f"Emotional state: {emotional_read}"

        # ── Step 3: Orchestrator synthesizes ──
        coverage_str = ", ".join(coverage_gaps) if coverage_gaps else "Good coverage so far"

        synthesize_prompt = SWARM_SYNTHESIZE_PROMPT.format(
            interviewer_name=self.persona.name,
            interviewer_role=self.persona.role,
            num_agents=len(self.agents),
            personality_brief=self.persona.system_prompt[:500],
            forum_feed=forum.build_feed(),
            emotional_advisory=emotional_advisory[:500],
            candidate_model=model_summary,
            coverage_gaps=coverage_str,
        )

        try:
            result = self.llm.generate_json(
                prompt=synthesize_prompt,
                system_prompt=self.persona.system_prompt,
                temperature=0.5,
            )

            elapsed = time.time() - start
            self.on_event({
                "type": "swarm_synthesized",
                "interviewer": self.persona.name,
                "elapsed_s": round(elapsed, 1),
            })

            return SwarmOutput(
                question=result.get("question", "Could you elaborate on that?"),
                turn_type=result.get("turn_type", "new_question"),
                confidence=float(result.get("confidence", 0.7)),
                reasoning=result.get("reasoning", ""),
                emotional_calibration=result.get("emotional_calibration", ""),
                debate_posts=forum.get_posts(),
                elapsed_seconds=round(elapsed, 1),
            )

        except Exception as e:
            # Fallback: pick the highest-confidence agent's question
            return self._fallback_from_forum(forum, time.time() - start)

    def _run_swarm_agent(
        self,
        agent: SwarmAgent,
        candidate_answer: str,
        transcript: str,
        candidate_model_summary: str,
        forum_feed: str,
    ) -> str:
        """Run a single swarm agent — returns its forum post content."""
        prompt = SWARM_AGENT_PROMPT.format(
            agent_name=agent.name,
            role=agent.role,
            instruction=agent.instruction,
            interviewer_name=self.persona.name,
            interviewer_role=self.persona.role,
            candidate_answer=candidate_answer[:1500],
            transcript=transcript[-2000:] if len(transcript) > 2000 else transcript,
            candidate_model=candidate_model_summary,
            forum_feed=forum_feed if forum_feed != "(No debate yet)" else "(You are posting first)",
        )

        raw = self.llm.generate(
            prompt=prompt,
            system_prompt=(
                f"You are {agent.name}, an internal analyst for interviewer {self.persona.name}. "
                f"Analyze the candidate's answer and recommend the next question. "
                f"Output valid JSON only."
            ),
            temperature=0.6,
            max_tokens=800,
        )

        # Parse and format the post
        try:
            data = json.loads(raw) if raw.strip().startswith("{") else self._extract_json(raw)
            analysis = data.get("analysis", "")
            question = data.get("recommended_question", "")
            confidence = data.get("confidence", 0.5)
            flags = data.get("flags", [])
            emotional = data.get("emotional_advisory", "")

            parts = []
            if analysis:
                parts.append(f"ANALYSIS: {analysis}")
            if question:
                parts.append(f"RECOMMENDED Q: {question}")
            parts.append(f"CONFIDENCE: {confidence}")
            if flags:
                parts.append(f"FLAGS: {', '.join(flags)}")
            if emotional:
                parts.append(f"EMOTIONAL: {emotional}")
            return "\n".join(parts)
        except Exception:
            return raw[:500]

    def _extract_json(self, text: str) -> dict:
        """Extract JSON from text that may contain markdown fences."""
        start = text.find("{")
        if start == -1:
            return {}
        depth, i = 0, start
        in_str, esc = False, False
        for i in range(start, len(text)):
            c = text[i]
            if esc:
                esc = False
                continue
            if c == "\\" and in_str:
                esc = True
                continue
            if c == '"' and not esc:
                in_str = not in_str
                continue
            if in_str:
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i + 1])
        return {}

    def _fallback_from_forum(self, forum: SwarmForum, elapsed: float) -> SwarmOutput:
        """If orchestrator synthesis fails, extract the best question from forum posts."""
        best_q = "Could you tell me more about that?"
        for post in forum.posts:
            if "RECOMMENDED Q:" in post.content:
                q = post.content.split("RECOMMENDED Q:")[1].split("\n")[0].strip()
                if q:
                    best_q = q
                    break
        return SwarmOutput(
            question=best_q,
            turn_type="new_question",
            confidence=0.5,
            reasoning="Fallback from agent debate",
            emotional_calibration="",
            debate_posts=forum.get_posts(),
            elapsed_seconds=round(elapsed, 1),
        )
