from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg, Sum
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from functools import wraps
from .models import Course, Topic, Flashcard, StudySession, FlashcardProgress, CardFeedback
from .forms import CourseForm, TopicForm, FlashcardForm, CardFeedbackForm
from .utils import generate_parameterized_card
import random
import json

# Create your views here.

# Custom decorators
def staff_required(view_func):
    """Decorator to require staff permissions"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("You must be a staff member to access this page.")
        return view_func(request, *args, **kwargs)
    return login_required(_wrapped_view)

def home(request):
    """Home page view"""
    context = {}
    if request.user.is_authenticated:
        courses = Course.objects.filter(created_by=request.user)
        recent_sessions = StudySession.objects.filter(user=request.user)[:5]
        context = {
            'courses': courses,
            'recent_sessions': recent_sessions,
        }
    return render(request, 'study/home.html', context)


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'study/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'study/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def course_list(request):
    """List all courses for the current user"""
    courses = Course.objects.filter(created_by=request.user).annotate(
        topic_count=Count('topics', distinct=True),
        flashcard_count=Count('topics__flashcards', distinct=True)
    )
    return render(request, 'study/course_list.html', {'courses': courses})


@login_required
def course_detail(request, course_id):
    """View details of a specific course"""
    course = get_object_or_404(Course, id=course_id, created_by=request.user)
    topics = course.topics.all().annotate(flashcard_count=Count('flashcards'))
    return render(request, 'study/course_detail.html', {'course': course, 'topics': topics})


@login_required
def topic_detail(request, topic_id):
    """View details of a specific topic"""
    topic = get_object_or_404(
        Topic.objects.select_related('course'),
        id=topic_id, 
        course__created_by=request.user
    )
    flashcards = topic.flashcards.all()
    return render(request, 'study/topic_detail.html', {
        'topic': topic,
        'flashcards': flashcards,
    })


@login_required
def study_session(request, topic_id):
    """Start a study session for a topic"""
    topic = get_object_or_404(
        Topic.objects.select_related('course'),
        id=topic_id, 
        course__created_by=request.user
    )
    flashcards = list(topic.flashcards.prefetch_related('skills'))
    
    if not flashcards:
        messages.warning(request, 'No flashcards available for this topic.')
        return redirect('topic_detail', topic_id=topic_id)
    
    # Shuffle flashcards for variety
    random.shuffle(flashcards)
    
    # Create study session
    session = StudySession.objects.create(user=request.user, topic=topic)
    
    # Process flashcards - generate parameterized cards if needed
    flashcards_data = []
    for fc in flashcards:
        # Base card data
        card_data = {
            'id': fc.id,
            'hint': fc.hint,
            'difficulty': fc.difficulty,
            'question_type': fc.question_type,
            'uses_latex': fc.uses_latex,
            'diagram_code': fc.diagram_code,
            'diagram_type': fc.diagram_type,
            'code_snippet': fc.code_snippet,
            'code_language': fc.code_language,
            'graph_image_url': fc.generated_graph_image.url if fc.generated_graph_image else None,
        }
        
        if fc.question_type == 'parameterized' and fc.parameter_spec:
            try:
                question, answer, values = generate_parameterized_card(
                    fc.parameter_spec,
                    fc.question_template,
                    fc.answer_template
                )
                card_data.update({
                    'question': question,
                    'answer': answer,
                    'is_parameterized': True,
                    'question_image': fc.question_image.url if fc.question_image else None,
                    'answer_image': fc.answer_image.url if fc.answer_image else None,
                })
            except Exception as e:
                # Fallback to template if generation fails
                messages.warning(request, f'Error generating parameterized card: {str(e)}')
                card_data.update({
                    'question': fc.question_template or fc.question,
                    'answer': fc.answer_template or fc.answer,
                    'is_parameterized': False,
                    'question_image': fc.question_image.url if fc.question_image else None,
                    'answer_image': fc.answer_image.url if fc.answer_image else None,
                })
        else:
            card_data.update({
                'question': fc.question,
                'answer': fc.answer,
                'is_parameterized': False,
                'question_image': fc.question_image.url if fc.question_image else None,
                'answer_image': fc.answer_image.url if fc.answer_image else None,
            })
        
        flashcards_data.append(card_data)
    
    # Pass flashcards_data directly to template for json_script tag (don't pre-serialize)
    
    return render(request, 'study/study_session.html', {
        'topic': topic,
        'flashcards': flashcards,
        'flashcards_data': flashcards_data,
        'session': session,
    })


@login_required
def end_study_session(request, session_id):
    """End a study session"""
    session = get_object_or_404(StudySession, id=session_id, user=request.user)
    
    if request.method == 'POST':
        cards_studied = int(request.POST.get('cards_studied', 0))
        session.cards_studied = cards_studied
        session.ended_at = timezone.now()
        session.save()
        
        messages.success(request, f'Study session completed! You studied {cards_studied} cards.')
        return redirect('topic_detail', topic_id=session.topic.id)
    
    return redirect('home')


@login_required
def update_flashcard_progress(request, flashcard_id):
    """Update progress for a flashcard (AJAX endpoint)"""
    if request.method == 'POST':
        flashcard = get_object_or_404(Flashcard, id=flashcard_id)
        
        # Verify user has access to this flashcard's course
        # Currently only course creators can update progress for their flashcards
        # TODO: When course sharing is implemented, check for shared access as well
        if flashcard.topic.course.created_by != request.user:
            return HttpResponseForbidden("You don't have permission to update progress for this flashcard")
        
        correct = request.POST.get('correct') == 'true'
        
        progress, created = FlashcardProgress.objects.get_or_create(
            user=request.user,
            flashcard=flashcard
        )
        
        progress.times_reviewed += 1
        if correct:
            progress.times_correct += 1
            progress.confidence_level = min(5, progress.confidence_level + 1)
        else:
            progress.confidence_level = max(0, progress.confidence_level - 1)
        
        progress.save()
        
        return redirect('study_session', topic_id=flashcard.topic.id)
    
    return redirect('home')


@login_required
def statistics(request):
    """View study statistics"""
    sessions = StudySession.objects.filter(user=request.user)
    
    # Use aggregate to avoid N+1 queries
    session_stats = sessions.aggregate(
        total_cards=Sum('cards_studied'),
        total_sessions=Count('id')
    )
    
    progress = FlashcardProgress.objects.filter(user=request.user)
    progress_stats = progress.aggregate(
        total_reviewed=Sum('times_reviewed'),
        total_correct=Sum('times_correct'),
        progress_count=Count('id')
    )
    
    # Calculate average success rate from aggregated totals
    total_reviewed = progress_stats['total_reviewed'] or 0
    total_correct = progress_stats['total_correct'] or 0
    avg_success_rate = (total_correct / total_reviewed * 100) if total_reviewed > 0 else 0
    
    context = {
        'total_cards': session_stats['total_cards'] or 0,
        'total_sessions': session_stats['total_sessions'],
        'average_success_rate': avg_success_rate,
        'recent_sessions': sessions.select_related('topic', 'topic__course')[:10],
    }
    
    return render(request, 'study/statistics.html', context)


# Content Creation Views

@login_required
def course_create(request):
    """Create a new course"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            messages.success(request, f'Course "{course.name}" created successfully!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()
    
    return render(request, 'study/course_form.html', {'form': form, 'title': 'Create Course'})


