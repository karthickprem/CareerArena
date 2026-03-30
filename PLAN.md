# CareerArena — AI Career Intelligence Engine

## Product Vision

**One-liner**: An AI-powered career intelligence engine where multiple specialist agents analyze your profile, debate your options in a visible arena, and deliver personalized, evidence-backed career strategy — not just job listings.

**What we are NOT**: A job board. A resume builder. A chatbot wrapper.

**What we ARE**: A team of AI career analysts that researches, debates, and strategizes on your behalf — like having a ₹50K/hr career advisory board for ₹999/month. And you can WATCH them work.

---

## Why Multi-Agent (The Moat)

Career decisions are inherently multi-faceted. No single perspective gives good advice:

- A salary expert might say "Take the higher-paying offer"
- A career strategist might say "The lower-paying startup has better growth"
- A market analyst might say "That entire sector is declining"
- A skills expert might say "You're not ready for either — build X first"

Our arena makes these agents **debate each other**, challenge assumptions, and produce a **consensus recommendation with dissenting views**. Users can watch the debate live. This is fundamentally different from a single AI giving one answer.

---

## Architecture Overview

### Two-Level Agent Hierarchy

```
┌──────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE                             │
│            Chat + Report View + VISIBLE ARENA (Reddit-style)         │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR                                 │
│                                                                      │
│  ┌──────────┐  ┌────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Query    │  │ Agent Pool │  │   Debate     │  │   Report     │  │
│  │  Router   │  │ Manager    │  │   Manager    │  │   Synthesizer│  │
│  └──────────┘  └────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────┐  ┌────────────┐                                       │
│  │ Directive │  │  Memory    │                                       │
│  │ Controller│  │  Manager   │                                       │
│  └──────────┘  └────────────┘                                       │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FIXED AGENTS (Team Leads)                        │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ Profile  │ │ Market   │ │Interview │ │ Skills   │ │Compensat.│ │
│  │ Analyst  │ │ Intel    │ │ Coach    │ │ Gap      │ │Strategist│ │
│  │ (Lead)   │ │ (Lead)   │ │ (Lead)   │ │ (Lead)   │ │ (Lead)   │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ │
│       │            │            │            │            │        │
│  ┌──────────┐                                                      │
│  │Contrarian│   (always active, challenges ALL findings)            │
│  │(Global)  │                                                      │
│  └──────────┘                                                      │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│               DYNAMIC SUB-AGENTS (Spawned Per Query)                │
│                                                                     │
│  Under Market Intel Lead:                                           │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐          │
│  │ Razorpay  │ │ PhonePe   │ │ Juspay    │ │ Stripe    │          │
│  │ Analyst   │ │ Analyst   │ │ Analyst   │ │ Analyst   │          │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘          │
│                                                                     │
│  Under Interview Coach Lead:                                        │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐                        │
│  │ Razorpay  │ │ PhonePe   │ │ Juspay    │                        │
│  │ Interview │ │ Interview │ │ Interview │                        │
│  └───────────┘ └───────────┘ └───────────┘                        │
│                                                                     │
│  Under Compensation Lead:                                           │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐                        │
│  │ Razorpay  │ │ PhonePe   │ │ Juspay    │                        │
│  │ Comp      │ │ Comp      │ │ Comp      │                        │
│  └───────────┘ └───────────┘ └───────────┘                        │
│                                                                     │
│  (Sub-agents are created dynamically based on user query context)   │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          TOOLS LAYER                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │WebSearch │ │ Salary   │ │ Company  │ │ Resume   │              │
│  │          │ │ Scraper  │ │ Data     │ │ Parser   │              │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │StockData │ │ News     │ │ Interview│ │ Course   │              │
│  │          │ │ Search   │ │ Patterns │ │ Database │              │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                 │
│  SQLite DB (forum posts, comments, memory, directives, cache)       │
│  Reused from Debug Arena's SimulationDB                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## How Two-Level Agents Work

### Fixed Agents (Team Leads)
Always present. 6 permanent specialists. They coordinate their domain and synthesize sub-agent findings.

| Fixed Agent | Role | Spawns Sub-Agents? |
|---|---|---|
| Profile Analyst | Honest resume/profile assessment | No (works alone) |
| Market Intel Lead | Market conditions, hiring trends | Yes — one per target company |
| Interview Coach Lead | Interview prep and strategy | Yes — one per target company |
| Skills Gap Lead | Skill assessment and learning path | Sometimes — per domain/stack |
| Compensation Lead | Salary, stocks, ESOPs, negotiation | Yes — one per target company |
| Contrarian | Challenges ALL findings | No (works alone, reads everything) |

### Dynamic Sub-Agents
Spawned based on the user's query and resume. If the user mentions 3 companies, the orchestrator creates 3 sub-agents under each relevant lead.

**Example: "Where should I apply in fintech?"**
```
Orchestrator analyzes → user targets fintech, backend role, 4yr experience
→ Identifies top 5 matching companies: Razorpay, PhonePe, Juspay, CRED, Stripe India
→ Spawns under Market Intel: 5 company-specific analysts
→ Spawns under Interview Coach: 5 company-specific prep experts
→ Spawns under Compensation: 5 company-specific comp analysts
→ Total: 6 fixed + 15 dynamic = 21 agents in the arena
→ Cap: max 5 companies, max 20 dynamic sub-agents per session
```

### How Sub-Agents Map to Debug Arena's Pattern
In Debug Arena, agents are created from knowledge graph entities (each IP block, register, firmware module becomes an agent). In CareerArena:
- The "knowledge graph" is the user's career context (companies, roles, skills)
- Each target company becomes a set of sub-agents
- Entity categories map: hardware/software/error → company/role/skill
- Same forum-based debate, same parallel execution, same directive system

---

## Visible Arena UX

### Two Views — Summary (Default) + Arena (Opt-in)

#### View 1: Summary Report (Default)
Clean, structured output. What most users see first.

```
┌─────────────────────────────────────────────────────────────┐
│  YOUR CAREER INTELLIGENCE REPORT                            │
│  Generated by 18 AI analysts | 2 debate rounds | 3 min     │
│                                                             │
│  🎯 Readiness: 65% for Senior Backend in Fintech           │
│                                                             │
│  💰 Salary Comparison                                       │
│  ┌──────────┬─────────┬─────────┬────────┬────────┐        │
│  │          │Razorpay │ PhonePe │ Juspay │ CRED   │        │
│  ├──────────┼─────────┼─────────┼────────┼────────┤        │
│  │ Base     │ ₹42L    │ ₹35L    │ ₹32L   │ ₹38L   │        │
│  │ Real Comp│ ₹48L    │ ₹52L    │ ₹35L*  │ ₹44L   │        │
│  │ Upside   │ Medium  │ Low     │ HIGH   │ Medium │        │
│  │ Your Fit │ 70%     │ 85%     │ 55%    │ 60%    │        │
│  └──────────┴─────────┴─────────┴────────┴────────┘        │
│  * Juspay ESOPs could be worth ₹40-80L if IPO              │
│                                                             │
│  ⚠️ Top Risks                                               │
│  1. No payment systems experience (required by 3/4)         │
│  2. Razorpay had layoffs in Q4 2025                         │
│  3. Your Go experience is thin                              │
│                                                             │
│  📋 Recommended Action Plan                                 │
│  Week 1-2: Build a payment gateway side project             │
│  Week 3-4: Practice system design (payments focus)          │
│  Week 5: Apply to PhonePe first (highest fit)               │
│                                                             │
│  🏟️ [Watch the full agent debate →]                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### View 2: Arena View (Opt-in)
Reddit-style threaded debate. Grouped by topic. Expandable.

