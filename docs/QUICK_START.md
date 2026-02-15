# Quick Start: Engineering Mathematics Curriculum

This guide will get you up and running with the Engineering Mathematics curriculum in under 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Study Platform installed and configured

## For Students: Just Log In!

**Good news!** If you're a student and the platform administrator has already set up the curriculum, you don't need to do anything. Just:

1. Log in to your account
2. Navigate to **My Courses**
3. You'll see the "Engineering Mathematics" course marked with a **📚 Public** badge
4. Start studying immediately!

All public content is automatically available to all users - no setup required.

## For Administrators: One-Time Setup

Run these commands **once** during initial deployment to create public content visible to all users:

```bash
# Initialize the public math curriculum (automatically creates 'system' user)
python manage.py populate_math_curriculum
python manage.py populate_comprehensive_math_cards
```

**That's it!** The curriculum is now available to all users who log in.

**What gets created:**
- ✅ 1 course: "Engineering Mathematics" (owned by system user)
- ✅ 13 topics: From Basic Arithmetic to Laplace Transforms
- ✅ 68 foundational skills
- ✅ 22 prerequisite relationships
- ✅ 59+ comprehensive flashcards

**Output:**
```
✓ Created system user: system
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

## Optional: Create Personal Copy

If you want to create a **personal copy** for editing or customization:

```bash
python manage.py populate_math_curriculum --user=<your_username>
python manage.py populate_comprehensive_math_cards --user=<your_username>
```

**Note:** This is rarely needed - most users just use the public content.

### Option A: Admin Interface
1. Navigate to `http://localhost:8000/admin`
2. Go to **Courses** → Find "Engineering Mathematics"
3. Click on the course to see all 13 topics

### Option B: Web Interface
1. Log in to the platform
2. Navigate to **My Courses**
3. Click on "Engineering Mathematics"
4. Browse the 13 topics

## Understanding the Learning Path

The curriculum follows this progression:

```
Foundation → Pre-University → Core Calculus → Advanced Math
 (1-2)          (3-5)            (6-7)          (8-13)
```

**Start here:**
- New to math? → Topic 1: Basic Arithmetic
- Comfortable with algebra? → Topic 3: Geometry
- Ready for calculus? → Topic 6: Differential Calculus

## Create Additional Flashcards (Optional)

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

## Start Studying

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
python manage.py populate_math_curriculum --skip-existing
```

**Option 2:** Delete existing course first
```python
from study.models import Course
Course.objects.filter(name='Engineering Mathematics', created_by__username='system').delete()
```

### Checking If Public Content Exists
```python
from django.contrib.auth.models import User
from study.models import Course

system_user = User.objects.filter(username='system').first()
if system_user:
    courses = Course.objects.filter(created_by=system_user)
    print(f"Public courses: {list(courses.values_list('name', flat=True))}")
else:
    print("System user does not exist - run populate_math_curriculum")
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
