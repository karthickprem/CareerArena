"""
InterviewerEngine — Dynamic behavioral engine for interview sub-agents.

Persona IDENTITY (name, expertise, system_prompt) is dynamic — generated per
candidate/company by PanelGenerator. Behavioral PATTERNS (phase machines,
question banks, personality micro-behaviors, difficulty ladders) are systematic
templates that any dynamic persona maps into.

This engine owns:
  1. Round phase machine (warmup -> explore -> deep_dive -> pressure -> wrap)
  2. Question bank per round_type + difficulty (~60 proven questions)
  3. Personality behavior templates per personality type
  4. Difficulty ladder (easy -> medium -> hard -> expert) — "find the ceiling"
  5. Per-interviewer scorecard — running assessment during the round
"""

from __future__ import annotations

import json
import logging
import random
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Tuple

from llm_client import LLMClient
from database import CareerDB
from knowledge_db import KnowledgeDB
from interviewer_personas import InterviewerPersona
from candidate_model import CandidateModel

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════
# ROUND PHASE MACHINE
# ═══════════════════════════════════════════════════════

ROUND_PHASES: Dict[str, List[dict]] = {
    # Technical / System Design / Domain rounds
    "technical": [
        {"name": "warmup", "min_questions": 1, "max_questions": 2,
         "goal": "Build rapport, ease candidate in with a comfortable topic from their resume"},
        {"name": "explore", "min_questions": 2, "max_questions": 3,
         "goal": "Broadly explore technical surface area — find out what they actually know vs claim"},
        {"name": "deep_dive", "min_questions": 2, "max_questions": 3,
         "goal": "Go DEEP on their strongest claimed area — find the ceiling of their knowledge"},
        {"name": "pressure", "min_questions": 1, "max_questions": 2,
         "goal": "Push into unknown territory — edge cases, trade-offs, what-ifs, system failures"},
        {"name": "wrap", "min_questions": 1, "max_questions": 1,
         "goal": "Final reflection question — what would they do differently, what excites them"},
    ],
    "system_design": [
        {"name": "warmup", "min_questions": 1, "max_questions": 1,
         "goal": "Light opener about their experience with scale or distributed systems"},
        {"name": "explore", "min_questions": 1, "max_questions": 2,
         "goal": "Present a design problem, let them think out loud about requirements"},
        {"name": "deep_dive", "min_questions": 3, "max_questions": 4,
         "goal": "Dig into their design choices — data models, APIs, scale, failure modes"},
        {"name": "pressure", "min_questions": 1, "max_questions": 2,
         "goal": "Change constraints — 10x traffic, new region, conflicting requirements"},
        {"name": "wrap", "min_questions": 1, "max_questions": 1,
         "goal": "Monitoring, deployment, team coordination around the design"},
    ],
    # Behavioral / HR rounds
    "behavioral": [
        {"name": "connect", "min_questions": 1, "max_questions": 2,
         "goal": "Personal connection — journey, motivations, what drives them"},
        {"name": "behavioral", "min_questions": 2, "max_questions": 3,
         "goal": "STAR-based questions on teamwork, conflict, leadership, failures"},
        {"name": "values", "min_questions": 2, "max_questions": 3,
         "goal": "Values alignment — work ethic, ethics, priorities, deal-breakers"},
        {"name": "negotiation", "min_questions": 1, "max_questions": 2,
         "goal": "Salary expectations, growth path, what they want from the role"},
        {"name": "close", "min_questions": 1, "max_questions": 1,
         "goal": "Reverse questions from candidate, final impressions"},
    ],
    "hr": [
        {"name": "connect", "min_questions": 1, "max_questions": 2,
         "goal": "Warm opener, make them feel this is a conversation not an interrogation"},
        {"name": "behavioral", "min_questions": 2, "max_questions": 3,
         "goal": "Behavioral probing with STAR — conflicts, failures, teamwork, deadlines"},
        {"name": "values", "min_questions": 2, "max_questions": 3,
         "goal": "Cultural fit, work-life balance views, what environment they thrive in"},
        {"name": "negotiation", "min_questions": 1, "max_questions": 2,
         "goal": "Salary discussion, notice period, joining timeline, competing offers"},
        {"name": "close", "min_questions": 1, "max_questions": 1,
         "goal": "Company pitch, reverse questions, next steps"},
    ],
    # Stress / Rapid-fire rounds
    "stress": [
        {"name": "disarm", "min_questions": 1, "max_questions": 1,
         "goal": "Deceptively friendly opener — lull them into comfort"},
        {"name": "challenge", "min_questions": 2, "max_questions": 3,
         "goal": "Challenge their claims and assumptions directly but professionally"},
        {"name": "rapid_fire", "min_questions": 2, "max_questions": 3,
         "goal": "Quick-fire questions across different areas — test agility and composure"},
        {"name": "contradiction", "min_questions": 1, "max_questions": 2,
         "goal": "Point out inconsistencies between their answers, see how they handle it"},
        {"name": "recovery", "min_questions": 1, "max_questions": 1,
         "goal": "Ease off, let them recover — shows emotional resilience observation"},
    ],
    # Final rounds (typically VP/Director level)
    "final": [
        {"name": "warmup", "min_questions": 1, "max_questions": 1,
         "goal": "Brief rapport — acknowledge the interview journey so far"},
        {"name": "strategic", "min_questions": 2, "max_questions": 3,
         "goal": "Big-picture thinking — where do they see impact, how do they think about problems"},
        {"name": "ownership", "min_questions": 2, "max_questions": 3,
         "goal": "Test ownership mindset — failures, disagreements with management, going above and beyond"},
        {"name": "culture", "min_questions": 1, "max_questions": 2,
         "goal": "Culture add assessment — what do they bring that the team doesn't have"},
        {"name": "close", "min_questions": 1, "max_questions": 1,
         "goal": "Final pitch and reverse questions"},
    ],
    # Domain-specific rounds
    "domain": [
        {"name": "warmup", "min_questions": 1, "max_questions": 2,
         "goal": "Explore their domain background and what drew them to this field"},
        {"name": "explore", "min_questions": 2, "max_questions": 3,
         "goal": "Broad domain knowledge check — fundamentals, terminology, awareness"},
        {"name": "deep_dive", "min_questions": 2, "max_questions": 3,
         "goal": "Deep into their specialization — applied knowledge, real scenarios"},
        {"name": "application", "min_questions": 1, "max_questions": 2,
         "goal": "How would they apply domain knowledge to solve a real business problem"},
        {"name": "wrap", "min_questions": 1, "max_questions": 1,
         "goal": "Industry trends, future of the domain, their continued learning plan"},
    ],
}

