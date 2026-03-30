"""
Config Generator: Creates simulation config from graph + profiles.

Same as Debug Arena's config_generator.py —
LLM generates initial posts, hot topics, and per-agent behavior configs.

Stage 3 in the pipeline:
  Stage 1: Resume → Knowledge Graph
  Stage 2: Graph → Agent Profiles
  Stage 3: Profiles + Graph → Simulation Config  ← THIS
  Stage 4: Simulation runs with config
"""

from __future__ import annotations

import json
import random
from concurrent.futures import ThreadPoolExecutor

from llm_client import LLMClient

EVENT_CONFIG_PROMPT = """You are a career intelligence simulation planner.

Given a user's career query, their resume data (as a knowledge graph), and the specialist agents
who will investigate, generate the simulation configuration:

1. initial_posts: Seed posts that kick off the arena discussion. Each post should represent
   an agent sharing their initial observation, hypothesis, or finding about the career question.
   - content: The forum post text (specific, data-oriented, actionable)
   - poster_type: "lead", "sub", or "contrarian"
   - poster_agent_id: The agent's user_id number

2. hot_topics: Key career topics that will drive the discussion.

3. narrative_direction: How the discussion should evolve across rounds.

## User's Career Question
{query}

## Companies Being Analyzed
{companies}

## Knowledge Graph Entities
{entity_list}

## Agent Roster (agent_id: name — summary)
{agent_list}

**Output valid JSON only:**
```json
{{
  "initial_posts": [
    {{
      "content": "Forum post text here — specific, data-oriented, with concrete numbers or observations",
      "poster_type": "lead",
      "poster_agent_id": 0
    }}
  ],
  "hot_topics": ["topic1", "topic2"],
  "narrative_direction": "Description of how discussion should evolve"
}}
```

Rules:
- Create 6-12 initial posts from different agents
- Posts should be SPECIFIC: include salary ranges, company names, skill assessments, market observations
- Each agent posts from their domain perspective (a compensation agent posts salary data, a culture agent posts work-life insights)
- Hot topics should be the key career questions the investigation needs to resolve
- At least 1 post should be CONTRARIAN — challenging an assumption or flagging a risk
- Posts should reference the user's actual resume data where relevant"""

AGENT_CONFIG_PROMPT = """You are configuring agent behavior for a career intelligence forum simulation.

For each agent, determine their activity patterns in the discussion.

## User's Question
{query}

## Companies
{companies}

## Agents
{agent_list}

For each agent, generate a config with:
- agent_id: matching the provided id
- entity_name: the entity name
- entity_type: the entity type
- activity_level: 0.0-1.0 (how frequently this agent participates)
  - Key analysts/specialists: 0.7-0.9
  - Supporting agents: 0.4-0.6
  - Peripheral agents: 0.2-0.4
- stance: "investigating", "advocate", "skeptic", "specialist", "synthesizer"
- influence_weight: 0.5-3.0 (how much weight their posts carry)
  - Domain experts: 2.0-3.0
  - Generalists: 1.0-1.5
  - Challengers: 1.5-2.0
- is_adversarial: true for ~20% of agents (designated challengers)
- interested_topics: list of topics this agent should focus on

**Output valid JSON only:**
```json
{{
  "agent_configs": [
    {{
      "agent_id": 0,
      "entity_name": "name",
      "entity_type": "type",
      "activity_level": 0.7,
      "stance": "investigating",
      "influence_weight": 1.5,
      "is_adversarial": false,
      "interested_topics": ["topic1"]
    }}
  ]
}}
```"""


def generate_config(
    llm: LLMClient,
    graph: dict,
    profiles: list[dict],
    query: str,
    companies: list[str] = None,
    on_progress=None,
) -> dict:
    """Generate simulation config from graph + profiles (Debug Arena Stage 3)."""

    def _progress(msg: str):
        if on_progress:
            on_progress(msg)

    companies = companies or []
    companies_str = ", ".join(companies) if companies else "General"

    entity_list = _format_entities(graph)
    agent_list = _format_agents(profiles)

    _progress("Generating initial posts and hot topics...")
    _progress("Generating agent behavior configs...")

    with ThreadPoolExecutor(max_workers=2) as pool:
        event_future = pool.submit(
            _generate_event_config, llm, query, companies_str, entity_list, agent_list
        )
        agent_future = pool.submit(
            _generate_agent_configs, llm, query, companies_str, agent_list
        )

        event_config = event_future.result()
        agent_configs = agent_future.result()

    _progress(
        f"Config ready: {len(event_config.get('initial_posts', []))} seed posts, "
        f"{len(event_config.get('hot_topics', []))} hot topics, "
        f"{len(agent_configs)} agent configs"
    )

    return {
        "event_config": event_config,
        "agent_configs": agent_configs,
    }


def _generate_event_config(
    llm: LLMClient, query: str, companies: str, entity_list: str, agent_list: str,
) -> dict:
    prompt = EVENT_CONFIG_PROMPT.format(
        query=query,
        companies=companies,
        entity_list=entity_list,
        agent_list=agent_list,
    )

    try:
        result = llm.generate_json(
            prompt=prompt,
            system_prompt="Generate simulation event configuration for a career intelligence forum.",
            temperature=0.5,
        )
        return result
    except Exception:
        return {
            "initial_posts": [],
            "hot_topics": [query[:50]],
            "narrative_direction": "Open investigation of the career question.",
        }


def _generate_agent_configs(llm: LLMClient, query: str, companies: str, agent_list: str) -> list[dict]:
    prompt = AGENT_CONFIG_PROMPT.format(
        query=query,
        companies=companies,
        agent_list=agent_list,
    )

    try:
        result = llm.generate_json(
            prompt=prompt,
            system_prompt="Generate agent behavior configurations for a career intelligence simulation.",
            temperature=0.3,
        )
        return result.get("agent_configs", [])
    except Exception:
        return []


def _format_entities(graph: dict) -> str:
    nodes = graph.get("nodes", [])
    if not nodes:
        return "No entities extracted."

    lines = []
    for n in nodes:
        labels = n.get("labels", ["Entity"])
        label = next((l for l in labels if l != "Entity"), "Entity")
        attrs = n.get("attributes", {})
        relevance = attrs.get("relevance", "medium")
        lines.append(f"  [{label}] {n['name']} (relevance: {relevance})")
    return "\n".join(lines)


def _format_agents(profiles: list[dict]) -> str:
    if not profiles:
        return "No agents."

    lines = []
    for p in profiles:
        uid = p.get("user_id", "?")
        name = p.get("name", "Unknown")
        bio = p.get("bio", "")[:100]
        lines.append(f"  {uid}: {name} — {bio}")
    return "\n".join(lines)
