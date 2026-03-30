"""
Company Round Blueprints — Deterministic round structures per hiring track.

Each blueprint row defines one round in a company's interview process:
  - round_type: maps to InterviewerEngine ROUND_PHASES keys
  - focus_areas: what this round tests
  - difficulty: easy / medium / hard / expert
  - interviewer_role_hint: suggested role for the AI interviewer
  - personality_hint: maps to InterviewerEngine PERSONALITY_BEHAVIORS
  - question_style_hint: guidance for question selection
  - eval_dimensions: what to score after this round
  - is_eliminatory: if True, poor performance here can end the process

Default blueprints cover unknown companies:
  5 domains × 5 experience levels = 25 default blueprints
"""
from typing import List, Dict


def _r(
    company: str, track: str, rnum: int, rtype: str, label: str,
    focus: list, diff: str, max_q: int = 6,
    role_hint: str = "", personality: str = "neutral",
    style_hint: str = "", eval_dims: list = None,
    notes: str = "", eliminatory: int = 0,
) -> Dict:
    return {
        "company_name": company,
        "track_code": track,
        "round_num": rnum,
        "round_type": rtype,
        "round_label": label,
        "focus_areas": focus,
        "difficulty": diff,
        "max_questions": max_q,
        "interviewer_role_hint": role_hint,
        "personality_hint": personality,
        "question_style_hint": style_hint,
        "eval_dimensions": eval_dims or [],
        "notes": notes,
        "is_eliminatory": eliminatory,
    }


def _d(
    domain: str, level: str, rnum: int, rtype: str, label: str,
    focus: list, diff: str, max_q: int = 6,
    role_hint: str = "", personality: str = "neutral",
    style_hint: str = "", eval_dims: list = None,
    notes: str = "",
) -> Dict:
    """Default blueprint row (no company)."""
    return {
        "domain": domain,
        "experience_level": level,
        "round_num": rnum,
        "round_type": rtype,
        "round_label": label,
        "focus_areas": focus,
        "difficulty": diff,
        "max_questions": max_q,
        "interviewer_role_hint": role_hint,
        "personality_hint": personality,
        "question_style_hint": style_hint,
        "eval_dimensions": eval_dims or [],
        "notes": notes,
    }


# ════════════════════════════════════════════════════════
# Reusable eval dimension sets
# ════════════════════════════════════════════════════════

_TECH_DIMS = ["technical_depth", "problem_solving", "coding_ability", "system_thinking"]
_BEHAVIORAL_DIMS = ["communication", "teamwork", "leadership", "conflict_resolution"]
_HR_DIMS = ["communication", "cultural_fit", "professionalism", "motivation"]
_DESIGN_DIMS = ["system_thinking", "scalability", "trade_off_analysis", "communication"]
_STRESS_DIMS = ["composure", "clarity_under_pressure", "logical_thinking", "confidence"]
_APTITUDE_DIMS = ["logical_reasoning", "quantitative_aptitude", "verbal_ability"]


