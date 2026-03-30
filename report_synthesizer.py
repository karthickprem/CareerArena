"""
Report Synthesizer — generates the final structured report from arena debate.

Takes the orchestrator output (synthesis from leads, contrarian challenges,
arena transcript) and produces a user-facing report.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from llm_client import LLMClient
from query_router import QueryType


REPORT_PROMPT = """You are the CareerArena Report Synthesizer.

Generate a comprehensive, actionable career intelligence report based on
the multi-agent debate results below.

## User Query
{query}

## Query Type
{query_type}

## Target Companies
{companies}

## Agent Synthesis (from lead agents)
{synthesis}

## Contrarian Challenges
{contrarian}

## Arena Debate Transcript
{transcript}

Generate a structured JSON report:
```json
{{
  "title": "Report title (e.g., 'Offer Comparison: Razorpay vs Flipkart SDE-2')",
  "executive_summary": "2-3 sentence summary of the key finding/recommendation",
  "sections": [
    {{
      "heading": "Section title",
      "content": "Detailed content with specific numbers, data, and recommendations",
      "confidence": 0.0-1.0,
      "source_agents": ["agent names that contributed"]
    }}
  ],
  "key_recommendations": [
    "Specific, actionable recommendation 1",
    "Specific, actionable recommendation 2"
  ],
  "risk_factors": [
    "Risk or caveat to be aware of"
  ],
  "data_quality_note": "Note about data freshness and reliability",
  "next_steps": [
    "Suggested follow-up action"
  ]
}}
```

