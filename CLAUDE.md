# PlaceRight — AI-Powered End-to-End College Placement Platform

## Product Vision

**One-liner:** "The platform that takes a Tier 3 college student from 'unemployable' to 'placed' — powered by multi-agent AI."

**What we are:** An end-to-end AI placement outcome platform that covers the FULL lifecycle: student profiling, personality assessment, skills gap analysis, personalized training plans, company-specific preparation, multi-agent interview practice, test evaluation, and placement analytics — all in one system.

**What makes us different:**
1. **Full lifecycle** — Not fragments. One platform from Day 1 of final year to offer letter.
2. **Multi-agent AI** — Panel interviews, GD simulation, AI coaching agents. No competitor has this.
3. **Company-specific training** — AI simulates TCS NQT, Infosys InfyTQ, Wipro NLTH interview styles.
4. **Built for Tier 3 economics** — Rs 500-1,500/student/year. Mobile-first. Tamil support from Day 1.

**Target:** Start with ONE college in Tamil Nadu. Prove outcomes. Then expand.

---

## The Problem

- Only **30-50% placement rate** at Tier 3 colleges vs 80-90% at IITs
- **83% of 2024 engineering graduates** remain unemployed
- Only **42.6%** of Indian graduates are employable
- Colleges use **fragmented tools** — SkillRack for coding, FACE for soft skills, AMCAT for testing, spreadsheets for tracking
- **No single platform** covers: assess → plan → train → practice → evaluate → place
- Existing tools are either **too expensive** (FACE charges lakhs), **too shallow** (PrepInsta is question banks), or **not AI-powered** (SkillRack is static)

---

## Platform Modules (6 Pillars)

```
┌──────────────────────────────────────────────────────────────────────┐
│                        PLACERIGHT PLATFORM                          │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │    1.    │  │    2.    │  │    3.    │  │    4.    │           │
│  │ STUDENT  │→│  SKILLS  │→│ TRAINING │→│ COMPANY  │           │
│  │ PROFILER │  │   GAP    │  │   PLAN   │  │ SPECIFIC │           │
│  │          │  │ ANALYZER │  │GENERATOR │  │   PREP   │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│       │                                          │                  │
│       │              ┌──────────┐                │                  │
│       │              │    5.    │                │                  │
│       └─────────────→│INTERVIEW │←───────────────┘                  │
│                      │ PRACTICE │                                   │
│                      │(existing)│                                   │
│                      └────┬─────┘                                   │
│                           │                                         │
│                      ┌────▼─────┐                                   │
│                      │    6.    │                                   │
│                      │  TEST &  │                                   │
│                      │EVALUATE  │                                   │
│                      └──────────┘                                   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              TPO DASHBOARD & PLACEMENT ANALYTICS              │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

### Module 1: Student Profiler
**Purpose:** Build a comprehensive student profile from multiple data points.

**Inputs:**
- Resume upload (PDF/DOCX)
- Academic transcripts (CGPA, subject-wise scores)
- Self-reported skills and interests (form)
- 15-min AI personality assessment (conversational, not MCQ)
- Communication assessment (2-min spoken English sample via mic)
- Technical skills auto-detection from resume + GitHub/LinkedIn (optional)

**AI Agents:**
- **Resume Analyst Agent** — Extracts skills, projects, experience, gaps
- **Personality Profiler Agent** — OCEAN model assessment through conversation (not boring MCQs)
- **Communication Scorer Agent** — Evaluates English fluency, confidence, articulation from voice sample
- **Academic Analyzer Agent** — Maps CGPA + subject scores to company eligibility cutoffs

**Output:** Student Profile Card with:
- Personality traits (OCEAN scores + plain-English description)
- Communication level (L1-L5 scale)
- Technical skills inventory (rated beginner/intermediate/advanced)
- Academic standing (eligible companies list)
- Strengths (top 3) and weaknesses (top 3)
- Employability score (0-100)

### Module 2: Skills Gap Analyzer
**Purpose:** Compare student profile against target company/role requirements.

**How it works:**
```
Student Profile  ──┐
                    ├──→ Gap Analysis Agent ──→ Gap Report
Company Requirements──┘

Example output:
┌─────────────────────────────────────────────────┐
│ TARGET: TCS Digital (Backend Developer)          │
│                                                  │
│ ELIGIBILITY: ✅ CGPA 7.2 (min 6.0)              │
│                                                  │
│ SKILL MATCH:                                     │
│  Python        ████████░░  80%  ✅ Ready         │
│  SQL           ██████░░░░  60%  ⚠️ Needs work   │
│  System Design ███░░░░░░░  30%  ❌ Gap           │
│  DSA           █████░░░░░  50%  ⚠️ Needs work   │
│  Communication ████░░░░░░  40%  ❌ Gap           │
│  Aptitude      ███████░░░  70%  ⚠️ Polish       │
│                                                  │
│ ESTIMATED TIME TO READY: 8-10 weeks              │
│ PLACEMENT PROBABILITY: 45% → 78% (after plan)   │
└─────────────────────────────────────────────────┘
```

**Data source for company requirements:**
- Curated database of company hiring patterns (TCS, Infosys, Wipro, Cognizant, Accenture, etc.)
- Historical placement data from the pilot college
- Web scraping of job postings + interview experiences from GeeksforGeeks, PrepInsta, etc.

### Module 3: Training Plan Generator
**Purpose:** Create a personalized, week-by-week training plan to close gaps.

**AI Agent:** Training Plan Architect Agent
- Takes: Student Profile + Gap Report + available time (weeks until placement season)
- Produces: Week-by-week plan with daily tasks

```
Example: Priya, 3rd year CSE, CGPA 7.2, targeting TCS/Infosys
Available time: 12 weeks

Week 1-3: FOUNDATION
  ├── DSA: Arrays, Strings, Sorting (2 problems/day on LeetCode)
  ├── Aptitude: Number systems, Percentages (30 min/day)
  ├── Communication: Daily 2-min voice recording + AI feedback
  └── Milestone test at end of Week 3

Week 4-6: INTERMEDIATE
  ├── DSA: Trees, Graphs, DP basics (2 problems/day)
  ├── SQL: Joins, Subqueries, Window functions (practice on HackerRank)
  ├── Communication: GD practice with AI (2x/week)
  └── Mock aptitude test (TCS pattern)

Week 7-9: COMPANY-SPECIFIC
  ├── TCS NQT: Full mock tests (3x/week)
  ├── Infosys InfyTQ: Coding rounds practice
  ├── System Design: Basic concepts (API design, DB choice)
  ├── Mock Interview: Panel interview with AI (1x/week)
  └── Resume review + optimization

Week 10-12: INTENSIVE PREP
  ├── Daily mock tests (alternating aptitude/coding)
  ├── 3 full panel interview simulations
  ├── GD practice (2x/week, company-specific topics)
  ├── HR round prep (salary negotiation, "tell me about yourself")
  └── Final readiness assessment
