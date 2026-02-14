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
            help='Username of the user who will own the content',
            required=True,
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Skip if flashcards already exist for topics',
        )

    def handle(self, *args, **options):
        username = options['user']
        skip_existing = options.get('skip_existing', False)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

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
            # Standard Q&A cards
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
                'question': 'List the first 10 prime numbers.',
                'answer': '2, 3, 5, 7, 11, 13, 17, 19, 23, 29',
                'difficulty': 'medium',
                'hint': 'Start with 2, the only even prime number',
                'skills': ['basic_arithmetic'],
            },
            # Parameterized cards
            {
                'question_type': 'parameterized',
                'question_template': 'Simplify the fraction: {numerator}/{denominator}',
                'answer_template': '{simplified_num}/{simplified_den}',
                'parameter_spec': {
                    'variables': {
                        'gcd': {'type': 'random_choice', 'choices': [2, 3, 4, 5, 6]},
                        'simplified_num': {'type': 'random_int', 'min': 1, 'max': 10},
                        'simplified_den': {'type': 'random_int', 'min': 2, 'max': 12},
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
            {
                'question': 'What is the quadratic formula?',
                'answer': 'x = (-b ± √(b² - 4ac)) / (2a) for equation ax² + bx + c = 0',
                'difficulty': 'medium',
                'uses_latex': True,
                'hint': 'Used to solve equations of the form ax² + bx + c = 0',
                'skills': ['quadratic_equations'],
            },
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
                'question': 'What is the difference of squares formula?',
                'answer': 'a² - b² = (a + b)(a - b)',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['factoring'],
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
                'question': 'What is the formula for the volume of a sphere?',
                'answer': 'V = (4/3)πr³, where r is the radius',
                'difficulty': 'medium',
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
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_trigonometry_cards(self, topic):
        """Create flashcards for Trigonometry Fundamentals"""
        skills = {
            'trigonometric_ratios': Skill.objects.get(name='trigonometric_ratios'),
            'trigonometric_identities': Skill.objects.get(name='trigonometric_identities'),
        }
        
        cards = [
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
                'question': 'What is the Pythagorean identity for trigonometry?',
                'answer': 'sin²(θ) + cos²(θ) = 1',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['trigonometric_identities'],
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
            {
                'question': 'What is the definition of a function?',
                'answer': 'A function is a relation where each input (x) has exactly one output (y).',
                'difficulty': 'easy',
                'skills': ['function_analysis'],
            },
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
                'question': 'What is e (Euler\'s number) approximately equal to?',
                'answer': 'Approximately 2.71828',
                'difficulty': 'easy',
                'skills': ['exponential_logarithmic'],
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
            {
                'question': 'What is the definition of a derivative?',
                'answer': 'f\'(x) = lim(h→0) [f(x+h) - f(x)] / h',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['derivative_calculation'],
            },
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
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_integral_calculus_cards(self, topic):
        """Create flashcards for Integral Calculus"""
        skills = {
            'integration_techniques': Skill.objects.get(name='integration_techniques'),
            'definite_integrals': Skill.objects.get(name='definite_integrals'),
        }
        
        cards = [
            {
                'question': 'State the Fundamental Theorem of Calculus (Part 1).',
                'answer': 'If F\'(x) = f(x), then ∫[a to b] f(x)dx = F(b) - F(a)',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['definite_integrals'],
            },
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
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_multivariable_calculus_cards(self, topic):
        """Create flashcards for Multivariable Calculus"""
        skills = {
            'partial_derivatives': Skill.objects.get(name='partial_derivatives'),
            'multiple_integrals': Skill.objects.get(name='multiple_integrals'),
        }
        
        cards = [
            {
                'question': 'What is a partial derivative?',
                'answer': 'The derivative of a multivariable function with respect to one variable, treating all other variables as constants.',
                'difficulty': 'medium',
                'skills': ['partial_derivatives'],
            },
            {
                'question': 'How do you compute ∂f/∂x for f(x,y)?',
                'answer': 'Take the derivative of f with respect to x, treating y as a constant.',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['partial_derivatives'],
            },
            {
                'question': 'What is a double integral used for?',
                'answer': 'Computing volumes under surfaces, areas of regions, or mass of 2D objects with varying density.',
                'difficulty': 'medium',
                'skills': ['multiple_integrals'],
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
            {
                'question': 'What is the determinant of a 2×2 matrix [[a,b],[c,d]]?',
                'answer': 'ad - bc',
                'difficulty': 'easy',
                'uses_latex': True,
                'skills': ['determinants'],
            },
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
                'question': 'What is the identity matrix?',
                'answer': 'A square matrix with 1s on the main diagonal and 0s elsewhere. Denoted as I.',
                'difficulty': 'easy',
                'skills': ['matrix_operations'],
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
            {
                'question': 'What is an ordinary differential equation (ODE)?',
                'answer': 'An equation containing a function of one variable and its derivatives.',
                'difficulty': 'easy',
                'skills': ['ode_classification'],
            },
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
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_pdes_cards(self, topic):
        """Create flashcards for Partial Differential Equations"""
        skills = {
            'pde_classification': Skill.objects.get(name='pde_classification'),
            'separation_of_variables': Skill.objects.get(name='separation_of_variables'),
        }
        
        cards = [
            {
                'question': 'What is a partial differential equation (PDE)?',
                'answer': 'An equation containing a function of multiple variables and its partial derivatives.',
                'difficulty': 'easy',
                'skills': ['pde_classification'],
            },
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
        ]
        
        return self._create_cards(topic, cards, skills)

    def create_fourier_analysis_cards(self, topic):
        """Create flashcards for Fourier Analysis"""
        skills = {
            'fourier_series': Skill.objects.get(name='fourier_series'),
            'fourier_transform': Skill.objects.get(name='fourier_transform'),
        }
        
        cards = [
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
                'question': 'What is the fundamental frequency?',
                'answer': 'The lowest frequency in a Fourier series, determining the period of the function.',
                'difficulty': 'easy',
                'skills': ['fourier_series'],
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
            {
                'question': 'What is the Laplace transform?',
                'answer': 'An integral transform that converts a function f(t) to F(s) = ∫₀^∞ e^(-st)f(t)dt',
                'difficulty': 'medium',
                'uses_latex': True,
                'skills': ['laplace_transform_calculation'],
            },
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
                'question': 'Why use Laplace transforms to solve ODEs?',
                'answer': 'They convert differential equations into algebraic equations, which are easier to solve.',
                'difficulty': 'medium',
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
