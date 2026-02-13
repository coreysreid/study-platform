# Code Structure Recommendations

**Quick Reference Guide**

This document provides quick, actionable recommendations for improving the study platform's code structure. For detailed analysis, see [ARCHITECTURE_REVIEW.md](ARCHITECTURE_REVIEW.md).

## Immediate Improvements (✅ Completed)

### 1. Performance Optimizations - DONE ✅
- **Fixed N+1 queries** in statistics view using `.aggregate()`
- **Added select_related/prefetch_related** to reduce database queries
- **Added pagination** to admin feedback review (25 items per page)

### 2. Code Quality - DONE ✅
- **Created `@staff_required` decorator** to eliminate duplicate permission checks
- **Added form validation** for parameterized cards
- **Improved error handling** with proper Django exceptions

### 3. Documentation - DONE ✅
- **Created comprehensive architecture review** document
- **Documented refactoring roadmap** with phases and timelines

## Next Steps (Prioritized)

### Phase 1: View Organization (1-2 weeks)

#### Split views.py into modules

**Current:** Single 430-line views.py file  
**Goal:** Multiple focused view files

```python
# Recommended structure
study/
  views/
    __init__.py          # Import all views
    auth.py             # register, login_view, logout_view
    courses.py          # Course CRUD operations
    topics.py           # Topic CRUD operations
    flashcards.py       # Flashcard CRUD operations
    sessions.py         # study_session, end_study_session
    feedback.py         # Feedback submission and review
    statistics.py       # User statistics
```

**Benefits:**
- Easier to navigate and maintain
- Reduces merge conflicts
- Better code organization
- Follows Django best practices

**Migration Steps:**
1. Create `study/views/` directory
2. Create `__init__.py` with imports
3. Move related views to appropriate files
4. Update imports in `urls.py`
5. Test thoroughly

### Phase 2: Convert to Class-Based Views (1-2 weeks)

#### Replace function-based CRUD views with Django's generic CBVs

**Example - Course List:**

**Before (FBV):**
```python
@login_required
def course_list(request):
    courses = Course.objects.filter(created_by=request.user).annotate(
        topic_count=Count('topics'),
        flashcard_count=Count('topics__flashcards')
    )
    return render(request, 'study/course_list.html', {'courses': courses})
```

**After (CBV):**
```python
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'study/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        return Course.objects.filter(
            created_by=self.request.user
        ).annotate(
            topic_count=Count('topics'),
            flashcard_count=Count('topics__flashcards')
        )
```

**Benefits:**
- ~40% less code
- Built-in pagination support
- Easier testing with mixins
- More consistent patterns

**Views to Convert:**
- ✅ `course_list` → `CourseListView`
- ✅ `course_detail` → `CourseDetailView`
- ✅ `course_create` → `CourseCreateView`
- ✅ `course_edit` → `CourseUpdateView`
- ✅ `course_delete` → `CourseDeleteView`
- ✅ `topic_detail` → `TopicDetailView`
- ✅ (Similar for topics and flashcards)

**Keep as FBVs:**
- `study_session` (complex business logic)
- `statistics` (custom aggregation logic)
- `admin_feedback_review` (custom filtering)

### Phase 3: Create Service Layer (2-3 weeks)

#### Extract business logic from views

**Problem:** Complex logic embedded in views makes testing difficult

**Solution:** Create service classes for business logic

```python
# study/services/flashcard_service.py

class FlashcardSessionService:
    """Handles flashcard session logic"""
    
    @staticmethod
    def prepare_flashcards_for_session(topic, user):
        """
        Prepare flashcards for a study session.
        
        Returns:
            list: Serialized flashcard data ready for JSON
        """
        flashcards = topic.flashcards.prefetch_related('skills')
        
        flashcards_data = []
        for fc in flashcards:
            card_data = FlashcardSessionService._serialize_flashcard(fc)
            flashcards_data.append(card_data)
        
        return flashcards_data
    
    @staticmethod
    def _serialize_flashcard(flashcard):
        """Serialize a single flashcard for session"""
        card_data = {
            'id': flashcard.id,
            'hint': flashcard.hint,
            'difficulty': flashcard.difficulty,
            # ... other fields
        }
        
        # Handle parameterized cards
        if flashcard.question_type == 'parameterized':
            card_data.update(
                FlashcardSessionService._generate_parameterized_data(flashcard)
            )
        else:
            card_data.update({
                'question': flashcard.question,
                'answer': flashcard.answer,
            })
        
        return card_data
    
    @staticmethod
    def _generate_parameterized_data(flashcard):
        """Generate data for parameterized card"""
        # Logic from current views.py lines 137-168
        pass


class FlashcardProgressService:
    """Manages flashcard progress tracking"""
    
    @staticmethod
    def update_progress(user, flashcard, correct):
        """
        Update user progress for a flashcard.
        
        Args:
            user: The user studying
            flashcard: The flashcard being reviewed
            correct: Boolean indicating if answer was correct
        """
        progress, created = FlashcardProgress.objects.get_or_create(
            user=user,
            flashcard=flashcard
        )
        
        progress.times_reviewed += 1
        if correct:
            progress.times_correct += 1
            progress.confidence_level = min(5, progress.confidence_level + 1)
        else:
            progress.confidence_level = max(1, progress.confidence_level - 1)
        
        progress.save()
        return progress
```

