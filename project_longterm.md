# Project Long-Term Reference

Platform vision, architecture decisions, and conventions that change rarely.
Update this file when a convention is established or changed — not for day-to-day work.

---

## Platform Vision

An interactive study platform for electrical engineering students (expandable to other subjects).
The platform provides structured curriculum, spaced-repetition flashcards, and progress tracking.

Target user: an engineering student working through a ~1,100-hour self-directed curriculum
(11 courses × ~100 hours each).

---

## Technology Stack

| Layer | Choice |
|-------|--------|
| Backend | Python / Django |
| Database | SQLite (dev), PostgreSQL (production via dj-database-url) |
| Frontend | HTML5, CSS custom properties, Vanilla JavaScript — no framework |
| Fonts | Inter (UI), JetBrains Mono (code) via Google Fonts |
| Design system | `study/static/study/css/theme.css` — tokens, components, light/dark mode |
| Math | MathJax 3 for LaTeX rendering (`$...$` inline, `$$...$$` display) |
| Diagrams | Mermaid.js (theme adapts to light/dark mode) |
| Code highlighting | Prism.js |
| Auth | Django built-in + django-allauth |
| Deployment | Railway |

---

## Data Model

### Hierarchy

```
Course  →  Topic  →  Flashcard
```

- **Course**: a subject area (~100 hours of study, ~10 weeks at 10 hrs/week).
  Has a `code` (e.g. `ENGMATH`, `ENG301`) and a `created_by` user.
  System-owned courses have `created_by.username == 'system'`.
  Has `aqf_level` (1–20, optional): 1–6 primary school, 7–12 secondary, 13–20 AQF levels 1–8+.

- **Topic**: one week's block of work within a course (~10 hours: pre-reading, lecture, tutorial, homework).
  Has `code` (ordering code, see convention below), `order` (legacy integer), and `prerequisites` (M2M self-ref).
  Has `aqf_level` (nullable, inherits from course via `effective_aqf_level` property) and
  `star_difficulty` (1–6, optional): relative difficulty within the subject.

- **Flashcard**: an atomic study unit — one definition, one formula, or one worked calculation.
  Has `question_type` (standard, multiple_choice, step_by_step, parameterized).
  Has `star_difficulty` (nullable, inherits from topic via `effective_star_difficulty` property).

### Other key models

- `CourseEnrollment`: user ↔ course with status (studying / mastered / shelved)
- `FlashcardProgress`: per-user per-card spaced-repetition state (confidence 0–5)
- `StudySession`: timestamped session record
- `TopicScore`: rolling 0–1 confidence score per user per topic
- `Skill`: foundational skill tag, M2M with Flashcard
- `AccountabilityLink` / `AccountabilityRelationship`: shareable observer links
- `UserBadge`: earned badges (slugs defined in `BADGE_DEFINITIONS`)

---

## Topic Code Convention

Topics use a `code` field (`CharField(max_length=5)`) that controls sort order and
provides a human-readable position reference.

### Format

```
NNNx
```

- `NNN` — three-digit zero-padded week number within the course (`001`, `002`, … `010`)
- `x`   — uppercase letter distinguishing sub-topics within the same week (`A`, `B`, …)

**Examples:** `001A`, `001B`, `002A`, `010B`

### Rules

| Rule | Detail |
|------|--------|
| One letter per week (normally) | `001A` is the standard single-topic week |
| Letter suffix for splits | `001A` + `001B` = two sub-topics that together form one week's work |
| Skip numbers freely | Gaps are fine; they leave room for future insertion |
| User-created topics | Leave `code` blank — they sort before system topics but that's acceptable |
| Max length | 5 characters (`max_length=5` on the field) |

### Ordering

`Meta.ordering = ['course', 'code', 'name']`

Lexicographic sort works correctly: `'' < '001A' < '001B' < '002A'`.
Blank-code topics sort first within a course (user-created topics in practice).

### Current assignments (system courses)

| Course | Topics |
|--------|--------|
| Foundation Mathematics (FOUND101) | 001A Basic Arithmetic & Number Sense, 001B Algebra Fundamentals, 002A Geometry, 002B Trigonometry Fundamentals, 003A Pre-Calculus |
| Mathematics 1A (SMA101) | 001A Functions & Limits, 001B Continuity & Exponential Functions, 002A Differential Calculus, 002B Curve Sketching & Optimisation, 003A Integral Calculus, 003B Applications of Integration, 004A Complex Numbers, 004B Vectors in 2D & 3D, 005A Linear Algebra, 005B Systems of Linear Equations |
| Mathematics 1B (SMA102) | 001A Advanced Integration Techniques, 001B Volumes Surface Areas & Applications, 002A Numerical Methods, 003A Vector Spaces & Linear Transformations, 003B Eigenvalues & Eigenvectors, 004A Multivariable Calculus, 004B Vector Functions & Line Integrals, 005A Surface Integrals & Green's Theorem, 005B Gauss's Divergence Theorem |
| Mathematics 2 (SMA209) | 001A Ordinary Differential Equations (ODEs), 001B Second-Order ODEs (Homogeneous), 002A Second-Order ODEs (Non-Homogeneous), 002B Systems of ODEs, 003A Fourier Analysis, 003B Fourier Transforms, 004A Laplace Transforms, 004B Laplace Transforms — Applications, 009A Partial Differential Equations (PDEs) |
| Data Analytics (SMA212) | 001A–010A (Descriptive Statistics → Python & Pandas for Data Analytics) |
| Circuit Analysis Fundamentals | 001A–006A (DC Circuit Analysis → AC Power Analysis) |
| Analog Electronics | 001A–010A + 002B, 006B, 008B — 13 topics, ~120 cards (Signals & Amplifiers → Oscillators, incl. Semiconductors, Differential Amplifiers, Output Stages & Power Amplifiers) |
| Digital Signal Processing | 001A–010A (Sinusoids & Phasors → MATLAB for DSP) |
| Embedded Systems | 001A–009A (Microcontroller Architecture → IoT & Connectivity) |
| Control Systems | 001A–009A (Laplace Transforms & Transfer Functions → MATLAB & Simulink for Control) |
| Electrical Machines & Motors | 001A–006A (Transformer Theory → Variable Speed Drives) |
| Power Systems | 001A–006A (Power System Structure → Power Electronics in Power Systems) |
| Linux Fundamentals (LFCA) | 001A–008A (Linux Basics & CLI → LFCA Exam Preparation) |
| Networking Fundamentals | 001A–008A (OSI Model & TCP/IP → Industrial Networking) |
| Industrial Automation & Robotics | 001A–009A (PLC Fundamentals → Functional Safety (IEC 61508)) |