# Default fallback
ROUND_PHASES["hr_behavioral"] = ROUND_PHASES["behavioral"]


# ═══════════════════════════════════════════════════════
# QUESTION BANK — Proven templates per round_type + phase
# Placeholders: {candidate_name}, {skill}, {project},
#   {company}, {role}, {topic}, {claim}, {weakness}
# ═══════════════════════════════════════════════════════

QUESTION_BANK: Dict[str, Dict[str, List[dict]]] = {
    "technical": {
        "warmup": [
            {"q": "I see you've worked with {skill} — what's the most interesting problem you solved with it?",
             "difficulty": "easy", "signal": "passion_and_depth", "follow_up": True},
            {"q": "Walk me through your {project} project. What was your specific contribution?",
             "difficulty": "easy", "signal": "ownership_clarity", "follow_up": True},
            {"q": "What's your go-to tech stack these days, and why?",
             "difficulty": "easy", "signal": "awareness_and_reasoning", "follow_up": False},
            {"q": "Before we dive in — which area of your work are you most proud of technically?",
             "difficulty": "easy", "signal": "self_awareness", "follow_up": True},
        ],
        "explore": [
            {"q": "You mentioned {skill} — can you explain how {topic} works under the hood?",
             "difficulty": "medium", "signal": "conceptual_depth", "follow_up": True},
            {"q": "If I gave you a choice between {skill} and an alternative, what trade-offs would you consider?",
             "difficulty": "medium", "signal": "trade_off_thinking", "follow_up": True},
            {"q": "How do you approach debugging a production issue that you've never seen before?",
             "difficulty": "medium", "signal": "problem_solving_process", "follow_up": True},
            {"q": "Walk me through how you'd design a simple REST API for {topic}. What decisions would you make?",
             "difficulty": "medium", "signal": "design_thinking", "follow_up": True},
            {"q": "What's the difference between {topic} and its alternatives? When would you pick each?",
             "difficulty": "medium", "signal": "breadth_and_comparison", "follow_up": False},
            {"q": "You listed {skill} on your resume — have you used it in production or mainly for learning?",
             "difficulty": "medium", "signal": "honesty_and_depth", "follow_up": True},
        ],
        "deep_dive": [
            {"q": "Let's go deeper on {topic}. Can you explain what happens internally when {specific_scenario}?",
             "difficulty": "hard", "signal": "internals_knowledge", "follow_up": True},
            {"q": "You said you used {skill} — what would happen if {edge_case}? How would you handle it?",
             "difficulty": "hard", "signal": "edge_case_handling", "follow_up": True},
            {"q": "If this system needed to handle 100x the current load, what would break first and how would you fix it?",
             "difficulty": "hard", "signal": "scalability_thinking", "follow_up": True},
            {"q": "Can you write the core logic for {topic} — just pseudocode is fine — how would you structure it?",
             "difficulty": "hard", "signal": "coding_ability", "follow_up": True},
            {"q": "What's the worst architectural decision you've seen (or made)? What would you do differently?",
             "difficulty": "hard", "signal": "judgment_and_learning", "follow_up": True},
        ],
        "pressure": [
            {"q": "I'm not fully convinced you understand {topic} deeply. Can you prove me wrong with a specific example?",
             "difficulty": "expert", "signal": "conviction_under_pressure", "follow_up": True},
            {"q": "Your approach to {topic} has a flaw — {specific_flaw}. How would you address that?",
             "difficulty": "expert", "signal": "handling_criticism", "follow_up": True},
            {"q": "If the CEO walked in right now and said 'ship this by Friday with half the features', what would you cut and why?",
             "difficulty": "expert", "signal": "prioritization_under_pressure", "follow_up": False},
            {"q": "A junior developer on your team wrote code that works but is terrible. How would you handle it?",
             "difficulty": "hard", "signal": "mentorship_and_diplomacy", "follow_up": True},
        ],
        "wrap": [
            {"q": "Looking back at your career so far, what would you learn differently if you started over?",
             "difficulty": "easy", "signal": "self_awareness_and_growth", "follow_up": False},
            {"q": "What's something in tech that excites you right now that you haven't had a chance to work on?",
             "difficulty": "easy", "signal": "curiosity_and_passion", "follow_up": False},
            {"q": "Any questions for me about the team or the kind of work you'd be doing here?",
             "difficulty": "easy", "signal": "engagement_and_curiosity", "follow_up": False},
        ],
    },

    "behavioral": {
        "connect": [
            {"q": "Tell me a bit about your journey — what led you to {role} as a career path?",
             "difficulty": "easy", "signal": "narrative_and_motivation", "follow_up": True},
            {"q": "What does a great day at work look like for you?",
             "difficulty": "easy", "signal": "values_and_fit", "follow_up": False},
            {"q": "Outside of work, what's something you're passionate about?",
             "difficulty": "easy", "signal": "personality_and_authenticity", "follow_up": False},
        ],
        "behavioral": [
            {"q": "Tell me about a time you had a disagreement with a teammate. How did you handle it?",
             "difficulty": "medium", "signal": "conflict_resolution", "follow_up": True},
            {"q": "Describe a situation where you failed at something important. What did you learn?",
             "difficulty": "medium", "signal": "resilience_and_learning", "follow_up": True},
            {"q": "Give me an example of when you had to meet a tight deadline. What did you do?",
             "difficulty": "medium", "signal": "time_management", "follow_up": True},
            {"q": "Tell me about a time you had to convince someone who disagreed with your approach.",
             "difficulty": "medium", "signal": "influence_and_communication", "follow_up": True},
            {"q": "Describe a project where the requirements changed midway. How did you adapt?",
             "difficulty": "medium", "signal": "adaptability", "follow_up": True},
            {"q": "Have you ever had to give difficult feedback to someone? How did you approach it?",
             "difficulty": "hard", "signal": "leadership_and_empathy", "follow_up": True},
            {"q": "Tell me about a decision you made that turned out to be wrong. What happened next?",
             "difficulty": "medium", "signal": "accountability", "follow_up": True},
        ],
        "values": [
            {"q": "What kind of work environment brings out your best performance?",
             "difficulty": "easy", "signal": "self_awareness", "follow_up": True},
            {"q": "If you found out a colleague was cutting corners on quality, what would you do?",
             "difficulty": "medium", "signal": "integrity", "follow_up": True},
            {"q": "How do you balance doing things the 'right way' versus doing them the 'fast way'?",
             "difficulty": "medium", "signal": "pragmatism_vs_idealism", "follow_up": True},
            {"q": "What's a workplace value you won't compromise on, even if it costs you?",
             "difficulty": "medium", "signal": "core_values", "follow_up": False},
        ],
        "negotiation": [
            {"q": "What are your salary expectations for this role?",
             "difficulty": "medium", "signal": "negotiation_skill", "follow_up": True},
            {"q": "What matters more to you — compensation, growth, or work-life balance? Walk me through your thinking.",
             "difficulty": "medium", "signal": "priority_clarity", "follow_up": True},
            {"q": "Where do you see yourself in 3-5 years, and how does this role fit into that?",
             "difficulty": "easy", "signal": "ambition_and_fit", "follow_up": True},
        ],
        "close": [
            {"q": "Do you have any questions for me or the team?",
             "difficulty": "easy", "signal": "engagement", "follow_up": False},
            {"q": "Is there anything you wish I had asked you today?",
             "difficulty": "easy", "signal": "self_advocacy", "follow_up": False},
        ],
    },

    "stress": {
        "disarm": [
            {"q": "I've heard good things from the earlier rounds. Tell me — what do you think went well?",
             "difficulty": "easy", "signal": "self_assessment_trap", "follow_up": True},
            {"q": "Relax, this is just a conversation. So, what makes you think you deserve this role?",
             "difficulty": "medium", "signal": "confidence_and_humility", "follow_up": True},
        ],
        "challenge": [
            {"q": "You said you 'led' {project} — but from what I see, it sounds like you were just a contributor. Clarify.",
             "difficulty": "hard", "signal": "honesty_under_challenge", "follow_up": True},
            {"q": "Your resume says {skill} but you couldn't explain {topic} clearly. Should I be concerned?",
             "difficulty": "hard", "signal": "handling_direct_criticism", "follow_up": True},
            {"q": "If I told you the panel so far thinks you're not strong enough for this role, how would you respond?",
             "difficulty": "expert", "signal": "composure_and_conviction", "follow_up": True},
            {"q": "Your experience is quite limited for this role. Why should we take a chance on you?",
             "difficulty": "hard", "signal": "self_advocacy_under_pressure", "follow_up": True},
        ],
        "rapid_fire": [
            {"q": "Quick answers — {topic_1} vs {topic_2}, which and why?",
             "difficulty": "medium", "signal": "decisiveness", "follow_up": False},
            {"q": "In one sentence, what's the biggest risk in {topic}?",
             "difficulty": "medium", "signal": "conciseness", "follow_up": False},
            {"q": "What's one thing on your resume that you'd remove if you were being completely honest?",
             "difficulty": "hard", "signal": "radical_honesty", "follow_up": True},
            {"q": "Name three mistakes you've made in the last year. Go.",
             "difficulty": "hard", "signal": "self_awareness_speed", "follow_up": True},
        ],
        "contradiction": [
            {"q": "Earlier you said {claim_1}, but now you're saying something different. Which is it?",
             "difficulty": "expert", "signal": "consistency", "follow_up": True},
            {"q": "You claim to value {value}, but your {project} example suggests the opposite. Explain.",
             "difficulty": "expert", "signal": "authenticity", "follow_up": True},
        ],
        "recovery": [
            {"q": "Fair enough. Let's end on a positive — what's the one thing about yourself that no interview can capture?",
             "difficulty": "easy", "signal": "recovery_and_authenticity", "follow_up": False},
            {"q": "I pushed you hard today. How are you feeling about this conversation, honestly?",
             "difficulty": "easy", "signal": "emotional_intelligence", "follow_up": False},
        ],
    },

    "final": {
        "warmup": [
            {"q": "You've been through quite a process today. How are you feeling about everything so far?",
             "difficulty": "easy", "signal": "self_awareness", "follow_up": True},
        ],
        "strategic": [
            {"q": "If you joined us, what's the first problem you'd want to solve and why?",
             "difficulty": "medium", "signal": "initiative_and_vision", "follow_up": True},
            {"q": "What do you think is the biggest challenge facing {company} or this industry right now?",
             "difficulty": "medium", "signal": "industry_awareness", "follow_up": True},
            {"q": "How would you measure your own success in this role after 6 months?",
             "difficulty": "medium", "signal": "goal_orientation", "follow_up": True},
        ],
        "ownership": [
            {"q": "Tell me about a time you did something that wasn't in your job description because it needed to be done.",
             "difficulty": "medium", "signal": "ownership_mindset", "follow_up": True},
            {"q": "Have you ever disagreed with your manager's decision? What did you do?",
             "difficulty": "hard", "signal": "courage_and_diplomacy", "follow_up": True},
            {"q": "What's the hardest feedback you've ever received? How did it change you?",
             "difficulty": "medium", "signal": "growth_mindset", "follow_up": True},
        ],
        "culture": [
            {"q": "What kind of team dynamic do you work best in?",
             "difficulty": "easy", "signal": "team_fit", "follow_up": True},
            {"q": "What would your previous manager say is your biggest area for improvement?",
             "difficulty": "medium", "signal": "self_awareness_external", "follow_up": True},
        ],
        "close": [
            {"q": "Before we wrap up — anything you'd like to add that we haven't covered?",
             "difficulty": "easy", "signal": "completeness", "follow_up": False},
        ],
    },
}