```
┌─────────────────────────────────────────────────────────────┐
│  🏟️ CAREER ARENA — Agent Discussion                        │
│  18 agents | 2 rounds | Topics: Salary, Skills, Interviews │
│                                                             │
│  ┌─ 💰 COMPENSATION THREAD ──────────────────────────────┐ │
│  │                                                       │ │
│  │  🏢 Razorpay_Comp_Analyst                     ▲ 12    │ │
│  │  "Base: ₹38-45L. ESOPs ~₹8-12L at current    │       │ │
│  │   valuation. But IPO timeline is unclear."     │       │ │
│  │                                                │       │ │
│  │    └─ 🏢 PhonePe_Comp_Analyst             ▲ 18│       │ │
│  │       "Base: ₹32-38L (lower). BUT RSUs via     │       │ │
│  │        Walmart — liquid, publicly traded.       │       │ │
│  │        Real total comp: ₹45-55L."               │       │ │
│  │                                                 │       │ │
│  │       └─ 😈 Contrarian                    ▲ 24 │       │ │
│  │          "You're both ignoring Juspay.          │       │ │
│  │           Lower base but 10x ESOP upside."      │       │ │
│  │                                                 │       │ │
│  │    └─ 💰 Compensation_Lead (Summary)            │       │ │
│  │       "Best risk-adjusted comp: PhonePe.        │       │ │
│  │        Best upside: Juspay. Best base: Razorpay"│       │ │
│  │                                                 │       │ │
│  └─────────────────────────────────────────────────┘       │
│                                                             │
│  ┌─ 🎓 SKILLS DEBATE ─────────────────────── [expand ▸] ┐ │
│  │  4 agents discussed • Key finding: Payment systems    │ │
│  │  experience is critical gap                           │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─ 🎤 INTERVIEW PREP ──────────────────── [expand ▸]  ┐ │
│  │  5 agents discussed • Key finding: PhonePe is most   │ │
│  │  aligned with user's current skillset                │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─ 📊 MARKET SIGNALS ──────────────────── [expand ▸]  ┐ │
│  │  5 agents discussed • Key finding: Fintech hiring    │ │
│  │  is recovering but selective                         │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

Agents vote (upvote/downvote) on each other's posts. Higher-voted findings surface first. Users see which claims were challenged and which survived scrutiny.

---

## The Orchestrator Layer (Detailed)

### Adapted from Debug Arena's Two-Controller Pattern

Debug Arena has two orchestration styles:
1. `Simulation` (simulation.py) — parallel turn executor, manages forum, injects directives
2. `ReportAgent` (report_agent.py) — LLM planner that reads transcripts, issues directives, decides stop

CareerArena combines these into a single Orchestrator:

### Orchestrator Flow

```
User Input (chat message or resume upload)
    │
    ▼
