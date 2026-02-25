import json

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Topic, Flashcard, Skill


class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        help_text='Optional. Without an email you cannot recover a lost password.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com (optional)'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

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
    steps_json = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': '[{"move": "Step label", "detail": "Full working"}, ...]',
        }),
        help_text='JSON array of steps for step_by_step cards. Each step needs a "move" key and optional "detail".',
    )

    class Meta:
        model = Flashcard
        fields = [
            'topic', 'question', 'question_image', 'answer', 'answer_image',
            'hint', 'difficulty', 'question_type', 'skills',
            'question_template', 'answer_template', 'parameter_spec',
            'teacher_explanation',
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
            'teacher_explanation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Full worked explanation written as a teacher would give it. Include reasoning and common mistakes.',
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['topic'].queryset = Topic.objects.filter(course__created_by=user)
        # Pre-populate steps_json from existing instance
        if self.instance and self.instance.pk and self.instance.steps:
            self.fields['steps_json'].initial = json.dumps(self.instance.steps, indent=2)

    def clean_steps_json(self):
        raw = self.cleaned_data.get('steps_json', '').strip()
        if not raw:
            return None
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise forms.ValidationError(f'Invalid JSON: {exc}')
        if not isinstance(parsed, list):
            raise forms.ValidationError('Steps must be a JSON array.')
        for i, step in enumerate(parsed):
            if 'move' not in step:
                raise forms.ValidationError(f'Step {i} is missing required "move" key.')
        return parsed

    def clean(self):
        """Validate parameterized card requirements"""
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')

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

            try:
                json.loads(parameter_spec)
            except json.JSONDecodeError as e:
                raise forms.ValidationError(
                    f"Parameter specification must be valid JSON: {str(e)}"
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        steps = self.cleaned_data.get('steps_json')
        if steps is not None:
            instance.steps = steps
        if commit:
            instance.save()
            self._save_m2m()
        return instance


