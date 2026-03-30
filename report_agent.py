"""
ReportAgent — The Octopus Brain.

Central orchestrator that reads the arena, issues directives to tentacles (agents),
decides when the investigation is complete, and synthesizes the final intelligence report.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from llm_client import LLMClient
from database import CareerDB

ORCHESTRATE_PROMPT = """You are the Octopus Brain — the central intelligence orchestrating a multi-agent career investigation.

Each agent is a tentacle: independently probing, investigating, debating. Your job is to direct them,
identify gaps, and decide when the investigation is complete.

## User's Career Question
{query}

## Current Arena Status
- Posts: {num_posts}
- Comments/Debates: {num_comments}
- Active Tentacles (Agents): {num_agents}
- Topics covered: {topics}
- Investigation cycle: {cycle_num}/{max_cycles}

## Arena Transcript
{transcript}

## Agent (Tentacle) Summaries
{agent_summaries}

Analyze the investigation and decide:
1. If key questions are THOROUGHLY answered and agents are CONVERGING → signal should_stop = true
2. If important angles are MISSING or claims are UNCHALLENGED → issue directives to specific agents
3. Be strategic: direct adversarial agents to challenge weak claims, direct specialists to dig deeper

Respond in JSON:
```json
{{
  "assessment": "Assessment of investigation quality, what's strong, what's weak",
  "convergence_score": 0.0-1.0,
  "missing_perspectives": ["specific gaps that still need investigation"],
  "should_stop": false,
  "directives": [
    {{
      "target_agent": "agent name",
      "task": "specific investigation task with clear deliverable",
      "priority": "high|medium|low"
    }}
  ],
  "stop_reason": "why stopping (if should_stop is true)"
}}
```"""

REPORT_PROMPT = """You are the Octopus Brain generating the final Career Intelligence Report.

You have directed dozens of specialist agents (tentacles) to investigate, debate, and challenge each other.
Now synthesize everything into a report that would IMPRESS a senior professional making career decisions.

## User's Question
{query}

## Query Type
{query_type}

## Companies Analyzed
{companies}

## Complete Arena Transcript (multi-agent debate)
{transcript}

## Agent Final Positions
{agent_summaries}

## Orchestrator Assessment
{assessment}

Generate a comprehensive, structured JSON report. The report should feel like it was written by a team
of elite career consultants who spent days researching. Be SPECIFIC — use numbers, company names,
salary ranges, timelines. Every section should provide UNIQUE VALUE.

```json
{{
  "title": "Compelling, specific report title (not generic)",
  "executive_summary": "3-4 sentence powerful summary. Lead with the most important finding. Include a specific number or recommendation. End with the key risk or caveat.",
  "sections": [
    {{
      "heading": "Clear, specific section title",
      "content": "Rich, detailed content (3-5 paragraphs). Include specific data points, comparisons, and analysis. Write as a career intelligence consultant would — authoritative but balanced. Use specifics: salary ranges (e.g., 35-45L base), company names, skill names, timelines (e.g., 6-9 months preparation).",
      "confidence": 0.0-1.0,
      "key_insights": [
        "A specific, non-obvious insight backed by the agent debate",
        "Another insight that the user likely didn't know"
      ],
      "recommendations": [
        "A specific, actionable recommendation with clear steps",
        "Another recommendation with a timeline"
      ],
      "caveats": [
        "An honest caveat or limitation about this section's analysis"
      ],
      "source_agents": ["agent names that contributed to this section"]
    }}
  ],
  "key_recommendations": [
    "Top 3-5 specific, actionable recommendations — each should be a complete sentence with a clear action, timeline, and expected outcome"
  ],
  "risk_factors": [
    "Specific risks the user should be aware of — not generic warnings but specific to their situation"
  ],
  "data_quality_note": "Honest note about data freshness and how to verify",
  "next_steps": [
    "Specific follow-up actions the user should take, in priority order"
  ]
}}
```

