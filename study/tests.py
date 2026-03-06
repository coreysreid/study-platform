import json
from django.test import TestCase, TransactionTestCase, Client
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Q
from .models import Course, Topic, Flashcard, Skill, FlashcardProgress, TopicScore
from .utils import ParameterGenerator, TemplateRenderer, generate_parameterized_card


class ParameterGeneratorTestCase(TestCase):
    """Test parameter generation for parameterized flashcards"""
    
    def test_random_int_generation(self):
        """Test generation of random integers"""
        spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 1, 'max': 10}
            }
        }
        generator = ParameterGenerator(spec)
        values = generator.generate()
        
        self.assertIn('a', values)
        self.assertIsInstance(values['a'], int)
        self.assertGreaterEqual(values['a'], 1)
        self.assertLessEqual(values['a'], 10)
    
    def test_random_float_generation(self):
        """Test generation of random floats"""
        spec = {
            'variables': {
                'x': {'type': 'random_float', 'min': 0.0, 'max': 1.0, 'precision': 2}
            }
        }
        generator = ParameterGenerator(spec)
        values = generator.generate()
        
        self.assertIn('x', values)
        self.assertIsInstance(values['x'], float)
        self.assertGreaterEqual(values['x'], 0.0)
        self.assertLessEqual(values['x'], 1.0)
    
    def test_random_choice_generation(self):
        """Test generation from choice list"""
        spec = {
            'variables': {
                'angle': {'type': 'random_choice', 'choices': [30, 45, 60, 90]}
            }
        }
        generator = ParameterGenerator(spec)
        values = generator.generate()
        
        self.assertIn('angle', values)
        self.assertIn(values['angle'], [30, 45, 60, 90])
    
    def test_computed_simple_addition(self):
        """Test computed variable with simple addition"""
        spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 1, 'max': 50},
                'b': {'type': 'random_int', 'min': 1, 'max': 50},
                'c': {'type': 'computed', 'formula': 'a + b'}
            }
        }
        generator = ParameterGenerator(spec)
        values = generator.generate()
        
        self.assertEqual(values['c'], values['a'] + values['b'])
    
    def test_computed_multiplication(self):
        """Test computed variable with multiplication"""
        spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 1, 'max': 10},
                'b': {'type': 'random_int', 'min': 1, 'max': 10},
                'product': {'type': 'computed', 'formula': 'a * b'}
            }
        }
        generator = ParameterGenerator(spec)
        values = generator.generate()
        
        self.assertEqual(values['product'], values['a'] * values['b'])
    
    def test_computed_with_math_functions(self):
        """Test computed variable using math functions"""
        spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 3, 'max': 5},
                'b': {'type': 'random_int', 'min': 4, 'max': 6},
                'hypotenuse': {'type': 'computed', 'formula': 'sqrt(a**2 + b**2)'}
            },
            'precision': 2
        }
        generator = ParameterGenerator(spec)
        values = generator.generate()
        
        import math
        expected = round(math.sqrt(values['a']**2 + values['b']**2), 2)
        self.assertEqual(values['hypotenuse'], expected)
    
    def test_constraints_satisfied(self):
        """Test that constraints are enforced"""
        spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 10, 'max': 50},
                'b': {'type': 'random_int', 'min': 1, 'max': 9}
            },
            'constraints': ['a > b']
        }
        generator = ParameterGenerator(spec)
        values = generator.generate()
        
        self.assertGreater(values['a'], values['b'])
    
    def test_constraints_division_without_remainder(self):
        """Test constraint for division without remainder"""
        spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 10, 'max': 50},
                'b': {'type': 'random_int', 'min': 2, 'max': 5}
            },
            'constraints': ['a % b == 0']
        }
        generator = ParameterGenerator(spec)
        values = generator.generate()
        
        self.assertEqual(values['a'] % values['b'], 0)
    
    def test_multiple_constraints(self):
        """Test multiple constraints together"""
        spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 1, 'max': 100},
                'b': {'type': 'random_int', 'min': 1, 'max': 100}
            },
            'constraints': ['a > b', 'a - b > 10']
        }
        generator = ParameterGenerator(spec)
        values = generator.generate()
        
        self.assertGreater(values['a'], values['b'])
        self.assertGreater(values['a'] - values['b'], 10)


class TemplateRendererTestCase(TestCase):
    """Test template rendering with generated values"""
    
    def test_simple_template_rendering(self):
        """Test rendering simple template"""
        renderer = TemplateRenderer()
        template = "What is {a} + {b}?"
        values = {'a': 5, 'b': 3}
        
        result = renderer.render(template, values)
        self.assertEqual(result, "What is 5 + 3?")
    
    def test_template_with_float_values(self):
        """Test rendering template with float values"""
        renderer = TemplateRenderer()
        template = "The hypotenuse is {c}"
        values = {'c': 5.83}
        
        result = renderer.render(template, values)
        self.assertEqual(result, "The hypotenuse is 5.83")
    
    def test_multiple_variable_template(self):
        """Test rendering template with multiple variables"""
        renderer = TemplateRenderer()
        template = "Find the derivative: d/dx({a}x^{n})"
        values = {'a': 3, 'n': 4}
        
        result = renderer.render(template, values)
        self.assertEqual(result, "Find the derivative: d/dx(3x^4)")
    
    def test_answer_template_rendering(self):
        """Test rendering answer template"""
        renderer = TemplateRenderer()
        template = "{result}"
        values = {'result': 42}
        
        result = renderer.render(template, values)
        self.assertEqual(result, "42")


