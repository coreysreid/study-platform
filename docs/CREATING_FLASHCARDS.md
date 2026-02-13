# Creating Flashcards Guide

This guide explains how to create different types of flashcards with the enhanced features.

## Flashcard Types

### 1. Standard Q&A Flashcards

Traditional flashcards for definitions, theorems, and conceptual understanding.

**Example - Basic Arithmetic:**
```python
from study.models import Topic, Flashcard, Skill

topic = Topic.objects.get(name='Basic Arithmetic & Number Sense')
skill = Skill.objects.get(name='fraction_operations')

flashcard = Flashcard.objects.create(
    topic=topic,
    question="What is 2/3 + 1/4?",
    answer="11/12 (Find common denominator: 8/12 + 3/12 = 11/12)",
    hint="Find a common denominator first",
    difficulty='easy',
    question_type='standard'
)
flashcard.skills.add(skill)
```

### 2. Multiple Choice Questions

Present options for students to choose from. Great for identifying correct formulas, selecting appropriate methods, or recognizing patterns.

**Example - Differential Calculus:**
```python
from study.models import Topic, Flashcard, MultipleChoiceOption, Skill

topic = Topic.objects.get(name='Differential Calculus')
skills = Skill.objects.filter(name__in=['derivative_calculation', 'differentiation_rules'])

flashcard = Flashcard.objects.create(
    topic=topic,
    question="What is the derivative of f(x) = x³?",
    answer="3x²",
    hint="Use the power rule: d/dx(xⁿ) = nxⁿ⁻¹",
    difficulty='easy',
    question_type='multiple_choice'
)
flashcard.skills.set(skills)

# Add options
MultipleChoiceOption.objects.create(
    flashcard=flashcard,
    option_text="3x²",
    is_correct=True,
    order=1
)
MultipleChoiceOption.objects.create(
    flashcard=flashcard,
    option_text="x²",
    is_correct=False,
    order=2
)
MultipleChoiceOption.objects.create(
    flashcard=flashcard,
    option_text="3x³",
    is_correct=False,
    order=3
)
MultipleChoiceOption.objects.create(
    flashcard=flashcard,
    option_text="x⁴",
    is_correct=False,
    order=4
)
```

### 3. Step-by-Step Problems

Break complex problems into discrete steps to help students understand the logical flow of problem-solving.

**Example - Integration:**
```python
from study.models import Topic, Flashcard, Skill

topic = Topic.objects.get(name='Integral Calculus')
skills = Skill.objects.filter(name__in=['integration_techniques', 'definite_integrals'])

# Step 1: Identify the problem type
flashcard1 = Flashcard.objects.create(
    topic=topic,
    question="Solve ∫(2x + 3)dx. Step 1: What type of integration problem is this?",
    answer="This is a basic polynomial integration problem using the power rule.",
    hint="Look at the form of the function being integrated",
    difficulty='easy',
    question_type='step_by_step'
)
flashcard1.skills.set(skills)

# Step 2: Apply the method
flashcard2 = Flashcard.objects.create(
    topic=topic,
    question="Solve ∫(2x + 3)dx. Step 2: What is the next step after identifying it as polynomial integration?",
    answer="Apply the power rule to each term separately: ∫2x dx + ∫3 dx",
    hint="Integrate term by term",
    difficulty='easy',
    question_type='step_by_step'
)
flashcard2.skills.set(skills)

# Step 3: Execute
flashcard3 = Flashcard.objects.create(
    topic=topic,
    question="Solve ∫(2x + 3)dx. Step 3: What is the result after applying the power rule?",
    answer="x² + 3x + C (where C is the constant of integration)",
    hint="Remember to add the constant of integration",
    difficulty='easy',
    question_type='step_by_step'
)
flashcard3.skills.set(skills)
```

## Skill Tagging Strategy

When creating flashcards, tag them with the foundational skills required to solve them. This enables the system to:
1. Identify weak areas when students answer incorrectly
2. Suggest prerequisite topics to review
3. Track mastery of specific skills over time

### Example: Complex Calculus Problem

