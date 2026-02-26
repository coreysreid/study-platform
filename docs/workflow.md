# Development Workflow

How to structure sessions, what to hand the agent, and what to expect back.
Covers the three main types of work on this platform: content, features, and diagrams.

---

## Session Setup

Every session starts from the project root. The agent reads:

1. `project_longterm.md` — conventions, architecture, data model
2. `project_shortterm.md` — open PRs, immediate priorities

All decisions are made from those two files. Do not rely on agent memory for
project state.

---

## 1. Content Sessions (flashcard population)

Used for: writing new flashcard migrations, adding circuit diagram scripts.

**What to give the agent**

Paste the unit outline directly into chat — week-by-week topics, learning
outcomes, or textbook chapter headings. The CDU handbook URL also works
(`stapps.cdu.edu.au` is publicly fetchable). The more structure you provide,
the better the topic and flashcard breakdown.

**What the agent produces**

- A new data migration (`study/migrations/NNNN_flashcards_<course>.py`)
  following the same idempotent pattern as migrations 0013–0024.
- For circuit-heavy topics: Schemdraw scripts in `scripts/circuits/` and
  SVGs committed alongside the migration.

**Verification checklist (run before PR)**

```bash
venv/bin/python -m py_compile study/migrations/NNNN_*.py   # syntax
venv/bin/python manage.py migrate                           # applies cleanly
venv/bin/python manage.py test study --verbosity=1          # all pass
```

**Content rules (from project_longterm.md)**
- One atomic concept per card (one definition, one formula, one worked example)
- MathJax for all equations: `$...$` inline, `$$...$$` display
- Circuit diagrams: inline SVG in the `question` field — see `docs/RICH_MEDIA_GUIDE.md`
- question_type: `standard` (default), `step_by_step` for multi-step derivations

---

## 2. Feature Sessions (Django backend / frontend)

Used for: new views, model changes, template updates, CSS.

**Branch naming**

```
feature/<short-description>      e.g. feature/sm2-algorithm
fix/<short-description>          e.g. fix/topic-ordering-edge-case
```

**Standard sequence**

1. Create feature branch from `main`.
2. Make changes; run `manage.py makemigrations` if models changed.
3. Run full test suite — all tests must pass (except the pre-existing
   `test_security_and_modes` failure, which is unrelated to all current work).
4. Commit, push, open PR targeting `main`.
5. Wait for CI (GitHub Actions) — must be green before merge.
6. Update `project_shortterm.md` after merge.

**Test command**

```bash
venv/bin/python manage.py test study --verbosity=1
```

Expected: `Ran N tests in Xs  OK` (77+ tests as of 2026-02-26).

**Migration rules**
- Schema migration first, data migration second — never combine in one `RunPython`.
- Data migrations must be idempotent (`get_or_create`, `filter().update()` with guards).
- Reverse functions are intentional no-ops (`pass`).
- Run `makemigrations --check` locally before pushing — CI will fail if the
  model state doesn't match migrations.

---

## 3. Circuit Diagram Sessions

Used for: adding new Schemdraw SVGs for topics that need them.

**Build order** (from `docs/circuit_diagram_plan.md`)

1. Circuit Analysis Fundamentals (~8 diagrams, passive components only — fastest)
2. Analog Electronics (~20 diagrams — most complex, but `bjt_common_emitter.py` is the template)
3. Embedded Systems, Electrical Machines, Power Systems (~5 each)

**Session pattern**

```
"Draw the <circuit name> for the <topic> topic in <course>."
```

The agent:
1. Copies `scripts/circuits/_template.py` → `scripts/circuits/<circuit_name>.py`
2. Writes the Schemdraw code and runs it to produce the SVG
3. Verifies the output visually (Playwright screenshot)
4. Commits the `.py` and `.svg` files
5. Updates the status column in `docs/circuit_diagram_plan.md`

**Integrating into a flashcard migration**

```python
import pathlib
SVG_DIR = pathlib.Path(__file__).resolve().parent.parent.parent / 'scripts' / 'circuits'

svg = (SVG_DIR / 'bjt_common_emitter.svg').read_text()
Flashcard.objects.get_or_create(
    topic=topic,
    question=f'<figure class="circuit-diagram">{svg}</figure><p>Question text</p>',
    defaults={'answer': '...', 'question_type': 'standard'},
)
```

---

## Agent Permissions

The project `.claude/settings.json` pre-approves:

| Category | Commands |
|----------|----------|
| Python (venv) | `venv/bin/python *`, `venv/bin/pip *` |
| Python (system) | `python3 *`, `pip install *` |
| Git (read) | `git status`, `git log`, `git diff`, `git branch`, `git show` |
| Git (write) | `git add`, `git commit`, `git checkout`, `git stash`, `git pull` |
| GitHub CLI | `gh pr *`, `gh api *`, `gh run *` |
| Filesystem | `ls`, `mkdir`, `cp`, `mv`, `head`, `tail` |

**Requires explicit approval (kept safe by deny list in settings.json):**
- `git push --force *`
- `git reset --hard *`
- `rm -rf *`

`git push` (non-force) is in `settings.local.json` (per-machine opt-in) but
not in the committed `settings.json` — this keeps pushes requiring a
deliberate action on machines where that's preferred.

---

## Prompt Templates

Copy-paste these to start common session types:

**Add flashcard content for a topic**
```
Add flashcard content for the "<topic name>" topic in <course name>.
Here is the unit outline / learning outcomes:
[paste content]
```

**Draw a circuit diagram**
```
Draw the <circuit description> for topic <NNNx> (<topic name>) in <course name>.
Use scripts/circuits/_template.py as the base.
```

**New feature**
```
Implement <feature description>.
Branch from main. Run tests before creating the PR.
```

**Fix a bug**
```
Fix: <description of the bug / failing test>.
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| `makemigrations --check` fails in CI | Run `venv/bin/python manage.py makemigrations` locally after any model change; commit the result |
| Migration 0029 required before any math-course content | Math courses exist from 0029 onwards; fresh installs need the full migration chain |
| SVG file missing at migration run time | Commit `.svg` files alongside the migration; `load_svg()` returns `''` gracefully if missing |
| Schemdraw label collisions | Add a short `elm.Line().up/down().length(0.3-0.5)` stub before `elm.Vdd()` or `elm.Ground()` |
| Topic `code` field blank after fresh install | Migration 0027 sets all codes; runs after 0026 (schema) adds the column |

---

*Last updated: 2026-02-26*