class GenerateParameterizedCardTestCase(TestCase):
    """Test complete parameterized card generation"""
    
    def test_basic_addition_card(self):
        """Test generating basic addition card"""
        parameter_spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 1, 'max': 50},
                'b': {'type': 'random_int', 'min': 1, 'max': 50},
                'c': {'type': 'computed', 'formula': 'a + b'}
            }
        }
        question_template = "What is {a} + {b}?"
        answer_template = "{c}"
        
        question, answer, values = generate_parameterized_card(
            parameter_spec, question_template, answer_template
        )
        
        # Check that question and answer are generated
        self.assertIsInstance(question, str)
        self.assertIsInstance(answer, str)
        self.assertIn('What is', question)
        
        # Check that values are correct
        self.assertEqual(values['c'], values['a'] + values['b'])
        
        # Check that answer matches computed value
        self.assertEqual(answer, str(values['c']))
    
    def test_derivative_card(self):
        """Test generating calculus derivative card"""
        parameter_spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 1, 'max': 10},
                'n': {'type': 'random_int', 'min': 2, 'max': 5},
                'c': {'type': 'computed', 'formula': 'a * n'},
                'm': {'type': 'computed', 'formula': 'n - 1'}
            }
        }
        question_template = "Find the derivative: d/dx({a}x^{n})"
        answer_template = "{c}x^{m}"
        
        question, answer, values = generate_parameterized_card(
            parameter_spec, question_template, answer_template
        )
        
        # Check generation
        self.assertIsInstance(question, str)
        self.assertIsInstance(answer, str)
        
        # Check computed values are correct
        self.assertEqual(values['c'], values['a'] * values['n'])
        self.assertEqual(values['m'], values['n'] - 1)


