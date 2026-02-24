# Learning Intelligence Layer — Design Document

**Date:** 2026-02-25
**Author:** coreysreid
**Status:** Approved — ready for implementation
**Context:** CDU VENG02, Semester 1 Year 3 — Analog Electronics, Control Systems, DSP, Embedded Systems

---

## Problem Statement

The platform has content (152 engineering maths cards) and study mechanics (spaced repetition, confidence tracking) but lacks the learning intelligence needed to actually help a student ace a mathematically demanding EE degree. Specifically:

1. Step-by-step problems (ODEs, Laplace transforms, Bode plots) are stored as flat Q&A cards — there is no mechanic to train the *process* of solving a problem, only the answer.
2. A student who struggles with ODEs has no signal that they should work on prerequisite calculus/integration first.
3. Cards have no teacher-style explanation — when stuck, the only option is the bare answer.
4. Content feedback (wrong answers, confusing steps, missing cards) mixes with bug reports in GitHub Issues, making it hard to process systematically.

---

## Goals

- Train procedural problem-solving (the "muscle memory" for multi-step maths) via active recall on individual steps.
- Detect when a student is struggling with a topic and recommend prerequisite work.
- Give students a full walkthrough when they need it, without short-circuiting active recall.
- Create a clean, agent-processable feedback loop for content quality.

---

## Feature 1: Step-by-Step Card Mechanic

### Concept

A single `step_by_step` flashcard stores a problem and its N solution steps. During a study session, the card expands into N virtual cards:

- Virtual card 1: Problem only → "What is the first move?"
- Virtual card 2: Problem + Step 1 → "What is the next move?"
- Virtual card k: Problem + Steps 1..k-1 → "What is Step k?"

The answer revealed is the step's `move` label (e.g. *"Apply partial fraction decomposition"*), followed optionally by the `detail` (the actual working). Spaced repetition tracks each step independently — if you consistently miss Step 3 of a Laplace transform problem, that step is promoted in the queue.

### Data Model Changes

```python
# study/models.py

class Flashcard(models.Model):
    # ... existing fields ...

    # Step-by-step fields (used when question_type='step_by_step')
    steps = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "Ordered list of solution steps. Each step: "
            '{"move": "short action name", "detail": "full working shown on reveal"}'
        )
    )
    teacher_explanation = models.TextField(
        blank=True,
        help_text=(
            "Full worked explanation written as a teacher would give it. "
            "Shown only on demand — never upfront. Include reasoning, context, "
            "and common mistakes."
        )
    )


class FlashcardProgress(models.Model):
    # ... existing fields ...

    step_index = models.IntegerField(
        null=True,
        blank=True,
        help_text=(
            "For step_by_step cards: which step this progress record tracks. "
            "null = whole card (non-step types)."
        )
    )
```

### Steps JSON Schema

```json
[
  {
    "move": "Find the integrating factor",
    "detail": "μ(x) = e^{\\int P(x)\\,dx} = e^{\\int 2\\,dx} = e^{2x}"
  },
  {
    "move": "Multiply both sides by μ(x)",
    "detail": "e^{2x}\\frac{dy}{dx} + 2e^{2x}y = 4xe^{2x}"
  },
  {
    "move": "Recognise the LHS as a product rule derivative",
    "detail": "\\frac{d}{dx}\\left[ye^{2x}\\right] = 4xe^{2x}"
  },
  {
    "move": "Integrate both sides",
    "detail": "ye^{2x} = \\int 4xe^{2x}\\,dx = 2xe^{2x} - e^{2x} + C"
  },
  {
    "move": "Solve for y",
    "detail": "y = 2x - 1 + Ce^{-2x}"
  }
]
```

### Study Session Expansion

In `study/views.py`, before rendering the study session:

1. For each `step_by_step` card in the session, generate N `VirtualCard` dataclass instances.
2. Each `VirtualCard` holds: `flashcard_id`, `step_index`, `problem`, `context_steps` (list of previous moves), `answer_move`, `answer_detail`.
3. Fetch or create `FlashcardProgress(flashcard=card, user=user, step_index=k)` for each virtual card.
4. The session queue is rebuilt from virtual cards + non-step cards.

### UI Flow (study_session.html)

```
┌─────────────────────────────────────────────────┐
│  Step 3 of 5                         [Progress] │
│                                                  │
│  PROBLEM                                         │
│  Solve: dy/dx + 2y = 4x                         │
│                                                  │
│  ✓ Step 1: Find the integrating factor           │
│  ✓ Step 2: Multiply both sides by μ(x)           │
│                                                  │
│  ❓ What is the next move?                        │
│                                                  │
│            [ Reveal Step 3 ]                     │
└─────────────────────────────────────────────────┘

After reveal:
┌─────────────────────────────────────────────────┐
│  Step 3: Recognise the LHS as a product rule     │
│          derivative                              │
│                                                  │
│  d/dx[ye^(2x)] = 4xe^(2x)                       │
│                                                  │
│  [ Show full teacher explanation ]               │
│                                                  │
│  How did you go?                                 │
│  [ Got it ] [ Nearly ] [ Missed it ]             │
└─────────────────────────────────────────────────┘
```

### Spaced Repetition

Each virtual card maps to its own `FlashcardProgress` record via `(flashcard_id, step_index)`. The existing confidence-based scheduling applies per step. Steps consistently rated "Missed it" are promoted; steps consistently rated "Got it" decay in frequency.

---

## Feature 2: Teacher Explanation