# Copy shared question banks for aliases
QUESTION_BANK["hr"] = QUESTION_BANK["behavioral"]
QUESTION_BANK["hr_behavioral"] = QUESTION_BANK["behavioral"]
QUESTION_BANK["domain"] = QUESTION_BANK["technical"]  # domain reuses technical structure


# ═══════════════════════════════════════════════════════
# PERSONALITY MICRO-BEHAVIORS
# ═══════════════════════════════════════════════════════

PERSONALITY_BEHAVIORS: Dict[str, dict] = {
    "warm_but_probing": {
        "tone": "Friendly and encouraging but notices everything. Makes the candidate feel heard, then asks the hard follow-up.",
        "sentence_starters": [
            "That's a great point — ",
            "I appreciate you sharing that. ",
            "That's interesting — ",
            "I can see that. ",
            "Fair enough — but let me ask you this: ",
        ],
        "follow_up_style": "Acknowledges the answer warmly, then pivots to the harder angle. 'That's great, but what about...'",
        "when_evasive": "Gently but firmly redirects: 'I hear you, but I'd really like to understand specifically...'",
        "when_strong": "Shows genuine enthusiasm: 'Oh that's impressive — tell me more about how you...'",
        "when_weak": "Supportive but probing: 'That's okay, let me approach it differently...'",
    },
    "intense": {
        "tone": "Direct, focused, no small talk. Respects depth and gets impatient with surface answers.",
        "sentence_starters": [
            "Okay, but specifically — ",
            "Walk me through that. ",
            "Why? ",
            "What else? ",
            "Go deeper — ",
        ],
        "follow_up_style": "Pushes immediately for more depth. No praise until earned. 'That's surface level — what really happened?'",
        "when_evasive": "Calls it out directly: 'You're not answering my question. Let me rephrase...'",
        "when_strong": "Brief acknowledgment then harder question: 'Good. Now what about...'",
        "when_weak": "Notes it clinically: 'Okay, let's move on. What about...'",
    },
    "skeptical": {
        "tone": "Questioning, thinks out loud, challenges assumptions. Not hostile but clearly unconvinced by default.",
        "sentence_starters": [
            "Hmm, I'm not sure I buy that — ",
            "That sounds good on paper, but — ",
            "Help me understand — ",
            "Are you sure about that? ",
            "Let me push back a little — ",
        ],
        "follow_up_style": "Challenges every claim with 'but what about' or 'have you considered'. Tests conviction.",
        "when_evasive": "Increases skepticism: 'You're dancing around this. What are you not telling me?'",
        "when_strong": "Grudging respect: 'Okay, fair point. But what if...'",
        "when_weak": "Probes whether they know they're weak: 'Do you think that answer was strong? Why or why not?'",
    },
    "neutral": {
        "tone": "Professional, balanced, methodical. Neither warm nor cold. Focuses on substance.",
        "sentence_starters": [
            "Understood. ",
            "Let's explore that further. ",
            "Moving on — ",
            "Interesting. ",
            "Noted. ",
        ],
        "follow_up_style": "Systematic — moves through topics methodically, asks clarifying questions when needed.",
        "when_evasive": "Rephrases the question more specifically: 'Let me ask it differently...'",
        "when_strong": "Acknowledges factually: 'That shows good understanding. Next...'",
        "when_weak": "Moves on without judgment: 'Alright, let's try another area...'",
    },
    "friendly": {
        "tone": "Conversational, puts people at ease, genuinely curious. Makes it feel like chatting with a senior colleague.",
        "sentence_starters": [
            "Oh nice! ",
            "Tell me more about that — ",
            "I love that you mentioned — ",
            "That reminds me — ",
            "You know what, that's a good take. ",
        ],
        "follow_up_style": "Builds on what the candidate says naturally, like a conversation not an interrogation.",
        "when_evasive": "Playfully persistent: 'Come on, you can tell me — what really happened?'",
        "when_strong": "Genuinely enthusiastic: 'That's exactly the kind of thinking we look for!'",
        "when_weak": "Encouraging: 'That's okay! Let me give you a hint and see if that helps...'",
    },
}


