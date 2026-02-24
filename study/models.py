from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import secrets
import string

BADGE_DEFINITIONS = [
    {'slug': 'first_session',      'name': 'First Steps',       'icon': '🎯', 'description': 'Complete your first study session',  'type': 'sessions', 'threshold': 1},
    {'slug': 'ten_sessions',       'name': 'Getting Into It',   'icon': '📚', 'description': 'Complete 10 study sessions',          'type': 'sessions', 'threshold': 10},
    {'slug': 'fifty_sessions',     'name': 'Committed',         'icon': '🏆', 'description': 'Complete 50 study sessions',          'type': 'sessions', 'threshold': 50},
    {'slug': 'hundred_cards',      'name': 'Card Centurion',    'icon': '🔥', 'description': 'Study 100 cards total',               'type': 'cards',    'threshold': 100},
    {'slug': 'five_hundred_cards', 'name': 'Dedicated Learner', 'icon': '💪', 'description': 'Study 500 cards total',               'type': 'cards',    'threshold': 500},
    {'slug': 'thousand_cards',     'name': 'Study Machine',     'icon': '⚡', 'description': 'Study 1,000 cards total',             'type': 'cards',    'threshold': 1000},
    {'slug': 'week_streak',        'name': 'Week Warrior',      'icon': '📅', 'description': 'Study 7 days in a row',               'type': 'streak',   'threshold': 7},
]

def generate_accountability_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(8))

# Create your models here.

class Course(models.Model):
    """Represents a course or subject (e.g., Electrical Engineering, Circuit Analysis)"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, blank=True, help_text="Course code (e.g., ENG301)")
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}" if self.code else self.name


class Topic(models.Model):
    """Represents a topic or chapter within a course"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Order of topic in course")
    prerequisites = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='required_for',
        help_text="Topics that should be mastered before this one"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course', 'order', 'name']
    
    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Skill(models.Model):
    """Represents a foundational skill or concept"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Flashcard(models.Model):
    """Represents a flashcard for studying"""
    QUESTION_TYPES = [
        ('standard', 'Standard Q&A'),
        ('multiple_choice', 'Multiple Choice'),
        ('step_by_step', 'Step-by-Step Problem'),
        ('parameterized', 'Parameterized/Randomized'),
    ]
    
    GRAPH_TYPES = [
        ('none', 'No Graph'),
        ('function', 'Function Plot'),
        ('parametric', 'Parametric Plot'),
        ('3d', '3D Surface Plot'),
        ('vector', 'Vector Field'),
    ]
    
    DIAGRAM_TYPES = [
        ('none', 'No Diagram'),
        ('flowchart', 'Flowchart'),
        ('sequence', 'Sequence Diagram'),
        ('class', 'Class Diagram'),
        ('state', 'State Diagram'),
        ('gantt', 'Gantt Chart'),
        ('mindmap', 'Mind Map'),
        ('pie', 'Pie Chart'),
        ('git', 'Git Graph'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='flashcards')
    question = models.TextField(help_text="Question or front of flashcard")
    answer = models.TextField(help_text="Answer or back of flashcard")
    hint = models.TextField(blank=True, help_text="Optional hint for the question")
    difficulty = models.CharField(
        max_length=10,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        default='medium'
    )
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default='standard',
        help_text="Type of question presentation"
    )
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='flashcards',
        help_text="Foundational skills required for this question"
    )
    
    # Parameterized card fields
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

    # Step-by-step card fields
    steps = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            'Ordered solution steps for step_by_step cards. '
            'List of {"move": "action label", "detail": "full working"}'
        )
    )
    teacher_explanation = models.TextField(
        blank=True,
        help_text=(
            'Full worked explanation written as a teacher would give it. '
            'Shown only on user request. Include reasoning and common mistakes.'
        )
    )
    
    # LaTeX/Math equation support
    uses_latex = models.BooleanField(
        default=False, 
        help_text='Check if this card contains LaTeX equations'
    )
    
    # Graph generation fields
    graph_type = models.CharField(
        max_length=20, 
        choices=GRAPH_TYPES, 
        default='none'
    )
    graph_code = models.TextField(
        blank=True, 
        help_text='Python code to generate graph using matplotlib'
    )
    graph_config = models.JSONField(
        null=True, 
        blank=True, 
        help_text='Graph configuration (title, labels, range, etc.)'
    )
    generated_graph_image = models.ImageField(
        upload_to='generated_graphs/', 
        null=True, 
        blank=True
    )
    
    # Diagram fields (Mermaid.js)
    diagram_type = models.CharField(
        max_length=20, 
        choices=DIAGRAM_TYPES, 
        default='none'
    )
    diagram_code = models.TextField(
        blank=True, 
        help_text='Mermaid.js diagram code'
    )
    
    # Code snippet support
    code_snippet = models.TextField(
        blank=True, 
        help_text='Code snippet to display'
    )
    code_language = models.CharField(
        max_length=20, 
        blank=True, 
        choices=[
            ('python', 'Python'),
            ('c', 'C'),
            ('cpp', 'C++'),
            ('matlab', 'MATLAB'),
            ('vhdl', 'VHDL'),
            ('javascript', 'JavaScript'),
        ]
    )
    
    # Card template reference
    template = models.ForeignKey(
        'CardTemplate', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text='Template used to create this card'
    )
    
    # Image fields
    question_image = models.ImageField(upload_to='flashcards/questions/', null=True, blank=True)
    answer_image = models.ImageField(upload_to='flashcards/answers/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['topic', '-created_at']
    
    def __str__(self):
        return f"{self.topic.name} - {self.question[:50]}..."


class CardTemplate(models.Model):
    """Template for creating flashcards with pre-configured settings"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        help_text="Category: math, circuit, programming, etc."
    )
    default_config = models.JSONField(
        help_text="Default settings for this template"
    )
    example_image = models.ImageField(
        upload_to='templates/', 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name


class MultipleChoiceOption(models.Model):
    """Options for multiple choice questions"""
    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name='choices',
        limit_choices_to={'question_type': 'multiple_choice'}
    )
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['flashcard', 'order']
    
    def __str__(self):
        return f"{self.flashcard.question[:30]}... - {self.option_text[:30]}..."


