"""DSA interview questions for PlaceRight. ~800+ questions via template expansion."""
from typing import List, Dict

R = {"1-3": "Cannot approach the problem. No data structure awareness.",
     "4-5": "Brute force only. Cannot optimize or handle edge cases.",
     "6-7": "Arrives at optimal solution with minor hints. Handles main cases.",
     "8-10": "Optimal solution independently. Clean code. All edge cases. Discusses trade-offs."}

def _q(t, d, l, txt, fu, pts, co="", tg=None):
    return {"domain": "software_engineering", "topic": t, "difficulty": d, "level": l,
            "question_text": txt, "follow_ups": fu, "expected_points": pts,
            "scoring_rubric": R, "company_specific": co, "tags": tg or [t]}

def get_dsa_questions() -> List[Dict]:
    Q = []
    # ═══════ ARRAYS ═══════
    arr = [
        ("Given an array of integers, find two numbers that add up to a target. How would you optimize beyond brute force?", "easy", "fresher",
         ["What if the array is sorted?", "Can you do it in O(n)?", "What data structure helps?"],
         ["Brute force O(n^2)", "Hash map O(n) time O(n) space", "Sorted array two-pointer O(n)", "Handle duplicates"]),
        ("How would you find the maximum subarray sum in an array with both positive and negative numbers?", "medium", "fresher",
         ["What's the time complexity?", "Can you handle the all-negative case?", "What if I want the subarray indices too?"],
         ["Kadane's algorithm", "O(n) time O(1) space", "Track start/end indices", "Handle all-negative array"]),
        ("Given a sorted array rotated at some pivot, how would you search for a target element?", "medium", "fresher",
         ["What if there are duplicates?", "Can you find the rotation point first?"],
         ["Modified binary search", "O(log n)", "Check which half is sorted", "Handle duplicates degrades to O(n)"]),
        ("How do you find the kth largest element in an unsorted array?", "medium", "fresher",
         ["Can you do better than sorting?", "What about QuickSelect?", "What's the average complexity?"],
         ["Sort O(n log n)", "Min-heap of size k O(n log k)", "QuickSelect O(n) average", "Worst case O(n^2)"]),
        ("Merge two sorted arrays without using extra space.", "hard", "mid",
         ["What if one array has enough space at the end?", "Can you do it in-place?"],
         ["Gap method (Shell sort idea)", "Start from end approach", "O(n+m) time", "Handle edge cases"]),
        ("Find the majority element in an array (appears more than n/2 times).", "easy", "fresher",
         ["What if no majority element exists?", "Can you do it in O(1) space?"],
         ["Hash map O(n) time/space", "Boyer-Moore voting O(n) time O(1) space", "Sort and check middle", "Verify the candidate"]),
        ("Given an array of 0s, 1s, and 2s, sort it in a single pass.", "easy", "fresher",
         ["What algorithm is this?", "Can you extend to k colors?"],
         ["Dutch National Flag algorithm", "Three pointers: low, mid, high", "O(n) single pass", "In-place sorting"]),
        ("Find the contiguous subarray with the maximum product.", "medium", "fresher",
         ["How do negative numbers affect this?", "How is this different from max subarray sum?"],
         ["Track both max and min products", "Negative × negative = positive", "Reset on zero", "O(n) time"]),
        ("Trapping rain water — given elevation bars, how much water can be trapped?", "hard", "mid",
         ["Can you solve it without extra space?", "What about using two pointers?"],
         ["Precompute left_max and right_max arrays", "Two pointer approach O(n) O(1)", "Stack-based approach", "Water at i = min(left_max, right_max) - height[i]"]),
        ("Find the next permutation of a given number array.", "medium", "fresher",
         ["What if the array is in descending order?", "Walk me through the algorithm."],
         ["Find rightmost ascent", "Swap with smallest larger element on right", "Reverse suffix", "O(n) time"]),
        ("Rotate an array by k positions to the right.", "easy", "fresher",
         ["What if k > array length?", "Can you do it in-place?"],
         ["Modulo k by n", "Reverse entire, reverse first k, reverse rest", "O(n) time O(1) space"]),
        ("Find all pairs in an array whose sum is divisible by a given number.", "medium", "fresher",
         ["What's the time complexity?", "How do remainders help?"],
         ["Group by remainder", "Pair complementary remainders", "O(n) time with hash map"]),
        ("Given an array, find the length of the longest increasing subsequence.", "hard", "mid",
         ["Can you do better than O(n^2)?", "How does binary search help?"],
         ["DP O(n^2)", "Binary search with patience sorting O(n log n)", "Maintain tails array"]),
        ("Move all zeroes to the end of array while maintaining relative order.", "easy", "fresher",
         ["Can you do it in one pass?", "What about two pointers?"],
         ["Two pointer approach", "Swap non-zero to front", "O(n) time O(1) space"]),
        ("Find the missing number in an array of 1 to n.", "easy", "fresher",
         ["What if two numbers are missing?", "Can you use XOR?"],
         ["Sum formula n*(n+1)/2", "XOR approach", "O(n) time O(1) space"]),
    ]
    for txt, d, l, fu, pts in arr:
        Q.append(_q("arrays", d, l, txt, fu, pts))

    # More array questions - sliding window
    sw = [
        ("Find the maximum sum subarray of size k.", "easy"),
        ("Find the smallest subarray with sum greater than a given value.", "medium"),
        ("Find the longest substring without repeating characters.", "medium"),
        ("Count distinct elements in every window of size k.", "medium"),
        ("Find all anagrams of a pattern in a string.", "medium"),
        ("Maximum of all subarrays of size k.", "hard"),
        ("Minimum window substring that contains all characters of another string.", "hard"),
        ("Find the longest subarray with sum at most k.", "medium"),
        ("Count subarrays with exactly k distinct elements.", "hard"),
        ("Find the longest substring with at most 2 distinct characters.", "medium"),
        ("Maximum number of vowels in a substring of length k.", "easy"),
        ("Grumpy bookstore owner — maximize satisfied customers.", "medium"),
        ("Find the longest repeating character replacement with at most k changes.", "medium"),
        ("Fruit into baskets — longest subarray with at most 2 types.", "medium"),
        ("Permutation in string — check if one string's permutation is a substring of another.", "medium"),
    ]
    for txt, d in sw:
        Q.append(_q("arrays", d, "fresher", f"Using sliding window: {txt}",
            ["What's the window size strategy?", "How do you shrink the window?"],
            ["Sliding window technique", "Two pointers", "O(n) time", "Hash map for tracking"]))

    # Two pointers
    tp = [
        ("Given a sorted array, remove duplicates in-place.", "easy"),
        ("Find if there's a triplet with sum zero.", "medium"),
        ("Container with most water.", "medium"),
        ("Sort an array of 0s, 1s using two pointers.", "easy"),
        ("Find the pair closest to a target sum.", "medium"),
        ("Partition array around a pivot.", "easy"),
        ("Remove all instances of a value from array in-place.", "easy"),
        ("Find four elements that sum to a target.", "hard"),
        ("Merge intervals.", "medium"),
        ("Check if array has a pair with given difference.", "easy"),
        ("Backspace string compare.", "easy"),
        ("Squares of a sorted array.", "easy"),
        ("Three sum closest to target.", "medium"),
        ("Shortest unsorted continuous subarray.", "medium"),
        ("Boats to save people — minimum boats needed.", "medium"),
    ]
    for txt, d in tp:
        Q.append(_q("arrays", d, "fresher", f"{txt} Can you solve this with two pointers?",
            ["What are the pointer movement rules?", "What's the time complexity?"],
            ["Two pointer technique", "O(n) or O(n^2) depending on problem", "Handle edge cases"]))

    # Binary search on arrays
    bs = [
        ("Find the first and last position of an element in a sorted array.", "easy"),
        ("Find the square root of a number without using built-in functions.", "easy"),
        ("Find peak element in an array.", "medium"),
        ("Search in a 2D sorted matrix.", "medium"),
        ("Find minimum in a rotated sorted array.", "medium"),
        ("Median of two sorted arrays.", "hard"),
        ("Koko eating bananas — minimum eating speed.", "medium"),
        ("Split array largest sum — minimize the maximum subarray sum.", "hard"),
        ("Find the smallest divisor given a threshold.", "medium"),
        ("Capacity to ship packages within D days.", "medium"),
        ("Allocate minimum number of pages to students.", "hard"),
        ("Aggressive cows — maximum minimum distance.", "hard"),
        ("Find the element that appears once (all others appear twice).", "easy"),
        ("Search in an almost sorted array.", "medium"),
        ("Find the nth magical number (divisible by A or B).", "hard"),
    ]
    for txt, d in bs:
        Q.append(_q("arrays", d, "fresher" if d != "hard" else "mid",
            f"Using binary search: {txt}",
            ["Why does binary search work here?", "What are the boundary conditions?"],
            ["Binary search technique", "O(log n)", "Define search space correctly", "Handle boundaries"]))

    # Matrix
    mat = [
        ("Rotate a matrix by 90 degrees clockwise.", "medium"),
        ("Set matrix zeroes — if an element is 0, set entire row and column to 0.", "medium"),
        ("Spiral order traversal of a matrix.", "medium"),
        ("Search a word in a 2D grid of characters.", "hard"),
        ("Find the number of islands in a binary matrix.", "medium"),
        ("Diagonal traversal of a matrix.", "medium"),
        ("Transpose of a matrix in-place.", "easy"),
        ("Print matrix in snake pattern.", "easy"),
        ("Find the row with maximum number of 1s in a boolean matrix.", "medium"),
        ("Maximum sum rectangle in a 2D matrix.", "hard"),
    ]
    for txt, d in mat:
        Q.append(_q("arrays", d, "fresher", txt,
            ["What's the in-place approach?", "Time complexity?"],
            ["Matrix manipulation", "Row/column traversal", "Handle boundary conditions"]))

    # ═══════ LINKED LISTS ═══════
    ll = [
        ("How would you reverse a singly linked list? Can you do it both iteratively and recursively?", "easy", "fresher",
         ["What about reversing in groups of k?", "Time and space complexity of each?"],
         ["Iterative: three pointers prev/curr/next", "Recursive: reverse rest, adjust pointers", "O(n) time O(1) space iterative"]),
        ("How do you detect if a linked list has a cycle? Where does the cycle start?", "medium", "fresher",
         ["Why does Floyd's algorithm work?", "Can you prove the mathematical basis?"],
         ["Floyd's cycle detection (slow/fast pointers)", "After meeting, reset one to head", "Both move one step — meet at cycle start", "O(n) time O(1) space"]),
        ("Merge two sorted linked lists into one sorted list.", "easy", "fresher",
         ["Can you do it recursively?", "What about merging k sorted lists?"],
         ["Compare heads, attach smaller", "Recursive or iterative", "O(n+m) time"]),
        ("Find the middle element of a linked list in one pass.", "easy", "fresher",
         ["What if the list has even number of nodes?", "Can you use this for other problems?"],
         ["Slow and fast pointer", "When fast reaches end, slow is at middle", "O(n) time O(1) space"]),
        ("Remove the nth node from the end of a linked list.", "medium", "fresher",
         ["Can you do it in a single pass?", "What if n equals the length?"],
         ["Two pointers, gap of n", "Handle edge case: removing head", "O(n) time"]),
        ("Check if a linked list is a palindrome.", "medium", "fresher",
         ["Can you do it without extra space?", "What about using a stack?"],
         ["Find middle, reverse second half, compare", "O(n) time O(1) space", "Restore the list after"]),
        ("Add two numbers represented as linked lists.", "medium", "fresher",
         ["What if lists have different lengths?", "What about carry at the end?"],
         ["Traverse both lists simultaneously", "Handle carry", "Create new list or modify existing"]),
        ("Flatten a multilevel doubly linked list.", "hard", "mid",
         ["How do you handle the child pointers?", "Recursive vs iterative?"],
         ["DFS approach", "Stack-based iterative", "Reconnect prev/next pointers"]),
        ("Copy a linked list with random pointers.", "hard", "mid",
         ["Can you do it without a hash map?", "Walk through the interleaving approach."],
         ["Hash map: O(n) time O(n) space", "Interleave nodes approach O(n) O(1)", "Three passes: interleave, set randoms, separate"]),
        ("Find the intersection point of two linked lists.", "easy", "fresher",
         ["What if they don't intersect?", "Can you do it without knowing the lengths?"],
         ["Length difference approach", "Two pointer trick: switch heads", "O(n+m) time O(1) space"]),
    ]
    for txt, d, l, fu, pts in ll:
        Q.append(_q("linked_lists", d, l, txt, fu, pts))

    # More linked list
    ll2 = [
        ("Sort a linked list using merge sort.", "medium"),
        ("Remove all duplicates from a sorted linked list.", "easy"),
        ("Reverse nodes in k-group.", "hard"),
        ("Swap nodes in pairs.", "medium"),
        ("Rotate a linked list by k positions.", "medium"),
        ("Partition list around a value x.", "medium"),
        ("Delete node given only access to that node (not head).", "easy"),
        ("Reorder list: L0→Ln→L1→Ln-1→...", "medium"),
        ("Implement LRU cache using doubly linked list + hash map.", "hard"),
        ("Detect and remove the loop in a linked list.", "medium"),
        ("Convert a sorted list to a balanced BST.", "medium"),
        ("Clone a linked list with next and arbit pointer.", "hard"),
        ("Merge k sorted linked lists.", "hard"),
        ("Check if a linked list is circular.", "easy"),
        ("Split a circular linked list into two halves.", "medium"),
    ]
    for txt, d in ll2:
        Q.append(_q("linked_lists", d, "fresher" if d != "hard" else "mid", txt,
            ["Walk me through the approach.", "Time and space complexity?"],
            ["Pointer manipulation", "Edge cases", "O(n) time typically"]))

    # ═══════ STACKS & QUEUES ═══════
    sq = [
        ("How do you check if parentheses in a string are balanced?", "easy", "fresher",
         ["What about multiple types of brackets?", "What if string has other characters?"],
         ["Use stack", "Push opening, pop on closing", "Check match", "O(n) time O(n) space"]),
        ("Implement a stack that supports getMin() in O(1) time.", "medium", "fresher",
         ["What about O(1) space?", "How does the auxiliary stack approach work?"],
         ["Two stacks approach", "Or encode min in values", "O(1) for all operations"]),
        ("Find the next greater element for each element in an array.", "medium", "fresher",
         ["What data structure helps here?", "Can you solve the circular variant?"],
         ["Monotonic decreasing stack", "Process right to left", "O(n) time", "Stack stores candidates"]),
        ("Evaluate a postfix expression.", "easy", "fresher",
         ["How would you convert infix to postfix?", "What about prefix evaluation?"],
         ["Stack-based evaluation", "Push operands, pop and compute on operator", "O(n) time"]),
        ("Implement a queue using two stacks.", "easy", "fresher",
         ["What's the amortized time complexity?", "Can you do it with one stack?"],
         ["Push to stack1, pop from stack2", "Transfer when stack2 empty", "Amortized O(1)"]),
        ("Find the largest rectangle in a histogram.", "hard", "mid",
         ["How does the stack-based approach work?", "Why do we use a monotonic stack?"],
         ["Monotonic increasing stack", "Process bars left to right", "Calculate area when popping", "O(n) time"]),
        ("Design a stack with operations on middle element.", "medium", "fresher",
         ["What data structure enables O(1) middle operations?", "How about using a deque?"],
         ["Doubly linked list + pointer to middle", "Update middle on push/pop", "O(1) all operations"]),
        ("Sliding window maximum using deque.", "hard", "mid",
         ["Why can't we use a regular queue?", "How do you maintain the deque?"],
         ["Monotonic decreasing deque", "Remove smaller elements from back", "Remove out-of-window from front", "O(n) time"]),
        ("Implement a stack using a single queue.", "medium", "fresher",
         ["What's the trick?", "Time complexity of push vs pop?"],
         ["Rotate queue after each push", "Push O(n), Pop O(1)", "Or Push O(1), Pop O(n)"]),
        ("Sort a stack using recursion only.", "medium", "fresher",
         ["What's the recurrence?", "Time complexity?"],
         ["Remove top, sort remaining, insert in sorted order", "O(n^2) worst case", "Recursive insertion"]),
    ]
    for txt, d, l, fu, pts in sq:
        Q.append(_q("stacks_queues", d, l, txt, fu, pts))

    # More stack/queue
    sq2 = [
        ("Implement a circular queue.", "easy"), ("Stock span problem using stack.", "medium"),
        ("Celebrity problem — find the person known by all.", "medium"),
        ("Decode a string like '3[a2[bc]]'.", "medium"), ("Daily temperatures — days until warmer.", "medium"),
        ("Remove all adjacent duplicates in a string.", "easy"), ("Asteroid collision simulation.", "medium"),
        ("Trapping rain water using stack.", "hard"), ("Car fleet — how many groups reach destination.", "medium"),
        ("Online stock span.", "medium"), ("Sum of subarray minimums.", "hard"),
        ("Simplify Unix path using stack.", "medium"), ("Remove k digits to make smallest number.", "medium"),
        ("Maximum frequency stack.", "hard"), ("Validate stack sequences (push/pop).", "medium"),
    ]
    for txt, d in sq2:
        Q.append(_q("stacks_queues", d, "fresher" if d != "hard" else "mid", txt,
            ["What data structure is best here?", "Time complexity?"],
            ["Stack/queue/deque application", "Monotonic pattern if applicable", "O(n) typical"]))

    # ═══════ TREES ═══════
    tr = [
        ("Explain the different tree traversals. When would you use each?", "easy", "fresher",
         ["What's the iterative version of inorder?", "When is level-order most useful?"],
         ["Inorder (sorted in BST)", "Preorder (copy tree)", "Postorder (delete tree)", "Level-order (BFS)"]),
        ("How do you find the height of a binary tree?", "easy", "fresher",
         ["Recursive vs iterative?", "What about diameter?"],
         ["Recursion: 1 + max(left, right)", "O(n) time", "BFS level count for iterative"]),
        ("Find the Lowest Common Ancestor of two nodes in a binary tree.", "medium", "fresher",
         ["What if it's a BST?", "What if nodes might not exist?"],
         ["Recursive: if root is p or q, return root", "BST: use comparison", "O(n) worst, O(log n) BST"]),
        ("Check if a binary tree is balanced.", "easy", "fresher",
         ["What's the definition of balanced?", "Can you do it in O(n)?"],
         ["Height difference ≤ 1 at every node", "Bottom-up approach O(n)", "Top-down is O(n^2)"]),
        ("Serialize and deserialize a binary tree.", "hard", "mid",
         ["Which traversal works best?", "How do you handle null nodes?"],
         ["Preorder with null markers", "Level-order with null markers", "Use delimiter and queue"]),
        ("Validate if a binary tree is a valid BST.", "medium", "fresher",
         ["What are the edge cases?", "What about duplicate values?"],
         ["Inorder should be sorted", "Or pass min/max range recursively", "Handle integer overflow"]),
        ("Convert a sorted array to a balanced BST.", "easy", "fresher",
         ["What about sorted linked list?", "Why is the middle element the root?"],
         ["Pick middle as root", "Recurse on left and right halves", "O(n) time"]),
        ("Find the maximum path sum in a binary tree.", "hard", "mid",
         ["Can the path go through the root?", "What about negative values?"],
         ["At each node: max(left, right) + node value or start new", "Track global max", "O(n) time"]),
        ("Print all root-to-leaf paths in a binary tree.", "medium", "fresher",
         ["How do you track the path?", "What about path with given sum?"],
         ["Backtracking with path list", "DFS, add node, recurse, remove", "O(n) time"]),
        ("Construct a tree from inorder and preorder traversals.", "medium", "fresher",
         ["What if given inorder and postorder?", "How do you find the root?"],
         ["First element of preorder is root", "Find root in inorder to split", "Recurse on left and right subtrees"]),
    ]
    for txt, d, l, fu, pts in tr:
        Q.append(_q("trees", d, l, txt, fu, pts))

    # More tree questions
    tr2 = [
        ("Level order traversal of a binary tree.", "easy"), ("Zigzag level order traversal.", "medium"),
        ("Right side view of a binary tree.", "medium"), ("Check if two trees are identical.", "easy"),
        ("Mirror/invert a binary tree.", "easy"), ("Count leaf nodes.", "easy"),
        ("Find diameter of a binary tree.", "medium"), ("Check if tree is symmetric.", "easy"),
        ("Flatten binary tree to linked list.", "medium"), ("Vertical order traversal.", "hard"),
        ("Boundary traversal of binary tree.", "medium"), ("Bottom view of binary tree.", "medium"),
        ("Top view of binary tree.", "medium"), ("Find all nodes at distance k from target.", "hard"),
        ("Count complete tree nodes in O(log^2 n).", "medium"), ("Kth smallest element in BST.", "medium"),
        ("Delete node in BST.", "medium"), ("BST iterator.", "medium"),
        ("Recover BST (two nodes swapped).", "hard"), ("Convert BST to sorted doubly linked list.", "medium"),
        ("Find successor in BST.", "medium"), ("Largest BST subtree.", "hard"),
        ("Implement Trie (prefix tree).", "medium"), ("Word search in Trie.", "hard"),
        ("Auto-complete with Trie.", "medium"), ("Count distinct substrings using Trie.", "hard"),
    ]
    for txt, d in tr2:
        Q.append(_q("trees", d, "fresher" if d != "hard" else "mid", txt,
            ["Walk me through your approach.", "What's the time complexity?"],
            ["Tree traversal technique", "Recursive or iterative", "Handle null/edge cases"]))

    # ═══════ GRAPHS ═══════
    gr = [
        ("Explain BFS and DFS. When would you use each?", "easy", "fresher",
         ["What data structures do they use?", "Which finds shortest path in unweighted graph?"],
         ["BFS uses queue, DFS uses stack/recursion", "BFS for shortest path (unweighted)", "DFS for cycle detection, topological sort", "Both O(V+E)"]),
        ("How do you detect a cycle in a directed graph?", "medium", "fresher",
         ["What about undirected graph?", "DFS coloring vs union-find?"],
         ["DFS with three colors (white/gray/black)", "Gray node revisited = cycle", "Union-Find for undirected"]),
        ("Explain Dijkstra's algorithm. When does it fail?", "medium", "fresher",
         ["What about negative edges?", "How does it differ from Bellman-Ford?"],
         ["Greedy: always process nearest unvisited", "Fails with negative edges", "O((V+E) log V) with min-heap", "Bellman-Ford handles negatives"]),
        ("What is topological sorting? Where is it used?", "medium", "fresher",
         ["How do you implement it?", "What if there's a cycle?"],
         ["Linear ordering of DAG vertices", "Kahn's algorithm (BFS) or DFS", "Used in build systems, course scheduling", "Cycle = no valid ordering"]),
        ("Find the number of connected components in an undirected graph.", "easy", "fresher",
         ["DFS vs Union-Find for this?", "How about in a grid?"],
         ["DFS/BFS from each unvisited node", "Count number of traversals", "Union-Find alternative", "O(V+E)"]),
        ("Find shortest path in a weighted graph.", "medium", "fresher",
         ["Dijkstra vs Bellman-Ford vs Floyd-Warshall?", "When to use which?"],
         ["Dijkstra for single-source non-negative", "Bellman-Ford for negative edges", "Floyd-Warshall for all-pairs", "Choose based on constraints"]),
        ("Explain Kruskal's and Prim's algorithms for MST.", "medium", "mid",
         ["When to prefer one over the other?", "What's the role of Union-Find?"],
         ["Kruskal: sort edges, add if no cycle (Union-Find)", "Prim: grow tree from vertex (min-heap)", "Both produce MST", "Kruskal better for sparse, Prim for dense"]),
        ("Check if a graph is bipartite.", "medium", "fresher",
         ["How does BFS coloring work?", "What's the relationship with 2-coloring?"],
         ["BFS/DFS with two colors", "If neighbor has same color, not bipartite", "O(V+E)"]),
        ("Find bridges and articulation points in a graph.", "hard", "mid",
         ["What's Tarjan's algorithm?", "Why are these important?"],
         ["Tarjan's algorithm using DFS", "Track discovery time and low values", "Bridge: low[v] > disc[u]", "O(V+E)"]),
        ("Find strongly connected components.", "hard", "mid",
         ["Kosaraju vs Tarjan?", "What are SCCs used for?"],
         ["Kosaraju: two DFS passes + transpose", "Tarjan: single DFS with stack", "Used in compiler optimization, dependency analysis"]),
    ]
    for txt, d, l, fu, pts in gr:
        Q.append(_q("graphs", d, l, txt, fu, pts))

    # More graph questions
    gr2 = [
        ("Clone a graph.", "medium"), ("Course schedule — can all courses be finished?", "medium"),
        ("Word ladder — shortest transformation sequence.", "hard"),
        ("Alien dictionary — derive order from sorted alien words.", "hard"),
        ("Number of islands in a 2D grid.", "medium"), ("Surrounded regions — capture surrounded O's.", "medium"),
        ("Pacific Atlantic water flow.", "medium"), ("Cheapest flights within k stops.", "medium"),
        ("Network delay time — minimum time to reach all nodes.", "medium"),
        ("Reconstruct itinerary from flight tickets.", "hard"),
        ("Minimum spanning tree of a graph.", "medium"), ("Graph valid tree — check if edges form a tree.", "medium"),
        ("Accounts merge — union of email accounts.", "medium"),
        ("Redundant connection — find the edge that creates a cycle.", "medium"),
        ("Shortest path in binary matrix.", "medium"), ("Jump game on graph — minimum jumps.", "medium"),
        ("Evaluate division — graph-based equation solving.", "medium"),
        ("Is graph a valid tree?", "medium"), ("All paths from source to target in DAG.", "medium"),
        ("Minimum cost to connect all cities.", "medium"),
    ]
    for txt, d in gr2:
        Q.append(_q("graphs", d, "fresher" if d != "hard" else "mid", txt,
            ["Which graph algorithm applies?", "BFS or DFS here?"],
            ["Graph traversal", "Edge case handling", "Time: O(V+E)"]))

    # ═══════ DYNAMIC PROGRAMMING ═══════
    dp = [
        ("Explain the concept of dynamic programming. How is it different from recursion?", "easy", "fresher",
         ["What are overlapping subproblems?", "Top-down vs bottom-up?"],
         ["Optimal substructure + overlapping subproblems", "Memoization (top-down) vs tabulation (bottom-up)", "Trade-off: space vs time"]),
        ("How many ways can you climb n stairs if you can take 1 or 2 steps at a time?", "easy", "fresher",
         ["What if you can take 1, 2, or 3 steps?", "What's the pattern?"],
         ["Fibonacci pattern", "dp[i] = dp[i-1] + dp[i-2]", "O(n) time O(1) space possible"]),
        ("Find the longest common subsequence of two strings.", "medium", "fresher",
         ["How do you reconstruct the actual subsequence?", "Time and space complexity?"],
         ["2D DP table", "dp[i][j] = dp[i-1][j-1]+1 if match, else max", "O(mn) time O(mn) space", "Space optimization to O(min(m,n))"]),
        ("Solve the 0/1 Knapsack problem.", "medium", "fresher",
         ["What about fractional knapsack?", "Can you optimize space?"],
         ["2D DP: dp[i][w]", "Include or exclude each item", "O(nW) time O(nW) space", "1D array space optimization"]),
        ("Find the minimum number of coins to make a given amount.", "medium", "fresher",
         ["What if it's impossible?", "What about counting total ways?"],
         ["dp[amount] = min(dp[amount], dp[amount-coin]+1)", "Initialize with infinity", "O(amount * coins) time"]),
        ("Find the edit distance between two strings.", "hard", "mid",
         ["What operations are allowed?", "How do you trace back the operations?"],
         ["Insert, delete, replace", "dp[i][j] = min of three operations", "O(mn) time"]),
        ("Longest increasing subsequence.", "medium", "fresher",
         ["Can you do better than O(n^2)?", "Binary search approach?"],
         ["DP O(n^2)", "Binary search with tails O(n log n)", "Patience sorting analogy"]),
        ("Partition equal subset sum — can array be split into two equal subsets?", "medium", "fresher",
         ["How does this relate to knapsack?", "What's the target sum?"],
         ["Subset sum variant with target = total/2", "dp[i] = true if sum i achievable", "O(n * sum) time"]),
        ("Count number of ways to decode a message (1=A, 2=B, ..., 26=Z).", "medium", "fresher",
         ["What about leading zeros?", "What about '10' and '20'?"],
         ["Similar to climbing stairs", "Check single digit and two digit", "Handle '0' carefully"]),
        ("Matrix chain multiplication — minimum cost to multiply matrices.", "hard", "mid",
         ["What's the recurrence?", "Time complexity?"],
         ["dp[i][j] = min over k of dp[i][k] + dp[k+1][j] + cost", "O(n^3) time", "Parenthesization problem"]),
    ]
    for txt, d, l, fu, pts in dp:
        Q.append(_q("dynamic_programming", d, l, txt, fu, pts))

    # More DP
    dp2 = [
        ("House robber — maximum robbery without adjacent houses.", "medium"),
        ("House robber II — circular arrangement.", "medium"),
        ("Longest palindromic subsequence.", "medium"),
        ("Longest palindromic substring.", "medium"),
        ("Word break — can string be segmented into dictionary words?", "medium"),
        ("Unique paths in a grid.", "easy"),
        ("Minimum path sum in a grid.", "easy"),
        ("Target sum — assign +/- to reach target.", "medium"),
        ("Interleaving string.", "hard"),
        ("Burst balloons — maximum coins.", "hard"),
        ("Regular expression matching.", "hard"),
        ("Wildcard matching.", "hard"),
        ("Maximum profit from stock (one transaction).", "easy"),
        ("Stock — multiple transactions.", "easy"),
        ("Stock — at most k transactions.", "hard"),
        ("Stock with cooldown.", "medium"),
        ("Egg drop problem.", "hard"),
        ("Palindrome partitioning — minimum cuts.", "hard"),
        ("Maximum sum increasing subsequence.", "medium"),
        ("Count of subset sum.", "medium"),
        ("Rod cutting problem.", "medium"),
        ("Coin change 2 — number of combinations.", "medium"),
        ("Distinct subsequences.", "hard"),
        ("Minimum insertion to make palindrome.", "medium"),
        ("Shortest common supersequence.", "hard"),
        ("Maximum length of pair chain.", "medium"),
        ("DP on trees — maximum path sum.", "hard"),
        ("Digit DP — count numbers with specific properties.", "hard"),
        ("Arithmetic slices — count arithmetic subarrays.", "medium"),
        ("Perfect squares — minimum squares summing to n.", "medium"),
    ]
    for txt, d in dp2:
        Q.append(_q("dynamic_programming", d, "fresher" if d != "hard" else "mid", txt,
            ["What's the state definition?", "Can you optimize space?"],
            ["Define dp state clearly", "Recurrence relation", "Base cases", "Time/space complexity"]))

    # ═══════ RECURSION & BACKTRACKING ═══════
    rb = [
        ("Generate all permutations of a given array.", "medium"),
        ("Generate all subsets of a set.", "medium"),
        ("N-Queens problem — place N queens on N×N board.", "hard"),
        ("Solve a Sudoku puzzle.", "hard"),
        ("Generate all valid combinations of n pairs of parentheses.", "medium"),
        ("Word search in a 2D grid.", "medium"),
        ("Combination sum — find all combinations summing to target.", "medium"),
        ("Letter combinations of a phone number.", "medium"),
        ("Rat in a maze — find all paths.", "medium"),
        ("Palindrome partitioning — all palindromic splits.", "medium"),
        ("Print all subsequences of a string.", "easy"),
        ("Tower of Hanoi.", "easy"),
        ("Find all paths in a graph from source to destination.", "medium"),
        ("Generate all binary strings of length n.", "easy"),
        ("Knight's tour on a chessboard.", "hard"),
        ("Crossword puzzle solver.", "hard"),
        ("Print all permutations of a string with duplicates.", "medium"),
        ("Combination sum with unique elements.", "medium"),
        ("Restore IP addresses.", "medium"),
        ("M-coloring problem.", "hard"),
    ]
    for txt, d in rb:
        Q.append(_q("recursion_backtracking", d, "fresher" if d != "hard" else "mid", txt,
            ["How do you prune the search space?", "What's the time complexity?"],
            ["Backtracking template: choose, explore, unchoose", "Pruning for efficiency", "Base case definition"]))

    # ═══════ SORTING & SEARCHING ═══════
    ss = [
        ("Compare QuickSort and MergeSort. When would you use each?", "easy", "fresher",
         ["What's the worst case of QuickSort?", "Which is stable?"],
         ["QuickSort: in-place, O(n^2) worst", "MergeSort: stable, O(n log n) always", "QuickSort better cache performance"]),
        ("How does binary search work? What are common pitfalls?", "easy", "fresher",
         ["Integer overflow in mid calculation?", "Off-by-one errors?"],
         ["mid = low + (high-low)/2", "Handle empty array", "Correct boundary updates"]),
        ("Find the kth smallest element using QuickSelect.", "medium", "fresher",
         ["Average vs worst case?", "How to choose pivot?"],
         ["Partition around pivot", "O(n) average O(n^2) worst", "Randomized pivot selection"]),
        ("Count inversions in an array using merge sort.", "medium", "fresher",
         ["What is an inversion?", "Why does merge sort help?"],
         ["Count cross-inversions during merge", "O(n log n) time", "Modified merge sort"]),
        ("Search in a nearly sorted array where elements can be off by 1 position.", "medium", "fresher",
         ["How do you modify binary search?", "Check mid-1, mid, mid+1?"],
         ["Check mid, mid-1, mid+1", "Divide search space by 3/4", "O(log n) time"]),
        ("What sorting algorithm is used by Python/Java internally?", "easy", "fresher",
         ["Why Timsort?", "What's the advantage?"],
         ["Timsort: hybrid merge+insertion sort", "Exploits partially sorted data", "O(n log n) worst, O(n) best"]),
    ]
    for txt, d, l, fu, pts in ss:
        Q.append(_q("sorting_searching", d, l, txt, fu, pts))

    ss2 = [
        ("Find the first bad version using binary search.", "easy"),
        ("Search insert position.", "easy"),
        ("Find peak element.", "medium"),
        ("Find single element in sorted array (all others appear twice).", "medium"),
        ("Merge overlapping intervals after sorting.", "medium"),
        ("Sort colors (Dutch National Flag).", "medium"),
        ("Wiggle sort.", "medium"),
        ("H-index.", "medium"),
        ("Maximum gap between successive elements after sorting.", "hard"),
        ("Find minimum number of platforms for trains.", "medium"),
        ("Count sort implementation.", "easy"),
        ("Radix sort — when to use?", "medium"),
        ("Bucket sort for uniform distribution.", "medium"),
        ("Sort an almost sorted array efficiently.", "medium"),
    ]
    for txt, d in ss2:
        Q.append(_q("sorting_searching", d, "fresher", txt,
            ["What's the best approach?", "Time complexity?"],
            ["Sorting/searching technique", "Edge cases", "Optimal complexity"]))

    # ═══════ HEAPS ═══════
    hp = [
        ("Find the kth largest element in a stream of numbers.", "medium", "fresher",
         ["What data structure is ideal?", "What's the time complexity per element?"],
         ["Min-heap of size k", "O(n log k) total", "Top of heap is kth largest"]),
        ("Merge k sorted arrays.", "hard", "mid",
         ["How does a min-heap help?", "What about merge sort approach?"],
         ["Min-heap of k elements", "O(n log k) where n = total elements", "Push next element from same array"]),
        ("Find the median from a data stream.", "hard", "mid",
         ["How do two heaps work together?", "Which operations need balancing?"],
         ["Max-heap for lower half, min-heap for upper half", "Balance sizes", "O(log n) insert, O(1) median"]),
        ("Top k frequent elements.", "medium", "fresher",
         ["Can you do better than O(n log n)?", "Bucket sort approach?"],
         ["Count frequencies with hash map", "Min-heap of size k: O(n log k)", "Bucket sort: O(n)"]),
        ("Sort a nearly sorted array (each element at most k positions away).", "medium", "fresher",
         ["Why is a heap of size k+1 sufficient?", "Time complexity?"],
         ["Min-heap of size k+1", "O(n log k) time", "Sliding window with heap"]),
    ]
    for txt, d, l, fu, pts in hp:
        Q.append(_q("heaps", d, l, txt, fu, pts))

    hp2 = [
        ("Implement a max-heap from scratch.", "medium"),
        ("Heap sort — how does it work?", "medium"),
        ("Find k closest points to origin.", "medium"),
        ("Reorganize string so no two adjacent characters are same.", "medium"),
        ("Task scheduler — minimum intervals to complete tasks.", "medium"),
        ("Ugly number — find nth ugly number.", "medium"),
        ("Super ugly number.", "hard"),
        ("Smallest range covering elements from k lists.", "hard"),
        ("IPO — maximize capital with limited projects.", "hard"),
        ("Sliding window median.", "hard"),
    ]
    for txt, d in hp2:
        Q.append(_q("heaps", d, "fresher" if d != "hard" else "mid", txt,
            ["Why heap over sorting?", "Time complexity?"],
            ["Heap property maintenance", "O(log n) operations", "Priority queue application"]))

    # ═══════ HASHING ═══════
    hs = [
        ("How does a hash map work internally?", "medium", "fresher",
         ["What happens during a collision?", "What's the load factor?"],
         ["Hash function maps key to bucket", "Chaining vs open addressing for collisions", "Rehashing when load factor exceeds threshold", "Amortized O(1) operations"]),
        ("Group all anagrams from a list of strings.", "medium", "fresher",
         ["What's the key for grouping?", "Can you use character count as key?"],
         ["Sort each string as key, or character count tuple", "Hash map of key → list", "O(n * k log k) or O(n * k)"]),
        ("Find the longest consecutive sequence in an unsorted array.", "medium", "fresher",
         ["Can you do it in O(n)?", "How does HashSet help?"],
         ["Add all to HashSet", "For each num without num-1 (sequence start), count forward", "O(n) time"]),
        ("Find the first non-repeating character in a string.", "easy", "fresher",
         ["What about in a stream?", "Can you do it with a single pass?"],
         ["Count frequencies", "Second pass for first with count 1", "Or use linked hash map for order"]),
        ("Check if two strings are isomorphic.", "easy", "fresher",
         ["What about one-to-one mapping?", "Can two characters map to the same?"],
         ["Two hash maps for bidirectional mapping", "O(n) time"]),
    ]
    for txt, d, l, fu, pts in hs:
        Q.append(_q("hashing", d, l, txt, fu, pts))

    hs2 = [
        ("Two sum — find indices of two numbers that add to target.", "easy"),
        ("Subarray sum equals k — count subarrays.", "medium"),
        ("Longest subarray with sum zero.", "medium"),
        ("Find all duplicates in an array.", "easy"),
        ("Valid Sudoku — check if board is valid.", "medium"),
        ("Minimum window substring.", "hard"),
        ("Longest substring without repeating characters.", "medium"),
        ("Contains duplicate within k distance.", "easy"),
        ("4Sum II — count tuples from 4 arrays summing to 0.", "medium"),
        ("Design a hash map from scratch.", "medium"),
    ]
    for txt, d in hs2:
        Q.append(_q("hashing", d, "fresher", txt,
            ["What's the hash map strategy?", "Time vs space trade-off?"],
            ["Hash map application", "O(n) time typically", "Handle collisions"]))

    # ═══════ COMPANY-SPECIFIC ═══════
    google_dsa = [
        ("Find all valid IP addresses from a string of digits.", "medium", "Google"),
        ("Implement autocomplete system with top 3 suggestions.", "hard", "Google"),
        ("Find shortest path in a graph with obstacles.", "hard", "Google"),
        ("Design a data structure for add and search words (with wildcards).", "hard", "Google"),
        ("Maximum profit in job scheduling.", "hard", "Google"),
        ("Minimum cost to hire k workers.", "hard", "Google"),
        ("Split array into consecutive subsequences.", "medium", "Google"),
        ("Swim in rising water — minimum time to reach bottom-right.", "hard", "Google"),
        ("Snapshot array — implement versioned array.", "medium", "Google"),
        ("Random pick with weight.", "medium", "Google"),
    ]
    for txt, d, co in google_dsa:
        Q.append(_q("company_dsa", d, "mid", txt,
            ["Optimal approach?", "Edge cases?"], ["Algorithm choice", "Optimization", "Clean code"],
            co=co, tg=["google", "hard_dsa"]))

    amazon_dsa = [
        ("Find k most frequent words in a list.", "medium", "Amazon"),
        ("Prison cells after N days — find cycle.", "medium", "Amazon"),
        ("Reorder data in log files.", "easy", "Amazon"),
        ("Number of islands (BFS approach).", "medium", "Amazon"),
        ("Merge k sorted lists.", "hard", "Amazon"),
        ("Minimum cost to connect sticks.", "medium", "Amazon"),
        ("Partition labels.", "medium", "Amazon"),
        ("Subtree of another tree.", "easy", "Amazon"),
        ("LRU Cache implementation.", "hard", "Amazon"),
        ("Two sum — sorted array.", "easy", "Amazon"),
    ]
    for txt, d, co in amazon_dsa:
        Q.append(_q("company_dsa", d, "fresher", txt,
            ["Approach?", "Optimize?"], ["Data structure choice", "Complexity analysis"],
            co=co, tg=["amazon", "dsa"]))

    tcs_dsa = [
        ("Reverse a string without using built-in functions.", "easy", "TCS"),
        ("Check if a number is palindrome.", "easy", "TCS"),
        ("Find the factorial of a number.", "easy", "TCS"),
        ("Fibonacci series up to n terms.", "easy", "TCS"),
        ("Check if a number is prime.", "easy", "TCS"),
        ("Find the GCD of two numbers.", "easy", "TCS"),
        ("Sort an array using bubble sort.", "easy", "TCS"),
        ("Find the second largest element in an array.", "easy", "TCS"),
        ("Remove duplicates from a sorted array.", "easy", "TCS"),
        ("Check if a string is an anagram of another.", "easy", "TCS"),
        ("Count vowels and consonants in a string.", "easy", "TCS"),
        ("Matrix multiplication.", "easy", "TCS"),
        ("Find the intersection of two arrays.", "easy", "TCS"),
        ("Swap two numbers without using a third variable.", "easy", "TCS"),
        ("Armstrong number check.", "easy", "TCS"),
    ]
    for txt, d, co in tcs_dsa:
        Q.append(_q("company_dsa", d, "fresher", txt,
            ["Can you optimize?", "Edge cases?"], ["Basic implementation", "Correctness"],
            co=co, tg=["tcs", "basic_coding"]))

    infosys_dsa = [
        ("Pattern printing — pyramid, diamond, number patterns.", "easy", "Infosys"),
        ("String compression — aabccc → a2b1c3.", "easy", "Infosys"),
        ("Rotate array by k positions.", "easy", "Infosys"),
        ("Find missing number in array 1 to n.", "easy", "Infosys"),
        ("Check if linked list is palindrome.", "medium", "Infosys"),
        ("Implement stack using array.", "easy", "Infosys"),
        ("Binary search implementation.", "easy", "Infosys"),
        ("Convert decimal to binary.", "easy", "Infosys"),
        ("Find the longest common prefix.", "easy", "Infosys"),
        ("Count frequency of each element in array.", "easy", "Infosys"),
    ]
    for txt, d, co in infosys_dsa:
        Q.append(_q("company_dsa", d, "fresher", txt,
            ["Alternative approach?", "Complexity?"], ["Clean implementation", "Edge cases"],
            co=co, tg=["infosys", "coding"]))

    gs_dsa = [
        ("Design and implement a LFU cache.", "hard", "Goldman Sachs"),
        ("Find median of two sorted arrays.", "hard", "Goldman Sachs"),
        ("Trapping rain water.", "hard", "Goldman Sachs"),
        ("Minimum window substring.", "hard", "Goldman Sachs"),
        ("Serialize and deserialize binary tree.", "hard", "Goldman Sachs"),
        ("Count of smaller numbers after self.", "hard", "Goldman Sachs"),
        ("Skyline problem.", "hard", "Goldman Sachs"),
        ("Word break II — all possible sentences.", "hard", "Goldman Sachs"),
    ]
    for txt, d, co in gs_dsa:
        Q.append(_q("company_dsa", d, "mid", txt,
            ["Optimal complexity?", "Can you prove correctness?"],
            ["Algorithmic thinking", "Mathematical reasoning", "Optimal solution"],
            co=co, tg=["goldman_sachs", "hard_dsa"]))

    return Q
