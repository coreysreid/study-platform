from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.db.models import Count, Avg, Sum, Q, F, Subquery, OuterRef, IntegerField
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from functools import wraps
from .models import (Course, Topic, Flashcard, StudySession, FlashcardProgress,
                     CourseEnrollment, StudyPreference, StudyGoal,
                     AccountabilityLink, AccountabilityRelationship,
                     UserBadge, BADGE_DEFINITIONS, TopicScore,
                     FlashcardVote, FlashcardComment, CardSuggestion,
                     SpacedRepetitionSettings)
import datetime
from .forms import CourseForm, TopicForm, FlashcardForm, CustomRegistrationForm
from .utils import generate_parameterized_card
import random
import json

# Create your views here.

# Constants
VALID_ENROLLMENT_STATUSES = {'studying', 'mastered', 'shelved'}
VOTE_FLAG_THRESHOLD = -5  # Cards with net score at or below this are flagged for review
SUGGESTION_MAX_QUESTION_LEN = 2000
SUGGESTION_MAX_ANSWER_LEN = 2000
SUGGESTION_MAX_HINT_LEN = 500

# Utility functions for public content
def get_system_user():
    """Get the system user for public content."""
    return User.objects.filter(username='system').first()

def get_public_content_filter(user, model_class):
    """
    Get a Q filter for accessing both user's own content and public content.
    
    Args:
        user: The current request user
        model_class: The model class being filtered (Course, Topic, etc.)
    
    Returns:
        Q object that filters for user's content OR public content
    """
    system_user = get_system_user()
    
    # Determine the field path based on the model
    if model_class == Course:
        field_path = 'created_by'
    elif model_class == Topic:
        field_path = 'course__created_by'
    elif model_class == Flashcard:
        field_path = 'topic__course__created_by'
    else:
        field_path = 'created_by'  # Default
    
    # Build filter: user's content OR public content
    return Q(**{field_path: user}) | (Q(**{field_path: system_user}) if system_user else Q(pk__in=[]))

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
        # Query: User's courses + Public courses
        courses = Course.objects.filter(get_public_content_filter(request.user, Course))
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
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Auto-enroll new users in all system courses
            system_user = get_system_user()
            if system_user:
                system_courses = Course.objects.filter(created_by=system_user)
                for course in system_courses:
                    CourseEnrollment.objects.get_or_create(
                        user=user, course=course,
                        defaults={'status': 'studying'}
                    )
            messages.success(request, 'Welcome! Browse the course catalogue to get started.')
            return redirect('course_catalog')
    else:
        form = CustomRegistrationForm()
    
    return render(request, 'study/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
    else:
        form = AuthenticationForm()

    for field in form.fields.values():
        field.widget.attrs.setdefault('class', 'form-control')

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')

    return render(request, 'study/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def course_list(request):
    """My Courses - Show courses the user is enrolled in and courses they created"""
    enrollments = CourseEnrollment.objects.filter(user=request.user).select_related('course').annotate(
        topic_count=Count('course__topics', distinct=True),
        flashcard_count=Count('course__topics__flashcards', distinct=True)
    ).order_by('-enrolled_at')
    
    # Also include courses created by the user
    owned_courses = Course.objects.filter(created_by=request.user).annotate(
        topic_count=Count('topics', distinct=True),
        flashcard_count=Count('topics__flashcards', distinct=True)
    ).order_by('name')
    
    return render(request, 'study/my_courses.html', {
        'enrollments': enrollments,
        'owned_courses': owned_courses,
    })


@login_required
def course_catalog(request):
    """Course Catalog - Browse all public courses available for enrollment"""
    system_user = get_system_user()
    
    if not system_user:
        messages.warning(request, 'No public courses available yet.')
        return redirect('course_list')
    
    # Get all public courses
    public_courses = Course.objects.filter(created_by=system_user).annotate(
        topic_count=Count('topics', distinct=True),
        flashcard_count=Count('topics__flashcards', distinct=True)
    ).order_by('name')
    
    # Get user's enrolled course IDs as a set for efficient membership checking
    enrolled_course_ids = set(CourseEnrollment.objects.filter(user=request.user).values_list('course_id', flat=True))
    
    # Mark which courses are enrolled
    for course in public_courses:
        course.is_enrolled = course.id in enrolled_course_ids
    
    return render(request, 'study/course_catalog.html', {'courses': public_courses})


@login_required
def course_detail(request, course_id):
    """View details of a specific course (enrolled or catalog)"""
    system_user = get_system_user()
    
    # Check if user is enrolled in this course
    enrollment = CourseEnrollment.objects.filter(user=request.user, course_id=course_id).first()
    
    if enrollment:
        # Show enrolled course details
        course = enrollment.course
    else:
        # Show catalog course (must be public)
        course = get_object_or_404(Course, id=course_id, created_by=system_user)
    
    topics = course.topics.all().annotate(flashcard_count=Count('flashcards')).order_by('code', 'name')
    
    return render(request, 'study/course_detail.html', {
        'course': course,
        'topics': topics,
        'enrollment': enrollment,
        'is_enrolled': enrollment is not None
    })


@login_required
@require_POST
def enroll_course(request, course_id):
    """Enroll in a public course"""
    system_user = get_system_user()
    
    # Only allow enrolling in public courses
    course = get_object_or_404(Course, id=course_id, created_by=system_user)
    
    # Create enrollment if it doesn't exist
    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'status': 'studying'}
    )
    
    if created:
        messages.success(request, f'Successfully enrolled in "{course.name}"!')
    else:
        messages.info(request, f'You are already enrolled in "{course.name}".')
    
    return redirect('course_list')