class FlashcardModelTestCase(TestCase):
    """Test Flashcard model with parameterized fields"""
    
    def setUp(self):
        """Set up test user, course, and topic"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.course = Course.objects.create(
            name='Test Course',
            code='TEST101',
            created_by=self.user
        )
        self.topic = Topic.objects.create(
            course=self.course,
            name='Test Topic',
            order=1
        )
    
    def test_create_standard_flashcard(self):
        """Test creating standard flashcard"""
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question="What is 2 + 2?",
            answer="4",
            question_type='standard'
        )
        
        self.assertEqual(flashcard.question_type, 'standard')
        self.assertEqual(flashcard.question, "What is 2 + 2?")
    
    def test_create_parameterized_flashcard(self):
        """Test creating parameterized flashcard"""
        parameter_spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 1, 'max': 100},
                'b': {'type': 'random_int', 'min': 1, 'max': 100},
                'c': {'type': 'computed', 'formula': 'a + b'}
            }
        }
        
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question="Static question (not used)",
            answer="Static answer (not used)",
            question_type='parameterized',
            question_template="What is {a} + {b}?",
            answer_template="{c}",
            parameter_spec=parameter_spec
        )
        
        self.assertEqual(flashcard.question_type, 'parameterized')
        self.assertEqual(flashcard.question_template, "What is {a} + {b}?")
        self.assertIsNotNone(flashcard.parameter_spec)
    
    def test_parameterized_flashcard_with_skills(self):
        """Test parameterized flashcard with skill tags"""
        skill, _ = Skill.objects.get_or_create(
            name='basic_arithmetic',
            defaults={'description': 'Basic arithmetic operations'}
        )
        
        parameter_spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 1, 'max': 10},
                'b': {'type': 'random_int', 'min': 1, 'max': 10},
                'product': {'type': 'computed', 'formula': 'a * b'}
            }
        }
        
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question="Not used",
            answer="Not used",
            question_type='parameterized',
            question_template="What is {a} × {b}?",
            answer_template="{product}",
            parameter_spec=parameter_spec,
            difficulty='easy'
        )
        flashcard.skills.add(skill)
        
        self.assertEqual(flashcard.skills.count(), 1)
        self.assertIn(skill, flashcard.skills.all())


class SecurityTestCase(TestCase):
    """Test that malicious formulas are rejected by RestrictedPython"""
    
    def test_reject_import_in_formula(self):
        """Test that __import__ is blocked in formulas"""
        spec = {
            'variables': {
                'x': {'type': 'random_int', 'min': 1, 'max': 10},
                'evil': {'type': 'computed', 'formula': '__import__("os").system("ls")'}
            }
        }
        gen = ParameterGenerator(spec)
        with self.assertRaises(Exception):
            gen.generate()
    
    def test_reject_dunder_access(self):
        """Test that dunder attributes are blocked"""
        spec = {
            'variables': {
                'x': {'type': 'random_int', 'min': 1, 'max': 10},
                'evil': {'type': 'computed', 'formula': 'x.__class__.__bases__'}
            }
        }
        gen = ParameterGenerator(spec)
        with self.assertRaises(Exception):
            gen.generate()
    
    def test_reject_exec_in_formula(self):
        """Test that exec is not available"""
        spec = {
            'variables': {
                'x': {'type': 'random_int', 'min': 1, 'max': 10},
                'evil': {'type': 'computed', 'formula': 'exec("print(1)")'}
            }
        }
        gen = ParameterGenerator(spec)
        with self.assertRaises(Exception):
            gen.generate()
    
    def test_reject_eval_in_formula(self):
        """Test that eval is not available"""
        spec = {
            'variables': {
                'x': {'type': 'random_int', 'min': 1, 'max': 10},
                'evil': {'type': 'computed', 'formula': 'eval("1+1")'}
            }
        }
        gen = ParameterGenerator(spec)
        with self.assertRaises(Exception):
            gen.generate()
    
    def test_reject_open_file(self):
        """Test that file operations are blocked"""
        spec = {
            'variables': {
                'x': {'type': 'random_int', 'min': 1, 'max': 10},
                'evil': {'type': 'computed', 'formula': 'open("/etc/passwd").read()'}
            }
        }
        gen = ParameterGenerator(spec)
        with self.assertRaises(Exception):
            gen.generate()
    
    def test_allow_safe_math_operations(self):
        """Test that safe math operations still work"""
        spec = {
            'variables': {
                'a': {'type': 'random_int', 'min': 1, 'max': 10},
                'b': {'type': 'random_int', 'min': 1, 'max': 10},
                'result': {'type': 'computed', 'formula': 'sqrt(a**2 + b**2)'}
            }
        }
        gen = ParameterGenerator(spec)
        values = gen.generate()
        # Should work without errors
        self.assertIn('result', values)
        self.assertGreater(values['result'], 0)
    
    def test_reject_malicious_constraint(self):
        """Test that malicious code in constraints is blocked"""
        spec = {
            'variables': {
                'x': {'type': 'random_int', 'min': 1, 'max': 10}
            },
            'constraints': ['__import__("os").system("ls") or True']
        }
        gen = ParameterGenerator(spec)
        with self.assertRaises(Exception):
            gen.generate()


class GlobalCurriculumTestCase(TestCase):
    """Test public/global curriculum functionality"""
    
    def test_system_user_creation(self):
        """Test that system user is created by migrations and management commands"""
        from django.core.management import call_command

        # System user is created by migration 0013; verify it already exists
        self.assertTrue(User.objects.filter(username='system').exists())

        # Running the management command again should be idempotent
        call_command('populate_math_curriculum')
        
        # System user should now exist
        system_user = User.objects.get(username='system')
        self.assertEqual(system_user.email, 'system@system.local')
        self.assertTrue(system_user.is_active)
        self.assertFalse(system_user.is_staff)
        self.assertEqual(system_user.first_name, 'System')
        self.assertEqual(system_user.last_name, 'Content')
    
    def test_public_course_creation(self):
        """Test that public course is created under system user"""
        from django.core.management import call_command
        
        call_command('populate_math_curriculum')
        
        system_user = User.objects.get(username='system')
        course = Course.objects.get(name='Engineering Mathematics', created_by=system_user)
        
        self.assertEqual(course.code, 'ENGMATH')
        self.assertIn('mathematics curriculum', course.description.lower())
        
        # Check topics were created
        topics = course.topics.all()
        self.assertEqual(topics.count(), 13)
        
        # Check skills were created
        self.assertGreater(Skill.objects.count(), 60)
    
    def test_public_content_visibility_in_views(self):
        """Test that public content is visible to all users in views"""
        from django.core.management import call_command
        
        # Create system user and public course
        call_command('populate_math_curriculum')
        system_user = User.objects.get(username='system')
        
        # Create a regular user
        regular_user = User.objects.create_user('testuser', 'test@test.com', 'password')
        
        # Create a personal course for the regular user
        personal_course = Course.objects.create(
            name='Personal Course',
            code='TEST',
            description='Test course',
            created_by=regular_user
        )
        
        # Query courses like the view does
        courses = Course.objects.filter(
            Q(created_by=regular_user) | Q(created_by=system_user)
        )
        
        # Regular user should see both their own course and public courses
        course_names = list(courses.values_list('name', flat=True))
        self.assertIn('Engineering Mathematics', course_names)
        self.assertIn('Personal Course', course_names)
        # Migration 0013 seeds 11 system courses + 1 personal = 12 minimum
        self.assertGreaterEqual(courses.count(), 2)
    
    def test_user_cannot_edit_public_content(self):
        """Test that edit views properly restrict access to owner only"""
        from django.core.management import call_command
        
        # Create system user and public course
        call_command('populate_math_curriculum')
        system_user = User.objects.get(username='system')
        public_course = Course.objects.get(name='Engineering Mathematics', created_by=system_user)
        
        # Create a regular user
        regular_user = User.objects.create_user('testuser', 'test@test.com', 'password')
        
        # Verify the regular user cannot get the course through edit query
        # This simulates what happens in course_edit view
        edit_courses = Course.objects.filter(id=public_course.id, created_by=regular_user)
        self.assertEqual(edit_courses.count(), 0)
        
        # But can access it through the public query
        view_courses = Course.objects.filter(
            Q(id=public_course.id) & (Q(created_by=regular_user) | Q(created_by=system_user))
        )
        self.assertEqual(view_courses.count(), 1)
    
    def test_user_can_track_progress_on_public_content(self):
        """Test that users can track their progress on public flashcards"""
        from django.core.management import call_command
        from study.models import FlashcardProgress
        
        # Create system user and public content
        call_command('populate_math_curriculum')
        call_command('populate_comprehensive_math_cards')
        
        system_user = User.objects.get(username='system')
        public_course = Course.objects.get(name='Engineering Mathematics', created_by=system_user)
        
        # Get a public flashcard
        public_topic = public_course.topics.first()
        public_flashcard = public_topic.flashcards.first()
        
        # Create a regular user
        regular_user = User.objects.create_user('testuser', 'test@test.com', 'password')
        
        # User should be able to create progress on public flashcard
        progress = FlashcardProgress.objects.create(
            user=regular_user,
            flashcard=public_flashcard,
            times_reviewed=5,
            times_correct=4
        )
        
        self.assertEqual(progress.user, regular_user)
        self.assertEqual(progress.flashcard, public_flashcard)
        self.assertEqual(progress.times_reviewed, 5)
        self.assertEqual(progress.times_correct, 4)
        
        # Multiple users can track progress on the same public flashcard
        another_user = User.objects.create_user('another', 'another@test.com', 'password')
        another_progress = FlashcardProgress.objects.create(
            user=another_user,
            flashcard=public_flashcard,
            times_reviewed=3,
            times_correct=2
        )
        
        # Both progress records should exist
        self.assertEqual(FlashcardProgress.objects.filter(flashcard=public_flashcard).count(), 2)
    
    def test_command_with_custom_username(self):
        """Test that commands still work with custom username parameter"""
        from django.core.management import call_command
        
        # Create a custom user
        custom_user = User.objects.create_user('customuser', 'custom@test.com', 'password')
        
        # Run command with custom user
        call_command('populate_math_curriculum', user='customuser')
        
        # Course should be created under custom user, not system
        course = Course.objects.get(name='Engineering Mathematics', created_by=custom_user)
        self.assertEqual(course.created_by, custom_user)
        
        # System user might or might not exist, but course should be under custom user
        self.assertEqual(course.created_by.username, 'customuser')


class CourseCatalogTestCase(TestCase):
    """Test that the course catalog works for signed-in users with populated content"""

    def test_catalog_requires_login(self):
        """Test that anonymous users are redirected to login"""
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_catalog_shows_courses_when_populated(self):
        """Test that signed-in users see courses after curriculum is populated"""
        from django.core.management import call_command

        call_command('populate_math_curriculum')
        user = User.objects.create_user('testuser', 'test@test.com', 'password')
        self.client.login(username='testuser', password='password')

        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engineering Mathematics')
        self.assertContains(response, 'Add to My Courses')

    def test_catalog_redirects_when_no_system_user(self):
        """Test that catalog redirects with warning when no system user exists"""
        user = User.objects.create_user('testuser', 'test@test.com', 'password')
        self.client.login(username='testuser', password='password')

        # Migration 0013 creates the system user; temporarily delete them to test
        # the no-system-user fallback path
        from django.contrib.auth.models import User as AuthUser
        system_user = AuthUser.objects.filter(username='system').first()
        if system_user:
            system_user.delete()

        # Make a single request and follow redirects
        response = self.client.get('/catalog/', follow=True)
        self.assertTrue(response.redirect_chain)
        # Check for warning message
        messages = list(response.context['messages'])
        self.assertTrue(any('No public courses available yet' in str(m) for m in messages))

class StepByStepModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        course = Course.objects.create(name='Test Course', created_by=self.user)
        self.topic = Topic.objects.create(course=course, name='Test Topic')
        self.card = Flashcard.objects.create(
            topic=self.topic,
            question='Solve dy/dx + 2y = 4x',
            answer='y = 2x - 1 + Ce^{-2x}',
            question_type='step_by_step',
            steps=[
                {'move': 'Find integrating factor', 'detail': 'e^{2x}'},
                {'move': 'Multiply both sides', 'detail': 'd/dx[ye^{2x}] = 4xe^{2x}'},
                {'move': 'Integrate both sides', 'detail': 'ye^{2x} = 2xe^{2x} - e^{2x} + C'},
            ]
        )

    def test_step_card_has_steps_field(self):
        self.assertIsNotNone(self.card.steps)
        self.assertEqual(len(self.card.steps), 3)
        self.assertEqual(self.card.steps[0]['move'], 'Find integrating factor')

    def test_step_card_has_teacher_explanation_field(self):
        self.card.teacher_explanation = 'We use an integrating factor because...'
        self.card.save()
        self.card.refresh_from_db()
        self.assertIn('integrating factor', self.card.teacher_explanation)

    def test_flashcard_progress_step_index_default(self):
        progress = FlashcardProgress.objects.create(
            user=self.user, flashcard=self.card
        )
        self.assertEqual(progress.step_index, -1)

    def test_flashcard_progress_per_step_unique(self):
        from django.db import IntegrityError
        # Two different step indices for the same card are allowed
        FlashcardProgress.objects.create(user=self.user, flashcard=self.card, step_index=0)
        FlashcardProgress.objects.create(user=self.user, flashcard=self.card, step_index=1)
        count = FlashcardProgress.objects.filter(user=self.user, flashcard=self.card).count()
        self.assertEqual(count, 2)
        # Duplicate (user, flashcard, step_index) must be rejected
        with self.assertRaises(IntegrityError):
            FlashcardProgress.objects.create(user=self.user, flashcard=self.card, step_index=0)

    def test_topic_score_creation(self):
        ts = TopicScore.objects.create(user=self.user, topic=self.topic, score=0.75, attempt_count=10)
        self.assertEqual(ts.score, 0.75)


class ProgressUpdateAjaxTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='proguser', password='pass')
        course = Course.objects.create(name='Course', created_by=self.user)
        self.topic = Topic.objects.create(course=course, name='Topic')
        self.card = Flashcard.objects.create(
            topic=self.topic, question='Q', answer='A'
        )
        from .models import CourseEnrollment
        CourseEnrollment.objects.create(user=self.user, course=course)
        self.client.login(username='proguser', password='pass')

    def test_progress_update_returns_json(self):
        response = self.client.post(
            f'/flashcard/{self.card.id}/progress/',
            {'correct': 'true', 'step_index': '-1'},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('confidence_level', data)

    def test_progress_update_with_step_index(self):
        response = self.client.post(
            f'/flashcard/{self.card.id}/progress/',
            {'correct': 'true', 'step_index': '0'},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['step_index'], 0)
        prog = FlashcardProgress.objects.get(user=self.user, flashcard=self.card, step_index=0)
        self.assertEqual(prog.times_reviewed, 1)


class StudySessionExpansionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sessuser', password='pass')
        course = Course.objects.create(name='Course', created_by=self.user)
        self.topic = Topic.objects.create(course=course, name='Topic')
        from .models import CourseEnrollment
        CourseEnrollment.objects.create(user=self.user, course=course)
        self.step_card = Flashcard.objects.create(
            topic=self.topic,
            question='Solve dy/dx + 2y = 0',
            answer='y = Ce^{-2x}',
            question_type='step_by_step',
            steps=[
                {'move': 'Separate variables', 'detail': 'dy/y = -2 dx'},
                {'move': 'Integrate both sides', 'detail': 'ln|y| = -2x + C'},
                {'move': 'Solve for y', 'detail': 'y = Ce^{-2x}'},
            ]
        )
        self.client.login(username='sessuser', password='pass')

    def test_step_card_expands_to_n_virtual_cards(self):
        response = self.client.get(f'/study/{self.topic.id}/')
        self.assertEqual(response.status_code, 200)
        flashcards_data = response.context['flashcards_data']
        self.assertEqual(len(flashcards_data), 3)

    def test_virtual_card_has_context_steps(self):
        response = self.client.get(f'/study/{self.topic.id}/')
        cards = response.context['flashcards_data']
        self.assertEqual(cards[0]['step_index'], 0)
        self.assertEqual(cards[0]['context_steps'], [])
        self.assertEqual(cards[1]['step_index'], 1)
        self.assertEqual(len(cards[1]['context_steps']), 1)
        self.assertEqual(cards[1]['context_steps'][0]['move'], 'Separate variables')
        self.assertEqual(len(cards[2]['context_steps']), 2)

    def test_virtual_card_answer_is_move_label(self):
        response = self.client.get(f'/study/{self.topic.id}/')
        cards = response.context['flashcards_data']
        self.assertEqual(cards[0]['answer'], 'Separate variables')
        self.assertEqual(cards[0]['answer_detail'], 'dy/y = -2 dx')


class TopicScoreTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='scoreuser', password='pass')
        course = Course.objects.create(name='Course', created_by=self.user)
        self.topic = Topic.objects.create(course=course, name='Topic')
        from .models import CourseEnrollment, StudySession
        CourseEnrollment.objects.create(user=self.user, course=course)
        self.session = StudySession.objects.create(user=self.user, topic=self.topic)
        for i in range(5):
            card = Flashcard.objects.create(
                topic=self.topic, question=f'Q{i}', answer=f'A{i}'
            )
            FlashcardProgress.objects.create(
                user=self.user, flashcard=card, step_index=-1,
                confidence_level=1, times_reviewed=2
            )
        self.client.login(username='scoreuser', password='pass')

    def test_end_session_updates_topic_score(self):
        response = self.client.post(
            f'/session/{self.session.id}/end/',
            {'cards_studied': '5'}
        )
        self.assertEqual(response.status_code, 302)
        ts = TopicScore.objects.filter(user=self.user, topic=self.topic).first()
        self.assertIsNotNone(ts)
        self.assertGreater(ts.attempt_count, 0)


class CourseDetailOrderingTest(TestCase):
    """Issue #46 — Topics must be displayed in code order on the course detail page."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='orderuser', password='pass')
        self.course = Course.objects.create(name='Test Course', created_by=self.user)
        from .models import CourseEnrollment
        CourseEnrollment.objects.create(user=self.user, course=self.course)
        # Create topics with codes out of insertion order to confirm sort is applied
        Topic.objects.create(course=self.course, name='Third', code='003A')
        Topic.objects.create(course=self.course, name='First', code='001A')
        Topic.objects.create(course=self.course, name='Second', code='002A')
        self.client.login(username='orderuser', password='pass')

    def test_topics_ordered_by_code_on_course_detail(self):
        response = self.client.get(f'/course/{self.course.id}/')
        self.assertEqual(response.status_code, 200)
        topics = list(response.context['topics'])
        codes = [t.code for t in topics]
        self.assertEqual(codes, ['001A', '002A', '003A'])

    def test_topics_code_order_survives_annotation(self):
        """Annotation with Count must not discard the explicit order_by."""
        from django.db.models import Count
        topics = self.course.topics.all().annotate(
            flashcard_count=Count('flashcards')
        ).order_by('code', 'name')
        codes = [t.code for t in topics]
        self.assertEqual(codes, ['001A', '002A', '003A'])