# ═══════════════════════════════════════════════════════
# QUESTIONING STYLE BEHAVIORS
# ═══════════════════════════════════════════════════════

QUESTIONING_STYLE_RULES: Dict[str, str] = {
    "deep_dive": """QUESTIONING STYLE: Deep Dive
- Pick ONE topic and go 3-4 levels deep before switching
- Ask 'why' and 'how' follow-ups relentlessly
- Only move on when you've found the candidate's ceiling on this topic
- Don't accept 'I used X' — ask 'why X, how did X work, what went wrong with X'""",

    "behavioral_star": """QUESTIONING STYLE: Behavioral STAR
- Structure questions to elicit Situation-Task-Action-Result
- If the candidate skips any STAR component, ask for it specifically
- 'What was the situation?' → 'What was YOUR specific role?' → 'What did YOU do?' → 'What was the outcome?'
- Probe for personal contribution, not team contribution""",

    "rapid_fire": """QUESTIONING STYLE: Rapid Fire
- Keep questions short and punchy — max 2 sentences
- Expect quick answers — if they ramble, interrupt politely
- Cover multiple topics quickly to test breadth and agility
- Mix technical, behavioral, and opinion questions""",

    "case_based": """QUESTIONING STYLE: Case-Based
- Present real-world scenarios and ask how they'd approach them
- Build on their answer — 'Okay, now what if [new constraint]?'
- Look for structured thinking, not just the right answer
- Test both breadth of approach and depth of reasoning""",

    "socratic": """QUESTIONING STYLE: Socratic
- Guide the candidate to discover answers through questions
- 'What do you think would happen if...?'
- 'How does that connect to...?'
- Don't give answers — help them think through it
- Reward the reasoning process, not just the conclusion""",
}


