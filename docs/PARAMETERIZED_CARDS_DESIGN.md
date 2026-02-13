# Parameterized/Randomized Flashcards - Design Document

> **Status**: ✅ IMPLEMENTED (v2.0) - This feature is fully functional and available for use.

> **Implementation Date**: February 2026

> **Documentation Sync Note**: This document now serves as both design specification and implementation reference.

## Problem Statement

Traditional static flashcards can be memorized rather than understood. A student might remember "2 + 3 = 5" without truly understanding addition. When faced with "7 + 9 = ?", they struggle because they memorized specific answers rather than the solving process.

## Solution: Parameterized Cards

Create flashcards that generate new random values each time they're presented, forcing students to understand and apply the solving process rather than memorize specific answers.

## Core Concept

Instead of storing:
```
Question: "What is 2 + 3?"
Answer: "5"
```

Store:
```
Question Template: "What is {a} + {b}?"
Answer Template: "{c}"
Parameters: {
  a: random integer 1-100,
  b: random integer 1-100,
  c: computed as a + b
}
```

Each presentation generates new values, creating unlimited variations from a single card definition.

## Use Cases

### 1. Basic Arithmetic
**Addition**: `{a} + {b} = ?`
- Range: 1-100 for beginners, 1-1000 for advanced
- Prevents memorization of sums
- Infinite practice variations

**Subtraction**: `{a} - {b} = ?`
- Ensure a > b for positive results
- Or allow negative numbers for advanced students

**Multiplication**: `{a} × {b} = ?`
- Start with single digits (1-9)
- Progress to larger numbers

**Division**: `{a} ÷ {b} = ?`
- Ensure a is divisible by b for clean answers
- Or teach remainders/decimals

### 2. Algebraic Simplification
**Example**: Simplify `{a}x + {b}x`
- Parameters: a, b (random integers)
- Answer: `{c}x` where c = a + b

**Example**: Expand `{a}(x + {b})`
- Answer: `{a}x + {c}` where c = a × b

### 3. Solving Equations
**Linear equations**: `{a}x + {b} = {c}`
- Generate a, b, c
- Answer: `x = {d}` where d = (c - b) / a
- Ensure a ≠ 0

**Quadratic**: `x² + {b}x + {c} = 0`
- Generate b, c such that equation has integer solutions
- Use factored form: (x - r₁)(x - r₂) to ensure solvability

### 4. Calculus
**Derivatives**: `d/dx({a}x^{n})`
- Random coefficient a
- Random power n
- Answer: `{a*n}x^{n-1}`

**Integrals**: `∫{a}x^{n} dx`
- Answer: `{a/(n+1)}x^{n+1} + C`
- Ensure n ≠ -1

### 5. Trigonometry
**Special angles**: `sin({angle}°)`
- angle: random from [0, 30, 45, 60, 90, 180, 270, 360]
- Answer from lookup table

**Identity**: `sin²({θ}) + cos²({θ}) = ?`
- Always equals 1, but reinforces understanding

### 6. Matrix Operations
**Matrix addition**: Add two 2×2 matrices with random integer elements
**Determinant**: `det([[{a}, {b}], [{c}, {d}]])`
- Answer: `{a*d - b*c}`

### 7. Unit Conversions
**Example**: Convert `{value} {from_unit}` to `{to_unit}`
- Random value
- Random compatible unit pairs
- Computed conversion

## Data Model Design

### Enhanced Flashcard Model

```python
class Flashcard(models.Model):
    # ... existing fields ...
    
    # New fields for parameterized cards
    question_template = models.TextField(
        blank=True,
        help_text="Template with {variable} placeholders. Used when question_type='parameterized'"
    )
    answer_template = models.TextField(
        blank=True,
        help_text="Template with {variable} placeholders for the answer"
    )
    parameter_spec = models.JSONField(
        blank=True,
        null=True,
        help_text="JSON specification of parameters, ranges, and computations"
    )
    
    # Add 'parameterized' to QUESTION_TYPES
    QUESTION_TYPES = [
        ('standard', 'Standard Q&A'),
        ('multiple_choice', 'Multiple Choice'),
        ('step_by_step', 'Step-by-Step Problem'),
        ('parameterized', 'Parameterized/Randomized'),  # NEW
    ]
```

### Parameter Specification Format

```python
{
    "variables": {
        "a": {
            "type": "random_int",
            "min": 1,
            "max": 100
        },
        "b": {
            "type": "random_int", 
            "min": 1,
            "max": 100
        },
        "c": {
            "type": "computed",
            "formula": "a + b"
        }
    },
    "constraints": [
        # Optional constraints
        "a > b",  # For subtraction without negatives
        "a % b == 0"  # For division without remainders
    ],
    "precision": 2  # For decimal answers
}
```