```python
topic = Topic.objects.get(name='Differential Calculus')

# This problem requires multiple skills
flashcard = Flashcard.objects.create(
    topic=topic,
    question="Find dy/dx for y = (3x² + 2)⁵",
    answer="dy/dx = 5(3x² + 2)⁴ · 6x = 30x(3x² + 2)⁴",
    hint="This requires the chain rule",
    difficulty='medium',
    question_type='standard'
)

# Tag with all required skills
required_skills = Skill.objects.filter(name__in=[
    'derivative_calculation',
    'differentiation_rules',  # Chain rule
    'polynomial_operations',  # For the inner function
    'exponent_rules'  # For understanding the power
])
flashcard.skills.set(required_skills)
```

## Building a Progressive Learning Path

### Example: Quadratic Equations Series

Start with basic concepts and build up to complex applications:

```python
topic = Topic.objects.get(name='Algebra Fundamentals')
skills = Skill.objects.filter(name__in=['quadratic_equations', 'factoring'])

# Easy: Recognize form
Flashcard.objects.create(
    topic=topic,
    question="What is the standard form of a quadratic equation?",
    answer="ax² + bx + c = 0, where a ≠ 0",
    difficulty='easy',
    question_type='standard'
).skills.set(skills)

# Medium: Solve by factoring
Flashcard.objects.create(
    topic=topic,
    question="Solve: x² - 5x + 6 = 0",
    answer="x = 2 or x = 3 (Factor as (x-2)(x-3) = 0)",
    hint="Factor the quadratic first",
    difficulty='medium',
    question_type='standard'
).skills.set(skills)

# Hard: Use quadratic formula
Flashcard.objects.create(
    topic=topic,
    question="Solve: 2x² + 3x - 5 = 0 using the quadratic formula",
    answer="x = 1 or x = -2.5. Using x = [-b ± √(b²-4ac)]/(2a)",
    hint="Identify a=2, b=3, c=-5, then apply the formula",
    difficulty='hard',
    question_type='standard'
).skills.set(skills)
```

## Bulk Import Strategy

For creating many flashcards, consider creating a CSV or JSON file and writing a script:

```python
import csv
from study.models import Topic, Flashcard, Skill

def import_flashcards_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            topic = Topic.objects.get(name=row['topic'])
            flashcard = Flashcard.objects.create(
                topic=topic,
                question=row['question'],
                answer=row['answer'],
                hint=row['hint'],
                difficulty=row['difficulty'],
                question_type=row['question_type']
            )
            
            # Add skills
            skill_names = row['skills'].split(',')
            skills = Skill.objects.filter(name__in=skill_names)
            flashcard.skills.set(skills)
```

## Best Practices

1. **Tag Comprehensively**: Don't just tag the main skill - include all foundational skills needed
2. **Progressive Difficulty**: Create easy, medium, and hard cards for each concept
3. **Clear Explanations**: Answers should explain the reasoning, not just give the result
4. **Good Hints**: Hints should guide without giving away the answer
5. **Step-by-Step for Complex Problems**: Break down multi-step problems into individual cards
6. **Multiple Choice for Misconceptions**: Use wrong options that represent common mistakes
7. **Test Your Cards**: Try solving them yourself to ensure clarity

## Next Steps

1. Start with foundational topics (Basic Arithmetic, Algebra)
2. Create flashcards for each topic as needed (no artificial limits - build as comprehensive as required)
3. Test the cards with actual study sessions
4. Gather feedback and refine
5. Gradually build out more advanced topics
6. Implement the review loop algorithm to suggest prerequisite topics

## Parameterized/Randomized Cards (v2.0 - Implemented!)

**Status**: ✅ Fully implemented and available!

Create cards that generate new random values each time they're presented, preventing memorization and forcing true understanding of the solving process.

### Quick Start

Use the management command to create 7 example parameterized cards:
```bash
python manage.py create_example_parameterized_cards --user=<your_username>
```

### 4. Parameterized Flashcards

**Example - Simple Addition:**
```python
from study.models import Topic, Flashcard, Skill

topic = Topic.objects.get(name='Basic Arithmetic & Number Sense')
skill = Skill.objects.get(name='basic_arithmetic')

flashcard = Flashcard.objects.create(
    topic=topic,
    question="Placeholder (not used for parameterized)",
    answer="Placeholder (not used for parameterized)",
    question_type='parameterized',
    question_template="What is {a} + {b}?",
    answer_template="{c}",
    parameter_spec={
        'variables': {
            'a': {'type': 'random_int', 'min': 1, 'max': 50},
            'b': {'type': 'random_int', 'min': 1, 'max': 50},
            'c': {'type': 'computed', 'formula': 'a + b'}
        }
    },
    hint="Add the two numbers together",
    difficulty='easy'
)
flashcard.skills.add(skill)
```