# ═══════════════════════════════════════════════════════
# DIFFICULTY LADDER
# ═══════════════════════════════════════════════════════

DIFFICULTY_LEVELS = ["easy", "medium", "hard", "expert"]

DIFFICULTY_RULES: Dict[str, str] = {
    "easy": "Ask straightforward, foundational questions. Don't probe too deep. Accept reasonable answers.",
    "medium": "Ask questions that require explanation and reasoning. Expect specific examples. Follow up once.",
    "hard": "Push for deep understanding. Challenge assumptions. Expect trade-off analysis and real-world edge cases.",
    "expert": "Maximum difficulty. Challenge every answer. Present contradictions. Expect system-level thinking and novel solutions.",
}


# ═══════════════════════════════════════════════════════
# ENGINE STATE & SCORECARD
# ═══════════════════════════════════════════════════════

@dataclass
class DimensionScore:
    dimension: str
    score: float = 0.0  # 0-10
    evidence: List[str] = field(default_factory=list)
    question_count: int = 0


@dataclass
class InterviewerScorecard:
    """Running scorecard maintained by each interviewer during their round."""
    scores: Dict[str, DimensionScore] = field(default_factory=dict)
    overall_impression: str = ""
    recommendation: str = ""  # HIRE/NO_HIRE/LEAN_HIRE etc.
    key_strengths: List[str] = field(default_factory=list)
    key_concerns: List[str] = field(default_factory=list)
    follow_up_areas: List[str] = field(default_factory=list)

    def init_dimensions(self, dimensions: List[str]):
        for d in dimensions:
            if d not in self.scores:
                self.scores[d] = DimensionScore(dimension=d)

    def update_from_analysis(self, analysis: dict):
        """Update scorecard from LLM analysis of a Q&A exchange."""
        for dim, score_data in analysis.get("dimension_scores", {}).items():
            if dim in self.scores:
                ds = self.scores[dim]
                new_score = float(score_data.get("score", 0))
                # Running average
                ds.score = (ds.score * ds.question_count + new_score) / (ds.question_count + 1)
                ds.question_count += 1
                if score_data.get("evidence"):
                    ds.evidence.append(score_data["evidence"])

        if analysis.get("strengths"):
            for s in analysis["strengths"]:
                if s not in self.key_strengths:
                    self.key_strengths.append(s)
        if analysis.get("concerns"):
            for c in analysis["concerns"]:
                if c not in self.key_concerns:
                    self.key_concerns.append(c)

    def get_summary(self) -> str:
        lines = []
        for dim, ds in self.scores.items():
            if ds.question_count > 0:
                lines.append(f"  {dim}: {ds.score:.1f}/10 ({ds.question_count} questions)")
        if self.key_strengths:
            lines.append(f"  Strengths: {', '.join(self.key_strengths[:4])}")
        if self.key_concerns:
            lines.append(f"  Concerns: {', '.join(self.key_concerns[:4])}")
        return "\n".join(lines) if lines else "  No scores yet."

    def to_dict(self) -> dict:
        return {
            "scores": {k: {"score": v.score, "evidence": v.evidence, "question_count": v.question_count}
                       for k, v in self.scores.items()},
            "key_strengths": self.key_strengths,
            "key_concerns": self.key_concerns,
            "overall_impression": self.overall_impression,
            "recommendation": self.recommendation,
        }