[1] QUERY ROUTER (new — replaces config_generator.py)
    │ • Classifies intent (INTERVIEW_READINESS, SALARY_INTEL, etc.)
    │ • Extracts entities: companies, roles, skills mentioned
    │ • Determines which fixed agents to activate
    │ • Determines how many sub-agents to spawn per company
    │ • Sets debate depth (1-3 rounds)
    ▼
[2] AGENT POOL MANAGER (adapts profile_generator.py)
    │ • Creates fixed agent instances with personas
    │ • Spawns dynamic sub-agents for each target company
    │ • Assigns cognitive styles (from Debug Arena's COGNITIVE_STYLES)
    │ • Marks Contrarian as adversarial (is_adversarial=True)
    │ • Loads tools for each agent
    ▼
[3] DEBATE MANAGER — Round 1: INVESTIGATE (adapts simulation.py)
    │ • All agents run in PARALLEL (ThreadPoolExecutor)
    │ • Each agent: tool calls → findings → post to arena
    │ • Uses Debug Arena's ReAct pattern: plan tools → execute → reason
    │ • Sub-agents research their specific company
    │ • Findings stored in DB (posts table)
    ▼
[4] DEBATE MANAGER — Round 2: DEBATE
    │ • Agents read each other's posts (personalized feed)
    │ • Challenge, agree, add nuance via comments
    │ • Contrarian MUST challenge at least one finding
    │ • Lead agents synthesize their sub-agents' findings
    │ • Vote system: agents upvote/downvote posts
    ▼
[5] DIRECTIVE CONTROLLER (optional, from report_agent.py pattern)
    │ • If significant disagreement detected:
    │   → Issues targeted directives to specific agents
    │   → "Razorpay_Analyst: verify the layoff numbers"
    │   → Runs Round 3 with only targeted agents
    ▼
[6] REPORT SYNTHESIZER (adapts report_agent.py)
    │ • Reads full arena transcript from DB
    │ • Multi-step investigation (report_agent's 3-6 step loop)
    │ • Produces structured JSON report
    │ • Generates chat-friendly summary
    │ • Attributes insights to agents
    │ • Highlights disagreements
    ▼
[7] MEMORY MANAGER
    │ • Stores session + findings + recommendations
    │ • Links to user profile for future context
    │ • Tracks for outcome feedback loop
    ▼
Output → User (Summary Report + Arena View)
```

---

## Agent Definitions

### Fixed Agent 1: Profile Analyst

**Role**: Brutally honest assessment of user's resume and professional profile.
**Persona**: Senior technical recruiter with 15 years of experience. Has seen 50,000 resumes.
**Tools**: resume_parser, web_search
**Sub-agents**: None (works alone)
**Key behavior**: Compares resume against EACH target role's specific requirements.

### Fixed Agent 2: Market Intelligence Lead

**Role**: Coordinates market research across all target companies.
**Persona**: Labor market economist tracking hiring trends daily.
**Tools**: salary_scraper, company_data, news_search, job_trends
**Sub-agents**: One per target company (e.g., Razorpay_Market_Analyst)
**Key behavior**: Lead synthesizes sub-agent findings into comparative analysis.

Each **Market Sub-Agent** has persona like:
> "You are an analyst specializing in {company_name}. Research their current
> hiring status, team size, recent news, growth trajectory, and what it's
> like to work there. Be specific and cite sources."

### Fixed Agent 3: Interview Coach Lead

**Role**: Coordinates interview preparation across target companies.
**Persona**: Ex-FAANG interviewer who has conducted 2,000+ interviews.
**Tools**: interview_patterns_db, company_data, web_search
**Sub-agents**: One per target company
**Key behavior**: Each sub-agent knows that specific company's interview process.

### Fixed Agent 4: Skills Gap Lead

**Role**: Identifies skill gaps and creates learning paths.
**Persona**: Technical learning architect who designs training paths.
**Tools**: web_search, course_database
**Sub-agents**: Optional — per technical domain if multiple skill areas
**Key behavior**: Maps current skills → required skills → gap → resources.

### Fixed Agent 5: Compensation Lead

**Role**: Analyzes total compensation and negotiation strategy.
**Persona**: Compensation consultant who has advised on 1,000+ offers.
**Tools**: salary_scraper, stock_data, company_data, web_search
**Sub-agents**: One per target company (breaks down each company's comp)
**Key behavior**: Sub-agents provide per-company breakdown, Lead creates comparison.

### Fixed Agent 6: Contrarian (Global)

**Role**: Challenges EVERY positive finding from ALL agents.
**Persona**: Skeptical career advisor. Always asks "what could go wrong?"
**Tools**: web_search, news_search, company_data
**Sub-agents**: None (reads everything, challenges everything)
**Key behavior**:
- Must disagree with at least one finding per company
- Must suggest at least one alternative company nobody mentioned
- Must flag at least one risk per recommendation
- Evidence-based only

---

## Debug Arena → CareerArena Component Map

### Direct Reuse (No Changes)

| Debug Arena File | Use In CareerArena | Notes |
|---|---|---|
| `llm_client.py` | LLM interface | Reuse as-is. Same OpenAI/Anthropic adapter. |
| `tools/base.py` | Tool ABC + ToolResult | Reuse as-is. Same Tool interface. |
| `tools/__init__.py` | Tool registry pattern | Reuse pattern, swap tool classes. |

### Adapt (Same Architecture, New Domain)

| Debug Arena File | CareerArena File | What Changes |
|---|---|---|
| `database.py` | `database.py` | Add: users, sessions, salary_cache, company_cache, interview_patterns, outcomes tables. Keep: posts, comments, follows, agent_memory, directives, agent_actions. |
| `simulation.py` | `orchestrator.py` | Core stays: parallel agent execution, ReAct tool loop, forum posting, directive injection, memory management. Change: agent personas, prompt templates, cognitive styles tuned for career domain. Add: query routing, sub-agent spawning, two-layer hierarchy. |
| `graph_builder.py` | `context_builder.py` | Instead of extracting entities from a bug report, extract context from resume + query: companies mentioned, roles, skills, experience level. Same chunking + LLM extraction pattern. |
| `profile_generator.py` | `agent_factory.py` | Instead of generating profiles from graph entities, generate agent personas from career context. Fixed agents have static personas. Dynamic sub-agents get company-specific personas. Same parallel generation pattern. |
| `config_generator.py` | `query_router.py` | Instead of generating simulation config, classify user query and determine: intent type, agents to activate, sub-agents to spawn, debate depth, initial seed posts. |
| `report_agent.py` | `synthesizer.py` | Same multi-step investigation loop (3-6 steps). Same DB-backed tools (read_full_forum, get_agent_position, search_memories). Output format changes to career report JSON. |
| `forum.py` | `arena.py` | Same forum mechanics (posts, comments, threads, likes). Add: topic grouping (compensation, skills, interviews), vote aggregation for arena view. |
| `main.py` | `main.py` | New pipeline: input → context build → agent factory → orchestrator → synthesizer → output. Same stage-based approach. |

### New Files (Career-Specific)

| New File | Purpose |
|---|---|
| `tools/web_search.py` | Web search via SerpAPI/Tavily/Brave |
| `tools/salary_scraper.py` | Scrape salary data from AmbitionBox/Levels.fyi |
| `tools/company_data.py` | Company info aggregator (web scraping + APIs) |
| `tools/resume_parser.py` | Parse PDF/DOCX resumes into structured data |
| `tools/stock_data.py` | Stock/ESOP valuation via Yahoo Finance |
| `tools/news_search.py` | Recent news about companies |
| `tools/interview_patterns.py` | Query internal interview patterns DB |
| `tools/course_db.py` | Search learning resources |
| `api.py` | FastAPI endpoints (REST + WebSocket) |
| `models.py` | Pydantic models for API request/response |

---

## Query Types

| Query Type | Example | Fixed Agents | Sub-Agents Per Company | Rounds |
|---|---|---|---|---|
| `PROFILE_REVIEW` | "Review my resume" | Profile, SkillsGap | 0 | 1 |
| `CAREER_STRATEGY` | "What should I do next?" | All 6 | 3-5 companies | 2-3 |
| `INTERVIEW_READINESS` | "Am I ready for X at Y?" | Profile, Skills, Interview, Market, Contrarian | 1-3 companies | 2 |
| `SALARY_INTEL` | "Salary for SDE-2 at Google?" | Market, Compensation | 1 company | 1 |
| `OFFER_COMPARISON` | "Compare these two offers" | Compensation, Market, Contrarian | 2-4 companies | 2 |
| `COMPANY_RESEARCH` | "Tell me about Razorpay" | Market, Interview, Compensation, Contrarian | 1 company | 2 |
| `SKILL_PLANNING` | "How to become ML engineer?" | SkillsGap, Market | 0-3 companies | 1-2 |
| `INTERVIEW_PREP` | "Prepare me for Amazon" | Interview, SkillsGap, Profile | 1 company | 2 |
| `NEGOTIATION` | "How to negotiate this offer?" | Compensation, Market, Contrarian | 1-2 companies | 2 |

---

## Database Schema

```sql
-- ============================================================
-- REUSED FROM DEBUG ARENA (with minor renames)
-- ============================================================

-- Arena posts (was: posts)
CREATE TABLE arena_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    agent_id TEXT,
    agent_name TEXT,
    agent_type TEXT,            -- 'fixed_lead' | 'dynamic_sub' | 'contrarian'
    parent_agent TEXT,          -- for sub-agents: which lead they belong to
    topic TEXT,                 -- 'compensation' | 'skills' | 'interview' | 'market' | 'general'
    content TEXT,
    post_type TEXT,             -- finding, challenge, evidence, recommendation, summary
    confidence REAL,
    evidence JSON,
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Arena comments with threading (was: comments)
CREATE TABLE arena_comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER REFERENCES arena_posts(id),
    parent_comment_id INTEGER,
    agent_id TEXT,
    agent_name TEXT,
    content TEXT,
    comment_type TEXT,          -- agree, disagree, add_nuance, challenge, evidence
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent memory across sessions (reused)
CREATE TABLE agent_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    session_id TEXT,
    agent_id TEXT,
    memory_type TEXT,           -- hypothesis, finding, tool_citation, recommendation
    content TEXT,
    confidence REAL,
    evidence JSON,
    source_tool TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Directives for targeted follow-up (reused)
CREATE TABLE directives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    target_agent_id TEXT,
    target_agent_name TEXT,
    task TEXT,
    status TEXT DEFAULT 'pending',  -- pending, completed
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- NEW FOR CAREER ARENA
-- ============================================================

-- User profiles
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resume_raw TEXT,            -- original resume text
    resume_data JSON,           -- parsed structured resume
    preferences JSON,           -- target roles, salary range, locations, industries
    linkedin_url TEXT
);

-- Sessions (one per user query)
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id),
    query_text TEXT,
    query_type TEXT,
    agents_activated JSON,      -- list of agent IDs used
    companies_analyzed JSON,    -- list of companies researched
    debate_rounds INTEGER,
    status TEXT DEFAULT 'running', -- running, completed, failed
    report JSON,                -- final synthesized report
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Outcome tracking (THE DATA MOAT)
CREATE TABLE outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT REFERENCES users(id),
    session_id TEXT REFERENCES sessions(id),
    recommendation TEXT,
    outcome TEXT,               -- got_offer, rejected, withdrew, accepted, negotiated
    outcome_details JSON,       -- company, role, final_salary, etc.
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cached salary data
CREATE TABLE salary_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    role TEXT,
    level TEXT,
    city TEXT,
    salary_data JSON,           -- {p25, p50, p75, sample_size}
    source TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cached company data
