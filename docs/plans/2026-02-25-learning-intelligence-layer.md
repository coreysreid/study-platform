# Learning Intelligence Layer — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add step-by-step active recall mechanics, teacher explanations, adaptive difficulty nudges, and a content feedback pipeline to the study platform.

**Architecture:** Step-by-step cards store ordered `steps` JSON on the `Flashcard` model; the study session view expands them into virtual card dicts at runtime. Per-step progress is tracked via `FlashcardProgress` with a new `step_index` field (`-1` = whole card, `0..N-1` = individual steps). `TopicScore` aggregates rolling confidence per user/topic to drive prerequisite nudges.

**Tech Stack:** Django 4.2, SQLite/PostgreSQL, vanilla JS (no build step), Django TestCase.

---

## Context You Need

- Main app: `study/`
- Models: `study/models.py`
- Views: `study/views.py` — `study_session` (line 278), `update_flashcard_progress` (line 402), `end_study_session` (line 376)
- URLs: `study/urls.py`
- Study session template: `study/templates/study/study_session.html`
- Tests: `study/tests.py`
- Latest migration: `0011_add_accountability_and_badges.py` — next is `0012`
- `FlashcardProgress.unique_together = ['user', 'flashcard']` — we change this in Task 1
- `markCorrect()` / `markIncorrect()` in the JS do NOT currently make AJAX calls — progress is only counted, not stored per-card. We fix this in Task 4.

---

## Task 1: Model Migration — steps, teacher_explanation, step_index, TopicScore

**Files:**
- Modify: `study/models.py`
- Create: `study/migrations/0012_learning_intelligence.py` (via makemigrations)

### Step 1: Add fields to models.py

In `study/models.py`, add to the `Flashcard` class after the `parameter_spec` field (line 142):

```python
    # Step-by-step card fields
    steps = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            'Ordered solution steps for step_by_step cards. '
            'List of {"move": "action label", "detail": "full working"}'
        )
    )
    teacher_explanation = models.TextField(
        blank=True,
        help_text=(
            'Full worked explanation written as a teacher would give it. '
            'Shown only on user request. Include reasoning and common mistakes.'
        )
    )
```

In `FlashcardProgress`, change `unique_together` and add `step_index`. Replace the entire `FlashcardProgress` class with:

```python
class FlashcardProgress(models.Model):
    """Tracks individual flashcard progress for spaced repetition"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcard_progress')
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name='progress')
    step_index = models.IntegerField(
        default=-1,
        help_text='-1 = whole card; 0..N-1 = individual step index for step_by_step cards'
    )
    times_reviewed = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(auto_now=True)
    confidence_level = models.IntegerField(
        default=0,
        help_text="0-5 confidence level for spaced repetition"
    )

    class Meta:
        unique_together = ['user', 'flashcard', 'step_index']
        ordering = ['-last_reviewed']

    def __str__(self):
        return f"{self.user.username} - {self.flashcard.question[:30]}..."

    @property
    def success_rate(self):
        if self.times_reviewed == 0:
            return 0
        return (self.times_correct / self.times_reviewed) * 100
```

Add `TopicScore` model at the end of `study/models.py`:

```python
class TopicScore(models.Model):
    """Rolling confidence score per user per topic, used for adaptive difficulty nudges"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_scores')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='user_scores')
    score = models.FloatField(default=0.0, help_text='0.0-1.0 rolling average confidence')
    attempt_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user.username} - {self.topic.name}: {self.score:.2f}"
```

### Step 2: Write the failing tests

In `study/tests.py`, update the import at line 4:
```python
from .models import Course, Topic, Flashcard, Skill, FlashcardProgress, TopicScore
```

Add at the bottom of `study/tests.py`:

