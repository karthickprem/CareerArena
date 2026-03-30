"""
Panel Orchestrator — the brain behind multi-agent interviews.

Decides who speaks next, what type of response (follow-up, challenge,
cross-reference, new question), tracks topic coverage, and determines
when the interview should wrap up.

Upgraded to work with InterviewerSwarm:
  - Each interviewer is backed by a swarm of 6-10 debate agents
  - The orchestrator decides WHO speaks, the swarm decides WHAT they say
  - Candidate model feeds into both orchestrator decisions and swarm debates
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, TYPE_CHECKING

from llm_client import LLMClient
from interviewer_personas import InterviewerPersona

if TYPE_CHECKING:
    from interviewer_swarm import InterviewerSwarm, SwarmOutput
    from candidate_model import CandidateModel


@dataclass
class TurnDecision:
    """What the orchestrator decides for the next turn(s)."""
    speakers: List[str]  # names of interviewers who should speak
    turn_types: Dict[str, str]  # speaker_name -> turn_type
    context_hints: Dict[str, str]  # speaker_name -> hint for their response
    should_wrap_up: bool = False
    wrap_up_reason: str = ""


@dataclass
class CoverageTracker:
    """Tracks which evaluation dimensions have been assessed."""
    dimensions: Dict[str, float] = field(default_factory=dict)  # dimension -> coverage 0-1
    topics_asked: List[str] = field(default_factory=list)
    questions_per_interviewer: Dict[str, int] = field(default_factory=dict)

    def update(self, dimension: str, amount: float = 0.2):
        current = self.dimensions.get(dimension, 0.0)
        self.dimensions[dimension] = min(1.0, current + amount)

    def overall_coverage(self) -> float:
        if not self.dimensions:
            return 0.0
        return sum(self.dimensions.values()) / len(self.dimensions)

    def least_covered(self, n: int = 3) -> List[str]:
        sorted_dims = sorted(self.dimensions.items(), key=lambda x: x[1])
        return [d for d, _ in sorted_dims[:n]]


class PanelOrchestrator:
    """
    Manages turn-taking in panel interviews.

    The orchestrator uses a combination of rules and LLM judgment to create
    natural-feeling panel dynamics:
    - No interviewer dominates (max 2 consecutive turns)
    - Follow-ups happen when answers are weak or interesting
    - Cross-references create realistic panel dynamics
    - Coverage tracking ensures all dimensions get assessed
    """

    def __init__(
        self,
        llm: LLMClient,
        panel: List[InterviewerPersona],
        interview_type: str = "panel",
        difficulty: str = "realistic",
        max_turns: int = 30,
    ):
        self.llm = llm
        self.panel = panel
        self.interview_type = interview_type
        self.difficulty = difficulty
        self.max_turns = max_turns
        self.turn_number = 0
        self.turn_history: List[dict] = []
        self.coverage = CoverageTracker()
        self._last_speakers: List[str] = []

        # Initialize coverage dimensions from panel
        all_dims = set()
        for p in panel:
            for d in p.eval_dimensions:
                all_dims.add(d)
        for d in all_dims:
            self.coverage.dimensions[d] = 0.0

    def get_opening(self) -> List[dict]:
        """Generate the opening sequence — panel introductions."""
        introductions = []
        for i, persona in enumerate(self.panel):
            if i == 0:
                content = (
                    f"Good morning. I'm {persona.name}, {persona.role}. "
                    f"Welcome to this interview. Let me introduce the panel."
                )
            else:
                content = f"Hello, I'm {persona.name}, {persona.role}. Looking forward to our conversation."

            introductions.append({
                "speaker": persona.name,
                "speaker_role": persona.role,
                "content": content,
                "turn_type": "introduction",
            })

        # First question from the lead interviewer
        first_q = self._generate_opening_question()
        introductions.append({
            "speaker": self.panel[0].name,
            "speaker_role": self.panel[0].role,
            "content": first_q,
            "turn_type": "question",
        })
        return introductions

    def decide_next_turn(
        self,
        candidate_answer: str,
        candidate_model: Optional["CandidateModel"] = None,
    ) -> TurnDecision:
        """
        After the candidate answers, decide who speaks next and what they say.

        Returns a TurnDecision with 1-2 speakers and their turn types.
        """
        self.turn_number += 1
        remaining = self.max_turns - self.turn_number

        # Wrap up if near the end
        if remaining <= 2:
            return TurnDecision(
                speakers=[self.panel[0].name],
                turn_types={self.panel[0].name: "wrap_up"},
                context_hints={self.panel[0].name: "Thank the candidate and ask if they have questions for the panel."},
                should_wrap_up=True,
                wrap_up_reason="turn_limit",
            )

        # Check coverage — if mostly covered, start wrapping up
        if self.coverage.overall_coverage() > 0.85 and remaining <= 6:
            return TurnDecision(
                speakers=[self.panel[0].name],
                turn_types={self.panel[0].name: "wrap_up"},
                context_hints={self.panel[0].name: "Coverage is good. Wrap up the interview."},
                should_wrap_up=True,
                wrap_up_reason="coverage_complete",
            )

        # Use LLM to decide the next turn
        return self._llm_decide(candidate_answer, candidate_model)

    def _llm_decide(
        self,
        candidate_answer: str,
        candidate_model: Optional["CandidateModel"] = None,
    ) -> TurnDecision:
        """Use LLM to make a nuanced turn decision."""
        transcript_summary = self._build_recent_context()
        coverage_summary = self._build_coverage_summary()

        panel_info = "\n".join([
            f"- {p.name} ({p.role}): focuses on {', '.join(p.eval_dimensions)}. "
            f"Style: {p.question_style}. Last spoke: {self._turns_since_spoke(p.name)} turns ago."
            for p in self.panel
        ])

        # Include candidate model insights if available
        candidate_insight = ""
        if candidate_model:
            candidate_insight = f"""