**Result**: Each time this card is presented, it generates new random values:
- "What is 23 + 17?" → "40"
- "What is 8 + 42?" → "50"
- "What is 31 + 19?" → "50"
- ... infinite variations!

### Variable Types

**1. random_int** - Random integer in range
```python
{'type': 'random_int', 'min': 1, 'max': 100}
```

**2. random_float** - Random decimal with precision
```python
{'type': 'random_float', 'min': 0.0, 'max': 10.0, 'precision': 2}
```

**3. random_choice** - Pick from list
```python
{'type': 'random_choice', 'choices': [30, 45, 60, 90]}
```

**4. computed** - Calculate from other variables
```python
{'type': 'computed', 'formula': 'a + b'}
{'type': 'computed', 'formula': 'sqrt(a**2 + b**2)'}  # Pythagorean theorem
```

### Advanced Examples

**Example - Pythagorean Theorem:**
```python
flashcard = Flashcard.objects.create(
    topic=topic,
    question="Not used",
    answer="Not used",
    question_type='parameterized',
    question_template="A right triangle has legs of length {a} and {b}. What is the hypotenuse? (Round to 2 decimal places)",
    answer_template="{c}",
    parameter_spec={
        'variables': {
            'a': {'type': 'random_int', 'min': 3, 'max': 12},
            'b': {'type': 'random_int', 'min': 3, 'max': 12},
            'c': {'type': 'computed', 'formula': 'round(sqrt(a**2 + b**2), 2)'}
        },
        'precision': 2
    },
    hint="Use the Pythagorean theorem: c² = a² + b²",
    difficulty='medium'
)
```

**Example - Division with Clean Results (using constraints):**
```python
flashcard = Flashcard.objects.create(
    topic=topic,
    question="Not used",
    answer="Not used", 
    question_type='parameterized',
    question_template="What is {a} ÷ {b}?",
    answer_template="{c}",
    parameter_spec={
        'variables': {
            'b': {'type': 'random_int', 'min': 2, 'max': 10},
            'c': {'type': 'random_int', 'min': 2, 'max': 12},
            'a': {'type': 'computed', 'formula': 'b * c'}
        },
        'constraints': ['a % b == 0']  # Ensure no remainder
    },
    hint="Divide the first number by the second",
    difficulty='medium'
)
```

### Constraints

Use constraints to ensure valid parameter combinations:

```python
'constraints': [
    'a > b',              # Ensure a is greater than b
    'a % b == 0',         # Ensure a is divisible by b
    'a - b > 10'          # Ensure difference is at least 10
]
```

### Available Math Functions

In computed formulas, you can use:
- Basic: `+`, `-`, `*`, `/`, `**` (power), `%` (modulo)
- Math functions: `sqrt()`, `abs()`, `round()`, `pow()`
- Trigonometry: `sin()`, `cos()`, `tan()`
- Logarithms: `log()`, `log10()`, `exp()`

### Benefits

1. **Prevents Memorization** - Students can't memorize answers, must understand process
2. **Unlimited Practice** - One card definition creates infinite variations
3. **Efficient Content Creation** - Create one card instead of hundreds
4. **Better Assessment** - True measure of understanding, not recall
5. **Adaptive Difficulty** - Can adjust parameter ranges based on performance

### Complete Example Set

See the `create_example_parameterized_cards` management command for 7 complete examples:
1. Simple Addition
2. Simple Subtraction
3. Multiplication
4. Division (clean results)
5. Fraction Addition
6. Pythagorean Theorem
7. Percentage Calculation

For full design documentation, see `docs/PARAMETERIZED_CARDS_DESIGN.md`.

## Future Enhancements

The groundwork is in place for:
- **Parameterized cards** (see above section)
- Automatic difficulty adjustment based on user performance
- Skill mastery tracking across all topics
- Prerequisite suggestion algorithm
- Adaptive learning paths
- Analytics dashboards showing strengths and weaknesses