CREATE TABLE company_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT UNIQUE,
    company_data JSON,          -- {funding, headcount, news, culture, glassdoor_rating}
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interview patterns (grows over time from users + scraping)
CREATE TABLE interview_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    role TEXT,
    level TEXT,
    pattern_data JSON,          -- {rounds, question_types, tips, duration}
    source TEXT,                 -- scraped | user_feedback | manual
    confidence REAL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Technical Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI (async, WebSocket for real-time arena streaming)
- **LLM Client**: Reuse Debug Arena's `llm_client.py` (OpenAI/Anthropic)
- **Database**: SQLite (MVP) → PostgreSQL (scale)
- **Task Queue**: None for MVP → Celery/Redis at scale

### Frontend
- **Framework**: Next.js 14+ (React)
- **UI Library**: shadcn/ui
- **Real-time**: WebSocket for streaming arena debate to user live

### Infrastructure
- **Hosting**: Railway or Fly.io (MVP)
- **LLM**: GPT-4o-mini for sub-agents, GPT-4o for Lead agents + Synthesizer
- **Cost**: Cache company/salary data aggressively. Sub-agents use cheaper models.

---

## Revenue Model

| Tier | Price | Target | Features |
|---|---|---|---|
| **Free** | ₹0 | Everyone | 3 queries/month, basic profile review, arena view |
| **Pro** | ₹999/month | Active job seekers | Unlimited queries, full reports, interview prep |
| **Premium** | ₹2,499/month | Senior professionals | + ESOP analysis, offer comparison, negotiation |
| **College** | ₹5-15L/year | Placement cells | Bulk access, admin dashboard, placement analytics |
| **Enterprise** | ₹2-5L/year | HR/L&D teams | Internal mobility, career pathing |