```

**Key principle:** The plan is ADAPTIVE — if the student struggles with DSA in Week 2, the AI extends DSA time and adjusts later weeks. Not a static PDF.

### Module 4: Company-Specific Preparation
**Purpose:** Train students for the EXACT format each company uses.

**Per-company modules (start with top 10 mass recruiters):**

| Company | Selection Process | What We Simulate |
|---------|------------------|-----------------|
| **TCS NQT** | Aptitude + Coding + Email Writing + Interview | Full NQT mock test + panel interview |
| **Infosys InfyTQ** | Aptitude + Coding (Java/Python) + Interview | InfyTQ format tests + HR round |
| **Wipro NLTH** | Aptitude + Essay + Coding + Interview | NLTH pattern test + group discussion |
| **Cognizant GenC** | Aptitude + Coding + Communication + Interview | GenC assessment + panel |
| **Accenture** | Cognitive + Technical + Coding + Interview | Full mock + communication round |
| **Capgemini** | Pseudo Code + English + Technical + Interview | Game-based assessment simulation |
| **HCL** | Aptitude + Technical + Coding + Interview | Standard mock + HR prep |
| **Tech Mahindra** | Aptitude + Coding + GD + Interview | GD simulation + panel |
| **LTI / LTIMindtree** | Aptitude + Coding + Interview | Mock tests + technical deep-dive |
| **Zoho** | Programming round (5 questions in C) + Advanced + Interview | C programming drills + system design |

**Data model:**
```python
CompanyProfile:
    name: str                    # "TCS"
    process_stages: List[Stage]  # [aptitude, coding, email, interview]
    aptitude_pattern: AptitudeConfig  # {quant: 30%, verbal: 25%, reasoning: 25%, etc.}
    coding_difficulty: str       # "easy-medium"
    coding_languages: List[str]  # ["Java", "Python", "C"]
    interview_format: str        # "panel" / "1on1" / "gd_then_panel"
    typical_duration: int        # minutes
    cgpa_cutoff: float          # 6.0
    backlog_policy: str         # "no_active_backlogs"
    salary_range: str           # "3.36-7 LPA"
    question_bank: List[Question]  # Curated from past years
    interview_personas: List[InterviewerPersona]  # Company-style interviewers
```

### Module 5: Interview Practice (PRIMARY FOCUS — Complete This First)
**Status: 70% built, completing to production quality.**

**Architecture (how it actually works):**
```
Screening (Kavitha, 5-phase state machine)
  → CandidateProfile (skills, personality, claims, weaknesses)
    → PanelGenerator (LLM-customized 3-4 interviewers + round plan)
      → RoundManager orchestrates sequential 1-on-1 rounds:
        Round N:
          → InterviewerEngine (phase machine: warmup→explore→deep_dive→pressure→wrap)
          → CandidateModel updated after every answer (strengths, weaknesses, evasion, depth)
          → InterviewForum: non-active interviewers post observations between rounds
        After all rounds:
          → Forum Reveal (progressive "behind the scenes" reveal to candidate)
          → EvaluationEngine (23 dimensions, per-panelist independent scoring)
          → Scorecard (overall score, dimension breakdown, action items)
```

**Key files:**
- `screening_agent.py` (1410 lines) — Kavitha, state-machine screening
- `panel_generator.py` — Profile → customized panel + round plan
- `round_manager.py` (808 lines) — Multi-round orchestrator
- `interviewer_engine.py` (993 lines) — Question bank + phase machine per round type
- `interviewer_swarm.py` (781 lines) — 8-10 debate agents per interviewer (NOT YET WIRED)
- `interview_forum.py` (413 lines) — Hidden inter-interviewer discussion
- `evaluation_engine.py` (130 lines) — Multi-dimensional scoring
- `candidate_model.py` — Real-time candidate assessment

**Known gaps to fix (see Phase 1 build plan above):**
1. InterviewerEngine ↔ RoundManager wiring unclear
2. Live observer reactions not implemented
3. Kavitha transition summary between rounds not implemented
4. CandidateModel not persisted to DB
5. InterviewerSwarm not wired (decision: wire for final round only)
6. Company-specific interviewer personas need seeding

**Modes (planned):**
- Panel Interview (2-4 AI interviewers, company-specific) — WORKING
- Group Discussion (3-5 AI participants + student) — NOT BUILT
- HR Round (behavioral, STAR method) — PARTIAL (via round_type config)
- Technical Deep-Dive (coding, system design) — PARTIAL (via round_type config)
- Stress Interview (rapid-fire, interruptions) — NOT BUILT

**Integration with placement platform (FUTURE — after Modules 1-4 built):**
- Pull student profile into interview context (interviewer knows the resume)
- Track interview scores over time (improvement curve)
- Interview difficulty adapts based on student's current level
- Post-interview feedback feeds back into training plan adjustments

### Module 6: Test & Evaluation Engine
**Purpose:** Regular assessments to measure progress and predict placement probability.

**Test types:**
1. **Aptitude Tests** — Quant, Verbal, Reasoning (company-specific patterns)
2. **Coding Tests** — DSA problems, timed (Easy/Medium/Hard)
3. **Communication Assessment** — AI evaluates spoken response (fluency, grammar, confidence)
4. **Mock Full Tests** — Simulate complete company selection process (2-3 hours)
5. **Personality Re-assessment** — Quarterly, track personality development
6. **Milestone Tests** — End of each training phase (Week 3, 6, 9, 12)

**Scoring:**
- Per-test scores stored longitudinally
- Percentile ranking within the batch
- Placement probability predictor (ML model trained on historical data)
- Weakness detection with specific drill recommendations

**AI Agent:** Evaluation Synthesizer Agent
- Takes all test scores + interview scores + training progress
- Produces: "Priya has improved 23% in aptitude over 4 weeks. Her SQL gap is closing but communication remains at L2. Recommend: 2 additional GD sessions this week. Placement probability for TCS: 72% (up from 45%)."

---

## Database Architecture

### Schema Design (PostgreSQL for production, SQLite for dev)

```sql
-- ==========================================
-- CORE ENTITIES
-- ==========================================

