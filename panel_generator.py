"""
PanelGenerator — Creates a tailored interview panel + round plan from CandidateProfile.

Reads the screening profile, queries KnowledgeDB for domain-specific persona templates
and company patterns, then generates 3-4 interviewers with a round plan specifying
who interviews when and what to focus on.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict

from llm_client import LLMClient
from knowledge_db import KnowledgeDB
from screening_agent import CandidateProfile
from interviewer_personas import InterviewerPersona
from round_blueprint_resolver import RoundBlueprintResolver, ResolvedBlueprint

logger = logging.getLogger(__name__)


@dataclass
class RoundConfig:
    round_num: int
    interviewer_name: str
    interviewer_role: str
    round_type: str  # technical, behavioral, system_design, hr, domain, stress, final
    focus_areas: List[str] = field(default_factory=list)
    max_questions: int = 8
    is_final: bool = False
    briefing_notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RoundPlan:
    rounds: List[RoundConfig] = field(default_factory=list)
    total_rounds: int = 0

    def to_dict(self) -> dict:
        return {
            "rounds": [r.to_dict() for r in self.rounds],
            "total_rounds": self.total_rounds,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RoundPlan":
        rounds = [RoundConfig(**r) for r in d.get("rounds", [])]
        return cls(rounds=rounds, total_rounds=d.get("total_rounds", len(rounds)))


class PanelGenerator:
    def __init__(self, llm: LLMClient, knowledge_db: KnowledgeDB):
        self.llm = llm
        self.knowledge_db = knowledge_db
        self.resolver = RoundBlueprintResolver(knowledge_db)

    def generate_panel(
        self,
        profile: CandidateProfile,
        company: str = "",
        role: str = "",
        panel_size: int = 3,
        difficulty: str = "realistic",
    ) -> tuple[List[InterviewerPersona], RoundPlan]:
        """
        Generate a tailored panel and round plan based on the candidate profile.

        Resolution order:
          1. Blueprint from DB (deterministic round structure, LLM generates personas only)
          2. Full LLM generation (fallback for unknown companies with no default)
        """
        target_company = company or profile.target_company
        target_role = role or profile.target_role
        domain = profile.domain or "software_engineering"

        # Step 1: Try deterministic blueprint
        blueprint = self.resolver.resolve(
            company=target_company,
            experience_level=profile.experience_level,
            role=target_role,
            domain=domain,
        )

        if blueprint:
            logger.info("Using %s blueprint: %s (%d rounds)",
                        blueprint.source, blueprint.track_name, blueprint.total_rounds)
            panel, round_plan = self._generate_from_blueprint(
                blueprint, profile, target_company, target_role, difficulty,
            )
            return panel, round_plan

        # Step 2: Fall through to full LLM generation
        logger.info("No blueprint found, falling back to LLM generation")
        level = self._map_experience_to_level(profile.experience_level)
        templates = self.knowledge_db.get_persona_templates(
            domain=domain, level=level, company=target_company,
        )

        company_profile = None
        if target_company:
            company_profile = self.knowledge_db.get_company_profile(target_company)

        panel, round_plan = self._generate_with_llm(
            profile, templates, company_profile,
            target_company, target_role,
            panel_size, difficulty,
        )

        return panel, round_plan

    def _generate_from_blueprint(
        self,
        blueprint: ResolvedBlueprint,
        profile: CandidateProfile,
        company: str,
        role: str,
        difficulty: str,
    ) -> tuple[List[InterviewerPersona], RoundPlan]:
        """
        Generate panel from a deterministic blueprint.

        Round structure (count, types, focus areas, difficulty) comes from the blueprint.
        LLM only generates persona IDENTITIES (names, system prompts) for each slot.
        """
        # Build round descriptions for the LLM prompt
        round_specs = []
        for r in blueprint.rounds:
            round_specs.append(
                f"Round {r.round_num}: {r.round_label} ({r.round_type}, {r.difficulty})\n"
                f"  Role: {r.interviewer_role_hint}\n"
                f"  Personality: {r.personality_hint}\n"
                f"  Focus: {', '.join(r.focus_areas)}\n"
                f"  Style: {r.question_style_hint}\n"
                f"  Notes: {r.notes}"
            )

        prompt = f"""Generate interviewer personas for this interview panel.

