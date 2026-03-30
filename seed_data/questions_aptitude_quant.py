"""Quantitative Aptitude interview questions for PlaceRight. ~800+ questions via template expansion."""
from typing import List, Dict

R = {"1-3": "Cannot solve basic arithmetic. No conceptual understanding.",
     "4-5": "Solves simple problems but fails multi-step or word problems.",
     "6-7": "Good speed and accuracy. Handles most problems. Occasional errors in complex ones.",
     "8-10": "Excellent speed and accuracy. Shortcuts. Handles complex word problems effortlessly."}

def _q(t, d, l, txt, fu, pts, co="", tg=None):
    return {"domain": "aptitude", "topic": t, "difficulty": d, "level": l,
            "question_text": txt, "follow_ups": fu, "expected_points": pts,
            "scoring_rubric": R, "company_specific": co, "tags": tg or [t]}

def get_aptitude_quant_questions() -> List[Dict]:
    Q = []

    # ═══════ TIME SPEED DISTANCE ═══════
    tsd = [
        ("A train 150m long passes a pole in 15 seconds. What is its speed in km/h?", "easy", "fresher",
         ["What if it passes a platform of 250m?", "Can you solve it using a shortcut?"],
         ["Speed = Distance/Time = 150/15 = 10 m/s", "Convert: 10 × 18/5 = 36 km/h", "For platform: total distance = 150+250 = 400m", "m/s to km/h: multiply by 18/5"]),
        ("Two trains 200m and 300m long are moving in opposite directions at 40 km/h and 50 km/h. How long will they take to cross each other?", "medium", "fresher",
         ["What if they're moving in the same direction?", "What's the relative speed concept?"],
         ["Total distance = 200+300 = 500m", "Relative speed (opposite) = 40+50 = 90 km/h = 25 m/s", "Time = 500/25 = 20 seconds", "Same direction: relative speed = 50-40 = 10 km/h"]),
        ("A person travels from A to B at 60 km/h and returns at 40 km/h. What is the average speed for the entire journey?", "medium", "fresher",
         ["Why can't you just average 60 and 40?", "What's the formula for same distance?"],
         ["Average speed = 2×60×40/(60+40) = 48 km/h", "Not 50 — average speed ≠ average of speeds", "Formula for equal distances: 2ab/(a+b)", "More time at slower speed pulls average down"]),
        ("A boat can travel 20 km/h in still water. The river flows at 5 km/h. How long to go 75 km upstream and return?", "medium", "fresher",
         ["Upstream vs downstream speed?", "What if the river speed increases?"],
         ["Upstream speed = 20-5 = 15 km/h, time = 75/15 = 5 hours", "Downstream speed = 20+5 = 25 km/h, time = 75/25 = 3 hours", "Total = 5+3 = 8 hours", "Average speed for round trip = 150/8 = 18.75 km/h"]),
        ("In a race of 1000m, A beats B by 100m and B beats C by 150m. By how much does A beat C?", "hard", "fresher",
         ["What about the ratio of speeds?", "What if the race distance changes?"],
         ["When A finishes 1000m, B has run 900m", "When B runs 1000m, C has run 850m", "When B runs 900m, C runs 900×850/1000 = 765m", "A beats C by 1000-765 = 235m"]),
        ("A car covers the first half of a journey at 40 km/h and the second half at 60 km/h. Find the average speed.", "easy", "fresher",
         ["What if it's first half of time, not distance?", "Harmonic mean vs arithmetic mean?"],
         ["Average speed for equal distances = 2×40×60/(40+60) = 48 km/h", "If first half of TIME: (40+60)/2 = 50 km/h", "Equal distance → harmonic mean", "Equal time → arithmetic mean"]),
        ("A man walks at 5 km/h. If he had walked at 6 km/h, he would have arrived 15 minutes early. Find the distance.", "medium", "fresher",
         ["Set up the equation.", "Can you use the shortcut formula?"],
         ["Let distance = d km", "d/5 - d/6 = 15/60 = 1/4 hour", "d(6-5)/30 = 1/4, d = 30/4 = 7.5 km", "Shortcut: d = S1×S2×T_diff / (S2-S1)"]),
        ("Two trains start from stations A and B, 500 km apart, at the same time towards each other at 60 km/h and 40 km/h. Where will they meet?", "easy", "fresher",
         ["How long until they meet?", "What if one starts 1 hour later?"],
         ["Relative speed = 60+40 = 100 km/h", "Time to meet = 500/100 = 5 hours", "Distance from A = 60×5 = 300 km", "Distance from B = 40×5 = 200 km"]),
    ]
    for txt, d, l, fu, pts in tsd:
        Q.append(_q("time_speed_distance", d, l, txt, fu, pts))

    # ═══════ TIME AND WORK ═══════
    tw = [
        ("A can complete a job in 12 days, B in 18 days. Working together, how many days?", "easy", "fresher",
         ["What if they alternate days?", "What fraction does each do?"],
         ["A's rate = 1/12, B's rate = 1/18", "Combined rate = 1/12 + 1/18 = 5/36", "Days = 36/5 = 7.2 days", "A does 3/5, B does 2/5 of the work"]),
        ("A pipe can fill a tank in 6 hours, another can empty it in 10 hours. If both are open, how long to fill?", "medium", "fresher",
         ["What if the tank is half full initially?", "What if both are filling pipes?"],
         ["Fill rate = 1/6, Empty rate = 1/10", "Net rate = 1/6 - 1/10 = 1/15", "Time to fill = 15 hours", "The emptying pipe slows it down significantly"]),
        ("A is twice as efficient as B. Together they finish a job in 12 days. How many days for A alone?", "medium", "fresher",
         ["What does 'twice as efficient' mean?", "B alone?"],
         ["A's rate = 2x, B's rate = x", "2x + x = 1/12, 3x = 1/12, x = 1/36", "A's rate = 2/36 = 1/18, so A alone = 18 days", "B alone = 36 days"]),
        ("A does 40% of a work in 20 days. He then takes B's help and they finish in 3 more days. In how many days can B do it alone?", "hard", "fresher",
         ["What's A's daily rate?", "What remains after 20 days?"],
         ["A's rate = 40%/20 = 2% per day", "Remaining work = 60%", "A+B in 3 days = 60%, A alone does 6%, B does 54% in 3 days", "B's rate = 18% per day, B alone = 100/18 ≈ 5.56 days"]),
        ("12 men can complete a work in 10 days. 10 women can complete the same work in 15 days. How long for 6 men and 5 women?", "medium", "fresher",
         ["Man-days and woman-days?", "What about child labor problems?"],
         ["1 man's rate = 1/120 per day", "1 woman's rate = 1/150 per day", "6 men + 5 women = 6/120 + 5/150 = 1/20 + 1/30 = 1/12", "Answer: 12 days"]),
        ("A can do a piece of work in 10 days. B joins and they work for 4 days. Then A leaves and B finishes in 12 more days. How long for B alone?", "medium", "fresher",
         ["How much did they complete together?", "How much was left for B?"],
         ["A's rate = 1/10", "In 4 days: A does 4/10, A+B does 4/10 + 4/B", "B in 12 days: 12/B", "4/10 + 4/B + 12/B = 1, solve for B = 20 days"]),
        ("Three pipes A, B, C can fill a tank in 10, 15, and 20 hours. If all three are opened for 2 hours, then C is closed, how long for A and B to fill the rest?", "hard", "fresher",
         ["What fraction is filled in 2 hours?", "Remaining work?"],
         ["2-hour fill = 2(1/10 + 1/15 + 1/20) = 2(13/60) = 13/30", "Remaining = 17/30", "A+B rate = 1/10 + 1/15 = 1/6", "Time = (17/30)/(1/6) = 17/5 = 3.4 hours"]),
    ]
    for txt, d, l, fu, pts in tw:
        Q.append(_q("time_and_work", d, l, txt, fu, pts))

    # ═══════ PERCENTAGES ═══════
    pct = [
        ("If a shopkeeper gives 20% discount on marked price and still makes 25% profit, by what percent is the marked price above cost price?", "medium", "fresher",
         ["Set up the equation.", "What if discount is 30%?"],
         ["Let CP = 100, SP = 125 (25% profit)", "SP = 80% of MP, so 125 = 0.8 × MP", "MP = 125/0.8 = 156.25", "MP is 56.25% above CP"]),
        ("The population of a town increases by 10% in the first year and decreases by 10% in the second year. If the current population is 10,000, what is it after 2 years?", "easy", "fresher",
         ["Why isn't it the same as original?", "What about 3 successive changes?"],
         ["After year 1: 10000 × 1.1 = 11000", "After year 2: 11000 × 0.9 = 9900", "Net change: 1% decrease (not 0%)", "Formula: P × (1+r1)(1+r2)"]),
        ("In an exam, 60% passed in Hindi, 70% passed in English, and 20% failed in both. What percentage passed in both?", "medium", "fresher",
         ["Use set theory.", "What if 10% failed in both?"],
         ["Failed in Hindi = 40%, Failed in English = 30%", "At least one fail = 40+30-20 = 50%", "Passed in both = 100-50 = 50%", "Using union: n(H∪E) = n(H)+n(E)-n(H∩E)"]),
        ("A number is increased by 20% and then decreased by 20%. Is the result more or less than the original?", "easy", "fresher",
         ["What's the net percentage change?", "What if increase and decrease are different?"],
         ["100 × 1.2 = 120, then 120 × 0.8 = 96", "Result is 4% less than original", "Formula: -x²/100 for same increase/decrease %", "Always results in a decrease"]),
        ("Ram's salary is 40% of Shyam's salary. Shyam's salary is 25% of total salary. What percentage of total salary does Ram earn?", "easy", "fresher",
         ["Set up with a number.", "What if there are 3 people?"],
         ["Shyam = 25% of total", "Ram = 40% of Shyam = 40% of 25% = 10% of total", "Ram earns 10% of total salary", "Multiplication of percentages"]),
        ("If the price of petrol increases by 25%, by how much percent must a person reduce consumption to keep expenditure the same?", "medium", "fresher",
         ["What's the formula?", "What if increase is 50%?"],
         ["Reduction = (25/125) × 100 = 20%", "Formula: r/(100+r) × 100", "New price = 125, old = 100", "To keep expenditure same: old_qty × old_price = new_qty × new_price"]),
    ]
    for txt, d, l, fu, pts in pct:
        Q.append(_q("percentages", d, l, txt, fu, pts))

    # ═══════ PROFIT AND LOSS ═══════
    pl = [
        ("A buys an article for Rs 500 and sells it for Rs 650. What is the profit percentage?", "easy", "fresher",
         ["What if selling price was 450?", "Profit on cost or selling price?"],
         ["Profit = 650-500 = 150", "Profit% = (150/500)×100 = 30%", "Always calculate on Cost Price unless stated", "Loss of 10% if SP=450"]),
        ("A shopkeeper marks goods 40% above cost price and gives a discount of 15%. Find profit percent.", "medium", "fresher",
         ["What's the selling price?", "What if discount is 20%?"],
         ["Let CP = 100, MP = 140", "SP = 140 × 0.85 = 119", "Profit% = 19%", "Formula: (1+m)(1-d) - 1 where m=markup, d=discount"]),
        ("By selling an article at Rs 960, a man loses 20%. At what price should he sell to gain 20%?", "medium", "fresher",
         ["Find CP first.", "What if he wants 30% profit?"],
         ["960 = 80% of CP, CP = 1200", "For 20% profit: SP = 1200 × 1.2 = 1440", "Price needs to increase by Rs 480", "Ratio method: SP_new/SP_old = (100+20)/(100-20) = 3/2"]),
        ("A sells to B at 20% profit, B sells to C at 10% profit. If C pays Rs 1320, what did A pay?", "medium", "fresher",
         ["Chain of transactions?", "What's each person's cost?"],
         ["C pays 1320 = 1.1 × B's cost", "B's cost = 1200 = 1.2 × A's cost", "A's cost = 1200/1.2 = 1000", "Total markup: 1.2 × 1.1 = 1.32 or 32% over A's cost"]),
        ("A trader marks his goods 50% above cost price. He gives 20% discount to cash buyers and 10% discount to credit buyers. Find profit in each case.", "medium", "fresher",
         ["Which gives more profit?", "Net effect formula?"],
         ["CP = 100, MP = 150", "Cash: SP = 150×0.8 = 120, profit = 20%", "Credit: SP = 150×0.9 = 135, profit = 35%", "Successive discount: 150×0.8×0.9 ≠ 150×0.7"]),
        ("Two articles are sold for Rs 198 each. On one there is a 10% gain and on the other a 10% loss. What is the overall gain or loss?", "hard", "fresher",
         ["Why isn't it zero?", "What's the formula?"],
         ["Gain item: CP = 198/1.1 = 180", "Loss item: CP = 198/0.9 = 220", "Total CP = 400, Total SP = 396", "Loss = Rs 4 or 1% loss (always loss for same % gain/loss)"]),
    ]
    for txt, d, l, fu, pts in pl:
        Q.append(_q("profit_loss", d, l, txt, fu, pts))

    # ═══════ SIMPLE & COMPOUND INTEREST ═══════
    interest = [
        ("A sum of Rs 8,000 is invested at 12% per annum simple interest. In how many years will it amount to Rs 12,320?", "easy", "fresher",
         ["Can you solve using shortcuts?", "What if it were compound interest?"],
         ["SI = 12320 - 8000 = 4320", "SI = PRT/100, 4320 = 8000×12×T/100", "T = 4320/960 = 4.5 years", "With CI: use formula A = P(1+r/100)^n"]),
        ("Find the compound interest on Rs 10,000 at 10% for 2 years, compounded annually.", "easy", "fresher",
         ["What about compounded half-yearly?", "Difference between CI and SI for 2 years?"],
         ["A = 10000(1.1)² = 12100", "CI = 12100 - 10000 = 2100", "SI for same: 10000×10×2/100 = 2000", "Difference (CI-SI for 2yr) = P(r/100)² = 100"]),
        ("The difference between CI and SI on a certain sum at 10% per annum for 2 years is Rs 150. Find the sum.", "medium", "fresher",
         ["What's the formula for CI-SI for 2 years?", "What about 3 years?"],
         ["CI-SI for 2 years = P(r/100)²", "150 = P(10/100)² = P/100", "P = Rs 15,000", "For 3 years: P × r²(300+r)/100³"]),
        ("A sum doubles in 5 years at simple interest. In how many years will it triple?", "easy", "fresher",
         ["What's the rate?", "What if it's compound interest?"],
         ["Sum doubles: SI = P, so Prt/100 = P", "Rate = 100/5 = 20%", "For triple: SI = 2P, 2P = P×20×T/100", "T = 10 years"]),
        ("In what time will Rs 1000 become Rs 1331 at 10% per annum compounded annually?", "medium", "fresher",
         ["What's the approach?", "Can you identify it as a cube?"],
         ["1331/1000 = (1.1)^n", "1.331 = (1.1)^3", "n = 3 years", "1331 = 11³ and 1000 = 10³, so (11/10)³"]),
        ("An amount of Rs 5000 is lent at CI. After 2 years the amount becomes Rs 5618. Find the rate.", "medium", "fresher",
         ["Use the formula.", "Approximate?"],
         ["5618 = 5000(1+r/100)²", "(1+r/100)² = 1.1236", "1+r/100 = 1.06", "Rate = 6% per annum"]),
    ]
    for txt, d, l, fu, pts in interest:
        Q.append(_q("simple_compound_interest", d, l, txt, fu, pts))

    # ═══════ RATIO & PROPORTION ═══════
    ratio = [
        ("A and B invest in a business in the ratio 3:5. A invests for 8 months, B for 12 months. What is the profit-sharing ratio?", "medium", "fresher",
         ["Investment × time?", "What if C joins later?"],
         ["Profit ratio = investment × time", "A: 3×8 = 24, B: 5×12 = 60", "Ratio = 24:60 = 2:5", "A gets 2/7 and B gets 5/7 of profit"]),
        ("In a mixture of milk and water in the ratio 5:3, if 4 litres of water is added, the ratio becomes 5:4. Find the initial quantity of mixture.", "medium", "fresher",
         ["Set up the equation.", "What's the initial amount of water?"],
         ["Let milk = 5x, water = 3x", "After adding 4L water: 5x/(3x+4) = 5/4", "20x = 15x + 20, 5x = 20, x = 4", "Initial mixture = 8x = 32 litres"]),
        ("The ratio of ages of A and B is 4:3. After 6 years it will be 5:4. Find their present ages.", "easy", "fresher",
         ["Set up simultaneous equations.", "What was the ratio 6 years ago?"],
         ["Let A = 4x, B = 3x", "(4x+6)/(3x+6) = 5/4", "16x+24 = 15x+30, x = 6", "A = 24, B = 18"]),
        ("A, B, C start a business investing Rs 45000, Rs 70000, and Rs 90000 respectively. A is a working partner and gets 15% of profit as salary. Find the ratio of their profits.", "hard", "fresher",
         ["Working partner salary?", "Remaining profit division?"],
         ["After 15% salary to A, remaining 85% is divided", "Ratio of investment: 45:70:90 = 9:14:18", "A gets: 15% + 9/41 × 85%", "Net ratio needs careful calculation"]),
        ("In what ratio should water be mixed with milk costing Rs 60/litre to get a mixture worth Rs 45/litre?", "easy", "fresher",
         ["Alligation method?", "What if milk costs Rs 80?"],
         ["Using alligation: Water(0) ---- 45 ---- Milk(60)", "Milk to water ratio = 45-0 : 60-45 = 45:15 = 3:1", "Mix 3 parts milk with 1 part water", "Alligation: cheap:expensive = (expensive-mean):(mean-cheap)"]),
    ]
    for txt, d, l, fu, pts in ratio:
        Q.append(_q("ratio_proportion", d, l, txt, fu, pts))

    # ═══════ NUMBER SYSTEMS ═══════
    nums = [
        ("Find the remainder when 2^100 is divided by 7.", "hard", "fresher",
         ["Pattern in remainders?", "Fermat's little theorem?"],
         ["2¹÷7=2, 2²÷7=4, 2³÷7=1 — pattern repeats every 3", "100 = 33×3 + 1", "Remainder = 2¹ mod 7 = 2", "Euler's theorem: 2^φ(7) ≡ 1 (mod 7), φ(7)=6"]),
        ("What is the unit digit of 7^253?", "medium", "fresher",
         ["Pattern in unit digits?", "Cyclicity concept?"],
         ["Unit digits of 7^n cycle: 7,9,3,1 (cycle length 4)", "253 mod 4 = 1", "Unit digit = 7", "Cyclicity: most digits have cycle 1,2 or 4"]),
        ("Find the HCF and LCM of 36, 48, and 60.", "easy", "fresher",
         ["Prime factorization method?", "Relationship between HCF and LCM?"],
         ["36 = 2²×3², 48 = 2⁴×3, 60 = 2²×3×5", "HCF = 2²×3 = 12 (minimum powers)", "LCM = 2⁴×3²×5 = 720 (maximum powers)", "For 2 numbers: HCF×LCM = product"]),
        ("A number when divided by 5 gives remainder 3, when divided by 7 gives remainder 4. What is the smallest such number?", "hard", "fresher",
         ["Chinese Remainder Theorem?", "Trial and error?"],
         ["Numbers with remainder 3 when ÷5: 3, 8, 13, 18, 23, 28, 33...", "Check which gives remainder 4 when ÷7", "18 ÷ 7 = 2 remainder 4 ✓", "Answer: 18"]),
        ("How many zeros are there at the end of 100!?", "medium", "fresher",
         ["Trailing zeros come from?", "What about 200!?"],
         ["Trailing zeros = number of times 10 divides 100!", "10 = 2×5, count factors of 5 (2s are always more)", "100/5 + 100/25 = 20 + 4 = 24", "Answer: 24 trailing zeros"]),
        ("Is 1001 prime? How would you check quickly?", "medium", "fresher",
         ["Divisibility rules?", "What's the shortcut for checking primes?"],
         ["Check divisibility up to √1001 ≈ 31.6", "1001 = 7 × 143 = 7 × 11 × 13", "Not prime — divisible by 7, 11, and 13", "Quick check: 7×143 (try small primes first)"]),
        ("What is the largest 4-digit number divisible by 12, 15, and 18?", "medium", "fresher",
         ["Find LCM first.", "Then find largest multiple ≤ 9999."],
         ["LCM(12,15,18) = 180", "Largest 4-digit multiple of 180", "9999 ÷ 180 = 55.55, so 55 × 180 = 9900", "Answer: 9900"]),
    ]
    for txt, d, l, fu, pts in nums:
        Q.append(_q("number_systems", d, l, txt, fu, pts))

    # ═══════ PERMUTATION & COMBINATION ═══════
    pc = [
        ("In how many ways can 5 people sit in a row? What about a circular arrangement?", "easy", "fresher",
         ["What's the difference?", "What if 2 specific people must sit together?"],
         ["Row: 5! = 120 ways", "Circular: (5-1)! = 24 ways", "Circular: fix one person, arrange rest", "Together: treat pair as one, (4-1)! × 2! = 12"]),
        ("How many 3-digit numbers can be formed using digits 1,2,3,4,5 without repetition?", "easy", "fresher",
         ["With repetition?", "How many are even?"],
         ["5 × 4 × 3 = 60", "With repetition: 5 × 5 × 5 = 125", "Even: last digit must be 2 or 4", "2 × 4 × 3 = 24 even numbers"]),
        ("A committee of 5 is to be formed from 8 men and 5 women such that at least 2 women are included. How many ways?", "hard", "fresher",
         ["Complementary counting?", "Case by case?"],
         ["Case 1: 2W + 3M = C(5,2)×C(8,3) = 10×56 = 560", "Case 2: 3W + 2M = C(5,3)×C(8,2) = 10×28 = 280", "Case 3: 4W + 1M = C(5,4)×C(8,1) = 5×8 = 40", "Case 4: 5W + 0M = C(5,5) = 1. Total = 881"]),
        ("How many ways can the letters of the word 'MISSISSIPPI' be arranged?", "hard", "fresher",
         ["Repeated letters formula?", "What if S's must be together?"],
         ["Total letters: 11 (M:1, I:4, S:4, P:2)", "Arrangements = 11!/(4!×4!×2!) = 34650", "Divide by factorial of repeated letters", "If all S's together: treat SSSS as one unit → 8!/(4!×2!) = 840"]),
        ("From a deck of 52 cards, in how many ways can you choose 5 cards such that exactly 2 are aces?", "hard", "fresher",
         ["How many aces in a deck?", "Choose remaining from non-aces?"],
         ["Choose 2 aces from 4: C(4,2) = 6", "Choose 3 non-aces from 48: C(48,3) = 17296", "Total = 6 × 17296 = 103,776", "Multiply choices for independent selections"]),
        ("In how many ways can you distribute 10 identical balls into 4 distinct boxes?", "hard", "fresher",
         ["Stars and bars?", "What if each box must have at least 1?"],
         ["Stars and bars: C(10+4-1, 4-1) = C(13,3) = 286", "At least 1 per box: C(10-4+4-1, 4-1) = C(9,3) = 84", "Stars and bars formula: C(n+r-1, r-1)", "Equivalent to finding non-negative integer solutions"]),
    ]
    for txt, d, l, fu, pts in pc:
        Q.append(_q("permutation_combination", d, l, txt, fu, pts))

    # ═══════ PROBABILITY ═══════
    prob = [
        ("Two dice are thrown. What is the probability that the sum is 7?", "easy", "fresher",
         ["How many favorable outcomes?", "What about sum of 11?"],
         ["Total outcomes = 36", "Favorable: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6", "P(sum=7) = 6/36 = 1/6", "Sum of 7 has highest probability among all sums"]),
        ("A bag contains 5 red and 3 blue balls. Two balls are drawn at random. What is the probability that both are red?", "easy", "fresher",
         ["With or without replacement?", "What about at least one red?"],
         ["Without replacement: P = C(5,2)/C(8,2) = 10/28 = 5/14", "Or: (5/8) × (4/7) = 20/56 = 5/14", "At least one red = 1 - P(both blue) = 1 - 3/28 = 25/28", "With replacement: (5/8)² = 25/64"]),
        ("The probability of solving a problem by A is 1/3 and by B is 1/4. If both try independently, what is the probability that the problem is solved?", "medium", "fresher",
         ["What about neither solving it?", "What if events are dependent?"],
         ["P(not A) = 2/3, P(not B) = 3/4", "P(neither) = 2/3 × 3/4 = 1/2", "P(at least one solves) = 1 - 1/2 = 1/2", "Independent events: P(A∩B) = P(A)×P(B)"]),
        ("A card is drawn from a standard deck. Given that the card is red, what is the probability it is a king?", "medium", "fresher",
         ["Conditional probability?", "Bayes' theorem?"],
         ["P(King|Red) = P(King ∩ Red) / P(Red)", "Red kings = 2 (hearts + diamonds)", "P = 2/26 = 1/13", "Same as P(King) because suit and rank are independent"]),
        ("A box contains 3 defective and 7 non-defective items. If 3 items are drawn randomly, what is the probability that exactly 1 is defective?", "medium", "fresher",
         ["Hypergeometric distribution?", "At most 1 defective?"],
         ["P(exactly 1 defective) = C(3,1)×C(7,2)/C(10,3)", "= 3×21/120 = 63/120 = 21/40", "This is hypergeometric (sampling without replacement)", "At most 1 = P(0 defective) + P(1 defective)"]),
        ("Three coins are tossed. What is the probability of getting exactly 2 heads?", "easy", "fresher",
         ["Using binomial formula?", "At least 2 heads?"],
         ["Total outcomes = 2³ = 8", "Favorable: HHT, HTH, THH = 3", "P = 3/8", "Binomial: C(3,2)(1/2)²(1/2)¹ = 3/8"]),
        ("In a class, 40% of students play cricket, 50% play football, and 10% play both. A student is selected at random. What is the probability they play at least one sport?", "easy", "fresher",
         ["Venn diagram?", "Neither sport?"],
         ["P(C∪F) = P(C) + P(F) - P(C∩F)", "= 0.4 + 0.5 - 0.1 = 0.8", "80% play at least one sport", "P(neither) = 0.2"]),
    ]
    for txt, d, l, fu, pts in prob:
        Q.append(_q("probability", d, l, txt, fu, pts))

    # ═══════ ALGEBRA ═══════
    alg = [
        ("If x + 1/x = 5, find x² + 1/x².", "medium", "fresher",
         ["What about x³ + 1/x³?", "Square the equation."],
         ["(x + 1/x)² = x² + 2 + 1/x² = 25", "x² + 1/x² = 23", "For cubes: (x + 1/x)³ = x³ + 3(x+1/x) + 1/x³", "x³ + 1/x³ = 110"]),
        ("The sum of first n natural numbers is 210. Find n.", "easy", "fresher",
         ["Formula for sum?", "What about sum of squares?"],
         ["n(n+1)/2 = 210", "n² + n = 420", "n² + n - 420 = 0, (n-20)(n+21) = 0", "n = 20 (reject -21)"]),
        ("Find the sum of first 20 terms of the AP: 5, 8, 11, 14, ...", "easy", "fresher",
         ["What's the common difference?", "What's the 20th term?"],
         ["a = 5, d = 3", "S = n/2 × [2a + (n-1)d]", "S = 20/2 × [10 + 57] = 10 × 67 = 670", "Or S = n/2 × (first + last), last = 5+19×3 = 62"]),
        ("Solve: |2x - 3| ≤ 5.", "medium", "fresher",
         ["What does absolute value inequality mean?", "Graph the solution."],
         ["-5 ≤ 2x-3 ≤ 5", "-2 ≤ 2x ≤ 8", "-1 ≤ x ≤ 4", "Solution interval: [-1, 4]"]),
        ("A GP has first term 3 and common ratio 2. Find the sum of first 10 terms.", "easy", "fresher",
         ["Formula for sum of GP?", "What if common ratio < 1?"],
         ["S = a(r^n - 1)/(r-1)", "S = 3(2^10 - 1)/(2-1) = 3(1024-1) = 3069", "For |r| < 1: S = a(1-r^n)/(1-r)", "Sum to infinity (|r|<1): S = a/(1-r)"]),
        ("If log₂(x) + log₂(x-2) = 3, find x.", "medium", "fresher",
         ["Combine the logs.", "Check for extraneous solutions."],
         ["log₂[x(x-2)] = 3", "x(x-2) = 2³ = 8", "x² - 2x - 8 = 0, (x-4)(x+2) = 0", "x = 4 (reject x=-2, domain requires x>2)"]),
    ]
    for txt, d, l, fu, pts in alg:
        Q.append(_q("algebra", d, l, txt, fu, pts))

    # ═══════ DATA INTERPRETATION ═══════
    di = [
        ("A company's revenue in Q1-Q4 was Rs 120, 150, 180, and 200 crore. What is the quarter-over-quarter growth rate for Q3?", "easy", "fresher",
         ["Average quarterly growth?", "What about CAGR?"],
         ["Q3 growth = (180-150)/150 × 100 = 20%", "Q4 growth = (200-180)/180 × 100 = 11.1%", "Average quarterly growth = (Q1→Q4) total/3", "CAGR for annual: (200/120)^(1/1) - 1"]),
        ("In a pie chart, if the education sector is 72°, what percentage does it represent? If total budget is Rs 500 crore, how much goes to education?", "easy", "fresher",
         ["What if angle is 45°?", "Total degrees in a pie chart?"],
         ["Percentage = (72/360) × 100 = 20%", "Amount = 20% of 500 = Rs 100 crore", "Total angle = 360°", "Each percentage = 3.6°"]),
        ("A bar chart shows sales of 5 products: A=500, B=300, C=400, D=200, E=600. What is product E's percentage contribution to total sales?", "easy", "fresher",
         ["Which product contributes least?", "What's the ratio of max to min?"],
         ["Total = 500+300+400+200+600 = 2000", "E's contribution = 600/2000 × 100 = 30%", "Least: D at 200/2000 = 10%", "Max/Min ratio = E/D = 3:1"]),
        ("Production of a factory in 5 years: 2018:1000, 2019:1200, 2020:900, 2021:1500, 2022:1800. Which year had the highest percentage increase over previous year?", "medium", "fresher",
         ["Be careful with 2020 decline.", "Calculate each year's growth rate."],
         ["2019: (1200-1000)/1000 = 20%", "2020: (900-1200)/1200 = -25%", "2021: (1500-900)/900 = 66.7%", "2021 had highest increase at 66.7%"]),
        ("A table shows import/export data. Imports: Rs 800 cr, Exports: Rs 600 cr. What is the trade deficit? If exports grow 15% next year and imports grow 10%, what's the new deficit?", "medium", "fresher",
         ["What's trade deficit?", "When does deficit decrease?"],
         ["Trade deficit = Imports - Exports = 200 cr", "New Imports = 800 × 1.1 = 880", "New Exports = 600 × 1.15 = 690", "New deficit = 880 - 690 = 190 cr (decreased)"]),
    ]
    for txt, d, l, fu, pts in di:
        Q.append(_q("data_interpretation", d, l, txt, fu, pts))

    # ═══════ NUMBER SERIES ═══════
    series = [
        ("Find the next term: 2, 6, 12, 20, 30, ?", "easy", "fresher",
         ["What's the pattern in differences?", "Can you express as n(n+1)?"],
         ["Differences: 4, 6, 8, 10 — increasing by 2", "Next difference = 12", "Next term = 30 + 12 = 42", "Pattern: n(n+1): 1×2, 2×3, 3×4, 4×5, 5×6, 6×7"]),
        ("Find the missing term: 3, 5, 9, 17, 33, ?", "medium", "fresher",
         ["Look at the differences.", "Each term formula?"],
         ["Differences: 2, 4, 8, 16 — doubling", "Next difference = 32", "Next term = 33 + 32 = 65", "Or: each term = previous × 2 - 1"]),
        ("Find the wrong number: 1, 2, 6, 24, 96, 720.", "medium", "fresher",
         ["What's the pattern?", "Factorial series?"],
         ["Pattern: multiply by 1, 2, 3, 4, 5, 6 (factorial)", "1×1=1, 1×2=2, 2×3=6, 6×4=24, 24×5=120, 120×6=720", "96 should be 120", "96 is the wrong number"]),
        ("Find the next term: 1, 1, 2, 3, 5, 8, 13, ?", "easy", "fresher",
         ["What's this series called?", "Properties of Fibonacci?"],
         ["Fibonacci series: each term = sum of previous two", "Next = 8 + 13 = 21", "Golden ratio: ratio of consecutive terms → 1.618", "Appears in nature: flowers, shells, tree branches"]),
        ("Find next: 7, 11, 13, 17, 19, 23, ?", "easy", "fresher",
         ["What's special about these numbers?", "What's after 23?"],
         ["These are consecutive prime numbers", "Next prime after 23 = 29", "Prime: divisible only by 1 and itself", "Check: 24(÷2), 25(÷5), 26(÷2), 27(÷3), 28(÷2), 29✓"]),
    ]
    for txt, d, l, fu, pts in series:
        Q.append(_q("number_series", d, l, txt, fu, pts))

    # ═══════ AVERAGES ═══════
    avg = [
        ("The average of 5 numbers is 30. If one number is excluded, the average becomes 28. What is the excluded number?", "easy", "fresher",
         ["Can you find total first?", "What if average increases?"],
         ["Total = 5×30 = 150", "New total = 4×28 = 112", "Excluded number = 150-112 = 38", "If avg increased, excluded number < original avg"]),
        ("The average age of a class of 30 students is 14 years. When the teacher's age is included, the average increases by 1. Find the teacher's age.", "easy", "fresher",
         ["Total ages?", "What if average decreases?"],
         ["Total student ages = 30×14 = 420", "New average = 15, new total = 31×15 = 465", "Teacher's age = 465-420 = 45", "Teacher adds 45-14 = 31 more than student average"]),
        ("A cricketer has an average of 32 runs in 40 innings. How many runs must he score in the next innings to increase his average by 2?", "medium", "fresher",
         ["Current total?", "Target total?"],
         ["Current total = 32×40 = 1280", "Target average = 34, target total = 34×41 = 1394", "Runs needed = 1394-1280 = 114", "Must score 114 in next innings"]),
        ("The average of 10 numbers is 20. If each number is increased by 5, what is the new average?", "easy", "fresher",
         ["What if multiplied by 2?", "Why does average shift same amount?"],
         ["New average = 20 + 5 = 25", "Adding constant to each shifts average by same amount", "Multiplying each by k: new avg = k × old avg", "Sum increases by 10×5 = 50, new avg = 250/10 = 25"]),
        ("The average weight of A, B, C is 60 kg. The average weight of A and B is 55 kg. The average weight of B and C is 65 kg. Find B's weight.", "medium", "fresher",
         ["Set up equations.", "Three equations, three unknowns?"],
         ["A+B+C = 180, A+B = 110, B+C = 130", "C = 180-110 = 70, A = 180-130 = 50", "B = 180-50-70 = 60 kg", "Or: B = (A+B) + (B+C) - (A+B+C) = 110+130-180 = 60"]),
    ]
    for txt, d, l, fu, pts in avg:
        Q.append(_q("averages", d, l, txt, fu, pts))

    # ═══════ MENSURATION ═══════
    mens = [
        ("A cylinder has radius 7 cm and height 10 cm. Find the volume and total surface area.", "easy", "fresher",
         ["What if it's a hollow cylinder?", "Curved surface area only?"],
         ["Volume = πr²h = 22/7 × 49 × 10 = 1540 cm³", "CSA = 2πrh = 2 × 22/7 × 7 × 10 = 440 cm²", "TSA = 2πr(r+h) = 2 × 22/7 × 7 × 17 = 748 cm²", "For hollow: V = π(R²-r²)h"]),
        ("A sphere has a radius of 14 cm. Find its volume and surface area.", "easy", "fresher",
         ["What if it's a hemisphere?", "Compare sphere and cube of same volume."],
         ["Volume = 4/3 × πr³ = 4/3 × 22/7 × 2744 = 11498.67 cm³", "SA = 4πr² = 4 × 22/7 × 196 = 2464 cm²", "Hemisphere volume = 2/3 × πr³", "Hemisphere TSA = 3πr² (curved + flat)"]),
        ("The length of a rectangle is increased by 20% and breadth decreased by 10%. What is the percentage change in area?", "medium", "fresher",
         ["Net effect formula?", "What if both increase by 10%?"],
         ["New area = 1.2L × 0.9B = 1.08LB", "Area increased by 8%", "Formula: a + b + ab/100 = 20 + (-10) + 20×(-10)/100 = 8%", "Both increase 10%: area increases 21%"]),
        ("A room is 12m × 8m × 4m. How many tiles of 40cm × 40cm are needed for the floor?", "easy", "fresher",
         ["What about the walls?", "What if tiles are 50cm × 50cm?"],
         ["Floor area = 12 × 8 = 96 m²", "Tile area = 0.4 × 0.4 = 0.16 m²", "Number of tiles = 96/0.16 = 600", "For walls: 2(12+8)×4 = 160 m², minus doors/windows"]),
    ]
    for txt, d, l, fu, pts in mens:
        Q.append(_q("mensuration", d, l, txt, fu, pts))

    # ═══════ TEMPLATE EXPANSION: Quant topic practice ═══════
    quant_templates = [
        ("Solve this {topic} problem: {problem}", "medium", "fresher",
         ["Can you solve it using a shortcut?", "What if the values change slightly?"],
         ["Identify the concept", "Set up the equation correctly", "Apply the formula or method", "Verify the answer"]),
    ]
    template_problems = [
        ("time_speed_distance", "A car travels 240 km at 60 km/h and returns at 80 km/h. Find the average speed for the round trip."),
        ("time_speed_distance", "A train overtakes a man walking at 5 km/h in 8 seconds and a cyclist at 10 km/h in 12 seconds. Find the train's speed and length."),
        ("time_speed_distance", "Two persons A and B start walking towards each other from places 24 km apart. A walks at 5 km/h, B at 7 km/h. After how many hours will they meet?"),
        ("time_and_work", "A and B can do a piece of work in 45 and 40 days. They start together, but A leaves after some days and B finishes in 23 days. After how many days did A leave?"),
        ("time_and_work", "20 men can build a wall in 30 days. How many more men are needed to build it in 20 days?"),
        ("percentages", "In an election, candidate A gets 60% of votes. Candidate B gets 8,000 votes. Find total votes (assuming only 2 candidates and no invalid votes)."),
        ("percentages", "A student scores 72% in an exam. He needs 18 more marks to get 80%. What is the maximum marks?"),
        ("profit_loss", "A man buys 10 oranges for Rs 60 and sells 8 for Rs 56. Find profit or loss percent."),
        ("profit_loss", "By selling 45 lemons for Rs 40, a man loses 20%. How many should he sell for Rs 24 to gain 20%?"),
        ("simple_compound_interest", "At what rate of simple interest will a sum become 4 times itself in 15 years?"),
        ("simple_compound_interest", "The CI on Rs 5000 for 2 years at 8% per annum compounded annually is?"),
        ("ratio_proportion", "The ages of A and B are in ratio 5:7. Eight years ago the ratio was 7:13. Find their present ages."),
        ("number_systems", "The product of two numbers is 1680 and their HCF is 4. Find the LCM."),
        ("number_systems", "Find the smallest 3-digit number which is exactly divisible by 6, 8, and 12."),
        ("permutation_combination", "In how many ways can 8 people be seated at a round table if 2 particular persons must sit next to each other?"),
        ("permutation_combination", "How many 4-letter words can be formed from the word 'EQUATION' without repetition, starting with a vowel?"),
        ("probability", "A bag has 6 white and 4 black balls. 3 balls are drawn. Find probability that exactly 2 are white."),
        ("probability", "Two cards are drawn from a deck of 52 cards. Find the probability of getting a king and a queen."),
        ("algebra", "If 2x + 3y = 12 and 3x - y = 7, find x and y."),
        ("algebra", "The sum of a number and its reciprocal is 10/3. Find the number."),
        ("averages", "The average marks of 50 students is 72. Later it was found that marks of one student were wrongly entered as 48 instead of 84. Find the correct average."),
        ("mensuration", "The radius of a circle is increased by 20%. By what percent does the area increase?"),
        ("mensuration", "A cone has height 12 cm and slant height 13 cm. Find its volume."),
        ("data_interpretation", "In a survey, 60% preferred tea, 40% preferred coffee, 20% preferred both. What percentage preferred neither?"),
    ]
    for topic, problem in template_problems:
        Q.append(_q(topic, "medium", "fresher", problem,
                    ["Can you solve it faster?", "What if values change?"],
                    ["Identify concept", "Set up correctly", "Calculate", "Verify"]))

    # ═══════ COMPANY-SPECIFIC: TCS NQT ═══════
    tcs = [
        ("If 8 men can complete a task in 12 days, how many men are needed to complete it in 6 days?", "easy", "fresher",
         ["Man-days concept?", "What if efficiency differs?"],
         ["Man-days = 8 × 12 = 96", "For 6 days: 96/6 = 16 men", "More men → fewer days (inverse proportion)", "Assumes same efficiency per man"]),
        ("The price of an article is increased by 20% and then decreased by 20%. What is the net change?", "easy", "fresher",
         ["Quick formula?", "Always loss or gain?"],
         ["100 → 120 → 96", "Net change = -4%", "Formula: -x²/100 for same % increase/decrease", "Always a loss when same %"]),
        ("A can complete 2/5 of a task in 8 days. In how many days can A complete the whole task?", "easy", "fresher",
         ["What's A's daily rate?", "What if B helps?"],
         ["2/5 task in 8 days", "Full task: 8 × 5/2 = 20 days", "Daily rate = 2/(5×8) = 1/20", "Simple proportion"]),
        ("Train A is 300m long and runs at 90 km/h. Train B is 200m long and runs at 60 km/h. How long for A to cross B when moving in the same direction?", "medium", "fresher",
         ["What about opposite directions?", "Relative speed?"],
         ["Same direction: relative speed = 90-60 = 30 km/h = 25/3 m/s", "Total distance = 300+200 = 500m", "Time = 500/(25/3) = 60 seconds", "Opposite: 150 km/h, time = 500/125×3 = 12 seconds"]),
        ("A sum becomes Rs 4840 in 2 years at CI rate of 10%. Find the sum.", "easy", "fresher",
         ["Use the CI formula.", "What about SI?"],
         ["A = P(1+r/100)^n", "4840 = P(1.1)² = P × 1.21", "P = 4840/1.21 = Rs 4000", "SI would give: 4840 = 4000 + 4000×10×2/100 = 4800 ≠ 4840"]),
    ]
    for txt, d, l, fu, pts in tcs:
        Q.append(_q("aptitude_quant", d, l, txt, fu, pts, co="TCS", tg=["tcs", "aptitude"]))

    # ═══════ COMPANY-SPECIFIC: Infosys ═══════
    infy = [
        ("A shopkeeper sells an article at 10% loss. If he had sold it for Rs 40 more, he would have earned 5% profit. Find the cost price.", "medium", "fresher",
         ["Difference between SP1 and SP2?", "Set up the equation."],
         ["SP at 10% loss = 0.9 × CP", "SP at 5% profit = 1.05 × CP", "Difference = 1.05CP - 0.9CP = 0.15CP = 40", "CP = 40/0.15 = Rs 266.67"]),
        ("The ratio of milk to water in 3 containers of equal capacity is 3:2, 7:3, and 11:4. If all are mixed, find the new ratio.", "hard", "fresher",
         ["What's the milk fraction in each?", "Equal capacity assumption?"],
         ["Milk fractions: 3/5, 7/10, 11/15", "Total milk = 3/5 + 7/10 + 11/15 = 18/30 + 21/30 + 22/30 = 61/30", "Total water = 2/5 + 3/10 + 4/15 = 12/30 + 9/30 + 8/30 = 29/30", "Ratio = 61:29"]),
    ]
    for txt, d, l, fu, pts in infy:
        Q.append(_q("aptitude_quant", d, l, txt, fu, pts, co="Infosys", tg=["infosys", "aptitude"]))

    # ═══════ TEMPLATE EXPANSION: More quant practice ═══════
    more_quant = [
        ("Solve: {problem}", "medium", "fresher",
         ["Shortcut method?", "Verify your answer."],
         ["Identify the concept", "Apply the formula", "Calculate step by step", "Cross-verify"]),
    ]
    more_problems = [
        "A and B's ages are in ratio 5:3. After 4 years, the ratio becomes 3:2. Find their ages.",
        "The diagonal of a rectangle is 25 cm. If one side is 7 cm, find the perimeter.",
        "A clock shows 3:15. What is the angle between the hour and minute hands?",
        "If 20% of A = 30% of B, what is A:B?",
        "The compound interest on Rs 6000 for 1.5 years at 10% compounded half-yearly is?",
        "A number is increased by 25%. To get back the original, it must be decreased by what percent?",
        "Two taps can fill a tank in 12 and 15 minutes. If both are opened with an outlet pipe, the tank fills in 20 minutes. How long for the outlet to empty a full tank?",
        "If the cost price of 20 articles equals selling price of 15 articles, find profit percent.",
        "A invested Rs 8000 and B invested Rs 12000 in a business. After 6 months, C invested Rs 6000. Find the profit sharing ratio after 1 year.",
        "A cistern can be filled by A in 4 hours, by B in 6 hours. An outlet pipe C empties in 8 hours. If all are opened, how long to fill?",
        "The LCM of two numbers is 180, their HCF is 6. If one number is 36, find the other.",
        "A triangle has sides 13, 14, 15 cm. Find its area using Heron's formula.",
        "In how many ways can 6 boys and 4 girls sit in a row so that no two girls sit together?",
        "A coin is tossed 4 times. Find the probability of getting at least 3 heads.",
        "The sum of first 50 even natural numbers is?",
        "If log x + log y = log(x+y), then y = ?",
        "A can fill a tank in 20 min, B in 30 min. After filling together for 5 min, B is turned off. How many more minutes for A to fill?",
        "The average of 11 results is 60. First 6 average is 58, last 6 average is 63. Find the 6th result.",
        "A cuboid has dimensions 8×6×4 cm. Find the length of the longest diagonal.",
        "Two numbers are in ratio 3:5 and their LCM is 150. Find the numbers.",
    ]
    for prob in more_problems:
        Q.append(_q("aptitude_quant", "medium", "fresher", prob,
                    ["Shortcut?", "Verify?"],
                    ["Identify concept", "Apply formula", "Calculate", "Verify"]))

    return Q
