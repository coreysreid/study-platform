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

## Parameterized/Randomized Cards (Future Feature)

**Concept**: Create cards that generate new values each time they're presented, preventing memorization and forcing true understanding of the solving process.

**Example - Addition Card:**
```python
# Future implementation concept
flashcard = Flashcard.objects.create(
    topic=topic,
    question_template="What is {a} + {b}?",
    answer_template="{c}",
    parameter_spec={
        'a': {'type': 'integer', 'min': 1, 'max': 100},
        'b': {'type': 'integer', 'min': 1, 'max': 100},
        'c': {'type': 'computed', 'formula': 'a + b'}
    },
    question_type='parameterized'
)
```

Each presentation generates new random values for `a` and `b`, and computes `c` automatically.

**Benefits:**
- Prevents memorization of specific answers
- Emphasizes understanding the solving process
- Unlimited practice variations from a single card
- Can be applied to any mathematical operation or pattern

**Potential Applications:**
- Basic arithmetic (addition, subtraction, multiplication, division)
- Algebraic simplification with different coefficients
- Calculus problems with varying functions
- Matrix operations with different dimensions
- Trigonometric identities with different angles

**Implementation Notes:**
- Would require new `question_template` and `answer_template` fields
- Need `parameter_spec` JSON field to define variable ranges and computations
- Frontend would need to render templates with generated values
- Could include verification that computed answers are correct

**Note**: This is a planned feature. Current implementation uses static question/answer fields.

## Future Enhancements

The groundwork is in place for:
- **Parameterized cards** (see above section)
- Automatic difficulty adjustment based on user performance
- Skill mastery tracking across all topics
- Prerequisite suggestion algorithm
- Adaptive learning paths
- Analytics dashboards showing strengths and weaknesses