@login_required
@require_POST
def unenroll_course(request, course_id):
    """Remove a course from My Courses"""
    enrollment = get_object_or_404(CourseEnrollment, user=request.user, course_id=course_id)
    course_name = enrollment.course.name
    enrollment.delete()
    messages.success(request, f'Removed "{course_name}" from your courses.')
    return redirect('course_list')


@login_required
@require_POST
def update_enrollment_status(request, course_id):
    """Update the status of an enrolled course"""
    enrollment = get_object_or_404(CourseEnrollment, user=request.user, course_id=course_id)
    new_status = request.POST.get('status')
    
    # Check if status is valid using constant derived from model's STATUS_CHOICES
    if new_status in VALID_ENROLLMENT_STATUSES:
        enrollment.status = new_status
        enrollment.save()
        messages.success(request, f'Updated status to "{enrollment.get_status_display()}".')
    else:
        messages.error(request, 'Invalid status.')
    
    return redirect('course_list')


def _annotate_with_votes(queryset, user):
    """Annotate a Flashcard queryset with upvotes, downvotes, net_votes, and user_vote."""
    user_vote_subquery = Subquery(
        FlashcardVote.objects.filter(
            user=user,
            flashcard=OuterRef('pk'),
        ).values('vote')[:1],
        output_field=IntegerField(),
    )
    # Two annotate() calls so the second can reference the first via F().
    return queryset.annotate(
        upvotes=Count('votes', filter=Q(votes__vote=FlashcardVote.UPVOTE)),
        downvotes=Count('votes', filter=Q(votes__vote=FlashcardVote.DOWNVOTE)),
    ).annotate(
        net_votes=F('upvotes') - F('downvotes'),
        user_vote=user_vote_subquery,
    )


@login_required
def topic_detail(request, topic_id):
    """View details of a specific topic."""
    topic = get_object_or_404(Topic.objects.select_related('course__created_by'), id=topic_id)

    system_user = get_system_user()
    is_owner = topic.course.created_by == request.user
    enrollment = CourseEnrollment.objects.filter(user=request.user, course=topic.course).first()

    # Only block access to privately-owned courses that the user has no relation to.
    # System (public) course topics are viewable by any authenticated user; the template
    # restricts interactive actions (voting, studying, suggesting) to enrolled users.
    if not enrollment and not is_owner and topic.course.created_by != system_user:
        messages.error(request, 'You must be enrolled in this course to view topics.')
        return redirect('course_catalog')

    # Annotate flashcards with vote counts and user's own vote, then sort best-first.
    flashcards = (
        _annotate_with_votes(topic.flashcards, request.user)
        .order_by('-net_votes', '-created_at')
        .prefetch_related('comments__user')
    )

    # Count cards due for review today
    today = datetime.date.today()
    due_count = FlashcardProgress.objects.filter(
        user=request.user,
        flashcard__topic=topic,
        next_review_date__lte=today,
        step_index=-1,
    ).count()

    return render(request, 'study/topic_detail.html', {
        'topic': topic,
        'flashcards': flashcards,
        'is_enrolled': enrollment is not None,
        'flag_threshold': VOTE_FLAG_THRESHOLD,
        'is_system_course': topic.course.created_by == system_user,
        'due_count': due_count,
    })