### Variable Types

1. **random_int**: Random integer in range
   ```python
   {"type": "random_int", "min": 1, "max": 100}
   ```

2. **random_float**: Random decimal in range
   ```python
   {"type": "random_float", "min": 0.0, "max": 10.0, "precision": 2}
   ```

3. **random_choice**: Pick from list
   ```python
   {"type": "random_choice", "choices": [30, 45, 60, 90]}
   ```

4. **computed**: Calculate from other variables
   ```python
   {"type": "computed", "formula": "a + b"}
   {"type": "computed", "formula": "a * b - c"}
   {"type": "computed", "formula": "sqrt(a**2 + b**2)"}
   ```

5. **lookup**: Look up from table
   ```python
   {"type": "lookup", "table": "trig_values", "key": "angle"}
   ```

## Implementation Plan

### Phase 1: Model Enhancement
1. Add new fields to Flashcard model
2. Create migration
3. Update admin interface to support parameterized cards
4. Add 'parameterized' to question type choices

### Phase 2: Parameter Engine
1. Create `ParameterGenerator` class
   - Parse parameter_spec JSON
   - Generate random values according to spec
   - Evaluate computed formulas
   - Verify constraints are met
   - Retry generation if constraints fail

2. Create `TemplateRenderer` class
   - Replace {variable} placeholders in templates
   - Format numbers according to precision
   - Handle edge cases (division by zero, etc.)

### Phase 3: Frontend Integration
1. Detect parameterized card type
2. Generate parameters when card is presented
3. Render question and answer templates
4. Store generated values with user's response
5. Allow "New variation" button for practice

### Phase 4: Answer Validation
1. For computed answers, validate student input matches computed value
2. Handle floating-point comparison (within tolerance)
3. Accept equivalent forms (fractions, decimals)
4. Provide feedback on process, not just final answer

## Example Implementations

### Example 1: Simple Addition

```python
flashcard = Flashcard.objects.create(
    topic=arithmetic_topic,
    question_template="What is {a} + {b}?",
    answer_template="{c}",
    parameter_spec={
        "variables": {
            "a": {"type": "random_int", "min": 1, "max": 50},
            "b": {"type": "random_int", "min": 1, "max": 50},
            "c": {"type": "computed", "formula": "a + b"}
        }
    },
    question_type='parameterized',
    difficulty='easy'
)
```

**Generated instances:**
- "What is 23 + 17?" → "40"
- "What is 8 + 42?" → "50"
- "What is 31 + 19?" → "50"
- ... infinite variations

### Example 2: Derivative

```python
flashcard = Flashcard.objects.create(
    topic=calculus_topic,
    question_template="Find the derivative: d/dx({a}x^{n})",
    answer_template="{c}x^{m}",
    parameter_spec={
        "variables": {
            "a": {"type": "random_int", "min": 1, "max": 10},
            "n": {"type": "random_int", "min": 2, "max": 5},
            "c": {"type": "computed", "formula": "a * n"},
            "m": {"type": "computed", "formula": "n - 1"}
        }
    },
    question_type='parameterized',
    difficulty='medium'
)
```

**Generated instances:**
- "Find the derivative: d/dx(3x^4)" → "12x^3"
- "Find the derivative: d/dx(7x^2)" → "14x^1" or "14x"
- "Find the derivative: d/dx(5x^3)" → "15x^2"

### Example 3: Pythagorean Theorem

```python
flashcard = Flashcard.objects.create(
    topic=geometry_topic,
    question_template="A right triangle has legs of length {a} and {b}. What is the length of the hypotenuse?",
    answer_template="{c:.2f}",
    parameter_spec={
        "variables": {
            "a": {"type": "random_int", "min": 3, "max": 12},
            "b": {"type": "random_int", "min": 3, "max": 12},
            "c": {"type": "computed", "formula": "sqrt(a**2 + b**2)"}
        },
        "precision": 2
    },
    question_type='parameterized',
    difficulty='medium'
)
```

### Example 4: Matrix Determinant

