from django.contrib import admin
from .models import Course, Topic, Flashcard, StudySession, FlashcardProgress, Skill, MultipleChoiceOption, CardFeedback

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
    filter_horizontal = ['prerequisites']


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'topic', 'difficulty', 'question_type', 'created_at']
    list_filter = ['difficulty', 'question_type', 'topic__course', 'created_at']
    search_fields = ['question', 'answer', 'question_template', 'answer_template']
    filter_horizontal = ['skills']
    fieldsets = (
        ('Basic Information', {
            'fields': ('topic', 'difficulty', 'question_type', 'skills')
        }),
        ('Standard Card', {
            'fields': ('question', 'question_image', 'answer', 'answer_image', 'hint'),
            'description': 'Use for standard, multiple choice, and step-by-step cards'
        }),
        ('Parameterized Card', {
            'fields': ('question_template', 'answer_template', 'parameter_spec'),
            'description': 'Use for parameterized/randomized cards. Templates use {variable} placeholders.',
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        question_text = obj.question_template if obj.question_type == 'parameterized' and obj.question_template else obj.question
        return question_text[:50] + '...' if len(question_text) > 50 else question_text
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


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(MultipleChoiceOption)
class MultipleChoiceOptionAdmin(admin.ModelAdmin):
    list_display = ['flashcard', 'option_text_preview', 'is_correct', 'order']
    list_filter = ['is_correct']
    search_fields = ['option_text', 'flashcard__question']
    ordering = ['flashcard', 'order']
    
    def option_text_preview(self, obj):
        return obj.option_text[:50] + '...' if len(obj.option_text) > 50 else obj.option_text
    option_text_preview.short_description = 'Option'


@admin.register(CardFeedback)
class CardFeedbackAdmin(admin.ModelAdmin):
    list_display = ['flashcard_preview', 'user', 'feedback_type', 'difficulty_rating', 'status', 'created_at']
    list_filter = ['feedback_type', 'status', 'difficulty_rating', 'created_at']
    search_fields = ['comment', 'flashcard__question', 'user__username']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Feedback Information', {
            'fields': ('flashcard', 'user', 'feedback_type', 'difficulty_rating', 'comment')
        }),
        ('Review Status', {
            'fields': ('status', 'reviewed_at', 'reviewed_by')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    def flashcard_preview(self, obj):
        return obj.flashcard.question[:50] + '...' if len(obj.flashcard.question) > 50 else obj.flashcard.question
    flashcard_preview.short_description = 'Flashcard'