```python
class StepByStepModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        course = Course.objects.create(name='Test Course', created_by=self.user)
        self.topic = Topic.objects.create(course=course, name='Test Topic')
        self.card = Flashcard.objects.create(
            topic=self.topic,
            question='Solve dy/dx + 2y = 4x',
            answer='y = 2x - 1 + Ce^{-2x}',
            question_type='step_by_step',
            steps=[
                {'move': 'Find integrating factor', 'detail': 'e^{2x}'},
                {'move': 'Multiply both sides', 'detail': 'd/dx[ye^{2x}] = 4xe^{2x}'},
                {'move': 'Integrate both sides', 'detail': 'ye^{2x} = 2xe^{2x} - e^{2x} + C'},
            ]
        )

    def test_step_card_has_steps_field(self):
        self.assertIsNotNone(self.card.steps)
        self.assertEqual(len(self.card.steps), 3)
        self.assertEqual(self.card.steps[0]['move'], 'Find integrating factor')

    def test_step_card_has_teacher_explanation_field(self):
        self.card.teacher_explanation = 'We use an integrating factor because...'
        self.card.save()
        self.card.refresh_from_db()
        self.assertIn('integrating factor', self.card.teacher_explanation)

    def test_flashcard_progress_step_index_default(self):
        progress = FlashcardProgress.objects.create(
            user=self.user, flashcard=self.card
        )
        self.assertEqual(progress.step_index, -1)

    def test_flashcard_progress_per_step_unique(self):
        FlashcardProgress.objects.create(user=self.user, flashcard=self.card, step_index=0)
        FlashcardProgress.objects.create(user=self.user, flashcard=self.card, step_index=1)
        count = FlashcardProgress.objects.filter(user=self.user, flashcard=self.card).count()
        self.assertEqual(count, 2)

    def test_topic_score_creation(self):
        ts = TopicScore.objects.create(user=self.user, topic=self.topic, score=0.75, attempt_count=10)
        self.assertEqual(ts.score, 0.75)
```

### Step 3: Run tests to verify they fail

```bash
cd /home/stewards_path/study-platform
python manage.py test study.tests.StepByStepModelTest -v 2
```

Expected: Errors about missing fields/models.

### Step 4: Create and apply migration

```bash
python manage.py makemigrations study --name learning_intelligence
python manage.py sqlmigrate study 0012
python manage.py migrate
```

### Step 5: Run tests to verify they pass

```bash
python manage.py test study.tests.StepByStepModelTest -v 2
```

Expected: All 5 tests pass.

### Step 6: Commit

```bash
git add study/models.py study/migrations/0012_learning_intelligence.py study/tests.py
git commit -m "feat: add steps, teacher_explanation, step_index, TopicScore models"
```

---

## Task 2: Make update_flashcard_progress Return JSON + Accept step_index

The view currently redirects (line 438). Study sessions need JSON responses for AJAX, and step cards need to pass `step_index`.

**Files:**
- Modify: `study/views.py` (lines 402-440)

### Step 1: Write failing test

In `study/tests.py`, add this import near the top:
```python
import json
from django.test import Client
```

Add at the bottom:

```python
class ProgressUpdateAjaxTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='proguser', password='pass')
        course = Course.objects.create(name='Course', created_by=self.user)
        self.topic = Topic.objects.create(course=course, name='Topic')
        self.card = Flashcard.objects.create(
            topic=self.topic, question='Q', answer='A'
        )
        from .models import CourseEnrollment
        CourseEnrollment.objects.create(user=self.user, course=course)
        self.client.login(username='proguser', password='pass')

    def test_progress_update_returns_json(self):
        response = self.client.post(
            f'/flashcard/{self.card.id}/progress/',
            {'correct': 'true', 'step_index': '-1'},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('confidence_level', data)

    def test_progress_update_with_step_index(self):
        response = self.client.post(
            f'/flashcard/{self.card.id}/progress/',
            {'correct': 'true', 'step_index': '0'},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['step_index'], 0)
        prog = FlashcardProgress.objects.get(user=self.user, flashcard=self.card, step_index=0)
        self.assertEqual(prog.times_reviewed, 1)
```

### Step 2: Run test to verify it fails

```bash
python manage.py test study.tests.ProgressUpdateAjaxTest -v 2
```

Expected: FAIL (currently returns a redirect, not JSON).

### Step 3: Rewrite update_flashcard_progress in views.py

Replace lines 402-440 with:

```python
@login_required
@require_POST
def update_flashcard_progress(request, flashcard_id):
    """Update per-card (or per-step) progress. Returns JSON."""
    from django.http import JsonResponse

    flashcard = get_object_or_404(Flashcard, id=flashcard_id)

    course = flashcard.topic.course
    is_owner = (course.created_by == request.user)
    has_enrollment = CourseEnrollment.objects.filter(
        user=request.user, course=course
    ).exists()
    if not (is_owner or has_enrollment):
        return JsonResponse({'error': 'No access'}, status=403)

    correct = request.POST.get('correct') == 'true'
    try:
        step_index = int(request.POST.get('step_index', '-1'))
    except (ValueError, TypeError):
        step_index = -1

    progress, _ = FlashcardProgress.objects.get_or_create(
        user=request.user,
        flashcard=flashcard,
        step_index=step_index,
    )

    progress.times_reviewed += 1
    if correct:
        progress.times_correct += 1
        progress.confidence_level = min(5, progress.confidence_level + 1)
    else:
        progress.confidence_level = max(0, progress.confidence_level - 1)
    progress.save()

    return JsonResponse({
        'confidence_level': progress.confidence_level,
        'times_reviewed': progress.times_reviewed,
        'step_index': step_index,
    })
```