@login_required
def course_edit(request, course_id):
    """Edit an existing course"""
    course = get_object_or_404(Course, id=course_id, created_by=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course "{course.name}" updated successfully!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'study/course_form.html', {'form': form, 'title': 'Edit Course', 'course': course})


@login_required
def topic_create(request, course_id=None):
    """Create a new topic"""
    if request.method == 'POST':
        form = TopicForm(request.POST, user=request.user)
        if form.is_valid():
            topic = form.save()
            messages.success(request, f'Topic "{topic.name}" created successfully!')
            return redirect('topic_detail', topic_id=topic.id)
    else:
        initial = {}
        if course_id:
            course = get_object_or_404(Course, id=course_id, created_by=request.user)
            initial['course'] = course
        form = TopicForm(initial=initial, user=request.user)
    
    return render(request, 'study/topic_form.html', {'form': form, 'title': 'Create Topic'})


@login_required
def topic_edit(request, topic_id):
    """Edit an existing topic"""
    topic = get_object_or_404(Topic, id=topic_id, course__created_by=request.user)
    
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Topic "{topic.name}" updated successfully!')
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = TopicForm(instance=topic, user=request.user)
    
    return render(request, 'study/topic_form.html', {'form': form, 'title': 'Edit Topic', 'topic': topic})


