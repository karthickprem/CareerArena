"""
CareerArena FastAPI Backend.

Endpoints:
  POST /api/query          — Submit a career query
  GET  /api/session/{id}   — Get session status + report
  GET  /api/session/{id}/arena — Get arena posts + comments
  GET  /api/sessions       — List recent sessions for a user
  WS   /ws/{session_id}    — Real-time streaming during analysis
"""

from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import CareerDB
from llm_client import LLMClient
from orchestrator import Orchestrator
from report_synthesizer import ReportSynthesizer
from query_router import route_query
from agent_factory import AgentFactory
from context_builder import ContextBuilder
from arena import Arena
from models import (
    QueryRequest, QueryResponse, SessionStatus, SessionListItem,
    ArenaPost, ArenaComment, AgentInfo, Report, ReportSection, WSMessage,
)

app = FastAPI(
    title="CareerArena API",
    description="Multi-Agent Career Intelligence Engine",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = CareerDB("career_arena.db")

try:
    from llm_client import LLMConfig
    config = LLMConfig.from_env()
    llm = LLMClient(config)
except Exception as e:
    print(f"[WARNING] LLM init failed: {e}", flush=True)
    llm = None

active_websockets: Dict[str, List[WebSocket]] = {}
running_sessions: Dict[str, dict] = {}


def get_orchestrator(session_id: str = ""):
    def ws_status(msg: str):
        running_sessions.setdefault(session_id, {}).setdefault("logs", []).append(
            {"time": time.time(), "msg": msg}
        )
        asyncio.get_event_loop().call_soon_threadsafe(
            _broadcast_sync, session_id, "status", {"message": msg}
        )

    return Orchestrator(llm=llm, db=db, on_status=ws_status if session_id else None)


def _broadcast_sync(session_id: str, msg_type: str, data: dict):
    """Schedule broadcast to websockets from sync context."""
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(_broadcast(session_id, msg_type, data))


async def _broadcast(session_id: str, msg_type: str, data: dict):
    if session_id not in active_websockets:
        return
    msg = json.dumps({
        "type": msg_type,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    })
    dead = []
    for ws in active_websockets[session_id]:
        try:
            await ws.send_text(msg)
        except Exception:
            dead.append(ws)
    for ws in dead:
        active_websockets[session_id].remove(ws)


# =========================================================
# REST Endpoints
# =========================================================

@app.post("/api/query", response_model=QueryResponse)
async def submit_query(
    query: str = Form(...),
    user_id: Optional[str] = Form(None),
    resume: Optional[UploadFile] = File(None),
):
    """Submit a career intelligence query."""
    resume_text = None
    if resume:
        content = await resume.read()
        resume_text = content.decode("utf-8", errors="ignore")

    effective_user = user_id or f"anon_{uuid.uuid4().hex[:8]}"

    routed = route_query(query)
    ctx_builder = ContextBuilder(db)

    resume_data = None
    if resume_text:
        from tools.resume_parser import ResumeParserTool
        parser = ResumeParserTool()
        result = parser.execute(raw_text=resume_text)
        if result.success:
            try:
                resume_data = json.loads(result.data) if isinstance(result.data, str) else result.data
            except (json.JSONDecodeError, TypeError):
                resume_data = {"raw_text": resume_text[:5000]}

    ctx = ctx_builder.build(routed, user_id=effective_user, resume_data=resume_data)
    session_id = ctx.session_id

    running_sessions[session_id] = {
        "status": "running",
        "query": query,
        "query_type": routed.query_type.value,
        "companies": routed.companies,
        "started_at": time.time(),
        "logs": [],
    }

    asyncio.get_event_loop().run_in_executor(
        None, _run_pipeline, session_id, query, effective_user, resume_data
    )

    return QueryResponse(
        session_id=session_id,
        status="running",
        message=f"Analysis started. {len(routed.fixed_agents)} agents activated for {routed.query_type.value}.",
    )


def _run_pipeline(session_id: str, query: str, user_id: str, resume_data: dict = None):
    """Run the full 3-tier orchestrator pipeline in a background thread."""
    import traceback
    try:
        _log_status(session_id, "Pipeline starting...")
        orch = Orchestrator(llm=llm, db=db, on_status=lambda msg: _log_status(session_id, msg))
        result = orch.run(query=query, user_id=user_id, resume_data=resume_data, session_id=session_id)

        report = result.get("report")
        if not report or not report.get("sections"):
            _log_status(session_id, "Generating report via synthesizer...")
            synthesizer = ReportSynthesizer(llm=llm)
            report = synthesizer.generate(result)

        running_sessions[session_id]["status"] = "completed"
        running_sessions[session_id]["result"] = result
        running_sessions[session_id]["report"] = report
        _log_status(session_id, "Pipeline completed successfully.")

    except Exception as e:
        tb = traceback.format_exc()
        print(f"Pipeline error for {session_id}: {tb}", flush=True)
        error_msg = f"{type(e).__name__}: {str(e)}" if str(e) else f"{type(e).__name__}: {tb[-300:]}"
        running_sessions[session_id]["status"] = "error"
        running_sessions[session_id]["error"] = error_msg
        _log_status(session_id, f"ERROR: {error_msg[:200]}")


def _log_status(session_id: str, msg: str):
    if session_id in running_sessions:
        running_sessions[session_id].setdefault("logs", []).append(
            {"time": time.time(), "msg": msg}
        )


@app.get("/api/session/{session_id}", response_model=SessionStatus)
async def get_session(session_id: str):
    """Get session status, agents, and report."""
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    runtime_info = running_sessions.get(session_id, {})
    status = runtime_info.get("status", session.get("status", "unknown"))

    agents = []
    arena_stats = {}
    report_data = None

    arena = Arena(db)
    arena_stats = arena.get_stats(session_id)

    if status == "completed":
        report_raw = runtime_info.get("report") or (
            json.loads(session["report"]) if session.get("report") else None
        )
        if report_raw:
            report_data = _parse_report(report_raw)

    companies = []
    if runtime_info.get("companies"):
        companies = runtime_info["companies"]
    elif session.get("companies_analyzed"):
        try:
            companies = json.loads(session["companies_analyzed"]) if isinstance(
                session["companies_analyzed"], str
            ) else session["companies_analyzed"]
        except (json.JSONDecodeError, TypeError):
            pass

    elapsed = None
    if runtime_info.get("started_at"):
        elapsed = round(time.time() - runtime_info["started_at"], 1)

    logs = runtime_info.get("logs", [])[-50:]

    tier_stats = None
    graph_stats = None
    if runtime_info.get("result"):
        tier_stats = runtime_info["result"].get("tier_stats")
        graph_stats = runtime_info["result"].get("graph_stats")

    return SessionStatus(
        session_id=session_id,
        status=status,
        query=session.get("query_text", runtime_info.get("query", "")),
        query_type=session.get("query_type", runtime_info.get("query_type", "")),
        companies=companies or [],
        agents=agents,
        arena_stats=arena_stats,
        report=report_data,
        elapsed_seconds=elapsed,
        created_at=session.get("created_at"),
        logs=logs,
        tier_stats=tier_stats,
        graph_stats=graph_stats,
        error=runtime_info.get("error"),
    )


@app.get("/api/session/{session_id}/arena")
async def get_arena(session_id: str):
    """Get all arena posts with comments for a session."""
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    arena = Arena(db)
    posts = arena.get_session_posts(session_id)

    result = []
    for post in posts:
        comments_raw = arena.get_post_comments(post["post_id"])
        comments = [
            {
                "comment_id": c["comment_id"],
                "post_id": c["post_id"],
                "agent_id": c.get("agent_id", ""),
                "agent_name": c.get("agent_name", ""),
                "content": c["content"],
                "comment_type": c.get("comment_type", "response"),
                "parent_comment_id": c.get("parent_comment_id"),
                "round_num": c.get("round_num", 0),
                "likes": c.get("likes", 0),
                "dislikes": c.get("dislikes", 0),
                "created_at": c.get("created_at", ""),
            }
            for c in comments_raw
        ]

        result.append({
            "post_id": post["post_id"],
            "agent_id": post.get("agent_id", ""),
            "agent_name": post.get("agent_name", ""),
            "agent_type": post.get("agent_type", ""),
            "topic": post.get("topic", "general"),
            "content": post["content"],
            "post_type": post.get("post_type", "analysis"),
            "confidence": post.get("confidence"),
            "round_num": post.get("round_num", 0),
            "likes": post.get("likes", 0),
            "dislikes": post.get("dislikes", 0),
            "created_at": post.get("created_at", ""),
            "comments": comments,
        })

    return {"session_id": session_id, "posts": result, "total": len(result)}


@app.get("/api/session/{session_id}/logs")
async def get_session_logs(session_id: str):
    """Get real-time logs for a running session."""
    runtime = running_sessions.get(session_id, {})
    return {
        "session_id": session_id,
        "status": runtime.get("status", "unknown"),
        "logs": runtime.get("logs", []),
    }


@app.get("/api/sessions")
async def list_sessions(user_id: Optional[str] = None, limit: int = 20):
    """List recent sessions."""
    if user_id:
        sessions = db.get_user_sessions(user_id, limit=limit)
    else:
        conn = db._get_conn()
        rows = conn.execute(
            "SELECT * FROM sessions ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        sessions = [dict(r) for r in rows]

    return {
        "sessions": [
            {
                "session_id": s["id"],
                "query": s.get("query_text", ""),
                "query_type": s.get("query_type", ""),
                "status": s.get("status", ""),
                "created_at": s.get("created_at", ""),
            }
            for s in sessions
        ]
    }


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "llm_available": llm is not None,
        "llm_model": llm.config.model if llm else None,
        "llm_provider": llm._provider if llm else None,
        "active_sessions": len([s for s in running_sessions.values() if s.get("status") == "running"]),
    }


# =========================================================
# WebSocket for real-time streaming
# =========================================================

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    if session_id not in active_websockets:
        active_websockets[session_id] = []
    active_websockets[session_id].append(websocket)

    try:
        await websocket.send_text(json.dumps({
            "type": "connected",
            "data": {"session_id": session_id},
            "timestamp": datetime.utcnow().isoformat(),
        }))

        runtime = running_sessions.get(session_id, {})
        for log in runtime.get("logs", []):
            await websocket.send_text(json.dumps({
                "type": "status",
                "data": {"message": log["msg"]},
                "timestamp": datetime.utcnow().isoformat(),
            }))

        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except asyncio.TimeoutError:
                await websocket.send_text(json.dumps({"type": "heartbeat"}))
                runtime = running_sessions.get(session_id, {})
                if runtime.get("status") in ("completed", "error"):
                    await websocket.send_text(json.dumps({
                        "type": "session_complete",
                        "data": {"status": runtime["status"]},
                        "timestamp": datetime.utcnow().isoformat(),
                    }))
                    break

    except WebSocketDisconnect:
        pass
    finally:
        if session_id in active_websockets:
            if websocket in active_websockets[session_id]:
                active_websockets[session_id].remove(websocket)


# =========================================================
# Helpers
# =========================================================

def _parse_report(raw: dict) -> Optional[Report]:
    try:
        sections = []
        for s in raw.get("sections", []):
            sections.append(ReportSection(
                heading=s.get("heading", ""),
                content=s.get("content", ""),
                confidence=s.get("confidence"),
                key_insights=s.get("key_insights", []),
                recommendations=s.get("recommendations", []),
                caveats=s.get("caveats", []),
                source_agents=s.get("source_agents", []),
            ))
        return Report(
            title=raw.get("title", ""),
            executive_summary=raw.get("executive_summary", ""),
            sections=sections,
            key_recommendations=raw.get("key_recommendations", []),
            risk_factors=raw.get("risk_factors", []),
            data_quality_note=raw.get("data_quality_note", ""),
            next_steps=raw.get("next_steps", []),
        )
    except Exception:
        return None


# =========================================================
# Interview Endpoints
# =========================================================

from interview_runner import InterviewRunner, InterviewConfig
from interviewer_personas import PANEL_PRESETS

active_interviews: Dict[str, InterviewRunner] = {}


@app.get("/api/interview/presets")
async def get_interview_presets():
    """Get available interview preset configurations."""
    return {
        "presets": {
            key: {
                "name": val["name"],
                "description": val["description"],
                "panel_size": val["panel_size"],
                "difficulty": val["difficulty"],
                "max_turns": val["max_turns"],
            }
            for key, val in PANEL_PRESETS.items()
        }
    }


@app.post("/api/interview/start")
async def start_interview(
    preset: str = Form("campus_placement"),
    role: str = Form(""),
    company: str = Form(""),
    difficulty: str = Form("realistic"),
    user_id: Optional[str] = Form(None),
):
    """Create and start a new interview session."""
    if not llm:
        raise HTTPException(status_code=503, detail="LLM not configured")

    config = InterviewConfig(
        preset=preset,
        role=role,
        company=company,
        difficulty=difficulty,
    )

    preset_info = PANEL_PRESETS.get(preset, {})
    config.panel_size = preset_info.get("panel_size", 3)
    config.max_turns = preset_info.get("max_turns", 30)
    config.interview_type = "upsc" if preset == "upsc_board" else "panel"

    def on_event(event):
        session_id = event.get("session_id", "")
        if session_id:
            asyncio.get_event_loop().call_soon_threadsafe(
                lambda: asyncio.ensure_future(
                    _broadcast(session_id, event.get("type", "event"), event)
                )
            )

    runner = InterviewRunner(
        llm=llm, db=db, config=config,
        on_event=on_event, user_id=user_id,
    )

    setup_result = runner.setup()
    session_id = runner.session_id
    active_interviews[session_id] = runner

    # Start the interview (introductions + first question)
    opening_turns = runner.start()

    return {
        "session_id": session_id,
        "panel": setup_result["panel"],
        "config": setup_result["config"],
        "opening": opening_turns,
    }


@app.post("/api/interview/{session_id}/answer")
async def submit_interview_answer(session_id: str, answer: str = Form(...)):
    """Submit candidate answer, get interviewer response(s)."""
    runner = active_interviews.get(session_id)
    if not runner:
        raise HTTPException(status_code=404, detail="Interview session not found")

    if runner.status not in ("active", "wrapping_up"):
        raise HTTPException(status_code=400, detail=f"Interview is {runner.status}")

    # Run in executor to avoid blocking
    loop = asyncio.get_event_loop()
    responses = await loop.run_in_executor(None, runner.submit_answer, answer)

    return {
        "session_id": session_id,
        "responses": responses,
        "state": runner.get_state(),
    }


@app.post("/api/interview/{session_id}/end")
async def end_interview(session_id: str):
    """End the interview and get evaluation."""
    runner = active_interviews.get(session_id)
    if not runner:
        raise HTTPException(status_code=404, detail="Interview session not found")

    loop = asyncio.get_event_loop()
    evaluation = await loop.run_in_executor(None, runner.end_interview)

    # Cleanup
    del active_interviews[session_id]

    return {
        "session_id": session_id,
        "evaluation": evaluation,
    }


@app.get("/api/interview/{session_id}")
async def get_interview_state(session_id: str):
    """Get current interview state."""
    runner = active_interviews.get(session_id)
    if runner:
        return runner.get_state()

    # Check DB for completed interviews
    session = db.get_interview_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview not found")

    return {
        "session_id": session_id,
        "status": session["status"],
        "interview_type": session["interview_type"],
        "role": session["role"],
        "company": session["company"],
        "total_turns": session["total_turns"],
    }


@app.get("/api/interview/{session_id}/transcript")
async def get_interview_transcript(session_id: str):
    """Get the full interview transcript."""
    turns = db.get_interview_turns(session_id)
    if not turns:
        raise HTTPException(status_code=404, detail="No transcript found")
    return {"session_id": session_id, "turns": turns}


@app.get("/api/interview/{session_id}/evaluation")
async def get_interview_evaluation(session_id: str):
    """Get interview scores and feedback."""
    scores = db.get_aggregated_scores(session_id)
    if not scores:
        raise HTTPException(status_code=404, detail="No evaluation found")
    return {"session_id": session_id, **scores}


@app.post("/api/interview/{session_id}/evaluate")
async def evaluate_interview(session_id: str):
    """Run evaluation for a completed multi-round interview."""
    if not round_manager:
        raise HTTPException(status_code=503, detail="LLM not configured")

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, round_manager.evaluate_interview, session_id
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@app.get("/api/interview/{session_id}/skill-gap")
async def get_skill_gap_report(session_id: str, company: str = "", role: str = ""):
    """Generate skill gap report from evaluation scores + candidate model."""
    if not round_manager:
        raise HTTPException(status_code=503, detail="LLM not configured")

    session = db.get_interview_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Check if evaluation has been run
    scores = db.get_aggregated_scores(session_id)
    if not scores or not scores.get("dimensions"):
        raise HTTPException(status_code=400, detail="Run evaluation first (POST /api/interview/{id}/evaluate)")

    # Get candidate model
    candidate_model = round_manager.candidate_models.get(session_id)
    if not candidate_model:
        saved = session.get("candidate_model_json")
        if saved:
            import json as _json
            from candidate_model import CandidateModel
            try:
                d = _json.loads(saved) if isinstance(saved, str) else saved
                candidate_model = CandidateModel.from_dict(d)
            except Exception:
                pass

    # Use session company/role if not specified
    target_company = company or session.get("company", "")
    target_role = role or session.get("role", "")

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: round_manager.evaluation_engine.generate_skill_gap_report(
            session_id=session_id,
            candidate_model=candidate_model,
            target_company=target_company,
            target_role=target_role,
        ),
    )
    return result