### Step 4: Run test to verify it passes

```bash
python manage.py test study.tests.ProgressUpdateAjaxTest -v 2
```

### Step 5: Commit

```bash
git add study/views.py study/tests.py
git commit -m "feat: update_flashcard_progress returns JSON and accepts step_index"
```

---

## Task 3: Expand step_by_step Cards in the study_session View

The view must convert `step_by_step` flashcards into N virtual card dicts before passing data to the template.

**Files:**
- Modify: `study/views.py` (study_session function, lines 299-371)

### Step 1: Write failing test

In `study/tests.py`, add:

```python
class StudySessionExpansionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sessuser', password='pass')
        course = Course.objects.create(name='Course', created_by=self.user)
        self.topic = Topic.objects.create(course=course, name='Topic')
        from .models import CourseEnrollment
        CourseEnrollment.objects.create(user=self.user, course=course)
        self.step_card = Flashcard.objects.create(
            topic=self.topic,
            question='Solve dy/dx + 2y = 0',
            answer='y = Ce^{-2x}',
            question_type='step_by_step',
            steps=[
                {'move': 'Separate variables', 'detail': 'dy/y = -2 dx'},
                {'move': 'Integrate both sides', 'detail': 'ln|y| = -2x + C'},
                {'move': 'Solve for y', 'detail': 'y = Ce^{-2x}'},
            ]
        )
        self.client.login(username='sessuser', password='pass')

    def test_step_card_expands_to_n_virtual_cards(self):
        response = self.client.get(f'/study/{self.topic.id}/')
        self.assertEqual(response.status_code, 200)
        flashcards_data = response.context['flashcards_data']
        self.assertEqual(len(flashcards_data), 3)

    def test_virtual_card_has_context_steps(self):
        response = self.client.get(f'/study/{self.topic.id}/')
        cards = response.context['flashcards_data']
        self.assertEqual(cards[0]['step_index'], 0)
        self.assertEqual(cards[0]['context_steps'], [])
        self.assertEqual(cards[1]['step_index'], 1)
        self.assertEqual(len(cards[1]['context_steps']), 1)
        self.assertEqual(cards[1]['context_steps'][0]['move'], 'Separate variables')
        self.assertEqual(len(cards[2]['context_steps']), 2)

    def test_virtual_card_answer_is_move_label(self):
        response = self.client.get(f'/study/{self.topic.id}/')
        cards = response.context['flashcards_data']
        self.assertEqual(cards[0]['answer'], 'Separate variables')
        self.assertEqual(cards[0]['answer_detail'], 'dy/y = -2 dx')
```

### Step 2: Run test to verify it fails

```bash
python manage.py test study.tests.StudySessionExpansionTest -v 2
```

### Step 3: Replace the flashcard processing loop in study_session

In `study/views.py`, replace lines 312-361 (the `flashcards_data` building loop) with:

```python
    flashcards_data = []
    for fc in flashcards:
        base = {
            'id': fc.id,
            'hint': fc.hint,
            'difficulty': fc.difficulty,
            'question_type': fc.question_type,
            'uses_latex': fc.uses_latex,
            'diagram_code': fc.diagram_code,
            'diagram_type': fc.diagram_type,
            'code_snippet': fc.code_snippet,
            'code_language': fc.code_language,
            'graph_image_url': fc.generated_graph_image.url if fc.generated_graph_image else None,
            'question_image': fc.question_image.url if fc.question_image else None,
            'answer_image': fc.answer_image.url if fc.answer_image else None,
            'teacher_explanation': fc.teacher_explanation,
        }

        if fc.question_type == 'step_by_step' and fc.steps:
            steps = fc.steps
            for k, step in enumerate(steps):
                virtual = dict(base)
                virtual.update({
                    'step_index': k,
                    'step_total': len(steps),
                    'question': fc.question,
                    'context_steps': steps[:k],
                    'answer': step['move'],
                    'answer_detail': step.get('detail', ''),
                    'is_parameterized': False,
                })
                flashcards_data.append(virtual)

        elif fc.question_type == 'parameterized' and fc.parameter_spec:
            try:
                question, answer, _ = generate_parameterized_card(
                    fc.parameter_spec, fc.question_template, fc.answer_template
                )
            except Exception:
                question = fc.question_template or fc.question
                answer = fc.answer_template or fc.answer
            base.update({
                'step_index': -1,
                'step_total': None,
                'question': question,
                'answer': answer,
                'answer_detail': '',
                'context_steps': [],
                'is_parameterized': True,
            })
            flashcards_data.append(base)

        else:
            base.update({
                'step_index': -1,
                'step_total': None,
                'question': fc.question,
                'answer': fc.answer,
                'answer_detail': '',
                'context_steps': [],
                'is_parameterized': False,
            })
            flashcards_data.append(base)
```