Full detail is in `study/migrations/0027_set_topic_codes.py` (original EE/CS courses) and `study/migrations/0029_restructure_mathematics.py` (mathematics split).

### Adding a new system topic

1. Decide which week block it belongs to in its course.
2. Assign the next available number (or letter suffix if it shares a week with an existing topic).
3. Set `code` in the topic dict in migration 0013 AND in the new data migration (or directly in a new seed migration).
4. Run `manage.py migrate` and verify sort order.

---

## Migration Conventions

- Data lives in migrations — no management commands for seeding system content.
- System course/topic/flashcard seeds: migrations `0013` (structure) + `0014`–`0024` (flashcards).
- Data migrations must be **idempotent** (use `get_or_create`, `filter().update()` with guards).
- Schema migration first, data migration second — never combine in one `RunPython`.
- Reverse functions for data migrations are intentional no-ops (`pass`).

---

## Design System

All visual styling lives in `study/static/study/css/theme.css`. Do not add inline styles to `base.html` or templates unless scoped to a single page's `{% block extra_css %}`.

### Tokens (CSS custom properties)

| Token group | Light | Dark |
|-------------|-------|------|
| `--bg` | `#FAFAF9` | `#18181B` |
| `--surface` | `#FFFFFF` | `#27272A` |
| `--accent` (torch flame) | `#F97316` | `#FB923C` |
| `--text-1` | `#1C1917` | `#FAFAFA` |
| `--font-sans` | Inter, system-ui | same |
| `--font-mono` | JetBrains Mono | same |

Dark mode is applied via `[data-theme="dark"]` on `<html>`. The attribute is set by a synchronous script in `<head>` (anti-FOUC) reading `localStorage('sp-theme')` or `prefers-color-scheme`. A theme-toggle button in the nav writes back to localStorage.

### Branding

- Name: **Steward's Path**
- Logo: inline SVG old-style pathfinder flame torch (organic flame in `--accent`, brown cloth-wrapped head, brown handle). Not a flashlight.
- Accent colour: torch flame orange (#F97316 light / #FB923C dark).

### Key component classes

| Class | Purpose |
|-------|---------|
| `.site-nav` / `.site-nav__inner` | Sticky top nav bar |
| `.site-nav__brand` | Logo + brand name link |
| `.site-nav__link` | Nav link (`.active` for current page) |
| `.dropdown` / `.dropdown__trigger` / `.dropdown__menu` | Hover dropdown |
| `.theme-toggle` | Light/dark toggle button |
| `.page-container` | Centred content wrapper (max 1240px) |
| `.content` | White/surface card for page body |
| `.card` / `.card__header` / `.card__title` | Secondary card component |
| `.btn` / `.btn-secondary` / `.btn-danger` / `.btn-ghost` | Button variants |
| `.form-group` / `.form-control` | Form inputs |
| `.message.success/error/warning/info` | Alert banners |
| `.badge` / `.badge-accent` / `span.topic-code` | Inline tags |
| `.fab-container` / `.fab` / `.fab-feedback` / `.fab-bug` | Fixed action buttons |
| `.modal-overlay` / `.modal` / `.modal__header` | Dialog modal |
| `.site-footer` | Page footer |

---

## Flashcard LaTeX Convention

All system flashcards must use `$...$` for inline math and `$$...$$` for display math.
Set `uses_latex=True` on any card containing math so MathJax renders it.

Do **not** use Unicode math characters (₁, ₂, μ, Ω, α, β) in place of LaTeX — they render poorly and cannot be typeset properly. Use `$V_1$`, `$\mu$`, `$\Omega$`, `$\alpha$`, `$\beta$` etc.

When fixing or adding cards with LaTeX, use an idempotent data migration (filter by topic + exact question text, then `.update()` or `.save()`).

---

## Template Conventions

- Topic code display: `{% if topic.code %}<span class="topic-code">{{ topic.code }}</span> · {% endif %}{{ topic.name }}`
- Use conditional so blank-code (user-created) topics render cleanly.
- Apply in detail/heading contexts: `course_detail.html`, `topic_detail.html`, `study_session.html`.
- Compact/snippet contexts (home, stats, observer) use plain `{{ topic.name }}` — course context makes the code redundant there.

---

## Testing

- Test runner: `venv/bin/python manage.py test study --verbosity=1`
- Known pre-existing failure: `test_security_and_modes` — imports the deleted `CardFeedback` model. Unrelated to all current work; ignore it.
- All other tests must pass before merging.

---

## Branch & PR Workflow

- Work on feature branches: `feature/<short-description>`
- PR into `main`; branch protection is active on the remote.
- Commit messages: `type: short description` (feat / fix / refactor / docs / chore).
