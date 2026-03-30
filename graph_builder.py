"""
Knowledge Graph Builder — decomposes resume + query into a rich career graph.

Mirrors Debug Arena's graph_builder.py but for career intelligence.

Pipeline:
  1. Resume text + query → LLM extraction → entities + edges
  2. Multiple chunks processed in parallel (for long resumes)
  3. Entities merged by name
  4. Graph persisted to DB

Entity types (career ontology):
  Skill, Technology, Company, Role, Project, Industry, Domain,
  Education, Certification, Achievement, Tool, Framework, Language,
  Methodology, SoftSkill, MarketSegment, CareerGoal, TargetCompany
"""

from __future__ import annotations

import json
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Optional

from llm_client import LLMClient

CAREER_ONTOLOGY = {
    "entity_types": [
        "Skill", "Technology", "Company", "Role", "Project", "Industry",
        "Domain", "Education", "Certification", "Achievement", "Tool",
        "Framework", "ProgrammingLanguage", "Methodology", "SoftSkill",
        "MarketSegment", "CareerGoal", "TargetCompany", "Experience",
        "Platform", "Database", "CloudService", "Person",
    ],
    "edge_types": [
        "HAS_SKILL", "WORKED_AT", "HELD_ROLE", "BUILT_PROJECT",
        "STUDIED_AT", "CERTIFIED_IN", "USES_TECHNOLOGY", "PART_OF_DOMAIN",
        "REQUIRES_SKILL", "COMPETES_WITH", "TARGETS_ROLE",
        "LED_TEAM", "MENTORED", "CONTRIBUTED_TO", "PROFICIENT_IN",
        "EXPERIENCED_WITH", "WANTS_TO_JOIN", "SIMILAR_TO",
        "PREREQUISITE_FOR", "COMPLEMENTS",
    ],
}

CHUNK_SIZE = 12000
CHUNK_OVERLAP = 1500
MAX_CHUNKS = 20

EXTRACTION_PROMPT = """You are a career intelligence knowledge graph extractor.

## Career Ontology
Entity types: {entity_types}
Edge types: {edge_types}

## Rules
1. Extract ALL entities from the resume/query — be EXHAUSTIVE
2. For each skill, technology, framework, tool — create a SEPARATE entity
3. For each company mentioned (past employers, target companies) — create a SEPARATE entity
4. For each role/position held — create a SEPARATE entity
5. For each project or achievement — create a SEPARATE entity
6. Create edges showing relationships between entities
7. Include the user's career goals and target companies from the query
8. Aim for 30-60 entities for a typical resume + query
9. Every entity MUST have a descriptive summary (1-2 sentences)
10. Classify entities correctly — don't lump skills and tools together

## Output Format
Return valid JSON only:
```json
{{
  "entities": [
    {{
      "name": "Entity Name",
      "type": "EntityType",
      "summary": "1-2 sentence description of this entity in the candidate's context",
      "attributes": {{"proficiency": "expert|advanced|intermediate|beginner", "years": 5, "relevance": "high|medium|low"}}
    }}
  ],
  "edges": [
    {{
      "source": "Entity Name 1",
      "target": "Entity Name 2",
      "relation_type": "EDGE_TYPE",
      "fact": "Brief description of the relationship"
    }}
  ]
}}
```"""