---

## Key Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| LLM hallucination on salary/company data | High | Cross-verify with scraped data. Agents cite sources. Confidence scores on all claims. |
| Too many agents = expensive | Medium | Cap at 5 companies / 20 sub-agents. Use GPT-4o-mini for sub-agents. Cache aggressively. |
| Users overwhelmed by arena | Medium | Summary view is default. Arena is opt-in. Grouped by topic. Collapsible threads. |
| "Just another AI career app" | Medium | The visible arena IS the differentiator. Nothing else shows you AI reasoning. |
| Competition copies approach | Medium | Data moat (outcome tracking). First-mover. Speed. |

---

## Success Metrics

### Month 1: MVP Live
- Working product with 6 fixed agents + dynamic sub-agents
- Visible arena view
- 50+ beta users

### Month 3: Traction
- 500+ users, 100+ weekly active
- 20+ paying Pro subscribers
- NPS > 50

### Month 6: Revenue
- 2,000+ users
- 100+ paying subscribers
- 3-5 college partnerships
- Outcome tracking live
- Pre-seed raised

### Month 12: Scale
- 10,000+ users
- 500+ paying subscribers
- 10+ colleges
- Proprietary career outcome dataset
- Seed round ready

---
---

# EXECUTION PLAN

## Debug Arena Core Stack Reuse Map

