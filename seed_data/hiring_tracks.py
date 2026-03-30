"""
Company Hiring Tracks — Structured hiring track data for top 20 companies.

Each company has 1-4 hiring tracks, each with:
  - target_levels: which experience levels this track applies to
  - eligibility: CGPA cutoff, branches, backlog policy
  - difficulty_tier: low / medium / high / very_high
  - selection_test: NQT, InfyTQ, NLTH, etc.
"""
from typing import List, Dict


def _t(
    company: str, code: str, name: str, levels: list, salary: str,
    elig: dict, tier: str, desc: str = "", test: str = "",
    bond: int = 0, training: str = "", default: int = 0,
) -> Dict:
    return {
        "company_name": company,
        "track_code": code,
        "track_name": name,
        "target_levels": levels,
        "salary_range": salary,
        "eligibility": elig,
        "difficulty_tier": tier,
        "description": desc,
        "selection_test": test,
        "bond_years": bond,
        "training_info": training,
        "is_default": default,
    }


_FRESHER = ["fresher"]
_FRESHER_JUNIOR = ["fresher", "1-3yr"]
_MID = ["3-7yr"]
_SENIOR = ["7-12yr", "12+yr"]
_ALL = ["fresher", "1-3yr", "3-7yr", "7-12yr", "12+yr"]
_CSE = ["CSE", "IT", "ECE", "EEE", "MCA"]
_ALL_BRANCHES = ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil", "MCA"]


