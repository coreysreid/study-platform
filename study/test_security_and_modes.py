from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import (
    Course, Topic, Flashcard, StudySession, CourseEnrollment,
    StudyPreference, CardFeedback
)
from .forms import CardFeedbackForm


class LogoutSecurityTestCase(TestCase):
    """Test that logout requires POST to prevent CSRF via GET"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_logout_via_get_does_not_logout(self):
        """GET request to logout should not log the user out"""
        response = self.client.get(reverse('logout'))
        # User should still be authenticated after GET
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_via_post_succeeds(self):
        """POST request to logout should log the user out"""
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        # After POST logout, user should be redirected to home
        # Verify by checking session is cleared
        response = self.client.get(reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class EndStudySessionValidationTestCase(TestCase):
    """Test input validation in end_study_session view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.course = Course.objects.create(name='Test', code='T', created_by=self.user)
        self.topic = Topic.objects.create(course=self.course, name='Topic', order=1)
        self.session = StudySession.objects.create(user=self.user, topic=self.topic)

    def test_negative_cards_studied_clamped_to_zero(self):
        """Negative cards_studied should be clamped to 0"""
        response = self.client.post(
            reverse('end_study_session', args=[self.session.id]),
            {'cards_studied': '-5'}
        )
        self.session.refresh_from_db()
        self.assertEqual(self.session.cards_studied, 0)

    def test_invalid_cards_studied_defaults_to_zero(self):
        """Non-integer cards_studied should default to 0"""
        response = self.client.post(
            reverse('end_study_session', args=[self.session.id]),
            {'cards_studied': 'abc'}
        )
        self.session.refresh_from_db()
        self.assertEqual(self.session.cards_studied, 0)

    def test_valid_cards_studied_accepted(self):
        """Valid positive integer cards_studied should be accepted"""
        response = self.client.post(
            reverse('end_study_session', args=[self.session.id]),
            {'cards_studied': '10'}
        )
        self.session.refresh_from_db()
        self.assertEqual(self.session.cards_studied, 10)


