# CareerArena — AI-Powered Placement Platform for Indian Colleges

An end-to-end AI placement outcome platform that takes a Tier 3 college student from "unemployable" to "placed" — powered by multi-agent AI.

Built for the Indian campus placement ecosystem. One platform covers the full lifecycle: student profiling, skills gap analysis, personalized training, company-specific preparation, multi-agent interview practice, and placement analytics.

## What Makes This Different

- **Multi-Agent Panel Interviews** — 2-4 AI interviewers conduct realistic panel interviews with a hidden deliberation forum. No competitor has this.
- **Company-Specific Simulation** — Trains students for the exact format TCS NQT, Infosys InfyTQ, Wipro NLTH, Zoho, and 100+ other companies use.
- **Full Lifecycle** — Not fragments. One platform from Day 1 of final year to offer letter.
- **Built for Tier 3 Economics** — Rs 500-1,500/student/year. Mobile-first.

## Architecture

```
Frontend (Next.js 14 + TypeScript + Tailwind)
    │
    ▼  REST API + WebSocket
Backend (FastAPI + Python 3.10)
    │
    ├── Multi-Agent Interview Engine
    │   ├── Screening Agent (Kavitha) — 5-phase conversational screening
    │   ├── Panel Generator — LLM-customized interviewer panels
    │   ├── Round Manager — Multi-round orchestration
    │   ├── Interviewer Engine — Phase-machine question generation
    │   ├── Interviewer Swarm — 8-10 debate agents for final round
    │   ├── Interview Forum — Hidden inter-interviewer deliberation
    │   ├── Candidate Model — Real-time candidate assessment
    │   └── Evaluation Engine — 23-dimension scoring + skill gap reports
    │
    ├── Career Intelligence Engine
    │   ├── 3-Tier Agent Pipeline (orchestrator → agents → tools)
    │   ├── Reddit-style visible arena (agents debate your career)
    │   └── Report Synthesizer
    │
    ├── Knowledge Database
    │   ├── 2,729 interview questions across 11 domains
    │   ├── 105 company profiles
    │   ├── 55 interviewer personas
    │   ├── 39 evaluation rubrics
    │   ├── 202 round blueprints
    │   └── 50 Indian context entries
    │
    └── SQLite (dev) / PostgreSQL (prod)
```

## Interview Flow

```
Student → Screening (chat with Kavitha)
  → Panel Reveal (animated interviewer introductions)
    → Round 1: 1-on-1 with Interviewer A (InterviewerEngine)
    → Round 2: 1-on-1 with Interviewer B (InterviewerEngine)
    → Final Round: 1-on-1 with Interviewer C (InterviewerSwarm — 8 debate agents)
      → Forum Reveal (behind-the-scenes deliberation)
        → Scorecard (23-dimension evaluation + skill gap report)
```

Between rounds, non-active interviewers post observations in a hidden forum. The candidate gets to see this "behind the scenes" discussion after the interview.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Framer Motion |
| Backend | FastAPI, Python 3.10, uvicorn |
| Database | SQLite (WAL mode) — 22 tables, 77 DB methods |
| LLM | OpenAI GPT-4o / GPT-4o-mini via AMD Gateway |
| Real-time | WebSocket for streaming interview responses |

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key (or AMD LLM Gateway access)

### Backend

```bash
cd career_arena

# Install dependencies
pip install -r requirements.txt

# Seed the knowledge database
python seed_knowledge.py

# Start the server
python -m uvicorn api:app --port 8002 --host 0.0.0.0
```

### Frontend

```bash
cd career_arena/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The frontend runs on `http://localhost:3000`, backend API on `http://localhost:8002`.

### Environment Variables

Create a `.env` file in the `career_arena/` directory:

```env
OPENAI_API_KEY=your_api_key_here
# Or for AMD Gateway:
# LLM_BASE_URL=https://your-gateway-url
# LLM_API_KEY=your_gateway_key
```

## API Endpoints

### Screening
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/screening/start` | Start screening session |
| POST | `/api/screening/answer` | Submit answer to Kavitha |
| POST | `/api/screening/complete` | Complete screening |
| GET | `/api/screening/status/{id}` | Get screening status |

### Multi-Round Interview
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/interview/multi/start` | Start multi-round interview |
| POST | `/api/interview/round/start` | Start a round |
| POST | `/api/interview/round/answer` | Submit answer in round |
| POST | `/api/interview/round/end` | End current round |

### Evaluation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/interview/{id}/evaluate` | Trigger evaluation |
| GET | `/api/interview/{id}/evaluation` | Get evaluation results |
| GET | `/api/interview/{id}/skill-gap` | Get skill gap report |

### Forum & Results
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/interview/{id}/forum` | Get forum deliberation |
| GET | `/api/interview/{id}/rounds` | Get round details |

### WebSocket
| Endpoint | Description |
|----------|-------------|
| `/ws/{id}` | Career intelligence streaming |
| `/ws/interview/{id}` | Interview response streaming |

## Frontend Pages

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/screening` | Start screening (name + resume) |
| `/screening/[id]` | Chat with Kavitha |
| `/interview` | Interview setup wizard |
| `/interview/[id]/panel` | Panel reveal animation |
| `/interview/[id]/round/[n]` | Live interview round |
| `/interview/[id]/forum` | Behind-the-scenes forum reveal |
| `/interview/[id]/results` | Scorecard + skill gap report |
| `/history` | Past sessions |

## Knowledge Database

Seeded with curated data covering the Indian campus placement ecosystem:

- **11 question domains**: DSA, DBMS, OOP, OS/Networks, Web Dev, System Design, Data Science, Behavioral, Quantitative Aptitude, Verbal Aptitude, Logical Reasoning
- **105 companies**: IT Services (TCS, Infosys, Wipro), Product (Google, Amazon, Flipkart), GCCs, Banking, Consulting
- **55 interviewer personas**: Software Engineering, Data Science, Consulting, UPSC, Banking across fresher/mid/senior levels
- **202 round blueprints**: 119 company-specific + 83 default templates

```bash
# Seed commands
python seed_knowledge.py                  # Full seed
python seed_knowledge.py --dry-run        # Preview counts
python seed_knowledge.py --only questions # Seed only questions
```

## Project Status

### Built (Module 5: Interview Practice)
- Screening agent with 5-phase state machine
- Multi-round panel interviews with company-specific personas
- Hybrid engine: InterviewerEngine for early rounds, InterviewerSwarm (8-10 debate agents) for final round
- Hidden inter-interviewer forum with live observations
- 23-dimension evaluation with per-panelist scoring
- Skill gap report generation
- Full frontend with animations and real-time streaming

### Planned
- Module 1: Student Profiler (resume parsing, personality assessment, communication scoring)
- Module 2: Skills Gap Analyzer (profile vs company requirements)
- Module 3: Training Plan Generator (adaptive week-by-week plans)
- Module 4: Company-Specific Prep (TCS NQT, Infosys InfyTQ mock tests)
- Module 6: Test & Evaluation Engine (aptitude, coding, progress tracking)
- TPO Dashboard (batch analytics, placement drive management)
- Auth system (JWT)

## Target Market

- **Primary**: Tier 3 engineering colleges in Tamil Nadu / South India
- **Pricing**: Rs 500-1,500/student/year (B2B to colleges)
- **GTM**: Free 3-month pilot with one college, prove placement rate improvement, then convert to paid

## License

Proprietary. All rights reserved.
