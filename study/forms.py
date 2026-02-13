from django import forms
from .models import Course, Topic, Flashcard, CardFeedback, Skill

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Circuit Analysis'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., ENG301'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Course description...'}),
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['course', 'name', 'description', 'order', 'prerequisites']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Ohm\'s Law'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Topic description...'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'prerequisites': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Limit course selection to user's own courses
            self.fields['course'].queryset = Course.objects.filter(created_by=user)
        # Filter prerequisites to same course topics if editing
        if self.instance and self.instance.pk:
            self.fields['prerequisites'].queryset = Topic.objects.filter(course=self.instance.course).exclude(pk=self.instance.pk)


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = [
            'topic', 'question', 'question_image', 'answer', 'answer_image', 
            'hint', 'difficulty', 'question_type', 'skills',
            'question_template', 'answer_template', 'parameter_spec'
        ]
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your question...'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter the answer...'}),
            'hint': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional hint...'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'skills': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 5}),
            'question_template': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Template with {variable} placeholders'}),
            'answer_template': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Answer template with {variable} placeholders'}),
            'parameter_spec': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'JSON parameter specification'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Limit topic selection to user's own topics
            self.fields['topic'].queryset = Topic.objects.filter(course__created_by=user)
    
    def clean(self):
        """Validate parameterized card requirements"""
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')
        
        # Validate parameterized cards have required fields
        if question_type == 'parameterized':
            question_template = cleaned_data.get('question_template')
            answer_template = cleaned_data.get('answer_template')
            parameter_spec = cleaned_data.get('parameter_spec')
            
            if not question_template:
                raise forms.ValidationError(
                    "Parameterized cards require a question template with {variable} placeholders."
                )
            
            if not answer_template:
                raise forms.ValidationError(
                    "Parameterized cards require an answer template."
                )
            
            if not parameter_spec:
                raise forms.ValidationError(
                    "Parameterized cards require a parameter specification (JSON format)."
                )
            
            # Validate parameter_spec is valid JSON
            if parameter_spec:
                import json
                try:
                    json.loads(parameter_spec)
                except json.JSONDecodeError as e:
                    raise forms.ValidationError(
                        f"Parameter specification must be valid JSON: {str(e)}"
                    )
        
        return cleaned_data


class CardFeedbackForm(forms.ModelForm):
    class Meta:
        model = CardFeedback
        fields = ['feedback_type', 'difficulty_rating', 'comment']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-control'}),
            'difficulty_rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Please provide details about your feedback...'}),
        }
