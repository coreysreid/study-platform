# Quick Start: Engineering Mathematics Curriculum

This guide will get you up and running with the Engineering Mathematics curriculum in under 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Study Platform installed and configured
- A user account created

## Step 1: Initialize the Curriculum

Run the management command to populate your database with the complete mathematics curriculum:

```bash
python manage.py populate_math_curriculum --user=<your_username>
```

**Example:**
```bash
python manage.py populate_math_curriculum --user=john
```

This creates:
- ✅ 1 course: "Engineering Mathematics"
- ✅ 13 topics: From Basic Arithmetic to Laplace Transforms
- ✅ 68 foundational skills
- ✅ 22 prerequisite relationships

**Output:**
```
Creating Engineering Mathematics course...
✓ Created course: Engineering Mathematics

Creating skill tags...
  ✓ Created skill: basic_arithmetic
  ✓ Created skill: fraction_operations
  [... 66 more skills ...]

Creating topics...
  ✓ Created topic 1: Basic Arithmetic & Number Sense
  ✓ Created topic 2: Algebra Fundamentals
  [... 11 more topics ...]

Setting up prerequisite relationships...
  ✓ Algebra Fundamentals requires Basic Arithmetic & Number Sense
  [... 21 more relationships ...]

✓ Successfully created Engineering Mathematics curriculum with 13 topics!
✓ Created 68 skill tags for prerequisite tracking
```

## Step 2: View the Curriculum

### Option A: Admin Interface
1. Navigate to `http://localhost:8000/admin`
2. Go to **Courses** → Find "Engineering Mathematics"
3. Click on the course to see all 13 topics

### Option B: Web Interface
1. Log in to the platform
2. Navigate to **My Courses**
3. Click on "Engineering Mathematics"
4. Browse the 13 topics

## Step 3: Understand the Learning Path

The curriculum follows this progression:

```
Foundation → Pre-University → Core Calculus → Advanced Math
 (1-2)          (3-5)            (6-7)          (8-13)
```

**Start here:**
- New to math? → Topic 1: Basic Arithmetic
- Comfortable with algebra? → Topic 3: Geometry
- Ready for calculus? → Topic 6: Differential Calculus

## Step 4: Create Your First Flashcards

See `docs/CREATING_FLASHCARDS.md` for detailed examples. Here's a quick one:

```python
from study.models import Topic, Flashcard, Skill

# Get a topic
topic = Topic.objects.get(name='Basic Arithmetic & Number Sense')

# Get a skill
skill = Skill.objects.get(name='fraction_operations')

# Create a flashcard
flashcard = Flashcard.objects.create(
    topic=topic,
    question="What is 1/2 + 1/4?",
    answer="3/4 (Common denominator: 2/4 + 1/4 = 3/4)",
    hint="Find a common denominator first",
    difficulty='easy',
    question_type='standard'
)

# Tag with skill
flashcard.skills.add(skill)
```

## Step 5: Start Studying

1. Navigate to a topic
2. Click "Start Studying"
3. Answer flashcards
4. Track your progress

## Understanding the Features

### Prerequisite System
Topics show what must be mastered first:
- Topic 2 (Algebra) requires Topic 1 (Arithmetic)
- Topic 6 (Differential Calculus) requires Topic 5 (Pre-Calculus)
- System prevents jumping ahead without preparation

### Skill Tagging
Each flashcard is tagged with required skills:
- When you answer incorrectly, system identifies weak skills
- Suggests reviewing prerequisite topics
- Tracks mastery across all topics

### Question Types
Three types supported:
1. **Standard Q&A**: Traditional flashcards
2. **Multiple Choice**: Pick the correct answer
3. **Step-by-Step**: Break complex problems into steps

## Documentation

For more details, see:

- **`docs/MATHEMATICS_CURRICULUM.md`** - Full curriculum details
  - All 13 topics with learning objectives
  - Skills developed in each topic
  - Prerequisite relationships
  - Estimated completion times

- **`docs/CREATING_FLASHCARDS.md`** - How to create flashcards
  - Examples for each question type
  - Skill tagging strategies
  - Best practices

- **`docs/LEARNING_PATH_VISUAL.md`** - Visual learning path
  - ASCII diagram of curriculum flow
  - Skill dependencies
  - Time investment expectations

- **`docs/IMPLEMENTATION_SUMMARY.md`** - Technical details
  - Model changes
  - Database schema
  - Future roadmap

## Common Tasks

### Viewing All Topics
```python
from study.models import Course, Topic

course = Course.objects.get(name='Engineering Mathematics')
topics = course.topics.all()

for topic in topics:
    print(f"{topic.order}. {topic.name}")
    prereqs = topic.prerequisites.all()
    if prereqs:
        print(f"   Requires: {', '.join([p.name for p in prereqs])}")
```

### Checking Skills
```python
from study.models import Skill

skills = Skill.objects.all().order_by('name')
print(f"Total skills: {skills.count()}")

# View by category
foundation = skills.filter(name__in=[
    'basic_arithmetic', 'fraction_operations', 'algebraic_manipulation'
])
print(f"Foundation skills: {foundation.count()}")
```

### Finding Topics by Skill
```python
from study.models import Skill, Flashcard

skill = Skill.objects.get(name='derivative_calculation')
flashcards = skill.flashcards.all()
topics = set(fc.topic for fc in flashcards)

print(f"Topics using '{skill.name}':")
for topic in topics:
    print(f"  - {topic.name}")
```

## Next Steps

1. **Create Flashcards**: Start with Topic 1 (Basic Arithmetic)
   - Create comprehensive card sets as needed (no artificial limits)
   - Use all three question types
   - Tag with appropriate skills

2. **Test the System**: Study through a few topics
   - Check if prerequisites make sense
   - Verify skill tracking works
   - Gather user feedback

3. **Build Features**: Implement the learning loop
   - Algorithm to suggest review topics
   - Skill mastery dashboard
   - Progress visualization

4. **Future Enhancement - Parameterized Cards**: 
   - Add support for randomized card values (e.g., a+b=c with random a, b)
   - Prevents memorization, enforces process understanding
   - See CREATING_FLASHCARDS.md for detailed design

5. **Expand Content**: Add more topics
   - Physics for engineers
   - Programming fundamentals
   - Circuit analysis

## Troubleshooting

### "Course already exists" Error
If you see this when running the populate command:

**Option 1:** Use `--skip-existing`
```bash
python manage.py populate_math_curriculum --user=john --skip-existing
```

**Option 2:** Delete existing course first
```python
from study.models import Course
Course.objects.filter(name='Engineering Mathematics').delete()
```

### "User does not exist" Error
Create the user first:
```bash
python manage.py createsuperuser
# Or for a regular user:
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('username', 'email@example.com', 'password')
```

### Migration Issues
If you encounter migration problems:
```bash
python manage.py migrate
python manage.py makemigrations study
python manage.py migrate study
```

## Support

For questions or issues:
1. Check the documentation files in `docs/`
2. Review the code examples in `docs/CREATING_FLASHCARDS.md`
3. Open an issue on GitHub

## Summary

You now have:
- ✅ A complete mathematics curriculum structure
- ✅ 13 progressive topics ready for content
- ✅ 68 foundational skills for tracking
- ✅ Prerequisite system for guided learning
- ✅ Support for multiple question types
- ✅ Comprehensive documentation

**Total setup time:** ~2 minutes (running one command!)

**Next:** Start creating flashcards and building out the content for each topic.

---

**Happy Learning! 📚🎓**