@login_required
def study_session(request, topic_id):
    """Start a study session for a topic - user must be enrolled.

    When ?review=1 is passed, only cards due for review today are included.
    """
    topic = get_object_or_404(Topic.objects.select_related('course'), id=topic_id)

    # Check if user is enrolled in this course
    enrollment = CourseEnrollment.objects.filter(user=request.user, course=topic.course).first()

    if not enrollment:
        messages.error(request, 'You must be enrolled in this course to study.')
        return redirect('course_catalog')

    # Get user's study mode preference
    preference, _ = StudyPreference.objects.get_or_create(user=request.user)
    valid_modes = {choice[0] for choice in StudyPreference.STUDY_MODES}
    mode_param = request.GET.get('mode')
    if mode_param in valid_modes:
        study_mode = mode_param
    else:
        study_mode = preference.study_mode

    is_review_mode = request.GET.get('review') == '1'
    today = datetime.date.today()

    if is_review_mode:
        # Only cards due today
        due_ids = set(
            FlashcardProgress.objects.filter(
                user=request.user,
                flashcard__topic=topic,
                next_review_date__lte=today,
                step_index=-1,
            ).values_list('flashcard_id', flat=True)
        )
        base_qs = topic.flashcards.filter(id__in=due_ids).prefetch_related('skills')
    else:
        base_qs = topic.flashcards.prefetch_related('skills')

    flashcards = list(_annotate_with_votes(base_qs, request.user))

    if not flashcards:
        if is_review_mode:
            messages.info(request, 'No cards are due for review right now. Great work!')
        else:
            messages.warning(request, 'No flashcards available for this topic.')
        return redirect('topic_detail', topic_id=topic_id)

    # Fetch SR progress for all cards in one query
    progress_map = {
        p.flashcard_id: p
        for p in FlashcardProgress.objects.filter(
            user=request.user,
            flashcard__in=flashcards,
            step_index=-1,
        )
    }

    # Shuffle for variety (due cards first when in review mode is not strictly needed)
    random.shuffle(flashcards)

    # Cap new (never-SM2-reviewed) cards to the user's daily_new_cards setting.
    # This only applies in normal study mode; review mode already shows only due cards.
    if not is_review_mode:
        sr_settings = SpacedRepetitionSettings.objects.filter(user=request.user).first()
        daily_new_cap = (
            sr_settings.daily_new_cards
            if sr_settings
            else SpacedRepetitionSettings.DEFAULT_DAILY_NEW_CARDS
        )
        seen = [f for f in flashcards if progress_map.get(f.id) is not None]
        new_cards = [f for f in flashcards if progress_map.get(f.id) is None]
        if len(new_cards) > daily_new_cap:
            flashcards = seen + new_cards[:daily_new_cap]

    # Create study session
    session = StudySession.objects.create(user=request.user, topic=topic)

    # Process flashcards - expand step_by_step cards into virtual cards
    flashcards_data = []
    for fc in flashcards:
        prog = progress_map.get(fc.id)
        base = {
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
            'question_image': fc.question_image.url if fc.question_image else None,
            'answer_image': fc.answer_image.url if fc.answer_image else None,
            'teacher_explanation': fc.teacher_explanation,
            'net_votes': fc.net_votes,
            'upvotes': fc.upvotes,
            'downvotes': fc.downvotes,
            'user_vote': fc.user_vote,
            # SR metadata for display
            'next_review_date': prog.next_review_date.isoformat() if prog and prog.next_review_date else None,
            'interval_days': prog.interval_days if prog else 0,
            'sm2_repetitions': prog.sm2_repetitions if prog else 0,
        }

        if fc.question_type == 'step_by_step' and fc.steps:
            steps = fc.steps
            for k, step in enumerate(steps):
                virtual = dict(base)
                virtual.update({
                    'step_index': k,
                    'step_total': len(steps),
                    'question': fc.question,
                    'context_steps': steps[:k],
                    'answer': step['move'],
                    'answer_detail': step.get('detail', ''),
                    'is_parameterized': False,
                })
                flashcards_data.append(virtual)

        elif fc.question_type == 'parameterized' and fc.parameter_spec:
            try:
                question, answer, _ = generate_parameterized_card(
                    fc.parameter_spec, fc.question_template, fc.answer_template
                )
            except Exception:
                question = fc.question_template or fc.question
                answer = fc.answer_template or fc.answer
            base.update({
                'step_index': -1,
                'step_total': None,
                'question': question,
                'answer': answer,
                'answer_detail': '',
                'context_steps': [],
                'is_parameterized': True,
            })
            flashcards_data.append(base)

        else:
            base.update({
                'step_index': -1,
                'step_total': None,
                'question': fc.question,
                'answer': fc.answer,
                'answer_detail': '',
                'context_steps': [],
                'is_parameterized': False,
            })
            flashcards_data.append(base)

    nudge_topics = []
    my_score = TopicScore.objects.filter(user=request.user, topic=topic).first()
    if my_score and my_score.score < 0.4 and my_score.attempt_count >= 10:
        for prereq in topic.prerequisites.all():
            prereq_score = TopicScore.objects.filter(user=request.user, topic=prereq).first()
            if prereq_score is None or prereq_score.score < 0.7:
                nudge_topics.append({
                    'topic': prereq,
                    'score_pct': int(prereq_score.score * 100) if prereq_score else None,
                })

    return render(request, 'study/study_session.html', {
        'topic': topic,
        'flashcards': flashcards,
        'flashcards_data': flashcards_data,
        'session': session,
        'study_mode': study_mode,
        'study_modes': StudyPreference.STUDY_MODES,
        'nudge_topics': nudge_topics,
        'is_review_mode': is_review_mode,
        'prerequisites': topic.prerequisites.all(),
    })


