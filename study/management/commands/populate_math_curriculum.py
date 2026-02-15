"""
Django management command to populate the database with core mathematics curriculum.

This command creates:
1. A core "Engineering Mathematics" course
2. All 13 topics outlined in the curriculum
3. Skills tags for prerequisite tracking
4. Sets up prerequisite relationships between topics

Usage:
    python manage.py populate_math_curriculum --user=<username>
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from study.models import Course, Topic, Skill


class Command(BaseCommand):
    help = 'Populates the database with core mathematics curriculum for engineering students'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Username of the user who will own the course (default: system)',
            default='system',
            required=False,
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Skip creation if course already exists',
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

        # Check if course already exists
        existing_course = Course.objects.filter(
            name='Engineering Mathematics',
            created_by=user
        ).first()

        if existing_course and skip_existing:
            self.stdout.write(
                self.style.WARNING(
                    f'Course "Engineering Mathematics" already exists for user {username}. Skipping.'
                )
            )
            return

        if existing_course:
            self.stdout.write(
                self.style.WARNING(
                    f'Deleting existing "Engineering Mathematics" course...'
                )
            )
            existing_course.delete()

        # Create the course
        self.stdout.write('Creating Engineering Mathematics course...')
        course = Course.objects.create(
            name='Engineering Mathematics',
            code='ENGMATH',
            description=(
                'Comprehensive mathematics curriculum for Bachelor of Engineering students. '
                'Starting from Year 6 foundation, progressing through calculus, linear algebra, '
                'differential equations, Fourier analysis, and Laplace transforms.'
            ),
            created_by=user
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Created course: {course.name}'))

        # Create all skills first
        self.stdout.write('\nCreating skill tags...')
        skills_data = [
            # Foundation Skills
            'basic_arithmetic', 'fraction_operations', 'decimal_operations',
            'order_of_operations', 'scientific_notation', 'algebraic_manipulation',
            'equation_solving', 'exponent_rules', 'polynomial_operations',
            'factoring', 'quadratic_equations',
            
            # Geometric Skills
            'geometric_reasoning', 'pythagorean_theorem', 'area_volume_calculations',
            'coordinate_geometry', 'angle_relationships',
            
            # Trigonometric Skills
            'trigonometric_ratios', 'right_triangle_solving', 'trigonometric_identities',
            'unit_circle', 'trig_equation_solving',
            
            # Pre-Calculus Skills
            'function_analysis', 'exponential_logarithmic', 'complex_numbers',
            'sequences_series', 'limit_concepts',
            
            # Calculus Skills
            'derivative_calculation', 'differentiation_rules', 'implicit_differentiation',
            'optimization', 'curve_analysis', 'related_rates', 'integration_techniques',
            'definite_integrals', 'area_calculations', 'volume_of_revolution',
            'applications_of_integration',
            
            # Advanced Skills
            'partial_derivatives', 'multiple_integrals', 'vector_calculus',
            'multivariable_optimization', 'coordinate_transformations', 'matrix_operations',
            'determinants', 'solving_linear_systems', 'eigenvalue_problems',
            'vector_spaces', 'linear_transformations', 'ode_classification',
            'first_order_ode_solving', 'second_order_ode_solving', 'systems_of_odes',
            'modeling_with_odes', 'pde_classification', 'separation_of_variables',
            'boundary_value_problems', 'method_of_characteristics', 'pde_applications',
            'fourier_series', 'fourier_coefficients', 'fourier_transform',
            'signal_analysis', 'frequency_domain', 'laplace_transform_calculation',
            'inverse_laplace_transform', 'solving_odes_with_laplace',
            'transfer_functions', 'system_analysis',
        ]

        skills = {}
        for skill_name in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_name,
                defaults={'description': f'Foundational skill: {skill_name.replace("_", " ").title()}'}
            )
            skills[skill_name] = skill
            if created:
                self.stdout.write(f'  ✓ Created skill: {skill_name}')
            else:
                self.stdout.write(f'  → Using existing skill: {skill_name}')

        # Define topics with their details
        topics_data = [
            {
                'order': 1,
                'name': 'Basic Arithmetic & Number Sense',
                'description': (
                    'Master operations with whole numbers, fractions, decimals, and percentages. '
                    'Understand order of operations (PEMDAS/BODMAS), work with positive and '
                    'negative numbers, scientific notation and significant figures, ratios and proportions.'
                ),
                'prerequisites': [],
            },
            {
                'order': 2,
                'name': 'Algebra Fundamentals',
                'description': (
                    'Manipulate algebraic expressions, solve linear equations and inequalities, '
                    'work with exponents and roots, factor polynomials, and solve systems of equations.'
                ),
                'prerequisites': ['Basic Arithmetic & Number Sense'],
            },
            {
                'order': 3,
                'name': 'Geometry',
                'description': (
                    'Understand geometric shapes and their properties, apply the Pythagorean theorem, '
                    'calculate areas, volumes, and surface areas, work with angles and triangles, '
                    'understand coordinate geometry basics.'
                ),
                'prerequisites': ['Basic Arithmetic & Number Sense', 'Algebra Fundamentals'],
            },
            {
                'order': 4,
                'name': 'Trigonometry Fundamentals',
                'description': (
                    'Understand trigonometric ratios, solve right triangles, apply trigonometric '
                    'identities, work with the unit circle, and solve trigonometric equations.'
                ),
                'prerequisites': ['Geometry', 'Algebra Fundamentals'],
            },
            {
                'order': 5,
                'name': 'Pre-Calculus',
                'description': (
                    'Master functions and their properties, understand limits and continuity concepts, '
                    'work with complex numbers, analyze sequences and series, study conic sections.'
                ),
                'prerequisites': ['Algebra Fundamentals', 'Geometry', 'Trigonometry Fundamentals'],
            },
            {
                'order': 6,
                'name': 'Differential Calculus',
                'description': (
                    'Understand the concept of derivatives, master differentiation techniques, '
                    'apply derivatives to real-world problems, analyze function behavior using '
                    'derivatives, and solve optimization problems.'
                ),
                'prerequisites': ['Pre-Calculus'],
            },
            {
                'order': 7,
                'name': 'Integral Calculus',
                'description': (
                    'Understand the concept of integration, master integration techniques, '
                    'apply integrals to calculate areas, volumes, and other quantities, '
                    'understand the Fundamental Theorem of Calculus.'
                ),
                'prerequisites': ['Differential Calculus'],
            },
            {
                'order': 8,
                'name': 'Multivariable Calculus',
                'description': (
                    'Extend calculus to functions of several variables, calculate partial derivatives '
                    'and multiple integrals, work with vector calculus, apply calculus to '
                    'three-dimensional problems.'
                ),
                'prerequisites': ['Differential Calculus', 'Integral Calculus'],
            },
            {
                'order': 9,
                'name': 'Linear Algebra',
                'description': (
                    'Understand vector spaces and linear transformations, master matrix operations, '
                    'solve systems of linear equations, calculate eigenvalues and eigenvectors, '
                    'apply linear algebra to engineering problems.'
                ),
                'prerequisites': ['Algebra Fundamentals', 'Pre-Calculus'],
            },
            {
                'order': 10,
                'name': 'Ordinary Differential Equations (ODEs)',
                'description': (
                    'Classify and solve different types of ODEs, understand solution methods for '
                    'first and higher-order equations, apply ODEs to model physical systems.'
                ),
                'prerequisites': ['Differential Calculus', 'Integral Calculus'],
            },
            {
                'order': 11,
                'name': 'Partial Differential Equations (PDEs)',
                'description': (
                    'Understand the nature of PDEs, classify PDEs (elliptic, parabolic, hyperbolic), '
                    'solve common PDEs using various methods, apply PDEs to engineering problems.'
                ),
                'prerequisites': ['Multivariable Calculus', 'Ordinary Differential Equations (ODEs)'],
            },
            {
                'order': 12,
                'name': 'Fourier Analysis',
                'description': (
                    'Understand Fourier series and their applications, compute Fourier coefficients, '
                    'apply Fourier transforms, use Fourier methods in signal processing.'
                ),
                'prerequisites': ['Integral Calculus', 'Trigonometry Fundamentals'],
            },
            {
                'order': 13,
                'name': 'Laplace Transforms',
                'description': (
                    'Understand and compute Laplace transforms, apply inverse Laplace transforms, '
                    'use Laplace transforms to solve ODEs, apply transforms to engineering problems.'
                ),
                'prerequisites': ['Integral Calculus', 'Ordinary Differential Equations (ODEs)'],
            },
        ]

        # Create topics
        self.stdout.write('\nCreating topics...')
        created_topics = {}
        
        for topic_data in topics_data:
            topic = Topic.objects.create(
                course=course,
                name=topic_data['name'],
                description=topic_data['description'],
                order=topic_data['order']
            )
            created_topics[topic_data['name']] = topic
            self.stdout.write(f'  ✓ Created topic {topic_data["order"]}: {topic.name}')

        # Set up prerequisites
        self.stdout.write('\nSetting up prerequisite relationships...')
        for topic_data in topics_data:
            topic = created_topics[topic_data['name']]
            for prereq_name in topic_data['prerequisites']:
                prereq_topic = created_topics[prereq_name]
                topic.prerequisites.add(prereq_topic)
                self.stdout.write(
                    f'  ✓ {topic.name} requires {prereq_topic.name}'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully created Engineering Mathematics curriculum with {len(topics_data)} topics!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Created {len(skills_data)} skill tags for prerequisite tracking'
            )
        )
        self.stdout.write('\nNext steps:')
        self.stdout.write('  1. Review the curriculum in docs/MATHEMATICS_CURRICULUM.md')
        self.stdout.write('  2. Begin creating flashcards for each topic')
        self.stdout.write('  3. Tag flashcards with appropriate skills')
        self.stdout.write('  4. Implement the learning feedback loop')
