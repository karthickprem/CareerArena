"""
Query Router — classifies user queries and extracts structured intent.
Determines which agents to activate, which companies to research,
and how deep the debate should go.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class QueryType(Enum):
    PROFILE_REVIEW = "PROFILE_REVIEW"
    CAREER_STRATEGY = "CAREER_STRATEGY"
    INTERVIEW_READINESS = "INTERVIEW_READINESS"
    SALARY_INTEL = "SALARY_INTEL"
    OFFER_COMPARISON = "OFFER_COMPARISON"
    COMPANY_RESEARCH = "COMPANY_RESEARCH"
    SKILL_PLANNING = "SKILL_PLANNING"
    INTERVIEW_PREP = "INTERVIEW_PREP"
    NEGOTIATION = "NEGOTIATION"
    GENERAL = "GENERAL"


@dataclass
class RoutedQuery:
    query_type: QueryType
    original_query: str
    companies: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)
    skills_mentioned: List[str] = field(default_factory=list)
    fixed_agents: List[str] = field(default_factory=list)
    debate_rounds: int = 1
    spawn_sub_agents: bool = False
    confidence: float = 0.0


AGENT_ACTIVATION_MAP = {
    QueryType.PROFILE_REVIEW: {
        "agents": ["profile_analyst", "skills_gap_lead"],
        "sub_agents": False,
        "rounds": 1,
    },
    QueryType.CAREER_STRATEGY: {
        "agents": [
            "profile_analyst", "market_intel_lead", "interview_coach_lead",
            "skills_gap_lead", "compensation_lead", "contrarian",
        ],
        "sub_agents": True,
        "rounds": 2,
    },
    QueryType.INTERVIEW_READINESS: {
        "agents": [
            "profile_analyst", "skills_gap_lead", "interview_coach_lead",
            "market_intel_lead", "contrarian",
        ],
        "sub_agents": True,
        "rounds": 2,
    },
    QueryType.SALARY_INTEL: {
        "agents": ["market_intel_lead", "compensation_lead"],
        "sub_agents": True,
        "rounds": 1,
    },
    QueryType.OFFER_COMPARISON: {
        "agents": ["compensation_lead", "market_intel_lead", "contrarian"],
        "sub_agents": True,
        "rounds": 2,
    },
    QueryType.COMPANY_RESEARCH: {
        "agents": [
            "market_intel_lead", "interview_coach_lead",
            "compensation_lead", "contrarian",
        ],
        "sub_agents": True,
        "rounds": 2,
    },
    QueryType.SKILL_PLANNING: {
        "agents": ["skills_gap_lead", "market_intel_lead"],
        "sub_agents": True,
        "rounds": 1,
    },
    QueryType.INTERVIEW_PREP: {
        "agents": ["interview_coach_lead", "skills_gap_lead", "profile_analyst"],
        "sub_agents": True,
        "rounds": 2,
    },
    QueryType.NEGOTIATION: {
        "agents": ["compensation_lead", "market_intel_lead", "contrarian"],
        "sub_agents": True,
        "rounds": 2,
    },
    QueryType.GENERAL: {
        "agents": ["profile_analyst", "market_intel_lead"],
        "sub_agents": False,
        "rounds": 1,
    },
}


QUERY_PATTERNS = {
    QueryType.PROFILE_REVIEW: [
        r"review\s+(my\s+)?resume",
        r"check\s+(my\s+)?profile",
        r"feedback\s+on\s+(my\s+)?resume",
        r"how('s| is)\s+my\s+(resume|profile|cv)",
        r"rate\s+my\s+(resume|profile)",
        r"what('s| is)\s+wrong\s+with\s+my",
    ],
    QueryType.INTERVIEW_READINESS: [
        r"(am|are)\s+i\s+ready\s+(for|to)",
        r"can\s+i\s+(crack|clear|pass)",
        r"ready\s+for\s+interview",
        r"should\s+i\s+apply",
        r"my\s+chances\s+(at|for|of)",
    ],
    QueryType.SALARY_INTEL: [
        r"salary\s+(for|of|at)",
        r"(how\s+much|what)\s+(does|do|is).*pay",
        r"compensation\s+(for|at)",
        r"ctc\s+(for|at|of)",
        r"package\s+(for|at|of)",
        r"(how\s+much|what).*earn",
    ],
    QueryType.OFFER_COMPARISON: [
        r"compare\s+(these\s+)?(offer|package|comp)",
        r"compare\s+\w+\s+vs\s+\w+",
        r"compare\s+\w+\s+and\s+\w+\s+offer",
        r"which\s+(offer|company|job)\s+(should|is\s+better)",
        r"\bvs\b.*offer",
        r"better\s+offer",
        r"(choose|pick)\s+between",
    ],
    QueryType.INTERVIEW_PREP: [
        r"prepare\s+(me\s+)?(for|to)",
        r"(interview\s+)?(prep|preparation)\s+(for|at)",
        r"(what|how)\s+.*interview\s+.*like\s+at",
        r"interview\s+(questions|pattern|process|rounds)\s+(at|for)",
        r"(coding|system\s+design|behavioral)\s+interview",
    ],
    QueryType.COMPANY_RESEARCH: [
        r"(tell\s+me\s+about|what\s+about)\s+\w+",
        r"(how\s+is|what('s| is))\s+\w+\s+(like|as\s+a\s+company)",
        r"(is\s+)?\w+\s+(good|bad)\s+(company|to\s+work)",
        r"(culture|wlb|work\s+life)\s+at",
    ],
    QueryType.SKILL_PLANNING: [
        r"how\s+to\s+(become|learn|transition|switch)",
        r"(skills|roadmap|path)\s+(for|to\s+become)",
        r"(what|which)\s+skills\s+(do\s+i|should\s+i|to)",
        r"(career|learning)\s+(path|roadmap)",
        r"(is|are)\s+\w+\s+enough\s+(for|to)",
        r"(what|which)\s+\w+\s+(should|do)\s+i\s+learn",
    ],
    QueryType.NEGOTIATION: [
        r"(how\s+to\s+)?negotiat",
        r"(counter|reject)\s+offer",
        r"(raise|increase|bump)\s+(my\s+)?(salary|ctc|offer|package)",
        r"(ask\s+for\s+)more\s+(money|salary|comp)",
    ],
    QueryType.CAREER_STRATEGY: [
        r"(what\s+should\s+i\s+do|next\s+step|career\s+advice)",
        r"(where|what)\s+should\s+i\s+work",
        r"(should\s+i\s+)(stay|leave|quit|switch)",
        r"(career|job)\s+(change|switch|move)",
        r"(5|five)\s+year\s+(plan|goal)",
    ],
}


def route_query(query: str, resume_data: Optional[dict] = None) -> RoutedQuery:
    """Classify a user query and determine agent activation plan."""
    query_lower = query.lower().strip()

    classified_type = _classify_by_patterns(query_lower)
    confidence = 0.85 if classified_type != QueryType.GENERAL else 0.5

    companies = _extract_companies(query)
    roles = _extract_roles(query)
    skills = _extract_skills(query)

    activation = AGENT_ACTIVATION_MAP[classified_type]

    return RoutedQuery(
        query_type=classified_type,
        original_query=query,
        companies=companies,
        roles=roles,
        skills_mentioned=skills,
        fixed_agents=activation["agents"],
        debate_rounds=activation["rounds"],
        spawn_sub_agents=activation["sub_agents"] and len(companies) > 0,
        confidence=confidence,
    )


def route_query_with_llm(query: str, llm_client, resume_data: Optional[dict] = None) -> RoutedQuery:
    """Use LLM for higher-accuracy classification when available."""
    pattern_result = route_query(query, resume_data)

    if pattern_result.confidence >= 0.85 and pattern_result.companies:
        return pattern_result

    prompt = f"""Classify this career query into one type and extract entities.