### Step 4: Run test to verify it passes

```bash
python manage.py test study.tests.StudySessionExpansionTest -v 2
```

### Step 5: Commit

```bash
git add study/views.py study/tests.py
git commit -m "feat: expand step_by_step cards into virtual cards in study session"
```

---

## Task 4: Study Session JS — Step Card Rendering + AJAX Progress Calls

Update `study_session.html` to render step cards, make AJAX progress calls, and show the teacher explanation button.

**Files:**
- Modify: `study/templates/study/study_session.html`

### Step 1: Add step card HTML and teacher panel

Inside `{% block content %}`, after the `.flashcard-container` div (around line 229), add:

```html
<!-- Step card display (shown instead of flip card for step_by_step) -->
<div id="stepCardContainer" style="display:none; max-width: 640px; margin: 0 auto;">
    <div style="background: #f8f9fa; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;">
        <div style="font-size: 0.8rem; color: #6c757d; margin-bottom: 0.5rem;" id="stepCounter"></div>
        <strong>Problem:</strong>
        <div id="stepQuestion" style="font-size: 1.1rem; margin: 0.5rem 0 1rem;"></div>
        <div id="priorStepsContainer" style="border-top: 1px solid #dee2e6; padding-top: 0.75rem;"></div>
        <div id="nextStepPrompt" style="margin-top: 0.75rem; color: #495057; font-style: italic;">
            What is the next move?
        </div>
    </div>
    <div id="stepReveal" style="display:none; background: #e8f5e9; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;">
        <strong>Step:</strong> <span id="stepMove" style="font-size: 1.1rem;"></span>
        <div id="stepDetail" style="margin-top: 0.5rem; font-size: 0.95rem; color: #555;"></div>
    </div>
</div>

<!-- Teacher explanation panel (hidden until requested) -->
<div id="teacherPanel" style="display:none; max-width: 640px; margin: 1rem auto; background: #fff8e1; border-radius: 12px; padding: 1.5rem;">
    <strong>Teacher Explanation</strong>
    <div id="teacherText" style="margin-top: 0.75rem; line-height: 1.6;"></div>
</div>
```

Add `id="flashcard-container"` to the existing `.flashcard-container` div:
```html
<div class="flashcard-container" id="flashcard-container">
```

### Step 2: Update the button row

Replace the existing button row (around line 235) with:

```html
<div style="display: flex; gap: 1rem; justify-content: center; margin-top: 2rem; flex-wrap: wrap;">
    <button onclick="markResult(true)" class="btn" style="background: #28a745;" id="gotItBtn">Got it</button>
    <button onclick="markResult(null)" class="btn btn-secondary" id="nearlyBtn">Nearly</button>
    <button onclick="markResult(false)" class="btn btn-danger" id="missedBtn">Missed it</button>
    <button onclick="nextCard()" class="btn btn-secondary">Skip</button>
</div>
<div style="display: flex; gap: 1rem; justify-content: center; margin-top: 0.5rem; flex-wrap: wrap;">
    <button onclick="showHint()" class="btn btn-secondary" id="hintBtn">Show Hint</button>
    <button onclick="toggleTeacherExplanation()" class="btn btn-secondary" id="teacherBtn" style="display:none;">Full Explanation</button>
    <button onclick="submitFeedback()" class="btn btn-secondary" id="feedbackBtn">Feedback</button>
</div>
```

### Step 3: Replace the JavaScript block

Replace the entire `<script>` block at the bottom of the template with the following. Note: all user-supplied content is set via `textContent`, never `innerHTML`. Image elements and mermaid diagrams (server-owned content) use DOM creation or the mermaid library's own renderer.

