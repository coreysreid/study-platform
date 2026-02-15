# Study Platform

An interactive Python-Django study tool designed for electrical engineering students, with expandable capabilities for other subjects and users.

> **Documentation Note**: See [docs/FEATURE_STATUS.md](docs/FEATURE_STATUS.md) for a complete list of implemented vs. planned features. This ensures documentation stays synchronized with the codebase.

## Features

- 📚 **Course Management**: Create and organize your studies by courses and topics
- 🎴 **Interactive Flashcards**: Create and study flashcards with active recall
- 🖼️ **Image Support**: Add images to questions and answers for visual learning
- 💬 **Card Feedback System**: Report issues, rate difficulty, and provide feedback on flashcards
- 👥 **User-Generated Content**: Full UI for creating courses, topics, and flashcards
- 📊 **Progress Tracking**: Monitor your study sessions and success rates
- 🎯 **Spaced Repetition**: Track confidence levels for optimal learning
- 👤 **User Authentication**: Secure login and personalized content
- 🎨 **Modern UI**: Clean, responsive interface with gradient designs
- 🔢 **LaTeX/Math Equations**: Render beautiful mathematical equations using MathJax
- 📈 **Graph Generation**: Create matplotlib graphs directly in flashcards with Python code
- 🎯 **Diagrams**: Add flowcharts, mind maps, and other diagrams with Mermaid.js
- 💻 **Code Snippets**: Display syntax-highlighted code in multiple programming languages
- 🎲 **Parameterized Cards**: Generate infinite variations with random values
- 🔧 **Admin Dashboard**: Review and manage user feedback on flashcards
- 🔐 **Production-Ready**: Database flexibility (SQLite/PostgreSQL) and security settings

## Technology Stack

- **Backend**: Python 3.8+ + Django 4.2
- **Database**: SQLite (dev) / PostgreSQL (production) via dj-database-url
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Django built-in auth system
- **Math Rendering**: MathJax 3 for LaTeX equations
- **Graphing**: Matplotlib + NumPy for dynamic graph generation
- **Diagrams**: Mermaid.js for flowcharts, mind maps, and more
- **Code Highlighting**: Prism.js for syntax-highlighted code snippets
- **Media Handling**: Pillow for image processing
- **Security**: Production-ready settings with validation

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
2. **Create a Course**: Click "Create" → "New Course" in the navigation menu
3. **Add Topics**: Within a course, click "Add Topic" to create topics
4. **Create Flashcards**: Add flashcards for each topic with questions, answers, and optional images
5. **Start Studying**: Navigate to a topic and click "Start Studying"

### Creating Content (User Interface)

**Creating Courses:**
- Navigate to "My Courses" and click "Create New Course"
- Enter course name, code (optional), and description
- You can only edit courses you created

**Creating Topics:**
- From a course page, click "Add Topic"
- Set name, description, order, and prerequisites
- Prerequisites help you organize learning dependencies

**Creating Flashcards:**
- From a topic page, click "Add Flashcard"
- Choose difficulty level and question type
- Add optional images to questions and answers (JPG, PNG)
- For parameterized cards, use templates with {variable} placeholders

### Feedback System

**Submitting Feedback:**
- During study sessions, click the "💬 Feedback" button
- Choose feedback type (Confusing, Incorrect, Needs Improvement, Other)
- Rate difficulty (1-5) and add comments
- Help improve flashcard quality for everyone

**Admin Feedback Review (Staff Only):**
- Access via navigation menu → "Feedback Review"
- Filter by status (Pending, Reviewed, Resolved) and type
- Quick links to edit flagged flashcards
- Mark feedback as reviewed or resolved

### Image Support

**Adding Images:**
- When creating/editing flashcards, use the image upload fields
- Supported formats: JPG, PNG, GIF
- Images display automatically during study sessions
- Maximum recommended size: 5MB per image

### Admin Interface

Access the Django admin interface at `http://localhost:8000/admin` to:
- Manage all content with advanced options
- View study session history
- Track flashcard progress
- Review and manage user feedback

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
- **Flashcard**: Question-answer pairs for studying with multiple question types and image support
- **CardFeedback**: User feedback on flashcards (type, difficulty rating, comments, status)
- **Skill**: Foundational skills/concepts for tracking learning foundations
- **MultipleChoiceOption**: Options for multiple choice questions
- **StudySession**: Tracks individual study sessions
- **FlashcardProgress**: Monitors progress on specific flashcards

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

**For Administrators** - Initialize the Engineering Mathematics curriculum as globally available public content:

```bash
# Run once during initial deployment (creates public content available in the catalog)
python manage.py populate_math_curriculum
python manage.py populate_comprehensive_math_cards
```

This creates a **"system" user** that owns the public content. The courses appear in the **Course Catalog** where users can browse and enroll. No need to specify a username - it defaults to creating/using the system user.

**What gets created:**
- The "Engineering Mathematics" course owned by the system user (visible in catalog)
- All 13 topics with descriptions
- 68 foundational skills
- Prerequisite relationships between topics
- 152 comprehensive flashcards covering all topics

**For Students** - To access the curriculum:
1. Log in to the platform
2. Go to **Course Catalog**
3. Click **"+ Add to My Courses"** on the Engineering Mathematics course
4. The course will appear in **My Courses** where you can start studying

**Optional: Create personal copy** - If you want to create a personal copy for editing:

```bash
python manage.py populate_math_curriculum --user=<your_username>
python manage.py populate_comprehensive_math_cards --user=<your_username>
```

This creates 150+ flashcards (152 total) covering:
- Basic arithmetic and number theory
- Algebra fundamentals with parameterized questions
- Geometry formulas and theorems
- Trigonometry ratios and identities
- Calculus concepts (differential and integral)
- Advanced topics (ODEs, PDEs, Fourier, Laplace)

