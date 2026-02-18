from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegistrationForm


class RegistrationFormTestCase(TestCase):
    """Test the custom registration form with optional email"""

    def test_registration_without_email(self):
        """Registration should succeed without providing an email"""
        form = RegistrationForm(data={
            'username': 'newuser',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!',
        })
        self.assertTrue(form.is_valid())

    def test_registration_with_email(self):
        """Registration should succeed with an email provided"""
        form = RegistrationForm(data={
            'username': 'newuser',
            'email': 'user@example.com',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!',
        })
        self.assertTrue(form.is_valid())

    def test_registration_with_empty_email(self):
        """Registration should succeed with empty email (explicitly blank)"""
        form = RegistrationForm(data={
            'username': 'newuser',
            'email': '',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!',
        })
        self.assertTrue(form.is_valid())

    def test_registration_with_invalid_email(self):
        """Registration should fail with an invalid email format"""
        form = RegistrationForm(data={
            'username': 'newuser',
            'email': 'not-an-email',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_field_has_help_text(self):
        """Email field should include warning about password recovery"""
        form = RegistrationForm()
        self.assertIn('password recovery', form.fields['email'].help_text)


class RegistrationViewTestCase(TestCase):
    """Test the registration view"""

    def setUp(self):
        self.client = Client()

    def test_register_page_loads(self):
        """Registration page should load successfully"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_register_page_shows_oauth_buttons(self):
        """Registration page should show OAuth sign-in options"""
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'Sign up with GitHub')
        self.assertContains(response, 'Sign up with Google')

    def test_register_page_shows_email_warning(self):
        """Registration page should show warning about no email"""
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'no way to recover your password')

    def test_register_creates_user_without_email(self):
        """POST with valid data (no email) should create user and redirect"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, '')

    def test_register_creates_user_with_email(self):
        """POST with valid data (with email) should create user and redirect"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'user@example.com',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'user@example.com')

    def test_register_redirects_authenticated_user(self):
        """Authenticated users should be redirected from registration page"""
        User.objects.create_user(username='existing', password='testpass')
        self.client.login(username='existing', password='testpass')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)


class LoginViewTestCase(TestCase):
    """Test the login view"""

    def setUp(self):
        self.client = Client()

    def test_login_page_loads(self):
        """Login page should load successfully"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_shows_oauth_buttons(self):
        """Login page should show OAuth sign-in options"""
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'Sign in with GitHub')
        self.assertContains(response, 'Sign in with Google')

    def test_login_page_shows_username_section(self):
        """Login page should show the traditional username/password section"""
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'or sign in with username')


class AdminHiddenFromNavigationTestCase(TestCase):
    """Test that Django admin link is hidden from main navigation"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_admin_link_not_in_navigation(self):
        """Admin link should not appear in the navigation bar"""
        response = self.client.get(reverse('home'))
        # The navigation should not contain a direct link to admin
        content = response.content.decode()
        self.assertNotIn('href="/admin/"', content)

    def test_admin_url_still_accessible(self):
        """Admin should still be accessible via direct URL"""
        response = self.client.get('/admin/', follow=False)
        # Should get a redirect to admin login (302) not a 404
        self.assertIn(response.status_code, [200, 302])