class FeedbackFormValidationTestCase(TestCase):
    """Test server-side validation of CardFeedbackForm"""

    def test_valid_difficulty_rating(self):
        """Difficulty rating within 1-5 should be valid"""
        form = CardFeedbackForm(data={
            'feedback_type': 'confusing',
            'difficulty_rating': 3,
            'comment': 'Test comment'
        })
        self.assertTrue(form.is_valid())

    def test_difficulty_rating_too_high(self):
        """Difficulty rating above 5 should be invalid"""
        form = CardFeedbackForm(data={
            'feedback_type': 'confusing',
            'difficulty_rating': 10,
            'comment': 'Test comment'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('difficulty_rating', form.errors)

    def test_difficulty_rating_too_low(self):
        """Difficulty rating below 1 should be invalid"""
        form = CardFeedbackForm(data={
            'feedback_type': 'confusing',
            'difficulty_rating': 0,
            'comment': 'Test comment'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('difficulty_rating', form.errors)

    def test_null_difficulty_rating_is_valid(self):
        """Null difficulty rating should be valid (it's optional)"""
        form = CardFeedbackForm(data={
            'feedback_type': 'confusing',
            'difficulty_rating': '',
            'comment': 'Test comment'
        })
        self.assertTrue(form.is_valid())


class StudyPreferenceModelTestCase(TestCase):
    """Test StudyPreference model"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_default_preference(self):
        """Test creating a preference with default mode"""
        pref = StudyPreference.objects.create(user=self.user)
        self.assertEqual(pref.study_mode, 'standard')

    def test_update_preference_mode(self):
        """Test updating study mode"""
        pref = StudyPreference.objects.create(user=self.user, study_mode='visual')
        self.assertEqual(pref.study_mode, 'visual')
        pref.study_mode = 'challenge'
        pref.save()
        pref.refresh_from_db()
        self.assertEqual(pref.study_mode, 'challenge')

    def test_preference_str_representation(self):
        """Test string representation"""
        pref = StudyPreference.objects.create(user=self.user, study_mode='visual')
        self.assertIn('testuser', str(pref))
        self.assertIn('Visual', str(pref))


class UpdateStudyModeViewTestCase(TestCase):
    """Test the update_study_mode view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_update_study_mode_post(self):
        """POST should update study mode"""
        response = self.client.post(reverse('update_study_mode'), {
            'study_mode': 'visual'
        })
        self.assertEqual(response.status_code, 302)
        pref = StudyPreference.objects.get(user=self.user)
        self.assertEqual(pref.study_mode, 'visual')

    def test_update_study_mode_invalid_mode(self):
        """Invalid mode should default to standard"""
        response = self.client.post(reverse('update_study_mode'), {
            'study_mode': 'invalid_mode'
        })
        pref = StudyPreference.objects.get(user=self.user)
        self.assertEqual(pref.study_mode, 'standard')

    def test_update_study_mode_get_not_allowed(self):
        """GET should not be allowed"""
        response = self.client.get(reverse('update_study_mode'))
        self.assertEqual(response.status_code, 405)

    def test_update_study_mode_requires_login(self):
        """Unauthenticated users should be redirected"""
        self.client.logout()
        response = self.client.post(reverse('update_study_mode'), {
            'study_mode': 'visual'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_update_study_mode_rejects_open_redirect(self):
        """External URLs in next parameter should be rejected"""
        response = self.client.post(reverse('update_study_mode'), {
            'study_mode': 'visual',
            'next': 'https://evil.example.com'
        })
        self.assertEqual(response.status_code, 302)
        # Should redirect to home, not the external URL
        self.assertEqual(response.url, reverse('home'))

    def test_update_study_mode_allows_safe_redirect(self):
        """Internal relative URLs in next parameter should be allowed"""
        response = self.client.post(reverse('update_study_mode'), {
            'study_mode': 'visual',
            'next': '/statistics/'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/statistics/')


class StudySessionModeTestCase(TestCase):
    """Test study session view with mode parameter"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.course = Course.objects.create(name='Test', code='T', created_by=self.user)
        self.topic = Topic.objects.create(course=self.course, name='Topic', order=1)
        self.flashcard = Flashcard.objects.create(
            topic=self.topic, question='Q?', answer='A', question_type='standard'
        )
        CourseEnrollment.objects.create(user=self.user, course=self.course)

    def test_study_session_default_mode(self):
        """Study session should use user's saved mode by default"""
        StudyPreference.objects.create(user=self.user, study_mode='visual')
        response = self.client.get(reverse('study_session', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['study_mode'], 'visual')

    def test_study_session_mode_override_via_query(self):
        """Mode parameter in URL should override saved preference for the session only"""
        StudyPreference.objects.create(user=self.user, study_mode='standard')
        response = self.client.get(
            reverse('study_session', args=[self.topic.id]) + '?mode=challenge'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['study_mode'], 'challenge')
        # Verify the preference was NOT persisted (temporary override only)
        pref = StudyPreference.objects.get(user=self.user)
        self.assertEqual(pref.study_mode, 'standard')

    def test_study_session_invalid_mode_falls_back_to_preference(self):
        """Invalid mode parameter should fallback to saved preference, not standard"""
        StudyPreference.objects.create(user=self.user, study_mode='visual')
        response = self.client.get(
            reverse('study_session', args=[self.topic.id]) + '?mode=invalid'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['study_mode'], 'visual')
        # Verify saved preference was not changed
        pref = StudyPreference.objects.get(user=self.user)
        self.assertEqual(pref.study_mode, 'visual')

    def test_study_session_includes_mode_list(self):
        """Study session context should include available modes"""
        response = self.client.get(reverse('study_session', args=[self.topic.id]))
        self.assertIn('study_modes', response.context)
        mode_keys = [m[0] for m in response.context['study_modes']]
        self.assertIn('standard', mode_keys)
        self.assertIn('visual', mode_keys)
        self.assertIn('text_heavy', mode_keys)
        self.assertIn('challenge', mode_keys)
