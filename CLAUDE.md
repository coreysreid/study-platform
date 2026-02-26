# Agent Instructions

Before doing any work in this repository, read both project files below.
They are the single source of truth for conventions, architecture, and current state.

- [`project_longterm.md`](project_longterm.md) — platform vision, data model, content conventions, coding rules
- [`project_shortterm.md`](project_shortterm.md) — open PRs, recent decisions, immediate priorities

Do not rely on memory or inference for project conventions — read the files.
Update `project_shortterm.md` whenever work is completed or priorities change.

## Session types

Three common session types, each with its own pattern:

- **Content** (flashcard migrations, circuit diagrams) → `docs/workflow.md § 1 & 3`
- **Feature** (Django backend / frontend) → `docs/workflow.md § 2`
- **Circuit diagram** (Schemdraw SVGs) → `docs/workflow.md § 3`

## Test command

```bash
venv/bin/python manage.py test study --verbosity=1
```

Expected: all tests pass. The pre-existing `test_security_and_modes` failure
was fixed in PR #42 — if it reappears, investigate before marking it as known.

## Permissions

Common commands are pre-approved in `.claude/settings.json`.
`git push --force`, `git reset --hard`, and `rm -rf` always require explicit approval.