**Note**: Run both commands for a complete math learning experience right after installation!

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

## Rich Media Flashcards (v3.0)

**NEW**: Enhance your flashcards with mathematical equations, graphs, diagrams, and code!

### LaTeX/Math Equations

Render beautiful mathematical equations using LaTeX syntax:

**Inline Math**: `$f(x) = x^2$` → $f(x) = x^2$

**Display Math**:
```
$$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$
```

Enable LaTeX support by checking "Uses LaTeX" when creating a flashcard.

### Python Graph Generation

Generate dynamic graphs using matplotlib code:

```python
x = np.linspace(-10, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.grid(True)
```

Features:
- Pre-built templates for common graph types
- Secure sandboxed code execution
- Support for parameterized graphs (graphs with random values)
- Automatic image generation and caching

### Diagrams with Mermaid.js

Create flowcharts, mind maps, and other diagrams:

**Flowchart Example**:
```mermaid
flowchart TD
    A[Start] --> B{Is x > 0?}
    B -->|Yes| C[Return sqrt(x)]
    B -->|No| D[Return error]
```

**Mind Map Example**:
```mermaid
mindmap
  root((Calculus))
    Differential
      Derivatives
      Chain Rule
    Integral
      Definite Integrals
      Applications
```

Supported diagram types:
- Flowcharts
- Sequence Diagrams
- Class Diagrams
- State Diagrams
- Mind Maps
- Gantt Charts
- Pie Charts
- Git Graphs

### Code Snippets

Display syntax-highlighted code in multiple programming languages:

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Supported languages:
- Python
- C/C++
- MATLAB
- VHDL
- JavaScript

### Creating Rich Media Cards

Via Django Admin:
1. Navigate to Flashcards
2. Create or edit a flashcard
3. Expand the "Rich Media", "Graphs", "Diagrams", or "Code Snippets" sections
4. Add your content
5. Save and study!

For detailed documentation and examples, see `docs/RICH_MEDIA_GUIDE.md`.
## Production Deployment

### Database Configuration

The platform supports both SQLite (development) and PostgreSQL (production):

```bash
# Set DATABASE_URL environment variable for PostgreSQL
export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# Or keep default SQLite
# (no DATABASE_URL needed - uses db.sqlite3)
```

### Security Settings

**Before deploying to production:**

1. Set a strong SECRET_KEY in your .env file
2. Set DEBUG=False
3. Configure ALLOWED_HOSTS with your domain
4. Uncomment production security settings in settings.py:
   - SECURE_SSL_REDIRECT
   - SESSION_COOKIE_SECURE
   - CSRF_COOKIE_SECURE
   - SECURE_HSTS_SECONDS
   - And others...

**The platform validates these settings automatically and will raise errors if:**
- SECRET_KEY is still using the default insecure key in production
- ALLOWED_HOSTS is not properly configured in production

### Media Files

Ensure media files are served properly:
- Development: Django serves media files automatically
- Production: Configure your web server (nginx, Apache) to serve /media/ directory
- Consider using cloud storage (S3, GCS) for media in production

### Checklist

- [ ] Set strong SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up PostgreSQL database
- [ ] Enable production security settings
- [ ] Configure media file serving
- [ ] Set up static file collection: `python manage.py collectstatic`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`

## Future Enhancements

- [x] Core mathematics curriculum structure
- [x] Prerequisite relationship system
- [x] Skill tagging for foundational concepts
- [x] Multiple question types support
- [x] **Parameterized/randomized cards** - Generate new values each time (e.g., a+b=c with random a,b)
- [x] **LaTeX/Math equation rendering** - Beautiful mathematical equations with MathJax
- [x] **Graph generation** - Create matplotlib graphs with Python code
- [x] **Diagrams** - Flowcharts, mind maps, and more with Mermaid.js
- [x] **Code snippets** - Syntax-highlighted code in multiple languages
- [x] **Image support in flashcards** - Add visual aids to questions and answers
- [x] **User feedback system** - Report issues and rate difficulty
- [x] **User-facing content creation** - Full UI for creating courses, topics, and flashcards
- [x] **Production security settings** - Database flexibility and validation
- [ ] Algorithm to suggest prerequisite review based on wrong answers
- [ ] Progress dashboard showing skill mastery
- [ ] Adaptive learning paths based on performance
- [ ] Multi-user support with shared courses
- [ ] Advanced spaced repetition algorithm (SM-2)
- [ ] Mobile app version
- [ ] Import/export flashcard decks
- [ ] Study reminders and scheduling
- [ ] Collaborative study groups
- [ ] Rich text editor for flashcard creation
- [ ] Rich text editor for notes
- [ ] Audio pronunciation for language learning

## Contributing

This project is currently designed for personal use but may be expanded in the future. Contributions and feedback are welcome!

**See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.**

### Branch Protection

To maintain code quality and prevent accidental changes, it's recommended to protect your main branch:

- **Quick Start**: [.github/BRANCH_PROTECTION_QUICKSTART.md](.github/BRANCH_PROTECTION_QUICKSTART.md) - 5-minute setup
- **Full Guide**: [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md) - Comprehensive documentation
- **Workflow Visual**: [docs/BRANCH_PROTECTION_WORKFLOW.md](docs/BRANCH_PROTECTION_WORKFLOW.md) - Visual workflow guide
- **Code Owners**: [.github/CODEOWNERS](.github/CODEOWNERS) - Automated review assignments
- **CI/CD**: [.github/workflows/ci.yml](.github/workflows/ci.yml) - Automated testing and checks

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