CANDIDATE MODEL:
{candidate_model.get_summary()}

EMOTIONAL READ:
{candidate_model.get_emotional_read()}
"""

        prompt = f"""You are the orchestrator of a panel interview. Decide what happens next.

PANEL:
{panel_info}

COVERAGE STATUS:
{coverage_summary}

RECENT TRANSCRIPT:
{transcript_summary}

CANDIDATE'S LATEST ANSWER:
{candidate_answer[:1500]}
{candidate_insight}
RULES:
1. Pick EXACTLY ONE panelist to ask the next question — just like a real interview, only one person speaks at a time
2. No panelist should speak more than 2 turns in a row
3. Prefer follow-ups when the answer was weak, vague, or interesting
4. Use cross-references ("As [name] mentioned...") for realistic panel dynamics
5. Prioritize uncovered evaluation dimensions
6. Balance between panelists — the one who hasn't spoken recently should get a chance
7. If the candidate is struggling emotionally, pick a supportive panelist next
8. If the candidate is very confident, pick a challenging panelist to probe deeper

Return JSON:
```json
{{
  "speaker": "Name1",
  "turn_type": "one of: follow_up, challenge, cross_reference, new_question, clarification",
  "context_hint": "Brief hint about what to focus on in the response",
  "reasoning": "Why this decision makes sense"
}}
```"""

        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt="You orchestrate panel interviews. Pick ONE panelist to speak next. Output valid JSON only.",
                temperature=0.4,
            )

            # Extract single speaker (handle both old and new format)
            speaker = result.get("speaker") or (result.get("speakers", [None])[0])
            valid_names = {p.name for p in self.panel}
            if speaker not in valid_names:
                speaker = self._pick_next_speaker()

            turn_type = (
                result.get("turn_type")
                or result.get("turn_types", {}).get(speaker, "new_question")
            )
            context_hint = (
                result.get("context_hint")
                or result.get("context_hints", {}).get(speaker, "")
            )

            return TurnDecision(
                speakers=[speaker],
                turn_types={speaker: turn_type},
                context_hints={speaker: context_hint},
            )
        except Exception:
            # Fallback: simple rotation
            next_speaker = self._pick_next_speaker()
            return TurnDecision(
                speakers=[next_speaker],
                turn_types={next_speaker: "new_question"},
                context_hints={next_speaker: f"Focus on: {', '.join(self.coverage.least_covered(2))}"},
            )

    def generate_swarm_response(
        self,
        persona: InterviewerPersona,
        swarm: "InterviewerSwarm",
        candidate_answer: str,
        candidate_model: "CandidateModel",
    ) -> "SwarmOutput":
        """
        Generate an interviewer's response via their debate swarm.

        Instead of a single LLM call, the swarm runs 6-10 debate agents in
        parallel, then the swarm orchestrator synthesizes the best question.

        Returns the full SwarmOutput with question, reasoning, and debate posts.
        """
        transcript = self._build_full_transcript()
        coverage_gaps = self.coverage.least_covered(3)

        output = swarm.think(
            candidate_answer=candidate_answer,
            transcript=transcript,
            candidate_model=candidate_model,
            coverage_gaps=coverage_gaps,
        )

        # Update coverage based on persona dimensions
        for dim in persona.eval_dimensions:
            self.coverage.update(dim, 0.15)

        # Track turn history
        self.turn_history.append({
            "turn": self.turn_number,
            "speaker": persona.name,
            "role": persona.role,
            "turn_type": output.turn_type,
            "content_preview": output.question[:100],
            "swarm_confidence": output.confidence,
            "swarm_reasoning": output.reasoning[:200],
        })
        self._last_speakers.append(persona.name)

        # Track questions per interviewer
        count = self.coverage.questions_per_interviewer.get(persona.name, 0)
        self.coverage.questions_per_interviewer[persona.name] = count + 1

        return output

    def generate_interviewer_response(
        self,
        persona: InterviewerPersona,
        turn_type: str,
        context_hint: str,
        candidate_answer: str,
    ) -> str:
        """
        Fallback: generate a single interviewer's response via direct LLM call.

        Used for wrap-ups, introductions, and when no swarm is available.
        """
        transcript = self._build_full_transcript()

        turn_instructions = {
            "follow_up": "Ask a follow-up question digging deeper into the candidate's last answer. Reference something specific they said.",
            "challenge": "Respectfully challenge or push back on something the candidate said. Present an alternative perspective.",
            "cross_reference": "Reference something another panelist asked or the candidate said earlier. Build on it.",
            "new_question": "Ask a new question on a topic not yet covered. Draw from your evaluation dimensions.",
            "clarification": "Ask the candidate to clarify a specific point from their answer.",
            "wrap_up": "Thank the candidate. Ask if they have any questions for the panel.",
            "introduction": "Introduce yourself briefly.",
        }

        instruction = turn_instructions.get(turn_type, turn_instructions["new_question"])

        prompt = f"""INTERVIEW TRANSCRIPT SO FAR:
{transcript}

