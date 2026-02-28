# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Agent Instructions

Before doing any work in this repository, read both project files below.
They are the single source of truth for conventions, architecture, and current state.

- [`project_longterm.md`](project_longterm.md) — platform vision, data model, content conventions, coding rules
- [`project_shortterm.md`](project_shortterm.md) — open PRs, recent decisions, immediate priorities

Do not rely on memory or inference for project conventions — read the files.
Update `project_shortterm.md` whenever work is completed or priorities change.

## Commands

```bash
# Development server
venv/bin/python manage.py runserver

# Run all tests
venv/bin/python manage.py test study --verbosity=1

# Run a single test
venv/bin/python manage.py test study.tests.TestClassName.test_method_name --verbosity=1

# Apply migrations
venv/bin/python manage.py migrate

# Check model/migration sync (must pass before pushing)
venv/bin/python manage.py makemigrations --check
```

Expected test result: all 77+ tests pass. The pre-existing `test_security_and_modes` failure
was fixed in PR #42 — if it reappears, investigate before marking it as known.

## App Structure

One Django app (`study/`) inside the `study_platform/` project:

- `study/models.py` — all models: Course, Topic, Flashcard, FlashcardProgress, CourseEnrollment, StudySession, TopicScore, Skill, UserBadge, AccountabilityLink
- `study/views.py` — all view functions; `get_system_user()` at line 31, `register()` at line 85
- `study/migrations/` — 0029 migrations on main; data seeds live here (not management commands)
- `study_platform/settings.py` — Django settings (SQLite dev / PostgreSQL prod via `dj-database-url`)

## Key Architecture: System User & Content Visibility

The `'system'` username owns all public curriculum content (courses, topics, flashcards).
`get_public_content_filter()` in `views.py` returns a `Q` filter combining the current user's
content with anything owned by the system user — this is how catalog courses are visible to all.

When adding new system content, always seed it via a data migration (idempotent, using
`get_or_create`) owned by the system user. Never use management commands for this.

## Session Types

Three common session types, each with its own pattern:

- **Content** (flashcard migrations, circuit diagrams) → `docs/workflow.md § 1 & 3`
- **Feature** (Django backend / frontend) → `docs/workflow.md § 2`
- **Circuit diagram** (Schemdraw SVGs) → `docs/workflow.md § 3`

## Permissions

Common commands are pre-approved in `.claude/settings.json`.
`git push --force`, `git reset --hard`, and `rm -rf` always require explicit approval.