## Candidate
- Name: {profile.name}
- Experience: {profile.experience_level}
- Domain: {profile.domain}
- Skills: {json.dumps(profile.skills)}
- Target: {company} — {role}
- Weaknesses: {profile.weaknesses}
- Notable Claims: {profile.notable_claims}
- Difficulty: {difficulty}

## Company & Track
- Company: {blueprint.company or 'General'}
- Track: {blueprint.track_name}
- Salary: {blueprint.salary_range}
- Difficulty Tier: {blueprint.difficulty_tier}

## Fixed Round Structure (DO NOT change the number of rounds or their types)
{chr(10).join(round_specs)}

## Task
Generate exactly {blueprint.total_rounds} interviewer personas — one per round.
Each persona must match the role hint and personality specified above.
Use realistic Indian names. Write detailed system prompts (300+ chars) that:
- Reference the candidate's specific profile
- Guide the interviewer's behavior for this round
- Include what to probe based on the candidate's weaknesses and claims

Return JSON:
```json
{{
  "interviewers": [
    {{
      "name": "Indian name",
      "role": "exact role from the round spec",
      "personality": "exact personality from the round spec",
      "question_style": "behavioral_star|deep_dive|rapid_fire|case_based|socratic",
      "eval_dimensions": ["dim1", "dim2"],
      "expertise": ["area1", "area2"],
      "interaction_style": "supportive|independent|challenging",
      "traits": {{"warmth": 0.0-1.0, "directness": 0.0-1.0, "humor": 0.0-1.0, "patience": 0.0-1.0}},
      "avatar_color": "#hex",
      "system_prompt": "Detailed system prompt for this specific candidate..."
    }}
  ]
}}
```"""

        result = self.llm.generate_json(
            prompt=prompt,
            system_prompt="You are an expert interview panel designer. Generate realistic Indian interviewer personas. Return valid JSON only.",
            temperature=0.6,
        )

        interviewers_data = result.get("interviewers", [])

        # Build panel and round plan from blueprint + LLM personas
        panel = []
        rounds = []

        for i, bp_round in enumerate(blueprint.rounds):
            # Get LLM-generated persona for this slot (or use fallback)
            if i < len(interviewers_data):
                p_data = interviewers_data[i]
            else:
                p_data = {
                    "name": f"Interviewer {i + 1}",
                    "role": bp_round.interviewer_role_hint,
                    "personality": bp_round.personality_hint,
                }

            persona = InterviewerPersona(
                name=p_data.get("name", f"Interviewer {i + 1}"),
                role=p_data.get("role", bp_round.interviewer_role_hint),
                personality=p_data.get("personality", bp_round.personality_hint),
                question_style=p_data.get("question_style", "deep_dive"),
                eval_dimensions=p_data.get("eval_dimensions", bp_round.eval_dimensions),
                expertise=p_data.get("expertise", bp_round.focus_areas),
                interaction_style=p_data.get("interaction_style", "independent"),
                traits=p_data.get("traits", {"warmth": 0.5, "directness": 0.5}),
                avatar_color=p_data.get("avatar_color", "#6366f1"),
                system_prompt=p_data.get("system_prompt", ""),
            )
            panel.append(persona)

            # Round structure is FIXED from blueprint
            rounds.append(RoundConfig(
                round_num=bp_round.round_num,
                interviewer_name=persona.name,
                interviewer_role=persona.role,
                round_type=bp_round.round_type,
                focus_areas=bp_round.focus_areas,
                max_questions=bp_round.max_questions,
                is_final=(i == len(blueprint.rounds) - 1),
                briefing_notes=bp_round.question_style_hint or bp_round.notes,
            ))

        round_plan = RoundPlan(rounds=rounds, total_rounds=len(rounds))
        return panel, round_plan

    def _map_experience_to_level(self, experience_level: str) -> str:
        mapping = {
            "fresher": "fresher",
            "1-3yr": "fresher",
            "3-7yr": "mid",
            "7-12yr": "senior",
            "12+yr": "senior",
        }
        return mapping.get(experience_level, "fresher")

    def _generate_with_llm(
        self,
        profile: CandidateProfile,
        templates: List[dict],
        company_profile: Optional[dict],
        company: str,
        role: str,
        panel_size: int,
        difficulty: str,
    ) -> tuple[List[InterviewerPersona], RoundPlan]:
        """Use LLM to generate a customized panel based on all available data."""

        templates_text = ""
        if templates:
            templates_text = "## Available Persona Templates\n"
            for t in templates:
                templates_text += f"- {t['name']} ({t['role']}): {t['personality']}, {t['question_style']}\n"

        company_text = ""
        if company_profile:
            cp = company_profile
            company_text = f"""## Company: {cp['company_name']}
