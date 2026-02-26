# Project Short-Term State

Current priorities, open PRs, and recent decisions.
Update this file whenever work is completed or priorities shift.

---

## Open Pull Requests

| PR | Branch | Description | Status |
|----|--------|-------------|--------|
| #42 | `feature/topic-code-ordering` | Topic `code` field (001A/001B/002A scheme); migrations 0026–0028; template display | Awaiting merge |
| — | `feature/mathematics-restructure` | Split Engineering Mathematics into 5 courses (migration 0029); Data Analytics added | Awaiting PR creation |

**Merge order matters:** #42 must merge before `feature/mathematics-restructure` (0029 depends on topics created by 0013–0024 and the code field from 0026).

---

## Recent Decisions

- **Topic code scheme chosen** (2026-02-26): `NNNx` format (e.g. `001A`, `001B`, `002A`).
  Replaces the legacy `order` integer. See `project_longterm.md` for full convention.

- **Codes documented in migration 0013** but applied by migration 0027, because 0013 runs
  before the `code` column is added (0026). This is by design — see comment in 0013.

- **Engineering Mathematics split** (2026-02-26): Single 13-topic course replaced by five
  CDU-aligned courses via migration 0029: Foundation Mathematics (FOUND101), Mathematics 1A
  (SMA101), Mathematics 1B (SMA102), Mathematics 2 (SMA209), Data Analytics (SMA212).
  Total topics: 43 (5 + 10 + 9 + 9 + 10). Existing flashcards move with their topics.

- **`CardFeedback` model deleted** (earlier): `test_security_and_modes` still imports it
  and fails. Pre-existing, unrelated to current work — leave it for a future cleanup PR.

---

## Immediate Priorities

1. Merge PR #42 (topic codes) — prerequisite for mathematics-restructure.
2. Create and merge PR for `feature/mathematics-restructure` — depends on #42.
3. After merges: add `topic-code` CSS styling (`span.topic-code`) to the base stylesheet
   so the code renders visually distinct from the topic name.
4. Add flashcard content for the 30 new topics in SMA101, SMA102, SMA209, SMA212.
5. Decide on next feature area — candidates:
   - SM-2 spaced repetition algorithm (currently only tracking confidence level)
   - Learning feedback loop (suggest prerequisite review on wrong answers)
   - Progress dashboard

---

## Known Issues / Tech Debt

- `test_security_and_modes` fails (imports deleted `CardFeedback`) — needs a cleanup PR.
- `FEATURE_STATUS.md` is significantly out of date (last updated 2026-02-13, pre-curriculum).
- `Topic.order` field still exists alongside `Topic.code` — could be removed once code is stable.