def get_round_blueprints() -> List[Dict]:
    return [
        # ════════════════════════════════════════
        # TCS Ninja — 3 rounds (mass hiring, easy)
        # ════════════════════════════════════════
        _r("TCS", "tcs_ninja", 1, "technical", "Technical Interview",
           ["basic_programming", "oops", "dbms", "data_structures"],
           "easy", 6, "Technical Interviewer",
           "friendly", "Ask fundamentals, no tricky questions. Focus on clarity of basics.",
           _TECH_DIMS, "Mass hiring — focus on fundamentals, not depth", 1),

        _r("TCS", "tcs_ninja", 2, "behavioral", "Managerial Round",
           ["teamwork", "academics", "career_goals", "learning_ability"],
           "easy", 5, "Manager",
           "warm_but_probing", "STAR-style questions about college projects and teamwork.",
           _BEHAVIORAL_DIMS, "Assess cultural fit and willingness to learn"),

        _r("TCS", "tcs_ninja", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "bond_acceptance", "company_knowledge"],
           "easy", 4, "HR Manager",
           "friendly", "Standard HR questions. Check willingness to relocate and accept bond.",
           _HR_DIMS, "2-year bond discussion is critical"),

        # ════════════════════════════════════════
        # TCS Digital — 4 rounds (higher bar)
        # ════════════════════════════════════════
        _r("TCS", "tcs_digital", 1, "technical", "Technical Round 1 — Fundamentals",
           ["data_structures", "algorithms", "oops", "dbms", "os"],
           "medium", 7, "Senior Developer",
           "neutral", "Deeper than Ninja. Expect understanding of time complexity and DB normalization.",
           _TECH_DIMS, "Must show depth beyond definitions", 1),

        _r("TCS", "tcs_digital", 2, "technical", "Technical Round 2 — Applied",
           ["coding", "problem_solving", "system_basics", "api_design"],
           "medium", 6, "Tech Lead",
           "warm_but_probing", "Coding-oriented. Ask to design a small module or debug pseudo-code.",
           _TECH_DIMS, "Practical application matters more than theory"),

        _r("TCS", "tcs_digital", 3, "behavioral", "Managerial Round",
           ["leadership", "conflict_resolution", "project_ownership", "learning_mindset"],
           "medium", 5, "Delivery Manager",
           "warm_but_probing", "Probe for real examples, not generic answers.",
           _BEHAVIORAL_DIMS),

        _r("TCS", "tcs_digital", 4, "hr", "HR Interview",
           ["salary_expectations", "relocation", "career_vision", "company_fit"],
           "easy", 4, "HR Manager",
           "friendly", "Standard HR. Slightly higher salary discussion.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # TCS Prime — 5 rounds (top tier)
        # ════════════════════════════════════════
        _r("TCS", "tcs_prime", 1, "technical", "Technical Round 1 — Core CS",
           ["data_structures", "algorithms", "complexity_analysis", "oops", "dbms"],
           "hard", 7, "Principal Engineer",
           "skeptical", "Expect strong fundamentals. Probe depth on algorithms and DS internals.",
           _TECH_DIMS, "Eliminatory — weak DS/Algo is a reject", 1),

        _r("TCS", "tcs_prime", 2, "technical", "Technical Round 2 — Coding Deep Dive",
           ["coding", "problem_solving", "optimization", "debugging"],
           "hard", 6, "Senior Architect",
           "intense", "Live coding or pseudo-code. Focus on optimization and edge cases.",
           _TECH_DIMS, "Ask to optimize naive solutions", 1),

        _r("TCS", "tcs_prime", 3, "system_design", "System Design Basics",
           ["api_design", "database_choice", "caching_basics", "monolith_vs_microservices"],
           "medium", 5, "Tech Lead",
           "warm_but_probing", "Basic system design — not FAANG level but must show awareness.",
           _DESIGN_DIMS, "Fresher level — expect awareness not mastery"),

        _r("TCS", "tcs_prime", 4, "behavioral", "Managerial Round",
           ["leadership", "ownership", "innovation", "conflict_resolution"],
           "medium", 5, "Senior Manager",
           "warm_but_probing", "Look for leadership potential and innovation mindset.",
           _BEHAVIORAL_DIMS),

        _r("TCS", "tcs_prime", 5, "hr", "HR Interview",
           ["salary_expectations", "career_trajectory", "company_alignment"],
           "easy", 4, "Senior HR",
           "friendly", "Higher package discussion. Assess long-term commitment.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Infosys Systems Engineer — 3 rounds
        # ════════════════════════════════════════
        _r("Infosys", "infosys_se", 1, "technical", "Technical Interview",
           ["basic_programming", "oops", "dbms_basics", "data_structures_basics"],
           "easy", 6, "Technical Interviewer",
           "friendly", "Very basic. Definition-level questions. Check foundational understanding.",
           _TECH_DIMS, "Low bar — looking for trainability", 1),

        _r("Infosys", "infosys_se", 2, "behavioral", "HR Round 1",
           ["introduction", "academics", "strengths_weaknesses", "team_experience"],
           "easy", 5, "HR Executive",
           "friendly", "Conversational. Assess communication and personality.",
           _BEHAVIORAL_DIMS),

        _r("Infosys", "infosys_se", 3, "hr", "HR Round 2",
           ["salary_expectations", "relocation", "bond_acceptance", "joining_date"],
           "easy", 4, "HR Manager",
           "friendly", "Formality round. Confirm logistics and expectations.",
           _HR_DIMS, "1-year bond"),

        # ════════════════════════════════════════
        # Infosys Specialist Programmer — 4 rounds
        # ════════════════════════════════════════
        _r("Infosys", "infosys_sp", 1, "technical", "Technical Round 1",
           ["data_structures", "algorithms", "oops", "dbms", "coding_basics"],
           "medium", 7, "Senior Developer",
           "neutral", "Solid fundamentals expected. Not just definitions — expect 'why' questions.",
           _TECH_DIMS, "", 1),

        _r("Infosys", "infosys_sp", 2, "technical", "Technical Round 2 — Coding",
           ["coding", "problem_solving", "logical_thinking"],
           "medium", 5, "Tech Lead",
           "warm_but_probing", "Practical coding questions. Pseudo-code or logic building.",
           _TECH_DIMS),

        _r("Infosys", "infosys_sp", 3, "behavioral", "Managerial Round",
           ["project_experience", "teamwork", "leadership_potential", "learning_agility"],
           "easy", 5, "Project Manager",
           "warm_but_probing", "Focus on project contributions and team dynamics.",
           _BEHAVIORAL_DIMS),

        _r("Infosys", "infosys_sp", 4, "hr", "HR Interview",
           ["salary_discussion", "relocation", "career_goals"],
           "easy", 4, "HR Manager",
           "friendly", "Standard HR. Higher package awareness.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Infosys Power Programmer — 4 rounds
        # ════════════════════════════════════════
        _r("Infosys", "infosys_pp", 1, "technical", "Technical Round 1 — Core",
           ["data_structures", "algorithms", "complexity", "system_concepts"],
           "hard", 7, "Principal Engineer",
           "skeptical", "Strong DS/Algo. Must handle medium-hard problems.",
           _TECH_DIMS, "Eliminatory", 1),

        _r("Infosys", "infosys_pp", 2, "technical", "Technical Round 2 — Coding & Design",
           ["coding", "optimization", "api_design", "database_design"],
           "hard", 6, "Architect",
           "intense", "Code walkthrough. Design a small system. Discuss trade-offs.",
           _TECH_DIMS + _DESIGN_DIMS),

        _r("Infosys", "infosys_pp", 3, "behavioral", "Managerial Round",
           ["innovation", "problem_ownership", "leadership", "technical_vision"],
           "medium", 5, "Senior Manager",
           "warm_but_probing", "Look for thought leadership and initiative.",
           _BEHAVIORAL_DIMS),

        _r("Infosys", "infosys_pp", 4, "hr", "HR Interview",
           ["career_trajectory", "salary_expectations", "company_alignment"],
           "easy", 4, "Senior HR",
           "friendly", "Power Programmer package discussion.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Wipro Elite — 3 rounds
        # ════════════════════════════════════════
        _r("Wipro", "wipro_elite", 1, "technical", "Technical Interview",
           ["basic_programming", "oops", "dbms_basics", "networking_basics"],
           "easy", 6, "Technical Interviewer",
           "friendly", "Basic fundamentals. Similar to TCS Ninja level.",
           _TECH_DIMS, "", 1),

        _r("Wipro", "wipro_elite", 2, "behavioral", "Managerial Round",
           ["teamwork", "communication", "adaptability", "learning_ability"],
           "easy", 5, "Manager",
           "warm_but_probing", "Soft skills assessment. Focus on communication.",
           _BEHAVIORAL_DIMS),

        _r("Wipro", "wipro_elite", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "bond_acceptance"],
           "easy", 4, "HR Manager",
           "friendly", "Standard HR. 1-year bond discussion.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Wipro Turbo — 4 rounds
        # ════════════════════════════════════════
        _r("Wipro", "wipro_turbo", 1, "technical", "Technical Round 1",
           ["data_structures", "algorithms", "oops", "dbms"],
           "medium", 7, "Senior Developer",
           "neutral", "Solid fundamentals. Expect problem-solving questions.",
           _TECH_DIMS, "", 1),

        _r("Wipro", "wipro_turbo", 2, "technical", "Technical Round 2 — Applied",
           ["coding", "problem_solving", "web_basics", "api_concepts"],
           "medium", 6, "Tech Lead",
           "warm_but_probing", "Practical coding and applied concepts.",
           _TECH_DIMS),

        _r("Wipro", "wipro_turbo", 3, "behavioral", "Managerial Round",
           ["leadership", "project_ownership", "conflict_resolution"],
           "medium", 5, "Delivery Manager",
           "warm_but_probing", "Look for ownership and initiative.",
           _BEHAVIORAL_DIMS),

        _r("Wipro", "wipro_turbo", 4, "hr", "HR Interview",
           ["salary_expectations", "career_goals", "relocation"],
           "easy", 4, "HR Manager",
           "friendly", "Higher package discussion.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Cognizant GenC — 3 rounds
        # ════════════════════════════════════════
        _r("Cognizant", "cognizant_genc", 1, "technical", "Technical Interview",
           ["basic_programming", "oops_basics", "dbms_basics", "data_structures_basics"],
           "easy", 6, "Technical Interviewer",
           "friendly", "Entry-level fundamentals. Focus on conceptual clarity.",
           _TECH_DIMS, "", 1),

        _r("Cognizant", "cognizant_genc", 2, "behavioral", "Communication & Behavioral",
           ["communication", "teamwork", "career_motivation", "academics"],
           "easy", 5, "Manager",
           "friendly", "Communication-heavy. Assess articulation and confidence.",
           _BEHAVIORAL_DIMS),

        _r("Cognizant", "cognizant_genc", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "company_knowledge"],
           "easy", 4, "HR Executive",
           "friendly", "Quick HR round. Confirm logistics.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Cognizant GenC Next — 4 rounds
        # ════════════════════════════════════════
        _r("Cognizant", "cognizant_genc_next", 1, "technical", "Technical Round 1",
           ["data_structures", "algorithms", "oops", "dbms", "os_basics"],
           "medium", 7, "Senior Developer",
           "neutral", "Expect depth beyond basics. 'Why' and 'how' questions.",
           _TECH_DIMS, "", 1),

        _r("Cognizant", "cognizant_genc_next", 2, "technical", "Technical Round 2 — Coding",
           ["coding", "problem_solving", "logical_thinking"],
           "medium", 5, "Tech Lead",
           "warm_but_probing", "Code writing or logic-building questions.",
           _TECH_DIMS),

        _r("Cognizant", "cognizant_genc_next", 3, "behavioral", "Managerial Round",
           ["project_experience", "teamwork", "learning_agility", "career_vision"],
           "easy", 5, "Project Manager",
           "warm_but_probing", "Assess growth potential and team skills.",
           _BEHAVIORAL_DIMS),

        _r("Cognizant", "cognizant_genc_next", 4, "hr", "HR Interview",
           ["salary_discussion", "relocation", "career_goals"],
           "easy", 4, "HR Manager",
           "friendly", "Standard HR.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Cognizant GenC Elevate — 5 rounds
        # ════════════════════════════════════════
        _r("Cognizant", "cognizant_genc_elevate", 1, "technical", "Technical Round 1 — Core CS",
           ["data_structures", "algorithms", "complexity", "oops_advanced"],
           "hard", 7, "Principal Developer",
           "skeptical", "High bar. Must demonstrate strong CS fundamentals.",
           _TECH_DIMS, "Eliminatory", 1),

        _r("Cognizant", "cognizant_genc_elevate", 2, "technical", "Technical Round 2 — Coding",
           ["coding", "optimization", "debugging", "problem_solving"],
           "hard", 6, "Senior Architect",
           "intense", "Hands-on coding. Expect optimization and edge case discussion.",
           _TECH_DIMS, "", 1),

        _r("Cognizant", "cognizant_genc_elevate", 3, "system_design", "Design Discussion",
           ["api_design", "database_choice", "architecture_basics"],
           "medium", 5, "Tech Lead",
           "warm_but_probing", "Basic design — awareness level for freshers.",
           _DESIGN_DIMS, "Don't expect FAANG-level design from freshers"),

        _r("Cognizant", "cognizant_genc_elevate", 4, "behavioral", "Managerial Round",
           ["leadership", "innovation", "ownership", "technical_communication"],
           "medium", 5, "Senior Manager",
           "warm_but_probing", "Look for initiative and leadership potential.",
           _BEHAVIORAL_DIMS),

        _r("Cognizant", "cognizant_genc_elevate", 5, "hr", "HR Interview",
           ["salary_expectations", "career_trajectory", "company_alignment"],
           "easy", 4, "Senior HR",
           "friendly", "Elevate package discussion.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Accenture ASE — 3 rounds
        # ════════════════════════════════════════
        _r("Accenture", "accenture_ase", 1, "technical", "Technical + Communication",
           ["basic_programming", "oops", "dbms_basics", "communication"],
           "easy", 6, "Technical Interviewer",
           "friendly", "Mixed technical and communication. Articulation matters.",
           _TECH_DIMS + ["communication"], "", 1),

        _r("Accenture", "accenture_ase", 2, "behavioral", "Behavioral Round",
           ["teamwork", "adaptability", "problem_solving_approach", "career_goals"],
           "easy", 5, "Manager",
           "warm_but_probing", "Focus on behavioral and cultural fit.",
           _BEHAVIORAL_DIMS),

        _r("Accenture", "accenture_ase", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "bond_acceptance", "joining_timeline"],
           "easy", 4, "HR Manager",
           "friendly", "2-year bond discussion.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Accenture ACE — 4 rounds
        # ════════════════════════════════════════
        _r("Accenture", "accenture_ace", 1, "technical", "Technical Round 1",
           ["data_structures", "algorithms", "oops", "dbms", "web_basics"],
           "medium", 7, "Senior Developer",
           "neutral", "Deeper technical. Must show understanding beyond surface.",
           _TECH_DIMS, "", 1),

        _r("Accenture", "accenture_ace", 2, "technical", "Technical Round 2 — Coding",
           ["coding", "problem_solving", "optimization"],
           "medium", 6, "Tech Lead",
           "warm_but_probing", "Practical coding and logic-building.",
           _TECH_DIMS),

        _r("Accenture", "accenture_ace", 3, "behavioral", "Managerial Round",
           ["leadership", "project_experience", "conflict_resolution", "innovation"],
           "medium", 5, "Delivery Manager",
           "warm_but_probing", "Assess for ACE-level potential.",
           _BEHAVIORAL_DIMS),

        _r("Accenture", "accenture_ace", 4, "hr", "HR Interview",
           ["salary_expectations", "career_vision", "bond_acceptance"],
           "easy", 4, "Senior HR",
           "friendly", "ACE package. 2-year bond.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # HCL Technologies — 3 rounds
        # ════════════════════════════════════════
        _r("HCL Technologies", "hcl_fresher", 1, "technical", "Technical Interview",
           ["basic_programming", "oops", "dbms_basics", "data_structures_basics"],
           "easy", 6, "Technical Interviewer",
           "friendly", "Standard fresher-level technical.",
           _TECH_DIMS, "", 1),

        _r("HCL Technologies", "hcl_fresher", 2, "behavioral", "Managerial Round",
           ["communication", "teamwork", "career_goals", "academics"],
           "easy", 5, "Manager",
           "warm_but_probing", "Soft skills and communication assessment.",
           _BEHAVIORAL_DIMS),

        _r("HCL Technologies", "hcl_fresher", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "bond_acceptance"],
           "easy", 4, "HR Manager",
           "friendly", "1-year bond. Standard HR.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Tech Mahindra — 3 rounds (includes GD)
        # ════════════════════════════════════════
        _r("Tech Mahindra", "techm_fresher", 1, "stress", "Group Discussion",
           ["current_affairs", "technology_trends", "social_issues", "articulation"],
           "easy", 5, "GD Moderator",
           "neutral", "GD round. Assess participation, logic, and communication.",
           _STRESS_DIMS + ["communication"], "GD is common in Tech Mahindra hiring", 1),

        _r("Tech Mahindra", "techm_fresher", 2, "technical", "Technical Interview",
           ["basic_programming", "oops", "dbms_basics", "networking_basics"],
           "easy", 6, "Technical Interviewer",
           "friendly", "Basic technical. Focus on clarity.",
           _TECH_DIMS),

        _r("Tech Mahindra", "techm_fresher", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "bond_acceptance", "career_goals"],
           "easy", 4, "HR Manager",
           "friendly", "1-year bond. Standard.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Capgemini Analyst — 3 rounds
        # ════════════════════════════════════════
        _r("Capgemini", "capgemini_analyst", 1, "technical", "Technical + Pseudo Code",
           ["pseudo_code", "basic_programming", "logical_thinking"],
           "easy", 6, "Technical Interviewer",
           "friendly", "Game-based + pseudo code. Unique format.",
           _TECH_DIMS, "Capgemini uses Plum assessment (game-based)", 1),

        _r("Capgemini", "capgemini_analyst", 2, "behavioral", "Communication Round",
           ["communication", "presentation", "teamwork", "adaptability"],
           "easy", 5, "Manager",
           "friendly", "Communication-heavy assessment.",
           _BEHAVIORAL_DIMS + ["communication"]),

        _r("Capgemini", "capgemini_analyst", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "company_knowledge"],
           "easy", 4, "HR Executive",
           "friendly", "Quick HR confirmation.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Capgemini Exceller — 4 rounds
        # ════════════════════════════════════════
        _r("Capgemini", "capgemini_exceller", 1, "technical", "Technical Round 1 — Pseudo Code & Logic",
           ["pseudo_code", "data_structures", "algorithms_basics", "logical_thinking"],
           "medium", 7, "Senior Developer",
           "neutral", "Deeper pseudo code and logic. Must show problem decomposition.",
           _TECH_DIMS, "", 1),

        _r("Capgemini", "capgemini_exceller", 2, "technical", "Technical Round 2 — Applied",
           ["coding", "problem_solving", "oops", "dbms"],
           "medium", 6, "Tech Lead",
           "warm_but_probing", "Applied technical. Coding + conceptual depth.",
           _TECH_DIMS),

        _r("Capgemini", "capgemini_exceller", 3, "behavioral", "Managerial Round",
           ["leadership", "project_experience", "communication", "career_vision"],
           "medium", 5, "Delivery Manager",
           "warm_but_probing", "Assess for Exceller-level potential.",
           _BEHAVIORAL_DIMS),

        _r("Capgemini", "capgemini_exceller", 4, "hr", "HR Interview",
           ["salary_expectations", "career_goals", "relocation"],
           "easy", 4, "HR Manager",
           "friendly", "Exceller package discussion.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # LTIMindtree — 3 rounds
        # ════════════════════════════════════════
        _r("LTIMindtree", "ltimindtree_fresher", 1, "technical", "Technical Interview",
           ["data_structures", "algorithms_basics", "oops", "dbms", "coding_basics"],
           "medium", 7, "Senior Developer",
           "neutral", "Medium difficulty. Expect coding questions.",
           _TECH_DIMS, "", 1),

        _r("LTIMindtree", "ltimindtree_fresher", 2, "behavioral", "Managerial Round",
           ["project_experience", "teamwork", "problem_solving_approach"],
           "easy", 5, "Project Manager",
           "warm_but_probing", "Project-focused behavioral.",
           _BEHAVIORAL_DIMS),

        _r("LTIMindtree", "ltimindtree_fresher", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "career_goals"],
           "easy", 4, "HR Manager",
           "friendly", "Standard HR. 1-year bond.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Zoho Fresher — 4 rounds (unique: C programming focus)
        # ════════════════════════════════════════
        _r("Zoho", "zoho_fresher", 1, "technical", "Programming Round 1 — C Basics",
           ["c_programming", "pointers", "arrays", "strings", "memory_management"],
           "hard", 5, "Senior Developer",
           "neutral", "Zoho is C-focused. Pure programming. No aptitude test.",
           _TECH_DIMS, "Unique: Zoho doesn't care about CGPA, only coding ability", 1),

        _r("Zoho", "zoho_fresher", 2, "technical", "Programming Round 2 — Advanced",
           ["data_structures", "algorithms", "dynamic_programming", "problem_solving"],
           "hard", 5, "Principal Engineer",
           "skeptical", "Advanced coding. Multiple problems with increasing difficulty.",
           _TECH_DIMS, "Expect 3-5 coding problems in a single sitting", 1),

        _r("Zoho", "zoho_fresher", 3, "system_design", "Design Discussion",
           ["oop_design", "class_design", "database_modeling", "real_world_modeling"],
           "medium", 5, "Architect",
           "warm_but_probing", "OOP design — model a real-world system. Not distributed systems.",
           _DESIGN_DIMS, "Zoho favors OOP design over distributed systems for freshers"),

        _r("Zoho", "zoho_fresher", 4, "hr", "HR + Cultural Fit",
           ["motivation", "problem_solving_passion", "learning_ability", "cultural_fit"],
           "easy", 5, "HR Manager",
           "warm_but_probing", "Zoho values passion for coding. Assess intrinsic motivation.",
           _HR_DIMS + ["motivation"]),

        # ════════════════════════════════════════
        # Zoho Lateral — 4 rounds
        # ════════════════════════════════════════
        _r("Zoho", "zoho_lateral", 1, "technical", "Technical Round — Deep",
           ["data_structures", "algorithms", "system_internals", "optimization"],
           "hard", 6, "Principal Engineer",
           "intense", "Deep technical. Expect hard coding problems.",
           _TECH_DIMS, "", 1),

        _r("Zoho", "zoho_lateral", 2, "system_design", "System Design",
           ["distributed_systems", "database_design", "scalability", "caching", "message_queues"],
           "hard", 6, "Chief Architect",
           "skeptical", "Full system design. Scale, reliability, data modeling.",
           _DESIGN_DIMS, "", 1),

        _r("Zoho", "zoho_lateral", 3, "behavioral", "Managerial Round",
           ["leadership", "team_management", "project_ownership", "conflict_resolution"],
           "medium", 5, "Engineering Manager",
           "warm_but_probing", "Assess leadership and ownership mindset.",
           _BEHAVIORAL_DIMS),

        _r("Zoho", "zoho_lateral", 4, "hr", "HR Interview",
           ["salary_negotiation", "career_goals", "cultural_fit"],
           "easy", 4, "HR Manager",
           "friendly", "Zoho values retention. Discuss growth path.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Persistent Systems — 3 rounds
        # ════════════════════════════════════════
        _r("Persistent Systems", "persistent_fresher", 1, "technical", "Technical Interview",
           ["data_structures", "oops", "dbms", "coding_basics", "web_basics"],
           "medium", 7, "Senior Developer",
           "neutral", "Medium-level technical. Good balance of theory and coding.",
           _TECH_DIMS, "", 1),

        _r("Persistent Systems", "persistent_fresher", 2, "behavioral", "Managerial Round",
           ["project_experience", "teamwork", "learning_agility"],
           "easy", 5, "Project Manager",
           "warm_but_probing", "Project-focused discussion.",
           _BEHAVIORAL_DIMS),

        _r("Persistent Systems", "persistent_fresher", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "career_goals"],
           "easy", 4, "HR Manager",
           "friendly", "Standard HR.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Mphasis — 3 rounds
        # ════════════════════════════════════════
        _r("Mphasis", "mphasis_fresher", 1, "technical", "Technical Interview",
           ["basic_programming", "oops_basics", "dbms_basics", "data_structures_basics"],
           "easy", 6, "Technical Interviewer",
           "friendly", "Basic technical assessment. Focus on fundamentals.",
           _TECH_DIMS, "", 1),

        _r("Mphasis", "mphasis_fresher", 2, "behavioral", "Behavioral Round",
           ["communication", "teamwork", "career_goals", "academics"],
           "easy", 5, "Manager",
           "friendly", "Communication and soft skills assessment.",
           _BEHAVIORAL_DIMS),

        _r("Mphasis", "mphasis_fresher", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "company_knowledge"],
           "easy", 4, "HR Executive",
           "friendly", "Quick HR round.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Google L3 — 5 rounds
        # ════════════════════════════════════════
        _r("Google", "google_l3", 1, "technical", "Coding Interview 1",
           ["algorithms", "data_structures", "complexity_analysis", "coding"],
           "hard", 5, "Software Engineer",
           "neutral", "LC medium-hard. Clean code + optimal solutions. Think out loud.",
           _TECH_DIMS, "45 min. 1-2 problems. Must code on whiteboard/editor.", 1),

        _r("Google", "google_l3", 2, "technical", "Coding Interview 2",
           ["algorithms", "data_structures", "dynamic_programming", "graph_algorithms"],
           "hard", 5, "Senior Software Engineer",
           "skeptical", "Harder problems. Edge cases matter. Discuss time/space trade-offs.",
           _TECH_DIMS, "Different topic area from Interview 1", 1),

        _r("Google", "google_l3", 3, "technical", "Coding Interview 3",
           ["algorithms", "system_thinking", "problem_decomposition"],
           "hard", 5, "Staff Engineer",
           "intense", "Hardest coding round. May include design elements.",
           _TECH_DIMS + _DESIGN_DIMS, "Often the 'bar raiser' for coding"),

        _r("Google", "google_l3", 4, "behavioral", "Googleyness & Leadership",
           ["googleyness", "leadership", "teamwork", "ambiguity_handling", "initiative"],
           "medium", 5, "Engineering Manager",
           "warm_but_probing", "STAR format. Focus on 'Googleyness' — humility, collaboration, bias for action.",
           _BEHAVIORAL_DIMS + ["initiative", "adaptability"],
           "Googleyness is a real evaluation dimension at Google"),

        _r("Google", "google_l3", 5, "final", "Hiring Committee Review",
           ["overall_assessment", "calibration", "level_fit"],
           "hard", 4, "Hiring Committee",
           "neutral", "Not a live round — but the candidate may be asked calibration questions.",
           ["overall_fit", "technical_ability", "leadership_potential"],
           "HC reviews all feedback. Candidate doesn't directly interact."),

        # ════════════════════════════════════════
        # Google L4 — 6 rounds
        # ════════════════════════════════════════
        _r("Google", "google_l4", 1, "technical", "Coding Interview 1",
           ["algorithms", "data_structures", "coding", "optimization"],
           "hard", 5, "Senior Software Engineer",
           "neutral", "LC medium-hard. Expected to produce clean, production-quality code.",
           _TECH_DIMS, "", 1),

        _r("Google", "google_l4", 2, "technical", "Coding Interview 2",
           ["algorithms", "data_structures", "complex_problem_solving"],
           "hard", 5, "Staff Engineer",
           "skeptical", "Harder problems. Must demonstrate depth and speed.",
           _TECH_DIMS, "", 1),

        _r("Google", "google_l4", 3, "system_design", "System Design Interview",
           ["distributed_systems", "scalability", "reliability", "data_modeling", "caching"],
           "hard", 6, "Principal Engineer",
           "warm_but_probing", "Design a large-scale system. Drive the conversation proactively.",
           _DESIGN_DIMS, "Must demonstrate ownership of the design. Drive, don't follow.", 1),

        _r("Google", "google_l4", 4, "system_design", "System Design Interview 2",
           ["api_design", "microservices", "consistency_models", "failure_handling"],
           "hard", 6, "Distinguished Engineer",
           "skeptical", "Second design round. Different problem domain. Expect trade-off challenges.",
           _DESIGN_DIMS, "Often covers a different domain than first design round"),

        _r("Google", "google_l4", 5, "behavioral", "Googleyness & Leadership",
           ["googleyness", "leadership", "mentoring", "cross_team_collaboration", "ambiguity"],
           "medium", 5, "Engineering Manager",
           "warm_but_probing", "L4 bar: must show influence beyond their team.",
           _BEHAVIORAL_DIMS + ["influence", "mentoring"]),

        _r("Google", "google_l4", 6, "final", "Hiring Committee Review",
           ["overall_assessment", "level_calibration", "project_complexity"],
           "hard", 4, "Hiring Committee",
           "neutral", "HC review. May loop back for additional rounds.",
           ["overall_fit", "technical_ability", "leadership"]),

        # ════════════════════════════════════════
        # Amazon SDE-1 — 5 rounds
        # ════════════════════════════════════════
        _r("Amazon", "amazon_sde1", 1, "technical", "Online Assessment (OA)",
           ["algorithms", "data_structures", "coding", "logical_reasoning"],
           "medium", 5, "Automated Assessment",
           "neutral", "2 coding problems + work simulation. 90 minutes.",
           _TECH_DIMS, "OA includes Leadership Principles work simulation", 1),

        _r("Amazon", "amazon_sde1", 2, "technical", "Coding Round 1",
           ["algorithms", "data_structures", "coding", "problem_solving"],
           "hard", 5, "SDE-2",
           "neutral", "1-2 coding problems. Must explain approach clearly. Think out loud.",
           _TECH_DIMS, "LP: Dive Deep, Deliver Results", 1),

        _r("Amazon", "amazon_sde1", 3, "technical", "Coding Round 2",
           ["algorithms", "data_structures", "optimization", "edge_cases"],
           "hard", 5, "Senior SDE",
           "skeptical", "Harder problems. Edge case handling is critical.",
           _TECH_DIMS, "LP: Insist on Highest Standards"),

        _r("Amazon", "amazon_sde1", 4, "behavioral", "Leadership Principles (LP) Round",
           ["ownership", "customer_obsession", "bias_for_action", "earn_trust", "deliver_results"],
           "medium", 6, "Bar Raiser / Manager",
           "warm_but_probing", "Deep LP-based behavioral. STAR format expected. Multiple stories needed.",
           _BEHAVIORAL_DIMS + ["ownership", "customer_focus"],
           "Bar Raiser has veto power. Prepare 6-8 LP stories.", 1),

        _r("Amazon", "amazon_sde1", 5, "hr", "Hiring Manager Round",
           ["team_fit", "career_goals", "salary_expectations", "growth_vision"],
           "easy", 4, "Hiring Manager",
           "warm_but_probing", "Mix of technical and behavioral. Manager gauges team fit.",
           _HR_DIMS + _BEHAVIORAL_DIMS),

        # ════════════════════════════════════════
        # Amazon SDE-2 — 6 rounds
        # ════════════════════════════════════════
        _r("Amazon", "amazon_sde2", 1, "technical", "Coding Round 1",
           ["algorithms", "data_structures", "coding", "optimization"],
           "hard", 5, "Senior SDE",
           "neutral", "LC medium-hard. Production-quality code expected.",
           _TECH_DIMS, "", 1),

        _r("Amazon", "amazon_sde2", 2, "technical", "Coding Round 2",
           ["algorithms", "complex_data_structures", "dynamic_programming"],
           "hard", 5, "Principal SDE",
           "skeptical", "Harder problems. Must discuss multiple approaches.",
           _TECH_DIMS, "", 1),

        _r("Amazon", "amazon_sde2", 3, "system_design", "System Design",
           ["distributed_systems", "scalability", "availability", "data_modeling", "api_design"],
           "hard", 6, "Principal SDE",
           "warm_but_probing", "Design a large-scale system. Must drive the design proactively.",
           _DESIGN_DIMS, "LP: Think Big, Invent and Simplify", 1),

        _r("Amazon", "amazon_sde2", 4, "behavioral", "LP Round 1",
           ["ownership", "customer_obsession", "bias_for_action", "disagree_and_commit"],
           "medium", 5, "Senior Manager",
           "warm_but_probing", "Deep LP stories. Need concrete examples with metrics.",
           _BEHAVIORAL_DIMS + ["ownership", "customer_focus"]),

        _r("Amazon", "amazon_sde2", 5, "stress", "Bar Raiser Round",
           ["leadership_principles", "cross_functional_influence", "handling_ambiguity"],
           "hard", 5, "Bar Raiser",
           "skeptical", "Bar Raiser has veto. Mix of LP + technical. Tests conviction under pressure.",
           _STRESS_DIMS + _BEHAVIORAL_DIMS,
           "Bar Raiser is an independent assessor from a different team", 1),

        _r("Amazon", "amazon_sde2", 6, "hr", "Hiring Manager Round",
           ["team_fit", "career_goals", "salary_negotiation", "growth_trajectory"],
           "easy", 4, "Hiring Manager",
           "warm_but_probing", "Final round. Team fit + expectations alignment.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Microsoft SDE 59 (New Grad) — 4 rounds
        # ════════════════════════════════════════
        _r("Microsoft", "microsoft_sde59", 1, "technical", "Coding Round 1",
           ["algorithms", "data_structures", "coding", "problem_solving"],
           "medium", 5, "Software Engineer",
           "neutral", "LC easy-medium. Focus on clean code and clear communication.",
           _TECH_DIMS, "Microsoft values thought process over perfect code", 1),

        _r("Microsoft", "microsoft_sde59", 2, "technical", "Coding Round 2",
           ["algorithms", "data_structures", "system_thinking", "debugging"],
           "hard", 5, "Senior Software Engineer",
           "warm_but_probing", "Harder problems. Must discuss trade-offs and alternative approaches.",
           _TECH_DIMS, "", 1),

        _r("Microsoft", "microsoft_sde59", 3, "behavioral", "Behavioral + Cultural Fit",
           ["growth_mindset", "collaboration", "diversity_inclusion", "innovation"],
           "medium", 5, "Engineering Manager",
           "warm_but_probing", "Microsoft values 'growth mindset'. STAR format. Failure stories welcome.",
           _BEHAVIORAL_DIMS + ["growth_mindset", "innovation"],
           "Growth mindset is a core Microsoft value"),

        _r("Microsoft", "microsoft_sde59", 4, "final", "As-Appropriate (AA) Round",
           ["overall_assessment", "level_calibration", "hire_no_hire"],
           "hard", 5, "Partner / Director",
           "skeptical", "Final decision-maker. Mix of technical + behavioral. Senior executive.",
           _TECH_DIMS + _BEHAVIORAL_DIMS,
           "AA interviewer has hire/no-hire authority", 1),

        # ════════════════════════════════════════
        # Microsoft SDE 60 — 5 rounds
        # ════════════════════════════════════════
        _r("Microsoft", "microsoft_sde60", 1, "technical", "Coding Round 1",
           ["algorithms", "data_structures", "coding", "optimization"],
           "hard", 5, "Senior Software Engineer",
           "neutral", "LC medium-hard. Clean, efficient code expected.",
           _TECH_DIMS, "", 1),

        _r("Microsoft", "microsoft_sde60", 2, "system_design", "System Design",
           ["distributed_systems", "scalability", "api_design", "cloud_services"],
           "hard", 6, "Principal Engineer",
           "warm_but_probing", "Full system design. Azure/cloud awareness is a plus.",
           _DESIGN_DIMS, "Azure-relevant design preferred but not required", 1),

        _r("Microsoft", "microsoft_sde60", 3, "technical", "Coding Round 2",
           ["algorithms", "complex_data_structures", "problem_decomposition"],
           "hard", 5, "Staff Engineer",
           "skeptical", "Hardest coding round. Multiple approaches expected.",
           _TECH_DIMS),

        _r("Microsoft", "microsoft_sde60", 4, "behavioral", "Behavioral + Leadership",
           ["growth_mindset", "mentoring", "cross_team_impact", "innovation"],
           "medium", 5, "Engineering Manager",
           "warm_but_probing", "Must show impact beyond individual contributions.",
           _BEHAVIORAL_DIMS + ["growth_mindset", "mentoring"]),

        _r("Microsoft", "microsoft_sde60", 5, "final", "As-Appropriate (AA) Round",
           ["overall_assessment", "level_calibration", "organizational_impact"],
           "hard", 5, "Partner / CVP",
           "skeptical", "Final decision. Senior executive assessment.",
           _TECH_DIMS + _BEHAVIORAL_DIMS, "CVP-level for SDE 60", 1),

        # ════════════════════════════════════════
        # Flipkart SDE-1 — 4 rounds
        # ════════════════════════════════════════
        _r("Flipkart", "flipkart_sde1", 1, "technical", "Machine Coding Round",
           ["coding", "oop_design", "clean_code", "working_solution"],
           "hard", 4, "SDE-2",
           "neutral", "90-min machine coding. Build a working solution with clean OOP design.",
           _TECH_DIMS + ["code_quality"],
           "Flipkart is famous for machine coding rounds", 1),

        _r("Flipkart", "flipkart_sde1", 2, "technical", "DSA Round",
           ["algorithms", "data_structures", "problem_solving", "optimization"],
           "hard", 5, "Senior SDE",
           "skeptical", "LC medium-hard. Must handle follow-ups and optimize.",
           _TECH_DIMS, "", 1),

        _r("Flipkart", "flipkart_sde1", 3, "behavioral", "Hiring Manager Round",
           ["ownership", "teamwork", "problem_solving_approach", "cultural_fit"],
           "medium", 5, "Engineering Manager",
           "warm_but_probing", "Mix of behavioral + light technical. Manager gauges fit.",
           _BEHAVIORAL_DIMS + ["ownership"]),

        _r("Flipkart", "flipkart_sde1", 4, "hr", "HR Round",
           ["salary_expectations", "team_preferences", "career_goals"],
           "easy", 4, "HR Manager",
           "friendly", "Standard HR. Salary band discussion.",
           _HR_DIMS),

        # ════════════════════════════════════════
        # Flipkart SDE-2 — 5 rounds
        # ════════════════════════════════════════
        _r("Flipkart", "flipkart_sde2", 1, "technical", "Machine Coding Round",
           ["coding", "oop_design", "design_patterns", "extensibility"],
           "hard", 4, "Senior SDE",
           "neutral", "90-min machine coding. Production-quality with design patterns.",
           _TECH_DIMS + ["code_quality"], "", 1),

        _r("Flipkart", "flipkart_sde2", 2, "technical", "DSA Round",
           ["algorithms", "data_structures", "optimization", "complexity"],
           "hard", 5, "Principal SDE",
           "skeptical", "Hard DSA. Must optimize and handle all edge cases.",
           _TECH_DIMS, "", 1),

        _r("Flipkart", "flipkart_sde2", 3, "system_design", "System Design (LLD + HLD)",
           ["low_level_design", "high_level_design", "distributed_systems", "data_modeling"],
           "hard", 6, "Principal SDE",
           "warm_but_probing", "Both LLD and HLD. Must drive the design conversation.",
           _DESIGN_DIMS, "Flipkart expects both LLD and HLD for SDE-2", 1),

        _r("Flipkart", "flipkart_sde2", 4, "behavioral", "Hiring Manager Round",
           ["leadership", "ownership", "cross_team_influence", "mentoring"],
           "medium", 5, "Engineering Manager",
           "warm_but_probing", "Must show leadership and influence beyond own team.",
           _BEHAVIORAL_DIMS + ["leadership", "mentoring"]),

        _r("Flipkart", "flipkart_sde2", 5, "hr", "HR Round",
           ["salary_negotiation", "career_trajectory", "team_fit"],
           "easy", 4, "Senior HR",
           "friendly", "Salary negotiation. Band discussion.",
           _HR_DIMS),
    ]


# ════════════════════════════════════════════════════════════════
# DEFAULT BLUEPRINTS — Fallback when company has no specific data
# 5 domains × 5 experience levels = 25 sets
# ════════════════════════════════════════════════════════════════

_DOMAINS = ["software_engineering", "data_science", "devops", "product_management", "qa_testing"]
_LEVELS = ["fresher", "1-3yr", "3-7yr", "7-12yr", "12+yr"]


def get_default_blueprints() -> List[Dict]:
    blueprints = []

    # ────────────────────────────────────
    # SOFTWARE ENGINEERING
    # ────────────────────────────────────
    # Fresher
    blueprints += [
        _d("software_engineering", "fresher", 1, "technical", "Technical Interview",
           ["data_structures", "algorithms", "oops", "dbms", "coding_basics"],
           "easy", 7, "Technical Interviewer", "friendly",
           "Focus on fundamentals. Be encouraging. Assess trainability.",
           _TECH_DIMS),
        _d("software_engineering", "fresher", 2, "behavioral", "Behavioral Round",
           ["communication", "teamwork", "career_goals", "learning_ability"],
           "easy", 5, "Manager", "warm_but_probing",
           "Assess communication and cultural fit. College project discussions.",
           _BEHAVIORAL_DIMS),
        _d("software_engineering", "fresher", 3, "hr", "HR Interview",
           ["salary_expectations", "relocation", "career_goals"],
           "easy", 4, "HR Manager", "friendly",
           "Standard HR. Confirm logistics and expectations.",
           _HR_DIMS),
    ]
    # 1-3yr
    blueprints += [
        _d("software_engineering", "1-3yr", 1, "technical", "Technical Round 1",
           ["data_structures", "algorithms", "system_concepts", "coding"],
           "medium", 7, "Senior Developer", "neutral",
           "Expect working knowledge. Ask about production experience.",
           _TECH_DIMS),
        _d("software_engineering", "1-3yr", 2, "technical", "Technical Round 2 — Applied",
           ["coding", "debugging", "api_design", "problem_solving"],
           "medium", 6, "Tech Lead", "warm_but_probing",
           "Practical coding. Real-world scenario questions.",
           _TECH_DIMS),
        _d("software_engineering", "1-3yr", 3, "behavioral", "Behavioral Round",
           ["teamwork", "conflict_resolution", "ownership", "learning_agility"],
           "easy", 5, "Engineering Manager", "warm_but_probing",
           "STAR format. Ask about real work situations.",
           _BEHAVIORAL_DIMS),
        _d("software_engineering", "1-3yr", 4, "hr", "HR Interview",
           ["salary_expectations", "notice_period", "career_goals"],
           "easy", 4, "HR Manager", "friendly",
           "Salary discussion. Notice period. Expectations alignment.",
           _HR_DIMS),
    ]
    # 3-7yr
    blueprints += [
        _d("software_engineering", "3-7yr", 1, "technical", "Technical Deep Dive",
           ["algorithms", "data_structures", "system_internals", "optimization"],
           "hard", 6, "Staff Engineer", "skeptical",
           "Deep technical. Expect mastery of fundamentals and production experience.",
           _TECH_DIMS),
        _d("software_engineering", "3-7yr", 2, "system_design", "System Design",
           ["distributed_systems", "scalability", "data_modeling", "api_design"],
           "hard", 6, "Principal Engineer", "warm_but_probing",
           "Full system design. Must drive the conversation.",
           _DESIGN_DIMS),
        _d("software_engineering", "3-7yr", 3, "behavioral", "Behavioral + Leadership",
           ["leadership", "mentoring", "cross_team_impact", "conflict_resolution"],
           "medium", 5, "Engineering Manager", "warm_but_probing",
           "Must show impact beyond individual contributions.",
           _BEHAVIORAL_DIMS + ["leadership"]),
        _d("software_engineering", "3-7yr", 4, "hr", "HR Interview",
           ["salary_negotiation", "career_trajectory", "team_preferences"],
           "easy", 4, "Senior HR", "friendly",
           "Experienced hire discussion. Band and growth path.",
           _HR_DIMS),
    ]
    # 7-12yr
    blueprints += [
        _d("software_engineering", "7-12yr", 1, "technical", "Technical Architecture",
           ["system_architecture", "performance", "security", "observability"],
           "hard", 6, "Distinguished Engineer", "skeptical",
           "Architecture-level discussion. Production war stories.",
           _TECH_DIMS + _DESIGN_DIMS),
        _d("software_engineering", "7-12yr", 2, "system_design", "System Design — Scale",
           ["distributed_systems", "reliability", "consistency_models", "data_pipelines"],
           "expert", 6, "VP Engineering", "intense",
           "Complex system design at scale. Must handle changing requirements.",
           _DESIGN_DIMS),
        _d("software_engineering", "7-12yr", 3, "behavioral", "Leadership & Vision",
           ["technical_vision", "org_building", "mentoring", "strategic_thinking"],
           "medium", 5, "VP/Director", "warm_but_probing",
           "Must show organizational impact and strategic thinking.",
           _BEHAVIORAL_DIMS + ["strategic_thinking", "mentoring"]),
        _d("software_engineering", "7-12yr", 4, "final", "Executive Round",
           ["overall_assessment", "culture_add", "vision_alignment"],
           "hard", 4, "CTO/VP", "skeptical",
           "Final executive assessment. Cultural and strategic fit.",
           ["overall_fit", "leadership", "strategic_thinking"]),
    ]
    # 12+yr
    blueprints += [
        _d("software_engineering", "12+yr", 1, "system_design", "Architecture & Vision",
           ["system_architecture", "org_design", "technology_strategy", "platform_thinking"],
           "expert", 6, "CTO", "intense",
           "Architecture at the organizational level. Platform strategy.",
           _DESIGN_DIMS + ["strategic_thinking"]),
        _d("software_engineering", "12+yr", 2, "behavioral", "Leadership Deep Dive",
           ["org_building", "talent_development", "executive_communication", "stakeholder_management"],
           "hard", 5, "CEO/VP", "warm_but_probing",
           "Executive-level leadership. Org building and strategy.",
           _BEHAVIORAL_DIMS + ["strategic_thinking", "executive_presence"]),
        _d("software_engineering", "12+yr", 3, "final", "Executive Panel",
           ["vision_alignment", "culture", "impact_potential"],
           "hard", 4, "Board/C-Suite", "skeptical",
           "Final executive assessment.",
           ["overall_fit", "leadership", "strategic_thinking", "culture_add"]),
    ]

    # ────────────────────────────────────
    # DATA SCIENCE
    # ────────────────────────────────────
    blueprints += [
        # Fresher
        _d("data_science", "fresher", 1, "technical", "Statistics & ML Fundamentals",
           ["statistics", "probability", "ml_basics", "python", "sql"],
           "easy", 7, "Data Scientist", "friendly",
           "Focus on stats and ML basics. Check Python and SQL proficiency.",
           ["statistics", "ml_knowledge", "coding_ability", "analytical_thinking"]),
        _d("data_science", "fresher", 2, "domain", "Data Analysis Case Study",
           ["data_analysis", "visualization", "business_metrics", "hypothesis_testing"],
           "easy", 5, "Senior Data Analyst", "warm_but_probing",
           "Give a small case study. Assess analytical thinking.",
           ["analytical_thinking", "business_sense", "communication"]),
        _d("data_science", "fresher", 3, "hr", "HR Interview",
           ["salary_expectations", "career_goals", "learning_ability"],
           "easy", 4, "HR Manager", "friendly", "", _HR_DIMS),
        # 1-3yr
        _d("data_science", "1-3yr", 1, "technical", "ML & Stats Deep Dive",
           ["machine_learning", "deep_learning_basics", "feature_engineering", "model_evaluation"],
           "medium", 7, "Senior Data Scientist", "neutral",
           "Expect hands-on ML experience. Ask about model deployment.",
           ["ml_knowledge", "coding_ability", "problem_solving", "statistics"]),
        _d("data_science", "1-3yr", 2, "domain", "Case Study & Business Impact",
           ["business_problem_framing", "data_pipeline", "ab_testing", "metrics_design"],
           "medium", 5, "Lead Data Scientist", "warm_but_probing",
           "Real-world case study. Business impact and A/B testing.",
           ["analytical_thinking", "business_sense", "communication", "problem_solving"]),
        _d("data_science", "1-3yr", 3, "behavioral", "Behavioral Round",
           ["collaboration", "stakeholder_management", "project_ownership"],
           "easy", 5, "Manager", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("data_science", "1-3yr", 4, "hr", "HR Interview",
           ["salary_expectations", "career_goals", "notice_period"],
           "easy", 4, "HR Manager", "friendly", "", _HR_DIMS),
        # 3-7yr
        _d("data_science", "3-7yr", 1, "technical", "Advanced ML & System Design",
           ["deep_learning", "nlp_cv", "ml_system_design", "model_serving"],
           "hard", 6, "Principal Data Scientist", "skeptical",
           "Advanced ML. Model serving at scale. MLOps awareness.",
           ["ml_knowledge", "system_thinking", "coding_ability", "scalability"]),
        _d("data_science", "3-7yr", 2, "system_design", "ML System Design",
           ["ml_pipelines", "feature_stores", "model_monitoring", "data_architecture"],
           "hard", 6, "ML Engineer Lead", "warm_but_probing",
           "Design an end-to-end ML system. Data pipeline to serving.",
           _DESIGN_DIMS + ["ml_knowledge"]),
        _d("data_science", "3-7yr", 3, "behavioral", "Leadership & Impact",
           ["mentoring", "stakeholder_management", "cross_team_collaboration"],
           "medium", 5, "Director", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("data_science", "3-7yr", 4, "hr", "HR Interview",
           ["salary_negotiation", "career_trajectory"],
           "easy", 4, "Senior HR", "friendly", "", _HR_DIMS),
        # 7-12yr
        _d("data_science", "7-12yr", 1, "technical", "ML Architecture & Strategy",
           ["ml_platform", "research_to_production", "team_building", "technical_strategy"],
           "expert", 6, "VP Data Science", "intense", "", _TECH_DIMS + _DESIGN_DIMS),
        _d("data_science", "7-12yr", 2, "behavioral", "Leadership & Org Impact",
           ["org_building", "strategy", "executive_communication"],
           "hard", 5, "VP/Director", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("data_science", "7-12yr", 3, "final", "Executive Round",
           ["vision", "culture_fit", "strategic_alignment"],
           "hard", 4, "CTO", "skeptical", "", ["overall_fit", "leadership"]),
        # 12+yr
        _d("data_science", "12+yr", 1, "system_design", "AI/ML Strategy & Platform",
           ["ai_strategy", "platform_architecture", "org_design"],
           "expert", 5, "CTO/CEO", "intense", "", _DESIGN_DIMS),
        _d("data_science", "12+yr", 2, "behavioral", "Executive Leadership",
           ["vision", "org_building", "stakeholder_management"],
           "hard", 5, "Board/C-Suite", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("data_science", "12+yr", 3, "final", "Executive Panel",
           ["overall_assessment"], "hard", 4, "Board", "skeptical", "",
           ["leadership", "strategic_thinking"]),
    ]

    # ────────────────────────────────────
    # DEVOPS
    # ────────────────────────────────────
    blueprints += [
        # Fresher
        _d("devops", "fresher", 1, "technical", "DevOps Fundamentals",
           ["linux", "networking", "scripting", "git", "ci_cd_basics"],
           "easy", 7, "DevOps Engineer", "friendly",
           "Linux basics, networking, shell scripting, Git.",
           ["technical_depth", "problem_solving", "system_thinking"]),
        _d("devops", "fresher", 2, "behavioral", "Behavioral Round",
           ["communication", "teamwork", "learning_ability"],
           "easy", 5, "Manager", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("devops", "fresher", 3, "hr", "HR Interview",
           ["salary_expectations", "career_goals"],
           "easy", 4, "HR Manager", "friendly", "", _HR_DIMS),
        # 1-3yr
        _d("devops", "1-3yr", 1, "technical", "DevOps Technical",
           ["docker", "kubernetes_basics", "ci_cd", "monitoring", "cloud_basics"],
           "medium", 7, "Senior DevOps Engineer", "neutral",
           "Containerization, CI/CD pipelines, basic cloud.",
           ["technical_depth", "problem_solving", "system_thinking", "automation"]),
        _d("devops", "1-3yr", 2, "domain", "Infrastructure Scenario",
           ["incident_response", "deployment_strategies", "infrastructure_as_code"],
           "medium", 5, "Lead SRE", "warm_but_probing",
           "Scenario-based. How would you handle X outage?",
           ["problem_solving", "system_thinking", "communication"]),
        _d("devops", "1-3yr", 3, "behavioral", "Behavioral Round",
           ["on_call_experience", "teamwork", "ownership"],
           "easy", 5, "Manager", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("devops", "1-3yr", 4, "hr", "HR Interview",
           ["salary_expectations", "on_call_willingness"],
           "easy", 4, "HR Manager", "friendly", "", _HR_DIMS),
        # 3-7yr
        _d("devops", "3-7yr", 1, "technical", "Infrastructure Deep Dive",
           ["kubernetes", "terraform", "cloud_architecture", "security", "observability"],
           "hard", 6, "Principal SRE", "skeptical", "",
           ["technical_depth", "system_thinking", "scalability", "security"]),
        _d("devops", "3-7yr", 2, "system_design", "Infrastructure Design",
           ["multi_region", "disaster_recovery", "zero_downtime", "cost_optimization"],
           "hard", 6, "Staff SRE", "warm_but_probing", "", _DESIGN_DIMS),
        _d("devops", "3-7yr", 3, "behavioral", "Leadership & Incident Management",
           ["incident_leadership", "mentoring", "cross_team_collaboration"],
           "medium", 5, "Director SRE", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("devops", "3-7yr", 4, "hr", "HR Interview",
           ["salary_negotiation", "career_trajectory"],
           "easy", 4, "Senior HR", "friendly", "", _HR_DIMS),
        # 7-12yr
        _d("devops", "7-12yr", 1, "system_design", "Platform Architecture",
           ["platform_engineering", "developer_experience", "cost_governance", "multi_cloud"],
           "expert", 6, "VP Infrastructure", "intense", "", _DESIGN_DIMS),
        _d("devops", "7-12yr", 2, "behavioral", "Leadership & Strategy",
           ["org_building", "vendor_management", "budget_planning"],
           "hard", 5, "VP Engineering", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("devops", "7-12yr", 3, "final", "Executive Round",
           ["overall_assessment", "strategic_vision"],
           "hard", 4, "CTO", "skeptical", "", ["leadership", "strategic_thinking"]),
        # 12+yr
        _d("devops", "12+yr", 1, "system_design", "Infrastructure Strategy",
           ["technology_strategy", "org_design", "platform_vision"],
           "expert", 5, "CTO", "intense", "", _DESIGN_DIMS),
        _d("devops", "12+yr", 2, "final", "Executive Panel",
           ["overall_assessment"], "hard", 4, "Board/C-Suite", "skeptical", "",
           ["leadership", "strategic_thinking"]),
    ]

    # ────────────────────────────────────
    # PRODUCT MANAGEMENT
    # ────────────────────────────────────
    blueprints += [
        # Fresher (Associate PM)
        _d("product_management", "fresher", 1, "domain", "Product Sense",
           ["product_thinking", "user_empathy", "feature_prioritization", "metrics"],
           "easy", 6, "Product Manager", "warm_but_probing",
           "Product sense questions. Favorite product analysis.",
           ["product_thinking", "analytical_thinking", "communication", "creativity"]),
        _d("product_management", "fresher", 2, "behavioral", "Behavioral & Communication",
           ["communication", "teamwork", "leadership_potential", "stakeholder_management"],
           "easy", 5, "Senior PM", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("product_management", "fresher", 3, "hr", "HR Interview",
           ["salary_expectations", "career_goals"],
           "easy", 4, "HR Manager", "friendly", "", _HR_DIMS),
        # 1-3yr
        _d("product_management", "1-3yr", 1, "domain", "Product Case Study",
           ["product_strategy", "user_research", "metrics_design", "go_to_market"],
           "medium", 6, "Senior PM", "warm_but_probing",
           "Product case study. Design a feature for X.",
           ["product_thinking", "analytical_thinking", "communication"]),
        _d("product_management", "1-3yr", 2, "domain", "Metrics & Analytics",
           ["ab_testing", "funnel_analysis", "kpi_design", "data_driven_decisions"],
           "medium", 5, "Lead PM", "neutral",
           "Analytical round. Metrics and data interpretation.",
           ["analytical_thinking", "data_literacy", "problem_solving"]),
        _d("product_management", "1-3yr", 3, "behavioral", "Behavioral Round",
           ["stakeholder_management", "cross_functional_collaboration", "conflict_resolution"],
           "easy", 5, "Director", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("product_management", "1-3yr", 4, "hr", "HR Interview",
           ["salary_expectations", "career_goals"],
           "easy", 4, "HR Manager", "friendly", "", _HR_DIMS),
        # 3-7yr
        _d("product_management", "3-7yr", 1, "domain", "Product Strategy",
           ["product_vision", "roadmap_planning", "competitive_analysis", "market_sizing"],
           "hard", 6, "VP Product", "skeptical",
           "Strategic product thinking. Market analysis.",
           ["product_thinking", "strategic_thinking", "communication"]),
        _d("product_management", "3-7yr", 2, "domain", "Execution & Metrics",
           ["execution_planning", "resource_allocation", "success_metrics", "experimentation"],
           "hard", 5, "Director Product", "warm_but_probing", "",
           ["analytical_thinking", "execution", "problem_solving"]),
        _d("product_management", "3-7yr", 3, "behavioral", "Leadership",
           ["team_leadership", "influence_without_authority", "executive_communication"],
           "medium", 5, "VP/Director", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("product_management", "3-7yr", 4, "final", "Executive Round",
           ["vision_alignment", "culture_fit"],
           "hard", 4, "CEO/CPO", "skeptical", "", ["leadership", "strategic_thinking"]),
        # 7-12yr
        _d("product_management", "7-12yr", 1, "domain", "Product Vision & Strategy",
           ["product_vision", "platform_strategy", "market_creation"],
           "expert", 6, "CPO", "intense", "",
           ["strategic_thinking", "product_thinking", "leadership"]),
        _d("product_management", "7-12yr", 2, "behavioral", "Executive Leadership",
           ["org_building", "board_communication", "cross_functional_leadership"],
           "hard", 5, "CEO", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("product_management", "7-12yr", 3, "final", "Board/Executive Panel",
           ["overall_assessment"], "hard", 4, "Board", "skeptical", "",
           ["leadership", "strategic_thinking"]),
        # 12+yr
        _d("product_management", "12+yr", 1, "domain", "Product & Business Strategy",
           ["business_strategy", "market_creation", "org_scaling"],
           "expert", 5, "CEO/Board", "intense", "",
           ["strategic_thinking", "leadership", "business_acumen"]),
        _d("product_management", "12+yr", 2, "final", "Executive Panel",
           ["overall_assessment"], "hard", 4, "Board", "skeptical", "",
           ["leadership", "strategic_thinking"]),
    ]

    # ────────────────────────────────────
    # QA / TESTING
    # ────────────────────────────────────
    blueprints += [
        # Fresher
        _d("qa_testing", "fresher", 1, "technical", "Testing Fundamentals",
           ["testing_concepts", "test_case_design", "manual_testing", "bug_lifecycle", "sdlc"],
           "easy", 7, "QA Lead", "friendly",
           "Testing basics. SDLC, test case writing, defect lifecycle.",
           ["testing_knowledge", "analytical_thinking", "attention_to_detail"]),
        _d("qa_testing", "fresher", 2, "behavioral", "Behavioral Round",
           ["communication", "attention_to_detail", "teamwork"],
           "easy", 5, "Manager", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("qa_testing", "fresher", 3, "hr", "HR Interview",
           ["salary_expectations", "career_goals"],
           "easy", 4, "HR Manager", "friendly", "", _HR_DIMS),
        # 1-3yr
        _d("qa_testing", "1-3yr", 1, "technical", "Testing Technical",
           ["automation_basics", "selenium", "api_testing", "test_frameworks", "sql"],
           "medium", 7, "Senior QA Engineer", "neutral",
           "Automation basics. Selenium, API testing, SQL queries.",
           ["testing_knowledge", "coding_ability", "analytical_thinking"]),
        _d("qa_testing", "1-3yr", 2, "domain", "Testing Scenarios",
           ["test_strategy", "regression_planning", "edge_case_identification"],
           "medium", 5, "QA Lead", "warm_but_probing",
           "Scenario-based. How would you test X feature?",
           ["testing_knowledge", "analytical_thinking", "problem_solving"]),
        _d("qa_testing", "1-3yr", 3, "behavioral", "Behavioral Round",
           ["teamwork", "conflict_with_developers", "quality_advocacy"],
           "easy", 5, "Manager", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("qa_testing", "1-3yr", 4, "hr", "HR Interview",
           ["salary_expectations", "career_goals"],
           "easy", 4, "HR Manager", "friendly", "", _HR_DIMS),
        # 3-7yr
        _d("qa_testing", "3-7yr", 1, "technical", "Automation & Architecture",
           ["test_architecture", "ci_cd_integration", "performance_testing", "security_testing"],
           "hard", 6, "Principal QA", "skeptical",
           "Test architecture. Performance and security testing.",
           ["testing_knowledge", "system_thinking", "coding_ability"]),
        _d("qa_testing", "3-7yr", 2, "domain", "Quality Strategy",
           ["test_strategy", "quality_metrics", "shift_left", "risk_based_testing"],
           "hard", 5, "QA Manager", "warm_but_probing", "",
           ["strategic_thinking", "analytical_thinking", "communication"]),
        _d("qa_testing", "3-7yr", 3, "behavioral", "Leadership",
           ["team_leadership", "mentoring", "process_improvement"],
           "medium", 5, "Director QA", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("qa_testing", "3-7yr", 4, "hr", "HR Interview",
           ["salary_negotiation", "career_trajectory"],
           "easy", 4, "Senior HR", "friendly", "", _HR_DIMS),
        # 7-12yr
        _d("qa_testing", "7-12yr", 1, "domain", "Quality Engineering Vision",
           ["quality_engineering", "test_platform", "org_quality_culture"],
           "expert", 6, "VP Quality", "intense", "",
           ["strategic_thinking", "system_thinking", "leadership"]),
        _d("qa_testing", "7-12yr", 2, "behavioral", "Executive Leadership",
           ["org_building", "quality_culture", "executive_communication"],
           "hard", 5, "VP Engineering", "warm_but_probing", "", _BEHAVIORAL_DIMS),
        _d("qa_testing", "7-12yr", 3, "final", "Executive Round",
           ["overall_assessment"], "hard", 4, "CTO", "skeptical", "",
           ["leadership", "strategic_thinking"]),
        # 12+yr
        _d("qa_testing", "12+yr", 1, "domain", "Quality Strategy & Org Design",
           ["quality_strategy", "org_design", "industry_standards"],
           "expert", 5, "CTO/VP", "intense", "",
           ["strategic_thinking", "leadership"]),
        _d("qa_testing", "12+yr", 2, "final", "Executive Panel",
           ["overall_assessment"], "hard", 4, "Board/C-Suite", "skeptical", "",
           ["leadership", "strategic_thinking"]),
    ]

    return blueprints