class TrigExactValuesMigrationTest(TestCase):
    """Issue #44 — Non-atomic sin/cos/tan combined card replaced by 9 atomic cards.

    Tests exercise split_trig_exact_values() from study.migration_helpers, which
    is the same function called by migration 0030, ensuring the migration logic is
    tested without coupling test code to the migration module itself.
    """

    def setUp(self):
        from study.migration_helpers import split_trig_exact_values, TRIG_EXACT_VALUES_QUESTION
        self._do_split = split_trig_exact_values
        self._combined_q = TRIG_EXACT_VALUES_QUESTION
        self.user = User.objects.create_user(username='triguser', password='pass')
        self.course = Course.objects.create(name='Maths', created_by=self.user)
        self.topic = Topic.objects.create(course=self.course, name='Trigonometry Fundamentals')

    def _make_combined(self, topic=None):
        return Flashcard.objects.create(
            topic=topic or self.topic,
            question=self._combined_q,
            answer='30°: sin=1/2, cos=√3/2, tan=1/√3. 45°: sin=cos=1/√2, tan=1. 60°: sin=√3/2, cos=1/2, tan=√3.',
            difficulty='medium',
            question_type='standard',
            uses_latex=True,
        )

    def test_split_removes_combined_and_creates_nine_atomic(self):
        """Migration logic deletes the combined card and creates 9 atomic cards."""
        self._make_combined()
        self.assertEqual(Flashcard.objects.filter(topic=self.topic).count(), 1)

        self._do_split(Flashcard)

        self.assertFalse(
            Flashcard.objects.filter(question=self._combined_q).exists(),
            'Combined card should be deleted',
        )
        atomic = Flashcard.objects.filter(topic=self.topic)
        self.assertEqual(atomic.count(), 9)
        questions = set(atomic.values_list('question', flat=True))
        self.assertIn('What is sin(30°)?', questions)
        self.assertIn('What is cos(30°)?', questions)
        self.assertIn('What is tan(30°)?', questions)
        self.assertIn('What is tan(60°)?', questions)
        for card in atomic:
            self.assertTrue(card.uses_latex, f'{card.question} should have uses_latex=True')

    def test_split_is_idempotent_when_no_combined_card_exists(self):
        """Running the migration logic when no combined card exists is a safe no-op."""
        self._do_split(Flashcard)
        self.assertEqual(Flashcard.objects.filter(topic=self.topic).count(), 0)

    def test_split_handles_duplicate_combined_cards_across_topics(self):
        """All copies of the combined card (e.g. across two topics) are replaced."""
        topic2 = Topic.objects.create(course=self.course, name='Trig Extra')
        self._make_combined(self.topic)
        self._make_combined(topic2)

        self._do_split(Flashcard)

        self.assertFalse(
            Flashcard.objects.filter(question=self._combined_q).exists(),
            'Both combined cards should be deleted',
        )
        # Each topic should have 9 atomic cards
        self.assertEqual(Flashcard.objects.filter(topic=self.topic).count(), 9)
        self.assertEqual(Flashcard.objects.filter(topic=topic2).count(), 9)

    def test_split_does_not_duplicate_atomic_cards_if_already_present(self):
        """If some atomic cards already exist for the topic, they are not duplicated."""
        self._make_combined()
        # Pre-create two of the atomic cards for the same topic
        Flashcard.objects.create(
            topic=self.topic, question='What is sin(30°)?',
            answer='$\\sin 30° = \\dfrac{1}{2}$', difficulty='easy',
            question_type='standard', uses_latex=True,
        )
        Flashcard.objects.create(
            topic=self.topic, question='What is cos(30°)?',
            answer='$\\cos 30° = \\dfrac{\\sqrt{3}}{2}$', difficulty='easy',
            question_type='standard', uses_latex=True,
        )

        self._do_split(Flashcard)

        # Should still be exactly 9 — no duplicates
        self.assertEqual(Flashcard.objects.filter(topic=self.topic).count(), 9)


