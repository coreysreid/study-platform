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
         'answer': '$\\int u\\, dv = uv - \\int v\\, du$. Choose $u$ to differentiate (becomes simpler) and $dv$ to integrate.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'LIATE rule for choosing $u$ in integration by parts.',
         'answer': 'Preference order: Logarithm, Inverse trig, Algebraic, Trig, Exponential. Choose $u$ from the earliest category present.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Evaluate $\\int x e^x\\, dx$ using integration by parts.',
         'answer': '$u = x$, $dv = e^x\\, dx$ $\\Rightarrow$ $du = dx$, $v = e^x$. Result: $x e^x - e^x + C = e^x(x-1) + C$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Choose $u$ and $dv$', 'detail': '$u = x$ (algebraic), $dv = e^x\\, dx$'},
                   {'move': 'Differentiate $u$ and integrate $dv$', 'detail': '$du = dx$, $v = e^x$'},
                   {'move': 'Apply formula', 'detail': '$\\int x e^x\\, dx = x e^x - \\int e^x\\, dx = e^x(x-1) + C$'}]},
        {'question': 'Partial fractions: decompose $\\dfrac{2x+1}{(x+1)(x-2)}$.',
         'answer': 'Write $\\dfrac{A}{x+1} + \\dfrac{B}{x-2}$. Multiply: $2x+1 = A(x-2)+B(x+1)$. $x=2$: $B=\\tfrac{5}{3}$. $x=-1$: $A=\\tfrac{1}{3}$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Set up decomposition', 'detail': '$\\dfrac{2x+1}{(x+1)(x-2)} = \\dfrac{A}{x+1} + \\dfrac{B}{x-2}$'},
                   {'move': 'Multiply by denominator', 'detail': '$2x+1 = A(x-2) + B(x+1)$'},
                   {'move': 'Substitute roots', 'detail': '$x=2 \\Rightarrow B=5/3$; $x=-1 \\Rightarrow A=1/3$'}]},
        {'question': 'Partial fractions for a repeated factor: decompose $\\dfrac{1}{(x-1)^2}$.',
         'answer': 'Write $\\dfrac{A}{x-1} + \\dfrac{B}{(x-1)^2}$. Each power of the repeated factor gets its own term.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Trigonometric substitution for $\\sqrt{a^2 - x^2}$.',
         'answer': 'Substitute $x = a\\sin\\theta$. Then $\\sqrt{a^2-x^2} = a\\cos\\theta$. Useful for $\\int\\sqrt{1-x^2}\\, dx$ and similar.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Trigonometric substitution for $\\sqrt{x^2 + a^2}$.',
         'answer': 'Substitute $x = a\\tan\\theta$. Then $\\sqrt{x^2+a^2} = a\\sec\\theta$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Improper integral $\\int_1^\\infty \\dfrac{1}{x^p}\\, dx$: when does it converge?',
         'answer': 'Converges when $p > 1$; value $= \\dfrac{1}{p-1}$. Diverges when $p \\le 1$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Evaluate $\\int_0^\\infty e^{-x}\\, dx$.',
         'answer': '$\\lim_{b \\to \\infty} \\left[-e^{-x}\\right]_0^b = \\lim_{b \\to \\infty}(1 - e^{-b}) = 1$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 001B — Volumes, Surface Areas & Applications
    # ------------------------------------------------------------------ #
    add_cards('Volumes, Surface Areas & Applications', [
        {'question': 'Disk method: volume of revolution about the $x$-axis.',
         'answer': '$V = \\pi \\int_a^b [R(x)]^2\\, dx$, where $R(x)$ is the radius (distance from $x$-axis to curve).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Washer method: volume when rotating region between $f(x)$ and $g(x)$ ($f \\ge g \\ge 0$) about $x$-axis.',
         'answer': '$V = \\pi \\int_a^b \\left([f(x)]^2 - [g(x)]^2\\right) dx$. Outer radius $R = f(x)$, inner radius $r = g(x)$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Shell method: volume from rotating $y = f(x) \\ge 0$ on $[a,b]$ about the $y$-axis.',
         'answer': '$V = 2\\pi \\int_a^b x\\, f(x)\\, dx$. Each shell has circumference $2\\pi x$, height $f(x)$, thickness $dx$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Surface area of revolution: rotate $y = f(x)$ on $[a,b]$ about the $x$-axis.',
         'answer': "$SA = 2\\pi \\int_a^b f(x)\\sqrt{1 + [f'(x)]^2}\\, dx$.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the volume of a sphere of radius $R$ using the disk method.',
         'answer': "Rotate $y = \\sqrt{R^2-x^2}$ about $x$-axis. $V = \\pi \\int_{-R}^R (R^2-x^2)\\, dx = \\pi\\left[R^2 x - \\dfrac{x^3}{3}\\right]_{-R}^R = \\dfrac{4}{3}\\pi R^3$.",
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Set up integral', 'detail': '$V = \\pi \\int_{-R}^R (R^2-x^2)\\, dx$'},
                   {'move': 'Integrate', 'detail': '$\\pi\\left[R^2 x - x^3/3\\right]_{-R}^R$'},
                   {'move': 'Evaluate', 'detail': '$\\pi\\left[(R^3 - R^3/3) - (-R^3 + R^3/3)\\right] = \\dfrac{4}{3}\\pi R^3$ ✓'}]},
    ])

    # ------------------------------------------------------------------ #
    # 002A — Numerical Methods
    # ------------------------------------------------------------------ #
    add_cards('Numerical Methods', [
        {'question': 'Newton-Raphson iteration formula.',
         'answer': "$x_{n+1} = x_n - \\dfrac{f(x_n)}{f'(x_n)}$. Starting from initial guess $x_0$, converges quadratically near a simple root.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'One Newton-Raphson step for $f(x) = x^2 - 2$ starting at $x_0 = 1$.',
         'answer': "$f(1) = -1$, $f'(1) = 2$. $x_1 = 1 - \\dfrac{-1}{2} = 1.5$. (Approximating $\\sqrt{2} \\approx 1.414$.)",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Bisection method: when does it apply?',
         'answer': 'When $f$ is continuous on $[a,b]$ and $f(a)$ and $f(b)$ have opposite signs. A root is guaranteed by IVT. Each step halves the interval.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Trapezoidal rule for $\\int_a^b f(x)\\, dx$ with $n$ subintervals.',
         'answer': '$T = \\dfrac{h}{2}[f(x_0) + 2f(x_1) + \\cdots + 2f(x_{n-1}) + f(x_n)]$, where $h = (b-a)/n$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Simpson's 1/3 rule ($n$ must be even).",
         'answer': "$S = \\dfrac{h}{3}[f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + \\cdots + 4f(x_{n-1}) + f(x_n)]$, $h = (b-a)/n$. More accurate than the trapezoidal rule.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Euler's method for $y' = f(x, y)$, $y(x_0) = y_0$.",
         'answer': '$y_{n+1} = y_n + h\\, f(x_n, y_n)$. Simple but first-order accurate (error $O(h)$). Step size $h$ must be small for accuracy.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is round-off error vs truncation error?',
         'answer': 'Round-off error: finite computer precision when representing numbers. Truncation error: error from approximating an infinite process (e.g. Taylor series) with a finite one.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    # ------------------------------------------------------------------ #
    # 003A — Vector Spaces & Linear Transformations
    # ------------------------------------------------------------------ #
    add_cards('Vector Spaces & Linear Transformations', [
        {'question': 'What is a vector space?',
         'answer': 'A set $V$ with addition and scalar multiplication satisfying 8 axioms: closure, associativity, commutativity, zero vector, additive inverses, and three distributive/associative scalar laws.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a subspace?',
         'answer': 'A subset $W \\subseteq V$ that is itself a vector space. Sufficient: $W$ contains $\\mathbf{0}$, and $W$ is closed under addition and scalar multiplication.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Linear independence: when is $\\{\\mathbf{v}_1, \\ldots, \\mathbf{v}_n\\}$ linearly independent?',
         'answer': 'Only the trivial combination gives zero: $c_1\\mathbf{v}_1 + \\cdots + c_n\\mathbf{v}_n = \\mathbf{0} \\Rightarrow c_1 = \\cdots = c_n = 0$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the span of a set of vectors?',
         'answer': '$\\operatorname{span}\\{\\mathbf{v}_1,\\ldots,\\mathbf{v}_n\\} = \\{c_1\\mathbf{v}_1 + \\cdots + c_n\\mathbf{v}_n : c_i \\in \\mathbb{R}\\}$ — all linear combinations.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a basis?',
         'answer': 'A set that is linearly independent AND spans $V$. The number of basis vectors equals the dimension $\\dim(V)$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Standard basis for $\\mathbb{R}^3$.',
         'answer': '$\\mathbf{e}_1 = (1,0,0)$, $\\mathbf{e}_2 = (0,1,0)$, $\\mathbf{e}_3 = (0,0,1)$. They are orthonormal (mutually perpendicular unit vectors).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Definition of a linear transformation $T: V \\to W$.',
         'answer': '$T$ satisfies: (1) $T(\\mathbf{u}+\\mathbf{v}) = T(\\mathbf{u})+T(\\mathbf{v})$; (2) $T(c\\mathbf{u}) = cT(\\mathbf{u})$. Equivalently: $T(\\alpha\\mathbf{u}+\\beta\\mathbf{v}) = \\alpha T(\\mathbf{u})+\\beta T(\\mathbf{v})$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Kernel (null space) of $T$.',
         'answer': '$\\ker(T) = \\{\\mathbf{v} \\in V : T(\\mathbf{v}) = \\mathbf{0}\\}$. It is a subspace of $V$. $T$ is injective iff $\\ker(T) = \\{\\mathbf{0}\\}$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Rank-Nullity Theorem.',
         'answer': '$\\dim(\\ker T) + \\dim(\\operatorname{im} T) = \\dim(V)$. Equivalently: $\\operatorname{nullity}(A) + \\operatorname{rank}(A) = n$ (number of columns of $A$).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 003B — Eigenvalues & Eigenvectors  (critical for Control Systems)
    # ------------------------------------------------------------------ #
    add_cards('Eigenvalues & Eigenvectors', [
        {'question': 'Definition of eigenvalue and eigenvector.',
         'answer': 'For square matrix $A$, $\\lambda$ is an eigenvalue and $\\mathbf{v} \\ne \\mathbf{0}$ is a corresponding eigenvector if $A\\mathbf{v} = \\lambda\\mathbf{v}$. The eigenvector is scaled, not rotated, by $A$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How do you find eigenvalues of $A$?',
         'answer': 'Solve the characteristic equation $\\det(A - \\lambda I) = 0$. The roots $\\lambda$ are the eigenvalues.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the eigenvalues of $A = \\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}$.',
         'answer': '$\\det(A-\\lambda I) = (2-\\lambda)^2 - 1 = \\lambda^2 - 4\\lambda + 3 = (\\lambda-1)(\\lambda-3) = 0$. Eigenvalues: $\\lambda_1 = 1$, $\\lambda_2 = 3$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Form $A - \\lambda I$', 'detail': '$\\begin{pmatrix}2-\\lambda&1\\\\1&2-\\lambda\\end{pmatrix}$'},
                   {'move': 'Compute determinant', 'detail': '$(2-\\lambda)^2 - 1 = \\lambda^2 - 4\\lambda + 3$'},
                   {'move': 'Factor', 'detail': '$(\\lambda-1)(\\lambda-3) = 0 \\Rightarrow \\lambda = 1, 3$'}]},
        {'question': 'How do you find eigenvectors for eigenvalue $\\lambda$?',
         'answer': 'Solve $(A - \\lambda I)\\mathbf{v} = \\mathbf{0}$ — i.e. find the null space of $(A - \\lambda I)$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the eigenvector of $A = \\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}$ for $\\lambda = 1$.',
         'answer': '$(A-I)\\mathbf{v} = \\mathbf{0}$: $\\begin{pmatrix}1&1\\\\1&1\\end{pmatrix}\\mathbf{v} = \\mathbf{0} \\Rightarrow v_1 + v_2 = 0$. Eigenvector: $[1,\\,-1]^T$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Form $A - I$', 'detail': '$\\begin{pmatrix}1&1\\\\1&1\\end{pmatrix}$'},
                   {'move': 'Solve $(A-I)\\mathbf{v}=\\mathbf{0}$', 'detail': '$v_1 + v_2 = 0$, so $v_2 = -v_1$'},
                   {'move': 'Write eigenvector', 'detail': '$\\mathbf{v} = [1,\\,-1]^T$ (or normalised: $[1/\\sqrt{2},\\,-1/\\sqrt{2}]^T$)'}]},
        {'question': 'Trace and determinant in terms of eigenvalues (2×2 case).',
         'answer': '$\\operatorname{tr}(A) = \\lambda_1 + \\lambda_2$ and $\\det(A) = \\lambda_1 \\lambda_2$. (General: sum and product of all eigenvalues.)',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Diagonalisation: when can $A$ be diagonalised?',
         'answer': '$A = PDP^{-1}$ where $D = \\operatorname{diag}(\\lambda_1,\\ldots,\\lambda_n)$. Possible iff $A$ has $n$ linearly independent eigenvectors (e.g. $n$ distinct eigenvalues).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Why are eigenvalues critical for control system stability?',
         'answer': 'System $\\dot{\\mathbf{x}} = A\\mathbf{x}$ is stable iff all eigenvalues of $A$ have negative real parts. In transfer function form: eigenvalues of $A$ = poles. Left-half-plane poles $\\Rightarrow$ stable.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': "Solve the ODE system $\\mathbf{x}' = A\\mathbf{x}$ using eigenvalues.",
         'answer': 'Solution: $\\mathbf{x}(t) = \\sum_i c_i \\mathbf{v}_i e^{\\lambda_i t}$, where $(\\lambda_i, \\mathbf{v}_i)$ are eigenpairs. Constants $c_i$ from initial condition $\\mathbf{x}(0)$.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Eigenvalues of an upper (or lower) triangular matrix.',
         'answer': 'The eigenvalues are the diagonal entries. $\\det(A - \\lambda I)$ for a triangular matrix gives a product of $(a_{ii} - \\lambda)$ terms.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 004B — Vector Functions & Line Integrals
    # ------------------------------------------------------------------ #
    add_cards('Vector Functions & Line Integrals', [
        {'question': 'What is a vector-valued function?',
         'answer': '$\\mathbf{r}(t) = \\langle x(t), y(t), z(t) \\rangle$. Maps scalar $t$ to a vector in $\\mathbb{R}^3$, tracing a curve as $t$ varies.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Derivative of $\\mathbf{r}(t) = \\langle x(t), y(t), z(t) \\rangle$.',
         'answer': "$\\mathbf{r}'(t) = \\langle x'(t), y'(t), z'(t) \\rangle$. The tangent vector to the curve at $t$.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Arc length of curve $\\mathbf{r}(t)$ from $t = a$ to $t = b$.',
         'answer': "$L = \\int_a^b |\\mathbf{r}'(t)|\\, dt = \\int_a^b \\sqrt{x'^2 + y'^2 + z'^2}\\, dt$.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Line integral of a scalar function $f$ along curve $C$.',
         'answer': "$\\int_C f\\, ds = \\int_a^b f(\\mathbf{r}(t))\\, |\\mathbf{r}'(t)|\\, dt$.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Work as a line integral: $W = \\int_C \\mathbf{F} \\cdot d\\mathbf{r}$.',
         'answer': "$W = \\int_a^b \\mathbf{F}(\\mathbf{r}(t)) \\cdot \\mathbf{r}'(t)\\, dt$. The dot product selects the component of force along the path.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a conservative vector field?',
         'answer': '$\\mathbf{F} = \\nabla f$ for some scalar potential $f$. Line integrals are path-independent: $\\int_C \\mathbf{F} \\cdot d\\mathbf{r} = f(B) - f(A)$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 005A — Surface Integrals & Green's Theorem
    # ------------------------------------------------------------------ #
    add_cards("Surface Integrals & Green's Theorem", [
        {"question": "State Green's Theorem.",
         'answer': "$\\oint_C P\\, dx + Q\\, dy = \\iint_D \\left(\\dfrac{\\partial Q}{\\partial x} - \\dfrac{\\partial P}{\\partial y}\\right) dA$. Converts a line integral around closed curve $C$ to a double integral over enclosed region $D$.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Use Green's Theorem to find the area of region $D$.",
         'answer': "$\\text{Area} = \\dfrac{1}{2} \\oint_C (x\\, dy - y\\, dx)$. Follows from Green's Theorem with $P = -y/2$, $Q = x/2$.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a surface integral of a scalar function over surface $S$?',
         'answer': '$\\iint_S f\\, dS = \\iint_D f(\\mathbf{r}(u,v))\\, |\\mathbf{r}_u \\times \\mathbf{r}_v|\\, dA$, where $\\mathbf{r}(u,v)$ parametrises $S$.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Flux integral: physical meaning and formula.',
         'answer': '$\\text{Flux} = \\iint_S \\mathbf{F} \\cdot d\\mathbf{S} = \\iint_S \\mathbf{F} \\cdot \\hat{\\mathbf{n}}\\, dS$. Measures net flow of $\\mathbf{F}$ through surface $S$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "State Stokes' Theorem.",
         'answer': "$\\iint_S (\\nabla \\times \\mathbf{F}) \\cdot d\\mathbf{S} = \\oint_C \\mathbf{F} \\cdot d\\mathbf{r}$. Relates the surface integral of curl $\\mathbf{F}$ to the line integral around boundary $C$ of $S$.",
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 005B — Gauss's Divergence Theorem
    # ------------------------------------------------------------------ #
    add_cards("Gauss's Divergence Theorem", [
        {'question': 'Define the divergence of $\\mathbf{F} = \\langle P, Q, R \\rangle$.',
         'answer': '$\\operatorname{div}\\mathbf{F} = \\nabla \\cdot \\mathbf{F} = \\dfrac{\\partial P}{\\partial x} + \\dfrac{\\partial Q}{\\partial y} + \\dfrac{\\partial R}{\\partial z}$. A scalar measuring net outward flux per unit volume.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {"question": "State the Divergence Theorem (Gauss's Theorem).",
         'answer': '$\\oiint_S \\mathbf{F} \\cdot d\\mathbf{S} = \\iiint_V (\\nabla \\cdot \\mathbf{F})\\, dV$. Outward flux through closed surface $S$ equals integral of divergence over enclosed volume $V$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Physical interpretation of the Divergence Theorem.',
         'answer': 'For fluid flow, total outward flux through a closed surface equals total "source strength" inside. $\\nabla \\cdot \\mathbf{F} > 0$: source; $< 0$: sink; $= 0$: incompressible.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Apply the Divergence Theorem: find $\\oiint_S \\mathbf{F} \\cdot d\\mathbf{S}$ for $\\mathbf{F} = \\langle x, y, z \\rangle$ over a unit sphere.',
         'answer': '$\\nabla \\cdot \\mathbf{F} = 3$. Volume of unit sphere $= \\dfrac{4}{3}\\pi$. Flux $= 3 \\cdot \\dfrac{4}{3}\\pi = 4\\pi$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Compute divergence', 'detail': '$\\nabla \\cdot \\langle x,y,z \\rangle = 3$'},
                   {'move': 'Apply theorem', 'detail': '$\\iiint_V 3\\, dV = 3 \\times V(\\text{unit sphere})$'},
                   {'move': 'Evaluate', 'detail': '$3 \\times \\dfrac{4\\pi}{3} = 4\\pi$'}]},
        {'question': 'Define the curl of $\\mathbf{F} = \\langle P, Q, R \\rangle$.',
         'answer': '$\\operatorname{curl}\\mathbf{F} = \\nabla \\times \\mathbf{F} = \\left\\langle \\dfrac{\\partial R}{\\partial y}-\\dfrac{\\partial Q}{\\partial z},\\; \\dfrac{\\partial P}{\\partial z}-\\dfrac{\\partial R}{\\partial x},\\; \\dfrac{\\partial Q}{\\partial x}-\\dfrac{\\partial P}{\\partial y} \\right\\rangle$. A vector measuring local rotation.',
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