```javascript
<script>
    const cards = JSON.parse(document.getElementById('flashcards-data').textContent);
    const studyMode = '{{ study_mode }}';
    const csrfToken = '{{ csrf_token }}';

    let currentIndex = 0;
    let cardsStudied = 0;
    let isFlipped = false;
    let isStepCard = false;
    let timerInterval = null;

    document.querySelector('.content').classList.add('mode-' + studyMode);
    const FLIP_DURATION = 650;
    const CHALLENGE_SECONDS = 30;

    function startTimer() {
        if (studyMode !== 'challenge') return;
        let timeLeft = CHALLENGE_SECONDS;
        const bar = document.getElementById('timerBar');
        bar.style.width = '100%';
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(function() {
            timeLeft -= 0.1;
            bar.style.width = Math.max(0, (timeLeft / CHALLENGE_SECONDS) * 100) + '%';
            if (timeLeft <= 0) { clearInterval(timerInterval); if (!isFlipped) revealCard(); }
        }, 100);
    }

    function stopTimer() {
        if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    }

    function loadCard() {
        if (currentIndex >= cards.length) { endSession(); return; }

        const card = cards[currentIndex];
        isStepCard = (card.question_type === 'step_by_step');
        isFlipped = false;

        document.getElementById('teacherPanel').style.display = 'none';
        document.getElementById('teacherBtn').style.display = 'none';
        document.getElementById('hint').style.display = 'none';
        document.getElementById('stepReveal').style.display = 'none';
        document.getElementById('nextStepPrompt').style.display = '';
        document.getElementById('feedbackBtn').dataset.cardId = card.id;
        document.getElementById('feedbackBtn').dataset.cardQuestion = card.question;

        if (card.teacher_explanation) {
            document.getElementById('teacherText').textContent = card.teacher_explanation;
        }

        if (isStepCard) {
            loadStepCard(card);
        } else {
            loadFlipCard(card);
        }

        document.getElementById('cardCounter').textContent = currentIndex + 1;
        document.getElementById('progressBar').style.width =
            ((currentIndex / cards.length) * 100) + '%';
        startTimer();
    }

    function loadFlipCard(card) {
        document.getElementById('flashcard-container').style.display = '';
        document.getElementById('stepCardContainer').style.display = 'none';

        const fc = document.getElementById('flashcard');
        if (fc.classList.contains('flipped')) fc.classList.remove('flipped');

        // Use textContent for all user-supplied text
        document.getElementById('question').textContent = card.question;
        document.getElementById('answer').textContent = card.answer;

        // Images: build elements safely
        setImage('questionImage', card.question_image);
        setImage('answerImage', card.answer_image);
        setImage('question-graph', card.graph_image_url);
        document.getElementById('answer-graph').textContent = '';

        // Diagrams: mermaid renders from trusted server-side diagram_code
        const qDiag = document.getElementById('question-diagram');
        qDiag.textContent = '';
        if (card.diagram_code) {
            const mermaidDiv = document.createElement('div');
            mermaidDiv.className = 'mermaid';
            mermaidDiv.textContent = card.diagram_code;
            qDiag.appendChild(mermaidDiv);
        }
        document.getElementById('answer-diagram').textContent = '';

        document.getElementById('question-code').textContent = '';
        document.getElementById('answer-code').textContent = '';

        if (studyMode !== 'challenge' && card.hint) {
            document.getElementById('hintBtn').style.display = 'inline-block';
            document.getElementById('hintText').textContent = card.hint;
        } else {
            document.getElementById('hintBtn').style.display = 'none';
        }

        if (typeof MathJax !== 'undefined') MathJax.typesetPromise();
        if (card.diagram_code && typeof mermaid !== 'undefined') mermaid.init(undefined, '.mermaid');
    }

    function loadStepCard(card) {
        document.getElementById('flashcard-container').style.display = 'none';
        document.getElementById('stepCardContainer').style.display = '';
        document.getElementById('hintBtn').style.display = 'none';

        document.getElementById('stepCounter').textContent =
            'Step ' + (card.step_index + 1) + ' of ' + card.step_total;
        document.getElementById('stepQuestion').textContent = card.question;

        const priorContainer = document.getElementById('priorStepsContainer');
        priorContainer.textContent = '';
        if (card.context_steps && card.context_steps.length > 0) {
            card.context_steps.forEach(function(s, i) {
                const div = document.createElement('div');
                div.style.cssText = 'margin-bottom: 0.4rem; color: #495057;';
                div.textContent = 'Step ' + (i + 1) + ': ' + s.move;
                priorContainer.appendChild(div);
            });
        }

        if (typeof MathJax !== 'undefined') MathJax.typesetPromise();
    }

    function setImage(containerId, url) {
        const el = document.getElementById(containerId);
        el.textContent = '';
        if (url) {
            const img = document.createElement('img');
            img.src = url;
            img.style.cssText = 'max-width:100%; max-height:200px;';
            el.appendChild(img);
        }
    }

    function revealCard() {
        stopTimer();
        if (isStepCard) {
            const card = cards[currentIndex];
            document.getElementById('stepMove').textContent = card.answer;
            document.getElementById('stepDetail').textContent = card.answer_detail || '';
            document.getElementById('stepReveal').style.display = '';
            document.getElementById('nextStepPrompt').style.display = 'none';
            if (card.teacher_explanation) {
                document.getElementById('teacherBtn').style.display = 'inline-block';
            }
            if (typeof MathJax !== 'undefined') MathJax.typesetPromise();
        } else {
            document.getElementById('flashcard').classList.add('flipped');
            const card = cards[currentIndex];
            if (card.teacher_explanation) {
                document.getElementById('teacherBtn').style.display = 'inline-block';
            }
        }
        isFlipped = true;
    }

    // Override flashcard click to use revealCard
    document.getElementById('flashcard').onclick = function() {
        if (!isFlipped) revealCard();
    };

    function toggleTeacherExplanation() {
        const panel = document.getElementById('teacherPanel');
        panel.style.display = (panel.style.display === 'none') ? '' : 'none';
    }

    function showHint() {
        document.getElementById('hint').style.display = 'block';
    }

    function postProgress(cardId, stepIndex, correct) {
        const url = '/flashcard/' + cardId + '/progress/';
        const body = new URLSearchParams({
            csrfmiddlewaretoken: csrfToken,
            correct: correct ? 'true' : 'false',
            step_index: stepIndex,
        });
        fetch(url, { method: 'POST', body: body }).catch(function() {});
    }

    function markResult(correct) {
        if (!isFlipped) { revealCard(); return; }
        const card = cards[currentIndex];
        postProgress(card.id, card.step_index, correct === true);
        cardsStudied++;
        moveToNext();
    }

    function moveToNext() {
        stopTimer();
        currentIndex++;
        if (isStepCard) {
            loadCard();
        } else {
            if (isFlipped) {
                document.getElementById('flashcard').classList.remove('flipped');
                setTimeout(loadCard, FLIP_DURATION);
            } else {
                loadCard();
            }
        }
    }

    function nextCard() {
        moveToNext();
    }

    function submitFeedback() {
        const btn = document.getElementById('feedbackBtn');
        const question = (btn.dataset.cardQuestion || '').substring(0, 60);
        const cardId = btn.dataset.cardId || '';
        if (typeof openFeedbackModal === 'function') {
            document.getElementById('feedbackTitle').value = 'Flashcard Feedback: ' + question;
            document.getElementById('feedbackType').value = 'content';
            document.getElementById('feedbackDescription').value =
                'Flashcard ID: ' + cardId + '\n\nPlease describe the issue:\n';
            openFeedbackModal();
        }
    }

    function endSession() {
        stopTimer();
        document.getElementById('cardsStudied').value = cardsStudied;
        document.getElementById('endSessionForm').submit();
    }

    loadCard();
</script>
```

