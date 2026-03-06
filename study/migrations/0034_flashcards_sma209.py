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
         'answer': "$ay'' + by' + cy = 0$, where $a, b, c$ are constants ($a \\ne 0$). The solution method uses the characteristic (auxiliary) equation.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': "Characteristic equation for $ay'' + by' + cy = 0$.",
         'answer': 'Substitute $y = e^{rx}$: $ar^2 + br + c = 0$. The roots $r_1, r_2$ determine the form of the general solution.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'General solution when characteristic equation has two distinct real roots $r_1 \\ne r_2$.',
         'answer': '$y = C_1 e^{r_1 x} + C_2 e^{r_2 x}$. Both roots real and different $\\Rightarrow$ overdamped system.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'General solution when characteristic equation has a repeated real root $r_1 = r_2 = r$.',
         'answer': '$y = (C_1 + C_2 x)e^{rx}$. The factor $x$ prevents linear dependence — critically damped system.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'General solution when characteristic equation has complex conjugate roots $r = \\alpha \\pm j\\beta$.',
         'answer': '$y = e^{\\alpha x}(C_1\\cos\\beta x + C_2\\sin\\beta x)$. This is the underdamped oscillating solution.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Solve $y'' - 5y' + 6y = 0$.",
         'answer': 'Characteristic: $r^2 - 5r + 6 = 0 \\Rightarrow (r-2)(r-3) = 0 \\Rightarrow r = 2, 3$. General solution: $y = C_1 e^{2x} + C_2 e^{3x}$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Write characteristic equation', 'detail': '$r^2 - 5r + 6 = 0$'},
                   {'move': 'Factor', 'detail': '$(r-2)(r-3) = 0 \\Rightarrow r = 2, r = 3$'},
                   {'move': 'Write solution', 'detail': '$y = C_1 e^{2x} + C_2 e^{3x}$'}]},
        {"question": "Solve $y'' + 4y' + 4y = 0$.",
         'answer': 'Characteristic: $r^2 + 4r + 4 = (r+2)^2 = 0 \\Rightarrow r = -2$ (repeated). Solution: $y = (C_1 + C_2 x)e^{-2x}$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Characteristic equation', 'detail': '$r^2 + 4r + 4 = 0$'},
                   {'move': 'Discriminant', 'detail': '$b^2-4ac = 16-16 = 0 \\Rightarrow$ repeated root $r = -2$'},
                   {'move': 'Write solution', 'detail': '$y = (C_1 + C_2 x)e^{-2x}$'}]},
        {"question": "Solve $y'' + 2y' + 5y = 0$.",
         'answer': 'Characteristic: $r^2 + 2r + 5 = 0 \\Rightarrow r = \\dfrac{-2 \\pm \\sqrt{4-20}}{2} = -1 \\pm 2j$. Solution: $y = e^{-x}(C_1\\cos 2x + C_2\\sin 2x)$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Characteristic equation', 'detail': '$r^2 + 2r + 5 = 0$'},
                   {'move': 'Quadratic formula', 'detail': '$r = \\dfrac{-2 \\pm \\sqrt{4-20}}{2} = -1 \\pm 2j$'},
                   {'move': 'Write solution ($\\alpha=-1$, $\\beta=2$)', 'detail': '$y = e^{-x}(C_1\\cos 2x + C_2\\sin 2x)$'}]},
        {'question': 'Mass-spring-damper ODE: $m\\ddot{x} + b\\dot{x} + kx = 0$. What are the three damping cases?',
         'answer': 'Discriminant $\\Delta = b^2 - 4mk$. $\\Delta > 0$: overdamped (exponential decay). $\\Delta = 0$: critically damped. $\\Delta < 0$: underdamped (oscillatory decay).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Natural frequency $\\omega_n$ and damping ratio $\\zeta$ from $m\\ddot{x} + b\\dot{x} + kx = 0$.',
         'answer': '$\\omega_n = \\sqrt{k/m}$ rad/s. $\\zeta = \\dfrac{b}{2\\sqrt{mk}}$. Underdamped: $0 < \\zeta < 1$. Critically damped: $\\zeta = 1$. Overdamped: $\\zeta > 1$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Apply initial conditions to $y'' - 5y' + 6y = 0$, $y(0) = 1$, $y'(0) = 0$.",
         'answer': 'General: $y = C_1 e^{2x} + C_2 e^{3x}$. $y(0) = C_1+C_2 = 1$. $y\'(0) = 2C_1+3C_2 = 0$. Solve: $C_1 = 3$, $C_2 = -2$.',
         'difficulty': 'hard', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'General solution', 'detail': '$y = C_1 e^{2x} + C_2 e^{3x}$'},
                   {'move': 'Apply $y(0)=1$', 'detail': '$C_1 + C_2 = 1$'},
                   {'move': "Apply $y'(0)=0$", 'detail': '$2C_1 + 3C_2 = 0$'},
                   {'move': 'Solve system', 'detail': '$C_1 = 3$, $C_2 = -2$'}]},
    ])

    # ------------------------------------------------------------------ #
    # 002A — Second-Order ODEs (Non-Homogeneous)
    # ------------------------------------------------------------------ #
    add_cards('Second-Order ODEs (Non-Homogeneous)', [
        {"question": "Structure of the general solution for $ay'' + by' + cy = g(x)$.",
         'answer': '$y = y_h + y_p$, where $y_h$ is the homogeneous solution (complementary function) and $y_p$ is any particular solution.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Method of undetermined coefficients: trial $y_p$ for $g(x) = Ae^{ax}$.',
         'answer': 'Try $y_p = Ke^{ax}$ (where $K$ is unknown). If $e^{ax}$ is already in $y_h$, multiply by $x$ (or $x^2$ for repeated).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Method of undetermined coefficients: trial $y_p$ for $g(x) = A\\cos(\\beta x) + B\\sin(\\beta x)$.',
         'answer': 'Try $y_p = K\\cos(\\beta x) + M\\sin(\\beta x)$. If $\\cos(\\beta x)$ or $\\sin(\\beta x)$ appears in $y_h$ (resonance), multiply by $x$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Method of undetermined coefficients: trial $y_p$ for $g(x)$ = polynomial of degree $n$.',
         'answer': 'Try $y_p = A_n x^n + A_{n-1}x^{n-1} + \\cdots + A_1 x + A_0$. If $c = 0$ in the ODE, multiply by $x$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Solve $y'' - y' - 2y = 6$ (particular solution only).",
         'answer': "$g(x) = 6$ is constant. Try $y_p = A$. $y_p'' = y_p' = 0 \\Rightarrow -2A = 6 \\Rightarrow A = -3$. So $y_p = -3$.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Solve $y'' + 4y = \\sin(2x)$ — why does the standard trial fail?",
         'answer': 'Homogeneous solution $y_h = C_1\\cos(2x) + C_2\\sin(2x)$. Since $\\sin(2x)$ is already in $y_h$ (resonance), the standard trial gives 0. Multiply by $x$: $y_p = x(A\\cos 2x + B\\sin 2x)$.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is variation of parameters?',
         'answer': "General method for $y_p$ when undetermined coefficients fails. Assumes $y_p = u_1(x)y_1 + u_2(x)y_2$ where $y_1, y_2$ form the homogeneous basis, and solves a system for $u_1', u_2'$.",
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Forced mass-spring-damper: $m\\ddot{x} + b\\dot{x} + kx = F_0\\cos(\\omega t)$. Steady-state particular solution?',
         'answer': '$y_p = X\\cos(\\omega t - \\phi)$, where $X = \\dfrac{F_0}{\\sqrt{(k-m\\omega^2)^2 + (b\\omega)^2}}$ and $\\phi = \\arctan\\dfrac{b\\omega}{k-m\\omega^2}$.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is resonance in a forced ODE?',
         'answer': 'Occurs when forcing frequency $\\omega = \\omega_n$ (natural frequency). With no damping, amplitude grows without bound ($x \\propto t\\sin(\\omega_n t)$). Damping limits the peak amplitude.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 002B — Systems of ODEs
    # ------------------------------------------------------------------ #
    add_cards('Systems of ODEs', [
        {'question': 'Matrix form of a first-order linear ODE system.',
         'answer': "$\\mathbf{x}' = A\\mathbf{x}$, where $\\mathbf{x} = [x_1(t),\\, x_2(t),\\, \\ldots]^T$ and $A$ is the coefficient matrix. This is the state-space form in control engineering.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {"question": "General solution of $\\mathbf{x}' = A\\mathbf{x}$ using eigenvalues.",
         'answer': '$\\mathbf{x}(t) = \\sum_i c_i \\mathbf{v}_i e^{\\lambda_i t}$, where $(\\lambda_i, \\mathbf{v}_i)$ are the eigenpairs of $A$. Constants $c_i$ from initial conditions $\\mathbf{x}(0)$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Solve $x_1' = x_1 + x_2$, $x_2' = x_2$, with $\\mathbf{x}(0) = [1,\\,1]^T$.",
         'answer': '$A = \\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}$, eigenvalue $\\lambda = 1$ (double), eigenvector $\\mathbf{v} = [1,0]^T$. Using the generalised eigenvector $\\mathbf{w} = [0,1]^T$: $\\mathbf{x}(t) = e^t[1+t,\\, 1]^T$, so $x_1(t) = (1+t)e^t$, $x_2(t) = e^t$.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Stability of $\\mathbf{x}' = A\\mathbf{x}$: condition on eigenvalues.",
         'answer': 'Asymptotically stable iff all eigenvalues have negative real parts ($\\operatorname{Re}(\\lambda_i) < 0$ for all $i$). Marginally stable if non-positive with no repeated imaginary-axis eigenvalues.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Convert $y'' + by' + cy = 0$ to a first-order system.",
         'answer': "Let $x_1 = y$, $x_2 = y'$. Then $x_1' = x_2$ and $x_2' = -cx_1 - bx_2$. Matrix form: $\\mathbf{x}' = \\begin{pmatrix}0&1\\\\-c&-b\\end{pmatrix}\\mathbf{x}$.",
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'State variables', 'detail': '$x_1 = y$, $x_2 = y\'$'},
                   {'move': "Write $x_1' = x_2$", 'detail': '$x_1\' = x_2$'},
                   {'move': "Write $x_2'$ from ODE", 'detail': "$x_2' = y'' = -by' - cy = -bx_2 - cx_1$"},
                   {'move': 'Matrix form', 'detail': "$\\mathbf{x}' = \\begin{pmatrix}0&1\\\\-c&-b\\end{pmatrix}\\mathbf{x}$"}]},
        {"question": "What is the matrix exponential $e^{At}$?",
         'answer': "$e^{At} = I + At + \\dfrac{(At)^2}{2!} + \\dfrac{(At)^3}{3!} + \\cdots$. The solution to $\\mathbf{x}' = A\\mathbf{x}$, $\\mathbf{x}(0) = \\mathbf{x}_0$ is $\\mathbf{x}(t) = e^{At}\\mathbf{x}_0$.",
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 003B — Fourier Transforms  (critical for DSP)
    # ------------------------------------------------------------------ #
    add_cards('Fourier Transforms', [
        {'question': 'Continuous Fourier Transform definition (frequency $f$ convention).',
         'answer': r'$X(f) = \int_{-\infty}^{\infty} x(t)\, e^{-j 2\pi f t}\, dt$. Decomposes $x(t)$ into its complex sinusoidal components.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Inverse Fourier Transform.',
         'answer': r'$x(t) = \int_{-\infty}^{\infty} X(f)\, e^{j 2\pi f t}\, df$. Reconstructs $x(t)$ from its spectrum $X(f)$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Angular frequency ($\\omega$) form of the Fourier Transform.',
         'answer': r'$X(\omega) = \int_{-\infty}^{\infty} x(t)\, e^{-j\omega t}\, dt$, $\quad x(t) = \dfrac{1}{2\pi}\int_{-\infty}^{\infty} X(\omega)\, e^{j\omega t}\, d\omega$. Note the $1/(2\pi)$ factor in the inverse.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform: Linearity property.',
         'answer': r'$\mathcal{F}\{ax(t) + by(t)\} = aX(f) + bY(f)$. The FT is a linear operator.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform: Time-shift property.',
         'answer': r'$\mathcal{F}\{x(t - t_0)\} = X(f)\, e^{-j 2\pi f t_0}$. A time delay multiplies the spectrum by a linear phase factor.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform: Frequency-shift (modulation) property.',
         'answer': r'$\mathcal{F}\{x(t)\, e^{j 2\pi f_0 t}\} = X(f - f_0)$. Multiplying by a complex exponential shifts the spectrum.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform: Convolution Theorem.',
         'answer': r'$\mathcal{F}\{x(t) * h(t)\} = X(f)\, H(f)$. Convolution in time $\leftrightarrow$ multiplication in frequency. Key for LTI system analysis.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Parseval's Theorem (energy preservation).",
         'answer': r'$\int_{-\infty}^{\infty} |x(t)|^2\, dt = \int_{-\infty}^{\infty} |X(f)|^2\, df$. Energy is preserved by the Fourier Transform.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform of the Dirac delta: $\\mathcal{F}\\{\\delta(t)\\}$.',
         'answer': r'$\mathcal{F}\{\delta(t)\} = 1$. Constant spectrum — the impulse contains all frequencies equally.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform of $\\delta(t - t_0)$.',
         'answer': r'$\mathcal{F}\{\delta(t - t_0)\} = e^{-j 2\pi f t_0}$. Modulus $1$, phase linearly decreasing with $f$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform of a rectangular pulse $\\operatorname{rect}(t/\\tau)$.',
         'answer': r'$\mathcal{F}\{\operatorname{rect}(t/\tau)\} = \tau\, \operatorname{sinc}(f\tau)$, where $\operatorname{sinc}(x) = \dfrac{\sin(\pi x)}{\pi x}$. Wider pulse $\leftrightarrow$ narrower sinc (time-bandwidth product).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Relationship between the Fourier Transform and Fourier Series.',
         'answer': 'A periodic signal with period $T$ has Fourier Series coefficients $c_n = \\dfrac{1}{T} X(f)$ evaluated at $f = n/T$, where $X(f)$ is the FT of one period. The spectrum is a line spectrum with spacing $1/T$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Fourier Transform: Time-scaling property.',
         'answer': r'$\mathcal{F}\{x(at)\} = \dfrac{1}{|a|} X(f/a)$. Compressing in time ($a>1$) stretches the spectrum; stretching compresses the spectrum.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'FT differentiation property: $\\mathcal{F}\\{x\'(t)\\}$.',
         'answer': r'$\mathcal{F}\{x\'(t)\} = j 2\pi f\, X(f)$. Each differentiation in time multiplies by $j 2\pi f$ in frequency.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 004B — Laplace Transforms — Applications  (critical for Control)
    # ------------------------------------------------------------------ #
    add_cards('Laplace Transforms \u2014 Applications', [
        {'question': 'Procedure for solving an IVP with Laplace Transforms.',
         'answer': '1. Take $\\mathcal{L}$ of both sides of the ODE. 2. Apply initial conditions. 3. Solve algebraically for $Y(s)$. 4. Take inverse Laplace (partial fractions + tables) to get $y(t)$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "$\\mathcal{L}\\{y'(t)\\}$ in terms of $Y(s)$ and initial conditions.",
         'answer': "$\\mathcal{L}\\{y'\\} = sY(s) - y(0)$. $\\mathcal{L}\\{y''\\} = s^2 Y(s) - sy(0) - y'(0)$.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Solve $y' + 2y = 0$, $y(0) = 3$ using Laplace Transforms.",
         'answer': '$\\mathcal{L}$: $sY - 3 + 2Y = 0 \\Rightarrow (s+2)Y = 3 \\Rightarrow Y = \\dfrac{3}{s+2}$. Inverse: $y(t) = 3e^{-2t}$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Take Laplace', 'detail': '$sY(s) - y(0) + 2Y(s) = 0$'},
                   {'move': 'Apply IC $y(0)=3$', 'detail': '$(s+2)Y = 3 \\Rightarrow Y = \\dfrac{3}{s+2}$'},
                   {'move': 'Inverse Laplace', 'detail': '$y(t) = 3e^{-2t}$'}]},
        {"question": "Solve $y'' + 4y = 0$, $y(0) = 1$, $y'(0) = 0$ using Laplace.",
         'answer': '$\\mathcal{L}$: $s^2 Y - s + 4Y = 0 \\Rightarrow Y(s^2+4) = s \\Rightarrow Y = \\dfrac{s}{s^2+4}$. Inverse: $y(t) = \\cos(2t)$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Take Laplace', 'detail': "$s^2 Y - sy(0) - y'(0) + 4Y = 0$"},
                   {'move': 'Apply ICs', 'detail': '$(s^2+4)Y = s \\Rightarrow Y = \\dfrac{s}{s^2+4}$'},
                   {'move': 'Inverse Laplace', 'detail': '$\\mathcal{L}^{-1}\\{s/(s^2+4)\\} = \\cos(2t)$'}]},
        {'question': 'Unit step function $u(t-a)$: definition and Laplace Transform.',
         'answer': '$u(t-a) = 0$ for $t < a$, $1$ for $t \\ge a$. $\\mathcal{L}\\{u(t-a)\\} = \\dfrac{e^{-as}}{s}$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Second Shifting Theorem ($t$-shifting).',
         'answer': '$\\mathcal{L}\\{f(t-a)\\, u(t-a)\\} = e^{-as} F(s)$. A time-delayed signal is multiplied by $e^{-as}$ in the $s$-domain.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Convolution Theorem for Laplace Transforms.',
         'answer': '$\\mathcal{L}\\{(f*g)(t)\\} = F(s) G(s)$, where $(f*g)(t) = \\int_0^t f(\\tau)g(t-\\tau)\\, d\\tau$. The output $y(t) = h(t)*u(t)$ where $H(s) = Y(s)/U(s)$ is the transfer function.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Final Value Theorem.',
         'answer': '$\\lim_{t \\to \\infty} f(t) = \\lim_{s \\to 0} sF(s)$, provided all poles of $sF(s)$ are in the left half-plane. Used to find steady-state output.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Initial Value Theorem.',
         'answer': '$\\lim_{t \\to 0^+} f(t) = \\lim_{s \\to \\infty} sF(s)$. Gives the initial value from the transform without inverting.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Partial fraction decomposition for $Y(s) = \\dfrac{1}{(s+1)(s+3)}$.',
         'answer': '$Y = \\dfrac{A}{s+1} + \\dfrac{B}{s+3}$. $A = \\dfrac{1}{s+3}\\big|_{s=-1} = \\dfrac{1}{2}$. $B = \\dfrac{1}{s+1}\\big|_{s=-3} = -\\dfrac{1}{2}$. $y(t) = \\dfrac{1}{2}(e^{-t} - e^{-3t})$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Set up partial fractions', 'detail': '$\\dfrac{A}{s+1} + \\dfrac{B}{s+3}$'},
                   {'move': 'Cover-up for $A$', 'detail': '$A = \\dfrac{1}{s+3}\\big|_{s=-1} = \\dfrac{1}{2}$'},
                   {'move': 'Cover-up for $B$', 'detail': '$B = \\dfrac{1}{s+1}\\big|_{s=-3} = -\\dfrac{1}{2}$'},
                   {'move': 'Inverse Laplace', 'detail': '$y(t) = \\dfrac{1}{2}(e^{-t} - e^{-3t})$'}]},
        {'question': 'Partial fractions with complex poles: $Y(s) = \\dfrac{1}{s^2+2s+5}$.',
         'answer': 'Complete the square: $s^2+2s+5 = (s+1)^2+4$. Then $\\mathcal{L}^{-1}\\left\\{\\dfrac{1}{(s+1)^2+4}\\right\\} = \\dfrac{1}{2}e^{-t}\\sin(2t)$.',
         'difficulty': 'hard', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Complete the square', 'detail': '$s^2+2s+5 = (s+1)^2+2^2$'},
                   {'move': 'Match standard form', 'detail': '$\\dfrac{1}{(s+1)^2+4} = \\dfrac{1}{2} \\cdot \\dfrac{2}{(s+1)^2+4}$'},
                   {'move': 'Inverse Laplace', 'detail': '$y(t) = \\dfrac{1}{2}e^{-t}\\sin(2t)$'}]},
        {'question': 'Connection between Laplace Transforms and transfer functions in control.',
         'answer': 'Transfer function $G(s) = Y(s)/U(s)$ (zero initial conditions). Poles of $G(s)$ = eigenvalues of $A$ (state matrix). Left-half-plane poles $\\Rightarrow$ stable; right-half-plane poles $\\Rightarrow$ unstable.',
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
