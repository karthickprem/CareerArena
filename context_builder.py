"""
Context Builder — prepares the full context object that agents consume.
Takes the routed query + resume data + DB history and builds a rich
context dict that every agent receives.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from query_router import RoutedQuery, QueryType


@dataclass
class SessionContext:
    session_id: str
    user_id: Optional[str]
    query: RoutedQuery
    resume_data: Optional[Dict[str, Any]] = None
    user_preferences: Optional[Dict[str, Any]] = None
    previous_sessions: List[Dict[str, Any]] = field(default_factory=list)
    tool_results: Dict[str, Any] = field(default_factory=dict)
    agent_directives: List[str] = field(default_factory=list)
    companies_context: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class ContextBuilder:
    def __init__(self, db=None):
        self._db = db

    def build(
        self,
        query: RoutedQuery,
        user_id: Optional[str] = None,
        resume_data: Optional[dict] = None,
    ) -> SessionContext:
        session_id = str(uuid.uuid4())[:12]

        user_prefs = None
        previous = []
        if self._db and user_id:
            user_prefs = self._load_user_preferences(user_id)
            previous = self._load_previous_sessions(user_id, limit=5)

        directives = self._generate_directives(query, resume_data)

        ctx = SessionContext(
            session_id=session_id,
            user_id=user_id,
            query=query,
            resume_data=resume_data,
            user_preferences=user_prefs,
            previous_sessions=previous,
            agent_directives=directives,
        )

        if self._db:
            effective_uid = user_id or "anonymous"
            if not self._db.get_user(effective_uid):
                self._db.create_user(user_id=effective_uid, email=None, name=effective_uid)
            self._db.create_session(
                session_id=session_id,
                user_id=effective_uid,
                query_text=query.original_query,
                query_type=query.query_type.value,
            )

        return ctx

    def enrich_with_tool_results(
        self, ctx: SessionContext, tool_name: str, result: dict
    ) -> None:
        ctx.tool_results[tool_name] = result

    def add_company_context(
        self, ctx: SessionContext, company: str, data: dict
    ) -> None:
        ctx.companies_context[company] = data

    def to_agent_prompt_context(self, ctx: SessionContext) -> str:
        """Serialize context into a text block agents can consume."""
        parts = []

        parts.append(f"## Session: {ctx.session_id}")
        parts.append(f"**Query**: {ctx.query.original_query}")
        parts.append(f"**Type**: {ctx.query.query_type.value}")
        parts.append(f"**Target Companies**: {', '.join(ctx.query.companies) or 'None specified'}")
        parts.append(f"**Target Roles**: {', '.join(ctx.query.roles) or 'Not specified'}")

        if ctx.resume_data:
            parts.append("\n## Resume Summary")
            rd = ctx.resume_data
            if rd.get("name"):
                parts.append(f"**Name**: {rd['name']}")
            if rd.get("skills"):
                parts.append(f"**Skills**: {', '.join(rd['skills'][:20])}")
            if rd.get("experience"):
                exp = rd["experience"]
                if isinstance(exp, list):
                    parts.append(f"**Experience**: {len(exp)} positions")
                    for e in exp[:3]:
                        parts.append(f"  - {e}")
                else:
                    parts.append(f"**Experience**: {exp}")
            if rd.get("education"):
                parts.append(f"**Education**: {rd['education']}")
            if rd.get("years_experience"):
                parts.append(f"**Years**: ~{rd['years_experience']}")

        if ctx.tool_results:
            parts.append("\n## Research Data")
            for tool_name, result in ctx.tool_results.items():
                parts.append(f"\n### {tool_name}")
                if isinstance(result, str):
                    parts.append(result[:2000])
                elif isinstance(result, dict):
                    parts.append(json.dumps(result, indent=2)[:2000])

        if ctx.companies_context:
            parts.append("\n## Company Intelligence")
            for company, data in ctx.companies_context.items():
                parts.append(f"\n### {company}")
                if isinstance(data, str):
                    parts.append(data[:1500])
                elif isinstance(data, dict):
                    parts.append(json.dumps(data, indent=2)[:1500])

        if ctx.agent_directives:
            parts.append("\n## Directives")
            for d in ctx.agent_directives:
                parts.append(f"- {d}")

        if ctx.previous_sessions:
            parts.append("\n## User History")
            parts.append(f"Previous sessions: {len(ctx.previous_sessions)}")
            for sess in ctx.previous_sessions[:3]:
                parts.append(
                    f"  - [{sess.get('query_type', '?')}] "
                    f"{sess.get('query_text', '')[:80]}"
                )

        return "\n".join(parts)

    def _generate_directives(
        self, query: RoutedQuery, resume_data: Optional[dict]
    ) -> list:
        directives = [
            "Be specific and evidence-based. Cite sources when possible.",
            "Focus on actionable insights, not generic advice.",
            "If data is uncertain, say so. Never fabricate salary figures.",
        ]

        type_directives = {
            QueryType.PROFILE_REVIEW: [
                "Be honest but constructive. Identify gaps AND strengths.",
                "Suggest specific improvements with examples.",
            ],
            QueryType.CAREER_STRATEGY: [
                "Consider multiple career paths and trade-offs.",
                "Factor in market timing and industry trends.",
            ],
            QueryType.INTERVIEW_READINESS: [
                "Assess honestly — don't sugarcoat weaknesses.",
                "Give a clear readiness score with rationale.",
            ],
            QueryType.SALARY_INTEL: [
                "Provide ranges, not single numbers.",
                "Break down: base + bonus + stocks + perks.",
            ],
            QueryType.OFFER_COMPARISON: [
                "Compare on: total comp, growth, learning, stability, culture.",
                "Use a scoring matrix for objectivity.",
            ],
            QueryType.INTERVIEW_PREP: [
                "Tailor prep to the specific company's known interview style.",
                "Include practice problems and behavioral question templates.",
            ],
            QueryType.NEGOTIATION: [
                "Provide specific scripts and counter-offer templates.",
                "Account for Indian market norms (notice period, joining bonus).",
            ],
            QueryType.SKILL_PLANNING: [
                "Prioritize skills by market demand and salary impact.",
                "Suggest specific resources (courses, projects, certifications).",
            ],
            QueryType.COMPANY_RESEARCH: [
                "Cover: funding, culture, engineering quality, WLB, growth trajectory.",
                "Include red flags and green flags.",
            ],
        }

        directives.extend(type_directives.get(query.query_type, []))

        if resume_data:
            years = resume_data.get("years_experience", 0)
            if years and years < 2:
                directives.append(
                    "User is early-career. Emphasize learning opportunities over pay."
                )
            elif years and years > 8:
                directives.append(
                    "User is senior. Focus on leadership, impact, and total comp."
                )

        return directives

    def _load_user_preferences(self, user_id: str) -> Optional[dict]:
        if not self._db:
            return None
        try:
            user = self._db.get_user(user_id)
            if user and user.get("preferences"):
                return json.loads(user["preferences"]) if isinstance(
                    user["preferences"], str
                ) else user["preferences"]
        except Exception:
            pass
        return None

    def _load_previous_sessions(
        self, user_id: str, limit: int = 5
    ) -> list:
        if not self._db:
            return []
        try:
            return self._db.get_user_sessions(user_id, limit=limit)
        except Exception:
            return []
