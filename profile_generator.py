"""
Profile Generator — turns knowledge graph entities into agent profiles.

Mirrors Debug Arena's profile_generator.py for career intelligence.

Pipeline:
  Graph nodes → LLM persona generation → Agent profiles with:
    - Rich persona (2000+ chars)
    - Category-specific prompts (skill, company, role, domain, etc.)
    - Tier assignment (1: screener, 2: specialist, 3: heavyweight)
    - Interested topics and tools
"""

from __future__ import annotations

import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Optional

from llm_client import LLMClient
from graph_builder import get_entity_context, classify_entity_priority

SYSTEM_PROMPT = (
    "You are a career intelligence agent profile designer. Generate detailed, "
    "unique agent personas for a multi-agent career analysis simulation. "
    "Each agent must have deep domain expertise and a distinct analytical perspective. "
    "Output valid JSON only."
)

SKILL_PROMPT = """Generate an agent profile for a career analyst who is a deep expert on: {entity_name}

Context:
{context}

This agent will analyze resumes and career paths through the lens of {entity_name} expertise.

Return JSON:
```json
{{
  "bio": "2-3 sentence bio establishing expertise (max 200 chars)",
  "persona": "Detailed persona (1500-2000 chars). Include: 1) What makes this skill valuable/overrated in current market, 2) How to evaluate proficiency vs buzzword-dropping, 3) Career paths this skill unlocks, 4) Red flags when assessing candidates, 5) How this skill interacts with other technologies. Write as a first-person character voice.",
  "expertise_level": "world_class|expert|specialist",
  "interested_topics": ["topic1", "topic2", "topic3"],
  "evaluation_focus": "What this agent specifically looks for when reviewing a candidate"
}}
```"""

COMPANY_PROMPT = """Generate an agent profile for a career analyst who is a deep insider on: {entity_name}

Context:
{context}

This agent will analyze whether candidates are a good fit for {entity_name} and what to expect.

Return JSON:
```json
{{
  "bio": "2-3 sentence bio establishing insider knowledge (max 200 chars)",
  "persona": "Detailed persona (1500-2000 chars). Include: 1) Company's engineering culture and values, 2) Interview process and what they really look for, 3) Compensation philosophy and ranges, 4) Growth opportunities and career trajectory, 5) Red flags and downsides that candidates should know. Write as a first-person character voice.",
  "expertise_level": "insider|observer|analyst",
  "interested_topics": ["topic1", "topic2", "topic3"],
  "evaluation_focus": "What this agent specifically assesses about a candidate's fit"
}}
```"""

ROLE_PROMPT = """Generate an agent profile for a career analyst who is an expert on: {entity_name}

Context:
{context}

This agent understands what it takes to succeed in {entity_name} roles across companies.

Return JSON:
```json
{{
  "bio": "2-3 sentence bio establishing role expertise (max 200 chars)",
  "persona": "Detailed persona (1500-2000 chars). Include: 1) What separates top performers from average in this role, 2) Common career progression paths, 3) Skills that actually matter vs job posting requirements, 4) How to demonstrate readiness for this role level, 5) Compensation expectations and negotiation leverage. Write as a first-person character voice.",
  "expertise_level": "veteran|specialist|analyst",
  "interested_topics": ["topic1", "topic2", "topic3"],
  "evaluation_focus": "Specific criteria this agent uses to evaluate candidate readiness"
}}
```"""

DOMAIN_PROMPT = """Generate an agent profile for a career analyst specializing in: {entity_name}

Context:
{context}

This agent analyzes careers through the lens of the {entity_name} domain.

Return JSON:
```json
{{
  "bio": "2-3 sentence bio establishing domain expertise (max 200 chars)",
  "persona": "Detailed persona (1500-2000 chars). Include: 1) Current state of this domain and market demand, 2) Key skills and experience needed to enter/advance, 3) Major players and opportunities, 4) Emerging trends and future outlook, 5) Common mistakes candidates make. Write as a first-person character voice.",
  "expertise_level": "authority|expert|specialist",
  "interested_topics": ["topic1", "topic2", "topic3"],
  "evaluation_focus": "Domain-specific criteria for evaluating candidates"
}}
```"""

