# Study Platform

An interactive Python-Django study tool designed for electrical engineering students, with expandable capabilities for other subjects and users.

> **Documentation Note**: See [docs/FEATURE_STATUS.md](docs/FEATURE_STATUS.md) for a complete list of implemented vs. planned features. This ensures documentation stays synchronized with the codebase.

## Features

- 📚 **Course Management**: Organize your studies by courses and topics
- 🎴 **Interactive Flashcards**: Create and study flashcards with active recall
- 📊 **Progress Tracking**: Monitor your study sessions and success rates
- 📝 **Note Taking**: Take and organize notes for each topic
- 🎯 **Spaced Repetition**: Track confidence levels for optimal learning
- 👤 **User Authentication**: Secure login and personalized content
- 🎨 **Modern UI**: Clean, responsive interface with gradient designs

## Technology Stack

- **Backend**: Python 3.12 + Django 6.0
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Django built-in auth system

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/coreysreid/study-platform.git
cd study-platform
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser account:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

8. Open your browser and navigate to `http://localhost:8000`

## Usage Guide

### Getting Started

1. **Register/Login**: Create an account or log in to access the platform
2. **Create a Course**: Go to Admin → Courses → Add Course
3. **Add Topics**: Within a course, add topics (e.g., "Circuit Analysis", "Semiconductors")
4. **Create Flashcards**: Add flashcards for each topic with questions and answers
5. **Start Studying**: Navigate to a topic and click "Start Studying"

### Admin Interface

Access the Django admin interface at `http://localhost:8000/admin` to:
- Manage courses, topics, and flashcards
- View study session history
- Track flashcard progress
- Manage user notes

### Study Sessions

During a study session:
- Click cards to flip and reveal answers
- Mark cards as correct or incorrect
- Use hints when available
- Track your progress with the progress bar

### Statistics

View your study statistics to:
- See total study sessions
- Track cards studied
- Monitor your success rate
- Review recent study history

## Project Structure

```
study-platform/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── study_platform/          # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
└── study/                   # Main application
    ├── models.py            # Database models
    ├── views.py             # View functions
    ├── urls.py              # App URL routing
    ├── admin.py             # Admin configuration
    └── templates/           # HTML templates
        └── study/
            ├── base.html
            ├── home.html
            ├── course_list.html
            ├── course_detail.html
            ├── topic_detail.html
            ├── study_session.html
            └── statistics.html
```

## Database Models

- **Course**: Represents a subject/course
- **Topic**: Chapters or sections within a course with prerequisite relationships
- **Flashcard**: Question-answer pairs for studying with multiple question types
- **Skill**: Foundational skills/concepts for tracking learning foundations
- **MultipleChoiceOption**: Options for multiple choice questions
- **StudySession**: Tracks individual study sessions
- **FlashcardProgress**: Monitors progress on specific flashcards
- **Note**: User notes for topics

## Core Mathematics Curriculum

The platform includes a comprehensive Engineering Mathematics curriculum designed for students starting from a Year 6 foundation. See [docs/MATHEMATICS_CURRICULUM.md](docs/MATHEMATICS_CURRICULUM.md) for the full curriculum.

### Curriculum Highlights

**13 Progressive Topics:**
1. Basic Arithmetic & Number Sense
2. Algebra Fundamentals
3. Geometry
4. Trigonometry Fundamentals
5. Pre-Calculus
6. Differential Calculus
7. Integral Calculus
8. Multivariable Calculus
9. Linear Algebra
10. Ordinary Differential Equations (ODEs)
11. Partial Differential Equations (PDEs)
12. Fourier Analysis
13. Laplace Transforms

**Key Features:**
- Prerequisite tracking system - Topics show what must be mastered first
- 68+ foundational skill tags for targeted review
- Multiple question types: Standard Q&A, Multiple Choice, Step-by-Step problems
- Estimated 70-85 weeks of content at a steady pace

