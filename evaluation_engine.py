"""
Evaluation Engine — multi-dimensional scoring by each panelist.

After the interview ends, each panelist independently scores the candidate
across their evaluation dimensions. Scores are aggregated into a final
scorecard with detailed feedback and actionable recommendations.
"""

from __future__ import annotations

import json
from typing import Dict, List, Optional

from llm_client import LLMClient
from database import CareerDB
from interviewer_personas import InterviewerPersona


EVALUATION_DIMENSIONS = {
    "communication": "Clarity of expression, structured responses, articulation",
    "technical_depth": "Depth of technical knowledge, accuracy, problem-solving",
    "problem_solving": "Analytical approach, breaking down problems, creative solutions",
    "leadership": "Ownership, initiative, ability to lead and influence",
    "domain_knowledge": "Industry awareness, domain expertise, practical understanding",
    "confidence": "Composure, conviction in answers, handling pressure",
    "structured_thinking": "Organized responses, logical flow, STAR format usage",
    "culture_fit": "Values alignment, teamwork, adaptability",
    "self_awareness": "Understanding strengths/weaknesses, growth mindset",
    "handling_pressure": "Composure under stress, recovery from tough questions",
    "motivation": "Genuine interest, preparation, career clarity",
    "quick_thinking": "Speed of response, thinking on feet, adaptability",
    "strategic_thinking": "Big picture view, connecting dots, long-term perspective",
    "practical_application": "Applying theory to real scenarios, pragmatism",
    "analytical_thinking": "Data-driven reasoning, evaluating trade-offs",
    "current_affairs": "Awareness of recent events, ability to form opinions",
    "india_awareness": "Understanding of India's challenges, governance, society",
    "personality": "Overall impression, authenticity, maturity",
    "integrity": "Honesty, ethical reasoning, moral clarity",
    "balanced_perspective": "Seeing multiple sides, nuanced thinking",
    "composure": "Maintaining calm, graceful handling of tough situations",
    "conviction": "Standing by positions when challenged, intellectual courage",
    "intellectual_curiosity": "Asking good questions, desire to learn, depth of interests",
    "ownership": "Taking responsibility, not deflecting blame",
}


