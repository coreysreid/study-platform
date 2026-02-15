from django.db import models
from django.contrib.auth.models import User

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
    times_reviewed = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(auto_now=True)
    confidence_level = models.IntegerField(
        default=0,
        help_text="0-5 confidence level for spaced repetition"
    )
    
    class Meta:
        unique_together = ['user', 'flashcard']
        ordering = ['-last_reviewed']
    
    def __str__(self):
        return f"{self.user.username} - {self.flashcard.question[:30]}..."
    
    @property
    def success_rate(self):
        if self.times_reviewed == 0:
            return 0
        return (self.times_correct / self.times_reviewed) * 100


class CardFeedback(models.Model):
    """User feedback on flashcards"""
    FEEDBACK_TYPES = [
        ('confusing', 'Confusing/Unclear'),
        ('incorrect', 'Incorrect Information'),
        ('needs_improvement', 'Needs Improvement'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]
    
    flashcard = models.ForeignKey('Flashcard', on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    difficulty_rating = models.IntegerField(null=True, blank=True, help_text='Rate difficulty 1-5')
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_feedback')
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_feedback_type_display()} - {self.flashcard}"



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