@app.get("/api/interview/history/{user_id}")
async def get_interview_history(user_id: str, limit: int = 20):
    """Get interview history for a user."""
    interviews = db.get_user_interviews(user_id, limit=limit)
    return {"interviews": interviews}


# =========================================================
# Interview WebSocket (real-time streaming)
# =========================================================

@app.websocket("/ws/interview/{session_id}")
async def interview_websocket(websocket: WebSocket, session_id: str):
    """WebSocket for real-time interview streaming."""
    await websocket.accept()

    if session_id not in active_websockets:
        active_websockets[session_id] = []
    active_websockets[session_id].append(websocket)

    try:
        await websocket.send_text(json.dumps({
            "type": "connected",
            "data": {"session_id": session_id},
        }))

        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=60.0)
                msg = json.loads(data)

                if msg.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))

                elif msg.get("type") == "answer":
                    runner = active_interviews.get(session_id)
                    if runner and runner.status == "active":
                        answer_text = msg.get("content", "")
                        loop = asyncio.get_event_loop()
                        responses = await loop.run_in_executor(
                            None, runner.submit_answer, answer_text
                        )
                        for resp in responses:
                            await websocket.send_text(json.dumps({
                                "type": "interviewer_response",
                                "data": resp,
                            }))

                elif msg.get("type") == "end":
                    runner = active_interviews.get(session_id)
                    if runner:
                        loop = asyncio.get_event_loop()
                        evaluation = await loop.run_in_executor(
                            None, runner.end_interview
                        )
                        await websocket.send_text(json.dumps({
                            "type": "evaluation",
                            "data": evaluation,
                        }))

            except asyncio.TimeoutError:
                await websocket.send_text(json.dumps({"type": "heartbeat"}))

    except WebSocketDisconnect:
        pass
    finally:
        if session_id in active_websockets:
            if websocket in active_websockets[session_id]:
                active_websockets[session_id].remove(websocket)


