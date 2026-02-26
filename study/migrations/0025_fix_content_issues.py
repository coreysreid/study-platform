from django.db import migrations


def fix_content_issues(apps, schema_editor):
    Flashcard = apps.get_model('study', 'Flashcard')

    # ------------------------------------------------------------------
    # Issue #41 — "Formula for average (real) power P."
    # uses_latex=True but answer used Unicode symbols instead of LaTeX
    # delimiters, so MathJax never processed it.
    # ------------------------------------------------------------------
    card = Flashcard.objects.filter(
        question='Formula for average (real) power P.'
    ).first()
    if card:
        card.answer = (
            '$P = \\frac{1}{2}V_m I_m \\cos\\phi = V_{rms}I_{rms}\\cos\\phi$. '
            'Units: watts (W). Only resistive components dissipate real power.'
        )
        card.uses_latex = True
        card.save()

    # ------------------------------------------------------------------
    # Issue #40 — "Complete the square: x² + 6x + 2 = 0"
    # Step 2 was missing the (b/2)² formula; add it and show all working.
    # ------------------------------------------------------------------
    card = Flashcard.objects.filter(
        question='Complete the square: x² + 6x + 2 = 0'
    ).first()
    if card:
        card.steps = [
            {'move': 'Move constant to right', 'detail': '$x^2 + 6x = -2$'},
            {'move': 'Apply $(b/2)^2$ rule', 'detail': '$b = 6$, so $(b/2)^2 = (6/2)^2 = 9$. Add 9 to both sides: $x^2 + 6x + 9 = -2 + 9$'},
            {'move': 'Factor left side', 'detail': '$(x + 3)^2 = 7$'},
            {'move': 'Solve for x', 'detail': '$x + 3 = \\pm\\sqrt{7}$, therefore $x = -3 \\pm \\sqrt{7}$'},
        ]
        card.answer = '$(x+3)^2 = 7 \\Rightarrow x = -3 \\pm \\sqrt{7}$'
        card.save()

    # ------------------------------------------------------------------
    # Issue #39 — "What is the short-circuit current if V=10V …"
    # Misleading terminology — "short-circuit current" implies a Thevenin
    # context that wasn't given. Rephrase as a straightforward Ohm's law
    # question.
    # ------------------------------------------------------------------
    card = Flashcard.objects.filter(
        question='What is the short-circuit current if V=10V is applied to R=5\u03a9?'
    ).first()
    if card:
        card.question = 'Find the current through a 5\u03a9 resistor connected in series with a 10V independent voltage source.'
        card.answer = "By Ohm's law: $I = V/R = 10/5 = 2\\,\\text{A}$."
        card.save()


def reverse_fn(apps, schema_editor):
    pass  # intentional no-op


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0024_flashcards_industrial_automation'),
    ]

    operations = [
        migrations.RunPython(fix_content_issues, reverse_fn),
    ]
