"""
Agent Factory — 3-tier dynamic agent system built from knowledge graph.

Architecture (mirrors btc_swarm's 3-tier + Debug Arena's graph-to-agent):

  Tier 1 — SCREENERS (6 fixed agents, always on):
    Fast triage: resume quality, skills match, market pulse, salary scan,
    ATS optimization, culture fit.

  Tier 2 — SPECIALISTS (up to 40 dynamic agents, from graph):
    Deep analysis per entity: skill experts, company insiders, role advisors,
    domain specialists, project evaluators. Generated from knowledge graph.
    Activate when Tier 1 signals align.

  Tier 3 — HEAVYWEIGHTS (4 fixed agents, activate when Tier 2 aligns):
    Bull/Bear debate, Risk assessment, Final synthesis.

Pipeline:
  Resume → graph_builder.build_graph() → profile_generator.generate_profiles()
  → AgentFactory.build_roster_from_profiles() → SimulationAgents
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from query_router import RoutedQuery, QueryType

COGNITIVE_STYLES = [
    "analytical", "intuitive", "pragmatic", "skeptical",
    "data-driven", "pattern-matching", "first-principles", "holistic",
]

TIER2_ACTIVATION_PCT = 0.60
TIER2_MIN_AGREE = 4
TIER3_ACTIVATION_PCT = 0.65
TIER3_MIN_AGREE = 5


@dataclass
class CareerAgent:
    agent_id: str
    name: str
    agent_type: str          # "screener" | "specialist" | "heavyweight" (legacy: "lead" | "sub")
    tier: int = 2            # 1, 2, or 3
    lead_type: str = ""
    company: Optional[str] = None
    entity_name: str = ""
    entity_type: str = ""
    entity_category: str = ""
    persona: str = ""
    system_prompt: str = ""
    cognitive_style: str = "analytical"
    is_adversarial: bool = False
    stance: str = "investigating"
    tools: List[str] = field(default_factory=list)
    messages: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.5
    interested_topics: List[str] = field(default_factory=list)
    evaluation_focus: str = ""
    heavyweight_role: str = ""  # "debate_bull", "debate_bear", "risk", "synthesizer"


class AgentFactory:
    """Creates 3-tier agent rosters from knowledge graph profiles."""

    def __init__(self, db=None):
        self._db = db

    def build_roster_from_profiles(
        self,
        profiles: Dict[str, List[Dict]],
        context_text: str = "",
    ) -> List[CareerAgent]:
        """Build full agent roster from profile_generator output.

        Args:
            profiles: dict with 'tier1', 'tier2', 'tier3' lists from generate_profiles()
            context_text: session context for system prompts
        """
        agents = []
        counter = 0

        for p in profiles.get("tier1", []):
            agent_id = f"t1_{p.get('screener_id', p['username'])}_{counter}"
            counter += 1
            agent = CareerAgent(
                agent_id=agent_id,
                name=p["name"],
                agent_type="screener",
                tier=1,
                lead_type="screener",
                entity_name=p.get("entity_name", p["name"]),
                entity_type="Screener",
                entity_category="screener",
                persona=p["persona"],
                system_prompt=self._build_system_prompt(p, context_text, tier=1),
                cognitive_style=random.choice(COGNITIVE_STYLES),
                tools=p.get("tools", ["web_search"]),
                interested_topics=p.get("interested_topics", []),
                evaluation_focus=p.get("evaluation_focus", ""),
                stance="investigating",
            )
            agents.append(agent)

        for p in profiles.get("tier2", []):
            agent_id = f"t2_{p['username']}_{counter}"
            counter += 1
            agent = CareerAgent(
                agent_id=agent_id,
                name=f"{p['name']} Specialist",
                agent_type="specialist",
                tier=2,
                lead_type=p.get("entity_category", "specialist"),
                entity_name=p.get("entity_name", p["name"]),
                entity_type=p.get("entity_type", "Skill"),
                entity_category=p.get("entity_category", "generic"),
                persona=p["persona"],
                system_prompt=self._build_system_prompt(p, context_text, tier=2),
                cognitive_style=random.choice(COGNITIVE_STYLES),
                tools=p.get("tools", ["web_search"]),
                interested_topics=p.get("interested_topics", []),
                evaluation_focus=p.get("evaluation_focus", ""),
                stance=p.get("stance", "investigating"),
            )

            if p.get("entity_category") == "company":
                agent.company = p["entity_name"]

            agents.append(agent)

        for p in profiles.get("tier3", []):
            agent_id = f"t3_{p.get('heavyweight_id', p['username'])}_{counter}"
            counter += 1
            hw_role = p.get("heavyweight_role", p.get("heavyweight_id", ""))
            is_adv = hw_role in ("debate_bear", "risk")

            agent = CareerAgent(
                agent_id=agent_id,
                name=p["name"],
                agent_type="heavyweight",
                tier=3,
                lead_type="heavyweight",
                entity_name=p.get("entity_name", p["name"]),
                entity_type="Heavyweight",
                entity_category=p.get("entity_category", "debate"),
                persona=p["persona"],
                system_prompt=self._build_system_prompt(p, context_text, tier=3),
                cognitive_style="first-principles" if is_adv else "holistic",
                is_adversarial=is_adv,
                tools=p.get("tools", ["web_search"]),
                interested_topics=p.get("interested_topics", []),
                evaluation_focus=p.get("evaluation_focus", ""),
                stance=p.get("stance", "investigating"),
                heavyweight_role=hw_role,
            )
            agents.append(agent)

        if self._db:
            self._persist_agents(agents)

        return agents

    def create_agent_roster(
        self,
        query: RoutedQuery,
        context_text: str = "",
    ) -> List[CareerAgent]:
        """Legacy compatibility: create agents from RoutedQuery (no graph).

        Falls back to Tier 1 screeners + basic agents from query.
        """
        from profile_generator import TIER1_SCREENERS, TIER3_HEAVYWEIGHTS
        profiles = {"tier1": [], "tier2": [], "tier3": []}

        for i, s in enumerate(TIER1_SCREENERS):
            profiles["tier1"].append({
                "user_id": i,
                "username": s["id"],
                "name": s["name"],
                "entity_name": s["name"],
                "entity_type": "Screener",
                "entity_category": "screener",
                "tier": 1,
                "bio": s["persona"][:200],
                "persona": s["persona"],
                "evaluation_focus": s["focus"],
                "interested_topics": [s["focus"].lower()],
                "tools": s["tools"],
                "stance": "investigating",
                "screener_id": s["id"],
            })

        idx = len(TIER1_SCREENERS)
        for company in query.companies:
            profiles["tier2"].append({
                "user_id": idx,
                "username": f"company_{company.lower().replace(' ', '_')}",
                "name": company,
                "entity_name": company,
                "entity_type": "TargetCompany",
                "entity_category": "company",
                "tier": 2,
                "persona": f"Deep insider knowledge of {company}: engineering culture, "
                           f"interview process, compensation, and growth opportunities.",
                "evaluation_focus": f"Candidate fit for {company}",
                "interested_topics": [company.lower()],
                "tools": ["company_research", "news_search", "web_search", "salary_lookup"],
                "stance": "investigating",
            })
            idx += 1

        base_id = idx
        for i, hw in enumerate(TIER3_HEAVYWEIGHTS):
            profiles["tier3"].append({
                "user_id": base_id + i,
                "username": hw["id"],
                "name": hw["name"],
                "entity_name": hw["name"],
                "entity_type": "Heavyweight",
                "entity_category": hw.get("role", "debate"),
                "tier": 3,
                "persona": hw["persona"],
                "evaluation_focus": hw["focus"],
                "interested_topics": [hw["focus"].lower()],
                "tools": hw["tools"],
                "stance": "advocate" if hw["id"] == "debate_bull" else (
                    "skeptic" if hw["id"] == "debate_bear" else "synthesizer"
                ),
                "heavyweight_id": hw["id"],
                "heavyweight_role": hw.get("role", ""),
            })

        return self.build_roster_from_profiles(profiles, context_text)

    def _build_system_prompt(self, profile: Dict, context_text: str, tier: int) -> str:
        tier_label = {1: "SCREENER (Tier 1 — Fast Triage)",
                      2: "SPECIALIST (Tier 2 — Deep Analysis)",
                      3: "HEAVYWEIGHT (Tier 3 — Debate & Synthesis)"}
        parts = [
            f"# {profile['name']}",
            f"## Role: {tier_label.get(tier, 'Analyst')}",
            "",
            profile.get("persona", "Career intelligence analyst."),
            "",
            f"## Evaluation Focus",
            profile.get("evaluation_focus", "General career analysis"),
            "",
            f"## Your Tools",
            f"You have access to: {', '.join(profile.get('tools', ['web_search']))}",
            "",
            "## Response Rules",
            "1. Be specific and evidence-based. Cite data sources.",
            "2. Never fabricate numbers (salaries, headcounts, funding).",
            "3. If uncertain, say so clearly.",
            "4. Structure your response with clear sections.",
            "5. Focus on actionable insights over generic advice.",
        ]

        if tier == 1:
            parts.extend([
                "",
                "## Tier 1 Protocol",
                "You are a FAST screener. Provide quick, directional assessments.",
                "Signal clearly: STRONG / MODERATE / WEAK / RED_FLAG",
                "Other tiers depend on your assessment to activate deeper analysis.",
            ])
        elif tier == 2:
            parts.extend([
                "",
                "## Tier 2 Protocol",
                "You are a DEEP specialist activated by Tier 1 screener consensus.",
                "Provide thorough, nuanced analysis within your domain expertise.",
                "Cite specific evidence and challenge other specialists' claims.",
            ])
        elif tier == 3:
            parts.extend([
                "",
                "## Tier 3 Protocol",
                "You are a HEAVYWEIGHT activated for final debate and synthesis.",
                "Build on ALL Tier 1 and Tier 2 findings.",
                "Challenge weak arguments. Demand evidence. Produce actionable recommendations.",
            ])

        if context_text:
            parts.extend(["", "## Session Context", context_text])

        return "\n".join(parts)

    def _persist_agents(self, agents: List[CareerAgent]) -> None:
        for agent in agents:
            try:
                self._db.save_agent_profile(
                    agent_id=agent.agent_id,
                    session_id="",
                    agent_name=agent.name,
                    agent_type=agent.agent_type,
                    persona=agent.persona,
                    company=agent.company or "",
                    cognitive_style=agent.cognitive_style,
                    is_adversarial=agent.is_adversarial,
                )
            except Exception:
                pass

    def get_tier(self, agents: List[CareerAgent], tier: int) -> List[CareerAgent]:
        return [a for a in agents if a.tier == tier]

    def get_screeners(self, agents: List[CareerAgent]) -> List[CareerAgent]:
        return self.get_tier(agents, 1)

    def get_specialists(self, agents: List[CareerAgent]) -> List[CareerAgent]:
        return self.get_tier(agents, 2)

    def get_heavyweights(self, agents: List[CareerAgent]) -> List[CareerAgent]:
        return self.get_tier(agents, 3)

    def get_debate_agents(self, agents: List[CareerAgent]) -> List[CareerAgent]:
        return [a for a in agents if a.heavyweight_role in ("debate_bull", "debate_bear")]

    def get_leads(self, agents: List[CareerAgent]) -> List[CareerAgent]:
        """Legacy compat."""
        return [a for a in agents if a.tier in (1, 3)]

    def get_subs_for_lead(self, agents: List[CareerAgent], lead_type: str) -> List[CareerAgent]:
        """Legacy compat."""
        return [a for a in agents if a.lead_type == lead_type and a.tier == 2]

    def get_contrarian(self, agents: List[CareerAgent]) -> Optional[CareerAgent]:
        for a in agents:
            if a.is_adversarial:
                return a
        return None

    def get_company_agents(self, agents: List[CareerAgent], company: str) -> List[CareerAgent]:
        return [a for a in agents if a.company and a.company.lower() == company.lower()]

    def describe_roster(self, agents: List[CareerAgent]) -> str:
        t1 = self.get_screeners(agents)
        t2 = self.get_specialists(agents)
        t3 = self.get_heavyweights(agents)

        lines = [
            f"Agent Roster: {len(agents)} total",
            f"  Tier 1 Screeners: {len(t1)}  |  Tier 2 Specialists: {len(t2)}  |  Tier 3 Heavyweights: {len(t3)}",
            "",
            "── Tier 1: Screeners (always on) ──",
        ]
        for a in t1:
            lines.append(f"  {a.name} [{a.cognitive_style}] → {a.evaluation_focus}")

        categories = {}
        for a in t2:
            categories.setdefault(a.entity_category, []).append(a)

        lines.append("")
        lines.append(f"── Tier 2: Specialists ({len(t2)} agents from knowledge graph) ──")
        for cat, cat_agents in sorted(categories.items()):
            lines.append(f"  [{cat.upper()}] ({len(cat_agents)} agents)")
            for a in cat_agents[:5]:
                lines.append(f"    {a.name} [{a.cognitive_style}]")
            if len(cat_agents) > 5:
                lines.append(f"    ... and {len(cat_agents) - 5} more")

        lines.append("")
        lines.append("── Tier 3: Heavyweights (debate + synthesis) ──")
        for a in t3:
            badge = " [ADVERSARIAL]" if a.is_adversarial else ""
            lines.append(f"  {a.name} [{a.stance}]{badge} → {a.evaluation_focus}")

        return "\n".join(lines)
