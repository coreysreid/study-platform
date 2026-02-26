# Degree Mapping

Maps CDU unit codes to platform courses. Used to track curriculum coverage and prioritise
new course development. Update when new courses are added to the platform.

**Coverage key**
- ✅ Covered — a platform course exists that maps directly to this unit
- ⚡ Partial — the unit is partly covered by an existing course or a single topic within one
- 🔲 Gap — no platform course exists yet; candidate for development
- — Out of scope — professional/soft skills, not planned for flashcard-based study

---

## CDU Bachelor of Engineering (Electrical & Electronics)

### Common / Core Units

| Code | Unit Name | Platform Course | Coverage |
|------|-----------|-----------------|----------|
| SMA101 | Mathematics 1A | Mathematics 1A (SMA101) | ✅ |
| SMA102 | Mathematics 1B | Mathematics 1B (SMA102) | ✅ |
| SMA209 | Mathematics 2A | Mathematics 2 (SMA209) | ✅ |
| ENG151 | Statics | — | 🔲 |
| ENG252 | Dynamics | — | 🔲 |
| ENG175 | Internet of Things | Embedded Systems (009A IoT & Connectivity), Networking Fundamentals | ⚡ |
| HIT137 | Software Now | — | 🔲 |
| SMA212 | Data Analytics | Data Analytics (SMA212) | ✅ |
| ENG305 | Safety, Risk and Reliability | Industrial Automation & Robotics (009A Functional Safety IEC 61508) | ⚡ |
| PMO201 | Project Management | — | — |
| ENG410 | Professional Practice for Engineers | — | — |
| ENG519 | Sustainability | — | — |
| IAS201 | Cultural Capabilities | — | — |
| CUC106 | Design and Innovation: Communicating Technology | — | — |

### Electrical & Electronics Specialisation

| Code | Unit Name | Platform Course | Coverage |
|------|-----------|-----------------|----------|
| ENG223 | Electrical Circuit Analysis | Circuit Analysis Fundamentals | ✅ |
| ENG221 | Analogue Electronics | Analog Electronics | ✅ |
| ENG571 | Analogue Devices | Analog Electronics | ✅ |
| ENG572 | Digital Signal Processing | Digital Signal Processing | ✅ |
| ENG574 | Power Systems Analysis | Power Systems | ✅ |
| ENG224 | Electrical Machines and Power Systems | Electrical Machines & Motors + Power Systems | ✅ |
| ENG325 | Systems Modelling and Control | Control Systems | ✅ |
| ENG576 | Control Engineering | Control Systems | ✅ |
| ENG320 | Embedded and Mobile Systems | Embedded Systems | ✅ |
| ENG229 | Digital Systems and Computer Architecture | — | 🔲 |
| ENG377 | Electromagnetics and Communication Technology | — | 🔲 |
| ENG573 | Communication Systems | — | 🔲 |
| ENG365 | C Programming | — | 🔲 |
| HIT391 | Machine Learning: Advancements and Applications | — | 🔲 |

**EE coverage summary:** 11/14 technical units covered · 3 gaps (ENG229, ENG377/573, ENG365) · 5 out-of-scope
Note: SMA212 Data Analytics now covered. Foundation Mathematics (FOUND101) is a bonus pre-university bridging course not in the CDU EE degree list.

---

## CDU Bachelor of IT (Computer Science)

| Code | Unit Name | Platform Course | Coverage |
|------|-----------|-----------------|----------|
| SMA101 | Mathematics 1A | Mathematics 1A (SMA101) | ✅ |
| SMA102 | Mathematics 1B | Mathematics 1B (SMA102) | ✅ |
| HIT172 | Operating Systems and Applications | Linux Fundamentals (LFCA) | ⚡ |
| HIT274 | Network Engineering Applications | Networking Fundamentals | ✅ |
| ENG229 | Digital Systems and Computer Architecture | — | 🔲 |
| ENG320 | Embedded and Mobile Systems | Embedded Systems | ✅ |
| ENG365 | C Programming | — | 🔲 |
| HIT140 | Foundations of Data Science | — | 🔲 |
| HIT220 | Algorithms and Complexity | — | 🔲 |
| HIT226 | Mobile Web Structures | — | 🔲 |
| HIT234 | Database Concepts | — | 🔲 |
| HIT237 | Building Interactive Software | — | 🔲 |
| HIT326 | Database-Driven Web Applications | — | 🔲 |
| HIT333 | Cyber Security | Networking Fundamentals (006A Network Security) | ⚡ |
| HIT339 | Distributed Development | — | 🔲 |
| HIT381 | Human Computer Interaction Design | — | 🔲 |
| HIT164 | Computing Fundamentals | — | 🔲 |
| PMO201 | Project Management | — | — |
| HIT401 | Capstone Project | — | — |

**CS coverage summary:** 4/17 technical units covered · 13 gaps · 2 out-of-scope
Note: SMA101 and SMA102 now have dedicated courses. SMA212/HIT140 gap remains (Data Analytics covers SMA212 topics but HIT140 may need extra content).

---

## Gap Analysis — Candidate New Courses

Ordered by: (a) appears in both degrees, (b) technical depth suited to flashcard format.

| Priority | Unit(s) | Proposed Platform Course | Notes |
|----------|---------|--------------------------|-------|
| 1 | ENG229 | Digital Systems & Computer Architecture | Shared by both degrees. Logic gates → ISA → microarchitecture → pipelines |
| 2 | ENG365 | C Programming | Shared. Syntax, pointers, memory, embedded C patterns |
| 3 | ENG573, ENG377 | Communication Systems & Electromagnetics | EE core. Modulation, antennas, Maxwell's equations |
| 4 | HIT140 | Data Science (foundations) | SMA212 now covered by Data Analytics course. HIT140 may need additional content (EDA, feature engineering) |
| 5 | HIT220 | Algorithms & Complexity | CS core. Big-O, sorting, graphs, dynamic programming |
| 6 | HIT333 | Cyber Security | Expand existing Network Security topic into full course |
| 7 | HIT172 | Operating Systems | Expand Linux Fundamentals or add a dedicated OS course |
| 8 | HIT234, HIT326 | Databases | SQL, schema design, ORMs, web-connected DBs |
| 9 | HIT391 | Machine Learning | Neural nets, scikit-learn, PyTorch basics |
| 10 | HIT237, HIT226, HIT326 | Web Development | HTML/CSS/JS → Django/React; may be out of scope long-term |

---

## Adding a New Course from a Unit

When you have a unit syllabus to add:

1. Paste the unit outline (topics list, week-by-week breakdown, or handbook description)
   directly into the chat.
2. The agent will map the outline to ~6–10 topics, assign `NNNx` codes, and draft a
   seed migration following the same pattern as migrations 0013–0024.
3. Add the new course entry to this file with ✅ coverage.

The more detail you provide (weekly topics, textbook chapters, learning outcomes),
the better the topic and flashcard breakdown will be. A CDU handbook snippet or a copy
of the unit outline PDF text is ideal.

---

*Last updated: 2026-02-26 — mathematics restructure (migration 0029)*