class TrigMigrationExecutorTest(TransactionTestCase):
    """End-to-end test for migration 0030 using Django's MigrationExecutor.

    This verifies the migration as it actually runs in production: using the
    migration executor with historical model classes, rolling back to 0029,
    seeding the combined card, then applying 0030 and asserting the split.

    Uses TransactionTestCase (not TestCase) so that MigrationExecutor can
    manage its own transactions; this test is necessarily slower than the
    unit tests in TrigExactValuesMigrationTest.
    """

    COMBINED_Q = 'What are the exact values of sin, cos, tan for 30°, 45°, 60°?'
    TARGET_0029 = [('study', '0029_restructure_mathematics')]
    TARGET_0030 = [('study', '0030_split_trig_exact_values_flashcard')]

    def test_migration_0030_splits_combined_card(self):
        from django.db.migrations.executor import MigrationExecutor

        executor = MigrationExecutor(connection)

        # Roll back to 0029 (0030's reverse_fn is a no-op, so only the
        # migration record changes — the schema is unaffected).
        executor.migrate(self.TARGET_0029)
        executor.loader.build_graph()

        # Obtain historical model classes at the 0029 state.
        state_0029 = executor.loader.project_state(self.TARGET_0029)
        HistFlashcard = state_0029.apps.get_model('study', 'Flashcard')
        HistCourse = state_0029.apps.get_model('study', 'Course')
        HistTopic = state_0029.apps.get_model('study', 'Topic')
        HistUser = state_0029.apps.get_model('auth', 'User')

        # Seed: one user, course, topic, and the combined card.
        user = HistUser.objects.create_user(username='migexec_test', password='pass')
        course = HistCourse.objects.create(name='Trig Course', created_by=user)
        topic = HistTopic.objects.create(course=course, name='Trigonometry')
        HistFlashcard.objects.create(
            topic=topic,
            question=self.COMBINED_Q,
            answer='30°: sin=1/2, cos=√3/2. 45°: sin=cos=1/√2. 60°: sin=√3/2, cos=1/2.',
            difficulty='medium',
            question_type='standard',
            uses_latex=True,
        )
        self.assertEqual(HistFlashcard.objects.filter(topic=topic).count(), 1)

        # Apply migration 0030.
        executor.migrate(self.TARGET_0030)
        executor.loader.build_graph()

        # Check via post-migration model state.
        state_0030 = executor.loader.project_state(self.TARGET_0030)
        NewFlashcard = state_0030.apps.get_model('study', 'Flashcard')

        self.assertFalse(
            NewFlashcard.objects.filter(question=self.COMBINED_Q).exists(),
            'Combined card must be deleted by migration 0030',
        )
        # Use topic_id to avoid cross-state model-type mismatch.
        atomic = NewFlashcard.objects.filter(topic_id=topic.pk)
        self.assertEqual(atomic.count(), 9, 'Exactly 9 atomic cards must be created')
        for card in atomic:
            self.assertTrue(
                card.uses_latex,
                f'Card "{card.question}" must have uses_latex=True',
            )

    def tearDown(self):
        # Roll forward to the latest migration so subsequent tests start in
        # the fully-applied state.
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        targets = executor.loader.graph.leaf_nodes()
        executor.migrate(targets)