@login_required
def end_study_session(request, session_id):
    """End a study session"""
    session = get_object_or_404(StudySession, id=session_id, user=request.user)
    
    if request.method == 'POST':
        try:
            cards_studied = max(0, int(request.POST.get('cards_studied', 0)))
        except (ValueError, TypeError):
            cards_studied = 0
        session.cards_studied = cards_studied
        session.ended_at = timezone.now()
        session.save()
        
        messages.success(request, f'Study session completed! You studied {cards_studied} cards.')

        # Award any newly earned badges
        stats = _get_user_stats(request.user)
        new_badges = _award_badges(request.user, stats)
        for badge in new_badges:
            messages.success(request, f"{badge['icon']} Badge earned: {badge['name']}!")

        _update_topic_score(request.user, session.topic)

        return redirect('topic_detail', topic_id=session.topic.id)
    
    return redirect('home')


# ---------------------------------------------------------------------------
# SM-2 spaced repetition algorithm
# ---------------------------------------------------------------------------

def _apply_sm2(progress, quality, settings=None):
    """Apply the SM-2 algorithm to a FlashcardProgress record.

    quality: integer 0–5
        0 = complete blackout / reset (same effect as 1)
        1 = wrong answer
        2 = correct but very hard (nearly forgot)
        3 = correct with significant effort
        4 = correct after brief hesitation  ← "Got it / Good"
        5 = perfect, no hesitation          ← "Easy"

    The record is mutated but NOT saved — the caller must call .save().
    """
    min_ef = settings.get_min_easiness() if settings else 1.3
    max_interval = settings.max_interval_days if settings else 365

    # Update SM-2 easiness factor
    ef = progress.easiness_factor
    ef = ef + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    ef = max(min_ef, ef)

    if quality < 3:
        # Forgot — reset the learning streak, go back to 1-day interval
        progress.sm2_repetitions = 0
        new_interval = 1
    else:
        # Remembered correctly
        reps = progress.sm2_repetitions
        if reps == 0:
            new_interval = 1
        elif reps == 1:
            new_interval = 6
        else:
            new_interval = round(progress.interval_days * ef)
        new_interval = min(new_interval, max_interval)
        progress.sm2_repetitions = reps + 1

    progress.easiness_factor = round(ef, 4)
    progress.interval_days = new_interval
    progress.next_review_date = (
        datetime.date.today() + datetime.timedelta(days=new_interval)
    )


