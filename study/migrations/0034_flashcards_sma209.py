from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return
    course = Course.objects.filter(name='Mathematics 2', created_by=system_user).first()
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
    # 001B — Second-Order ODEs (Homogeneous)
    # Critical prerequisite for Control Systems & Analog Electronics
    # ------------------------------------------------------------------ #
    add_cards('Second-Order ODEs (Homogeneous)', [
        {'question': 'General form of a linear second-order homogeneous ODE.',
         'answer': 'ay\'\' + by\' + cy = 0, where a, b, c are constants (a ≠ 0). The solution method uses the characteristic (auxiliary) equation.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Characteristic equation for ay\'\' + by\' + cy = 0.',
         'answer': 'Substitute y = eʳˣ: ar² + br + c = 0. The roots r₁, r₂ determine the form of the general solution.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'General solution when characteristic equation has two distinct real roots r₁ ≠ r₂.',
         'answer': 'y = C₁e^(r₁x) + C₂e^(r₂x). Both roots real and different → overdamped system.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'General solution when characteristic equation has a repeated real root r₁ = r₂ = r.',
         'answer': 'y = (C₁ + C₂x)e^(rx). The factor x prevents linear dependence — critically damped system.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'General solution when characteristic equation has complex conjugate roots r = α ± jβ.',
         'answer': 'y = e^(αx)(C₁cos(βx) + C₂sin(βx)). This is the underdamped oscillating solution.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Solve y\'\' − 5y\' + 6y = 0.',
         'answer': 'Characteristic equation: r² − 5r + 6 = 0 → (r−2)(r−3) = 0 → r = 2, 3. General solution: y = C₁e^(2x) + C₂e^(3x).',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Write characteristic equation', 'detail': 'r² − 5r + 6 = 0'},
                   {'move': 'Factor', 'detail': '(r−2)(r−3) = 0 → r = 2, r = 3'},
                   {'move': 'Write solution', 'detail': 'y = C₁e^(2x) + C₂e^(3x)'}]},
        {'question': 'Solve y\'\' + 4y\' + 4y = 0.',
         'answer': 'Characteristic: r² + 4r + 4 = (r+2)² = 0 → r = −2 (repeated). Solution: y = (C₁ + C₂x)e^(−2x).',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Characteristic equation', 'detail': 'r² + 4r + 4 = 0'},
                   {'move': 'Discriminant', 'detail': 'b²−4ac = 16−16 = 0 → repeated root r = −2'},
                   {'move': 'Write solution', 'detail': 'y = (C₁ + C₂x)e^(−2x)'}]},
        {'question': 'Solve y\'\' + 2y\' + 5y = 0.',
         'answer': 'Characteristic: r² + 2r + 5 = 0 → r = (−2 ± √(4−20))/2 = −1 ± 2j. Solution: y = e^(−x)(C₁cos(2x) + C₂sin(2x)).',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Characteristic equation', 'detail': 'r² + 2r + 5 = 0'},
                   {'move': 'Quadratic formula', 'detail': 'r = (−2 ± √(4−20))/2 = −1 ± j2'},
                   {'move': 'Write solution (α=−1, β=2)', 'detail': 'y = e^(−x)(C₁cos 2x + C₂sin 2x)'}]},
        {'question': 'Mass-spring-damper ODE: mẍ + bẋ + kx = 0. What are the three damping cases?',
         'answer': 'Discriminant Δ = b² − 4mk. Δ > 0: overdamped (two real roots, exponential decay). Δ = 0: critically damped (repeated root). Δ < 0: underdamped (oscillatory decay).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Natural frequency ωₙ and damping ratio ζ from mẍ + bẋ + kx = 0.',
         'answer': 'ωₙ = √(k/m) [rad/s]. ζ = b/(2√(mk)). Underdamped: 0 < ζ < 1. Critically damped: ζ = 1. Overdamped: ζ > 1.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Apply initial conditions to y\'\' − 5y\' + 6y = 0, y(0) = 1, y\'(0) = 0.',
         'answer': 'General: y = C₁e^(2x) + C₂e^(3x). y(0) = C₁+C₂ = 1. y\'(0) = 2C₁+3C₂ = 0. Solve: C₁ = 3, C₂ = −2.',
         'difficulty': 'hard', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'General solution', 'detail': 'y = C₁e^(2x) + C₂e^(3x)'},
                   {'move': 'Apply y(0)=1', 'detail': 'C₁ + C₂ = 1'},
                   {'move': "Apply y'(0)=0", 'detail': '2C₁ + 3C₂ = 0'},
                   {'move': 'Solve system', 'detail': 'C₁ = 3, C₂ = −2'}]},
    ])

    # ------------------------------------------------------------------ #
    # 002A — Second-Order ODEs (Non-Homogeneous)
    # ------------------------------------------------------------------ #
    add_cards('Second-Order ODEs (Non-Homogeneous)', [
        {'question': 'Structure of the general solution for ay\'\' + by\' + cy = g(x).',
         'answer': 'y = y_h + y_p, where y_h is the homogeneous solution (complementary function) and y_p is any particular solution.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Method of undetermined coefficients: what is the trial y_p for g(x) = Aeᵃˣ?',
         'answer': 'Try y_p = Keᵃˣ (where K is unknown). If eᵃˣ is a term in y_h, multiply by x (or x² for repeated).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Method of undetermined coefficients: trial y_p for g(x) = A cos(βx) + B sin(βx).',
         'answer': 'Try y_p = K cos(βx) + M sin(βx). If cos(βx) or sin(βx) appears in y_h (resonance), multiply by x.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Method of undetermined coefficients: trial y_p for g(x) = polynomial of degree n.',
         'answer': 'Try y_p = Aₙxⁿ + Aₙ₋₁xⁿ⁻¹ + … + A₁x + A₀. If c = 0 (no constant term in ODE), multiply by x.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Solve y\'\' − y\' − 2y = 6 (particular solution only).',
         'answer': 'g(x) = 6 is a constant. Try y_p = A. y_p\'\' = y_p\' = 0 → 0 − 0 − 2A = 6 → A = −3. So y_p = −3.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Solve y\'\' + 4y = sin(2x) — why does the standard trial fail?',
         'answer': 'Homogeneous solution y_h = C₁cos(2x) + C₂sin(2x). Since sin(2x) is already in y_h, this is resonance — standard trial gives 0. Multiply trial by x: y_p = x(A cos 2x + B sin 2x).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is variation of parameters?',
         'answer': 'General method for y_p when undetermined coefficients fails. Assumes y_p = u₁(x)y₁ + u₂(x)y₂ where y₁, y₂ form the homogeneous basis, and solves a system for u₁\', u₂\'.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Forced mass-spring-damper mẍ + bẋ + kx = F₀cos(ωt). What is the steady-state particular solution?',
         'answer': 'y_p = X cos(ωt − φ), where X = F₀/√((k−mω²)² + (bω)²) and φ = arctan(bω/(k−mω²)). This is forced harmonic oscillation.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is resonance in a forced ODE?',
         'answer': 'Occurs when forcing frequency ω = ωₙ (natural frequency). With no damping (b=0), amplitude grows without bound (x ∝ t sin(ωₙt)). Damping limits the peak amplitude.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 002B — Systems of ODEs
    # ------------------------------------------------------------------ #
    add_cards('Systems of ODEs', [
        {'question': 'Matrix form of a first-order linear ODE system.',
         'answer': "x' = Ax, where x = [x₁(t), x₂(t), …]ᵀ and A is the coefficient matrix. This is the state-space form in control engineering.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'General solution of x\' = Ax using eigenvalues.',
         'answer': 'x(t) = Σ cᵢ vᵢ e^(λᵢt), where (λᵢ, vᵢ) are the eigenpairs of A. Constants cᵢ from initial conditions x(0).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Solve x₁\' = x₁ + x₂, x₂\' = x₂, with x(0) = [1, 1]ᵀ.',
         'answer': 'A = [[1,1],[0,1]]. Eigenvalues: λ = 1 (double). Eigenvector: [1,0]. Solution: x(t) = e^t([1,0] + t[0,1]) (from generalized eigenvector). x₁(t) = (1+t)eᵗ, x₂(t) = eᵗ.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Stability of x\' = Ax: condition on eigenvalues.',
         'answer': 'Asymptotically stable iff all eigenvalues have negative real parts. Marginally stable if eigenvalues have non-positive real parts with no repeated imaginary-axis eigenvalues.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Convert second-order ODE y\'\' + by\' + cy = 0 to a first-order system.',
         'answer': 'Let x₁ = y, x₂ = y\'. Then x₁\' = x₂ and x₂\' = −cy − by\' = −cx₁ − bx₂. Matrix form: [x₁,x₂]\' = [[0,1],[−c,−b]][x₁,x₂].',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'State variables', 'detail': 'x₁ = y, x₂ = y\''},
                   {'move': "Write x₁' = x₂", 'detail': 'x₁\' = x₂'},
                   {'move': "Write x₂' from ODE", 'detail': "x₂' = y'' = −by' − cy = −bx₂ − cx₁"},
                   {'move': 'Matrix form', 'detail': "x' = [[0,1],[−c,−b]] x"}]},
        {'question': 'What is the matrix exponential e^(At)?',
         'answer': "e^(At) = I + At + (At)²/2! + (At)³/3! + … The solution to x' = Ax, x(0) = x₀ is x(t) = e^(At) x₀.",
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 003B — Fourier Transforms  (critical for DSP)
    # ------------------------------------------------------------------ #
    add_cards('Fourier Transforms', [
        {'question': 'Continuous Fourier Transform definition (frequency f convention).',
         'answer': 'X(f) = ∫_{−∞}^{∞} x(t) e^(−j2πft) dt. Decomposes x(t) into its complex sinusoidal components.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Inverse Fourier Transform.',
         'answer': 'x(t) = ∫_{−∞}^{∞} X(f) e^(j2πft) df. Reconstructs x(t) from its spectrum X(f).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Angular frequency (ω) form of the Fourier Transform.',
         'answer': 'X(ω) = ∫_{−∞}^{∞} x(t) e^(−jωt) dt, x(t) = (1/2π) ∫_{−∞}^{∞} X(ω) e^(jωt) dω. Note the 1/2π factor in the inverse.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform: Linearity property.',
         'answer': 'FT{ax(t) + by(t)} = aX(f) + bY(f). The FT is a linear operator.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform: Time-shift property.',
         'answer': 'FT{x(t − t₀)} = X(f) e^(−j2πft₀). A time delay multiplies the spectrum by a linear phase factor.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform: Frequency-shift (modulation) property.',
         'answer': 'FT{x(t) e^(j2πf₀t)} = X(f − f₀). Multiplying by a complex exponential shifts the spectrum.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform: Convolution Theorem.',
         'answer': 'FT{x(t) * h(t)} = X(f) · H(f). Convolution in time ↔ multiplication in frequency. Key for LTI system analysis.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Parseval\'s Theorem (energy in time = energy in frequency).',
         'answer': '∫_{−∞}^{∞} |x(t)|² dt = ∫_{−∞}^{∞} |X(f)|² df. Energy is preserved by the Fourier Transform.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform of the Dirac delta: FT{δ(t)}.',
         'answer': 'FT{δ(t)} = 1. Constant spectrum — the impulse contains all frequencies equally.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform of δ(t − t₀).',
         'answer': 'FT{δ(t−t₀)} = e^(−j2πft₀). Modulus 1, phase linearly decreasing with f.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform of a rectangular pulse: rect(t/τ).',
         'answer': 'FT{rect(t/τ)} = τ sinc(fτ), where sinc(x) = sin(πx)/(πx). Wider pulse in time → narrower sinc in frequency (time-bandwidth product).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Relationship between Fourier Transform and Fourier Series.',
         'answer': 'A periodic signal x_T(t) with period T has Fourier Series coefficients cₙ = (1/T) X(f) at f = n/T, where X(f) is the FT of one period. The spectrum is a line spectrum with spacing 1/T.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform: Time-scaling property.',
         'answer': 'FT{x(at)} = (1/|a|) X(f/a). Compressing in time (a>1) stretches the spectrum; stretching in time compresses the spectrum.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'FT differentiation property: FT{dx/dt}.',
         'answer': 'FT{x\'(t)} = j2πf · X(f). Each differentiation in time multiplies by j2πf in frequency.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 004B — Laplace Transforms — Applications  (critical for Control)
    # ------------------------------------------------------------------ #
    add_cards('Laplace Transforms — Applications', [
        {'question': 'Procedure for solving an IVP with Laplace Transforms.',
         'answer': '1. Take L of both sides of the ODE. 2. Apply initial conditions to eliminate integration constants. 3. Solve algebraically for Y(s). 4. Take inverse Laplace (partial fractions + tables) to get y(t).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'L{y\'(t)} in terms of Y(s) and initial conditions.',
         'answer': 'L{y\'} = sY(s) − y(0). L{y\'\'} = s²Y(s) − sy(0) − y\'(0).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Solve y\' + 2y = 0, y(0) = 3 using Laplace Transforms.',
         'answer': 'L: sY − 3 + 2Y = 0 → Y(s+2) = 3 → Y = 3/(s+2). Inverse: y(t) = 3e^(−2t).',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Take Laplace', 'detail': 'sY(s) − y(0) + 2Y(s) = 0'},
                   {'move': 'Apply IC y(0)=3', 'detail': '(s+2)Y = 3 → Y = 3/(s+2)'},
                   {'move': 'Inverse Laplace', 'detail': 'y(t) = 3e^(−2t)'}]},
        {'question': 'Solve y\'\' + 4y = 0, y(0) = 1, y\'(0) = 0 using Laplace.',
         'answer': 'L: s²Y − s + 4Y = 0 → Y(s²+4) = s → Y = s/(s²+4). Inverse: y(t) = cos(2t).',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Take Laplace', 'detail': 's²Y − sy(0) − y\'(0) + 4Y = 0'},
                   {'move': 'Apply ICs', 'detail': '(s²+4)Y = s → Y = s/(s²+4)'},
                   {'move': 'Inverse Laplace', 'detail': 'L⁻¹{s/(s²+4)} = cos(2t)'}]},
        {'question': 'Unit step function u(t − a): definition and Laplace Transform.',
         'answer': 'u(t−a) = 0 for t < a, 1 for t ≥ a. L{u(t−a)} = e^(−as)/s. Used to model signals that switch on at t = a.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Second Shifting Theorem (t-shifting).',
         'answer': 'L{f(t−a)u(t−a)} = e^(−as) F(s). A time-delayed signal is multiplied by e^(−as) in the s-domain.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Convolution Theorem for Laplace Transforms.',
         'answer': 'L{f * g}(t) = F(s)·G(s), where (f*g)(t) = ∫₀ᵗ f(τ)g(t−τ) dτ. The output y(t) = h(t)*u(t) where H(s) = Y(s)/U(s) is the transfer function.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Final Value Theorem.',
         'answer': 'lim_{t→∞} f(t) = lim_{s→0} sF(s), provided all poles of sF(s) are in the left half-plane. Used to find steady-state output.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Initial Value Theorem.',
         'answer': 'lim_{t→0⁺} f(t) = lim_{s→∞} sF(s). Gives the initial value from the transform without inverting.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Partial fraction decomposition for Y(s) = 1/((s+1)(s+3)).',
         'answer': 'Y = A/(s+1) + B/(s+3). A = [1/(s+3)]_{s=−1} = 1/2. B = [1/(s+1)]_{s=−3} = −1/2. y(t) = (1/2)e^(−t) − (1/2)e^(−3t).',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Set up partial fractions', 'detail': 'A/(s+1) + B/(s+3)'},
                   {'move': 'Cover-up method for A', 'detail': 'A = 1/(s+3)|_{s=−1} = 1/2'},
                   {'move': 'Cover-up method for B', 'detail': 'B = 1/(s+1)|_{s=−3} = −1/2'},
                   {'move': 'Inverse Laplace', 'detail': 'y(t) = (e^(−t) − e^(−3t))/2'}]},
        {'question': 'Partial fractions with complex conjugate poles: Y(s) = 1/(s²+2s+5).',
         'answer': 'Complete the square: s²+2s+5 = (s+1)²+4. L⁻¹{1/((s+1)²+4)} = (1/2)e^(−t)sin(2t).',
         'difficulty': 'hard', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Complete the square', 'detail': 's²+2s+5 = (s+1)²+2²'},
                   {'move': 'Match standard form', 'detail': '1/((s+1)²+4) = (1/2) · 2/((s+1)²+4)'},
                   {'move': 'Inverse Laplace', 'detail': 'y(t) = (1/2)e^(−t)sin(2t)'}]},
        {'question': 'Connection between Laplace Transforms and transfer functions in control.',
         'answer': 'Transfer function G(s) = Y(s)/U(s) (zero initial conditions). Poles of G(s) = eigenvalues of A (state matrix). LHP poles → stable; RHP poles → unstable.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0033_flashcards_sma102'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_func),
    ]