Industry: {cp.get('industry', '')}
Hiring Bar: {cp.get('hiring_bar', '')}
Culture: {cp.get('culture_notes', '')}
Evaluation Priorities: {json.loads(cp['evaluation_priorities']) if isinstance(cp.get('evaluation_priorities'), str) else cp.get('evaluation_priorities', [])}
"""

        prompt = f"""Design an interview panel and round plan for this candidate.

## Candidate Profile
- Name: {profile.name}
- Experience: {profile.experience_level}
- Domain: {profile.domain}
- Skills: {json.dumps(profile.skills)}
- Education: {profile.education}
- Target Role: {role or 'Not specified'}
- Target Company: {company or 'Not specified'}
- Notable Claims to Verify: {profile.notable_claims}
- Strengths: {profile.strengths}
- Weaknesses: {profile.weaknesses}
- Communication Style: {profile.communication_style}

{templates_text}
{company_text}

## Requirements
- Panel size: {panel_size} interviewers
- Difficulty: {difficulty}
- Each interviewer conducts exactly ONE round (1-on-1)
- The final round should be HR/managerial focusing on overall fit
- Each round should target different dimensions
- Later rounds should probe gaps and verify claims from earlier rounds

## Important Design Principles
1. The panel should cover: technical depth + behavioral/HR + leadership/strategic
2. Each interviewer needs a DISTINCT personality and questioning style
3. Briefing notes should reference SPECIFIC things from the candidate's profile
4. Focus areas should target the candidate's weaknesses and verify notable claims
5. Use realistic Indian names