Query: "{query}"

Types: PROFILE_REVIEW, CAREER_STRATEGY, INTERVIEW_READINESS, SALARY_INTEL,
OFFER_COMPARISON, COMPANY_RESEARCH, SKILL_PLANNING, INTERVIEW_PREP, NEGOTIATION, GENERAL

Respond in JSON:
{{
  "query_type": "TYPE_NAME",
  "companies": ["company1", "company2"],
  "roles": ["role1"],
  "skills": ["skill1", "skill2"]
}}"""

    try:
        response = llm_client.chat(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini",
            temperature=0.1,
        )
        parsed = json.loads(response)

        qtype = QueryType(parsed.get("query_type", "GENERAL"))
        companies = parsed.get("companies", []) or pattern_result.companies
        roles = parsed.get("roles", []) or pattern_result.roles
        skills = parsed.get("skills", []) or pattern_result.skills_mentioned

        activation = AGENT_ACTIVATION_MAP[qtype]

        return RoutedQuery(
            query_type=qtype,
            original_query=query,
            companies=companies,
            roles=roles,
            skills_mentioned=skills,
            fixed_agents=activation["agents"],
            debate_rounds=activation["rounds"],
            spawn_sub_agents=activation["sub_agents"] and len(companies) > 0,
            confidence=0.95,
        )
    except Exception:
        return pattern_result


def _classify_by_patterns(query_lower: str) -> QueryType:
    scores = {}
    for qtype, patterns in QUERY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, query_lower):
                scores[qtype] = scores.get(qtype, 0) + 1

    if scores:
        return max(scores, key=scores.get)
    return QueryType.GENERAL


_KNOWN_COMPANIES = [
    "google", "amazon", "microsoft", "apple", "meta", "facebook", "netflix",
    "flipkart", "razorpay", "phonepe", "cred", "swiggy", "zomato",
    "zerodha", "groww", "meesho", "ola", "uber", "paytm", "juspay",
    "atlassian", "salesforce", "oracle", "sap", "ibm", "intel", "amd",
    "qualcomm", "nvidia", "tcs", "infosys", "wipro", "hcl", "cognizant",
    "accenture", "deloitte", "walmart", "myntra", "nykaa", "dream11",
    "sharechat", "dunzo", "lenskart", "unacademy", "byju", "byjus",
    "freshworks", "zoho", "bharatpe", "slice", "jar", "jupiter",
    "thoughtspot", "postman", "browserstack", "hashedin", "tekion",
]


def _extract_companies(query: str) -> list:
    query_lower = query.lower()
    found = []
    for company in _KNOWN_COMPANIES:
        pattern = r'\b' + re.escape(company) + r'\b'
        if re.search(pattern, query_lower):
            found.append(company.title())
    return found


_KNOWN_ROLES = [
    "software engineer", "sde", "backend engineer", "frontend engineer",
    "full stack", "fullstack", "product manager", "data scientist",
    "data analyst", "data engineer", "ml engineer", "machine learning",
    "devops", "sre", "system design", "architect", "tech lead",
    "engineering manager", "qa engineer", "test engineer", "security engineer",
    "mobile developer", "android developer", "ios developer",
    "cloud engineer", "platform engineer",
]


def _extract_roles(query: str) -> list:
    query_lower = query.lower()
    found = []
    for role in _KNOWN_ROLES:
        if role in query_lower:
            found.append(role.title())
    return found


_KNOWN_SKILLS = [
    "python", "java", "javascript", "typescript", "go", "golang", "rust",
    "c++", "cpp", "react", "angular", "vue", "node", "nodejs", "django",
    "flask", "fastapi", "spring", "docker", "kubernetes", "k8s", "aws",
    "gcp", "azure", "sql", "nosql", "mongodb", "redis", "kafka",
    "machine learning", "deep learning", "nlp", "computer vision",
    "system design", "dsa", "data structures", "algorithms",
    "microservices", "graphql", "rest api", "ci/cd", "terraform",
]


def _extract_skills(query: str) -> list:
    query_lower = query.lower()
    found = []
    for skill in _KNOWN_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, query_lower):
            found.append(skill)
    return found
