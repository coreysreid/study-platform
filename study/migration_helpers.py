"""
Utility functions used by data migrations.

Extracted here so they can be imported independently by both migration files
(which receive a historical model class via apps.get_model()) and tests (which
pass the live model class directly).
"""

# ---------------------------------------------------------------------------
# Migration 0030 — trig exact-values flashcard split
# ---------------------------------------------------------------------------

TRIG_EXACT_VALUES_QUESTION = 'What are the exact values of sin, cos, tan for 30°, 45°, 60°?'

TRIG_ATOMIC_CARDS = [
    # 30°
    {'question': 'What is sin(30°)?',
     'answer': '$\\sin 30° = \\dfrac{1}{2}$',
     'difficulty': 'easy'},
    {'question': 'What is cos(30°)?',
     'answer': '$\\cos 30° = \\dfrac{\\sqrt{3}}{2}$',
     'difficulty': 'easy'},
    {'question': 'What is tan(30°)?',
     'answer': '$\\tan 30° = \\dfrac{1}{\\sqrt{3}} = \\dfrac{\\sqrt{3}}{3}$',
     'difficulty': 'easy'},
    # 45°
    {'question': 'What is sin(45°)?',
     'answer': '$\\sin 45° = \\dfrac{1}{\\sqrt{2}} = \\dfrac{\\sqrt{2}}{2}$',
     'difficulty': 'easy'},
    {'question': 'What is cos(45°)?',
     'answer': '$\\cos 45° = \\dfrac{1}{\\sqrt{2}} = \\dfrac{\\sqrt{2}}{2}$',
     'difficulty': 'easy'},
    {'question': 'What is tan(45°)?',
     'answer': '$\\tan 45° = 1$',
     'difficulty': 'easy'},
    # 60°
    {'question': 'What is sin(60°)?',
     'answer': '$\\sin 60° = \\dfrac{\\sqrt{3}}{2}$',
     'difficulty': 'easy'},
    {'question': 'What is cos(60°)?',
     'answer': '$\\cos 60° = \\dfrac{1}{2}$',
     'difficulty': 'easy'},
    {'question': 'What is tan(60°)?',
     'answer': '$\\tan 60° = \\sqrt{3}$',
     'difficulty': 'easy'},
]


def split_trig_exact_values(Flashcard):
    """
    Replace any combined sin/cos/tan exact-values flashcard(s) with 9 atomic cards.

    Accepts any Flashcard model class — either a historical class from
    apps.get_model() (for use inside migrations) or the live class (for tests).

    Idempotent: skips atomic cards that already exist for the topic.
    Handles multiple copies of the combined card across different topics.
    """
    combined_qs = Flashcard.objects.filter(question=TRIG_EXACT_VALUES_QUESTION)

    if not combined_qs.exists():
        return  # already fixed or never existed

    for combined in combined_qs:
        topic = combined.topic
        combined.delete()

        for card_data in TRIG_ATOMIC_CARDS:
            if Flashcard.objects.filter(topic=topic, question=card_data['question']).exists():
                continue
            Flashcard.objects.create(
                topic=topic,
                question=card_data['question'],
                answer=card_data['answer'],
                difficulty=card_data['difficulty'],
                question_type='standard',
                uses_latex=True,
            )
