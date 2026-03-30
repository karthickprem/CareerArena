"""OS & Computer Networks interview questions for PlaceRight. ~500 questions via template expansion."""
from typing import List, Dict

R_OS = {"1-3": "No grasp of OS fundamentals. Cannot explain basic concepts.",
        "4-5": "Bookish knowledge only. Cannot apply to scenarios.",
        "6-7": "Good understanding with examples. Minor gaps.",
        "8-10": "Deep understanding. Real-world scenarios. Discusses trade-offs."}

R_CN = {"1-3": "Cannot explain basic networking concepts.",
        "4-5": "Knows definitions but confused about protocols and layers.",
        "6-7": "Solid understanding of protocols. Can troubleshoot basic issues.",
        "8-10": "Expert knowledge. Designs network architectures. Deep protocol understanding."}

def _q(t, d, l, txt, fu, pts, rubric=None, co="", tg=None):
    return {"domain": "software_engineering", "topic": t, "difficulty": d, "level": l,
            "question_text": txt, "follow_ups": fu, "expected_points": pts,
            "scoring_rubric": rubric or R_OS, "company_specific": co, "tags": tg or [t]}

def get_os_networks_questions() -> List[Dict]:
    Q = []

    # ═══════ PROCESS MANAGEMENT ═══════
    proc = [
        ("What is the difference between a process and a thread? When would you use threads over processes?", "easy", "fresher",
         ["Can threads share memory?", "What happens if one thread crashes?", "What's a green thread?"],
         ["Process: independent, separate memory space", "Thread: lightweight, shared memory", "Thread crash can kill process", "Threads for I/O bound, processes for isolation"]),
        ("Walk me through what happens when you run a program from the command line. What does the OS do?", "medium", "fresher",
         ["Where does the process control block come from?", "What about shared libraries?"],
         ["Shell forks a child process", "exec() loads the binary into memory", "Loader resolves dynamic libraries", "PCB created, scheduled for execution"]),
        ("What is a context switch? Why is it expensive?", "medium", "fresher",
         ["How expensive in real numbers?", "What's saved/restored?", "How does it compare process vs thread?"],
         ["Save current process state (registers, PC, stack)", "Load next process state from PCB", "TLB flush for process switch", "Thread context switch cheaper — shared address space"]),
        ("What are the different states of a process? Draw the state transition diagram.", "easy", "fresher",
         ["What triggers each transition?", "Can a process go from waiting to running directly?"],
         ["New → Ready → Running → Waiting → Terminated", "Ready → Running: scheduler dispatch", "Running → Waiting: I/O or event wait", "No direct Waiting → Running transition"]),
        ("Explain Inter-Process Communication. What are the different IPC mechanisms?", "medium", "fresher",
         ["When would you use shared memory vs message passing?", "What about pipes vs sockets?"],
         ["Shared memory: fastest, needs synchronization", "Message passing: easier, slower", "Pipes: parent-child, named pipes for unrelated", "Sockets: network or local IPC"]),
        ("What is a zombie process? How is it different from an orphan process?", "medium", "fresher",
         ["How do you clean up zombies?", "What's the init process role?"],
         ["Zombie: terminated but parent hasn't called wait()", "Orphan: parent terminated, adopted by init", "Zombie uses PID entry — can exhaust PIDs", "Fix: parent calls wait() or waitpid()"]),
        ("What are system calls? Give me examples from file I/O and process management.", "easy", "fresher",
         ["User mode vs kernel mode?", "What triggers a mode switch?"],
         ["Interface between user program and kernel", "Process: fork(), exec(), wait(), exit()", "File: open(), read(), write(), close()", "Mode switch via software interrupt"]),
        ("Explain fork() in Unix. What does it return and why?", "medium", "fresher",
         ["What happens to open files after fork?", "What is copy-on-write?"],
         ["Creates child process — exact copy of parent", "Returns 0 to child, child PID to parent, -1 on error", "Copy-on-write: pages shared until modified", "Child inherits file descriptors"]),
        ("What is a process control block (PCB)? What information does it contain?", "easy", "fresher",
         ["Where is it stored?", "Who manages it?"],
         ["Process state, PID, program counter", "CPU registers, memory management info", "I/O status, scheduling info", "Stored in kernel memory"]),
        ("What is the difference between preemptive and non-preemptive scheduling?", "easy", "fresher",
         ["Which is used in modern OS?", "What about real-time systems?"],
         ["Preemptive: OS can interrupt running process", "Non-preemptive: process runs until it yields", "Modern OS: preemptive (Linux, Windows)", "Non-preemptive: simpler, no race conditions"]),
    ]
    for txt, d, l, fu, pts in proc:
        Q.append(_q("process_management", d, l, txt, fu, pts))

    # ═══════ CPU SCHEDULING ═══════
    sched = [
        ("Compare FCFS, SJF, and Round Robin scheduling. Which is best for interactive systems?", "medium", "fresher",
         ["What about starvation?", "How do you know burst time in advance for SJF?"],
         ["FCFS: simple but convoy effect", "SJF: optimal avg wait time but starvation possible", "RR: fair, good response time for interactive", "SJF burst time prediction via exponential averaging"]),
        ("Three processes arrive at time 0 with burst times 24, 3, 3. Calculate average waiting time for FCFS and SJF.", "easy", "fresher",
         ["What if they arrive at different times?", "Which gives better average?"],
         ["FCFS order: P1(0), P2(24), P3(27) → avg wait = 17", "SJF order: P2(0), P3(3), P1(6) → avg wait = 3", "SJF dramatically better here", "But SJF has starvation problem"]),
        ("What is the time quantum in Round Robin? What happens if it's too small or too large?", "medium", "fresher",
         ["Typical values?", "How does it affect response time vs throughput?"],
         ["Too small: excessive context switches", "Too large: degrades to FCFS", "Typical: 10-100 ms", "Trade-off: response time vs overhead"]),
        ("Explain the Multilevel Feedback Queue scheduling algorithm. Why is it considered the most sophisticated?", "hard", "mid",
         ["How do processes move between queues?", "What parameters need tuning?"],
         ["Multiple queues with different priorities", "New processes start in highest priority queue", "CPU-bound processes sink to lower queues", "I/O-bound processes stay in higher queues"]),
        ("What is priority scheduling? How do you prevent starvation?", "medium", "fresher",
         ["Aging technique?", "Priority inversion problem?"],
         ["Higher priority processes run first", "Starvation: low priority waits indefinitely", "Aging: gradually increase priority of waiting processes", "Priority inversion: Mars Pathfinder bug"]),
        ("Given 5 processes with arrival and burst times, calculate turnaround and waiting time for SJF (non-preemptive). P1(0,6), P2(1,4), P3(2,2), P4(3,5), P5(4,3).", "medium", "fresher",
         ["What about preemptive SJF (SRTF)?", "Draw the Gantt chart."],
         ["Gantt: P1(0-6), P3(6-8), P5(8-11), P2(11-15), P4(15-20)", "Avg turnaround time calculation", "Avg waiting time calculation", "SRTF would preempt P1 when P3 arrives"]),
        ("What is the convoy effect in FCFS scheduling?", "easy", "fresher",
         ["How does it affect I/O-bound processes?", "Solution?"],
         ["One long CPU-bound process blocks shorter ones", "Short I/O-bound processes wait behind long CPU-bound", "Poor CPU and device utilization", "Solution: preemptive scheduling"]),
        ("Compare preemptive and non-preemptive SJF. Calculate average waiting time for: P1(0,7), P2(2,4), P3(4,1), P4(5,4).", "hard", "fresher",
         ["Which gives better average?", "What's the downside of preemptive?"],
         ["Non-preemptive: P1 runs fully first", "Preemptive (SRTF): P1 preempted when shorter arrives", "SRTF gives better average waiting time", "SRTF has more context switches"]),
    ]
    for txt, d, l, fu, pts in sched:
        Q.append(_q("cpu_scheduling", d, l, txt, fu, pts))

    # ═══════ MEMORY MANAGEMENT ═══════
    mem = [
        ("What is virtual memory? How does it let you run programs larger than physical RAM?", "medium", "fresher",
         ["What's the page table?", "What about thrashing?", "TLB?"],
         ["Address space abstraction — larger than physical memory", "Demand paging: load pages only when needed", "Page table maps virtual → physical addresses", "Swap space on disk for pages not in RAM"]),
        ("Explain paging. How does the OS translate a virtual address to a physical address?", "medium", "fresher",
         ["What is a page fault?", "What's the TLB?", "Multi-level page tables?"],
         ["Virtual address = page number + offset", "Page table lookup: page number → frame number", "Physical address = frame number + offset", "TLB caches recent page table entries"]),
        ("What is segmentation? How is it different from paging?", "medium", "fresher",
         ["External fragmentation?", "Segmentation fault?"],
         ["Segmentation: logical units (code, data, stack)", "Paging: fixed-size pages", "Segmentation: variable-size, external fragmentation", "Paging: fixed-size, internal fragmentation"]),
        ("Compare the page replacement algorithms: FIFO, LRU, and Optimal. Given the reference string 7,0,1,2,0,3,0,4,2,3,0,3,2 with 3 frames, how many page faults for each?", "hard", "fresher",
         ["Belady's anomaly?", "How is LRU implemented in practice?"],
         ["FIFO: replace oldest page, suffers Belady's anomaly", "LRU: replace least recently used, good but expensive", "Optimal: replace page used farthest in future (theoretical)", "Count page faults for each algorithm"]),
        ("What is thrashing? How does the OS detect and prevent it?", "hard", "mid",
         ["Working set model?", "How does it affect system performance?"],
         ["CPU spends more time swapping than executing", "Cause: too many processes, insufficient frames", "Detection: high page fault rate, low CPU utilization", "Prevention: working set model, limit multiprogramming"]),
        ("What is internal fragmentation vs external fragmentation?", "easy", "fresher",
         ["Which is worse?", "How does compaction help?"],
         ["Internal: wasted space within allocated block", "External: free space scattered in small chunks", "Paging: internal fragmentation (last page)", "Segmentation: external fragmentation"]),
        ("Explain the difference between logical and physical address space.", "easy", "fresher",
         ["Who generates logical addresses?", "When does mapping happen?"],
         ["Logical: generated by CPU, program's view", "Physical: actual RAM location", "MMU translates at runtime", "Same logical address can map to different physical"]),
        ("What is a page fault? Walk me through what happens when one occurs.", "medium", "fresher",
         ["How expensive is a page fault?", "Major vs minor page fault?"],
         ["Trap to OS", "Check if valid reference, find free frame", "Read page from disk to frame", "Update page table, restart instruction"]),
        ("What is the working set of a process? How does it relate to thrashing?", "hard", "mid",
         ["How is working set size determined?", "What's the window size?"],
         ["Set of pages referenced in recent time window", "If working set > available frames → thrashing", "Working set model: allocate frames for working set", "Window too small: insufficient pages, too large: wasteful"]),
        ("What is demand paging? How does it differ from pre-paging?", "medium", "fresher",
         ["Lazy loading?", "When is pre-paging beneficial?"],
         ["Demand: load page only on access (page fault)", "Pre-paging: load pages in advance", "Demand: less I/O initially, page faults later", "Pre-paging: fewer faults but may load unneeded pages"]),
    ]
    for txt, d, l, fu, pts in mem:
        Q.append(_q("memory_management", d, l, txt, fu, pts))

    # ═══════ DEADLOCKS ═══════
    dead = [
        ("What are the four necessary conditions for a deadlock? Can you have a deadlock if any one is missing?", "medium", "fresher",
         ["Which condition is easiest to break?", "Can you have a deadlock with only 2 processes?"],
         ["Mutual exclusion, Hold and wait, No preemption, Circular wait", "All four must hold simultaneously", "Remove any one to prevent deadlock", "Circular wait is most practical to prevent"]),
        ("Explain the Banker's Algorithm with an example. Given 5 processes and 3 resource types, determine if the system is in a safe state.", "hard", "fresher",
         ["What's the time complexity?", "What happens if the state is unsafe?"],
         ["Available, Max, Allocation, Need matrices", "Find safe sequence: process that can finish with available", "Release resources, check next process", "If sequence found → safe state"]),
        ("What is the difference between deadlock prevention, avoidance, and detection?", "medium", "fresher",
         ["Which is used in real OS?", "Which is most practical?"],
         ["Prevention: eliminate one of four conditions", "Avoidance: check before granting (Banker's)", "Detection: allow deadlock, detect and recover", "Real OS: mostly detection + recovery"]),
        ("Two processes need resources A and B. P1 holds A and requests B. P2 holds B and requests A. How do you resolve this?", "easy", "fresher",
         ["How would ordering resources prevent this?", "What about timeout?"],
         ["Classic circular wait deadlock", "Solution: impose ordering (always request A before B)", "Timeout: release resources if waiting too long", "Kill one process and restart"]),
        ("What is a livelock? How is it different from a deadlock?", "medium", "mid",
         ["Real-world analogy?", "How do you detect livelock?"],
         ["Livelock: processes keep changing state without progress", "Both processes respond to each other's actions", "Analogy: two people in a corridor, both step aside same way", "Harder to detect than deadlock"]),
        ("What is resource allocation graph? How do you detect deadlock using it?", "medium", "fresher",
         ["Single instance vs multiple instances?", "Cycle detection?"],
         ["Nodes: processes and resources", "Edges: request (process→resource) and assignment (resource→process)", "Single instance: cycle = deadlock", "Multiple instances: cycle necessary but not sufficient"]),
        ("How does the OS recover from a deadlock?", "medium", "fresher",
         ["Process termination?", "Resource preemption?"],
         ["Kill one or more processes", "Preempt resources from some processes", "Rollback to safe checkpoint", "Choose victim based on priority, resources held, time run"]),
    ]
    for txt, d, l, fu, pts in dead:
        Q.append(_q("deadlocks", d, l, txt, fu, pts))

    # ═══════ SYNCHRONIZATION ═══════
    sync = [
        ("What is a race condition? Give me a real example from your code or a common scenario.", "medium", "fresher",
         ["How do you detect race conditions?", "Tools for detection?"],
         ["Two threads access shared data concurrently", "Result depends on execution order", "Example: two threads incrementing a counter", "Solution: mutex, semaphore, atomic operations"]),
        ("Explain the Producer-Consumer problem. How would you solve it?", "medium", "fresher",
         ["What if buffer is full/empty?", "Using semaphores vs monitors?"],
         ["Shared bounded buffer between producer and consumer", "Producer adds items, consumer removes", "Semaphores: empty, full, mutex", "Block producer when full, consumer when empty"]),
        ("What is a mutex? How is it different from a semaphore?", "medium", "fresher",
         ["Binary semaphore vs mutex?", "Can a different thread unlock a mutex?"],
         ["Mutex: binary lock, owned by thread", "Semaphore: counting, can be > 1", "Mutex: only owner can unlock", "Semaphore: any thread can signal"]),
        ("Solve the Reader-Writer problem. How do you ensure writers don't starve?", "hard", "mid",
         ["Writer preference vs reader preference?", "What about fairness?"],
         ["Multiple readers can read simultaneously", "Writers need exclusive access", "Reader preference: writers may starve", "Writer preference: readers may starve"]),
        ("Explain the Dining Philosophers problem. What's your preferred solution?", "hard", "fresher",
         ["What about asymmetric solutions?", "Can you use a waiter?"],
         ["5 philosophers, 5 forks, need 2 forks to eat", "Naive solution: deadlock possible", "Solutions: asymmetric (one picks right first), limit 4 at table", "Monitor-based solution preferred"]),
        ("What are monitors? How do they differ from semaphores?", "medium", "mid",
         ["Condition variables?", "How does Java's synchronized use monitors?"],
         ["High-level synchronization construct", "Mutual exclusion built-in", "Condition variables for waiting/signaling", "Java: every object has a monitor (synchronized)"]),
        ("What is a spin lock? When would you use it over a mutex?", "medium", "mid",
         ["Busy waiting?", "Multiprocessor only?"],
         ["Thread spins in loop until lock available", "No context switch — stays on CPU", "Good for short critical sections on multiprocessors", "Bad for single processor — wastes CPU"]),
        ("What is the critical section problem? What are the requirements for a solution?", "easy", "fresher",
         ["Peterson's solution?", "Hardware support?"],
         ["Section of code accessing shared resources", "Requirements: mutual exclusion, progress, bounded waiting", "Peterson's: software solution for 2 processes", "Hardware: test-and-set, compare-and-swap"]),
    ]
    for txt, d, l, fu, pts in sync:
        Q.append(_q("synchronization", d, l, txt, fu, pts))

    # ═══════ FILE SYSTEMS ═══════
    fs = [
        ("What are the different file allocation methods? Compare contiguous, linked, and indexed.", "medium", "fresher",
         ["Which is used in ext4?", "External fragmentation?"],
         ["Contiguous: fast access, external fragmentation", "Linked: no fragmentation, slow random access", "Indexed: index block points to data blocks", "Ext4: extent-based (optimized contiguous)"]),
        ("What is an inode? What information does it store?", "medium", "fresher",
         ["What's NOT in the inode?", "How many inodes on a filesystem?"],
         ["File metadata: owner, permissions, timestamps, size", "Pointers to data blocks (direct, indirect)", "File name NOT in inode — it's in directory entry", "Fixed number of inodes at format time"]),
        ("What is a journaling file system? Why is it important?", "medium", "fresher",
         ["What happens without journaling during a crash?", "Write-ahead log?"],
         ["Logs changes before applying to main filesystem", "Crash recovery: replay or undo journal", "Prevents filesystem corruption", "Examples: ext4, NTFS, XFS"]),
        ("Explain hard links vs soft links (symbolic links) in Linux.", "easy", "fresher",
         ["Can you hard link directories?", "What happens when you delete the original?"],
         ["Hard link: another name for same inode", "Soft link: pointer to file path", "Delete original: hard link still works, soft link breaks", "Hard links can't cross filesystems"]),
        ("What is the difference between ext3, ext4, and XFS?", "medium", "mid",
         ["Maximum file size?", "Which is better for large files?"],
         ["ext4: extents, fast fsck, large files up to 16TB", "ext3: journal, no extents, slower", "XFS: best for large files, parallel I/O", "ext4 is default on most Linux distros"]),
    ]
    for txt, d, l, fu, pts in fs:
        Q.append(_q("file_systems", d, l, txt, fu, pts))

    # ═══════ DISK SCHEDULING ═══════
    disk = [
        ("Compare FCFS, SSTF, SCAN, and C-SCAN disk scheduling. Given a queue of requests and head at position 53, calculate total head movement for each.", "hard", "fresher",
         ["Which is fairest?", "Elevator algorithm?"],
         ["FCFS: serve in order, most movement", "SSTF: nearest request first, starvation possible", "SCAN: elevator — one direction then reverse", "C-SCAN: one direction only, jump back"]),
        ("What is the seek time, rotational latency, and transfer time in disk access?", "easy", "fresher",
         ["Which dominates?", "How do SSDs change this?"],
         ["Seek time: move head to track", "Rotational latency: wait for sector to rotate under head", "Transfer time: read/write data", "Seek time dominates — minimize it"]),
        ("Head is at track 50, queue: 82, 170, 43, 140, 24, 16, 190. Calculate SCAN total movement (moving toward 0 first).", "medium", "fresher",
         ["What about C-SCAN?", "Compare with SSTF."],
         ["SCAN toward 0: 50→43→24→16→0→82→140→170→190", "Total = 50+190 = 240 (or calculated step by step)", "Each direction change adds distance", "Gantt-like track-by-track calculation"]),
        ("Why do SSDs not need traditional disk scheduling algorithms?", "easy", "fresher",
         ["Random vs sequential access on SSD?", "What about SSD wear leveling?"],
         ["No mechanical parts — no seek time", "Random access same speed as sequential", "Wear leveling: distribute writes evenly", "TRIM command for SSD optimization"]),
    ]
    for txt, d, l, fu, pts in disk:
        Q.append(_q("disk_scheduling", d, l, txt, fu, pts))

    # ═══════ LINUX COMMANDS ═══════
    linux = [
        ("How would you find all files larger than 100MB modified in the last 7 days? Write the command.", "medium", "fresher",
         ["What about find vs locate?", "How do you handle filenames with spaces?"],
         ["find / -size +100M -mtime -7", "find uses real-time search, locate uses database", "Handle spaces: quotes or -print0 | xargs -0", "Add -type f for files only"]),
        ("What's the difference between ps, top, and htop? When do you use each?", "easy", "fresher",
         ["How do you find a specific process?", "What about kill?"],
         ["ps: snapshot of processes", "top: real-time updating view", "htop: interactive version of top", "ps aux | grep process_name to find specific"]),
        ("Explain file permissions in Linux. What does chmod 755 mean?", "easy", "fresher",
         ["What's the difference between chmod and chown?", "Sticky bit?"],
         ["rwxr-xr-x: owner=rwx(7), group=rx(5), others=rx(5)", "r=4, w=2, x=1", "chmod: change permissions, chown: change owner", "Sticky bit: only owner can delete (used on /tmp)"]),
        ("How do you redirect output, error, and both to a file?", "easy", "fresher",
         ["Append vs overwrite?", "What's /dev/null?"],
         ["stdout: > or 1>", "stderr: 2>", "Both: &> or 2>&1", "/dev/null: discard output"]),
        ("What is a pipe? How is it different from redirection?", "easy", "fresher",
         ["Named pipes?", "Can you pipe stderr?"],
         ["Pipe: output of one command → input of next", "Redirection: output to file", "Pipe connects two processes", "Named pipe (FIFO): mkfifo, persists in filesystem"]),
        ("How would you monitor disk usage on a Linux server?", "easy", "fresher",
         ["df vs du?", "What if disk is 90% full?"],
         ["df -h: filesystem-level usage", "du -sh: directory-level usage", "ncdu: interactive disk usage analyzer", "lsof to find deleted files still held open"]),
        ("What is the difference between grep, awk, and sed?", "medium", "fresher",
         ["When would you use awk over grep?", "Regular expressions?"],
         ["grep: pattern matching/searching", "sed: stream editing (find and replace)", "awk: pattern scanning + processing (columns)", "grep for search, sed for edit, awk for transform"]),
        ("How do you set up a cron job? What's the format?", "easy", "fresher",
         ["How do you debug a failing cron job?", "crontab -e?"],
         ["Five fields: minute hour day month weekday", "* * * * * = every minute", "crontab -e to edit, -l to list", "Redirect output to log for debugging"]),
        ("What are signals in Linux? What's the difference between SIGTERM and SIGKILL?", "medium", "fresher",
         ["Can you catch SIGKILL?", "What about SIGHUP?"],
         ["SIGTERM (15): graceful termination, can be caught", "SIGKILL (9): forced termination, cannot be caught", "SIGHUP: terminal closed, used for config reload", "kill -9 is last resort"]),
        ("How do you troubleshoot a process using too much CPU?", "medium", "mid",
         ["What tools would you use?", "What if it's a Java process?"],
         ["top/htop to identify process", "strace to see system calls", "perf for CPU profiling", "For Java: jstack for thread dump, jvisualvm"]),
    ]
    for txt, d, l, fu, pts in linux:
        Q.append(_q("linux_commands", d, l, txt, fu, pts, tg=["linux", "os"]))

    # ═══════ OSI MODEL ═══════
    osi = [
        ("When you type google.com in your browser and press Enter, walk me through what happens at each network layer.", "hard", "fresher",
         ["What about HTTPS?", "Where does DNS fit?", "What about caching?"],
         ["DNS resolution → IP address", "TCP 3-way handshake", "TLS handshake for HTTPS", "HTTP request → response → rendering"]),
        ("Explain the 7 layers of the OSI model. What protocol operates at each layer?", "medium", "fresher",
         ["TCP/IP model has how many layers?", "Where does SSL/TLS fit?"],
         ["Physical: bits, Ethernet cables", "Data Link: frames, MAC, switches", "Network: packets, IP, routers", "Transport: TCP/UDP, segments"]),
        ("What's the difference between the OSI model and the TCP/IP model?", "easy", "fresher",
         ["Which is used in practice?", "Why 7 layers vs 4?"],
         ["OSI: 7 layers (theoretical)", "TCP/IP: 4 layers (practical)", "TCP/IP combines OSI layers 5-7 into Application", "TCP/IP is what the internet actually uses"]),
        ("At which layer does a router operate? What about a switch? A hub?", "easy", "fresher",
         ["Layer 3 switch?", "Where does a firewall operate?"],
         ["Hub: Physical (Layer 1) — broadcasts everything", "Switch: Data Link (Layer 2) — MAC addresses", "Router: Network (Layer 3) — IP addresses", "L3 switch: combines switching + routing"]),
        ("What is encapsulation in networking? How does data change as it moves down the layers?", "medium", "fresher",
         ["What's a PDU?", "What about de-encapsulation?"],
         ["Application: data → Transport: segment → Network: packet → Data Link: frame → Physical: bits", "Each layer adds its header", "De-encapsulation: reverse process at receiver", "PDU: Protocol Data Unit at each layer"]),
    ]
    for txt, d, l, fu, pts in osi:
        Q.append(_q("osi_model", d, l, txt, fu, pts, rubric=R_CN, tg=["networking", "osi"]))

    # ═══════ TCP/UDP ═══════
    tcp = [
        ("Explain the TCP three-way handshake. What happens if the final ACK is lost?", "medium", "fresher",
         ["What about four-way termination?", "SYN flood attack?"],
         ["SYN → SYN-ACK → ACK", "Establishes connection, exchanges sequence numbers", "Lost ACK: server retransmits SYN-ACK", "SYN flood: exhaust server resources with half-open connections"]),
        ("When would you choose UDP over TCP? Give me real-world examples.", "easy", "fresher",
         ["Video streaming?", "DNS?", "Gaming?"],
         ["UDP: faster, no connection overhead", "Video streaming: occasional loss is OK", "DNS: small queries, speed matters", "Gaming: low latency critical, can tolerate loss"]),
        ("How does TCP ensure reliable data delivery? What happens when a packet is lost?", "medium", "fresher",
         ["Retransmission timeout?", "Fast retransmit?", "Sliding window?"],
         ["Sequence numbers track order", "ACK confirms receipt", "Timeout retransmission for lost packets", "Sliding window for flow control"]),
        ("What is TCP flow control? How does the sliding window protocol work?", "medium", "fresher",
         ["What is window size?", "What's the difference between flow control and congestion control?"],
         ["Receiver advertises window size (how much it can accept)", "Sender limits unacknowledged data to window size", "Flow control: end-to-end (receiver capacity)", "Congestion control: network capacity"]),
        ("Explain TCP congestion control — slow start, congestion avoidance, fast retransmit, fast recovery.", "hard", "mid",
         ["What triggers slow start vs congestion avoidance?", "What is cwnd?"],
         ["Slow start: exponential growth until threshold", "Congestion avoidance: linear growth after threshold", "Fast retransmit: 3 duplicate ACKs → retransmit immediately", "Fast recovery: halve cwnd instead of reset"]),
        ("What is Nagle's algorithm? When would you disable it?", "hard", "mid",
         ["TCP_NODELAY?", "Interactive applications?"],
         ["Buffers small segments, sends when ACK received or buffer full", "Reduces number of small packets", "Disable for low-latency apps (gaming, SSH)", "TCP_NODELAY socket option"]),
        ("What are TCP keep-alive packets? Why do we need them?", "medium", "fresher",
         ["How often?", "What about application-level heartbeats?"],
         ["Detect dead connections", "Sent when no data exchanged for a period", "Default: 2 hours (configurable)", "Application-level heartbeats more responsive"]),
        ("What happens during TCP connection termination? Explain the four-way handshake.", "medium", "fresher",
         ["What is TIME_WAIT?", "Why wait 2MSL?"],
         ["FIN → ACK → FIN → ACK", "Both sides independently close their end", "TIME_WAIT: wait 2×MSL before reusing port", "Ensures delayed packets don't corrupt new connection"]),
    ]
    for txt, d, l, fu, pts in tcp:
        Q.append(_q("tcp_udp", d, l, txt, fu, pts, rubric=R_CN, tg=["networking", "tcp"]))

    # ═══════ IP ADDRESSING & SUBNETTING ═══════
    ip = [
        ("Given the IP address 192.168.1.0/24, how many usable host addresses are there? What are the network and broadcast addresses?", "easy", "fresher",
         ["What if it's /26?", "Why can't you use network and broadcast addresses?"],
         ["/24 = 256 addresses, 254 usable", "Network: 192.168.1.0, Broadcast: 192.168.1.255", "First address is network, last is broadcast", "Subnet mask: 255.255.255.0"]),
        ("Subnet the network 10.0.0.0/8 into subnets with at least 500 hosts each. How many subnets can you create?", "hard", "fresher",
         ["What's the subnet mask?", "VLSM?"],
         ["Need 500 hosts → 2^n - 2 >= 500 → n=9 → /23", "Subnet mask: 255.255.254.0", "Number of subnets: 2^(23-8) = 32768", "Each subnet: 510 usable hosts"]),
        ("What is NAT? Why was it invented and what problem does it solve?", "medium", "fresher",
         ["Types of NAT?", "How does NAT affect peer-to-peer?", "NAT traversal?"],
         ["Network Address Translation: maps private to public IPs", "Conserves IPv4 addresses", "Types: static, dynamic, PAT (port address translation)", "Breaks end-to-end connectivity"]),
        ("What is the difference between IPv4 and IPv6? Why haven't we fully migrated?", "medium", "fresher",
         ["Address size?", "IPv6 features?", "Dual stack?"],
         ["IPv4: 32-bit (4.3 billion), IPv6: 128-bit", "IPv6: no NAT needed, built-in security (IPsec)", "Migration slow: infrastructure cost, compatibility", "Dual stack: run both simultaneously"]),
        ("What are private IP ranges? Why can't they be routed on the internet?", "easy", "fresher",
         ["Which ranges?", "How does NAT use them?"],
         ["10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16", "Reserved for internal networks", "Routers drop packets with private source/dest on internet", "NAT translates to public IP at gateway"]),
        ("What is CIDR notation? How does it differ from classful addressing?", "medium", "fresher",
         ["Supernetting?", "VLSM?"],
         ["Classless Inter-Domain Routing", "/n notation specifies network bits", "Eliminates Class A/B/C waste", "Enables variable-length subnet masks"]),
        ("What is ARP? How does a machine find the MAC address for a given IP?", "medium", "fresher",
         ["ARP cache?", "ARP spoofing?"],
         ["Address Resolution Protocol: IP → MAC", "Broadcasts ARP request on LAN", "Target responds with its MAC", "ARP cache stores recent mappings"]),
        ("What is DHCP? Walk me through how a device gets an IP address when it joins a network.", "medium", "fresher",
         ["DORA process?", "What if DHCP server is down?"],
         ["Discover → Offer → Request → Acknowledge", "Client broadcasts discover, server offers IP", "Client requests offered IP, server acknowledges", "Lease-based: IP assigned for a duration"]),
    ]
    for txt, d, l, fu, pts in ip:
        Q.append(_q("ip_addressing", d, l, txt, fu, pts, rubric=R_CN, tg=["networking", "ip"]))

    # ═══════ HTTP & APPLICATION LAYER ═══════
    http = [
        ("What's the difference between HTTP and HTTPS? How does TLS work?", "medium", "fresher",
         ["What is a certificate?", "Symmetric vs asymmetric encryption?"],
         ["HTTPS = HTTP + TLS encryption", "TLS handshake: certificate verification + key exchange", "Asymmetric for key exchange, symmetric for data", "Prevents eavesdropping and tampering"]),
        ("Explain HTTP status codes. What's the difference between 301 and 302? 401 and 403?", "easy", "fresher",
         ["When do you use 204?", "What about 429?"],
         ["2xx: success, 3xx: redirect, 4xx: client error, 5xx: server error", "301: permanent redirect, 302: temporary", "401: unauthenticated, 403: forbidden (lacks permission)", "429: rate limited"]),
        ("What are HTTP methods? When do you use PUT vs PATCH vs POST?", "easy", "fresher",
         ["Idempotency?", "Safe methods?"],
         ["GET: read, POST: create, PUT: replace, PATCH: partial update, DELETE: remove", "PUT: idempotent (same result if repeated)", "POST: not idempotent", "PATCH: partial update, PUT: full replacement"]),
        ("How do cookies work? What's the difference between session cookies and persistent cookies?", "medium", "fresher",
         ["SameSite attribute?", "Cookie vs localStorage?", "HttpOnly flag?"],
         ["Server sets cookie via Set-Cookie header", "Session cookie: deleted when browser closes", "Persistent: has expiry date", "HttpOnly: not accessible via JavaScript"]),
        ("What is a REST API? What makes an API RESTful?", "medium", "fresher",
         ["REST vs SOAP?", "HATEOAS?", "Versioning strategies?"],
         ["Representational State Transfer", "Stateless, resource-based URLs", "Standard HTTP methods for CRUD", "JSON responses, proper status codes"]),
        ("What is the difference between HTTP/1.1 and HTTP/2?", "medium", "mid",
         ["Multiplexing?", "Server push?", "Header compression?"],
         ["HTTP/2: multiplexing (multiple requests on one connection)", "Binary protocol vs text-based", "Header compression (HPACK)", "Server push: send resources before requested"]),
        ("Explain DNS resolution step by step. What happens when you query a domain name?", "medium", "fresher",
         ["Recursive vs iterative?", "DNS caching?", "TTL?"],
         ["Browser cache → OS cache → resolver → root → TLD → authoritative", "Recursive: resolver does all lookups", "Iterative: resolver gets referrals, queries each", "TTL: how long to cache the record"]),
        ("What are the different DNS record types?", "easy", "fresher",
         ["What's CNAME used for?", "MX records?"],
         ["A: domain → IPv4", "AAAA: domain → IPv6", "CNAME: alias to another domain", "MX: mail server, NS: nameserver, TXT: verification"]),
    ]
    for txt, d, l, fu, pts in http:
        Q.append(_q("http_application", d, l, txt, fu, pts, rubric=R_CN, tg=["networking", "http"]))

    # ═══════ ROUTING ═══════
    routing = [
        ("What's the difference between static and dynamic routing?", "easy", "fresher",
         ["When is static routing sufficient?", "What are routing protocols?"],
         ["Static: manually configured routes", "Dynamic: routes discovered via protocols", "Static: simple, small networks", "Dynamic: scalable, adapts to changes"]),
        ("Compare distance vector and link-state routing protocols.", "medium", "fresher",
         ["Examples of each?", "Count to infinity problem?"],
         ["Distance vector: shares routing table with neighbors (RIP)", "Link-state: shares network topology with all (OSPF)", "DV: slow convergence, count-to-infinity", "LS: faster convergence, more memory/CPU"]),
        ("What is BGP and why is it critical for the internet?", "hard", "mid",
         ["Path vector?", "BGP hijacking?"],
         ["Border Gateway Protocol: inter-AS routing", "Path vector protocol: avoids loops", "Autonomous Systems exchange reachability info", "BGP hijacking: route traffic through malicious AS"]),
        ("What is the difference between a routing table and a forwarding table?", "medium", "fresher",
         ["Who builds each?", "Which is used for actual packet forwarding?"],
         ["Routing table: built by routing protocols, contains all routes", "Forwarding table: optimized subset used for fast lookup", "Routing table → forwarding table via FIB", "Forwarding table used by hardware for line-rate switching"]),
        ("Explain how a router forwards a packet. What happens when no route matches?", "medium", "fresher",
         ["Default route?", "Longest prefix match?"],
         ["Extract destination IP from packet", "Longest prefix match in routing table", "Decrement TTL, update checksum", "No match: drop packet, send ICMP unreachable"]),
    ]
    for txt, d, l, fu, pts in routing:
        Q.append(_q("routing", d, l, txt, fu, pts, rubric=R_CN, tg=["networking", "routing"]))

    # ═══════ DATA LINK LAYER ═══════
    dll = [
        ("What's the difference between a hub, switch, and router?", "easy", "fresher",
         ["Where does a bridge fit?", "Managed vs unmanaged switch?"],
         ["Hub: broadcasts to all ports (L1)", "Switch: forwards to specific port via MAC table (L2)", "Router: forwards between networks via IP (L3)", "Switch eliminates collisions"]),
        ("How does a switch learn MAC addresses and build its forwarding table?", "medium", "fresher",
         ["What about unknown unicast?", "MAC table aging?"],
         ["Learns source MAC from incoming frames", "Associates MAC with port", "Unknown destination: floods to all ports", "Aging: removes entries after timeout"]),
        ("What is a VLAN? Why would you use it?", "medium", "fresher",
         ["How do VLANs improve security?", "802.1Q tagging?"],
         ["Virtual LAN: logical network segmentation", "Reduces broadcast domains", "Security: isolate departments", "802.1Q: VLAN tag in Ethernet frame"]),
        ("What is the Ethernet frame format? What's in the header?", "medium", "fresher",
         ["Maximum frame size?", "What's the FCS?"],
         ["Preamble, dest MAC, source MAC, EtherType, data, FCS", "Max payload: 1500 bytes (MTU)", "FCS: Frame Check Sequence for error detection", "EtherType identifies upper layer protocol"]),
        ("What is CSMA/CD? How does it prevent collisions in Ethernet?", "medium", "fresher",
         ["Is it still used?", "What about wireless (CSMA/CA)?"],
         ["Carrier Sense Multiple Access / Collision Detection", "Listen before transmitting", "If collision: stop, send jam, exponential backoff", "Obsolete with full-duplex switches"]),
    ]
    for txt, d, l, fu, pts in dll:
        Q.append(_q("data_link_layer", d, l, txt, fu, pts, rubric=R_CN, tg=["networking", "data_link"]))

    # ═══════ NETWORK SECURITY ═══════
    sec = [
        ("What is a firewall? What's the difference between stateless and stateful firewalls?", "easy", "fresher",
         ["Where does a WAF fit?", "IDS vs IPS?"],
         ["Filters traffic based on rules", "Stateless: checks individual packets", "Stateful: tracks connection state", "WAF: application-layer (HTTP) filtering"]),
        ("Explain how VPN works. What protocols does it use?", "medium", "fresher",
         ["IPSec vs OpenVPN?", "Split tunneling?"],
         ["Creates encrypted tunnel over public network", "Protocols: IPSec, OpenVPN, WireGuard", "Encrypts all traffic between endpoints", "Split tunnel: only some traffic through VPN"]),
        ("What is a man-in-the-middle attack? How does HTTPS prevent it?", "medium", "fresher",
         ["Certificate pinning?", "What if the attacker has a valid cert?"],
         ["Attacker intercepts communication between two parties", "HTTPS: certificate verification prevents impersonation", "TLS encrypts data — attacker can't read", "Certificate authority trust chain"]),
        ("What is a DDoS attack? How can you mitigate it?", "medium", "fresher",
         ["SYN flood?", "Rate limiting?", "CDN protection?"],
         ["Distributed Denial of Service: overwhelm with traffic", "SYN flood: exhaust connection table", "Mitigation: rate limiting, CDN, scrubbing", "Cloud providers: AWS Shield, Cloudflare"]),
        ("What is DNS spoofing? How does DNSSEC prevent it?", "hard", "mid",
         ["How does cache poisoning work?", "Is DNSSEC widely deployed?"],
         ["Attacker provides fake DNS responses", "Cache poisoning: corrupt DNS resolver cache", "DNSSEC: digital signatures on DNS records", "Deployment slow due to complexity"]),
    ]
    for txt, d, l, fu, pts in sec:
        Q.append(_q("network_security", d, l, txt, fu, pts, rubric=R_CN, tg=["networking", "security"]))

    # ═══════ SOCKET PROGRAMMING ═══════
    sock = [
        ("What is a socket? How does the client-server model work with TCP sockets?", "medium", "fresher",
         ["Socket types?", "What about non-blocking sockets?"],
         ["Socket: endpoint for communication (IP + port)", "Server: socket → bind → listen → accept", "Client: socket → connect", "Both: send/recv, then close"]),
        ("What is the difference between blocking and non-blocking I/O? How does select/poll/epoll help?", "hard", "mid",
         ["Event-driven architecture?", "How does Node.js use this?"],
         ["Blocking: thread waits until I/O completes", "Non-blocking: returns immediately, check later", "select/poll: monitor multiple file descriptors", "epoll: scalable alternative for Linux"]),
        ("What are well-known ports? Name 5 common ones.", "easy", "fresher",
         ["Ephemeral ports?", "Why are ports below 1024 privileged?"],
         ["HTTP: 80, HTTPS: 443, SSH: 22, DNS: 53, FTP: 21", "SMTP: 25, MySQL: 3306, PostgreSQL: 5432", "Well-known: 0-1023, need root to bind", "Ephemeral: 49152-65535 for client connections"]),
        ("How would you handle multiple client connections in a server?", "medium", "mid",
         ["Thread per connection?", "Thread pool?", "Event loop?"],
         ["Thread per connection: simple but doesn't scale", "Thread pool: bounded resources, queued connections", "Event loop (select/epoll): single thread, many connections", "async/await: modern approach (asyncio, Node.js)"]),
    ]
    for txt, d, l, fu, pts in sock:
        Q.append(_q("socket_programming", d, l, txt, fu, pts, rubric=R_CN, tg=["networking", "sockets"]))

    # ═══════ TEMPLATE EXPANSION: OS Concepts ═══════
    os_concepts = [
        ("Explain the concept of {concept} in operating systems. Why is it important?", "medium", "fresher",
         ["How does Linux implement this?", "What about Windows?"],
         ["{concept} definition and purpose", "How it's implemented in modern OS", "Real-world implications", "Performance trade-offs"]),
    ]
    concepts = ["virtual memory", "paging", "demand paging", "copy-on-write", "memory-mapped files",
                "DMA (Direct Memory Access)", "RAID levels", "bootstrapping", "system calls",
                "interrupt handling", "kernel space vs user space", "multitasking", "multiprocessing",
                "process scheduling", "swapping"]
    for tmpl_txt, d, l, fu, pts in os_concepts:
        for c in concepts:
            Q.append(_q("os_concepts", d, l, tmpl_txt.format(concept=c),
                        [f.format(concept=c) for f in fu],
                        [pt.format(concept=c) for pt in pts]))

    # ═══════ TEMPLATE EXPANSION: Protocol comparisons ═══════
    protocol_templates = [
        ("Compare {a} and {b}. When would you use each?", "medium", "fresher",
         ["Which is more commonly used today?", "Performance differences?"],
         ["Definition of {a}", "Definition of {b}", "Key differences", "Use cases for each"]),
    ]
    protocols = [
        ("TCP", "UDP"), ("HTTP", "HTTPS"), ("IPv4", "IPv6"),
        ("FTP", "SFTP"), ("SMTP", "IMAP"), ("HTTP/1.1", "HTTP/2"),
        ("REST", "GraphQL"), ("WebSocket", "HTTP long polling"),
        ("SSL", "TLS"), ("OSPF", "RIP"), ("ARP", "RARP"),
        ("Unicast", "Multicast"), ("Hub", "Switch"), ("Router", "Gateway"),
    ]
    for tmpl_txt, d, l, fu, pts in protocol_templates:
        for a, b in protocols:
            Q.append(_q("protocol_comparison", d, l, tmpl_txt.format(a=a, b=b),
                        [f.format(a=a, b=b) for f in fu],
                        [pt.format(a=a, b=b) for pt in pts], rubric=R_CN, tg=["networking", "comparison"]))

    # ═══════ COMPANY-SPECIFIC ═══════
    cisco = [
        ("How does OSPF establish neighbor relationships? What are the different states?", "hard", "mid",
         ["DR/BDR election?", "OSPF areas?"],
         ["Down → Init → 2-Way → ExStart → Exchange → Loading → Full", "Hello packets for neighbor discovery", "DR/BDR reduce update traffic", "Areas: backbone (0) + regular areas"]),
        ("Explain how a Layer 3 switch differs from a traditional router.", "medium", "mid",
         ["When to use each?", "ASIC-based forwarding?"],
         ["L3 switch: hardware-based routing at wire speed", "Router: software-based, more features (NAT, VPN)", "L3 switch for LAN routing", "Router for WAN connections"]),
        ("What is STP (Spanning Tree Protocol)? Why is it needed?", "medium", "fresher",
         ["Root bridge election?", "RSTP?"],
         ["Prevents loops in L2 networks", "Elects root bridge, blocks redundant paths", "Loop: broadcast storm, MAC table instability", "RSTP: faster convergence"]),
        ("How would you troubleshoot a network connectivity issue between two servers?", "medium", "mid",
         ["Layer by layer?", "Which commands?"],
         ["ping for basic connectivity", "traceroute to find where it breaks", "Check IP config (ifconfig/ip addr)", "Check routes, firewall rules, DNS"]),
    ]
    for txt, d, l, fu, pts in cisco:
        Q.append(_q("networking_advanced", d, l, txt, fu, pts, rubric=R_CN, co="Cisco", tg=["cisco", "networking"]))

    amazon_os = [
        ("You have a Linux server that's running slow. How do you diagnose and fix it?", "hard", "mid",
         ["Which metrics do you check first?", "What tools?"],
         ["Check CPU (top), memory (free), disk (iostat), network (netstat)", "Identify bottleneck: CPU-bound vs I/O-bound vs memory-bound", "Check processes: which is consuming resources?", "Analyze: logs, strace, profiling"]),
        ("How does the Linux kernel manage memory for a process?", "hard", "mid",
         ["Virtual address space layout?", "Heap vs stack?"],
         ["Virtual address space: text, data, BSS, heap, stack", "Heap: dynamic allocation (malloc/free)", "Stack: function calls, local variables", "Kernel manages page tables, TLB"]),
        ("Explain how select() and epoll() differ. Why is epoll better for high-concurrency servers?", "hard", "mid",
         ["O(n) vs O(1)?", "Level-triggered vs edge-triggered?"],
         ["select: O(n) scan all FDs each call, 1024 FD limit", "epoll: O(1) for ready FDs, no limit", "epoll: kernel tracks interest, notifies on events", "Edge-triggered: notify once, level-triggered: keep notifying"]),
        ("What is a container? How does it differ from a virtual machine at the OS level?", "medium", "mid",
         ["Namespaces and cgroups?", "Security isolation?"],
         ["Container: shares host OS kernel, isolated processes", "VM: full OS with hypervisor", "Container: namespaces (PID, network, mount) + cgroups", "Lighter weight, faster startup vs VM"]),
    ]
    for txt, d, l, fu, pts in amazon_os:
        Q.append(_q("os_advanced", d, l, txt, fu, pts, co="Amazon", tg=["amazon", "os"]))

    tcs_os = [
        ("What is an operating system? List the main functions.", "easy", "fresher",
         ["Types of OS?", "Real-time OS?"],
         ["Manages hardware resources", "Process management, memory management, file management", "I/O management, security", "Types: batch, time-sharing, real-time, distributed"]),
        ("What is a semaphore? How does it solve the critical section problem?", "medium", "fresher",
         ["Binary vs counting?", "wait() and signal()?"],
         ["Integer variable for synchronization", "Binary: 0 or 1 (like mutex)", "Counting: controls access to N resources", "wait() decrements, signal() increments"]),
        ("What is paging? How does it solve external fragmentation?", "medium", "fresher",
         ["Page vs frame?", "Page table?"],
         ["Divide memory into fixed-size pages (logical) and frames (physical)", "Any page can map to any frame", "No external fragmentation — all blocks same size", "Internal fragmentation in last page"]),
        ("What is the difference between multiprogramming and multitasking?", "easy", "fresher",
         ["Time-sharing?", "Which is more common?"],
         ["Multiprogramming: multiple programs in memory", "Multitasking: CPU switches rapidly between tasks", "Multitasking is form of multiprogramming with time-sharing", "Modern OS: preemptive multitasking"]),
        ("Explain FCFS disk scheduling. Given head at 50 and queue [98, 183, 37, 122, 14, 124, 65, 67], calculate total head movement.", "medium", "fresher",
         ["Compare with SSTF.", "Is FCFS fair?"],
         ["Process in order: 50→98→183→37→122→14→124→65→67", "Calculate absolute differences and sum", "FCFS is fair but high total movement", "SSTF would reduce movement but may starve"]),
    ]
    for txt, d, l, fu, pts in tcs_os:
        Q.append(_q("os_basics", d, l, txt, fu, pts, co="TCS", tg=["tcs", "os"]))

    return Q