SYSTEM_PROMPT = (
    "You are a career intelligence system that extracts detailed knowledge graphs "
    "from resumes and career queries. Be exhaustive — extract every skill, technology, "
    "company, role, project, domain, and career goal. Output valid JSON only."
)


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE,
                overlap: int = CHUNK_OVERLAP, max_chunks: int = MAX_CHUNKS) -> List[str]:
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    pos = 0
    while pos < len(text) and len(chunks) < max_chunks:
        end = min(pos + chunk_size, len(text))
        if end < len(text):
            for sep in ["\n\n", "\n", ". ", " "]:
                brk = text.rfind(sep, pos + chunk_size // 2, end)
                if brk > pos:
                    end = brk + len(sep)
                    break
        chunks.append(text[pos:end])
        pos = end - overlap if end < len(text) else end
    return chunks


def _extract_chunk(llm: LLMClient, chunk: str, chunk_idx: int,
                   total_chunks: int) -> Dict[str, Any]:
    prefix = f"[Document chunk {chunk_idx + 1}/{total_chunks}] " if total_chunks > 1 else ""
    prompt = f"{prefix}Extract the career knowledge graph from this text:\n\n{chunk}"

    try:
        result = llm.generate_json(
            prompt=prompt,
            system_prompt=EXTRACTION_PROMPT.format(
                entity_types=", ".join(CAREER_ONTOLOGY["entity_types"]),
                edge_types=", ".join(CAREER_ONTOLOGY["edge_types"]),
            ),
            temperature=0.2,
        )
        return result
    except Exception as e:
        print(f"  Graph extraction error (chunk {chunk_idx}): {e}")
        return {"entities": [], "edges": []}


def _merge_extractions(results: List[Dict]) -> tuple:
    entity_map = {}
    all_edges = []

    for r in results:
        for ent in r.get("entities", []):
            name = ent.get("name", "").strip()
            if not name:
                continue
            key = name.lower()
            if key in entity_map:
                existing = entity_map[key]
                new_summary = ent.get("summary", "")
                if len(new_summary) > len(existing.get("summary", "")):
                    existing["summary"] = new_summary
                for k, v in ent.get("attributes", {}).items():
                    existing.setdefault("attributes", {}).setdefault(k, v)
            else:
                entity_map[key] = {
                    "name": name,
                    "type": ent.get("type", "Skill"),
                    "summary": ent.get("summary", ""),
                    "attributes": ent.get("attributes", {}),
                }

        for edge in r.get("edges", []):
            src = edge.get("source", "").strip()
            tgt = edge.get("target", "").strip()
            if src and tgt:
                all_edges.append(edge)

    seen_edges = set()
    deduped_edges = []
    for e in all_edges:
        key = (e["source"].lower(), e["target"].lower(), e.get("relation_type", ""))
        if key not in seen_edges:
            seen_edges.add(key)
            deduped_edges.append(e)

    return list(entity_map.values()), deduped_edges


def build_graph(
    llm: LLMClient,
    resume_text: str,
    query: str = "",
    companies: List[str] = None,
    db=None,
    on_progress: Optional[Callable] = None,
) -> Dict[str, Any]:
    """Extract a career knowledge graph from resume + query.

    Returns:
        dict with 'nodes' (list of entity dicts with uuid) and 'edges' (list of edge dicts with uuid)
    """
    full_text = resume_text
    if query:
        full_text += f"\n\n## Career Query\n{query}"
    if companies:
        full_text += f"\n\n## Target Companies to Analyze\n{', '.join(companies)}"

    chunks = _chunk_text(full_text)
    total = len(chunks)

    if on_progress:
        on_progress(f"Extracting knowledge graph from {total} chunk(s)...")

    if total == 1:
        results = [_extract_chunk(llm, chunks[0], 0, 1)]
    else:
        results = [None] * total
        with ThreadPoolExecutor(max_workers=min(20, total)) as pool:
            futures = {
                pool.submit(_extract_chunk, llm, chunk, i, total): i
                for i, chunk in enumerate(chunks)
            }
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    results[idx] = future.result()
                except Exception:
                    results[idx] = {"entities": [], "edges": []}
        results = [r for r in results if r is not None]

    entities, edges = _merge_extractions(results)

    if companies:
        for company in companies:
            key = company.lower()
            exists = any(e["name"].lower() == key for e in entities)
            if not exists:
                entities.append({
                    "name": company,
                    "type": "TargetCompany",
                    "summary": f"Target company from user's career query: {company}",
                    "attributes": {"relevance": "high", "source": "query"},
                })

    name_to_uuid = {}
    nodes = []
    for ent in entities:
        uid = uuid.uuid4().hex[:12]
        name_to_uuid[ent["name"].lower()] = uid
        nodes.append({
            "uuid": uid,
            "name": ent["name"],
            "labels": ["Entity", ent.get("type", "Skill")],
            "summary": ent.get("summary", ""),
            "attributes": ent.get("attributes", {}),
        })

    edge_list = []
    for e in edges:
        src_uuid = name_to_uuid.get(e["source"].lower())
        tgt_uuid = name_to_uuid.get(e["target"].lower())
        if src_uuid and tgt_uuid:
            edge_list.append({
                "uuid": uuid.uuid4().hex[:12],
                "source_node_uuid": src_uuid,
                "target_node_uuid": tgt_uuid,
                "name": e.get("relation_type", "RELATED_TO"),
                "fact": e.get("fact", ""),
            })

    graph = {
        "nodes": nodes,
        "edges": edge_list,
        "metadata": {
            "entity_count": len(nodes),
            "edge_count": len(edge_list),
            "chunks_processed": total,
            "resume_length": len(resume_text),
            "query": query[:200],
        },
    }

    if on_progress:
        on_progress(f"Knowledge graph: {len(nodes)} entities, {len(edge_list)} edges")

    return graph


def get_entity_context(graph: Dict, entity_name: str) -> str:
    """Build rich context for an entity — for profile generation."""
    node = None
    for n in graph["nodes"]:
        if n["name"].lower() == entity_name.lower():
            node = n
            break

    if not node:
        return f"Entity: {entity_name} (no additional context available)"

    uuid_to_name = {n["uuid"]: n["name"] for n in graph["nodes"]}

    lines = [
        f"## {node['name']} ({', '.join(node['labels'])})",
        f"Summary: {node.get('summary', 'N/A')}",
    ]

    attrs = node.get("attributes", {})
    if attrs:
        lines.append(f"Attributes: {json.dumps(attrs)}")

    related = []
    for edge in graph["edges"]:
        if edge["source_node_uuid"] == node["uuid"]:
            target = uuid_to_name.get(edge["target_node_uuid"], "?")
            related.append(f"  → {edge['name']} → {target}: {edge.get('fact', '')}")
        elif edge["target_node_uuid"] == node["uuid"]:
            source = uuid_to_name.get(edge["source_node_uuid"], "?")
            related.append(f"  ← {source} → {edge['name']}: {edge.get('fact', '')}")

    if related:
        lines.append("\nRelationships:")
        lines.extend(related[:15])

    nearby = [n for n in graph["nodes"]
              if n["uuid"] != node["uuid"] and n["labels"][-1] == node["labels"][-1]]
    if nearby:
        lines.append(f"\nSimilar entities: {', '.join(n['name'] for n in nearby[:10])}")

    return "\n".join(lines)


def classify_entity_priority(entity: Dict) -> int:
    """Priority-rank a graph entity for Tier 2 specialist assignment.

    Lower number = higher priority (gets a specialist agent first).
    All graph entities become Tier 2 agents; this just controls ordering.
    """
    etype = entity.get("type", entity.get("labels", ["", "Skill"])[-1])
    attrs = entity.get("attributes", {})
    relevance = attrs.get("relevance", "medium")

    priority_1 = {"TargetCompany", "CareerGoal", "Company", "Role", "Experience"}
    priority_2 = {"Domain", "Industry", "MarketSegment", "Project", "Achievement"}
    priority_3 = {"Skill", "Technology", "Framework", "ProgrammingLanguage", "Tool"}
    priority_4 = {"Database", "CloudService", "Platform", "Methodology",
                  "SoftSkill", "Education", "Certification", "Person"}

    if etype in priority_1:
        base = 1
    elif etype in priority_2:
        base = 2
    elif etype in priority_3:
        base = 3
    elif etype in priority_4:
        base = 4
    else:
        base = 3

    if relevance == "high":
        base = max(1, base - 1)
    elif relevance == "low":
        base = min(4, base + 1)

    return base