@login_required
@require_POST
def update_flashcard_progress(request, flashcard_id):
    """Update per-card (or per-step) progress. Returns JSON.

    Accepts either:
      • quality=<0-5>  (SM-2 quality rating, preferred)
      • correct=true/false  (legacy — maps to quality 4 or 1)
    """

    flashcard = get_object_or_404(Flashcard, id=flashcard_id)

    course = flashcard.topic.course
    is_owner = (course.created_by == request.user)
    has_enrollment = CourseEnrollment.objects.filter(
        user=request.user, course=course
    ).exists()
    if not (is_owner or has_enrollment):
        return JsonResponse({'error': 'No access'}, status=403)

    # Resolve quality (0-5).  Legacy "correct" boolean mapped to 4 / 1.
    raw_quality = request.POST.get('quality')
    if raw_quality is not None:
        try:
            quality = int(raw_quality)
            if not (0 <= quality <= 5):
                raise ValueError
        except (ValueError, TypeError):
            return JsonResponse({'error': 'quality must be 0–5'}, status=400)
    else:
        # Legacy path
        correct = request.POST.get('correct') == 'true'
        quality = 4 if correct else 1

    try:
        step_index = int(request.POST.get('step_index', '-1'))
    except (ValueError, TypeError):
        step_index = -1

    progress, _ = FlashcardProgress.objects.get_or_create(
        user=request.user,
        flashcard=flashcard,
        step_index=step_index,
    )

    # Classic confidence tracking (kept for backwards compatibility)
    progress.times_reviewed = F('times_reviewed') + 1
    if quality >= 3:
        progress.times_correct = F('times_correct') + 1
        progress.confidence_level = min(5, progress.confidence_level + 1)
    else:
        progress.confidence_level = max(0, progress.confidence_level - 1)

    # SM-2 scheduling is always on the whole-card (step_index=-1) record so that
    # due_count and review mode (which filter by step_index=-1) see step-by-step cards.
    settings = SpacedRepetitionSettings.objects.filter(user=request.user).first()
    if step_index == -1:
        _apply_sm2(progress, quality, settings)
        progress.save()
        progress.refresh_from_db()
        sr_progress = progress
    else:
        # Save stats-only record for the individual step; apply SM-2 to the whole-card record.
        progress.save()
        sr_progress, _ = FlashcardProgress.objects.get_or_create(
            user=request.user,
            flashcard=flashcard,
            step_index=-1,
        )
        _apply_sm2(sr_progress, quality, settings)
        sr_progress.save()
        sr_progress.refresh_from_db()
        progress.refresh_from_db()

    return JsonResponse({
        'confidence_level': progress.confidence_level,
        'times_reviewed': progress.times_reviewed,
        'next_review_date': (
            sr_progress.next_review_date.isoformat() if sr_progress.next_review_date else None
        ),
        'interval_days': sr_progress.interval_days,
        'step_index': step_index,
    })


@login_required
@require_POST
def mark_card_never_seen(request, flashcard_id):
    """Reset a card's SM-2 progress to 'new' (never seen).

    This lets a user flag a card they don't recognise so it is
    treated as brand-new and re-introduced from the beginning.
    """
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    course = flashcard.topic.course
    is_owner = (course.created_by == request.user)
    has_enrollment = CourseEnrollment.objects.filter(
        user=request.user, course=course
    ).exists()
    if not (is_owner or has_enrollment):
        return JsonResponse({'error': 'No access'}, status=403)

    FlashcardProgress.objects.filter(
        user=request.user,
        flashcard=flashcard,
    ).update(
        times_reviewed=0,
        times_correct=0,
        confidence_level=0,
        easiness_factor=2.5,
        interval_days=0,
        sm2_repetitions=0,
        next_review_date=None,
    )

    return JsonResponse({'status': 'reset'})


@login_required
def review_session(request, topic_id):
    """Redirect to the study session restricted to cards that are due for review today."""
    topic = get_object_or_404(
        Topic.objects.select_related('course'),
        id=topic_id,
    )
    course = topic.course

    is_owner = (course.created_by == request.user)
    has_enrollment = CourseEnrollment.objects.filter(
        user=request.user, course=course,
    ).exists()
    if not (is_owner or has_enrollment):
        messages.warning(request, 'You must be enrolled to review this topic.')
        return redirect('topic_detail', topic_id=topic_id)

    today = datetime.date.today()

    # Check if any cards are actually due
    due_count = FlashcardProgress.objects.filter(
        user=request.user,
        flashcard__topic=topic,
        next_review_date__lte=today,
        step_index=-1,
    ).count()

    if not due_count:
        messages.info(request, 'No cards are due for review in this topic right now. Great work!')
        return redirect('topic_detail', topic_id=topic_id)

    return redirect(reverse('study_session', kwargs={'topic_id': topic_id}) + '?review=1')


@login_required
def spaced_repetition_settings(request):
    """View and update the user's SM-2 spaced repetition settings."""
    settings_obj, _ = SpacedRepetitionSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        try:
            ease_modifier = int(request.POST.get(
                'ease_modifier', SpacedRepetitionSettings.DEFAULT_EASE_MODIFIER))
            max_interval = int(request.POST.get(
                'max_interval_days', SpacedRepetitionSettings.DEFAULT_MAX_INTERVAL_DAYS))
            daily_new = int(request.POST.get(
                'daily_new_cards', SpacedRepetitionSettings.DEFAULT_DAILY_NEW_CARDS))
        except (ValueError, TypeError):
            messages.error(request, 'Invalid values — please use the sliders.')
            return redirect('spaced_repetition_settings')

        # Clamp to model validator bounds
        settings_obj.ease_modifier = max(-2, min(2, ease_modifier))
        settings_obj.max_interval_days = max(30, min(730, max_interval))
        settings_obj.daily_new_cards = max(1, min(100, daily_new))
        settings_obj.save()
        messages.success(request, 'Spaced repetition settings saved.')
        return redirect('spaced_repetition_settings')

    return render(request, 'study/spaced_repetition_settings.html', {
        'settings': settings_obj,
        'speed_choices': SpacedRepetitionSettings.SPEED_CHOICES,
    })