@dataclass
class RoundEngineState:
    """Tracks the engine's state during a single round."""
    phase_index: int = 0
    phase_question_count: int = 0
    current_difficulty: str = "medium"
    follow_up_depth: int = 0  # How deep into a follow-up chain (0 = new topic)
    max_follow_up_depth: int = 3
    current_topic: str = ""
    questions_used: List[str] = field(default_factory=list)
    scorecard: InterviewerScorecard = field(default_factory=InterviewerScorecard)
    total_questions: int = 0

    def to_dict(self) -> dict:
        return {
            "phase_index": self.phase_index,
            "phase_question_count": self.phase_question_count,
            "current_difficulty": self.current_difficulty,
            "follow_up_depth": self.follow_up_depth,
            "current_topic": self.current_topic,
            "questions_used": self.questions_used,
            "total_questions": self.total_questions,
            "scorecard": self.scorecard.to_dict(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RoundEngineState":
        state = cls(
            phase_index=d.get("phase_index", 0),
            phase_question_count=d.get("phase_question_count", 0),
            current_difficulty=d.get("current_difficulty", "medium"),
            follow_up_depth=d.get("follow_up_depth", 0),
            current_topic=d.get("current_topic", ""),
            questions_used=d.get("questions_used", []),
            total_questions=d.get("total_questions", 0),
        )
        # Reconstruct scorecard
        sc_data = d.get("scorecard", {})
        if sc_data:
            state.scorecard.key_strengths = sc_data.get("key_strengths", [])
            state.scorecard.key_concerns = sc_data.get("key_concerns", [])
            state.scorecard.overall_impression = sc_data.get("overall_impression", "")
            for dim, v in sc_data.get("scores", {}).items():
                state.scorecard.scores[dim] = DimensionScore(
                    dimension=dim, score=v.get("score", 0),
                    evidence=v.get("evidence", []), question_count=v.get("question_count", 0),
                )
        return state


# ═══════════════════════════════════════════════════════
# THE ENGINE
# ═══════════════════════════════════════════════════════

class InterviewerEngine:
    """
    Dynamic behavioral engine for interview sub-agents.

    Personas are DYNAMIC (identity generated per candidate/company).
    Behaviors are SYSTEMATIC (phase machines, question banks, personality templates).
    """

    def __init__(self, llm: LLMClient, db: CareerDB, knowledge_db: KnowledgeDB):
        self.llm = llm
        self.db = db
        self.knowledge_db = knowledge_db
        # Per-session round states: (session_id, round_num) -> RoundEngineState
        self._states: Dict[Tuple[str, int], RoundEngineState] = {}

    def _get_state(self, session_id: str, round_num: int) -> RoundEngineState:
        key = (session_id, round_num)
        if key not in self._states:
            self._states[key] = RoundEngineState()
        return self._states[key]

    def _get_phases(self, round_type: str) -> List[dict]:
        return ROUND_PHASES.get(round_type, ROUND_PHASES["technical"])

    def _get_current_phase(self, state: RoundEngineState, round_type: str) -> dict:
        phases = self._get_phases(round_type)
        idx = min(state.phase_index, len(phases) - 1)
        return phases[idx]

    def _should_advance_phase(self, state: RoundEngineState, round_type: str) -> bool:
        phases = self._get_phases(round_type)
        if state.phase_index >= len(phases) - 1:
            return False  # Already on last phase
        current = phases[state.phase_index]
        return state.phase_question_count >= current["max_questions"]

    def _advance_phase(self, state: RoundEngineState, round_type: str) -> str:
        phases = self._get_phases(round_type)
        if state.phase_index < len(phases) - 1:
            state.phase_index += 1
            state.phase_question_count = 0
            state.follow_up_depth = 0
            return phases[state.phase_index]["name"]
        return phases[-1]["name"]

    def _adjust_difficulty(self, state: RoundEngineState, candidate_model: Optional[CandidateModel]):
        """Adjust difficulty based on candidate performance — find the ceiling."""
        if not candidate_model or len(candidate_model.depth_trajectory) < 2:
            return

        recent_depth = candidate_model.depth_trajectory[-1]
        current_idx = DIFFICULTY_LEVELS.index(state.current_difficulty)

        if recent_depth >= 0.75 and current_idx < len(DIFFICULTY_LEVELS) - 1:
            # Strong answer — escalate
            state.current_difficulty = DIFFICULTY_LEVELS[current_idx + 1]
        elif recent_depth < 0.3 and current_idx > 0:
            # Weak answer — note ceiling, step back
            state.current_difficulty = DIFFICULTY_LEVELS[current_idx - 1]
        # If 0.3-0.75, stay at current level

    def _select_bank_questions(
        self, state: RoundEngineState, round_type: str, phase_name: str,
        difficulty: str, count: int = 3, company: str = "",
    ) -> List[dict]:
        """Select questions from the hardcoded bank + KnowledgeDB."""
        bank = QUESTION_BANK.get(round_type, QUESTION_BANK["technical"])
        phase_questions = list(bank.get(phase_name, []))

        if not phase_questions:
            phase_questions = list(QUESTION_BANK["technical"].get(phase_name, []))

        # Merge company-specific questions from KnowledgeDB
        if self.knowledge_db and company:
            try:
                db_questions = self.knowledge_db.get_questions(
                    company=company, round_type=round_type, difficulty=difficulty,
                )
                for dbq in db_questions:
                    phase_questions.append({
                        "q": dbq["question_text"],
                        "difficulty": dbq["difficulty"],
                        "signal": dbq.get("topic", "general"),
                        "follow_up": bool(dbq.get("follow_ups")),
                    })
            except Exception as e:
                logger.debug("KnowledgeDB question lookup failed: %s", e)

        # Filter by difficulty (allow current and one level below)
        diff_idx = DIFFICULTY_LEVELS.index(difficulty) if difficulty in DIFFICULTY_LEVELS else 1
        allowed = set(DIFFICULTY_LEVELS[max(0, diff_idx - 1):diff_idx + 1])

        eligible = [
            q for q in phase_questions
            if q["difficulty"] in allowed and q["q"] not in state.questions_used
        ]

        if not eligible:
            eligible = [q for q in phase_questions if q["q"] not in state.questions_used]

        return random.sample(eligible, min(count, len(eligible))) if eligible else []

    def _fill_placeholders(self, question: str, profile_data: dict, candidate_model: Optional[CandidateModel]) -> str:
        """Fill {placeholders} in question templates with real candidate data."""
        skills = profile_data.get("skills", {})
        skill_list = list(skills.keys()) if isinstance(skills, dict) else skills if isinstance(skills, list) else []
        projects = profile_data.get("projects", [])
        project_names = [p.get("name", p) if isinstance(p, dict) else str(p) for p in projects[:3]]

        replacements = {
            "{candidate_name}": profile_data.get("name", "the candidate"),
            "{skill}": random.choice(skill_list) if skill_list else "your primary technology",
            "{project}": random.choice(project_names) if project_names else "your most recent project",
            "{company}": profile_data.get("target_company", "the company"),
            "{role}": profile_data.get("target_role", "this role"),
            "{topic}": random.choice(skill_list) if skill_list else "software engineering",
        }

        # Fill from candidate model
        if candidate_model:
            weak_areas = [k for k, v in candidate_model.knowledge_map.items() if v == "weak"]
            strong_areas = [k for k, v in candidate_model.knowledge_map.items() if v == "strong"]
            replacements["{weakness}"] = random.choice(weak_areas) if weak_areas else "areas for improvement"
            replacements["{claim}"] = random.choice(candidate_model.claims[-5:]) if candidate_model.claims else "your experience"

            if candidate_model.contradictions:
                replacements["{claim_1}"] = candidate_model.contradictions[-1]
            else:
                replacements["{claim_1}"] = "something earlier"

        for key, value in replacements.items():
            question = question.replace(key, str(value))

        # Clean up any remaining unfilled placeholders
        import re
        question = re.sub(r'\{[a-z_]+\}', 'that topic', question)

        return question

    def generate_opening(
        self,
        session_id: str,
        round_num: int,
        interviewer: InterviewerPersona,
        round_type: str,
        focus_areas: List[str],
        profile_data: dict,
        forum_digest: str = "",
        briefing_notes: str = "",
        candidate_model: Optional[CandidateModel] = None,
    ) -> str:
        """Generate the interviewer's opening for a round using the behavioral engine."""
        state = self._get_state(session_id, round_num)
        state.scorecard.init_dimensions(interviewer.eval_dimensions)

        phases = self._get_phases(round_type)
        phase = phases[0] if phases else {"name": "warmup", "goal": "Build rapport"}

        # Get personality behaviors
        personality = PERSONALITY_BEHAVIORS.get(
            interviewer.personality, PERSONALITY_BEHAVIORS["neutral"]
        )
        style_rules = QUESTIONING_STYLE_RULES.get(
            interviewer.question_style, QUESTIONING_STYLE_RULES["deep_dive"]
        )

        # Select warm-up questions from bank + KnowledgeDB
        company = profile_data.get("target_company", "")
        warmup_questions = self._select_bank_questions(state, round_type, phase["name"], "easy", 3, company=company)
        warmup_text = ""
        if warmup_questions:
            filled = [self._fill_placeholders(q["q"], profile_data, candidate_model) for q in warmup_questions]
            warmup_text = f"\n## Suggested Opening Questions (pick ONE, adapt to your personality)\n" + \
                          "\n".join(f"- {q}" for q in filled)

        # Candidate insights for rounds 2+
        candidate_insights = candidate_model.get_summary() if candidate_model and round_num > 1 else ""

        # HR/final round context
        hr_context = ""
        if round_type in ("hr", "hr_behavioral", "final") or (round_num > 1 and round_type == "behavioral"):
            company = profile_data.get("target_company", "")
            role = profile_data.get("target_role", "")
            hr_context = f"""
## Special Context for This Round
This is a {'FINAL' if round_type == 'final' else 'HR/behavioral'} round.
Company: {company} | Role: {role}
You should cover: behavioral scenarios, cultural fit, career goals, and salary expectations.
Address any red flags from the forum discussions."""

        prompt = f"""You are {interviewer.name} ({interviewer.role}), starting Round {round_num}.

## Your Personality
{personality['tone']}
Typical speech patterns: {', '.join(personality['sentence_starters'][:3])}

## Your Questioning Style
{style_rules}

## Your System Prompt
{interviewer.system_prompt}

## Round Structure
This round has {len(phases)} phases: {' -> '.join(p['name'] for p in phases)}
You are in phase: {phase['name']} — Goal: {phase['goal']}

## Focus Areas
{', '.join(focus_areas)}

{f'## Briefing Notes{chr(10)}{briefing_notes}' if briefing_notes else ''}

{f'## Forum Discussion (private — candidate cannot see this){chr(10)}{forum_digest}' if forum_digest else ''}

{f'## Candidate Assessment from Previous Rounds{chr(10)}{candidate_insights}' if candidate_insights else ''}

{hr_context}

## Candidate Info
Name: {profile_data.get('name', 'the candidate')}
Experience: {profile_data.get('experience_level', 'unknown')}
Domain: {profile_data.get('domain', 'unknown')}
{warmup_text}

---

Generate your opening. Include:
1. A brief introduction of yourself that matches your personality type ({interviewer.personality})
2. Set expectations for this round
3. Your FIRST question — pick from the suggested questions or create one that fits your style
{'4. Reference observations from the forum if they help frame your approach' if forum_digest else ''}

Keep it natural and conversational. 3-5 sentences. Speak in Indian English.
Your personality is {interviewer.personality} — make sure your tone matches."""

        system = f"""You are {interviewer.name}, {interviewer.role}.
Personality: {interviewer.personality} — {personality['tone']}
Speak naturally in Indian English. Be authentic to your personality type."""

        try:
            result = self.llm.generate(prompt=prompt, system_prompt=system, temperature=0.7)
            state.total_questions = 1
            state.phase_question_count = 1
            return result
        except Exception as e:
            logger.error(f"Opening generation failed: {e}")
            return f"Hello! I'm {interviewer.name}, {interviewer.role}. I'll be speaking with you for this round. Let's start — could you tell me about your most recent project?"

    def generate_question(
        self,
        session_id: str,
        round_num: int,
        interviewer: InterviewerPersona,
        round_type: str,
        focus_areas: List[str],
        round_transcript: str,
        profile_data: dict,
        questions_asked: int,
        max_questions: int,
        forum_digest: str = "",
        live_suggestions: str = "",
        candidate_model: Optional[CandidateModel] = None,
    ) -> str:
        """Generate the next question using the behavioral engine."""
        state = self._get_state(session_id, round_num)

        # Check phase transition
        if self._should_advance_phase(state, round_type):
            new_phase = self._advance_phase(state, round_type)
            logger.info(f"[{session_id}] R{round_num} phase advanced to: {new_phase}")

        # Adjust difficulty based on candidate performance
        self._adjust_difficulty(state, candidate_model)

        current_phase = self._get_current_phase(state, round_type)
        phases = self._get_phases(round_type)
        remaining = max_questions - questions_asked

        # Get personality + style behaviors
        personality = PERSONALITY_BEHAVIORS.get(
            interviewer.personality, PERSONALITY_BEHAVIORS["neutral"]
        )
        style_rules = QUESTIONING_STYLE_RULES.get(
            interviewer.question_style, QUESTIONING_STYLE_RULES["deep_dive"]
        )
        difficulty_rule = DIFFICULTY_RULES.get(
            state.current_difficulty, DIFFICULTY_RULES["medium"]
        )

        # Select questions from bank + KnowledgeDB for current phase
        company = profile_data.get("target_company", "")
        bank_questions = self._select_bank_questions(
            state, round_type, current_phase["name"], state.current_difficulty, 3, company=company
        )
        bank_text = ""
        if bank_questions:
            filled = [self._fill_placeholders(q["q"], profile_data, candidate_model) for q in bank_questions]
            bank_text = f"\n## Suggested Questions for This Phase (adapt to context, pick ONE or create your own)\n" + \
                        "\n".join(f"- {q}" for q in filled)

        # Candidate model insights
        candidate_insights = candidate_model.get_summary() if candidate_model else ""

        # Scorecard summary
        scorecard_summary = state.scorecard.get_summary()

        # Emotional state handling
        emotional_instructions = ""
        if candidate_model:
            emo = candidate_model.current_emotional_state
            if emo in ("nervous", "frustrated", "defensive"):
                emotional_instructions = f"\n## Emotional Read: Candidate seems {emo}\n{personality['when_weak']}"
            elif emo in ("confident", "enthusiastic"):
                emotional_instructions = f"\n## Emotional Read: Candidate seems {emo}\n{personality['when_strong']}"
            if candidate_model.evasion_count > 0 and candidate_model.emotional_arc[-1:] == ["evasive"]:
                emotional_instructions += f"\n{personality['when_evasive']}"

        prompt = f"""You are {interviewer.name} ({interviewer.role}).

## Your Personality
{personality['tone']}
Follow-up style: {personality['follow_up_style']}
{emotional_instructions}

## Your Questioning Style
{style_rules}

## Current Round State
Phase: {current_phase['name']} ({state.phase_index + 1}/{len(phases)}) — Goal: {current_phase['goal']}
Difficulty: {state.current_difficulty} — {difficulty_rule}
Questions asked: {questions_asked}/{max_questions} | Remaining: {remaining}
Follow-up depth: {state.follow_up_depth}/{state.max_follow_up_depth}

## Your Running Scorecard
{scorecard_summary}

## Focus Areas
{', '.join(focus_areas)}

{f'## Forum Insights (private){chr(10)}{forum_digest}' if forum_digest else ''}

{f'## Live Observer Notes{chr(10)}{live_suggestions}' if live_suggestions else ''}

{f'## Candidate Assessment{chr(10)}{candidate_insights}' if candidate_insights else ''}

{bank_text}

## Conversation So Far
{round_transcript}

---

Based on the conversation, generate your NEXT question. Follow these rules:

1. **Phase awareness**: You're in the '{current_phase['name']}' phase. {current_phase['goal']}
2. **Difficulty**: Current level is {state.current_difficulty}. {difficulty_rule}
3. **Follow-up vs new topic**: If follow_up_depth < {state.max_follow_up_depth} and the last answer was interesting/weak, follow up. Otherwise, move to a new topic.
4. **If EVASIVE**: Don't let them off the hook — rephrase and probe the same area
5. **If STRONG**: Push harder — escalate difficulty or go deeper
6. **If CONTRADICTION detected**: Address it directly but diplomatically
7. **Wrapping up**: If remaining <= 2, start closing with key final questions
8. **Stay in character**: Your personality is {interviewer.personality} — match the tone
9. **Ask ONE question only**. Reference specific things the candidate said.
10. **If colleagues suggested probing something in live notes, consider it**

Also analyze the last exchange and return scoring. Return JSON:
```json
{{
  "question": "your next question — ONE question only",
  "dimension_scores": {{
    "dimension_name": {{"score": 0-10, "evidence": "brief evidence from last answer"}}
  }},
  "strengths": ["specific strength from last answer"],
  "concerns": ["specific concern from last answer"],
  "follow_up_topic": "what you're probing — or empty string if new topic",
  "difficulty_assessment": "was last answer easy/medium/hard level?"
}}
```"""

        system = f"""You are {interviewer.name}, {interviewer.role}.
Personality: {interviewer.personality} — {personality['tone']}
Style: {interviewer.question_style}
Ask ONE question. Stay in character. Speak in Indian English. Return valid JSON."""

        try:
            result = self.llm.generate_json(prompt=prompt, system_prompt=system, temperature=0.7)

            question = result.get("question", "Could you elaborate on that?")

            # Update engine state
            state.total_questions += 1
            state.phase_question_count += 1

            # Track follow-up depth
            follow_up_topic = result.get("follow_up_topic", "")
            if follow_up_topic and follow_up_topic == state.current_topic:
                state.follow_up_depth += 1
            else:
                state.follow_up_depth = 0 if not follow_up_topic else 1
                state.current_topic = follow_up_topic or ""

            # Track used questions
            state.questions_used.append(question[:100])

            # Update scorecard
            state.scorecard.update_from_analysis(result)

            return question

        except Exception as e:
            logger.error(f"Question generation failed: {e}")
            state.total_questions += 1
            state.phase_question_count += 1
            return "That's interesting. Could you elaborate on that point a bit more?"

    def get_scorecard(self, session_id: str, round_num: int) -> dict:
        """Get the running scorecard for a specific round."""
        state = self._get_state(session_id, round_num)
        return state.scorecard.to_dict()

    def get_engine_state(self, session_id: str, round_num: int) -> dict:
        """Get the full engine state for debugging/persistence."""
        state = self._get_state(session_id, round_num)
        return state.to_dict()

    def set_engine_state(self, session_id: str, round_num: int, state_dict: dict):
        """Restore engine state from a dict (for session resumption)."""
        self._states[(session_id, round_num)] = RoundEngineState.from_dict(state_dict)
