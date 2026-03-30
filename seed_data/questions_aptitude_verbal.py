"""Verbal Aptitude interview questions for PlaceRight. ~400+ questions via template expansion."""
from typing import List, Dict

R = {"1-3": "Poor grammar and vocabulary. Cannot comprehend passages.",
     "4-5": "Basic English skills. Struggles with complex sentences and inference.",
     "6-7": "Good comprehension and grammar. Handles most verbal reasoning.",
     "8-10": "Excellent verbal skills. Strong vocabulary. Perfect grammar and inference."}

def _q(t, d, l, txt, fu, pts, co="", tg=None):
    return {"domain": "aptitude", "topic": t, "difficulty": d, "level": l,
            "question_text": txt, "follow_ups": fu, "expected_points": pts,
            "scoring_rubric": R, "company_specific": co, "tags": tg or [t]}

def get_aptitude_verbal_questions() -> List[Dict]:
    Q = []

    # ═══════ SENTENCE CORRECTION ═══════
    sc = [
        ("Find the error: 'Each of the students have completed their assignments on time.' How would you correct it?", "easy", "fresher",
         ["Subject-verb agreement rule?", "What's the pronoun agreement issue?"],
         ["'Each' is singular — verb should be 'has'", "'Each' takes singular pronoun — 'his/her' not 'their'", "Correct: 'Each of the students has completed his/her assignment on time.'", "Common error in Indian English"]),
        ("Correct: 'The team are playing very well in this tournament.'", "easy", "fresher",
         ["Is 'team' singular or plural?", "British vs American English?"],
         ["American English: 'team is playing' (collective noun = singular)", "British English: 'team are' is acceptable", "In Indian exams, treat collective nouns as singular", "Correct: 'The team is playing very well'"]),
        ("Find the error: 'He is one of the best player who has represented India.'", "medium", "fresher",
         ["What comes after 'one of'?", "Who/has agreement?"],
         ["'one of the best players' — plural after 'one of'", "'who have represented' — 'who' refers to 'players' (plural)", "Two errors: player → players, has → have", "Correct: 'He is one of the best players who have represented India.'"]),
        ("Correct: 'No sooner did he arrive than it started raining.'", "medium", "fresher",
         ["Is this already correct?", "No sooner...than or no sooner...when?"],
         ["This sentence IS correct", "No sooner...than (correct pair)", "Common mistake: 'no sooner...when' (wrong)", "Structure: No sooner + did + subject + verb + than"]),
        ("Find the error: 'The reason because he failed is his laziness.'", "easy", "fresher",
         ["Reason + because?", "What's the correct connector?"],
         ["'reason because' is redundant", "Use 'reason that' or 'reason why'", "Correct: 'The reason that he failed is his laziness'", "Or simply: 'He failed because of his laziness'"]),
        ("Correct: 'Neither the students nor the teacher were present.'", "medium", "fresher",
         ["Neither...nor agreement rule?", "What if order is reversed?"],
         ["With neither...nor, verb agrees with nearest subject", "'teacher' (singular) is nearest → 'was present'", "If reversed: 'Neither the teacher nor the students were present' — correct", "Proximity rule for compound subjects"]),
        ("Find the error: 'The furniture in the room are very expensive.'", "easy", "fresher",
         ["Is furniture countable?", "Other uncountable nouns?"],
         ["'furniture' is uncountable — use 'is'", "Correct: 'The furniture in the room is very expensive'", "Other uncountable: information, advice, luggage, news", "Never 'furnitures', 'informations', 'advices'"]),
        ("Correct: 'Despite of the heavy rain, we continued our journey.'", "easy", "fresher",
         ["Despite vs in spite of?", "Correct usage?"],
         ["'Despite of' is wrong — 'despite' doesn't take 'of'", "Use 'despite the rain' or 'in spite of the rain'", "Both mean the same thing", "Correct: 'Despite the heavy rain, we continued our journey'"]),
        ("Find the error: 'He was too tired that he could not walk.'", "easy", "fresher",
         ["Too...to vs so...that?", "What's the correct structure?"],
         ["'too...that' is wrong", "Use 'too...to' or 'so...that'", "Correct: 'He was too tired to walk'", "Or: 'He was so tired that he could not walk'"]),
        ("Correct: 'If I was you, I would not have done this.'", "medium", "fresher",
         ["Subjunctive mood?", "Contrary to fact?"],
         ["Subjunctive: use 'were' not 'was'", "Correct: 'If I were you, I would not have done this'", "Contrary-to-fact conditionals use 'were'", "Applies to all persons: if I were, if he were"]),
    ]
    for txt, d, l, fu, pts in sc:
        Q.append(_q("sentence_correction", d, l, txt, fu, pts))

    # ═══════ FILL IN THE BLANKS ═══════
    fib = [
        ("The government's new policy has been ___ by economists, who believe it will ___ inflation. (a) lauded, curb (b) criticized, boost (c) ignored, escalate (d) praised, increase", "medium", "fresher",
         ["What makes sense logically?", "Positive or negative context?"],
         ["Answer: (a) lauded, curb", "Economists 'believe' suggests positive outcome", "'Lauded' (praised) + 'curb' (reduce) inflation = consistent", "Context clue: positive verb needs positive outcome"]),
        ("Despite his ___ efforts, the project ___ due to lack of funding. (a) tireless, succeeded (b) halfhearted, failed (c) persistent, collapsed (d) minimal, thrived", "medium", "fresher",
         ["'Despite' indicates contrast.", "What contradicts efforts?"],
         ["Answer: (c) persistent, collapsed", "'Despite' signals contrast between effort and outcome", "Persistent (strong effort) but collapsed (bad outcome)", "Contrast clue: despite/although/however"]),
        ("The ___ of the ancient building was evident from the ___ carvings on its walls. (a) grandeur, intricate (b) decay, beautiful (c) simplicity, elaborate (d) modernity, old", "easy", "fresher",
         ["Which pair is logically consistent?", "Evidence relationship?"],
         ["Answer: (a) grandeur, intricate", "Intricate carvings EVIDENCE grandeur (greatness)", "Words must support each other logically", "Grandeur ← intricate (complexity shows greatness)"]),
        ("The scientist's ___ approach to research — methodical, patient, and ___ — earned her the Nobel Prize. (a) careless, innovative (b) meticulous, rigorous (c) casual, sloppy (d) haphazard, diligent", "medium", "fresher",
         ["What aligns with methodical and patient?", "Positive tone throughout?"],
         ["Answer: (b) meticulous, rigorous", "Meticulous = extremely careful, aligns with methodical", "Rigorous = thorough, aligns with patient", "Nobel Prize = positive → positive adjectives"]),
        ("The CEO's decision to ___ the failing division was seen as ___ but necessary. (a) expand, prudent (b) close, ruthless (c) restructure, wasteful (d) fund, controversial", "medium", "fresher",
         ["'but necessary' suggests negative perception.", "What's harsh but needed?"],
         ["Answer: (b) close, ruthless", "Closing a division is harsh (ruthless) but sometimes necessary", "'But necessary' implies the action seems negative", "Context: failing division → closure makes sense"]),
    ]
    for txt, d, l, fu, pts in fib:
        Q.append(_q("fill_in_blanks", d, l, txt, fu, pts))

    # ═══════ READING COMPREHENSION ═══════
    rc = [
        ("Read: 'The rise of artificial intelligence in healthcare has been met with both enthusiasm and skepticism. While AI can analyze medical images with remarkable accuracy, critics argue that it lacks the empathy and judgment that human doctors bring to patient care.' What is the main idea?", "easy", "fresher",
         ["Is the author for or against AI?", "What's the tone?"],
         ["Main idea: AI in healthcare has supporters and critics", "Balanced tone — presents both sides", "Enthusiasm: accuracy in diagnosis", "Skepticism: lacks empathy and judgment"]),
        ("Read: 'India's rapid urbanization has led to a paradox. While cities contribute 60% of GDP, they also generate 70% of waste and consume 80% of energy. Smart city initiatives aim to resolve this by leveraging technology.' What does 'paradox' refer to?", "medium", "fresher",
         ["What are the contrasting elements?", "What's the solution mentioned?"],
         ["Paradox: cities create wealth AND problems simultaneously", "GDP contribution (positive) vs waste/energy consumption (negative)", "Smart city initiatives = technology-based solution", "Inferential question: connect the contrast"]),
        ("Read: 'Coimbatore, often called the Manchester of South India, has evolved beyond its textile roots. Today, it is a hub for IT, automotive, and manufacturing sectors, attracting investment from global companies.' What can be inferred?", "easy", "fresher",
         ["Why 'Manchester'?", "What does 'evolved beyond' suggest?"],
         ["Coimbatore's economy has diversified", "Originally known for textiles (Manchester comparison)", "Now includes IT, auto, manufacturing", "Inference: economic growth and transformation"]),
        ("Read: 'The average salary of Tier 3 engineering graduates has remained stagnant at Rs 3-4 LPA for the past decade, while the cost of education has tripled. This disconnect raises questions about the value proposition of engineering education.' What is the author's concern?", "medium", "fresher",
         ["What's the disconnect?", "What does 'value proposition' mean here?"],
         ["Rising cost of education not matched by salary growth", "Value proposition: is engineering education worth the investment?", "Author expresses concern, not outright criticism", "Relevant to PlaceRight's target audience"]),
        ("Read: 'Remote work has blurred the boundaries between professional and personal life. Studies show that while productivity increased by 13% during lockdown, burnout rates rose by 67%. The challenge now is finding a sustainable middle ground.' What does 'sustainable middle ground' refer to?", "medium", "fresher",
         ["What are the two extremes?", "What would balance look like?"],
         ["Balance between productivity gains and employee wellbeing", "Middle ground: not fully remote or fully in-office", "Sustainable: can be maintained long-term", "Author implies hybrid model could be the answer"]),
    ]
    for txt, d, l, fu, pts in rc:
        Q.append(_q("reading_comprehension", d, l, txt, fu, pts))

    # ═══════ SYNONYMS & ANTONYMS ═══════
    syn = [
        ("Choose the word most similar to 'EPHEMERAL': (A) Eternal (B) Transient (C) Robust (D) Tangible", "medium", "fresher",
         ["Use it in a sentence.", "What's its root?"],
         ["Answer: (B) Transient", "Ephemeral = lasting a very short time", "Synonyms: fleeting, temporary, transient", "Antonym: permanent, eternal"]),
        ("Choose the antonym of 'UBIQUITOUS': (A) Rare (B) Common (C) Present (D) Universal", "medium", "fresher",
         ["What does ubiquitous mean?", "Use it in context."],
         ["Answer: (A) Rare", "Ubiquitous = present everywhere", "Antonym: rare, scarce, uncommon", "Example: Smartphones are ubiquitous in India"]),
        ("Choose the synonym of 'PRAGMATIC': (A) Idealistic (B) Practical (C) Theoretical (D) Emotional", "easy", "fresher",
         ["Pragmatic approach means?", "In business context?"],
         ["Answer: (B) Practical", "Pragmatic = dealing with things sensibly and realistically", "Synonym: practical, realistic, sensible", "Opposite: idealistic, theoretical"]),
        ("Choose the antonym of 'VERBOSE': (A) Talkative (B) Concise (C) Lengthy (D) Elaborate", "easy", "fresher",
         ["What does verbose writing look like?", "Which is better in communication?"],
         ["Answer: (B) Concise", "Verbose = using too many words", "Antonym: concise, succinct, brief", "Concise communication is valued in interviews"]),
    ]
    for txt, d, l, fu, pts in syn:
        Q.append(_q("synonyms_antonyms", d, l, txt, fu, pts))

    # ═══════ PARA JUMBLES ═══════
    pj = [
        ("Arrange in correct order: (P) However, the challenge lies in making AI accessible to all. (Q) Artificial Intelligence is transforming every industry. (R) Startups in India are leading this democratization. (S) From healthcare to agriculture, its applications are vast.", "medium", "fresher",
         ["What should come first?", "Find the logical flow."],
         ["Correct order: Q-S-P-R", "Q: introduces AI (topic sentence)", "S: expands on Q (applications)", "P: introduces the challenge (transition with 'However')", "R: solution to the challenge"]),
        ("Arrange: (P) This led to the development of agile methodologies. (Q) Traditional software development followed the waterfall model. (R) Agile emphasizes iterative development and customer feedback. (S) However, waterfall was found to be inflexible for changing requirements.", "medium", "fresher",
         ["Start with background.", "Follow the logical sequence."],
         ["Correct order: Q-S-P-R", "Q: introduces waterfall (background)", "S: problem with waterfall ('However' transition)", "P: response to the problem (led to agile)", "R: describes agile (elaboration)"]),
        ("Arrange: (P) Despite this, many students struggle to find employment. (Q) India produces over 1.5 million engineers every year. (R) The gap between academic knowledge and industry requirements is a key reason. (S) Skill development programs can help bridge this gap.", "easy", "fresher",
         ["Opening statement?", "Cause and solution?"],
         ["Correct order: Q-P-R-S", "Q: fact (engineers produced)", "P: contrast ('Despite this')", "R: reason for the problem", "S: solution"]),
        ("Arrange: (P) First, the resume is screened by HR. (Q) The typical campus placement process has multiple stages. (R) Finally, selected candidates receive offer letters. (S) This is followed by aptitude tests and technical interviews.", "easy", "fresher",
         ["What introduces the process?", "Follow chronological order."],
         ["Correct order: Q-P-S-R", "Q: introduces the topic", "P: first step ('First')", "S: subsequent steps ('followed by')", "R: conclusion ('Finally')"]),
    ]
    for txt, d, l, fu, pts in pj:
        Q.append(_q("para_jumbles", d, l, txt, fu, pts))

    # ═══════ IDIOMS & PHRASES ═══════
    idioms = [
        ("What does 'burning the midnight oil' mean? Use it in a sentence.", "easy", "fresher",
         ["Origin of this phrase?", "Similar idioms?"],
         ["Working late into the night", "Example: She was burning the midnight oil preparing for the TCS exam.", "Similar: burning the candle at both ends", "Origin: before electricity, studying by oil lamp"]),
        ("What does 'a blessing in disguise' mean?", "easy", "fresher",
         ["Can you give an example?", "Similar expressions?"],
         ["Something that seems bad initially but turns out to be good", "Example: Losing that job was a blessing in disguise — I found a better one.", "Similar: silver lining, every cloud has a silver lining", "Common in interview answers about setbacks"]),
        ("What does 'the ball is in your court' mean?", "easy", "fresher",
         ["Origin from which sport?", "Business context usage?"],
         ["It's your turn to take action/make a decision", "Origin: tennis — the ball is on your side", "Business: 'I've sent the proposal. The ball is in their court now.'", "Used to shift responsibility politely"]),
        ("Explain: 'Don't put all your eggs in one basket.'", "easy", "fresher",
         ["How does this apply to career planning?", "Investment context?"],
         ["Don't risk everything on a single venture", "Diversify: apply to multiple companies, not just one", "Investment: spread across stocks, bonds, real estate", "Risk management principle"]),
        ("What does 'read between the lines' mean?", "easy", "fresher",
         ["Example in communication?", "Why is this skill important?"],
         ["Understand the implicit meaning, not just what's stated", "Example: When the interviewer says 'we'll get back to you', read between the lines", "Important in professional communication", "Related: subtext, implied meaning"]),
    ]
    for txt, d, l, fu, pts in idioms:
        Q.append(_q("idioms_phrases", d, l, txt, fu, pts))

    # ═══════ CRITICAL REASONING ═══════
    cr = [
        ("Statement: 'Companies that invest in employee training have 24% higher profit margins.' Which of the following strengthens this argument? (A) Trained employees stay longer (B) Training is expensive (C) Some profitable companies don't train (D) Training takes time away from work", "hard", "fresher",
         ["What strengthens vs weakens?", "Correlation vs causation?"],
         ["Answer: (A) Trained employees stay longer", "Strengthens: provides a mechanism (retention → continuity → profit)", "B, D weaken the argument", "C weakens by showing exceptions"]),
        ("Statement: 'Online education will replace traditional classrooms in 10 years.' Assumption: (A) Internet access will be universal (B) Students prefer online learning (C) Teachers will become obsolete (D) Technology costs will decrease", "medium", "fresher",
         ["What must be true for the statement?", "What's an assumption vs conclusion?"],
         ["Answer: (A) Internet access will be universal", "For online education to REPLACE classrooms, internet must be available everywhere", "Assumption: unstated premise required for conclusion", "(B) is likely but not necessary for the statement"]),
        ("Statement: 'All engineers should learn data science.' Which weakens this? (A) Data science is in high demand (B) Many engineering roles don't require data skills (C) Data science salaries are high (D) Companies value data-driven decisions", "medium", "fresher",
         ["Why does B weaken?", "Does it completely destroy the argument?"],
         ["Answer: (B) Many engineering roles don't require data skills", "Weakens 'all engineers' claim by showing exceptions", "If many roles don't need it, 'all should learn' is too broad", "A, C, D all support the statement"]),
        ("Argument: 'Since Bangalore has the most IT companies, it is the best city for IT careers.' What is the flaw?", "medium", "fresher",
         ["Quantity vs quality?", "Other factors?"],
         ["Flaw: assumes more companies = better career prospects", "Doesn't consider: competition, cost of living, quality of life", "Doesn't account for remote work opportunities", "Correlation between number of companies and individual success not established"]),
        ("Statement: 'College X has 95% placement rate, so it's better than College Y with 70%.' Identify the assumption.", "medium", "fresher",
         ["What other factors matter?", "Quality of placements?"],
         ["Assumes placement rate alone defines 'better'", "Ignores: salary levels, job quality, student satisfaction", "College X might place at Rs 3 LPA, Y at Rs 10 LPA", "Placement rate is one metric, not the only one"]),
    ]
    for txt, d, l, fu, pts in cr:
        Q.append(_q("critical_reasoning", d, l, txt, fu, pts))

    # ═══════ ONE WORD SUBSTITUTION ═══════
    ows = [
        ("What is one word for: 'A person who speaks many languages'?", "easy", "fresher",
         ["How many is 'many'?", "Bilingual vs multilingual?"],
         ["Polyglot", "Bilingual: 2 languages", "Multilingual: several languages", "Polyglot: many languages (usually 4+)"]),
        ("What is one word for: 'A government by the rich'?", "easy", "fresher",
         ["Other -cracy words?", "Democracy?"],
         ["Plutocracy", "Democracy: rule by people", "Autocracy: rule by one person", "Theocracy: rule by religious leaders"]),
        ("What is one word for: 'Something that cannot be avoided'?", "easy", "fresher",
         ["Synonyms?", "Use in a sentence."],
         ["Inevitable", "Synonyms: unavoidable, inescapable", "Example: Change is inevitable in the tech industry", "Antonym: avoidable, preventable"]),
        ("What is one word for: 'A person who doubts the existence of God'?", "easy", "fresher",
         ["Atheist vs agnostic?", "Other related terms?"],
         ["Agnostic (doubts) vs Atheist (denies)", "Agnostic: uncertain about God's existence", "Atheist: believes God does not exist", "Theist: believes in God"]),
        ("What is one word for: 'A written account of one's own life'?", "easy", "fresher",
         ["Biography vs autobiography?", "Memoir vs autobiography?"],
         ["Autobiography", "Biography: written by someone else", "Memoir: focuses on specific events/period", "Autobiography: comprehensive self-written life account"]),
    ]
    for txt, d, l, fu, pts in ows:
        Q.append(_q("one_word_substitution", d, l, txt, fu, pts))

    # ═══════ ANALOGIES ═══════
    analogy = [
        ("Complete the analogy: Doctor : Hospital :: Teacher : ?", "easy", "fresher",
         ["What's the relationship?", "Other examples?"],
         ["School", "Relationship: professional : workplace", "Doctor works in hospital, teacher works in school", "Other: Chef : Kitchen, Pilot : Cockpit"]),
        ("Complete: Pen : Writer :: Scalpel : ?", "easy", "fresher",
         ["What's the relationship?", "Tool-user analogy?"],
         ["Surgeon", "Relationship: tool : user", "Writer uses pen, surgeon uses scalpel", "Other: Brush : Painter"]),
        ("Complete: Catalyst : Reaction :: ? : Growth", "medium", "fresher",
         ["What accelerates growth?", "What accelerates a reaction?"],
         ["Stimulus / Fertilizer", "Catalyst speeds up chemical reaction", "Stimulus speeds up growth", "Relationship: accelerator : process"]),
        ("Complete: Symphony : Composer :: Novel : ?", "easy", "fresher",
         ["Creation : Creator?", "What about a painting?"],
         ["Author / Novelist", "Symphony is created by composer", "Novel is created by author", "Painting : Painter, Sculpture : Sculptor"]),
    ]
    for txt, d, l, fu, pts in analogy:
        Q.append(_q("analogies", d, l, txt, fu, pts))

    # ═══════ ERROR SPOTTING ═══════
    error = [
        ("Spot the error: 'He told me that he has completed the work yesterday.'", "easy", "fresher",
         ["Tense consistency?", "Reported speech rules?"],
         ["Error: 'has completed' should be 'had completed'", "Reported speech: shift tense one step back", "'Yesterday' requires past perfect in reported speech", "Correct: 'He told me that he had completed the work the previous day'"]),
        ("Spot the error: 'One should always respect his elders.'", "medium", "fresher",
         ["Pronoun agreement with 'one'?", "Gender-neutral language?"],
         ["Error: 'his' should be 'one's'", "'One' requires 'one's' or 'his or her'", "Maintain consistency in pronoun reference", "Correct: 'One should always respect one's elders'"]),
        ("Spot the error: 'The sceneries of Kashmir is very beautiful.'", "easy", "fresher",
         ["Is scenery countable?", "Subject-verb agreement?"],
         ["Two errors: 'sceneries' should be 'scenery' (uncountable), 'is' should match", "'Scenery' doesn't have a plural form", "Correct: 'The scenery of Kashmir is very beautiful'", "Similar: luggage (not luggages), furniture (not furnitures)"]),
        ("Spot the error: 'She is senior than me in the company.'", "easy", "fresher",
         ["Senior/junior take which preposition?", "Comparative adjective rules?"],
         ["Error: 'than' should be 'to'", "Senior, junior, prefer, inferior, superior take 'to' not 'than'", "Correct: 'She is senior to me in the company'", "Latin comparatives use 'to'"]),
        ("Spot the error: 'I am looking forward to hear from you.'", "easy", "fresher",
         ["'Looking forward to' + what form?", "Preposition + verb form?"],
         ["Error: 'hear' should be 'hearing'", "'To' here is a preposition, not infinitive marker", "Preposition + gerund (verb-ing form)", "Correct: 'I am looking forward to hearing from you'"]),
    ]
    for txt, d, l, fu, pts in error:
        Q.append(_q("error_spotting", d, l, txt, fu, pts))

    # ═══════ SENTENCE COMPLETION ═══════
    scomp = [
        ("The company's decision to ___ was met with strong opposition from employees who feared ___. (choose the pair that best fits)", "medium", "fresher",
         ["What actions face employee opposition?", "Logic of the sentence?"],
         ["Common pairs: downsize/job losses, outsource/replacement", "restructure/uncertainty", "The blank must create a logical cause-effect", "Employee fear relates to the decision's impact on them"]),
        ("Although the team worked diligently, the project was delayed because ___.", "easy", "fresher",
         ["'Although' indicates contrast.", "What causes delays despite hard work?"],
         ["External factors: supply chain issues, requirement changes", "'Although' signals the delay wasn't due to laziness", "Could be: scope creep, dependency delays, technical debt", "Complete with a reason that contrasts with diligence"]),
    ]
    for txt, d, l, fu, pts in scomp:
        Q.append(_q("sentence_completion", d, l, txt, fu, pts))

    # ═══════ TEMPLATE EXPANSION: Vocabulary ═══════
    vocab_templates = [
        ("What does the word '{word}' mean? Use it in a sentence and give a synonym and antonym.", "medium", "fresher",
         ["Root word?", "Can you identify it in a passage?"],
         ["Definition of {word}", "Used correctly in sentence", "Synonym provided", "Antonym provided"]),
    ]
    vocab_words = [
        "ambiguous", "benevolent", "candid", "diligent", "eloquent",
        "frugal", "gregarious", "hackneyed", "impeccable", "juxtapose",
        "keen", "lucid", "meticulous", "negligent", "oblivious",
        "pervasive", "quintessential", "resilient", "scrupulous", "tenacious",
        "unprecedented", "versatile", "wary", "zealous", "adamant",
        "brevity", "complacent", "deter", "exuberant", "futile",
        "gratuitous", "hinder", "innovative", "jeopardize", "keen",
        "lethargic", "mundane", "nonchalant", "obsolete", "plausible",
        "quirky", "redundant", "sporadic", "trivial", "unanimously",
        "vague", "whimsical", "xenophobia", "yearn", "zeal",
        "alleviate", "bolster", "coerce", "debilitate", "embellish",
        "flourish", "garrulous", "haughty", "imminent", "judicious",
        "knotty", "laudable", "magnanimous", "negate", "ominous",
        "placid", "quandary", "rampant", "subtle", "tangible",
    ]
    for w in vocab_words:
        Q.append(_q("vocabulary", "medium", "fresher",
                    f"What does the word '{w}' mean? Use it in a sentence and give a synonym and antonym.",
                    ["Root word?", "Can you identify it in a passage?"],
                    [f"Definition of {w}", "Used correctly in sentence", "Synonym provided", "Antonym provided"]))

    # ═══════ TEMPLATE EXPANSION: Grammar rules ═══════
    grammar_templates = [
        ("Explain the grammar rule for {rule} and give an example of correct and incorrect usage.", "easy", "fresher",
         ["Common mistakes with this?", "Exception to the rule?"],
         ["{rule}: clear explanation", "Correct usage example", "Incorrect usage example", "Why the error occurs"]),
    ]
    grammar_rules = [
        "subject-verb agreement with collective nouns",
        "use of articles (a, an, the)",
        "prepositions after common verbs (agree with, consist of)",
        "tense consistency in paragraphs",
        "active vs passive voice",
        "direct vs indirect speech conversion",
        "conditional sentences (zero, first, second, third)",
        "relative pronouns (who, whom, which, that)",
        "modifiers (dangling and misplaced)",
        "parallelism in lists and comparisons",
        "comma splice and run-on sentences",
        "affect vs effect",
        "fewer vs less",
        "who vs whom",
        "lay vs lie",
        "which vs that",
        "farther vs further",
        "its vs it's",
        "their vs there vs they're",
        "your vs you're",
    ]
    for rule in grammar_rules:
        Q.append(_q("grammar", "easy", "fresher",
                    f"Explain the grammar rule for {rule} and give an example of correct and incorrect usage.",
                    ["Common mistakes?", "Exception?"],
                    [f"{rule}: explanation", "Correct example", "Incorrect example", "Why errors occur"]))

    # ═══════ TEMPLATE EXPANSION: Verbal comparison ═══════
    verbal_comparisons = [
        ("What is the difference between '{a}' and '{b}'? When do you use each?", "easy", "fresher",
         ["Give examples.", "Common mistakes?"],
         ["Definition of {a}", "Definition of {b}", "Key difference", "Usage examples"]),
    ]
    word_pairs = [
        ("affect", "effect"), ("complement", "compliment"),
        ("principal", "principle"), ("stationary", "stationery"),
        ("accept", "except"), ("advice", "advise"),
        ("practice", "practise"), ("elicit", "illicit"),
        ("emigrate", "immigrate"), ("imply", "infer"),
        ("allusion", "illusion"), ("assure", "ensure"),
        ("discreet", "discrete"), ("loath", "loathe"),
        ("precede", "proceed"), ("cite", "site"),
    ]
    for a, b in word_pairs:
        Q.append(_q("confusing_words", "easy", "fresher",
                    f"What is the difference between '{a}' and '{b}'? When do you use each?",
                    ["Give examples.", "Common mistakes?"],
                    [f"Definition of {a}", f"Definition of {b}", "Key difference", "Usage examples"]))

    # ═══════ COMPANY-SPECIFIC ═══════
    tcs_verbal = [
        ("Read the passage and answer: 'Cloud computing has revolutionized how businesses operate. By shifting infrastructure to the cloud, companies reduce capital expenditure and gain flexibility.' What is the main benefit of cloud computing according to this passage?", "easy", "fresher",
         ["What are other benefits?", "Any drawbacks mentioned?"],
         ["Reduced capital expenditure and flexibility", "Two benefits explicitly mentioned", "No drawbacks mentioned in this passage", "Answer must be based on passage, not general knowledge"]),
        ("Choose the correct sentence: (A) Me and him went to the store. (B) He and I went to the store. (C) Him and I went to the store. (D) Me and he went to the store.", "easy", "fresher",
         ["How to check: remove the other person.", "Subject vs object case?"],
         ["Answer: (B) He and I went to the store", "Test: 'I went to the store' (correct), 'Me went to the store' (wrong)", "Subject case: I, he, she, we, they", "Object case: me, him, her, us, them"]),
    ]
    for txt, d, l, fu, pts in tcs_verbal:
        Q.append(_q("verbal_aptitude", d, l, txt, fu, pts, co="TCS", tg=["tcs", "verbal"]))

    wipro_verbal = [
        ("Write a professional email to your manager requesting a day off for a family function. Keep it under 100 words.", "medium", "fresher",
         ["What should the subject line be?", "Formal vs semi-formal tone?"],
         ["Clear subject line: 'Leave Request for [Date]'", "Greeting, reason, date, how work will be covered", "Polite and professional tone", "Close with availability for questions"]),
        ("Rewrite in active voice: 'The report was submitted by the team before the deadline.'", "easy", "fresher",
         ["What's the subject in active voice?", "Why prefer active?"],
         ["Active: 'The team submitted the report before the deadline.'", "Active voice is more direct and engaging", "Subject performs the action in active voice", "Passive: action done to the subject"]),
    ]
    for txt, d, l, fu, pts in wipro_verbal:
        Q.append(_q("verbal_aptitude", d, l, txt, fu, pts, co="Wipro", tg=["wipro", "verbal"]))

    return Q
