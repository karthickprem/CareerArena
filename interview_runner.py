"""
Interview Runner — manages the full interview lifecycle.

Lifecycle: setup -> introductions -> rounds (question/answer) -> wrap-up -> evaluation

Each round:
  1. Candidate answer is analyzed by CandidateAnalyzer (updates CandidateModel)
  2. Orchestrator decides who speaks next (TurnDecision), informed by CandidateModel
  3. Selected interviewer's swarm debates internally (8-10 agents in parallel)
  4. Swarm orchestrator synthesizes ONE question from the debate
  5. Response sent to client
  6. Candidate submits answer, loop back to step 1

The swarm architecture means each interviewer question is backed by a
full multi-agent debate — mimicking how a real human interviewer's
brain processes multiple considerations simultaneously.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from llm_client import LLMClient
from database import CareerDB
from interviewer_personas import (
    InterviewerPersona,
    build_panel,
    PANEL_PRESETS,
)
from panel_orchestrator import PanelOrchestrator
from evaluation_engine import EvaluationEngine
from interviewer_swarm import InterviewerSwarm
from candidate_model import CandidateModel, CandidateAnalyzer


@dataclass
class InterviewConfig:
    interview_type: str = "panel"  # panel, gd, 1on1
    preset: str = "campus_placement"
    role: str = ""
    company: str = ""
    difficulty: str = "realistic"  # practice, realistic, stress_test
    panel_size: int = 3
    max_turns: int = 30
    resume_text: str = ""
    job_description: str = ""

    def to_dict(self) -> dict:
        return {
            "interview_type": self.interview_type,
            "preset": self.preset,
            "role": self.role,
            "company": self.company,
            "difficulty": self.difficulty,
            "panel_size": self.panel_size,
            "max_turns": self.max_turns,
        }


class InterviewRunner:
    """Manages a single interview session from start to finish."""

    def __init__(
        self,
        llm: LLMClient,
        db: CareerDB,
        config: InterviewConfig,
        on_event: Optional[Callable[[dict], None]] = None,
        user_id: Optional[str] = None,
    ):
        self.llm = llm
        self.db = db
        self.config = config
        self.on_event = on_event or (lambda e: None)
        self.user_id = user_id
        self.session_id = str(uuid.uuid4())[:12]
        self.turn_counter = 0
        self.status = "setup"
        self.panel: List[InterviewerPersona] = []
        self.orchestrator: Optional[PanelOrchestrator] = None
        self.transcript: List[dict] = []

        # Swarm architecture: each interviewer backed by a debate swarm
        self.swarms: Dict[str, InterviewerSwarm] = {}  # name -> swarm

        # Real-time candidate assessment
        self.candidate_model = CandidateModel()
        self.candidate_analyzer = CandidateAnalyzer(llm)

    def setup(self) -> dict:
        """Initialize the interview — build panel, create swarms, create DB session."""
        self.panel = build_panel(
            preset_key=self.config.preset,
            role=self.config.role,
            company=self.config.company,
        )

        preset = PANEL_PRESETS.get(self.config.preset, {})
        max_turns = self.config.max_turns or preset.get("max_turns", 30)

        self.orchestrator = PanelOrchestrator(
            llm=self.llm,
            panel=self.panel,
            interview_type=self.config.interview_type,
            difficulty=self.config.difficulty,
            max_turns=max_turns,
        )

        # Create a debate swarm for each panelist
        for persona in self.panel:
            self.swarms[persona.name] = InterviewerSwarm(
                llm=self.llm,
                persona=persona,
                on_event=self.on_event,
            )

        # Create DB session
        self.db.create_interview_session(
            session_id=self.session_id,
            interview_type=self.config.interview_type,
            role=self.config.role,
            company=self.config.company,
            difficulty=self.config.difficulty,
            panel_size=len(self.panel),
            config=self.config.to_dict(),
            panel=[p.to_dict() for p in self.panel],
            user_id=self.user_id,
            max_turns=max_turns,
        )

        self.status = "ready"

        panel_info = [
            {
                "name": p.name,
                "role": p.role,
                "personality": p.personality,
                "avatar_color": p.avatar_color,
            }
            for p in self.panel
        ]
        swarm_info = {
            name: len(swarm.agents)
            for name, swarm in self.swarms.items()
        }

        self._emit("session_created", {
            "session_id": self.session_id,
            "panel": panel_info,
            "swarms": swarm_info,
            "config": self.config.to_dict(),
        })

        return {
            "session_id": self.session_id,
            "panel": [
                {
                    "name": p.name,
                    "role": p.role,
                    "personality": p.personality,
                    "avatar_color": p.avatar_color,
                    "eval_dimensions": p.eval_dimensions,
                }
                for p in self.panel
            ],
            "config": self.config.to_dict(),
        }

    def start(self) -> List[dict]:
        """Start the interview — return opening introductions + first question."""
        self.db.start_interview(self.session_id)
        self.status = "active"

        openings = self.orchestrator.get_opening()
        responses = []

        for opening in openings:
            self.turn_counter += 1
            self.db.add_interview_turn(
                session_id=self.session_id,
                turn_number=self.turn_counter,
                speaker=opening["speaker"],
                speaker_role=opening["speaker_role"],
                content=opening["content"],
                turn_type=opening["turn_type"],
            )
            turn_data = {
                "turn_number": self.turn_counter,
                **opening,
            }
            self.transcript.append(turn_data)
            responses.append(turn_data)

            self._emit("interviewer_speaking", turn_data)

        return responses

    def submit_answer(self, answer: str) -> List[dict]:
        """
        Process a candidate answer and return interviewer response(s).

        This is the core loop:
        1. Record candidate answer
        2. Analyze answer via CandidateAnalyzer → update CandidateModel
        3. Ask orchestrator who speaks next (informed by CandidateModel)
        4. Run selected interviewer's swarm (8-10 debate agents → 1 synthesized question)
        5. Return all new turns
        """
        if self.status != "active":
            return []

        # Record candidate answer
        self.turn_counter += 1
        self.db.add_interview_turn(
            session_id=self.session_id,
            turn_number=self.turn_counter,
            speaker="Candidate",
            speaker_role="candidate",
            content=answer,
            turn_type="answer",
        )
        candidate_turn = {
            "turn_number": self.turn_counter,
            "speaker": "Candidate",
            "speaker_role": "candidate",
            "content": answer,
            "turn_type": "answer",
        }
        self.transcript.append(candidate_turn)
        self.orchestrator.record_candidate_answer(answer)

        self._emit("candidate_answered", candidate_turn)

        # ── Analyze candidate's answer and update model ──
        last_question = self._get_last_question()
        transcript_text = self._build_transcript_text()

        analysis = self.candidate_analyzer.analyze_answer(
            answer=answer,
            question=last_question,
            transcript_so_far=transcript_text,
            candidate_model=self.candidate_model,
        )
        self.candidate_model.update(analysis)

        self._emit("candidate_analyzed", {
            "depth_score": analysis.depth_score,
            "confidence": analysis.confidence_signals,
            "emotional_state": analysis.emotional_state,
            "evasion": analysis.evasion_detected,
            "recommended_difficulty": self.candidate_model.recommended_difficulty,
        })

        # ── Ask orchestrator for next turn decision (informed by model) ──
        decision = self.orchestrator.decide_next_turn(
            candidate_answer=answer,
            candidate_model=self.candidate_model,
        )

        if decision.should_wrap_up:
            return self._handle_wrap_up(decision)

        # ── Generate responses via swarm debate ──
        responses = []
        for speaker_name in decision.speakers:
            persona = self.orchestrator.get_persona_by_name(speaker_name)
            if not persona:
                continue

            self._emit("interviewer_thinking", {
                "speaker": speaker_name,
                "role": persona.role,
            })

            swarm = self.swarms.get(speaker_name)

            if swarm:
                # Route through the swarm — full multi-agent debate
                swarm_output = self.orchestrator.generate_swarm_response(
                    persona=persona,
                    swarm=swarm,
                    candidate_answer=answer,
                    candidate_model=self.candidate_model,
                )
                response_text = swarm_output.question
                turn_type = swarm_output.turn_type
            else:
                # Fallback to direct LLM call (shouldn't happen normally)
                turn_type = decision.turn_types.get(speaker_name, "new_question")
                context_hint = decision.context_hints.get(speaker_name, "")
                response_text = self.orchestrator.generate_interviewer_response(
                    persona=persona,
                    turn_type=turn_type,
                    context_hint=context_hint,
                    candidate_answer=answer,
                )

            self.turn_counter += 1
            self.db.add_interview_turn(
                session_id=self.session_id,
                turn_number=self.turn_counter,
                speaker=speaker_name,
                speaker_role=persona.role,
                content=response_text,
                turn_type=turn_type,
            )

            turn_data = {
                "turn_number": self.turn_counter,
                "speaker": speaker_name,
                "speaker_role": persona.role,
                "content": response_text,
                "turn_type": turn_type,
            }
            self.transcript.append(turn_data)
            responses.append(turn_data)

            self._emit("interviewer_speaking", turn_data)

        return responses

    def _get_last_question(self) -> str:
        """Get the last interviewer question from the transcript."""
        for turn in reversed(self.transcript):
            if turn.get("speaker_role") != "candidate":
                return turn.get("content", "")
        return ""

    def _build_transcript_text(self) -> str:
        """Build a plain-text transcript for candidate analysis."""
        lines = []
        for t in self.transcript[-10:]:  # Last 10 turns
            lines.append(f"[{t['speaker']}]: {t['content'][:200]}")
        return "\n".join(lines)

    def _handle_wrap_up(self, decision) -> List[dict]:
        """Handle interview wrap-up sequence."""
        self.status = "wrapping_up"
        responses = []

        # Lead interviewer wraps up
        lead = self.panel[0]
        wrap_up_text = self.orchestrator.generate_interviewer_response(
            persona=lead,
            turn_type="wrap_up",
            context_hint=decision.context_hints.get(lead.name, ""),
            candidate_answer="",
        )

        self.turn_counter += 1
        self.db.add_interview_turn(
            session_id=self.session_id,
            turn_number=self.turn_counter,
            speaker=lead.name,
            speaker_role=lead.role,
            content=wrap_up_text,
            turn_type="wrap_up",
        )

        turn_data = {
            "turn_number": self.turn_counter,
            "speaker": lead.name,
            "speaker_role": lead.role,
            "content": wrap_up_text,
            "turn_type": "wrap_up",
        }
        self.transcript.append(turn_data)
        responses.append(turn_data)

        self._emit("interview_wrapping_up", turn_data)

        return responses

    def end_interview(self) -> dict:
        """Finalize the interview and generate evaluation."""
        self.status = "evaluating"
        self._emit("evaluating", {
            "session_id": self.session_id,
            "candidate_model": self.candidate_model.to_dict(),
        })

        self.db.complete_interview(self.session_id)

        # Run evaluation — pass the candidate model for richer context
        evaluator = EvaluationEngine(self.llm, self.db)
        evaluation = evaluator.evaluate(
            session_id=self.session_id,
            panel=self.panel,
            transcript=self.transcript,
            candidate_model=self.candidate_model,
        )

        self.status = "completed"
        self._emit("interview_complete", {
            "session_id": self.session_id,
            "overall_score": evaluation.get("overall", 0),
            "candidate_model": self.candidate_model.to_dict(),
        })

        return evaluation

    def get_state(self) -> dict:
        """Return current interview state."""
        orch_status = self.orchestrator.get_status() if self.orchestrator else {}
        return {
            "session_id": self.session_id,
            "status": self.status,
            "turn_number": self.turn_counter,
            "panel": [
                {"name": p.name, "role": p.role, "avatar_color": p.avatar_color}
                for p in self.panel
            ],
            "config": self.config.to_dict(),
            "orchestrator": orch_status,
            "candidate_model": self.candidate_model.to_dict(),
        }

    def _emit(self, event_type: str, data: dict):
        """Emit an event to the callback."""
        self.on_event({"type": event_type, "timestamp": time.time(), **data})
