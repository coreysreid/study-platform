# Agent Instructions — Content Feedback Queue

This file tells Claude Code how to process content feedback for the study platform.
Direct the agent here with: *"work through the content feedback issues"*

---

## What This Is

Users report content problems (wrong answers, confusing steps, missing cards) from within
the study session. These are filed as GitHub Issues with the label `content-feedback`,
separate from bug reports (`bug` label).

This file is the agent's runbook for processing that queue.

---

## Step-by-Step Process

### 1. List open content feedback issues

```bash
gh issue list --repo coreysreid/study-platform --label content-feedback --state open
```

Work through them oldest-first.

### 2. For each issue

Read the issue body. It will contain:
- The card ID (or topic name if it's a "needs more cards" request)
- The type of problem (wrong answer / confusing step / needs explanation / needs more cards)
- Any user note

Identify the affected card(s):
- Check the management command that created it (likely `populate_comprehensive_math_cards.py` or a topic-specific command)
- Check the DB directly if needed: `python manage.py shell -c "from study.models import Flashcard; print(Flashcard.objects.get(pk=ID).question)"`

### 3. Make the fix

| Issue type | Action |
|------------|--------|
| Wrong answer | Fix the `answer` field (and `steps` detail if applicable) in the management command. Run the command with `--skip-existing` behaviour bypassed to update the record, OR apply a data migration. |
| Confusing step wording | Edit the `steps[k].move` or `steps[k].detail` in the management command and re-apply. |
| Needs better explanation | Add or improve `teacher_explanation` on the card. |
| Needs more cards | Create a new management command or extend an existing one with additional `Flashcard` records for that topic. |

### 4. Close the issue

```bash
gh issue close <NUMBER> --comment "Fixed: <brief description of what changed>"
```

### 5. Log the action

Append an entry to `feedback/resolved.md` following the existing format:

```markdown
## YYYY-MM-DD — <short description>

**Issue:** #<number> — "<issue title>"
**Card:** Flashcard #<id>, Topic: <topic name>
**Change:** <what was changed>
**Pattern noted:** <any reusable insight for future content authoring>
```

### 6. Commit

```bash
git add -A
git commit -m "Content fix: <brief description> (closes #<number>)"
```

---

## Content Quality Principles

These have been learned from resolved issues. Apply them when authoring or fixing cards.

- Step `move` labels should be action phrases: *"Find the integrating factor"*, not *"Integrating factor"*.
- Step `detail` should show the actual working with LaTeX, not just name the result.
- `teacher_explanation` should explain *why*, not just *what*. Include common mistakes.
- Difficulty should match: if a card requires integration by parts, it should not be marked `easy`.
- For EE topics, always ground abstract maths in a circuit/signal context where possible.

---

## Labels Reference

| Label | Meaning |
|-------|---------|
| `content-feedback` | Wrong/missing/confusing content — agent handles these |
| `bug` | Functional/UX issue — developer handles these |
| `enhancement` | Feature request — reviewed by owner |