Rules:
- Be specific — include salary ranges, company names, skill names
- Every recommendation must be actionable
- Flag uncertainty clearly
- Include both positives and negatives
- The report should be useful enough to make real decisions"""


SECTION_TEMPLATES = {
    QueryType.PROFILE_REVIEW: [
        "Profile Strengths",
        "Critical Gaps",
        "Market Positioning",
        "Improvement Roadmap",
    ],
    QueryType.CAREER_STRATEGY: [
        "Current Position Assessment",
        "Market Opportunities",
        "Recommended Path",
        "Skills Investment",
        "Timeline & Milestones",
    ],
    QueryType.INTERVIEW_READINESS: [
        "Readiness Score",
        "Strength Areas",
        "Gap Analysis",
        "Preparation Plan",
        "Company-Specific Tips",
    ],
    QueryType.SALARY_INTEL: [
        "Compensation Breakdown",
        "Market Comparison",
        "Negotiation Leverage Points",
    ],
    QueryType.OFFER_COMPARISON: [
        "Compensation Comparison",
        "Growth & Learning",
        "Stability & Risk",
        "Culture & WLB",
        "Recommendation",
    ],
    QueryType.COMPANY_RESEARCH: [
        "Company Overview",
        "Engineering Culture",
        "Compensation & Benefits",
        "Growth Trajectory",
        "Red Flags & Green Flags",
    ],
    QueryType.SKILL_PLANNING: [
        "Current Skills Assessment",
        "Target Role Requirements",
        "Priority Skills to Learn",
        "Learning Roadmap",
        "Resources & Timeline",
    ],
    QueryType.INTERVIEW_PREP: [
        "Interview Process",
        "Key Topics to Prepare",
        "Practice Problems",
        "Behavioral Questions",
        "Company-Specific Tips",
    ],
    QueryType.NEGOTIATION: [
        "Current Offer Analysis",
        "Market Benchmark",
        "Negotiation Strategy",
        "Counter-Offer Script",
        "Walk-Away Points",
    ],
}


class ReportSynthesizer:
    def __init__(self, llm: Optional[LLMClient] = None):
        self.llm = llm

    def generate(self, orchestrator_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured report from orchestrator output."""
        if self.llm:
            return self._generate_with_llm(orchestrator_result)
        return self._generate_structured(orchestrator_result)

    def _generate_with_llm(self, result: Dict[str, Any]) -> Dict[str, Any]:
        synthesis_text = json.dumps(result.get("synthesis", {}), indent=2, default=str)
        contrarian_text = json.dumps(result.get("contrarian", {}), indent=2, default=str)
        transcript = result.get("transcript", "")

        prompt = REPORT_PROMPT.format(
            query=result.get("query", ""),
            query_type=result.get("query_type", ""),
            companies=", ".join(result.get("companies", [])),
            synthesis=synthesis_text[:4000],
            contrarian=contrarian_text[:2000],
            transcript=transcript[:4000],
        )

        try:
            report = self.llm.generate_json(
                prompt=prompt,
                system_prompt="You generate structured career intelligence reports.",
                temperature=0.3,
            )
            report["metadata"] = {
                "session_id": result.get("session_id"),
                "query_type": result.get("query_type"),
                "agents_used": result.get("agents_used"),
                "debate_rounds": result.get("debate_rounds"),
                "elapsed_seconds": result.get("elapsed_seconds"),
            }
            return report
        except Exception as e:
            return self._generate_structured(result, error=str(e))

    def _generate_structured(
        self, result: Dict[str, Any], error: str = ""
    ) -> Dict[str, Any]:
        """Fallback: build report directly from synthesis data without LLM."""
        query_type = result.get("query_type", "GENERAL")
        synthesis = result.get("synthesis", {})
        contrarian = result.get("contrarian", {})

        sections = []
        for domain, data in synthesis.items():
            if isinstance(data, dict):
                sections.append({
                    "heading": data.get("domain", domain).replace("_", " ").title(),
                    "content": data.get("summary", "No summary available."),
                    "confidence": data.get("confidence", 0.5),
                    "key_insights": data.get("key_insights", []),
                    "recommendations": data.get("recommendations", []),
                    "caveats": data.get("caveats", []),
                })

        all_recommendations = []
        for s in sections:
            all_recommendations.extend(s.get("recommendations", []))

        risk_factors = contrarian.get("blind_spots", [])
        for challenge in contrarian.get("challenges", []):
            if isinstance(challenge, dict):
                risk_factors.append(
                    f"{challenge.get('target_agent', '?')}: {challenge.get('challenge', '')}"
                )

        report = {
            "title": f"Career Intelligence: {result.get('query', '')[:60]}",
            "executive_summary": contrarian.get(
                "overall_assessment", "Multi-agent analysis complete."
            ),
            "sections": sections,
            "key_recommendations": all_recommendations[:5],
            "risk_factors": risk_factors[:5],
            "data_quality_note": (
                "Data sourced from web search and public sources. "
                "Salary figures are estimates — verify with actual offers."
            ),
            "next_steps": [
                "Verify salary data with current employees or Blind/Glassdoor",
                "Prepare targeted questions for the hiring manager",
            ],
            "metadata": {
                "session_id": result.get("session_id"),
                "query_type": query_type,
                "agents_used": result.get("agents_used"),
                "debate_rounds": result.get("debate_rounds"),
                "elapsed_seconds": result.get("elapsed_seconds"),
                "arena_stats": result.get("arena_stats"),
            },
        }

        if error:
            report["_llm_error"] = error

        return report

    def format_text(self, report: Dict[str, Any]) -> str:
        """Format report as readable text for CLI/terminal output."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"  {report.get('title', 'Career Intelligence Report')}")
        lines.append("=" * 70)
        lines.append("")

        if report.get("executive_summary"):
            lines.append("EXECUTIVE SUMMARY")
            lines.append("-" * 40)
            lines.append(report["executive_summary"])
            lines.append("")

        for section in report.get("sections", []):
            lines.append(f">> {section.get('heading', 'Section')}")
            conf = section.get("confidence")
            if conf is not None:
                lines.append(f"   Confidence: {conf:.0%}")
            lines.append(section.get("content", ""))
            for insight in section.get("key_insights", []):
                lines.append(f"   * {insight}")
            for rec in section.get("recommendations", []):
                lines.append(f"   -> {rec}")
            for cav in section.get("caveats", []):
                lines.append(f"   ! {cav}")
            lines.append("")

        if report.get("key_recommendations"):
            lines.append("KEY RECOMMENDATIONS")
            lines.append("-" * 40)
            for i, rec in enumerate(report["key_recommendations"], 1):
                lines.append(f"  {i}. {rec}")
            lines.append("")

        if report.get("risk_factors"):
            lines.append("RISK FACTORS")
            lines.append("-" * 40)
            for risk in report["risk_factors"]:
                lines.append(f"  ! {risk}")
            lines.append("")

        if report.get("next_steps"):
            lines.append("NEXT STEPS")
            lines.append("-" * 40)
            for step in report["next_steps"]:
                lines.append(f"  -> {step}")
            lines.append("")

        if report.get("data_quality_note"):
            lines.append(f"Note: {report['data_quality_note']}")

        meta = report.get("metadata", {})
        if meta:
            lines.append("")
            lines.append(f"Session: {meta.get('session_id', '?')} | "
                         f"Agents: {meta.get('agents_used', '?')} | "
                         f"Rounds: {meta.get('debate_rounds', '?')} | "
                         f"Time: {meta.get('elapsed_seconds', '?')}s")

        lines.append("=" * 70)
        return "\n".join(lines)
