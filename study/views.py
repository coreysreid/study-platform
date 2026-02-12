from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg
from .models import Course, Topic, Flashcard, StudySession, FlashcardProgress, Note
import random
import json

# Create your views here.

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
        topic_count=Count('topics'),
        flashcard_count=Count('topics__flashcards')
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
    topic = get_object_or_404(Topic, id=topic_id, course__created_by=request.user)
    flashcards = topic.flashcards.all()
    notes = topic.notes.filter(user=request.user)
    return render(request, 'study/topic_detail.html', {
        'topic': topic,
        'flashcards': flashcards,
        'notes': notes,
    })


@login_required
def study_session(request, topic_id):
    """Start a study session for a topic"""
    topic = get_object_or_404(Topic, id=topic_id, course__created_by=request.user)
    flashcards = list(topic.flashcards.all())
    
    if not flashcards:
        messages.warning(request, 'No flashcards available for this topic.')
        return redirect('topic_detail', topic_id=topic_id)
    
    # Shuffle flashcards for variety
    random.shuffle(flashcards)
    
    # Create study session
    session = StudySession.objects.create(user=request.user, topic=topic)
    
    # Serialize flashcards to JSON for JavaScript
    flashcards_json = json.dumps([{
        'id': fc.id,
        'question': fc.question,
        'answer': fc.answer,
        'hint': fc.hint,
        'difficulty': fc.difficulty
    } for fc in flashcards])
    
    return render(request, 'study/study_session.html', {
        'topic': topic,
        'flashcards': flashcards,
        'flashcards_json': flashcards_json,
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
    total_cards = sum(session.cards_studied for session in sessions)
    total_sessions = sessions.count()
    
    progress = FlashcardProgress.objects.filter(user=request.user)
    progress_count = progress.count()
    average_success_rate = sum(p.success_rate for p in progress) / progress_count if progress_count > 0 else 0
    
    context = {
        'total_cards': total_cards,
        'total_sessions': total_sessions,
        'average_success_rate': average_success_rate,
        'recent_sessions': sessions[:10],
    }
    
    return render(request, 'study/statistics.html', context)

