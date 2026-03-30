"""OOP & Design Pattern interview questions for PlaceRight. ~500 questions via template expansion."""
from typing import List, Dict

R = {"1-3": "No understanding of OOP concepts. Cannot explain basics.",
     "4-5": "Knows definitions but cannot apply. No real-world examples.",
     "6-7": "Solid grasp of concepts with examples. Minor gaps in advanced topics.",
     "8-10": "Expert understanding. Applies patterns correctly. Discusses trade-offs."}

def _q(t, d, l, txt, fu, pts, co="", tg=None):
    return {"domain": "software_engineering", "topic": t, "difficulty": d, "level": l,
            "question_text": txt, "follow_ups": fu, "expected_points": pts,
            "scoring_rubric": R, "company_specific": co, "tags": tg or [t]}

def get_oop_questions() -> List[Dict]:
    Q = []

    # ═══════ FOUR PILLARS ═══════
    pillars = [
        ("Let's say you have a Payment class and need to support UPI, credit card, and net banking. How would you design this using polymorphism?", "medium", "fresher",
         ["How does runtime polymorphism work here?", "What if we add a new payment method later?", "How does this relate to the Open-Closed principle?"],
         ["Base Payment class with process() method", "Subclasses override process()", "Runtime dispatch via virtual function", "Easy extension without modifying existing code"]),
        ("Can you explain what encapsulation means with a real-world example? Why can't we just make everything public?", "easy", "fresher",
         ["What's the difference between encapsulation and data hiding?", "How do getters/setters help?", "What happens if someone directly modifies internal state?"],
         ["Bundling data + methods together", "Controlled access via access modifiers", "Prevents invalid state", "Example: bank account balance"]),
        ("If I have a Vehicle class and Car inherits from it, what all does Car get from Vehicle? What are the gotchas?", "easy", "fresher",
         ["Can you override a constructor?", "What about private members?", "Does Car inherit static methods?"],
         ["Inherits public/protected members", "Constructors not inherited but called", "Private members exist but not accessible", "Method overriding for specialization"]),
        ("What's the difference between abstraction and encapsulation? Most candidates confuse these — explain with a real example.", "medium", "fresher",
         ["Can you have abstraction without encapsulation?", "How do abstract classes help with abstraction?", "Give me a real-world analogy."],
         ["Abstraction = hiding complexity, showing essentials", "Encapsulation = bundling + access control", "Abstraction is design level, encapsulation is implementation", "ATM example: abstraction hides banking logic"]),
        ("You're building an e-commerce platform. Show me how you'd use all four OOP pillars in the Order module.", "hard", "mid",
         ["How does polymorphism help with different order types?", "Where does abstraction come in?", "How do you ensure encapsulation of payment details?"],
         ["Encapsulation: Order class hides internal state", "Inheritance: RegularOrder, BulkOrder from Order", "Polymorphism: calculateDiscount() varies by type", "Abstraction: OrderProcessor interface"]),
        ("Why do we say 'program to an interface, not an implementation'? Can you give me a scenario where this matters?", "medium", "fresher",
         ["How does this relate to dependency injection?", "What if you're in a hurry — would you skip this?", "How does this help in testing?"],
         ["Loose coupling between components", "Easy to swap implementations", "Enables unit testing with mocks", "Example: database interface — MySQL today, Postgres tomorrow"]),
        ("What is method overloading vs method overriding? Can you overload in Python? What about Java?", "easy", "fresher",
         ["Is overloading compile-time or runtime?", "Can you override a static method?", "What's the @Override annotation for?"],
         ["Overloading: same name, different params (compile-time)", "Overriding: subclass redefines parent method (runtime)", "Python: no true overloading, uses default args", "Java: supports both"]),
        ("Explain the diamond problem in multiple inheritance. How do Python and Java handle it differently?", "hard", "fresher",
         ["What is MRO in Python?", "Why did Java choose interfaces over multiple inheritance?", "Can you still face ambiguity with interfaces?"],
         ["Diamond: D inherits B,C which both inherit A", "Ambiguity in method resolution", "Python: MRO (C3 linearization)", "Java: no multiple class inheritance, uses interfaces"]),
        ("What happens when you do 'Animal a = new Dog()' in Java? Walk me through the memory and method dispatch.", "medium", "fresher",
         ["Where does the object live in memory?", "What if Dog has a method Animal doesn't?", "What about instance variables — which version is used?"],
         ["Object created on heap as Dog", "Reference type is Animal", "Methods: Dog's version called (dynamic dispatch)", "Variables: Animal's version used (no dynamic dispatch for fields)"]),
        ("When should you use composition over inheritance? Give me a scenario where inheritance would be wrong.", "medium", "mid",
         ["How does the Liskov Substitution Principle relate?", "Can you always refactor inheritance to composition?", "What's the performance difference?"],
         ["Inheritance: is-a relationship only", "Composition: has-a, more flexible", "Favor composition when behavior varies independently", "Example: Bird inheriting Flyable — Penguin breaks it"]),
        ("How is polymorphism achieved in C++ vs Java vs Python? What's the role of vtable?", "hard", "mid",
         ["What's early vs late binding?", "How does Python achieve polymorphism without explicit interfaces?", "What's the performance cost of virtual functions?"],
         ["C++: virtual functions, vtable lookup", "Java: all methods virtual by default", "Python: duck typing, no vtable needed", "Vtable: per-class table of function pointers"]),
        ("You have a Shape hierarchy with Circle, Rectangle, Triangle. How do you add area() and perimeter() without modifying existing classes?", "medium", "fresher",
         ["Can you use the Visitor pattern here?", "What if I add a new shape later?", "How does the open-closed principle apply?"],
         ["Define abstract Shape with abstract area()/perimeter()", "Each subclass implements its own formula", "Alternative: Visitor pattern for operations", "Open-closed: new shapes don't change existing code"]),
        ("What's the difference between abstract class and interface? When would you choose one over the other?", "easy", "fresher",
         ["Can abstract class have constructors?", "Can interface have default methods in Java 8+?", "Can a class implement multiple interfaces?"],
         ["Abstract class: partial implementation + state", "Interface: pure contract (pre-Java 8)", "Abstract when sharing code, interface for capability", "Java 8 blurred the line with default methods"]),
        ("If I create an abstract class with all abstract methods, is it the same as an interface?", "medium", "fresher",
         ["What about state/fields?", "What about constructors?", "Multiple inheritance difference?"],
         ["Not the same — abstract class can hold state", "Abstract class has constructors", "Single inheritance limit for abstract classes", "Interface allows multiple implementation"]),
        ("Explain how access modifiers work in Java. What's the difference between private, protected, default, and public?", "easy", "fresher",
         ["Can a subclass access private members of parent?", "What's the use of protected?", "When would you use default/package-private?"],
         ["private: class only", "default: package only", "protected: package + subclasses", "public: everywhere"]),
        ("What's constructor chaining? How does it work with inheritance?", "easy", "fresher",
         ["What happens if parent has no default constructor?", "What's the order of constructor calls?", "How does this() differ from super()?"],
         ["this(): calls another constructor in same class", "super(): calls parent constructor", "Parent constructor always runs first", "Compiler adds super() implicitly if not written"]),
        ("What is a copy constructor? Why doesn't Java provide one by default like C++?", "medium", "fresher",
         ["Shallow vs deep copy?", "How does clone() differ?", "What about immutable objects — do they need copying?"],
         ["Creates new object as copy of existing", "Java: use clone() or manual copy constructor", "Shallow: copies references, deep: copies objects", "Immutable objects don't need copying"]),
        ("If I serialize an object and deserialize it, does the constructor run?", "hard", "mid",
         ["What about final fields?", "What if the parent class isn't serializable?", "How does transient keyword affect this?"],
         ["No — deserialization bypasses constructor", "Uses unsafe allocation", "Parent's no-arg constructor runs if parent not Serializable", "Transient fields get default values"]),
    ]
    for txt, d, l, fu, pts in pillars:
        Q.append(_q("oop_pillars", d, l, txt, fu, pts))

    # ═══════ SOLID PRINCIPLES ═══════
    solid = [
        ("What does the S in SOLID stand for? Can you show me a class that violates it and how you'd fix it?", "medium", "fresher",
         ["What if the class is small — does SRP still apply?", "How do you decide what 'one responsibility' means?"],
         ["Single Responsibility Principle", "One class = one reason to change", "Example: User class handling auth + email + logging", "Split into separate classes"]),
        ("Explain the Open-Closed Principle. How would you add a new discount type to an e-commerce app without modifying existing code?", "medium", "fresher",
         ["Is it always possible to follow OCP?", "How does Strategy pattern help here?"],
         ["Open for extension, closed for modification", "Use interfaces/abstract classes", "Strategy pattern for discount algorithms", "New discount = new class, not modified switch-case"]),
        ("What is the Liskov Substitution Principle? Give me an example where violating it causes a real bug.", "medium", "mid",
         ["Is Square a valid subtype of Rectangle?", "How do you test for LSP violations?"],
         ["Subtype must be substitutable for base type", "Square/Rectangle: setWidth breaks if substituted", "Violations cause unexpected behavior", "Design by contract"]),
        ("What's the Interface Segregation Principle? Show me a fat interface and how you'd split it.", "medium", "fresher",
         ["How many methods is too many?", "What about convenience interfaces?"],
         ["Clients shouldn't depend on methods they don't use", "Split fat interfaces into focused ones", "Example: Worker interface split into Workable, Eatable", "Reduces coupling"]),
        ("Explain Dependency Inversion. How does it help in unit testing?", "medium", "mid",
         ["DI vs DIP — what's the difference?", "How do DI frameworks like Spring use this?"],
         ["High-level shouldn't depend on low-level", "Both depend on abstractions", "Inject dependencies via constructor", "Easy to mock in tests"]),
        ("You're given a class with 3000 lines of code doing user management, payment processing, and email sending. Walk me through how you'd refactor it using SOLID principles.", "hard", "mid",
         ["Where do you start?", "How do you ensure nothing breaks during refactoring?", "What about shared state between these responsibilities?"],
         ["SRP: split into UserService, PaymentService, EmailService", "OCP: use interfaces for extensibility", "DIP: inject dependencies", "Write tests first, then refactor"]),
        ("Can you over-apply SOLID? When does following these principles hurt more than help?", "hard", "mid",
         ["What about small projects?", "Does YAGNI conflict with OCP?"],
         ["Yes — over-engineering is real", "YAGNI vs OCP tension", "Small projects don't need full abstraction", "Pragmatism over dogma"]),
        ("How does SOLID relate to design patterns? Can you name a pattern for each principle?", "hard", "mid",
         ["Is Strategy always the answer for OCP?", "Which principle does Factory pattern address?"],
         ["SRP: Facade pattern", "OCP: Strategy pattern", "LSP: Template Method", "ISP: Adapter pattern", "DIP: Factory/Abstract Factory"]),
    ]
    for txt, d, l, fu, pts in solid:
        Q.append(_q("solid_principles", d, l, txt, fu, pts))

    # ═══════ DESIGN PATTERNS ═══════
    patterns = [
        ("Implement a Singleton in your preferred language. What are the pitfalls most people miss?", "medium", "fresher",
         ["Is Singleton thread-safe?", "How do you test code that uses Singleton?", "Why do some people call it an anti-pattern?"],
         ["Private constructor", "Static instance method", "Thread safety: double-checked locking or enum", "Testing difficulty — hard to mock"]),
        ("When would you use Factory Method vs Abstract Factory? Give me a real scenario for each.", "hard", "mid",
         ["How does Factory differ from simple if-else?", "Can you combine both patterns?"],
         ["Factory Method: single product family", "Abstract Factory: multiple related product families", "Example: UI toolkit — Button/Checkbox per OS", "Decouples client from concrete classes"]),
        ("Explain the Observer pattern. How is it used in event systems like GUI frameworks or pub/sub?", "medium", "fresher",
         ["What are the drawbacks?", "How does it relate to the Publisher-Subscriber pattern?", "Memory leaks with observers?"],
         ["Subject maintains list of observers", "Notify all on state change", "Loose coupling between components", "Drawback: unexpected update cascades"]),
        ("You need to add logging, authentication, and caching to existing API calls without modifying them. Which pattern?", "medium", "fresher",
         ["How is Decorator different from inheritance?", "Can you chain multiple decorators?", "Performance implications?"],
         ["Decorator pattern", "Wraps existing object with new behavior", "Composable — stack multiple decorators", "Alternative: Proxy pattern for access control"]),
        ("What's the Strategy pattern? How would you use it for sorting — sometimes you want speed, sometimes memory efficiency.", "medium", "fresher",
         ["How does Strategy differ from State pattern?", "Can you use lambdas instead of full strategy classes?"],
         ["Define family of algorithms", "Encapsulate each, make interchangeable", "Client selects strategy at runtime", "Example: SortStrategy with QuickSort, MergeSort, HeapSort"]),
        ("Explain the Builder pattern. When is it better than a constructor with many parameters?", "medium", "fresher",
         ["How does it differ from Factory?", "What's the fluent interface approach?", "When is Builder overkill?"],
         ["Separates construction from representation", "Handles complex objects step by step", "Avoids telescoping constructors", "Fluent API: builder.setName().setAge().build()"]),
        ("What is the Adapter pattern? Give me a real-world scenario in your projects.", "easy", "fresher",
         ["Adapter vs Bridge?", "Object adapter vs class adapter?"],
         ["Converts interface of one class to another", "Makes incompatible interfaces work together", "Example: legacy XML API to modern JSON API", "Wrapper pattern"]),
        ("Explain MVC architecture. How do modern frameworks like Spring MVC or Django implement it?", "medium", "fresher",
         ["What's MVVM?", "Where does the business logic go?", "How does MVC relate to separation of concerns?"],
         ["Model: data + business logic", "View: UI presentation", "Controller: handles input, coordinates model/view", "Variants: MVP, MVVM"]),
        ("What's the Proxy pattern? How is it different from Decorator?", "medium", "mid",
         ["Types of proxies?", "How does Spring AOP use proxies?", "Performance proxy vs protection proxy?"],
         ["Controls access to real object", "Same interface as real object", "Types: virtual, protection, remote, caching", "Decorator adds behavior, Proxy controls access"]),
        ("Explain the Template Method pattern. Where have you seen it in frameworks?", "medium", "mid",
         ["How is it different from Strategy?", "What's the Hollywood Principle?"],
         ["Define skeleton of algorithm in base class", "Subclasses override specific steps", "Hollywood: don't call us, we'll call you", "Example: JUnit setUp/tearDown, Spring's JdbcTemplate"]),
        ("What is the Command pattern? How would you use it to implement undo/redo?", "hard", "mid",
         ["How does it enable macro recording?", "Command vs Strategy?"],
         ["Encapsulates request as object", "Supports undo via inverse commands", "Command queue for sequential execution", "Decouples sender from receiver"]),
        ("When would you use the State pattern instead of a bunch of if-else statements?", "medium", "mid",
         ["State vs Strategy?", "How do you handle state transitions?"],
         ["Object changes behavior based on internal state", "Each state is a separate class", "Eliminates complex conditionals", "State transition logic in state objects"]),
        ("Explain the Facade pattern. How does it simplify complex subsystems?", "easy", "fresher",
         ["When is Facade a bad idea?", "Facade vs Adapter?"],
         ["Provides simplified interface to complex subsystem", "Doesn't prevent direct subsystem access", "Reduces coupling for clients", "Example: JDBC DriverManager"]),
        ("What is the Iterator pattern? How do for-each loops use it internally?", "easy", "fresher",
         ["External vs internal iterators?", "How does it work with generators in Python?"],
         ["Sequential access without exposing internals", "hasNext() + next() interface", "Java: Iterable + Iterator", "Python: __iter__ + __next__"]),
        ("Explain the Chain of Responsibility pattern. How do middleware pipelines in Express/Django use it?", "medium", "mid",
         ["What if no handler processes the request?", "How do you order the chain?"],
         ["Request passes through chain of handlers", "Each handler decides to process or pass along", "Decouples sender from receiver", "Example: logging → auth → rate-limit → handler"]),
        ("You need to support exporting data in CSV, JSON, XML, and PDF. Which design pattern would you use and why?", "medium", "fresher",
         ["What if we need to add Excel later?", "How does this follow OCP?"],
         ["Strategy pattern for export algorithms", "Each format is a strategy implementation", "Factory to create appropriate exporter", "Easy to add new formats"]),
    ]
    for txt, d, l, fu, pts in patterns:
        Q.append(_q("design_patterns", d, l, txt, fu, pts))

    # ═══════ CLASSES & OBJECTS ═══════
    classes = [
        ("What happens internally when you create an object using 'new' keyword in Java?", "medium", "fresher",
         ["Where does memory allocation happen?", "When does the constructor run?", "What about static initialization?"],
         ["Memory allocated on heap", "Default values assigned", "Constructor chain executes", "Reference stored on stack"]),
        ("What's the difference between a class and an object? Sounds basic, but explain like I'm a non-programmer.", "easy", "fresher",
         ["Can you have a class without objects?", "What's a class in memory?"],
         ["Class: blueprint/template", "Object: instance of blueprint", "Class defines structure, object holds data", "Analogy: class=recipe, object=actual dish"]),
        ("What are static methods and when should you use them? Can you access instance variables from a static method?", "easy", "fresher",
         ["What about static variables?", "When is static a bad idea?", "How does Singleton use static?"],
         ["Belong to class, not instance", "No access to instance members", "Use for utility/helper methods", "Example: Math.max(), Collections.sort()"]),
        ("Explain the 'this' keyword. How does it differ across Java, Python (self), and JavaScript?", "easy", "fresher",
         ["What about 'this' in arrow functions?", "Can you use this in static context?"],
         ["Reference to current instance", "Java: implicit, Python: explicit self", "JavaScript: dynamic, depends on call context", "Arrow functions: lexical this"]),
        ("What is the difference between shallow copy and deep copy? When does it matter?", "medium", "fresher",
         ["How do you implement deep copy in Java?", "What about Python's copy module?", "When is shallow copy sufficient?"],
         ["Shallow: copies references, not objects", "Deep: recursively copies all objects", "Matters with mutable nested objects", "Java: implement Cloneable or serialization"]),
        ("What are inner classes in Java? When would you use them?", "medium", "fresher",
         ["Static vs non-static inner?", "Anonymous inner classes?", "How do lambdas relate?"],
         ["Member inner class: access outer's members", "Static inner: like top-level but scoped", "Anonymous: inline interface implementation", "Local inner: defined in method"]),
        ("What is method hiding vs method overriding? How do static methods behave with inheritance?", "medium", "fresher",
         ["Can you override a static method?", "What's the output of this code...?"],
         ["Static methods are hidden, not overridden", "Called based on reference type, not object type", "Instance methods: dynamic dispatch", "Static methods: compile-time binding"]),
        ("Explain the final keyword in Java. What happens if I mark a class, method, and variable as final?", "easy", "fresher",
         ["Can you have a final mutable object?", "Final vs immutable?", "Why is String final?"],
         ["Final class: can't extend", "Final method: can't override", "Final variable: can't reassign (not immutable!)", "Final reference can point to mutable object"]),
        ("What is an immutable class? How would you create one?", "medium", "fresher",
         ["Why is String immutable in Java?", "Benefits of immutability?", "Thread safety implications?"],
         ["All fields private final", "No setters", "Return copies of mutable objects", "Benefits: thread-safe, cacheable, hashmap-safe"]),
        ("Explain garbage collection. How does Java decide when to delete an object?", "medium", "fresher",
         ["What's the difference between mark-sweep and generational GC?", "Can you force GC?", "What are memory leaks in Java?"],
         ["No manual deallocation — GC handles it", "Unreachable objects are collected", "Generational: young/old generation", "System.gc() is a suggestion, not command"]),
        ("What is the Object class in Java? What methods does every object have?", "easy", "fresher",
         ["Why should you override equals and hashCode together?", "What does toString() default to?"],
         ["Root of all Java classes", "Methods: equals, hashCode, toString, clone, finalize, getClass", "equals default: reference comparison", "hashCode contract with equals"]),
        ("What is the difference between == and .equals() in Java?", "easy", "fresher",
         ["What about String comparison?", "What about autoboxing with Integer?"],
         ["== compares references (for objects)", "equals() compares content (if overridden)", "String pool makes == work sometimes", "Integer caching: -128 to 127"]),
        ("How does autoboxing work in Java? What are the hidden performance costs?", "medium", "fresher",
         ["What about null unboxing?", "Integer cache range?", "When does autoboxing cause bugs?"],
         ["Auto-conversion between primitives and wrappers", "Integer.valueOf() for boxing", "intValue() for unboxing", "NullPointerException on null unboxing"]),
    ]
    for txt, d, l, fu, pts in classes:
        Q.append(_q("classes_objects", d, l, txt, fu, pts))

    # ═══════ INHERITANCE TYPES ═══════
    inheritance = [
        ("Draw the inheritance hierarchy you'd design for a university management system — Person, Student, Faculty, TA.", "medium", "fresher",
         ["What if a TA is both Student and Faculty?", "How do you handle it in Java vs Python?"],
         ["Person → Student, Faculty", "TA: needs multiple inheritance or interfaces", "Java: TA implements TeachingAssistant interface", "Python: TA(Student, Faculty) with MRO"]),
        ("What is multilevel inheritance? Give me a 3-level example and explain when it becomes a problem.", "easy", "fresher",
         ["How deep is too deep?", "What's the fragile base class problem?"],
         ["A → B → C", "Each level adds specialization", "Too deep: hard to maintain, tightly coupled", "Prefer composition over deep hierarchies"]),
        ("Can you have hierarchical inheritance without code duplication? What if two siblings need the same method?", "medium", "fresher",
         ["Pull up to parent?", "Use a mixin?", "What about utility classes?"],
         ["Hierarchical: one parent, multiple children", "Common behavior: pull up to parent", "Alternative: mixin or utility class", "Avoid: duplicating code in siblings"]),
        ("What's the difference between IS-A and HAS-A relationship? Give me examples of each in your projects.", "easy", "fresher",
         ["Which maps to inheritance vs composition?", "Can IS-A become HAS-A through refactoring?"],
         ["IS-A: inheritance (Dog is-a Animal)", "HAS-A: composition (Car has-a Engine)", "HAS-A is more flexible", "Prefer HAS-A unless clear IS-A"]),
        ("What's hybrid inheritance? Why is it considered dangerous?", "medium", "fresher",
         ["How does C++ handle it?", "Virtual inheritance?"],
         ["Combination of multiple inheritance types", "Can cause diamond problem", "C++: virtual base classes", "Java: avoids via interface-only multiple inheritance"]),
        ("Explain Python's Method Resolution Order (MRO). What is C3 linearization?", "hard", "mid",
         ["Can you predict the MRO for a complex hierarchy?", "What causes MRO errors?"],
         ["Algorithm to determine method lookup order", "C3 linearization: consistent ordering", "Left-to-right depth-first with deduplication", "TypeError if inconsistent hierarchy"]),
    ]
    for txt, d, l, fu, pts in inheritance:
        Q.append(_q("inheritance", d, l, txt, fu, pts))

    # ═══════ INTERFACES & ABSTRACT CLASSES ═══════
    interfaces = [
        ("Your team lead asks you to design a plugin system where third-party developers can add features. Do you use abstract class or interface?", "medium", "mid",
         ["What about default methods?", "How do you ensure backward compatibility?"],
         ["Interface: defines contract for plugins", "Abstract class: if shared base behavior needed", "Default methods for backward compatibility", "Interface enables multiple implementation"]),
        ("What are default methods in Java 8 interfaces? Why were they added?", "medium", "fresher",
         ["Can they cause diamond problem?", "Can you override a default method?"],
         ["Added for backward compatibility", "Existing interfaces can add methods without breaking implementors", "Yes, diamond problem possible — must override", "Static methods in interfaces too"]),
        ("What is a functional interface? How does it enable lambda expressions?", "easy", "fresher",
         ["Examples of built-in functional interfaces?", "@FunctionalInterface annotation?"],
         ["Exactly one abstract method", "Can have default/static methods", "Lambda is anonymous implementation", "Examples: Runnable, Comparator, Predicate"]),
        ("Can interfaces have constructors? Why or why not?", "easy", "fresher",
         ["What about abstract class constructors?", "How do you initialize interface constants?"],
         ["No — interfaces can't be instantiated", "No state to initialize", "Constants must be initialized inline", "Abstract classes can have constructors"]),
        ("What's a marker interface? Is it still needed with annotations?", "medium", "fresher",
         ["Examples?", "Serializable vs @Serializable annotation?"],
         ["Empty interface used as tag/marker", "Examples: Serializable, Cloneable", "Annotations are modern alternative", "Marker interface enables instanceof check"]),
        ("In Python, we don't have interfaces. How do you achieve the same effect?", "medium", "fresher",
         ["What is ABC module?", "Duck typing vs formal interfaces?", "Protocol classes in Python 3.8+?"],
         ["abc.ABC + @abstractmethod", "Duck typing: implicit interfaces", "Protocol: structural subtyping", "Convention: raise NotImplementedError"]),
    ]
    for txt, d, l, fu, pts in interfaces:
        Q.append(_q("interfaces_abstract", d, l, txt, fu, pts))

    # ═══════ JAVA SPECIFIC ═══════
    java = [
        ("Explain how the JVM works. What happens from the moment you run 'java MyClass' until the program executes?", "hard", "fresher",
         ["What are the JVM memory areas?", "What is JIT compilation?", "How does class loading work?"],
         ["ClassLoader loads .class file", "Bytecode verifier checks", "JIT compiles hot methods to native code", "Memory: heap, stack, method area, PC register"]),
        ("What is the Java Collections Framework? When would you use ArrayList vs LinkedList vs HashMap?", "medium", "fresher",
         ["What about ConcurrentHashMap?", "TreeMap vs HashMap?", "When does ArrayList beat LinkedList?"],
         ["ArrayList: random access O(1), insert O(n)", "LinkedList: insert O(1), access O(n)", "HashMap: key-value O(1) average", "Choose based on access patterns"]),
        ("What is the String pool in Java? Why does 'hello' == 'hello' return true but new String('hello') == new String('hello') returns false?", "medium", "fresher",
         ["How does intern() work?", "Is StringBuffer in the pool?", "Memory implications?"],
         ["String pool: cache of string literals in heap", "Literals reuse pool entries", "new String() creates new object always", "intern() forces pool usage"]),
        ("Explain Java's exception hierarchy. Checked vs unchecked — when do you use each?", "medium", "fresher",
         ["What about Error vs Exception?", "Should you catch RuntimeException?", "Custom exceptions — checked or unchecked?"],
         ["Throwable → Error, Exception", "Exception → checked (IOException) + unchecked (RuntimeException)", "Checked: recoverable, must handle", "Unchecked: programming errors"]),
        ("What is multithreading in Java? Explain the difference between extends Thread and implements Runnable.", "medium", "fresher",
         ["What about Callable?", "Thread safety mechanisms?", "What is a thread pool?"],
         ["Thread: single inheritance used up", "Runnable: flexible, preferred", "Callable: returns value + throws exception", "ExecutorService for thread pooling"]),
        ("What are Java generics? What is type erasure and why does it matter?", "hard", "mid",
         ["Bounded wildcards?", "Why can't you create generic arrays?", "Reification?"],
         ["Compile-time type safety", "Type erasure: types removed at runtime", "Cannot do instanceof with generics", "Wildcards: ? extends T, ? super T"]),
        ("What is the volatile keyword in Java? How is it different from synchronized?", "hard", "mid",
         ["Visibility vs atomicity?", "When is volatile enough?", "What about AtomicInteger?"],
         ["Volatile: visibility guarantee, no caching", "Synchronized: mutual exclusion + visibility", "Volatile: single variable reads/writes", "Atomic classes: CAS-based thread safety"]),
        ("Explain Java Streams API. How is it different from iterating with a for loop?", "medium", "fresher",
         ["Lazy evaluation?", "Parallel streams?", "When not to use streams?"],
         ["Declarative data processing pipeline", "Lazy: intermediate ops not evaluated immediately", "map, filter, reduce, collect", "Parallel: automatic multi-threading"]),
        ("What's the difference between HashMap and Hashtable? Why is Hashtable considered legacy?", "easy", "fresher",
         ["Thread safety differences?", "ConcurrentHashMap vs Hashtable?", "Null key handling?"],
         ["HashMap: not synchronized, allows null", "Hashtable: synchronized, no null", "ConcurrentHashMap: better concurrent alternative", "Hashtable legacy: poor scalability"]),
        ("What are Java annotations? How do you create a custom annotation?", "medium", "fresher",
         ["Retention policies?", "How does Spring use annotations?"],
         ["Metadata for classes/methods/fields", "Built-in: @Override, @Deprecated, @SuppressWarnings", "Retention: SOURCE, CLASS, RUNTIME", "Custom: @interface + @Retention + @Target"]),
    ]
    for txt, d, l, fu, pts in java:
        Q.append(_q("java_specific", d, l, txt, fu, pts, tg=["java", "oop"]))

    # ═══════ PYTHON OOP ═══════
    python_oop = [
        ("What are dunder methods in Python? Explain __init__, __str__, __repr__, __eq__ with examples.", "medium", "fresher",
         ["__str__ vs __repr__?", "What is __hash__?", "How does __call__ work?"],
         ["Double underscore special methods", "__init__: constructor", "__str__: human-readable, __repr__: unambiguous", "__eq__: equality comparison"]),
        ("What are metaclasses in Python? When would you ever need to use one?", "hard", "mid",
         ["type() is a metaclass?", "How does Django models use metaclasses?", "__new__ vs __init__ in metaclass?"],
         ["Classes that create classes", "type is the default metaclass", "Control class creation behavior", "Use cases: ORMs, API frameworks, validation"]),
        ("Explain Python's MRO and how super() works with multiple inheritance.", "hard", "mid",
         ["What order does super() follow?", "Can you skip a parent?", "What's cooperative multiple inheritance?"],
         ["MRO: C3 linearization", "super() follows MRO, not parent", "Cooperative: all classes use super()", "Use mro() to inspect order"]),
        ("What are decorators in Python? How would you write a decorator that logs function execution time?", "medium", "fresher",
         ["What about decorators with arguments?", "Class-based decorators?", "functools.wraps — why?"],
         ["Function that wraps another function", "Uses closure to add behavior", "@syntax sugar for func = decorator(func)", "functools.wraps preserves metadata"]),
        ("What is the descriptor protocol in Python? How do properties use it?", "hard", "mid",
         ["__get__, __set__, __delete__?", "Data vs non-data descriptors?", "How does property() work internally?"],
         ["Protocol: __get__, __set__, __delete__", "Property is a descriptor", "Data descriptor: has __set__", "Controls attribute access at class level"]),
        ("What's the difference between @staticmethod and @classmethod? When do you use each?", "easy", "fresher",
         ["Can staticmethod access class variables?", "What about factory methods?"],
         ["staticmethod: no cls or self, plain function in class namespace", "classmethod: receives cls, can access class state", "classmethod for factory methods", "staticmethod for utility functions"]),
        ("How does Python handle private variables? What's name mangling?", "easy", "fresher",
         ["Is anything truly private in Python?", "Single vs double underscore?", "Convention vs enforcement?"],
         ["Single underscore: convention for private", "Double underscore: name mangling (_Class__var)", "Nothing truly private — convention-based", "Name mangling prevents accidental access in subclasses"]),
        ("What are dataclasses in Python? How do they compare to named tuples?", "easy", "fresher",
         ["Mutable vs immutable?", "Can you add methods to dataclasses?", "What about __post_init__?"],
         ["@dataclass auto-generates __init__, __repr__, __eq__", "Mutable by default (frozen=True for immutable)", "Named tuples: immutable, tuple-based", "Dataclasses: more flexible, full classes"]),
        ("Explain Python's slots mechanism. When and why would you use __slots__?", "hard", "mid",
         ["Memory savings?", "Can you use slots with inheritance?", "Limitations?"],
         ["Replaces __dict__ with fixed set of attributes", "Memory savings: no per-instance dict", "Faster attribute access", "Can't add attributes dynamically"]),
        ("What is duck typing? How does it differ from structural typing (Protocol)?", "medium", "fresher",
         ["EAFP vs LBYL?", "How does isinstance() fit in?", "When does duck typing break?"],
         ["If it walks like a duck, quacks like a duck...", "Check behavior, not type", "Protocol: formal duck typing with type checking", "EAFP: try/except approach"]),
    ]
    for txt, d, l, fu, pts in python_oop:
        Q.append(_q("python_oop", d, l, txt, fu, pts, tg=["python", "oop"]))

    # ═══════ EXCEPTION HANDLING ═══════
    exceptions = [
        ("What is the difference between throw and throws in Java?", "easy", "fresher",
         ["When would you re-throw an exception?", "Custom exception example?"],
         ["throw: actually throws exception object", "throws: declares method can throw", "throw in method body, throws in signature", "Custom: extend Exception or RuntimeException"]),
        ("How do you handle exceptions in a microservice where one service calling another fails?", "hard", "mid",
         ["Circuit breaker pattern?", "Fallback mechanisms?", "Retry with exponential backoff?"],
         ["Catch specific exceptions", "Circuit breaker for repeated failures", "Retry with backoff for transient errors", "Fallback/default response for graceful degradation"]),
        ("What happens if an exception is thrown inside a finally block?", "medium", "fresher",
         ["Does the original exception get lost?", "try-with-resources vs finally?"],
         ["Finally exception suppresses the try/catch exception", "Original exception lost", "Use try-with-resources for auto-closing", "Suppressed exceptions in Java 7+"]),
        ("What is exception chaining? How does it help in debugging?", "medium", "fresher",
         ["How to preserve original stack trace?", "When to wrap vs rethrow?"],
         ["Wrapping original exception as cause", "throw new CustomException(message, originalException)", "Preserves root cause for debugging", "Common at layer boundaries"]),
        ("Should you catch Exception or catch specific exception types? Why?", "easy", "fresher",
         ["Pokemon exception handling?", "What about Error?"],
         ["Catch specific exceptions", "Generic catch hides bugs", "Never catch Error (OutOfMemoryError etc.)", "Pokemon: catch(Exception e) — gotta catch 'em all — anti-pattern"]),
    ]
    for txt, d, l, fu, pts in exceptions:
        Q.append(_q("exception_handling", d, l, txt, fu, pts))

    # ═══════ UML & MODELING ═══════
    uml = [
        ("Draw a class diagram for an online bookstore. What relationships would you use?", "medium", "fresher",
         ["Association vs aggregation vs composition?", "Where do interfaces go?"],
         ["Classes: Book, Author, Order, Customer, Cart", "Composition: Order-OrderItem", "Aggregation: Author-Book", "Association: Customer-Order"]),
        ("What's the difference between aggregation and composition? Give me a real example.", "easy", "fresher",
         ["If the parent is deleted, what happens to children?", "How do you represent them in UML?"],
         ["Composition: strong ownership, child dies with parent", "Aggregation: weak ownership, child survives", "Composition: House-Room", "Aggregation: Department-Employee"]),
        ("Draw a sequence diagram for a user login flow in your application.", "medium", "fresher",
         ["What about error cases?", "Where does authentication happen?"],
         ["Client → Controller → AuthService → Database", "Lifelines for each component", "Return messages for responses", "Alt blocks for success/failure"]),
        ("What is a use case diagram? How does it differ from a sequence diagram?", "easy", "fresher",
         ["When do you use each?", "Who is the actor?"],
         ["Use case: what the system does (bird's eye view)", "Sequence: how it does it (detailed flow)", "Use case: actors + use cases + relationships", "Sequence: objects + messages over time"]),
        ("Explain the different types of relationships in UML — dependency, association, generalization, realization.", "medium", "fresher",
         ["How do you represent each with arrows?", "When does dependency become association?"],
         ["Dependency: uses (dashed arrow)", "Association: has-a (solid line)", "Generalization: is-a (solid triangle)", "Realization: implements (dashed triangle)"]),
    ]
    for txt, d, l, fu, pts in uml:
        Q.append(_q("uml_modeling", d, l, txt, fu, pts))

    # ═══════ GENERICS & TYPE SAFETY ═══════
    generics = [
        ("What are generics and why do we need them? What would happen without generics?", "easy", "fresher",
         ["ClassCastException at runtime?", "Type erasure?"],
         ["Compile-time type safety", "Without generics: Object-based, runtime casts", "Eliminates ClassCastException", "Reusable data structures"]),
        ("What is the difference between List<? extends Number> and List<? super Number>?", "hard", "mid",
         ["PECS rule?", "When to use each?"],
         ["extends: upper bound, read-only (producer)", "super: lower bound, write-only (consumer)", "PECS: Producer Extends, Consumer Super", "extends Number: Integer, Double etc. — can read as Number"]),
        ("Can you create a generic method that works with both Comparable and custom comparators?", "hard", "mid",
         ["Bounded type parameters?", "Multiple bounds?"],
         ["<T extends Comparable<T>> for natural ordering", "Comparator<T> parameter for custom", "Multiple bounds: <T extends A & B>", "Method-level vs class-level generics"]),
        ("What is type erasure in Java generics? Why can't you do 'new T()' inside a generic class?", "hard", "mid",
         ["What information is lost?", "How does reflection help?"],
         ["Generics removed at compile time", "JVM sees raw types", "Can't create generic instances — type unknown at runtime", "Workaround: pass Class<T> and use reflection"]),
    ]
    for txt, d, l, fu, pts in generics:
        Q.append(_q("generics", d, l, txt, fu, pts, tg=["java", "generics"]))

    # ═══════ COMPANY-SPECIFIC: ZOHO ═══════
    zoho = [
        ("Design a library management system with classes for Book, Member, Loan, Librarian. Show the class hierarchy and relationships.", "hard", "fresher",
         ["How do you handle overdue books?", "What design patterns would you use?", "How about reservation system?"],
         ["Book: title, author, ISBN, availability", "Member: name, borrowed books, fine", "Loan: book, member, dates, status", "Observer for notifications, Strategy for fine calculation"]),
        ("Write a program to demonstrate runtime polymorphism with a Shape hierarchy. Include at least 4 shapes.", "medium", "fresher",
         ["What if shapes need to be compared by area?", "How do you handle 3D shapes?"],
         ["Abstract Shape class with abstract area(), perimeter()", "Circle, Rectangle, Triangle, Hexagon extend Shape", "Runtime dispatch based on actual object type", "Comparable<Shape> for area comparison"]),
        ("Implement the Singleton pattern that is thread-safe, serialization-safe, and reflection-safe.", "hard", "mid",
         ["What about enum-based Singleton?", "Why is double-checked locking needed?"],
         ["Enum singleton: simplest, all guarantees", "DCL with volatile for lazy init", "readResolve() for serialization safety", "Private constructor + check in constructor for reflection"]),
        ("Design a parking lot system. Support different vehicle types, floors, and payment.", "hard", "fresher",
         ["What about handicapped spots?", "How do you find nearest available spot?"],
         ["Vehicle hierarchy: Car, Bike, Truck", "ParkingSpot: size, floor, occupied", "ParkingLot: floors, spots, entry/exit", "Strategy for payment, Observer for availability"]),
        ("What is the Decorator pattern? Implement it for a Pizza ordering system with toppings.", "medium", "fresher",
         ["How is this different from inheritance?", "What about removing a topping?"],
         ["Base Pizza interface/class", "ToppingDecorator wraps Pizza", "Each topping adds cost + description", "Composable: new Cheese(new Mushroom(new PlainPizza()))"]),
        ("Implement an LRU Cache using OOP principles. What classes and interfaces would you design?", "hard", "mid",
         ["Thread safety?", "How does LinkedHashMap help?"],
         ["Cache interface with get(), put()", "LRUCache implements Cache", "Doubly linked list + HashMap internally", "O(1) get and put operations"]),
        ("Design a notification system that supports email, SMS, and push notifications. Show how you'd extend it for WhatsApp.", "medium", "fresher",
         ["Which design pattern?", "How do you handle failures?"],
         ["Notification interface with send()", "EmailNotifier, SMSNotifier, PushNotifier", "Factory to create appropriate notifier", "Adding WhatsApp: new class, no existing code changes (OCP)"]),
        ("Walk me through how you'd design a chess game using OOP. Focus on the class hierarchy for pieces.", "hard", "fresher",
         ["How do you handle special moves like castling?", "How do pieces know valid moves?"],
         ["Abstract Piece: color, position, isValidMove()", "King, Queen, Rook, Bishop, Knight, Pawn", "Board: 8x8 grid of squares", "Game: tracks turns, check/checkmate, history"]),
    ]
    for txt, d, l, fu, pts in zoho:
        Q.append(_q("oop_design", d, l, txt, fu, pts, co="Zoho", tg=["zoho", "oop", "design"]))

    # ═══════ COMPANY-SPECIFIC: WIPRO ═══════
    wipro = [
        ("What are the four pillars of OOP? Explain each with a real-world example.", "easy", "fresher",
         ["Which pillar is most important?", "How do they relate to each other?"],
         ["Encapsulation: ATM hides banking logic", "Inheritance: Manager is-a Employee", "Polymorphism: same draw() for Circle, Square", "Abstraction: TV remote hides electronics"]),
        ("What is the difference between an abstract class and an interface? Give a scenario where you'd use each.", "easy", "fresher",
         ["Can abstract class have non-abstract methods?", "Default methods in interfaces?"],
         ["Abstract class: partial implementation + state", "Interface: contract definition", "Abstract when sharing code among related classes", "Interface for unrelated classes with common behavior"]),
        ("What is method overriding? Can you override a static method?", "easy", "fresher",
         ["What about private methods?", "What's the @Override annotation for?"],
         ["Subclass provides specific implementation of parent's method", "Same signature required", "Static methods: hidden, not overridden", "@Override: compile-time check"]),
        ("Explain constructor overloading with an example.", "easy", "fresher",
         ["What is constructor chaining?", "Default constructor when others exist?"],
         ["Multiple constructors with different parameters", "this() to chain constructors", "Compiler doesn't add default if any constructor exists", "Common for providing flexible initialization"]),
        ("What is the difference between composition and aggregation? Give examples from a college management system.", "easy", "fresher",
         ["If college closes, what happens to departments vs students?", "UML representation?"],
         ["Composition: College-Department (department dies with college)", "Aggregation: College-Student (student exists independently)", "Composition: strong has-a", "Aggregation: weak has-a"]),
    ]
    for txt, d, l, fu, pts in wipro:
        Q.append(_q("oop_basics", d, l, txt, fu, pts, co="Wipro", tg=["wipro", "oop"]))

    # ═══════ COMPANY-SPECIFIC: TCS ═══════
    tcs = [
        ("What is the difference between a class and a structure?", "easy", "fresher",
         ["Access modifiers difference?", "Memory allocation?"],
         ["Class: reference type, heap", "Struct: value type, stack (C#), similar in C++", "Class: default private (C++), struct: default public", "Struct for small data containers"]),
        ("Explain polymorphism with a real-time example from your project.", "easy", "fresher",
         ["Compile-time vs runtime?", "How did you implement it?"],
         ["Runtime: method overriding (virtual functions)", "Compile-time: method overloading, operator overloading", "Real example from own project", "Explain how it reduced code duplication"]),
        ("What is a virtual function? Why do we need it?", "easy", "fresher",
         ["Pure virtual function?", "What is a vtable?"],
         ["Enables runtime polymorphism", "Base class pointer can call derived class method", "Pure virtual = abstract method", "Vtable: array of function pointers"]),
        ("What is the diamond problem? How do you solve it?", "medium", "fresher",
         ["Virtual inheritance in C++?", "How does Java avoid it?"],
         ["D inherits B and C, both inherit A", "Ambiguity: which A's method does D use?", "C++: virtual inheritance", "Java: no multiple class inheritance"]),
        ("What are the advantages and disadvantages of OOP?", "easy", "fresher",
         ["When is OOP not suitable?", "Procedural vs OOP?"],
         ["Advantages: reusability, maintainability, modularity", "Disadvantages: overhead, complexity for simple tasks", "Not ideal: performance-critical, simple scripts", "Functional programming gaining popularity"]),
    ]
    for txt, d, l, fu, pts in tcs:
        Q.append(_q("oop_basics", d, l, txt, fu, pts, co="TCS", tg=["tcs", "oop"]))

    # ═══════ ADDITIONAL DESIGN QUESTIONS ═══════
    extra_design = [
        ("What's the difference between Adapter and Facade pattern?", "medium", "mid",
         ["Can you use both together?", "Which simplifies, which converts?"],
         ["Adapter: converts interface to another", "Facade: simplifies complex subsystem", "Adapter: one-to-one mapping", "Facade: one interface for many components"]),
        ("Explain the Flyweight pattern. Where is it used in real systems?", "hard", "mid",
         ["String pool?", "Integer cache?"],
         ["Shares common state among many objects", "Intrinsic (shared) vs extrinsic (unique) state", "Examples: Java String pool, Integer cache", "Reduces memory when many similar objects"]),
        ("What's the Prototype pattern? How does clone() in Java relate?", "medium", "mid",
         ["Deep vs shallow clone?", "When is prototype better than new?"],
         ["Creates copies of existing objects", "Avoids expensive construction", "clone() implements Prototype", "Useful when object creation is costly"]),
        ("Explain the Mediator pattern. How does it reduce coupling?", "medium", "mid",
         ["Chat room example?", "Mediator vs Observer?"],
         ["Central hub for communication", "Components talk through mediator, not directly", "Reduces N-to-N to N-to-1", "Example: chat room, air traffic control"]),
        ("What is the Composite pattern? How would you use it for a file system?", "medium", "mid",
         ["File vs Directory?", "How does it enable uniform treatment?"],
         ["Tree structure for part-whole hierarchies", "Component interface: File and Directory", "Directory contains Components (files or directories)", "Uniform operation: size(), display() on both"]),
        ("What is cohesion and coupling? How do you achieve high cohesion and low coupling?", "easy", "fresher",
         ["Types of coupling?", "How do interfaces reduce coupling?"],
         ["Cohesion: how focused a class is", "Coupling: how dependent classes are", "High cohesion: class does one thing well", "Low coupling: minimal dependencies between classes"]),
        ("What is the Law of Demeter? Why is it called 'don't talk to strangers'?", "medium", "mid",
         ["Method chaining — does it violate LoD?", "When to break this rule?"],
         ["Only call methods of direct collaborators", "Don't chain: a.getB().getC().doSomething()", "Reduces coupling", "Builder pattern chains are OK — they return self"]),
        ("What is dependency injection? Explain constructor injection vs setter injection.", "medium", "fresher",
         ["Which is preferred?", "How does Spring DI work?"],
         ["Passing dependencies from outside", "Constructor: required dependencies, immutable", "Setter: optional dependencies, mutable", "Spring: @Autowired, @Inject"]),
        ("How do you decide between using an enum and a class hierarchy?", "medium", "mid",
         ["Type safety?", "When enums are insufficient?"],
         ["Enum: fixed set of constants with behavior", "Class hierarchy: extensible, open for new types", "Enum: payment types (limited set)", "Hierarchy: shapes (may add new shapes)"]),
        ("What is the Tell, Don't Ask principle? How does it improve OOP design?", "medium", "mid",
         ["Examples of violation?", "Getter-heavy classes?"],
         ["Tell objects what to do, don't query and decide for them", "Moves logic into the object that owns the data", "Violation: if(account.getBalance() > amount) account.withdraw()", "Better: account.withdrawIfSufficient(amount)"]),
    ]
    for txt, d, l, fu, pts in extra_design:
        Q.append(_q("design_principles", d, l, txt, fu, pts))

    # ═══════ ADDITIONAL CORE OOP ═══════
    more_core = [
        ("What is object cloning? When would you prefer it over creating a new object?", "medium", "fresher",
         ["Shallow vs deep clone?", "Cloneable interface?"],
         ["Creates exact copy of an object", "Faster than constructor for complex objects", "Shallow: copies references", "Deep: copies all nested objects"]),
        ("What are abstract methods? Can an abstract class have non-abstract methods?", "easy", "fresher",
         ["Can abstract class have constructors?", "Can abstract class be final?"],
         ["Abstract method: declaration without body", "Yes, abstract class can have concrete methods", "Subclass MUST implement all abstract methods", "Abstract + final: contradiction — won't compile"]),
        ("What is upcasting and downcasting? When do you need explicit casting?", "medium", "fresher",
         ["ClassCastException?", "instanceof check?"],
         ["Upcasting: child to parent (implicit, safe)", "Downcasting: parent to child (explicit, risky)", "ClassCastException if wrong type", "Always use instanceof before downcasting"]),
        ("What is the difference between compile-time and runtime polymorphism?", "easy", "fresher",
         ["Examples of each?", "Which is more flexible?"],
         ["Compile-time: overloading, resolved at compile", "Runtime: overriding, resolved at execution", "Runtime: more flexible, enables OCP", "Compile-time: faster, less overhead"]),
        ("Explain tight coupling vs loose coupling with a real scenario.", "easy", "fresher",
         ["How do interfaces help?", "DI and loose coupling?"],
         ["Tight: classes directly depend on concrete classes", "Loose: depend on abstractions", "Tight: hard to test, change, maintain", "Loose: easy to swap implementations"]),
        ("What is association? How is it different from dependency?", "medium", "fresher",
         ["Multiplicity?", "Bidirectional vs unidirectional?"],
         ["Association: lasting relationship between objects", "Dependency: temporary, uses-a", "Association: Teacher-Student (ongoing)", "Dependency: Order uses Printer temporarily"]),
        ("What are the different types of constructors? Explain with code.", "easy", "fresher",
         ["Copy constructor?", "Default constructor?"],
         ["Default: no parameters", "Parameterized: takes arguments", "Copy: creates object from existing", "Overloaded: multiple constructors"]),
        ("What is early binding vs late binding?", "medium", "fresher",
         ["Which is faster?", "When does Java use each?"],
         ["Early: method resolved at compile time", "Late: method resolved at runtime", "Early: static, private, final methods", "Late: virtual methods (overridden)"]),
        ("What is a nested class? When would you use it over a top-level class?", "medium", "fresher",
         ["Static vs non-static nested?", "Anonymous classes?"],
         ["Logically groups classes used together", "Non-static: accesses outer class members", "Static: doesn't need outer instance", "Anonymous: one-time use implementations"]),
        ("What is the difference between is-a, has-a, and uses-a relationships?", "easy", "fresher",
         ["UML representation?", "Code examples?"],
         ["is-a: inheritance (Dog is-a Animal)", "has-a: composition/aggregation (Car has-a Engine)", "uses-a: dependency (Order uses Printer)", "Prefer has-a and uses-a over is-a"]),
    ]
    for txt, d, l, fu, pts in more_core:
        Q.append(_q("oop_fundamentals", d, l, txt, fu, pts))

    # ═══════ TEMPLATE EXPANSION: More pattern questions ═══════
    pattern_templates = [
        ("Explain the {p} pattern. Give a real-world use case.", "medium", "fresher",
         ["When is it overkill?", "How does it relate to SOLID?"],
         ["{p} pattern definition", "Real-world use case", "Class diagram structure", "Advantages and disadvantages"]),
    ]
    extra_patterns = ["Repository", "Specification", "Unit of Work", "Data Transfer Object (DTO)",
                      "Active Record", "Service Locator", "Null Object", "Event Sourcing",
                      "Plugin", "Bridge", "Memento", "Interpreter"]
    for tmpl_txt, d, l, fu, pts in pattern_templates:
        for p in extra_patterns:
            Q.append(_q("design_patterns", d, l, tmpl_txt.format(p=p),
                        [f.format(p=p) for f in fu], [pt.format(p=p) for pt in pts]))

    # ═══════ TEMPLATE EXPANSION: Java collection questions ═══════
    collection_templates = [
        ("Explain when you would use {c} vs other alternatives. What are its time complexities?", "medium", "fresher",
         ["Thread-safe alternative?", "Internal implementation?"],
         ["Use case for {c}", "Time complexities: get/put/add", "Internal data structure", "Common pitfalls"]),
    ]
    collections = ["ArrayList", "LinkedList", "HashMap", "TreeMap", "HashSet", "LinkedHashSet",
                   "PriorityQueue", "ArrayDeque", "ConcurrentHashMap", "CopyOnWriteArrayList",
                   "EnumSet", "WeakHashMap"]
    for tmpl_txt, d, l, fu, pts in collection_templates:
        for c in collections:
            Q.append(_q("java_collections", d, l, tmpl_txt.format(c=c),
                        [f.format(c=c) for f in fu], [pt.format(c=c) for pt in pts],
                        tg=["java", "collections"]))

    # ═══════ TEMPLATE EXPANSION: SOLID violation scenarios ═══════
    solid_scenarios = [
        ("Here is a class that handles {scenario}. Identify which SOLID principle(s) it violates and refactor it.", "hard", "mid",
         ["What's the most critical violation?", "How would you test the refactored version?"],
         ["Identify the violation(s)", "Explain why it's problematic", "Propose refactored design", "Show how it enables testing"]),
    ]
    scenarios = [
        "user registration, email sending, and database logging",
        "order processing with discount calculation, payment, and notification",
        "file parsing for CSV, JSON, and XML in a single switch statement",
        "report generation with database query, formatting, and PDF export",
        "authentication with password hashing, token generation, and session management",
        "form validation, sanitization, and storage in one method",
        "API controller that queries DB, transforms data, and renders response",
        "notification service that handles email, SMS, push, and WhatsApp in one class",
    ]
    for tmpl_txt, d, l, fu, pts in solid_scenarios:
        for s in scenarios:
            Q.append(_q("solid_refactoring", d, l, tmpl_txt.format(scenario=s),
                        fu, pts))

    # ═══════ TEMPLATE EXPANSION: OOP comparison questions ═══════
    comparison_templates = [
        ("What is the difference between {a} and {b}? When would you use each?", "medium", "fresher",
         ["Can you use both together?", "Which is more common in production code?"],
         ["Definition of {a}", "Definition of {b}", "Key differences", "Use cases for each"]),
    ]
    comparisons = [
        ("method overloading", "method overriding"),
        ("abstract class", "concrete class"),
        ("composition", "inheritance"),
        ("interface", "abstract class"),
        ("static binding", "dynamic binding"),
        ("shallow copy", "deep copy"),
        ("aggregation", "composition"),
        ("encapsulation", "abstraction"),
        ("checked exceptions", "unchecked exceptions"),
        ("final", "finally"),
        ("final class", "abstract class"),
        ("this", "super"),
        ("instanceof", "getClass()"),
        ("String", "StringBuilder"),
        ("HashMap", "Hashtable"),
    ]
    for tmpl_txt, d, l, fu, pts in comparison_templates:
        for a, b in comparisons:
            Q.append(_q("oop_comparisons", d, l, tmpl_txt.format(a=a, b=b),
                        [f.format(a=a, b=b) for f in fu],
                        [pt.format(a=a, b=b) for pt in pts]))

    return Q
