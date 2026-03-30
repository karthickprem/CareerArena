"""
Question augmenter — uses LLM to generate company-specific interview questions
that can't be easily curated by hand.

Usage:
    from seed_data.question_augmenter import generate_company_questions
    questions = generate_company_questions(companies, cache_dir="seed_data/cache")
"""

from __future__ import annotations

import json
import os
from typing import List, Dict


GENERATION_PROMPT = """Generate {count} realistic interview questions that {company_name} ({industry})
specifically asks in campus placement drives and lateral hiring at Indian engineering colleges.

For each question, return a JSON object with these exact fields:
- "domain": one of "software_engineering", "behavioral", "aptitude", "data_science"
- "topic": specific topic (e.g., "coding", "system_design", "leadership_principles", "aptitude")
- "difficulty": "easy", "medium", or "hard"
- "level": "fresher" or "mid"
- "question_text": exactly how a real interviewer at {company_name} would phrase this question
- "follow_ups": array of 2-3 natural follow-up questions
- "expected_points": array of 3-5 key points in a good answer
- "scoring_rubric": object with keys "1-3", "4-5", "6-7", "8-10" mapping to descriptions
- "company_specific": "{company_name}"
- "tags": array of relevant tags

Focus on what makes {company_name}'s interviews DIFFERENT from generic interviews.
{company_context}

Return a JSON array of {count} question objects. Return ONLY the JSON array, no other text."""


def generate_company_questions(
    companies: List[dict],
    count_per_company: int = 15,
    cache_dir: str = "seed_data/cache",
    skip_cached: bool = True,
) -> List[dict]:
    """
    Generate company-specific interview questions using LLM.

    Args:
        companies: List of company profile dicts (must have company_name, industry)
        count_per_company: How many questions to generate per company
        cache_dir: Directory to cache generated questions
        skip_cached: If True, skip companies already in cache

    Returns:
        List of question dicts ready for bulk_add_questions()
    """
    try:
        from llm_client import LLMClient
    except ImportError:
        print("  [Augmenter] LLMClient not available. Skipping LLM augmentation.")
        return []

    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "questions_generated.json")

    # Load existing cache
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)

    client = LLMClient()
    all_questions = []

    for i, company in enumerate(companies):
        name = company["company_name"]

        if skip_cached and name in cache:
            all_questions.extend(cache[name])
            continue

        print(f"  [{i+1}/{len(companies)}] Generating questions for {name}...")

        context_parts = []
        if company.get("hiring_bar"):
            context_parts.append(f"Hiring bar: {company['hiring_bar']}")
        if company.get("evaluation_priorities"):
            priorities = company["evaluation_priorities"]
            if isinstance(priorities, list):
                context_parts.append(f"They prioritize: {', '.join(priorities)}")
        if company.get("culture_notes"):
            context_parts.append(f"Culture: {company['culture_notes'][:200]}")

        company_context = "\n".join(context_parts) if context_parts else ""

        prompt = GENERATION_PROMPT.format(
            count=count_per_company,
            company_name=name,
            industry=company.get("industry", "Technology"),
            company_context=company_context,
        )

        try:
            response = client.chat(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini",
                temperature=0.8,
            )

            content = response.strip()
            # Extract JSON array from response
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]

            questions = json.loads(content)
            if isinstance(questions, list):
                # Ensure company_specific is set
                for q in questions:
                    q["company_specific"] = name
                cache[name] = questions
                all_questions.extend(questions)
                print(f"    Generated {len(questions)} questions")
            else:
                print(f"    Unexpected response format for {name}")

        except json.JSONDecodeError as e:
            print(f"    JSON parse error for {name}: {e}")
        except Exception as e:
            print(f"    Error generating for {name}: {e}")

        # Save cache incrementally
        with open(cache_file, "w") as f:
            json.dump(cache, f, indent=2)

    print(f"  Total LLM-generated questions: {len(all_questions)}")
    return all_questions
