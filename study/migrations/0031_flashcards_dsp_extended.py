from django.db import migrations


class Migration(migrations.Migration):
    """
    Merge migration: reconciles the two independent 0030 migrations:
      - 0030_flashcards_dsp_extended  (DSP atomic flashcard expansion)
      - 0030_split_trig_exact_values_flashcard  (trig exact-values split from main)
    Both depend on 0029_restructure_mathematics; this merge makes them a single leaf node.
    """

    dependencies = [
        ('study', '0030_flashcards_dsp_extended'),
        ('study', '0030_split_trig_exact_values_flashcard'),
    ]

    operations = [
    ]