### Step 4: Manual test

```bash
python manage.py runserver
```

1. Create a `step_by_step` card with 3 steps via `/admin/`
2. Enroll in the course, start a study session
3. Verify: step prompt shown (no flip), reveal works, prior steps shown on cards 2+
4. Verify: Got it / Nearly / Missed it all call the progress endpoint (check DevTools Network tab)
5. Verify: Full Explanation button appears after reveal if teacher_explanation is set

### Step 5: Run full test suite

```bash
python manage.py test study -v 2
```

### Step 6: Commit

```bash
git add study/templates/study/study_session.html
git commit -m "feat: step card UI with active recall reveal, teacher explanation, AJAX progress"
```

---

## Task 5: Adaptive Difficulty — TopicScore + Prerequisite Nudge

**Files:**
- Modify: `study/views.py`
- Modify: `study/templates/study/study_session.html`

### Step 1: Write failing test

In `study/tests.py`, add:

```python
class TopicScoreTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='scoreuser', password='pass')
        course = Course.objects.create(name='Course', created_by=self.user)
        self.topic = Topic.objects.create(course=course, name='Topic')
        from .models import CourseEnrollment, StudySession
        CourseEnrollment.objects.create(user=self.user, course=course)
        self.session = StudySession.objects.create(user=self.user, topic=self.topic)
        for i in range(5):
            card = Flashcard.objects.create(
                topic=self.topic, question=f'Q{i}', answer=f'A{i}'
            )
            FlashcardProgress.objects.create(
                user=self.user, flashcard=card, step_index=-1,
                confidence_level=1, times_reviewed=2
            )
        self.client.login(username='scoreuser', password='pass')

    def test_end_session_updates_topic_score(self):
        response = self.client.post(
            f'/session/{self.session.id}/end/',
            {'cards_studied': '5'}
        )
        self.assertEqual(response.status_code, 302)
        ts = TopicScore.objects.filter(user=self.user, topic=self.topic).first()
        self.assertIsNotNone(ts)
        self.assertGreater(ts.attempt_count, 0)
```

