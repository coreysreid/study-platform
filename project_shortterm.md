# Project Short-Term State

Current priorities, open PRs, and recent decisions.
Update this file whenever work is completed or priorities shift.

---

## Open Pull Requests

| PR | Description | Status |
|----|-------------|--------|
| open | DSP atomic flashcards (DSP First Ch 1 & 2, Kamen Ch 1); migration 0030 | 🔄 In review |

| PR | Description | Merged |
|----|-------------|--------|
| #42 | Topic `code` field (001A/001B/002A scheme); migrations 0026–0028; template display | ✅ 2026-02-26 |
| #43 | Split Engineering Mathematics into 5 CDU-aligned courses; migration 0029 | ✅ 2026-02-26 |

---

## Recent Decisions

- **DSP atomic card expansion** (2026-03-06): Migration 0030 adds 19-card topic `001B`
  "Signal Fundamentals & Operations" (Kamen Ch 1), plus 8 gap-fill cards to `001A`
  (DSP First Ch 1) and 9 gap-fill cards to `002A` (DSP First Ch 2). All new cards
  use proper `$...$` LaTeX delimiters and follow the one-concept-per-card principle.

- **Topic code scheme chosen** (2026-02-26): `NNNx` format (e.g. `001A`, `001B`, `002A`).
  `code` is now the primary sort key (`Meta.ordering`); `Topic.order` is legacy and may
  be removed once `code` is stable. Codes are documented in migration 0013 but applied
  by migration 0027, because 0013 runs before the `code` column is added (0026).

- **Engineering Mathematics split** (2026-02-26): Single 13-topic course replaced by five
  CDU-aligned courses via migration 0029: Foundation Mathematics (FOUND101), Mathematics 1A
  (SMA101), Mathematics 1B (SMA102), Mathematics 2 (SMA209), Data Analytics (SMA212).
  Total topics: 43 (5 + 10 + 9 + 9 + 10). Existing flashcards move with their topics.

- **`CardFeedback` model deleted** (earlier): import and dead test class removed from
  `test_security_and_modes` in PR #42. All 77 tests now pass.

- **Circuit diagram pipeline established** (2026-02-26): Schemdraw generates SVGs offline;
  inline into flashcard `question` field as plain text. First diagram: `bjt_common_emitter.svg`.
  ~42 diagrams planned — see `docs/circuit_diagram_plan.md` for full list and build order.

- **Agent permissions configured** (2026-02-26): `.claude/settings.json` pre-approves
  venv/python, git, gh CLI, and filesystem commands. Force-push, hard-reset, and rm -rf
  still require explicit approval. `docs/workflow.md` documents session patterns.

---

## Immediate Priorities

1. Add `topic-code` CSS styling (`span.topic-code`) to the base stylesheet
   so the code renders visually distinct from the topic name.
2. Add flashcard content for the 30 new topics in SMA101, SMA102, SMA209, SMA212.
3. Work through circuit diagrams — start with Circuit Analysis Fundamentals
   (~8 passive-component diagrams; see `docs/circuit_diagram_plan.md` build order).
4. Decide on next feature area — candidates:
   - SM-2 spaced repetition algorithm (currently only tracking confidence level)
   - Learning feedback loop (suggest prerequisite review on wrong answers)
   - Progress dashboard

---

## Known Issues / Tech Debt

- `FEATURE_STATUS.md` is significantly out of date (last updated 2026-02-13, pre-curriculum).
- `Topic.order` field still exists alongside `Topic.code` — could be removed once code is stable.
