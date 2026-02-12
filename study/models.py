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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course', 'order', 'name']
    
    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Flashcard(models.Model):
    """Represents a flashcard for studying"""
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['topic', '-created_at']
    
    def __str__(self):
        return f"{self.topic.name} - {self.question[:50]}..."


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


class Note(models.Model):
    """User notes for topics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