### Step 2: Run test to verify it fails

```bash
python manage.py test study.tests.TopicScoreTest -v 2
```

### Step 3: Add _update_topic_score helper

In `study/views.py`, add this function near the other helpers (`_calculate_streak`, `_award_badges`):

```python
def _update_topic_score(user, topic):
    """Recompute and save rolling confidence score for user/topic."""
    recent_progress = FlashcardProgress.objects.filter(
        flashcard__topic=topic,
        user=user,
    ).order_by('-last_reviewed')[:10]

    if not recent_progress:
        return

    # confidence_level is 0-5; normalise to 0.0-1.0
    avg = sum(p.confidence_level for p in recent_progress) / (5.0 * len(recent_progress))

    TopicScore.objects.update_or_create(
        user=user,
        topic=topic,
        defaults={
            'score': round(avg, 3),
            'attempt_count': FlashcardProgress.objects.filter(
                flashcard__topic=topic, user=user
            ).count(),
        }
    )
```

Add `TopicScore` to the import at line 15:
```python
from .models import (Course, Topic, Flashcard, StudySession, FlashcardProgress,
                     CourseEnrollment, StudyPreference, StudyGoal,
                     AccountabilityLink, AccountabilityRelationship,
                     UserBadge, BADGE_DEFINITIONS, TopicScore)
```

In `end_study_session`, after the `_award_badges` call, add:
```python
        _update_topic_score(request.user, session.topic)
```

### Step 4: Add prerequisite nudge logic to study_session view

Before the `return render(...)` at the end of `study_session`, add:

```python
    nudge_topics = []
    my_score = TopicScore.objects.filter(user=request.user, topic=topic).first()
    if my_score and my_score.score < 0.4 and my_score.attempt_count >= 10:
        for prereq in topic.prerequisites.all():
            prereq_score = TopicScore.objects.filter(user=request.user, topic=prereq).first()
            if prereq_score is None or prereq_score.score < 0.7:
                nudge_topics.append({
                    'topic': prereq,
                    'score_pct': int(prereq_score.score * 100) if prereq_score else None,
                })
```

Pass `nudge_topics` in the render context.

### Step 5: Add nudge UI to study_session.html

At the top of `{% block content %}` before the session heading, add:

```html
{% if nudge_topics %}
<div style="background:#fff8e1;border:1px solid #ffe082;border-radius:10px;padding:1.25rem;margin-bottom:1.5rem;max-width:640px;margin-left:auto;margin-right:auto;">
    <strong>Heads up</strong>
    <p style="margin:0.5rem 0;">Your recent scores on <em>{{ topic.name }}</em> suggest some prerequisite topics may need reinforcement.</p>
    <ul style="margin:0.5rem 0 0.75rem;padding-left:1.25rem;">
    {% for item in nudge_topics %}
        <li>
            <a href="{% url 'study_session' item.topic.id %}">{{ item.topic.name }}</a>
            {% if item.score_pct is not None %}(score: {{ item.score_pct }}%){% else %}(no recent activity){% endif %}
        </li>
    {% endfor %}
    </ul>
    <a href="?" class="btn btn-secondary" style="font-size:0.85rem;padding:0.3rem 0.75rem;">Dismiss</a>
</div>
{% endif %}
```

### Step 6: Run test to verify it passes

```bash
python manage.py test study.tests.TopicScoreTest -v 2
```

### Step 7: Run full suite

```bash
python manage.py test study -v 2
```

### Step 8: Commit

```bash
git add study/views.py study/templates/study/study_session.html study/tests.py
git commit -m "feat: adaptive difficulty with TopicScore and prerequisite regression nudge"
```