CANDIDATE'S LATEST ANSWER:
{candidate_answer[:2000]}

YOUR TASK:
{instruction}

ADDITIONAL CONTEXT:
{context_hint}

IMPORTANT:
- Ask exactly ONE question (unless wrapping up)
- Keep your response under 150 words
- Stay in character
- Reference previous answers when relevant
- Don't repeat questions already asked"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=persona.system_prompt,
            temperature=0.7,
            max_tokens=500,
        )

        # Update coverage based on turn type and persona
        for dim in persona.eval_dimensions:
            self.coverage.update(dim, 0.15)

        # Track turn history
        self.turn_history.append({
            "turn": self.turn_number,
            "speaker": persona.name,
            "role": persona.role,
            "turn_type": turn_type,
            "content_preview": response[:100],
        })
        self._last_speakers.append(persona.name)

        # Track questions per interviewer
        count = self.coverage.questions_per_interviewer.get(persona.name, 0)
        self.coverage.questions_per_interviewer[persona.name] = count + 1

        return response.strip()

    def record_candidate_answer(self, answer: str):
        """Record the candidate's answer in turn history."""
        self.turn_history.append({
            "turn": self.turn_number,
            "speaker": "Candidate",
            "role": "candidate",
            "turn_type": "answer",
            "content_preview": answer[:100],
        })

    def get_status(self) -> dict:
        """Current interview status."""
        return {
            "turn_number": self.turn_number,
            "max_turns": self.max_turns,
            "remaining_turns": self.max_turns - self.turn_number,
            "coverage": self.coverage.overall_coverage(),
            "coverage_by_dimension": dict(self.coverage.dimensions),
            "questions_per_interviewer": dict(self.coverage.questions_per_interviewer),
            "least_covered": self.coverage.least_covered(3),
        }

    # ───────────────────────────────────────
    # Private helpers
    # ───────────────────────────────────────

    def _generate_opening_question(self) -> str:
        """Generate the first question — usually 'Tell us about yourself'."""
        lead = self.panel[0]
        if self.interview_type == "upsc_board":
            return (
                "Let's begin. I see from your form that you've chosen an interesting "
                "background. Could you briefly tell us about yourself and what drew you "
                "to the civil services?"
            )
        return (
            "Let's get started. Could you tell us about yourself — your background, "
            "what you've been working on, and what interests you about this opportunity?"
        )

    def _pick_next_speaker(self) -> str:
        """Simple heuristic to pick the next speaker."""
        # Don't let the same person speak 3 times in a row
        if len(self._last_speakers) >= 2 and self._last_speakers[-1] == self._last_speakers[-2]:
            exclude = self._last_speakers[-1]
            candidates = [p for p in self.panel if p.name != exclude]
        else:
            candidates = list(self.panel)

        # Prefer the interviewer who has spoken least
        min_count = float("inf")
        best = candidates[0]
        for p in candidates:
            count = self.coverage.questions_per_interviewer.get(p.name, 0)
            if count < min_count:
                min_count = count
                best = p
        return best.name

    def _turns_since_spoke(self, name: str) -> int:
        """How many turns since this interviewer last spoke."""
        for i, entry in enumerate(reversed(self.turn_history)):
            if entry["speaker"] == name:
                return i
        return len(self.turn_history)

    def _build_recent_context(self, n: int = 6) -> str:
        """Build a summary of recent turns."""
        recent = self.turn_history[-n:]
        lines = []
        for t in recent:
            lines.append(f"[{t['speaker']} ({t['role']})] [{t['turn_type']}]: {t['content_preview']}")
        return "\n".join(lines) if lines else "(Interview just started)"

    def _build_full_transcript(self) -> str:
        """Build the full transcript for agent context."""
        lines = []
        for t in self.turn_history:
            lines.append(f"[{t['speaker']} ({t['role']})]: {t['content_preview']}")
        return "\n".join(lines) if lines else "(Interview just started)"

    def _build_coverage_summary(self) -> str:
        """Build a readable coverage summary."""
        lines = []
        for dim, val in sorted(self.coverage.dimensions.items()):
            bar = "#" * int(val * 10) + "." * (10 - int(val * 10))
            lines.append(f"  {dim}: [{bar}] {val:.0%}")
        lines.append(f"  Overall: {self.coverage.overall_coverage():.0%}")
        return "\n".join(lines)

    def get_persona_by_name(self, name: str) -> Optional[InterviewerPersona]:
        """Look up a panel member by name."""
        for p in self.panel:
            if p.name == name:
                return p
        return None