PROJECT_PROMPT = """Generate an agent profile for a career analyst who evaluates: {entity_name}

Context:
{context}

This agent assesses project experience and its career impact.

Return JSON:
```json
{{
  "bio": "2-3 sentence bio establishing project evaluation expertise (max 200 chars)",
  "persona": "Detailed persona (1500-2000 chars). Include: 1) What makes this project impressive or unremarkable, 2) Technical depth signals to look for, 3) How to present this in interviews, 4) Transferable skills demonstrated, 5) How hiring managers evaluate this type of work. Write as a first-person character voice.",
  "expertise_level": "evaluator|specialist|analyst",
  "interested_topics": ["topic1", "topic2", "topic3"],
  "evaluation_focus": "How this agent evaluates project impact and candidate contribution"
}}
```"""

GENERIC_PROMPT = """Generate an agent profile for a career analyst with expertise in: {entity_name}

Context:
{context}

Return JSON:
```json
{{
  "bio": "2-3 sentence bio (max 200 chars)",
  "persona": "Detailed persona (1500-2000 chars). Establish deep expertise, analytical perspective, and what this agent specifically contributes to career analysis. Write as a first-person character voice.",
  "expertise_level": "expert|specialist|analyst",
  "interested_topics": ["topic1", "topic2", "topic3"],
  "evaluation_focus": "What this agent specifically evaluates"
}}
```"""

PROMPT_MAP = {
    "skill": SKILL_PROMPT,
    "company": COMPANY_PROMPT,
    "role": ROLE_PROMPT,
    "domain": DOMAIN_PROMPT,
    "project": PROJECT_PROMPT,
    "generic": GENERIC_PROMPT,
}

TIER1_SCREENERS = [
    {
        "id": "screen_resume",
        "name": "ResumeScreener",
        "persona": (
            "I'm a veteran technical recruiter who has screened 50,000+ resumes for top tech companies. "
            "I see through inflated titles and buzzword-stuffed skills sections instantly. I assess: "
            "career trajectory coherence, skill depth vs breadth signals, gap explanations, and "
            "role progression logic. I flag red flags like job-hopping without growth, skill claims "
            "without project evidence, and education-experience mismatches. My screening is fast, "
            "brutal, and accurate."
        ),
        "tools": ["resume_parser", "web_search"],
        "focus": "Resume quality, career coherence, red flags",
    },
    {
        "id": "screen_skills",
        "name": "SkillsScanner",
        "persona": (
            "I'm a technical assessment specialist who evaluates whether candidates actually know "
            "what they claim. I cross-reference stated skills with project descriptions, years of "
            "experience, and industry standards. I know the difference between 'used Python once' and "
            "'architected distributed systems in Python'. I identify skill gaps that will surface in "
            "interviews and rate true proficiency levels."
        ),
        "tools": ["resume_parser", "web_search"],
        "focus": "Skill verification, proficiency depth, gaps",
    },
    {
        "id": "screen_market",
        "name": "MarketPulse",
        "persona": (
            "I track the tech job market across India in real-time. I know which companies are "
            "hiring aggressively, which are on quiet freezes, which teams are being restructured. "
            "I monitor funding rounds, layoff signals, and headcount changes. I provide the market "
            "reality check that prevents candidates from wasting time on dead opportunities."
        ),
        "tools": ["web_search", "news_search", "company_research"],
        "focus": "Market conditions, hiring signals, company health",
    },
    {
        "id": "screen_salary",
        "name": "CompScanner",
        "persona": (
            "I specialize in Indian tech compensation data. I know real salary bands, not posted "
            "ranges. I track base, bonus, ESOP/RSU structures, joining bonuses, and retention "
            "packages across companies and levels. I provide quick market-rate assessments and "
            "identify negotiation opportunities."
        ),
        "tools": ["salary_lookup", "web_search", "company_research"],
        "focus": "Compensation reality check, market rates",
    },
    {
        "id": "screen_ats",
        "name": "ATSOptimizer",
        "persona": (
            "I'm an ATS (Applicant Tracking System) and hiring pipeline expert. I know exactly "
            "how resumes get filtered before humans see them. I evaluate keyword optimization, "
            "format compatibility, and whether the resume will survive automated screening. "
            "I also assess LinkedIn profile strength and online presence."
        ),
        "tools": ["resume_parser", "web_search"],
        "focus": "ATS compatibility, keyword optimization, online presence",
    },
    {
        "id": "screen_culture",
        "name": "CultureFit",
        "persona": (
            "I assess candidate-company cultural alignment. I know the difference between Razorpay's "
            "hustle culture, Google's structured environment, and startup chaos. I evaluate whether "
            "a candidate's work style, communication patterns, and career motivations align with "
            "target companies. I prevent costly cultural misfits."
        ),
        "tools": ["web_search", "company_research"],
        "focus": "Cultural alignment, work style compatibility",
    },
]

