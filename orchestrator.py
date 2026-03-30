"""
Orchestrator — Debug Arena-aligned career intelligence pipeline.

Architecture (EXACTLY like Debug Arena main.py):

  Stage 1: Resume + Query → Knowledge Graph (entity + relationship extraction)
  Stage 2: Graph Entities → Agent Profiles (enriched, typed personas)
  Stage 3: Profiles + Graph → Simulation Config (initial posts, hot topics, agent behavior)
  Stage 4: Parallel Autonomous Simulation with Tool-Equipped Agents
           - ReAct agents investigate using tools (web search, salary data, etc.)
           - Agents post findings, debate, challenge each other in the arena
           - Orchestrator (ReportAgent) reads arena → issues directives
           - Directed agents run again with priority tasks
           - Repeat until convergence
           - Generate final report

Two layers of control:
  - WORKERS: all agents with ReAct tools — investigate, debate, challenge
  - ORCHESTRATOR: ReportAgent assigns tasks and decides when to stop
"""

from __future__ import annotations

import json
import time
from typing import Any, Callable, Dict, List, Optional

from llm_client import LLMClient
from database import CareerDB
from query_router import route_query, RoutedQuery
from context_builder import ContextBuilder, SessionContext
from arena import Arena
from graph_builder import build_graph
from profile_generator import generate_profiles
from config_generator import generate_config
from simulation import Simulation, SimulationAgent
from report_agent import ReportAgent


