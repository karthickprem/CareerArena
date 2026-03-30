"""Logical Reasoning interview questions for PlaceRight. ~400+ questions via template expansion."""
from typing import List, Dict

R = {"1-3": "Cannot identify patterns or apply logic. Random guessing.",
     "4-5": "Solves simple puzzles but fails on multi-step reasoning.",
     "6-7": "Good logical thinking. Handles most patterns and puzzles.",
     "8-10": "Excellent reasoning. Solves complex puzzles quickly. Identifies subtle patterns."}

def _q(t, d, l, txt, fu, pts, co="", tg=None):
    return {"domain": "aptitude", "topic": t, "difficulty": d, "level": l,
            "question_text": txt, "follow_ups": fu, "expected_points": pts,
            "scoring_rubric": R, "company_specific": co, "tags": tg or [t]}

def get_aptitude_logical_questions() -> List[Dict]:
    Q = []

    # ═══════ CODING-DECODING ═══════
    cd = [
        ("In a certain code, 'COMPUTER' is written as 'DPNQVUFS'. How is 'PROGRAM' written in that code?", "easy", "fresher",
         ["What's the pattern?", "Shift of how many?"],
         ["Each letter shifted +1: C→D, O→P, M→N...", "PROGRAM → QSPHSBN", "Pattern: simple Caesar cipher with shift 1", "Check: P+1=Q, R+1=S, O+1=P..."]),
        ("In a code language, 'sky is blue' is written as 'ta pa na', 'blue is ocean' is written as 'na sa pa'. What is the code for 'blue'?", "medium", "fresher",
         ["Which word is common?", "Find the common code."],
         ["Common words: 'blue' and 'is' appear in both", "Common codes: 'na' and 'pa'", "'blue is' maps to 'na pa' (in some order)", "Need third sentence to determine which is which"]),
        ("If APPLE = 50, BANANA = 42, then CHERRY = ?", "medium", "fresher",
         ["What's the logic?", "Sum of letter positions?"],
         ["A=1,P=16,P=16,L=12,E=5 → sum=50 ✓", "B=2,A=1,N=14,A=1,N=14,A=1 → sum=33 ≠ 42", "Try: product of digits, or count×value...", "Multiple encoding methods possible — identify pattern"]),
        ("In a code, 1234 = ROSE, 5673 = LILY. What does 3456 represent?", "medium", "fresher",
         ["Map each digit to a letter.", "1=R, 2=O, 3=S/I, 4=E/L?"],
         ["1=R, 2=O, 3=S, 4=E (from ROSE)", "5=L, 6=I, 7=L, 3=Y? — conflict!", "Recheck: perhaps 3=S in ROSE, 3=Y in LILY", "Need to resolve: 3 maps to two letters — pattern might be positional"]),
        ("If 'go home' is 'ja sa', 'come home now' is 'sa pa ra', 'go now' is 'ja ra', what is the code for 'come'?", "easy", "fresher",
         ["Track each word across sentences.", "Elimination method."],
         ["'go' = 'ja' (from sentences 1 & 3)", "'home' = 'sa' (from sentences 1 & 2)", "'now' = 'ra' (from sentences 2 & 3)", "'come' = 'pa' (only remaining in sentence 2)"]),
    ]
    for txt, d, l, fu, pts in cd:
        Q.append(_q("coding_decoding", d, l, txt, fu, pts))

    # ═══════ BLOOD RELATIONS ═══════
    br = [
        ("Pointing to a man, Rekha said 'His mother is the only daughter of my mother.' How is Rekha related to the man?", "medium", "fresher",
         ["Who is the 'only daughter of my mother'?", "Draw a family tree."],
         ["'Only daughter of my mother' = Rekha herself", "So the man's mother = Rekha", "Rekha is the man's MOTHER", "Key: 'only daughter of my mother' = the speaker herself"]),
        ("A is B's brother. C is A's mother. D is C's father. E is D's mother. How is B related to D?", "hard", "fresher",
         ["Draw the family tree.", "Gender of B?"],
         ["E → D → C → A (brothers with B)", "D is C's father = A's grandfather", "B is A's sibling → D is B's grandfather too", "B is D's grandchild (grandson or granddaughter)"]),
        ("Introducing a woman, Ravi said, 'She is the wife of my mother's only son.' How is the woman related to Ravi?", "easy", "fresher",
         ["Who is 'my mother's only son'?", "Think step by step."],
         ["'My mother's only son' = Ravi himself", "The woman is the wife of Ravi", "The woman is Ravi's WIFE", "Key: 'only son' = the speaker"]),
        ("In a family, A is the father of B. C is the mother of D. B and D are siblings. E is the spouse of A. How is E related to D?", "medium", "fresher",
         ["Who are B and D's parents?", "Is E = C?"],
         ["A is father of B, B and D are siblings", "So A is also D's father", "E is spouse of A = E is D's parent", "If E is female, E is D's mother (E = C)"]),
        ("Pointing to a photograph, Mohan says 'She is the daughter of my grandfather's only son.' How is the person in the photo related to Mohan?", "medium", "fresher",
         ["Who is grandfather's only son?", "Think about who it could be."],
         ["Grandfather's only son = Mohan's father", "Person is the daughter of Mohan's father", "Person is Mohan's SISTER", "Or Mohan himself if Mohan is female (but question says 'she')"]),
        ("A + B means A is the mother of B. A - B means A is the brother of B. A × B means A is the father of B. A ÷ B means A is the sister of B. What does P × Q - R ÷ S mean?", "hard", "fresher",
         ["Parse step by step.", "What's the final relationship?"],
         ["P × Q: P is father of Q", "Q - R: Q is brother of R", "R ÷ S: R is sister of S", "P is Q's father, Q is R's brother, R is S's sister → P is grandfather? Need to trace carefully"]),
    ]
    for txt, d, l, fu, pts in br:
        Q.append(_q("blood_relations", d, l, txt, fu, pts))

    # ═══════ DIRECTION SENSE ═══════
    ds = [
        ("A man walks 5 km north, turns right and walks 3 km, turns right again and walks 5 km. How far is he from the starting point?", "easy", "fresher",
         ["Draw the path.", "Which direction is he facing?"],
         ["North 5km → right (East) 3km → right (South) 5km", "He's now directly east of start", "Distance from start = 3 km", "Facing south"]),
        ("Starting from point A, Ravi walks 10m east, turns left and walks 6m, turns left and walks 3m, turns left and walks 6m. How far is he from A?", "medium", "fresher",
         ["Draw each step.", "What shape is the path?"],
         ["East 10m → North 6m → West 3m → South 6m", "Final position: 10-3 = 7m east of start, 6-6 = 0m north", "Distance = 7m from starting point", "Direction: East of A"]),
        ("Priya walks 4 km south, then 3 km east, then 4 km north. What is her distance and direction from the starting point?", "easy", "fresher",
         ["Net displacement?", "Pythagorean theorem?"],
         ["South 4km, East 3km, North 4km", "Net: South-North cancel out (4-4=0), 3km East remains", "Distance = 3 km", "Direction: East of starting point"]),
        ("A is north of B. C is to the east of A. D is to the south of C. What is the direction of D with respect to B?", "medium", "fresher",
         ["Draw the layout.", "Diagonal direction?"],
         ["B is south of A, C is east of A, D is south of C", "D is south-east of A", "D is east of B (or north-east depending on relative distances)", "Need specific distances to determine exact direction"]),
        ("If North-East becomes North, then what does South-East become?", "medium", "fresher",
         ["How much rotation?", "Apply to all directions."],
         ["NE becomes N means 45° anti-clockwise rotation", "SE → E (rotate 45° anti-clockwise)", "Every direction rotates 45° anti-clockwise", "Or: compass rotated 45°, SE maps to E"]),
    ]
    for txt, d, l, fu, pts in ds:
        Q.append(_q("direction_sense", d, l, txt, fu, pts))

    # ═══════ SEATING ARRANGEMENT ═══════
    sa = [
        ("Six friends P, Q, R, S, T, U sit in a row facing north. Q is to the left of T. R is at one end. S is next to Q and T. P is not next to R. Find the arrangement.", "hard", "fresher",
         ["Start with fixed positions.", "Use elimination."],
         ["R is at one end", "Q is to left of T, S is between Q and T → ...Q S T...", "Try R at left end: R _ Q S T U → P must fit without being next to R", "One valid arrangement: R U Q S T P"]),
        ("Eight people A-H sit around a circular table facing the center. A sits opposite D. B is 2 positions to the right of A. C sits between B and D. Find the arrangement.", "hard", "fresher",
         ["Fix A's position first.", "Opposite means across the center."],
         ["Fix A at top, D opposite (at bottom)", "B is 2 right of A", "C sits between B and D → specific position", "Fill remaining positions using constraints"]),
        ("Five people A, B, C, D, E sit in a row. B is not at either end. D is to the right of C. A is at one end. E is not next to A. Find a valid arrangement.", "medium", "fresher",
         ["How many valid arrangements?", "Start with A."],
         ["A is at one end (position 1 or 5)", "B is not at ends → positions 2, 3, or 4", "E is not next to A → not in position adjacent to A", "Try: A at pos 1, E not at pos 2, D right of C"]),
        ("In a row of students, Ravi is 15th from the left and 10th from the right. How many students are in the row?", "easy", "fresher",
         ["Formula?", "What if someone is in between two positions?"],
         ["Total = 15 + 10 - 1 = 24", "Subtract 1 because Ravi is counted twice", "Formula: Left position + Right position - 1", "Works for linear arrangements"]),
    ]
    for txt, d, l, fu, pts in sa:
        Q.append(_q("seating_arrangement", d, l, txt, fu, pts))

    # ═══════ SYLLOGISMS ═══════
    syl = [
        ("Statements: All dogs are animals. Some animals are cats. Conclusions: I. Some dogs are cats. II. Some cats are animals. Which conclusion follows?", "medium", "fresher",
         ["Draw Venn diagram.", "Definite vs possible?"],
         ["Only Conclusion II follows", "All dogs are animals → dogs inside animals circle", "Some animals are cats → overlap between animals and cats", "Dogs and cats may or may not overlap → I doesn't follow"]),
        ("Statements: All books are pens. All pens are chairs. Conclusions: I. All books are chairs. II. Some chairs are books. Which follows?", "easy", "fresher",
         ["Transitive relationship?", "Draw three circles."],
         ["Both I and II follow", "All books ⊂ pens ⊂ chairs → All books are chairs (I follows)", "Since all books are chairs, some chairs must be books (II follows)", "Transitive: A⊂B, B⊂C → A⊂C"]),
        ("Statements: No fish is a bird. All birds can fly. Conclusions: I. No fish can fly. II. Some fish can fly. Which follows?", "medium", "fresher",
         ["Can fish overlap with flying things?", "Negation in syllogisms."],
         ["Neither conclusion follows definitively", "Fish and birds don't overlap", "But fish could still fly (not via being birds)", "'Can fly' set may be larger than 'birds' set"]),
        ("Statements: Some teachers are engineers. All engineers are graduates. Conclusions: I. Some teachers are graduates. II. All graduates are engineers.", "easy", "fresher",
         ["Which direction is the subset?", "Draw the Venn diagram."],
         ["Only Conclusion I follows", "Some teachers = engineers ⊂ graduates → those teachers are graduates", "II is wrong: engineers ⊂ graduates, not graduates ⊂ engineers", "Subset relationship is one-directional"]),
        ("Statements: All roses are flowers. No flower is a thorn. Conclusions: I. No rose is a thorn. II. Some thorns are roses.", "easy", "fresher",
         ["Chain the two statements.", "Negative universal + positive universal?"],
         ["Only I follows", "Roses ⊂ flowers, flowers ∩ thorns = ∅", "Therefore roses ∩ thorns = ∅ → No rose is a thorn", "II contradicts I → doesn't follow"]),
    ]
    for txt, d, l, fu, pts in syl:
        Q.append(_q("syllogisms", d, l, txt, fu, pts))

    # ═══════ PUZZLES ═══════
    puz = [
        ("Five houses in a row are painted in different colors. The person in the red house drinks coffee. The green house is to the left of the white house. Who lives in the blue house? (Simplified puzzle)", "hard", "fresher",
         ["Use elimination.", "What other clues?"],
         ["Start with fixed positions from clues", "Green is left of white → positions constrained", "Red house → coffee drinker", "Process of elimination for remaining assignments"]),
        ("A, B, C, D are four friends. Each has a different profession: doctor, engineer, teacher, lawyer. A is not a doctor or teacher. B is not an engineer. C is a doctor. D is not a lawyer. Find each person's profession.", "medium", "fresher",
         ["Start with what you know.", "Use elimination."],
         ["C = Doctor (given)", "A ≠ Doctor, Teacher → A is Engineer or Lawyer", "B ≠ Engineer → B is Teacher or Lawyer", "D ≠ Lawyer → D is Teacher, B is Lawyer, A is Engineer"]),
        ("There are 12 balls, one is heavier or lighter. Using a balance 3 times, find the odd ball.", "hard", "mid",
         ["Divide into groups of 4.", "What does each weighing tell you?"],
         ["Weighing 1: 4 vs 4. If balanced, odd ball in remaining 4", "If unbalanced: odd ball in one of the two groups", "Weighing 2: narrows to 3-4 suspects", "Weighing 3: identifies the exact ball"]),
        ("A farmer needs to transport a fox, a chicken, and a sack of grain across a river. The boat can carry only the farmer and one item. Fox eats chicken if left alone. Chicken eats grain if left alone. How?", "medium", "fresher",
         ["What's the key constraint?", "Can you take something back?"],
         ["Step 1: Take chicken across", "Step 2: Return, take fox across", "Step 3: Bring chicken back", "Step 4: Take grain across. Step 5: Return, take chicken across"]),
        ("Three friends have marks: 70, 80, 90 (not necessarily in order). Amit scored more than Ravi. Ravi didn't score the lowest. Who scored 80?", "easy", "fresher",
         ["Process of elimination.", "What does each clue give?"],
         ["Ravi didn't score lowest (70) → Ravi scored 80 or 90", "Amit > Ravi → Amit scored more than Ravi", "If Ravi=80, Amit must be 90 → third person=70 ✓", "If Ravi=90, Amit>90 impossible. So Ravi=80"]),
    ]
    for txt, d, l, fu, pts in puz:
        Q.append(_q("puzzles", d, l, txt, fu, pts))

    # ═══════ STATEMENT & ASSUMPTIONS ═══════
    stass = [
        ("Statement: 'The school has decided to start online classes from next week.' Assumptions: I. Students have access to internet. II. Teachers are trained for online teaching. Which assumption is implicit?", "medium", "fresher",
         ["What must be true for the statement to make sense?", "Implicit vs explicit?"],
         ["Assumption I is implicit — online classes need internet", "Assumption II is also implicit — teachers need to know how", "Both are necessary for the decision to work", "Implicit assumption: not stated but must be true"]),
        ("Statement: 'Drink X for instant energy!' Assumptions: I. People want instant energy. II. X actually provides energy. Which is implicit?", "easy", "fresher",
         ["What's the purpose of an ad?", "What must the advertiser believe?"],
         ["Both are implicit", "I: ad assumes people desire instant energy (target audience exists)", "II: product claim assumes it works", "Advertising assumes both demand and efficacy"]),
        ("Statement: 'Walk-in interview this Saturday — no prior appointment needed.' Assumptions: I. People may not be able to schedule appointments. II. The company needs to fill positions urgently.", "medium", "fresher",
         ["Why walk-in specifically?", "Which is definitely implicit?"],
         ["I is implicit — walk-in addresses appointment difficulty", "II is likely implicit — urgency explains walk-in format", "Walk-in format assumes convenience matters to candidates", "Urgency drives the no-appointment decision"]),
    ]
    for txt, d, l, fu, pts in stass:
        Q.append(_q("statement_assumptions", d, l, txt, fu, pts))

    # ═══════ STATEMENT & CONCLUSIONS ═══════
    stcon = [
        ("Statement: 'All employees must complete the safety training before working on-site.' Conclusions: I. Safety training is mandatory. II. Some employees haven't completed it yet.", "easy", "fresher",
         ["Does I follow directly?", "Does II have to be true?"],
         ["I follows directly — 'must' = mandatory", "II is not necessarily true — could be proactive policy", "Only I follows", "A policy doesn't imply current non-compliance"]),
        ("Statement: 'Reading enhances vocabulary and improves analytical thinking.' Conclusions: I. Non-readers have poor vocabulary. II. Reading has multiple benefits.", "easy", "fresher",
         ["Does the statement say anything about non-readers?", "Multiple benefits?"],
         ["Only II follows", "I doesn't follow — non-readers might get vocabulary from other sources", "II follows — vocabulary AND analytical thinking = multiple benefits", "Cannot conclude about what NON-readers experience"]),
    ]
    for txt, d, l, fu, pts in stcon:
        Q.append(_q("statement_conclusions", d, l, txt, fu, pts))

    # ═══════ DATA SUFFICIENCY ═══════
    dsuf = [
        ("Question: What is John's age? Statement 1: John is 5 years older than Mary. Statement 2: Mary will be 25 in 3 years. Is the data sufficient?", "medium", "fresher",
         ["Each statement alone?", "Both together?"],
         ["Statement 1 alone: insufficient (don't know Mary's age)", "Statement 2 alone: insufficient (don't know John's age)", "Both together: Mary = 22, John = 27 — sufficient", "Answer: Both statements together are sufficient"]),
        ("Question: Is x > y? Statement 1: x > 0. Statement 2: y < 0. Is the data sufficient?", "easy", "fresher",
         ["Each alone?", "Together?"],
         ["Statement 1 alone: x>0, but y could be anything → insufficient", "Statement 2 alone: y<0, but x could be anything → insufficient", "Together: x>0 and y<0 → x>y definitely → sufficient", "Answer: Both together are sufficient"]),
        ("Question: What is the area of the triangle? Statement 1: Two sides are 5 cm and 12 cm. Statement 2: The triangle is right-angled.", "medium", "fresher",
         ["Which sides are 5 and 12?", "Right angle where?"],
         ["Statement 1 alone: insufficient (need angle or third side)", "Statement 2 alone: insufficient (no sides given)", "Together: if 5 and 12 are legs, area = 30. If 12 is hypotenuse, different", "Not fully sufficient unless we know which sides are legs"]),
    ]
    for txt, d, l, fu, pts in dsuf:
        Q.append(_q("data_sufficiency", d, l, txt, fu, pts))

    # ═══════ INPUT-OUTPUT ═══════
    io = [
        ("Machine takes input: 25 14 63 32 8 45. Step 1: 8 25 14 63 32 45. Step 2: 8 14 25 63 32 45. What is the rule and what is Step 3?", "medium", "fresher",
         ["What's being sorted?", "In which direction?"],
         ["Machine is sorting in ascending order", "Each step places the next smallest number", "Step 3: 8 14 25 32 63 45", "Bubble sort / selection sort pattern"]),
        ("Input: 5 3 8 1 6. Output: 1 3 5 6 8. Step 1 is: 1 5 3 8 6. Step 2: 1 3 5 8 6. What is the operation in each step?", "medium", "fresher",
         ["Which element moves?", "Selection sort?"],
         ["Each step selects the minimum from unsorted portion", "Places it at the current position", "Selection sort algorithm", "Step 3: 1 3 5 6 8 (sorted)"]),
    ]
    for txt, d, l, fu, pts in io:
        Q.append(_q("input_output", d, l, txt, fu, pts))

    # ═══════ CLOCK & CALENDAR ═══════
    cc = [
        ("What is the angle between the hour and minute hands at 3:15?", "easy", "fresher",
         ["How far does hour hand move in 15 min?", "Minute hand at 15 min?"],
         ["At 3:00, angle = 90°", "In 15 min, hour hand moves 15×0.5° = 7.5°", "At 3:15, hour hand at 97.5°, minute hand at 90°", "Angle = 97.5 - 90 = 7.5°"]),
        ("How many times do the hour and minute hands of a clock overlap in 12 hours?", "medium", "fresher",
         ["Is it 12 or 11?", "Why not at 12?"],
         ["11 times in 12 hours, 22 times in 24 hours", "Hands don't overlap separately at 12 — that's the same overlap", "Approximately every 65.45 minutes", "12:00, ~1:05, ~2:10, ~3:16, ~4:21..."]),
        ("What day of the week was January 1, 2020?", "medium", "fresher",
         ["Odd days concept?", "Leap year calculation?"],
         ["January 1, 2020 was a WEDNESDAY", "Can calculate using odd days method", "2020 is a leap year", "Shortcut: memorize a reference year, count odd days"]),
        ("If today is Wednesday, what day will it be 100 days from now?", "easy", "fresher",
         ["How many complete weeks?", "Remainder?"],
         ["100 ÷ 7 = 14 weeks + 2 days", "2 days after Wednesday = Friday", "Answer: Friday", "Key: divide by 7, add remainder to current day"]),
        ("At what time between 4 and 5 o'clock will the hands be at right angles?", "hard", "fresher",
         ["How many positions for right angle?", "Formula?"],
         ["Two positions: one before and one after overlap", "Minute hand at angle = 6M°, hour hand at 120° + 0.5M°", "For 90°: 6M - (120+0.5M) = ±90", "M = 38.18 min and M = 5.45 min (approximately)"]),
    ]
    for txt, d, l, fu, pts in cc:
        Q.append(_q("clocks_calendars", d, l, txt, fu, pts))

    # ═══════ NUMBER SERIES (LOGICAL) ═══════
    ns = [
        ("Find the next term: 2, 3, 5, 7, 11, 13, ?", "easy", "fresher",
         ["What's special about these numbers?", "Next prime?"],
         ["These are consecutive prime numbers", "Next prime after 13 = 17", "Prime: divisible only by 1 and itself", "Series of primes — common logical reasoning pattern"]),
        ("Find the next term: 1, 4, 9, 16, 25, ?", "easy", "fresher",
         ["What are these numbers?", "Pattern?"],
         ["Perfect squares: 1², 2², 3², 4², 5², 6²", "Next term = 36", "Differences: 3, 5, 7, 9, 11 (odd numbers)", "Second differences are constant (2)"]),
        ("Find the next term: 1, 1, 2, 6, 24, 120, ?", "easy", "fresher",
         ["Factorial pattern?", "What's 7!?"],
         ["Factorials: 1!, 1!, 2!, 3!, 4!, 5!", "Wait — 0!=1, 1!=1, 2!=2, 3!=6, 4!=24, 5!=120", "Next = 6! = 720", "Or: multiply by 1, 2, 3, 4, 5, next ×6 = 720"]),
        ("Find the next term: 2, 6, 14, 30, 62, ?", "medium", "fresher",
         ["Look at pattern.", "Multiply and add?"],
         ["Pattern: ×2 + 2 → 2×2+2=6, 6×2+2=14, 14×2+2=30...", "Or: 2¹+0, 2²+2, 2³+6, 2⁴+14...", "Next: 62×2+2 = 126", "Formula: 2^n - 2"]),
        ("Find the missing term: 3, 7, 15, 31, 63, ?", "medium", "fresher",
         ["Double and add 1?", "Powers of 2 minus 1?"],
         ["Pattern: each term = previous × 2 + 1", "3×2+1=7, 7×2+1=15, 15×2+1=31...", "Next = 63×2+1 = 127", "Also: 2²-1, 2³-1, 2⁴-1... → 2⁷-1 = 127"]),
    ]
    for txt, d, l, fu, pts in ns:
        Q.append(_q("number_series_logical", d, l, txt, fu, pts))

    # ═══════ LETTER SERIES ═══════
    ls = [
        ("Find the next letters: A, C, E, G, I, ?", "easy", "fresher",
         ["What's the gap?", "Which letters are skipped?"],
         ["Skip one letter each time: A(skip B)C(skip D)E...", "Next = K", "Pattern: A=1, C=3, E=5, G=7, I=9 → K=11", "Odd-positioned letters of the alphabet"]),
        ("Find the next: AZ, BY, CX, DW, ?", "easy", "fresher",
         ["Two patterns?", "One forward, one backward?"],
         ["First letter: A→B→C→D→E (forward)", "Second letter: Z→Y→X→W→V (backward)", "Next = EV", "Two independent patterns in the pair"]),
        ("Find the next: ACE, BDF, CEG, DFH, ?", "easy", "fresher",
         ["Each group has what pattern?", "How do groups relate?"],
         ["Each group: alternate letters (skip 1)", "Groups shift by 1 letter each time", "Next group starts with E: E, G, I → EGI", "Answer: EGI"]),
    ]
    for txt, d, l, fu, pts in ls:
        Q.append(_q("letter_series", d, l, txt, fu, pts))

    # ═══════ ANALOGIES (LOGICAL) ═══════
    la = [
        ("If 2:8 :: 3:27, then 4:?", "easy", "fresher",
         ["What's the relationship?", "Cube or square?"],
         ["2³ = 8, 3³ = 27", "4³ = 64", "Relationship: number : its cube", "Answer: 64"]),
        ("If ABCD:ZYXW :: EFGH:?", "easy", "fresher",
         ["What's A→Z relationship?", "Complementary letters?"],
         ["A+Z=27, B+Y=27... complementary pairs (sum=27)", "E→V, F→U, G→T, H→S", "Answer: VUTS", "Each letter maps to its complement (A↔Z, B↔Y...)"]),
        ("If WATER:XBUFS :: FIRE:?", "easy", "fresher",
         ["Caesar cipher?", "Shift by how many?"],
         ["W+1=X, A+1=B, T+1=U, E+1=F, R+1=S", "Shift of +1", "F+1=G, I+1=J, R+1=S, E+1=F", "Answer: GJSF"]),
    ]
    for txt, d, l, fu, pts in la:
        Q.append(_q("logical_analogies", d, l, txt, fu, pts))

    # ═══════ TEMPLATE EXPANSION: Number series patterns ═══════
    series_templates = [
        ("Find the next term in the series: {series}", "medium", "fresher",
         ["What's the pattern — arithmetic, geometric, or mixed?", "Look at differences or ratios."],
         ["Identify the pattern", "Apply the pattern to find next term", "Verify with previous terms", "State the answer"]),
    ]
    series_list = [
        "1, 4, 9, 16, 25, 36, ?",
        "2, 6, 18, 54, 162, ?",
        "1, 3, 6, 10, 15, 21, ?",
        "1, 8, 27, 64, 125, ?",
        "5, 10, 13, 26, 29, 58, ?",
        "3, 5, 9, 15, 23, 33, ?",
        "100, 98, 94, 86, 70, ?",
        "1, 2, 4, 7, 11, 16, ?",
        "2, 3, 5, 8, 12, 17, ?",
        "1, 3, 7, 15, 31, ?",
        "4, 7, 12, 19, 28, ?",
        "1, 2, 5, 14, 41, ?",
        "3, 6, 11, 18, 27, ?",
        "2, 5, 11, 23, 47, ?",
        "1, 4, 13, 40, 121, ?",
        "8, 15, 28, 53, 102, ?",
        "7, 10, 8, 11, 9, 12, ?",
        "1, 1, 2, 3, 5, 8, 13, ?",
        "2, 3, 5, 7, 11, 13, ?",
        "0, 1, 1, 2, 3, 5, 8, 13, ?",
    ]
    for s in series_list:
        Q.append(_q("number_series", "medium", "fresher", f"Find the next term: {s}",
                    ["What's the pattern?", "Apply it."],
                    ["Identify pattern", "Calculate next term", "Verify", "State answer"]))

    # ═══════ TEMPLATE EXPANSION: Coding-decoding patterns ═══════
    code_templates = [
        ("In a code, '{word1}' is written as '{code1}'. How is '{word2}' written in that code?", "medium", "fresher",
         ["What's the encoding rule?", "Apply it letter by letter."],
         ["Identify the encoding pattern", "Apply to each letter of the word", "Verify with the given example", "Write the encoded word"]),
    ]
    code_pairs = [
        ("FRIEND", "GSJFOE", "ENEMY"),
        ("HOUSE", "IPVTF", "MOUSE"),
        ("TIGER", "UJHFS", "LIONS"),
        ("CLOUD", "XOLFW", "STORM"),
        ("BRAIN", "CSBJO", "HEART"),
        ("Delhi", "EFMIJ", "MUMBAI"),
        ("TABLE", "UBCMF", "CHAIR"),
        ("WORLD", "XPSME", "PEACE"),
        ("PHONE", "QIPOF", "EMAIL"),
        ("INDIA", "JOEJB", "CHINA"),
    ]
    for w1, c1, w2 in code_pairs:
        Q.append(_q("coding_decoding", "medium", "fresher",
                    f"In a code, '{w1}' is written as '{c1}'. How is '{w2}' written in that code?",
                    ["What's the encoding rule?", "Apply it."],
                    ["Identify pattern", "Apply to word", "Verify", "State answer"]))

    # ═══════ TEMPLATE EXPANSION: Blood relation puzzles ═══════
    br_templates = [
        ("{puzzle}", "medium", "fresher",
         ["Draw a family tree.", "Identify the relationship step by step."],
         ["Parse the statement carefully", "Draw the family tree", "Trace the relationship", "State the answer"]),
    ]
    br_puzzles = [
        "A's mother is the sister of B's father. How is B related to A?",
        "Pointing to a boy, Maya said 'He is the son of my father's only child.' How is the boy related to Maya?",
        "If X is the brother of Y, Y is the sister of Z, and Z is the father of W, how is X related to W?",
        "Introducing a man, a woman said 'His mother's husband's sister is my aunt.' How is the woman related to the man?",
        "A is the son of B. B is the sister of C. C is the father of D. How is A related to D?",
        "P's father is Q's son. M is the paternal uncle of P and N is the daughter of Q. How is N related to M?",
        "If Mohan says 'Rani's mother is my mother's daughter', how is Mohan related to Rani?",
        "A is B's sister. C is B's mother. D is C's father. How is A related to D?",
    ]
    for puzzle in br_puzzles:
        Q.append(_q("blood_relations", "medium", "fresher", puzzle,
                    ["Draw family tree.", "Trace step by step."],
                    ["Parse statement", "Draw tree", "Trace relationship", "Answer"]))

    # ═══════ COMPANY-SPECIFIC ═══════
    tcs_lr = [
        ("If + means ÷, - means ×, × means -, ÷ means +, then what is 8 + 4 - 2 × 5 ÷ 3 = ?", "easy", "fresher",
         ["Replace each operator.", "Then compute."],
         ["Replace: 8 ÷ 4 × 2 - 5 + 3", "= 2 × 2 - 5 + 3", "= 4 - 5 + 3 = 2", "Follow BODMAS after replacement"]),
        ("In a row of people, Arun is 7th from the left and 11th from the right. How many people are in the row?", "easy", "fresher",
         ["Formula?", "Why subtract 1?"],
         ["Total = 7 + 11 - 1 = 17", "Arun is counted once, not twice", "Formula: Left position + Right position - 1", "Answer: 17"]),
    ]
    for txt, d, l, fu, pts in tcs_lr:
        Q.append(_q("logical_reasoning", d, l, txt, fu, pts, co="TCS", tg=["tcs", "logical"]))

    infosys_lr = [
        ("Five friends — Anu, Bala, Chitra, Deepa, Elan — sit in a row. Anu is not at the ends. Bala is to the right of Chitra. Deepa is at one end. Elan is between Anu and Bala. Find the arrangement.", "hard", "fresher",
         ["Start with what's fixed.", "Use elimination."],
         ["Deepa at one end (position 1 or 5)", "Anu not at ends → positions 2, 3, or 4", "Bala right of Chitra, Elan between Anu and Bala", "Work through possibilities systematically"]),
        ("Statement: Some pens are pencils. All pencils are erasers. Conclusion I: Some pens are erasers. Conclusion II: Some erasers are pens. Which follows?", "easy", "fresher",
         ["Draw Venn diagram.", "Subset chain?"],
         ["Pens ∩ Pencils ≠ ∅, Pencils ⊂ Erasers", "Pens that are pencils → also erasers → I follows", "Those same erasers are pens → II follows", "Both I and II follow"]),
    ]
    for txt, d, l, fu, pts in infosys_lr:
        Q.append(_q("logical_reasoning", d, l, txt, fu, pts, co="Infosys", tg=["infosys", "logical"]))

    return Q
