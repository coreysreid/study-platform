"""
Issue #44 — Flashcard "What are the exact values of sin, cos, tan for 30°, 45°, 60°?"
is not atomic: it bundles 9 distinct facts into one card.

Replace it with 9 individual flashcards, one per (angle, function) combination.
"""
from django.db import migrations


ATOMIC_CARDS = [
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


def split_trig_card(apps, schema_editor):
    Flashcard = apps.get_model('study', 'Flashcard')

    combined = Flashcard.objects.filter(
        question='What are the exact values of sin, cos, tan for 30°, 45°, 60°?'
    ).first()

    if combined is None:
        return  # already fixed or never existed

    topic = combined.topic
    combined.delete()

    for card_data in ATOMIC_CARDS:
        # Idempotent: skip if a card with this question already exists for the topic
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


def reverse_fn(apps, schema_editor):
    pass  # intentional no-op


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0029_restructure_mathematics'),
    ]

    operations = [
        migrations.RunPython(split_trig_card, reverse_fn),
    ]