class Orchestrator:
    def __init__(
        self,
        llm: Optional[LLMClient] = None,
        db: Optional[CareerDB] = None,
        on_status: Optional[Callable] = None,
    ):
        self.llm = llm
        self.db = db or CareerDB()
        self.arena = Arena(self.db)
        self.ctx_builder = ContextBuilder(self.db)
        self._on_status = on_status or (lambda msg: print(f"  [{time.strftime('%H:%M:%S')}] {msg}"))

    def run(
        self,
        query: str,
        user_id: Optional[str] = None,
        resume_data: Optional[dict] = None,
        resume_file: Optional[str] = None,
        session_id: Optional[str] = None,
        max_cycles: int = 5,
        max_agents: int = 40,
    ) -> Dict[str, Any]:
        """Execute the Debug Arena-aligned career intelligence pipeline."""
        start = time.time()

        # Classify the query
        self._status("Classifying query...")
        routed = route_query(query, resume_data)
        self._status(
            f"Query type: {routed.query_type.value} | "
            f"Companies: {routed.companies} | "
            f"Agents: {len(routed.fixed_agents)}"
        )

        if resume_file and not resume_data:
            resume_data = self._parse_resume(resume_file)

        # Build session context
        self._status("Building session context...")
        if session_id:
            ctx = SessionContext(
                session_id=session_id,
                user_id=user_id,
                query=routed,
                resume_data=resume_data,
            )
        else:
            ctx = self.ctx_builder.build(routed, user_id, resume_data)

        if self.llm:
            result = self._run_pipeline(routed, ctx, resume_data, max_cycles, max_agents)
        else:
            self._status("No LLM configured — running in offline mode")
            result = self._run_offline(ctx)

        elapsed = time.time() - start
        self._status(f"Pipeline complete in {elapsed:.1f}s")

        result["session_id"] = ctx.session_id
        result["query"] = query
        result["query_type"] = routed.query_type.value
        result["companies"] = routed.companies
        result["elapsed_seconds"] = round(elapsed, 1)

        if self.db:
            self.db.complete_session(
                ctx.session_id,
                report=json.dumps(result, default=str),
            )

        return result

    def _run_pipeline(
        self,
        routed: RoutedQuery,
        ctx: SessionContext,
        resume_data: Optional[dict],
        max_cycles: int,
        max_agents: int,
    ) -> Dict[str, Any]:
        """Four-stage pipeline — exactly like Debug Arena main.py.

        Stage 1: Resume → Knowledge Graph
        Stage 2: Graph → Agent Profiles
        Stage 3: Profiles + Graph → Simulation Config
        Stage 4: Simulation (ReAct + Arena + Orchestration)
        """

        # ═══════════════════════════════════════════════════
        # STAGE 1: Resume + Query → Knowledge Graph
        # ═══════════════════════════════════════════════════

        self._status("═══ STAGE 1: Knowledge Graph ═══")
        resume_text = ""
        if resume_data:
            resume_text = resume_data.get("raw_text", "")
            if not resume_text:
                resume_text = json.dumps(resume_data, indent=2)

        graph = build_graph(
            llm=self.llm,
            resume_text=resume_text,
            query=routed.original_query,
            companies=routed.companies,
            on_progress=self._status,
        )

        entity_count = graph["metadata"]["entity_count"]
        edge_count = graph["metadata"]["edge_count"]
        self._status(f"  Entities: {entity_count}, Relationships: {edge_count}")

        if self.db:
            self.db.set_meta(f"graph_{ctx.session_id}", json.dumps(graph, default=str))

        # ═══════════════════════════════════════════════════
        # STAGE 2: Graph Entities → Agent Profiles
        # ═══════════════════════════════════════════════════

        self._status("═══ STAGE 2: Agent Profiles ═══")
        profiles_result = generate_profiles(
            llm=self.llm,
            graph=graph,
            on_progress=self._status,
            max_tier2=min(max_agents, max(8, entity_count)),
        )

        all_profiles = profiles_result["all"]
        self._status(f"  Generated {len(all_profiles)} agent profiles")
        for p in all_profiles[:10]:
            self._status(f"    [{p.get('entity_type', '?')}] {p.get('name', '?')}")

        # ═══════════════════════════════════════════════════
        # STAGE 3: Profiles + Graph → Simulation Config
        # ═══════════════════════════════════════════════════

        self._status("═══ STAGE 3: Simulation Config ═══")
        config = generate_config(
            llm=self.llm,
            graph=graph,
            profiles=all_profiles,
            query=routed.original_query,
            companies=routed.companies,
            on_progress=self._status,
        )

        ec = config.get("event_config", {})
        initial_posts = ec.get("initial_posts", [])
        hot_topics = ec.get("hot_topics", [])
        self._status(f"  Initial posts: {len(initial_posts)}")
        self._status(f"  Hot topics: {hot_topics}")

        # ═══════════════════════════════════════════════════
        # STAGE 4: Parallel Autonomous Simulation
        # ═══════════════════════════════════════════════════

        self._status("═══ STAGE 4: Parallel Simulation (ReAct + Arena + Orchestration) ═══")

        focus_areas = ", ".join(routed.companies) if routed.companies else routed.original_query

        sim = Simulation(
            llm=self.llm,
            db=self.db,
            session_id=ctx.session_id,
            profiles=all_profiles,
            config=config,
            graph=graph,
            on_event=self._make_event_handler(),
            focus_areas=focus_areas,
        )

        self._status(f"  {len(sim.agents)} agents | {len(sim.tools)} tools | "
                      f"Adversarial: {[a.name for a in sim.agents if a.is_adversarial]}")

        # Step 1: ALL agents run initial sweep (ReAct → investigate → post)
        self._status("--- Initial Sweep: ALL agents investigate & post ---")
        sim.run_initial_sweep()

        # Step 2: Orchestration loop — ReportAgent reads arena, assigns tasks
        self._status("--- Orchestration: ReportAgent directing investigation ---")
        report_agent = ReportAgent(self.llm, self.db)
        last_assessment = ""

        for cycle in range(1, max_cycles + 1):
            self._status(f"\n--- Orchestrator Cycle {cycle}/{max_cycles} ---")

            orch_result = report_agent.orchestrate(
                session_id=ctx.session_id,
                query=routed.original_query,
                cycle_num=cycle,
                max_cycles=max_cycles,
            )

            convergence = orch_result.get("convergence_score", 0)
            last_assessment = orch_result.get("assessment", "")
            directives = orch_result.get("directives", [])

            self._status(
                f"  Convergence: {convergence:.0%} | "
                f"Directives: {len(directives)} | "
                f"Assessment: {last_assessment[:120]}"
            )

            if orch_result.get("should_stop"):
                self._status(f"  Stopping: {orch_result.get('stop_reason', 'converged')}")
                break

            if directives:
                self._status(f"  Directing {len(directives)} agents...")
                for d in directives:
                    self._status(f"    → {d.get('target_agent', '?')}: {d.get('task', '?')[:80]}")
                sim.run_directed_cycle(directives, cycle)

        sim.finalize()

        # Step 3: Generate final report
        self._status("═══ Generating Final Report ═══")
        report = report_agent.generate_report(
            session_id=ctx.session_id,
            query=routed.original_query,
            query_type=routed.query_type.value,
            companies=routed.companies,
            assessment=last_assessment,
        )

        arena_stats = self.arena.get_stats(ctx.session_id)
        transcript = self.arena.build_transcript(ctx.session_id)

        return {
            "arena_stats": arena_stats,
            "transcript": transcript,
            "report": report,
            "orchestrator_assessment": last_assessment,
            "agents_used": len(sim.agents),
            "graph_stats": {
                "entities": entity_count,
                "edges": edge_count,
            },
        }

    def _make_event_handler(self):
        def on_event(event: dict):
            etype = event.get("type", "")
            if etype == "agent_investigating":
                name = event.get("agent_name", "?")
                tag = " [ADV]" if event.get("is_adversarial") else ""
                dtag = " [DIRECTIVE]" if event.get("has_directive") else ""
                self._status(f"  🦑 {name} investigating{tag}{dtag}")
            elif etype == "forum_post":
                seed = " (seed)" if event.get("seed") else ""
                self._status(f"  📡 {event.get('agent_name', '?')} posted{seed}: {event.get('content', '')[:80]}")
            elif etype == "forum_comment":
                self._status(f"  💬 {event.get('agent_name', '?')} commented on Post#{event.get('post_id', '?')}")
            elif etype == "tool_result":
                status = "OK" if event.get("success") else "FAIL"
                self._status(f"  🔧 {event.get('agent_name', '?')} → {event.get('tool', '?')}: {status}")
            elif etype == "cycle_end":
                stats = {k: event.get(k) for k in ("total_posts", "total_comments") if k in event}
                phase = event.get("phase", "?")
                self._status(f"  Cycle {event.get('cycle', '?')} [{phase}] done: {stats}")
            elif etype == "sim_complete":
                self._status(
                    f"  🐙 Simulation complete — {event.get('elapsed_s', '?')}s, "
                    f"{event.get('total_posts', 0)} posts, {event.get('total_comments', 0)} comments"
                )
        return on_event

    def _run_offline(self, ctx: SessionContext) -> Dict[str, Any]:
        return {
            "arena_stats": {"total_posts": 0, "total_comments": 0, "active_agents": 0},
            "transcript": "",
            "report": {
                "title": f"Career Intelligence: {ctx.query.original_query[:60]}",
                "executive_summary": "Offline mode — connect LLM for full analysis.",
                "sections": [],
                "key_recommendations": ["Configure AMD_LLM_API_KEY for real analysis"],
                "risk_factors": ["Running without LLM"],
                "next_steps": [],
                "data_quality_note": "No LLM configured.",
            },
            "orchestrator_assessment": "Offline mode",
            "agents_used": 0,
        }

    def _parse_resume(self, file_path: str) -> Optional[dict]:
        from tools import get_all_tools
        tools = {t.name: t for t in get_all_tools()}
        if "resume_parser" in tools:
            result = tools["resume_parser"].execute(file_path=file_path)
            if result.success:
                try:
                    return json.loads(result.data) if isinstance(result.data, str) else result.data
                except (json.JSONDecodeError, TypeError):
                    pass
        return None

    def _status(self, msg: str):
        if self._on_status:
            self._on_status(msg)