@login_required
@require_POST
def vote_flashcard(request, flashcard_id):
    """Upvote or downvote a public flashcard. Returns JSON with updated counts.

    POST body: vote=1 (upvote) or vote=-1 (downvote).
    Submitting the same vote again removes it (toggle).
    Users cannot vote on their own cards or on cards in courses they are not enrolled in.
    """
    flashcard = get_object_or_404(
        Flashcard.objects.select_related('topic__course__created_by'),
        id=flashcard_id,
    )

    course = flashcard.topic.course

    # Prevent self-voting
    if course.created_by == request.user:
        return JsonResponse({'error': 'You cannot vote on your own cards.'}, status=403)

    # Require enrollment in the course to vote
    if not CourseEnrollment.objects.filter(user=request.user, course=course).exists():
        return JsonResponse({'error': 'You must be enrolled in this course to vote.'}, status=403)

    try:
        vote_value = int(request.POST.get('vote', 0))
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid vote value.'}, status=400)

    if vote_value not in (FlashcardVote.UPVOTE, FlashcardVote.DOWNVOTE):
        return JsonResponse({'error': 'Vote must be 1 or -1.'}, status=400)

    with transaction.atomic():
        vote_obj, created = FlashcardVote.objects.get_or_create(
            user=request.user,
            flashcard=flashcard,
            defaults={'vote': vote_value},
        )
        if created:
            user_vote = vote_value
        elif vote_obj.vote == vote_value:
            # Same vote submitted again — toggle off
            vote_obj.delete()
            user_vote = 0
        else:
            # Change vote direction
            vote_obj.vote = vote_value
            vote_obj.save(update_fields=['vote'])
            user_vote = vote_value

    # Recalculate totals
    totals = FlashcardVote.objects.filter(flashcard=flashcard).aggregate(
        upvotes=Count('pk', filter=Q(vote=FlashcardVote.UPVOTE)),
        downvotes=Count('pk', filter=Q(vote=FlashcardVote.DOWNVOTE)),
    )
    net = totals['upvotes'] - totals['downvotes']

    return JsonResponse({
        'upvotes': totals['upvotes'],
        'downvotes': totals['downvotes'],
        'net_votes': net,
        'user_vote': user_vote,
        'flagged': net <= VOTE_FLAG_THRESHOLD,
    })


@login_required
@require_POST
def comment_flashcard(request, flashcard_id):
    """Add a comment or suggested improvement to a flashcard."""
    flashcard = get_object_or_404(
        Flashcard.objects.select_related('topic__course__created_by'),
        id=flashcard_id,
    )

    # Must be enrolled in or own the course
    course = flashcard.topic.course
    is_owner = course.created_by == request.user
    has_enrollment = CourseEnrollment.objects.filter(user=request.user, course=course).exists()
    if not (is_owner or has_enrollment):
        return JsonResponse({'error': 'No access.'}, status=403)

    body = request.POST.get('body', '').strip()
    if not body:
        messages.error(request, 'Comment cannot be empty.')
        return redirect('topic_detail', topic_id=flashcard.topic_id)

    if len(body) > 1000:
        messages.error(request, 'Comment must be 1000 characters or fewer.')
        return redirect('topic_detail', topic_id=flashcard.topic_id)

    FlashcardComment.objects.create(user=request.user, flashcard=flashcard, body=body)
    messages.success(request, 'Comment added.')
    return redirect('topic_detail', topic_id=flashcard.topic_id)


