"""
CareerArena Database Layer — adapted from Debug Arena's SimulationDB.

Reuses the proven SQLite forum schema (posts, comments, memory, directives)
and adds career-specific tables (users, sessions, salary/company cache, outcomes).
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime
from typing import Optional, List, Dict


class CareerDB:
    def __init__(self, db_path: str = "career_arena.db"):
        self.db_path = db_path
        self._local = threading.local()
        self._init_schema()

    def _get_conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA foreign_keys=ON")
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
        return self._local.conn

    def _init_schema(self):
        conn = self._get_conn()
        conn.executescript("""
            -- ===========================================
            -- USER & SESSION TABLES (new for CareerArena)
            -- ===========================================

            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                name TEXT,
                resume_raw TEXT,
                resume_data JSON,
                preferences JSON,
                linkedin_url TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT REFERENCES users(id),
                query_text TEXT NOT NULL,
                query_type TEXT,
                resume_context JSON,
                companies_analyzed JSON,
                agents_activated JSON,
                debate_rounds INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',
                report JSON,
                created_at TEXT NOT NULL,
                completed_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
            CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);

            -- ===========================================
            -- ARENA TABLES (adapted from Debug Arena)
            -- ===========================================

            CREATE TABLE IF NOT EXISTS arena_posts (
                post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                agent_type TEXT DEFAULT 'fixed',
                parent_agent TEXT,
                topic TEXT,
                content TEXT NOT NULL,
                post_type TEXT DEFAULT 'finding',
                confidence REAL,
                evidence JSON,
                round_num INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                dislikes INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_arena_posts_session ON arena_posts(session_id);
            CREATE INDEX IF NOT EXISTS idx_arena_posts_topic ON arena_posts(topic);
            CREATE INDEX IF NOT EXISTS idx_arena_posts_agent ON arena_posts(agent_id);
            CREATE INDEX IF NOT EXISTS idx_arena_posts_round ON arena_posts(round_num);

            CREATE TABLE IF NOT EXISTS arena_comments (
                comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL REFERENCES arena_posts(post_id),
                parent_comment_id INTEGER,
                session_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                content TEXT NOT NULL,
                comment_type TEXT DEFAULT 'reply',
                round_num INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                dislikes INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (parent_comment_id) REFERENCES arena_comments(comment_id)
            );
            CREATE INDEX IF NOT EXISTS idx_arena_comments_post ON arena_comments(post_id);
            CREATE INDEX IF NOT EXISTS idx_arena_comments_parent ON arena_comments(parent_comment_id);
            CREATE INDEX IF NOT EXISTS idx_arena_comments_session ON arena_comments(session_id);

            CREATE TABLE IF NOT EXISTS follows (
                follower_id TEXT NOT NULL,
                followee_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (follower_id, followee_id, session_id)
            );

            -- ===========================================
            -- AGENT MEMORY (reused from Debug Arena)
            -- ===========================================

            CREATE TABLE IF NOT EXISTS agent_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                session_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                round_num INTEGER DEFAULT 0,
                memory_type TEXT NOT NULL,
                content TEXT NOT NULL,
                confidence TEXT,
                evidence JSON,
                source_tool TEXT,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_memory_session ON agent_memory(session_id);
            CREATE INDEX IF NOT EXISTS idx_memory_agent ON agent_memory(agent_id);
            CREATE INDEX IF NOT EXISTS idx_memory_type ON agent_memory(memory_type);
            CREATE INDEX IF NOT EXISTS idx_memory_user ON agent_memory(user_id);

            -- ===========================================
            -- DIRECTIVES (reused from Debug Arena)
            -- ===========================================

            CREATE TABLE IF NOT EXISTS directives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                target_agent_id TEXT,
                target_agent_name TEXT,
                task TEXT NOT NULL,
                priority TEXT DEFAULT 'high',
                status TEXT DEFAULT 'pending',
                assigned_round INTEGER,
                completed_round INTEGER,
                result TEXT,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_directives_session ON directives(session_id);
            CREATE INDEX IF NOT EXISTS idx_directives_agent ON directives(target_agent_id);
            CREATE INDEX IF NOT EXISTS idx_directives_status ON directives(status);

            -- ===========================================
            -- AGENT PROFILES (adapted from Debug Arena)
            -- ===========================================

            CREATE TABLE IF NOT EXISTS agent_profiles (
                agent_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                agent_type TEXT NOT NULL,
                parent_agent TEXT,
                persona TEXT,
                topic TEXT,
                company TEXT,
                cognitive_style TEXT,
                is_adversarial INTEGER DEFAULT 0,
                config JSON,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_profiles_session ON agent_profiles(session_id);

            -- ===========================================
            -- CAREER-SPECIFIC CACHE TABLES (new)
            -- ===========================================

            CREATE TABLE IF NOT EXISTS salary_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                level TEXT,
                city TEXT,
                salary_data JSON,
                source TEXT,
                scraped_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_salary_company ON salary_cache(company, role);

            CREATE TABLE IF NOT EXISTS company_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT UNIQUE NOT NULL,
                company_data JSON,
                last_updated TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS interview_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT,
                level TEXT,
                pattern_data JSON,
                source TEXT DEFAULT 'scraped',
                confidence REAL DEFAULT 0.5,
                last_updated TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_interview_company ON interview_patterns(company);

            -- ===========================================
            -- OUTCOME TRACKING (the data moat)
            -- ===========================================

            CREATE TABLE IF NOT EXISTS outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT REFERENCES users(id),
                session_id TEXT,
                company TEXT,
                role TEXT,
                recommendation TEXT,
                outcome TEXT,
                outcome_details JSON,
                reported_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_outcomes_user ON outcomes(user_id);

            -- ===========================================
            -- INTERVIEW TABLES (Panel Interview Platform)
            -- ===========================================

            CREATE TABLE IF NOT EXISTS interview_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                interview_type TEXT NOT NULL DEFAULT 'panel',
                role TEXT NOT NULL DEFAULT '',
                company TEXT NOT NULL DEFAULT '',
                difficulty TEXT NOT NULL DEFAULT 'realistic',
                panel_size INTEGER NOT NULL DEFAULT 3,
                status TEXT NOT NULL DEFAULT 'setup',
                config_json JSON,
                panel_json JSON,
                total_turns INTEGER DEFAULT 0,
                max_turns INTEGER DEFAULT 30,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE INDEX IF NOT EXISTS idx_interview_sessions_user ON interview_sessions(user_id);
            CREATE INDEX IF NOT EXISTS idx_interview_sessions_status ON interview_sessions(status);

            CREATE TABLE IF NOT EXISTS interview_turns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL REFERENCES interview_sessions(id),
                turn_number INTEGER NOT NULL,
                speaker TEXT NOT NULL,
                speaker_role TEXT DEFAULT '',
                content TEXT NOT NULL,
                turn_type TEXT NOT NULL DEFAULT 'question',
                metadata JSON,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_interview_turns_session ON interview_turns(session_id);

            CREATE TABLE IF NOT EXISTS interview_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL REFERENCES interview_sessions(id),
                evaluator_agent TEXT NOT NULL,
                evaluator_role TEXT DEFAULT '',
                dimension TEXT NOT NULL,
                score REAL NOT NULL,
                max_score REAL NOT NULL DEFAULT 10.0,
                evidence TEXT,
                feedback TEXT,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_interview_scores_session ON interview_scores(session_id);

            -- ===========================================
            -- ACTION LOG
            -- ===========================================

            CREATE TABLE IF NOT EXISTS agent_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                round_num INTEGER NOT NULL,
                agent_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                action_type TEXT NOT NULL,
                target_id INTEGER,
                content TEXT,
                thinking TEXT,
                tool_results TEXT,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_actions_session ON agent_actions(session_id);
            CREATE INDEX IF NOT EXISTS idx_actions_agent ON agent_actions(agent_id);

            -- ===========================================
            -- SCREENING TABLES (Multi-Round V2)
            -- ===========================================

            CREATE TABLE IF NOT EXISTS screening_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                resume_data JSON,
                candidate_profile JSON,
                status TEXT DEFAULT 'active',
                questions_asked INTEGER DEFAULT 0,
                coverage JSON,
                created_at TEXT NOT NULL,
                completed_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_screening_status ON screening_sessions(status);

            CREATE TABLE IF NOT EXISTS screening_turns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL REFERENCES screening_sessions(id),
                turn_number INTEGER NOT NULL,
                speaker TEXT NOT NULL,
                content TEXT NOT NULL,
                analysis JSON,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_screening_turns_session ON screening_turns(session_id);

            -- ===========================================
            -- INTERVIEW ROUNDS (Multi-Round V2)
            -- ===========================================

            CREATE TABLE IF NOT EXISTS interview_rounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL REFERENCES interview_sessions(id),
                round_num INTEGER NOT NULL,
                interviewer_name TEXT NOT NULL,
                interviewer_role TEXT NOT NULL,
                round_type TEXT NOT NULL,
                focus_areas JSON,
                max_questions INTEGER DEFAULT 8,
                questions_asked INTEGER DEFAULT 0,
                is_final INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',
                forum_digest_used TEXT,
                started_at TEXT,
                completed_at TEXT,
                UNIQUE(session_id, round_num)
            );
            CREATE INDEX IF NOT EXISTS idx_interview_rounds_session ON interview_rounds(session_id);
            CREATE INDEX IF NOT EXISTS idx_interview_rounds_status ON interview_rounds(status);
        """)

        # Add V2 columns to interview_sessions (safe to re-run)
        for col_sql in [
            "ALTER TABLE interview_sessions ADD COLUMN screening_session_id TEXT",
            "ALTER TABLE interview_sessions ADD COLUMN round_plan JSON",
            "ALTER TABLE interview_sessions ADD COLUMN current_round INTEGER DEFAULT 0",
            "ALTER TABLE interview_sessions ADD COLUMN total_rounds INTEGER DEFAULT 0",
            "ALTER TABLE interview_sessions ADD COLUMN candidate_model_json TEXT",
        ]:
            try:
                conn.execute(col_sql)
            except sqlite3.OperationalError:
                pass  # Column already exists

        conn.commit()

    # =====================================================
    # USER MANAGEMENT
    # =====================================================

    def create_user(self, user_id: str, email: str = "", name: str = "") -> dict:
        conn = self._get_conn()
        now = datetime.now().isoformat()
        conn.execute(
            "INSERT OR IGNORE INTO users (id, email, name, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, email, name, now, now),
        )
        conn.commit()
        return self.get_user(user_id)

    def get_user(self, user_id: str) -> Optional[dict]:
        row = self._get_conn().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

    def update_user_resume(self, user_id: str, resume_raw: str, resume_data: dict) -> None:
        conn = self._get_conn()
        conn.execute(
            "UPDATE users SET resume_raw = ?, resume_data = ?, updated_at = ? WHERE id = ?",
            (resume_raw, json.dumps(resume_data), datetime.now().isoformat(), user_id),
        )
        conn.commit()

    def update_user_preferences(self, user_id: str, preferences: dict) -> None:
        conn = self._get_conn()
        conn.execute(
            "UPDATE users SET preferences = ?, updated_at = ? WHERE id = ?",
            (json.dumps(preferences), datetime.now().isoformat(), user_id),
        )
        conn.commit()

    # =====================================================
    # SESSION MANAGEMENT
    # =====================================================

    def create_session(self, session_id: str, user_id: str, query_text: str,
                       query_type: str = "", resume_context: dict = None) -> dict:
        conn = self._get_conn()
        now = datetime.now().isoformat()
        conn.execute(
            "INSERT INTO sessions (id, user_id, query_text, query_type, resume_context, status, created_at) "
            "VALUES (?, ?, ?, ?, ?, 'running', ?)",
            (session_id, user_id, query_text, query_type,
             json.dumps(resume_context or {}), now),
        )
        conn.commit()
        return self.get_session(session_id)

    def get_session(self, session_id: str) -> Optional[dict]:
        row = self._get_conn().execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        return dict(row) if row else None

    def update_session(self, session_id: str, **kwargs) -> None:
        conn = self._get_conn()
        sets = []
        vals = []
        for k, v in kwargs.items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v)
            sets.append(f"{k} = ?")
            vals.append(v)
        vals.append(session_id)
        conn.execute(f"UPDATE sessions SET {', '.join(sets)} WHERE id = ?", vals)
        conn.commit()

    def complete_session(self, session_id: str, report: dict) -> None:
        self.update_session(
            session_id,
            status="completed",
            report=report,
            completed_at=datetime.now().isoformat(),
        )

    def get_user_sessions(self, user_id: str, limit: int = 20) -> list[dict]:
        rows = self._get_conn().execute(
            "SELECT * FROM sessions WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    # =====================================================
    # ARENA POSTS (adapted from Debug Arena's posts)
    # =====================================================

    def create_post(self, session_id: str, agent_id: str, agent_name: str,
                    content: str, topic: str = "general", post_type: str = "finding",
                    agent_type: str = "fixed", parent_agent: str = "",
                    confidence: float = None, evidence: list = None,
                    round_num: int = 0) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO arena_posts (session_id, agent_id, agent_name, agent_type, "
            "parent_agent, topic, content, post_type, confidence, evidence, round_num, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (session_id, agent_id, agent_name, agent_type, parent_agent, topic,
             content, post_type, confidence, json.dumps(evidence or []),
             round_num, datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_post(self, post_id: int) -> Optional[dict]:
        row = self._get_conn().execute(
            "SELECT * FROM arena_posts WHERE post_id = ?", (post_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_session_posts(self, session_id: str, topic: str = None) -> list[dict]:
        conn = self._get_conn()
        if topic:
            rows = conn.execute(
                "SELECT * FROM arena_posts WHERE session_id = ? AND topic = ? ORDER BY post_id",
                (session_id, topic),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM arena_posts WHERE session_id = ? ORDER BY post_id",
                (session_id,),
            ).fetchall()
        return [dict(r) for r in rows]

    def like_post(self, post_id: int) -> None:
        conn = self._get_conn()
        conn.execute("UPDATE arena_posts SET likes = likes + 1 WHERE post_id = ?", (post_id,))
        conn.commit()

    def dislike_post(self, post_id: int) -> None:
        conn = self._get_conn()
        conn.execute("UPDATE arena_posts SET dislikes = dislikes + 1 WHERE post_id = ?", (post_id,))
        conn.commit()

    # =====================================================
    # ARENA COMMENTS (adapted from Debug Arena)
    # =====================================================

    def create_comment(self, post_id: int, session_id: str, agent_id: str,
                       agent_name: str, content: str, comment_type: str = "reply",
                       parent_comment_id: int = None, round_num: int = 0) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO arena_comments (post_id, parent_comment_id, session_id, agent_id, "
            "agent_name, content, comment_type, round_num, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (post_id, parent_comment_id, session_id, agent_id, agent_name,
             content, comment_type, round_num, datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_comments_for_post(self, post_id: int) -> list[dict]:
        rows = self._get_conn().execute(
            "SELECT * FROM arena_comments WHERE post_id = ? ORDER BY comment_id",
            (post_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def like_comment(self, comment_id: int) -> None:
        conn = self._get_conn()
        conn.execute("UPDATE arena_comments SET likes = likes + 1 WHERE comment_id = ?", (comment_id,))
        conn.commit()

    def dislike_comment(self, comment_id: int) -> None:
        conn = self._get_conn()
        conn.execute("UPDATE arena_comments SET dislikes = dislikes + 1 WHERE comment_id = ?", (comment_id,))
        conn.commit()

    # =====================================================
    # FOLLOWS (reused from Debug Arena)
    # =====================================================

    def follow(self, follower_id: str, followee_id: str, session_id: str) -> None:
        conn = self._get_conn()
        conn.execute(
            "INSERT OR IGNORE INTO follows (follower_id, followee_id, session_id, created_at) "
            "VALUES (?, ?, ?, ?)",
            (follower_id, followee_id, session_id, datetime.now().isoformat()),
        )
        conn.commit()

    def get_following(self, agent_id: str, session_id: str) -> list[str]:
        rows = self._get_conn().execute(
            "SELECT followee_id FROM follows WHERE follower_id = ? AND session_id = ?",
            (agent_id, session_id),
        ).fetchall()
        return [r["followee_id"] for r in rows]

    # =====================================================
    # AGENT MEMORY (reused from Debug Arena)
    # =====================================================

    def save_memory(self, session_id: str, agent_id: str, agent_name: str,
                    round_num: int, memory_type: str, content: str,
                    user_id: str = "", confidence: str = "",
                    evidence: list = None, source_tool: str = "") -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO agent_memory (user_id, session_id, agent_id, agent_name, round_num, "
            "memory_type, content, confidence, evidence, source_tool, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, session_id, agent_id, agent_name, round_num, memory_type,
             content, confidence, json.dumps(evidence or []),
             source_tool, datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_agent_memories(self, agent_id: str, session_id: str = None,
                           memory_type: str = None, limit: int = 20) -> list[dict]:
        conn = self._get_conn()
        query = "SELECT * FROM agent_memory WHERE agent_id = ?"
        params = [agent_id]
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        if memory_type:
            query += " AND memory_type = ?"
            params.append(memory_type)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def get_latest_hypothesis(self, agent_id: str, session_id: str) -> Optional[dict]:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT * FROM agent_memory WHERE agent_id = ? AND session_id = ? "
            "AND memory_type = 'hypothesis' ORDER BY id DESC LIMIT 1",
            (agent_id, session_id),
        ).fetchone()
        return dict(row) if row else None

    def search_memories(self, query: str, session_id: str = None, limit: int = 15) -> list[dict]:
        conn = self._get_conn()
        q = f"%{query}%"
        if session_id:
            rows = conn.execute(
                "SELECT * FROM agent_memory WHERE content LIKE ? AND session_id = ? "
                "ORDER BY id DESC LIMIT ?",
                (q, session_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM agent_memory WHERE content LIKE ? ORDER BY id DESC LIMIT ?",
                (q, limit),
            ).fetchall()
        return [dict(r) for r in rows]

    # =====================================================
    # DIRECTIVES (reused from Debug Arena)
    # =====================================================

    def save_directive(self, session_id: str, target_agent_id: str,
                       target_agent_name: str, task: str,
                       priority: str = "high", assigned_round: int = 0) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO directives (session_id, target_agent_id, target_agent_name, "
            "task, priority, status, assigned_round, created_at) "
            "VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)",
            (session_id, target_agent_id, target_agent_name, task, priority,
             assigned_round, datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_pending_directives(self, session_id: str, agent_id: str = None,
                                agent_name: str = None) -> list[dict]:
        conn = self._get_conn()
        query = "SELECT * FROM directives WHERE session_id = ? AND status = 'pending'"
        params = [session_id]
        if agent_id:
            query += " AND target_agent_id = ?"
            params.append(agent_id)
        elif agent_name:
            query += " AND target_agent_name = ?"
            params.append(agent_name)
        query += " ORDER BY priority DESC, id ASC"
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def complete_directive(self, directive_id: int, result: str, completed_round: int = 0) -> None:
        conn = self._get_conn()
        conn.execute(
            "UPDATE directives SET status = 'completed', result = ?, completed_round = ? WHERE id = ?",
            (result, completed_round, directive_id),
        )
        conn.commit()

    # =====================================================
    # AGENT PROFILES
    # =====================================================

    def save_agent_profile(self, agent_id: str, session_id: str, agent_name: str,
                           agent_type: str, persona: str, topic: str = "",
                           company: str = "", parent_agent: str = "",
                           cognitive_style: str = "", is_adversarial: bool = False,
                           config: dict = None) -> None:
        conn = self._get_conn()
        conn.execute(
            "INSERT OR REPLACE INTO agent_profiles (agent_id, session_id, agent_name, "
            "agent_type, parent_agent, persona, topic, company, cognitive_style, "
            "is_adversarial, config, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (agent_id, session_id, agent_name, agent_type, parent_agent, persona,
             topic, company, cognitive_style, int(is_adversarial),
             json.dumps(config or {}), datetime.now().isoformat()),
        )
        conn.commit()

    def get_session_agents(self, session_id: str) -> list[dict]:
        rows = self._get_conn().execute(
            "SELECT * FROM agent_profiles WHERE session_id = ? ORDER BY agent_type, agent_name",
            (session_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    # =====================================================
    # PERSONALIZED FEED (adapted from Debug Arena)
    # =====================================================

    def get_personalized_feed(self, session_id: str, agent_id: str,
                              agent_keywords: list[str] = None,
                              max_posts: int = 15, sample_size: int = 8) -> str:
        import random as _rng
        conn = self._get_conn()
        following = set(self.get_following(agent_id, session_id))

        posts = conn.execute(
            "SELECT p.*, (SELECT COUNT(*) FROM arena_comments c WHERE c.post_id = p.post_id) AS comment_count "
            "FROM arena_posts p WHERE p.session_id = ? ORDER BY p.post_id DESC LIMIT ?",
            (session_id, max_posts * 3),
        ).fetchall()

        already_commented = set()
        my_comments = conn.execute(
            "SELECT DISTINCT post_id FROM arena_comments WHERE agent_id = ? AND session_id = ?",
            (agent_id, session_id),
        ).fetchall()
        for row in my_comments:
            already_commented.add(row["post_id"])

        scored = []
        for p in posts:
            p = dict(p)
            score = 0.0
            if p["agent_id"] in following:
                score += 30
            score += min(p["likes"], 10) * 1.5
            score -= p["dislikes"]
            if agent_keywords:
                content_lower = p["content"].lower()
                for kw in agent_keywords:
                    if kw.lower() in content_lower:
                        score += 15

            cc = p["comment_count"]
            if cc > 5:
                score -= (cc - 5) * 3
            elif cc < 3:
                score += (3 - cc) * 5

            if p["post_id"] in already_commented:
                score -= 15
            if p["agent_id"] == agent_id:
                score -= 10

            score += p["post_id"] * 0.3
            scored.append((score, p))

        scored.sort(key=lambda x: x[0], reverse=True)
        candidate_pool = [p for _, p in scored[:max_posts]]

        if not candidate_pool:
            return "The arena is empty. No posts yet."

        if len(candidate_pool) > sample_size:
            sampled = _rng.sample(candidate_pool, sample_size)
        else:
            sampled = candidate_pool
        sampled.sort(key=lambda p: p["post_id"])

        max_comments_shown = 6
        lines = []
        for p in sampled:
            vote_str = f"+{p['likes']}" if p["dislikes"] == 0 else f"+{p['likes']}/-{p['dislikes']}"
            topic_tag = f" [{p['topic']}]" if p.get("topic") else ""
            type_tag = f" ({p['agent_type']})" if p.get("agent_type") else ""
            lines.append(
                f"[Post #{p['post_id']}]{topic_tag} by {p['agent_name']}{type_tag} "
                f"({vote_str}, {p['comment_count']} comments)"
            )
            lines.append(f"  {p['content']}")

            all_comments = self.get_comments_for_post(p["post_id"])
            children_map = {}
            roots = []
            for c in all_comments:
                pid = c.get("parent_comment_id")
                if pid:
                    children_map.setdefault(pid, []).append(c)
                else:
                    roots.append(c)

            shown_count = 0

            def _render_thread(comment, depth=0):
                nonlocal shown_count
                if shown_count >= max_comments_shown:
                    return
                shown_count += 1
                indent = "  " + "  " * depth
                prefix = "↩" if depth > 0 else "└─"
                c_vote = f"+{comment['likes']}" if comment["dislikes"] == 0 else f"+{comment['likes']}/-{comment['dislikes']}"
                ctype = f" [{comment['comment_type']}]" if comment.get("comment_type") else ""
                lines.append(
                    f"{indent}{prefix} [Comment #{comment['comment_id']}]{ctype} "
                    f"[{comment['agent_name']}] ({c_vote}): {comment['content']}"
                )
                for child in children_map.get(comment["comment_id"], []):
                    _render_thread(child, depth + 1)

            if len(all_comments) > max_comments_shown:
                lines.append(f"  ... ({len(all_comments) - max_comments_shown} earlier comments hidden)")
            for root in roots:
                _render_thread(root)
            lines.append("")
        return "\n".join(lines)

    # =====================================================
    # CACHE: SALARY DATA
    # =====================================================

    def cache_salary(self, company: str, role: str, salary_data: dict,
                     level: str = "", city: str = "", source: str = "") -> None:
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO salary_cache (company, role, level, city, salary_data, source, scraped_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (company, role, level, city, json.dumps(salary_data), source,
             datetime.now().isoformat()),
        )
        conn.commit()

    def get_cached_salary(self, company: str, role: str, max_age_days: int = 7) -> Optional[dict]:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT * FROM salary_cache WHERE company = ? AND role = ? "
            "ORDER BY scraped_at DESC LIMIT 1",
            (company, role),
        ).fetchone()
        if not row:
            return None
        row = dict(row)
        scraped = datetime.fromisoformat(row["scraped_at"])
        if (datetime.now() - scraped).days > max_age_days:
            return None
        return row

    # =====================================================
    # CACHE: COMPANY DATA
    # =====================================================

    def cache_company(self, company_name: str, company_data: dict) -> None:
        conn = self._get_conn()
        conn.execute(
            "INSERT OR REPLACE INTO company_cache (company_name, company_data, last_updated) "
            "VALUES (?, ?, ?)",
            (company_name, json.dumps(company_data), datetime.now().isoformat()),
        )
        conn.commit()

    def get_cached_company(self, company_name: str, max_age_days: int = 7) -> Optional[dict]:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT * FROM company_cache WHERE company_name = ? LIMIT 1",
            (company_name,),
        ).fetchone()
        if not row:
            return None
        row = dict(row)
        updated = datetime.fromisoformat(row["last_updated"])
        if (datetime.now() - updated).days > max_age_days:
            return None
        return row

    # =====================================================
    # INTERVIEW PATTERNS
    # =====================================================

    def save_interview_pattern(self, company: str, pattern_data: dict,
                                role: str = "", level: str = "",
                                source: str = "scraped", confidence: float = 0.5) -> None:
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO interview_patterns (company, role, level, pattern_data, "
            "source, confidence, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (company, role, level, json.dumps(pattern_data), source,
             confidence, datetime.now().isoformat()),
        )
        conn.commit()

    def get_interview_pattern(self, company: str, role: str = "") -> Optional[dict]:
        conn = self._get_conn()
        if role:
            row = conn.execute(
                "SELECT * FROM interview_patterns WHERE company = ? AND role = ? "
                "ORDER BY confidence DESC, last_updated DESC LIMIT 1",
                (company, role),
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT * FROM interview_patterns WHERE company = ? "
                "ORDER BY confidence DESC, last_updated DESC LIMIT 1",
                (company,),
            ).fetchone()
        return dict(row) if row else None

    # =====================================================
    # OUTCOME TRACKING (the data moat)
    # =====================================================

    def record_outcome(self, user_id: str, session_id: str, outcome: str,
                       company: str = "", role: str = "",
                       recommendation: str = "", outcome_details: dict = None) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO outcomes (user_id, session_id, company, role, recommendation, "
            "outcome, outcome_details, reported_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, session_id, company, role, recommendation, outcome,
             json.dumps(outcome_details or {}), datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    # =====================================================
    # ARENA TRANSCRIPT (adapted from Debug Arena)
    # =====================================================

    def build_transcript(self, session_id: str) -> str:
        posts = self.get_session_posts(session_id)
        lines = []
        for p in posts:
            vote_str = f"+{p['likes']}" if p["dislikes"] == 0 else f"+{p['likes']}/-{p['dislikes']}"
            topic_tag = f" [{p['topic']}]" if p.get("topic") else ""
            lines.append(
                f"[Post #{p['post_id']}]{topic_tag} by {p['agent_name']} "
                f"({p['agent_type']}) ({vote_str})"
            )
            lines.append(p["content"])

            all_comments = self.get_comments_for_post(p["post_id"])
            children_map = {}
            roots = []
            for c in all_comments:
                pid = c.get("parent_comment_id")
                if pid:
                    children_map.setdefault(pid, []).append(c)
                else:
                    roots.append(c)

            def _render(comment, depth=0):
                indent = "  " * (depth + 1)
                prefix = "↩ Reply" if depth > 0 else "Reply"
                ctype = f" [{comment['comment_type']}]" if comment.get("comment_type") else ""
                lines.append(
                    f"{indent}{prefix}{ctype} by {comment['agent_name']} "
                    f"(Comment #{comment['comment_id']}): {comment['content']}"
                )
                for child in children_map.get(comment["comment_id"], []):
                    _render(child, depth + 1)

            for root in roots:
                _render(root)
            lines.append("")
        return "\n".join(lines)

    # =====================================================
    # STATS
    # =====================================================

    def get_session_stats(self, session_id: str) -> dict:
        conn = self._get_conn()
        post_count = conn.execute(
            "SELECT COUNT(*) FROM arena_posts WHERE session_id = ?", (session_id,)
        ).fetchone()[0]
        comment_count = conn.execute(
            "SELECT COUNT(*) FROM arena_comments WHERE session_id = ?", (session_id,)
        ).fetchone()[0]
        agent_count = conn.execute(
            "SELECT COUNT(DISTINCT agent_id) FROM arena_posts WHERE session_id = ?", (session_id,)
        ).fetchone()[0]
        topics = conn.execute(
            "SELECT DISTINCT topic FROM arena_posts WHERE session_id = ? AND topic IS NOT NULL",
            (session_id,),
        ).fetchall()
        return {
            "total_posts": post_count,
            "total_comments": comment_count,
            "active_agents": agent_count,
            "topics": [r["topic"] for r in topics],
        }

    # =====================================================
    # METADATA
    # =====================================================

    def set_meta(self, key: str, value: str) -> None:
        conn = self._get_conn()
        conn.execute(
            "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)"
        )
        conn.execute("INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)", (key, value))
        conn.commit()

    def get_meta(self, key: str) -> Optional[str]:
        conn = self._get_conn()
        try:
            row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
            return row[0] if row else None
        except Exception:
            return None

    # =====================================================
    # AGENT ACTIONS, SEARCH, AND COMMENT THREADS
    # =====================================================

    def log_action(
        self,
        session_id: str,
        round_num: int,
        agent_id: str,
        agent_name: str,
        action_type: str,
        target_id: int = None,
        content: str = "",
        thinking: str = "",
        tool_results: str = "",
    ) -> None:
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO agent_actions (session_id, round_num, agent_id, agent_name, "
            "action_type, target_id, content, thinking, tool_results, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                session_id,
                round_num,
                agent_id,
                agent_name,
                action_type,
                target_id,
                content,
                thinking,
                tool_results,
                datetime.now().isoformat(),
            ),
        )
        conn.commit()

    def search_posts(self, session_id: str, query: str, limit: int = 10) -> str:
        conn = self._get_conn()
        query_like = f"%{query}%"
        posts = conn.execute(
            "SELECT * FROM arena_posts WHERE session_id = ? AND content LIKE ? "
            "ORDER BY likes DESC LIMIT ?",
            (session_id, query_like, limit),
        ).fetchall()
        comments = conn.execute(
            "SELECT c.*, p.agent_name AS post_author FROM arena_comments c "
            "JOIN arena_posts p ON c.post_id = p.post_id "
            "WHERE c.session_id = ? AND c.content LIKE ? ORDER BY c.likes DESC LIMIT ?",
            (session_id, query_like, limit),
        ).fetchall()
        lines = []
        if posts:
            lines.append(f"Found {len(posts)} posts matching '{query}':")
            for p in posts:
                p = dict(p)
                lines.append(
                    f"  [Post #{p['post_id']}] by {p['agent_name']}: {p['content'][:800]}"
                )
        if comments:
            lines.append(f"Found {len(comments)} comments matching '{query}':")
            for c in comments:
                c = dict(c)
                lines.append(
                    f"  [Comment on Post #{c['post_id']}] by {c['agent_name']}: "
                    f"{c['content'][:600]}"
                )
        if not lines:
            return f"No posts or comments found matching '{query}'."
        return "\n".join(lines)

    def get_all_agent_summaries(self, session_id: str) -> list:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT agent_id, agent_name, COUNT(*) as memory_count, "
            "MAX(round_num) as last_active_round "
            "FROM agent_memory WHERE session_id = ? GROUP BY agent_id ORDER BY memory_count DESC",
            (session_id,),
        ).fetchall()
        summaries = []
        for r in rows:
            r = dict(r)
            latest_hyp = self.get_latest_hypothesis(r["agent_id"], session_id)
            r["latest_hypothesis"] = latest_hyp["content"] if latest_hyp else None
            r["hypothesis_confidence"] = latest_hyp["confidence"] if latest_hyp else None
            summaries.append(r)
        return summaries

    def get_comment(self, comment_id: int) -> Optional[dict]:
        row = self._get_conn().execute(
            "SELECT * FROM arena_comments WHERE comment_id = ?", (comment_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_thread_chain(self, comment_id: int, max_depth: int = 10) -> list:
        chain = []
        cid = comment_id
        for _ in range(max_depth):
            c = self.get_comment(cid)
            if not c:
                break
            chain.append(c)
            if not c.get("parent_comment_id"):
                break
            cid = c["parent_comment_id"]
        return chain

    def get_replies_to_comment(self, comment_id: int) -> list:
        rows = self._get_conn().execute(
            "SELECT * FROM arena_comments WHERE parent_comment_id = ? ORDER BY comment_id",
            (comment_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    # =====================================================
    # INTERVIEW SESSION MANAGEMENT
    # =====================================================

    def create_interview_session(
        self,
        session_id: str,
        interview_type: str = "panel",
        role: str = "",
        company: str = "",
        difficulty: str = "realistic",
        panel_size: int = 3,
        config: dict = None,
        panel: list = None,
        user_id: str = None,
        max_turns: int = 30,
    ) -> dict:
        conn = self._get_conn()
        now = datetime.now().isoformat()
        conn.execute(
            "INSERT INTO interview_sessions "
            "(id, user_id, interview_type, role, company, difficulty, panel_size, "
            "status, config_json, panel_json, max_turns, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, 'setup', ?, ?, ?, ?)",
            (
                session_id, user_id, interview_type, role, company,
                difficulty, panel_size, json.dumps(config or {}),
                json.dumps(panel or []), max_turns, now,
            ),
        )
        conn.commit()
        return self.get_interview_session(session_id)

    def get_interview_session(self, session_id: str) -> Optional[dict]:
        row = self._get_conn().execute(
            "SELECT * FROM interview_sessions WHERE id = ?", (session_id,)
        ).fetchone()
        return dict(row) if row else None

    def update_interview_session(self, session_id: str, **kwargs) -> None:
        conn = self._get_conn()
        sets, vals = [], []
        for k, v in kwargs.items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v)
            sets.append(f"{k} = ?")
            vals.append(v)
        vals.append(session_id)
        conn.execute(
            f"UPDATE interview_sessions SET {', '.join(sets)} WHERE id = ?", vals
        )
        conn.commit()

    def start_interview(self, session_id: str) -> None:
        self.update_interview_session(
            session_id, status="active", started_at=datetime.now().isoformat()
        )

    def complete_interview(self, session_id: str) -> None:
        self.update_interview_session(
            session_id, status="completed", completed_at=datetime.now().isoformat()
        )

    def get_user_interviews(self, user_id: str, limit: int = 20) -> list:
        rows = self._get_conn().execute(
            "SELECT * FROM interview_sessions WHERE user_id = ? "
            "ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    # =====================================================
    # INTERVIEW TURNS
    # =====================================================

    def add_interview_turn(
        self,
        session_id: str,
        turn_number: int,
        speaker: str,
        content: str,
        turn_type: str = "question",
        speaker_role: str = "",
        metadata: dict = None,
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO interview_turns "
            "(session_id, turn_number, speaker, speaker_role, content, turn_type, metadata, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                session_id, turn_number, speaker, speaker_role,
                content, turn_type, json.dumps(metadata or {}),
                datetime.now().isoformat(),
            ),
        )
        conn.execute(
            "UPDATE interview_sessions SET total_turns = ? WHERE id = ?",
            (turn_number, session_id),
        )
        conn.commit()
        return cur.lastrowid

    def get_interview_turns(self, session_id: str) -> list:
        rows = self._get_conn().execute(
            "SELECT * FROM interview_turns WHERE session_id = ? ORDER BY turn_number",
            (session_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_interview_transcript(self, session_id: str) -> str:
        turns = self.get_interview_turns(session_id)
        lines = []
        for t in turns:
            role_tag = f" ({t['speaker_role']})" if t['speaker_role'] else ""
            type_tag = f" [{t['turn_type']}]" if t['turn_type'] not in ('question', 'answer') else ""
            lines.append(f"[Turn {t['turn_number']}] {t['speaker']}{role_tag}{type_tag}:")
            lines.append(f"  {t['content']}")
            lines.append("")
        return "\n".join(lines)

    # =====================================================
    # INTERVIEW SCORES
    # =====================================================

    def add_interview_score(
        self,
        session_id: str,
        evaluator_agent: str,
        dimension: str,
        score: float,
        max_score: float = 10.0,
        evaluator_role: str = "",
        evidence: str = "",
        feedback: str = "",
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO interview_scores "
            "(session_id, evaluator_agent, evaluator_role, dimension, score, "
            "max_score, evidence, feedback, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                session_id, evaluator_agent, evaluator_role, dimension,
                score, max_score, evidence, feedback,
                datetime.now().isoformat(),
            ),
        )
        conn.commit()
        return cur.lastrowid

    def get_interview_scores(self, session_id: str) -> list:
        rows = self._get_conn().execute(
            "SELECT * FROM interview_scores WHERE session_id = ? ORDER BY evaluator_agent, dimension",
            (session_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_aggregated_scores(self, session_id: str) -> dict:
        scores = self.get_interview_scores(session_id)
        if not scores:
            return {}
        by_dimension = {}
        by_evaluator = {}
        for s in scores:
            dim = s["dimension"]
            ev = s["evaluator_agent"]
            if dim not in by_dimension:
                by_dimension[dim] = []
            by_dimension[dim].append(s["score"])
            if ev not in by_evaluator:
                by_evaluator[ev] = {"role": s["evaluator_role"], "scores": {}}
            by_evaluator[ev]["scores"][dim] = {
                "score": s["score"],
                "max": s["max_score"],
                "evidence": s["evidence"],
                "feedback": s["feedback"],
            }
        consensus = {}
        for dim, vals in by_dimension.items():
            consensus[dim] = round(sum(vals) / len(vals), 1)
        overall = round(sum(consensus.values()) / len(consensus), 1) if consensus else 0
        return {
            "overall": overall,
            "dimensions": consensus,
            "by_evaluator": by_evaluator,
        }

    # =====================================================
    # SCREENING SESSION MANAGEMENT (Multi-Round V2)
    # =====================================================

    def create_screening_session(
        self, session_id: str, user_id: str = "", resume_data: dict = None
    ) -> dict:
        conn = self._get_conn()
        now = datetime.now().isoformat()
        conn.execute(
            "INSERT INTO screening_sessions "
            "(id, user_id, resume_data, status, questions_asked, coverage, created_at) "
            "VALUES (?, ?, ?, 'active', 0, ?, ?)",
            (session_id, user_id, json.dumps(resume_data or {}), json.dumps({}), now),
        )
        conn.commit()
        return self.get_screening_session(session_id)

    def get_screening_session(self, session_id: str) -> Optional[dict]:
        row = self._get_conn().execute(
            "SELECT * FROM screening_sessions WHERE id = ?", (session_id,)
        ).fetchone()
        return dict(row) if row else None

    def update_screening_session(self, session_id: str, **kwargs) -> None:
        conn = self._get_conn()
        sets, vals = [], []
        for k, v in kwargs.items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v)
            sets.append(f"{k} = ?")
            vals.append(v)
        vals.append(session_id)
        conn.execute(
            f"UPDATE screening_sessions SET {', '.join(sets)} WHERE id = ?", vals
        )
        conn.commit()

    def complete_screening(self, session_id: str, candidate_profile: dict) -> None:
        self.update_screening_session(
            session_id,
            status="completed",
            candidate_profile=candidate_profile,
            completed_at=datetime.now().isoformat(),
        )

    def add_screening_turn(
        self, session_id: str, turn_number: int, speaker: str,
        content: str, analysis: dict = None
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO screening_turns "
            "(session_id, turn_number, speaker, content, analysis, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, turn_number, speaker, content,
             json.dumps(analysis or {}), datetime.now().isoformat()),
        )
        conn.execute(
            "UPDATE screening_sessions SET questions_asked = ? WHERE id = ?",
            (turn_number, session_id),
        )
        conn.commit()
        return cur.lastrowid

    def get_screening_turns(self, session_id: str) -> List[dict]:
        rows = self._get_conn().execute(
            "SELECT * FROM screening_turns WHERE session_id = ? ORDER BY turn_number",
            (session_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_screening_transcript(self, session_id: str) -> str:
        turns = self.get_screening_turns(session_id)
        lines = []
        for t in turns:
            lines.append(f"[{t['speaker']}]: {t['content']}")
        return "\n".join(lines)

    # =====================================================
    # INTERVIEW ROUNDS (Multi-Round V2)
    # =====================================================

    def create_interview_round(
        self, session_id: str, round_num: int, interviewer_name: str,
        interviewer_role: str, round_type: str, focus_areas: list = None,
        max_questions: int = 8, is_final: bool = False
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO interview_rounds "
            "(session_id, round_num, interviewer_name, interviewer_role, round_type, "
            "focus_areas, max_questions, is_final, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')",
            (session_id, round_num, interviewer_name, interviewer_role,
             round_type, json.dumps(focus_areas or []), max_questions, int(is_final)),
        )
        conn.commit()
        return cur.lastrowid

    def get_interview_round(self, session_id: str, round_num: int) -> Optional[dict]:
        row = self._get_conn().execute(
            "SELECT * FROM interview_rounds WHERE session_id = ? AND round_num = ?",
            (session_id, round_num),
        ).fetchone()
        return dict(row) if row else None

    def get_all_rounds(self, session_id: str) -> List[dict]:
        rows = self._get_conn().execute(
            "SELECT * FROM interview_rounds WHERE session_id = ? ORDER BY round_num",
            (session_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def update_interview_round(self, session_id: str, round_num: int, **kwargs) -> None:
        conn = self._get_conn()
        sets, vals = [], []
        for k, v in kwargs.items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v)
            sets.append(f"{k} = ?")
            vals.append(v)
        vals.extend([session_id, round_num])
        conn.execute(
            f"UPDATE interview_rounds SET {', '.join(sets)} "
            "WHERE session_id = ? AND round_num = ?", vals
        )
        conn.commit()

    def start_interview_round(self, session_id: str, round_num: int,
                               forum_digest: str = "") -> None:
        self.update_interview_round(
            session_id, round_num,
            status="active",
            forum_digest_used=forum_digest,
            started_at=datetime.now().isoformat(),
        )
        self.update_interview_session(session_id, current_round=round_num)

    def complete_interview_round(self, session_id: str, round_num: int) -> None:
        self.update_interview_round(
            session_id, round_num,
            status="completed",
            completed_at=datetime.now().isoformat(),
        )

    def increment_round_questions(self, session_id: str, round_num: int) -> int:
        conn = self._get_conn()
        conn.execute(
            "UPDATE interview_rounds SET questions_asked = questions_asked + 1 "
            "WHERE session_id = ? AND round_num = ?",
            (session_id, round_num),
        )
        conn.commit()
        row = conn.execute(
            "SELECT questions_asked FROM interview_rounds "
            "WHERE session_id = ? AND round_num = ?",
            (session_id, round_num),
        ).fetchone()
        return row[0] if row else 0

    def get_round_turns(self, session_id: str, round_num: int) -> List[dict]:
        """Get interview turns for a specific round by filtering on metadata."""
        rows = self._get_conn().execute(
            "SELECT * FROM interview_turns WHERE session_id = ? "
            "AND json_extract(metadata, '$.round_num') = ? ORDER BY turn_number",
            (session_id, round_num),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_round_transcript(self, session_id: str, round_num: int) -> str:
        turns = self.get_round_turns(session_id, round_num)
        lines = []
        for t in turns:
            role_tag = f" ({t['speaker_role']})" if t.get('speaker_role') else ""
            lines.append(f"[{t['speaker']}{role_tag}]: {t['content']}")
        return "\n".join(lines)

    # =====================================================
    # FORUM POSTS BY ROUND (Multi-Round V2)
    # =====================================================

    def get_forum_posts_by_round(self, session_id: str, round_num: int) -> List[dict]:
        rows = self._get_conn().execute(
            "SELECT * FROM arena_posts WHERE session_id = ? AND round_num = ? "
            "ORDER BY post_id",
            (session_id, round_num),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_forum_posts_up_to_round(self, session_id: str, up_to_round: int) -> List[dict]:
        rows = self._get_conn().execute(
            "SELECT * FROM arena_posts WHERE session_id = ? AND round_num <= ? "
            "ORDER BY round_num, post_id",
            (session_id, up_to_round),
        ).fetchall()
        return [dict(r) for r in rows]

    def build_forum_digest(self, session_id: str, up_to_round: int) -> str:
        """Build a formatted digest of all forum posts up to a given round."""
        posts = self.get_forum_posts_up_to_round(session_id, up_to_round)
        if not posts:
            return ""
        lines = ["## Inter-Interviewer Forum Discussion\n"]
        current_round = -1
        for p in posts:
            if p["round_num"] != current_round:
                current_round = p["round_num"]
                lines.append(f"\n### After Round {current_round}\n")
            lines.append(f"**{p['agent_name']}** ({p.get('agent_type', '')}):")
            lines.append(f"{p['content']}\n")
            comments = self.get_comments_for_post(p["post_id"])
            for c in comments:
                lines.append(f"  > **{c['agent_name']}** replies: {c['content']}")
        return "\n".join(lines)

    def close(self):
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None
