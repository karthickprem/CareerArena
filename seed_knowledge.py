#!/usr/bin/env python3
"""
seed_knowledge.py — One-time seed script to populate knowledge.db
with comprehensive interview preparation data for PlaceRight.

Usage:
    python seed_knowledge.py                         # Full run (curated only)
    python seed_knowledge.py --skip-questions         # Skip question seeding
    python seed_knowledge.py --only questions          # Seed only questions
    python seed_knowledge.py --only companies          # Seed only companies
    python seed_knowledge.py --dry-run                 # Count items without writing
    python seed_knowledge.py --db-path /path/to.db     # Custom DB path
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
import time

# Ensure career_arena is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from knowledge_db import KnowledgeDB


def load_questions():
    """Load all question modules and return combined list."""
    all_questions = []

    modules = [
        ("DSA", "seed_data.questions_dsa", "get_dsa_questions"),
        ("DBMS", "seed_data.questions_dbms", "get_dbms_questions"),
        ("OS/Networks", "seed_data.questions_os_networks", "get_os_networks_questions"),
        ("OOP", "seed_data.questions_oop", "get_oop_questions"),
        ("Web Dev", "seed_data.questions_web", "get_web_questions"),
        ("Aptitude Quant", "seed_data.questions_aptitude_quant", "get_aptitude_quant_questions"),
        ("Aptitude Verbal", "seed_data.questions_aptitude_verbal", "get_aptitude_verbal_questions"),
        ("Aptitude Logical", "seed_data.questions_aptitude_logical", "get_aptitude_logical_questions"),
        ("Behavioral", "seed_data.questions_behavioral", "get_behavioral_questions"),
        ("System Design", "seed_data.questions_system_design", "get_system_design_questions"),
        ("Data Science", "seed_data.questions_data_science", "get_data_science_questions"),
    ]

    for label, module_path, func_name in modules:
        try:
            mod = __import__(module_path, fromlist=[func_name])
            getter = getattr(mod, func_name)
            questions = getter()
            print(f"  [{label}] Loaded {len(questions)} questions")
            all_questions.extend(questions)
        except ImportError as e:
            print(f"  [{label}] SKIPPED — module not found: {e}")
        except Exception as e:
            print(f"  [{label}] ERROR — {e}")

    return all_questions


def load_companies():
    """Load company profiles."""
    try:
        from seed_data.companies import get_companies
        companies = get_companies()
        print(f"  [Companies] Loaded {len(companies)} profiles")
        return companies
    except ImportError as e:
        print(f"  [Companies] SKIPPED — {e}")
        return []


def load_personas():
    """Load persona templates."""
    try:
        from seed_data.personas import get_personas
        personas = get_personas()
        print(f"  [Personas] Loaded {len(personas)} templates")
        return personas
    except ImportError as e:
        print(f"  [Personas] SKIPPED — {e}")
        return []


def load_rubrics():
    """Load evaluation rubrics."""
    try:
        from seed_data.rubrics import get_rubrics
        rubrics = get_rubrics()
        print(f"  [Rubrics] Loaded {len(rubrics)} rubrics")
        return rubrics
    except ImportError as e:
        print(f"  [Rubrics] SKIPPED — {e}")
        return []


def load_indian_context():
    """Load Indian context data."""
    try:
        from seed_data.indian_context import get_indian_context
        contexts = get_indian_context()
        print(f"  [Indian Context] Loaded {len(contexts)} entries")
        return contexts
    except ImportError as e:
        print(f"  [Indian Context] SKIPPED — {e}")
        return []


def load_hiring_tracks():
    """Load company hiring tracks."""
    try:
        from seed_data.hiring_tracks import get_hiring_tracks
        tracks = get_hiring_tracks()
        print(f"  [Hiring Tracks] Loaded {len(tracks)} tracks")
        return tracks
    except ImportError as e:
        print(f"  [Hiring Tracks] SKIPPED — {e}")
        return []


def load_round_blueprints():
    """Load company round blueprints."""
    try:
        from seed_data.round_blueprints import get_round_blueprints
        blueprints = get_round_blueprints()
        print(f"  [Round Blueprints] Loaded {len(blueprints)} company blueprints")
        return blueprints
    except ImportError as e:
        print(f"  [Round Blueprints] SKIPPED — {e}")
        return []


def load_default_blueprints():
    """Load default round blueprints."""
    try:
        from seed_data.round_blueprints import get_default_blueprints
        defaults = get_default_blueprints()
        print(f"  [Default Blueprints] Loaded {len(defaults)} default blueprints")
        return defaults
    except ImportError as e:
        print(f"  [Default Blueprints] SKIPPED — {e}")
        return []


def dedup_questions(questions: list) -> list:
    """Remove duplicate questions based on question_text hash."""
    seen = set()
    unique = []
    for q in questions:
        h = hashlib.md5(q["question_text"].strip().lower().encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique.append(q)
    dupes = len(questions) - len(unique)
    if dupes:
        print(f"  Removed {dupes} duplicate questions")
    return unique


def validate_question(q: dict) -> bool:
    """Basic validation for a question dict."""
    required = ["domain", "topic", "difficulty", "level", "question_text"]
    return all(q.get(k) for k in required)


def validate_company(c: dict) -> bool:
    """Basic validation for a company dict."""
    return bool(c.get("company_name"))


def print_distribution(questions: list):
    """Print question distribution by domain and difficulty."""
    from collections import Counter
    domain_counts = Counter(q["domain"] for q in questions)
    difficulty_counts = Counter(q["difficulty"] for q in questions)
    level_counts = Counter(q["level"] for q in questions)

    print("\n  Distribution by domain:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
        print(f"    {domain}: {count}")

    print("\n  Distribution by difficulty:")
    for diff, count in sorted(difficulty_counts.items()):
        print(f"    {diff}: {count}")

    print("\n  Distribution by level:")
    for level, count in sorted(level_counts.items()):
        print(f"    {level}: {count}")


def main():
    parser = argparse.ArgumentParser(description="Seed knowledge.db with comprehensive data")
    parser.add_argument("--db-path", default="knowledge.db", help="Path to knowledge.db")
    parser.add_argument("--dry-run", action="store_true", help="Count items without writing to DB")
    parser.add_argument("--only", choices=["questions", "companies", "personas", "rubrics", "context",
                                          "tracks", "blueprints"],
                        help="Seed only a specific category")
    parser.add_argument("--skip-questions", action="store_true", help="Skip question seeding")
    parser.add_argument("--no-wipe", action="store_true", help="Don't wipe existing data first")
    args = parser.parse_args()

    print("=" * 60)
    print("PlaceRight Knowledge Database Seeder")
    print("=" * 60)
    print(f"DB path: {os.path.abspath(args.db_path)}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()

    db = KnowledgeDB(db_path=args.db_path)

    # Show current stats
    current = db.get_stats()
    print("Current DB stats:")
    for k, v in current.items():
        print(f"  {k}: {v}")
    print()

    # Wipe if not dry-run and not no-wipe
    if not args.dry_run and not args.no_wipe:
        print("Wiping existing data...")
        db.wipe_all()
        print("  Done.\n")

    start = time.time()

    # ==========================================
    # PHASE 1: Load all curated data
    # ==========================================
    print("=" * 40)
    print("PHASE 1: Loading curated data")
    print("=" * 40)

    seed_all = args.only is None

    # Questions
    questions = []
    if (seed_all and not args.skip_questions) or args.only == "questions":
        print("\nLoading questions...")
        questions = load_questions()
        questions = [q for q in questions if validate_question(q)]
        questions = dedup_questions(questions)
        print(f"\n  Total valid unique questions: {len(questions)}")
        print_distribution(questions)

    # Companies
    companies = []
    if seed_all or args.only == "companies":
        print("\nLoading companies...")
        companies = load_companies()
        companies = [c for c in companies if validate_company(c)]
        print(f"  Total valid companies: {len(companies)}")

    # Personas
    personas = []
    if seed_all or args.only == "personas":
        print("\nLoading personas...")
        personas = load_personas()
        print(f"  Total personas: {len(personas)}")

    # Rubrics
    rubrics = []
    if seed_all or args.only == "rubrics":
        print("\nLoading rubrics...")
        rubrics = load_rubrics()
        print(f"  Total rubrics: {len(rubrics)}")

    # Indian Context
    contexts = []
    if seed_all or args.only == "context":
        print("\nLoading Indian context...")
        contexts = load_indian_context()
        print(f"  Total context entries: {len(contexts)}")

    # Hiring Tracks
    tracks = []
    if seed_all or args.only == "tracks":
        print("\nLoading hiring tracks...")
        tracks = load_hiring_tracks()
        print(f"  Total tracks: {len(tracks)}")

    # Round Blueprints
    round_blueprints = []
    default_blueprints = []
    if seed_all or args.only == "blueprints":
        print("\nLoading round blueprints...")
        round_blueprints = load_round_blueprints()
        default_blueprints = load_default_blueprints()
        print(f"  Total company blueprints: {len(round_blueprints)}")
        print(f"  Total default blueprints: {len(default_blueprints)}")

    load_time = time.time() - start
    print(f"\nData loading took {load_time:.1f}s")

    # ==========================================
    # PHASE 2: Insert into database
    # ==========================================
    if args.dry_run:
        print("\n[DRY RUN] Skipping database insertion.")
    else:
        print("\n" + "=" * 40)
        print("PHASE 2: Inserting into database")
        print("=" * 40)

        insert_start = time.time()

        if questions:
            print(f"\nInserting {len(questions)} questions...")
            count = db.bulk_add_questions(questions)
            print(f"  Inserted {count} questions")

        if companies:
            print(f"\nInserting {len(companies)} companies...")
            count = db.bulk_add_companies(companies)
            print(f"  Inserted {count} companies")

        if personas:
            print(f"\nInserting {len(personas)} personas...")
            count = db.bulk_add_personas(personas)
            print(f"  Inserted {count} personas")

        if rubrics:
            print(f"\nInserting {len(rubrics)} rubrics...")
            count = db.bulk_add_rubrics(rubrics)
            print(f"  Inserted {count} rubrics")

        if contexts:
            print(f"\nInserting {len(contexts)} context entries...")
            count = db.bulk_add_indian_context(contexts)
            print(f"  Inserted {count} context entries")

        if tracks:
            print(f"\nInserting {len(tracks)} hiring tracks...")
            count = db.bulk_add_hiring_tracks(tracks)
            print(f"  Inserted {count} hiring tracks")

        if round_blueprints:
            print(f"\nInserting {len(round_blueprints)} company round blueprints...")
            count = db.bulk_add_round_blueprints(round_blueprints)
            print(f"  Inserted {count} company round blueprints")

        if default_blueprints:
            print(f"\nInserting {len(default_blueprints)} default round blueprints...")
            count = db.bulk_add_default_blueprints(default_blueprints)
            print(f"  Inserted {count} default round blueprints")

        insert_time = time.time() - insert_start
        print(f"\nDatabase insertion took {insert_time:.1f}s")

    # ==========================================
    # PHASE 3: Verify
    # ==========================================
    print("\n" + "=" * 40)
    print("FINAL STATS")
    print("=" * 40)

    final = db.get_stats()
    for k, v in final.items():
        print(f"  {k}: {v}")

    total_time = time.time() - start
    print(f"\nTotal time: {total_time:.1f}s")

    db_size = os.path.getsize(args.db_path) if os.path.exists(args.db_path) else 0
    print(f"DB file size: {db_size / 1024 / 1024:.1f} MB")

    print("\nDone!")
    db.close()


if __name__ == "__main__":
    main()
