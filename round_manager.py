"""
RoundManager — Orchestrates multi-round sequential 1-on-1 interviews.

Manages the flow: screening → panel reveal → round 1 → forum → round 2 → ... → final → forum reveal.

Each round:
  1. Start round with interviewer context (profile + forum digest from prior rounds)
  2. Interviewer asks questions (uses existing InterviewerSwarm)
  3. Candidate answers, loop for 5-8 questions
  4. End round → trigger InterviewForum (observers post)
  5. Advance to next round
"""

from __future__ import annotations

import json
import uuid
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Callable

from concurrent.futures import ThreadPoolExecutor
from llm_client import LLMClient
from database import CareerDB
from knowledge_db import KnowledgeDB
from screening_agent import CandidateProfile
from panel_generator import PanelGenerator, RoundPlan, RoundConfig
from interview_forum import InterviewForum, ForumPost
from interviewer_personas import InterviewerPersona
from candidate_model import CandidateModel, CandidateAnalyzer
from evaluation_engine import EvaluationEngine
from interviewer_engine import InterviewerEngine
from interviewer_swarm import InterviewerSwarm

logger = logging.getLogger(__name__)


@dataclass
class RoundStartResponse:
    round_num: int
    interviewer_name: str
    interviewer_role: str
    round_type: str
    focus_areas: List[str]
    opening_message: str
    is_final: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RoundEndResponse:
    round_num: int
    questions_asked: int
    next_round: Optional[int]
    forum_posts: List[dict]
    is_interview_complete: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