**Updated View:**
```python
@login_required
def study_session(request, topic_id):
    """Start a study session for a topic"""
    topic = get_object_or_404(
        Topic.objects.select_related('course'),
        id=topic_id, 
        course__created_by=request.user
    )
    
    # Use service layer
    flashcards_data = FlashcardSessionService.prepare_flashcards_for_session(
        topic, request.user
    )
    
    if not flashcards_data:
        messages.warning(request, 'No flashcards available for this topic.')
        return redirect('topic_detail', topic_id=topic_id)
    
    session = StudySession.objects.create(user=request.user, topic=topic)
    flashcards_json = json.dumps(flashcards_data)
    
    return render(request, 'study/study_session.html', {
        'topic': topic,
        'flashcards_json': flashcards_json,
        'session': session,
    })
```

**Benefits:**
- Views become thin controllers
- Business logic is reusable (can be used in API views, management commands, etc.)
- Easier to test in isolation
- Better separation of concerns

### Phase 4: Add Database Optimizations (1 week)

#### Add constraints and indexes

```python
# study/models.py

class Course(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['name']
        # Prevent duplicate course names per user
        unique_together = [['name', 'created_by']]
        indexes = [
            models.Index(fields=['created_by', 'name']),
        ]


class Flashcard(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, db_index=True)
    difficulty = models.CharField(max_length=10, db_index=True)
    question_type = models.CharField(max_length=20, db_index=True)
    
    class Meta:
        ordering = ['topic', 'id']
        indexes = [
            # Compound index for common queries
            models.Index(fields=['topic', 'difficulty']),
            models.Index(fields=['topic', 'question_type']),
        ]


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', '-started_at']),
        ]
```

**Migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Phase 5: Refactor Flashcard Model (2-3 weeks)

#### Use multi-table inheritance or composition

**Current Problem:** Flashcard model has 20+ fields for different card types

**Option 1: Abstract Base Classes**
```python
class BaseFlashcard(models.Model):
    """Common fields for all flashcards"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    hint = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class StandardFlashcard(BaseFlashcard):
    """Traditional Q&A flashcards"""
    question = models.TextField()
    answer = models.TextField()
    question_image = models.ImageField(upload_to='flashcards/questions/', null=True, blank=True)
    answer_image = models.ImageField(upload_to='flashcards/answers/', null=True, blank=True)


class ParameterizedFlashcard(BaseFlashcard):
    """Flashcards with random parameters"""
    question_template = models.TextField()
    answer_template = models.TextField()
    parameter_spec = models.JSONField()
```

**Option 2: Composition (Recommended)**
```python
class Flashcard(models.Model):
    """Core flashcard model"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=10)
    card_type = models.CharField(max_length=20, choices=CARD_TYPES)
    # Only common fields here
    
    def get_content(self):
        """Polymorphic method to get card content"""
        if self.card_type == 'standard':
            return self.standard_content
        elif self.card_type == 'parameterized':
            return self.parameterized_content
        # ... etc


class StandardFlashcardContent(models.Model):
    """Content for standard cards"""
    flashcard = models.OneToOneField(Flashcard, on_delete=models.CASCADE, related_name='standard_content')
    question = models.TextField()
    answer = models.TextField()
    question_image = models.ImageField(upload_to='flashcards/questions/', null=True, blank=True)
    answer_image = models.ImageField(upload_to='flashcards/answers/', null=True, blank=True)


class ParameterizedFlashcardContent(models.Model):
    """Content for parameterized cards"""
    flashcard = models.OneToOneField(Flashcard, on_delete=models.CASCADE, related_name='parameterized_content')
    question_template = models.TextField()
    answer_template = models.TextField()
    parameter_spec = models.JSONField()


class RichMediaFlashcardContent(models.Model):
    """Rich media features (optional, can attach to any card)"""
    flashcard = models.OneToOneField(Flashcard, on_delete=models.CASCADE, related_name='rich_media')
    uses_latex = models.BooleanField(default=False)
    diagram_code = models.TextField(blank=True)
    code_snippet = models.TextField(blank=True)
    # ... other rich media fields
```

