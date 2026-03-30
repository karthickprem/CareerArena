"""
Comprehensive Indian placement context data for CareerArena.

Covers campus placements, interview culture, salary negotiation,
common mistakes, regional ecosystems, UPSC personality tests,
and group discussion formats — all deeply specific to the Indian
context with real company names, INR figures, and cultural norms
aimed at Tier 2/3 college students.
"""

from typing import List, Dict


def get_indian_context() -> List[Dict]:
    """Return 50+ entries of Indian placement context data.

    Each entry is a dict with keys:
        category (str)  - broad category
        topic    (str)  - specific topic within category
        content  (str)  - detailed explanatory text (2-5 paragraphs)
        tips     (list) - 3-7 actionable tips
    """
    return [
        # =====================================================================
        # CAMPUS PLACEMENT (15 entries)
        # =====================================================================
        {
            "category": "campus_placement",
            "topic": "tier_system",
            "content": (
                "Indian engineering colleges are informally classified into tiers that "
                "strongly influence placement outcomes. Tier 1 includes IITs, NITs, BITS "
                "Pilani, and top IIITs. Tier 2 covers well-known state and private "
                "universities such as VIT, SRM, Manipal, PESIT, and top state government "
                "colleges like CEG Anna University or COEP Pune. Tier 3 encompasses the "
                "vast majority of AICTE-approved private engineering colleges — roughly "
                "3,500+ institutions across India.\n\n"
                "For Tier 3 students the placement landscape is fundamentally different. "
                "Companies like Google, Microsoft, or Goldman Sachs almost never visit "
                "these campuses. Instead, the dominant recruiters are IT services "
                "companies — TCS, Infosys, Wipro, Cognizant, HCL, Tech Mahindra, "
                "Capgemini, and Accenture. These firms conduct mass hiring drives "
                "(TCS NQT, InfyTQ, Wipro NLTH) that are open to students from all "
                "tiers, but the entry salaries are typically 3-4 LPA.\n\n"
                "The tier label is not a permanent ceiling. Many successful engineers "
                "from Tier 3 colleges have moved to top product companies within 2-3 "
                "years by building strong DSA skills, contributing to open source, or "
                "cracking off-campus drives. The key is to treat the first job as a "
                "stepping stone rather than a destination."
            ),
            "tips": [
                "Do not let the tier label define your ceiling — treat it as a starting point.",
                "Focus on mass-recruiter drives (TCS NQT, InfyTQ) for guaranteed first placement.",
                "Simultaneously prepare for off-campus roles at startups and mid-tier product companies.",
                "Build a strong GitHub profile with 3-5 non-trivial projects to stand out.",
                "Target service-based companies for stability and product companies for growth.",
                "Network on LinkedIn with alumni from your college who moved to better companies.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "day_1_day_2_companies",
            "content": (
                "In Indian campus placements, companies are slotted into days based on "
                "the salary packages they offer. 'Day 1' companies pay the highest CTC "
                "— typically 10 LPA and above — and include firms like Microsoft, "
                "Google, Amazon, Oracle, Samsung R&D, and top-tier consulting firms. "
                "'Day 2' and 'Day 3' companies offer progressively lower packages, "
                "usually in the 5-9 LPA and 3-5 LPA ranges respectively.\n\n"
                "At Tier 2 and Tier 3 colleges, 'Day 1' often features companies like "
                "Zoho, Freshworks, or occasionally PayPal and Cisco, offering packages "
                "in the 6-12 LPA range. 'Day 2' slots are filled by service companies "
                "like TCS Digital (7 LPA), Infosys Power Programmer (8 LPA), and "
                "Cognizant GenC Elevate (6 LPA). The regular mass-hiring roles from "
                "TCS, Infosys, and Wipro at 3.36-3.8 LPA typically come on Day 3 or "
                "as open-pool drives.\n\n"
                "Once a student is placed on an earlier day, they are usually not "
                "allowed to sit for subsequent days — this is the 'one-offer' policy "
                "followed by most placement cells. Some colleges allow students to "
                "appear for a 'dream company' slot even after being placed, but this "
                "is institution-specific."
            ),
            "tips": [
                "Clarify your college's 'dream company' policy with the placement cell early.",
                "If Day 1 companies are realistic for your profile, prepare DSA on LeetCode medium-hard.",
                "Do not skip Day 2/3 drives hoping for better — a bird in hand matters.",
                "Understand that Day 1 at a Tier 3 college equals Day 3 at an IIT — calibrate expectations.",
                "Track which companies visited your college in the past 3 years to plan preparation.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "ppt_etiquette",
            "content": (
                "The Pre-Placement Talk (PPT) is a formal presentation given by a "
                "company before its recruitment drive begins on campus. In India, PPTs "
                "are often the first interaction between students and the company, and "
                "how you behave during a PPT can directly affect your chances. HR "
                "representatives from companies like Infosys, TCS, and Zoho actively "
                "observe student behaviour during PPTs and sometimes note down names "
                "of students who asked intelligent questions.\n\n"
                "PPTs typically cover the company overview, roles offered, CTC breakup, "
                "work culture, and the selection process. At Tier 2/3 colleges, many "
                "students skip PPTs thinking they are unnecessary — this is a mistake. "
                "The PPT often reveals details about the interview format (e.g., "
                "whether there will be a coding round, how many HR rounds, or if "
                "there is a group discussion) that are not available elsewhere.\n\n"
                "Cultural etiquette matters: arrive 10 minutes early, sit in the front "
                "rows, keep your phone on silent, and stay till the end. When asking "
                "questions, avoid salary-related queries in public — save those for "
                "one-on-one conversations after the PPT."
            ),
            "tips": [
                "Attend every PPT even for companies you are unsure about — information is power.",
                "Prepare 2-3 thoughtful questions about the role, technology stack, or growth path.",
                "Never ask about salary, leaves, or work-from-home policy during the PPT Q&A.",
                "Take notes — the PPT content often appears as HR interview questions.",
                "Introduce yourself to the HR team after the PPT; a warm handshake creates recall.",
                "Dress formally even for the PPT — first impressions start here.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "dream_companies_vs_mass_recruiters",
            "content": (
                "In Indian campus placements there is a clear divide between 'dream' "
                "companies and 'mass recruiters.' Dream companies — Zoho, Freshworks, "
                "Hasura, Razorpay, PayPal, Amazon, or Microsoft — hire selectively, "
                "typically 2-15 students per campus, and offer packages from 8-25+ LPA. "
                "Mass recruiters — TCS, Infosys, Wipro, Cognizant, HCL, Capgemini, "
                "and Accenture — hire in bulk (50-500+ per campus) and offer 3-5 LPA.\n\n"
                "For Tier 3 students, mass recruiters are the safety net. These "
                "companies run their own national-level hiring exams: TCS NQT "
                "(National Qualifier Test), Infosys InfyTQ, Wipro NLTH (National "
                "Level Talent Hunt), and Cognizant GenC. Clearing these exams "
                "guarantees an interview even if the company does not visit your campus.\n\n"
                "The strategic approach is to secure a mass-recruiter offer first and "
                "then prepare aggressively for dream companies. A common mistake Tier 3 "
                "students make is ignoring mass recruiters while aiming only for dream "
                "companies, ending up with no offers at all."
            ),
            "tips": [
                "Register for TCS NQT, InfyTQ, and Wipro NLTH by the August-September deadline.",
                "Secure one mass-recruiter offer for confidence, then aim higher.",
                "Dream-company prep requires LeetCode medium-level proficiency at minimum.",
                "Study company-specific patterns — Zoho loves logical reasoning and C programming.",
                "Freshworks and Razorpay value system design even for freshers — prepare basics.",
                "Do not reject a 3.5 LPA offer thinking 10 LPA will come — be pragmatic.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "off_campus_strategies",
            "content": (
                "Off-campus placements are the primary route for students whose "
                "colleges have limited placement support. In India, off-campus "
                "opportunities come through job portals (Naukri, Internshala, "
                "LinkedIn), company career pages, referral networks, and hiring "
                "challenges on platforms like HackerEarth, HackerRank, and Unstop.\n\n"
                "The most effective off-campus strategy for freshers is the referral "
                "route. Find alumni or connections on LinkedIn who work at your target "
                "company and request a referral with a polished resume and a brief "
                "message explaining why you are a fit. Companies like Google, "
                "Microsoft, Flipkart, and Swiggy actively encourage employee referrals "
                "and your resume gets priority screening.\n\n"
                "Another proven approach is participating in company-sponsored coding "
                "contests. TCS CodeVita, Infosys HackWithInfy, Wipro Elite NTH, and "
                "Amazon WOW (Work on Web) are open to all college students and winners "
                "get direct interview calls or even pre-placement offers. For startups, "
                "AngelList (now Wellfound), YCombinator's Work at a Startup page, and "
                "Twitter/X job postings by founders are goldmines."
            ),
            "tips": [
                "Apply to 15-20 companies per week through LinkedIn Easy Apply and Naukri.",
                "Customize your resume for each application — generic resumes get filtered out.",
                "Participate in CodeVita, HackWithInfy, and Smart Interviews challenges.",
                "Build a LinkedIn presence — post about projects, share learning, engage with tech content.",
                "Ask for referrals politely with a clear message; do not send blank connection requests.",
                "Track applications in a spreadsheet — company, date, status, follow-up date.",
                "Attend hackathons — winners often get fast-tracked interviews at sponsor companies.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "cgpa_cutoffs_by_company",
            "content": (
                "Most Indian companies set a minimum CGPA or percentage cutoff for "
                "campus placements. The cutoffs vary significantly. Top product "
                "companies like Google and Microsoft typically require 7.0+ CGPA (or "
                "70%+). Mass recruiters are more lenient: TCS requires 60% aggregate "
                "with no active backlogs, Infosys requires 60% with no more than one "
                "backlog, Wipro requires 60% with no backlogs, and Cognizant requires "
                "60% with no standing arrears.\n\n"
                "Some companies like Zoho and Freshworks are known for being CGPA-"
                "agnostic — they focus entirely on aptitude and coding skills. Zoho "
                "has historically hired students with CGPAs as low as 5.5 if they "
                "demonstrated strong programming ability.\n\n"
                "For students with low CGPAs (below 6.0), the strategy should focus on "
                "companies without strict cutoffs, off-campus opportunities, and "
                "startups that prioritize skills over academic scores. Building a "
                "strong portfolio with projects, open-source contributions, and "
                "internship experience can compensate for a low CGPA."
            ),
            "tips": [
                "Check exact CGPA cutoffs on your college placement cell's notice board each year.",
                "If your CGPA is below 7.0, prioritize Zoho, startups, and companies with 60% cutoff.",
                "Some companies accept CGPA from the last 4 semesters — calculate that separately.",
                "Internship conversions bypass CGPA cutoffs entirely — pursue internships aggressively.",
                "Keep clearing backlogs on priority; even one active backlog disqualifies you from most drives.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "backlog_policies",
            "content": (
                "Backlogs (also called arrears or KTs) are a critical factor in Indian "
                "campus placements. Companies distinguish between 'active backlogs' "
                "(subjects you have not yet cleared) and 'history of backlogs' (subjects "
                "you failed once but subsequently cleared). Most mass recruiters like "
                "TCS and Wipro require zero active backlogs at the time of joining. "
                "Infosys allows a maximum of one active backlog at the time of the "
                "exam but requires it to be cleared before joining.\n\n"
                "The impact of backlog history varies: TCS and Cognizant typically do "
                "not count cleared backlogs as long as you meet the aggregate percentage. "
                "However, companies like Accenture and Capgemini may ask about backlog "
                "history during HR rounds. Having more than 3-4 backlogs in your history "
                "can be a red flag for some recruiters.\n\n"
                "If you have backlogs, be proactive. Clear them in the supplementary "
                "exams before the placement season (which typically runs August to "
                "January). Some universities allow special exams specifically so students "
                "can clear backlogs before placements — use these opportunities."
            ),
            "tips": [
                "Clear all active backlogs before August of your final year.",
                "Check if your university offers special supplementary exams before placement season.",
                "If asked about backlogs in an interview, be honest but focus on what you learned.",
                "Target companies like Zoho and startups that do not ask about backlog history.",
                "Some service companies have a 'maximum 2 backlog history' policy — verify before applying.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "placement_committee_role",
            "content": (
                "The Placement Committee (or Placement Cell) is a student-run body "
                "under the Training and Placement Officer (TPO) that coordinates all "
                "placement activities. At Tier 2/3 colleges, this committee is crucial "
                "because the TPO alone cannot handle the logistics of multiple company "
                "drives happening simultaneously.\n\n"
                "Student placement coordinators handle company communication, schedule "
                "PPTs, manage student eligibility lists, arrange interview rooms, and "
                "ensure smooth logistics on placement day. Being on the placement "
                "committee has a dual benefit: you get insider information about "
                "upcoming companies and their requirements, and you build networking "
                "skills by interacting with HR professionals directly.\n\n"
                "However, there is a trade-off. Placement coordinators often spend so "
                "much time organizing drives for others that they neglect their own "
                "preparation. The best approach is to join the committee in your "
                "pre-final year, build connections, and then step back during your "
                "final year to focus on your own placements."
            ),
            "tips": [
                "Volunteer for the placement committee in your 3rd year to gain early insights.",
                "Use your coordinator access to understand what companies look for in candidates.",
                "Build personal rapport with HR visitors — they may remember you during interviews.",
                "Do not sacrifice your own preparation for committee duties in your final year.",
                "Maintain a database of company contacts for future off-campus referrals.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "tpo_relationship",
            "content": (
                "The Training and Placement Officer (TPO) is arguably the most "
                "influential person in your placement journey at a Tier 2/3 college. "
                "The TPO maintains relationships with company HR teams, negotiates "
                "which companies visit the campus, and often has the final say on "
                "student eligibility for specific drives.\n\n"
                "In Indian colleges, the TPO-student dynamic is often hierarchical. "
                "Students are expected to be respectful, punctual, and compliant with "
                "placement cell rules. Violating rules — such as not showing up for "
                "a drive you registered for, or rejecting an offer without valid "
                "reason — can lead to being blacklisted from future drives. This is "
                "because 'no-shows' damage the college's reputation with the company.\n\n"
                "Building a positive relationship with the TPO is strategic. Visit "
                "the placement cell, show genuine interest in contributing, and keep "
                "the TPO informed about your career goals. Some TPOs go out of their "
                "way to recommend strong students to specific companies or share "
                "off-campus job leads."
            ),
            "tips": [
                "Introduce yourself to the TPO early in your pre-final year.",
                "Never register for a drive and then skip it — this blacklists you.",
                "If you need to withdraw from a drive, inform the TPO at least 24 hours in advance.",
                "Share your career preferences so the TPO can recommend you to relevant companies.",
                "Volunteer to help with placement logistics — TPOs remember helpful students.",
                "Do not argue with the TPO publicly; escalate concerns through proper channels.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "winter_vs_summer_placements",
            "content": (
                "Indian campus placements follow two primary seasons. The main "
                "placement season runs from August to December of the final year, "
                "with the most prestigious companies visiting in September-October. "
                "The 'winter' or extended placement season runs from January to May "
                "and is for companies that did not fill their quotas or smaller firms "
                "looking for talent.\n\n"
                "Summer placements, on the other hand, refer to internship placements "
                "that happen in January-March of the pre-final year. Summer internships "
                "are increasingly important because many companies — including Amazon, "
                "Microsoft, Goldman Sachs, and even service companies like TCS — offer "
                "Pre-Placement Offers (PPOs) to strong interns, allowing them to skip "
                "the main placement season entirely.\n\n"
                "At Tier 3 colleges, the winter season is often more relevant than the "
                "main season because companies that visit in the extended season tend to "
                "have lower CGPA cutoffs and are more open to students from smaller "
                "institutions."
            ),
            "tips": [
                "Do not get demotivated if you are not placed by December — many good companies come later.",
                "Pursue summer internships aggressively in your pre-final year for PPO chances.",
                "Companies visiting in January-March often have urgent hiring needs and faster decisions.",
                "Use the December gap to improve DSA skills for winter season drives.",
                "Internship-to-PPO conversion rates at top companies are often 50-70% — take internships seriously.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "service_bond_reality",
            "content": (
                "Many IT services companies in India require freshers to sign a "
                "service agreement or 'bond' committing to work for a specific "
                "duration — typically 1 to 3 years. TCS has a bond of 1 year with a "
                "penalty of approximately Rs. 50,000. Infosys does not enforce a formal "
                "bond but expects 12-18 months of service. Wipro historically had a "
                "bond of 15 months. Cognizant does not have a formal bond.\n\n"
                "The enforceability of these bonds is a grey area in Indian labour law. "
                "The Indian Contract Act (Section 27) generally considers restraint of "
                "trade to be void. In practice, most companies do not pursue legal "
                "action against employees who leave before the bond period — but they "
                "may withhold experience letters, deduct from the final settlement, or "
                "make the exit process difficult.\n\n"
                "The practical advice is: honour the bond if possible (1-2 years of "
                "experience is valuable anyway), but do not let bond anxiety prevent "
                "you from accepting an offer. If you must leave early, negotiate "
                "directly with HR — most companies prefer a smooth exit over a messy "
                "legal process."
            ),
            "tips": [
                "Read the bond agreement carefully before signing — understand the penalty amount.",
                "TCS bond penalty of ~50,000 INR is manageable if you get a significantly better offer.",
                "Most bonds are not legally enforceable, but companies may withhold experience letters.",
                "Complete at least the bond period to build a clean professional record.",
                "If you must leave early, discuss with your manager first — some waive the bond for good performers.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "notice_period_freshers",
            "content": (
                "Notice periods for freshers in Indian IT companies vary. Most service "
                "companies have a 30-day notice period for employees within their first "
                "year, which may increase to 60-90 days after the first year. Some "
                "product companies like Flipkart and Myntra have a 60-day notice period "
                "from day one. Startups typically have 15-30 day notice periods.\n\n"
                "During the notice period, you are expected to complete a knowledge "
                "transfer (KT) to your replacement or team members, return company "
                "assets (laptop, ID card), and clear all pending work. Some companies "
                "offer a 'notice period buyout' where your new employer pays your "
                "current company to release you immediately — this is common in "
                "product companies and the cost is typically 1-2 months' salary.\n\n"
                "For freshers, the notice period is also the most vulnerable time "
                "professionally. Do not badmouth your current employer, do not slack "
                "off during the notice period, and ensure a clean exit. Your experience "
                "letter and background verification depend on a proper handover."
            ),
            "tips": [
                "Check your offer letter for the exact notice period clause before joining.",
                "Negotiate a shorter notice period at the time of joining if possible.",
                "During notice period, complete KT professionally — your reputation follows you.",
                "Ask your new employer if they offer notice period buyout before resigning.",
                "Never abscond — it leads to a negative remark in background verification.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "relocation_expectations",
            "content": (
                "Relocation is a standard expectation for campus hires in India. Most "
                "IT services companies have multiple offices and freshers are typically "
                "assigned to a location based on business needs — not personal "
                "preference. TCS may send you to any of its 100+ offices across India. "
                "Infosys typically assigns freshers to Mysuru for training and then "
                "relocates them to Bangalore, Hyderabad, Pune, or Chennai. Wipro and "
                "Cognizant have similar multi-city assignment policies.\n\n"
                "Location preferences are collected during onboarding, but there is "
                "no guarantee. Students from Tamil Nadu hoping to stay in Chennai, or "
                "students from Andhra Pradesh wanting Hyderabad, may be sent to Pune "
                "or Kolkata instead. This is a reality that Tier 2/3 students — many "
                "of whom have never lived away from home — must prepare for.\n\n"
                "Product companies and startups are more predictable with locations. "
                "Zoho is primarily Chennai-based, Freshworks is Chennai/Bangalore, "
                "Flipkart is Bangalore, and Razorpay is Bangalore. If location is "
                "important to you, factor it into your company choices."
            ),
            "tips": [
                "Mentally prepare for relocation to any metro city — flexibility increases your options.",
                "Budget Rs. 15,000-25,000 for initial relocation costs (deposit, essentials, travel).",
                "Connect with batchmates being posted to the same city for shared accommodation.",
                "If location is critical, target companies known for specific cities (Zoho for Chennai).",
                "After 6-12 months, you can request an internal transfer — but do not rely on it.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "probation_period",
            "content": (
                "Almost all Indian companies place freshers on a probation period — "
                "typically 3-6 months — during which your performance is closely "
                "monitored and termination is easier. During probation, your notice "
                "period is usually shorter (7-15 days instead of 30-90 days), and you "
                "may not be eligible for certain benefits like health insurance top-ups "
                "or performance bonuses.\n\n"
                "At IT services companies, the probation period often coincides with "
                "the initial training phase. TCS Xplore (previously TCS ILP) and "
                "Infosys Global Education Centre in Mysuru have training programs "
                "lasting 2-4 months. Performance in these training programs determines "
                "your project allocation and sometimes your role designation (e.g., "
                "Infosys Systems Engineer vs. Power Programmer).\n\n"
                "Failure during probation is rare but not impossible. Students who "
                "consistently score poorly in training assessments, show attendance "
                "issues, or exhibit behavioural problems can be let go. Treat the "
                "probation period like an extended interview — perform well and "
                "you will be confirmed."
            ),
            "tips": [
                "Treat the first 6 months as an extended interview — show enthusiasm and reliability.",
                "Attend all training sessions and score well on assessments — they affect project allocation.",
                "Build relationships with your training batch — they become your professional network.",
                "Do not take leaves during probation unless absolutely necessary.",
                "Ask for feedback regularly from your manager or training coordinator.",
            ],
        },
        {
            "category": "campus_placement",
            "topic": "lateral_vs_campus",
            "content": (
                "Campus placement means getting hired while still in college through "
                "on-campus drives. Lateral hiring means applying to companies after "
                "gaining work experience — typically 1-3 years. In India, the switch "
                "from a service company (campus placement at 3-4 LPA) to a product "
                "company (lateral hire at 8-15 LPA) is one of the most common and "
                "lucrative career transitions in tech.\n\n"
                "The lateral hiring process is very different from campus placements. "
                "There are no aptitude tests — the focus is on Data Structures and "
                "Algorithms (DSA), System Design (for 2+ years of experience), and "
                "domain knowledge. Companies like Flipkart, Swiggy, PhonePe, Paytm, "
                "and Atlassian actively hire laterally from service companies, and "
                "they specifically look for candidates who have done real project work "
                "beyond just 'support and maintenance.'\n\n"
                "The typical timeline for a successful lateral switch is: join a "
                "service company, gain 1.5-2 years of experience, prepare DSA for "
                "3-6 months alongside work, crack interviews at product companies, "
                "and make the switch with a 100-200% salary hike. This is the most "
                "well-trodden path for Tier 3 college graduates to reach top companies."
            ),
            "tips": [
                "Plan for a lateral switch from Day 1 if your campus placement is at a service company.",
                "Start DSA preparation on LeetCode 6 months before you plan to switch.",
                "Target 150-200 LeetCode problems (mix of easy, medium, hard) for lateral interviews.",
                "System Design basics (HLD) become important for roles at 2+ years of experience.",
                "A lateral switch from TCS/Infosys to Flipkart/Swiggy can mean a jump from 4 to 12-18 LPA.",
                "Keep your current job performance strong — you need a good reference and experience letter.",
            ],
        },
        # =====================================================================
        # INTERVIEW CULTURE (10 entries)
        # =====================================================================
        {
            "category": "interview_culture",
            "topic": "greeting_etiquette",
            "content": (
                "Greeting etiquette in Indian interviews has cultural nuances that "
                "differ from Western norms. In campus placements, you typically enter "
                "the interview room, make eye contact with the interviewer(s), say "
                "'Good morning/afternoon, sir/ma'am,' and wait to be asked to sit. "
                "Using 'sir' and 'ma'am' is standard and expected in Indian "
                "professional settings — it is not considered overly formal.\n\n"
                "Handshakes are common in corporate interviews, especially at MNCs "
                "and product companies. Keep the handshake firm but not crushing. In "
                "more traditional settings (government PSU interviews, some South "
                "Indian companies), a slight nod or folded hands (namaste) may be "
                "more appropriate. Read the room — if the interviewer extends a hand, "
                "reciprocate; if not, a polite verbal greeting suffices.\n\n"
                "When there is a panel of interviewers, greet the room collectively "
                "('Good morning, everyone') rather than individually. Make eye contact "
                "with each panel member briefly. Address questions to the person who "
                "asked them but periodically look at other panel members too."
            ),
            "tips": [
                "Always say 'Good morning/afternoon' with the appropriate sir/ma'am honorific.",
                "Wait for the interviewer to ask you to sit before taking a seat.",
                "A firm handshake is safe for MNC interviews; gauge the setting for others.",
                "Carry a folder with resume copies, certificates, and a pen — it shows preparedness.",
                "Smile naturally when greeting — nervousness is normal but a smile eases the tension.",
            ],
        },
        {
            "category": "interview_culture",
            "topic": "dress_code_campus_vs_corporate",
            "content": (
                "For campus placements at Indian colleges, the standard dress code is "
                "formal: men wear a light-coloured full-sleeve shirt, dark trousers, "
                "leather belt, and polished formal shoes. A tie is optional but adds "
                "a professional touch. Women wear a formal salwar-kameez, saree, or "
                "Western formals (blouse with trousers or a formal kurta with "
                "trousers). Avoid flashy colours, heavy jewellery, or strong perfume.\n\n"
                "For corporate interviews at company offices, the dress code may be "
                "slightly more relaxed, especially at startups and product companies. "
                "Companies like Flipkart, Swiggy, and Zomato have casual dress "
                "cultures, but you should still dress one level above the company's "
                "norm for an interview. A clean polo shirt with chinos is acceptable "
                "for startup interviews.\n\n"
                "Virtual interviews have their own considerations. Wear formal attire "
                "from head to toe (not just the visible part) as you may need to stand "
                "up unexpectedly. Ensure your background is clean and well-lit. "
                "Avoid sitting on your bed — use a desk or table with a neutral "
                "background."
            ),
            "tips": [
                "For campus placements: full formals, no exceptions. Iron your clothes the night before.",
                "For startup interviews: smart casuals (collared t-shirt, clean jeans) are acceptable.",
                "Women can wear Indian or Western formals — comfort and confidence matter most.",
                "Keep a dedicated 'interview outfit' ready — do not scramble on the morning of.",
                "Groom well: trimmed nails, neat hair, minimal cologne, polished shoes.",
                "In virtual interviews, test your camera angle and lighting 30 minutes before.",
            ],
        },
        {
            "category": "interview_culture",
            "topic": "virtual_interview_setup",
            "content": (
                "Since 2020, virtual interviews have become a permanent part of Indian "
                "hiring, especially for initial screening rounds. Companies like TCS, "
                "Infosys, Wipro, and Cognizant conduct their mass hiring entirely "
                "online through their own platforms (TCS iON, Infosys HackWithInfy). "
                "Product companies use Zoom, Google Meet, or Microsoft Teams for "
                "interviews.\n\n"
                "The biggest challenge for Tier 2/3 students is infrastructure: "
                "unreliable internet connections, shared living spaces with noise, "
                "and lack of a proper desk setup. These are real problems that need "
                "real solutions — borrow a friend's quiet room, go to a library or "
                "coworking space, or use your college's computer lab if available.\n\n"
                "Technical setup matters enormously. Use a laptop (not a phone), "
                "ensure a stable internet connection (minimum 5 Mbps), use wired "
                "earphones with a microphone (not Bluetooth — they disconnect), "
                "and have a backup plan (mobile hotspot, nearby friend with wifi). "
                "Test the interview platform 24 hours before the interview to "
                "ensure there are no compatibility issues."
            ),
            "tips": [
                "Test your setup 24 hours before — camera, microphone, internet, and platform.",
                "Use wired earphones with a mic, not Bluetooth — they are more reliable.",
                "Keep a mobile hotspot ready as backup internet.",
                "Sit against a plain wall or use a professional virtual background.",
                "Close all unnecessary browser tabs and applications to avoid notifications.",
                "Keep water, a pen, and blank paper on your desk — you may need to jot notes.",
                "Look into the camera, not the screen, to maintain virtual eye contact.",
            ],
        },
        {
            "category": "interview_culture",
            "topic": "panel_dynamics_reading_room",
            "content": (
                "Panel interviews — where 2-4 interviewers simultaneously assess you "
                "— are common in Indian campus placements, especially for IT services "
                "companies and PSUs. Understanding panel dynamics can significantly "
                "improve your performance. Typically, one panel member leads the "
                "questioning while others observe and take notes. The lead may "
                "alternate between technical and HR questions.\n\n"
                "Learning to 'read the room' is a crucial soft skill. If an "
                "interviewer leans forward and nods, they are engaged — elaborate on "
                "your answer. If they look at their watch, start writing, or look at "
                "another panel member, wrap up your answer concisely. If a technical "
                "interviewer asks an increasingly difficult sequence of questions, "
                "they are probing your depth — it is okay to say 'I am not sure about "
                "this specific area, but here is my approach to figuring it out.'\n\n"
                "In Indian panels, there is often a 'stress interviewer' who "
                "deliberately challenges your answers, questions your confidence, "
                "or asks provocative questions like 'Why should we hire you when "
                "there are IIT students available?' This is a test of composure, "
                "not a personal attack. Stay calm, answer with data and examples, "
                "and do not get defensive."
            ),
            "tips": [
                "Address your answer to the person who asked, but briefly look at other panelists.",
                "If a panelist seems disengaged, do not try to win them over — focus on the questioner.",
                "When a 'stress question' comes, pause for 2 seconds, smile, and respond calmly.",
                "If asked 'Why not an IIT student?', focus on your unique strengths, not IIT bashing.",
                "Watch for cues to wrap up — if the panel looks satisfied, do not over-elaborate.",
            ],
        },
        {
            "category": "interview_culture",
            "topic": "waiting_room_behavior",
            "content": (
                "The waiting room during campus placements is a high-stress "
                "environment where 50-200 students may be waiting for their turn. How "
                "you conduct yourself here matters more than you think. HR "
                "representatives sometimes observe candidates in the waiting area to "
                "assess their behaviour — are they calm and composed, or anxious and "
                "disruptive?\n\n"
                "Common waiting room mistakes include: loudly discussing answers from "
                "previous rounds (which may reach other candidates and interviewers), "
                "spreading panic by saying 'the questions were very tough,' showing "
                "off by listing your achievements to others, or spending the entire "
                "time on your phone. None of these help your cause.\n\n"
                "Use the waiting time productively. Quietly review your resume — the "
                "interviewer will ask about the projects and skills listed on it. "
                "Mentally rehearse your self-introduction (keep it under 90 seconds). "
                "Review the company information from the PPT. If there is a long wait, "
                "it is acceptable to politely ask the coordinator for an estimated time."
            ),
            "tips": [
                "Do not discuss previous round questions loudly — it can disqualify you.",
                "Review your resume and practice your self-introduction while waiting.",
                "Avoid forming large groups that create noise — sit with 1-2 close friends quietly.",
                "Keep your phone on silent and avoid scrolling social media visibly.",
                "Carry a book or notes related to the company — reading shows seriousness.",
            ],
        },
        {
            "category": "interview_culture",
            "topic": "thank_you_followup",
            "content": (
                "The culture of thank-you notes after interviews is growing in India "
                "but is still not as prevalent as in the US. In campus placements, "
                "thank-you emails are rare because you often do not have the "
                "interviewer's personal email. However, for off-campus interviews — "
                "especially at startups and product companies — a brief thank-you "
                "email within 24 hours can make a positive impression.\n\n"
                "The thank-you note should be concise: thank the interviewer for "
                "their time, reference a specific topic discussed during the interview "
                "to show engagement, and reiterate your interest in the role. Keep it "
                "under 5 sentences. Do not use this as an opportunity to explain or "
                "correct answers you gave during the interview — that comes across as "
                "insecure.\n\n"
                "On LinkedIn, connecting with your interviewer after an off-campus "
                "interview is acceptable but not during the process. Wait until the "
                "hiring decision is made. If you are selected, connect and thank them. "
                "If you are rejected, connecting and asking for feedback is a mature "
                "move that may lead to future opportunities."
            ),
            "tips": [
                "For off-campus interviews, send a brief thank-you email within 24 hours.",
                "Reference something specific from the interview to make it personal.",
                "Do not write long thank-you emails — 3-5 sentences are ideal.",
                "Do not send thank-you messages during campus placements — it is unusual.",
                "Connect on LinkedIn after the process concludes, not during it.",
            ],
        },
        {
            "category": "interview_culture",
            "topic": "body_language_indian_context",
            "content": (
                "Body language in Indian interviews carries weight but is interpreted "
                "through cultural context. Maintaining eye contact is important, but "
                "unbroken staring can be perceived as aggressive in Indian culture. "
                "The ideal is to maintain eye contact for 3-4 seconds, briefly look "
                "away (at your hands or notes), and re-establish eye contact. This "
                "shows confidence without intimidation.\n\n"
                "Posture matters. Sit up straight with your back against the chair, "
                "feet flat on the floor, and hands on the table or your lap. Avoid "
                "crossing your arms (defensive), slouching (uninterested), or "
                "fidgeting with a pen (nervous). Leaning slightly forward when "
                "listening shows interest.\n\n"
                "Indian cultural norms around body language differ from Western ones. "
                "Head wobbling (the characteristic Indian head shake) is a natural "
                "gesture that indicates agreement or understanding — do not try to "
                "suppress it, but also do not overdo it. Pointing with your finger is "
                "considered rude in many Indian cultures — use an open palm to "
                "gesture instead. Nodding while the interviewer speaks shows you are "
                "actively listening."
            ),
            "tips": [
                "Maintain natural eye contact — 3-4 seconds on, brief break, then reconnect.",
                "Sit upright with an open posture — no crossed arms or hunched shoulders.",
                "Nod occasionally when the interviewer speaks to show active listening.",
                "Use hand gestures moderately to emphasize points — too much is distracting.",
                "Avoid touching your face or hair repeatedly — it signals nervousness.",
                "Practice your body language in mock interviews with friends.",
            ],
        },
        {
            "category": "interview_culture",
            "topic": "english_accent_anxiety",
            "content": (
                "Many students from Tier 2/3 colleges, especially those from Tamil, "
                "Telugu, or Hindi-medium backgrounds, experience anxiety about their "
                "English accent during interviews. This anxiety is often exaggerated "
                "— interviewers at Indian companies are familiar with regional accents "
                "and do not judge based on how 'American' your English sounds.\n\n"
                "What matters far more than accent is clarity and structure. Speak "
                "clearly, at a moderate pace, and in complete sentences. Avoid mixing "
                "languages mid-sentence (code-switching with Hindi or Tamil words) "
                "during formal interviews, though this is perfectly acceptable in "
                "casual startup interviews. Use simple, direct language rather than "
                "trying to use complex vocabulary that you are unsure about.\n\n"
                "If English is genuinely a weak area, invest 30 minutes daily in "
                "improvement. Watch English tech talks on YouTube (channels like "
                "Fireship, TechWithTim, or Traversy Media), practice thinking in "
                "English, and speak English with friends for at least 30 minutes "
                "daily. Record yourself answering common interview questions and "
                "listen back to identify areas for improvement."
            ),
            "tips": [
                "Clarity matters more than accent — speak slowly and clearly.",
                "Practice answering 10 common HR questions in English daily for 2 weeks.",
                "Record yourself and listen back — you will catch filler words like 'umm' and 'basically'.",
                "Watch English tech content on YouTube to naturally improve fluency.",
                "Do not apologize for your accent — it is part of who you are.",
                "If you do not understand a question, ask the interviewer to repeat — this is normal.",
                "Use the STAR method (Situation, Task, Action, Result) to structure answers clearly.",
            ],
        },
        {
            "category": "interview_culture",
            "topic": "technical_vs_hr_different_styles",
            "content": (
                "Indian interviews typically have two distinct phases: the technical "
                "round(s) and the HR round. These require fundamentally different "
                "preparation and styles. The technical round tests your knowledge of "
                "programming, data structures, databases, operating systems, and "
                "project work. The HR round tests your personality, communication, "
                "cultural fit, and professional maturity.\n\n"
                "In technical rounds at service companies (TCS, Infosys, Wipro), "
                "expect questions on basic programming (C, Java, Python), DBMS (SQL "
                "queries, normalization), OS (deadlocks, process scheduling), and CN "
                "(OSI layers, TCP/IP). At product companies, expect LeetCode-style "
                "coding problems. The style is direct: write code, explain your "
                "approach, discuss time complexity.\n\n"
                "HR rounds in India cover standard topics: 'Tell me about yourself,' "
                "'Why this company?', 'Where do you see yourself in 5 years?', "
                "'Are you willing to relocate?', and 'What is your expected salary?' "
                "The biggest mistake freshers make is treating the HR round casually. "
                "Many technically strong candidates are rejected in the HR round for "
                "showing arrogance, poor communication, or giving canned answers."
            ),
            "tips": [
                "Prepare for technical and HR rounds as completely separate exams.",
                "For service company technicals: revise DBMS, OS, CN, and OOPS fundamentals.",
                "For product company technicals: solve at least 100 LeetCode problems.",
                "For HR rounds: prepare genuine, personalized answers — not memorized scripts.",
                "When asked 'What is your expected salary?', say 'As per company standards' for mass recruiters.",
                "Practice mock HR interviews with friends — delivery matters as much as content.",
            ],
        },
        {
            "category": "interview_culture",
            "topic": "group_discussion_survival",
            "content": (
                "Group Discussions (GDs) are used by many Indian companies — "
                "especially IT services firms, banks, and MBA programs — as a "
                "screening round before interviews. In a typical GD, 8-12 candidates "
                "are given a topic (e.g., 'Is AI a threat to jobs?', 'Should college "
                "education be mandatory for tech jobs?') and must discuss it for "
                "15-20 minutes while evaluators observe.\n\n"
                "GDs in India test four things: communication skills, leadership, "
                "teamwork, and subject knowledge. The common mistake is trying to "
                "dominate the discussion by speaking the most. Evaluators actually "
                "penalize overly aggressive participants who interrupt others or "
                "repeat the same point. Quality of contribution matters more than "
                "quantity of airtime.\n\n"
                "The ideal GD strategy: speak early (within the first 2 minutes) to "
                "establish presence, make 3-4 substantive points backed by examples "
                "or data, acknowledge and build on others' points ('I agree with "
                "what Priya said, and I'd like to add...'), and summarize if you "
                "get the chance. Avoid personal attacks, emotional arguments, or "
                "factual claims you cannot support."
            ),
            "tips": [
                "Speak within the first 2 minutes — initiators are noticed positively.",
                "Make 3-4 quality points rather than repeating the same idea 10 times.",
                "Build on others' points using phrases like 'Adding to what X said...'",
                "If the GD becomes chaotic, be the person who brings structure — 'Can we consider this from another angle?'",
                "Avoid being a 'fishmarket' participant — interrupting constantly is penalized.",
                "If you are naturally quiet, practice GDs with friends weekly for a month before placements.",
                "Read newspapers (The Hindu, Economic Times) for 30 minutes daily — GD topics often come from current affairs.",
            ],
        },
        # =====================================================================
        # SALARY NEGOTIATION (8 entries)
        # =====================================================================
        {
            "category": "salary_negotiation",
            "topic": "fresher_dont_negotiate_mass_recruiters",
            "content": (
                "A crucial reality for Indian freshers: do not try to negotiate "
                "salary with mass recruiters like TCS, Infosys, Wipro, Cognizant, or "
                "HCL. These companies have fixed CTC bands for campus hires — "
                "typically 3.36 LPA (TCS), 3.6 LPA (Infosys Systems Engineer), "
                "4.25 LPA (Infosys Digital Specialist Engineer), 3.5 LPA (Wipro), "
                "and 4.0 LPA (Cognizant GenC Next). These are non-negotiable packages "
                "offered to thousands of students across India.\n\n"
                "Attempting to negotiate can backfire — the HR team may perceive you "
                "as someone who does not understand how mass hiring works, or worse, "
                "as arrogant. When asked 'What is your expected salary?', the safe "
                "answer is 'I am open to the company's standard compensation for "
                "freshers.' This shows maturity and realism.\n\n"
                "The exception is when you have a competing offer from a product "
                "company or a premium role within the same company. For instance, if "
                "you qualify for TCS Digital (7-7.5 LPA) instead of TCS Ninja "
                "(3.36 LPA), that higher package is earned through the exam, not "
                "negotiation."
            ),
            "tips": [
                "Never negotiate salary with mass recruiters — the packages are fixed for all freshers.",
                "When asked about expected salary, say 'As per company norms for freshers.'",
                "Focus on getting the 'premium' role (TCS Digital, Infosys Power Programmer) through exams.",
                "Your first salary is a starting point — plan for a significant jump within 2-3 years.",
                "Instead of negotiating salary, ask about role preferences or location choices.",
            ],
        },
        {
            "category": "salary_negotiation",
            "topic": "lateral_negotiation_tactics",
            "content": (
                "Lateral hiring (switching jobs with experience) is where real salary "
                "negotiation happens in India. The standard expectation is a 30-50% "
                "hike when switching companies, though jumps of 80-150% are common "
                "when moving from service to product companies. For example, a TCS "
                "employee earning 5 LPA can realistically negotiate 10-14 LPA at "
                "Flipkart, Swiggy, or similar product companies.\n\n"
                "Key tactics for lateral negotiation: always have a competing offer "
                "or at least be in the interview pipeline at multiple companies. When "
                "asked about your current CTC, you are legally allowed to share it "
                "but also mention your 'expected CTC' based on market rates. Use "
                "platforms like Glassdoor India, Levels.fyi (for product companies), "
                "and AmbitionBox to research salary ranges for your target role and "
                "experience level.\n\n"
                "The negotiation conversation typically happens with the HR recruiter "
                "after you clear technical rounds. Frame your ask as: 'Based on my "
                "skills, experience, and the market range for this role, my expected "
                "CTC is X-Y LPA.' Always give a range, and make the lower end of "
                "your range the minimum you would accept."
            ),
            "tips": [
                "Research salary ranges on Glassdoor, AmbitionBox, and Levels.fyi before negotiating.",
                "Always have a competing offer — it is your strongest leverage.",
                "Give a salary range where the bottom is your acceptable minimum.",
                "Do not reveal your current CTC unless specifically asked — share expected CTC instead.",
                "Negotiate over email when possible — it gives you time to think and creates a record.",
                "If the base salary is fixed, negotiate joining bonus, relocation allowance, or stock options.",
                "Never accept on the spot — say 'Thank you, I will review and respond by [date].'",
            ],
        },
        {
            "category": "salary_negotiation",
            "topic": "ctc_breakdown_components",
            "content": (
                "Understanding CTC (Cost to Company) breakup is essential for every "
                "Indian professional. CTC is NOT your take-home salary — it includes "
                "every cost the company incurs on you. A typical CTC of 4 LPA at an "
                "IT services company breaks down roughly as: Basic Salary (40% = "
                "1.6 LPA), HRA (20% = 0.8 LPA), Special Allowance (15% = 0.6 LPA), "
                "PF (Employer Contribution, 12% of Basic = 0.19 LPA), Gratuity "
                "(4.8% of Basic = 0.077 LPA), Medical Insurance (0.15 LPA), and "
                "Variable Pay (rest).\n\n"
                "The gap between CTC and in-hand salary shocks most freshers. From "
                "a 4 LPA CTC, your monthly in-hand salary will be approximately "
                "Rs. 25,000-28,000 after deductions for PF (employee share), "
                "professional tax, and income tax. The variable component (often "
                "10-15% of CTC) is not guaranteed — it depends on company and "
                "individual performance.\n\n"
                "At higher CTCs (10+ LPA), the breakup becomes more complex with "
                "components like ESOP/RSU (stock options), performance bonuses, "
                "NPS contributions, meal coupons (Sodexo), LTA (Leave Travel "
                "Allowance), and car lease components. Understanding each component "
                "helps you compare offers accurately rather than just comparing "
                "headline CTC numbers."
            ),
            "tips": [
                "Always ask for the full CTC breakup in writing before accepting an offer.",
                "Compare in-hand monthly salary, not just CTC — that is what you actually receive.",
                "Variable pay (bonus) is NOT guaranteed — do not count it as assured income.",
                "PF contributions (both employer and employee) are locked until retirement/resignation.",
                "Use online CTC calculators (IncomeTaxIndia, ClearTax) to estimate your take-home.",
                "If two offers have similar CTC, choose the one with a higher fixed component.",
            ],
        },
        {
            "category": "salary_negotiation",
            "topic": "in_hand_vs_ctc_reality",
            "content": (
                "The difference between CTC and in-hand salary is one of the most "
                "misunderstood aspects of Indian compensation. Here is a realistic "
                "breakdown at different CTC levels:\n\n"
                "At 3.5 LPA CTC (typical mass recruiter): Monthly in-hand is "
                "approximately Rs. 22,000-25,000. At 6 LPA CTC: Monthly in-hand is "
                "approximately Rs. 38,000-42,000. At 10 LPA CTC: Monthly in-hand "
                "is approximately Rs. 58,000-65,000. At 15 LPA CTC: Monthly in-hand "
                "is approximately Rs. 80,000-90,000. At 25 LPA CTC: Monthly in-hand "
                "is approximately Rs. 1,20,000-1,40,000. These are approximate "
                "figures assuming the new tax regime and standard deductions.\n\n"
                "The key deductions that reduce your CTC to in-hand are: Employee PF "
                "contribution (12% of basic), Professional Tax (Rs. 200/month in most "
                "states), Income Tax (based on slab), and any recovery for company "
                "benefits (health insurance premium, food coupon contributions). "
                "Additionally, components like gratuity (payable after 5 years), "
                "employer PF, and insurance premiums are part of CTC but never "
                "reach your bank account directly."
            ),
            "tips": [
                "A 4 LPA offer means ~25K/month in hand, not 33K — budget accordingly.",
                "Ask HR for a 'salary slip sample' to understand exact in-hand before joining.",
                "In-hand salary varies by city due to different professional tax rates.",
                "New tax regime vs old regime choice affects your take-home — calculate both.",
                "Food coupons (Sodexo/Zeta) are tax-free up to Rs. 50/meal — they save real money.",
            ],
        },
        {
            "category": "salary_negotiation",
            "topic": "stock_options_indian_startups",
            "content": (
                "Employee Stock Options (ESOPs) are increasingly common in Indian "
                "startups, but freshers and early-career professionals often "
                "misunderstand their value. ESOPs give you the right to buy company "
                "shares at a predetermined price (strike price) after a vesting "
                "period — typically 4 years with a 1-year cliff. This means you get "
                "nothing if you leave before 1 year, 25% after 1 year, and the rest "
                "vests monthly or quarterly over the next 3 years.\n\n"
                "At well-funded startups like Razorpay, CRED, Zerodha, Meesho, or "
                "PhonePe, ESOPs can be worth substantial money if the company goes "
                "public (IPO) or gets acquired. For example, early employees at "
                "Freshworks reportedly earned Rs. 1-5 crore from ESOPs when the "
                "company went public on NASDAQ in 2021. However, for every "
                "Freshworks, there are hundreds of startups whose ESOPs became "
                "worthless because the company shut down or never went public.\n\n"
                "When evaluating ESOP offers, ask: What is the current valuation? "
                "What is the vesting schedule? Is there a buyback policy? What happens "
                "to vested ESOPs if you leave? Tax implications are also important — "
                "ESOPs are taxed at exercise (when you buy them) and again at sale "
                "(capital gains), which can be a significant financial hit if the "
                "company has not gone public yet."
            ),
            "tips": [
                "Do not treat ESOPs as cash equivalent — they are high-risk, high-reward.",
                "Ask about the vesting schedule, cliff period, and exercise window explicitly.",
                "Check if the company has an ESOP buyback policy — this lets you sell shares before IPO.",
                "Prefer a higher base salary over ESOPs unless the startup is clearly on an IPO path.",
                "Understand the tax implications: ESOPs are taxed as perquisite on exercise.",
                "Research the company's funding round and valuation to estimate ESOP value.",
            ],
        },
        {
            "category": "salary_negotiation",
            "topic": "joining_bonus_negotiation",
            "content": (
                "Joining bonuses are one-time payments made to new hires, typically "
                "ranging from Rs. 50,000 to Rs. 5,00,000+ depending on the company "
                "and level. In Indian tech, joining bonuses are common at product "
                "companies and startups for lateral hires but are rare for campus "
                "freshers from Tier 2/3 colleges.\n\n"
                "Companies offer joining bonuses to bridge the gap when they cannot "
                "meet a candidate's salary expectations through the regular CTC. For "
                "example, if you are asking for 15 LPA and the company's band for "
                "your role caps at 13 LPA, they might offer a Rs. 2,00,000 joining "
                "bonus to make the total first-year compensation close to 15 LPA.\n\n"
                "Important catch: joining bonuses usually come with a clawback clause. "
                "If you leave within 1 year (sometimes 2 years), you must return the "
                "full bonus amount. This is legally enforceable in India. Also, "
                "joining bonuses are fully taxable as income in the year received, "
                "so a Rs. 2,00,000 joining bonus may net you only Rs. 1,40,000 after "
                "30% tax."
            ),
            "tips": [
                "Joining bonuses are negotiable when the base salary hits its ceiling.",
                "Always read the clawback clause — know how long you must stay to keep the bonus.",
                "Factor in taxes — a 2 LPA joining bonus nets ~1.4 LPA after 30% tax bracket.",
                "Request the joining bonus to be paid in the first month's payroll for tax efficiency.",
                "If choosing between two offers, the one without a joining bonus but higher base is usually better long-term.",
            ],
        },
        {
            "category": "salary_negotiation",
            "topic": "retention_bonus",
            "content": (
                "Retention bonuses are paid to employees companies want to keep — "
                "usually after 2-3 years of service or when the employee receives "
                "an outside offer. In the Indian IT industry, retention bonuses have "
                "become common during periods of high attrition, such as 2021-2022 "
                "when mass resignations hit service companies.\n\n"
                "Typical retention bonus structures at Indian companies: TCS offers "
                "retention bonuses ranging from Rs. 50,000 to Rs. 3,00,000 for "
                "high-performing employees with 2+ years of tenure. Infosys rolled "
                "out retention bonuses of Rs. 1-2 LPA for employees in the 2-5 year "
                "band during the 2021 attrition crisis. Product companies may offer "
                "even higher retention packages — Rs. 5-15 LPA in additional RSUs or "
                "cash bonuses.\n\n"
                "How to trigger a retention bonus: the most common way is to have a "
                "competing offer letter. When you inform your manager that you have "
                "received an offer at a higher CTC, the company may counter with a "
                "retention bonus. However, this strategy has risks — your loyalty may "
                "be questioned, and you might be first on the list during layoffs."
            ),
            "tips": [
                "Do not seek retention bonuses just for the money — it can damage trust.",
                "If you genuinely want to stay, a retention bonus is a fair negotiation.",
                "Get the retention bonus details in writing — verbal promises are unreliable.",
                "Retention bonuses usually come with a 1-2 year lock-in — factor this in.",
                "Do not use fake offer letters to trigger a retention bonus — background checks will expose this.",
            ],
        },
        {
            "category": "salary_negotiation",
            "topic": "notice_period_buyout",
            "content": (
                "Notice period buyout is when your new employer compensates your "
                "current employer to release you before your notice period ends. This "
                "is increasingly common in Indian tech hiring where notice periods "
                "range from 30 to 90 days, and companies want new hires to join quickly.\n\n"
                "How it typically works: if you have a 60-day notice period at TCS and "
                "your new employer (say Flipkart) wants you to join in 30 days, "
                "Flipkart may pay TCS the equivalent of 30 days' salary to release "
                "you early. The cost is borne entirely by the new employer and is "
                "separate from your compensation. Some companies include notice period "
                "buyout as part of the offer letter; others process it on a case-by-case "
                "basis.\n\n"
                "Not all companies agree to release employees on buyout. Service "
                "companies like TCS and Infosys have formal early-release processes "
                "but may still require 15-30 days minimum. Startups and smaller "
                "companies may not have a formal buyout policy but can be flexible "
                "if you negotiate directly. Always discuss the notice period timeline "
                "with both your current and new employer to avoid complications."
            ),
            "tips": [
                "Ask your new employer during offer stage if they support notice period buyout.",
                "Some companies advertise 'immediate joining' but do not actually pay for buyout — clarify.",
                "Negotiate with your current manager for early release even without formal buyout.",
                "If you have a 90-day notice period, start the discussion early — many companies will not wait 90 days.",
                "Never abscond from your current company — it leads to BGV (background verification) failure.",
            ],
        },
        # =====================================================================
        # COMMON MISTAKES (5 entries)
        # =====================================================================
        {
            "category": "common_mistakes",
            "topic": "fresher_common_mistakes",
            "content": (
                "Freshers from Tier 2/3 Indian colleges make predictable mistakes "
                "during placements that are easily avoidable with awareness. The most "
                "common mistake is inadequate preparation — relying on college "
                "curriculum instead of dedicated placement preparation. College exams "
                "test theory, but placement exams test application: writing code on "
                "paper, solving aptitude problems under time pressure, and communicating "
                "clearly in English.\n\n"
                "Another major mistake is poor resume writing. Freshers either stuff "
                "their resume with every technology they have heard of (listing Java, "
                "Python, C++, JavaScript, React, Angular, Node.js, AWS, Docker, "
                "Kubernetes when they have only written basic programs in Java) or "
                "write resumes that look like a marksheet (listing subjects instead "
                "of projects and skills). The resume should be 1 page, project-focused, "
                "and honest about skill levels.\n\n"
                "The third critical mistake is not practising mock interviews. Many "
                "students can solve problems on paper but freeze when asked to explain "
                "their approach verbally. The interview is not just about getting the "
                "right answer — it is about demonstrating thought process, handling "
                "pressure, and communicating effectively."
            ),
            "tips": [
                "Start placement preparation at least 6 months before placement season (begin in January/February of pre-final year).",
                "Keep your resume to 1 page with honest, verifiable skills and 2-3 real projects.",
                "Practice mock interviews — ask a friend to grill you on your resume and projects.",
                "Do not list skills you cannot discuss for 5 minutes in an interview.",
                "Solve 50+ aptitude questions from IndiaBIX or Placement Preparation before quant rounds.",
                "Prepare your self-introduction so well that you can deliver it at 3 AM if woken up.",
                "Research each company before its drive — 'Why do you want to join us?' is always asked.",
            ],
        },
        {
            "category": "common_mistakes",
            "topic": "experienced_common_mistakes",
            "content": (
                "Experienced professionals (2-7 years) in Indian tech make their own "
                "set of interview mistakes. The biggest is jumping into lateral "
                "interviews without adequate DSA preparation. Service-company "
                "professionals who have spent years doing support, testing, or "
                "maintenance work often have not written algorithmic code since "
                "college. Product company interviews will test BFS, DFS, dynamic "
                "programming, and system design — topics that need dedicated "
                "preparation.\n\n"
                "Another common mistake is not being able to articulate project "
                "impact. When interviewers at companies like Amazon, Google, or "
                "Flipkart ask about your project, they want to hear about business "
                "impact: 'I optimized the database query that reduced page load time "
                "from 5 seconds to 1.2 seconds, improving user retention by 15%.' "
                "Simply describing what you did without quantifying the impact makes "
                "your contribution sound trivial.\n\n"
                "A third mistake is salary-related: accepting the first offer without "
                "negotiation, or conversely, overpricing yourself based on inflated "
                "LinkedIn salary data. The sweet spot is 30-50% above your current "
                "CTC for a lateral move within the same tier, and 80-150% when moving "
                "from services to product companies."
            ),
            "tips": [
                "Dedicate 3-6 months to DSA prep before lateral interviews, even if you have 5 years of experience.",
                "Quantify every project on your resume — use numbers, percentages, and business impact.",
                "Practice system design for any role at 2+ years of experience.",
                "Do not badmouth your current employer in interviews — it is always a red flag.",
                "Research realistic salary ranges for your target role and experience on Levels.fyi.",
                "Prepare for behavioural questions using the STAR method with real examples from work.",
            ],
        },
        {
            "category": "common_mistakes",
            "topic": "hr_round_blunders",
            "content": (
                "The HR round is where technically strong candidates most often "
                "stumble in Indian placements. The number one blunder is answering "
                "'Tell me about yourself' with a recitation of your resume: 'My name "
                "is X, I studied in Y college, my CGPA is Z, I know Java and Python.' "
                "This is boring and adds no value beyond what the interviewer can "
                "read. Instead, craft a narrative: your passion, a defining project, "
                "and why this company excites you.\n\n"
                "Other critical HR round blunders in Indian interviews: saying 'I "
                "want to do an MBA/MS after 2 years' (signals you will leave soon), "
                "saying 'Money is my motivation' (sounds mercenary), saying 'I have "
                "no weaknesses' (sounds delusional), asking about work-life balance "
                "in a way that implies you want to work minimum hours, or expressing "
                "strong preferences about location ('I can ONLY work in Chennai').\n\n"
                "The most damaging blunder specific to Indian campus placements is "
                "lying about projects. Interviewers are experienced — they will ask "
                "follow-up questions like 'Which API did you use for the payment "
                "gateway?' or 'How did you handle concurrent database writes?' If "
                "you listed a project you copied from YouTube without understanding "
                "it, you will be caught."
            ),
            "tips": [
                "Craft a 90-second 'Tell me about yourself' that tells a story, not a resume recap.",
                "Never say you plan to leave for MBA/MS — say you want to grow within the company.",
                "For 'What is your weakness?', give a genuine weakness WITH how you are addressing it.",
                "Do not lie about projects — prepare to answer deep follow-up questions on everything in your resume.",
                "Research the company well enough to answer 'Why this company?' with specific reasons.",
                "When asked about salary expectations, say 'As per company standards' for fresher roles.",
            ],
        },
        {
            "category": "common_mistakes",
            "topic": "technical_round_mistakes",
            "content": (
                "In Indian campus placement technical rounds, the most frequent "
                "mistake is jumping to code without discussing the approach. "
                "Interviewers want to see your thought process: understand the "
                "problem, discuss edge cases, propose a brute-force approach, "
                "optimize it, and then write code. Students who start writing code "
                "immediately often go down the wrong path and waste time.\n\n"
                "Another mistake specific to Indian interviews: memorizing solutions "
                "from GeeksforGeeks or LeetCode without understanding the underlying "
                "concepts. Interviewers can tell when you have memorized an answer — "
                "they will modify the problem slightly and you will be stuck. "
                "Understanding WHY a solution works (e.g., why does a two-pointer "
                "approach work for the container problem?) is more valuable than "
                "memorizing the code.\n\n"
                "For service company technical rounds, a different set of mistakes "
                "occurs: not revising CS fundamentals. Questions like 'What is "
                "normalization?', 'Explain virtual memory,' 'What is polymorphism?' "
                "are asked at TCS, Infosys, and Wipro interviews. These are "
                "straightforward questions from your 2nd/3rd year syllabus, yet "
                "many students cannot answer them clearly because they studied only "
                "for exams and forgot everything."
            ),
            "tips": [
                "Always discuss your approach verbally BEFORE writing code.",
                "Start with a brute-force solution, then optimize — do not jump to optimal directly.",
                "For service company interviews: revise DBMS, OS, CN, and OOPS from standard textbooks.",
                "Understand solutions conceptually — do not just memorize GeeksforGeeks code.",
                "Practice writing code on paper/whiteboard — campus interviews may not have a computer.",
                "If stuck, communicate: 'I am thinking about using X approach because...'",
                "Handle edge cases explicitly — null inputs, empty arrays, single elements.",
            ],
        },
        {
            "category": "common_mistakes",
            "topic": "gd_mistakes",
            "content": (
                "Group Discussion (GD) mistakes in Indian campus placements and MBA "
                "admissions are remarkably consistent. The biggest mistake is treating "
                "the GD as a debate to 'win.' GDs are not about being right — they "
                "are about demonstrating communication, teamwork, and analytical "
                "thinking. Students who aggressively try to dominate the discussion, "
                "interrupt others, or insist their viewpoint is the only correct one "
                "are almost always eliminated.\n\n"
                "The second major mistake is staying silent. In a 15-minute GD with "
                "10 participants, you need to speak at least 3-4 times to be noticed "
                "by evaluators. Silent participants are invisible, regardless of how "
                "well they were listening. On the other extreme, speaking too much "
                "without substance (repeating the same point, making vague statements "
                "like 'It has both advantages and disadvantages') is equally harmful.\n\n"
                "Cultural mistakes specific to India: using Hindi or regional languages "
                "in a GD that is supposed to be in English, making politically "
                "controversial statements (religion, caste, political parties), or "
                "getting personally aggressive with another participant. Also avoid "
                "quoting unverifiable statistics — saying 'According to a study, 85% "
                "of companies prefer...' without citing the source undermines "
                "credibility."
            ),
            "tips": [
                "Speak at least 3-4 times in a 15-minute GD — silence means elimination.",
                "Make your points concise — 20-30 seconds per intervention is ideal.",
                "Never interrupt aggressively — wait for a natural pause and say 'I would like to add...'",
                "Avoid controversial topics: religion, caste, specific political parties.",
                "Support your points with examples and data, not opinions.",
                "If you want to summarize at the end, volunteer: 'If I may summarize the key points discussed...'",
                "Stay calm even if someone attacks your point — respond with facts, not emotion.",
            ],
        },
        # =====================================================================
        # REGIONAL CONTEXT (7 entries)
        # =====================================================================
        {
            "category": "regional_context",
            "topic": "bangalore_tech_ecosystem",
            "content": (
                "Bangalore (Bengaluru) remains India's undisputed tech capital, "
                "hosting offices of Google, Amazon, Microsoft, Apple, Flipkart, "
                "Swiggy, PhonePe, Razorpay, Zerodha, CRED, and thousands of "
                "startups. The city accounts for approximately 35-40% of India's "
                "total tech jobs. For a fresher from a Tier 2/3 college, Bangalore "
                "offers the highest density of job opportunities and the most active "
                "tech community.\n\n"
                "Key tech hubs within Bangalore: Whitefield (IT parks like ITPB, "
                "Prestige Tech Park), Electronic City (Infosys campus, Wipro, HCL), "
                "Outer Ring Road / Sarjapur Road (Goldman Sachs, SAP, Oracle, many "
                "startups), Koramangala (startup hub — Flipkart started here), and "
                "Manyata Tech Park (northern corridor with TCS, Cisco, and others). "
                "Freshers should target accommodation within 5-10 km of their office "
                "to manage Bangalore's notorious traffic.\n\n"
                "Cost of living in Bangalore for a fresher: shared PG accommodation "
                "costs Rs. 8,000-15,000/month, food is Rs. 5,000-8,000/month, "
                "transport is Rs. 2,000-4,000/month (bus/metro + auto), and "
                "miscellaneous expenses add Rs. 3,000-5,000. Total: approximately "
                "Rs. 20,000-30,000/month. On a 3.5 LPA salary (about 25K in-hand), "
                "this leaves very little savings — plan accordingly."
            ),
            "tips": [
                "Bangalore has the most tech jobs in India — if flexibility is an option, prioritize it.",
                "Join Bangalore tech meetups and communities (BangaloreJS, PythonPune equiv) for networking.",
                "Live near your office — Bangalore traffic can turn a 10km commute into 90 minutes.",
                "Use Namma Metro for commutes along the Purple and Green lines to save time and money.",
                "Cost of living is high — budget carefully on a 3-4 LPA salary.",
                "Attend hackathons and tech events at Koramangala, HSR Layout, and Indiranagar.",
            ],
        },
        {
            "category": "regional_context",
            "topic": "hyderabad_gcc_hub",
            "content": (
                "Hyderabad has emerged as India's leading Global Capability Centre "
                "(GCC) hub, with over 250 MNC centres including Google, Amazon, "
                "Microsoft, Apple, Meta, Qualcomm, Deloitte, and Wells Fargo. The "
                "city's HITEC City and Gachibowli areas form one of the largest tech "
                "corridors in Asia. For students from Andhra Pradesh and Telangana "
                "colleges, Hyderabad is the natural first destination.\n\n"
                "The GCC model means that many Hyderabad tech jobs are in engineering "
                "and R&D for MNCs, not just IT services. This translates to "
                "better-than-average salaries: a fresher at a GCC like Google "
                "Hyderabad or Amazon Hyderabad can expect 12-25 LPA, while GCCs of "
                "financial companies (Goldman Sachs, Deutsche Bank, UBS) offer "
                "8-15 LPA. Even service companies pay slightly better in Hyderabad "
                "due to GCC competition.\n\n"
                "Cost of living in Hyderabad is 20-30% lower than Bangalore, making "
                "it attractive for freshers. PG accommodation in areas like "
                "Madhapur, Kondapur, or Kukatpally costs Rs. 6,000-12,000/month. "
                "The Hyderabad Metro connects major tech corridors, and the city's "
                "food scene (biryani culture!) is both excellent and affordable."
            ),
            "tips": [
                "Hyderabad GCCs offer some of the best fresher salaries outside Bangalore.",
                "Target GCC hiring drives — they often have separate recruitment from the parent company.",
                "Areas like Madhapur, Kondapur, and Gachibowli are close to most tech offices.",
                "Cost of living advantage: you save more in Hyderabad than Bangalore on the same salary.",
                "Learn about financial services tech (payments, risk systems) to target banking GCCs.",
                "Hyderabad's startup scene is growing — check T-Hub incubator companies for opportunities.",
            ],
        },
        {
            "category": "regional_context",
            "topic": "pune_it_corridor",
            "content": (
                "Pune is India's third-largest IT hub, known for its blend of IT "
                "services, MNC R&D centres, and a growing startup ecosystem. Key "
                "tech employers include Infosys, TCS, Wipro, Cognizant, Persistent "
                "Systems, Veritas, Synechron, BMC Software, and NVIDIA. The main "
                "IT hubs are Hinjewadi IT Park, Magarpatta Cybercity, Kharadi, and "
                "the Baner-Balewadi corridor.\n\n"
                "Pune has a strong connection with engineering colleges in Maharashtra "
                "— COEP, VIT Pune, PICT, MIT Pune, and Pune University's affiliated "
                "colleges feed a large number of graduates into the local IT industry. "
                "The city is particularly strong in automotive tech (Volkswagen IT, "
                "Tata Motors), embedded systems, and enterprise software.\n\n"
                "For freshers, Pune offers a middle ground between Bangalore's "
                "opportunities and its high costs. PG accommodation costs Rs. "
                "5,000-10,000/month, and the overall cost of living is 15-25% "
                "lower than Bangalore. The city's weather (pleasant most of the "
                "year), food culture, and active social scene make it a favourite "
                "among young professionals."
            ),
            "tips": [
                "Pune is ideal for freshers from Maharashtra colleges — strong alumni networks exist.",
                "Target Hinjewadi IT Park for service company jobs and Kharadi/Baner for product companies.",
                "Pune's automotive and embedded systems sector is unique — relevant for ECE graduates.",
                "The city has a strong marathon and trekking culture — great for work-life balance.",
                "PMPML buses and the upcoming Pune Metro make commuting manageable.",
            ],
        },
        {
            "category": "regional_context",
            "topic": "chennai_it_services_hub",
            "content": (
                "Chennai is one of India's oldest IT hubs and a stronghold of IT "
                "services companies. TCS, Infosys, Cognizant, HCL, Zoho, Freshworks, "
                "PayPal, and BNY Mellon all have major offices here. The IT corridors "
                "are OMR (Old Mahabalipuram Road, also called the IT Expressway), "
                "Sholinganallur, Thoraipakkam, and Guindy/Mount Road for older "
                "offices.\n\n"
                "For students from Tamil Nadu colleges (Anna University affiliates, "
                "VIT Vellore, SRM, SASTRA, PSG Tech, Amrita), Chennai is the default "
                "first-job city. The city's tech landscape is dominated by services "
                "companies, but there is a growing product ecosystem led by Zoho "
                "(headquartered in Tenkasi, main office in Chennai), Freshworks "
                "(born in Chennai), Chargebee, Kissflow, and several AI/ML startups.\n\n"
                "Zoho deserves special mention for Tier 2/3 students. The company "
                "has no CGPA cutoff, pays 5-8 LPA for freshers, provides excellent "
                "training, and has a unique work culture that values deep "
                "programming skills over pedigree. Zoho's off-campus hiring process "
                "(through Zoho Recruitment portal and campus drives at non-tier-1 "
                "colleges) is one of the best opportunities for Tier 3 students."
            ),
            "tips": [
                "Zoho is the best opportunity for Tier 3 students in Chennai — prepare C, Java, and logical reasoning.",
                "OMR is the main IT corridor — find accommodation in Velachery, Thoraipakkam, or Perungudi.",
                "Chennai's cost of living is lower than Bangalore — PG at Rs. 5,000-10,000/month.",
                "The city has a strong tech community — attend Chennai Geeks, ChennaiPy, and GDG Chennai events.",
                "Tamil-medium students should not worry — many Chennai companies have multilingual teams.",
                "Freshworks, Chargebee, and Kissflow actively hire from Tier 2/3 TN colleges.",
            ],
        },
        {
            "category": "regional_context",
            "topic": "ncr_startup_ecosystem",
            "content": (
                "The NCR (National Capital Region) comprising Delhi, Noida, Gurgaon "
                "(Gurugram), and Ghaziabad is India's second-largest tech job market. "
                "Gurgaon houses offices of Google, Meta, LinkedIn, Paytm, Zomato, "
                "PolicyBazaar, and several unicorn startups. Noida has a large "
                "concentration of IT services companies (HCL, TCS, Wipro) and is "
                "also home to companies like Paytm, OYO, and Samsung R&D.\n\n"
                "NCR is particularly strong in fintech, edtech, and consumer internet "
                "startups. Companies like Razorpay (Gurgaon office), Groww, "
                "PhysicsWallah, Unacademy, and Lenskart are headquartered in NCR. "
                "For students interested in startup culture, NCR offers more "
                "opportunities than any city except Bangalore.\n\n"
                "The downside of NCR is the cost of living and commute. Gurgaon "
                "accommodation is expensive (Rs. 10,000-18,000 for a shared PG), "
                "traffic is severe, and the extreme weather (45-degree summers, "
                "cold winters, pollution) can be challenging. Noida offers slightly "
                "cheaper living with the Delhi Metro providing connectivity."
            ),
            "tips": [
                "NCR is ideal for fintech, edtech, and consumer startup careers.",
                "Gurgaon's Cyber City and Golf Course Road are the premium tech areas.",
                "Noida Sector 62 and 125-135 are major IT hubs with lower living costs than Gurgaon.",
                "Delhi Metro makes NCR navigable — choose accommodation near a Metro station.",
                "Air quality is a genuine health concern — invest in an air purifier for your room.",
                "Startup hiring in NCR is often through referrals — network aggressively on LinkedIn.",
            ],
        },
        {
            "category": "regional_context",
            "topic": "coimbatore_emerging_tech",
            "content": (
                "Coimbatore is an emerging tech hub in Tamil Nadu, often called the "
                "'Manchester of South India' for its manufacturing heritage but "
                "increasingly relevant for tech. The city has a growing cluster of "
                "IT and ITES companies including Bosch, KGiSL, Aspire Systems, "
                "Cognizant, and several homegrown startups. The TIDEL Park and "
                "Coimbatore IT SEZ are the primary tech zones.\n\n"
                "For students from Coimbatore-area colleges (PSG Tech, Amrita, "
                "CIT, Sri Krishna College, Kumaraguru), the city offers an "
                "alternative to the Chennai/Bangalore migration. Salaries are "
                "typically 10-20% lower than Chennai (a fresher at a Coimbatore IT "
                "company earns 2.5-4 LPA), but the cost of living is significantly "
                "lower — PG accommodation costs Rs. 3,000-6,000/month and food is "
                "very affordable.\n\n"
                "The Coimbatore startup ecosystem is growing, driven by the "
                "Forge Accelerator, COINS (Coimbatore Innovation Ecosystem), and "
                "local angel investor networks. Companies like Vuram (hyperautomation), "
                "CloudSEK (cybersecurity), and several SaaS startups have emerged "
                "from Coimbatore. For students who prefer a smaller city with "
                "lower competition and cost, Coimbatore is a viable option."
            ),
            "tips": [
                "Coimbatore is ideal if you prefer smaller-city living with lower costs.",
                "PSG Tech and Amrita alumni networks are strong in local companies — leverage them.",
                "The city is strong in IoT, embedded systems, and manufacturing tech — relevant for ECE students.",
                "Use Coimbatore as a springboard — gain 1-2 years of experience, then move to Bangalore.",
                "Attend local tech meetups and the Google Developer Group Coimbatore for networking.",
            ],
        },
        {
            "category": "regional_context",
            "topic": "tier2_city_opportunities",
            "content": (
                "Beyond the metro cities, several Tier 2 cities in India are "
                "developing significant tech ecosystems. Jaipur has a growing IT "
                "sector with companies like Infosys (SEZ), Genpact, and several "
                "digital marketing and web development firms. Kochi hosts the "
                "Infopark with TCS, UST Global, IBS Software, and a vibrant startup "
                "scene. Thiruvananthapuram has Technopark — India's first tech park "
                "— with TCS, Infosys, UST Global, and IBS.\n\n"
                "Other emerging Tier 2 tech cities include: Indore (TCS, Infosys, "
                "and a growing startup culture), Bhubaneswar (Infocity with TCS, "
                "Mindtree, and NASSCOM-supported startup hub), Chandigarh (IT Park "
                "with Infosys, and proximity to Mohali's fintech sector), and "
                "Mysuru (Infosys Global Education Centre and a calm, affordable "
                "city for early career).\n\n"
                "Working in a Tier 2 city has genuine advantages: dramatically lower "
                "cost of living (Rs. 10,000-15,000/month total expenses), less "
                "competition for jobs, proximity to family for many students, and "
                "an increasingly good quality of life. The trade-off is fewer "
                "company options and slightly lower salaries. But for a first job, "
                "a Tier 2 city can be an excellent choice."
            ),
            "tips": [
                "Do not overlook Tier 2 cities — the savings advantage makes them financially smart for freshers.",
                "Kochi, Thiruvananthapuram, and Mysuru offer excellent quality of life with decent tech jobs.",
                "Remote work has opened doors — you can live in a Tier 2 city and work for a Bangalore startup.",
                "Tier 2 city experience counts equally on your resume — skills matter more than location.",
                "Use Tier 2 city positions to build skills and then leverage for metro city lateral moves.",
                "Check NASSCOM and state government startup portals for Tier 2 city opportunities.",
            ],
        },
        # =====================================================================
        # UPSC CONTEXT (3 entries)
        # =====================================================================
        {
            "category": "upsc_context",
            "topic": "personality_test_detailed",
            "content": (
                "The UPSC Civil Services Personality Test (commonly called the "
                "Interview) is the final stage of the Civil Services Examination, "
                "carrying 275 marks. Unlike corporate interviews, this is not a "
                "knowledge test — the board assesses your personality traits: "
                "intellectual curiosity, social cohesion, integrity, leadership "
                "qualities, mental alertness, critical thinking, clarity of "
                "expression, balance of judgment, and moral compass.\n\n"
                "The interview typically lasts 25-35 minutes. A five-member board, "
                "led by a Chairman (usually a retired civil servant, academic, or "
                "expert), asks questions spanning your Detailed Application Form "
                "(DAF), current affairs, ethics, your optional subject, and general "
                "awareness. Questions can range from 'Why do you want to leave a "
                "high-paying IT job for civil services?' to 'What would you do if "
                "your superior officer asks you to do something unethical?' to "
                "'What is your opinion on the recent Supreme Court judgment on X?'\n\n"
                "Marks in the personality test typically range from 40% to 75% "
                "(110-206 out of 275). Scores below 40% or above 75% are rare. "
                "The average is around 55% (151 marks). A strong personality test "
                "performance can compensate for a weaker written exam score and vice "
                "versa. Preparation should focus on self-awareness, DAF analysis, "
                "and being well-informed on current national and international issues."
            ),
            "tips": [
                "Analyse every line of your DAF — questions will come from your hobbies, hometown, college, and work experience.",
                "Practice with mock interview boards — Vajiram, Shankar IAS, ForumIAS, and KSG offer mock interviews.",
                "Read newspapers (The Hindu, Indian Express) and Rajya Sabha TV debates for balanced perspectives.",
                "Prepare strong answers for 'Why civil services?', 'Why leave your current career?', and 'What is your biggest failure?'.",
                "Be honest if you do not know something — 'I am not sure about the specifics, but my understanding is...' is better than bluffing.",
                "Dress formally: men in a suit/blazer with tie, women in a formal saree or professional attire.",
                "Reach the venue 30 minutes early — the UPSC interview is typically at UPSC Bhawan, Dholpur House, New Delhi.",
            ],
        },
        {
            "category": "upsc_context",
            "topic": "daf_preparation_strategy",
            "content": (
                "The Detailed Application Form (DAF) is the most important document "
                "for your UPSC Personality Test. Every field in the DAF — your name, "
                "birthplace, educational qualifications, work experience, hobbies, "
                "extracurricular activities, and service preferences — is a potential "
                "source of interview questions. Strategic DAF preparation is the "
                "foundation of interview success.\n\n"
                "When filling the DAF, be strategic but honest. List hobbies you can "
                "discuss in depth — if you write 'reading,' be prepared to discuss "
                "your last 5 books and your favourite author's worldview. If you "
                "write 'cricket,' know the rules, recent controversies, and the role "
                "of BCCI in Indian sports governance. Common DAF-based questions "
                "include: 'You are from [your district] — tell us about its "
                "development challenges,' 'Your optional is [subject] — how would "
                "you apply this knowledge as a district collector?', and 'You "
                "worked at [company] — what did you learn about leadership there?'\n\n"
                "For service preferences (IAS, IPS, IFS, IRS), have a clear "
                "rationale. If you prefer IAS, be ready to explain why administrative "
                "service appeals to you more than police or foreign service. For "
                "cadre preferences, know the states you have listed — their geography, "
                "economy, governance challenges, and recent policy initiatives."
            ),
            "tips": [
                "Map every DAF entry to potential questions — create a 'DAF question bank' of 100+ questions.",
                "For each hobby, prepare: why you started, what you have learned, how it shapes your worldview.",
                "Know your home district inside out — economy, demography, key schemes, and challenges.",
                "Research your optional subject's relevance to governance and current affairs.",
                "Prepare 2-3 specific incidents from your work/college life that demonstrate leadership and ethics.",
                "Have a clear, convincing answer for why you chose each service and cadre preference.",
                "Practice with a mentor who has cleared UPSC — they know what boards look for.",
            ],
        },
        {
            "category": "upsc_context",
            "topic": "board_composition_styles",
            "content": (
                "UPSC interview boards consist of a Chairman and four members, each "
                "with different backgrounds — typically a mix of academics, retired "
                "bureaucrats, professionals, and subject matter experts. The "
                "composition of your board significantly influences the interview "
                "experience. Boards chaired by former civil servants tend to focus "
                "on administrative scenarios and ethics, while those chaired by "
                "academics may dive deeper into your optional subject and current "
                "affairs.\n\n"
                "Famous board chairpersons have distinct styles. Some are known for "
                "being friendly and conversational, putting candidates at ease. "
                "Others are known for stress interviews — rapid-fire questions, "
                "challenging your views, or asking provocative questions to test "
                "composure. Neither style is 'better' or 'worse' for scoring — what "
                "matters is how you handle the dynamic.\n\n"
                "Board behaviour during the interview is worth observing. If the "
                "Chairman smiles and nods, it does not necessarily mean you are doing "
                "well — they may be encouraging you to continue. If a member looks "
                "stern, they may just have that demeanour. Focus on the content of "
                "your answers rather than trying to read facial expressions. After "
                "each member finishes their questions, a brief 'Thank you, sir/ma'am' "
                "before the next member begins is good etiquette."
            ),
            "tips": [
                "Do not try to predict your board's style — prepare for both friendly and stress interviews.",
                "Address the Chairman by 'Chairman Sir/Ma'am' and members by 'Sir/Ma'am.'",
                "If a member disagrees with your view, say 'That is a valid perspective, sir. However, I believe...'",
                "Do not argue with the board — present your view and accept theirs graciously.",
                "If you face a stress interview, stay calm — composure itself earns marks.",
                "Thank the board collectively before leaving: 'Thank you, sir/ma'am. It was a pleasure.'",
            ],
        },
        # =====================================================================
        # GD FORMAT (2 entries)
        # =====================================================================
        {
            "category": "gd_format",
            "topic": "mba_admissions_gd",
            "content": (
                "Group Discussions for MBA admissions (IIMs, XLRI, MDI, SPJIMR, and "
                "other top B-schools) are different from campus placement GDs. MBA GDs "
                "are more structured and evaluators look for specific competencies: "
                "analytical thinking, data-driven argumentation, leadership, teamwork, "
                "and communication quality. Topics tend to be abstract ('Is democracy "
                "the best form of governance?'), case-based ('Should India ban "
                "cryptocurrency?'), or current affairs-based ('Impact of AI on "
                "employment in India').\n\n"
                "The format varies by institution. IIMs typically conduct a GD with "
                "8-10 participants for 15-20 minutes, sometimes with a 2-minute "
                "preparation time. Some IIMs have replaced traditional GDs with "
                "Written Ability Tests (WATs) — a 20-minute essay writing exercise. "
                "XLRI uses a GD+Personal Interview format. MDI Gurgaon conducts "
                "both GD and a personal interview.\n\n"
                "Scoring in MBA GDs is more nuanced than in placement GDs. B-school "
                "evaluators use specific rubrics: content quality (25%), "
                "communication skills (25%), leadership and initiative (20%), "
                "teamwork and interpersonal skills (20%), and body language (10%). "
                "They specifically note who initiated the discussion, who summarized "
                "it, who brought in new perspectives, and who facilitated quiet "
                "members to speak."
            ),
            "tips": [
                "Read The Hindu editorials and Mint opinion pages daily for GD content preparation.",
                "Practice structuring arguments: premise, evidence, counterpoint, conclusion.",
                "For abstract topics, define the topic first to anchor the discussion — this shows leadership.",
                "Keep one hand free for gesturing — do not fold both arms or fidget with objects.",
                "If the GD goes off-track, bring it back: 'Let us refocus on the core question...'",
                "Prepare 20-30 topics with 3 points each — most GD topics are variations of common themes.",
                "Watch IIM interview experience videos on YouTube (InsideIIM channel) for realistic preparation.",
            ],
        },
        {
            "category": "gd_format",
            "topic": "campus_placement_gd",
            "content": (
                "Campus placement GDs are conducted by IT services companies (TCS, "
                "Infosys, Wipro, Cognizant, Capgemini) as a mass screening tool to "
                "filter candidates before the personal interview round. Unlike MBA "
                "GDs, placement GDs are less about depth and more about basic "
                "communication ability. Topics are usually straightforward: 'Social "
                "media: boon or bane?', 'Should engineering education be in regional "
                "languages?', 'Is remote work the future?', 'Impact of technology "
                "on privacy.'\n\n"
                "The format is typically 10-12 students, 15-minute discussion, and "
                "the evaluator (usually an HR executive) observes silently. In some "
                "companies, you may be asked to write a 200-word summary after the "
                "GD. The selection rate from GDs is usually 50-60% — it is a filter, "
                "not a deep evaluation. The bar is: can you speak clearly in English "
                "for 30 seconds, do you have basic awareness of the topic, and can "
                "you interact with a group without being disruptive?\n\n"
                "For Tier 2/3 students who are not confident in English, campus "
                "placement GDs are the most anxiety-inducing round. The key insight "
                "is that evaluators are looking for clarity and effort, not "
                "eloquence. A well-structured point in simple English beats a "
                "grammatically perfect but vague contribution."
            ),
            "tips": [
                "Campus placement GDs have a lower bar than MBA GDs — clear communication is enough.",
                "Prepare 10 common topics with 3 solid points each (for and against).",
                "If English is a concern, practice speaking about GD topics for 2 minutes daily.",
                "Do not stay silent — even one clear contribution is better than none.",
                "Avoid using your phone to look up facts during the GD — it looks unprofessional.",
                "If asked to write a summary, structure it as: topic intro, 3 key points discussed, conclusion.",
            ],
        },
    ]