class RoundManager:
    def __init__(
        self,
        llm: LLMClient,
        db: CareerDB,
        knowledge_db: KnowledgeDB,
    ):
        self.llm = llm
        self.db = db
        self.knowledge_db = knowledge_db
        self.forum = InterviewForum(db, llm)
        self.panel_generator = PanelGenerator(llm, knowledge_db)
        self.analyzer = CandidateAnalyzer(llm)
        self.evaluation_engine = EvaluationEngine(llm, db)
        self.engine = InterviewerEngine(llm, db, knowledge_db)
        # Per-session candidate models: session_id -> CandidateModel
        self.candidate_models: Dict[str, CandidateModel] = {}
        # Per-session swarm instances for final round: session_id -> InterviewerSwarm
        self._swarms: Dict[str, InterviewerSwarm] = {}

    def create_multi_round_session(
        self,
        profile: CandidateProfile,
        company: str = "",
        role: str = "",
        screening_session_id: str = "",
        panel_size: int = 3,
        difficulty: str = "realistic",
    ) -> dict:
        """
        Create a new multi-round interview session from a CandidateProfile.
        Returns session_id, panel, and round_plan.
        """
        # Generate panel and round plan
        panel, round_plan = self.panel_generator.generate_panel(
            profile=profile,
            company=company or profile.target_company,
            role=role or profile.target_role,
            panel_size=panel_size,
            difficulty=difficulty,
        )

        # Create interview session in DB
        session_id = str(uuid.uuid4())[:12]
        self.db.create_interview_session(
            session_id=session_id,
            interview_type="multi_round",
            role=role or profile.target_role,
            company=company or profile.target_company,
            difficulty=difficulty,
            panel_size=len(panel),
            config={"profile": profile.to_dict(), "difficulty": difficulty},
            panel=[p.to_dict() for p in panel],
            max_turns=round_plan.total_rounds * 16,  # ~16 turns per round (8 Q + 8 A)
        )

        # Set V2 fields
        self.db.update_interview_session(
            session_id,
            screening_session_id=screening_session_id,
            round_plan=round_plan.to_dict(),
            current_round=0,
            total_rounds=round_plan.total_rounds,
        )

        # Create round records in DB
        for rc in round_plan.rounds:
            self.db.create_interview_round(
                session_id=session_id,
                round_num=rc.round_num,
                interviewer_name=rc.interviewer_name,
                interviewer_role=rc.interviewer_role,
                round_type=rc.round_type,
                focus_areas=rc.focus_areas,
                max_questions=rc.max_questions,
                is_final=rc.is_final,
            )

        # --- Gap 1: Kavitha posts screening briefing to forum ---
        self._post_screening_briefing(session_id, profile, panel, round_plan)

        return {
            "session_id": session_id,
            "panel": [p.to_dict() for p in panel],
            "round_plan": round_plan.to_dict(),
            "total_rounds": round_plan.total_rounds,
        }

    def _post_screening_briefing(
        self, session_id: str, profile: CandidateProfile,
        panel: List[InterviewerPersona], round_plan: RoundPlan,
    ):
        """Kavitha posts her screening findings to the forum so all interviewers are briefed."""
        panel_names = ", ".join(p.name for p in panel)
        round_summary = "\n".join(
            f"  Round {r.round_num}: {r.interviewer_name} ({r.round_type}) - focus: {', '.join(r.focus_areas)}"
            for r in round_plan.rounds
        )

        prompt = f"""You are Kavitha, the screening recruiter. You just finished profiling a candidate and are now briefing the interview panel in a private forum.

## Candidate Profile You Built
- Name: {profile.name}
- Experience: {profile.experience_level}
- Domain: {profile.domain}
- Education: {profile.education}
- Skills: {json.dumps(profile.skills)}
- Projects: {json.dumps(profile.projects[:3])}
- Communication Style: {profile.communication_style}
- Strengths: {', '.join(profile.strengths)}
- Weaknesses: {', '.join(profile.weaknesses)}
- Notable Claims to Verify: {', '.join(profile.notable_claims)}
- Career Goals: {profile.career_goals}
- Stress Tolerance: {profile.stress_tolerance}

## Interview Panel
{panel_names}

## Round Plan
{round_summary}

---

Write a briefing post for the panel. Include:
1. Your overall impression of the candidate (2-3 sentences)
2. Key things each interviewer should probe (reference specific claims/gaps)
3. Red flags or inconsistencies you noticed
4. The candidate's emotional state and communication style
5. Specific recommendations: "Ask about X because they claimed Y but couldn't elaborate"

Write naturally, like a recruiter briefing colleagues over chai. 5-8 sentences."""

        try:
            briefing = self.llm.generate(
                prompt=prompt,
                system_prompt="You are Kavitha, a warm Indian recruiter. Write honestly and specifically. This is a private forum — be candid.",
                temperature=0.6,
            )

            self.db.create_post(
                session_id=session_id,
                agent_id="kavitha_screening",
                agent_name="Kavitha",
                content=briefing,
                topic="screening_briefing",
                post_type="strategy",
                agent_type="Screening Recruiter",
                round_num=0,
            )
            logger.info(f"[{session_id}] Kavitha posted screening briefing to forum")
        except Exception as e:
            logger.warning(f"Failed to post screening briefing: {e}")

    def start_round(self, session_id: str, round_num: int) -> RoundStartResponse:
        """Start a specific round. Returns interviewer intro + opening question."""
        session = self.db.get_interview_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        round_info = self.db.get_interview_round(session_id, round_num)
        if not round_info:
            raise ValueError(f"Round {round_num} not found for session {session_id}")

        # Get panel data
        panel_json = json.loads(session["panel_json"]) if isinstance(session.get("panel_json"), str) else session.get("panel_json", [])

        # Find this round's interviewer persona
        interviewer = None
        for p in panel_json:
            if p["name"] == round_info["interviewer_name"]:
                interviewer = p
                break

        if not interviewer:
            interviewer = panel_json[round_num - 1] if round_num <= len(panel_json) else panel_json[0]

        # Get forum digest from previous rounds
        forum_digest = ""
        if round_num > 1:
            forum_digest = self.db.build_forum_digest(session_id, round_num - 1)

        # Get candidate profile from config
        config = json.loads(session["config_json"]) if isinstance(session.get("config_json"), str) else session.get("config_json", {})
        profile_data = config.get("profile", {})

        # Get round plan for briefing notes
        round_plan_data = json.loads(session.get("round_plan", "{}")) if isinstance(session.get("round_plan"), str) else session.get("round_plan", {})
        briefing_notes = ""
        for r in round_plan_data.get("rounds", []):
            if r.get("round_num") == round_num:
                briefing_notes = r.get("briefing_notes", "")
                break

        # Restore candidate model from DB if not in memory (e.g. after server restart)
        if session_id not in self.candidate_models:
            saved = session.get("candidate_model_json")
            if saved:
                try:
                    d = json.loads(saved) if isinstance(saved, str) else saved
                    self.candidate_models[session_id] = CandidateModel.from_dict(d)
                    logger.info(f"[{session_id}] Restored CandidateModel from DB")
                except Exception as e:
                    logger.warning(f"Failed to restore CandidateModel: {e}")

        # For final/HR round, get full forum digest (not just previous round)
        is_final = bool(round_info.get("is_final", 0))
        if is_final:
            forum_digest = self.db.build_forum_digest(session_id, round_num)

        # Generate opening message
        opening = self._generate_opening(
            session_id, interviewer, round_info, profile_data,
            forum_digest, briefing_notes, round_num,
        )

        # Mark round as active
        self.db.start_interview_round(session_id, round_num, forum_digest)
        self.db.start_interview(session_id)

        # Save opening turn
        turn_offset = self._get_turn_offset(session_id, round_num)
        self.db.add_interview_turn(
            session_id=session_id,
            turn_number=turn_offset + 1,
            speaker=round_info["interviewer_name"],
            content=opening,
            turn_type="question",
            speaker_role=round_info["interviewer_role"],
            metadata={"round_num": round_num, "is_opening": True},
        )

        return RoundStartResponse(
            round_num=round_num,
            interviewer_name=round_info["interviewer_name"],
            interviewer_role=round_info["interviewer_role"],
            round_type=round_info["round_type"],
            focus_areas=json.loads(round_info["focus_areas"]) if isinstance(round_info.get("focus_areas"), str) else round_info.get("focus_areas", []),
            opening_message=opening,
            is_final=bool(round_info.get("is_final", 0)),
        )

    def submit_answer(
        self, session_id: str, round_num: int, answer: str
    ) -> dict:
        """
        Submit candidate's answer for the current round.
        Analyzes the answer via CandidateAnalyzer, updates the CandidateModel,
        then feeds the model into question generation for intelligent follow-ups.
        """
        session = self.db.get_interview_session(session_id)
        round_info = self.db.get_interview_round(session_id, round_num)

        if not session or not round_info:
            raise ValueError("Invalid session or round")

        # Save candidate answer
        turn_offset = self._get_turn_offset(session_id, round_num)
        existing_round_turns = self.db.get_round_turns(session_id, round_num)
        turn_number = turn_offset + len(existing_round_turns) + 1

        self.db.add_interview_turn(
            session_id=session_id,
            turn_number=turn_number,
            speaker="Candidate",
            content=answer,
            turn_type="answer",
            metadata={"round_num": round_num},
        )

        # --- CandidateModel integration ---
        # Initialize model for this session if needed
        if session_id not in self.candidate_models:
            self.candidate_models[session_id] = CandidateModel()

        model = self.candidate_models[session_id]

        # Get the last question asked (for analysis context)
        last_question = ""
        for turn in reversed(existing_round_turns):
            content = turn.get("content", "")
            speaker = turn.get("speaker", "")
            if speaker != "Candidate" and content:
                last_question = content
                break

        # Analyze the answer
        transcript = self.db.get_round_transcript(session_id, round_num)
        try:
            analysis = self.analyzer.analyze_answer(
                answer=answer,
                question=last_question,
                transcript_so_far=transcript,
                candidate_model=model,
            )
            model.update(analysis)
            logger.info(
                f"[{session_id}] Answer analyzed: depth={analysis.depth_score:.2f} "
                f"conf={analysis.confidence_signals:.2f} evasion={analysis.evasion_detected} "
                f"pattern={analysis.response_pattern}"
            )
            # Persist model to DB after every answer
            try:
                self.db.update_interview_session(
                    session_id, candidate_model_json=model.to_dict(),
                )
            except Exception as save_err:
                logger.warning(f"Failed to persist CandidateModel: {save_err}")
        except Exception as e:
            logger.warning(f"CandidateAnalyzer failed (non-fatal): {e}")

        # Check if round should end
        questions_asked = self.db.increment_round_questions(session_id, round_num)
        max_q = round_info.get("max_questions", 8)

        if questions_asked >= max_q:
            return {
                "is_round_complete": True,
                "questions_asked": questions_asked,
                "responses": [],
                "candidate_model": model.to_dict(),
            }

        # --- Gap 2+3: Fire live observer reactions every 2-3 questions ---
        if questions_asked >= 2 and questions_asked % 2 == 0:
            self._run_live_observers(session_id, round_num, round_info, session, questions_asked, last_question, answer)

        # Generate interviewer's next question (now informed by candidate model + live suggestions)
        response = self._generate_question(session_id, round_num, round_info, session)

        # Save interviewer response
        self.db.add_interview_turn(
            session_id=session_id,
            turn_number=turn_number + 1,
            speaker=round_info["interviewer_name"],
            content=response,
            turn_type="question",
            speaker_role=round_info["interviewer_role"],
            metadata={"round_num": round_num},
        )

        return {
            "is_round_complete": False,
            "questions_asked": questions_asked,
            "responses": [{
                "speaker": round_info["interviewer_name"],
                "role": round_info["interviewer_role"],
                "content": response,
                "type": "question",
            }],
            "candidate_model": model.to_dict(),
        }

    def end_round(self, session_id: str, round_num: int) -> RoundEndResponse:
        """
        End a round and trigger the inter-interviewer forum.
        Returns forum posts and next round info.
        """
        session = self.db.get_interview_session(session_id)
        round_info = self.db.get_interview_round(session_id, round_num)

        # Mark round as completed
        self.db.complete_interview_round(session_id, round_num)

        # Get round transcript
        round_transcript = self.db.get_round_transcript(session_id, round_num)

        # Get panel
        panel_json = json.loads(session["panel_json"]) if isinstance(session.get("panel_json"), str) else session.get("panel_json", [])
        panel = [InterviewerPersona.from_dict(p) for p in panel_json]

        # Get candidate summary
        config = json.loads(session["config_json"]) if isinstance(session.get("config_json"), str) else session.get("config_json", {})
        candidate_summary = json.dumps(config.get("profile", {}), indent=2)

        # Get previous forum posts
        previous_forum = self.db.build_forum_digest(session_id, round_num - 1) if round_num > 1 else ""

        # Run forum — observers post their thoughts
        forum_posts = self.forum.run_observer_round(
            session_id=session_id,
            round_num=round_num,
            active_interviewer=round_info["interviewer_name"],
            round_transcript=round_transcript,
            panel=panel,
            candidate_summary=candidate_summary,
            previous_forum=previous_forum,
        )

        # --- Gap 4: Kavitha posts transition summary directing next interviewer ---
        total_rounds = session.get("total_rounds", 0)
        is_complete = round_num >= total_rounds
        next_round = None if is_complete else round_num + 1

        if not is_complete and next_round:
            next_round_info = self.db.get_interview_round(session_id, next_round)
            if next_round_info:
                self._post_transition_summary(
                    session_id, round_num, round_info, next_round_info,
                    round_transcript, config, forum_posts,
                )

        if is_complete:
            # --- Gap 5: Post-interview forum verdict from all agents ---
            self._post_forum_verdict(session_id, panel, config, round_transcript)
            self.db.complete_interview(session_id)

        return RoundEndResponse(
            round_num=round_num,
            questions_asked=round_info.get("questions_asked", 0),
            next_round=next_round,
            forum_posts=[p.to_dict() for p in forum_posts],
            is_interview_complete=is_complete,
        )

    def _generate_opening(
        self,
        session_id: str,
        interviewer: dict,
        round_info: dict,
        profile_data: dict,
        forum_digest: str,
        briefing_notes: str,
        round_num: int,
    ) -> str:
        """Generate the interviewer's opening message via InterviewerEngine."""
        focus_areas = json.loads(round_info["focus_areas"]) if isinstance(round_info.get("focus_areas"), str) else round_info.get("focus_areas", [])
        model = self.candidate_models.get(session_id)
        persona = InterviewerPersona.from_dict(interviewer)

        return self.engine.generate_opening(
            session_id=session_id,
            round_num=round_num,
            interviewer=persona,
            round_type=round_info.get("round_type", "technical"),
            focus_areas=focus_areas,
            profile_data=profile_data,
            forum_digest=forum_digest,
            briefing_notes=briefing_notes,
            candidate_model=model,
        )

    def _generate_question(
        self, session_id: str, round_num: int,
        round_info: dict, session: dict,
    ) -> str:
        """Generate the interviewer's next question.

        Uses InterviewerSwarm for the final round (multi-agent debate),
        InterviewerEngine for all earlier rounds (single LLM call).
        """
        round_transcript = self.db.get_round_transcript(session_id, round_num)

        # Get interviewer persona
        panel_json = json.loads(session["panel_json"]) if isinstance(session.get("panel_json"), str) else session.get("panel_json", [])
        interviewer = None
        for p in panel_json:
            if p["name"] == round_info["interviewer_name"]:
                interviewer = p
                break
        if not interviewer:
            interviewer = {"name": round_info["interviewer_name"], "role": round_info["interviewer_role"]}

        persona = InterviewerPersona.from_dict(interviewer)
        focus_areas = json.loads(round_info["focus_areas"]) if isinstance(round_info.get("focus_areas"), str) else round_info.get("focus_areas", [])
        forum_digest = round_info.get("forum_digest_used", "")
        live_suggestions = self.forum.get_live_suggestions(session_id, round_num)
        questions_asked = round_info.get("questions_asked", 0)
        max_questions = round_info.get("max_questions", 8)
        model = self.candidate_models.get(session_id)

        config = json.loads(session["config_json"]) if isinstance(session.get("config_json"), str) else session.get("config_json", {})
        profile_data = config.get("profile", {})

        # --- HYBRID: Use InterviewerSwarm for final round ---
        is_final = bool(round_info.get("is_final", False))
        if is_final and model:
            return self._generate_question_swarm(
                session_id, round_num, persona, round_transcript,
                model, focus_areas,
            )

        # Standard path: InterviewerEngine
        return self.engine.generate_question(
            session_id=session_id,
            round_num=round_num,
            interviewer=persona,
            round_type=round_info.get("round_type", "technical"),
            focus_areas=focus_areas,
            round_transcript=round_transcript,
            profile_data=profile_data,
            questions_asked=questions_asked,
            max_questions=max_questions,
            forum_digest=forum_digest,
            live_suggestions=live_suggestions,
            candidate_model=model,
        )

    def _generate_question_swarm(
        self,
        session_id: str,
        round_num: int,
        persona: InterviewerPersona,
        round_transcript: str,
        model: CandidateModel,
        focus_areas: List[str],
    ) -> str:
        """Use InterviewerSwarm (multi-agent debate) for the final round."""
        # Get or create swarm for this session
        if session_id not in self._swarms:
            self._swarms[session_id] = InterviewerSwarm(
                llm=self.llm,
                persona=persona,
            )
            logger.info(f"[{session_id}] Created InterviewerSwarm for final round ({persona.name})")

        swarm = self._swarms[session_id]

        # Extract last candidate answer from transcript
        last_answer = ""
        lines = round_transcript.strip().split("\n")
        for line in reversed(lines):
            if line.startswith("Candidate:"):
                last_answer = line[len("Candidate:"):].strip()
                break

        # Coverage gaps = focus areas not yet covered deeply
        coverage_gaps = list(focus_areas)

        try:
            output = swarm.think(
                candidate_answer=last_answer,
                transcript=round_transcript,
                candidate_model=model,
                coverage_gaps=coverage_gaps,
            )
            logger.info(
                f"[{session_id}] Swarm generated question: "
                f"type={output.turn_type}, confidence={output.confidence:.2f}, "
                f"elapsed={output.elapsed_seconds}s"
            )
            return output.question
        except Exception as e:
            logger.warning(f"[{session_id}] Swarm failed, falling back to engine: {e}")
            return self.engine.generate_question(
                session_id=session_id,
                round_num=round_num,
                interviewer=persona,
                round_type="final",
                focus_areas=focus_areas,
                round_transcript=round_transcript,
                profile_data={},
                questions_asked=0,
                max_questions=8,
                forum_digest="",
                live_suggestions="",
                candidate_model=model,
            )

    def _post_forum_verdict(
        self, session_id: str, panel: List[InterviewerPersona],
        config: dict, final_transcript: str,
    ):
        """After the interview is complete, each agent posts their hire/no-hire verdict to the forum."""
        model = self.candidate_models.get(session_id)
        model_summary = model.get_summary() if model else "No assessment data."
        full_forum = self.db.build_forum_digest(session_id, 999)  # Get all forum posts

        def _generate_verdict(interviewer: InterviewerPersona) -> None:
            prompt = f"""You are {interviewer.name} ({interviewer.role}). The interview is now complete.

## Your Evaluation Dimensions
{', '.join(interviewer.eval_dimensions)}

## Candidate Profile
{json.dumps(config.get('profile', {}), indent=2)[:1500]}

## Full Forum Discussion
{full_forum[:2000]}

## Candidate Assessment
{model_summary}

---

Post your FINAL VERDICT to the forum. Include:
1. Your recommendation: STRONG HIRE / HIRE / LEAN HIRE / LEAN NO HIRE / NO HIRE
2. 2-3 key reasons for your decision
3. Specific strengths you observed from your expertise area
4. Specific concerns or gaps
5. One sentence of advice for the candidate regardless of outcome

Return JSON:
```json
{{
  "recommendation": "STRONG HIRE|HIRE|LEAN HIRE|LEAN NO HIRE|NO HIRE",
  "content": "your verdict post — 4-6 sentences covering reasons, strengths, concerns, and advice"
}}
```"""

            try:
                result = self.llm.generate_json(
                    prompt=prompt,
                    system_prompt=f"You are {interviewer.name}, {interviewer.role}. Give your honest final verdict.",
                    temperature=0.5,
                )

                verdict_text = f"**{result.get('recommendation', 'PENDING')}**\n\n{result.get('content', '')}"

                self.db.create_post(
                    session_id=session_id,
                    agent_id=interviewer.name.lower().replace(" ", "_"),
                    agent_name=interviewer.name,
                    content=verdict_text,
                    topic="final_verdict",
                    post_type="verdict",
                    agent_type=interviewer.role,
                    round_num=999,  # Special round_num for verdict
                )
                logger.info(f"[{session_id}] {interviewer.name} posted verdict: {result.get('recommendation')}")
            except Exception as e:
                logger.error(f"Verdict failed for {interviewer.name}: {e}")

        # Run verdicts in parallel
        with ThreadPoolExecutor(max_workers=len(panel)) as pool:
            futures = [pool.submit(_generate_verdict, p) for p in panel]
            for f in futures:
                try:
                    f.result()
                except Exception as e:
                    logger.error(f"Verdict thread failed: {e}")

        # Kavitha posts final summary
        try:
            kavitha_prompt = f"""You are Kavitha, the screening recruiter. The interview is now complete and all panelists have posted their verdicts.

## Forum Verdicts
{self.db.build_forum_digest(session_id, 999)}

## Candidate Assessment
{model_summary}

Write a final summary wrapping up the interview. Include:
1. Overall consensus of the panel (hire/no-hire leaning)
2. The candidate's strongest and weakest areas across all rounds
3. A brief note on how the candidate compared to typical candidates at this level
4. One actionable takeaway for the candidate

4-5 sentences. Be warm but honest."""

            summary = self.llm.generate(
                prompt=kavitha_prompt,
                system_prompt="You are Kavitha, summarizing the panel's decision. Be encouraging but truthful.",
                temperature=0.5,
            )

            self.db.create_post(
                session_id=session_id,
                agent_id="kavitha_screening",
                agent_name="Kavitha",
                content=summary,
                topic="final_summary",
                post_type="verdict",
                agent_type="Screening Recruiter",
                round_num=999,
            )
            logger.info(f"[{session_id}] Kavitha posted final summary")
        except Exception as e:
            logger.warning(f"Kavitha final summary failed: {e}")

    def _post_transition_summary(
        self, session_id: str, completed_round_num: int,
        completed_round: dict, next_round: dict,
        round_transcript: str, config: dict,
        forum_posts: List[ForumPost],
    ):
        """Kavitha posts a transition summary after each round, directing the next interviewer."""
        forum_highlights = "\n".join(
            f"- {p.agent_name}: {p.content}" for p in forum_posts
        ) if forum_posts else "No forum discussion yet."

        model = self.candidate_models.get(session_id)
        model_summary = model.get_summary() if model else "No assessment data yet."

        next_focus = json.loads(next_round["focus_areas"]) if isinstance(next_round.get("focus_areas"), str) else next_round.get("focus_areas", [])

        prompt = f"""You are Kavitha, the screening recruiter coordinating this interview panel.

Round {completed_round_num} just finished. {completed_round['interviewer_name']} ({completed_round['interviewer_role']}) was the interviewer.

## What happened in Round {completed_round_num}
{round_transcript[-2000:]}

## Forum Discussion After Round {completed_round_num}
{forum_highlights}

## Candidate Assessment So Far
{model_summary}

## Next Up
Round {completed_round_num + 1}: {next_round['interviewer_name']} ({next_round['interviewer_role']})
Focus areas: {', '.join(next_focus)}

---

Write a transition post for {next_round['interviewer_name']}. Include:
1. Quick summary of how the candidate performed in Round {completed_round_num} (2 sentences)
2. Specific things {next_round['interviewer_name']} should probe based on what emerged
3. Any red flags, evasions, or contradictions to follow up on
4. The candidate's current emotional state / confidence level
5. Suggested opening angle for Round {completed_round_num + 1}

Write like a recruiter briefing a colleague between rounds. 4-6 sentences. Be specific and actionable."""

        try:
            transition = self.llm.generate(
                prompt=prompt,
                system_prompt="You are Kavitha, coordinating the interview panel. Be specific and helpful.",
                temperature=0.6,
            )

            self.db.create_post(
                session_id=session_id,
                agent_id="kavitha_screening",
                agent_name="Kavitha",
                content=transition,
                topic=f"transition_round_{completed_round_num}_to_{completed_round_num + 1}",
                post_type="strategy",
                agent_type="Screening Recruiter",
                round_num=completed_round_num,
            )
            logger.info(f"[{session_id}] Kavitha posted transition summary: R{completed_round_num} → R{completed_round_num + 1}")
        except Exception as e:
            logger.warning(f"Transition summary failed: {e}")

    def _run_live_observers(
        self, session_id: str, round_num: int,
        round_info: dict, session: dict,
        question_num: int, last_question: str, last_answer: str,
    ):
        """Fire live observer reactions asynchronously during an active round."""
        panel_json = json.loads(session["panel_json"]) if isinstance(session.get("panel_json"), str) else session.get("panel_json", [])
        panel = [InterviewerPersona.from_dict(p) for p in panel_json]

        config = json.loads(session["config_json"]) if isinstance(session.get("config_json"), str) else session.get("config_json", {})
        candidate_summary = json.dumps(config.get("profile", {}), indent=2)

        try:
            self.forum.run_live_observation(
                session_id=session_id,
                round_num=round_num,
                active_interviewer=round_info["interviewer_name"],
                question_num=question_num,
                last_question=last_question,
                last_answer=last_answer,
                panel=panel,
                candidate_summary=candidate_summary,
            )
            logger.info(f"[{session_id}] Live observers fired for Q{question_num}")
        except Exception as e:
            logger.warning(f"Live observers failed (non-fatal): {e}")

    def _get_turn_offset(self, session_id: str, round_num: int) -> int:
        """Calculate turn number offset for a given round."""
        all_turns = self.db.get_interview_turns(session_id)
        return len(all_turns)

    def get_round_status(self, session_id: str, round_num: int) -> dict:
        """Get the current status of a round."""
        round_info = self.db.get_interview_round(session_id, round_num)
        if not round_info:
            return {"error": "Round not found"}

        return {
            "round_num": round_num,
            "interviewer": round_info["interviewer_name"],
            "role": round_info["interviewer_role"],
            "status": round_info["status"],
            "questions_asked": round_info.get("questions_asked", 0),
            "max_questions": round_info.get("max_questions", 8),
            "is_final": bool(round_info.get("is_final", 0)),
        }

    def get_interview_status(self, session_id: str) -> dict:
        """Get overall interview status across all rounds."""
        session = self.db.get_interview_session(session_id)
        if not session:
            return {"error": "Session not found"}

        rounds = self.db.get_all_rounds(session_id)
        return {
            "session_id": session_id,
            "status": session["status"],
            "current_round": session.get("current_round", 0),
            "total_rounds": session.get("total_rounds", 0),
            "rounds": [
                {
                    "round_num": r["round_num"],
                    "interviewer": r["interviewer_name"],
                    "role": r["interviewer_role"],
                    "status": r["status"],
                    "questions_asked": r.get("questions_asked", 0),
                }
                for r in rounds
            ],
        }

    def evaluate_interview(self, session_id: str) -> dict:
        """
        Run evaluation across all rounds of a completed multi-round interview.
        Each panelist scores independently, then results are aggregated.
        """
        session = self.db.get_interview_session(session_id)
        if not session:
            return {"error": "Session not found"}

        if session.get("status") != "completed":
            return {"error": "Interview not yet completed"}

        # Get panel
        panel_json = json.loads(session["panel_json"]) if isinstance(
            session.get("panel_json"), str
        ) else session.get("panel_json", [])
        panel = [InterviewerPersona.from_dict(p) for p in panel_json]

        # Get full transcript across all rounds
        transcript = self.db.get_interview_turns(session_id)

        # Get candidate model if available
        candidate_model = self.candidate_models.get(session_id)

        # Run evaluation
        result = self.evaluation_engine.evaluate(
            session_id=session_id,
            panel=panel,
            transcript=transcript,
            candidate_model=candidate_model,
        )

        return result