```
debug_arena/                    career_arena/
├── llm_client.py          →   ├── llm_client.py            [COPY AS-IS]
├── database.py            →   ├── database.py              [EXTEND — add new tables]
├── simulation.py          →   ├── orchestrator.py           [ADAPT — core engine]
├── forum.py               →   ├── arena.py                  [ADAPT — add topics, votes]
├── graph_builder.py       →   ├── context_builder.py        [ADAPT — resume/query context]
├── profile_generator.py   →   ├── agent_factory.py          [ADAPT — career agent profiles]
├── config_generator.py    →   ├── query_router.py           [ADAPT — query classification]
├── report_agent.py        →   ├── synthesizer.py            [ADAPT — career report output]
├── main.py                →   ├── main.py                   [REWRITE — new pipeline]
├── tools/                      ├── tools/
│   ├── base.py            →   │   ├── base.py              [COPY AS-IS]
│   ├── __init__.py        →   │   ├── __init__.py          [ADAPT — new tool list]
│   ├── regdb.py           ✗   │   ├── web_search.py        [NEW]
│   ├── jira_search.py     ✗   │   ├── salary_scraper.py    [NEW]
│   ├── doc_search.py      ✗   │   ├── company_data.py      [NEW]
│   ├── code_search.py     ✗   │   ├── resume_parser.py     [NEW]
│   └── ...                ✗   │   ├── news_search.py        [NEW]
│                               │   ├── stock_data.py         [NEW]
│                               │   └── interview_patterns.py [NEW]
│                               ├── api.py                    [NEW — FastAPI endpoints]
│                               ├── models.py                 [NEW — Pydantic schemas]
│                               └── frontend/                 [NEW — Next.js app]
```

