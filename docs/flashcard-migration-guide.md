# Flashcard Migration Authoring Guide

Lessons learned creating migrations 0013–0024. Follow this to avoid repeating mistakes.

---

## Migration Template

```python
from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return

    course = Course.objects.filter(
        name='EXACT COURSE NAME FROM 0013', created_by=system_user
    ).first()
    if not course:
        return

    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    def add_cards(topic_name, cards):
        topic = topics.get(topic_name)
        if not topic or Flashcard.objects.filter(topic=topic).exists():
            return  # idempotent: skip if any cards already exist for this topic
        for card in cards:
            Flashcard.objects.create(topic=topic, **card)

    add_cards('Topic Name', [...])


def reverse_fn(apps, schema_editor):
    pass  # intentional no-op — never destroy user-facing flashcard data on rollback


class Migration(migrations.Migration):

    dependencies = [
        ('study', '00NN_previous_migration'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
```

---

## Flashcard Field Reference

```python
{
    # Required
    'question': 'text',        # never use apostrophes in single-quoted strings — see below
    'answer':   'text',        # NEVER None — use '' for step_by_step cards
    'difficulty': 'easy',      # 'easy' | 'medium' | 'hard'
    'question_type': 'standard',  # 'standard' | 'step_by_step' | 'parameterized'
    'uses_latex': True,        # True for maths/formulas; False for CLI/code/prose

    # Optional
    'hint': 'text',            # shown before answer; omit key entirely if not needed
    'teacher_explanation': 'text',  # extra context shown after answer

    # Required when question_type='step_by_step'
    'steps': [
        {'move': 'Step label', 'detail': 'Explanation of this step'},
        ...
    ],
}
```

---

## Critical Rules (bugs hit in practice)

### 1. `answer` must never be `None`
The DB column is NOT NULL. Use `''` (empty string) for `step_by_step` cards where the
steps carry the answer content.

```python
# WRONG — causes IntegrityError: NOT NULL constraint failed
{'question': 'Derive X', 'answer': None, 'question_type': 'step_by_step', ...}

# CORRECT
{'question': 'Derive X', 'answer': '', 'question_type': 'step_by_step', ...}
```

### 2. Apostrophes in single-quoted strings cause SyntaxError
```python
# WRONG — SyntaxError: unterminated string literal
{'question': 'State De Moivre's theorem.', ...}

# CORRECT — use double quotes when the string contains an apostrophe
{'question': "State De Moivre's theorem.", ...}

# ALSO CORRECT — escape the apostrophe
{'question': 'State De Moivre\'s theorem.', ...}
```

### 3. Course names must exactly match migration 0013
Topic lookup uses `topics = {t.name: t for t in Topic.objects.filter(course=course)}`.
If the name doesn't match, `topic` is `None` and all cards are silently skipped.

Check `0013_seed_course_structures.py` for exact strings. Current course names:
- `'Engineering Mathematics'`
- `'Circuit Analysis Fundamentals'`
- `'Analog Electronics'`
- `'Digital Signal Processing'`
- `'Embedded Systems'`
- `'Control Systems'`
- `'Electrical Machines & Motors'`
- `'Power Systems'`
- `'Linux Fundamentals (LFCA)'`
- `'Networking Fundamentals'`
- `'Industrial Automation & Robotics'`

### 4. Use `get_or_create` for Skills in tests
Migration 0013 seeds ~60 skill names. Tests that call `Skill.objects.create(name='basic_arithmetic')`
will hit a UNIQUE constraint. Always use:
```python
skill, _ = Skill.objects.get_or_create(name='basic_arithmetic', defaults={...})
```

---

## Verification Workflow

```bash
# 1. Syntax check before running migrations
/home/stewards_path/study-platform/venv/bin/python -m py_compile study/migrations/0NNN_*.py

# 2. Run migrations
/home/stewards_path/study-platform/venv/bin/python manage.py migrate

# 3. Verify counts
/home/stewards_path/study-platform/venv/bin/python manage.py shell -c "
from study.models import Course, Topic, Flashcard
from django.contrib.auth.models import User
system = User.objects.get(username='system')
for c in Course.objects.filter(created_by=system).order_by('name'):
    fc = Flashcard.objects.filter(topic__course=c).count()
    print(f'{c.name}: {Topic.objects.filter(course=c).count()} topics, {fc} flashcards')
"

# 4. Run tests
/home/stewards_path/study-platform/venv/bin/python manage.py test study --verbosity=1
```

---

## Content Guidelines

| Subject | `uses_latex` | Notes |
|---------|-------------|-------|
| Maths / EE theory | `True` | All formulas, equations |
| CLI commands, code, MATLAB syntax | `False` | Plain text renders better |
| Definitions with no symbols | `False` | |

**Card mix per topic (~12–20 cards):** aim for ~60% standard, ~30% step_by_step, ~10% parameterized.

**`step_by_step` cards:** each `move` is a short imperative label ("Identify losses",
"Apply Kirchhoff's voltage law"); each `detail` is the concrete calculation or rule for
that step. Keep steps 4–7 items.

---

## Known Pre-existing Issue
`study/test_security_and_modes.py` imports `CardFeedback` which was deleted from
`study/models.py` before the curriculum branch. This causes 1 import error in the test
suite that is **not** related to flashcard migrations — do not attempt to fix it in a
content migration PR.