TIER3_HEAVYWEIGHTS = [
    {
        "id": "debate_bull",
        "name": "CareerAdvocate",
        "role": "debate_bull",
        "persona": (
            "I build the STRONGEST possible case FOR the recommended career moves. I find every "
            "piece of evidence supporting the path. I model best-case scenarios with realistic "
            "probabilities. But I'm not a cheerleader — my advocacy is evidence-based and I "
            "acknowledge real risks while arguing they're manageable. I've seen too many candidates "
            "miss opportunities due to analysis paralysis."
        ),
        "tools": ["web_search", "company_research", "salary_lookup"],
        "focus": "Build strongest evidence-based case FOR recommendations",
    },
    {
        "id": "debate_bear",
        "name": "CareerChallenger",
        "role": "debate_bear",
        "persona": (
            "I challenge EVERY recommendation with rigorous counter-arguments. If the consensus says "
            "'join company X', I present every reason NOT to. I model worst-case scenarios, surface "
            "hidden risks, and demand stronger evidence. I'm the reason candidates don't make "
            "catastrophic career moves. My challenges are specific, data-backed, not generically "
            "pessimistic."
        ),
        "tools": ["web_search", "news_search", "company_research"],
        "focus": "Challenge recommendations, surface risks, demand evidence",
    },
    {
        "id": "risk_officer",
        "name": "RiskAssessor",
        "persona": (
            "I'm the final risk checkpoint. I assess: financial risk (salary stability, runway), "
            "career risk (pigeonholing, dead-end roles), market risk (industry decline, automation), "
            "and execution risk (skill gaps, interview readiness). I assign risk ratings and recommend "
            "mitigation strategies. No recommendation leaves without my risk assessment."
        ),
        "tools": ["web_search", "company_research", "salary_lookup"],
        "focus": "Comprehensive risk assessment, mitigation strategies",
    },
    {
        "id": "career_strategist",
        "name": "CareerStrategist",
        "role": "synthesizer",
        "persona": (
            "I synthesize ALL agent findings into a coherent career strategy. I weigh competing "
            "arguments from the bull and bear, factor in risk assessments, and produce the final "
            "ranked recommendations. I think in 5-year arcs, not just immediate moves. I identify "
            "the sequence of moves that maximizes long-term career value."
        ),
        "tools": ["web_search", "company_research"],
        "focus": "Final synthesis, ranked recommendations, long-term strategy",
    },
]


