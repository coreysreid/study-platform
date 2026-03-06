from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return
    course = Course.objects.filter(name='Mathematics 1A', created_by=system_user).first()
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
    # 001A — Functions & Limits
    # ------------------------------------------------------------------ #
    add_cards('Functions & Limits', [
        {'question': 'Define a function.',
         'answer': 'A function f: A → B assigns to each element x in domain A exactly one element f(x) in codomain B. Key: each input has one output.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is the domain of f(x) = √(4 − x²)?',
         'answer': 'Need 4 − x² ≥ 0, so x² ≤ 4, i.e. −2 ≤ x ≤ 2. Domain: [−2, 2].',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What does the vertical line test determine?',
         'answer': 'Whether a curve in the xy-plane represents a function. A curve is a function if and only if every vertical line intersects it at most once.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Informal definition of lim_{x→a} f(x) = L.',
         'answer': 'As x gets arbitrarily close to a (but not equal), f(x) gets arbitrarily close to L. The value of f at a does not matter.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Evaluate lim_{x→3} (x² − 9)/(x − 3).',
         'answer': 'Factor: (x²−9)/(x−3) = (x+3)(x−3)/(x−3) = x+3. Limit = 3+3 = 6.',
         'difficulty': 'easy', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Factor numerator', 'detail': 'x²−9 = (x+3)(x−3)'},
                   {'move': 'Cancel', 'detail': '(x+3)(x−3)/(x−3) = x+3  (x ≠ 3)'},
                   {'move': 'Substitute', 'detail': 'lim = 3+3 = 6'}]},
        {'question': 'When does a two-sided limit fail to exist?',
         'answer': 'When left-hand limit ≠ right-hand limit, or when the function oscillates or grows without bound near the point.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'State the Squeeze Theorem.',
         'answer': 'If g(x) ≤ f(x) ≤ h(x) near a and lim_{x→a} g(x) = lim_{x→a} h(x) = L, then lim_{x→a} f(x) = L.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Evaluate lim_{x→0} sin(x)/x.',
         'answer': '1. This fundamental limit is proved using the Squeeze Theorem and is the basis for all trigonometric derivatives.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Evaluate lim_{x→∞} (3x² + 2x)/(x² − 5).',
         'answer': 'Divide numerator and denominator by x²: (3 + 2/x)/(1 − 5/x²) → 3/1 = 3 as x→∞.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Divide by highest power x²', 'detail': '(3 + 2/x)/(1 − 5/x²)'},
                   {'move': 'Take limit', 'detail': '2/x → 0 and 5/x² → 0'},
                   {'move': 'Result', 'detail': '3/1 = 3'}]},
        {'question': 'What is a horizontal asymptote?',
         'answer': 'y = L is a horizontal asymptote if lim_{x→∞} f(x) = L or lim_{x→−∞} f(x) = L.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State L\'Hôpital\'s Rule.',
         'answer': 'If lim_{x→a} f(x)/g(x) gives 0/0 or ∞/∞, then lim_{x→a} f(x)/g(x) = lim_{x→a} f\'(x)/g\'(x), provided the latter limit exists.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Use L\'Hôpital\'s Rule to find lim_{x→0} (e^x − 1)/x.',
         'answer': '0/0 form. Differentiate top and bottom: lim e^x / 1 = e⁰ = 1.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 001B — Continuity & Exponential Functions
    # ------------------------------------------------------------------ #
    add_cards('Continuity & Exponential Functions', [
        {'question': 'Three conditions for f to be continuous at x = a.',
         'answer': '1. f(a) is defined. 2. lim_{x→a} f(x) exists. 3. lim_{x→a} f(x) = f(a).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a removable discontinuity?',
         'answer': 'The limit exists but either f(a) is undefined or f(a) ≠ lim_{x→a} f(x). The "hole" can be filled by redefining f(a).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a jump discontinuity?',
         'answer': 'The left-hand and right-hand limits both exist but are unequal. The function "jumps" from one value to another.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'State the Intermediate Value Theorem (IVT).',
         'answer': 'If f is continuous on [a, b] and k is any value between f(a) and f(b), then there exists c ∈ (a, b) such that f(c) = k.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the natural base e?',
         'answer': 'e = lim_{n→∞} (1 + 1/n)^n ≈ 2.71828. The unique base for which d/dx[eˣ] = eˣ.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is d/dx[eˣ]?',
         'answer': 'd/dx[eˣ] = eˣ. The exponential function is its own derivative.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is d/dx[e^(f(x))]? (chain rule)',
         'answer': "d/dx[e^(f(x))] = e^(f(x)) · f'(x).",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is d/dx[ln(x)]?',
         'answer': 'd/dx[ln(x)] = 1/x, for x > 0.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Solve for x: e^(2x) = 7.',
         'answer': 'Take ln of both sides: 2x = ln 7, so x = (ln 7)/2 ≈ 0.973.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'List four properties of e^x.',
         'answer': '1. e^(a+b) = eᵃ·eᵇ. 2. e^(a−b) = eᵃ/eᵇ. 3. (eᵃ)ᵇ = e^(ab). 4. e⁰ = 1. Domain: all reals; range: (0,∞).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Change of base formula for logarithms.',
         'answer': 'log_b(x) = ln(x)/ln(b). Example: log₁₀(100) = ln(100)/ln(10) = 2.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Differentiate f(x) = ln(x² + 1).',
         'answer': "f'(x) = 1/(x²+1) · 2x = 2x/(x²+1). Chain rule: derivative of outer × derivative of inner.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 002B — Curve Sketching & Optimisation
    # ------------------------------------------------------------------ #
    add_cards('Curve Sketching & Optimisation', [
        {'question': 'What is a critical point of f(x)?',
         'answer': "A point x = c where f'(c) = 0 or f'(c) is undefined. Critical points are candidates for local extrema.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'First Derivative Test for local extrema.',
         'answer': "At critical point c: if f' changes + to −, local max. If f' changes − to +, local min. If no sign change, neither.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Second Derivative Test for local extrema.',
         'answer': "At critical point c where f'(c) = 0: if f''(c) > 0, local min; if f''(c) < 0, local max; if f''(c) = 0, inconclusive.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What does f\'\'(x) > 0 tell you about the shape of f?',
         'answer': 'f is concave up (curves upward, like a cup). f\'\' < 0 means concave down (curves downward, like a cap).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is an inflection point?',
         'answer': 'A point where the concavity changes (from concave up to down, or vice versa). Occurs where f\'\'(x) = 0 and changes sign.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How do you find absolute (global) max/min on a closed interval [a, b]?',
         'answer': '1. Find all critical points in (a, b). 2. Evaluate f at critical points and endpoints a, b. 3. Largest value = global max; smallest = global min.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Find the critical points of f(x) = x³ − 3x.',
         'answer': "f'(x) = 3x² − 3 = 0 → x² = 1 → x = ±1. Critical points at x = −1 (local max) and x = 1 (local min).",
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Differentiate', 'detail': "f'(x) = 3x² − 3"},
                   {'move': 'Set equal to zero', 'detail': "3x² − 3 = 0 → x = ±1"},
                   {'move': 'Classify', 'detail': "f''(x) = 6x: f''(-1) = -6 < 0 (max), f''(1) = 6 > 0 (min)"}]},
        {'question': 'Optimisation setup: a rectangle has perimeter 20 m. Maximise its area.',
         'answer': 'Let width = x. Then length = 10 − x. Area A = x(10−x) = 10x − x². A\' = 10 − 2x = 0 → x = 5. A square with side 5 m gives max area 25 m².',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Variables', 'detail': 'Width x, length 10−x (perimeter: 2x+2(10−x)=20 ✓)'},
                   {'move': 'Objective', 'detail': 'A = x(10−x) = 10x − x²'},
                   {'move': 'Differentiate and solve', 'detail': "A' = 10 − 2x = 0 → x = 5"},
                   {'move': 'Verify maximum', 'detail': "A'' = −2 < 0 ✓, A(5) = 25 m²"}]},
        {'question': 'What is the relationship between the graphs of f, f\', and f\'\'?',
         'answer': "Where f' > 0: f is increasing. Where f' < 0: f is decreasing. Where f'' > 0: f is concave up. Where f'' < 0: f is concave down.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 003B — Applications of Integration
    # ------------------------------------------------------------------ #
    add_cards('Applications of Integration', [
        {'question': 'Formula for the area between curves y = f(x) and y = g(x) from x = a to x = b.',
         'answer': 'A = ∫_a^b |f(x) − g(x)| dx. If f(x) ≥ g(x) on [a,b]: A = ∫_a^b [f(x) − g(x)] dx.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Disk method: volume of solid of revolution about x-axis.',
         'answer': 'V = π ∫_a^b [f(x)]² dx. Slicing perpendicular to x-axis creates disks of radius f(x) and thickness dx.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Washer method: volume when rotating the region between f(x) ≥ g(x) ≥ 0 about the x-axis.',
         'answer': 'V = π ∫_a^b ([f(x)]² − [g(x)]²) dx. Each slice is a washer with outer radius f(x) and inner radius g(x).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Shell method: volume of solid from rotating y = f(x) about y-axis.',
         'answer': 'V = 2π ∫_a^b x·f(x) dx. Shell has radius x, height f(x), and thickness dx.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Average value of f(x) on [a, b].',
         'answer': 'f_avg = (1/(b−a)) ∫_a^b f(x) dx.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Arc length of y = f(x) from x = a to x = b.',
         'answer': 'L = ∫_a^b √(1 + [f\'(x)]²) dx.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the area enclosed by y = x² and y = x.',
         'answer': 'Intersect at x = 0, x = 1 (since x² = x → x = 0 or 1). A = ∫₀¹ (x − x²) dx = [x²/2 − x³/3]₀¹ = 1/2 − 1/3 = 1/6.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Find intersections', 'detail': 'x² = x → x(x−1) = 0 → x = 0, 1'},
                   {'move': 'Determine top curve', 'detail': 'x > x² on [0,1] (check x = 0.5: 0.5 > 0.25 ✓)'},
                   {'move': 'Integrate', 'detail': '∫₀¹ (x − x²) dx = [x²/2 − x³/3]₀¹ = 1/2 − 1/3 = 1/6'}]},
        {'question': 'Work done by a variable force F(x) moving an object from x = a to x = b.',
         'answer': 'W = ∫_a^b F(x) dx.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 004A — Complex Numbers  (critical for DSP, Control, Analog)
    # ------------------------------------------------------------------ #
    add_cards('Complex Numbers', [
        {'question': 'Define the imaginary unit j.',
         'answer': 'j = √(−1), so j² = −1. (Engineers use j; mathematicians use i.)',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Rectangular form of a complex number.',
         'answer': 'z = a + jb, where a = Re{z} (real part) and b = Im{z} (imaginary part). a, b ∈ ℝ.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Complex conjugate of z = a + jb.',
         'answer': 'z* = a − jb. Reflects across the real axis on the Argand diagram. z · z* = a² + b² = |z|².',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Modulus (magnitude) of z = a + jb.',
         'answer': '|z| = r = √(a² + b²). The distance from the origin to z on the Argand diagram.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Argument (phase angle) of z = a + jb.',
         'answer': 'arg(z) = θ = atan2(b, a) (four-quadrant inverse tangent). Units: radians or degrees. Notation: ∠z.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Convert z = 3 + 4j to polar form.',
         'answer': 'r = √(9 + 16) = 5. θ = arctan(4/3) ≈ 53.13° = 0.927 rad. Polar form: 5∠53.13° or 5e^(j·0.927).',
         'difficulty': 'easy', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Compute modulus', 'detail': 'r = √(3² + 4²) = √25 = 5'},
                   {'move': 'Compute argument', 'detail': 'θ = arctan(4/3) ≈ 53.13°'},
                   {'move': 'Write polar form', 'detail': 'z = 5∠53.13°'}]},
        {'question': 'State Euler\'s formula.',
         'answer': 'e^(jθ) = cos θ + j sin θ. Therefore: cos θ = Re{e^(jθ)} and sin θ = Im{e^(jθ)}.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Exponential (polar) form of z = a + jb.',
         'answer': 'z = r·e^(jθ), where r = |z| and θ = arg(z). Equivalent to z = r(cos θ + j sin θ).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Multiply two complex numbers in polar form: z₁ = r₁e^(jθ₁) and z₂ = r₂e^(jθ₂).',
         'answer': 'z₁·z₂ = r₁r₂ e^(j(θ₁+θ₂)) = r₁r₂∠(θ₁+θ₂). Magnitudes multiply; angles add.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Divide two complex numbers in polar form.',
         'answer': 'z₁/z₂ = (r₁/r₂) e^(j(θ₁−θ₂)) = (r₁/r₂)∠(θ₁−θ₂). Magnitudes divide; angles subtract.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Divide z₁ = 2 + j by z₂ = 1 + 2j in rectangular form.',
         'answer': 'Multiply by conjugate: (2+j)(1−2j)/((1+2j)(1−2j)) = (2−4j+j−2j²)/(1+4) = (2−3j+2)/5 = (4−3j)/5 = 0.8 − 0.6j.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Multiply numerator and denominator by conjugate of denominator', 'detail': 'Conjugate of (1+2j) is (1−2j)'},
                   {'move': 'Expand numerator', 'detail': '(2+j)(1−2j) = 2−4j+j−2j² = 2−3j+2 = 4−3j'},
                   {'move': 'Expand denominator', 'detail': '(1+2j)(1−2j) = 1+4 = 5'},
                   {'move': 'Simplify', 'detail': '(4−3j)/5 = 0.8 − 0.6j'}]},
        {'question': 'De Moivre\'s Theorem.',
         'answer': '(r e^(jθ))^n = r^n e^(jnθ), i.e. (r∠θ)^n = rⁿ∠(nθ). Used to compute powers of complex numbers.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the two square roots of j.',
         'answer': 'Write j = e^(jπ/2). Roots: e^(j·π/4) and e^(j·(π/4+π)) = e^(j·5π/4). i.e. (1+j)/√2 and −(1+j)/√2.',
         'difficulty': 'hard', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Express j in exponential form', 'detail': 'j = e^(jπ/2) = 1∠90°'},
                   {'move': 'Apply root formula', 'detail': 'Roots: e^(j(π/2 + 2πk)/2) for k = 0, 1'},
                   {'move': 'k=0', 'detail': 'e^(jπ/4) = cos45°+jsin45° = (1+j)/√2'},
                   {'move': 'k=1', 'detail': 'e^(j5π/4) = cos225°+jsin225° = −(1+j)/√2'}]},
        {'question': 'How does a complex number represent a sinusoidal signal (phasor)?',
         'answer': 'A cos(ωt+φ) = Re{A e^(jφ) e^(jωt)}. The phasor X = A e^(jφ) = A∠φ encodes amplitude A and phase φ, dropping the e^(jωt) carrier.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Express e^(jπ) in rectangular form.',
         'answer': "e^(jπ) = cos π + j sin π = −1 + 0j = −1. Euler's identity: e^(jπ) + 1 = 0.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the impedance of a capacitor C at frequency ω?',
         'answer': 'Z_C = 1/(jωC). In polar form: (1/ωC)∠−90°. The imaginary (negative) impedance means voltage lags current by 90°.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the impedance of an inductor L at frequency ω?',
         'answer': 'Z_L = jωL. In polar form: ωL∠90°. The imaginary (positive) impedance means voltage leads current by 90°.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 004B — Vectors in 2D & 3D
    # ------------------------------------------------------------------ #
    add_cards('Vectors in 2D & 3D', [
        {'question': 'Component form of a 3D vector from point A to point B.',
         'answer': 'AB⃗ = B − A = ⟨b₁−a₁, b₂−a₂, b₃−a₃⟩. Each component is the difference in that coordinate.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Magnitude of vector v = ⟨a, b, c⟩.',
         'answer': '|v| = √(a² + b² + c²).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Unit vector in direction of v.',
         'answer': 'v̂ = v / |v|. Has magnitude 1 and same direction as v.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Dot product definition and formula.',
         'answer': 'a · b = |a||b| cos θ = a₁b₁ + a₂b₂ + a₃b₃. Scalar result. Measures "how parallel" two vectors are.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'When are two non-zero vectors perpendicular?',
         'answer': 'When a · b = 0. cos 90° = 0, so the dot product is zero.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the angle between a = ⟨1, 0, 1⟩ and b = ⟨0, 1, 1⟩.',
         'answer': 'a · b = 0 + 0 + 1 = 1. |a| = |b| = √2. cos θ = 1/2 → θ = 60°.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Cross product a × b: direction and magnitude.',
         'answer': 'Direction: perpendicular to both a and b (right-hand rule). Magnitude: |a × b| = |a||b| sin θ = area of parallelogram spanned by a and b.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Cross product formula: a × b for a = ⟨a₁,a₂,a₃⟩ and b = ⟨b₁,b₂,b₃⟩.',
         'answer': 'a × b = ⟨a₂b₃−a₃b₂, a₃b₁−a₁b₃, a₁b₂−a₂b₁⟩. Can use the 3×3 determinant with î, ĵ, k̂.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Scalar projection of a onto b.',
         'answer': 'comp_b(a) = (a · b)/|b|. The signed length of the shadow of a in direction b.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Vector projection of a onto b.',
         'answer': 'proj_b(a) = ((a · b)/|b|²) b. The component of a in the direction of b as a vector.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 005B — Systems of Linear Equations
    # ------------------------------------------------------------------ #
    add_cards('Systems of Linear Equations', [
        {'question': 'What is an augmented matrix?',
         'answer': '[A | b] — the coefficient matrix A with the constant column b appended. Encodes the system Ax = b.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Three elementary row operations.',
         'answer': '1. Swap two rows (Rᵢ ↔ Rⱼ). 2. Multiply a row by a non-zero scalar (Rᵢ → cRᵢ). 3. Add a multiple of one row to another (Rᵢ → Rᵢ + cRⱼ).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is row echelon form (REF)?',
         'answer': 'Each row has a leading 1 (pivot) further right than the row above; rows of zeros are at bottom. Used as intermediate form for back substitution.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is reduced row echelon form (RREF)?',
         'answer': 'REF where each pivot is 1 and every other entry in the pivot column is 0. Gives the solution directly without back substitution.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Three possible solution types for a linear system.',
         'answer': '1. Unique solution (consistent, independent). 2. Infinitely many solutions (consistent, dependent — free variables). 3. No solution (inconsistent — contradictory equation like 0 = 1).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Solve using Gaussian elimination: x + y = 3, 2x − y = 0.',
         'answer': 'Augmented matrix: [1 1|3; 2 −1|0]. R₂ → R₂−2R₁: [1 1|3; 0 −3|−6]. Back sub: −3y = −6 → y = 2; x = 3−2 = 1. Solution: (1, 2).',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Write augmented matrix', 'detail': '[1 1 | 3; 2 −1 | 0]'},
                   {'move': 'Eliminate x from row 2', 'detail': 'R₂ → R₂ − 2R₁: [0 −3 | −6]'},
                   {'move': 'Back substitute', 'detail': 'y = 2, then x = 3 − 2 = 1'}]},
        {'question': 'What is a free variable?',
         'answer': 'A variable corresponding to a column without a pivot in RREF. It can take any value; basic (pivot) variables are expressed in terms of free variables.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Rank of a matrix: definition and role in solution existence.',
         'answer': 'Rank = number of pivot rows. System Ax = b is consistent iff rank(A) = rank([A|b]). Unique solution iff rank = number of unknowns.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0031_flashcards_dsp_extended'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_func),
    ]
