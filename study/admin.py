from django.contrib import admin
from .models import Course, Topic, Flashcard, StudySession, FlashcardProgress, Note

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_by', 'created_at']
    list_filter = ['created_by', 'created_at']
    search_fields = ['name', 'code', 'description']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'order', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['course', 'order']


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'topic', 'difficulty', 'created_at']
    list_filter = ['difficulty', 'topic__course', 'created_at']
    search_fields = ['question', 'answer']
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'started_at', 'ended_at', 'cards_studied']
    list_filter = ['user', 'topic__course', 'started_at']
    readonly_fields = ['started_at']


@admin.register(FlashcardProgress)
class FlashcardProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'flashcard_preview', 'times_reviewed', 'times_correct', 'success_rate', 'confidence_level', 'last_reviewed']
    list_filter = ['user', 'confidence_level', 'last_reviewed']
    search_fields = ['user__username', 'flashcard__question']
    
    def flashcard_preview(self, obj):
        return obj.flashcard.question[:30] + '...' if len(obj.flashcard.question) > 30 else obj.flashcard.question
    flashcard_preview.short_description = 'Flashcard'
    
    def success_rate(self, obj):
        return f"{obj.success_rate:.1f}%"
    success_rate.short_description = 'Success Rate'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'topic', 'created_at', 'updated_at']
    list_filter = ['user', 'topic__course', 'created_at']
    search_fields = ['title', 'content']

