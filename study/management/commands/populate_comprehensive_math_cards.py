"""
Management command to create comprehensive flashcard content for all math topics.

This command creates a substantial set of flashcards across all 13 topics in the
Engineering Mathematics curriculum, ensuring users can complete math courses
right off installation.

Usage:
    python manage.py populate_comprehensive_math_cards --user=<username>
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from study.models import Course, Topic, Flashcard, Skill


class Command(BaseCommand):
    help = 'Populates comprehensive flashcard content for Engineering Mathematics curriculum'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Username of the user who will own the content (default: system)',
            default='system',
            required=False,
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Skip if flashcards already exist for topics',
        )

    def handle(self, *args, **options):
        username = options.get('user', 'system')
        skip_existing = options.get('skip_existing', False)

        # Only auto-create the special "system" user; require other users to pre-exist
        if username == 'system':
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'is_staff': False,
                    'is_active': True,
                    'email': f'{username}@system.local',
                    'first_name': 'System',
                    'last_name': 'Content'
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created system user: {username}')
                )
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(
                    f'User "{username}" does not exist. Please create this user before running this command.'
                )

        # Get the Engineering Mathematics course
        try:
            course = Course.objects.get(name='Engineering Mathematics', created_by=user)
        except Course.DoesNotExist:
            raise CommandError(
                'Engineering Mathematics course not found. '
                'Run populate_math_curriculum first.'
            )

        self.stdout.write('\nCreating comprehensive flashcard content...\n')
        
        total_created = 0
        
        # Get all topics
        topics = course.topics.all().order_by('order')
        
        for topic in topics:
            existing_count = topic.flashcards.count()
            
            if skip_existing and existing_count > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f'Skipping {topic.name} - already has {existing_count} flashcards'
                    )
                )
                continue
            
            self.stdout.write(f'\n📚 Creating flashcards for: {topic.name}')
            
            # Create flashcards based on topic
            created = 0
            
            if topic.name == 'Basic Arithmetic & Number Sense':
                created = self.create_basic_arithmetic_cards(topic)
            elif topic.name == 'Algebra Fundamentals':
                created = self.create_algebra_fundamentals_cards(topic)
            elif topic.name == 'Geometry':
                created = self.create_geometry_cards(topic)
            elif topic.name == 'Trigonometry Fundamentals':
                created = self.create_trigonometry_cards(topic)
            elif topic.name == 'Pre-Calculus':
                created = self.create_precalculus_cards(topic)
            elif topic.name == 'Differential Calculus':
                created = self.create_differential_calculus_cards(topic)
            elif topic.name == 'Integral Calculus':
                created = self.create_integral_calculus_cards(topic)
            elif topic.name == 'Multivariable Calculus':
                created = self.create_multivariable_calculus_cards(topic)
            elif topic.name == 'Linear Algebra':
                created = self.create_linear_algebra_cards(topic)
            elif topic.name == 'Ordinary Differential Equations (ODEs)':
                created = self.create_odes_cards(topic)
            elif topic.name == 'Partial Differential Equations (PDEs)':
                created = self.create_pdes_cards(topic)
            elif topic.name == 'Fourier Analysis':
                created = self.create_fourier_analysis_cards(topic)
            elif topic.name == 'Laplace Transforms':
                created = self.create_laplace_transforms_cards(topic)
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'  ⚠️ No flashcard generator found for topic "{topic.name}". '
                        'No flashcards were created for this topic.'
                    )
                )
            
            total_created += created
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created} flashcards'))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully created {total_created} total flashcards across all topics!'
            )
        )

    def create_basic_arithmetic_cards(self, topic):
        """Create flashcards for Basic Arithmetic & Number Sense"""
        skills = {
            'basic_arithmetic': Skill.objects.get(name='basic_arithmetic'),
            'fraction_operations': Skill.objects.get(name='fraction_operations'),
            'decimal_operations': Skill.objects.get(name='decimal_operations'),
            'order_of_operations': Skill.objects.get(name='order_of_operations'),
        }
        
        cards = [
            # Easy difficulty cards (5 cards)
            {
                'question': 'What is the order of operations (PEMDAS/BODMAS)?',
                'answer': 'Parentheses/Brackets, Exponents/Orders, Multiplication and Division (left to right), Addition and Subtraction (left to right)',
                'difficulty': 'easy',
                'hint': 'Remember: Please Excuse My Dear Aunt Sally',
                'skills': ['order_of_operations'],
            },
            {
                'question': 'What is a prime number?',
                'answer': 'A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.',
                'difficulty': 'easy',
                'hint': 'Think about numbers that can only be divided by 1 and themselves',
                'skills': ['basic_arithmetic'],
            },
            {
                'question': 'What is the absolute value of a number?',
                'answer': 'The absolute value is the distance of a number from zero, always non-negative. For example, |−5| = 5 and |5| = 5.',
                'difficulty': 'easy',
                'hint': 'Think of distance from zero on a number line',
                'skills': ['basic_arithmetic'],
            },
            {
                'question': 'What is the difference between an even and odd number?',
                'answer': 'Even numbers are divisible by 2 (e.g., 2, 4, 6), while odd numbers leave a remainder of 1 when divided by 2 (e.g., 1, 3, 5).',
                'difficulty': 'easy',
                'skills': ['basic_arithmetic'],
            },
            {
                'question_type': 'parameterized',
                'question_template': 'Convert {decimal} to a percentage.',
                'answer_template': '{percent}%',
                'parameter_spec': {
                    'variables': {
                        'decimal': {'type': 'random_choice', 'choices': [0.25, 0.5, 0.75, 0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]},
                        'percent': {'type': 'computed', 'formula': 'decimal * 100'},
                    }
                },
                'difficulty': 'easy',
                'hint': 'Multiply by 100',
                'skills': ['decimal_operations'],
            },
            # Medium difficulty cards (7 cards)
            {
                'question': 'List the first 10 prime numbers.',
                'answer': '2, 3, 5, 7, 11, 13, 17, 19, 23, 29',
                'difficulty': 'medium',
                'hint': 'Start with 2, the only even prime number',
                'skills': ['basic_arithmetic'],
            },
            {
                'question': 'What is the Greatest Common Divisor (GCD)?',
                'answer': 'The GCD is the largest positive integer that divides two or more numbers without a remainder. For example, GCD(12, 18) = 6.',
                'difficulty': 'medium',
                'hint': 'Think of the largest number that divides both numbers evenly',
                'skills': ['basic_arithmetic'],
            },
            {
                'question': 'What is the Least Common Multiple (LCM)?',
                'answer': 'The LCM is the smallest positive integer that is divisible by two or more numbers. For example, LCM(4, 6) = 12.',
                'difficulty': 'medium',
                'hint': 'Think of the smallest number that both numbers divide into',
                'skills': ['basic_arithmetic'],
            },
            {
                'question': 'How do you add fractions with different denominators?',
                'answer': 'Find a common denominator (usually the LCM), convert both fractions, then add the numerators. Example: 1/3 + 1/4 = 4/12 + 3/12 = 7/12',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'You need a common denominator first',
                'skills': ['fraction_operations'],
            },
            {
                'question': 'What is scientific notation?',
                'answer': 'A way of expressing numbers as a product of a number between 1 and 10 and a power of 10. Example: 3,000 = 3 × 10³',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['basic_arithmetic'],
            },
            {
                'question_type': 'parameterized',
                'question_template': 'Simplify the fraction: {numerator}/{denominator}',
                'answer_template': '{simplified_num}/{simplified_den}',
                'parameter_spec': {
                    'variables': {
                        'gcd': {'type': 'random_choice', 'choices': [2, 3, 4, 5, 6]},
                        'simplified_num': {'type': 'random_int', 'min': 1, 'max': 10},
                        'simplified_den': {'type': 'computed', 'formula': 'simplified_num + 1'},
                        'numerator': {'type': 'computed', 'formula': 'gcd * simplified_num'},
                        'denominator': {'type': 'computed', 'formula': 'gcd * simplified_den'},
                    }
                },
                'difficulty': 'medium',
                'hint': 'Find the greatest common divisor (GCD)',
                'skills': ['fraction_operations'],
            },
            {
                'question_type': 'parameterized',
                'question_template': 'Calculate: ({a} + {b}) × {c}',
                'answer_template': '{result}',
                'parameter_spec': {
                    'variables': {
                        'a': {'type': 'random_int', 'min': 1, 'max': 10},
                        'b': {'type': 'random_int', 'min': 1, 'max': 10},
                        'c': {'type': 'random_int', 'min': 2, 'max': 5},
                        'result': {'type': 'computed', 'formula': '(a + b) * c'},
                    }
                },
                'difficulty': 'medium',
                'hint': 'Remember order of operations: parentheses first',
                'skills': ['order_of_operations'],
            },
            # Hard difficulty cards (3 cards)
            {
                'question': 'Convert the decimal 0.625 to a fraction in simplest form.',
                'answer': '5/8. Process: 0.625 = 625/1000, then simplify by dividing both by 125.',
                'difficulty': 'hard',
                'hint': 'Count decimal places to determine denominator, then simplify',
                'skills': ['fraction_operations', 'decimal_operations'],
            },
            {
                'question': 'Calculate 15% of 240.',
                'answer': '36. Process: 240 × 0.15 = 36',
                'difficulty': 'hard',
                'hint': 'Convert percentage to decimal, then multiply',
                'skills': ['decimal_operations', 'basic_arithmetic'],
            },
            {
                'question_type': 'parameterized',
                'question_template': 'What is {percent}% of {number}?',
                'answer_template': '{result}',
                'parameter_spec': {
                    'variables': {
                        'percent': {'type': 'random_choice', 'choices': [10, 15, 20, 25, 30, 40, 50]},
                        'number': {'type': 'random_int', 'min': 50, 'max': 200},
                        'result': {'type': 'computed', 'formula': 'round((percent / 100) * number, 2)'},
                    }
                },
                'difficulty': 'hard',
                'hint': 'Convert percent to decimal and multiply',
                'skills': ['decimal_operations', 'basic_arithmetic'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_algebra_fundamentals_cards(self, topic):
        """Create flashcards for Algebra Fundamentals"""
        skills = {
            'algebraic_manipulation': Skill.objects.get(name='algebraic_manipulation'),
            'equation_solving': Skill.objects.get(name='equation_solving'),
            'exponent_rules': Skill.objects.get(name='exponent_rules'),
            'factoring': Skill.objects.get(name='factoring'),
            'quadratic_equations': Skill.objects.get(name='quadratic_equations'),
        }
        
        cards = [
            # Easy difficulty cards (5 cards)
            {
                'question': 'What are the exponent rules for multiplication?',
                'answer': 'x^a × x^b = x^(a+b). When multiplying powers with the same base, add the exponents.',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['exponent_rules'],
            },
            {
                'question': 'What are the exponent rules for division?',
                'answer': 'x^a ÷ x^b = x^(a-b). When dividing powers with the same base, subtract the exponents.',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['exponent_rules'],
            },
            {
                'question': 'What is the difference of squares formula?',
                'answer': 'a² - b² = (a + b)(a - b)',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['factoring'],
            },
            {
                'question': 'What is the power of a power rule?',
                'answer': '(x^a)^b = x^(ab). Multiply the exponents when raising a power to a power.',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['exponent_rules'],
            },
            {
                'question_type': 'parameterized',
                'question_template': 'Solve for x: {a}x + {b} = {c}',
                'answer_template': 'x = {solution}',
                'parameter_spec': {
                    'variables': {
                        'a': {'type': 'random_int', 'min': 2, 'max': 10},
                        'b': {'type': 'random_int', 'min': 1, 'max': 20},
                        'c': {'type': 'random_int', 'min': 10, 'max': 50},
                        'solution': {'type': 'computed', 'formula': 'round((c - b) / a, 2)'},
                    }
                },
                'difficulty': 'easy',
                'hint': 'Isolate x by subtracting b from both sides, then dividing by a',
                'skills': ['equation_solving'],
            },
            # Medium difficulty cards (7 cards)
            {
                'question': 'What is the quadratic formula?',
                'answer': 'x = (-b ± √(b² - 4ac)) / (2a) for equation ax² + bx + c = 0',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Used to solve equations of the form ax² + bx + c = 0',
                'skills': ['quadratic_equations'],
            },
            {
                'question': 'Expand: (x + 3)(x + 5)',
                'answer': 'x² + 8x + 15. Use FOIL: First (x·x), Outer (x·5), Inner (3·x), Last (3·5)',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Use the FOIL method or distributive property',
                'skills': ['algebraic_manipulation'],
            },
            {
                'question': 'What is the discriminant of a quadratic equation and what does it tell us?',
                'answer': 'The discriminant is b² - 4ac. If > 0: two real roots; if = 0: one real root; if < 0: two complex roots.',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': "It's the expression under the square root in the quadratic formula",
                'skills': ['quadratic_equations'],
            },
            {
                'question': 'Solve the inequality: 2x + 5 > 13',
                'answer': 'x > 4. Subtract 5 from both sides: 2x > 8, then divide by 2: x > 4',
                'difficulty': 'medium',
                'hint': 'Treat it like an equation, but keep the inequality sign',
                'skills': ['equation_solving'],
            },
            {
                'question': 'What is an absolute value equation?',
                'answer': 'An equation containing absolute value expressions like |x| = 5, which has solutions x = 5 and x = -5.',
                'difficulty': 'medium',
                'hint': 'Absolute value represents distance from zero',
                'skills': ['equation_solving'],
            },
            {
                'question_type': 'parameterized',
                'question_template': 'Factor: x² + {b}x + {c}',
                'answer_template': '(x + {p})(x + {q})',
                'parameter_spec': {
                    'variables': {
                        'p': {'type': 'random_int', 'min': 1, 'max': 6},
                        'q': {'type': 'random_int', 'min': 1, 'max': 6},
                        'b': {'type': 'computed', 'formula': 'p + q'},
                        'c': {'type': 'computed', 'formula': 'p * q'},
                    }
                },
                'difficulty': 'medium',
                'hint': 'Find two numbers that multiply to c and add to b',
                'skills': ['factoring'],
            },
            {
                'question_type': 'parameterized',
                'question_template': 'Simplify: x^{a} × x^{b}',
                'answer_template': 'x^{sum}',
                'parameter_spec': {
                    'variables': {
                        'a': {'type': 'random_int', 'min': 2, 'max': 8},
                        'b': {'type': 'random_int', 'min': 2, 'max': 8},
                        'sum': {'type': 'computed', 'formula': 'a + b'},
                    }
                },
                'difficulty': 'medium',
                'hint': 'Add the exponents when multiplying with same base',
                'skills': ['exponent_rules'],
                'uses_latex': True,
            },
            # Hard difficulty cards (3 cards)
            {
                'question': 'Solve the system of equations: 2x + y = 7 and x - y = 2',
                'answer': 'x = 3, y = 1. Add equations to eliminate y: 3x = 9, so x = 3. Substitute back: 3 - y = 2, so y = 1.',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Try the elimination method by adding the equations',
                'skills': ['equation_solving'],
            },
            {
                'question': 'Factor completely: x³ - 8',
                'answer': '(x - 2)(x² + 2x + 4). This is a difference of cubes: a³ - b³ = (a - b)(a² + ab + b²)',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Recognize this as a difference of cubes where a = x and b = 2',
                'skills': ['factoring'],
            },
            {
                'question': 'Simplify the rational expression: (x² - 4)/(x² - 3x + 2)',
                'answer': '(x + 2)/(x - 1). Factor numerator: (x+2)(x-2), factor denominator: (x-1)(x-2), cancel (x-2)',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Factor both numerator and denominator, then cancel common factors',
                'skills': ['factoring', 'algebraic_manipulation'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_geometry_cards(self, topic):
        """Create flashcards for Geometry"""
        skills = {
            'geometric_reasoning': Skill.objects.get(name='geometric_reasoning'),
            'pythagorean_theorem': Skill.objects.get(name='pythagorean_theorem'),
            'area_volume_calculations': Skill.objects.get(name='area_volume_calculations'),
        }
        
        cards = [
            # Easy difficulty cards (4 cards)
            {
                'question': 'State the Pythagorean theorem.',
                'answer': 'In a right triangle, a² + b² = c², where c is the hypotenuse and a, b are the other two sides.',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['pythagorean_theorem'],
            },
            {
                'question': 'What is the formula for the area of a circle?',
                'answer': 'A = πr², where r is the radius',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['area_volume_calculations'],
            },
            {
                'question': 'What is the sum of interior angles in a triangle?',
                'answer': '180 degrees',
                'difficulty': 'easy',
                'skills': ['geometric_reasoning'],
            },
            {
                'question_type': 'parameterized',
                'question_template': 'Find the area of a rectangle with length {length} and width {width}.',
                'answer_template': '{area} square units',
                'parameter_spec': {
                    'variables': {
                        'length': {'type': 'random_int', 'min': 5, 'max': 20},
                        'width': {'type': 'random_int', 'min': 3, 'max': 15},
                        'area': {'type': 'computed', 'formula': 'length * width'},
                    }
                },
                'difficulty': 'easy',
                'hint': 'Area = length × width',
                'skills': ['area_volume_calculations'],
            },
            # Medium difficulty cards (6 cards)
            {
                'question': 'What is the formula for the volume of a sphere?',
                'answer': 'V = (4/3)πr³, where r is the radius',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['area_volume_calculations'],
            },
            {
                'question': 'What is the formula for the circumference of a circle?',
                'answer': 'C = 2πr or C = πd, where r is the radius and d is the diameter',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['area_volume_calculations'],
            },
            {
                'question': 'What is the formula for the volume of a cylinder?',
                'answer': 'V = πr²h, where r is the radius and h is the height',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Think of it as the area of the base times the height',
                'skills': ['area_volume_calculations'],
            },
            {
                'question': 'What are the properties of an equilateral triangle?',
                'answer': 'All three sides are equal, all three angles are 60°, it has three lines of symmetry',
                'difficulty': 'medium',
                'skills': ['geometric_reasoning'],
            },
            {
                'question': 'When two parallel lines are cut by a transversal, what angles are equal?',
                'answer': 'Corresponding angles are equal, alternate interior angles are equal, alternate exterior angles are equal',
                'difficulty': 'medium',
                'hint': 'Think about the patterns formed by parallel lines and a transversal',
                'skills': ['geometric_reasoning'],
            },
            {
                'question': 'What is the distance formula between two points (x₁, y₁) and (x₂, y₂)?',
                'answer': 'd = √[(x₂ - x₁)² + (y₂ - y₁)²]',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': "It's derived from the Pythagorean theorem",
                'skills': ['pythagorean_theorem'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': 'What is the formula for the volume of a cone?',
                'answer': 'V = (1/3)πr²h, where r is the radius and h is the height',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': "It's one-third the volume of a cylinder with the same base and height",
                'skills': ['area_volume_calculations'],
            },
            {
                'question_type': 'parameterized',
                'question_template': 'Find the hypotenuse of a right triangle with legs {a} and {b}.',
                'answer_template': '{hypotenuse}',
                'parameter_spec': {
                    'variables': {
                        'index': {'type': 'random_choice', 'choices': [0, 1, 2, 3, 4, 5]},
                        'a': {'type': 'computed', 'formula': '[3, 5, 6, 8, 9, 12][index]'},
                        'b': {'type': 'computed', 'formula': '[4, 12, 8, 15, 12, 16][index]'},
                        'hypotenuse': {'type': 'computed', 'formula': 'round((a**2 + b**2)**0.5, 2)'},
                    }
                },
                'difficulty': 'hard',
                'hint': 'Use the Pythagorean theorem: a² + b² = c²',
                'skills': ['pythagorean_theorem'],
                'uses_latex': True,
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_trigonometry_cards(self, topic):
        """Create flashcards for Trigonometry Fundamentals"""
        skills = {
            'trigonometric_ratios': Skill.objects.get(name='trigonometric_ratios'),
            'trigonometric_identities': Skill.objects.get(name='trigonometric_identities'),
        }
        
        cards = [
            # Easy difficulty cards (5 cards)
            {
                'question': 'Define sin(θ) in a right triangle.',
                'answer': 'sin(θ) = opposite / hypotenuse',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['trigonometric_ratios'],
            },
            {
                'question': 'Define cos(θ) in a right triangle.',
                'answer': 'cos(θ) = adjacent / hypotenuse',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['trigonometric_ratios'],
            },
            {
                'question': 'Define tan(θ) in a right triangle.',
                'answer': 'tan(θ) = opposite / adjacent = sin(θ) / cos(θ)',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['trigonometric_ratios'],
            },
            {
                'question': 'What is sin(30°)?',
                'answer': '1/2 or 0.5',
                'difficulty': 'easy',
                'hint': 'Remember special angles: 30°, 45°, 60°',
                'skills': ['trigonometric_ratios'],
            },
            {
                'question': 'What is cos(60°)?',
                'answer': '1/2 or 0.5',
                'difficulty': 'easy',
                'hint': 'Remember special angles: 30°, 45°, 60°',
                'skills': ['trigonometric_ratios'],
            },
            # Medium difficulty cards (5 cards)
            {
                'question': 'What is the Pythagorean identity for trigonometry?',
                'answer': 'sin²(θ) + cos²(θ) = 1',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['trigonometric_identities'],
            },
            {
                'question': 'What are the reciprocal trigonometric functions?',
                'answer': 'csc(θ) = 1/sin(θ), sec(θ) = 1/cos(θ), cot(θ) = 1/tan(θ)',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Cosecant, secant, and cotangent',
                'skills': ['trigonometric_ratios'],
            },
            {
                'question': 'What is sin(45°)?',
                'answer': '√2/2 ≈ 0.707',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'This is the same as cos(45°)',
                'skills': ['trigonometric_ratios'],
            },
            {
                'question': 'How do you convert degrees to radians?',
                'answer': 'Multiply by π/180. For example, 180° = π radians, 90° = π/2 radians',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Think about how many degrees are in a full circle (360°) vs radians (2π)',
                'skills': ['trigonometric_ratios'],
            },
            {
                'question': 'What is the double angle formula for sin(2θ)?',
                'answer': 'sin(2θ) = 2sin(θ)cos(θ)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['trigonometric_identities'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': 'What is the Law of Sines?',
                'answer': 'a/sin(A) = b/sin(B) = c/sin(C), where a, b, c are sides and A, B, C are opposite angles',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Used for solving non-right triangles',
                'skills': ['trigonometric_ratios'],
            },
            {
                'question': 'What is the Law of Cosines?',
                'answer': 'c² = a² + b² - 2ab·cos(C), where c is a side and C is the opposite angle',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Generalizes the Pythagorean theorem to any triangle',
                'skills': ['trigonometric_ratios'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_precalculus_cards(self, topic):
        """Create flashcards for Pre-Calculus"""
        skills = {
            'function_analysis': Skill.objects.get(name='function_analysis'),
            'exponential_logarithmic': Skill.objects.get(name='exponential_logarithmic'),
            'limit_concepts': Skill.objects.get(name='limit_concepts'),
        }
        
        cards = [
            # Easy difficulty cards (4 cards)
            {
                'question': 'What is the definition of a function?',
                'answer': 'A function is a relation where each input (x) has exactly one output (y).',
                'difficulty': 'easy',
                'skills': ['function_analysis'],
            },
            {
                'question': "What is e (Euler's number) approximately equal to?",
                'answer': 'Approximately 2.71828',
                'difficulty': 'easy',
                'skills': ['exponential_logarithmic'],
            },
            {
                'question': 'What is the domain of a function?',
                'answer': 'The domain is the set of all possible input values (x-values) for which the function is defined.',
                'difficulty': 'easy',
                'skills': ['function_analysis'],
            },
            {
                'question': 'What is the range of a function?',
                'answer': 'The range is the set of all possible output values (y-values) that the function can produce.',
                'difficulty': 'easy',
                'skills': ['function_analysis'],
            },
            # Medium difficulty cards (6 cards)
            {
                'question': 'What is the logarithm rule: log(ab)?',
                'answer': 'log(ab) = log(a) + log(b)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['exponential_logarithmic'],
            },
            {
                'question': 'What is the logarithm rule: log(a/b)?',
                'answer': 'log(a/b) = log(a) - log(b)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['exponential_logarithmic'],
            },
            {
                'question': 'What is the informal definition of a limit?',
                'answer': 'The limit of f(x) as x approaches a is L if f(x) gets arbitrarily close to L as x gets close to a.',
                'difficulty': 'medium',
                'skills': ['limit_concepts'],
            },
            {
                'question': 'What is the logarithm rule: log(a^n)?',
                'answer': 'log(a^n) = n·log(a)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['exponential_logarithmic'],
            },
            {
                'question': 'What is a composite function?',
                'answer': 'A composite function (f ∘ g)(x) = f(g(x)) means you apply g first, then apply f to the result.',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Think of it as a function of a function',
                'skills': ['function_analysis'],
            },
            {
                'question': 'How do you find the inverse of a function f(x)?',
                'answer': 'Swap x and y, then solve for y. The result is f⁻¹(x). The function must be one-to-one.',
                'difficulty': 'medium',
                'hint': 'Inverse functions "undo" each other',
                'skills': ['function_analysis'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': 'What is exponential growth formula?',
                'answer': 'A(t) = A₀e^(kt), where A₀ is initial amount, k is growth rate, and t is time',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Used in population growth, compound interest, etc.',
                'skills': ['exponential_logarithmic'],
            },
            {
                'question': 'What transformation does f(x-h) + k represent?',
                'answer': 'Horizontal shift right by h units and vertical shift up by k units',
                'difficulty': 'hard',
                'hint': 'Remember: horizontal shifts are opposite to what you might expect',
                'skills': ['function_analysis'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_differential_calculus_cards(self, topic):
        """Create flashcards for Differential Calculus"""
        skills = {
            'derivative_calculation': Skill.objects.get(name='derivative_calculation'),
            'differentiation_rules': Skill.objects.get(name='differentiation_rules'),
        }
        
        cards = [
            # Easy difficulty cards (4 cards)
            {
                'question': 'What is the power rule for derivatives?',
                'answer': 'd/dx(x^n) = nx^(n-1)',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['differentiation_rules'],
            },
            {
                'question': 'What is the derivative of sin(x)?',
                'answer': 'cos(x)',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['differentiation_rules'],
            },
            {
                'question': 'What is the derivative of cos(x)?',
                'answer': '-sin(x)',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['differentiation_rules'],
            },
            {
                'question': 'What is the derivative of e^x?',
                'answer': 'e^x (the derivative of e^x is itself)',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['differentiation_rules'],
            },
            # Medium difficulty cards (6 cards)
            {
                'question': 'What is the definition of a derivative?',
                'answer': 'f\'(x) = lim(h→0) [f(x+h) - f(x)] / h',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['derivative_calculation'],
            },
            {
                'question': 'What is the product rule for derivatives?',
                'answer': 'd/dx[f(x)g(x)] = f\'(x)g(x) + f(x)g\'(x)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['differentiation_rules'],
            },
            {
                'question': 'What is the chain rule for derivatives?',
                'answer': 'd/dx[f(g(x))] = f\'(g(x)) · g\'(x)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['differentiation_rules'],
            },
            {
                'question': 'What is the quotient rule for derivatives?',
                'answer': 'd/dx[f(x)/g(x)] = [f\'(x)g(x) - f(x)g\'(x)] / [g(x)]²',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Low d-high minus high d-low, square the bottom and away we go',
                'skills': ['differentiation_rules'],
            },
            {
                'question': 'What is the derivative of ln(x)?',
                'answer': '1/x',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['differentiation_rules'],
            },
            {
                'question': 'What is implicit differentiation?',
                'answer': 'A technique to find dy/dx when y is not explicitly solved for, by differentiating both sides with respect to x',
                'difficulty': 'medium',
                'hint': 'Useful for equations like x² + y² = 1',
                'skills': ['differentiation_rules'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': 'What is a critical point and how do you find it?',
                'answer': 'A point where f\'(x) = 0 or f\'(x) is undefined. Find by setting the derivative equal to zero and solving.',
                'difficulty': 'hard',
                'hint': 'These points are candidates for local maxima and minima',
                'skills': ['derivative_calculation'],
            },
            {
                'question': "What is L'Hôpital's Rule?",
                'answer': 'If lim f(x)/g(x) gives 0/0 or ∞/∞, then lim f(x)/g(x) = lim f\'(x)/g\'(x)',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Used to evaluate indeterminate forms by taking derivatives',
                'skills': ['derivative_calculation'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_integral_calculus_cards(self, topic):
        """Create flashcards for Integral Calculus"""
        skills = {
            'integration_techniques': Skill.objects.get(name='integration_techniques'),
            'definite_integrals': Skill.objects.get(name='definite_integrals'),
        }
        
        cards = [
            # Easy difficulty cards (4 cards)
            {
                'question': 'What is the power rule for integration?',
                'answer': '∫x^n dx = x^(n+1)/(n+1) + C, where n ≠ -1',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['integration_techniques'],
            },
            {
                'question': 'What is ∫sin(x)dx?',
                'answer': '-cos(x) + C',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['integration_techniques'],
            },
            {
                'question': 'What is ∫cos(x)dx?',
                'answer': 'sin(x) + C',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['integration_techniques'],
            },
            {
                'question': 'What is ∫e^x dx?',
                'answer': 'e^x + C',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['integration_techniques'],
            },
            # Medium difficulty cards (6 cards)
            {
                'question': 'State the Fundamental Theorem of Calculus (Part 1).',
                'answer': 'If F\'(x) = f(x), then ∫[a to b] f(x)dx = F(b) - F(a)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['definite_integrals'],
            },
            {
                'question': 'What is ∫(1/x)dx?',
                'answer': 'ln|x| + C',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['integration_techniques'],
            },
            {
                'question': 'What is u-substitution in integration?',
                'answer': 'A technique where you substitute u = g(x), du = g\'(x)dx to simplify the integral',
                'difficulty': 'medium',
                'hint': 'The reverse of the chain rule',
                'skills': ['integration_techniques'],
            },
            {
                'question': 'What is integration by parts formula?',
                'answer': '∫u dv = uv - ∫v du',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'The reverse of the product rule',
                'skills': ['integration_techniques'],
            },
            {
                'question': 'How do you find the area between two curves f(x) and g(x) from a to b?',
                'answer': 'A = ∫[a to b] |f(x) - g(x)|dx, or ∫[a to b] [upper function - lower function]dx',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Integrate the difference between the upper and lower functions',
                'skills': ['definite_integrals'],
            },
            {
                'question': 'What is the disk method for volume of revolution?',
                'answer': 'V = π∫[a to b] [f(x)]² dx, used when rotating around the x-axis',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Think of stacking circular disks',
                'skills': ['definite_integrals'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': 'What is the average value of a function f(x) on [a, b]?',
                'answer': 'f_avg = (1/(b-a))∫[a to b] f(x)dx',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': "It's the definite integral divided by the interval length",
                'skills': ['definite_integrals'],
            },
            {
                'question': 'What is the shell method for volume of revolution?',
                'answer': 'V = 2π∫[a to b] x·f(x)dx, used when rotating around the y-axis',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Think of cylindrical shells with radius x and height f(x)',
                'skills': ['definite_integrals'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_multivariable_calculus_cards(self, topic):
        """Create flashcards for Multivariable Calculus"""
        skills = {
            'partial_derivatives': Skill.objects.get(name='partial_derivatives'),
            'multiple_integrals': Skill.objects.get(name='multiple_integrals'),
        }
        
        cards = [
            # Easy difficulty cards (3 cards)
            {
                'question': 'How do you compute ∂f/∂x for f(x,y)?',
                'answer': 'Take the derivative of f with respect to x, treating y as a constant.',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['partial_derivatives'],
            },
            {
                'question': 'What is a level curve?',
                'answer': 'A curve in the xy-plane where a function f(x,y) has a constant value c, represented by f(x,y) = c',
                'difficulty': 'easy',
                'skills': ['partial_derivatives'],
            },
            {
                'question': 'What is the notation for a double integral over region R?',
                'answer': '∬_R f(x,y) dA or ∫∫_R f(x,y) dx dy',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['multiple_integrals'],
            },
            # Medium difficulty cards (5 cards)
            {
                'question': 'What is a partial derivative?',
                'answer': 'The derivative of a multivariable function with respect to one variable, treating all other variables as constants.',
                'difficulty': 'medium',
                'skills': ['partial_derivatives'],
            },
            {
                'question': 'What is a double integral used for?',
                'answer': 'Computing volumes under surfaces, areas of regions, or mass of 2D objects with varying density.',
                'difficulty': 'medium',
                'skills': ['multiple_integrals'],
            },
            {
                'question': 'What is the gradient vector ∇f?',
                'answer': '∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z), a vector pointing in the direction of steepest increase',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'It contains all the partial derivatives',
                'skills': ['partial_derivatives'],
            },
            {
                'question': 'What is a directional derivative?',
                'answer': 'The rate of change of f in the direction of a unit vector u, given by D_u f = ∇f · u',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': "It's the dot product of the gradient and the direction vector",
                'skills': ['partial_derivatives'],
            },
            {
                'question': 'What is the chain rule for multivariable functions?',
                'answer': 'If z = f(x,y) where x = x(t) and y = y(t), then dz/dt = (∂f/∂x)(dx/dt) + (∂f/∂y)(dy/dt)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['partial_derivatives'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': 'What is a triple integral used for?',
                'answer': 'Computing volumes in 3D space, mass of 3D objects, or other 3D accumulations: ∭_V f(x,y,z) dV',
                'difficulty': 'hard',
                'uses_latex': True,
                'skills': ['multiple_integrals'],
            },
            {
                'question': 'What is the divergence of a vector field F = (P, Q, R)?',
                'answer': 'div F = ∇·F = ∂P/∂x + ∂Q/∂y + ∂R/∂z, a measure of how much the field spreads out',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': "It's the dot product of del and the vector field",
                'skills': ['partial_derivatives'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_linear_algebra_cards(self, topic):
        """Create flashcards for Linear Algebra"""
        skills = {
            'matrix_operations': Skill.objects.get(name='matrix_operations'),
            'determinants': Skill.objects.get(name='determinants'),
            'eigenvalue_problems': Skill.objects.get(name='eigenvalue_problems'),
        }
        
        cards = [
            # Easy difficulty cards (4 cards)
            {
                'question': 'What is the determinant of a 2×2 matrix [[a,b],[c,d]]?',
                'answer': 'ad - bc',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['determinants'],
            },
            {
                'question': 'What is the identity matrix?',
                'answer': 'A square matrix with 1s on the main diagonal and 0s elsewhere. Denoted as I.',
                'difficulty': 'easy',
                'skills': ['matrix_operations'],
            },
            {
                'question': 'What is a zero matrix?',
                'answer': 'A matrix where all elements are zero, denoted as O or 0',
                'difficulty': 'easy',
                'skills': ['matrix_operations'],
            },
            {
                'question': 'What is the transpose of a matrix?',
                'answer': 'The transpose A^T is formed by swapping rows and columns: (A^T)_ij = A_ji',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['matrix_operations'],
            },
            # Medium difficulty cards (6 cards)
            {
                'question': 'What is an eigenvalue?',
                'answer': 'A scalar λ such that Av = λv for some non-zero vector v, where A is a square matrix.',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['eigenvalue_problems'],
            },
            {
                'question': 'What is matrix multiplication rule?',
                'answer': 'For matrices A(m×n) and B(n×p), the product AB is m×p, where (AB)ij = Σ(Aik × Bkj)',
                'difficulty': 'medium',
                'skills': ['matrix_operations'],
            },
            {
                'question': 'What is the dot product of vectors u = (u1, u2) and v = (v1, v2)?',
                'answer': 'u·v = u1v1 + u2v2, a scalar value',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['matrix_operations'],
            },
            {
                'question': 'What does it mean for a matrix to be invertible?',
                'answer': 'A square matrix A is invertible if there exists a matrix A⁻¹ such that AA⁻¹ = A⁻¹A = I',
                'difficulty': 'medium',
                'hint': 'The determinant must be non-zero',
                'skills': ['determinants'],
            },
            {
                'question': 'What is a linear transformation?',
                'answer': 'A function T: V → W that preserves vector addition and scalar multiplication: T(u+v) = T(u)+T(v) and T(cv) = cT(v)',
                'difficulty': 'medium',
                'skills': ['matrix_operations'],
            },
            {
                'question': 'What is the rank of a matrix?',
                'answer': 'The rank is the dimension of the column space (or row space), equal to the number of linearly independent rows or columns',
                'difficulty': 'medium',
                'hint': 'It tells you the dimension of the image of the linear transformation',
                'skills': ['matrix_operations'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': 'What is the cross product of 3D vectors u = (u1,u2,u3) and v = (v1,v2,v3)?',
                'answer': 'u×v = (u2v3-u3v2, u3v1-u1v3, u1v2-u2v1), a vector perpendicular to both u and v',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Use the determinant with i, j, k unit vectors',
                'skills': ['matrix_operations'],
            },
            {
                'question': 'What is the characteristic equation for finding eigenvalues?',
                'answer': 'det(A - λI) = 0, where λ is an eigenvalue, A is the matrix, and I is the identity',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Set the determinant of (A - λI) equal to zero',
                'skills': ['eigenvalue_problems'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_odes_cards(self, topic):
        """Create flashcards for Ordinary Differential Equations"""
        skills = {
            'ode_classification': Skill.objects.get(name='ode_classification'),
            'first_order_ode_solving': Skill.objects.get(name='first_order_ode_solving'),
        }
        
        cards = [
            # Easy difficulty cards (3 cards)
            {
                'question': 'What is an ordinary differential equation (ODE)?',
                'answer': 'An equation containing a function of one variable and its derivatives.',
                'difficulty': 'easy',
                'skills': ['ode_classification'],
            },
            {
                'question': 'What is the order of a differential equation?',
                'answer': 'The order is the highest derivative that appears in the equation',
                'difficulty': 'easy',
                'skills': ['ode_classification'],
            },
            {
                'question': 'What is a linear differential equation?',
                'answer': 'An ODE where the dependent variable and its derivatives appear only to the first power and are not multiplied together',
                'difficulty': 'easy',
                'skills': ['ode_classification'],
            },
            # Medium difficulty cards (5 cards)
            {
                'question': 'What is the general form of a first-order linear ODE?',
                'answer': 'dy/dx + P(x)y = Q(x)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['ode_classification'],
            },
            {
                'question': 'What is a separable ODE?',
                'answer': 'An ODE that can be written as dy/dx = f(x)g(y), allowing separation of variables.',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['first_order_ode_solving'],
            },
            {
                'question': 'What is an integrating factor for first-order linear ODEs?',
                'answer': 'μ(x) = e^(∫P(x)dx), used to solve dy/dx + P(x)y = Q(x) by multiplying both sides',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'It makes the left side an exact derivative',
                'skills': ['first_order_ode_solving'],
            },
            {
                'question': 'What is the general solution form for a second-order linear homogeneous ODE?',
                'answer': 'y = c₁y₁ + c₂y₂, where y₁ and y₂ are linearly independent solutions',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['ode_classification'],
            },
            {
                'question': 'What is the characteristic equation for ay\'\' + by\' + cy = 0?',
                'answer': 'ar² + br + c = 0. The roots r₁ and r₂ determine the general solution: y = c₁e^(r₁x) + c₂e^(r₂x) for distinct real roots',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Replace y with e^(rx) and solve for r',
                'skills': ['first_order_ode_solving'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': 'What is the method of undetermined coefficients?',
                'answer': 'A technique for finding particular solutions to non-homogeneous linear ODEs by guessing a form based on the non-homogeneous term',
                'difficulty': 'hard',
                'hint': 'Used when the right-hand side is polynomial, exponential, sine, or cosine',
                'skills': ['first_order_ode_solving'],
            },
            {
                'question': 'What is variation of parameters?',
                'answer': 'A method to find particular solutions of non-homogeneous ODEs by replacing constants in the homogeneous solution with functions',
                'difficulty': 'hard',
                'hint': 'More general than undetermined coefficients, works for any continuous function',
                'skills': ['first_order_ode_solving'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_pdes_cards(self, topic):
        """Create flashcards for Partial Differential Equations"""
        skills = {
            'pde_classification': Skill.objects.get(name='pde_classification'),
            'separation_of_variables': Skill.objects.get(name='separation_of_variables'),
        }
        
        cards = [
            # Easy difficulty cards (3 cards)
            {
                'question': 'What is a partial differential equation (PDE)?',
                'answer': 'An equation containing a function of multiple variables and its partial derivatives.',
                'difficulty': 'easy',
                'skills': ['pde_classification'],
            },
            {
                'question': 'What is a boundary condition in PDEs?',
                'answer': 'Conditions specifying the values of the solution or its derivatives at the boundary of the domain',
                'difficulty': 'easy',
                'skills': ['pde_classification'],
            },
            {
                'question': 'What is an initial condition in PDEs?',
                'answer': 'Conditions specifying the value of the solution and/or its derivatives at time t=0',
                'difficulty': 'easy',
                'skills': ['pde_classification'],
            },
            # Medium difficulty cards (5 cards)
            {
                'question': 'Name the three main types of second-order PDEs.',
                'answer': 'Elliptic, Parabolic, and Hyperbolic',
                'difficulty': 'medium',
                'skills': ['pde_classification'],
            },
            {
                'question': 'What is the heat equation?',
                'answer': '∂u/∂t = α∇²u, a parabolic PDE modeling heat diffusion',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['pde_classification'],
            },
            {
                'question': 'What is the wave equation?',
                'answer': '∂²u/∂t² = c²∇²u, a hyperbolic PDE modeling wave propagation',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['pde_classification'],
            },
            {
                'question': "What is Laplace's equation?",
                'answer': '∇²u = 0, an elliptic PDE describing steady-state phenomena',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Also called the harmonic equation',
                'skills': ['pde_classification'],
            },
            {
                'question': 'What is the method of separation of variables?',
                'answer': 'A technique where you assume the solution can be written as a product of functions, each depending on only one variable',
                'difficulty': 'medium',
                'hint': 'For example, u(x,t) = X(x)T(t)',
                'skills': ['separation_of_variables'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': "What is the D'Alembert solution to the wave equation?",
                'answer': 'u(x,t) = f(x-ct) + g(x+ct), representing waves traveling in opposite directions',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Represents the general solution for the 1D wave equation',
                'skills': ['pde_classification'],
            },
            {
                'question': 'What role do Fourier series play in solving PDEs?',
                'answer': 'They expand the solution in terms of orthogonal eigenfunctions, satisfying boundary conditions and simplifying the PDE',
                'difficulty': 'hard',
                'hint': 'Particularly useful with separation of variables',
                'skills': ['separation_of_variables'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_fourier_analysis_cards(self, topic):
        """Create flashcards for Fourier Analysis"""
        skills = {
            'fourier_series': Skill.objects.get(name='fourier_series'),
            'fourier_transform': Skill.objects.get(name='fourier_transform'),
        }
        
        cards = [
            # Easy difficulty cards (3 cards)
            {
                'question': 'What is the fundamental frequency?',
                'answer': 'The lowest frequency in a Fourier series, determining the period of the function.',
                'difficulty': 'easy',
                'skills': ['fourier_series'],
            },
            {
                'question': 'What is the period of a periodic function f(x)?',
                'answer': 'The smallest positive value T such that f(x+T) = f(x) for all x',
                'difficulty': 'easy',
                'skills': ['fourier_series'],
            },
            {
                'question': 'What are harmonics in Fourier series?',
                'answer': 'Integer multiples of the fundamental frequency, representing the frequency components of the signal',
                'difficulty': 'easy',
                'skills': ['fourier_series'],
            },
            # Medium difficulty cards (5 cards)
            {
                'question': 'What is a Fourier series?',
                'answer': 'A representation of a periodic function as a sum of sine and cosine functions.',
                'difficulty': 'medium',
                'skills': ['fourier_series'],
            },
            {
                'question': 'What is the Fourier transform used for?',
                'answer': 'Converting a signal from time domain to frequency domain, analyzing frequency components.',
                'difficulty': 'medium',
                'skills': ['fourier_transform'],
            },
            {
                'question': 'What is the general form of a Fourier series for period 2L?',
                'answer': 'f(x) = a₀/2 + Σ[aₙcos(nπx/L) + bₙsin(nπx/L)]',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Sum goes from n=1 to infinity',
                'skills': ['fourier_series'],
            },
            {
                'question': 'How do even and odd functions simplify Fourier series?',
                'answer': 'Even functions have only cosine terms (bₙ=0), odd functions have only sine terms (aₙ=0)',
                'difficulty': 'medium',
                'hint': 'Even: f(-x)=f(x), Odd: f(-x)=-f(x)',
                'skills': ['fourier_series'],
            },
            {
                'question': 'What is the inverse Fourier transform?',
                'answer': 'f(t) = ∫F(ω)e^(iωt)dω/(2π), converts from frequency domain back to time domain',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['fourier_transform'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': 'What is the convolution theorem for Fourier transforms?',
                'answer': 'The Fourier transform of a convolution is the product of the Fourier transforms: F{f*g} = F{f}·F{g}',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Convolution in time domain = multiplication in frequency domain',
                'skills': ['fourier_transform'],
            },
            {
                'question': "What is Parseval's theorem?",
                'answer': 'The total energy in time domain equals total energy in frequency domain: ∫|f(t)|²dt = ∫|F(ω)|²dω',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Energy is conserved between domains',
                'skills': ['fourier_transform'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_laplace_transforms_cards(self, topic):
        """Create flashcards for Laplace Transforms"""
        skills = {
            'laplace_transform_calculation': Skill.objects.get(name='laplace_transform_calculation'),
            'inverse_laplace_transform': Skill.objects.get(name='inverse_laplace_transform'),
            'solving_odes_with_laplace': Skill.objects.get(name='solving_odes_with_laplace'),
        }
        
        cards = [
            # Easy difficulty cards (3 cards)
            {
                'question': 'What is L{1}?',
                'answer': '1/s',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['laplace_transform_calculation'],
            },
            {
                'question': 'What is L{e^(at)}?',
                'answer': '1/(s-a)',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['laplace_transform_calculation'],
            },
            {
                'question': 'What is L{t^n} for n ≥ 0?',
                'answer': 'n!/s^(n+1)',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['laplace_transform_calculation'],
            },
            # Medium difficulty cards (5 cards)
            {
                'question': 'What is the Laplace transform?',
                'answer': 'An integral transform that converts a function f(t) to F(s) = ∫₀^∞ e^(-st)f(t)dt',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['laplace_transform_calculation'],
            },
            {
                'question': 'Why use Laplace transforms to solve ODEs?',
                'answer': 'They convert differential equations into algebraic equations, which are easier to solve.',
                'difficulty': 'medium',
                'skills': ['solving_odes_with_laplace'],
            },
            {
                'question': 'What is L{sin(ωt)}?',
                'answer': 'ω/(s² + ω²)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['laplace_transform_calculation'],
            },
            {
                'question': 'What is L{cos(ωt)}?',
                'answer': 's/(s² + ω²)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['laplace_transform_calculation'],
            },
            {
                'question': 'What is the linearity property of Laplace transforms?',
                'answer': 'L{af(t) + bg(t)} = aL{f(t)} + bL{g(t)}, where a and b are constants',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['laplace_transform_calculation'],
            },
            # Hard difficulty cards (2 cards)
            {
                'question': 'What is the First Shifting Theorem (s-shift)?',
                'answer': 'L{e^(at)f(t)} = F(s-a), where F(s) = L{f(t)}',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'Multiplying by e^(at) shifts the transform by a',
                'skills': ['laplace_transform_calculation'],
            },
            {
                'question': 'What is the Laplace transform of a derivative L{f\'(t)}?',
                'answer': 'sF(s) - f(0), where F(s) = L{f(t)}',
                'difficulty': 'hard',
                'uses_latex': True,
                'hint': 'This is why Laplace transforms are useful for ODEs',
                'skills': ['solving_odes_with_laplace'],
            },
        ]
        
        return self._create_cards(topic, cards, skills)

    def _create_cards(self, topic, cards_data, skills_dict):
        """Helper method to create flashcards from data"""
        count = 0
        for card_data in cards_data:
            # Handle parameterized cards
            if card_data.get('question_type') == 'parameterized':
                flashcard = Flashcard.objects.create(
                    topic=topic,
                    question='Placeholder for parameterized card',
                    answer='Placeholder',
                    question_type='parameterized',
                    question_template=card_data['question_template'],
                    answer_template=card_data['answer_template'],
                    parameter_spec=card_data['parameter_spec'],
                    difficulty=card_data['difficulty'],
                    hint=card_data.get('hint', ''),
                    uses_latex=card_data.get('uses_latex', False),
                )
            else:
                # Standard Q&A cards
                flashcard = Flashcard.objects.create(
                    topic=topic,
                    question=card_data['question'],
                    answer=card_data['answer'],
                    difficulty=card_data['difficulty'],
                    hint=card_data.get('hint', ''),
                    uses_latex=card_data.get('uses_latex', False),
                )
            
            # Add skills
            if 'skills' in card_data:
                for skill_name in card_data['skills']:
                    if skill_name in skills_dict:
                        flashcard.skills.add(skills_dict[skill_name])
            
            count += 1
        
        return count
