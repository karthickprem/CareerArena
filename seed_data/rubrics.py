"""
Evaluation rubrics for the PlaceRight AI interview platform.

13 dimensions x 3 levels (fresher / mid / senior) = 39 rubrics.
Calibrated for Indian engineering campus placement and early-career hiring.
"""

from typing import List, Dict


def get_rubrics() -> List[Dict]:
    """Return the full list of 39 evaluation rubrics."""
    return [
        # ──────────────────────────────────────────────
        # 1. COMMUNICATION
        # ──────────────────────────────────────────────
        {
            "dimension": "communication",
            "level": "fresher",
            "score_1_2": (
                "Struggles to form coherent sentences in English or any "
                "chosen language. Gives one-word answers, long awkward "
                "silences, or mumbles inaudibly. Cannot explain even a "
                "final-year project without losing the thread."
            ),
            "score_3_4": (
                "Can speak in complete sentences but frequently pauses to "
                "search for words. Mixes tenses and skips connectors, making "
                "the narrative hard to follow. Gives vague answers like "
                "'I did many things in my project' without specifics."
            ),
            "score_5_6": (
                "Communicates ideas adequately but in a flat, unstructured "
                "way. Can describe a project or concept when prompted but "
                "rarely volunteers context. Occasional grammatical slips "
                "that do not block understanding."
            ),
            "score_7_8": (
                "Speaks clearly and organises answers with a beginning, "
                "middle, and end. Uses concrete examples from coursework or "
                "internships. Adjusts explanation depth when asked to "
                "simplify or elaborate. Maintains eye contact and steady pace."
            ),
            "score_9_10": (
                "Articulate and engaging. Structures answers using frameworks "
                "(STAR, situation-action-result) without being prompted. "
                "Handles technical jargon and layperson language with equal "
                "ease. Asks clarifying questions that show active listening."
            ),
            "key_indicators": [
                "Sentence completeness and logical flow",
                "Use of concrete examples vs vague generalities",
                "Ability to adjust explanation depth on request",
                "Active listening cues — paraphrasing the question before answering",
                "Appropriate pace — neither rushing nor dragging",
            ],
            "red_flags": [
                "Memorised script delivered verbatim regardless of the question",
                "Refusing to answer in English when the role demands it",
                "Interrupting the interviewer repeatedly",
                "Using filler words ('basically', 'actually') in every sentence",
            ],
        },
        {
            "dimension": "communication",
            "level": "mid",
            "score_1_2": (
                "Cannot articulate what they have been doing for the last "
                "2-4 years of work experience. Responses are disjointed and "
                "lack any narrative about impact or ownership."
            ),
            "score_3_4": (
                "Describes day-to-day tasks but cannot connect them to "
                "business outcomes. Struggles to explain technical decisions "
                "to a non-technical audience. Often says 'we did' without "
                "clarifying personal contribution."
            ),
            "score_5_6": (
                "Communicates clearly about familiar topics but becomes "
                "vague when discussing cross-functional work or stakeholder "
                "management. Can present a decent walkthrough of past work "
                "if given time to prepare."
            ),
            "score_7_8": (
                "Tells a compelling story about projects — covers context, "
                "their role, technical choices, trade-offs, and measurable "
                "outcomes. Comfortable switching between technical depth and "
                "executive summary. Writes clear documentation."
            ),
            "score_9_10": (
                "Exceptional communicator who can influence decisions in "
                "meetings, write persuasive design docs, and present to "
                "clients or leadership. Tailors message precisely to the "
                "audience. Handles tough questions with composure and clarity."
            ),
            "key_indicators": [
                "Ability to separate personal contribution from team effort",
                "Clarity when explaining trade-offs and technical decisions",
                "Comfort presenting to non-technical stakeholders",
                "Written communication quality (docs, emails, PRs)",
            ],
            "red_flags": [
                "Cannot name a single measurable outcome from past projects",
                "Blames team or management for communication failures",
                "Over-uses jargon to mask shallow understanding",
            ],
        },
        {
            "dimension": "communication",
            "level": "senior",
            "score_1_2": (
                "Despite years of experience, cannot convey architectural "
                "decisions or strategy clearly. Answers are rambling and "
                "disorganised. Would struggle to represent the team in "
                "a client call or leadership review."
            ),
            "score_3_4": (
                "Can communicate within their immediate team but falters "
                "when addressing cross-org audiences. Avoids writing RFCs "
                "or design documents. Delegates presentation work to others."
            ),
            "score_5_6": (
                "Solid one-on-one communicator. Can run team stand-ups and "
                "sprint reviews competently. Occasionally loses the room "
                "during longer presentations or when challenged on details."
            ),
            "score_7_8": (
                "Strong communicator who can align multiple teams around a "
                "technical vision. Writes influential design docs, mentors "
                "juniors on communication, and handles escalations with "
                "diplomacy. Comfortable in CXO-level discussions."
            ),
            "score_9_10": (
                "Thought-leader level communicator. Drives org-wide alignment "
                "through clear vision statements, blogs, or tech talks. "
                "Navigates ambiguous political situations with nuance. "
                "Represents the company externally at conferences or with "
                "enterprise clients."
            ),
            "key_indicators": [
                "Quality and influence of written artifacts (RFCs, ADRs)",
                "Ability to align cross-functional teams verbally",
                "Mentoring others on communication skills",
                "Executive presence in high-stakes meetings",
            ],
            "red_flags": [
                "Avoids documentation and relies solely on verbal communication",
                "Cannot simplify complex architecture for non-engineers",
                "Dismissive tone when juniors ask questions",
            ],
        },

        # ──────────────────────────────────────────────
        # 2. TECHNICAL DEPTH
        # ──────────────────────────────────────────────
        {
            "dimension": "technical_depth",
            "level": "fresher",
            "score_1_2": (
                "Cannot explain basic data structures (arrays, linked lists) "
                "or write a simple loop. Appears to have no hands-on coding "
                "experience despite listing projects on the resume."
            ),
            "score_3_4": (
                "Knows textbook definitions but cannot apply them. For "
                "example, can define a stack but cannot use one to solve "
                "a bracket-matching problem. Code has syntax errors and "
                "no edge-case handling."
            ),
            "score_5_6": (
                "Can solve straightforward DSA problems (two-pointer, basic "
                "recursion) with some guidance. Understands OOP concepts and "
                "can write working code for simple CRUD features. Knows one "
                "language reasonably well."
            ),
            "score_7_8": (
                "Solves medium-level coding problems independently with "
                "clean, readable code. Understands time/space complexity "
                "and can optimise brute-force solutions. Has built at least "
                "one non-trivial project (e.g., a full-stack app, ML model, "
                "or embedded system) and can explain design decisions."
            ),
            "score_9_10": (
                "Solves hard-level problems and can discuss multiple "
                "approaches with trade-offs. Deep understanding of at least "
                "one domain (systems, ML, web, mobile). Has contributed to "
                "open source or built products used by real users. Code "
                "quality rivals that of a working professional."
            ),
            "key_indicators": [
                "Ability to write compilable, correct code on a whiteboard or editor",
                "Understanding of time and space complexity",
                "Depth of final-year project — toy demo vs real system",
                "Familiarity with version control, testing, deployment basics",
            ],
            "red_flags": [
                "Cannot write a for-loop or function definition",
                "Claims projects on resume but cannot explain any code from them",
                "Zero awareness of how software is built beyond college labs",
            ],
        },
        {
            "dimension": "technical_depth",
            "level": "mid",
            "score_1_2": (
                "Despite 2-4 years of experience, cannot explain the "
                "architecture of systems they have worked on. Struggles with "
                "basic debugging and has no understanding of system design "
                "fundamentals."
            ),
            "score_3_4": (
                "Can complete assigned tickets but has never designed a "
                "feature end-to-end. Limited understanding of the tech stack "
                "beyond the immediate layer they work in. Cannot discuss "
                "database indexing, caching, or API design with confidence."
            ),
            "score_5_6": (
                "Competent in their primary stack. Can design a simple "
                "feature with appropriate data models, APIs, and basic error "
                "handling. Understands common patterns (MVC, repository, "
                "pub-sub) but may not know when to deviate from them."
            ),
            "score_7_8": (
                "Designs features considering scalability, failure modes, "
                "and observability. Can articulate trade-offs between SQL "
                "and NoSQL, monolith and microservices, sync and async. Has "
                "experience with CI/CD, containerisation, and at least one "
                "cloud provider."
            ),
            "score_9_10": (
                "Deep expertise in their domain with breadth across "
                "adjacent areas. Can design systems handling millions of "
                "requests. Understands distributed systems concepts "
                "(CAP theorem, consensus, partitioning). Actively improves "
                "team practices — code review standards, testing strategy."
            ),
            "key_indicators": [
                "Ability to draw and explain the architecture of a past system",
                "Understanding of non-functional requirements (latency, throughput)",
                "Experience with production incidents and debugging",
                "Code review quality and mentoring of juniors",
            ],
            "red_flags": [
                "Has never read or contributed to system design discussions",
                "Cannot explain why a particular database or framework was chosen",
                "No experience with production environments or deployments",
            ],
        },
        {
            "dimension": "technical_depth",
            "level": "senior",
            "score_1_2": (
                "Cannot architect a system beyond basic CRUD. Has stayed "
                "in a narrow role for years without growing. Unable to "
                "evaluate technology choices or mentor others technically."
            ),
            "score_3_4": (
                "Knows their specific stack deeply but lacks breadth. Cannot "
                "discuss trade-offs across paradigms (event-driven vs "
                "request-response, relational vs graph). Has not led any "
                "significant technical initiative."
            ),
            "score_5_6": (
                "Can design moderately complex systems and has led small "
                "teams technically. Understands security, compliance, and "
                "operational concerns. May lack depth in newer areas like "
                "ML ops, edge computing, or platform engineering."
            ),
            "score_7_8": (
                "Designs systems that are resilient, cost-effective, and "
                "maintainable. Has driven major migrations, re-architectures, "
                "or platform builds. Sets technical direction for a team or "
                "squad. Deep expertise in at least two domains."
            ),
            "score_9_10": (
                "Industry-recognised expertise. Designs systems used by "
                "millions. Can evaluate emerging technologies and make "
                "build-vs-buy decisions with strong business reasoning. "
                "Creates internal frameworks or tools adopted org-wide. "
                "Publishes or speaks on technical topics."
            ),
            "key_indicators": [
                "Ability to make and justify build-vs-buy decisions",
                "Track record of successful large-scale technical initiatives",
                "Breadth across infrastructure, application, and data layers",
                "Influence on org-wide engineering standards",
            ],
            "red_flags": [
                "No evidence of technical leadership or mentorship",
                "Relies on a single technology and resists alternatives",
                "Cannot estimate system capacity or cost",
            ],
        },

        # ──────────────────────────────────────────────
        # 3. PROBLEM SOLVING
        # ──────────────────────────────────────────────
        {
            "dimension": "problem_solving",
            "level": "fresher",
            "score_1_2": (
                "Freezes when given an unfamiliar problem. Cannot break it "
                "into smaller parts or identify what is being asked. Jumps "
                "to random code without thinking."
            ),
            "score_3_4": (
                "Understands the problem statement after clarification but "
                "cannot devise a plan. Tries to recall a memorised solution "
                "rather than reasoning from first principles. Gives up "
                "quickly when the first approach fails."
            ),
            "score_5_6": (
                "Can decompose a problem into sub-problems with some "
                "guidance. Identifies brute-force approaches and, when "
                "nudged, thinks about optimisation. Uses examples and test "
                "cases to validate thinking."
            ),
            "score_7_8": (
                "Breaks down problems methodically — clarifies constraints, "
                "identifies patterns, considers edge cases before coding. "
                "Can pivot to a new approach when the current one hits a "
                "wall. Thinks aloud clearly so the interviewer can follow."
            ),
            "score_9_10": (
                "Tackles novel problems with structured creativity. "
                "Identifies multiple solution strategies, compares them on "
                "complexity and feasibility, and chooses the best one with "
                "reasoning. Catches tricky edge cases proactively. "
                "Demonstrates strong intuition built from practice."
            ),
            "key_indicators": [
                "Asks clarifying questions before diving in",
                "Uses examples and dry runs to test logic",
                "Recovers gracefully when an approach fails",
                "Thinks aloud in a structured way",
            ],
            "red_flags": [
                "Starts coding without understanding the problem",
                "Cannot handle any deviation from textbook problems",
                "Claims 'I know this problem' but produces wrong solution",
            ],
        },
        {
            "dimension": "problem_solving",
            "level": "mid",
            "score_1_2": (
                "Cannot troubleshoot a production issue even with logs and "
                "metrics available. Waits for someone else to diagnose. "
                "No systematic approach to debugging."
            ),
            "score_3_4": (
                "Can fix bugs when pointed to the right file but struggles "
                "to trace issues across services or layers. Does not use "
                "logs, metrics, or profiling tools effectively."
            ),
            "score_5_6": (
                "Follows a reasonable debugging process — reproduces the "
                "issue, checks logs, narrows down the cause. Can solve "
                "within-service problems independently but needs help with "
                "cross-service or infrastructure issues."
            ),
            "score_7_8": (
                "Approaches ambiguous problems with structured hypotheses. "
                "Can trace an issue from the frontend through APIs, queues, "
                "and databases. Proposes both short-term fixes and long-term "
                "prevention strategies. Uses data to validate root cause."
            ),
            "score_9_10": (
                "Exceptional at navigating ambiguity. Can diagnose complex "
                "production incidents under pressure, coordinate with "
                "multiple teams, and drive resolution. Builds tools or "
                "runbooks that prevent recurrence. Thinks in systems, "
                "not just components."
            ),
            "key_indicators": [
                "Structured debugging methodology",
                "Ability to trace issues across system boundaries",
                "Distinguishing symptoms from root causes",
                "Proposing preventive measures, not just fixes",
            ],
            "red_flags": [
                "Only solution is 'restart the server'",
                "Blames other teams without evidence",
                "No curiosity about why something failed",
            ],
        },
        {
            "dimension": "problem_solving",
            "level": "senior",
            "score_1_2": (
                "Cannot frame or scope complex, ambiguous problems. Jumps "
                "to solutions without understanding constraints. Has never "
                "driven resolution of a critical incident independently."
            ),
            "score_3_4": (
                "Can solve well-defined problems but struggles when "
                "requirements are ambiguous or conflicting. Does not "
                "proactively identify problems — only reacts when they "
                "are reported."
            ),
            "score_5_6": (
                "Identifies and solves problems within their domain. Can "
                "lead incident response for familiar failure modes. "
                "Occasionally misses systemic issues because they focus "
                "on symptoms."
            ),
            "score_7_8": (
                "Frames complex, cross-cutting problems clearly. Identifies "
                "root causes of organisational or architectural issues and "
                "proposes systemic fixes. Balances short-term pragmatism "
                "with long-term correctness. Coaches others through their "
                "problem-solving process."
            ),
            "score_9_10": (
                "Anticipates problems before they manifest — through "
                "architecture reviews, chaos engineering, or trend analysis. "
                "Turns incidents into learning opportunities for the org. "
                "Can navigate problems that span technical, people, and "
                "process dimensions simultaneously."
            ),
            "key_indicators": [
                "Track record of resolving high-severity incidents",
                "Ability to scope and frame ambiguous problems",
                "Proactive identification of systemic risks",
                "Coaching others on problem-solving methodology",
            ],
            "red_flags": [
                "Avoids ambiguity — only works on well-scoped tickets",
                "No examples of proactive problem identification",
                "Relies on heroics rather than systematic approaches",
            ],
        },

        # ──────────────────────────────────────────────
        # 4. LEADERSHIP
        # ──────────────────────────────────────────────
        {
            "dimension": "leadership",
            "level": "fresher",
            "score_1_2": (
                "No evidence of taking initiative in any context — academic, "
                "extracurricular, or personal. Always waited for instructions "
                "from professors or team leads."
            ),
            "score_3_4": (
                "Participated in group activities but never took ownership. "
                "Was part of a team for a college fest or project but cannot "
                "describe any decision they personally drove."
            ),
            "score_5_6": (
                "Led a small team in a college project, club, or hackathon. "
                "Can describe how they divided work and coordinated "
                "deliverables. May struggle to articulate conflict resolution "
                "or how they handled an underperforming teammate."
            ),
            "score_7_8": (
                "Took visible leadership roles — technical club secretary, "
                "hackathon team lead, or open-source maintainer. Can "
                "describe specific situations where they influenced "
                "peers, resolved disagreements, or stepped up when "
                "things went wrong."
            ),
            "score_9_10": (
                "Demonstrated exceptional initiative — founded a college "
                "chapter, organised a large event, or led a startup attempt. "
                "Shows maturity beyond their years in how they describe "
                "motivating others, making tough calls, and taking "
                "accountability for failures."
            ),
            "key_indicators": [
                "Specific examples of influencing peers without authority",
                "Ownership during group projects — did they drive or drift?",
                "Response to failure or conflict in team settings",
                "Initiative beyond what was required by the curriculum",
            ],
            "red_flags": [
                "Claims leadership but describes only individual work",
                "Cannot name a single situation where they influenced others",
                "Takes credit for team outcomes without acknowledging peers",
            ],
        },
        {
            "dimension": "leadership",
            "level": "mid",
            "score_1_2": (
                "After 2-4 years, has never mentored a junior, led a "
                "feature, or taken ownership beyond assigned tasks. "
                "Purely an individual contributor with no influence."
            ),
            "score_3_4": (
                "Has informally helped new joiners but never owned a "
                "mentoring relationship. Can lead a feature if the scope "
                "is fully defined but does not shape requirements or "
                "push back on unreasonable timelines."
            ),
            "score_5_6": (
                "Mentors 1-2 juniors and can lead a small feature "
                "end-to-end. Participates in hiring interviews. Speaks "
                "up in team discussions but does not consistently drive "
                "decisions."
            ),
            "score_7_8": (
                "Owns a significant area of the product or codebase. "
                "Actively shapes technical direction within the team. "
                "Mentors juniors with structured feedback and growth plans. "
                "Can run sprint planning and retrospectives effectively."
            ),
            "score_9_10": (
                "Recognised as a go-to person across teams. Drives "
                "initiatives that improve engineering culture — better "
                "testing, documentation, on-call processes. Influences "
                "product decisions with data-backed arguments. Ready to "
                "step into a formal tech lead role."
            ),
            "key_indicators": [
                "Scope of ownership — task-level vs feature-level vs area-level",
                "Quality and impact of mentoring relationships",
                "Ability to influence without formal authority",
                "Proactive improvement of team processes",
            ],
            "red_flags": [
                "No evidence of helping anyone grow",
                "Avoids responsibility for outcomes beyond their code",
                "Passive in team discussions and planning",
            ],
        },
        {
            "dimension": "leadership",
            "level": "senior",
            "score_1_2": (
                "Senior by title only. Has never set direction for a team "
                "or project. Cannot articulate a vision or inspire others. "
                "Avoids difficult conversations."
            ),
            "score_3_4": (
                "Manages tasks and timelines but does not lead people. "
                "Team members do not look to them for guidance or "
                "inspiration. Avoids organisational politics entirely "
                "rather than navigating them constructively."
            ),
            "score_5_6": (
                "Leads a team competently — runs meetings, tracks progress, "
                "handles escalations. Developing the ability to give "
                "difficult feedback and make unpopular decisions. "
                "Respected within the immediate team."
            ),
            "score_7_8": (
                "Sets technical vision for a team or domain. Develops "
                "engineers through stretch assignments and candid feedback. "
                "Navigates organisational complexity to get things done. "
                "Balances individual contribution with multiplying the "
                "team's output."
            ),
            "score_9_10": (
                "Organisational leader who shapes culture and standards "
                "beyond their immediate team. Builds high-performing teams "
                "from scratch. Makes difficult people decisions with empathy "
                "and clarity. Known for developing others into leaders. "
                "Trusted by leadership for strategic input."
            ),
            "key_indicators": [
                "Track record of building and growing teams",
                "Ability to set and communicate a compelling vision",
                "Handling of difficult conversations and decisions",
                "Influence beyond the immediate team",
            ],
            "red_flags": [
                "Micromanages instead of delegating",
                "Takes credit for team achievements",
                "Avoids giving constructive feedback to avoid conflict",
                "No succession planning — single point of failure",
            ],
        },

        # ──────────────────────────────────────────────
        # 5. DOMAIN KNOWLEDGE
        # ──────────────────────────────────────────────
        {
            "dimension": "domain_knowledge",
            "level": "fresher",
            "score_1_2": (
                "No awareness of the industry or domain the company "
                "operates in. Has not researched the company's products, "
                "customers, or market. Cannot connect any coursework to "
                "real-world applications."
            ),
            "score_3_4": (
                "Has a surface-level understanding — knows the company "
                "name and vaguely what it does. Cannot discuss industry "
                "trends, competitors, or how technology applies to the "
                "business domain."
            ),
            "score_5_6": (
                "Has done basic research — can name the company's main "
                "products and target customers. Connects some coursework "
                "(e.g., DBMS to fintech, networking to cloud) to the "
                "domain. Awareness is bookish rather than practical."
            ),
            "score_7_8": (
                "Demonstrates genuine interest in the domain — has tried "
                "the product, read industry blogs, or completed relevant "
                "MOOCs. Can discuss how technology solves real problems "
                "in the space. Asks thoughtful questions about the company's "
                "technical challenges."
            ),
            "score_9_10": (
                "Deep domain awareness unusual for a fresher. May have "
                "done an internship or personal project in the space. "
                "Understands regulatory, competitive, and user-experience "
                "dimensions of the domain. Can articulate why they are "
                "specifically excited about this industry."
            ),
            "key_indicators": [
                "Pre-interview research on the company and domain",
                "Ability to connect academic concepts to industry problems",
                "Genuine curiosity demonstrated through questions asked",
                "Relevant side projects, internships, or coursework",
            ],
            "red_flags": [
                "Cannot name what the company does",
                "Zero interest in the domain — applying purely for the package",
                "Confuses the company with a competitor",
            ],
        },
        {
            "dimension": "domain_knowledge",
            "level": "mid",
            "score_1_2": (
                "Has worked in the domain for years but cannot explain "
                "basic business concepts, user personas, or regulatory "
                "requirements relevant to their work."
            ),
            "score_3_4": (
                "Understands the immediate technical context but not the "
                "broader business landscape. Cannot explain how their "
                "feature impacts revenue, user retention, or compliance."
            ),
            "score_5_6": (
                "Solid understanding of the domain they have worked in. "
                "Knows key metrics, user workflows, and common pain points. "
                "May lack cross-domain perspective if switching industries."
            ),
            "score_7_8": (
                "Deep domain expertise — understands regulatory constraints, "
                "competitive landscape, and user behaviour patterns. Can "
                "translate domain requirements into technical specifications. "
                "Stays current with industry developments."
            ),
            "score_9_10": (
                "Recognised domain expert within their organisation. "
                "Product managers seek their input on feasibility and "
                "strategy. Can identify opportunities that others miss "
                "because they understand both the technology and the market."
            ),
            "key_indicators": [
                "Ability to explain business impact of technical decisions",
                "Awareness of regulatory and compliance considerations",
                "Understanding of user personas and workflows",
                "Engagement with industry community (meetups, publications)",
            ],
            "red_flags": [
                "Treats domain knowledge as 'not my job'",
                "Cannot name the company's key metrics or KPIs",
                "No curiosity about why features are built, only how",
            ],
        },
        {
            "dimension": "domain_knowledge",
            "level": "senior",
            "score_1_2": (
                "Despite seniority, has a shallow understanding of the "
                "business domain. Makes technical decisions without "
                "considering regulatory, market, or user-experience "
                "implications."
            ),
            "score_3_4": (
                "Knows the domain at a practitioner level but cannot "
                "contribute to strategic discussions. Does not anticipate "
                "how market shifts might affect technical architecture."
            ),
            "score_5_6": (
                "Strong domain knowledge for their current company or "
                "vertical. Can participate in product strategy discussions. "
                "May struggle to transfer knowledge if the target role is "
                "in a different vertical."
            ),
            "score_7_8": (
                "Industry-level domain expertise. Shapes product roadmaps "
                "with insights from deep domain understanding. Anticipates "
                "regulatory changes and prepares the platform accordingly. "
                "Bridges the gap between engineering and business leadership."
            ),
            "score_9_10": (
                "Thought leader in the domain. Influences industry "
                "standards, speaks at domain conferences, or advises "
                "leadership on market strategy. Can evaluate M&A targets "
                "or partnership opportunities from a technical-domain "
                "perspective."
            ),
            "key_indicators": [
                "Contribution to product strategy and roadmap",
                "Anticipation of regulatory or market changes",
                "Ability to evaluate business opportunities technically",
                "Cross-vertical knowledge and pattern recognition",
            ],
            "red_flags": [
                "Ignores domain context in technical decisions",
                "Cannot explain the business model to a new engineer",
                "No engagement with industry trends or community",
            ],
        },

        # ──────────────────────────────────────────────
        # 6. CONFIDENCE
        # ──────────────────────────────────────────────
        {
            "dimension": "confidence",
            "level": "fresher",
            "score_1_2": (
                "Extremely nervous — shaking voice, no eye contact, "
                "apologises before every answer. Says 'I don't know' even "
                "for topics they have studied. Appears to have no belief "
                "in their own preparation."
            ),
            "score_3_4": (
                "Visibly anxious but manages to answer some questions. "
                "Frequently second-guesses correct answers. Looks for "
                "validation after every statement ('Is that right?'). "
                "Body language is closed and defensive."
            ),
            "score_5_6": (
                "Moderate confidence — comfortable with familiar topics "
                "but becomes hesitant with unfamiliar ones. Can maintain "
                "composure but does not project conviction. Answers feel "
                "safe rather than bold."
            ),
            "score_7_8": (
                "Projects calm confidence without arrogance. Admits when "
                "they do not know something and pivots constructively. "
                "Defends their technical choices with reasoning when "
                "challenged. Maintains composure even when a question is "
                "unexpectedly hard."
            ),
            "score_9_10": (
                "Naturally self-assured. Takes challenging questions as "
                "opportunities to demonstrate thinking rather than threats. "
                "Handles pushback gracefully by saying 'That is a good "
                "point, let me reconsider' without crumbling. Confidence "
                "is grounded in preparation and self-awareness."
            ),
            "key_indicators": [
                "Steady voice and open body language",
                "Willingness to say 'I don't know, but here's how I'd find out'",
                "Defending answers when challenged rather than immediately folding",
                "Absence of excessive hedging or apologising",
            ],
            "red_flags": [
                "Overconfidence — dismisses questions or argues rudely",
                "Fabricates answers rather than admitting ignorance",
                "Confidence collapses at the first tough question",
            ],
        },
        {
            "dimension": "confidence",
            "level": "mid",
            "score_1_2": (
                "Despite experience, appears unsure about their own skills "
                "and decisions. Cannot advocate for their ideas in meetings. "
                "Defers to others even on topics they know well."
            ),
            "score_3_4": (
                "Confident in routine situations but rattled by unexpected "
                "questions or senior stakeholders. Tends to over-qualify "
                "statements ('I think maybe it could be...'). Avoids "
                "presenting work to larger groups."
            ),
            "score_5_6": (
                "Comfortable in day-to-day interactions. Can present their "
                "work to the team and handle standard questions. May "
                "hesitate when challenged by senior engineers or when "
                "discussing areas outside their expertise."
            ),
            "score_7_8": (
                "Confidently navigates technical discussions with peers and "
                "senior engineers. Pushes back on bad ideas respectfully. "
                "Comfortable saying 'I need to investigate further' without "
                "losing credibility. Presents to cross-functional audiences "
                "with ease."
            ),
            "score_9_10": (
                "Inspires confidence in others. Stakeholders trust their "
                "estimates and technical judgments. Handles high-pressure "
                "situations (production incidents, client escalations) with "
                "calm authority. Balances confidence with humility "
                "seamlessly."
            ),
            "key_indicators": [
                "Ability to push back constructively on bad ideas",
                "Comfort with uncertainty — can act without complete information",
                "Consistency of confidence across audiences and situations",
                "Handling of being wrong — graceful course-correction",
            ],
            "red_flags": [
                "Aggressive when challenged — conflates confidence with dominance",
                "Never admits mistakes or changes position",
                "Confidence varies wildly based on audience seniority",
            ],
        },
        {
            "dimension": "confidence",
            "level": "senior",
            "score_1_2": (
                "Lacks the conviction expected at their level. Cannot make "
                "decisions without extensive validation from others. Would "
                "not inspire confidence in a team they are supposed to lead."
            ),
            "score_3_4": (
                "Confident in their technical niche but visibly "
                "uncomfortable in leadership situations — org-level "
                "presentations, cross-team negotiations, or strategy "
                "discussions."
            ),
            "score_5_6": (
                "Competent and composed in most situations. Can make "
                "decisions and stand by them. Occasionally hesitates on "
                "high-stakes calls where the data is ambiguous."
            ),
            "score_7_8": (
                "Radiates quiet confidence. Makes difficult decisions with "
                "incomplete information and owns the outcomes. Comfortable "
                "challenging leadership respectfully. Others look to them "
                "for stability during crises."
            ),
            "score_9_10": (
                "Executive-level presence. Can walk into a room of VPs, "
                "present a controversial technical strategy, and win buy-in "
                "through calm, evidence-based conviction. Confidence is "
                "contagious — elevates the confidence of everyone around "
                "them."
            ),
            "key_indicators": [
                "Decision-making velocity under uncertainty",
                "Owning outcomes — not deflecting blame when things go wrong",
                "Comfort with executive and board-level audiences",
                "Ability to project calm during crises",
            ],
            "red_flags": [
                "Arrogance masquerading as confidence",
                "Cannot make a call without consensus",
                "Loses composure when plans go sideways",
            ],
        },

        # ──────────────────────────────────────────────
        # 7. STRUCTURED THINKING
        # ──────────────────────────────────────────────
        {
            "dimension": "structured_thinking",
            "level": "fresher",
            "score_1_2": (
                "Answers are stream-of-consciousness with no logical "
                "structure. Jumps between topics mid-sentence. Cannot "
                "organise thoughts even when given time."
            ),
            "score_3_4": (
                "Shows some attempt at structure but loses it under "
                "pressure. Might list 'firstly' and 'secondly' but the "
                "points themselves are unrelated or overlapping. Cannot "
                "summarise a complex topic concisely."
            ),
            "score_5_6": (
                "Can provide structured answers for rehearsed topics "
                "(tell me about yourself, describe your project). Structure "
                "breaks down for unexpected or analytical questions. Uses "
                "simple frameworks when prompted."
            ),
            "score_7_8": (
                "Naturally organises answers into clear segments. When "
                "asked a complex question, takes a moment to think, then "
                "delivers a structured response. Can break down a vague "
                "problem into components without being told to. Uses "
                "mental models from coursework or reading."
            ),
            "score_9_10": (
                "Exceptionally organised thinker. Applies frameworks "
                "(MECE, first-principles, cost-benefit) naturally. Can "
                "take a sprawling, ambiguous question and restructure it "
                "into a clear decision tree. Impressive for someone "
                "without professional experience."
            ),
            "key_indicators": [
                "Pausing to organise thoughts before speaking",
                "Using numbered points or categories unprompted",
                "Ability to summarise a long discussion in 2-3 sentences",
                "Recognising when a question has multiple parts and addressing each",
            ],
            "red_flags": [
                "Contradicts themselves within the same answer",
                "Cannot summarise their own project in under 60 seconds",
                "Answers wander without reaching a conclusion",
            ],
        },
        {
            "dimension": "structured_thinking",
            "level": "mid",
            "score_1_2": (
                "Cannot present a coherent status update or project "
                "proposal. Meetings they run are disorganised and "
                "inconclusive. Written communication (emails, docs) "
                "is rambling."
            ),
            "score_3_4": (
                "Can follow a template or agenda but cannot create "
                "structure for a novel situation. Design documents are "
                "incomplete or jump between abstraction levels "
                "inconsistently."
            ),
            "score_5_6": (
                "Produces reasonably structured design docs and proposals. "
                "Can break features into stories and tasks. May over-index "
                "on detail for simple problems or under-specify complex ones."
            ),
            "score_7_8": (
                "Thinks in systems — can decompose a problem across "
                "multiple dimensions (technical, operational, business). "
                "Writes clear, structured documents that others can act on. "
                "Facilitates meetings that reach decisions."
            ),
            "score_9_10": (
                "Master of structure. Can take a chaotic situation — "
                "unclear requirements, competing priorities, incomplete "
                "data — and create a clear plan with dependencies, risks, "
                "and milestones. Documents they write become templates "
                "others follow."
            ),
            "key_indicators": [
                "Quality of written artifacts (design docs, project plans)",
                "Ability to facilitate meetings towards decisions",
                "Decomposition of features into well-scoped work items",
                "Consistent structure across different communication contexts",
            ],
            "red_flags": [
                "Meetings they run are unfocused and inconclusive",
                "Cannot write a one-page summary of a complex project",
                "Misses critical dimensions when analysing problems",
            ],
        },
        {
            "dimension": "structured_thinking",
            "level": "senior",
            "score_1_2": (
                "Cannot create clarity from ambiguity. Strategic "
                "discussions they lead go in circles. Unable to synthesise "
                "inputs from multiple stakeholders into a coherent plan."
            ),
            "score_3_4": (
                "Structures well-defined problems competently but struggles "
                "with open-ended strategic questions. Cannot create a "
                "roadmap that balances competing priorities across teams."
            ),
            "score_5_6": (
                "Produces solid technical strategies and project plans "
                "within their domain. Can structure cross-team initiatives "
                "with guidance. Occasionally misses second-order effects "
                "or external dependencies."
            ),
            "score_7_8": (
                "Creates frameworks that others adopt — decision matrices, "
                "evaluation criteria, risk assessment models. Can structure "
                "a multi-quarter initiative spanning multiple teams with "
                "clear milestones, dependencies, and decision points."
            ),
            "score_9_10": (
                "Brings order to organisational chaos. Can take a "
                "company-wide technical challenge and structure it into "
                "a phased strategy with clear ownership, success metrics, "
                "and contingency plans. Thinking is both broad and precise."
            ),
            "key_indicators": [
                "Ability to create frameworks adopted by others",
                "Synthesis of cross-functional inputs into actionable plans",
                "Balancing multiple competing priorities with clear rationale",
                "Quality of strategic roadmaps and multi-quarter plans",
            ],
            "red_flags": [
                "Produces plans that are too abstract to act on",
                "Cannot prioritise — everything is equally important",
                "Misses critical dependencies between workstreams",
            ],
        },

        # ──────────────────────────────────────────────
        # 8. CULTURE FIT
        # ──────────────────────────────────────────────
        {
            "dimension": "culture_fit",
            "level": "fresher",
            "score_1_2": (
                "Shows no interest in the company or team dynamics. "
                "Answers suggest they would be difficult to work with — "
                "dismissive of collaboration, resistant to feedback, or "
                "unwilling to do tasks they consider 'beneath' them."
            ),
            "score_3_4": (
                "Neutral about the company — would join any company that "
                "pays well. Has not thought about work environment "
                "preferences. Answers about teamwork are generic and "
                "unconvincing."
            ),
            "score_5_6": (
                "Shows basic alignment with the company's values when "
                "prompted. Can describe positive teamwork experiences "
                "from college. Willing to learn and adapt but has not "
                "thought deeply about what kind of workplace suits them."
            ),
            "score_7_8": (
                "Demonstrates genuine enthusiasm for the company's mission "
                "or culture. Gives specific examples of collaboration, "
                "feedback, and adaptability from college or internships. "
                "Has thoughtful preferences about work style — not just "
                "'I can work in any environment.'"
            ),
            "score_9_10": (
                "Strong cultural alignment backed by evidence. Has chosen "
                "this company for specific cultural reasons they can "
                "articulate. Demonstrates values like ownership, curiosity, "
                "and empathy through concrete stories. Would contribute "
                "positively to team morale from day one."
            ),
            "key_indicators": [
                "Specific reasons for choosing this company beyond compensation",
                "Examples of collaboration and handling disagreements",
                "Openness to feedback and willingness to do unglamorous work",
                "Alignment with the company's stated values",
            ],
            "red_flags": [
                "Disparages previous teams, colleges, or professors",
                "Only cares about CTC and brand name",
                "Shows entitlement — 'I should not have to do testing'",
                "Rigid about location, team, or project preferences on day one",
            ],
        },
        {
            "dimension": "culture_fit",
            "level": "mid",
            "score_1_2": (
                "Toxic behaviours evident — badmouths previous employers, "
                "shows no respect for process or people, or has a 'not my "
                "job' attitude for anything beyond coding."
            ),
            "score_3_4": (
                "Transactional approach to work — clocks in, completes "
                "tickets, clocks out. No evidence of caring about team "
                "success, product quality, or helping others."
            ),
            "score_5_6": (
                "Positive team player who follows cultural norms. "
                "Participates in team activities and is generally liked. "
                "May not actively shape or improve the culture."
            ),
            "score_7_8": (
                "Actively contributes to a positive team environment. "
                "Helps during on-call, volunteers for unglamorous tasks, "
                "and gives constructive feedback. Aligns with the company's "
                "working style and can describe how they have adapted to "
                "different cultures."
            ),
            "score_9_10": (
                "Culture carrier who embodies and reinforces the company's "
                "values. Improves team dynamics through actions — organising "
                "knowledge-sharing sessions, onboarding new members, or "
                "mediating conflicts. Others describe them as someone who "
                "makes the team better."
            ),
            "key_indicators": [
                "Track record of positive team contributions beyond code",
                "Adaptability to different work cultures",
                "Willingness to do unglamorous but necessary work",
                "How they describe previous teams and managers",
            ],
            "red_flags": [
                "Blames every previous employer for problems",
                "Rigid about processes — 'that is not how we did it at X'",
                "No examples of helping someone outside their immediate scope",
            ],
        },
        {
            "dimension": "culture_fit",
            "level": "senior",
            "score_1_2": (
                "Would actively harm the culture. History of creating "
                "silos, hoarding information, or playing political games. "
                "Describes people as resources to be managed rather than "
                "individuals to be supported."
            ),
            "score_3_4": (
                "Neutral cultural presence. Neither toxic nor inspiring. "
                "Would maintain the status quo without improving team "
                "dynamics, values, or ways of working."
            ),
            "score_5_6": (
                "Positive role model within their immediate team. "
                "Supports the culture but does not actively evolve it. "
                "May struggle to navigate cultural differences across "
                "distributed or cross-functional teams."
            ),
            "score_7_8": (
                "Actively shapes team culture — establishes norms around "
                "code reviews, feedback, inclusion, and psychological "
                "safety. Can navigate and bridge cultural differences "
                "across offices, time zones, or functions."
            ),
            "score_9_10": (
                "Defines and evolves the engineering culture. Creates "
                "environments where people do their best work. Handles "
                "culture clashes with nuance. Has a track record of "
                "retaining and attracting talent because people want to "
                "work with them."
            ),
            "key_indicators": [
                "Track record of building inclusive, high-performing teams",
                "Approach to handling cultural conflicts or diversity challenges",
                "Impact on team retention and morale",
                "Consistency between stated values and observed behaviours",
            ],
            "red_flags": [
                "Creates in-groups and out-groups",
                "Tolerates toxic behaviour from high performers",
                "Culture is 'work hard, play hard' with no substance",
            ],
        },

        # ──────────────────────────────────────────────
        # 9. SELF AWARENESS
        # ──────────────────────────────────────────────
        {
            "dimension": "self_awareness",
            "level": "fresher",
            "score_1_2": (
                "Cannot identify any personal strengths or weaknesses. "
                "Gives canned answers like 'my weakness is I work too hard.' "
                "No reflection on academic performance, learning patterns, "
                "or personal growth areas."
            ),
            "score_3_4": (
                "Offers generic self-assessment disconnected from evidence. "
                "Cannot explain why they succeeded or failed at specific "
                "tasks. Blames external factors for all setbacks without "
                "considering their own role."
            ),
            "score_5_6": (
                "Can identify strengths and weaknesses with some accuracy. "
                "Acknowledges areas for improvement but may not have a "
                "concrete plan to address them. Self-assessment roughly "
                "matches demonstrated performance."
            ),
            "score_7_8": (
                "Thoughtful self-reflection. Can describe specific "
                "situations where they identified a gap and worked to close "
                "it — for example, realising they were weak in DSA and "
                "completing a structured practice plan. Accepts feedback "
                "genuinely and describes how they acted on it."
            ),
            "score_9_10": (
                "Exceptional self-awareness for their age. Accurately "
                "assesses their technical and interpersonal strengths and "
                "gaps. Has a deliberate growth plan. Can articulate their "
                "learning style, motivators, and stress triggers. "
                "Demonstrates growth mindset through concrete examples."
            ),
            "key_indicators": [
                "Accuracy of self-assessment vs demonstrated ability",
                "Specific examples of acting on feedback",
                "Awareness of learning style and growth areas",
                "Humility without self-deprecation",
            ],
            "red_flags": [
                "Dunning-Kruger effect — vastly overestimates abilities",
                "Uses rehearsed 'weakness' answers with no substance",
                "Cannot describe a single failure or mistake",
                "Defensive when given feedback during the interview itself",
            ],
        },
        {
            "dimension": "self_awareness",
            "level": "mid",
            "score_1_2": (
                "Significant gap between self-perception and reality. "
                "Claims senior-level skills but performance is junior. "
                "Cannot acknowledge any area needing improvement."
            ),
            "score_3_4": (
                "Some self-awareness but inconsistent. May acknowledge "
                "technical gaps but be blind to interpersonal ones (or "
                "vice versa). Has not sought structured feedback from "
                "managers or peers."
            ),
            "score_5_6": (
                "Reasonable self-awareness. Can discuss strengths and "
                "weaknesses with examples. Accepts performance review "
                "feedback and works on it. May still have blind spots "
                "around soft skills or leadership."
            ),
            "score_7_8": (
                "Actively seeks feedback through 1:1s, peer reviews, and "
                "retrospectives. Can articulate how they have grown over "
                "their career and what specifically drove that growth. "
                "Awareness extends to impact on others — understands how "
                "their communication style or decisions affect the team."
            ),
            "score_9_10": (
                "Deep self-awareness that drives deliberate development. "
                "Has a clear narrative of their career arc — what they "
                "learned at each stage and why they made each move. "
                "Understands their triggers, biases, and default patterns. "
                "Uses this awareness to be a better colleague and leader."
            ),
            "key_indicators": [
                "Seeking feedback proactively, not just accepting it",
                "Clear narrative of career growth and learning",
                "Awareness of impact on others (team dynamics, culture)",
                "Alignment between self-assessment and references or track record",
            ],
            "red_flags": [
                "Blames every job change on the employer",
                "Cannot name anything they would do differently",
                "Self-assessment wildly mismatched with demonstrated skills",
            ],
        },
        {
            "dimension": "self_awareness",
            "level": "senior",
            "score_1_2": (
                "No introspection despite years of experience. Cannot "
                "articulate their leadership style, strengths, or growth "
                "areas. Unaware of how they are perceived by others."
            ),
            "score_3_4": (
                "Some awareness of technical strengths but blind to "
                "interpersonal impact. Does not understand why past teams "
                "struggled or why attrition happened. Attributes all "
                "success to personal brilliance."
            ),
            "score_5_6": (
                "Reasonable self-awareness. Can discuss leadership mistakes "
                "and learnings. Seeks feedback but may not always act on it "
                "consistently. Understands their style but may not adapt "
                "it to different situations."
            ),
            "score_7_8": (
                "Highly self-aware leader. Knows their strengths, "
                "weaknesses, triggers, and biases. Adapts their style to "
                "different situations and people. Has worked with coaches "
                "or mentors to develop blind spots. Can discuss failures "
                "with genuine reflection."
            ),
            "score_9_10": (
                "Rare level of self-awareness. Models vulnerability and "
                "growth mindset for the organisation. Openly shares "
                "mistakes and learnings. Uses self-awareness to build "
                "trust and create psychological safety. Their team mirrors "
                "this openness."
            ),
            "key_indicators": [
                "Openness about past mistakes and genuine learnings",
                "Adaptability of leadership style to context",
                "Use of coaching, mentoring, or structured reflection",
                "Consistency between self-perception and team feedback",
            ],
            "red_flags": [
                "Infallibility complex — has never been wrong",
                "Cannot explain why people have left their team",
                "No evidence of personal development or coaching",
            ],
        },

        # ──────────────────────────────────────────────
        # 10. HANDLING PRESSURE
        # ──────────────────────────────────────────────
        {
            "dimension": "handling_pressure",
            "level": "fresher",
            "score_1_2": (
                "Completely overwhelmed by the interview itself. Cannot "
                "think when asked difficult questions. Breaks down or "
                "shuts down visibly. No evidence of handling any stressful "
                "situation in academics or life."
            ),
            "score_3_4": (
                "Manages routine interview pressure but crumbles when "
                "challenged or when a rapid-fire round begins. When asked "
                "about stressful situations, describes only panic and "
                "no coping mechanism."
            ),
            "score_5_6": (
                "Handles standard interview pressure adequately. Can "
                "describe a stressful situation (exam, project deadline) "
                "and how they managed. Performance dips slightly under "
                "time pressure but does not collapse."
            ),
            "score_7_8": (
                "Remains composed when questions get harder or the pace "
                "increases. Can describe managing competing deadlines — "
                "semester exams plus placement prep plus project submission. "
                "Takes a breath, thinks, and responds methodically."
            ),
            "score_9_10": (
                "Thrives under pressure. Uses challenging questions as "
                "opportunities to showcase thinking. Has managed genuinely "
                "stressful situations — college event crises, family "
                "responsibilities during academics, or startup-like "
                "intensity during internships — and can articulate coping "
                "strategies with maturity."
            ),
            "key_indicators": [
                "Composure during rapid-fire or stress-test portions of interview",
                "Quality of answers does not drop sharply under pressure",
                "Specific examples of managing stressful situations",
                "Presence of conscious coping strategies (not just 'I managed somehow')",
            ],
            "red_flags": [
                "Visible panic — hyperventilating, long silences, tears",
                "Blames the interviewer for making things stressful",
                "No example of any challenging situation ever faced",
            ],
        },
        {
            "dimension": "handling_pressure",
            "level": "mid",
            "score_1_2": (
                "Cannot handle production incidents, tight deadlines, or "
                "difficult stakeholder conversations. Freezes or makes "
                "panicked decisions that worsen the situation."
            ),
            "score_3_4": (
                "Gets through pressure situations but with visible stress "
                "that affects the team. Makes hasty decisions under "
                "pressure and often needs to course-correct later. No "
                "structured approach to stress management."
            ),
            "score_5_6": (
                "Manages typical work pressure — sprint deadlines, "
                "production bugs, code review pushback. May become "
                "stressed during major incidents or when multiple "
                "priorities collide but recovers without major impact."
            ),
            "score_7_8": (
                "Stays calm during incidents and tight deadlines. Has "
                "developed personal strategies for managing pressure — "
                "prioritisation frameworks, time-boxing, delegation. Can "
                "support teammates who are stressed. Performance remains "
                "consistent under pressure."
            ),
            "score_9_10": (
                "A calming presence during crises. Takes charge of "
                "stressful situations and brings structure — assigns roles, "
                "sets priorities, communicates status. Has managed "
                "high-stakes scenarios (data loss, security breach, client "
                "escalation) and emerged with trust intact."
            ),
            "key_indicators": [
                "Track record during production incidents",
                "Decision quality under time constraints",
                "Impact on team morale during stressful periods",
                "Personal stress management strategies",
            ],
            "red_flags": [
                "Takes stress out on teammates",
                "Makes impulsive decisions during incidents",
                "Disappears or becomes unreachable during crises",
            ],
        },
        {
            "dimension": "handling_pressure",
            "level": "senior",
            "score_1_2": (
                "Cannot lead through high-pressure situations. Team loses "
                "confidence in them during crises. Makes poor decisions "
                "when stakes are high and timeline is short."
            ),
            "score_3_4": (
                "Manages personal pressure but cannot create calm for "
                "others. During major incidents or org changes, adds to "
                "the anxiety rather than reducing it. Escalates too early "
                "or too late."
            ),
            "score_5_6": (
                "Handles standard pressures of a senior role competently. "
                "Can lead incident response and manage stakeholder "
                "expectations during delays. May show wear during "
                "prolonged high-pressure periods."
            ),
            "score_7_8": (
                "Rock-solid under pressure. Has led teams through "
                "critical incidents, organisational changes, or major "
                "launches without compromising decision quality or team "
                "morale. Creates psychological safety during stressful "
                "periods."
            ),
            "score_9_10": (
                "Exemplary crisis leader. Can manage simultaneous "
                "technical, people, and business pressures. Makes tough "
                "calls (cutting scope, reassigning people, pushing back on "
                "leadership) with clarity and empathy. Teams they have led "
                "through crises describe the experience as formative "
                "rather than traumatic."
            ),
            "key_indicators": [
                "Track record leading teams through crises",
                "Decision quality during high-stakes situations",
                "Team morale and retention during pressure periods",
                "Escalation judgment — timing and communication",
            ],
            "red_flags": [
                "Becomes a bottleneck during crises — cannot delegate",
                "History of burnout without recovery strategies",
                "Team attrition spikes during pressure periods",
            ],
        },

        # ──────────────────────────────────────────────
        # 11. MOTIVATION
        # ──────────────────────────────────────────────
        {
            "dimension": "motivation",
            "level": "fresher",
            "score_1_2": (
                "No discernible motivation for the role or the field. "
                "Chose engineering because of parental pressure and has "
                "no interest in technology. Cannot articulate why they "
                "want to work at all, let alone at this company."
            ),
            "score_3_4": (
                "Motivation is purely extrinsic — salary, brand name, "
                "air-conditioned office. No curiosity about the work "
                "itself. Has not done anything beyond the bare minimum "
                "curriculum."
            ),
            "score_5_6": (
                "Shows moderate interest in the field. Has completed "
                "some online courses or built small projects. Motivation "
                "is a mix of career growth and genuine interest but "
                "neither is deeply articulated."
            ),
            "score_7_8": (
                "Clearly motivated by both the work and the opportunity. "
                "Can articulate what excites them about technology and "
                "this specific role. Has pursued learning beyond college — "
                "personal projects, competitive programming, hackathons, "
                "or open-source contributions."
            ),
            "score_9_10": (
                "Deeply driven by intrinsic motivation — genuine passion "
                "for building things, solving problems, or a specific "
                "domain. Has a track record of self-directed learning and "
                "creation. Energy and enthusiasm are infectious. Has a "
                "clear view of where they want to be in 3-5 years and "
                "how this role fits."
            ),
            "key_indicators": [
                "Self-directed learning beyond the curriculum",
                "Specificity of career goals and how this role fits",
                "Energy and enthusiasm during the interview",
                "Evidence of curiosity — questions asked about the role and company",
            ],
            "red_flags": [
                "Only motivation is 'my parents want me to get a job'",
                "Cannot name a single thing that excites them about the role",
                "Has done nothing beyond attending college classes",
                "Applying to every company without differentiation",
            ],
        },
        {
            "dimension": "motivation",
            "level": "mid",
            "score_1_2": (
                "Appears to be leaving the current role only because of "
                "dissatisfaction, not because of any pull towards the new "
                "role. Cannot articulate what they want from the next "
                "stage of their career."
            ),
            "score_3_4": (
                "Primary motivation is a salary hike or a better brand "
                "name on the resume. Has not invested in learning new "
                "skills or taking on challenging work in the current role. "
                "Career trajectory looks passive — things happened to "
                "them rather than being chosen."
            ),
            "score_5_6": (
                "Motivated by a combination of growth and better "
                "opportunities. Can articulate what they want to learn "
                "and achieve. Has taken some initiative in their current "
                "role but could be more proactive about career development."
            ),
            "score_7_8": (
                "Driven by clear professional goals — wants to lead, "
                "deepen expertise, or transition to a specific domain. "
                "Has actively shaped their career through stretch "
                "assignments, learning investments, or strategic moves. "
                "This opportunity aligns with a deliberate plan."
            ),
            "score_9_10": (
                "Deeply motivated professional with a compelling career "
                "narrative. Every role change was a conscious step towards "
                "a vision. Continues to invest in growth — conference "
                "talks, side projects, mentoring. Motivated by impact, "
                "not just advancement. Brings passion that elevates "
                "the team."
            ),
            "key_indicators": [
                "Clarity of career goals and how this role fits",
                "Investment in professional development",
                "Proactive career management vs passive job hopping",
                "Intrinsic vs purely extrinsic motivation",
            ],
            "red_flags": [
                "Every job change was purely about money",
                "No learning or growth in the last 2 years",
                "Cannot explain why they want this specific role",
                "Negative motivation only — running away from current job",
            ],
        },
        {
            "dimension": "motivation",
            "level": "senior",
            "score_1_2": (
                "Appears burnt out or coasting. No passion for the work "
                "or the role. Motivation seems limited to maintaining "
                "their current lifestyle and compensation."
            ),
            "score_3_4": (
                "Motivated primarily by title or compensation. Has stopped "
                "growing technically and is not interested in developing "
                "others. Going through the motions of leadership without "
                "genuine engagement."
            ),
            "score_5_6": (
                "Professionally motivated with reasonable goals. Wants "
                "to lead larger teams or more complex systems. May lack "
                "the fire to drive transformation or inspire others."
            ),
            "score_7_8": (
                "Motivated by impact — building great products, developing "
                "people, solving hard problems at scale. Has a clear vision "
                "for their career and how this role advances it. Inspires "
                "motivation in others through their own example."
            ),
            "score_9_10": (
                "Missionary, not mercenary. Deeply motivated by a vision "
                "that transcends personal advancement — building world-class "
                "engineering teams, solving problems that matter, or "
                "advancing the state of the art. Track record shows "
                "sustained intensity and commitment over many years."
            ),
            "key_indicators": [
                "Clarity of long-term vision and purpose",
                "Evidence of sustained passion over many years",
                "Motivation to develop others, not just themselves",
                "Willingness to take on hard problems vs safe bets",
            ],
            "red_flags": [
                "Seeking the role for title inflation or retirement-in-place",
                "No energy or curiosity during the interview",
                "Career narrative is a series of disconnected hops",
            ],
        },

        # ──────────────────────────────────────────────
        # 12. STRATEGIC THINKING
        # ──────────────────────────────────────────────
        {
            "dimension": "strategic_thinking",
            "level": "fresher",
            "score_1_2": (
                "No ability to think beyond the immediate task. Cannot "
                "reason about why certain technical choices are made or "
                "what impact a feature has on users. Purely executes "
                "instructions."
            ),
            "score_3_4": (
                "Shows basic awareness that decisions have consequences "
                "but cannot articulate trade-offs. When asked 'why did you "
                "choose this approach for your project?', gives answers "
                "like 'because sir told us' or 'it was easy.'"
            ),
            "score_5_6": (
                "Can discuss trade-offs in their project choices when "
                "prompted — why they chose React over Angular, Python "
                "over Java. Thinking is limited to technical trade-offs "
                "without considering user impact, scalability, or cost."
            ),
            "score_7_8": (
                "Thinks beyond the code. Can discuss how a feature they "
                "built would scale, what would break, and how it could "
                "be improved. Shows awareness of user needs and business "
                "context even in academic projects. Asks forward-looking "
                "questions during the interview."
            ),
            "score_9_10": (
                "Unusually strategic for a fresher. Can reason about "
                "product-market fit, competitive dynamics, and technology "
                "trends. Has made strategic decisions in college — choosing "
                "skills to invest in, projects to build, or clubs to join "
                "based on long-term thinking rather than immediate "
                "gratification."
            ),
            "key_indicators": [
                "Ability to explain 'why' behind technical choices",
                "Awareness of trade-offs beyond just 'it works'",
                "Forward-looking questions about the role and company",
                "Evidence of deliberate choices in academic or personal trajectory",
            ],
            "red_flags": [
                "Cannot explain a single 'why' behind any project decision",
                "Thinks only about the current task, never the bigger picture",
                "No questions about the company's direction or strategy",
            ],
        },
        {
            "dimension": "strategic_thinking",
            "level": "mid",
            "score_1_2": (
                "Purely tactical — executes tickets without understanding "
                "the broader initiative. Cannot explain how their work "
                "connects to product or business goals."
            ),
            "score_3_4": (
                "Understands the immediate product context but cannot "
                "think in terms of quarters or years. Does not consider "
                "technical debt, platform evolution, or market dynamics "
                "when making decisions."
            ),
            "score_5_6": (
                "Starting to think strategically — considers technical "
                "debt and scalability in decisions. Can contribute to "
                "planning discussions with useful observations. May not "
                "yet have the experience to drive strategic direction."
            ),
            "score_7_8": (
                "Thinks multi-quarter. Considers how today's decisions "
                "affect tomorrow's architecture, team structure, and "
                "product capabilities. Can identify when a short-term "
                "hack is acceptable and when it creates unacceptable "
                "long-term cost. Proposes initiatives that shape the "
                "team's roadmap."
            ),
            "score_9_10": (
                "Strategic thinker who sees the chess board several moves "
                "ahead. Connects technical decisions to business outcomes, "
                "competitive positioning, and team growth. Proactively "
                "identifies strategic opportunities — 'If we build this "
                "platform now, it enables three product lines next year.' "
                "Influences the roadmap with data-backed proposals."
            ),
            "key_indicators": [
                "Connection between technical and business thinking",
                "Multi-quarter perspective in decision-making",
                "Proactive identification of strategic opportunities",
                "Influence on team or product roadmap",
            ],
            "red_flags": [
                "Cannot explain how their work connects to business goals",
                "Ignores technical debt without strategic reasoning",
                "Never proposes improvements — only executes what is asked",
            ],
        },
        {
            "dimension": "strategic_thinking",
            "level": "senior",
            "score_1_2": (
                "Despite seniority, thinks only at the project level. "
                "Cannot articulate a technology strategy or connect "
                "engineering investments to business outcomes."
            ),
            "score_3_4": (
                "Has a strategy for their immediate domain but cannot "
                "think at the organisational level. Does not consider "
                "how engineering strategy intersects with product, "
                "go-to-market, or hiring strategy."
            ),
            "score_5_6": (
                "Develops reasonable technical strategies for their "
                "area. Can participate in org-level planning discussions "
                "and contribute useful perspectives. May lack the "
                "commercial acumen to link technical strategy to "
                "business outcomes compellingly."
            ),
            "score_7_8": (
                "Drives technical strategy that is clearly aligned with "
                "business goals. Makes build-vs-buy decisions with "
                "financial reasoning. Anticipates industry trends and "
                "positions the team accordingly. Influences the "
                "organisation's multi-year engineering roadmap."
            ),
            "score_9_10": (
                "CTO-calibre strategic thinker. Shapes the company's "
                "technical direction with a deep understanding of market "
                "dynamics, competitive landscape, and emerging technologies. "
                "Makes strategic bets that create lasting competitive "
                "advantage. Can present technical strategy to a board "
                "of directors with clarity and conviction."
            ),
            "key_indicators": [
                "Quality of multi-year technical strategy",
                "Alignment between technical and business strategy",
                "Anticipation of industry trends and competitive moves",
                "Strategic bets that created measurable value",
            ],
            "red_flags": [
                "No strategic artifacts — no tech radar, roadmap, or vision doc",
                "Strategy is a list of technologies, not business outcomes",
                "Cannot articulate the competitive landscape",
            ],
        },

        # ──────────────────────────────────────────────
        # 13. ANALYTICAL THINKING
        # ──────────────────────────────────────────────
        {
            "dimension": "analytical_thinking",
            "level": "fresher",
            "score_1_2": (
                "Cannot interpret basic data — a table, a graph, or a "
                "simple equation. Answers to analytical questions are "
                "random guesses with no reasoning shown."
            ),
            "score_3_4": (
                "Shows some numerical reasoning but makes frequent logical "
                "errors. Can calculate but cannot set up the problem. "
                "When given a case or estimation question, the approach "
                "is haphazard with no structure."
            ),
            "score_5_6": (
                "Can approach estimation and analytical questions with a "
                "basic framework. Makes reasonable assumptions and works "
                "through them step by step. May miss important variables "
                "or make arithmetic errors under pressure."
            ),
            "score_7_8": (
                "Strong analytical skills. Breaks down estimation "
                "questions (e.g., 'How many delivery drivers does Swiggy "
                "need in Chennai?') with clear assumptions, logical "
                "segmentation, and sanity checks. Can interpret data from "
                "charts or tables and draw correct conclusions."
            ),
            "score_9_10": (
                "Exceptional analytical ability. Approaches complex "
                "problems with rigorous logic and creative decomposition. "
                "Identifies second-order effects and sensitivity points "
                "in their analysis. Can critique their own assumptions "
                "and adjust. Would excel in data science or consulting "
                "roles as well as engineering."
            ),
            "key_indicators": [
                "Structured approach to estimation problems",
                "Quality of assumptions — reasonable and stated explicitly",
                "Ability to interpret data and draw conclusions",
                "Self-correction and sanity-checking of results",
            ],
            "red_flags": [
                "Guesses without any reasoning",
                "Cannot set up a basic ratio or percentage calculation",
                "Refuses to attempt estimation questions",
            ],
        },
        {
            "dimension": "analytical_thinking",
            "level": "mid",
            "score_1_2": (
                "Cannot analyse system metrics, performance data, or "
                "user analytics. Makes decisions based on gut feel with "
                "no data to support them."
            ),
            "score_3_4": (
                "Looks at data when told to but does not proactively "
                "instrument or analyse. Can read a dashboard but cannot "
                "design one. Misses correlations and draws wrong "
                "conclusions from partial data."
            ),
            "score_5_6": (
                "Uses data to support decisions — checks metrics before "
                "and after changes, runs basic A/B analysis, and monitors "
                "system performance. May not have deep statistical "
                "knowledge but applies common sense to data."
            ),
            "score_7_8": (
                "Data-driven decision maker. Designs experiments, "
                "instruments systems for observability, and uses analytics "
                "to guide technical and product decisions. Can spot "
                "anomalies in data and investigate root causes. "
                "Communicates findings clearly to non-technical audiences."
            ),
            "score_9_10": (
                "Rigorous analytical thinker who brings quantitative "
                "reasoning to every decision. Builds dashboards and "
                "analytical tools adopted by the team. Can design and "
                "interpret complex experiments (multi-variate tests, "
                "cohort analysis). Identifies insights that change the "
                "direction of projects."
            ),
            "key_indicators": [
                "Use of data in daily decision-making",
                "Quality of system instrumentation and monitoring",
                "Ability to design and interpret experiments",
                "Communication of analytical findings to stakeholders",
            ],
            "red_flags": [
                "Makes significant decisions without data",
                "Confuses correlation with causation",
                "Cannot explain metrics on their own dashboards",
            ],
        },
        {
            "dimension": "analytical_thinking",
            "level": "senior",
            "score_1_2": (
                "Despite seniority, makes major decisions without "
                "analytical rigour. Cannot evaluate the ROI of an "
                "engineering investment or interpret business metrics."
            ),
            "score_3_4": (
                "Uses basic metrics but lacks sophistication. Cannot "
                "model the impact of architectural changes on cost, "
                "performance, or user experience. Relies on intuition "
                "for decisions that warrant quantitative analysis."
            ),
            "score_5_6": (
                "Competent analytical thinker. Uses data to support "
                "proposals and evaluates options with quantitative "
                "criteria. May not drive the analytical culture on the "
                "team but follows it when established."
            ),
            "score_7_8": (
                "Establishes analytical rigour across the team. Defines "
                "KPIs, builds business cases for engineering investments, "
                "and makes trade-off decisions with clear, data-backed "
                "reasoning. Can model cost-benefit scenarios for major "
                "architectural decisions."
            ),
            "score_9_10": (
                "World-class analytical capability. Can model complex "
                "systems — predicting the impact of architectural changes "
                "on cost, latency, reliability, and developer productivity. "
                "Builds analytical frameworks adopted across the org. "
                "Brings the same rigour to people decisions (hiring "
                "velocity, team sizing) as to technical ones."
            ),
            "key_indicators": [
                "Business case quality for engineering investments",
                "Sophistication of cost-benefit and trade-off analyses",
                "Analytical frameworks created for the team or org",
                "Application of analytical thinking to non-technical decisions",
            ],
            "red_flags": [
                "Cannot justify engineering investments in business terms",
                "No metrics or KPIs for the areas they own",
                "Relies on authority rather than evidence to drive decisions",
            ],
        },
    ]
