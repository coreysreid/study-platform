import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
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
        skill = Skill.objects.create(
            name='basic_arithmetic',
            description='Basic arithmetic operations'
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
        """Test that system user is created when running management commands"""
        from django.core.management import call_command
        
        # System user should not exist initially
        self.assertFalse(User.objects.filter(username='system').exists())
        
        # Run the command
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
        
        # Regular user should see both their own course and public course
        course_names = list(courses.values_list('name', flat=True))
        self.assertIn('Engineering Mathematics', course_names)
        self.assertIn('Personal Course', course_names)
        self.assertEqual(courses.count(), 2)
    
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
        FlashcardProgress.objects.create(user=self.user, flashcard=self.card, step_index=0)
        FlashcardProgress.objects.create(user=self.user, flashcard=self.card, step_index=1)
        count = FlashcardProgress.objects.filter(user=self.user, flashcard=self.card).count()
        self.assertEqual(count, 2)

    def test_topic_score_creation(self):
        ts = TopicScore.objects.create(user=self.user, topic=self.topic, score=0.75, attempt_count=10)
        self.assertEqual(ts.score, 0.75)
