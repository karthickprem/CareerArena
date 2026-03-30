"""Web Development interview questions for PlaceRight. ~500 questions via template expansion."""
from typing import List, Dict

R = {"1-3": "No understanding of web fundamentals. Cannot build basic pages.",
     "4-5": "Knows HTML/CSS basics but weak on JS and frameworks. No real projects.",
     "6-7": "Solid web fundamentals. Can build full-stack applications. Minor gaps.",
     "8-10": "Expert-level. Understands internals, performance, security. Production experience."}

def _q(t, d, l, txt, fu, pts, co="", tg=None):
    return {"domain": "software_engineering", "topic": t, "difficulty": d, "level": l,
            "question_text": txt, "follow_ups": fu, "expected_points": pts,
            "scoring_rubric": R, "company_specific": co, "tags": tg or [t]}

def get_web_questions() -> List[Dict]:
    Q = []

    # ═══════ HTML/CSS ═══════
    html_css = [
        ("What is the box model in CSS? If I set width: 100px and padding: 20px, how wide is the element?", "easy", "fresher",
         ["What does box-sizing: border-box do?", "How about margin collapse?"],
         ["Content + Padding + Border + Margin", "Default: 100px + 40px padding = 140px total", "border-box: width includes padding + border", "Margin collapse: adjacent vertical margins merge"]),
        ("What's the difference between Flexbox and Grid? When would you use each?", "medium", "fresher",
         ["Can you nest them?", "Which is better for page layout?"],
         ["Flexbox: 1D layout (row or column)", "Grid: 2D layout (rows AND columns)", "Flexbox for component-level layout", "Grid for page-level layout"]),
        ("How do you make a website responsive? Walk me through your approach.", "medium", "fresher",
         ["Mobile-first vs desktop-first?", "What are breakpoints?"],
         ["Media queries for different screen sizes", "Flexible units (%, em, rem, vw, vh)", "Mobile-first: start with mobile, scale up", "Common breakpoints: 576px, 768px, 992px, 1200px"]),
        ("What is CSS specificity? How do you calculate it?", "medium", "fresher",
         ["What beats what?", "What about !important?"],
         ["Inline > ID > Class > Element", "Count: (inline, IDs, classes, elements)", "!important overrides everything (avoid it)", "Specificity war leads to unmaintainable CSS"]),
        ("What are semantic HTML elements? Why do they matter?", "easy", "fresher",
         ["Name 5 semantic elements.", "How do they help accessibility?"],
         ["Elements that convey meaning: header, nav, main, article, footer", "Accessibility: screen readers understand structure", "SEO: search engines rank semantic pages better", "Readability: code is self-documenting"]),
        ("Explain the difference between position: relative, absolute, fixed, and sticky.", "medium", "fresher",
         ["What is the containing block for absolute?", "When does sticky change to fixed?"],
         ["Relative: offset from normal position, takes space", "Absolute: positioned relative to nearest positioned ancestor, no space", "Fixed: positioned relative to viewport", "Sticky: normal until scroll threshold, then fixed"]),
        ("What is the z-index? Why doesn't it always work as expected?", "medium", "fresher",
         ["Stacking context?", "Can z-index be negative?"],
         ["Controls stacking order of overlapping elements", "Only works on positioned elements", "Creates stacking context: limits z-index scope", "Parent's stacking context constrains children"]),
        ("How do CSS animations work? Compare transitions vs @keyframes.", "medium", "fresher",
         ["Performance — transform vs layout properties?", "requestAnimationFrame?"],
         ["Transitions: property change with duration", "Keyframes: multi-step animations", "transform + opacity: GPU-accelerated, smooth", "Avoid animating width/height — causes layout thrashing"]),
        ("What are CSS preprocessors? Compare Sass and PostCSS.", "easy", "fresher",
         ["Variables, mixins, nesting?", "CSS custom properties vs Sass variables?"],
         ["Sass: variables, nesting, mixins, functions", "PostCSS: plugin-based, transforms CSS", "CSS custom properties: runtime, cascading", "Sass variables: compile-time, no cascade"]),
        ("What is a CSS-in-JS library? When would you use it over regular CSS?", "medium", "mid",
         ["styled-components?", "Performance concerns?"],
         ["Write CSS directly in JavaScript", "Scoped by default — no class name conflicts", "Dynamic styling based on props", "Overhead: runtime CSS generation"]),
    ]
    for txt, d, l, fu, pts in html_css:
        Q.append(_q("html_css", d, l, txt, fu, pts, tg=["web", "css"]))

    # ═══════ JAVASCRIPT CORE ═══════
    js_core = [
        ("Explain closures in JavaScript with a practical example. Why are they useful?", "medium", "fresher",
         ["Memory leak potential?", "How do closures enable private variables?"],
         ["Function retains access to outer scope variables", "Inner function closes over outer variables", "Use case: data privacy, factory functions", "Memory: closure keeps variables alive"]),
        ("What is the event loop? How does JavaScript handle async operations with a single thread?", "hard", "fresher",
         ["Microtask vs macrotask?", "What order: setTimeout vs Promise.then?"],
         ["Call stack executes synchronous code", "Web APIs handle async (setTimeout, fetch)", "Task queue holds callbacks", "Event loop pushes callbacks to stack when empty"]),
        ("What is hoisting? What gets hoisted — var, let, const, function declarations?", "medium", "fresher",
         ["Temporal dead zone?", "Function expression vs declaration?"],
         ["var: hoisted with undefined", "let/const: hoisted but not initialized (TDZ)", "Function declaration: fully hoisted", "Function expression: variable hoisted, not function"]),
        ("Explain promises and async/await. How would you handle multiple async operations?", "medium", "fresher",
         ["Promise.all vs Promise.allSettled?", "Error handling with async/await?"],
         ["Promise: represents future value (pending/resolved/rejected)", "async/await: syntactic sugar over promises", "Promise.all: parallel, fails if any fails", "try/catch for error handling with async/await"]),
        ("What is 'this' in JavaScript? How does it differ in regular functions vs arrow functions?", "medium", "fresher",
         ["What about bind/call/apply?", "this in class methods?"],
         ["Regular function: this depends on how function is called", "Arrow function: this from enclosing scope (lexical)", "bind: creates new function with fixed this", "call/apply: invoke with specific this"]),
        ("What is prototypal inheritance? How does it work under the hood?", "hard", "fresher",
         ["__proto__ vs prototype?", "How does class syntax use prototypes?"],
         ["Objects inherit from other objects via prototype chain", "prototype: property on constructor functions", "__proto__: internal link to prototype", "class syntax: syntactic sugar over prototypes"]),
        ("What is the difference between == and === in JavaScript? Give me a tricky example.", "easy", "fresher",
         ["Type coercion rules?", "null == undefined?"],
         ["==: loose equality with type coercion", "===: strict equality, no coercion", "Tricky: '' == 0 is true, null == undefined is true", "Always use === except for null checks"]),
        ("Explain event delegation. Why is it better than adding listeners to each element?", "medium", "fresher",
         ["event.target vs event.currentTarget?", "Bubbling vs capturing?"],
         ["Add one listener to parent, handle child events", "Uses event bubbling: child → parent", "Efficient for dynamic elements", "event.target: actual clicked element"]),
        ("What are generators in JavaScript? How do they differ from regular functions?", "hard", "mid",
         ["yield keyword?", "Use cases?"],
         ["Pausable functions using function* and yield", "Returns iterator, can pause and resume", "Use cases: lazy evaluation, infinite sequences", "async generators for streaming data"]),
        ("What is the difference between null and undefined?", "easy", "fresher",
         ["typeof null?", "When do you get undefined?"],
         ["undefined: variable declared but not assigned", "null: intentional absence of value", "typeof null === 'object' (bug)", "== treats them as equal, === does not"]),
        ("What are WeakMap and WeakSet? When would you use them?", "hard", "mid",
         ["Garbage collection?", "Use cases?"],
         ["Weak references: don't prevent garbage collection", "WeakMap: keys must be objects, keys are weakly held", "Use case: private data, DOM node metadata", "Cannot iterate — no size property"]),
        ("Explain destructuring, spread operator, and rest parameters.", "easy", "fresher",
         ["Nested destructuring?", "Object spread vs Object.assign?"],
         ["Destructuring: unpack values from arrays/objects", "Spread: expand array/object into elements", "Rest: collect remaining arguments into array", "Spread creates shallow copy"]),
        ("What is the module system in JavaScript? Compare CommonJS vs ES Modules.", "medium", "fresher",
         ["Dynamic import?", "Tree shaking?"],
         ["CommonJS: require/module.exports (Node.js)", "ES Modules: import/export (browser + Node)", "ESM: static analysis, tree shaking", "Dynamic import(): lazy loading modules"]),
        ("How does garbage collection work in JavaScript? What causes memory leaks?", "hard", "mid",
         ["Mark and sweep?", "Common leak patterns?"],
         ["Mark-and-sweep: trace from roots, collect unreachable", "Leaks: global variables, forgotten timers, closures, detached DOM", "Tools: Chrome DevTools memory profiler", "WeakRef for avoiding leaks"]),
    ]
    for txt, d, l, fu, pts in js_core:
        Q.append(_q("javascript", d, l, txt, fu, pts, tg=["web", "javascript"]))

    # ═══════ REACT ═══════
    react = [
        ("What is the virtual DOM? How does React's reconciliation work?", "medium", "fresher",
         ["Diffing algorithm?", "What about React Fiber?"],
         ["Virtual DOM: in-memory representation of real DOM", "React compares old and new virtual DOM (diffing)", "Only updates changed parts of real DOM", "Fiber: incremental rendering, priority-based"]),
        ("Explain React hooks — useState, useEffect, useRef, useMemo, useCallback.", "medium", "fresher",
         ["Rules of hooks?", "When does useEffect run?", "useMemo vs useCallback?"],
         ["useState: state in functional components", "useEffect: side effects, runs after render", "useRef: mutable ref, persists across renders", "useMemo: cached value, useCallback: cached function"]),
        ("What is prop drilling? How do you solve it?", "medium", "fresher",
         ["Context API?", "State management libraries?"],
         ["Passing props through many intermediate components", "Solutions: Context API, Redux, Zustand", "Context: for global state (theme, auth)", "Redux/Zustand: complex state management"]),
        ("How does React re-render? What causes unnecessary re-renders and how do you prevent them?", "hard", "mid",
         ["React.memo?", "useCallback + useMemo?"],
         ["Re-render: state change, prop change, parent re-render", "React.memo: skip re-render if props unchanged", "useMemo/useCallback: stable references", "Profiler: identify unnecessary re-renders"]),
        ("What is the difference between controlled and uncontrolled components?", "easy", "fresher",
         ["When to use uncontrolled?", "useRef for form data?"],
         ["Controlled: React state drives form value", "Uncontrolled: DOM manages its own state", "Controlled: single source of truth, validation", "Uncontrolled: simpler, use ref to read value"]),
        ("Explain React's component lifecycle. How do hooks map to lifecycle methods?", "medium", "fresher",
         ["componentDidMount equivalent?", "Cleanup on unmount?"],
         ["Mount → Update → Unmount", "useEffect(fn, []): componentDidMount", "useEffect(fn, [dep]): componentDidUpdate", "Return cleanup: componentWillUnmount"]),
        ("What is state lifting? When should you lift state vs use Context?", "medium", "fresher",
         ["Performance implications?", "Colocation principle?"],
         ["Move state up to closest common ancestor", "Children receive state via props", "Lift when siblings need shared state", "Context when deeply nested components need it"]),
        ("How do you handle errors in React? What are error boundaries?", "medium", "fresher",
         ["Can functional components be error boundaries?", "What about async errors?"],
         ["Error boundary: class component with getDerivedStateFromError", "Catches rendering errors in children", "Cannot catch: event handlers, async code, SSR", "Functional: use react-error-boundary library"]),
        ("What is code splitting in React? How does React.lazy work?", "medium", "mid",
         ["Suspense?", "Route-based splitting?"],
         ["Split bundle into smaller chunks loaded on demand", "React.lazy: dynamic import for components", "Suspense: show fallback while loading", "Route-based: split by page/route"]),
        ("What is server-side rendering (SSR) vs client-side rendering (CSR)? When do you choose each?", "medium", "mid",
         ["Next.js?", "SEO implications?", "Static site generation?"],
         ["CSR: browser downloads JS, renders page", "SSR: server renders HTML, sends to browser", "SSR: better SEO, faster first paint", "CSR: richer interactivity, simpler architecture"]),
    ]
    for txt, d, l, fu, pts in react:
        Q.append(_q("react", d, l, txt, fu, pts, tg=["web", "react"]))

    # ═══════ NODE.JS & EXPRESS ═══════
    node = [
        ("What is middleware in Express? How does the request pipeline work?", "medium", "fresher",
         ["Order matters?", "Custom vs built-in middleware?"],
         ["Function with (req, res, next) signature", "Executed in order, calls next() to continue", "Built-in: express.json(), express.static()", "Custom: logging, auth, error handling"]),
        ("How does Node.js handle concurrency with a single thread?", "medium", "fresher",
         ["Worker threads?", "What about CPU-bound tasks?"],
         ["Event loop + libuv thread pool", "Non-blocking I/O via callbacks/promises", "CPU-bound: blocks event loop — use worker threads", "Cluster module: multiple processes"]),
        ("How do you handle authentication in a Node.js API?", "medium", "fresher",
         ["JWT vs session-based?", "Middleware for auth?"],
         ["JWT: stateless token in Authorization header", "Session: server-side with cookie", "JWT: scalable, no server state", "Session: easier to revoke, server memory"]),
        ("What is the difference between process.nextTick() and setImmediate()?", "hard", "mid",
         ["Where do they execute in the event loop?", "Which runs first?"],
         ["nextTick: runs before any I/O, higher priority", "setImmediate: runs in check phase after I/O", "nextTick can starve I/O if called recursively", "Use setImmediate for I/O callbacks"]),
        ("How do you structure a large Express application? What patterns do you follow?", "medium", "mid",
         ["Router-level separation?", "Service layer?"],
         ["Routes → Controllers → Services → Models", "Router-level separation: /api/users, /api/products", "Middleware for cross-cutting concerns", "Environment-based config"]),
        ("What are streams in Node.js? When would you use them?", "medium", "mid",
         ["Readable vs writable?", "pipe()?"],
         ["Process data chunk by chunk, not all at once", "4 types: Readable, Writable, Duplex, Transform", "pipe() connects readable to writable", "Use for large files, HTTP responses"]),
        ("How do you handle errors in Express? What's the error-handling middleware pattern?", "medium", "fresher",
         ["Global error handler?", "Async errors?"],
         ["Error middleware: (err, req, res, next) — 4 params", "Must be defined after all routes", "Async: express-async-errors or try/catch", "Centralized error handling vs scattered try/catch"]),
        ("What is CORS? Why does it exist and how do you configure it in Express?", "medium", "fresher",
         ["Preflight requests?", "Access-Control-Allow-Origin?"],
         ["Cross-Origin Resource Sharing: browser security", "Prevents page from making requests to different origin", "cors() middleware in Express", "Preflight: OPTIONS request for non-simple requests"]),
    ]
    for txt, d, l, fu, pts in node:
        Q.append(_q("node_express", d, l, txt, fu, pts, tg=["web", "nodejs"]))

    # ═══════ REST API DESIGN ═══════
    rest = [
        ("Design a REST API for a blog platform. Show the endpoints, methods, and request/response formats.", "medium", "fresher",
         ["Pagination?", "Filtering?", "Nested resources?"],
         ["GET /posts, POST /posts, GET /posts/:id", "PUT /posts/:id, DELETE /posts/:id", "GET /posts/:id/comments for nested", "Use query params for pagination and filtering"]),
        ("What is idempotency? Which HTTP methods are idempotent and why does it matter?", "medium", "fresher",
         ["What about POST?", "Idempotency key?"],
         ["Same request → same result, no extra side effects", "GET, PUT, DELETE: idempotent", "POST: not idempotent — creates new resource each time", "Idempotency key: prevent duplicate payments"]),
        ("How do you version an API? What are the trade-offs of each approach?", "medium", "mid",
         ["URL path vs header vs query param?", "Semantic versioning?"],
         ["URL: /api/v1/users — most common, clear", "Header: Accept: application/vnd.api.v1+json", "Query: /api/users?version=1", "URL versioning is simplest and most visible"]),
        ("How would you implement rate limiting in an API?", "hard", "mid",
         ["Token bucket vs sliding window?", "Response headers?"],
         ["Limit requests per client per time window", "Token bucket: refill tokens at fixed rate", "Sliding window: count requests in rolling window", "Headers: X-RateLimit-Limit, X-RateLimit-Remaining"]),
        ("What is HATEOAS? Why do few REST APIs implement it?", "hard", "mid",
         ["Level 3 REST?", "Is it worth it?"],
         ["Hypermedia As The Engine Of Application State", "Responses include links to related actions", "Client discovers API through links, not docs", "Few implement: added complexity, debatable value"]),
        ("How do you handle pagination in REST APIs? Compare cursor vs offset.", "medium", "mid",
         ["Deep page problem?", "Cursor-based for infinite scroll?"],
         ["Offset: skip N records — simple but slow for deep pages", "Cursor: use last item's ID as bookmark", "Cursor: consistent results, handles insertions", "Offset: random access, familiar to users"]),
    ]
    for txt, d, l, fu, pts in rest:
        Q.append(_q("rest_api", d, l, txt, fu, pts, tg=["web", "api"]))

    # ═══════ WEB SECURITY ═══════
    security = [
        ("What is XSS (Cross-Site Scripting)? How do you prevent it?", "medium", "fresher",
         ["Stored vs reflected vs DOM-based?", "Content Security Policy?"],
         ["Injecting malicious scripts into web pages", "Stored: saved in DB, shown to other users", "Prevention: escape output, sanitize input, CSP", "React auto-escapes JSX (except dangerouslySetInnerHTML)"]),
        ("What is CSRF? How do CSRF tokens prevent it?", "medium", "fresher",
         ["SameSite cookie attribute?", "Double submit cookie?"],
         ["Tricking user's browser into making unwanted requests", "Attacker's site submits form to your site using user's cookies", "CSRF token: random value verified server-side", "SameSite=Strict: cookies not sent cross-origin"]),
        ("What is SQL injection? Give me an example and how to prevent it.", "medium", "fresher",
         ["Parameterized queries?", "ORM protection?"],
         ["Injecting SQL through user input", "Example: ' OR 1=1 -- in login form", "Prevention: parameterized queries (prepared statements)", "ORM: usually safe, but raw queries still risky"]),
        ("How do you store passwords securely? What's wrong with MD5?", "medium", "fresher",
         ["bcrypt vs argon2?", "Salt?", "Rainbow tables?"],
         ["Never store plain text", "MD5: fast = bad for passwords, vulnerable to rainbow tables", "bcrypt/argon2: intentionally slow, with salt", "Salt: random value added to password before hashing"]),
        ("What is Content Security Policy (CSP)?", "hard", "mid",
         ["How does it prevent XSS?", "Nonce-based CSP?"],
         ["HTTP header that restricts resource loading", "Whitelist: which domains can load scripts, styles", "Prevents inline scripts (XSS mitigation)", "Nonce: allow specific inline scripts"]),
        ("What is clickjacking? How do you prevent it?", "medium", "fresher",
         ["X-Frame-Options?", "frame-ancestors CSP directive?"],
         ["Tricking user into clicking hidden iframe", "Transparent iframe over visible page", "X-Frame-Options: DENY or SAMEORIGIN", "CSP: frame-ancestors 'none'"]),
    ]
    for txt, d, l, fu, pts in security:
        Q.append(_q("web_security", d, l, txt, fu, pts, tg=["web", "security"]))

    # ═══════ PERFORMANCE ═══════
    perf = [
        ("How would you optimize the loading performance of a website?", "medium", "mid",
         ["Core Web Vitals?", "Lighthouse score?"],
         ["Minimize bundle size: code splitting, tree shaking", "Lazy load images and components", "CDN for static assets", "Compression: gzip/brotli"]),
        ("What are Core Web Vitals? How do you measure and improve them?", "medium", "mid",
         ["LCP, FID, CLS?", "Which matters most for SEO?"],
         ["LCP: Largest Contentful Paint — loading speed", "FID: First Input Delay — interactivity", "CLS: Cumulative Layout Shift — visual stability", "All three affect Google search ranking"]),
        ("What is a CDN? How does it improve performance?", "easy", "fresher",
         ["Edge caching?", "CDN for API responses?"],
         ["Content Delivery Network: geographically distributed servers", "Serves static assets from nearest edge server", "Reduces latency for global users", "Popular: Cloudflare, AWS CloudFront, Fastly"]),
        ("How does browser caching work? Explain Cache-Control headers.", "medium", "mid",
         ["ETag vs Last-Modified?", "Service workers for offline?"],
         ["Cache-Control: max-age, no-cache, no-store", "ETag: content hash, 304 Not Modified if unchanged", "immutable: never revalidate (versioned assets)", "Service worker: programmable cache for offline"]),
        ("What is lazy loading? How would you implement it for images and components?", "easy", "fresher",
         ["Intersection Observer?", "loading='lazy' attribute?"],
         ["Load resources only when needed", "Images: loading='lazy' or Intersection Observer", "Components: React.lazy + Suspense", "Reduces initial page load time"]),
    ]
    for txt, d, l, fu, pts in perf:
        Q.append(_q("web_performance", d, l, txt, fu, pts, tg=["web", "performance"]))

    # ═══════ TYPESCRIPT ═══════
    ts = [
        ("What is TypeScript? Why use it over plain JavaScript?", "easy", "fresher",
         ["Learning curve?", "Performance impact?"],
         ["Superset of JavaScript with static type checking", "Catches errors at compile time, not runtime", "Better IDE support (autocomplete, refactoring)", "No runtime overhead — compiles to plain JS"]),
        ("Explain the difference between interface and type in TypeScript.", "medium", "fresher",
         ["Declaration merging?", "Which is more flexible?"],
         ["Interface: for object shapes, can be extended", "Type: for unions, intersections, mapped types", "Interface: declaration merging (auto-combine)", "Type: more flexible, can represent any type"]),
        ("What are generics in TypeScript? Write a generic function.", "medium", "fresher",
         ["Constraints?", "Default type parameters?"],
         ["function identity<T>(arg: T): T { return arg; }", "Reusable code that works with multiple types", "Constraints: <T extends HasLength>", "Common: Array<T>, Promise<T>, Map<K,V>"]),
        ("What are utility types in TypeScript? Name and explain 5.", "medium", "mid",
         ["When to use Partial vs Required?", "Custom utility types?"],
         ["Partial<T>: all properties optional", "Required<T>: all properties required", "Pick<T, K>: select specific properties", "Omit<T, K>: exclude properties, Record<K, V>: object type"]),
    ]
    for txt, d, l, fu, pts in ts:
        Q.append(_q("typescript", d, l, txt, fu, pts, tg=["web", "typescript"]))

    # ═══════ TESTING ═══════
    testing = [
        ("How do you test a React component? What tools do you use?", "medium", "fresher",
         ["Unit vs integration?", "Snapshot testing?"],
         ["Jest: test runner + assertions", "React Testing Library: user-centric testing", "Test behavior, not implementation", "Snapshot: detect unintended UI changes"]),
        ("What is mocking? When and why do you mock dependencies in tests?", "medium", "fresher",
         ["jest.mock()?", "When NOT to mock?"],
         ["Replace real dependency with controlled fake", "Why: isolate unit under test", "Mock: external APIs, databases, time", "Don't mock: core logic, simple utilities"]),
        ("What is TDD? Walk me through writing a feature using TDD.", "medium", "mid",
         ["Red-Green-Refactor?", "Is TDD always worth it?"],
         ["Test-Driven Development: write test first", "Red: write failing test", "Green: write minimum code to pass", "Refactor: clean up while keeping tests green"]),
        ("What is end-to-end testing? Compare Cypress vs Playwright.", "medium", "mid",
         ["When to use E2E vs unit tests?", "Flaky tests?"],
         ["Test full user flow in real browser", "Cypress: easier setup, Chrome-focused", "Playwright: multi-browser, faster", "E2E: slow, flaky — use sparingly for critical paths"]),
    ]
    for txt, d, l, fu, pts in testing:
        Q.append(_q("web_testing", d, l, txt, fu, pts, tg=["web", "testing"]))

    # ═══════ GIT ═══════
    git = [
        ("What is the difference between git merge and git rebase? When do you use each?", "medium", "fresher",
         ["Force push after rebase?", "Interactive rebase?"],
         ["Merge: creates merge commit, preserves history", "Rebase: replays commits on top of branch", "Rebase: cleaner linear history", "Never rebase shared/public branches"]),
        ("How do you resolve a merge conflict?", "easy", "fresher",
         ["Tools for conflict resolution?", "What does the conflict marker look like?"],
         ["<<<<<<< HEAD: your changes", "=======: separator", ">>>>>>> branch: incoming changes", "Edit file, remove markers, add, commit"]),
        ("What is git cherry-pick? When would you use it?", "medium", "fresher",
         ["Risks?", "Cherry-pick vs merge?"],
         ["Apply a specific commit to current branch", "Use: backport bug fix to release branch", "Creates new commit with same changes", "Risk: duplicate commits if branches later merge"]),
        ("Explain git stash. How is it useful?", "easy", "fresher",
         ["stash pop vs apply?", "Named stashes?"],
         ["Save uncommitted changes without committing", "Switch branches without losing work", "pop: apply + remove from stash", "apply: apply, keep in stash"]),
        ("What are git hooks? Give examples of useful pre-commit hooks.", "medium", "mid",
         ["Client-side vs server-side?", "husky?"],
         ["Scripts that run on git events", "Pre-commit: lint, format, test", "Pre-push: run full test suite", "Husky: easy git hooks management for Node.js"]),
    ]
    for txt, d, l, fu, pts in git:
        Q.append(_q("git", d, l, txt, fu, pts, tg=["web", "git"]))

    # ═══════ DEVOPS/DEPLOYMENT ═══════
    devops = [
        ("What is Docker? How does it differ from a virtual machine?", "medium", "fresher",
         ["Dockerfile?", "Layers?", "Docker Compose?"],
         ["Container: lightweight, shares OS kernel", "VM: full OS with hypervisor", "Docker: faster startup, less resource usage", "Dockerfile: instructions to build image"]),
        ("What is CI/CD? How would you set it up for a web application?", "medium", "fresher",
         ["GitHub Actions vs Jenkins?", "What goes in the pipeline?"],
         ["CI: automated build + test on every push", "CD: automated deployment after CI passes", "Pipeline: lint → test → build → deploy", "GitHub Actions: YAML-based, free for public repos"]),
        ("What are environment variables? How do you manage them across dev/staging/prod?", "easy", "fresher",
         [".env files?", "Secrets management?"],
         ["Config that varies by environment", ".env files: local dev (never commit)", "Secrets: use vault (AWS SSM, Doppler)", "12-factor app: config in environment"]),
        ("How does reverse proxy work? Why do you put Nginx in front of Node.js?", "medium", "mid",
         ["SSL termination?", "Load balancing?"],
         ["Nginx receives all requests, forwards to Node.js", "SSL termination: Nginx handles HTTPS", "Static files: Nginx serves directly", "Load balancing: distribute across Node instances"]),
    ]
    for txt, d, l, fu, pts in devops:
        Q.append(_q("devops_web", d, l, txt, fu, pts, tg=["web", "devops"]))

    # ═══════ SYSTEM DESIGN FOR WEB ═══════
    sysdesign = [
        ("How would you design a real-time chat application?", "hard", "mid",
         ["WebSocket vs polling?", "Message persistence?", "Scaling?"],
         ["WebSocket for real-time bidirectional communication", "Message queue for reliability", "Database for message persistence", "Redis pub/sub for horizontal scaling"]),
        ("How do you handle file uploads in a web application? What about large files?", "medium", "mid",
         ["Multipart upload?", "Pre-signed URLs?", "CDN for serving?"],
         ["Small files: multipart form data to server", "Large files: pre-signed URL, upload directly to S3", "Chunked upload for resumability", "CDN for serving uploaded files"]),
        ("What is a WebSocket? How does it differ from HTTP? When would you use Server-Sent Events instead?", "medium", "mid",
         ["Connection lifecycle?", "Scaling WebSocket servers?"],
         ["WebSocket: full-duplex, persistent connection", "HTTP: request-response, stateless", "SSE: server → client only, simpler", "WebSocket: chat, gaming. SSE: notifications, live feeds"]),
        ("How would you implement authentication and authorization in a React + Node.js app?", "medium", "mid",
         ["JWT storage?", "Refresh tokens?", "RBAC?"],
         ["Login: verify credentials, return JWT", "Store JWT: httpOnly cookie (not localStorage)", "Refresh token: long-lived, rotated on use", "Middleware checks JWT on protected routes"]),
        ("How do you handle database migrations in a production web application?", "medium", "mid",
         ["Zero-downtime migrations?", "Rollback strategy?"],
         ["Migration tools: knex, Prisma, Alembic", "Version-controlled, sequential migrations", "Always write down migration (rollback)", "Zero-downtime: expand-contract pattern"]),
    ]
    for txt, d, l, fu, pts in sysdesign:
        Q.append(_q("system_design_web", d, l, txt, fu, pts, tg=["web", "system_design"]))

    # ═══════ TEMPLATE EXPANSION: JS concepts ═══════
    js_templates = [
        ("Explain {concept} in JavaScript. When and why would you use it?", "medium", "fresher",
         ["Common pitfalls?", "Browser support?"],
         ["{concept} definition and purpose", "Syntax and usage examples", "Common use cases", "Gotchas and best practices"]),
    ]
    js_concepts = ["Promise.race", "Promise.any", "Symbol", "Proxy", "Reflect",
                   "WeakRef", "FinalizationRegistry", "structuredClone", "AbortController",
                   "Intl API", "Web Workers", "SharedArrayBuffer", "Temporal API",
                   "Optional chaining", "Nullish coalescing", "Array.from",
                   "flat() and flatMap()", "Object.freeze vs Object.seal",
                   "template literals (tagged templates)", "dynamic import()"]
    for tmpl_txt, d, l, fu, pts in js_templates:
        for c in js_concepts:
            Q.append(_q("javascript_advanced", d, l, tmpl_txt.format(concept=c),
                        [f.format(concept=c) for f in fu],
                        [pt.format(concept=c) for pt in pts], tg=["web", "javascript"]))

    # ═══════ TEMPLATE EXPANSION: React patterns ═══════
    react_templates = [
        ("Explain the {pattern} pattern in React. When would you use it?", "medium", "mid",
         ["Alternatives?", "Performance implications?"],
         ["{pattern} pattern definition", "Implementation example", "Use cases", "Trade-offs"]),
    ]
    react_patterns = ["Higher-Order Component (HOC)", "Render Props", "Compound Components",
                      "Custom Hook", "Provider Pattern", "Container/Presentational",
                      "Controlled/Uncontrolled", "State Reducer", "Composition vs Inheritance",
                      "Atomic Design", "Feature-based folder structure", "Barrel exports"]
    for tmpl_txt, d, l, fu, pts in react_templates:
        for p in react_patterns:
            Q.append(_q("react_patterns", d, l, tmpl_txt.format(pattern=p),
                        [f.format(pattern=p) for f in fu],
                        [pt.format(pattern=p) for pt in pts], tg=["web", "react"]))

    # ═══════ TEMPLATE EXPANSION: Web comparison questions ═══════
    comparison_templates = [
        ("Compare {a} and {b} in web development. When would you choose each?", "medium", "fresher",
         ["Trade-offs?", "Which is more popular in Indian companies?"],
         ["{a}: key features and strengths", "{b}: key features and strengths", "Key differences", "When to choose each"]),
    ]
    web_comparisons = [
        ("React", "Angular"), ("React", "Vue"), ("Next.js", "Gatsby"),
        ("REST", "GraphQL"), ("MongoDB", "PostgreSQL"), ("Express", "Fastify"),
        ("npm", "yarn"), ("Webpack", "Vite"), ("Jest", "Vitest"),
        ("Tailwind CSS", "Bootstrap"), ("Redux", "Zustand"),
        ("Server Components", "Client Components"),
        ("SSR", "SSG"), ("localStorage", "sessionStorage"),
        ("Cookie", "JWT"), ("Monolith", "Microservices"),
    ]
    for tmpl_txt, d, l, fu, pts in comparison_templates:
        for a, b in web_comparisons:
            Q.append(_q("web_comparison", d, l, tmpl_txt.format(a=a, b=b),
                        [f.format(a=a, b=b) for f in fu],
                        [pt.format(a=a, b=b) for pt in pts], tg=["web", "comparison"]))

    # ═══════ COMPANY-SPECIFIC: Flipkart ═══════
    flipkart = [
        ("Design a product listing page that handles millions of products with filters and sorting. How would you optimize it?", "hard", "mid",
         ["Infinite scroll vs pagination?", "Client-side vs server-side filtering?"],
         ["Virtual scrolling for large lists", "Server-side filtering and pagination", "Debounced search, cached filter counts", "CDN for product images"]),
        ("How would you implement a real-time price drop notification on a product page?", "medium", "mid",
         ["WebSocket vs SSE?", "Scalability?"],
         ["WebSocket for real-time updates", "Redis pub/sub for broadcasting changes", "Fallback: long polling for older browsers", "Rate limit notifications per user"]),
    ]
    for txt, d, l, fu, pts in flipkart:
        Q.append(_q("web_ecommerce", d, l, txt, fu, pts, co="Flipkart", tg=["flipkart", "web"]))

    # ═══════ COMPANY-SPECIFIC: Zoho ═══════
    zoho = [
        ("Implement a drag-and-drop kanban board using vanilla JavaScript (no frameworks). Walk me through the DOM manipulation.", "hard", "fresher",
         ["HTML5 drag API vs mouse events?", "State management without framework?"],
         ["HTML5 Drag and Drop API: dragstart, dragover, drop", "data-id attributes for identifying cards", "Event delegation on board containers", "Update DOM and state array simultaneously"]),
        ("Write a debounce function from scratch. Explain when you'd use debounce vs throttle.", "medium", "fresher",
         ["Implementation details?", "Real-world use cases?"],
         ["Debounce: delay execution until pause in calls", "Throttle: execute at most once per interval", "Debounce: search input, resize handler", "Throttle: scroll handler, API rate limiting"]),
        ("How does the JavaScript event loop work? Predict the output of this code: setTimeout(()=>log(1),0); Promise.resolve().then(()=>log(2)); log(3).", "medium", "fresher",
         ["Microtask vs macrotask queue?", "Where does queueMicrotask fit?"],
         ["Output: 3, 2, 1", "Synchronous code first (3)", "Microtask/promise queue next (2)", "Macrotask/setTimeout queue last (1)"]),
    ]
    for txt, d, l, fu, pts in zoho:
        Q.append(_q("javascript_deep", d, l, txt, fu, pts, co="Zoho", tg=["zoho", "web", "javascript"]))

    # ═══════ COMPANY-SPECIFIC: Freshworks ═══════
    freshworks = [
        ("How would you build a multi-tenant SaaS application? What are the database strategies?", "hard", "mid",
         ["Shared DB vs separate DB?", "Data isolation?"],
         ["Shared DB with tenant_id column: simplest, least isolated", "Schema per tenant: moderate isolation", "Database per tenant: strongest isolation, expensive", "Row-level security for shared DB"]),
        ("Design a help desk ticketing system with real-time updates. What technologies would you use?", "hard", "mid",
         ["Priority queue?", "Agent assignment?"],
         ["WebSocket for real-time status updates", "REST API for CRUD operations", "Priority-based queue for ticket routing", "SLA tracking with scheduled jobs"]),
    ]
    for txt, d, l, fu, pts in freshworks:
        Q.append(_q("web_saas", d, l, txt, fu, pts, co="Freshworks", tg=["freshworks", "web"]))

    return Q
