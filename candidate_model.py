"""
Candidate Model — real-time assessment of the interviewee.

Built and updated after EVERY candidate answer. This is what makes
the interview feel intelligent: the system builds a mental model
of the candidate and adjusts its behavior accordingly.

The model feeds into:
  - Swarm debate agents (each sees the current model)
  - Orchestrator decisions (difficulty adjustment, topic selection)
  - Evaluation engine (final scoring is informed by trajectory)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from llm_client import LLMClient


@dataclass
class AnswerAnalysis:
    """Analysis of a single candidate answer."""
    strengths_shown: List[str] = field(default_factory=list)
    weaknesses_shown: List[str] = field(default_factory=list)
    depth_score: float = 0.5  # 0 = surface, 1 = expert-level
    confidence_signals: float = 0.5  # 0 = very uncertain, 1 = very confident
    evasion_detected: bool = False
    contradiction_detected: bool = False
    contradiction_detail: str = ""
    response_pattern: str = "normal"  # rehearsed, authentic, rambling, concise, evasive
    emotional_state: str = "neutral"  # nervous, confident, defensive, enthusiastic, frustrated
    notable_claims: List[str] = field(default_factory=list)
    knowledge_boundary: str = ""  # "knows X but not Y"


@dataclass
class CandidateModel:
    """
    Accumulated model of the candidate, updated after every answer.

    This is NOT a static profile — it evolves through the interview.
    """
    # Assessed capabilities (grow over time)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)

    # Dimension-level assessment (0-1 for each)
    assessed_dimensions: Dict[str, float] = field(default_factory=dict)

    # Knowledge map: what we know they know / don't know
    knowledge_map: Dict[str, str] = field(default_factory=dict)  # topic -> "strong" / "weak" / "unknown"

    # Behavioral tracking
    confidence_trajectory: List[float] = field(default_factory=list)  # per-answer confidence
    depth_trajectory: List[float] = field(default_factory=list)  # per-answer depth
    evasion_count: int = 0
    contradiction_count: int = 0
    contradictions: List[str] = field(default_factory=list)

    # Overall emotional arc
    emotional_arc: List[str] = field(default_factory=list)  # ["neutral", "nervous", "recovering", ...]
    current_emotional_state: str = "neutral"

    # Response patterns
    response_patterns: Dict[str, int] = field(default_factory=dict)  # pattern -> count
    dominant_pattern: str = "normal"

    # Claims made (for cross-referencing / contradiction detection)
    claims: List[str] = field(default_factory=list)

    # Overall assessment
    overall_impression: str = ""
    recommended_difficulty: str = "realistic"  # practice, realistic, stress_test

    def update(self, analysis: AnswerAnalysis):
        """Update the model with a new answer analysis."""
        # Merge strengths/weaknesses (deduplicate)
        for s in analysis.strengths_shown:
            if s not in self.strengths:
                self.strengths.append(s)
        for w in analysis.weaknesses_shown:
            if w not in self.weaknesses:
                self.weaknesses.append(w)

        # Track trajectories
        self.confidence_trajectory.append(analysis.confidence_signals)
        self.depth_trajectory.append(analysis.depth_score)

        # Evasion / contradiction
        if analysis.evasion_detected:
            self.evasion_count += 1
        if analysis.contradiction_detected:
            self.contradiction_count += 1
            if analysis.contradiction_detail:
                self.contradictions.append(analysis.contradiction_detail)

        # Emotional arc
        self.emotional_arc.append(analysis.emotional_state)
        self.current_emotional_state = analysis.emotional_state

        # Response patterns
        p = analysis.response_pattern
        self.response_patterns[p] = self.response_patterns.get(p, 0) + 1
        self.dominant_pattern = max(self.response_patterns, key=self.response_patterns.get)

        # Knowledge map
        if analysis.knowledge_boundary:
            parts = analysis.knowledge_boundary.split(" but ")
            if len(parts) == 2:
                self.knowledge_map[parts[0].strip()] = "strong"
                self.knowledge_map[parts[1].strip()] = "weak"

        # Claims
        self.claims.extend(analysis.notable_claims)

        # Adjust recommended difficulty
        self._update_difficulty()

    def _update_difficulty(self):
        """Adjust difficulty based on performance trajectory."""
        if len(self.depth_trajectory) < 3:
            return

        recent_depth = sum(self.depth_trajectory[-3:]) / 3
        recent_confidence = sum(self.confidence_trajectory[-3:]) / 3

        if recent_depth > 0.75 and recent_confidence > 0.7:
            self.recommended_difficulty = "stress_test"
        elif recent_depth < 0.35 or (self.evasion_count > 2 and recent_confidence < 0.4):
            self.recommended_difficulty = "practice"
        else:
            self.recommended_difficulty = "realistic"

    def get_summary(self) -> str:
        """Text summary for feeding into agent prompts."""
        lines = []
        if self.strengths:
            lines.append(f"STRENGTHS: {', '.join(self.strengths[:5])}")
        if self.weaknesses:
            lines.append(f"WEAKNESSES: {', '.join(self.weaknesses[:5])}")
        if self.knowledge_map:
            strong = [k for k, v in self.knowledge_map.items() if v == "strong"]
            weak = [k for k, v in self.knowledge_map.items() if v == "weak"]
            if strong:
                lines.append(f"STRONG ON: {', '.join(strong[:4])}")
            if weak:
                lines.append(f"WEAK ON: {', '.join(weak[:4])}")
        lines.append(f"EMOTIONAL STATE: {self.current_emotional_state}")
        if self.evasion_count > 0:
            lines.append(f"EVASIONS: {self.evasion_count} times")
        if self.contradiction_count > 0:
            lines.append(f"CONTRADICTIONS: {self.contradiction_count} — {'; '.join(self.contradictions[:2])}")

        avg_depth = sum(self.depth_trajectory) / len(self.depth_trajectory) if self.depth_trajectory else 0.5
        lines.append(f"AVERAGE DEPTH: {avg_depth:.0%} | PATTERN: {self.dominant_pattern}")
        lines.append(f"RECOMMENDED DIFFICULTY: {self.recommended_difficulty}")
        return "\n".join(lines)

    def get_emotional_read(self) -> str:
        """Summary of emotional state for the empathy reader agent."""
        if len(self.emotional_arc) < 2:
            return f"Current state: {self.current_emotional_state}. Too early for trend analysis."

        recent = self.emotional_arc[-3:]
        trend = "stable"
        if recent[-1] in ("nervous", "frustrated", "defensive") and recent[0] in ("neutral", "confident"):
            trend = "declining"
        elif recent[-1] in ("confident", "enthusiastic") and recent[0] in ("nervous", "neutral"):
            trend = "improving"

        recent_confidence = self.confidence_trajectory[-3:] if len(self.confidence_trajectory) >= 3 else self.confidence_trajectory
        avg_conf = sum(recent_confidence) / len(recent_confidence) if recent_confidence else 0.5

        return (
            f"Current: {self.current_emotional_state} | Trend: {trend} | "
            f"Confidence: {avg_conf:.0%} | Arc: {' -> '.join(self.emotional_arc[-5:])}"
        )

    def to_dict(self) -> dict:
        return {
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "assessed_dimensions": self.assessed_dimensions,
            "knowledge_map": self.knowledge_map,
            "evasion_count": self.evasion_count,
            "contradiction_count": self.contradiction_count,
            "contradictions": self.contradictions,
            "current_emotional_state": self.current_emotional_state,
            "emotional_arc": self.emotional_arc,
            "dominant_pattern": self.dominant_pattern,
            "recommended_difficulty": self.recommended_difficulty,
            "confidence_trajectory": self.confidence_trajectory,
            "depth_trajectory": self.depth_trajectory,
            "claims": self.claims,
            "response_patterns": self.response_patterns,
            "knowledge_map": self.knowledge_map,
            "overall_impression": self.overall_impression,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CandidateModel":
        """Restore a CandidateModel from a serialized dict."""
        m = cls(
            strengths=d.get("strengths", []),
            weaknesses=d.get("weaknesses", []),
            assessed_dimensions=d.get("assessed_dimensions", {}),
            knowledge_map=d.get("knowledge_map", {}),
            confidence_trajectory=d.get("confidence_trajectory", []),
            depth_trajectory=d.get("depth_trajectory", []),
            evasion_count=d.get("evasion_count", 0),
            contradiction_count=d.get("contradiction_count", 0),
            contradictions=d.get("contradictions", []),
            emotional_arc=d.get("emotional_arc", []),
            current_emotional_state=d.get("current_emotional_state", "neutral"),
            response_patterns=d.get("response_patterns", {}),
            dominant_pattern=d.get("dominant_pattern", "normal"),
            claims=d.get("claims", []),
            overall_impression=d.get("overall_impression", ""),
            recommended_difficulty=d.get("recommended_difficulty", "realistic"),
        )
        return m


class CandidateAnalyzer:
    """Uses LLM to analyze each candidate answer and update the model."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def analyze_answer(
        self,
        answer: str,
        question: str,
        transcript_so_far: str,
        candidate_model: CandidateModel,
    ) -> AnswerAnalysis:
        """Analyze a candidate's answer against context."""
        previous_claims = "; ".join(candidate_model.claims[-10:]) if candidate_model.claims else "None yet"

        prompt = f"""Analyze this interview candidate's answer.

QUESTION ASKED:
{question[:500]}

CANDIDATE'S ANSWER:
{answer[:2000]}

PREVIOUS CLAIMS BY CANDIDATE:
{previous_claims}

CURRENT MODEL:
{candidate_model.get_summary()}

Analyze deeply — like a senior interviewer reading between the lines.

Return JSON:
```json
{{
  "strengths_shown": ["specific strength demonstrated in this answer"],
  "weaknesses_shown": ["specific weakness or gap revealed"],
  "depth_score": 0.0-1.0,
  "confidence_signals": 0.0-1.0,
  "evasion_detected": false,
  "contradiction_detected": false,
  "contradiction_detail": "if detected, what contradicts what",
  "response_pattern": "one of: rehearsed, authentic, rambling, concise, evasive, normal",
  "emotional_state": "one of: nervous, confident, defensive, enthusiastic, frustrated, neutral, recovering",
  "notable_claims": ["specific factual claims to track for later cross-referencing"],
  "knowledge_boundary": "knows X but not Y (single sentence or empty string)"
}}
```"""

        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt=(
                    "You are an expert interviewer psychologist. Analyze candidate answers for "
                    "depth, authenticity, emotional signals, evasions, and contradictions. "
                    "Be precise. Output valid JSON only."
                ),
                temperature=0.2,
            )

            return AnswerAnalysis(
                strengths_shown=result.get("strengths_shown", []),
                weaknesses_shown=result.get("weaknesses_shown", []),
                depth_score=float(result.get("depth_score", 0.5)),
                confidence_signals=float(result.get("confidence_signals", 0.5)),
                evasion_detected=bool(result.get("evasion_detected", False)),
                contradiction_detected=bool(result.get("contradiction_detected", False)),
                contradiction_detail=result.get("contradiction_detail", ""),
                response_pattern=result.get("response_pattern", "normal"),
                emotional_state=result.get("emotional_state", "neutral"),
                notable_claims=result.get("notable_claims", []),
                knowledge_boundary=result.get("knowledge_boundary", ""),
            )
        except Exception:
            return AnswerAnalysis()
