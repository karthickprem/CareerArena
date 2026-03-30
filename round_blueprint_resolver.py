"""
RoundBlueprintResolver — Deterministic round structure resolution.

Resolution order:
  1. Company + experience_level → match hiring track → get blueprints
  2. No company match → default_round_blueprints for domain + experience_level
  3. Nothing found → return None (caller falls back to LLM)

No LLM calls. Pure database lookup + keyword matching.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict

from knowledge_db import KnowledgeDB

logger = logging.getLogger(__name__)


@dataclass
class ResolvedRound:
    """One round in a resolved blueprint."""
    round_num: int
    round_type: str           # technical, system_design, behavioral, hr, stress, final, domain
    round_label: str          # Human-readable label
    focus_areas: List[str]
    difficulty: str           # easy, medium, hard, expert
    max_questions: int
    interviewer_role_hint: str
    personality_hint: str     # warm_but_probing, intense, skeptical, neutral, friendly
    question_style_hint: str
    eval_dimensions: List[str]
    notes: str
    is_eliminatory: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ResolvedBlueprint:
    """Complete resolved round structure for an interview."""
    company: str
    track_name: str
    track_code: str
    experience_level: str
    difficulty_tier: str       # low, medium, high, very_high
    rounds: List[ResolvedRound]
    total_rounds: int
    source: str                # "company_blueprint" | "default_blueprint"
    salary_range: str = ""
    selection_test: str = ""
    bond_years: int = 0

    def to_dict(self) -> dict:
        d = asdict(self)
        d["rounds"] = [r.to_dict() for r in self.rounds]
        return d

    @property
    def round_types(self) -> List[str]:
        return [r.round_type for r in self.rounds]


# Keywords that map to specific hiring tracks
_TRACK_KEYWORDS: Dict[str, List[str]] = {
    # TCS
    "tcs_ninja": ["ninja"],
    "tcs_digital": ["digital"],
    "tcs_prime": ["prime", "codevita"],
    # Infosys
    "infosys_se": ["systems engineer", "se"],
    "infosys_sp": ["specialist", "sp"],
    "infosys_pp": ["power programmer", "pp"],
    # Wipro
    "wipro_elite": ["elite"],
    "wipro_turbo": ["turbo"],
    # Cognizant
    "cognizant_genc": ["genc"],
    "cognizant_genc_next": ["genc next", "next"],
    "cognizant_genc_elevate": ["elevate"],
    # Accenture
    "accenture_ase": ["ase", "associate"],
    "accenture_ace": ["ace", "advanced"],
    # Capgemini
    "capgemini_analyst": ["analyst"],
    "capgemini_exceller": ["exceller"],
    # Google
    "google_l3": ["l3", "new grad", "entry"],
    "google_l4": ["l4", "mid"],
    # Amazon
    "amazon_sde1": ["sde1", "sde-1", "entry"],
    "amazon_sde2": ["sde2", "sde-2", "mid"],
    # Microsoft
    "microsoft_sde59": ["sde59", "59", "new grad", "entry"],
    "microsoft_sde60": ["sde60", "60", "mid"],
    # Flipkart
    "flipkart_sde1": ["sde1", "sde-1", "entry"],
    "flipkart_sde2": ["sde2", "sde-2", "mid"],
    # Zoho
    "zoho_fresher": ["fresher", "campus"],
    "zoho_lateral": ["lateral", "experienced"],
}


class RoundBlueprintResolver:
    """Resolves interview round structure from database without LLM."""

    def __init__(self, knowledge_db: KnowledgeDB):
        self.db = knowledge_db

    def resolve(
        self,
        company: str = "",
        experience_level: str = "fresher",
        role: str = "",
        domain: str = "software_engineering",
    ) -> Optional[ResolvedBlueprint]:
        """
        Resolve round structure deterministically.

        Args:
            company: Target company name (e.g., "TCS", "Google")
            experience_level: fresher, 1-3yr, 3-7yr, 7-12yr, 12+yr
            role: Target role text (e.g., "TCS Digital", "SDE-1")
            domain: Job domain for default fallback

        Returns:
            ResolvedBlueprint if found, None if no data available.
        """
        # Try company-specific blueprint first
        if company:
            blueprint = self._resolve_company(company, experience_level, role)
            if blueprint:
                return blueprint

        # Fallback to default blueprint
        blueprint = self._resolve_default(domain, experience_level)
        if blueprint:
            return blueprint

        logger.info("No blueprint found for company=%s level=%s domain=%s",
                     company, experience_level, domain)
        return None

    def get_available_tracks(
        self, company: str, experience_level: str = None,
    ) -> List[dict]:
        """List available hiring tracks for a company."""
        tracks = self.db.get_hiring_tracks(company, level=experience_level)
        result = []
        for t in tracks:
            result.append({
                "track_code": t["track_code"],
                "track_name": t["track_name"],
                "salary_range": t["salary_range"],
                "difficulty_tier": t["difficulty_tier"],
                "target_levels": json.loads(t["target_levels"]) if isinstance(t["target_levels"], str) else t["target_levels"],
                "is_default": bool(t.get("is_default", 0)),
            })
        return result

    # ──────────────────────────────────────────
    # Internal
    # ──────────────────────────────────────────

    def _resolve_company(
        self, company: str, level: str, role: str,
    ) -> Optional[ResolvedBlueprint]:
        """Try to resolve via company_hiring_tracks + company_round_blueprints."""
        tracks = self.db.get_hiring_tracks(company, level=level)
        if not tracks:
            logger.debug("No tracks for company=%s level=%s", company, level)
            return None

        # Match a track
        track = self._match_track(tracks, role)
        if not track:
            return None

        # Get round blueprints for this track
        rows = self.db.get_round_blueprints(company, track["track_code"])
        if not rows:
            logger.debug("No blueprints for track=%s", track["track_code"])
            return None

        rounds = self._rows_to_rounds(rows)
        elig = json.loads(track["eligibility"]) if isinstance(track["eligibility"], str) else track["eligibility"]

        return ResolvedBlueprint(
            company=company,
            track_name=track["track_name"],
            track_code=track["track_code"],
            experience_level=level,
            difficulty_tier=track["difficulty_tier"],
            rounds=rounds,
            total_rounds=len(rounds),
            source="company_blueprint",
            salary_range=track.get("salary_range", ""),
            selection_test=track.get("selection_test", ""),
            bond_years=track.get("bond_years", 0),
        )

    def _resolve_default(
        self, domain: str, level: str,
    ) -> Optional[ResolvedBlueprint]:
        """Fallback to default_round_blueprints."""
        rows = self.db.get_default_blueprints(domain, level)
        if not rows:
            logger.debug("No default blueprints for domain=%s level=%s", domain, level)
            return None

        rounds = self._rows_to_rounds(rows, is_company=False)

        return ResolvedBlueprint(
            company="",
            track_name=f"Default — {domain}",
            track_code=f"default_{domain}_{level}",
            experience_level=level,
            difficulty_tier=self._infer_tier(level),
            rounds=rounds,
            total_rounds=len(rounds),
            source="default_blueprint",
        )

    def _match_track(self, tracks: List[dict], role: str) -> Optional[dict]:
        """
        Match a track from the list using role keywords.

        Priority:
          1. Keyword match in role string → specific track
          2. No keyword match → track with is_default=1
          3. No default → lowest difficulty track
        """
        if role:
            role_lower = role.lower()
            # Check each track's keywords
            for track in tracks:
                code = track["track_code"]
                keywords = _TRACK_KEYWORDS.get(code, [])
                for kw in keywords:
                    if kw in role_lower:
                        logger.debug("Keyword '%s' matched track %s", kw, code)
                        return track

        # Fallback: is_default (tracks already sorted by is_default DESC)
        for track in tracks:
            if track.get("is_default"):
                return track

        # Last resort: lowest difficulty
        tier_order = {"low": 0, "medium": 1, "high": 2, "very_high": 3}
        return min(tracks, key=lambda t: tier_order.get(t.get("difficulty_tier", "low"), 0))

    def _rows_to_rounds(self, rows: List[dict], is_company: bool = True) -> List[ResolvedRound]:
        """Convert DB rows to ResolvedRound objects."""
        rounds = []
        for row in rows:
            focus = row.get("focus_areas", "[]")
            if isinstance(focus, str):
                focus = json.loads(focus)
            eval_dims = row.get("eval_dimensions", "[]")
            if isinstance(eval_dims, str):
                eval_dims = json.loads(eval_dims)

            rounds.append(ResolvedRound(
                round_num=row["round_num"],
                round_type=row["round_type"],
                round_label=row["round_label"],
                focus_areas=focus,
                difficulty=row["difficulty"],
                max_questions=row.get("max_questions", 6),
                interviewer_role_hint=row.get("interviewer_role_hint", ""),
                personality_hint=row.get("personality_hint", "neutral"),
                question_style_hint=row.get("question_style_hint", ""),
                eval_dimensions=eval_dims,
                notes=row.get("notes", ""),
                is_eliminatory=bool(row.get("is_eliminatory", 0)) if is_company else False,
            ))
        return rounds

    @staticmethod
    def _infer_tier(level: str) -> str:
        """Infer difficulty tier from experience level."""
        return {
            "fresher": "low",
            "1-3yr": "medium",
            "3-7yr": "high",
            "7-12yr": "very_high",
            "12+yr": "very_high",
        }.get(level, "medium")