def get_hiring_tracks() -> List[Dict]:
    return [
        # ════════════════════════════════════════
        # TCS — 3 tracks
        # ════════════════════════════════════════
        _t("TCS", "tcs_ninja", "TCS Ninja", _FRESHER, "3.36 LPA",
           {"min_cgpa": 6.0, "branches": _ALL_BRANCHES, "backlogs": "no_active"},
           "low", "Mass hiring track for freshers. Aptitude + basic coding.",
           "TCS NQT", 2, "ILP at Trivandrum/Chennai, 2-3 months", 1),

        _t("TCS", "tcs_digital", "TCS Digital", _FRESHER, "7 LPA",
           {"min_cgpa": 7.0, "branches": _CSE, "backlogs": "no_active_or_history"},
           "medium", "Higher package for strong NQT performers. Deeper technical interview.",
           "TCS NQT (Digital cutoff)", 2, "ILP at Trivandrum/Chennai, 2-3 months"),

        _t("TCS", "tcs_prime", "TCS Prime", _FRESHER, "9 LPA",
           {"min_cgpa": 7.5, "branches": _CSE, "backlogs": "none"},
           "high", "Top-tier hiring. Strong coding + system design awareness required.",
           "TCS NQT (Prime cutoff) + CodeVita", 2, "ILP at Trivandrum/Chennai"),

        # ════════════════════════════════════════
        # Infosys — 3 tracks
        # ════════════════════════════════════════
        _t("Infosys", "infosys_se", "Systems Engineer", _FRESHER, "3.6 LPA",
           {"min_cgpa": 6.0, "branches": _ALL_BRANCHES, "backlogs": "no_active"},
           "low", "Standard fresher hiring. InfyTQ or campus test + interview.",
           "InfyTQ / Campus Test", 1, "Mysore campus training, 3-4 months", 1),

        _t("Infosys", "infosys_sp", "Specialist Programmer", _FRESHER, "5 LPA",
           {"min_cgpa": 7.0, "branches": _CSE, "backlogs": "no_active"},
           "medium", "Better package for candidates who clear InfyTQ certification.",
           "InfyTQ Certification", 1, "Mysore campus training"),

        _t("Infosys", "infosys_pp", "Power Programmer", _FRESHER, "6.5 LPA",
           {"min_cgpa": 7.5, "branches": _CSE, "backlogs": "none"},
           "high", "Top track via HackWithInfy or strong InfyTQ performance.",
           "HackWithInfy / InfyTQ Advanced", 1, "Mysore campus training"),

        # ════════════════════════════════════════
        # Wipro — 2 tracks
        # ════════════════════════════════════════
        _t("Wipro", "wipro_elite", "Wipro Elite", _FRESHER, "3.5 LPA",
           {"min_cgpa": 6.0, "branches": _ALL_BRANCHES, "backlogs": "no_active"},
           "low", "Standard campus hiring via NLTH exam.",
           "Wipro NLTH", 1, "Training at Wipro campus", 1),

        _t("Wipro", "wipro_turbo", "Wipro Turbo", _FRESHER, "6.5 LPA",
           {"min_cgpa": 7.0, "branches": _CSE, "backlogs": "no_active"},
           "medium", "Higher package for top NLTH performers.",
           "Wipro NLTH (Turbo cutoff)", 1, "Training at Wipro campus"),

        # ════════════════════════════════════════
        # Cognizant — 3 tracks
        # ════════════════════════════════════════
        _t("Cognizant", "cognizant_genc", "GenC", _FRESHER, "4 LPA",
           {"min_cgpa": 6.0, "branches": _ALL_BRANCHES, "backlogs": "no_active"},
           "low", "Entry-level mass hiring track.",
           "AMCAT / Cognizant Online Test", 0, "", 1),

        _t("Cognizant", "cognizant_genc_next", "GenC Next", _FRESHER, "6.75 LPA",
           {"min_cgpa": 7.0, "branches": _CSE, "backlogs": "no_active"},
           "medium", "Mid-tier track requiring stronger coding skills.",
           "Cognizant Online Test (Next cutoff)"),

        _t("Cognizant", "cognizant_genc_elevate", "GenC Elevate", _FRESHER, "9.5 LPA",
           {"min_cgpa": 7.5, "branches": _CSE, "backlogs": "none"},
           "high", "Top track. Strong coding + aptitude required.",
           "Cognizant Online Test (Elevate cutoff)"),

        # ════════════════════════════════════════
        # Accenture — 2 tracks
        # ════════════════════════════════════════
        _t("Accenture", "accenture_ase", "Associate Software Engineer", _FRESHER, "4.5 LPA",
           {"min_cgpa": 6.0, "branches": _ALL_BRANCHES, "backlogs": "no_active"},
           "low", "Standard campus hiring. Cognitive + communication + technical.",
           "Accenture Assessment", 2, "Bangalore campus training", 1),

        _t("Accenture", "accenture_ace", "ACE (Advanced)", _FRESHER, "7 LPA",
           {"min_cgpa": 7.0, "branches": _CSE, "backlogs": "no_active"},
           "medium", "Advanced track with deeper coding round.",
           "Accenture Assessment (ACE cutoff)", 2, "Bangalore campus training"),

        # ════════════════════════════════════════
        # HCL Technologies — 1 track
        # ════════════════════════════════════════
        _t("HCL Technologies", "hcl_fresher", "Fresher Hiring", _FRESHER, "3.5-4 LPA",
           {"min_cgpa": 6.0, "branches": _ALL_BRANCHES, "backlogs": "no_active"},
           "low", "Standard fresher campus hiring.",
           "HCL Online Test", 1, "Training at Noida/Chennai campus", 1),

        # ════════════════════════════════════════
        # Tech Mahindra — 1 track
        # ════════════════════════════════════════
        _t("Tech Mahindra", "techm_fresher", "Fresher Hiring", _FRESHER, "3.25-3.75 LPA",
           {"min_cgpa": 6.0, "branches": _ALL_BRANCHES, "backlogs": "no_active"},
           "low", "Campus hiring with GD round.",
           "Tech Mahindra Online Test", 1, "Training at Pune/Hyderabad", 1),

        # ════════════════════════════════════════
        # Capgemini — 2 tracks
        # ════════════════════════════════════════
        _t("Capgemini", "capgemini_analyst", "Analyst", _FRESHER, "3.8 LPA",
           {"min_cgpa": 6.0, "branches": _ALL_BRANCHES, "backlogs": "no_active"},
           "low", "Standard track with game-based assessment.",
           "Plum Assessment + Pseudo Code Test", 0, "", 1),

        _t("Capgemini", "capgemini_exceller", "Exceller", _FRESHER, "6 LPA",
           {"min_cgpa": 7.0, "branches": _CSE, "backlogs": "no_active"},
           "medium", "Higher track with deeper pseudo code and communication round.",
           "Plum Assessment + Pseudo Code (Exceller cutoff)"),

        # ════════════════════════════════════════
        # LTIMindtree — 1 track
        # ════════════════════════════════════════
        _t("LTIMindtree", "ltimindtree_fresher", "Fresher Hiring", _FRESHER, "4.5 LPA",
           {"min_cgpa": 6.5, "branches": _CSE, "backlogs": "no_active"},
           "medium", "Campus hiring with coding + technical interview.",
           "LTIMindtree Online Test", 1, "", 1),

        # ════════════════════════════════════════
        # Zoho — 2 tracks
        # ════════════════════════════════════════
        _t("Zoho", "zoho_fresher", "Fresher (C Programming)", _FRESHER, "5-7 LPA",
           {"min_cgpa": 0, "branches": _CSE, "backlogs": "flexible"},
           "high", "Unique hiring — C programming focused, no CGPA cutoff. Multiple coding rounds.",
           "Zoho Off-Campus / Campus Test", 0, "In-house training at Zoho campus", 1),

        _t("Zoho", "zoho_lateral", "Lateral Hire", _MID, "8-15 LPA",
           {"min_cgpa": 0, "branches": _CSE, "backlogs": "flexible"},
           "high", "Experienced hire with deep technical + system design rounds.",
           "Zoho Coding Challenge"),

        # ════════════════════════════════════════
        # Persistent Systems — 1 track
        # ════════════════════════════════════════
        _t("Persistent Systems", "persistent_fresher", "Fresher Hiring", _FRESHER, "4.6 LPA",
           {"min_cgpa": 6.5, "branches": _CSE, "backlogs": "no_active"},
           "medium", "Campus hiring with aptitude + coding + interview.",
           "Persistent Online Test", 0, "", 1),

        # ════════════════════════════════════════
        # Mphasis — 1 track
        # ════════════════════════════════════════
        _t("Mphasis", "mphasis_fresher", "Fresher Hiring", _FRESHER, "3.5 LPA",
           {"min_cgpa": 6.0, "branches": _ALL_BRANCHES, "backlogs": "no_active"},
           "low", "Standard campus hiring.",
           "Mphasis Online Test", 0, "", 1),

        # ════════════════════════════════════════
        # Google — 2 tracks
        # ════════════════════════════════════════
        _t("Google", "google_l3", "Software Engineer L3", _FRESHER_JUNIOR, "25-35 LPA",
           {"min_cgpa": 0, "branches": _CSE, "backlogs": "flexible"},
           "very_high", "New grad / junior hire. Multiple coding + behavioral rounds.",
           "Google Online Assessment", 0, "", 1),

        _t("Google", "google_l4", "Software Engineer L4", _MID, "35-55 LPA",
           {"min_cgpa": 0, "branches": _CSE, "backlogs": "flexible"},
           "very_high", "Mid-level hire. Coding + system design + behavioral + hiring committee.",
           "Google Recruiter Screen"),

        # ════════════════════════════════════════
        # Amazon — 2 tracks
        # ════════════════════════════════════════
        _t("Amazon", "amazon_sde1", "SDE-1", _FRESHER_JUNIOR, "25-40 LPA",
           {"min_cgpa": 0, "branches": _CSE, "backlogs": "flexible"},
           "very_high", "Entry-level SDE. OA + phone screen + onsite loops.",
           "Amazon OA", 0, "", 1),

        _t("Amazon", "amazon_sde2", "SDE-2", _MID, "40-65 LPA",
           {"min_cgpa": 0, "branches": _CSE, "backlogs": "flexible"},
           "very_high", "Mid-level SDE. System design heavy.",
           "Amazon Recruiter Screen"),

        # ════════════════════════════════════════
        # Microsoft — 2 tracks
        # ════════════════════════════════════════
        _t("Microsoft", "microsoft_sde59", "SDE 59 (New Grad)", _FRESHER_JUNIOR, "18-28 LPA",
           {"min_cgpa": 0, "branches": _CSE, "backlogs": "flexible"},
           "high", "New grad SDE. Coding + design + behavioral.",
           "Microsoft Online Assessment", 0, "", 1),

        _t("Microsoft", "microsoft_sde60", "SDE 60", _MID, "28-42 LPA",
           {"min_cgpa": 0, "branches": _CSE, "backlogs": "flexible"},
           "very_high", "Mid-level SDE with system design emphasis.",
           "Microsoft Recruiter Screen"),

        # ════════════════════════════════════════
        # Flipkart — 2 tracks
        # ════════════════════════════════════════
        _t("Flipkart", "flipkart_sde1", "SDE-1", _FRESHER_JUNIOR, "20-30 LPA",
           {"min_cgpa": 0, "branches": _CSE, "backlogs": "flexible"},
           "high", "Entry-level SDE at Flipkart. Machine coding + DSA.",
           "Flipkart Hiring Challenge", 0, "", 1),

        _t("Flipkart", "flipkart_sde2", "SDE-2", _MID, "30-50 LPA",
           {"min_cgpa": 0, "branches": _CSE, "backlogs": "flexible"},
           "very_high", "Mid-level SDE. System design + LLD + HLD.",
           "Flipkart Recruiter Screen"),
    ]