@login_required
def flashcard_create(request, topic_id=None):
    """Create a new flashcard"""
    if request.method == 'POST':
        form = FlashcardForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            flashcard = form.save()
            messages.success(request, 'Flashcard created successfully!')
            return redirect('topic_detail', topic_id=flashcard.topic.id)
    else:
        initial = {}
        if topic_id:
            topic = get_object_or_404(Topic, id=topic_id, course__created_by=request.user)
            initial['topic'] = topic
        form = FlashcardForm(initial=initial, user=request.user)
    
    return render(request, 'study/flashcard_form.html', {'form': form, 'title': 'Create Flashcard'})


@login_required
def flashcard_edit(request, flashcard_id):
    """Edit an existing flashcard"""
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, topic__course__created_by=request.user)
    
    if request.method == 'POST':
        form = FlashcardForm(request.POST, request.FILES, instance=flashcard, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Flashcard updated successfully!')
            return redirect('topic_detail', topic_id=flashcard.topic.id)
    else:
        form = FlashcardForm(instance=flashcard, user=request.user)
    
    return render(request, 'study/flashcard_form.html', {'form': form, 'title': 'Edit Flashcard', 'flashcard': flashcard})


# Feedback Views

@login_required
def submit_feedback(request, flashcard_id):
    """Submit feedback for a flashcard"""
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    
    if request.method == 'POST':
        form = CardFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.flashcard = flashcard
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            # Return to topic detail page
            return redirect('topic_detail', topic_id=flashcard.topic.id)
    else:
        form = CardFeedbackForm()
    
    return render(request, 'study/feedback_form.html', {'form': form, 'flashcard': flashcard})


@staff_required
def admin_feedback_review(request):
    """Admin dashboard for reviewing feedback (staff only)"""
    # Get filter parameters
    status_filter = request.GET.get('status', 'pending')
    feedback_type_filter = request.GET.get('feedback_type', '')
    page_number = request.GET.get('page', 1)
    
    # Build query
    feedback_list = CardFeedback.objects.select_related('flashcard', 'user', 'reviewed_by')
    
    if status_filter:
        feedback_list = feedback_list.filter(status=status_filter)
    if feedback_type_filter:
        feedback_list = feedback_list.filter(feedback_type=feedback_type_filter)
    
    # Add pagination
    paginator = Paginator(feedback_list, 25)  # 25 items per page
    page_obj = paginator.get_page(page_number)
    
    context = {
        'feedback_list': page_obj,
        'status_filter': status_filter,
        'feedback_type_filter': feedback_type_filter,
    }
    
    return render(request, 'study/admin_feedback_review.html', context)


@staff_required
def update_feedback_status(request, feedback_id):
    """Update feedback status (staff only)"""
    feedback = get_object_or_404(CardFeedback, id=feedback_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'reviewed', 'resolved']:
            feedback.status = new_status
            if new_status in ['reviewed', 'resolved']:
                feedback.reviewed_at = timezone.now()
                feedback.reviewed_by = request.user
            feedback.save()
            messages.success(request, f'Feedback marked as {new_status}.')
    
    return redirect('admin_feedback_review')