CRITICAL RULES:
- Minimum 5 sections, maximum 8 — each covering a distinct angle
- Every section MUST have at least 2 key_insights and 1 recommendation
- Be brutally specific: "Apply to Google L5 within 3 months" not "Consider applying to top companies"
- Include salary ranges with base + RSU + bonus breakdown when discussing compensation
- Flag genuine risks — don't sugarcoat. If the user isn't ready, say so clearly
- Each section confidence score should reflect actual debate quality on that topic
- The report should tell a STORY: situation → analysis → findings → recommendations → risks → next steps"""


class ReportAgent:
    """The Octopus Brain — orchestrates the investigation and synthesizes the report."""

    def __init__(self, llm: LLMClient, db: CareerDB):
        self.llm = llm
        self.db = db

    def orchestrate(
        self,
        session_id: str,
        query: str,
        cycle_num: int,
        max_cycles: int = 5,
    ) -> Dict[str, Any]:
        """Assess the arena and issue directives or signal stop."""
        stats = self.db.get_session_stats(session_id)
        transcript = self.db.build_transcript(session_id)
        agent_summaries = self._get_agent_summaries(session_id)

        prompt = ORCHESTRATE_PROMPT.format(
            query=query,
            num_posts=stats["total_posts"],
            num_comments=stats["total_comments"],
            num_agents=stats["active_agents"],
            topics=", ".join(stats.get("topics", [])),
            cycle_num=cycle_num,
            transcript=transcript[:6000],
            agent_summaries=agent_summaries[:2000],
            max_cycles=max_cycles,
        )

        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt="You are the Octopus Brain — the central intelligence of a multi-agent career investigation system. Direct the tentacles strategically.",
                temperature=0.3,
            )
        except Exception as e:
            return {
                "should_stop": cycle_num >= max_cycles,
                "directives": [],
                "assessment": f"Orchestration error: {e}",
                "convergence_score": 0.5,
            }

        directives = result.get("directives", [])
        for d in directives:
            agent_name = d.get("target_agent", "")
            task = d.get("task", "")
            priority = d.get("priority", "high")
            if agent_name and task:
                self.db.save_directive(
                    session_id=session_id,
                    target_agent_id="",
                    target_agent_name=agent_name,
                    task=task,
                    priority=priority,
                    assigned_round=cycle_num,
                )

        return result

    def generate_report(
        self,
        session_id: str,
        query: str,
        query_type: str = "",
        companies: List[str] = None,
        assessment: str = "",
    ) -> Dict[str, Any]:
        """Generate the final structured report from arena discussion."""
        transcript = self.db.build_transcript(session_id)
        agent_summaries = self._get_agent_summaries(session_id)
        stats = self.db.get_session_stats(session_id)

        prompt = REPORT_PROMPT.format(
            query=query,
            query_type=query_type,
            companies=", ".join(companies or []),
            transcript=transcript[:6000],
            agent_summaries=agent_summaries[:2000],
            assessment=assessment[:1000],
        )

        try:
            report = self.llm.generate_json(
                prompt=prompt,
                system_prompt=(
                    "You are an elite career intelligence consultant synthesizing a multi-agent investigation. "
                    "Your reports are known for being brutally specific, data-rich, and genuinely useful. "
                    "Never be generic. Always include specific numbers, company names, timelines, and action items."
                ),
                temperature=0.4,
            )

            for section in report.get("sections", []):
                if "key_insights" not in section:
                    section["key_insights"] = []
                if "recommendations" not in section:
                    section["recommendations"] = []
                if "caveats" not in section:
                    section["caveats"] = []

            report["metadata"] = {
                "session_id": session_id,
                "query_type": query_type,
                "arena_stats": stats,
            }
            return report
        except Exception as e:
            return self._fallback_report(session_id, query, stats, str(e))

    def _get_agent_summaries(self, session_id: str) -> str:
        summaries = self.db.get_all_agent_summaries(session_id)
        if not summaries:
            return "No agent summaries available."
        lines = []
        for s in summaries:
            hyp = s.get("latest_hypothesis", "No hypothesis")
            conf = s.get("hypothesis_confidence", "?")
            lines.append(
                f"- {s['agent_name']}: {hyp} (confidence: {conf}, "
                f"{s['memory_count']} memories, last active round {s['last_active_round']})"
            )
        return "\n".join(lines)

    def _fallback_report(self, session_id: str, query: str, stats: dict, error: str) -> dict:
        posts = self.db.get_session_posts(session_id)
        sections = []
        for p in posts[:10]:
            sections.append({
                "heading": f"Analysis by {p['agent_name']}",
                "content": p["content"],
                "confidence": p.get("confidence", 0.5),
                "key_insights": [],
                "recommendations": [],
                "caveats": [],
                "source_agents": [p["agent_name"]],
            })
        return {
            "title": f"Career Intelligence: {query[:60]}",
            "executive_summary": "Multi-agent investigation complete. Report synthesized from arena debate.",
            "sections": sections,
            "key_recommendations": [],
            "risk_factors": [f"Report generation encountered an issue: {error}"],
            "data_quality_note": "Data sourced from agent investigation. Verify with actual offers and current employees.",
            "next_steps": ["Verify findings with current employees", "Prepare targeted questions for interviews"],
            "metadata": {"session_id": session_id, "arena_stats": stats},
        }