# =========================================================
# Multi-Round V2 Endpoints
# =========================================================

from screening_agent import ScreeningAgent
from round_manager import RoundManager
from knowledge_db import KnowledgeDB

knowledge_db = KnowledgeDB("knowledge.db")
screening_agent = ScreeningAgent(llm=llm, db=db, knowledge_db=knowledge_db) if llm else None
round_manager = RoundManager(llm=llm, db=db, knowledge_db=knowledge_db) if llm else None


# --- Screening ---

@app.post("/api/screening/start")
async def start_screening(
    name: str = Form(""),
    resume_file: Optional[UploadFile] = File(None),
):
    """Start a screening conversation."""
    if not screening_agent:
        raise HTTPException(status_code=503, detail="LLM not configured")

    resume_data = None
    if resume_file:
        content = await resume_file.read()
        resume_text = content.decode("utf-8", errors="ignore")
        try:
            from tools.resume_parser import ResumeParserTool
            parser = ResumeParserTool()
            result = parser.execute(raw_text=resume_text)
            if result.success:
                resume_data = json.loads(result.data) if isinstance(result.data, str) else result.data
        except Exception:
            resume_data = {"raw_text": resume_text[:3000]}

    result = screening_agent.start(name=name, resume_data=resume_data)
    return result


@app.post("/api/screening/{session_id}/answer")
async def screening_answer(session_id: str, answer: str = Form(...)):
    """Submit candidate answer in screening conversation."""
    if not screening_agent:
        raise HTTPException(status_code=503, detail="LLM not configured")

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, screening_agent.process_answer, session_id, answer
    )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@app.post("/api/screening/{session_id}/complete")