### Populating the Curriculum

To initialize the Engineering Mathematics curriculum in your database:

```bash
python manage.py populate_math_curriculum --user=<your_username>
```

This creates:
- The "Engineering Mathematics" course
- All 13 topics with descriptions
- 68 foundational skills
- Prerequisite relationships between topics

The curriculum provides the structure; the next phase is creating flashcards for each topic.

## Parameterized Flashcards (v2.0)

**NEW**: Create flashcards that generate infinite variations with random values!

### What are Parameterized Cards?

Instead of static flashcards that can be memorized, parameterized cards generate new random values each time they're presented:

**Traditional Card:**
- Question: "What is 2 + 3?"
- Answer: "5"
- Problem: Students memorize the answer, not the process

**Parameterized Card:**
- Template: "What is {a} + {b}?"
- Parameters: a = random(1-50), b = random(1-50), c = a + b
- Result: Each time generates new values like "What is 17 + 23?" or "What is 45 + 8?"

### Quick Start with Parameterized Cards

Create example cards for the Basic Arithmetic topic:

```bash
python manage.py create_example_parameterized_cards --user=<your_username>
```

This creates 7 example parameterized cards including:
- Simple Addition: "What is {a} + {b}?"
- Multiplication: "What is {a} × {b}?"
- Pythagorean Theorem: "Triangle with legs {a} and {b}, find hypotenuse"
- Percentage: "What is {percent}% of {number}?"
- And more!

### Creating Your Own Parameterized Cards

Via Django Admin, create a flashcard with:
- **Question Type**: Parameterized/Randomized
- **Question Template**: "What is {a} + {b}?"
- **Answer Template**: "{c}"
- **Parameter Spec** (JSON):
```json
{
  "variables": {
    "a": {"type": "random_int", "min": 1, "max": 50},
    "b": {"type": "random_int", "min": 1, "max": 50},
    "c": {"type": "computed", "formula": "a + b"}
  }
}
```

See `docs/PARAMETERIZED_CARDS_DESIGN.md` for full documentation and advanced examples.

## Future Enhancements

- [x] Core mathematics curriculum structure
- [x] Prerequisite relationship system
- [x] Skill tagging for foundational concepts
- [x] Multiple question types support
- [x] **Parameterized/randomized cards** - Generate new values each time (e.g., a+b=c with random a,b)
- [ ] Algorithm to suggest prerequisite review based on wrong answers
- [ ] Progress dashboard showing skill mastery
- [ ] Adaptive learning paths based on performance
- [ ] Multi-user support with shared courses
- [ ] Advanced spaced repetition algorithm (SM-2)
- [ ] Mobile app version
- [ ] Import/export flashcard decks
- [ ] Study reminders and scheduling
- [ ] Collaborative study groups
- [ ] Rich text editor for notes
- [ ] Image support in flashcards
- [ ] Audio pronunciation for language learning

## Contributing

This project is currently designed for personal use but may be expanded in the future. Suggestions and feedback are welcome!

### Branch Protection

To maintain code quality and prevent accidental changes, it's recommended to protect your main branch:

- **Quick Start**: See [.github/BRANCH_PROTECTION_QUICKSTART.md](.github/BRANCH_PROTECTION_QUICKSTART.md) for a 5-minute setup guide
- **Full Guide**: See [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md) for comprehensive documentation
- **Code Owners**: Automatically request reviews with [.github/CODEOWNERS](.github/CODEOWNERS)
- **Automated Checks**: Use [.github/workflows/ci.yml](.github/workflows/ci.yml) for CI/CD

With branch protection enabled:
1. All changes must go through Pull Requests
2. Changes require review and approval
3. Automated tests must pass before merging
4. Direct pushes to main are prevented

## License

This project is open source and available for educational purposes.

## Contact

Built by an Electrical Engineering student at CDU for personal study enhancement.

---

**Happy Studying! 📚✨**
