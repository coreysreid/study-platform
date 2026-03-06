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

- **Mathematics flashcard expansion** (2026-03-06): Migrations 0032–0035 add 247 new
  flashcards across the 30 empty topics created by migration 0029. Coverage:
  SMA101 (76 new cards incl. 17 for Complex Numbers), SMA102 (56 new cards incl. 10 for
  Eigenvalues & Eigenvectors), SMA209 (52 new cards incl. Fourier Transforms and
  Laplace Applications — both critical for CDU EE units), SMA212 (63 cards for all 10
  Data Analytics topics). All courses now have zero empty topics.

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

- **Issues #44, #46, #47, #48 resolved** (2026-03-03):
  - #46 (Bug): Added explicit `.order_by('code', 'name')` to `course_detail` topics queryset
    so annotations (COUNT) don't discard `Meta.ordering`.
  - #47: Missed cards are now re-queued 3 positions ahead in the JS deck so users revisit
    them in the same session; step-by-step cards carry their context when re-queued.
  - #48: Added "Reveal Answer" button (result buttons hidden until revealed); fixed visual-mode
    CSS so the flashcard container expands to 400px and buttons are no longer obstructed.
  - #44: Migration 0030 splits the non-atomic "What are the exact values of sin, cos, tan
    for 30°, 45°, 60°?" flashcard into 9 individual atomic LaTeX-enabled cards.

---

## Immediate Priorities

1. Add `topic-code` CSS styling (`span.topic-code`) to the base stylesheet
   so the code renders visually distinct from the topic name.
2. ~~Add flashcard content for the 30 new topics in SMA101, SMA102, SMA209, SMA212.~~ ✅ Done — migrations 0032–0035.
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