@login_required
@require_POST
def suggest_card(request, topic_id):
    """Submit a card suggestion for a topic (pending admin review)."""
    topic = get_object_or_404(Topic.objects.select_related('course__created_by'), id=topic_id)

    # Must be enrolled in this course (suggestions are for system courses; owners use add-flashcard)
    if not CourseEnrollment.objects.filter(user=request.user, course=topic.course).exists():
        messages.error(request, 'You must be enrolled in this course to suggest a card.')
        return redirect('topic_detail', topic_id=topic_id)

    question = request.POST.get('question', '').strip()
    answer = request.POST.get('answer', '').strip()
    hint = request.POST.get('hint', '').strip()

    if not question or not answer:
        messages.error(request, 'Both question and answer are required.')
        return redirect('topic_detail', topic_id=topic_id)

    if (len(question) > SUGGESTION_MAX_QUESTION_LEN
            or len(answer) > SUGGESTION_MAX_ANSWER_LEN
            or len(hint) > SUGGESTION_MAX_HINT_LEN):
        messages.error(
            request,
            f'Question and answer must each be {SUGGESTION_MAX_QUESTION_LEN} characters or fewer; '
            f'hint must be {SUGGESTION_MAX_HINT_LEN} characters or fewer.',
        )
        return redirect('topic_detail', topic_id=topic_id)

    CardSuggestion.objects.create(
        topic=topic,
        submitted_by=request.user,
        question=question,
        answer=answer,
        hint=hint,
    )
    messages.success(request, 'Thank you! Your card suggestion has been submitted for review.')
    return redirect('topic_detail', topic_id=topic_id)


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
        'streak': _calculate_streak(request.user),
        'badges': _enrich_badges(request.user),
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



@login_required
@require_POST
def update_study_mode(request):
    """Update user's study mode preference"""
    new_mode = request.POST.get('study_mode', 'standard')
    valid_modes = {choice[0] for choice in StudyPreference.STUDY_MODES}
    if new_mode not in valid_modes:
        new_mode = 'standard'
    
    preference, _ = StudyPreference.objects.get_or_create(user=request.user)
    preference.study_mode = new_mode
    preference.save()
    
    messages.success(request, f'Study mode updated to "{preference.get_study_mode_display()}".')
    
    # Redirect back to the referring page or home (validated to prevent open redirects)
    next_url = request.POST.get('next', '')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return redirect(next_url)
    return redirect('home')


# ── Accountability & Motivation ──────────────────────────────────────────────

def _calculate_streak(user):
    """Return the current consecutive-day study streak for a user."""
    today = timezone.now().date()
    streak = 0
    check_date = today
    while True:
        if StudySession.objects.filter(user=user, started_at__date=check_date).exists():
            streak += 1
            check_date -= datetime.timedelta(days=1)
        else:
            break
    return streak


def _get_user_stats(user):
    """Return a dict of aggregated stats used by multiple views."""
    session_agg = StudySession.objects.filter(user=user).aggregate(
        total_sessions=Count('id'),
        total_cards=Sum('cards_studied'),
    )
    progress_agg = FlashcardProgress.objects.filter(user=user).aggregate(
        total_reviewed=Sum('times_reviewed'),
        total_correct=Sum('times_correct'),
    )
    total_reviewed = progress_agg['total_reviewed'] or 0
    total_correct = progress_agg['total_correct'] or 0
    return {
        'total_sessions': session_agg['total_sessions'] or 0,
        'total_cards': session_agg['total_cards'] or 0,
        'average_success_rate': (total_correct / total_reviewed * 100) if total_reviewed else 0,
        'streak': _calculate_streak(user),
    }


def _award_badges(user, stats):
    """Check all badge thresholds and award any newly earned badges. Returns list of new badge dicts."""
    earned_slugs = set(UserBadge.objects.filter(user=user).values_list('badge_slug', flat=True))
    new_badges = []
    for badge in BADGE_DEFINITIONS:
        if badge['slug'] in earned_slugs:
            continue
        if badge['type'] == 'sessions' and stats['total_sessions'] >= badge['threshold']:
            UserBadge.objects.create(user=user, badge_slug=badge['slug'])
            new_badges.append(badge)
        elif badge['type'] == 'cards' and stats['total_cards'] >= badge['threshold']:
            UserBadge.objects.create(user=user, badge_slug=badge['slug'])
            new_badges.append(badge)
        elif badge['type'] == 'streak' and stats['streak'] >= badge['threshold']:
            UserBadge.objects.create(user=user, badge_slug=badge['slug'])
            new_badges.append(badge)
    return new_badges

def _update_topic_score(user, topic):
    """Recompute and save rolling confidence score for user/topic."""
    recent_progress = FlashcardProgress.objects.filter(
        flashcard__topic=topic,
        user=user,
    ).order_by('-last_reviewed')[:10]

    if not recent_progress:
        return

    # confidence_level is 0-5; normalise to 0.0-1.0
    avg = sum(p.confidence_level for p in recent_progress) / (5.0 * len(recent_progress))

    TopicScore.objects.update_or_create(
        user=user,
        topic=topic,
        defaults={
            'score': round(avg, 3),
            'attempt_count': FlashcardProgress.objects.filter(
                flashcard__topic=topic, user=user
            ).count(),
        }
    )



