"""Tests for rich media features in flashcards"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from study.models import Course, Topic, Flashcard, CardTemplate
from study.utils.graph_generator import (
    safe_execute_graph_code, 
    generate_graph,
    get_graph_template
)
import matplotlib.pyplot as plt
import numpy as np


class LaTeXSupportTestCase(TestCase):
    """Test LaTeX/Math equation support"""
    
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
    
    def test_create_flashcard_with_latex(self):
        """Test creating flashcard with LaTeX equations"""
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question="What is the quadratic formula? $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$",
            answer="The solution to $ax^2 + bx + c = 0$",
            uses_latex=True
        )
        
        self.assertTrue(flashcard.uses_latex)
        self.assertIn('$x = \\frac{-b', flashcard.question)
    
    def test_latex_field_defaults_to_false(self):
        """Test that uses_latex defaults to False"""
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question="Simple question",
            answer="Simple answer"
        )
        
        self.assertFalse(flashcard.uses_latex)


class GraphGenerationTestCase(TestCase):
    """Test graph generation functionality"""
    
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
    
    def test_safe_execute_simple_graph_code(self):
        """Test executing simple matplotlib code safely"""
        code = """
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
"""
        fig = safe_execute_graph_code(code)
        self.assertIsNotNone(fig)
        plt.close(fig)
    
    def test_safe_execute_rejects_forbidden_keywords(self):
        """Test that forbidden keywords are rejected"""
        forbidden_codes = [
            "import os",
            "exec('print(1)')",
            "eval('2+2')",
            "open('file.txt')",
            "__import__('os')",
        ]
        
        for code in forbidden_codes:
            with self.assertRaises(ValueError):
                safe_execute_graph_code(code)
    
    def test_safe_execute_with_variables(self):
        """Test code execution with variable substitution"""
        code = """
a = {a}
b = {b}
x = np.linspace(-5, 5, 100)
y = a * x + b
plt.plot(x, y)
"""
        variables = {'a': 2, 'b': 3}
        fig = safe_execute_graph_code(code, variables)
        self.assertIsNotNone(fig)
        plt.close(fig)
    
    def test_graph_type_choices(self):
        """Test that graph type choices are available"""
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question="Graph question",
            answer="Graph answer",
            graph_type='function'
        )
        
        self.assertEqual(flashcard.graph_type, 'function')
        
        # Test other graph types
        for graph_type, _ in Flashcard.GRAPH_TYPES:
            flashcard.graph_type = graph_type
            flashcard.save()
            self.assertEqual(flashcard.graph_type, graph_type)
    
    def test_get_graph_template(self):
        """Test getting pre-built graph templates"""
        template = get_graph_template('function')
        self.assertIn('code', template)
        self.assertIn('config', template)
        self.assertIn('x = np.linspace', template['code'])


class DiagramSupportTestCase(TestCase):
    """Test diagram (Mermaid.js) support"""
    
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
    
    def test_create_flashcard_with_diagram(self):
        """Test creating flashcard with Mermaid diagram"""
        diagram_code = """
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[End]
    C --> D
"""
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question="What is the algorithm flow?",
            answer="See diagram",
            diagram_type='flowchart',
            diagram_code=diagram_code
        )
        
        self.assertEqual(flashcard.diagram_type, 'flowchart')
        self.assertIn('flowchart TD', flashcard.diagram_code)
    
    def test_diagram_type_choices(self):
        """Test that diagram type choices are available"""
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question="Diagram question",
            answer="Diagram answer",
            diagram_type='mindmap'
        )
        
        self.assertEqual(flashcard.diagram_type, 'mindmap')


class CodeSnippetTestCase(TestCase):
    """Test code snippet support"""
    
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
    
    def test_create_flashcard_with_code_snippet(self):
        """Test creating flashcard with code snippet"""
        code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question="What does this function do?",
            answer="Calculates factorial",
            code_snippet=code,
            code_language='python'
        )
        
        self.assertEqual(flashcard.code_language, 'python')
        self.assertIn('def factorial', flashcard.code_snippet)
    
    def test_code_language_choices(self):
        """Test that code language choices are available"""
        languages = ['python', 'c', 'cpp', 'matlab', 'vhdl', 'javascript']
        
        for lang in languages:
            flashcard = Flashcard.objects.create(
                topic=self.topic,
                question=f"Code in {lang}",
                answer="Answer",
                code_snippet="print('hello')",
                code_language=lang
            )
            self.assertEqual(flashcard.code_language, lang)


class CardTemplateTestCase(TestCase):
    """Test CardTemplate model"""
    
    def test_create_card_template(self):
        """Test creating a card template"""
        template = CardTemplate.objects.create(
            name='Basic Math Problem',
            description='Simple math problem with LaTeX',
            category='math',
            default_config={
                'uses_latex': True,
                'difficulty': 'easy'
            }
        )
        
        self.assertEqual(template.name, 'Basic Math Problem')
        self.assertEqual(template.category, 'math')
        self.assertTrue(template.default_config['uses_latex'])
    
    def test_flashcard_with_template(self):
        """Test creating flashcard linked to template"""
        user = User.objects.create_user(username='testuser', password='testpass')
        course = Course.objects.create(
            name='Test Course',
            code='TEST101',
            created_by=user
        )
        topic = Topic.objects.create(
            course=course,
            name='Test Topic',
            order=1
        )
        
        template = CardTemplate.objects.create(
            name='Calculus Problem',
            description='Derivative problem',
            category='math',
            default_config={'uses_latex': True}
        )
        
        flashcard = Flashcard.objects.create(
            topic=topic,
            question="Find derivative",
            answer="Answer",
            template=template
        )
        
        self.assertEqual(flashcard.template, template)


class RichMediaIntegrationTestCase(TestCase):
    """Test integration of multiple rich media features"""
    
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
    
    def test_flashcard_with_multiple_media_types(self):
        """Test flashcard with LaTeX, code, and diagram"""
        flashcard = Flashcard.objects.create(
            topic=self.topic,
            question="Implement and explain: $f(x) = x^2$",
            answer="Square function",
            uses_latex=True,
            code_snippet="def f(x):\n    return x**2",
            code_language='python',
            diagram_type='flowchart',
            diagram_code='flowchart LR\n    A[Input x] --> B[Square x]\n    B --> C[Return]'
        )
        
        self.assertTrue(flashcard.uses_latex)
        self.assertEqual(flashcard.code_language, 'python')
        self.assertEqual(flashcard.diagram_type, 'flowchart')
        self.assertIn('def f(x)', flashcard.code_snippet)
        self.assertIn('flowchart LR', flashcard.diagram_code)