Every card (all types) gets a `teacher_explanation` field. For step-by-step cards this is the complete worked solution with full commentary. For standard cards it is a deeper explanation of the concept.

**Principles for content authors:**
- Write as if talking to a student who is stuck, not one who already understands.
- Explain *why* each step is taken, not just *what* the step is.
- Flag common mistakes (e.g. *"Students often forget the +C here because..."*).
- Use LaTeX freely — the platform already renders it.

**UI:** A "Show full explanation" button is always present on the answer side of any card. It never appears before the answer is revealed. It expands inline — no page navigation.

---

## Feature 3: Adaptive Difficulty & Prerequisite Regression

### Performance Tracking

After each study session, compute a **topic confidence score**: rolling average of the last 10 `FlashcardProgress.confidence` values for that topic (per user).

```python
# Pseudo-logic
recent = FlashcardProgress.objects.filter(
    flashcard__topic=topic, user=user
).order_by('-updated_at')[:10]
score = mean(p.confidence for p in recent)  # 0.0–1.0
```

Store this as a `TopicScore` model (or extend `CourseEnrollment`).

### Regression Signal

If a topic score drops below **0.4** (40%) across 10+ attempts, the system:

1. Checks that topic's `prerequisites` M2M.
2. For each prerequisite with a score above 0.7, surfaces no warning (you've got it).
3. For prerequisites with no score or score below 0.7, generates a nudge.

**Nudge UI** — shown at the start of the next session for that topic:

```
┌─────────────────────────────────────────────────────────┐
│ 💡 Heads up                                              │
│                                                          │
│ Your recent scores on Laplace Transforms suggest some   │
│ of the prerequisite maths may need reinforcement.        │
│                                                          │
│ Topics that might help:                                  │
│  → Integration Techniques  (no recent activity)         │
│  → Complex Numbers          (score: 38%)                 │
│                                                          │
│  [ Study Integration Techniques ]  [ Dismiss ]          │
└─────────────────────────────────────────────────────────┘
```

### Difficulty Progression Within a Topic

Cards are served in difficulty order by default (easy → medium → hard). As confidence on easy cards exceeds 0.8 across 5+ attempts, those cards drop to a low-frequency maintenance schedule. Hard cards are promoted earlier when easy cards are solid. This requires no new model fields — it uses existing `difficulty` and `confidence`.

### New Model

```python
class TopicScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)  # 0.0–1.0
    attempt_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'topic')
```

---

## Feature 4: Feedback System — Content vs Functional Split

### Separation of Concerns

| Type | Examples | Destination |
|------|----------|-------------|
| Content issue | Wrong answer, confusing step wording, missing cards for a topic, step order wrong | GitHub Issue, label: `content-feedback` |
| Bug / UX issue | Page crashes, broken layout, login problems | GitHub Issue, label: `bug` (existing flow) |

### In-Study Feedback Button

Present on every card (both question and answer sides). Clicking opens a small modal:

```
What's the issue?
  ○ This answer looks wrong
  ○ A step description is confusing
  ○ I need a better explanation for this topic
  ○ This topic needs more cards
  ○ Something else (UX/bug)
[ Optional: add a note ]
[ Submit ]
```

Content types → `content-feedback` GitHub Issue.
"Something else" → existing `bug` GitHub Issue flow.

### Agent-Facing Repository Files

```
feedback/
  AGENT_INSTRUCTIONS.md   # How Claude should process content feedback
  resolved.md             # Audit log of all agent-made content changes
```

#### `feedback/AGENT_INSTRUCTIONS.md`

Instructs Claude Code to:
1. List open GitHub Issues with label `content-feedback`.
2. For each issue: identify the affected card(s), assess the reported problem, make the fix (edit management command, fix `steps` JSON, improve `teacher_explanation`, create new cards).
3. Close the GitHub Issue with a comment describing what was changed.
4. Append an entry to `feedback/resolved.md`.
5. Commit all changes.

#### `feedback/resolved.md`

Chronological log of content changes made by agent action. Format:

```markdown
## 2026-02-25 — Fixed sign error in ODE step card

**Issue:** #45 — "Step 3 of the first-order ODE card has a sign error"
**Card:** Flashcard #42, Topic: First-Order ODEs
**Change:** Corrected `detail` for step 3: `-Ce^{-2x}` → `+Ce^{-2x}`
**Pattern noted:** Always verify sign when dividing by integrating factor.
```

Over time this log becomes a quality guide for authoring new content.

---

## Implementation Order

1. **Migration** — add `steps`, `teacher_explanation` to `Flashcard`; add `step_index` to `FlashcardProgress`; add `TopicScore` model.
2. **Study session expansion** — `VirtualCard` dataclass, session queue rebuild, per-step progress tracking.
3. **Study session UI** — step context display, reveal mechanic, "Show full explanation" button, three-option confidence rating.
4. **Adaptive difficulty** — `TopicScore` computation in `_award_badges` / session end view; nudge UI at session start.
5. **Feedback modal** — content vs bug split; `content-feedback` GitHub Issue creation.
6. **Repo feedback files** — `feedback/AGENT_INSTRUCTIONS.md`, `feedback/resolved.md`.
7. **Admin / form support** — `FlashcardForm` update to support `steps` JSON editor; `teacher_explanation` textarea.

---

## Out of Scope for This Sprint

- EE curriculum content (Analog Electronics, Control Systems, DSP, Embedded) — separate issue #37
- Content-first UX redesign — issue #38
- Upvote/downvote system — issue #36
- Password reset, mobile responsiveness, REST API