def _enrich_badges(user):
    """Return list of all badge defs annotated with earned status and date."""
    earned = {ub.badge_slug: ub.earned_at for ub in UserBadge.objects.filter(user=user)}
    result = []
    for badge in BADGE_DEFINITIONS:
        b = dict(badge)
        b['earned'] = badge['slug'] in earned
        b['earned_at'] = earned.get(badge['slug'])
        result.append(b)
    return result


@login_required
def accountability_settings(request):
    """Manage study goals, sharing codes, and observer relationships."""
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'set_goal':
            try:
                daily = max(0, int(request.POST.get('daily_cards', 0)))
            except (ValueError, TypeError):
                daily = 0
            goal, _ = StudyGoal.objects.get_or_create(user=request.user)
            goal.daily_cards = daily
            goal.save()
            messages.success(request, 'Study goal updated.')

        elif action == 'create_link':
            label = request.POST.get('label', '').strip()[:100]
            link = AccountabilityLink.objects.create(sharer=request.user, label=label)
            messages.success(request, f'New sharing code created: {link.code}')

        elif action == 'revoke_link':
            link_id = request.POST.get('link_id')
            AccountabilityLink.objects.filter(id=link_id, sharer=request.user).update(is_active=False)
            messages.success(request, 'Sharing code deactivated.')

        elif action == 'leave':
            rel_id = request.POST.get('relationship_id')
            AccountabilityRelationship.objects.filter(id=rel_id, observer=request.user).delete()
            messages.success(request, 'You are no longer observing that user.')

        return redirect('accountability_settings')

    goal, _ = StudyGoal.objects.get_or_create(user=request.user)
    links = AccountabilityLink.objects.filter(sharer=request.user, is_active=True).prefetch_related('observers__observer')
    observing = AccountabilityRelationship.objects.filter(
        observer=request.user, link__is_active=True
    ).select_related('link__sharer')

    # Today's card count for goal progress
    today = timezone.now().date()
    cards_today = StudySession.objects.filter(
        user=request.user, started_at__date=today
    ).aggregate(total=Sum('cards_studied'))['total'] or 0

    return render(request, 'study/accountability.html', {
        'goal': goal,
        'links': links,
        'observing': observing,
        'cards_today': cards_today,
        'streak': _calculate_streak(request.user),
    })


@login_required
def join_accountability(request):
    """Enter a sharing code to observe someone's progress."""
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        try:
            link = AccountabilityLink.objects.get(code=code, is_active=True)
        except AccountabilityLink.DoesNotExist:
            messages.error(request, 'Invalid or expired code.')
            return redirect('join_accountability')

        if link.sharer == request.user:
            messages.error(request, "You can't follow your own code.")
            return redirect('join_accountability')

        _, created = AccountabilityRelationship.objects.get_or_create(
            observer=request.user, link=link
        )
        if created:
            messages.success(request, f"You are now following {link.sharer.username}'s progress.")
        else:
            messages.info(request, f"You are already following {link.sharer.username}.")
        return redirect('observer_dashboard', code=code)

    return render(request, 'study/join_accountability.html')


@login_required
def observer_dashboard(request, code):
    """Read-only view of a sharer's study progress."""
    link = get_object_or_404(AccountabilityLink, code=code, is_active=True)

    # Must be an observer or the sharer themselves
    is_sharer = (link.sharer == request.user)
    is_observer = AccountabilityRelationship.objects.filter(
        observer=request.user, link=link
    ).exists()

    if not is_sharer and not is_observer:
        messages.error(request, 'You need a valid code to view this dashboard.')
        return redirect('join_accountability')

    sharer = link.sharer
    stats = _get_user_stats(sharer)
    recent_sessions = StudySession.objects.filter(user=sharer).select_related(
        'topic', 'topic__course'
    )[:10]
    badges = _enrich_badges(sharer)
    goal, _ = StudyGoal.objects.get_or_create(user=sharer)

    today = timezone.now().date()
    cards_today = StudySession.objects.filter(
        user=sharer, started_at__date=today
    ).aggregate(total=Sum('cards_studied'))['total'] or 0

    return render(request, 'study/observer_dashboard.html', {
        'sharer': sharer,
        'stats': stats,
        'recent_sessions': recent_sessions,
        'badges': badges,
        'goal': goal,
        'cards_today': cards_today,
        'is_sharer': is_sharer,
    })

