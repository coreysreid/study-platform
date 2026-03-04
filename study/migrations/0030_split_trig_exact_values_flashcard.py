"""
Issue #44 — Flashcard "What are the exact values of sin, cos, tan for 30°, 45°, 60°?"
is not atomic: it bundles 9 distinct facts into one card.

Replace it with 9 individual flashcards, one per (angle, function) combination.
"""
from django.db import migrations
from study.migration_helpers import split_trig_exact_values


def split_trig_card(apps, schema_editor):
    split_trig_exact_values(apps.get_model('study', 'Flashcard'))


def reverse_fn(apps, schema_editor):
    pass  # intentional no-op


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0029_restructure_mathematics'),
    ]

    operations = [
        migrations.RunPython(split_trig_card, reverse_fn),
    ]