class StudySession(models.Model):
    """Tracks study sessions for a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='study_sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    cards_studied = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"


class FlashcardProgress(models.Model):
    """Tracks individual flashcard progress for spaced repetition"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcard_progress')
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name='progress')
    step_index = models.IntegerField(
        default=-1,
        validators=[MinValueValidator(-1)],
        help_text='-1 = whole card; 0..N-1 = individual step index for step_by_step cards'
    )
    times_reviewed = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(auto_now=True)
    confidence_level = models.IntegerField(
        default=0,
        help_text="0-5 confidence level for spaced repetition"
    )

    class Meta:
        unique_together = ['user', 'flashcard', 'step_index']
        ordering = ['-last_reviewed']

    def __str__(self):
        return f"{self.user.username} - {self.flashcard.question[:30]}..."

    @property
    def success_rate(self):
        if self.times_reviewed == 0:
            return 0
        return (self.times_correct / self.times_reviewed) * 100



class StudyGoal(models.Model):
    """User's daily card study target"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='study_goal')
    daily_cards = models.IntegerField(default=0, help_text='Target cards per day (0 = no goal)')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.daily_cards} cards/day"


class AccountabilityLink(models.Model):
    """A shareable code that lets others observe your progress"""
    sharer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accountability_links')
    code = models.CharField(max_length=10, unique=True, default=generate_accountability_code)
    label = models.CharField(max_length=100, blank=True, help_text='Optional label (e.g., "Teacher", "Study Group")')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sharer.username} - {self.code}"


class AccountabilityRelationship(models.Model):
    """Records an observer following a sharer via an accountability link"""
    observer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='observing')
    link = models.ForeignKey(AccountabilityLink, on_delete=models.CASCADE, related_name='observers')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['observer', 'link']

    def __str__(self):
        return f"{self.observer.username} observing {self.link.sharer.username}"


class UserBadge(models.Model):
    """Records a badge earned by a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge_slug = models.CharField(max_length=50)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge_slug']
        ordering = ['earned_at']

    def __str__(self):
        return f"{self.user.username} - {self.badge_slug}"


class CourseEnrollment(models.Model):
    """Tracks user enrollment in courses with status"""
    STATUS_CHOICES = [
        ('studying', 'Studying'),
        ('mastered', 'Mastered'),
        ('shelved', 'Shelved'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='studying')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name} ({self.status})"


class StudyPreference(models.Model):
    """User preferences for study mode customization"""
    STUDY_MODES = [
        ('standard', 'Standard'),
        ('visual', 'Visual (emphasis on diagrams and images)'),
        ('text_heavy', 'Text Heavy (focus on text content)'),
        ('challenge', 'Challenge (timed, no hints)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='study_preference')
    study_mode = models.CharField(max_length=20, choices=STUDY_MODES, default='standard')
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_study_mode_display()}"

class TopicScore(models.Model):
    """Rolling confidence score per user per topic, used for adaptive difficulty nudges"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_scores')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='user_scores')
    score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='0.0-1.0 rolling average confidence'
    )
    attempt_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user.username} - {self.topic.name}: {self.score:.2f}"