---

## Task 6: Feedback Modal — Content vs Bug Split

**Files:**
- Modify: `study/templates/study/base.html`
- Modify: `study/views.py` (submit_feedback view)

### Step 1: Read the existing feedback modal

```bash
grep -n "feedbackModal\|openFeedbackModal\|feedbackType\|submit_feedback\|feedbackCategory" \
  /home/stewards_path/study-platform/study/templates/study/base.html | head -20
grep -n "submit_feedback\|github\|label" \
  /home/stewards_path/study-platform/study/views.py | head -20
```

Read the full `submit_feedback` view to understand how it calls GitHub before making changes.

### Step 2: Add category radio to the feedback modal in base.html

Find the feedback form in `base.html`. Before the title/description inputs, add:

```html
<div style="margin-bottom:1rem;">
    <label style="display:block;margin-bottom:0.4rem;font-weight:600;">Issue type</label>
    <label style="margin-right:1.5rem;">
        <input type="radio" name="feedbackCategory" value="content" checked>
        Content issue
        <span style="font-size:0.8rem;color:#666;">(wrong answer, confusing step, needs more cards)</span>
    </label><br>
    <label>
        <input type="radio" name="feedbackCategory" value="bug">
        Bug / UX issue
        <span style="font-size:0.8rem;color:#666;">(page crash, broken feature)</span>
    </label>
</div>
```

### Step 3: Update submit_feedback in views.py

Read the full `submit_feedback` function first. Then add label selection:

```python
    category = request.POST.get('feedbackCategory', 'bug')
    label = 'content-feedback' if category == 'content' else 'bug'
    # Use `label` in the GitHub Issues API call labels list
```

Apply this by finding where the labels are set in the GitHub API call and substituting `label`.

### Step 4: Manual test

Start the server, trigger the feedback button from a study session, select "Content issue", submit. Check GitHub Issues for the `content-feedback` label.

### Step 5: Commit

```bash
git add study/templates/study/base.html study/views.py
git commit -m "feat: feedback modal content vs bug split with content-feedback label"
```

---

## Task 7: Admin + FlashcardForm Support for steps

**Files:**
- Modify: `study/forms.py`
- Modify: `study/admin.py`

### Step 1: Read existing FlashcardForm

Read `study/forms.py` in full before editing.

### Step 2: Add steps_json field and teacher_explanation to FlashcardForm

In `study/forms.py`, add a `steps_json` CharField and `teacher_explanation` to the form. Add a `clean_steps_json` method that validates the JSON structure. In `save()`, write cleaned steps to `instance.steps`. Also add `teacher_explanation` to `Meta.fields`.

Key validation:

```python
def clean_steps_json(self):
    raw = self.cleaned_data.get('steps_json', '').strip()
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise forms.ValidationError(f'Invalid JSON: {exc}')
    if not isinstance(parsed, list):
        raise forms.ValidationError('Steps must be a JSON array.')
    for i, step in enumerate(parsed):
        if 'move' not in step:
            raise forms.ValidationError(f'Step {i} is missing required "move" key.')
    return parsed
```

### Step 3: Update admin.py

Read `study/admin.py` in full. Add a fieldset for step fields in `FlashcardAdmin`:

```python
('Step-by-Step Fields', {
    'fields': ('steps', 'teacher_explanation'),
    'classes': ('collapse',),
}),
```

### Step 4: Run full test suite

```bash
python manage.py test study -v 2
```

### Step 5: Commit

```bash
git add study/forms.py study/admin.py
git commit -m "feat: form and admin support for steps JSON and teacher_explanation"
```

---

## Final Verification Checklist

Run these before declaring the feature complete:

```bash
python manage.py test study -v 2
```

Manual checks:
- [ ] Create a `step_by_step` card with 3 steps via `/admin/`
- [ ] Study session shows step card UI (problem + prior steps, no flip)
- [ ] Revealing each step shows the move label + detail
- [ ] Got it / Nearly / Missed it make AJAX calls to `/flashcard/N/progress/` (check DevTools)
- [ ] Full Explanation button appears after reveal when `teacher_explanation` is set
- [ ] After 10+ low-confidence attempts on a topic with a prerequisite, nudge appears at session start
- [ ] Feedback modal shows content/bug radio; content issues get `content-feedback` GitHub label
- [ ] `feedback/AGENT_INSTRUCTIONS.md` and `feedback/resolved.md` are in the repo