-- College (one for now, designed for multi-tenancy)
CREATE TABLE colleges (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    code            TEXT UNIQUE,              -- "SKCET", "KGISL", etc.
    location        TEXT,                      -- "Coimbatore, TN"
    tier            TEXT DEFAULT 'tier3',
    autonomous      BOOLEAN DEFAULT FALSE,
    total_students  INT,
    tpo_name        TEXT,
    tpo_email       TEXT,
    tpo_phone       TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Batches (2024-2028 batch, 2025-2029 batch, etc.)
CREATE TABLE batches (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    college_id      UUID REFERENCES colleges(id),
    name            TEXT NOT NULL,             -- "2022-2026 CSE"
    department      TEXT NOT NULL,             -- "CSE", "ECE", "IT", "MECH"
    graduation_year INT NOT NULL,             -- 2026
    total_students  INT,
    placement_season_start DATE,              -- When companies start visiting
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- STUDENT PROFILE (The Core Record)
-- ==========================================

CREATE TABLE students (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id        UUID REFERENCES batches(id),

    -- Basic info
    name            TEXT NOT NULL,
    email           TEXT UNIQUE NOT NULL,
    phone           TEXT,
    gender          TEXT,
    dob             DATE,

    -- Academic
    cgpa            DECIMAL(3,2),              -- 7.20
    tenth_pct       DECIMAL(5,2),              -- 89.50
    twelfth_pct     DECIMAL(5,2),              -- 85.00
    backlogs_active INT DEFAULT 0,
    backlogs_history INT DEFAULT 0,

    -- Resume
    resume_raw      TEXT,                      -- Raw resume text
    resume_file_url TEXT,                      -- S3/local path to uploaded resume
    resume_parsed   JSONB,                     -- AI-extracted structured data

    -- Profile (AI-generated)
    personality     JSONB,                     -- OCEAN scores + description
    communication_level TEXT,                  -- L1-L5
    employability_score INT,                   -- 0-100
    strengths       JSONB,                     -- ["problem_solving", "teamwork"]
    weaknesses      JSONB,                     -- ["communication", "dsa"]
    profile_summary TEXT,                      -- AI-written 200-word summary

    -- Technical skills
    skills          JSONB,                     -- {"python": "intermediate", "java": "beginner"}
    github_url      TEXT,
    linkedin_url    TEXT,

    -- Preferences
    target_companies JSONB,                    -- ["TCS", "Infosys", "Wipro"]
    preferred_role  TEXT,                      -- "Backend Developer"
    location_pref   JSONB,                     -- ["Chennai", "Bangalore", "Any"]
    salary_expectation TEXT,                   -- "3-5 LPA"

    -- Status
    placement_status TEXT DEFAULT 'preparing', -- preparing / interviewing / placed / opted_out
    placed_company   TEXT,
    placed_role      TEXT,
    placed_salary    TEXT,
    placed_date      DATE,

    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- ASSESSMENTS & SCORES
-- ==========================================

-- Personality assessment sessions
CREATE TABLE personality_assessments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      UUID REFERENCES students(id),
    assessment_type TEXT NOT NULL,             -- "personality" / "communication" / "aptitude"

    -- For personality: conversational AI assessment
    conversation    JSONB,                     -- Full conversation transcript

    -- Results
    scores          JSONB,                     -- {"openness": 72, "conscientiousness": 85, ...}
    analysis        TEXT,                      -- AI narrative analysis
    recommendations JSONB,                     -- Improvement suggestions

    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Skills inventory (detailed, per-student)
CREATE TABLE skill_assessments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      UUID REFERENCES students(id),
    skill_name      TEXT NOT NULL,             -- "python", "sql", "dsa", "communication"
    category        TEXT NOT NULL,             -- "technical" / "aptitude" / "soft_skill"
    level           TEXT,                      -- "beginner" / "intermediate" / "advanced"
    score           INT,                       -- 0-100
    assessed_by     TEXT,                      -- "ai_test" / "self_reported" / "resume_parse"
    assessed_at     TIMESTAMPTZ DEFAULT NOW()
);

-- Test results (aptitude, coding, mock tests)
CREATE TABLE test_results (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      UUID REFERENCES students(id),
    test_type       TEXT NOT NULL,             -- "aptitude" / "coding" / "mock_full" / "company_specific"
    test_name       TEXT,                      -- "TCS NQT Mock Test 3"
    company_target  TEXT,                      -- "TCS" (null for general tests)

    -- Scores
    total_score     INT,
    max_score       INT,
    percentage      DECIMAL(5,2),
    section_scores  JSONB,                     -- {"quant": 18, "verbal": 15, "reasoning": 20, "coding": 2}

    -- Timing
    time_taken_mins INT,
    time_allowed_mins INT,

    -- Analysis
    wrong_answers   JSONB,                     -- [{question_id, topic, correct_answer, student_answer}]
    weak_topics     JSONB,                     -- ["percentage", "permutation", "dp"]
    ai_feedback     TEXT,                      -- AI-generated feedback

    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- TRAINING PLANS
-- ==========================================

CREATE TABLE training_plans (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      UUID REFERENCES students(id),

    -- Plan metadata
    target_companies JSONB,                    -- ["TCS", "Infosys"]
    total_weeks     INT,                       -- 12
    start_date      DATE,
    end_date        DATE,
    status          TEXT DEFAULT 'active',     -- active / completed / paused / revised

    -- The plan itself
    weekly_plan     JSONB,                     -- Detailed week-by-week structure
    /*
    weekly_plan example:
    [
        {
            "week": 1,
            "theme": "Foundation",
            "tasks": [
                {"type": "dsa", "topic": "Arrays", "daily_target": "2 problems", "resource": "leetcode_easy"},
                {"type": "aptitude", "topic": "Number Systems", "daily_target": "30 min", "resource": "internal"},
                {"type": "communication", "task": "2-min voice recording", "daily_target": "1/day"},
            ],
            "milestone_test": "foundation_test_1",
            "completed": false
        },
        ...
    ]
    */

    -- Progress
    current_week    INT DEFAULT 1,
    overall_progress DECIMAL(5,2) DEFAULT 0,   -- 0-100%

    -- AI adaptation log
    revisions       JSONB,                     -- [{date, reason, changes}]

    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Daily task tracking
CREATE TABLE daily_tasks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id         UUID REFERENCES training_plans(id),
    student_id      UUID REFERENCES students(id),

    date            DATE NOT NULL,
    week_number     INT,

    task_type       TEXT NOT NULL,             -- "dsa" / "aptitude" / "communication" / "mock_test" / "gd"
    task_description TEXT NOT NULL,
    resource_url    TEXT,                      -- Link to problem/exercise

    status          TEXT DEFAULT 'pending',    -- pending / completed / skipped
    time_spent_mins INT,
    score           INT,                       -- If applicable

    completed_at    TIMESTAMPTZ
);

-- ==========================================
-- INTERVIEW SESSIONS (Integrates with existing CareerArena)
-- ==========================================

CREATE TABLE interview_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      UUID REFERENCES students(id),

    -- Config
    interview_type  TEXT NOT NULL,             -- "panel" / "gd" / "hr" / "technical" / "stress"
    company_target  TEXT,                      -- "TCS" (null for general)
    difficulty      TEXT DEFAULT 'realistic',  -- practice / realistic / stress
    panel_size      INT DEFAULT 3,

    -- Session data
    transcript      JSONB,                     -- Full conversation
    duration_mins   INT,

    -- Evaluation
    scores          JSONB,                     -- Per-panelist scores per dimension
    overall_score   INT,                       -- 0-100
    feedback        JSONB,                     -- Per-panelist feedback
    action_items    JSONB,                     -- ["Practice X", "Improve Y"]

    -- Status
    status          TEXT DEFAULT 'in_progress', -- in_progress / completed / abandoned

    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- COMPANY DATA
-- ==========================================

CREATE TABLE companies (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT UNIQUE NOT NULL,
    industry        TEXT,

    -- Hiring info
    typical_roles   JSONB,                     -- ["Backend Developer", "QA", "Support"]
    salary_range    JSONB,                     -- {"min": 336000, "max": 700000}
    cgpa_cutoff     DECIMAL(3,2),
    backlog_policy  TEXT,
    bond_years      INT,

    -- Selection process
    process_stages  JSONB,                     -- ["aptitude", "coding", "gd", "technical_interview", "hr"]
    aptitude_pattern JSONB,                    -- {"quant": 30, "verbal": 25, "reasoning": 25, "programming": 20}
    coding_languages JSONB,                    -- ["Java", "Python", "C"]
    coding_difficulty TEXT,                    -- "easy" / "medium" / "hard"
    interview_format TEXT,                     -- "panel" / "1on1" / "gd_then_panel"

    -- Question bank
    sample_questions JSONB,                    -- Categorized past questions

    -- Interview style (for AI simulation)
    interviewer_personas JSONB,                -- Company-style interviewer templates

    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- College-company placement history
CREATE TABLE placement_history (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    college_id      UUID REFERENCES colleges(id),
    company_id      UUID REFERENCES companies(id),
    batch_id        UUID REFERENCES batches(id),

    year            INT,
    students_eligible INT,
    students_appeared INT,
    students_placed  INT,
    roles_offered   JSONB,
    salary_offered  JSONB,

    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- TPO DASHBOARD DATA
-- ==========================================

-- Placement drives (when companies visit)
CREATE TABLE placement_drives (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    college_id      UUID REFERENCES colleges(id),
    company_id      UUID REFERENCES companies(id),
    batch_id        UUID REFERENCES batches(id),

    drive_date      DATE,
    status          TEXT DEFAULT 'upcoming',   -- upcoming / ongoing / completed / cancelled
    eligible_count  INT,
    registered_count INT,
    appeared_count  INT,
    selected_count  INT,

    -- Results
    selected_students JSONB,                   -- [{student_id, role, salary}]

    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Why This Schema

1. **Student-centric** — Everything connects to the student record. One student, one journey.
2. **Longitudinal tracking** — Every assessment, test, interview is timestamped. We can show improvement curves.
3. **Multi-tenancy ready** — College → Batch → Student hierarchy. One college now, easy to add more.
4. **AI-friendly** — JSONB fields for flexible AI-generated content (personality scores, training plans, evaluation).
5. **Company data is first-class** — Not just question banks. Full company selection process profiles.
6. **TPO dashboard built-in** — Placement drives, eligibility tracking, batch analytics.

---

## LLM Strategy — What to Use, When, and How to Keep Costs Down

### Model Selection Matrix

| Task | Model | Why | Cost/Call | Calls/Student/Month |
|------|-------|-----|-----------|---------------------|
| **Orchestrator decisions** (routing, turn mgmt) | GPT-4o-mini | Fast (<500ms), cheap, good enough for classification | ~Rs 0.2 | 200 |
| **Personality assessment** (conversational) | GPT-4o | Needs nuance, empathy, OCEAN analysis | ~Rs 2-3 | 5 (one-time) |
| **Communication scoring** (voice transcript eval) | GPT-4o-mini | Rubric-based, structured output | ~Rs 0.5 | 10 |
| **Training plan generation** | GPT-4o | Complex reasoning, multi-week planning | ~Rs 3-5 | 2 |
| **Interview agent responses** | GPT-4o | Quality conversation, persona consistency | ~Rs 1-2 | 50 |
| **Interview short reactions** | GPT-4o-mini | "I agree with Priya" — short, fast | ~Rs 0.1 | 30 |
| **Evaluation/scoring** | GPT-4o | Accuracy matters for scoring | ~Rs 2-3 | 10 |
| **Test question generation** | GPT-4o-mini | Pattern-based, template-guided | ~Rs 0.3 | 20 |
| **Daily feedback/nudges** | GPT-4o-mini | Short motivational + progress updates | ~Rs 0.1 | 30 |
| **Gap analysis** | GPT-4o | Analytical, needs reasoning | ~Rs 2-3 | 2 |
| **Resume parsing** | GPT-4o-mini | Structured extraction, reliable | ~Rs 0.5 | 1 (one-time) |

### Cost Per Student Per Month

```
Active student using platform regularly:

One-time setup (first month):
  Personality assessment (5 calls × Rs 2.5)     = Rs 12.5
  Communication assessment (2 calls × Rs 0.5)   = Rs 1
  Resume parsing (1 call × Rs 0.5)              = Rs 0.5
  Gap analysis (2 calls × Rs 2.5)               = Rs 5
  Training plan (2 calls × Rs 4)                = Rs 8
  Subtotal:                                       Rs 27

Monthly recurring:
  Interview practice (4 sessions × Rs 20)        = Rs 80
  Aptitude tests (8 tests × Rs 5 for AI feedback)= Rs 40
  Daily feedback/nudges (30 × Rs 0.1)            = Rs 3
  Training plan adjustments (2 × Rs 4)           = Rs 8
  Communication re-assessment (2 × Rs 0.5)       = Rs 1
  Test generation (20 × Rs 0.3)                  = Rs 6
  Subtotal:                                       Rs 138

TOTAL MONTH 1: ~Rs 165/student
TOTAL MONTH 2+: ~Rs 138/student
```

**At Rs 1,000/student/year (B2B price), over ~6 months active use:**
- Revenue: Rs 1,000
- LLM cost: Rs 165 + (5 × Rs 138) = Rs 855
- **Gross margin: 14.5% — TOO THIN**

### Cost Optimization Strategies (CRITICAL for unit economics)

**1. Aggressive caching (saves 40-50%)**
- Cache company-specific questions, rubrics, persona prompts
- Cache training plan templates per profile archetype
- Cache common interview questions + model answers
- Cache test questions — generate once, serve to all students

**2. Batch processing (saves 20-30%)**
- Generate daily nudges for all students in one batch call (not individual)
- Batch test evaluation — score 10 tests in one call, not 10 separate calls
- Pre-generate weekly training content in one call per archetype

**3. Use GPT-4o-mini more aggressively (saves 30-40%)**
- Most feedback doesn't need GPT-4o. Mini with good prompts is 80% as good
- Interview orchestrator on mini, only interviewer responses on 4o
- Test scoring with structured rubrics on mini

**4. Template + fill approach (saves 20%)**
- Don't generate training plans from scratch — have 10-15 templates, AI fills in details
- Interview feedback has a structured template — AI fills dimensions, not free-form
- Test questions: 70% from curated bank, 30% AI-generated

**5. Consider Claude Haiku for simple tasks**
- Haiku is cheaper than GPT-4o-mini for simple classification/routing
- Use for: query routing, task classification, simple feedback generation

### Revised Cost After Optimization

```
Optimized monthly cost per active student:
  Interview practice (4 sessions × Rs 12)        = Rs 48
  Tests (8 tests × Rs 2 AI feedback)             = Rs 16
  Daily nudges (batched, Rs 1 total)              = Rs 1
  Plan adjustments (1 × Rs 3)                     = Rs 3
  Other (communication, misc)                     = Rs 5
  TOTAL: ~Rs 73/student/month

Over 6 months: Rs 73 × 6 = Rs 438
At Rs 1,000/student/year: 56% gross margin ✅
At Rs 1,500/student/year: 71% gross margin ✅
```

### LLM Provider Strategy

```
Primary:   AMD LLM Gateway (GPT-4o, GPT-4o-mini) — current access
Backup:    OpenAI direct API
Future:    Anthropic Claude (for evaluation tasks — more analytical)

For production scale, evaluate:
- DeepSeek V3 — very cheap, good for Hindi/Tamil content generation
- Llama 3.3 70B (self-hosted) — zero marginal cost for high-volume tasks
- Gemini 2.0 Flash — Google's fast model, competitive pricing, good for Indian languages

Self-hosting trigger: When monthly LLM spend crosses Rs 50,000
  → Host Llama 3.3 70B on a single A100 for Rs 30,000/month
  → Use for: test generation, daily feedback, simple scoring
  → Keep GPT-4o for: interviews, evaluation, personality assessment
```

---

## Technical Architecture (Detailed)

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js 14 + PWA)                    │
│                                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────┐ │
│  │  Student  │ │ Training │ │Interview │ │   Test   │ │  TPO  │ │
│  │  Profile  │ │   Plan   │ │ Practice │ │  Center  │ │ Dash  │ │
│  │  & Onboard│ │   View   │ │  (exist) │ │          │ │       │ │
│  └─────┬────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘ └───┬───┘ │
│        └──────────┬──┴──────────┬─┴────────────┴──────────┘     │
│                   │             │                                  │
│         ┌────────▼─────────────▼────────┐                        │
│         │   REST API + WebSocket Client  │                        │
│         │   Web Speech API (STT/TTS)     │                        │
│         └───────────────┬────────────────┘                        │
└─────────────────────────┼────────────────────────────────────────┘
                          │ HTTPS / WSS
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                 BACKEND (FastAPI + Python 3.11+)                  │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                    API GATEWAY                            │    │
│  │  Auth (JWT) │ Rate Limiting │ Request Routing             │    │
│  └──────────────────────┬───────────────────────────────────┘    │
│                          │                                        │
│  ┌───────────┬───────────┼───────────┬───────────────────┐      │
│  │           │           │           │                   │      │
│  ▼           ▼           ▼           ▼                   ▼      │
│ ┌─────┐  ┌──────┐  ┌──────────┐ ┌──────┐         ┌─────────┐  │
│ │Prof-│  │Train-│  │Interview │ │Test  │         │   TPO   │  │
│ │iling│  │ ing  │  │Orchestr- │ │Engine│         │Dashboard│  │
│ │Svc  │  │Plan  │  │ator     │ │      │         │  API    │  │
│ │     │  │Svc   │  │(existing)│ │      │         │         │  │
│ └──┬──┘  └──┬───┘  └────┬────┘ └──┬───┘         └────┬────┘  │
│    │        │           │         │                   │        │
│    └────────┴─────┬─────┴─────────┴───────────────────┘        │
│                   │                                              │
│  ┌────────────────▼──────────────────────────────────────────┐  │
│  │              MULTI-AGENT ENGINE (MiroFish-based)           │  │
│  │                                                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │  │
│  │  │Profiler  │ │Gap       │ │Training  │ │Evaluation    │ │  │
│  │  │Agents    │ │Analyzer  │ │Plan      │ │Synthesizer   │ │  │
│  │  │          │ │Agents    │ │Architect │ │Agent         │ │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────────┐  │  │
│  │  │Interview │ │GD        │ │Panel Orchestrator        │  │  │
│  │  │Panel     │ │Simulator │ │(existing)                │  │  │
│  │  │Agents    │ │Agents    │ │                          │  │  │
│  │  └──────────┘ └──────────┘ └──────────────────────────┘  │  │
│  └────────────────────┬──────────────────────────────────────┘  │
│                       │                                          │
│  ┌────────────────────▼──────────────────────────────────────┐  │
│  │                   LLM ROUTER                               │  │
│  │                                                            │  │
│  │  Task Classification → Model Selection → Call → Cache      │  │
│  │                                                            │  │
│  │  GPT-4o (quality)  │  GPT-4o-mini (fast)  │  Cache Layer  │  │
│  └────────────────────┬──────────────────────────────────────┘  │
│                       │                                          │
│  ┌────────────────────▼──────────────────────────────────────┐  │
│  │                   DATA LAYER                               │  │
│  │                                                            │  │
│  │  PostgreSQL (prod)     │  Redis (cache + sessions)         │  │
│  │  SQLite (dev)          │  S3/Local (resumes, files)        │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### Tech Stack (Final)

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Frontend** | Next.js 14 + TypeScript + Tailwind | Already built. PWA for mobile. |
| **Backend** | FastAPI (Python 3.10) | Already built. Async, WebSocket, fast. See "Current Status" for run command. |
| **Database (dev)** | SQLite + WAL mode | Already working. Zero setup. |
| **Database (prod)** | PostgreSQL (Supabase free tier) | Free tier = 500MB, enough for 1 college. |
| **Cache** | In-memory dict (dev) / Redis (prod) | LLM response caching. |
| **Auth** | Simple JWT (self-rolled) | Don't need NextAuth complexity for 1 college. |
| **File Storage** | Local filesystem (dev) / Supabase Storage (prod) | Resumes, voice recordings. |
| **LLM** | AMD Gateway → OpenAI API | Current access. Switch if needed. |
| **Hosting** | Single VPS (Hetzner/DigitalOcean India) | Rs 1,500-3,000/month. Enough for 500 students. |
| **Speech** | Web Speech API (browser-native) | Free. No server cost. Works on mobile Chrome. |
| **Payments** | Razorpay | Skip for pilot. College pays directly. |
| **Monitoring** | Sentry free tier + custom logging | Enough for pilot. |

### Why NOT Microservices

You're a solo builder. One FastAPI app, one database, one deployment. Split later when you have revenue and a team. Premature architecture is the #1 killer of solo projects.

```
DEPLOYMENT (Single Server):

VPS (4 vCPU, 8GB RAM, India region) — Rs 2,500/month

├── Nginx (reverse proxy + SSL)
├── FastAPI backend (uvicorn, 4 workers)
├── Next.js frontend (static export, served by Nginx)
├── PostgreSQL (or SQLite for first 3 months)
├── Redis (for caching, optional initially)
└── Certbot (free SSL)

Can handle: 500 concurrent users, 50 simultaneous interview sessions
Monthly cost: Rs 2,500 (server) + Rs 5,000-15,000 (LLM API) = Rs 7,500-17,500
```

---

## Go-to-Market Plan: The One College Pilot

### Step 1: Pick the College (Week 1)

**Ideal first college profile:**
- Private engineering college in Tamil Nadu (your network)
- 500-1,500 students
- Autonomous (not university-affiliated — faster decision-making)
- Poor to mediocre placement record (40-60% — they're desperate)
- TPO who is frustrated with current tools and open to technology
- Already uses SkillRack or similar (so students are used to platforms)

**Specific targets (examples):**
- Coimbatore: KGISL, Hindusthan, KPR, SNS, Rathinam, Nandha
- Chennai: SRM Easwari, Jeppiaar, Vel Tech, Sathyabama
- Trichy: Mookambigai, Saranathan, Kings
- Madurai: Sethu, Thiagarajar (if allowed)

**Approach:** Go through personal network. Find ONE TPO who will champion you. Don't cold-email 50 colleges.

### Step 2: The Pitch (Week 1-2)

**Don't pitch a product. Pitch a pilot.**

```
"I'll work with your 2026 batch CSE students for FREE for 3 months.
I bring an AI platform that:
  1. Profiles each student (personality, skills, gaps)
  2. Creates personalized training plans
  3. Runs AI mock interviews (panel format, like real ones)
  4. Tracks progress weekly

You get: A dashboard showing every student's readiness.
I get: Data, feedback, and a case study.

If placements improve, we discuss pricing for next batch.
No risk for you. No cost. Just try it."
```

**What you need from them:**
- Access to final-year CSE students (50-100 is enough to start)
- Student data: names, CGPA, resumes (they have this)
- 1 hour/week from TPO for feedback
- Permission to deploy the platform (just a web URL)
- Placement results at end of season (to measure impact)

### Step 3: Onboard Students (Week 3-4)

**Onboarding flow (10-15 minutes per student):**
1. Student logs in (simple email/password, no OTP needed for pilot)
2. Uploads resume (or types basic info if no resume)
3. Enters academic details (CGPA, 10th/12th marks)
4. Takes AI personality assessment (5-min conversational)
5. Records 1-min spoken English sample
6. Selects target companies (from list: TCS, Infosys, etc.)
7. Gets: Profile Card + Gap Report + 12-week Training Plan

**Critical: Make this a guided session.**
Don't just send a link. Go to the college, set up in a lab, onboard 50 students in one day with a volunteer/TPO helping. First impression matters.

### Step 4: Run the Pilot (3 Months)

**Month 1: Assessment + Training Plan**
- All students profiled and have training plans
- Students complete daily tasks (DSA, aptitude, communication)
- Weekly aptitude test (AI-generated, company-specific pattern)
- You track engagement metrics daily
- TPO gets weekly dashboard update

**Month 2: Practice + Interview Prep**
- Students start mock interviews (AI panel, 1x/week)
- GD practice sessions (AI-powered, 2x/week for MBA-seeking students)
- Company-specific mock tests (full TCS NQT simulation, etc.)
- Identify at-risk students (low engagement, low scores) — TPO nudges them
- You iterate on the product based on feedback

**Month 3: Intensive Prep + Placement Season**
- Daily mock tests
- 2-3 full panel interview simulations per student
- Final readiness report for each student
- TPO uses dashboard to recommend students for specific drives
- Track actual placement outcomes

### Step 5: Measure & Prove (End of Pilot)

**Success metrics to track:**
- Placement rate improvement (vs previous year's batch)
- Average score improvement (aptitude, coding, communication)
- Student engagement (% completing daily tasks)
- Student satisfaction (simple 1-5 rating)
- TPO satisfaction (would they pay?)
- Number of interview sessions completed
- Specific student success stories (X was at 35% employability, reached 75%, got placed at TCS)

**This data IS your sales deck for the next 10 colleges.**

### Step 6: Convert to Paid (Month 4+)

**Pricing for college B2B:**
```
Pilot proved results → Now charge:

BASIC: Rs 500/student/year
  - Profile + Gap Analysis
  - Training Plan (non-adaptive)
  - 2 mock interviews/month
  - Monthly test
  - Basic TPO dashboard

PRO: Rs 1,000/student/year
  - Everything in Basic +
  - Adaptive training plans
  - 8 mock interviews/month (panel + GD)
  - Company-specific prep (top 10 companies)
  - Weekly tests
  - Full TPO analytics dashboard

PREMIUM: Rs 1,500/student/year
  - Everything in Pro +
  - Unlimited interviews
  - All company modules
  - Communication coaching
  - Priority support
  - Placement prediction model

For a 1,000-student college:
  Basic: Rs 5 lakh/year
  Pro: Rs 10 lakh/year
  Premium: Rs 15 lakh/year
```

**First revenue target: 5 colleges × Rs 5-10 lakh = Rs 25-50 lakh ARR**

---

## Solo Builder Execution Plan

### Current Status (Audited 2026-03-30)

```
CODEBASE: 57 Python files, ~32,000 lines backend + ~4,000 lines frontend
RUNTIME: Python 3.10 (/tool/pandora/bin/python3.10), vendored deps in .pip_libs/
SERVER: PYTHONPATH=.pip_libs /tool/pandora/bin/python3.10 -m uvicorn api:app --port 8002 --host 0.0.0.0
FRONTEND: cd frontend && npm run dev (Next.js 14.2.15, port 3000)
DATABASES: career_arena.db (22 tables, 77 DB methods) + knowledge.db (8 tables)
```

**Backend Files (status per file):**

```
INTERVIEW ENGINE (Module 5):
  ✅ screening_agent.py    (1,409 lines) — Kavitha, 5-phase state machine, complete & tested
  ✅ panel_generator.py    (294 lines)   — LLM-customized panel from CandidateProfile, complete
  ✅ evaluation_engine.py  (263 lines)   — 23-dimension scoring, per-panelist, complete
  ✅ candidate_model.py    (275 lines)   — Real-time candidate assessment, complete
  ✅ panel_orchestrator.py (472 lines)   — Turn-taking + response generation, complete
  ✅ interview_runner.py   (424 lines)   — Single-session interview lifecycle, complete
  🔨 round_manager.py     (808 lines)   — Multi-round orchestrator, 70% — gaps in observer reactions, Kavitha transition, model persistence
  🔨 interviewer_engine.py (993 lines)  — Phase machine + question bank, 60% — wiring to RoundManager unclear
  🔨 interview_forum.py   (413 lines)   — Hidden inter-interviewer forum, 60% — full integration unclear
  ⚠️ interviewer_swarm.py (781 lines)   — 8-10 debate agents per interviewer, complete but NOT WIRED

CAREER INTELLIGENCE (legacy system, fully working but separate from interview flow):
  ✅ orchestrator.py       (338 lines)   — 3-tier agent pipeline
  ✅ query_router.py       (326 lines)   — 9 query types
  ✅ context_builder.py    (233 lines)   — Resume + query context
  ✅ agent_factory.py      (373 lines)   — 3-tier agent roster
  ✅ profile_generator.py  (518 lines)   — Knowledge graph → agent profiles
  ✅ graph_builder.py      (354 lines)   — Resume → knowledge graph
  ✅ config_generator.py   (234 lines)   — Simulation config
  ✅ simulation.py         (1,167 lines) — MiroFish-aligned forum simulation
  ✅ arena.py              (164 lines)   — Reddit-style forum
  ✅ report_synthesizer.py (303 lines)   — Report generation
  ✅ report_agent.py       (281 lines)   — Detailed report agent

INFRASTRUCTURE:
  ✅ api.py                (922 lines)   — 27 REST endpoints + 2 WebSocket endpoints
  ✅ database.py           (1,521 lines) — 22 tables, 77 methods, WAL mode
  ✅ knowledge_db.py       (1,466 lines) — 8 tables, auto-seeds on first run
  ✅ llm_client.py         (283 lines)   — OpenAI (AMD Gateway) + Anthropic support
  ✅ models.py             (132 lines)   — Pydantic request/response models
  ✅ interviewer_personas.py (466 lines) — Persona dataclass + panel presets
  ✅ main.py               (261 lines)   — CLI entry point
  ✅ seed_knowledge.py     (372 lines)   — Seeds knowledge DB from seed_data/

SEED DATA (all complete, data-only files — 2,729 questions, 105 companies, 55 personas, 39 rubrics, 50 context):
  ✅ seed_data/companies.py              (1,981 lines) — 105 company profiles (IT Services, Product, GCC, Consulting)
  ✅ seed_data/personas.py               (1,537 lines) — 55 interviewer personas across domains × levels
  ✅ seed_data/rubrics.py                (1,860 lines) — 39 evaluation rubrics (13 dimensions × 3 levels)
  ✅ seed_data/questions_behavioral.py   (615 lines)   — 560 behavioral/HR questions
  ✅ seed_data/questions_dsa.py          (694 lines)   — 349 DSA questions (arrays, trees, graphs, DP, etc.)
  ✅ seed_data/questions_dbms.py         (1,363 lines) — 520 DBMS/SQL questions
  ✅ seed_data/questions_data_science.py (1,650 lines) — 300 data science/ML questions
  ✅ seed_data/questions_oop.py          (609 lines)   — 186 OOP/design pattern questions
  ✅ seed_data/questions_os_networks.py  (538 lines)   — 152 OS + networking questions
  ✅ seed_data/questions_web.py          (426 lines)   — 136 web dev questions (JS, React, Node, REST)
  ✅ seed_data/questions_system_design.py (359 lines)  — 136 system design questions
  ✅ seed_data/questions_aptitude_quant.py  (new)      — 134 quantitative aptitude questions
  ✅ seed_data/questions_aptitude_verbal.py (new)      — 164 verbal aptitude questions
  ✅ seed_data/questions_aptitude_logical.py (new)     — 98 logical reasoning questions
  ✅ seed_data/round_blueprints.py       (1,298 lines) — 202 round blueprints (119 company + 83 default)
  ✅ seed_data/hiring_tracks.py          (242 lines)   — 30 company hiring track pipelines
  ✅ seed_data/indian_context.py         (1,628 lines) — 50 Indian context entries (7 categories)
  ✅ seed_data/question_augmenter.py     (137 lines)   — LLM-based question generation (optional Phase 3)
  ✅ seed_data/company_enricher.py       (96 lines)    — Web search company enrichment (optional Phase 2)

TOOLS (all complete):
  ✅ tools/resume_parser.py     (223 lines) — LLM-based resume parsing
  ✅ tools/web_search.py        (199 lines) — Web search integration
  ✅ tools/company_data.py      (127 lines) — Company data fetcher
  ✅ tools/interview_patterns.py (125 lines) — Interview pattern scraper
  ✅ tools/salary_scraper.py    (120 lines) — Salary data fetcher
  ✅ tools/news_search.py       (120 lines) — News search
  ✅ tools/stock_data.py        (78 lines)  — Stock data fetcher
  ✅ tools/base.py              (51 lines)  — Base tool class
```

**Knowledge DB Seed Data (seeded via `python seed_knowledge.py`):**
```
  2,729 unique interview questions across 11 domains:
    ├── questions_dsa.py             — 349 questions (arrays, trees, graphs, DP, linked lists, stacks, sorting, heaps, hashing, recursion)
    ├── questions_behavioral.py      — 560 questions (self-intro, strengths/weaknesses, STAR, teamwork, leadership)
    ├── questions_dbms.py            — 520 questions (SQL, normalization, transactions, indexing, joins, triggers)
    ├── questions_data_science.py    — 300 questions (statistics, ML, regression, classification, NLP, deep learning)
    ├── questions_oop.py             — 186 questions (4 pillars, SOLID, design patterns, Java/Python OOP, UML)
    ├── questions_aptitude_verbal.py — 164 questions (grammar, vocabulary, reading comprehension, para jumbles, idioms)
    ├── questions_os_networks.py     — 152 questions (process mgmt, memory, TCP/IP, OSI, HTTP, sockets)
    ├── questions_web.py             — 136 questions (HTML/CSS, JavaScript, React, Node, REST, security, DevOps)
    ├── questions_system_design.py   — 136 questions (URL shortener, chat systems, caching, microservices, LLD)
    ├── questions_aptitude_quant.py  — 134 questions (time/speed, percentages, P&C, probability, DI, algebra)
    └── questions_aptitude_logical.py — 98 questions (coding-decoding, blood relations, seating, syllogisms, puzzles)
  105 company profiles (IT Services, Product/Tech, GCCs, Banking, Consulting)
  55 interviewer personas (SE, DS, Consulting, UPSC, Banking × fresher/mid/senior)
  39 evaluation rubrics (13 dimensions × 3 levels, 5 score bands each)
  50 Indian context entries (campus placement, interview culture, salary negotiation, regional context)
  30 hiring tracks (company-specific selection pipelines)
  202 round blueprints (119 company-specific + 83 default templates)

Seed CLI:
  python seed_knowledge.py                        # Full run (~0.2s for curated data)
  python seed_knowledge.py --dry-run              # Count items, don't write
  python seed_knowledge.py --skip-questions        # Skip questions, seed everything else
  python seed_knowledge.py --only questions        # Seed only questions
  python seed_knowledge.py --no-wipe              # Append without wiping existing data
  python seed_knowledge.py --db-path /path/to.db  # Custom database path
```

**Question format standard (every question includes):**
```python
{
    "domain": "software_engineering",     # or "aptitude", "behavioral"
    "topic": "arrays",                    # specific topic
    "difficulty": "medium",               # easy / medium / hard
    "level": "mid",                       # fresher / mid / senior
    "question_text": "Walk me through...",# Natural interviewer phrasing, not textbook
    "follow_ups": ["What if...", ...],    # 2-3 probing questions
    "expected_points": ["point1", ...],   # 3-5 key answer points
    "scoring_rubric": "...",              # 5-band rubric (1=poor to 5=excellent)
    "company_specific": "TCS",            # or "" for general
    "tags": ["arrays", "dsa"]            # for filtering and retrieval
}
```

**Frontend (all pages complete and functional):**
```
  ✅ /                           — Landing page with demo animation, features, testimonials
  ✅ /screening                  — Name + resume upload form
  ✅ /screening/[id]             — Chat with Kavitha (coverage tracker, TTS)
  ✅ /interview                  — 3-step wizard (preset, role/company, difficulty)
  ✅ /interview/[id]             — Live panel interview (single-session, legacy)
  ✅ /interview/[id]/panel       — Panel reveal animation
  ✅ /interview/[id]/round/[n]   — Individual round 1-on-1 interview
  ✅ /interview/[id]/forum       — Behind-the-scenes forum reveal (progressive animation)
  ✅ /interview/[id]/results     — Scorecard (score ring, dimension bars, panelist feedback, action items)
  ✅ /history                    — Past sessions list
  ✅ /session/[id]               — Legacy career intelligence viewer
  15 reusable components, 1 custom hook (useTTS), 540-line typed API client
```

**API Endpoints (27 REST + 2 WebSocket):**
```
  Screening:     POST start, POST answer, POST complete, GET status
  Multi-round:   POST multi/start, POST round/start, POST round/answer, POST round/end
  Interview:     POST start, POST answer, POST end, GET state, GET transcript
  Evaluation:    POST evaluate, GET evaluation
  Forum:         GET forum, GET rounds
  Knowledge:     GET stats, GET companies
  Career query:  POST query, GET session, GET arena, GET logs, GET sessions
  WebSocket:     /ws/{id} (career), /ws/interview/{id} (interview)
```

**What's NOT built (Modules 1-4, 6):**
```
  ❌ Student Profiler (Module 1) — No students table, no onboarding, no personality assessment
  ❌ Skills Gap Analyzer (Module 2) — No gap analysis agent, no skill comparison
  ❌ Training Plan Generator (Module 3) — No training_plans table, no daily tasks
  ❌ Company-Specific Prep (Module 4) — No mock test engine, no TCS NQT/Infosys InfyTQ simulation
  ❌ Test & Evaluation Engine (Module 6) — No aptitude MCQ engine, no coding tests, no progress tracking
  ❌ TPO Dashboard — No batch analytics, no student progress view
  ❌ Auth system — No JWT, no login/signup
```

### Build Priority: INTERVIEW AGENT FIRST

Complete the interview practice engine (Module 5) to production quality before touching anything else.
This is the differentiator. No competitor has multi-agent panel interviews with hidden forum.

### Phase 1: Complete Interview Agent (Current Focus)

```
STEP 1: Fix Integration Gaps (Critical)
  ├── Gap 1: Verify InterviewerEngine ↔ RoundManager wiring
  │   File: round_manager.py — _generate_question() must call InterviewerEngine
  │   File: interviewer_engine.py — generate_question() must work with round context
  │
  ├── Gap 2: Implement _run_live_observers() in RoundManager
  │   File: round_manager.py — After each answer, non-active interviewers react
  │   This creates the "live forum" feel during the round
  │
  ├── Gap 3: Implement Kavitha transition summary
  │   File: round_manager.py — end_round() posts Kavitha's briefing for next interviewer
  │   "Kavitha whispers to next interviewer: here's what happened..."
  │
  └── Gap 4: Persist CandidateModel to DB
      File: round_manager.py — Save model checkpoint after each answer
      File: database.py — Add candidate_model_snapshots table or JSON column
      Risk: Process crash mid-interview loses all accumulated insights

STEP 2: Wire or Remove InterviewerSwarm (Decision Required)
  Option A: WIRE IT — RoundManager calls swarm instead of single-LLM question generation
    Pro: Richer questions, multi-perspective debate, unique differentiator
    Con: 8-10x more LLM calls per question, slower response time
  Option B: REMOVE IT — Delete interviewer_swarm.py, use InterviewerEngine only
    Pro: Simpler, faster, cheaper
    Con: Lose the "debate agent" sophistication
  Option C: HYBRID — Swarm for final round only, Engine for earlier rounds
    Pro: Best of both, cost-effective
    Recommended: Option C

STEP 3: Harden Forum Integration
  ├── Verify forum posts persist and survive session end
  ├── Test get_full_forum() returns posts organized by round
  ├── Test forum reveal page displays all posts with replies
  ├── Add forum summary generation (key themes across all rounds)
  └── Files: interview_forum.py, database.py, api.py

STEP 4: Company-Specific Interviewer Personas
  ├── Seed 10 company-specific interviewer templates into KnowledgeDB
  │   TCS, Infosys, Wipro, Cognizant, Accenture, HCL, Tech Mahindra,
  │   Capgemini, LTIMindtree, Zoho — each with distinct interview style
  ├── Panel generator picks company-style personas when company is specified
  └── Files: knowledge_db.py, panel_generator.py

STEP 5: End-to-End Testing + Frontend Polish
  ├── Run full flow: screening → panel → 3 rounds → forum → scorecard
  ├── Test with different company targets (TCS vs Zoho = very different)
  ├── Test edge cases: short answers, evasion, strong candidate, weak candidate
  ├── Polish scorecard UI: per-panelist breakdown, radar chart, action items
  ├── Polish forum reveal: progressive reveal animation, sentiment colors
  └── Fix any bugs found during testing
```

### Phase 2: Student Profiling + Gap Analysis (AFTER Phase 1)

```
  ├── Database schema (students, assessments, skill_assessments)
  ├── Student onboarding API + frontend
  ├── Resume parsing → structured profile
  ├── AI personality assessment (conversational OCEAN)
  ├── Skills gap analyzer (profile vs company requirements)
  ├── Gap report generation
  └── Connect screening output to student profile
```

### Phase 3: Training Plans + Testing (AFTER Phase 2)

```
  ├── Training plan generator agent
  ├── Daily task tracking
  ├── Aptitude test MCQ engine
  ├── Company-specific mock tests (TCS NQT, Infosys InfyTQ)
  ├── Test scoring + AI feedback
  └── Progress tracking dashboard
```

### Phase 4: TPO Dashboard + Deploy (AFTER Phase 3)

```
  ├── Auth system (JWT)
  ├── TPO dashboard (batch overview, readiness scores)
  ├── Student dashboard (progress, scores over time)
  ├── Deploy to VPS
  └── College onboarding prep
```

### What to SKIP for Pilot (add later)

- Mobile app (use responsive web)
- Razorpay/payments (college pays directly)
- Voice/STT for interviews (text-only for MVP)
- GD mode beyond basic MVP
- Coding test auto-grading (use simple test cases)
- Vernacular/Tamil (English first)
- Redis caching (in-memory dict fine for 500 students)
- PostgreSQL (SQLite fine for pilot)

---

## Hiring Plan

### Don't Hire Until You Have

1. **One college pilot running** (product-market fit signal)
2. **At least Rs 2-3 lakh MRR** (or clear commitment from 3+ colleges)
3. **Clear bottleneck** that isn't solvable by working harder alone

### Hiring Timeline

```
STAGE 0: Solo (Now → Month 6)
  You do everything. Product, code, sales, support.
  Monthly burn: Rs 20,000-30,000 (server + LLM API + misc)

STAGE 1: First Hire (Month 6-9, after 3+ paying colleges)
  HIRE: Full-stack Developer (Junior, Rs 25-35K/month)
  Why: You need to focus on sales + product decisions.
        Junior dev handles: bug fixes, frontend polish, test content creation.
  Where: Freelancer from college network, or Internshala/LinkedIn.
  Type: Part-time or contract first. Full-time only if revenue supports it.

STAGE 2: Sales + Content (Month 9-12, after 5+ colleges, Rs 5L+ MRR)
  HIRE: Campus Sales + Ops Person (Rs 20-30K/month)
  Why: B2B college sales is relationship-heavy. You can't code AND visit 20 colleges.
        This person: visits colleges, onboards students, handles TPO relationships.
  Profile: Recent MBA grad or experienced placement coordinator.
           Someone who has BEEN a TPO or worked in campus recruitment.

  HIRE: Content Creator (Part-time, Rs 10-15K/month)
  Why: Need aptitude questions, GD topics, company-specific content at scale.
        Also: LinkedIn/YouTube content for marketing.
  Profile: Someone who cracked placement exams recently (2024-25 batch).

STAGE 3: Scale (Month 12-18, after 15+ colleges, Rs 15L+ MRR)
  HIRE: Senior Backend Engineer (Rs 60-80K/month)
  Why: Need to handle scale (1000s of students), optimize infra, build ML models.

  HIRE: AI/ML Engineer (Rs 50-70K/month)
  Why: Placement prediction model, advanced evaluation, fine-tuning prompts at scale.

  HIRE: 2 more Campus Sales reps (Rs 20-30K each)
  Why: Each rep can handle 10-15 colleges. Need geographic coverage.

STAGE 4: Series A territory (Month 18+, 50+ colleges, Rs 50L+ MRR)
  Build a real team: CTO, VP Sales, Product Manager, etc.
  But that's a problem for future you.
```

### Who NOT to Hire Early

- **No co-founder** unless they bring distribution (college network) or deep AI expertise AND are willing to work for equity
- **No marketing agency** — your marketing is product results + word of mouth between TPOs
- **No data scientist** — GPT-4o IS your data scientist for now
- **No devops** — one server, Nginx, done
- **No customer support** — you + WhatsApp group for the pilot

---

## Key Metrics to Track

### Student Metrics
- Employability score improvement (pre vs post)
- Training plan completion rate (% daily tasks done)
- Test score trends (week over week)
- Interview score trends (session over session)
- Placement outcome (placed / not placed / opted out)

### Platform Metrics
- DAU / WAU / MAU (student engagement)
- Sessions per student per week
- Average time on platform per session
- Feature usage distribution (which modules used most)
- LLM cost per student per month

### Business Metrics
- Number of colleges onboarded
- Students per college (penetration)
- Revenue per college
- College retention (renew next year?)
- NPS score (students + TPOs)
- CAC per college (time + travel + demo cost)

---

## Competitive Moat — What We Build That's Hard to Copy

1. **Multi-agent interview panel** — Orchestration logic is complex. 12K+ lines of agent code already written.
2. **Longitudinal student data** — 6 months of assessment data per student creates a flywheel. Better data → better AI → better outcomes → more colleges.
3. **Company-specific simulation fidelity** — Each company module is hand-curated + AI-enhanced. Takes time to build, easy to maintain.
4. **TPO relationships** — B2B education sales are sticky. Once a TPO champions you, competitors can't get in.
5. **Placement outcome data** — If we prove placement rate improvement with data, that IS the moat. No competitor can claim outcomes they don't have.

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| LLM costs blow up | Medium | High | Aggressive caching, model tiering, self-host fallback |
| College says no to pilot | Medium | Medium | Have 3-4 backup colleges. Offer is zero-risk for them. |
| Students don't engage | High | High | Gamification, TPO enforcement, WhatsApp nudges, peer competition |
| Naan Mudhalvan displaces us | Low | High | We complement NM (they do content, we do AI practice). Position as "NM + PlaceRight together." |
| AI quality disappoints | Medium | High | Start text-only. Manage expectations. Show improvement data, not perfection. |
| Solo builder burnout | High | Critical | Ship MVP, not perfection. 10-week plan is aggressive but finite. |
| IT hiring freeze continues | Medium | Medium | Expand beyond IT — cover GCC roles, non-tech roles (BPO, KPO). |

---

## Development Guidelines

### Code Principles
- **Reuse existing CareerArena code.** Don't rebuild what works.
- **One FastAPI app, one database.** No microservices. No over-engineering.
- **JSONB for flexible AI output.** Don't over-normalize what AI generates.
- **Stream everything.** Interview responses, test feedback, profile generation — all streamed via WebSocket.
- **Mobile-first responsive.** Most Tier 3 students access on phone.
- **Prompt engineering > model upgrades.** Spend time on prompts, not infra.

### Agent Design Principles
- Each agent has a clear, single responsibility
- Agents share context through the student profile (the source of truth)
- Panel orchestrator decides turn order (agents don't self-select)
- Evaluation agents score independently, then consensus
- All agent outputs stored for debugging and improvement

### Data Principles
- Student data is sacred — encrypt PII, backup daily
- Every AI interaction logged (for prompt improvement)
- Placement outcomes linked to training data (prove causation)
- TPO never sees raw AI conversation — only structured reports
- DPDP Act compliance from Day 1

### Performance Targets
- Page load: < 2 seconds
- Interview first response: < 2 seconds (streamed)
- Test submission → result: < 5 seconds
- Profile generation: < 30 seconds (after onboarding)
- Training plan generation: < 60 seconds
- TPO dashboard load: < 3 seconds
- Concurrent users: 100 (enough for 1 college)