---

## Day-by-Day Execution Plan

### WEEK 1: Core Engine (Days 1-7)

#### Day 1: Project Setup + Database
- [ ] Create `career_arena/` directory structure
- [ ] Copy `llm_client.py` and `tools/base.py` from debug_arena
- [ ] Adapt `database.py`: add users, sessions, salary_cache, company_cache, interview_patterns, outcomes tables on top of existing posts/comments/memory/directives
- [ ] Write database migration/init script
- [ ] Test: create DB, insert test data, query back

#### Day 2: Tools — Web Search + Resume Parser
- [ ] Implement `tools/web_search.py` (Tavily or SerpAPI — pick one)
- [ ] Implement `tools/resume_parser.py` (pdfplumber for PDF, python-docx for DOCX, extract structured data)
- [ ] Set up `tools/__init__.py` with new tool registry
- [ ] Test: search "Razorpay salary SDE-2", parse a sample resume

#### Day 3: Tools — Salary + Company Data
- [ ] Implement `tools/salary_scraper.py` (scrape AmbitionBox or use web search as proxy)
- [ ] Implement `tools/company_data.py` (aggregate from web search + news)
- [ ] Implement `tools/news_search.py` (NewsAPI or web search filtered)
- [ ] Test: get salary for "Backend Engineer at Razorpay Bangalore"

#### Day 4: Query Router + Context Builder
- [ ] Implement `query_router.py`: LLM classifies intent, extracts companies/roles/skills
- [ ] Implement `context_builder.py`: takes resume + query → extracts career context (target companies, roles, experience level, skills)
- [ ] Output: `CareerContext` object with all entities needed for agent spawning
- [ ] Test: "Am I ready for Razorpay?" → {intent: INTERVIEW_READINESS, companies: ["Razorpay"], role: "Backend Engineer"}

#### Day 5: Agent Factory (Fixed + Dynamic)
- [ ] Implement `agent_factory.py`:
  - Fixed agent persona templates (Profile, Market Lead, Interview Lead, Skills Lead, Comp Lead, Contrarian)
  - Dynamic sub-agent generator: given a company name + lead type → generate company-specific persona
  - Cognitive style assignment (from Debug Arena)
  - Adversarial flag for Contrarian
- [ ] Test: generate full agent roster for a 3-company query

#### Day 6: Orchestrator Core (Adapt simulation.py)
- [ ] Implement `orchestrator.py`:
  - Port `_run_round_parallel` from simulation.py
  - Port `_run_agent_turn` with ReAct tool loop
  - Port Phase 1 (analyze + hypothesize) and Phase 2 (post/comment/reply)
  - Add two-round debate flow: Investigate → Debate
  - Wire in directive system from Debug Arena
- [ ] Implement `arena.py` (adapt forum.py): posts with topics, comments with threading, vote tracking
- [ ] Test: run a full 2-round debate with 4 agents on a test query

#### Day 7: Report Synthesizer
- [ ] Implement `synthesizer.py` (adapt report_agent.py):
  - Multi-step investigation loop (read arena, analyze, synthesize)
  - Career report JSON schema (readiness score, salary comparison, risks, action plan)
  - Generate both structured report and chat-friendly summary
- [ ] Wire up full pipeline: main.py → query router → agent factory → orchestrator → synthesizer → output
- [ ] Test: end-to-end run with a real query + resume

### WEEK 2: API + Frontend (Days 8-14)