Return JSON:
```json
{{
  "panel": [
    {{
      "name": "Indian name",
      "role": "role title",
      "personality": "warm_but_probing|intense|skeptical|neutral|friendly",
      "question_style": "behavioral_star|deep_dive|rapid_fire|case_based|socratic",
      "eval_dimensions": ["dim1", "dim2", "dim3"],
      "expertise": ["area1", "area2"],
      "interaction_style": "supportive|independent|challenging",
      "traits": {{"warmth": 0.0-1.0, "directness": 0.0-1.0, "humor": 0.0-1.0, "patience": 0.0-1.0}},
      "avatar_color": "#hex",
      "system_prompt": "Detailed system prompt (300+ chars) defining personality, style, approach, and what to probe for this specific candidate"
    }}
  ],
  "round_plan": [
    {{
      "round_num": 1,
      "interviewer_name": "name from panel",
      "interviewer_role": "role",
      "round_type": "technical|behavioral|system_design|hr|domain|stress|final",
      "focus_areas": ["area1", "area2"],
      "max_questions": 6-8,
      "is_final": false,
      "briefing_notes": "What this interviewer should know/probe about this specific candidate"
    }}
  ]
}}
```"""

        result = self.llm.generate_json(
            prompt=prompt,
            system_prompt="You are an expert interview panel designer. Create realistic, tailored interview panels for Indian candidates. Return valid JSON only.",
            temperature=0.6,
        )

        # Build InterviewerPersona objects
        panel = []
        for p_data in result.get("panel", []):
            persona = InterviewerPersona(
                name=p_data.get("name", "Interviewer"),
                role=p_data.get("role", "Interviewer"),
                personality=p_data.get("personality", "neutral"),
                question_style=p_data.get("question_style", "deep_dive"),
                eval_dimensions=p_data.get("eval_dimensions", []),
                expertise=p_data.get("expertise", []),
                interaction_style=p_data.get("interaction_style", "independent"),
                traits=p_data.get("traits", {"warmth": 0.5, "directness": 0.5}),
                avatar_color=p_data.get("avatar_color", "#6366f1"),
                system_prompt=p_data.get("system_prompt", ""),
            )
            panel.append(persona)

        # Build RoundPlan
        rounds = []
        for r_data in result.get("round_plan", []):
            rc = RoundConfig(
                round_num=r_data.get("round_num", len(rounds) + 1),
                interviewer_name=r_data.get("interviewer_name", ""),
                interviewer_role=r_data.get("interviewer_role", ""),
                round_type=r_data.get("round_type", "technical"),
                focus_areas=r_data.get("focus_areas", []),
                max_questions=r_data.get("max_questions", 8),
                is_final=r_data.get("is_final", False),
                briefing_notes=r_data.get("briefing_notes", ""),
            )
            rounds.append(rc)

        round_plan = RoundPlan(rounds=rounds, total_rounds=len(rounds))

        # Fallback: if LLM returned empty, use templates
        if not panel:
            panel, round_plan = self._fallback_panel(profile, panel_size)

        return panel, round_plan

    def _fallback_panel(
        self, profile: CandidateProfile, panel_size: int
    ) -> tuple[List[InterviewerPersona], RoundPlan]:
        """Fallback: build panel from knowledge DB templates."""
        domain = profile.domain or "software_engineering"
        level = self._map_experience_to_level(profile.experience_level)
        target_company = getattr(profile, 'target_company', '') or ''
        templates = self.knowledge_db.get_persona_templates(
            domain=domain, level=level, company=target_company,
        )

        panel = []
        rounds = []

        # Always include an HR interviewer
        hr_templates = self.knowledge_db.get_persona_templates(
            role="HR Lead", company=target_company,
        )
        if hr_templates:
            t = hr_templates[0]
            panel.append(self._template_to_persona(t))

        # Add domain-specific interviewers
        for t in templates[:panel_size - 1]:
            if t["name"] not in [p.name for p in panel]:
                panel.append(self._template_to_persona(t))

        # Build round plan
        round_types = ["technical", "behavioral", "final"]
        for i, persona in enumerate(panel):
            is_final = (i == len(panel) - 1)
            rounds.append(RoundConfig(
                round_num=i + 1,
                interviewer_name=persona.name,
                interviewer_role=persona.role,
                round_type=round_types[i] if i < len(round_types) else "technical",
                focus_areas=persona.eval_dimensions[:3],
                max_questions=8,
                is_final=is_final,
                briefing_notes=f"Focus on: {', '.join(persona.eval_dimensions[:3])}",
            ))

        return panel, RoundPlan(rounds=rounds, total_rounds=len(rounds))

    def _template_to_persona(self, template: dict) -> InterviewerPersona:
        """Convert a knowledge DB template row to an InterviewerPersona."""
        return InterviewerPersona(
            name=template["name"],
            role=template["role"],
            personality=template["personality"],
            question_style=template["question_style"],
            eval_dimensions=json.loads(template["eval_dimensions"]) if isinstance(template.get("eval_dimensions"), str) else template.get("eval_dimensions", []),
            expertise=json.loads(template["expertise"]) if isinstance(template.get("expertise"), str) else template.get("expertise", []),
            interaction_style=template.get("interaction_style", "independent"),
            traits=json.loads(template["traits"]) if isinstance(template.get("traits"), str) else template.get("traits", {}),
            avatar_color=template.get("avatar_color", "#6366f1"),
            system_prompt=template.get("system_prompt", ""),
        )