def _classify_entity(entity_type: str) -> str:
    skill_types = {"Skill", "Technology", "Tool", "Framework", "ProgrammingLanguage",
                   "Database", "CloudService", "Platform"}
    company_types = {"Company", "TargetCompany"}
    role_types = {"Role", "Experience"}
    domain_types = {"Domain", "Industry", "MarketSegment"}
    project_types = {"Project", "Achievement"}

    if entity_type in skill_types:
        return "skill"
    elif entity_type in company_types:
        return "company"
    elif entity_type in role_types:
        return "role"
    elif entity_type in domain_types:
        return "domain"
    elif entity_type in project_types:
        return "project"
    return "generic"


def _generate_username(name: str) -> str:
    import re
    clean = re.sub(r"[^a-zA-Z0-9_]", "_", name.lower())
    clean = re.sub(r"_+", "_", clean).strip("_")
    return f"{clean}_{random.randint(100, 999)}"


def _generate_single_profile(
    llm: LLMClient,
    node: Dict,
    idx: int,
    graph: Dict,
    tier: int,
) -> Dict[str, Any]:
    entity_name = node["name"]
    entity_type = node["labels"][-1] if len(node.get("labels", [])) > 1 else "Skill"
    category = _classify_entity(entity_type)
    context = get_entity_context(graph, entity_name)

    prompt_template = PROMPT_MAP.get(category, GENERIC_PROMPT)
    prompt = prompt_template.format(
        entity_name=entity_name,
        context=context[:5000],
    )

    try:
        result = llm.generate_json(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
            temperature=0.7,
        )
    except Exception:
        result = _fallback_profile(node, entity_type, category)

    tools = _tools_for_category(category)
    interested = result.get("interested_topics", [entity_name.lower()])
    if not isinstance(interested, list):
        interested = [entity_name.lower()]

    return {
        "user_id": idx,
        "username": _generate_username(entity_name),
        "name": entity_name,
        "entity_name": entity_name,
        "entity_type": entity_type,
        "entity_category": category,
        "tier": tier,
        "bio": result.get("bio", f"Expert on {entity_name}"),
        "persona": result.get("persona", f"Deep expertise in {entity_name} with focus on career impact."),
        "expertise_level": result.get("expertise_level", "specialist"),
        "evaluation_focus": result.get("evaluation_focus", f"Evaluates candidates through {entity_name} lens"),
        "interested_topics": interested,
        "tools": tools,
        "stance": _stance_for_category(category),
    }


def _fallback_profile(node: Dict, entity_type: str, category: str) -> Dict:
    return {
        "bio": f"Expert analyst specializing in {node['name']}",
        "persona": (
            f"I am a career intelligence analyst with deep expertise in {node['name']}. "
            f"My focus area is {entity_type}. I analyze candidates and career paths through "
            f"the lens of {node['name']}, evaluating skills, market demand, and growth potential. "
            f"Summary: {node.get('summary', 'N/A')}"
        ),
        "expertise_level": "specialist",
        "interested_topics": [node["name"].lower()],
        "evaluation_focus": f"Evaluates {category} aspects of career decisions",
    }


def _tools_for_category(category: str) -> List[str]:
    return {
        "skill": ["resume_parser", "web_search"],
        "company": ["company_research", "news_search", "web_search", "salary_lookup"],
        "role": ["web_search", "salary_lookup", "company_research"],
        "domain": ["web_search", "news_search", "company_research"],
        "project": ["resume_parser", "web_search"],
        "generic": ["web_search"],
    }.get(category, ["web_search"])


def _stance_for_category(category: str) -> str:
    return {
        "skill": "specialist",
        "company": "investigating",
        "role": "investigating",
        "domain": "specialist",
        "project": "investigating",
        "generic": "investigating",
    }.get(category, "investigating")