async def complete_screening(
    session_id: str,
    company: str = Form(""),
    role: str = Form(""),
    panel_size: int = Form(3),
):
    """Complete screening and generate panel + round plan."""
    if not screening_agent or not round_manager:
        raise HTTPException(status_code=503, detail="LLM not configured")

    loop = asyncio.get_event_loop()

    # Build candidate profile
    profile = await loop.run_in_executor(
        None, screening_agent.complete, session_id
    )

    # Create multi-round interview
    session_result = await loop.run_in_executor(
        None,
        lambda: round_manager.create_multi_round_session(
            profile=profile,
            company=company,
            role=role,
            screening_session_id=session_id,
            panel_size=panel_size,
        )
    )

    return {
        "candidate_profile": profile.to_dict(),
        **session_result,
    }


@app.get("/api/screening/{session_id}")
async def get_screening_status(session_id: str):
    """Get screening session status."""
    if not screening_agent:
        raise HTTPException(status_code=503, detail="LLM not configured")
    status = screening_agent.get_session_status(session_id)
    if "error" in status:
        raise HTTPException(status_code=404, detail=status["error"])
    return status


# --- Multi-Round Interview ---

@app.post("/api/interview/multi/start")
async def start_multi_round(
    screening_session_id: str = Form(...),
    company: str = Form(""),
    role: str = Form(""),
    panel_size: int = Form(3),
):
    """Start a multi-round interview from a completed screening session."""
    if not round_manager or not screening_agent:
        raise HTTPException(status_code=503, detail="LLM not configured")

    session = db.get_screening_session(screening_session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Screening session not found")

    profile_data = json.loads(session["candidate_profile"]) if isinstance(session.get("candidate_profile"), str) else session.get("candidate_profile", {})
    if not profile_data:
        raise HTTPException(status_code=400, detail="Screening not completed yet")

    from screening_agent import CandidateProfile
    profile = CandidateProfile.from_dict(profile_data)

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: round_manager.create_multi_round_session(
            profile=profile,
            company=company,
            role=role,
            screening_session_id=screening_session_id,
            panel_size=panel_size,
        )
    )

    return result