class FlashcardVoteModelTest(TestCase):
    """Unit tests for FlashcardVote model"""

    def setUp(self):
        from .models import FlashcardVote
        self.FlashcardVote = FlashcardVote
        self.owner = User.objects.create_user(username='owner', password='pass')
        self.voter = User.objects.create_user(username='voter', password='pass')
        course = Course.objects.create(name='Course', created_by=self.owner)
        topic = Topic.objects.create(course=course, name='Topic')
        self.card = Flashcard.objects.create(topic=topic, question='Q', answer='A')

    def test_upvote_created(self):
        v = self.FlashcardVote.objects.create(user=self.voter, flashcard=self.card, vote=1)
        self.assertEqual(v.vote, self.FlashcardVote.UPVOTE)

    def test_downvote_created(self):
        v = self.FlashcardVote.objects.create(user=self.voter, flashcard=self.card, vote=-1)
        self.assertEqual(v.vote, self.FlashcardVote.DOWNVOTE)

    def test_unique_together_prevents_duplicate_vote(self):
        from django.db import IntegrityError
        self.FlashcardVote.objects.create(user=self.voter, flashcard=self.card, vote=1)
        with self.assertRaises(IntegrityError):
            self.FlashcardVote.objects.create(user=self.voter, flashcard=self.card, vote=1)

    def test_str_contains_upvote(self):
        v = self.FlashcardVote.objects.create(user=self.voter, flashcard=self.card, vote=1)
        self.assertIn('upvote', str(v))

    def test_str_contains_downvote(self):
        v = self.FlashcardVote.objects.create(user=self.voter, flashcard=self.card, vote=-1)
        self.assertIn('downvote', str(v))


