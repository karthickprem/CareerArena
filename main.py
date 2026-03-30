"""
CareerArena — Multi-Agent Career Intelligence Engine.

Usage:
  python main.py "What is the salary for SDE-2 at Google Bangalore?"
  python main.py --resume resume.pdf "Am I ready for Amazon interview?"
  python main.py --interactive
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Optional

from database import CareerDB
from llm_client import LLMClient
from orchestrator import Orchestrator
from report_synthesizer import ReportSynthesizer


def create_status_callback():
    """Create a status callback that prints with timestamps."""
    start = time.time()

    def callback(msg: str):
        elapsed = time.time() - start
        print(f"  [{elapsed:6.1f}s] {msg}")

    return callback


def run_query(
    query: str,
    resume_file: Optional[str] = None,
    user_id: str = "cli_user",
    db_path: str = "career_arena.db",
) -> dict:
    """Run a single query through the full pipeline."""
    db = CareerDB(db_path)

    try:
        llm = LLMClient()
    except Exception as e:
        print(f"Warning: LLM client init failed ({e}). Running in offline mode.")
        llm = None

    orchestrator = Orchestrator(
        llm=llm,
        db=db,
        on_status=create_status_callback(),
    )

    result = orchestrator.run(
        query=query,
        user_id=user_id,
        resume_file=resume_file,
    )

    synthesizer = ReportSynthesizer(llm=llm)
    report = synthesizer.generate(result)

    print()
    print(synthesizer.format_text(report))

    report_file = f"report_{result['session_id']}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nFull report saved to: {report_file}")

    return report


def interactive_mode(db_path: str = "career_arena.db"):
    """Interactive CLI mode for continuous queries."""
    print("=" * 60)
    print("  CareerArena — Multi-Agent Career Intelligence Engine")
    print("  Type your career question, or 'quit' to exit.")
    print("  Use 'resume <path>' to load a resume first.")
    print("=" * 60)
    print()

    resume_file = None
    user_id = "interactive_user"

    while True:
        try:
            query = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if query.lower().startswith("resume "):
            resume_file = query.split(" ", 1)[1].strip()
            print(f"Resume loaded: {resume_file}")
            continue

        if query.lower() == "help":
            print_help()
            continue

        print()
        try:
            run_query(
                query=query,
                resume_file=resume_file,
                user_id=user_id,
                db_path=db_path,
            )
        except Exception as e:
            print(f"Error: {e}")

        print()


def print_help():
    print("""
Available query types:
  Resume Review:    "Review my resume for backend roles"
  Salary Intel:     "Salary for SDE-2 at Google Bangalore?"
  Offer Compare:    "Compare Razorpay vs Flipkart offers"
  Interview Prep:   "Prepare me for Amazon interview"
  Career Strategy:  "What should I do next in my career?"
  Company Research: "Tell me about Cred as a company"
  Skill Planning:   "How to become an ML engineer?"
  Negotiation:      "How to negotiate my Razorpay offer?"

Commands:
  resume <path>  — Load a resume (PDF, DOCX, or TXT)
  help           — Show this message
  quit           — Exit
""")


def demo_mode():
    """Run a demo without LLM to show the architecture working."""
    from query_router import route_query
    from context_builder import ContextBuilder
    from agent_factory import AgentFactory
    from arena import Arena

    print("=" * 60)
    print("  CareerArena — DEMO MODE (no LLM required)")
    print("=" * 60)
    print()

    db = CareerDB(":memory:")
    factory = AgentFactory(db)
    ctx_builder = ContextBuilder(db)
    arena = Arena(db)
    synthesizer = ReportSynthesizer()

    queries = [
        "Compare Google vs Razorpay vs Flipkart for SDE-2",
        "Review my resume for backend engineer roles",
        "What is the salary for Product Manager at Swiggy?",
        "Prepare me for Amazon system design interview",
    ]

    for query in queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print("-" * 60)

        routed = route_query(query)
        ctx = ctx_builder.build(routed)
        agents = factory.create_agent_roster(routed, ctx_builder.to_agent_prompt_context(ctx))

        print(f"Type: {routed.query_type.value}")
        print(f"Companies: {routed.companies}")
        print(f"\n{factory.describe_roster(agents)}")

        for i, agent in enumerate(agents[:3]):
            arena.create_post(
                session_id=ctx.session_id,
                agent_id=agent.agent_id,
                agent_name=agent.name,
                agent_type=agent.agent_type,
                topic=agent.lead_type,
                content=f"[Demo] {agent.name} analysis for: {query}",
                confidence=0.7 + (i * 0.05),
            )

        mock_result = {
            "session_id": ctx.session_id,
            "query": query,
            "query_type": routed.query_type.value,
            "companies": routed.companies,
            "agents_used": len(agents),
            "debate_rounds": routed.debate_rounds,
            "arena_stats": arena.get_stats(ctx.session_id),
            "synthesis": {
                agent.lead_type: {
                    "domain": agent.lead_type,
                    "summary": f"[Demo] {agent.name} synthesized findings.",
                    "key_insights": [f"Insight from {agent.name}"],
                    "recommendations": [f"Recommendation from {agent.name}"],
                    "confidence": 0.75,
                    "caveats": ["Demo mode — no real data"],
                }
                for agent in factory.get_leads(agents)
                if not agent.is_adversarial
            },
            "contrarian": {
                "challenges": [{"target_agent": "All", "challenge": "Demo challenge"}],
                "blind_spots": ["This is demo mode"],
                "overall_assessment": "Demo — connect LLM for real analysis.",
            },
            "transcript": arena.build_transcript(ctx.session_id),
            "elapsed_seconds": 0.1,
        }

        report = synthesizer.generate(mock_result)
        print(synthesizer.format_text(report))

    print("\nDemo complete! Run with a real query for full LLM-powered analysis.")


def main():
    parser = argparse.ArgumentParser(
        description="CareerArena — Multi-Agent Career Intelligence Engine",
    )
    parser.add_argument("query", nargs="?", help="Career query to analyze")
    parser.add_argument("--resume", help="Path to resume file (PDF, DOCX, TXT)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--demo", action="store_true", help="Demo mode (no LLM needed)")
    parser.add_argument("--db", default="career_arena.db", help="Database path")
    parser.add_argument("--user", default="cli_user", help="User ID")

    args = parser.parse_args()

    if args.demo:
        demo_mode()
    elif args.interactive:
        interactive_mode(db_path=args.db)
    elif args.query:
        run_query(
            query=args.query,
            resume_file=args.resume,
            user_id=args.user,
            db_path=args.db,
        )
    else:
        parser.print_help()
        print("\nQuick start:")
        print('  python main.py --demo')
        print('  python main.py "Salary for SDE-2 at Google?"')
        print('  python main.py --interactive')


if __name__ == "__main__":
    main()