class EvaluationEngine:
    def __init__(self, llm: LLMClient, db: CareerDB):
        self.llm = llm
        self.db = db

    def evaluate(
        self,
        session_id: str,
        panel: List[InterviewerPersona],
        transcript: List[dict],
        candidate_model=None,
    ) -> dict:
        """
        Run full evaluation — each panelist scores independently,
        then aggregate into final scorecard.

        If a CandidateModel is provided, its accumulated insights
        (emotional arc, evasions, contradictions, knowledge map) are
        included in each panelist's evaluation prompt for richer scoring.
        """
        transcript_text = self._format_transcript(transcript)

        # Build candidate model context if available
        model_context = ""
        if candidate_model:
            model_context = f"""
CANDIDATE MODEL (accumulated during interview):
{candidate_model.get_summary()}

EMOTIONAL ARC: {' -> '.join(candidate_model.emotional_arc[-10:])}
EVASION COUNT: {candidate_model.evasion_count}
CONTRADICTION COUNT: {candidate_model.contradiction_count}
{('CONTRADICTIONS: ' + '; '.join(candidate_model.contradictions[:3])) if candidate_model.contradictions else ''}
"""

        # Each panelist evaluates independently
        evaluations = {}
        for persona in panel:
            eval_result = self._evaluate_as_panelist(
                persona, transcript_text, session_id, model_context
            )
            evaluations[persona.name] = {
                "role": persona.role,
                "scores": eval_result.get("scores", {}),
                "overall_impression": eval_result.get("overall_impression", ""),
                "key_observations": eval_result.get("key_observations", []),
                "recommendation": eval_result.get("recommendation", ""),
            }

            # Save individual scores to DB
            for dim, score_data in eval_result.get("scores", {}).items():
                self.db.add_interview_score(
                    session_id=session_id,
                    evaluator_agent=persona.name,
                    evaluator_role=persona.role,
                    dimension=dim,
                    score=score_data.get("score", 5),
                    evidence=score_data.get("evidence", ""),
                    feedback=score_data.get("feedback", ""),
                )

        # Aggregate scores
        aggregated = self.db.get_aggregated_scores(session_id)

        # Generate action items
        action_items = self._generate_action_items(
            evaluations, aggregated, transcript_text
        )

        return {
            "session_id": session_id,
            "overall": aggregated.get("overall", 0),
            "dimensions": aggregated.get("dimensions", {}),
            "by_evaluator": evaluations,
            "action_items": action_items,
            "summary": self._generate_summary(evaluations, aggregated),
        }

    def _evaluate_as_panelist(
        self,
        persona: InterviewerPersona,
        transcript: str,
        session_id: str,
        model_context: str = "",
    ) -> dict:
        """Have a single panelist evaluate the candidate."""
        dimensions_to_score = persona.eval_dimensions
        dim_descriptions = "\n".join(
            f"- {d}: {EVALUATION_DIMENSIONS.get(d, d)}"
            for d in dimensions_to_score
        )

        prompt = f"""You just completed a panel interview. Review the transcript and score the candidate.

INTERVIEW TRANSCRIPT:
{transcript[:6000]}
{model_context}
YOUR EVALUATION DIMENSIONS:
{dim_descriptions}

Score each dimension from 1-10 with specific evidence from the transcript.

Return JSON:
```json
{{
  "scores": {{
    "{dimensions_to_score[0]}": {{
      "score": 7,
      "evidence": "Specific quote or behavior from the transcript",
      "feedback": "What the candidate did well and what to improve"
    }}
  }},
  "overall_impression": "2-3 sentence summary of the candidate's performance",
  "key_observations": [
    "Observation 1 with evidence",
    "Observation 2 with evidence"
  ],
  "recommendation": "hire / maybe / pass — with brief reasoning"
}}
```

Score ALL dimensions listed above. Be specific with evidence — cite actual answers."""

        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt=persona.system_prompt + "\n\nYou are now evaluating the candidate post-interview. Be honest, fair, and specific.",
                temperature=0.3,
            )
            return result
        except Exception:
            # Fallback with neutral scores
            return {
                "scores": {d: {"score": 5, "evidence": "", "feedback": ""} for d in dimensions_to_score},
                "overall_impression": "Unable to generate detailed evaluation.",
                "key_observations": [],
                "recommendation": "maybe",
            }

    def _generate_action_items(
        self,
        evaluations: dict,
        aggregated: dict,
        transcript: str,
    ) -> List[dict]:
        """Generate actionable improvement recommendations."""
        dims = aggregated.get("dimensions", {})
        weak_areas = sorted(dims.items(), key=lambda x: x[1])[:3]

        prompt = f"""Based on this interview evaluation, generate 4-5 specific, actionable improvement recommendations.

SCORES:
{json.dumps(dims, indent=2)}

WEAKEST AREAS: {', '.join(f'{d} ({s}/10)' for d, s in weak_areas)}

PANELIST FEEDBACK:
{json.dumps({name: ev.get('key_observations', []) for name, ev in evaluations.items()}, indent=2)}

Return JSON:
```json
{{
  "action_items": [
    {{
      "priority": "high",
      "area": "dimension name",
      "recommendation": "Specific action to take",
      "practice_tip": "How to practice this skill"
    }}
  ]
}}
```"""

        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt="You are a career coach generating actionable interview improvement advice. Be specific and practical.",
                temperature=0.4,
            )
            return result.get("action_items", [])
        except Exception:
            return [
                {
                    "priority": "high",
                    "area": weak_areas[0][0] if weak_areas else "general",
                    "recommendation": "Practice with more mock interviews",
                    "practice_tip": "Focus on structured responses using the STAR method",
                }
            ]

    def _generate_summary(self, evaluations: dict, aggregated: dict) -> str:
        """Generate a brief text summary."""
        overall = aggregated.get("overall", 0)
        dims = aggregated.get("dimensions", {})

        strong = [d for d, s in dims.items() if s >= 7]
        weak = [d for d, s in dims.items() if s < 5]

        lines = [f"Overall Score: {overall}/10"]
        if strong:
            lines.append(f"Strengths: {', '.join(strong)}")
        if weak:
            lines.append(f"Needs Improvement: {', '.join(weak)}")

        recs = [ev.get("recommendation", "") for ev in evaluations.values()]
        hire_count = sum(1 for r in recs if "hire" in r.lower() and "not" not in r.lower())
        lines.append(f"Panel Verdict: {hire_count}/{len(recs)} recommend hire")

        return " | ".join(lines)

    def generate_skill_gap_report(
        self,
        session_id: str,
        candidate_model=None,
        target_company: str = "",
        target_role: str = "",
    ) -> dict:
        """
        Generate a structured skill gap report from evaluation scores + candidate model.

        Returns gap analysis with: current level, required level, gap severity,
        and specific improvement plan for each weak dimension.
        """
        aggregated = self.db.get_aggregated_scores(session_id)
        dims = aggregated.get("dimensions", {})

        # Build knowledge map from candidate model if available
        knowledge_context = ""
        if candidate_model:
            km = getattr(candidate_model, "knowledge_map", {})
            strong_topics = [k for k, v in km.items() if v == "strong"]
            weak_topics = [k for k, v in km.items() if v == "weak"]
            knowledge_context = (
                f"STRONG TOPICS: {', '.join(strong_topics) if strong_topics else 'None identified'}\n"
                f"WEAK TOPICS: {', '.join(weak_topics) if weak_topics else 'None identified'}\n"
                f"EVASION COUNT: {candidate_model.evasion_count}\n"
                f"DOMINANT RESPONSE PATTERN: {candidate_model.dominant_pattern}\n"
            )

        prompt = f"""Analyze this candidate's interview performance and generate a skill gap report.

TARGET COMPANY: {target_company or 'General'}
TARGET ROLE: {target_role or 'Software Engineer'}

INTERVIEW SCORES (1-10 scale):
{json.dumps(dims, indent=2)}

{knowledge_context}

Generate a skill gap report with:
1. Each dimension scored, categorized as: ready (7+), needs_work (4-6), critical_gap (<4)
2. For each gap, a specific 2-4 week improvement plan
3. Overall readiness percentage
4. Top 3 priorities to work on immediately

Return JSON:
```json
{{
  "readiness_pct": 0-100,
  "gaps": [
    {{
      "dimension": "dimension_name",
      "current_score": 5,
      "required_score": 7,
      "severity": "ready|needs_work|critical_gap",
      "gap_description": "What's missing and why it matters",
      "improvement_plan": "Specific 2-4 week plan with daily actions",
      "resources": ["resource1", "resource2"]
    }}
  ],
  "top_priorities": [
    {{
      "area": "dimension",
      "action": "What to do this week",
      "expected_improvement": "What success looks like"
    }}
  ],
  "overall_assessment": "2-3 sentence summary of readiness"
}}
```"""

        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt=(
                    "You are an expert career coach for Indian engineering students. "
                    "Generate practical, actionable skill gap reports. "
                    "Recommendations should be specific to Indian placement interviews. "
                    "Return valid JSON only."
                ),
                temperature=0.3,
            )
            return {
                "session_id": session_id,
                "target_company": target_company,
                "target_role": target_role,
                "readiness_pct": result.get("readiness_pct", 0),
                "gaps": result.get("gaps", []),
                "top_priorities": result.get("top_priorities", []),
                "overall_assessment": result.get("overall_assessment", ""),
                "scores": dims,
            }
        except Exception:
            # Fallback: compute from raw scores
            gaps = []
            for dim, score in sorted(dims.items(), key=lambda x: x[1]):
                severity = "ready" if score >= 7 else ("needs_work" if score >= 4 else "critical_gap")
                gaps.append({
                    "dimension": dim,
                    "current_score": score,
                    "required_score": 7,
                    "severity": severity,
                    "gap_description": EVALUATION_DIMENSIONS.get(dim, dim),
                    "improvement_plan": "Practice with mock interviews focusing on this area.",
                    "resources": [],
                })
            critical = [g for g in gaps if g["severity"] == "critical_gap"]
            needs_work = [g for g in gaps if g["severity"] == "needs_work"]
            ready_count = sum(1 for g in gaps if g["severity"] == "ready")
            readiness = int(ready_count / max(len(gaps), 1) * 100)
            return {
                "session_id": session_id,
                "target_company": target_company,
                "target_role": target_role,
                "readiness_pct": readiness,
                "gaps": gaps,
                "top_priorities": [
                    {"area": g["dimension"], "action": "Focus on improving this area", "expected_improvement": "Score 7+"}
                    for g in (critical + needs_work)[:3]
                ],
                "overall_assessment": f"Readiness: {readiness}%. {len(critical)} critical gaps, {len(needs_work)} areas need work.",
                "scores": dims,
            }

    def _format_transcript(self, transcript: List[dict]) -> str:
        """Format transcript list into readable text."""
        lines = []
        for t in transcript:
            role = f" ({t.get('speaker_role', '')})" if t.get("speaker_role") else ""
            lines.append(f"[Turn {t.get('turn_number', '?')}] {t['speaker']}{role}: {t['content']}")
        return "\n\n".join(lines)