def generate_profiles(
    llm: LLMClient,
    graph: Dict,
    on_progress: Optional[Callable] = None,
    max_tier2: int = 40,
) -> Dict[str, List[Dict]]:
    """Generate all agent profiles from the knowledge graph.

    Returns dict with keys: 'tier1', 'tier2', 'tier3', 'all'
    """
    if on_progress:
        on_progress(f"Generating profiles from {len(graph['nodes'])} graph entities...")

    tier1_profiles = []
    for i, screener in enumerate(TIER1_SCREENERS):
        tier1_profiles.append({
            "user_id": i,
            "username": screener["id"],
            "name": screener["name"],
            "entity_name": screener["name"],
            "entity_type": "Screener",
            "entity_category": "screener",
            "tier": 1,
            "bio": screener["persona"][:200],
            "persona": screener["persona"],
            "expertise_level": "expert",
            "evaluation_focus": screener["focus"],
            "interested_topics": [screener["focus"].lower()],
            "tools": screener["tools"],
            "stance": "investigating",
            "screener_id": screener["id"],
        })

    if on_progress:
        on_progress(f"Tier 1: {len(tier1_profiles)} screeners ready")

    tier2_candidates = []
    for node in graph["nodes"]:
        priority = classify_entity_priority(node)
        tier2_candidates.append((node, priority))

    tier2_candidates.sort(key=lambda x: (x[1], -len(x[0].get("summary", ""))))
    selected = tier2_candidates[:max_tier2]

    if on_progress:
        on_progress(f"Generating Tier 2 profiles: {len(selected)} specialists...")

    tier2_profiles = [None] * len(selected)
    total = len(selected)

    with ThreadPoolExecutor(max_workers=min(15, total)) as pool:
        futures = {}
        for idx, (node, tier) in enumerate(selected):
            uid = len(tier1_profiles) + idx
            f = pool.submit(_generate_single_profile, llm, node, uid, graph, 2)
            futures[f] = idx

        for future in as_completed(futures):
            idx = futures[future]
            try:
                tier2_profiles[idx] = future.result()
            except Exception as e:
                node, _ = selected[idx]
                tier2_profiles[idx] = _fallback_profile(node, "Skill", "generic")
                tier2_profiles[idx].update({
                    "user_id": len(tier1_profiles) + idx,
                    "username": _generate_username(node["name"]),
                    "name": node["name"],
                    "entity_name": node["name"],
                    "entity_type": "Skill",
                    "entity_category": "generic",
                    "tier": 2,
                    "tools": ["web_search"],
                    "stance": "investigating",
                })

            if on_progress and (idx + 1) % 5 == 0:
                on_progress(f"  Generated {idx + 1}/{total} Tier 2 profiles")

    tier2_profiles = [p for p in tier2_profiles if p is not None]

    if on_progress:
        on_progress(f"Tier 2: {len(tier2_profiles)} specialists ready")

    tier3_profiles = []
    base_id = len(tier1_profiles) + len(tier2_profiles)
    for i, hw in enumerate(TIER3_HEAVYWEIGHTS):
        tier3_profiles.append({
            "user_id": base_id + i,
            "username": hw["id"],
            "name": hw["name"],
            "entity_name": hw["name"],
            "entity_type": "Heavyweight",
            "entity_category": hw.get("role", "debate"),
            "tier": 3,
            "bio": hw["persona"][:200],
            "persona": hw["persona"],
            "expertise_level": "world_class",
            "evaluation_focus": hw["focus"],
            "interested_topics": [hw["focus"].lower()],
            "tools": hw["tools"],
            "stance": "advocate" if hw["id"] == "debate_bull" else ("skeptic" if hw["id"] == "debate_bear" else "synthesizer"),
            "heavyweight_id": hw["id"],
            "heavyweight_role": hw.get("role", ""),
        })

    if on_progress:
        on_progress(f"Tier 3: {len(tier3_profiles)} heavyweights ready")

    all_profiles = tier1_profiles + tier2_profiles + tier3_profiles

    if on_progress:
        on_progress(
            f"Total roster: {len(all_profiles)} agents "
            f"(T1:{len(tier1_profiles)} T2:{len(tier2_profiles)} T3:{len(tier3_profiles)})"
        )

    return {
        "tier1": tier1_profiles,
        "tier2": tier2_profiles,
        "tier3": tier3_profiles,
        "all": all_profiles,
    }
