# Study Platform

An interactive Python-Django study tool designed for electrical engineering students, with expandable capabilities for other subjects and users.

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

## Future Enhancements

- [x] Core mathematics curriculum structure
- [x] Prerequisite relationship system
- [x] Skill tagging for foundational concepts
- [x] Multiple question types support
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

## License

This project is open source and available for educational purposes.

## Contact

Built by an Electrical Engineering student at CDU for personal study enhancement.

---

**Happy Studying! 📚✨**
