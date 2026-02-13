from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course, Topic, Flashcard, Skill
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
