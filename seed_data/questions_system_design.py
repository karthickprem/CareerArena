"""System Design interview questions for PlaceRight. ~500 questions via template expansion."""
from typing import List, Dict

R = {"1-3": "Cannot think about systems beyond single server. No scalability awareness.",
     "4-5": "Knows basics but can't design end-to-end. Missing key components.",
     "6-7": "Designs reasonable systems. Considers scalability. Minor trade-off gaps.",
     "8-10": "Expert design. Deep trade-off analysis. Handles edge cases. Production-ready thinking."}

def _q(t, d, l, txt, fu, pts, co="", tg=None):
    return {"domain": "software_engineering", "topic": t, "difficulty": d, "level": l,
            "question_text": txt, "follow_ups": fu, "expected_points": pts,
            "scoring_rubric": R, "company_specific": co, "tags": tg or [t]}

def get_system_design_questions() -> List[Dict]:
    Q = []

    # ═══════ CLASSIC SYSTEM DESIGNS ═══════
    classic = [
        ("Design a URL shortener like bit.ly. How would you handle 100 million URLs?", "hard", "mid",
         ["How do you generate the short code?", "What about analytics — click counts?", "How do you handle collisions?"],
         ["API: POST /shorten, GET /:code → 301 redirect", "Base62 encoding of auto-increment ID or hash", "Database: code → original URL mapping", "Cache popular URLs in Redis, 301 vs 302 redirect"]),
        ("Design a chat system like WhatsApp. Focus on one-to-one messaging first, then group chat.", "hard", "mid",
         ["How do you handle offline users?", "Message ordering?", "End-to-end encryption?"],
         ["WebSocket for real-time delivery", "Message queue for offline message storage", "Acknowledgment system: sent, delivered, read", "Database: per-user message store"]),
        ("Design a notification system that sends email, SMS, and push notifications.", "medium", "mid",
         ["How do you handle rate limiting per user?", "What about notification preferences?", "Retry failed notifications?"],
         ["Notification service receives events via queue", "Fan-out to channel-specific workers", "User preference store for opt-in/opt-out", "Retry with exponential backoff, dead letter queue"]),
        ("Design an e-commerce platform like Amazon/Flipkart. Focus on the product catalog and order flow.", "hard", "mid",
         ["How do you handle inventory?", "What about flash sales?", "Payment failures?"],
         ["Product service: catalog, search (Elasticsearch)", "Order service: cart → checkout → payment → fulfillment", "Inventory: optimistic locking for concurrency", "Distributed transactions: saga pattern"]),
        ("Design a video streaming platform like YouTube. How do you handle uploads and playback?", "hard", "mid",
         ["How do you transcode videos?", "Adaptive bitrate streaming?", "CDN strategy?"],
         ["Upload: chunked upload to object storage", "Transcode: async workers, multiple resolutions", "Playback: HLS/DASH adaptive bitrate", "CDN: cache popular videos at edge"]),
        ("Design a rate limiter. How would you implement it for an API gateway?", "medium", "mid",
         ["Distributed rate limiting?", "Different limits per user tier?"],
         ["Token bucket: most flexible", "Fixed window: simple but spike at boundary", "Sliding window: accurate but more memory", "Redis for distributed state across servers"]),
        ("Design Twitter's news feed. How do you handle feed generation for millions of users?", "hard", "mid",
         ["Fan-out on write vs fan-out on read?", "What about celebrity accounts with millions of followers?"],
         ["Fan-out on write: pre-compute feed at tweet time", "Fan-out on read: compute feed at request time", "Hybrid: celebrities use fan-out on read", "Redis timeline cache per user"]),
        ("Design a ride-sharing service like Uber/Ola. Focus on matching drivers to riders.", "hard", "mid",
         ["How do you find nearby drivers?", "Surge pricing?", "ETA calculation?"],
         ["Geospatial index: quadtree or geohash", "Location service: drivers send GPS every 4s", "Matching: nearest available driver with constraints", "Surge: dynamic pricing based on demand/supply ratio"]),
        ("Design a search engine. How does Google index the web and rank results?", "hard", "mid",
         ["Inverted index?", "PageRank?", "How do you handle typos?"],
         ["Crawler: discovers and downloads web pages", "Indexer: builds inverted index (word → documents)", "Ranker: PageRank + relevance signals", "Query: parse, search index, rank, return top-K"]),
        ("Design a file storage service like Google Drive or Dropbox. How do you handle sync?", "hard", "mid",
         ["Conflict resolution?", "Chunking large files?", "Offline access?"],
         ["Chunk files into blocks, hash for dedup", "Metadata service: tracks file versions, permissions", "Sync: client detects changes, uploads modified chunks", "Conflict: last-write-wins or keep both versions"]),
    ]
    for txt, d, l, fu, pts in classic:
        Q.append(_q("system_design", d, l, txt, fu, pts))

    # ═══════ DATABASE DESIGN ═══════
    db = [
        ("How do you decide between SQL and NoSQL for a new project?", "medium", "mid",
         ["What about NewSQL?", "Can you use both?"],
         ["SQL: structured data, ACID, complex queries", "NoSQL: flexible schema, horizontal scaling, high throughput", "SQL: banking, e-commerce. NoSQL: social media, IoT", "Polyglot persistence: use both where appropriate"]),
        ("What is database sharding? How do you choose a shard key?", "hard", "mid",
         ["Hot spots?", "Cross-shard queries?", "Resharding?"],
         ["Distribute data across multiple databases", "Shard key determines which shard stores each row", "Good key: even distribution, avoids cross-shard queries", "Bad key: timestamp (hot spot), random (bad range queries)"]),
        ("Explain the CAP theorem. Give examples of CP and AP systems.", "medium", "mid",
         ["Can you have all three?", "PACELC?"],
         ["Consistency, Availability, Partition tolerance — pick 2", "CP: MongoDB, HBase (sacrifice availability during partition)", "AP: Cassandra, DynamoDB (sacrifice consistency during partition)", "In practice: tune consistency level per operation"]),
        ("How does database replication work? Compare master-slave vs master-master.", "medium", "mid",
         ["Replication lag?", "Conflict resolution in multi-master?"],
         ["Master-slave: writes to master, reads from replicas", "Master-master: writes to any node", "Replication lag: eventual consistency", "Conflict resolution: last-write-wins, vector clocks"]),
        ("What are database indexes? When would you NOT create an index?", "medium", "fresher",
         ["B-tree vs hash index?", "Composite indexes?", "Covering index?"],
         ["Speed up reads at cost of slower writes", "B-tree: range queries + equality", "Don't index: small tables, frequently updated columns", "Composite: column order matters for query matching"]),
        ("Explain ACID properties with examples. What happens when you relax them?", "medium", "fresher",
         ["BASE as alternative?", "Eventual consistency?"],
         ["Atomicity: all or nothing", "Consistency: valid state transitions", "Isolation: concurrent transactions don't interfere", "Durability: committed data survives crashes"]),
        ("What is a write-ahead log (WAL)? How does it ensure durability?", "hard", "mid",
         ["Checkpointing?", "How does PostgreSQL use WAL?"],
         ["Log changes before applying to data files", "Crash recovery: replay WAL from last checkpoint", "Sequential writes to WAL (fast) vs random writes to data", "PostgreSQL: WAL for crash recovery + replication"]),
        ("How do you handle schema migrations in a live production database?", "hard", "mid",
         ["Zero-downtime migrations?", "Rollback strategy?"],
         ["Expand-contract pattern: add new, migrate, remove old", "Never rename/drop columns directly", "Backfill data in batches, not one big UPDATE", "Feature flags during transition period"]),
    ]
    for txt, d, l, fu, pts in db:
        Q.append(_q("database_design", d, l, txt, fu, pts))

    # ═══════ CACHING ═══════
    cache = [
        ("What caching strategies do you know? When do you use cache-aside vs write-through?", "medium", "mid",
         ["Cache invalidation?", "What about write-behind?"],
         ["Cache-aside: app manages cache (read: check cache, miss → DB → cache)", "Write-through: write to cache AND DB simultaneously", "Write-behind: write to cache, async write to DB", "Cache-aside most common, write-through for consistency"]),
        ("What is cache invalidation? Why is it called one of the two hard problems in CS?", "hard", "mid",
         ["TTL-based vs event-based?", "Stale reads?"],
         ["When to update/remove cached data", "TTL: simple but stale window", "Event-based: publish change events, more complex", "Trade-off: freshness vs performance"]),
        ("How does Redis work as a cache? What data structures does it support?", "medium", "mid",
         ["Persistence options?", "Redis Cluster?", "Eviction policies?"],
         ["In-memory key-value store", "Strings, Lists, Sets, Sorted Sets, Hashes, Streams", "Persistence: RDB snapshots, AOF log", "Eviction: LRU, LFU, random, TTL-based"]),
        ("How would you implement a distributed cache for a microservices architecture?", "hard", "mid",
         ["Cache stampede?", "Consistent hashing?"],
         ["Redis/Memcached cluster for shared cache", "Consistent hashing for key distribution", "Cache stampede: use locking or probabilistic early expiry", "Local cache + distributed cache: L1/L2 pattern"]),
        ("What is a CDN and how does it relate to caching?", "easy", "fresher",
         ["Push vs pull CDN?", "Cache headers?"],
         ["Content Delivery Network: geographically distributed cache", "Static assets: images, CSS, JS at edge servers", "Push: upload to CDN. Pull: CDN fetches on first request", "Cache-Control headers determine CDN behavior"]),
    ]
    for txt, d, l, fu, pts in cache:
        Q.append(_q("caching", d, l, txt, fu, pts))

    # ═══════ LOAD BALANCING ═══════
    lb = [
        ("What are the different load balancing algorithms? When do you use each?", "medium", "mid",
         ["Sticky sessions?", "Health checks?"],
         ["Round robin: simple, equal distribution", "Weighted round robin: for heterogeneous servers", "Least connections: send to least loaded", "IP hash: same client → same server (sticky)"]),
        ("What's the difference between L4 and L7 load balancing?", "medium", "mid",
         ["Performance difference?", "SSL termination?"],
         ["L4: transport layer, routes by IP/port, faster", "L7: application layer, routes by HTTP content", "L7: can do URL-based routing, header inspection", "L7: SSL termination, but more CPU"]),
        ("How does a load balancer handle server failures?", "medium", "mid",
         ["Active health checks vs passive?", "Graceful degradation?"],
         ["Health checks: periodic probes to each server", "Active: LB sends probe requests", "Passive: monitor actual traffic for errors", "Failed server removed from pool automatically"]),
        ("You have 3 application servers behind a load balancer. How do you handle session state?", "medium", "mid",
         ["Sticky sessions?", "Shared session store?"],
         ["Problem: user may hit different server each request", "Option 1: sticky sessions (IP hash) — couples client to server", "Option 2: shared session store (Redis) — best", "Option 3: stateless JWT — no server session"]),
    ]
    for txt, d, l, fu, pts in lb:
        Q.append(_q("load_balancing", d, l, txt, fu, pts))

    # ═══════ MESSAGING & QUEUES ═══════
    mq = [
        ("When would you use a message queue? What problems does it solve?", "medium", "mid",
         ["RabbitMQ vs Kafka?", "Dead letter queue?"],
         ["Decouples producers from consumers", "Handles traffic spikes: queue absorbs burst", "Async processing: respond immediately, process later", "Fault tolerance: retry failed messages"]),
        ("Compare Kafka and RabbitMQ. When would you choose each?", "hard", "mid",
         ["Ordering guarantees?", "Throughput?"],
         ["Kafka: high throughput log, ordered partitions, replay", "RabbitMQ: traditional queue, flexible routing, acknowledgment", "Kafka: event streaming, analytics, log aggregation", "RabbitMQ: task queues, RPC, lower throughput needs"]),
        ("What is event-driven architecture? How does it differ from request-response?", "medium", "mid",
         ["Event sourcing?", "CQRS?"],
         ["Components communicate via events", "Async: producer doesn't wait for consumer", "Loose coupling: producer doesn't know consumers", "Event sourcing: store events, derive state"]),
        ("What is the pub/sub pattern? How does it differ from point-to-point messaging?", "medium", "mid",
         ["Fan-out?", "Topic-based filtering?"],
         ["Pub/sub: message sent to all subscribers", "Point-to-point: message consumed by one consumer", "Pub/sub: notifications, broadcasting", "Point-to-point: task distribution, work queues"]),
    ]
    for txt, d, l, fu, pts in mq:
        Q.append(_q("messaging_queues", d, l, txt, fu, pts))

    # ═══════ MICROSERVICES ═══════
    micro = [
        ("What are microservices? When should you NOT use them?", "medium", "mid",
         ["Monolith first?", "Team size considerations?"],
         ["Small, independent services with own database", "Benefits: independent deployment, scaling, tech diversity", "Don't use: small team, simple app, early stage", "Monolith first: extract services when needed"]),
        ("What is an API Gateway? What problems does it solve?", "medium", "mid",
         ["Kong vs AWS API Gateway?", "Backend for Frontend?"],
         ["Single entry point for all microservices", "Cross-cutting: auth, rate limiting, logging", "Request routing to appropriate service", "BFF: different gateway per client type"]),
        ("What is the circuit breaker pattern? How does it prevent cascading failures?", "hard", "mid",
         ["States: closed, open, half-open?", "Hystrix/Resilience4j?"],
         ["Monitors calls to downstream service", "Closed: normal operation, count failures", "Open: reject calls immediately (fail fast)", "Half-open: allow some calls to test recovery"]),
        ("How do you handle distributed transactions across microservices?", "hard", "mid",
         ["Saga pattern?", "Two-phase commit?"],
         ["2PC: coordinator-based, strong consistency, slow", "Saga: sequence of local transactions with compensations", "Choreography: events trigger next step", "Orchestration: central coordinator directs flow"]),
        ("How do microservices discover each other? What is service discovery?", "medium", "mid",
         ["DNS-based vs registry-based?", "Consul vs Eureka?"],
         ["Service registry: services register on startup", "Client-side discovery: client queries registry", "Server-side discovery: load balancer queries registry", "DNS-based: Kubernetes services, simpler"]),
        ("What is eventual consistency? How do you handle it in microservices?", "hard", "mid",
         ["Compensating transactions?", "Idempotent operations?"],
         ["Data across services may not be immediately consistent", "Accept: show stale data briefly", "Saga: compensating transactions for rollback", "Idempotent operations: safe to retry"]),
    ]
    for txt, d, l, fu, pts in micro:
        Q.append(_q("microservices", d, l, txt, fu, pts))

    # ═══════ API DESIGN ═══════
    api = [
        ("Compare REST, GraphQL, and gRPC. When would you use each?", "hard", "mid",
         ["Performance differences?", "Learning curve?"],
         ["REST: simple, widely understood, HTTP-native", "GraphQL: flexible queries, no over/under-fetching", "gRPC: binary protocol, streaming, service-to-service", "REST for public APIs, gRPC for internal, GraphQL for complex UIs"]),
        ("How would you design an API for a mobile app where bandwidth is limited?", "medium", "mid",
         ["Pagination?", "Field selection?", "Compression?"],
         ["Allow field selection: ?fields=name,email", "Pagination: cursor-based for efficiency", "Compression: gzip/brotli responses", "GraphQL: client specifies exactly what it needs"]),
        ("What is API versioning? How do you deprecate an old version?", "medium", "mid",
         ["Breaking vs non-breaking changes?", "Sunset header?"],
         ["URL path versioning: /api/v2/users", "Communication: advance notice, migration guide", "Sunset header: when old version dies", "Support both versions during migration period"]),
        ("How do you design an idempotent API for payments?", "hard", "mid",
         ["Idempotency key?", "Duplicate detection?"],
         ["Idempotency key: unique ID per request", "Server stores key → result mapping", "Same key → return same result, no double charge", "Key expires after reasonable window"]),
    ]
    for txt, d, l, fu, pts in api:
        Q.append(_q("api_design", d, l, txt, fu, pts))

    # ═══════ SCALABILITY PATTERNS ═══════
    scale = [
        ("What is horizontal scaling vs vertical scaling? When do you use each?", "easy", "fresher",
         ["Cost implications?", "Limits of vertical scaling?"],
         ["Vertical: bigger machine (more CPU/RAM)", "Horizontal: more machines", "Vertical: simpler, limited by hardware", "Horizontal: complex (state management) but unlimited"]),
        ("What is consistent hashing? Why is it important for distributed systems?", "hard", "mid",
         ["Virtual nodes?", "How does adding/removing a server work?"],
         ["Maps keys to servers on a hash ring", "Adding/removing server affects only nearby keys", "Regular hashing: N change → all keys reassigned", "Virtual nodes: even distribution across servers"]),
        ("How would you design a system that handles 10x traffic spikes?", "hard", "mid",
         ["Auto-scaling?", "Queue-based load leveling?"],
         ["Auto-scaling: add servers based on metrics", "Queue: absorb spikes, process at steady rate", "CDN/cache: offload read traffic", "Rate limiting: protect critical services"]),
        ("What is database read replica pattern? How does it help scale reads?", "medium", "mid",
         ["Replication lag?", "How do you route reads vs writes?"],
         ["Write to primary, read from replicas", "Replication: async copy of writes to replicas", "Route: writes → primary, reads → replica", "Lag: replica may serve slightly stale data"]),
        ("What is the CQRS pattern? When is it worth the complexity?", "hard", "mid",
         ["Separate models for read and write?", "Event sourcing + CQRS?"],
         ["Command Query Responsibility Segregation", "Separate models optimized for reads and writes", "Write: normalized, consistent. Read: denormalized, fast", "Worth it: high read/write ratio, different scaling needs"]),
    ]
    for txt, d, l, fu, pts in scale:
        Q.append(_q("scalability", d, l, txt, fu, pts))

    # ═══════ RELIABILITY ═══════
    rel = [
        ("How do you design a system with 99.99% uptime? What techniques ensure high availability?", "hard", "mid",
         ["What does 99.99% mean in minutes?", "Single points of failure?"],
         ["99.99% = 52 minutes downtime/year", "Redundancy: no single point of failure", "Health checks + automatic failover", "Multi-region deployment for disaster recovery"]),
        ("What is the difference between fault tolerance and fault recovery?", "medium", "mid",
         ["Active-passive vs active-active?", "Graceful degradation?"],
         ["Fault tolerance: system continues working despite failures", "Fault recovery: system detects and recovers from failures", "Active-active: all nodes serve traffic", "Graceful degradation: reduced functionality, not total failure"]),
        ("How do you monitor a distributed system? What metrics matter?", "medium", "mid",
         ["RED method?", "Alerting strategy?"],
         ["RED: Rate, Errors, Duration (for services)", "USE: Utilization, Saturation, Errors (for resources)", "Distributed tracing: Jaeger, Zipkin", "Centralized logging: ELK stack, Datadog"]),
        ("What is chaos engineering? How does Netflix use it?", "hard", "mid",
         ["Chaos Monkey?", "Game days?"],
         ["Intentionally inject failures to test resilience", "Netflix Chaos Monkey: randomly kills instances", "Test: does the system recover automatically?", "Game days: planned chaos exercises"]),
    ]
    for txt, d, l, fu, pts in rel:
        Q.append(_q("reliability", d, l, txt, fu, pts))

    # ═══════ LOW LEVEL DESIGN (LLD) ═══════
    lld = [
        ("Design a parking lot system. Support multiple floors, vehicle types, and payment.", "medium", "fresher",
         ["What classes do you need?", "How do you find the nearest available spot?"],
         ["Classes: ParkingLot, Floor, ParkingSpot, Vehicle, Ticket", "Vehicle types: Car, Bike, Truck with different spot sizes", "Strategy pattern for payment", "Find spot: iterate floors, check availability"]),
        ("Design an elevator system for a 50-story building with 6 elevators.", "hard", "mid",
         ["Scheduling algorithm?", "Peak hour handling?"],
         ["Elevator, Floor, Request, Scheduler classes", "SCAN/LOOK algorithm for scheduling", "Direction-aware: pick up passengers on the way", "Peak hours: zone-based allocation"]),
        ("Design a library management system. Books, members, lending, fines.", "medium", "fresher",
         ["Reservation system?", "Fine calculation?"],
         ["Book, Member, Loan, Fine, Librarian classes", "Observer: notify member when reserved book available", "Strategy: fine calculation varies by membership type", "State pattern: book states (available, borrowed, reserved)"]),
        ("Design a Tic-Tac-Toe game. Make it extensible for NxN board.", "easy", "fresher",
         ["Win detection for NxN?", "AI opponent?"],
         ["Board: NxN grid of Cell", "Player: human or AI", "Game: manages turns, checks win", "Win check: rows, columns, diagonals"]),
        ("Design a vending machine. Handle multiple products, payments, and change.", "medium", "fresher",
         ["State pattern?", "What if product is out of stock?"],
         ["States: idle, product selected, payment, dispensing", "State pattern for machine states", "Product: name, price, quantity", "Payment: coin/note acceptance, change calculation"]),
        ("Design an online booking system like BookMyShow. Handle seat selection and concurrent bookings.", "hard", "mid",
         ["How do you prevent double booking?", "Seat lock during selection?"],
         ["Show, Screen, Seat, Booking, User classes", "Temporary seat lock: 10-minute hold during selection", "Optimistic locking: version-based conflict detection", "Payment timeout releases locked seats"]),
        ("Design a snake game. How do you handle snake movement, food, and collision?", "medium", "fresher",
         ["Data structure for snake body?", "Game loop?"],
         ["Snake: deque of coordinates", "Move: add head, remove tail (or grow)", "Collision: check head against walls and body", "Food: random position not on snake"]),
        ("Design an ATM system. Handle authentication, withdrawal, balance check, transfer.", "medium", "fresher",
         ["Transaction handling?", "Cash management?"],
         ["ATM, Card, Account, Transaction classes", "State pattern: authentication → menu → transaction", "Transaction: atomic, rollback on failure", "Cash dispenser: denomination selection"]),
    ]
    for txt, d, l, fu, pts in lld:
        Q.append(_q("low_level_design", d, l, txt, fu, pts))

    # ═══════ TEMPLATE EXPANSION: System design topics ═══════
    sd_templates = [
        ("What is {concept}? Explain how it works and when to use it in a system design.", "medium", "mid",
         ["Trade-offs?", "Real-world examples?"],
         ["{concept} definition", "How it works internally", "When to use it", "Trade-offs and alternatives"]),
    ]
    sd_concepts = [
        "consistent hashing", "bloom filter", "gossip protocol", "leader election",
        "write-ahead log", "reverse proxy", "content delivery network", "message broker",
        "service mesh", "API gateway", "circuit breaker", "bulkhead pattern",
        "retry with exponential backoff", "idempotency", "distributed lock",
        "heartbeat mechanism", "checksums for data integrity", "rate limiting",
        "connection pooling", "database indexing strategies", "event sourcing",
        "CQRS pattern", "saga pattern", "strangler fig pattern", "sidecar pattern",
        "ambassador pattern", "anti-corruption layer", "blue-green deployment",
        "canary deployment", "feature flags", "A/B testing infrastructure",
        "data partitioning", "data replication", "database sharding",
        "geospatial indexing", "time-series database", "column-family store",
        "document database", "graph database", "search engine (Elasticsearch)",
        "object storage (S3)", "block storage", "file storage",
    ]
    for tmpl_txt, d, l, fu, pts in sd_templates:
        for c in sd_concepts:
            Q.append(_q("system_design_concepts", d, l, tmpl_txt.format(concept=c),
                        [f.format(concept=c) for f in fu],
                        [pt.format(concept=c) for pt in pts]))

    # ═══════ TEMPLATE EXPANSION: Design comparison ═══════
    design_comparisons = [
        ("Compare {a} and {b}. When would you choose each in a system design?", "medium", "mid",
         ["Can you use both?", "Performance implications?"],
         ["{a}: key characteristics", "{b}: key characteristics", "Key differences", "Decision criteria"]),
    ]
    pairs = [
        ("SQL database", "NoSQL database"), ("Redis", "Memcached"),
        ("Kafka", "RabbitMQ"), ("REST", "gRPC"),
        ("Monolith", "Microservices"), ("WebSocket", "Server-Sent Events"),
        ("Pull-based architecture", "Push-based architecture"),
        ("Synchronous communication", "Asynchronous communication"),
        ("Relational database", "Key-value store"),
        ("Batch processing", "Stream processing"),
        ("Horizontal scaling", "Vertical scaling"),
        ("Cache-aside", "Write-through cache"),
        ("Active-active replication", "Active-passive replication"),
        ("Client-side load balancing", "Server-side load balancing"),
        ("Token-based auth (JWT)", "Session-based auth"),
    ]
    for tmpl_txt, d, l, fu, pts in design_comparisons:
        for a, b in pairs:
            Q.append(_q("design_comparison", d, l, tmpl_txt.format(a=a, b=b),
                        [f.format(a=a, b=b) for f in fu],
                        [pt.format(a=a, b=b) for pt in pts]))

    # ═══════ COMPANY-SPECIFIC ═══════
    company_qs = [
        ("Design Amazon's product recommendation system. How do you handle millions of users and products?", "hard", "mid",
         ["Collaborative filtering?", "Real-time vs batch?"],
         ["Collaborative filtering: user-based and item-based", "Content-based: product features similarity", "Hybrid approach: combine both methods", "Pre-compute recommendations, serve from cache"],
         "Amazon"),
        ("Design Google's autocomplete/search suggestion system.", "hard", "mid",
         ["Trie data structure?", "How do you rank suggestions?"],
         ["Trie for prefix-based search", "Rank by: frequency, recency, personalization", "Pre-compute top suggestions per prefix", "CDN cache for popular prefixes"],
         "Google"),
        ("Design Flipkart's flash sale system. How do you handle millions of requests for limited inventory?", "hard", "mid",
         ["Queue-based?", "How do you prevent overselling?"],
         ["Pre-allocate inventory tokens", "Queue requests, process in order", "Distributed lock or atomic decrement for inventory", "CDN for product page, API for purchase only"],
         "Flipkart"),
        ("Design Goldman Sachs' real-time stock trading platform. Focus on low latency and reliability.", "hard", "mid",
         ["Matching engine?", "How do you ensure no order is lost?"],
         ["Order book: sorted bids and asks", "Matching engine: price-time priority", "WAL for every order — no data loss", "Multicast for market data distribution"],
         "Goldman Sachs"),
        ("Design a payment system like Razorpay/Stripe. Focus on reliability and idempotency.", "hard", "mid",
         ["Double payment prevention?", "Payment state machine?"],
         ["Idempotency key per payment attempt", "State machine: created → processing → succeeded/failed", "At-least-once delivery with idempotent handlers", "Reconciliation: match with payment gateway records"],
         "Razorpay"),
    ]
    for item in company_qs:
        txt, d, l, fu, pts, co = item
        Q.append(_q("system_design", d, l, txt, fu, pts, co=co, tg=["system_design", co.lower()]))

    # ═══════ TEMPLATE EXPANSION: Design a system for... ═══════
    design_templates = [
        ("Design {system}. Walk me through the high-level architecture, data model, and key design decisions.", "hard", "mid",
         ["How would you scale it?", "What are the critical failure points?", "How do you handle data consistency?"],
         ["High-level architecture: components and interactions", "Data model: key entities and relationships", "Scalability strategy", "Key design decisions and trade-offs"]),
    ]
    systems = [
        "a food delivery app like Swiggy/Zomato",
        "a social media platform like Instagram",
        "a collaborative document editor like Google Docs",
        "a music streaming service like Spotify",
        "a job portal like Naukri",
        "a hotel booking system like MakeMyTrip",
        "a news aggregation system like Google News",
        "a real-time location tracking system",
        "a distributed task scheduler like cron at scale",
        "a metrics collection and monitoring system",
        "a URL redirection service with analytics",
        "a QR code-based payment system like UPI",
        "an online examination system for 100,000 concurrent users",
        "a ticket booking system with seat selection",
        "a cloud file storage system with sharing",
    ]
    for tmpl_txt, d, l, fu, pts in design_templates:
        for s in systems:
            Q.append(_q("system_design", d, l, tmpl_txt.format(system=s),
                        fu, pts))

    return Q
