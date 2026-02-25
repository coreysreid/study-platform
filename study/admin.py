from django.contrib import admin
from .models import (
    Course, Topic, Flashcard, StudySession, FlashcardProgress,
    Skill, MultipleChoiceOption, CardTemplate, CourseEnrollment,
    StudyPreference, TopicScore
)

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
    list_display = ['question_preview', 'topic', 'difficulty', 'question_type', 'uses_latex', 'created_at']
    list_filter = ['difficulty', 'question_type', 'uses_latex', 'graph_type', 'diagram_type', 'topic__course', 'created_at']
    search_fields = ['question', 'answer', 'question_template', 'answer_template']
    filter_horizontal = ['skills']
    fieldsets = (
        ('Basic Information', {
            'fields': ('topic', 'difficulty', 'question_type', 'skills', 'template')
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
        ('Rich Media', {
            'fields': ('uses_latex',),
            'description': 'LaTeX/Math equation support',
            'classes': ('collapse',)
        }),
        ('Graphs', {
            'fields': ('graph_type', 'graph_code', 'graph_config', 'generated_graph_image'),
            'description': 'Python matplotlib graph generation',
            'classes': ('collapse',)
        }),
        ('Diagrams', {
            'fields': ('diagram_type', 'diagram_code'),
            'description': 'Mermaid.js diagrams (flowcharts, mind maps, etc.)',
            'classes': ('collapse',)
        }),
        ('Code Snippets', {
            'fields': ('code_snippet', 'code_language'),
            'description': 'Syntax-highlighted code snippets',
            'classes': ('collapse',)
        }),
        ('Step-by-Step Fields', {
            'fields': ('steps', 'teacher_explanation'),
            'description': 'Steps JSON and teacher explanation for step_by_step cards',
            'classes': ('collapse',),
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


@admin.register(CardTemplate)
class CardTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description', 'category']
    ordering = ['category', 'name']



@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'enrolled_at', 'updated_at']
    list_filter = ['status', 'enrolled_at', 'course']
    search_fields = ['user__username', 'course__name']
    ordering = ['-enrolled_at']


@admin.register(StudyPreference)
class StudyPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'study_mode', 'updated_at']
    list_filter = ['study_mode']
    search_fields = ['user__username']


@admin.register(TopicScore)
class TopicScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'score', 'attempt_count', 'updated_at']
    list_filter = ['topic__course', 'updated_at']
    search_fields = ['user__username', 'topic__name']
    ordering = ['-updated_at']
