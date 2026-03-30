"""
KnowledgeDB — Separate SQLite database for interview domain knowledge.

Stores persona templates, question banks, company profiles, evaluation rubrics,
and Indian context data. This is the "content engine" that feeds the screening
agent, panel generator, and interviewer swarms with domain-specific knowledge.

Database file: knowledge.db (separate from career_arena.db)
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime
from typing import Optional, List, Dict


class KnowledgeDB:
    def __init__(self, db_path: str = "knowledge.db"):
        self.db_path = db_path
        self._local = threading.local()
        self._init_schema()
        self._seed_if_empty()

    def _get_conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA foreign_keys=ON")
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
        return self._local.conn

    def _init_schema(self):
        conn = self._get_conn()
        conn.executescript("""
            -- =============================================
            -- PERSONA TEMPLATES
            -- =============================================
            CREATE TABLE IF NOT EXISTS persona_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                level TEXT NOT NULL,
                role TEXT NOT NULL,
                name TEXT NOT NULL,
                personality TEXT NOT NULL,
                question_style TEXT NOT NULL,
                system_prompt TEXT NOT NULL,
                traits JSON,
                eval_dimensions JSON,
                expertise JSON,
                voice_config JSON,
                interaction_style TEXT DEFAULT 'independent',
                avatar_color TEXT DEFAULT '#6366f1',
                tags JSON,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_persona_domain ON persona_templates(domain);
            CREATE INDEX IF NOT EXISTS idx_persona_level ON persona_templates(level);
            CREATE INDEX IF NOT EXISTS idx_persona_role ON persona_templates(role);

            -- =============================================
            -- QUESTION BANK
            -- =============================================
            CREATE TABLE IF NOT EXISTS question_bank (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                topic TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                level TEXT NOT NULL,
                question_text TEXT NOT NULL,
                follow_ups JSON,
                scoring_rubric JSON,
                expected_points JSON,
                company_specific TEXT,
                tags JSON,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_question_domain ON question_bank(domain);
            CREATE INDEX IF NOT EXISTS idx_question_topic ON question_bank(topic);
            CREATE INDEX IF NOT EXISTS idx_question_difficulty ON question_bank(difficulty);
            CREATE INDEX IF NOT EXISTS idx_question_company ON question_bank(company_specific);

            -- =============================================
            -- COMPANY PROFILES
            -- =============================================
            CREATE TABLE IF NOT EXISTS company_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT UNIQUE NOT NULL,
                industry TEXT,
                interview_process JSON,
                common_questions JSON,
                salary_ranges JSON,
                evaluation_priorities JSON,
                culture_notes TEXT,
                hiring_bar TEXT,
                tips JSON,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_company_name ON company_profiles(company_name);

            -- =============================================
            -- EVALUATION RUBRICS
            -- =============================================
            CREATE TABLE IF NOT EXISTS evaluation_rubrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dimension TEXT NOT NULL,
                level TEXT NOT NULL,
                score_1_2 TEXT NOT NULL,
                score_3_4 TEXT NOT NULL,
                score_5_6 TEXT NOT NULL,
                score_7_8 TEXT NOT NULL,
                score_9_10 TEXT NOT NULL,
                key_indicators JSON,
                red_flags JSON,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_rubric_dimension ON evaluation_rubrics(dimension);
            CREATE INDEX IF NOT EXISTS idx_rubric_level ON evaluation_rubrics(level);

            -- =============================================
            -- INDIAN CONTEXT
            -- =============================================
            CREATE TABLE IF NOT EXISTS indian_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                tips JSON,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_context_category ON indian_context(category);
            CREATE INDEX IF NOT EXISTS idx_context_topic ON indian_context(topic);

            -- =============================================
            -- COMPANY HIRING TRACKS
            -- =============================================
            CREATE TABLE IF NOT EXISTS company_hiring_tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                track_code TEXT NOT NULL,
                track_name TEXT NOT NULL,
                target_levels JSON NOT NULL,
                salary_range TEXT NOT NULL,
                eligibility JSON NOT NULL,
                difficulty_tier TEXT NOT NULL,
                description TEXT,
                selection_test TEXT,
                bond_years INTEGER DEFAULT 0,
                training_info TEXT,
                is_default INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                UNIQUE(company_name, track_code)
            );
            CREATE INDEX IF NOT EXISTS idx_track_company ON company_hiring_tracks(company_name);
            CREATE INDEX IF NOT EXISTS idx_track_code ON company_hiring_tracks(track_code);

            -- =============================================
            -- COMPANY ROUND BLUEPRINTS
            -- =============================================
            CREATE TABLE IF NOT EXISTS company_round_blueprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                track_code TEXT NOT NULL,
                round_num INTEGER NOT NULL,
                round_type TEXT NOT NULL,
                round_label TEXT NOT NULL,
                focus_areas JSON NOT NULL,
                difficulty TEXT NOT NULL,
                max_questions INTEGER DEFAULT 8,
                interviewer_role_hint TEXT,
                personality_hint TEXT,
                question_style_hint TEXT,
                eval_dimensions JSON,
                notes TEXT,
                is_eliminatory INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                UNIQUE(company_name, track_code, round_num)
            );
            CREATE INDEX IF NOT EXISTS idx_blueprint_company ON company_round_blueprints(company_name);
            CREATE INDEX IF NOT EXISTS idx_blueprint_track ON company_round_blueprints(track_code);

            -- =============================================
            -- DEFAULT ROUND BLUEPRINTS
            -- =============================================
            CREATE TABLE IF NOT EXISTS default_round_blueprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                round_num INTEGER NOT NULL,
                round_type TEXT NOT NULL,
                round_label TEXT NOT NULL,
                focus_areas JSON NOT NULL,
                difficulty TEXT NOT NULL,
                max_questions INTEGER DEFAULT 8,
                interviewer_role_hint TEXT,
                personality_hint TEXT,
                question_style_hint TEXT,
                eval_dimensions JSON,
                notes TEXT,
                created_at TEXT NOT NULL,
                UNIQUE(domain, experience_level, round_num)
            );
            CREATE INDEX IF NOT EXISTS idx_default_bp_domain ON default_round_blueprints(domain);
            CREATE INDEX IF NOT EXISTS idx_default_bp_level ON default_round_blueprints(experience_level);
        """)
        conn.commit()

        # Add round_type column to question_bank if not present
        try:
            conn.execute("ALTER TABLE question_bank ADD COLUMN round_type TEXT DEFAULT ''")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists

    # =====================================================
    # PERSONA TEMPLATES
    # =====================================================

    def add_persona_template(
        self, domain: str, level: str, role: str, name: str,
        personality: str, question_style: str, system_prompt: str,
        traits: dict = None, eval_dimensions: list = None,
        expertise: list = None, voice_config: dict = None,
        interaction_style: str = "independent", avatar_color: str = "#6366f1",
        tags: list = None,
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO persona_templates "
            "(domain, level, role, name, personality, question_style, system_prompt, "
            "traits, eval_dimensions, expertise, voice_config, interaction_style, "
            "avatar_color, tags, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (domain, level, role, name, personality, question_style, system_prompt,
             json.dumps(traits or {}), json.dumps(eval_dimensions or []),
             json.dumps(expertise or []), json.dumps(voice_config or {}),
             interaction_style, avatar_color, json.dumps(tags or []),
             datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_persona_templates(
        self, domain: str = None, level: str = None, role: str = None,
        company: str = None,
    ) -> List[dict]:
        conn = self._get_conn()
        query = "SELECT * FROM persona_templates WHERE 1=1"
        params = []
        if domain:
            query += " AND domain = ?"
            params.append(domain)
        if level:
            query += " AND level = ?"
            params.append(level)
        if role:
            query += " AND role = ?"
            params.append(role)
        if company:
            # Match company name in JSON tags array
            query += " AND tags LIKE ?"
            params.append(f'%"{company}"%')
        query += " ORDER BY id"
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def get_persona_template(self, template_id: int) -> Optional[dict]:
        row = self._get_conn().execute(
            "SELECT * FROM persona_templates WHERE id = ?", (template_id,)
        ).fetchone()
        return dict(row) if row else None

    # =====================================================
    # QUESTION BANK
    # =====================================================

    def add_question(
        self, domain: str, topic: str, difficulty: str, level: str,
        question_text: str, follow_ups: list = None,
        scoring_rubric: dict = None, expected_points: list = None,
        company_specific: str = "", tags: list = None,
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO question_bank "
            "(domain, topic, difficulty, level, question_text, follow_ups, "
            "scoring_rubric, expected_points, company_specific, tags, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (domain, topic, difficulty, level, question_text,
             json.dumps(follow_ups or []), json.dumps(scoring_rubric or {}),
             json.dumps(expected_points or []), company_specific,
             json.dumps(tags or []), datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_questions(
        self, domain: str = None, topic: str = None,
        difficulty: str = None, level: str = None,
        company: str = None, round_type: str = None,
        limit: int = 20,
    ) -> List[dict]:
        conn = self._get_conn()
        query = "SELECT * FROM question_bank WHERE 1=1"
        params = []
        if domain:
            query += " AND domain = ?"
            params.append(domain)
        if topic:
            query += " AND topic = ?"
            params.append(topic)
        if difficulty:
            query += " AND difficulty = ?"
            params.append(difficulty)
        if level:
            query += " AND level = ?"
            params.append(level)
        if company:
            query += " AND company_specific = ?"
            params.append(company)
        if round_type:
            query += " AND round_type = ?"
            params.append(round_type)
        query += " ORDER BY RANDOM() LIMIT ?"
        params.append(limit)
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def get_question(self, question_id: int) -> Optional[dict]:
        row = self._get_conn().execute(
            "SELECT * FROM question_bank WHERE id = ?", (question_id,)
        ).fetchone()
        return dict(row) if row else None

    # =====================================================
    # COMPANY PROFILES
    # =====================================================

    def add_company_profile(
        self, company_name: str, industry: str = "",
        interview_process: dict = None, common_questions: list = None,
        salary_ranges: dict = None, evaluation_priorities: list = None,
        culture_notes: str = "", hiring_bar: str = "", tips: list = None,
    ) -> int:
        conn = self._get_conn()
        now = datetime.now().isoformat()
        cur = conn.execute(
            "INSERT OR REPLACE INTO company_profiles "
            "(company_name, industry, interview_process, common_questions, "
            "salary_ranges, evaluation_priorities, culture_notes, hiring_bar, "
            "tips, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (company_name, industry, json.dumps(interview_process or {}),
             json.dumps(common_questions or []), json.dumps(salary_ranges or {}),
             json.dumps(evaluation_priorities or []), culture_notes, hiring_bar,
             json.dumps(tips or []), now, now),
        )
        conn.commit()
        return cur.lastrowid

    def get_company_profile(self, company_name: str) -> Optional[dict]:
        row = self._get_conn().execute(
            "SELECT * FROM company_profiles WHERE company_name = ? COLLATE NOCASE",
            (company_name,),
        ).fetchone()
        return dict(row) if row else None

    def get_all_companies(self) -> List[str]:
        rows = self._get_conn().execute(
            "SELECT company_name FROM company_profiles ORDER BY company_name"
        ).fetchall()
        return [r["company_name"] for r in rows]

    # =====================================================
    # EVALUATION RUBRICS
    # =====================================================

    def add_rubric(
        self, dimension: str, level: str,
        score_1_2: str, score_3_4: str, score_5_6: str,
        score_7_8: str, score_9_10: str,
        key_indicators: list = None, red_flags: list = None,
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO evaluation_rubrics "
            "(dimension, level, score_1_2, score_3_4, score_5_6, score_7_8, "
            "score_9_10, key_indicators, red_flags, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (dimension, level, score_1_2, score_3_4, score_5_6, score_7_8,
             score_9_10, json.dumps(key_indicators or []),
             json.dumps(red_flags or []), datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_rubric(self, dimension: str, level: str = None) -> Optional[dict]:
        conn = self._get_conn()
        if level:
            row = conn.execute(
                "SELECT * FROM evaluation_rubrics WHERE dimension = ? AND level = ?",
                (dimension, level),
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT * FROM evaluation_rubrics WHERE dimension = ? LIMIT 1",
                (dimension,),
            ).fetchone()
        return dict(row) if row else None

    def get_all_rubrics(self, level: str = None) -> List[dict]:
        conn = self._get_conn()
        if level:
            rows = conn.execute(
                "SELECT * FROM evaluation_rubrics WHERE level = ? ORDER BY dimension",
                (level,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM evaluation_rubrics ORDER BY dimension, level"
            ).fetchall()
        return [dict(r) for r in rows]

    # =====================================================
    # INDIAN CONTEXT
    # =====================================================

    def add_indian_context(
        self, category: str, topic: str, content: str, tips: list = None,
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO indian_context (category, topic, content, tips, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (category, topic, content, json.dumps(tips or []),
             datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_indian_context(self, category: str = None, topic: str = None) -> List[dict]:
        conn = self._get_conn()
        query = "SELECT * FROM indian_context WHERE 1=1"
        params = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if topic:
            query += " AND topic = ?"
            params.append(topic)
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    # =====================================================
    # COMPANY HIRING TRACKS
    # =====================================================

    def add_hiring_track(
        self, company_name: str, track_code: str, track_name: str,
        target_levels: list, salary_range: str, eligibility: dict,
        difficulty_tier: str, description: str = "", selection_test: str = "",
        bond_years: int = 0, training_info: str = "", is_default: int = 0,
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT OR REPLACE INTO company_hiring_tracks "
            "(company_name, track_code, track_name, target_levels, salary_range, "
            "eligibility, difficulty_tier, description, selection_test, bond_years, "
            "training_info, is_default, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (company_name, track_code, track_name, json.dumps(target_levels),
             salary_range, json.dumps(eligibility), difficulty_tier, description,
             selection_test, bond_years, training_info, is_default,
             datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_hiring_tracks(
        self, company_name: str, level: str = None,
    ) -> List[dict]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM company_hiring_tracks WHERE company_name = ? COLLATE NOCASE ORDER BY is_default DESC, id",
            (company_name,),
        ).fetchall()
        tracks = [dict(r) for r in rows]
        if level:
            tracks = [t for t in tracks if level in json.loads(t["target_levels"])]
        return tracks

    def get_hiring_track(self, company_name: str, track_code: str) -> Optional[dict]:
        row = self._get_conn().execute(
            "SELECT * FROM company_hiring_tracks WHERE company_name = ? COLLATE NOCASE AND track_code = ?",
            (company_name, track_code),
        ).fetchone()
        return dict(row) if row else None

    # =====================================================
    # COMPANY ROUND BLUEPRINTS
    # =====================================================

    def add_round_blueprint(
        self, company_name: str, track_code: str, round_num: int,
        round_type: str, round_label: str, focus_areas: list,
        difficulty: str, max_questions: int = 8,
        interviewer_role_hint: str = "", personality_hint: str = "",
        question_style_hint: str = "", eval_dimensions: list = None,
        notes: str = "", is_eliminatory: int = 0,
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT OR REPLACE INTO company_round_blueprints "
            "(company_name, track_code, round_num, round_type, round_label, "
            "focus_areas, difficulty, max_questions, interviewer_role_hint, "
            "personality_hint, question_style_hint, eval_dimensions, notes, "
            "is_eliminatory, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (company_name, track_code, round_num, round_type, round_label,
             json.dumps(focus_areas), difficulty, max_questions,
             interviewer_role_hint, personality_hint, question_style_hint,
             json.dumps(eval_dimensions or []), notes, is_eliminatory,
             datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_round_blueprints(
        self, company_name: str, track_code: str,
    ) -> List[dict]:
        rows = self._get_conn().execute(
            "SELECT * FROM company_round_blueprints "
            "WHERE company_name = ? COLLATE NOCASE AND track_code = ? ORDER BY round_num",
            (company_name, track_code),
        ).fetchall()
        return [dict(r) for r in rows]

    # =====================================================
    # DEFAULT ROUND BLUEPRINTS
    # =====================================================

    def add_default_blueprint(
        self, domain: str, experience_level: str, round_num: int,
        round_type: str, round_label: str, focus_areas: list,
        difficulty: str, max_questions: int = 8,
        interviewer_role_hint: str = "", personality_hint: str = "",
        question_style_hint: str = "", eval_dimensions: list = None,
        notes: str = "",
    ) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT OR REPLACE INTO default_round_blueprints "
            "(domain, experience_level, round_num, round_type, round_label, "
            "focus_areas, difficulty, max_questions, interviewer_role_hint, "
            "personality_hint, question_style_hint, eval_dimensions, notes, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (domain, experience_level, round_num, round_type, round_label,
             json.dumps(focus_areas), difficulty, max_questions,
             interviewer_role_hint, personality_hint, question_style_hint,
             json.dumps(eval_dimensions or []), notes,
             datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid

    def get_default_blueprints(
        self, domain: str, experience_level: str,
    ) -> List[dict]:
        rows = self._get_conn().execute(
            "SELECT * FROM default_round_blueprints "
            "WHERE domain = ? AND experience_level = ? ORDER BY round_num",
            (domain, experience_level),
        ).fetchall()
        return [dict(r) for r in rows]

    # =====================================================
    # SEED DATA
    # =====================================================

    def _seed_if_empty(self):
        conn = self._get_conn()
        count = conn.execute("SELECT COUNT(*) FROM question_bank").fetchone()[0]
        if count > 0:
            return  # Skip if data exists (either from seed script or prior run)
        self._seed_questions()
        self._seed_companies()
        self._seed_rubrics()
        self._seed_indian_context()
        self._seed_persona_templates()

    def _seed_persona_templates(self):
        templates = [
            # Software Engineering
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "Technical Lead", "name": "Arjun Mehta",
                "personality": "intense", "question_style": "deep_dive",
                "system_prompt": "You are Arjun Mehta, a Senior Technical Lead. You test fundamental CS knowledge — data structures, algorithms, OOP concepts. For freshers, you start with basics and go deeper based on answers. You're direct and technical but fair. Ask ONE question at a time.",
                "traits": {"warmth": 0.3, "directness": 0.9, "humor": 0.2, "patience": 0.6},
                "eval_dimensions": ["technical_depth", "problem_solving", "fundamentals"],
                "expertise": ["data_structures", "algorithms", "oop", "databases"],
                "voice_config": {"googleVoiceName": "en-IN-Wavenet-B", "speakingRate": 1.0},
            },
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "HR Lead", "name": "Priya Sharma",
                "personality": "warm_but_probing", "question_style": "behavioral_star",
                "system_prompt": "You are Priya Sharma, an experienced HR Lead. For freshers, you assess communication skills, enthusiasm, cultural fit, and career clarity. You use STAR method for behavioral questions. You're warm but notice inconsistencies. Ask ONE question at a time.",
                "traits": {"warmth": 0.85, "directness": 0.5, "humor": 0.3, "patience": 0.9},
                "eval_dimensions": ["communication", "culture_fit", "motivation", "self_awareness"],
                "expertise": ["behavioral_assessment", "campus_hiring", "soft_skills"],
                "voice_config": {"googleVoiceName": "en-IN-Wavenet-A", "speakingRate": 0.95},
            },
            {
                "domain": "software_engineering", "level": "mid",
                "role": "Engineering Manager", "name": "Meera Krishnan",
                "personality": "skeptical", "question_style": "case_based",
                "system_prompt": "You are Meera Krishnan, Engineering Manager. For mid-level candidates (3-7 yrs), you test system design thinking, ownership, and ability to work in ambiguity. Ask about past projects — probe what THEY did vs the team. Challenge vague claims. Ask ONE question at a time.",
                "traits": {"warmth": 0.4, "directness": 0.8, "humor": 0.15, "patience": 0.6},
                "eval_dimensions": ["system_design", "ownership", "leadership", "impact"],
                "expertise": ["system_design", "team_management", "architecture"],
                "voice_config": {"googleVoiceName": "en-IN-Wavenet-C", "speakingRate": 0.9},
            },
            {
                "domain": "software_engineering", "level": "senior",
                "role": "VP Engineering", "name": "Rajesh Nair",
                "personality": "neutral", "question_style": "socratic",
                "system_prompt": "You are Rajesh Nair, VP Engineering. For senior candidates (8+ yrs), you assess strategic thinking, architecture decisions, team building, and business impact. Ask about trade-offs, failures, and lessons learned. Test if they think like a leader. Ask ONE question at a time.",
                "traits": {"warmth": 0.5, "directness": 0.7, "humor": 0.2, "patience": 0.7},
                "eval_dimensions": ["strategic_thinking", "architecture", "leadership", "mentoring"],
                "expertise": ["engineering_leadership", "org_design", "product_strategy"],
                "voice_config": {"googleVoiceName": "en-IN-Wavenet-D", "speakingRate": 0.85},
            },
            # Data Science
            {
                "domain": "data_science", "level": "fresher",
                "role": "Data Science Lead", "name": "Dr. Ananya Rao",
                "personality": "warm_but_probing", "question_style": "socratic",
                "system_prompt": "You are Dr. Ananya Rao, Data Science Lead. You test statistics fundamentals, ML concepts, Python/SQL skills, and ability to think about data problems. For freshers, start with basics — probability, regression, classification. Go deeper based on confidence. Ask ONE question at a time.",
                "traits": {"warmth": 0.7, "directness": 0.6, "humor": 0.25, "patience": 0.8},
                "eval_dimensions": ["statistics", "ml_fundamentals", "coding", "analytical_thinking"],
                "expertise": ["machine_learning", "statistics", "python", "sql"],
                "voice_config": {"googleVoiceName": "en-IN-Neural2-A", "speakingRate": 0.95},
            },
            # Consulting / MBA
            {
                "domain": "consulting", "level": "fresher",
                "role": "Partner", "name": "Sanjay Gupta",
                "personality": "intense", "question_style": "case_based",
                "system_prompt": "You are Sanjay Gupta, Partner at a consulting firm. You conduct case interviews — present business problems and evaluate structured thinking, quantitative skills, and communication. Test frameworks usage, market sizing, and profitability analysis. Ask ONE question/case at a time.",
                "traits": {"warmth": 0.3, "directness": 0.85, "humor": 0.1, "patience": 0.5},
                "eval_dimensions": ["structured_thinking", "quantitative", "communication", "business_acumen"],
                "expertise": ["case_interviews", "strategy", "market_analysis"],
                "voice_config": {"googleVoiceName": "en-IN-Wavenet-D", "speakingRate": 1.05},
            },
            # IT Services — Campus-specific
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "Senior Software Engineer", "name": "Neha Iyer",
                "personality": "skeptical", "question_style": "case_based",
                "system_prompt": "You are Neha Iyer, a Senior Software Engineer at an IT services company. You conduct system-thinking and aptitude rounds for freshers. You test basic system design, logical reasoning, and how candidates handle unfamiliar problems. You are mildly skeptical but patient. Use case-based scenarios from real client projects. Ask ONE question at a time.",
                "traits": {"warmth": 0.5, "directness": 0.8, "humor": 0.3, "patience": 0.8},
                "eval_dimensions": ["aptitude", "system_design_basics", "learning_ability", "structured_thinking"],
                "expertise": ["basic_system_design", "aptitude", "client_project_scenarios"],
                "voice_config": {"googleVoiceName": "en-IN-Wavenet-A", "speakingRate": 0.95},
            },
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "Project Manager", "name": "Deepak Varma",
                "personality": "neutral", "question_style": "situational",
                "system_prompt": "You are Deepak Varma, a Project Manager in the Banking & Financial Services unit. You assess freshers for client-readiness: can they work in a process-driven environment, handle changing requirements, communicate with seniors, and adapt to different technology stacks? You use realistic workplace scenarios. Be professional and fair. Ask ONE question at a time.",
                "traits": {"warmth": 0.55, "directness": 0.75, "humor": 0.2, "patience": 0.7},
                "eval_dimensions": ["communication", "client_readiness", "adaptability", "teamwork"],
                "expertise": ["project_management", "client_handling", "requirement_analysis"],
                "voice_config": {"googleVoiceName": "en-IN-Wavenet-B", "speakingRate": 0.9},
            },
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "HR Business Partner", "name": "Kavya Nair",
                "personality": "warm_but_probing", "question_style": "behavioral_star",
                "system_prompt": "You are Kavya Nair, an HR Business Partner responsible for campus hiring. You are warm and supportive but probe deeply using STAR questions. You assess cultural fit, stability (bond acceptance, relocation willingness), communication, and long-term commitment. For freshers from Tier 3 colleges, be encouraging but realistic about IT services career expectations. Ask ONE question at a time.",
                "traits": {"warmth": 0.9, "directness": 0.6, "humor": 0.4, "patience": 0.9},
                "eval_dimensions": ["culture_fit", "stability", "communication", "willingness_to_learn"],
                "expertise": ["behavioral_assessment", "campus_hiring", "retention_assessment"],
                "voice_config": {"googleVoiceName": "en-IN-Neural2-A", "speakingRate": 0.9},
            },
            # UPSC
            {
                "domain": "upsc", "level": "all",
                "role": "Chairman", "name": "Justice (Retd.) Suresh Patel",
                "personality": "neutral", "question_style": "socratic",
                "system_prompt": "You are Justice (Retd.) Suresh Patel, chairing a UPSC board. You test personality, integrity, balanced perspective. Start from the candidate's DAF — hometown, hobbies, optional subject. Ask opinion questions on governance, ethics, and current affairs. Be dignified and fair. Ask ONE question at a time.",
                "traits": {"warmth": 0.5, "directness": 0.7, "humor": 0.2, "patience": 0.8},
                "eval_dimensions": ["personality", "integrity", "balanced_perspective", "composure"],
                "expertise": ["governance", "constitutional_law", "ethics"],
                "voice_config": {"googleVoiceName": "en-IN-Wavenet-D", "speakingRate": 0.85},
            },
            # ─── Company-Specific: TCS ───
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "TCS Technical Interviewer", "name": "Ramesh Sundaram",
                "personality": "neutral", "question_style": "deep_dive",
                "system_prompt": "You are Ramesh Sundaram, a TCS Technical Interviewer for campus hiring. TCS interviews for freshers focus on CS fundamentals: OOP, DBMS, OS basics, and simple coding. You are methodical — start with basics, go slightly deeper if candidate is strong. TCS values consistency over brilliance. Check willingness to work on any technology stack. Never intimidate — TCS wants trainable freshers, not experts. Ask ONE question at a time.",
                "traits": {"warmth": 0.6, "directness": 0.7, "humor": 0.2, "patience": 0.8},
                "eval_dimensions": ["technical_depth", "fundamentals", "learning_ability", "communication"],
                "expertise": ["oop", "dbms", "os_basics", "sql", "java_basics"],
                "tags": ["TCS"],
            },
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "TCS HR Manager", "name": "Lakshmi Venkatesh",
                "personality": "warm_but_probing", "question_style": "behavioral_star",
                "system_prompt": "You are Lakshmi Venkatesh, TCS HR Manager for campus placements. You assess willingness to relocate anywhere in India, acceptance of 2-year service bond, salary expectations (freshers get 3.36-7 LPA), and long-term commitment. You are warm but direct about TCS expectations. Check if candidate has realistic expectations about IT services work culture — shifts, on-call, client projects. Ask about extracurriculars and leadership in college. Ask ONE question at a time.",
                "traits": {"warmth": 0.85, "directness": 0.65, "humor": 0.3, "patience": 0.9},
                "eval_dimensions": ["communication", "culture_fit", "stability", "motivation"],
                "expertise": ["campus_hiring", "retention_assessment", "tcs_culture"],
                "tags": ["TCS"],
            },
            # ─── Company-Specific: Infosys ───
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "Infosys Technical Lead", "name": "Karthik Ramanathan",
                "personality": "intense", "question_style": "deep_dive",
                "system_prompt": "You are Karthik Ramanathan, Infosys Technical Lead for InfyTQ hiring. Infosys values strong programming fundamentals — test Java/Python coding ability, not just theory. Ask candidates to explain code logic, trace through algorithms, discuss time complexity. Infosys InfyTQ candidates should know at least one language deeply. Check if they've done the InfyTQ certification. You are thorough but fair. Ask ONE question at a time.",
                "traits": {"warmth": 0.4, "directness": 0.85, "humor": 0.15, "patience": 0.6},
                "eval_dimensions": ["technical_depth", "coding_ability", "problem_solving", "analytical_thinking"],
                "expertise": ["java", "python", "algorithms", "data_structures", "infytq_pattern"],
                "tags": ["Infosys"],
            },
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "Infosys HR Partner", "name": "Divya Subramaniam",
                "personality": "warm_but_probing", "question_style": "situational",
                "system_prompt": "You are Divya Subramaniam, Infosys HR Partner. You assess freshers on communication clarity, teamwork attitude, and adaptability to Infosys culture (Mysore training, global deployments). Check awareness of Infosys values — C-LIFE (Client value, Leadership by example, Integrity, Fairness, Excellence). Probe career aspirations and willingness to work in any domain/location assigned. Ask ONE question at a time.",
                "traits": {"warmth": 0.8, "directness": 0.55, "humor": 0.25, "patience": 0.85},
                "eval_dimensions": ["communication", "culture_fit", "self_awareness", "motivation"],
                "expertise": ["behavioral_assessment", "infosys_culture", "global_readiness"],
                "tags": ["Infosys"],
            },
            # ─── Company-Specific: Wipro ───
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "Wipro Technical Panel", "name": "Anil Kumar Reddy",
                "personality": "neutral", "question_style": "rapid_fire",
                "system_prompt": "You are Anil Kumar Reddy, Wipro Technical Interviewer for NLTH (National Level Talent Hunt). Wipro interviews are moderately technical for freshers — focus on DBMS, networking basics, OOP, and one programming language. You also test written communication since Wipro has an essay/email writing round. Be balanced and give candidates a chance to recover from weak answers. Ask ONE question at a time.",
                "traits": {"warmth": 0.5, "directness": 0.7, "humor": 0.3, "patience": 0.75},
                "eval_dimensions": ["technical_depth", "communication", "structured_thinking", "fundamentals"],
                "expertise": ["dbms", "networking", "oop", "written_communication"],
                "tags": ["Wipro"],
            },
            # ─── Company-Specific: Cognizant ───
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "Cognizant GenC Interviewer", "name": "Pradeep Mohan",
                "personality": "warm_but_probing", "question_style": "case_based",
                "system_prompt": "You are Pradeep Mohan, Cognizant GenC Interviewer. Cognizant GenC hires freshers into digital tracks — test awareness of cloud, agile, and modern development practices alongside CS fundamentals. The GenC Next track expects stronger coding skills. You test communication heavily since Cognizant is client-facing. Be friendly but probe for depth. Ask ONE question at a time.",
                "traits": {"warmth": 0.7, "directness": 0.6, "humor": 0.35, "patience": 0.8},
                "eval_dimensions": ["technical_depth", "communication", "practical_application", "quick_thinking"],
                "expertise": ["cloud_basics", "agile", "full_stack_basics", "communication"],
                "tags": ["Cognizant"],
            },
            # ─── Company-Specific: Zoho ───
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "Zoho Senior Developer", "name": "Senthil Murugan",
                "personality": "intense", "question_style": "deep_dive",
                "system_prompt": "You are Senthil Murugan, Senior Developer at Zoho, Chennai. Zoho interviews are HARD — even for freshers, you test programming depth, not just theory. Zoho expects candidates to write code in C (their preferred language for campus hiring). Test problem-solving with actual coding problems: string manipulation, array operations, linked list operations. Zoho values first-principles thinkers over framework users. No frameworks — raw coding ability. Ask ONE question at a time.",
                "traits": {"warmth": 0.3, "directness": 0.9, "humor": 0.1, "patience": 0.5},
                "eval_dimensions": ["coding_ability", "problem_solving", "technical_depth", "analytical_thinking"],
                "expertise": ["c_programming", "data_structures", "algorithms", "system_design_basics"],
                "tags": ["Zoho"],
            },
            # ─── Company-Specific: Accenture ───
            {
                "domain": "software_engineering", "level": "fresher",
                "role": "Accenture Communication Assessor", "name": "Meghna Pillai",
                "personality": "warm_but_probing", "question_style": "situational",
                "system_prompt": "You are Meghna Pillai, Accenture Communication and Behavioral Assessor. Accenture places heavy weight on communication skills and cultural fit for freshers. Test spoken English clarity, ability to explain technical concepts to non-technical people, and situational judgment. Accenture values diversity and inclusion — assess teamwork mindset. Their process includes cognitive + technical + coding + interview. Ask ONE question at a time.",
                "traits": {"warmth": 0.75, "directness": 0.6, "humor": 0.4, "patience": 0.85},
                "eval_dimensions": ["communication", "structured_thinking", "culture_fit", "quick_thinking"],
                "expertise": ["communication_assessment", "situational_judgment", "accenture_culture"],
                "tags": ["Accenture"],
            },
        ]

        for t in templates:
            self.add_persona_template(**t)

    def _seed_questions(self):
        questions = [
            # === Software Engineering — Fresher ===
            {"domain": "software_engineering", "topic": "data_structures", "difficulty": "easy", "level": "fresher",
             "question_text": "What is the difference between an Array and a LinkedList? When would you use one over the other?",
             "follow_ups": ["What about time complexity for insertion at the beginning?", "How does memory allocation differ?"],
             "expected_points": ["contiguous vs non-contiguous memory", "O(1) vs O(n) access", "insertion/deletion tradeoffs"]},
            {"domain": "software_engineering", "topic": "data_structures", "difficulty": "medium", "level": "fresher",
             "question_text": "Explain what a HashMap is and how it handles collisions.",
             "follow_ups": ["What happens when the load factor exceeds threshold?", "Can you name a real-world use case?"],
             "expected_points": ["key-value pairs", "hashing function", "chaining or open addressing", "O(1) average lookup"]},
            {"domain": "software_engineering", "topic": "oop", "difficulty": "easy", "level": "fresher",
             "question_text": "Explain the four pillars of Object-Oriented Programming with examples.",
             "follow_ups": ["Give me a real example where you used polymorphism", "What is the difference between abstraction and encapsulation?"],
             "expected_points": ["encapsulation", "inheritance", "polymorphism", "abstraction", "real examples"]},
            {"domain": "software_engineering", "topic": "databases", "difficulty": "easy", "level": "fresher",
             "question_text": "What is the difference between SQL and NoSQL databases? Give examples of when you'd choose each.",
             "follow_ups": ["What is ACID?", "Can you name a scenario where NoSQL would fail?"],
             "expected_points": ["structured vs flexible schema", "ACID vs eventual consistency", "MySQL/PostgreSQL vs MongoDB/DynamoDB"]},
            {"domain": "software_engineering", "topic": "algorithms", "difficulty": "medium", "level": "fresher",
             "question_text": "What is the time complexity of QuickSort? When does it perform worst?",
             "follow_ups": ["How does MergeSort compare?", "Which sorting algorithm is used in Python's built-in sort?"],
             "expected_points": ["O(n log n) average", "O(n^2) worst case", "pivot selection matters", "already sorted input"]},
            {"domain": "software_engineering", "topic": "web_dev", "difficulty": "easy", "level": "fresher",
             "question_text": "What happens when you type a URL into a browser and press Enter?",
             "follow_ups": ["What is DNS resolution?", "What is the difference between HTTP and HTTPS?"],
             "expected_points": ["DNS lookup", "TCP connection", "HTTP request", "server response", "rendering"]},
            {"domain": "software_engineering", "topic": "os", "difficulty": "medium", "level": "fresher",
             "question_text": "What is the difference between a process and a thread?",
             "follow_ups": ["What is a deadlock?", "How does context switching work?"],
             "expected_points": ["own memory space vs shared", "context switching cost", "concurrency"]},
            {"domain": "software_engineering", "topic": "project", "difficulty": "easy", "level": "fresher",
             "question_text": "Tell me about a project you worked on that you're most proud of. What was your specific contribution?",
             "follow_ups": ["What was the hardest challenge?", "What would you do differently?", "What did you learn from it?"],
             "expected_points": ["clear role description", "technical choices", "challenges faced", "outcome/impact"]},

            # === Software Engineering — Mid Level ===
            {"domain": "software_engineering", "topic": "system_design", "difficulty": "medium", "level": "mid",
             "question_text": "How would you design a URL shortener like bit.ly?",
             "follow_ups": ["How would you handle 10 million requests per second?", "What database would you use and why?", "How do you handle expiration?"],
             "expected_points": ["hash generation", "database choice", "caching", "scalability", "analytics"]},
            {"domain": "software_engineering", "topic": "system_design", "difficulty": "hard", "level": "mid",
             "question_text": "Design a real-time notification system for a platform with 50 million users.",
             "follow_ups": ["How do you handle offline users?", "Push vs pull?", "How do you prioritize notifications?"],
             "expected_points": ["WebSocket/SSE", "message queue", "fan-out", "priority system", "rate limiting"]},
            {"domain": "software_engineering", "topic": "architecture", "difficulty": "medium", "level": "mid",
             "question_text": "When would you choose microservices over a monolith? What are the tradeoffs?",
             "follow_ups": ["Have you migrated from monolith to microservices?", "How do you handle distributed transactions?"],
             "expected_points": ["team scaling", "deployment independence", "complexity cost", "data consistency"]},

            # === Software Engineering — Senior ===
            {"domain": "software_engineering", "topic": "leadership", "difficulty": "hard", "level": "senior",
             "question_text": "Tell me about a time you had to make a technical decision that the team disagreed with. How did you handle it?",
             "follow_ups": ["Would you make the same decision again?", "How did you bring the team around?"],
             "expected_points": ["data-driven decision", "stakeholder management", "communication", "outcome"]},
            {"domain": "software_engineering", "topic": "system_design", "difficulty": "hard", "level": "senior",
             "question_text": "You're building a system that needs 99.99% uptime. Walk me through your architecture.",
             "follow_ups": ["How do you handle regional failover?", "What's your monitoring strategy?", "How do you do zero-downtime deployments?"],
             "expected_points": ["redundancy", "load balancing", "health checks", "circuit breakers", "chaos engineering"]},

            # === Behavioral / HR ===
            {"domain": "behavioral", "topic": "self_introduction", "difficulty": "easy", "level": "fresher",
             "question_text": "Tell me about yourself.",
             "follow_ups": ["What motivated you to apply for this role?", "Where do you see yourself in 5 years?"],
             "expected_points": ["structured response", "relevant highlights", "career narrative", "enthusiasm"]},
            {"domain": "behavioral", "topic": "teamwork", "difficulty": "easy", "level": "fresher",
             "question_text": "Describe a time when you worked in a team and faced a conflict. How did you resolve it?",
             "follow_ups": ["What was your specific role?", "What did you learn from the experience?"],
             "expected_points": ["STAR format", "specific example", "resolution approach", "learning"]},
            {"domain": "behavioral", "topic": "failure", "difficulty": "medium", "level": "mid",
             "question_text": "Tell me about a time you failed at something important. What happened and what did you learn?",
             "follow_ups": ["How did your team react?", "What would you do differently?"],
             "expected_points": ["honesty", "accountability", "specific learning", "growth mindset"]},
            {"domain": "behavioral", "topic": "leadership", "difficulty": "medium", "level": "mid",
             "question_text": "Give an example of when you took initiative without being asked.",
             "follow_ups": ["What was the impact?", "How did your manager respond?"],
             "expected_points": ["proactive behavior", "clear impact", "ownership mindset"]},

            # === Data Science ===
            {"domain": "data_science", "topic": "statistics", "difficulty": "easy", "level": "fresher",
             "question_text": "Explain the difference between Type 1 and Type 2 errors. Give a real-world example.",
             "follow_ups": ["Which is worse in a medical test scenario?", "How does sample size affect both?"],
             "expected_points": ["false positive vs false negative", "practical example", "tradeoff awareness"]},
            {"domain": "data_science", "topic": "ml", "difficulty": "medium", "level": "fresher",
             "question_text": "What is overfitting? How do you detect and prevent it?",
             "follow_ups": ["What is cross-validation?", "Explain regularization in simple terms"],
             "expected_points": ["train vs test performance gap", "regularization", "cross-validation", "more data"]},
            {"domain": "data_science", "topic": "ml", "difficulty": "medium", "level": "mid",
             "question_text": "You're building a model to predict customer churn. Walk me through your approach from data to deployment.",
             "follow_ups": ["How do you handle class imbalance?", "What metrics would you use?", "How do you explain the model to business stakeholders?"],
             "expected_points": ["EDA", "feature engineering", "model selection", "evaluation metrics", "deployment"]},

            # === UPSC ===
            {"domain": "upsc", "topic": "governance", "difficulty": "medium", "level": "all",
             "question_text": "India has been pushing for digital governance. What are the benefits and risks of increasing digitization in government services?",
             "follow_ups": ["What about digital divide in rural India?", "How do you balance privacy with transparency?"],
             "expected_points": ["efficiency gains", "digital divide", "privacy concerns", "cybersecurity", "balanced view"]},
            {"domain": "upsc", "topic": "ethics", "difficulty": "medium", "level": "all",
             "question_text": "You are posted as a District Collector. A powerful local politician is pressuring you to allot land illegally. What do you do?",
             "follow_ups": ["What if your transfer is threatened?", "How do you document this?"],
             "expected_points": ["rule of law", "documentation", "escalation", "integrity under pressure"]},
            {"domain": "upsc", "topic": "current_affairs", "difficulty": "easy", "level": "all",
             "question_text": "What is your opinion on India's approach to climate change? Is India doing enough?",
             "follow_ups": ["What about India's renewable energy targets?", "How should India balance growth and sustainability?"],
             "expected_points": ["development vs environment", "India's NDCs", "renewable energy progress", "balanced perspective"]},

            # === Company-Specific ===
            {"domain": "software_engineering", "topic": "coding", "difficulty": "medium", "level": "fresher",
             "question_text": "Write a function to check if a string is a palindrome, considering only alphanumeric characters.",
             "company_specific": "TCS",
             "follow_ups": ["What is the time complexity?", "Can you do it without extra space?"],
             "expected_points": ["two-pointer approach", "character filtering", "case handling", "O(n) time"]},
            {"domain": "software_engineering", "topic": "coding", "difficulty": "easy", "level": "fresher",
             "question_text": "What is the difference between '==' and '===' in JavaScript?",
             "company_specific": "Infosys",
             "follow_ups": ["Give an example where they produce different results", "Which should you prefer?"],
             "expected_points": ["type coercion", "strict equality", "practical preference"]},
            {"domain": "software_engineering", "topic": "system_design", "difficulty": "hard", "level": "mid",
             "question_text": "Design Google Docs — a collaborative real-time document editor.",
             "company_specific": "Google",
             "follow_ups": ["How do you handle conflicts?", "What about offline editing?", "How do you scale to millions of documents?"],
             "expected_points": ["OT or CRDT", "WebSocket", "versioning", "conflict resolution", "storage"]},

            # === Campus Placement — Technical (what TCS/Infosys/Wipro actually ask freshers) ===
            {"domain": "software_engineering", "topic": "oop", "difficulty": "easy", "level": "fresher",
             "question_text": "Explain the four pillars of Object-Oriented Programming with real-world examples.",
             "follow_ups": ["Can you give a code example of polymorphism?", "What is the difference between method overloading and overriding?"],
             "expected_points": ["encapsulation", "abstraction", "inheritance", "polymorphism", "real-world analogies"]},
            {"domain": "software_engineering", "topic": "dbms", "difficulty": "easy", "level": "fresher",
             "question_text": "What is normalization in DBMS? Explain 1NF, 2NF, and 3NF with examples.",
             "follow_ups": ["What is denormalization and when would you use it?", "What is a foreign key?"],
             "expected_points": ["removing redundancy", "1NF: atomic values", "2NF: no partial dependency", "3NF: no transitive dependency"]},
            {"domain": "software_engineering", "topic": "os", "difficulty": "easy", "level": "fresher",
             "question_text": "What is the difference between a process and a thread?",
             "follow_ups": ["What is a deadlock?", "How does a semaphore work?"],
             "expected_points": ["process has own memory space", "threads share memory", "context switching cost", "concurrency"]},
            {"domain": "software_engineering", "topic": "networking", "difficulty": "easy", "level": "fresher",
             "question_text": "Explain the difference between TCP and UDP. When would you use each?",
             "follow_ups": ["What is the three-way handshake?", "Give a real-world example of UDP usage."],
             "expected_points": ["connection-oriented vs connectionless", "reliability vs speed", "TCP: web/email", "UDP: streaming/gaming"]},
            {"domain": "software_engineering", "topic": "coding", "difficulty": "easy", "level": "fresher",
             "question_text": "Write a program to reverse a string without using built-in reverse functions.",
             "follow_ups": ["What is the time complexity?", "Can you do it in-place?"],
             "expected_points": ["loop-based swap", "O(n) time", "O(1) extra space for in-place"]},
            {"domain": "software_engineering", "topic": "coding", "difficulty": "easy", "level": "fresher",
             "question_text": "Write a program to check if a number is prime.",
             "follow_ups": ["How can you optimize this?", "What is the time complexity of your optimized solution?"],
             "expected_points": ["check divisibility up to sqrt(n)", "handle edge cases 0,1,2", "O(sqrt(n)) time"]},
            {"domain": "software_engineering", "topic": "coding", "difficulty": "medium", "level": "fresher",
             "question_text": "Write a program to find the second largest element in an array without sorting.",
             "follow_ups": ["What if there are duplicates?", "What is the time and space complexity?"],
             "expected_points": ["single pass with two variables", "handle duplicates", "O(n) time O(1) space"]},
            {"domain": "software_engineering", "topic": "sql", "difficulty": "easy", "level": "fresher",
             "question_text": "Write a SQL query to find the second highest salary from an Employee table.",
             "follow_ups": ["What if there are duplicate salaries?", "Can you do it without subqueries?"],
             "expected_points": ["subquery with MAX", "LIMIT OFFSET approach", "DENSE_RANK window function"]},

            # === Campus Placement — Behavioral (common in HR rounds) ===
            {"domain": "behavioral", "topic": "campus_hr", "difficulty": "easy", "level": "fresher",
             "question_text": "Are you willing to relocate anywhere in India? What about working in shifts?",
             "follow_ups": ["What if you are posted to a city far from your family?", "Have you ever lived away from home?"],
             "expected_points": ["willingness", "practical awareness", "past experience away from home", "positive attitude"]},
            {"domain": "behavioral", "topic": "campus_hr", "difficulty": "easy", "level": "fresher",
             "question_text": "Tell me about the service bond. Are you comfortable with it?",
             "follow_ups": ["What if you get a better offer during the bond period?", "Why do you think companies have bond periods?"],
             "expected_points": ["understanding of bond terms", "commitment", "loyalty reasoning", "honest response"]},
            {"domain": "behavioral", "topic": "campus_hr", "difficulty": "easy", "level": "fresher",
             "question_text": "What are your salary expectations for a fresher role?",
             "follow_ups": ["What if we offer less than what you expected?", "What matters more to you — salary or learning?"],
             "expected_points": ["realistic expectation", "market awareness", "emphasis on learning", "flexibility"]},
            {"domain": "behavioral", "topic": "campus_hr", "difficulty": "medium", "level": "fresher",
             "question_text": "You have a gap in your academic record. Can you explain what happened?",
             "follow_ups": ["What did you learn from that period?", "How did you get back on track?"],
             "expected_points": ["honest explanation", "growth mindset", "lessons learned", "resilience"]},
            {"domain": "behavioral", "topic": "campus_hr", "difficulty": "easy", "level": "fresher",
             "question_text": "Why should we hire you over other candidates from your college?",
             "follow_ups": ["What unique qualities do you bring?", "Give me a specific example."],
             "expected_points": ["specific strengths", "concrete examples", "self-awareness", "not generic"]},

            # === Campus Placement — Aptitude (verbal reasoning for interview discussion) ===
            {"domain": "aptitude", "topic": "logical_reasoning", "difficulty": "easy", "level": "fresher",
             "question_text": "If you have 8 balls and one is heavier, what is the minimum number of weighings needed to find the heavier ball using a balance scale?",
             "follow_ups": ["Walk me through your approach step by step.", "What if there were 27 balls?"],
             "expected_points": ["2 weighings", "divide into groups of 3", "elimination strategy", "generalization to log base 3"]},
        ]

        for q in questions:
            self.add_question(**q)

    def _seed_companies(self):
        companies = [
            {
                "company_name": "TCS",
                "industry": "IT Services",
                "interview_process": {
                    "rounds": ["Aptitude Test", "Technical Interview", "Managerial Interview", "HR Interview"],
                    "duration": "1-2 days for campus, 2-3 weeks for lateral",
                    "mode": "On-campus or virtual",
                },
                "common_questions": [
                    "Tell me about yourself",
                    "Why TCS?",
                    "Explain OOP concepts",
                    "Write a program to reverse a string",
                    "Difference between DBMS and RDBMS",
                    "What is your expected CTC?",
                ],
                "salary_ranges": {"fresher": "3.3-3.6 LPA", "digital_fresher": "7-7.5 LPA", "experienced_3yr": "5-8 LPA"},
                "evaluation_priorities": ["communication", "aptitude", "basic_coding", "willingness_to_learn"],
                "culture_notes": "Process-driven, values loyalty, large team environment. Expect to work on client projects. Bond period of 1 year.",
                "hiring_bar": "Medium — focuses on aptitude and communication more than deep tech",
                "tips": ["Practice aptitude (quant, verbal, reasoning)", "Be ready for basic coding in C/Java/Python", "Show willingness to relocate", "Don't negotiate salary for fresher roles"],
            },
            {
                "company_name": "Infosys",
                "industry": "IT Services",
                "interview_process": {
                    "rounds": ["Online Test", "Technical Interview", "HR Interview"],
                    "duration": "1 day for campus",
                    "mode": "On-campus or InfyTQ platform",
                },
                "common_questions": [
                    "Tell me about yourself",
                    "Why Infosys?",
                    "Explain SDLC",
                    "Difference between Java and Python",
                    "What is cloud computing?",
                    "Where do you see yourself in 5 years?",
                ],
                "salary_ranges": {"fresher_se": "3.6 LPA", "fresher_specialist": "5-6 LPA", "power_programmer": "8-9 LPA"},
                "evaluation_priorities": ["aptitude", "communication", "basic_tech", "cultural_fit"],
                "culture_notes": "Innovation-focused (Infosys BPM, Infosys Nia). Values continuous learning. Strong training program (Mysore campus).",
                "hiring_bar": "Medium — InfyTQ certification gives edge",
                "tips": ["Complete InfyTQ certification for better package", "Practice HackerRank-style problems", "Show interest in emerging tech"],
            },
            {
                "company_name": "Wipro",
                "industry": "IT Services",
                "interview_process": {
                    "rounds": ["Online Assessment", "Technical Interview", "HR Interview"],
                    "duration": "1-2 days",
                    "mode": "On-campus or virtual (WILP/Elite programs)",
                },
                "common_questions": [
                    "Tell me about yourself",
                    "Why do you want to join Wipro?",
                    "Explain DBMS normalization",
                    "What is agile methodology?",
                    "Write a program for fibonacci series",
                ],
                "salary_ranges": {"fresher": "3.5-4 LPA", "elite": "6.5 LPA", "turbo": "9 LPA"},
                "evaluation_priorities": ["aptitude", "communication", "basic_programming", "adaptability"],
                "culture_notes": "Focus on digital transformation. Multiple hiring tracks (WILP, Elite, Turbo). Spirit of Wipro values.",
                "hiring_bar": "Medium",
                "tips": ["Apply through Elite/Turbo for higher package", "Practice amcat-style aptitude", "Show awareness of Wipro's digital initiatives"],
            },
            {
                "company_name": "Google",
                "industry": "Technology",
                "interview_process": {
                    "rounds": ["Phone Screen", "4-5 Onsite Rounds (Coding + System Design + Behavioral)", "Hiring Committee Review"],
                    "duration": "4-8 weeks total",
                    "mode": "Virtual or on-site (Bangalore/Hyderabad)",
                },
                "common_questions": [
                    "Design a distributed cache",
                    "Implement LRU cache",
                    "System design: YouTube/Gmail/Maps",
                    "Tell me about a time you dealt with ambiguity",
                    "How would you improve Google Search?",
                ],
                "salary_ranges": {"L3": "25-35 LPA", "L4": "35-55 LPA", "L5": "55-85 LPA"},
                "evaluation_priorities": ["coding", "algorithms", "system_design", "googleyness", "leadership"],
                "culture_notes": "Data-driven, flat hierarchy, 20% time, strong engineering culture. Values innovation and impact.",
                "hiring_bar": "Very High — false negatives preferred over false positives",
                "tips": ["Practice LeetCode medium/hard", "Study 'Designing Data-Intensive Applications'", "Prepare behavioral with STAR method", "Mock interviews are essential"],
            },
            {
                "company_name": "Amazon",
                "industry": "Technology",
                "interview_process": {
                    "rounds": ["Online Assessment (OA)", "Phone Screen", "4-5 Loop Rounds (Coding + System Design + Leadership Principles)"],
                    "duration": "3-6 weeks",
                    "mode": "Virtual or Bangalore/Hyderabad office",
                },
                "common_questions": [
                    "Tell me about a time you disagreed with your manager",
                    "Design an e-commerce recommendation system",
                    "Implement a trie data structure",
                    "How would you handle conflicting priorities?",
                    "Tell me about a time you delivered results under tight deadline",
                ],
                "salary_ranges": {"SDE1": "25-40 LPA", "SDE2": "40-65 LPA", "SDE3": "70-100 LPA"},
                "evaluation_priorities": ["leadership_principles", "coding", "system_design", "ownership", "customer_obsession"],
                "culture_notes": "Leadership Principles are everything. Customer obsession, ownership, bias for action. Fast-paced, high-bar.",
                "hiring_bar": "Very High — every interview is evaluated against Leadership Principles",
                "tips": ["Memorize all 16 Leadership Principles", "Prepare 2 stories per LP", "Practice system design at scale", "Show ownership and customer focus in every answer"],
            },
            {
                "company_name": "Microsoft",
                "industry": "Technology",
                "interview_process": {
                    "rounds": ["Online Assessment", "Phone Screen", "4 Onsite Rounds (Coding + Design + Behavioral)"],
                    "duration": "3-5 weeks",
                    "mode": "Virtual or Bangalore/Hyderabad/Noida office",
                },
                "common_questions": [
                    "Design a parking lot system",
                    "Implement a binary search tree",
                    "Tell me about your most impactful project",
                    "How do you handle technical debt?",
                    "Design Microsoft Teams notification system",
                ],
                "salary_ranges": {"SDE_59": "18-28 LPA", "SDE_60": "28-42 LPA", "SDE2_61": "38-55 LPA", "Senior_62": "55-80 LPA"},
                "evaluation_priorities": ["coding", "problem_solving", "design", "collaboration", "growth_mindset"],
                "culture_notes": "Growth mindset culture (Satya Nadella era). Collaborative, inclusive. Values learning and customer empathy.",
                "hiring_bar": "High — looks for growth mindset and collaboration alongside technical skill",
                "tips": ["Study low-level design + OOP patterns", "Show growth mindset", "Practice collaborative problem-solving", "Understand Azure basics"],
            },
            {
                "company_name": "Cognizant",
                "industry": "IT Services",
                "interview_process": {
                    "rounds": ["Online Assessment (Aptitude + Coding)", "Technical Interview", "HR Interview"],
                    "duration": "1-2 days for campus",
                    "mode": "On-campus or virtual (GenC / GenC Next / GenC Elevate tracks)",
                },
                "common_questions": [
                    "Tell me about yourself",
                    "Why Cognizant?",
                    "Explain OOP concepts with examples",
                    "Difference between stack and queue",
                    "What is normalization in DBMS?",
                    "Write a program to find the second largest element in an array",
                    "What is your understanding of Agile?",
                ],
                "salary_ranges": {"GenC": "4-4.5 LPA", "GenC_Next": "6.5-7 LPA", "GenC_Elevate": "9-9.5 LPA"},
                "evaluation_priorities": ["aptitude", "communication", "basic_coding", "logical_reasoning", "adaptability"],
                "culture_notes": "Digital-first culture. Strong focus on upskilling and continuous learning. Multiple hiring tracks with increasing difficulty and pay (GenC < GenC Next < GenC Elevate). Part of the Tata Group ecosystem. Large presence in Chennai, Hyderabad, Pune.",
                "hiring_bar": "Medium — GenC has lower bar; GenC Elevate requires strong coding + aptitude",
                "tips": ["Practice AMCAT-style aptitude (quant + logical + verbal)", "For GenC Elevate, practice coding on HackerRank/LeetCode (easy-medium)", "Research Cognizant's digital transformation initiatives", "Show willingness to learn new technologies", "Be ready for situational/behavioral questions in HR round"],
            },
            {
                "company_name": "Accenture",
                "industry": "IT Services & Consulting",
                "interview_process": {
                    "rounds": ["Cognitive & Technical Assessment", "Coding Round", "Communication Assessment", "Interview (Technical + HR)"],
                    "duration": "1-2 days for campus",
                    "mode": "On-campus or virtual",
                },
                "common_questions": [
                    "Tell me about yourself",
                    "Why Accenture?",
                    "Explain the difference between C and Java",
                    "What is cloud computing? Name some providers",
                    "Explain polymorphism with example",
                    "Write a program to check if a number is prime",
                    "Tell me about a time you worked under pressure",
                    "What do you know about Accenture's services?",
                ],
                "salary_ranges": {"ASE": "4.5 LPA", "ACE": "7-7.5 LPA", "advanced_track": "9-11 LPA"},
                "evaluation_priorities": ["cognitive_ability", "communication", "technical_fundamentals", "teamwork", "client_readiness"],
                "culture_notes": "Global consulting and IT services firm. Strong emphasis on communication and client-facing skills. Values diversity and inclusion. Rotational model means freshers may work across technologies. Large training programs at Bangalore campus. Bond period of 2 years for freshers.",
                "hiring_bar": "Medium — cognitive + communication weighted heavily alongside technical",
                "tips": ["Practice cognitive ability tests (pattern recognition, logical reasoning)", "Communication assessment is scored separately — practice spoken English", "Know about Accenture's key service areas (Technology, Strategy, Consulting, Operations)", "For ACE track, prepare coding in Java/Python", "Show awareness of emerging tech (AI, cloud, blockchain)"],
            },
            {
                "company_name": "HCL Technologies",
                "industry": "IT Services",
                "interview_process": {
                    "rounds": ["Online Test (Aptitude + Technical)", "Technical Interview", "HR Interview"],
                    "duration": "1-2 days for campus",
                    "mode": "On-campus or virtual",
                },
                "common_questions": [
                    "Tell me about yourself",
                    "Why HCL?",
                    "Explain OOP with real-world examples",
                    "What is the difference between process and thread?",
                    "Write a program to check if a string is palindrome",
                    "Explain normalization in DBMS",
                    "What are your strengths and weaknesses?",
                ],
                "salary_ranges": {"fresher": "3.5-4 LPA", "TechBee": "2-3 LPA (10+2 track)", "experienced_3yr": "6-9 LPA"},
                "evaluation_priorities": ["aptitude", "technical_fundamentals", "communication", "problem_solving"],
                "culture_notes": "Employee-first culture (Ideapreneurship). Strong presence in infrastructure management and cybersecurity. Mode 1-2-3 framework. Large operations in Noida, Chennai, Madurai. Bond period of 1 year for freshers.",
                "hiring_bar": "Medium — balanced aptitude + technical assessment",
                "tips": ["Practice aptitude thoroughly (HCL's test is moderately difficult)", "Be ready for OS and networking basics", "Know about HCL's Mode 1-2-3 strategy", "Show interest in infrastructure/cloud services", "Be ready for relocation to Noida/Chennai"],
            },
            {
                "company_name": "Tech Mahindra",
                "industry": "IT Services & Telecom",
                "interview_process": {
                    "rounds": ["Online Assessment (Aptitude + English + Coding)", "Technical Interview", "Group Discussion (sometimes)", "HR Interview"],
                    "duration": "1-2 days for campus",
                    "mode": "On-campus or virtual",
                },
                "common_questions": [
                    "Tell me about yourself",
                    "Why Tech Mahindra?",
                    "Explain polymorphism with example",
                    "What is the difference between TCP and UDP?",
                    "Write a program to find factorial of a number",
                    "What is cloud computing?",
                    "Discuss a recent technology trend",
                    "GD topics: AI replacing jobs, 5G impact, remote work future",
                ],
                "salary_ranges": {"fresher": "3.25-3.75 LPA", "digital_track": "5-6 LPA", "experienced_3yr": "5-8 LPA"},
                "evaluation_priorities": ["communication", "aptitude", "basic_tech", "teamwork", "current_affairs_awareness"],
                "culture_notes": "Part of Mahindra Group. Strong in telecom and 5G. Rise philosophy — values community and sustainability. GD is common in campus hiring. Operations in Pune, Hyderabad, Chennai, Noida. Bond period of 1 year.",
                "hiring_bar": "Medium — GD round is a differentiator; communication weighted heavily",
                "tips": ["Prepare for GD — practice articulating opinions on tech topics", "Know about 5G and telecom basics (Tech Mahindra's core domain)", "Practice English communication — scored separately in online test", "Know about Tech Mahindra's Rise philosophy", "Be ready to discuss current affairs and tech trends"],
            },
            {
                "company_name": "Capgemini",
                "industry": "IT Services & Consulting",
                "interview_process": {
                    "rounds": ["Game-Based Assessment (Plum)", "Pseudo Code MCQ Test", "Technical + Communication Interview", "HR Interview"],
                    "duration": "1-2 days for campus",
                    "mode": "On-campus or virtual",
                },
                "common_questions": [
                    "Tell me about yourself",
                    "Why Capgemini?",
                    "Explain the concept of inheritance",
                    "What is the difference between array and linked list?",
                    "Write pseudo code for binary search",
                    "What do you understand by DevOps?",
                    "Describe a challenging situation you handled",
                    "Where do you see yourself in 3 years?",
                ],
                "salary_ranges": {"analyst": "3.8 LPA", "senior_analyst": "5-6 LPA", "elevated_track": "7-8 LPA"},
                "evaluation_priorities": ["cognitive_ability", "pseudo_code_logic", "communication", "behavioral_traits", "adaptability"],
                "culture_notes": "European heritage (French company). Strong emphasis on innovation and sustainability. Game-based assessment (Plum) is unique — tests cognitive traits, not just aptitude. Values diversity. Operations in Mumbai, Pune, Bangalore, Chennai. 18-month bond for freshers.",
                "hiring_bar": "Medium — game-based assessment is different from traditional aptitude tests",
                "tips": ["Practice pseudo code — Capgemini's test is logic-based, not language-specific", "Do well in Plum assessment (game-based) — this is the first filter", "Research Capgemini's DAGGER framework and consulting approach", "Communication round is separate and important", "Show adaptability and willingness to work across domains"],
            },
        ]

        for c in companies:
            self.add_company_profile(**c)

    def _seed_rubrics(self):
        rubrics = [
            {
                "dimension": "communication", "level": "fresher",
                "score_1_2": "Incoherent, cannot form complete sentences. Long pauses. No structure.",
                "score_3_4": "Basic communication but unclear. Rambles. Poor vocabulary. Needs multiple clarifications.",
                "score_5_6": "Adequate communication. Can explain ideas but lacks polish. Occasional filler words.",
                "score_7_8": "Clear, structured communication. Good vocabulary. Explains complex ideas simply. Confident.",
                "score_9_10": "Exceptional communicator. Articulate, concise, engaging. Adapts explanation to audience.",
                "key_indicators": ["clarity", "structure", "confidence", "vocabulary", "conciseness"],
                "red_flags": ["excessive filler words", "inability to complete thoughts", "memorized scripts"],
            },
            {
                "dimension": "technical_depth", "level": "fresher",
                "score_1_2": "Cannot explain basic concepts. No understanding of fundamentals.",
                "score_3_4": "Knows definitions but cannot apply. Superficial understanding. Fails follow-up questions.",
                "score_5_6": "Solid fundamentals. Can solve standard problems. Struggles with edge cases.",
                "score_7_8": "Strong understanding. Can apply concepts to new problems. Knows tradeoffs.",
                "score_9_10": "Exceptional depth. Can discuss internals, optimizations, and alternatives. Clear mental model.",
                "key_indicators": ["fundamentals", "application", "tradeoff awareness", "depth of explanation"],
                "red_flags": ["memorized answers without understanding", "cannot handle follow-ups", "buzzword dropping"],
            },
            {
                "dimension": "problem_solving", "level": "fresher",
                "score_1_2": "Cannot approach unfamiliar problems. Gives up immediately.",
                "score_3_4": "Tries but uses trial-and-error without structure. Cannot break down problems.",
                "score_5_6": "Reasonable approach. Can break down problems. May miss edge cases.",
                "score_7_8": "Structured problem-solving. Considers multiple approaches. Handles edge cases.",
                "score_9_10": "Excellent analytical thinking. Creative solutions. Optimizes naturally.",
                "key_indicators": ["structured approach", "breaking down", "edge cases", "optimization"],
                "red_flags": ["random guessing", "giving up quickly", "cannot think aloud"],
            },
            {
                "dimension": "culture_fit", "level": "fresher",
                "score_1_2": "Negative attitude. Shows no interest in company or role. Red flag behaviors.",
                "score_3_4": "Neutral. Generic answers. No research on company. Purely transactional.",
                "score_5_6": "Positive attitude. Some awareness of company. Willing to learn.",
                "score_7_8": "Strong alignment with values. Has researched the company. Genuine enthusiasm.",
                "score_9_10": "Perfect fit. Deep understanding of company culture. Values alignment. Authentic enthusiasm.",
                "key_indicators": ["company research", "value alignment", "enthusiasm", "team orientation"],
                "red_flags": ["badmouthing previous employers", "only interested in salary", "no questions about the role"],
            },
            {
                "dimension": "system_design", "level": "mid",
                "score_1_2": "Cannot design basic systems. No understanding of scalability.",
                "score_3_4": "Knows components but cannot connect them. Design is a list, not a system.",
                "score_5_6": "Can design working systems. Handles basic scalability. Misses some tradeoffs.",
                "score_7_8": "Strong designs with clear tradeoffs. Considers failure modes. Knows when to use what.",
                "score_9_10": "Expert-level design. Anticipates problems. Discusses CAP theorem, consistency models, caching strategies naturally.",
                "key_indicators": ["component selection", "scalability", "tradeoffs", "failure handling", "data flow"],
                "red_flags": ["no consideration of scale", "single point of failure", "cannot justify choices"],
            },
            {
                "dimension": "leadership", "level": "senior",
                "score_1_2": "No leadership experience or awareness. Individual contributor mindset only.",
                "score_3_4": "Has managed tasks but not people. Cannot articulate leadership philosophy.",
                "score_5_6": "Some leadership experience. Can delegate and coordinate. Still developing.",
                "score_7_8": "Strong leader. Mentors others. Drives technical direction. Handles conflicts well.",
                "score_9_10": "Exceptional leader. Builds teams, shapes culture, drives org-level impact. Inspires others.",
                "key_indicators": ["mentoring", "decision-making", "conflict resolution", "vision", "team building"],
                "red_flags": ["takes all credit", "cannot delegate", "avoids difficult conversations"],
            },
        ]

        for r in rubrics:
            self.add_rubric(**r)

    def _seed_indian_context(self):
        contexts = [
            {
                "category": "interview_culture",
                "topic": "greeting_etiquette",
                "content": "Indian interviews typically start with 'Good morning/afternoon, sir/ma'am'. Addressing interviewers respectfully is important. A slight head nod or namaste is common. Don't use first names unless invited to.",
                "tips": ["Greet each panelist", "Use sir/ma'am initially", "Wait to be asked to sit"],
            },
            {
                "category": "interview_culture",
                "topic": "salary_negotiation",
                "content": "In India, salary negotiation culture varies by company type. IT services (TCS/Infosys) have fixed packages for freshers — don't negotiate. Startups and product companies expect negotiation. Always research salary bands on Glassdoor/AmbitionBox before the interview.",
                "tips": ["Don't negotiate at mass recruiters", "Research market rates", "Quote a range not a fixed number", "Consider total CTC not just base"],
            },
            {
                "category": "interview_culture",
                "topic": "common_mistakes",
                "content": "Common mistakes in Indian interviews: 1) Memorized 'Tell me about yourself' that sounds scripted, 2) Saying 'I want to learn' without showing what you've already learned, 3) Not asking questions to the panel, 4) Badmouthing previous company, 5) Bringing up caste/religion/politics unprompted.",
                "tips": ["Prepare but don't memorize", "Show self-learning ability", "Always have 2-3 questions ready"],
            },
            {
                "category": "campus_placement",
                "topic": "process_overview",
                "content": "Indian campus placements follow a structured process: Pre-Placement Talk (PPT) → Online Test (Aptitude + Coding) → Group Discussion (for some) → Technical Interview → HR Interview. Companies visit in order of CTC — highest paying first (Day 1 companies). Once placed, students are typically out of the placement pool.",
                "tips": ["Attend PPTs to understand company culture", "Day 1 companies have highest bar", "Prepare aptitude early"],
            },
            {
                "category": "campus_placement",
                "topic": "tier_system",
                "content": "Indian colleges are informally tiered: Tier 1 (IITs, NITs, BITS, IIITs — top 100), Tier 2 (good state/private colleges — next 500), Tier 3 (remaining). The companies that visit and packages offered vary dramatically by tier. Tier 2/3 students should focus on IT services companies and build strong fundamentals.",
                "tips": ["Focus on what visits YOUR campus", "Build projects to stand out from Tier 2/3", "Online assessments are the equalizer"],
            },
            {
                "category": "upsc",
                "topic": "personality_test_format",
                "content": "The UPSC Personality Test (interview) is conducted by a board of 4-5 members chaired by a senior bureaucrat/academic. Duration: 25-30 minutes. It tests personality, not knowledge. The board starts from your DAF (Detailed Application Form) — hobbies, optional subject, home state, work experience. They assess suitability for civil services.",
                "tips": ["Know your DAF thoroughly", "Have opinions on current affairs", "Show balanced perspective", "Don't bluff — say 'I don't know' if needed"],
            },
            {
                "category": "gd",
                "topic": "group_discussion_format",
                "content": "Group Discussions (GDs) are common in MBA admissions (IIMs, XLRI) and some campus placements. Format: 8-12 participants, 15-20 min, observed by 2-3 panelists. Evaluated on: content quality, communication, leadership, teamwork, body language. Common mistake: being too aggressive or too silent.",
                "tips": ["Initiate if possible but don't force it", "Listen and build on others' points", "Use data and examples", "Summarize if you haven't spoken enough", "Don't interrupt aggressively"],
            },
        ]

        for c in contexts:
            self.add_indian_context(**c)

    # =====================================================
    # BULK OPERATIONS (used by seed_knowledge.py)
    # =====================================================

    def wipe_all(self):
        """Delete all data from all tables. Used by seed script for idempotent re-seeding."""
        conn = self._get_conn()
        for table in ["question_bank", "company_profiles", "persona_templates",
                      "evaluation_rubrics", "indian_context",
                      "company_hiring_tracks", "company_round_blueprints",
                      "default_round_blueprints"]:
            conn.execute(f"DELETE FROM {table}")
        conn.commit()

    def bulk_add_questions(self, questions: List[dict]) -> int:
        """Insert multiple questions in a single transaction."""
        conn = self._get_conn()
        count = 0
        for q in questions:
            conn.execute(
                "INSERT INTO question_bank "
                "(domain, topic, difficulty, level, question_text, follow_ups, "
                "scoring_rubric, expected_points, company_specific, tags, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (q["domain"], q["topic"], q["difficulty"], q["level"], q["question_text"],
                 json.dumps(q.get("follow_ups", [])), json.dumps(q.get("scoring_rubric", {})),
                 json.dumps(q.get("expected_points", [])), q.get("company_specific", ""),
                 json.dumps(q.get("tags", [])), datetime.now().isoformat()),
            )
            count += 1
        conn.commit()
        return count

    def bulk_add_companies(self, companies: List[dict]) -> int:
        """Insert multiple company profiles in a single transaction."""
        conn = self._get_conn()
        now = datetime.now().isoformat()
        count = 0
        for c in companies:
            conn.execute(
                "INSERT OR REPLACE INTO company_profiles "
                "(company_name, industry, interview_process, common_questions, "
                "salary_ranges, evaluation_priorities, culture_notes, hiring_bar, "
                "tips, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (c["company_name"], c.get("industry", ""),
                 json.dumps(c.get("interview_process", {})),
                 json.dumps(c.get("common_questions", [])),
                 json.dumps(c.get("salary_ranges", {})),
                 json.dumps(c.get("evaluation_priorities", [])),
                 c.get("culture_notes", ""), c.get("hiring_bar", ""),
                 json.dumps(c.get("tips", [])), now, now),
            )
            count += 1
        conn.commit()
        return count

    def bulk_add_personas(self, personas: List[dict]) -> int:
        """Insert multiple persona templates in a single transaction."""
        conn = self._get_conn()
        count = 0
        for p in personas:
            conn.execute(
                "INSERT INTO persona_templates "
                "(domain, level, role, name, personality, question_style, system_prompt, "
                "traits, eval_dimensions, expertise, voice_config, interaction_style, "
                "avatar_color, tags, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (p["domain"], p["level"], p["role"], p["name"],
                 p["personality"], p["question_style"], p["system_prompt"],
                 json.dumps(p.get("traits", {})), json.dumps(p.get("eval_dimensions", [])),
                 json.dumps(p.get("expertise", [])), json.dumps(p.get("voice_config", {})),
                 p.get("interaction_style", "independent"),
                 p.get("avatar_color", "#6366f1"), json.dumps(p.get("tags", [])),
                 datetime.now().isoformat()),
            )
            count += 1
        conn.commit()
        return count

    def bulk_add_rubrics(self, rubrics: List[dict]) -> int:
        """Insert multiple evaluation rubrics in a single transaction."""
        conn = self._get_conn()
        count = 0
        for r in rubrics:
            conn.execute(
                "INSERT INTO evaluation_rubrics "
                "(dimension, level, score_1_2, score_3_4, score_5_6, score_7_8, "
                "score_9_10, key_indicators, red_flags, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (r["dimension"], r["level"], r["score_1_2"], r["score_3_4"],
                 r["score_5_6"], r["score_7_8"], r["score_9_10"],
                 json.dumps(r.get("key_indicators", [])),
                 json.dumps(r.get("red_flags", [])),
                 datetime.now().isoformat()),
            )
            count += 1
        conn.commit()
        return count

    def bulk_add_indian_context(self, contexts: List[dict]) -> int:
        """Insert multiple indian context entries in a single transaction."""
        conn = self._get_conn()
        count = 0
        for c in contexts:
            conn.execute(
                "INSERT INTO indian_context (category, topic, content, tips, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (c["category"], c["topic"], c["content"],
                 json.dumps(c.get("tips", [])),
                 datetime.now().isoformat()),
            )
            count += 1
        conn.commit()
        return count

    def bulk_add_hiring_tracks(self, tracks: List[dict]) -> int:
        """Insert multiple hiring tracks in a single transaction."""
        conn = self._get_conn()
        count = 0
        for t in tracks:
            conn.execute(
                "INSERT OR REPLACE INTO company_hiring_tracks "
                "(company_name, track_code, track_name, target_levels, salary_range, "
                "eligibility, difficulty_tier, description, selection_test, bond_years, "
                "training_info, is_default, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (t["company_name"], t["track_code"], t["track_name"],
                 json.dumps(t.get("target_levels", [])), t["salary_range"],
                 json.dumps(t.get("eligibility", {})), t["difficulty_tier"],
                 t.get("description", ""), t.get("selection_test", ""),
                 t.get("bond_years", 0), t.get("training_info", ""),
                 t.get("is_default", 0), datetime.now().isoformat()),
            )
            count += 1
        conn.commit()
        return count

    def bulk_add_round_blueprints(self, blueprints: List[dict]) -> int:
        """Insert multiple round blueprints in a single transaction."""
        conn = self._get_conn()
        count = 0
        for b in blueprints:
            conn.execute(
                "INSERT OR REPLACE INTO company_round_blueprints "
                "(company_name, track_code, round_num, round_type, round_label, "
                "focus_areas, difficulty, max_questions, interviewer_role_hint, "
                "personality_hint, question_style_hint, eval_dimensions, notes, "
                "is_eliminatory, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (b["company_name"], b["track_code"], b["round_num"],
                 b["round_type"], b["round_label"], json.dumps(b["focus_areas"]),
                 b["difficulty"], b.get("max_questions", 8),
                 b.get("interviewer_role_hint", ""), b.get("personality_hint", ""),
                 b.get("question_style_hint", ""),
                 json.dumps(b.get("eval_dimensions", [])),
                 b.get("notes", ""), b.get("is_eliminatory", 0),
                 datetime.now().isoformat()),
            )
            count += 1
        conn.commit()
        return count

    def bulk_add_default_blueprints(self, blueprints: List[dict]) -> int:
        """Insert multiple default blueprints in a single transaction."""
        conn = self._get_conn()
        count = 0
        for b in blueprints:
            conn.execute(
                "INSERT OR REPLACE INTO default_round_blueprints "
                "(domain, experience_level, round_num, round_type, round_label, "
                "focus_areas, difficulty, max_questions, interviewer_role_hint, "
                "personality_hint, question_style_hint, eval_dimensions, notes, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (b["domain"], b["experience_level"], b["round_num"],
                 b["round_type"], b["round_label"], json.dumps(b["focus_areas"]),
                 b["difficulty"], b.get("max_questions", 8),
                 b.get("interviewer_role_hint", ""), b.get("personality_hint", ""),
                 b.get("question_style_hint", ""),
                 json.dumps(b.get("eval_dimensions", [])),
                 b.get("notes", ""), datetime.now().isoformat()),
            )
            count += 1
        conn.commit()
        return count

    # =====================================================
    # UTILITY
    # =====================================================

    def get_stats(self) -> dict:
        conn = self._get_conn()
        return {
            "persona_templates": conn.execute("SELECT COUNT(*) FROM persona_templates").fetchone()[0],
            "questions": conn.execute("SELECT COUNT(*) FROM question_bank").fetchone()[0],
            "companies": conn.execute("SELECT COUNT(*) FROM company_profiles").fetchone()[0],
            "rubrics": conn.execute("SELECT COUNT(*) FROM evaluation_rubrics").fetchone()[0],
            "indian_context": conn.execute("SELECT COUNT(*) FROM indian_context").fetchone()[0],
            "hiring_tracks": conn.execute("SELECT COUNT(*) FROM company_hiring_tracks").fetchone()[0],
            "round_blueprints": conn.execute("SELECT COUNT(*) FROM company_round_blueprints").fetchone()[0],
            "default_blueprints": conn.execute("SELECT COUNT(*) FROM default_round_blueprints").fetchone()[0],
        }

    def close(self):
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None
