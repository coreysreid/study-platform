# Project Short-Term State

Current priorities, open PRs, and recent decisions.
Update this file whenever work is completed or priorities shift.

---

## Open Pull Requests

| PR | Branch | Description | Status |
|----|--------|-------------|--------|
| #41 | `feature/curriculum-population` | 11 courses, 95 topics, 873 flashcards seeded via migrations 0013–0024; auto-enrollment on register | Awaiting merge |
| #42 | `feature/topic-code-ordering` | Topic `code` field (001A/001B/002A scheme); migrations 0026–0027; template display | Awaiting merge |

**Merge order matters:** #41 must merge before #42 (0026/0027 depend on the topics created by 0013–0024).

---

## Recent Decisions

- **Topic code scheme chosen** (2026-02-26): `NNNx` format (e.g. `001A`, `001B`, `002A`).
  Replaces the legacy `order` integer. See `project_longterm.md` for full convention.

- **Codes documented in migration 0013** but applied by migration 0027, because 0013 runs
  before the `code` column is added (0026). This is by design — see comment in 0013.

- **`CardFeedback` model deleted** (earlier): `test_security_and_modes` still imports it
  and fails. Pre-existing, unrelated to current work — leave it for a future cleanup PR.

---

## Immediate Priorities

1. Merge PR #41 (curriculum population) — prerequisite for everything else.
2. Merge PR #42 (topic codes) — depends on #41.
3. After merge: add `topic-code` CSS styling (`span.topic-code`) to the base stylesheet
   so the code renders visually distinct from the topic name.
4. Decide on next feature area — candidates:
   - SM-2 spaced repetition algorithm (currently only tracking confidence level)
   - Learning feedback loop (suggest prerequisite review on wrong answers)
   - Progress dashboard

---

## Known Issues / Tech Debt

- `test_security_and_modes` fails (imports deleted `CardFeedback`) — needs a cleanup PR.
- `FEATURE_STATUS.md` is significantly out of date (last updated 2026-02-13, pre-curriculum).
- `Topic.order` field still exists alongside `Topic.code` — could be removed once code is stable.