**Benefits:**
- Cleaner separation of concerns
- Can easily add new card types
- Reduces null fields in database
- Better performance (smaller table scans)

## Quick Wins (< 1 hour each)

### 1. Add Type Hints
```python
from typing import Dict, List, Optional
from django.contrib.auth.models import User

def generate_parameterized_card(
    parameter_spec: Dict,
    question_template: str,
    answer_template: str
) -> tuple[str, str, Dict]:
    """Generate a parameterized flashcard with random values."""
    # Implementation
    pass
```

### 2. Add Docstrings
```python
def study_session(request, topic_id):
    """
    Start a study session for a topic.
    
    Loads all flashcards for the topic, generates parameterized card data,
    creates a new StudySession record, and serializes flashcards to JSON
    for the client-side study interface.
    
    Args:
        request: The HTTP request object
        topic_id: ID of the topic to study
        
    Returns:
        HttpResponse: Rendered study session template with flashcard data
        
    Raises:
        Http404: If topic doesn't exist or user doesn't have access
    """
    # Implementation
    pass
```

### 3. Add get_user_model()
```python
# Instead of:
from django.contrib.auth.models import User

# Use:
from django.contrib.auth import get_user_model
User = get_user_model()
```

This allows for custom user models in the future.

### 4. Add Model Managers
```python
class FlashcardQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(topic__course__created_by=user)
    
    def by_difficulty(self, difficulty):
        return self.filter(difficulty=difficulty)
    
    def parameterized(self):
        return self.filter(question_type='parameterized')


class Flashcard(models.Model):
    # ... fields ...
    
    objects = FlashcardQuerySet.as_manager()

# Usage:
flashcards = Flashcard.objects.for_user(request.user).by_difficulty('easy')
```

## Testing Recommendations

### 1. Add Service Layer Tests
```python
# study/tests/test_services.py

from django.test import TestCase
from study.services import FlashcardSessionService
from study.models import Course, Topic, Flashcard

class FlashcardSessionServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.course = Course.objects.create(name='Test Course', created_by=self.user)
        self.topic = Topic.objects.create(course=self.course, name='Test Topic')
        
    def test_prepare_flashcards_for_session(self):
        # Create test flashcards
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question='Test question',
            answer='Test answer'
        )
        
        # Test service
        result = FlashcardSessionService.prepare_flashcards_for_session(
            self.topic, self.user
        )
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['question'], 'Test question')
```

### 2. Add Integration Tests
```python
# study/tests/test_study_flow.py

from django.test import TestCase, Client
from django.urls import reverse

class StudyFlowIntegrationTestCase(TestCase):
    def test_complete_study_session(self):
        """Test the complete flow from course creation to study session"""
        # 1. Create user and log in
        # 2. Create course
        # 3. Create topic
        # 4. Create flashcards
        # 5. Start study session
        # 6. Complete session
        # 7. Check statistics
        pass
```

### 3. Add Performance Tests
```python
from django.test import TestCase
from django.test.utils import override_settings
from django.db import connection
from django.test.utils import CaptureQueriesContext

class PerformanceTestCase(TestCase):
    def test_statistics_query_count(self):
        """Ensure statistics view uses efficient queries"""
        # Create test data
        # ...
        
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse('statistics'))
        
        # Should be 2 queries (sessions + progress)
        self.assertLessEqual(len(queries), 3)
```

## Monitoring and Maintenance

### 1. Add Django Debug Toolbar (Development)
```python
# requirements-dev.txt
django-debug-toolbar==4.2.0

# settings.py (development only)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

### 2. Add Query Logging (Development)
```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}
```

### 3. Regular Maintenance Tasks
```bash
# Clean up old generated graphs
python manage.py cleanup_old_graphs --days=30

# Check for N+1 queries
python manage.py check --deploy

# Run tests
python manage.py test

# Check code coverage
coverage run --source='study' manage.py test
coverage report
```

## Summary

The study platform has a solid foundation. By following these recommendations in phases, you can:

1. **Immediately** benefit from performance improvements (✅ done)
2. **Short-term** (1-3 months): Improve code organization and maintainability
3. **Long-term** (3-12 months): Build a scalable architecture that supports team growth

All recommendations are based on Django best practices and have been battle-tested in production applications.

---

**Quick Reference:**
- 📖 Full analysis: [ARCHITECTURE_REVIEW.md](ARCHITECTURE_REVIEW.md)
- 🔧 Current PR: Phase 1 improvements (performance, code quality)
- ⏭️ Next PR: View organization (Phase 2)