@app.post("/api/interview/{session_id}/round/{round_num}/start")
async def start_round(session_id: str, round_num: int):
    """Start a specific round of the multi-round interview."""
    if not round_manager:
        raise HTTPException(status_code=503, detail="LLM not configured")

    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(
            None, round_manager.start_round, session_id, round_num
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result.to_dict()


@app.post("/api/interview/{session_id}/round/{round_num}/answer")
async def submit_round_answer(
    session_id: str, round_num: int, answer: str = Form(...)
):
    """Submit candidate answer within a round."""
    if not round_manager:
        raise HTTPException(status_code=503, detail="LLM not configured")

    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(
            None, round_manager.submit_answer, session_id, round_num, answer
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result


@app.post("/api/interview/{session_id}/round/{round_num}/end")
async def end_round(session_id: str, round_num: int):
    """End a round and trigger the inter-interviewer forum."""
    if not round_manager:
        raise HTTPException(status_code=503, detail="LLM not configured")

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, round_manager.end_round, session_id, round_num
    )

    return result.to_dict()


@app.get("/api/interview/{session_id}/forum")
async def get_forum(session_id: str):
    """Get the full inter-interviewer forum (for reveal page)."""
    if not round_manager:
        raise HTTPException(status_code=503, detail="LLM not configured")

    forum_data = round_manager.forum.get_full_forum(session_id)
    summary = round_manager.forum.get_forum_summary(session_id)

    return {
        "session_id": session_id,
        "rounds": forum_data,
        "summary": summary,
    }


@app.get("/api/interview/{session_id}/rounds")
async def get_round_status(session_id: str):
    """Get status of all rounds in an interview."""
    if not round_manager:
        raise HTTPException(status_code=503, detail="LLM not configured")

    status = round_manager.get_interview_status(session_id)
    if "error" in status:
        raise HTTPException(status_code=404, detail=status["error"])
    return status


@app.get("/api/knowledge/stats")
async def get_knowledge_stats():
    """Get knowledge database statistics."""
    return knowledge_db.get_stats()


@app.get("/api/knowledge/companies")
async def get_knowledge_companies():
    """Get list of companies with profiles."""
    return {"companies": knowledge_db.get_all_companies()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
