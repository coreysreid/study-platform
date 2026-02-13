"""Management command to create example parameterized flashcards"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from study.models import Course, Topic, Flashcard, Skill


class Command(BaseCommand):
    help = 'Creates example parameterized flashcards for demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            required=True,
            help='Username to create cards for'
        )

    def handle(self, *args, **options):
        username = options['user']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))
            return

        # Get or create the Engineering Mathematics course
        course, created = Course.objects.get_or_create(
            name='Engineering Mathematics',
            created_by=user,
            defaults={
                'code': 'MATH101',
                'description': 'Comprehensive mathematics curriculum from basics to engineering level'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created course: {course.name}'))
        else:
            self.stdout.write(f'  Using existing course: {course.name}')

        # Get the Basic Arithmetic topic
        try:
            topic = Topic.objects.get(course=course, name='Basic Arithmetic & Number Sense')
        except Topic.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Basic Arithmetic topic not found. Run populate_math_curriculum first.'
            ))
            return

        # Get relevant skills
        try:
            basic_arithmetic = Skill.objects.get(name='basic_arithmetic')
            fraction_ops = Skill.objects.get(name='fraction_operations')
        except Skill.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Required skills not found. Run populate_math_curriculum first.'
            ))
            return

        self.stdout.write('\nCreating parameterized flashcards...\n')

        # 1. Simple Addition
        card1 = Flashcard.objects.create(
            topic=topic,
            question='Placeholder for parameterized card',
            answer='Placeholder',
            question_type='parameterized',
            question_template='What is {a} + {b}?',
            answer_template='{c}',
            parameter_spec={
                'variables': {
                    'a': {'type': 'random_int', 'min': 1, 'max': 50},
                    'b': {'type': 'random_int', 'min': 1, 'max': 50},
                    'c': {'type': 'computed', 'formula': 'a + b'}
                }
            },
            hint='Add the two numbers together',
            difficulty='easy'
        )
        card1.skills.add(basic_arithmetic)
        self.stdout.write(self.style.SUCCESS('  ✓ Created: Simple Addition (e.g., "What is 23 + 17?")'))

        # 2. Simple Subtraction
        card2 = Flashcard.objects.create(
            topic=topic,
            question='Placeholder',
            answer='Placeholder',
            question_type='parameterized',
            question_template='What is {a} - {b}?',
            answer_template='{c}',
            parameter_spec={
                'variables': {
                    'a': {'type': 'random_int', 'min': 20, 'max': 100},
                    'b': {'type': 'random_int', 'min': 1, 'max': 19},
                    'c': {'type': 'computed', 'formula': 'a - b'}
                },
                'constraints': ['a > b']
            },
            hint='Subtract the second number from the first',
            difficulty='easy'
        )
        card2.skills.add(basic_arithmetic)
        self.stdout.write(self.style.SUCCESS('  ✓ Created: Simple Subtraction (e.g., "What is 50 - 13?")'))

        # 3. Multiplication
        card3 = Flashcard.objects.create(
            topic=topic,
            question='Placeholder',
            answer='Placeholder',
            question_type='parameterized',
            question_template='What is {a} × {b}?',
            answer_template='{c}',
            parameter_spec={
                'variables': {
                    'a': {'type': 'random_int', 'min': 2, 'max': 12},
                    'b': {'type': 'random_int', 'min': 2, 'max': 12},
                    'c': {'type': 'computed', 'formula': 'a * b'}
                }
            },
            hint='Multiply the two numbers',
            difficulty='easy'
        )
        card3.skills.add(basic_arithmetic)
        self.stdout.write(self.style.SUCCESS('  ✓ Created: Multiplication (e.g., "What is 7 × 9?")'))

        # 4. Division (clean results)
        card4 = Flashcard.objects.create(
            topic=topic,
            question='Placeholder',
            answer='Placeholder',
            question_type='parameterized',
            question_template='What is {a} ÷ {b}?',
            answer_template='{c}',
            parameter_spec={
                'variables': {
                    'b': {'type': 'random_int', 'min': 2, 'max': 10},
                    'c': {'type': 'random_int', 'min': 2, 'max': 12},
                    'a': {'type': 'computed', 'formula': 'b * c'}
                },
                'constraints': ['a % b == 0']
            },
            hint='Divide the first number by the second',
            difficulty='medium'
        )
        card4.skills.add(basic_arithmetic)
        self.stdout.write(self.style.SUCCESS('  ✓ Created: Division (e.g., "What is 72 ÷ 8?")'))

        # 5. Fraction Addition (same denominator)
        card5 = Flashcard.objects.create(
            topic=topic,
            question='Placeholder',
            answer='Placeholder',
            question_type='parameterized',
            question_template='What is {a}/{d} + {b}/{d}?',
            answer_template='{c}/{d}',
            parameter_spec={
                'variables': {
                    'a': {'type': 'random_int', 'min': 1, 'max': 5},
                    'b': {'type': 'random_int', 'min': 1, 'max': 5},
                    'd': {'type': 'random_choice', 'choices': [2, 3, 4, 5, 6, 8, 10, 12]},
                    'c': {'type': 'computed', 'formula': 'a + b'}
                },
                'constraints': ['c < d']
            },
            hint='Add the numerators, keep the denominator the same',
            difficulty='medium'
        )
        card5.skills.add(fraction_ops)
        self.stdout.write(self.style.SUCCESS('  ✓ Created: Fraction Addition (e.g., "What is 2/5 + 1/5?")'))

        # 6. Pythagorean Theorem (special triangles)
        card6 = Flashcard.objects.create(
            topic=topic,
            question='Placeholder',
            answer='Placeholder',
            question_type='parameterized',
            question_template='A right triangle has legs of length {a} and {b}. What is the hypotenuse? (Round to 2 decimal places)',
            answer_template='{c}',
            parameter_spec={
                'variables': {
                    'a': {'type': 'random_int', 'min': 3, 'max': 12},
                    'b': {'type': 'random_int', 'min': 3, 'max': 12},
                    'c': {'type': 'computed', 'formula': 'round(sqrt(a**2 + b**2), 2)'}
                },
                'precision': 2
            },
            hint='Use the Pythagorean theorem: c² = a² + b²',
            difficulty='medium'
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Created: Pythagorean Theorem (e.g., "Triangle with legs 3 and 4")'))

        # 7. Percentage Calculation
        card7 = Flashcard.objects.create(
            topic=topic,
            question='Placeholder',
            answer='Placeholder',
            question_type='parameterized',
            question_template='What is {percent}% of {number}?',
            answer_template='{result}',
            parameter_spec={
                'variables': {
                    'percent': {'type': 'random_choice', 'choices': [10, 20, 25, 50, 75]},
                    'number': {'type': 'random_choice', 'choices': [20, 40, 60, 80, 100, 120, 200]},
                    'result': {'type': 'computed', 'formula': 'round(number * percent / 100, 2)'}
                },
                'precision': 2
            },
            hint='Multiply the number by the percentage and divide by 100',
            difficulty='medium'
        )
        card7.skills.add(basic_arithmetic)
        self.stdout.write(self.style.SUCCESS('  ✓ Created: Percentage Calculation (e.g., "What is 25% of 80?")'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Successfully created 7 example parameterized flashcards for topic "{topic.name}"!'
        ))
        self.stdout.write('\nThese cards will generate new random values each time they are presented.')
        self.stdout.write('To see them in action, start a study session for the Basic Arithmetic topic.')