#### Day 8: FastAPI Backend
- [ ] Implement `api.py`:
  - POST `/api/query` — submit career query (with optional resume upload)
  - GET `/api/session/{id}` — get session status + report
  - GET `/api/arena/{session_id}` — get arena posts/comments for arena view
  - WebSocket `/ws/session/{id}` — stream arena debate in real-time
- [ ] Implement `models.py` — Pydantic request/response schemas
- [ ] Test: submit query via curl, get report back

#### Day 9: Frontend — Project Setup + Chat UI
- [ ] Initialize Next.js project in `frontend/`
- [ ] Install shadcn/ui
- [ ] Build chat interface: text input + resume upload button
- [ ] Connect to API: submit query, show loading state
- [ ] Display: streaming status ("Profile Analyst is investigating...")

#### Day 10: Frontend — Report View
- [ ] Build structured report component:
  - Readiness score (circular progress)
  - Salary comparison table
  - Risk list
  - Action plan with timeline
  - "Watch Arena" button
- [ ] Style with shadcn/ui (clean, professional)

#### Day 11: Frontend — Arena View
- [ ] Build Reddit-style arena view:
  - Posts grouped by topic (Compensation, Skills, Interview, Market)
  - Threaded comments (collapsible)
  - Agent name + type badges (Lead, Sub-Agent, Contrarian)
  - Upvote/downvote display
  - Expand/collapse per topic group
- [ ] Connect to arena API endpoint

#### Day 12: Frontend — Real-time Streaming
- [ ] WebSocket connection: stream arena posts as agents debate
- [ ] Show agent activity indicators ("Razorpay_Analyst is typing...")
- [ ] Auto-scroll as new posts appear
- [ ] Transition: debate → report when complete

#### Day 13: User Accounts + Resume Storage
- [ ] Simple auth (email + password, or magic link)
- [ ] Store resume in user profile
- [ ] Session history (list of past queries + reports)
- [ ] Resume auto-attached to future queries

#### Day 14: Integration Testing
- [ ] Full end-to-end test: signup → upload resume → query → debate → report → arena view
- [ ] Fix bugs, handle edge cases
- [ ] Test with 3-5 different query types

### WEEK 3: Polish + Launch (Days 15-21)

#### Day 15: Add Remaining Agents
- [ ] Add SkillsGap agent with course/resource recommendations
- [ ] Add Compensation agent with stock/ESOP analysis
- [ ] Add `tools/stock_data.py` (Yahoo Finance)
- [ ] Add `tools/interview_patterns.py` (internal DB)

#### Day 16: Seed Data
- [ ] Populate interview_patterns for top 20 Indian tech companies
- [ ] Seed salary_cache with known data points (Levels.fyi, AmbitionBox)
- [ ] Seed company_cache with top 50 tech companies in India

#### Day 17: Cost Optimization + Rate Limiting
- [ ] Implement caching: don't re-scrape company/salary data if < 7 days old
- [ ] Use GPT-4o-mini for sub-agents, GPT-4o only for Lead synthesis + Contrarian
- [ ] Rate limiting: 3 queries/day for free users
- [ ] Error handling: graceful degradation if tool fails

#### Day 18: Landing Page
- [ ] Build landing page (can be a section of the Next.js app)
- [ ] Hero: "Your AI Career Advisory Board"
- [ ] Demo: embedded screenshot/GIF of arena debate
- [ ] CTA: "Try Free — Upload Your Resume"
- [ ] Pricing section

#### Day 19: Deploy
- [ ] Deploy backend to Railway (or Fly.io)
- [ ] Deploy frontend to Vercel
- [ ] Set up domain name
- [ ] SSL, environment variables, API keys
- [ ] Smoke test on production

#### Day 20: Beta Testing
- [ ] Share with 10-15 friends/colleagues
- [ ] Collect feedback (Google Form or in-app)
- [ ] Fix critical bugs

#### Day 21: Soft Launch
- [ ] Post on r/developersIndia, r/indian_academia
- [ ] Share on LinkedIn, Twitter
- [ ] Target: 50 signups in first week

---

## Post-Launch Priorities (Week 4+)

1. **Iterate based on feedback** — fix the top 3 complaints
2. **Outcome tracking** — "Did you get the job? Tell us" prompt after 30 days
3. **Interview pattern crowdsourcing** — "What did they ask you?" after interviews
4. **College outreach** — pitch to 5 placement cells with demo + data
5. **Content marketing** — anonymized arena debates as LinkedIn/Twitter content
