"""
Company enricher — uses WebSearchTool to fetch live salary/interview data
from the internet and enrich company profiles in knowledge.db.

Usage:
    from seed_data.company_enricher import enrich_companies
    enriched = enrich_companies(company_names, cache_dir="seed_data/cache")
"""

from __future__ import annotations

import json
import os
import time
from typing import List, Dict, Optional


def enrich_companies(
    company_names: List[str],
    cache_dir: str = "seed_data/cache",
    skip_cached: bool = True,
) -> Dict[str, dict]:
    """
    Enrich company profiles with live data from web search.

    Uses the existing WebSearchTool (Tavily API + DuckDuckGo fallback)
    to search for salary ranges, interview processes, and culture data.

    Args:
        company_names: List of company names to enrich
        cache_dir: Directory to cache results as JSON
        skip_cached: If True, skip companies already in cache

    Returns:
        Dict mapping company_name -> enriched data dict
    """
    try:
        from tools.web_search import WebSearchTool
    except ImportError:
        print("  [Enricher] WebSearchTool not available. Skipping enrichment.")
        return {}

    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "companies_enriched.json")

    # Load existing cache
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)

    search = WebSearchTool()
    enriched = {}

    for i, company in enumerate(company_names):
        if skip_cached and company in cache:
            enriched[company] = cache[company]
            continue

        print(f"  [{i+1}/{len(company_names)}] Enriching {company}...")

        data = {"salary_info": "", "interview_info": "", "culture_info": ""}

        try:
            # Search 1: Salary data
            result = search.execute(
                query=f"{company} salary India 2025 2026 fresher experienced LPA CTC ambitionbox glassdoor",
                num_results=5,
            )
            if result.success:
                data["salary_info"] = result.data[:2000]

            time.sleep(2)  # Rate limiting

            # Search 2: Interview process
            result = search.execute(
                query=f"{company} interview process campus placement rounds 2025 2026 geeksforgeeks",
                num_results=5,
            )
            if result.success:
                data["interview_info"] = result.data[:2000]

            time.sleep(2)

        except Exception as e:
            print(f"    Error enriching {company}: {e}")

        enriched[company] = data
        cache[company] = data

        # Save cache incrementally
        with open(cache_file, "w") as f:
            json.dump(cache, f, indent=2)

    print(f"  Enriched {len(enriched)} companies")
    return enriched
