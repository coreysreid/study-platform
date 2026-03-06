from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return
    course = Course.objects.filter(name='Mathematics 1B', created_by=system_user).first()
    if not course:
        return
    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    def add_cards(topic_name, cards):
        topic = topics.get(topic_name)
        if not topic or Flashcard.objects.filter(topic=topic).exists():
            return
        for card in cards:
            Flashcard.objects.create(topic=topic, **card)

    # ------------------------------------------------------------------ #
    # 001A — Advanced Integration Techniques
    # ------------------------------------------------------------------ #
    add_cards('Advanced Integration Techniques', [
        {'question': 'Integration by parts formula.',
         'answer': '∫ u dv = uv − ∫ v du. Choose u to differentiate (becomes simpler) and dv to integrate.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'LIATE rule for choosing u in integration by parts.',
         'answer': 'Preference order: Logarithm, Inverse trig, Algebraic, Trig, Exponential. Choose u from earliest category.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Evaluate ∫ x eˣ dx using integration by parts.',
         'answer': 'u = x, dv = eˣ dx → du = dx, v = eˣ. ∫ x eˣ dx = x eˣ − ∫ eˣ dx = x eˣ − eˣ + C = eˣ(x−1) + C.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Choose u and dv', 'detail': 'u = x (algebraic), dv = eˣ dx'},
                   {'move': 'Differentiate u and integrate dv', 'detail': 'du = dx, v = eˣ'},
                   {'move': 'Apply formula', 'detail': '∫ x eˣ dx = x eˣ − ∫ eˣ dx = eˣ(x−1) + C'}]},
        {'question': 'Partial fractions for distinct linear factors: decompose (2x+1)/((x+1)(x−2)).',
         'answer': 'Write as A/(x+1) + B/(x−2). Multiply through: 2x+1 = A(x−2) + B(x+1). x=2: 5=3B → B=5/3. x=−1: −1=−3A → A=1/3.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Set up decomposition', 'detail': '(2x+1)/((x+1)(x−2)) = A/(x+1) + B/(x−2)'},
                   {'move': 'Multiply by denominator', 'detail': '2x+1 = A(x−2) + B(x+1)'},
                   {'move': 'Substitute roots', 'detail': 'x=2 → B=5/3; x=−1 → A=1/3'}]},
        {'question': 'Partial fractions for a repeated linear factor: how to decompose 1/(x−1)²?',
         'answer': 'Write A/(x−1) + B/(x−1)². Each power of the repeated factor gets its own term.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Trigonometric substitution for √(a²−x²).',
         'answer': 'Substitute x = a sin θ. Then √(a²−x²) = a cos θ. Useful for ∫ √(1−x²) dx and similar.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Trigonometric substitution for √(x²+a²).',
         'answer': 'Substitute x = a tan θ. Then √(x²+a²) = a sec θ.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Improper integral ∫₁^∞ 1/xᵖ dx: when does it converge?',
         'answer': 'Converges when p > 1; value = 1/(p−1). Diverges when p ≤ 1.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Evaluate the improper integral ∫₀^∞ e^(−x) dx.',
         'answer': 'lim_{b→∞} ∫₀^b e^(−x) dx = lim_{b→∞} [−e^(−x)]₀^b = lim_{b→∞} (1 − e^(−b)) = 1.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 001B — Volumes, Surface Areas & Applications
    # ------------------------------------------------------------------ #
    add_cards('Volumes, Surface Areas & Applications', [
        {'question': 'Disk method: volume of revolution about x-axis.',
         'answer': 'V = π ∫_a^b [R(x)]² dx, where R(x) is the radius (distance from x-axis to curve).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Washer method: volume when rotating region between f(x) and g(x) about x-axis (f ≥ g ≥ 0).',
         'answer': 'V = π ∫_a^b ([f(x)]² − [g(x)]²) dx. Outer radius R = f(x), inner radius r = g(x).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Shell method: volume from rotating y = f(x) ≥ 0 on [a,b] about the y-axis.',
         'answer': 'V = 2π ∫_a^b x·f(x) dx. Each shell has circumference 2πx, height f(x), thickness dx.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Surface area of revolution: rotate y = f(x) on [a,b] about x-axis.',
         'answer': 'SA = 2π ∫_a^b f(x) √(1 + [f\'(x)]²) dx.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the volume of a sphere of radius R using the disk method.',
         'answer': 'Rotate y = √(R²−x²) about x-axis, x from −R to R. V = π ∫_{-R}^R (R²−x²) dx = π[R²x − x³/3]_{-R}^R = (4/3)πR³.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Set up integral', 'detail': 'V = π ∫_{-R}^R (R²−x²) dx'},
                   {'move': 'Integrate', 'detail': '[R²x − x³/3]_{-R}^R'},
                   {'move': 'Evaluate', 'detail': '(R³ − R³/3) − (−R³ + R³/3) = (4/3)πR³ ✓'}]},
    ])

    # ------------------------------------------------------------------ #
    # 002A — Numerical Methods
    # ------------------------------------------------------------------ #
    add_cards('Numerical Methods', [
        {'question': 'Newton-Raphson iteration formula.',
         'answer': 'x_{n+1} = xₙ − f(xₙ)/f\'(xₙ). Starting from initial guess x₀, converges quadratically near a simple root.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'One Newton-Raphson step for f(x) = x² − 2 starting at x₀ = 1.',
         'answer': "f(1) = −1, f'(1) = 2. x₁ = 1 − (−1)/2 = 1.5. (Approximating √2 ≈ 1.414.)",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Bisection method: when does it apply?',
         'answer': 'When f is continuous on [a,b] and f(a) and f(b) have opposite signs. A root is guaranteed by IVT. Each step halves the interval.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Trapezoidal rule for ∫_a^b f(x) dx with n subintervals.',
         'answer': 'T = (h/2)[f(x₀) + 2f(x₁) + 2f(x₂) + … + 2f(x_{n−1}) + f(xₙ)], where h = (b−a)/n.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Simpson\'s 1/3 rule (n must be even).',
         'answer': 'S = (h/3)[f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + … + 4f(x_{n−1}) + f(xₙ)], h = (b−a)/n. More accurate than trapezoidal.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Euler\'s method for y\' = f(x, y), y(x₀) = y₀.',
         'answer': 'yₙ₊₁ = yₙ + h·f(xₙ, yₙ). Simple but first-order accurate (error O(h)). Step size h must be small for accuracy.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is round-off error vs truncation error in numerical methods?',
         'answer': 'Round-off error: finite computer precision when representing numbers. Truncation error: error from approximating an infinite process (e.g. Taylor series) with a finite one.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    # ------------------------------------------------------------------ #
    # 003A — Vector Spaces & Linear Transformations
    # ------------------------------------------------------------------ #
    add_cards('Vector Spaces & Linear Transformations', [
        {'question': 'What is a vector space?',
         'answer': 'A set V with addition and scalar multiplication satisfying 8 axioms: closure, associativity, commutativity, identity (0), inverses, scalar distributivity, vector distributivity, scalar associativity.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is a subspace?',
         'answer': 'A subset W ⊆ V that is itself a vector space under the same operations. Sufficient conditions: W contains 0, and W is closed under addition and scalar multiplication.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Linear independence: what does it mean for {v₁, v₂, …, vₙ} to be linearly independent?',
         'answer': 'Only the trivial combination gives zero: c₁v₁ + c₂v₂ + … + cₙvₙ = 0 ⟹ c₁ = c₂ = … = cₙ = 0.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the span of a set of vectors?',
         'answer': 'Span{v₁,…,vₙ} = {c₁v₁ + … + cₙvₙ : cᵢ ∈ ℝ} — all linear combinations. It is the smallest subspace containing all vᵢ.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a basis?',
         'answer': 'A set that is linearly independent AND spans V. The number of basis vectors equals the dimension of V.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Standard basis for ℝ³.',
         'answer': 'e₁ = (1,0,0), e₂ = (0,1,0), e₃ = (0,0,1). They are orthonormal (mutually perpendicular unit vectors).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Definition of a linear transformation T: V → W.',
         'answer': 'T satisfies: 1. T(u+v) = T(u)+T(v) (additivity). 2. T(cu) = cT(u) (homogeneity). Equivalently: T(αu+βv) = αT(u)+βT(v).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Kernel (null space) of a linear transformation T.',
         'answer': 'ker(T) = {v ∈ V : T(v) = 0}. It is a subspace of V. T is injective (one-to-one) iff ker(T) = {0}.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Rank-Nullity Theorem.',
         'answer': 'dim(ker T) + dim(im T) = dim(V). Equivalently: nullity(A) + rank(A) = n (number of columns).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 003B — Eigenvalues & Eigenvectors  (critical for Control Systems)
    # ------------------------------------------------------------------ #
    add_cards('Eigenvalues & Eigenvectors', [
        {'question': 'Definition of eigenvalue and eigenvector.',
         'answer': 'For square matrix A, λ is an eigenvalue and v ≠ 0 is a corresponding eigenvector if Av = λv. The eigenvector is scaled, not rotated, by A.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How do you find eigenvalues of A?',
         'answer': 'Solve the characteristic equation det(A − λI) = 0. The roots λ are the eigenvalues.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the eigenvalues of A = [[2, 1], [1, 2]].',
         'answer': 'det(A−λI) = (2−λ)²−1 = λ²−4λ+3 = (λ−1)(λ−3) = 0. Eigenvalues: λ₁ = 1, λ₂ = 3.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Form A − λI', 'detail': '[[2−λ, 1], [1, 2−λ]]'},
                   {'move': 'Compute determinant', 'detail': '(2−λ)² − 1 = λ² − 4λ + 3'},
                   {'move': 'Factor', 'detail': '(λ−1)(λ−3) = 0 → λ = 1, 3'}]},
        {'question': 'How do you find eigenvectors for eigenvalue λ?',
         'answer': 'Solve (A − λI)v = 0 — i.e. the null space of (A − λI). Find vectors v that are in the kernel.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the eigenvector of A = [[2,1],[1,2]] for λ = 1.',
         'answer': '(A−I)v = 0 → [[1,1],[1,1]]v = 0 → v₁ + v₂ = 0 → v = t[1,−1]. Eigenvector: [1,−1] (or any scalar multiple).',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Form A − λI = A − I', 'detail': '[[1,1],[1,1]]'},
                   {'move': 'Solve (A−I)v = 0', 'detail': 'v₁ + v₂ = 0, so v₂ = −v₁'},
                   {'move': 'Write eigenvector', 'detail': 'v = [1, −1]ᵀ (normalised: [1/√2, −1/√2]ᵀ)'}]},
        {'question': 'Trace and determinant in terms of eigenvalues.',
         'answer': 'For a 2×2 matrix: tr(A) = λ₁ + λ₂ and det(A) = λ₁ · λ₂. (General: sum and product of all eigenvalues.)',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Diagonalisation: when can A be diagonalised?',
         'answer': 'A = PDP⁻¹ where D = diag(λ₁,…,λₙ). Possible iff A has n linearly independent eigenvectors (e.g. n distinct eigenvalues, or all repeated eigenvalues have full geometric multiplicity).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Why are eigenvalues critical for control system stability?',
         'answer': 'System ẋ = Ax is stable iff all eigenvalues of A have negative real parts. In transfer function form: eigenvalues of A = poles. Poles in left half-plane → stable.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Solve the ODE system x\' = Ax using eigenvalues.',
         'answer': 'Solution: x(t) = Σ cᵢ vᵢ e^(λᵢt), where (λᵢ, vᵢ) are eigenpairs. Constants cᵢ from initial condition x(0) = Σ cᵢ vᵢ.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Eigenvalues of an upper (or lower) triangular matrix.',
         'answer': 'The eigenvalues are the diagonal entries. det(A − λI) for a triangular matrix gives a product of (aᵢᵢ − λ) terms.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 004B — Vector Functions & Line Integrals
    # ------------------------------------------------------------------ #
    add_cards('Vector Functions & Line Integrals', [
        {'question': 'What is a vector-valued function?',
         'answer': 'r(t) = ⟨x(t), y(t), z(t)⟩. Maps a scalar t to a vector in ℝ² or ℝ³, tracing a curve as t varies.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Derivative of r(t) = ⟨x(t), y(t), z(t)⟩.',
         'answer': "r'(t) = ⟨x'(t), y'(t), z'(t)⟩. The tangent vector to the curve at t.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Arc length of curve r(t) from t = a to t = b.',
         'answer': "L = ∫_a^b |r'(t)| dt = ∫_a^b √(x'² + y'² + z'²) dt.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Line integral of a scalar function f along curve C.',
         'answer': "∫_C f ds = ∫_a^b f(r(t)) |r'(t)| dt.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Work as a line integral: W = ∫_C F · dr.',
         'answer': "W = ∫_a^b F(r(t)) · r'(t) dt. The dot product selects the component of force along the path.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a conservative vector field?',
         'answer': 'F = ∇f for some scalar potential f. Line integrals are path-independent: ∫_C F · dr = f(B) − f(A).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 005A — Surface Integrals & Green's Theorem
    # ------------------------------------------------------------------ #
    add_cards("Surface Integrals & Green's Theorem", [
        {'question': "State Green's Theorem.",
         'answer': '∮_C P dx + Q dy = ∬_D (∂Q/∂x − ∂P/∂y) dA. Converts a line integral around closed curve C to a double integral over enclosed region D.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': "Use Green's Theorem to find the area of region D.",
         'answer': 'Area = (1/2) ∮_C (x dy − y dx). This follows from Green\'s Theorem with P = −y/2, Q = x/2.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a surface integral of a scalar function over surface S?',
         'answer': '∬_S f dS = ∬_D f(r(u,v)) |rᵤ × rᵥ| dA, where r(u,v) parametrises S.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Flux integral: physical meaning and formula.',
         'answer': 'Flux = ∬_S F · dS = ∬_S F · n̂ dS. Measures the net flow of F through surface S per unit time (e.g. fluid flow, electric flux).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': "State Stokes' Theorem.",
         'answer': "∬_S (∇ × F) · dS = ∮_C F · dr. Relates the surface integral of curl F to the line integral around boundary C of S.",
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 005B — Gauss's Divergence Theorem
    # ------------------------------------------------------------------ #
    add_cards("Gauss's Divergence Theorem", [
        {'question': 'Define the divergence of F = ⟨P, Q, R⟩.',
         'answer': 'div F = ∇ · F = ∂P/∂x + ∂Q/∂y + ∂R/∂z. A scalar measuring the net outward flux per unit volume.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': "State the Divergence Theorem (Gauss's Theorem).",
         'answer': '∯_S F · dS = ∭_V (∇ · F) dV. The outward flux through closed surface S equals the integral of divergence over enclosed volume V.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Physical interpretation of the Divergence Theorem.',
         'answer': 'For fluid flow, the total outward flux through a closed surface equals the total "source strength" inside. Divergence > 0: source; < 0: sink; = 0: incompressible.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Apply the Divergence Theorem: find ∯_S F · dS for F = ⟨x, y, z⟩ over a unit sphere.',
         'answer': '∇ · F = 1+1+1 = 3. Volume of unit sphere = (4/3)π. Flux = 3 · (4/3)π = 4π.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Compute divergence', 'detail': '∇ · ⟨x,y,z⟩ = 3'},
                   {'move': 'Apply theorem', 'detail': '∭_V 3 dV = 3 × V(unit sphere)'},
                   {'move': 'Evaluate', 'detail': '3 × (4π/3) = 4π'}]},
        {'question': 'Define the curl of F = ⟨P, Q, R⟩.',
         'answer': 'curl F = ∇ × F = ⟨∂R/∂y−∂Q/∂z, ∂P/∂z−∂R/∂x, ∂Q/∂x−∂P/∂y⟩. A vector measuring local rotation.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0032_flashcards_sma101'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_func),
    ]
