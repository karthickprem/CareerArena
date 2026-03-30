"""
Pydantic models for the CareerArena API.
Request/response schemas for all endpoints.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class QueryType(str, Enum):
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


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=2000)
    user_id: Optional[str] = None
    resume_text: Optional[str] = None


class QueryResponse(BaseModel):
    session_id: str
    status: str = "queued"
    message: str = "Query submitted successfully"


class AgentInfo(BaseModel):
    agent_id: str
    name: str
    agent_type: str
    lead_type: str
    company: Optional[str] = None
    cognitive_style: str = ""
    is_adversarial: bool = False


class ArenaPost(BaseModel):
    post_id: int
    agent_id: str
    agent_name: str
    agent_type: str
    topic: str
    content: str
    post_type: str = "analysis"
    confidence: Optional[float] = None
    round_num: int = 0
    likes: int = 0
    dislikes: int = 0
    created_at: str
    comments: List[ArenaComment] = []


class ArenaComment(BaseModel):
    comment_id: int
    post_id: int
    agent_id: str
    agent_name: str
    content: str
    comment_type: str = "response"
    parent_comment_id: Optional[int] = None
    round_num: int = 0
    likes: int = 0
    dislikes: int = 0
    created_at: str


ArenaPost.model_rebuild()


class ReportSection(BaseModel):
    heading: str
    content: str
    confidence: Optional[float] = None
    key_insights: List[str] = []
    recommendations: List[str] = []
    caveats: List[str] = []
    source_agents: List[str] = []


class Report(BaseModel):
    title: str
    executive_summary: str
    sections: List[ReportSection] = []
    key_recommendations: List[str] = []
    risk_factors: List[str] = []
    data_quality_note: str = ""
    next_steps: List[str] = []


class SessionStatus(BaseModel):
    session_id: str
    status: str
    query: str
    query_type: str
    companies: List[str] = []
    agents: List[AgentInfo] = []
    arena_stats: Dict[str, Any] = {}
    report: Optional[Report] = None
    elapsed_seconds: Optional[float] = None
    created_at: Optional[str] = None
    logs: List[Dict[str, Any]] = []
    tier_stats: Optional[Dict[str, int]] = None
    graph_stats: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class SessionListItem(BaseModel):
    session_id: str
    query: str
    query_type: str
    status: str
    created_at: str
    agents_count: int = 0


class WSMessage(BaseModel):
    type: str  # "status", "agent_action", "arena_post", "report_ready", "error"
    data: Dict[str, Any] = {}
    timestamp: Optional[str] = None