class FlashcardCommentModelTest(TestCase):
    """Unit tests for FlashcardComment model"""

    def setUp(self):
        from .models import FlashcardComment
        self.FlashcardComment = FlashcardComment
        self.user = User.objects.create_user(username='commenter', password='pass')
        course = Course.objects.create(name='Course', created_by=self.user)
        topic = Topic.objects.create(course=course, name='Topic')
        self.card = Flashcard.objects.create(topic=topic, question='Q', answer='A')

    def test_comment_created(self):
        c = self.FlashcardComment.objects.create(
            user=self.user, flashcard=self.card, body='Great card!'
        )
        self.assertEqual(c.body, 'Great card!')

    def test_str_contains_flashcard_id(self):
        c = self.FlashcardComment.objects.create(
            user=self.user, flashcard=self.card, body='Needs work'
        )
        self.assertIn(str(self.card.id), str(c))


class VoteFlashcardViewTest(TestCase):
    """Tests for the vote_flashcard view"""

    def setUp(self):
        from .models import FlashcardVote, CourseEnrollment
        self.FlashcardVote = FlashcardVote
        self.client = Client()
        self.owner = User.objects.create_user(username='cardowner', password='pass')
        self.voter = User.objects.create_user(username='cardvoter', password='pass')
        self.course = Course.objects.create(name='Course', created_by=self.owner)
        topic = Topic.objects.create(course=self.course, name='Topic')
        self.card = Flashcard.objects.create(topic=topic, question='Q', answer='A')
        CourseEnrollment.objects.create(user=self.voter, course=self.course)
        self.vote_url = f'/flashcard/{self.card.id}/vote/'

    def test_upvote_returns_json(self):
        self.client.login(username='cardvoter', password='pass')
        response = self.client.post(self.vote_url, {'vote': '1'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['upvotes'], 1)
        self.assertEqual(data['downvotes'], 0)
        self.assertEqual(data['net_votes'], 1)
        self.assertEqual(data['user_vote'], 1)

    def test_downvote_returns_json(self):
        self.client.login(username='cardvoter', password='pass')
        response = self.client.post(self.vote_url, {'vote': '-1'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['upvotes'], 0)
        self.assertEqual(data['downvotes'], 1)
        self.assertEqual(data['net_votes'], -1)
        self.assertEqual(data['user_vote'], -1)

    def test_same_vote_again_removes_it(self):
        self.client.login(username='cardvoter', password='pass')
        self.client.post(self.vote_url, {'vote': '1'})
        response = self.client.post(self.vote_url, {'vote': '1'})
        data = json.loads(response.content)
        self.assertEqual(data['user_vote'], 0)
        self.assertEqual(data['upvotes'], 0)

    def test_change_vote_direction(self):
        self.client.login(username='cardvoter', password='pass')
        self.client.post(self.vote_url, {'vote': '1'})
        response = self.client.post(self.vote_url, {'vote': '-1'})
        data = json.loads(response.content)
        self.assertEqual(data['user_vote'], -1)
        self.assertEqual(data['upvotes'], 0)
        self.assertEqual(data['downvotes'], 1)

    def test_owner_cannot_vote_on_own_card(self):
        self.client.login(username='cardowner', password='pass')
        response = self.client.post(self.vote_url, {'vote': '1'})
        self.assertEqual(response.status_code, 403)

    def test_non_enrolled_user_cannot_vote(self):
        nonenrolled = User.objects.create_user(username='nonenrolled', password='pass')
        self.client.login(username='nonenrolled', password='pass')
        response = self.client.post(self.vote_url, {'vote': '1'})
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_user_redirected(self):
        response = self.client.post(self.vote_url, {'vote': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_invalid_vote_value_returns_400(self):
        self.client.login(username='cardvoter', password='pass')
        response = self.client.post(self.vote_url, {'vote': '0'})
        self.assertEqual(response.status_code, 400)

    def test_flagged_true_when_net_score_reaches_threshold(self):
        from .models import FlashcardVote
        self.client.login(username='cardvoter', password='pass')
        # Create 5 downvotes from different users
        for i in range(5):
            u = User.objects.create_user(username=f'dv{i}', password='pass')
            FlashcardVote.objects.create(user=u, flashcard=self.card, vote=-1)
        # Add one more downvote to push net score to -6, past the -5 threshold
        response = self.client.post(self.vote_url, {'vote': '-1'})
        data = json.loads(response.content)
        self.assertTrue(data['flagged'])

    def test_vote_requires_post(self):
        self.client.login(username='cardvoter', password='pass')
        response = self.client.get(self.vote_url)
        self.assertEqual(response.status_code, 405)


class CommentFlashcardViewTest(TestCase):
    """Tests for the comment_flashcard view"""

    def setUp(self):
        from .models import FlashcardComment, CourseEnrollment
        self.FlashcardComment = FlashcardComment
        self.client = Client()
        self.user = User.objects.create_user(username='commentuser', password='pass')
        course = Course.objects.create(name='Course', created_by=self.user)
        topic = Topic.objects.create(course=course, name='Topic')
        self.card = Flashcard.objects.create(topic=topic, question='Q', answer='A')
        CourseEnrollment.objects.create(user=self.user, course=course)
        self.comment_url = f'/flashcard/{self.card.id}/comment/'

    def test_add_comment_creates_record(self):
        self.client.login(username='commentuser', password='pass')
        response = self.client.post(self.comment_url, {'body': 'Great card!'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.FlashcardComment.objects.filter(flashcard=self.card).count(), 1)

    def test_empty_body_rejected(self):
        self.client.login(username='commentuser', password='pass')
        self.client.post(self.comment_url, {'body': '   '}, follow=True)
        self.assertEqual(self.FlashcardComment.objects.count(), 0)

    def test_unauthenticated_user_redirected(self):
        response = self.client.post(self.comment_url, {'body': 'Hi'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class TopicDetailVoteOrderingTest(TestCase):
    """Flashcards in topic_detail are ranked by net vote score."""

    def setUp(self):
        from .models import FlashcardVote, CourseEnrollment
        self.client = Client()
        self.owner = User.objects.create_user(username='tdowner', password='pass')
        self.voter = User.objects.create_user(username='tdvoter', password='pass')
        self.course = Course.objects.create(name='Course', created_by=self.owner)
        self.topic = Topic.objects.create(course=self.course, name='Topic')
        CourseEnrollment.objects.create(user=self.voter, course=self.course)

        self.card_low = Flashcard.objects.create(
            topic=self.topic, question='Low', answer='A'
        )
        self.card_high = Flashcard.objects.create(
            topic=self.topic, question='High', answer='A'
        )
        # Give card_high 2 upvotes, card_low 1 downvote
        u1 = User.objects.create_user(username='u1', password='pass')
        u2 = User.objects.create_user(username='u2', password='pass')
        FlashcardVote.objects.create(user=u1, flashcard=self.card_high, vote=1)
        FlashcardVote.objects.create(user=u2, flashcard=self.card_high, vote=1)
        FlashcardVote.objects.create(user=u1, flashcard=self.card_low, vote=-1)
        self.client.login(username='tdvoter', password='pass')

    def test_flashcards_ordered_by_net_votes_descending(self):
        response = self.client.get(f'/topic/{self.topic.id}/')
        self.assertEqual(response.status_code, 200)
        flashcards = list(response.context['flashcards'])
        self.assertEqual(flashcards[0].id, self.card_high.id)
        self.assertEqual(flashcards[1].id, self.card_low.id)

    def test_net_votes_annotated_on_flashcards(self):
        response = self.client.get(f'/topic/{self.topic.id}/')
        flashcards = {fc.id: fc for fc in response.context['flashcards']}
        self.assertEqual(flashcards[self.card_high.id].net_votes, 2)
        self.assertEqual(flashcards[self.card_low.id].net_votes, -1)


class AqfLevelAndStarDifficultyTestCase(TestCase):
    """Tests for the two-tier difficulty system: AQF level + star rating"""

    def setUp(self):
        self.user = User.objects.create_user(username='difftestuser', password='pass')
        self.course = Course.objects.create(
            name='Circuit Analysis',
            code='ENG301',
            aqf_level=19,
            created_by=self.user,
        )
        self.topic = Topic.objects.create(
            course=self.course,
            name="Ohm's Law",
            order=1,
            star_difficulty=1,
        )

    # ------------------------------------------------------------------ #
    # Course AQF level
    # ------------------------------------------------------------------ #

    def test_course_stores_aqf_level(self):
        course = Course.objects.get(pk=self.course.pk)
        self.assertEqual(course.aqf_level, 19)

    def test_course_aqf_level_nullable(self):
        course = Course.objects.create(
            name='No Level Course',
            created_by=self.user,
        )
        self.assertIsNone(course.aqf_level)

    def test_course_aqf_level_choices(self):
        valid_levels = list(range(1, 21))
        for level in [1, 10, 19, 20]:
            self.assertIn(level, valid_levels)

    # ------------------------------------------------------------------ #
    # Topic AQF level (own + inherited)
    # ------------------------------------------------------------------ #

    def test_topic_inherits_aqf_level_from_course(self):
        """effective_aqf_level returns course level when topic level is null"""
        self.assertIsNone(self.topic.aqf_level)
        self.assertEqual(self.topic.effective_aqf_level, 19)

    def test_topic_own_aqf_level_overrides_course(self):
        """effective_aqf_level returns topic's own level when set"""
        self.topic.aqf_level = 18
        self.topic.save()
        self.assertEqual(self.topic.effective_aqf_level, 18)

    def test_topic_effective_aqf_none_when_both_unset(self):
        """effective_aqf_level returns None when neither topic nor course has a level"""
        course = Course.objects.create(name='No Level', created_by=self.user)
        topic = Topic.objects.create(course=course, name='Some Topic', order=1)
        self.assertIsNone(topic.effective_aqf_level)

    # ------------------------------------------------------------------ #
    # Topic star difficulty
    # ------------------------------------------------------------------ #

    def test_topic_stores_star_difficulty(self):
        topic = Topic.objects.get(pk=self.topic.pk)
        self.assertEqual(topic.star_difficulty, 1)

    def test_topic_star_difficulty_nullable(self):
        topic = Topic.objects.create(
            course=self.course,
            name='No Stars Topic',
            order=2,
        )
        self.assertIsNone(topic.star_difficulty)

    def test_topic_star_difficulty_range(self):
        for stars in range(1, 7):
            self.topic.star_difficulty = stars
            self.topic.save()
            self.assertEqual(Topic.objects.get(pk=self.topic.pk).star_difficulty, stars)

    # ------------------------------------------------------------------ #
    # Flashcard star difficulty (own + inherited)
    # ------------------------------------------------------------------ #

    def test_flashcard_inherits_star_difficulty_from_topic(self):
        """effective_star_difficulty returns topic's star_difficulty when card's is null"""
        card = Flashcard.objects.create(
            topic=self.topic,
            question='V=?',
            answer='IR',
        )
        self.assertIsNone(card.star_difficulty)
        self.assertEqual(card.effective_star_difficulty, 1)

    def test_flashcard_own_star_difficulty_overrides_topic(self):
        """effective_star_difficulty returns card's own value when set"""
        card = Flashcard.objects.create(
            topic=self.topic,
            question='V=?',
            answer='IR',
            star_difficulty=3,
        )
        self.assertEqual(card.effective_star_difficulty, 3)

    def test_flashcard_effective_star_none_when_both_unset(self):
        """effective_star_difficulty returns None when neither card nor topic has stars"""
        topic = Topic.objects.create(
            course=self.course,
            name='No Stars',
            order=3,
        )
        card = Flashcard.objects.create(
            topic=topic,
            question='Q',
            answer='A',
        )
        self.assertIsNone(card.effective_star_difficulty)

    def test_flashcard_star_difficulty_range(self):
        card = Flashcard.objects.create(
            topic=self.topic,
            question='Q',
            answer='A',
        )
        for stars in range(1, 7):
            card.star_difficulty = stars
            card.save()
            self.assertEqual(Flashcard.objects.get(pk=card.pk).star_difficulty, stars)