```python
flashcard = Flashcard.objects.create(
    topic=linear_algebra_topic,
    question_template="Find the determinant of the matrix: [[{a}, {b}], [{c}, {d}]]",
    answer_template="{det}",
    parameter_spec={
        "variables": {
            "a": {"type": "random_int", "min": -5, "max": 5},
            "b": {"type": "random_int", "min": -5, "max": 5},
            "c": {"type": "random_int", "min": -5, "max": 5},
            "d": {"type": "random_int", "min": -5, "max": 5},
            "det": {"type": "computed", "formula": "a*d - b*c"}
        }
    },
    question_type='parameterized',
    difficulty='medium'
)
```

## Benefits

1. **Prevents Memorization**: Students can't memorize answers, must understand process
2. **Unlimited Practice**: One card definition creates infinite variations
3. **Adaptive Difficulty**: Can adjust parameter ranges based on performance
4. **Efficient Content Creation**: Create one card instead of hundreds
5. **Better Assessment**: True measure of understanding, not recall
6. **Maintains Engagement**: Each practice session feels fresh

## Challenges and Solutions

### Challenge 1: Complex Formula Evaluation
**Problem**: Some formulas are complex or require special functions
**Solution**: 
- Use Python's `eval()` with safe namespace (math functions only)
- Or implement custom formula parser
- Pre-validate formulas in admin interface

### Challenge 2: Ensuring Solvable Problems
**Problem**: Random generation might create unsolvable problems (e.g., division by zero)
**Solution**:
- Implement constraints in parameter_spec
- Regenerate if constraints fail (max retries)
- Validate during card creation

### Challenge 3: Answer Format Variations
**Problem**: "2/3" vs "0.67" vs "0.666..." are all correct
**Solution**:
- Accept multiple answer formats
- Implement smart comparison (within tolerance)
- Provide answer format guidance in card

### Challenge 4: Performance
**Problem**: Generating parameters for every card view
**Solution**:
- Cache generated values during study session
- Pre-generate batch of variations
- Optimize formula evaluation

## Testing Strategy

1. **Unit Tests**: Test parameter generation in isolation
2. **Constraint Tests**: Verify constraints are enforced
3. **Formula Tests**: Test all formula types work correctly
4. **Template Tests**: Verify template rendering
5. **Edge Cases**: Division by zero, negative numbers, etc.
6. **Performance Tests**: Ensure generation is fast enough

## Migration Path

1. Existing cards remain unchanged (use question/answer fields)
2. New parameterized cards use templates
3. Can convert existing cards to parameterized format
4. Both types coexist in the system

## User Interface Considerations

1. **Card Creation**: Admin interface needs parameter spec builder
2. **Study View**: "New Variation" button for more practice
3. **Progress Tracking**: Track across all variations of a card
4. **Difficulty**: Can adjust ranges based on success rate

## Future Extensions

1. **Word Problems**: Template in problem context with parameters
2. **Multi-Step Problems**: Chain multiple parameterized steps
3. **Graphical Elements**: Generate graphs/diagrams with parameters
4. **Community Cards**: Share parameterized card definitions
5. **AI Generation**: Use AI to suggest good parameter ranges

## Conclusion

Parameterized flashcards represent a significant enhancement to the learning platform. By preventing memorization and forcing true understanding, they align with the platform's goal of mastery-based learning. 

**✅ Implementation Complete**: The system has been successfully implemented with all core features:
- Random integer, float, and choice variable types
- Computed variables with safe formula evaluation
- Constraint validation system
- Template rendering
- Full integration with study sessions
- Comprehensive test coverage (18 unit tests)
- 7 example cards demonstrating various use cases

## Implementation Summary

**Files Modified:**
- `study/models.py` - Added parameterized fields to Flashcard model
- `study/utils.py` - Parameter generation and template rendering engine (NEW)
- `study/views.py` - Integration with study session view
- `study/admin.py` - Admin interface support
- `study/tests.py` - Comprehensive test suite
- `study/migrations/0003_*.py` - Database migration (NEW)

**Management Commands:**
- `create_example_parameterized_cards` - Creates 7 example cards (NEW)

**Testing:**
- 18 unit tests covering all functionality
- All tests passing
- CodeQL security scan: 0 vulnerabilities

## References

- Model definition: `study/models.py`
- Parameter engine: `study/utils.py`
- Card creation guide: `docs/CREATING_FLASHCARDS.md`
- Curriculum structure: `docs/MATHEMATICS_CURRICULUM.md`
- Feature status: `docs/FEATURE_STATUS.md`

---

**Implementation Status**: ✅ Fully Implemented (v2.0)

**Version**: 2.0 (February 2026)

**Usage**: 
```bash
# Create example cards
python manage.py create_example_parameterized_cards --user=<username>

# Or create via Django Admin using question_type='parameterized'
```
6. Gather user feedback
