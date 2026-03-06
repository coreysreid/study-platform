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
         'answer': 'A function $f: A \\to B$ assigns to each element $x$ in domain $A$ exactly one element $f(x)$ in codomain $B$. Key: each input has one output.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the domain of $f(x) = \\sqrt{4 - x^2}$?',
         'answer': 'Need $4 - x^2 \\ge 0$, so $x^2 \\le 4$, i.e. $-2 \\le x \\le 2$. Domain: $[-2, 2]$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What does the vertical line test determine?',
         'answer': 'Whether a curve in the $xy$-plane represents a function. A curve is a function if and only if every vertical line intersects it at most once.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Informal definition of $\\lim_{x \\to a} f(x) = L$.',
         'answer': 'As $x$ gets arbitrarily close to $a$ (but not equal), $f(x)$ gets arbitrarily close to $L$. The value of $f$ at $a$ does not matter.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Evaluate $\\lim_{x \\to 3} \\dfrac{x^2 - 9}{x - 3}$.',
         'answer': 'Factor: $\\dfrac{x^2-9}{x-3} = \\dfrac{(x+3)(x-3)}{x-3} = x+3$. Limit $= 3+3 = 6$.',
         'difficulty': 'easy', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Factor numerator', 'detail': '$x^2-9 = (x+3)(x-3)$'},
                   {'move': 'Cancel', 'detail': '$\\dfrac{(x+3)(x-3)}{x-3} = x+3 \\quad (x \\ne 3)$'},
                   {'move': 'Substitute', 'detail': '$\\lim = 3+3 = 6$'}]},
        {'question': 'When does a two-sided limit fail to exist?',
         'answer': 'When the left-hand limit $\\ne$ right-hand limit, or when the function oscillates or grows without bound near the point.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State the Squeeze Theorem.',
         'answer': 'If $g(x) \\le f(x) \\le h(x)$ near $a$ and $\\lim_{x \\to a} g(x) = \\lim_{x \\to a} h(x) = L$, then $\\lim_{x \\to a} f(x) = L$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Evaluate $\\lim_{x \\to 0} \\dfrac{\\sin x}{x}$.',
         'answer': '$1$. This fundamental limit is proved using the Squeeze Theorem and is the basis for all trigonometric derivatives.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Evaluate $\\lim_{x \\to \\infty} \\dfrac{3x^2 + 2x}{x^2 - 5}$.',
         'answer': 'Divide top and bottom by $x^2$: $\\dfrac{3 + 2/x}{1 - 5/x^2} \\to \\dfrac{3}{1} = 3$ as $x \\to \\infty$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Divide by highest power $x^2$', 'detail': '$\\dfrac{3 + 2/x}{1 - 5/x^2}$'},
                   {'move': 'Take limit', 'detail': '$2/x \\to 0$ and $5/x^2 \\to 0$'},
                   {'move': 'Result', 'detail': '$3/1 = 3$'}]},
        {'question': 'What is a horizontal asymptote?',
         'answer': '$y = L$ is a horizontal asymptote if $\\lim_{x \\to \\infty} f(x) = L$ or $\\lim_{x \\to -\\infty} f(x) = L$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {"question": "State L'Hôpital's Rule.",
         'answer': "If $\\lim_{x \\to a} f(x)/g(x)$ gives $0/0$ or $\\infty/\\infty$, then $\\lim_{x \\to a} \\dfrac{f(x)}{g(x)} = \\lim_{x \\to a} \\dfrac{f'(x)}{g'(x)}$, provided the latter limit exists.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {"question": "Use L'Hôpital's Rule to find $\\lim_{x \\to 0} \\dfrac{e^x - 1}{x}$.",
         'answer': '$0/0$ form. Differentiate top and bottom: $\\lim \\dfrac{e^x}{1} = e^0 = 1$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 001B — Continuity & Exponential Functions
    # ------------------------------------------------------------------ #
    add_cards('Continuity & Exponential Functions', [
        {'question': 'Three conditions for $f$ to be continuous at $x = a$.',
         'answer': '1. $f(a)$ is defined. 2. $\\lim_{x \\to a} f(x)$ exists. 3. $\\lim_{x \\to a} f(x) = f(a)$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a removable discontinuity?',
         'answer': 'The limit exists but either $f(a)$ is undefined or $f(a) \\ne \\lim_{x \\to a} f(x)$. The "hole" can be filled by redefining $f(a)$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a jump discontinuity?',
         'answer': 'The left-hand and right-hand limits both exist but are unequal. The function "jumps" from one value to another.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'State the Intermediate Value Theorem (IVT).',
         'answer': 'If $f$ is continuous on $[a, b]$ and $k$ is any value between $f(a)$ and $f(b)$, then there exists $c \\in (a, b)$ such that $f(c) = k$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the natural base $e$?',
         'answer': '$e = \\lim_{n \\to \\infty} \\left(1 + \\dfrac{1}{n}\\right)^n \\approx 2.71828$. The unique base for which $\\dfrac{d}{dx}[e^x] = e^x$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is $\\dfrac{d}{dx}[e^x]$?',
         'answer': '$\\dfrac{d}{dx}[e^x] = e^x$. The exponential function is its own derivative.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is $\\dfrac{d}{dx}[e^{f(x)}]$? (chain rule)',
         'answer': "$\\dfrac{d}{dx}[e^{f(x)}] = e^{f(x)} \\cdot f'(x)$.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is $\\dfrac{d}{dx}[\\ln x]$?',
         'answer': '$\\dfrac{d}{dx}[\\ln x] = \\dfrac{1}{x}$, for $x > 0$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Solve for $x$: $e^{2x} = 7$.',
         'answer': 'Take $\\ln$ of both sides: $2x = \\ln 7$, so $x = \\dfrac{\\ln 7}{2} \\approx 0.973$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'List four properties of $e^x$.',
         'answer': '1. $e^{a+b} = e^a \\cdot e^b$. 2. $e^{a-b} = e^a/e^b$. 3. $(e^a)^b = e^{ab}$. 4. $e^0 = 1$. Domain: all reals; range: $(0, \\infty)$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Change of base formula for logarithms.',
         'answer': '$\\log_b x = \\dfrac{\\ln x}{\\ln b}$. Example: $\\log_{10} 100 = \\dfrac{\\ln 100}{\\ln 10} = 2$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Differentiate $f(x) = \\ln(x^2 + 1)$.',
         'answer': "$f'(x) = \\dfrac{1}{x^2+1} \\cdot 2x = \\dfrac{2x}{x^2+1}$. Chain rule: derivative of outer times derivative of inner.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 002B — Curve Sketching & Optimisation
    # ------------------------------------------------------------------ #
    add_cards('Curve Sketching & Optimisation', [
        {'question': 'What is a critical point of $f(x)$?',
         'answer': "A point $x = c$ where $f'(c) = 0$ or $f'(c)$ is undefined. Critical points are candidates for local extrema.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'First Derivative Test for local extrema.',
         'answer': "At critical point $c$: if $f'$ changes $+$ to $-$, local max. If $f'$ changes $-$ to $+$, local min. If no sign change, neither.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Second Derivative Test for local extrema.',
         'answer': "At critical point $c$ where $f'(c) = 0$: if $f''(c) > 0$, local min; if $f''(c) < 0$, local max; if $f''(c) = 0$, inconclusive.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': "What does $f''(x) > 0$ tell you about the shape of $f$?",
         'answer': "$f$ is concave up (curves upward, like a cup). $f'' < 0$ means concave down (curves downward, like a cap).",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is an inflection point?',
         'answer': "A point where the concavity changes. Occurs where $f''(x) = 0$ and changes sign.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How do you find absolute (global) max/min on a closed interval $[a, b]$?',
         'answer': '1. Find all critical points in $(a, b)$. 2. Evaluate $f$ at critical points and endpoints $a$, $b$. 3. Largest value = global max; smallest = global min.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the critical points of $f(x) = x^3 - 3x$.',
         'answer': "$f'(x) = 3x^2 - 3 = 0 \\Rightarrow x^2 = 1 \\Rightarrow x = \\pm 1$. Critical points at $x = -1$ (local max) and $x = 1$ (local min).",
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Differentiate', 'detail': "$f'(x) = 3x^2 - 3$"},
                   {'move': 'Set equal to zero', 'detail': "$3x^2 - 3 = 0 \\Rightarrow x = \\pm 1$"},
                   {'move': 'Classify', 'detail': "$f''(x) = 6x$: $f''(-1) = -6 < 0$ (max), $f''(1) = 6 > 0$ (min)"}]},
        {'question': 'Optimisation: a rectangle has perimeter 20 m. Maximise its area.',
         'answer': 'Let width $= x$. Then length $= 10 - x$. Area $A = x(10-x) = 10x - x^2$. $A\' = 10 - 2x = 0 \\Rightarrow x = 5$. Max area $= 25$ m².',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Variables', 'detail': 'Width $x$, length $10-x$ (perimeter: $2x+2(10-x)=20$ ✓)'},
                   {'move': 'Objective', 'detail': '$A = x(10-x) = 10x - x^2$'},
                   {'move': 'Differentiate and solve', 'detail': "$A' = 10 - 2x = 0 \\Rightarrow x = 5$"},
                   {'move': 'Verify maximum', 'detail': "$A'' = -2 < 0$ ✓, $A(5) = 25$ m²"}]},
        {'question': "What is the relationship between $f$, $f'$, and $f''$?",
         'answer': "Where $f' > 0$: $f$ is increasing. Where $f' < 0$: $f$ is decreasing. Where $f'' > 0$: $f$ is concave up. Where $f'' < 0$: $f$ is concave down.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 003B — Applications of Integration
    # ------------------------------------------------------------------ #
    add_cards('Applications of Integration', [
        {'question': 'Formula for the area between curves $y = f(x)$ and $y = g(x)$ from $x = a$ to $x = b$.',
         'answer': '$A = \\int_a^b |f(x) - g(x)|\\, dx$. If $f(x) \\ge g(x)$ on $[a,b]$: $A = \\int_a^b [f(x) - g(x)]\\, dx$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Disk method: volume of solid of revolution about the $x$-axis.',
         'answer': '$V = \\pi \\int_a^b [f(x)]^2\\, dx$. Slicing perpendicular to $x$-axis creates disks of radius $f(x)$ and thickness $dx$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Washer method: volume when rotating the region between $f(x) \\ge g(x) \\ge 0$ about the $x$-axis.',
         'answer': '$V = \\pi \\int_a^b \\left([f(x)]^2 - [g(x)]^2\\right) dx$. Each slice is a washer with outer radius $f(x)$ and inner radius $g(x)$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Shell method: volume of solid from rotating $y = f(x)$ about the $y$-axis.',
         'answer': '$V = 2\\pi \\int_a^b x\\, f(x)\\, dx$. Shell has radius $x$, height $f(x)$, and thickness $dx$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Average value of $f(x)$ on $[a, b]$.',
         'answer': '$f_{\\text{avg}} = \\dfrac{1}{b-a} \\int_a^b f(x)\\, dx$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Arc length of $y = f(x)$ from $x = a$ to $x = b$.',
         'answer': "$L = \\int_a^b \\sqrt{1 + [f'(x)]^2}\\, dx$.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the area enclosed by $y = x^2$ and $y = x$.',
         'answer': 'Intersect at $x = 0$, $x = 1$. $A = \\int_0^1 (x - x^2)\\, dx = \\left[\\dfrac{x^2}{2} - \\dfrac{x^3}{3}\\right]_0^1 = \\dfrac{1}{2} - \\dfrac{1}{3} = \\dfrac{1}{6}$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Find intersections', 'detail': '$x^2 = x \\Rightarrow x(x-1) = 0 \\Rightarrow x = 0, 1$'},
                   {'move': 'Determine top curve', 'detail': '$x > x^2$ on $[0,1]$ (check $x = 0.5$: $0.5 > 0.25$ ✓)'},
                   {'move': 'Integrate', 'detail': '$\\int_0^1 (x - x^2)\\, dx = \\left[\\dfrac{x^2}{2} - \\dfrac{x^3}{3}\\right]_0^1 = \\dfrac{1}{6}$'}]},
        {'question': 'Work done by a variable force $F(x)$ moving an object from $x = a$ to $x = b$.',
         'answer': '$W = \\int_a^b F(x)\\, dx$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 004A — Complex Numbers  (critical for DSP, Control, Analog)
    # ------------------------------------------------------------------ #
    add_cards('Complex Numbers', [
        {'question': 'Define the imaginary unit $j$.',
         'answer': '$j = \\sqrt{-1}$, so $j^2 = -1$. (Engineers use $j$; mathematicians use $i$.)',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Rectangular form of a complex number.',
         'answer': '$z = a + jb$, where $a = \\operatorname{Re}\\{z\\}$ (real part) and $b = \\operatorname{Im}\\{z\\}$ (imaginary part). $a, b \\in \\mathbb{R}$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Complex conjugate of $z = a + jb$.',
         'answer': '$z^* = a - jb$. Reflects across the real axis on the Argand diagram. $z \\cdot z^* = a^2 + b^2 = |z|^2$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Modulus (magnitude) of $z = a + jb$.',
         'answer': '$|z| = r = \\sqrt{a^2 + b^2}$. The distance from the origin to $z$ on the Argand diagram.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Argument (phase angle) of $z = a + jb$.',
         'answer': '$\\arg(z) = \\theta = \\operatorname{atan2}(b,\\, a)$ (four-quadrant arctangent). Units: radians or degrees. Notation: $\\angle z$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Convert $z = 3 + 4j$ to polar form.',
         'answer': '$r = \\sqrt{9 + 16} = 5$. $\\theta = \\arctan(4/3) \\approx 53.13^\\circ = 0.927$ rad. Polar form: $5\\angle 53.13^\\circ$ or $5e^{j \\cdot 0.927}$.',
         'difficulty': 'easy', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Compute modulus', 'detail': '$r = \\sqrt{3^2 + 4^2} = \\sqrt{25} = 5$'},
                   {'move': 'Compute argument', 'detail': '$\\theta = \\arctan(4/3) \\approx 53.13^\\circ$'},
                   {'move': 'Write polar form', 'detail': '$z = 5\\angle 53.13^\\circ$'}]},
        {"question": "State Euler's formula.",
         'answer': '$e^{j\\theta} = \\cos\\theta + j\\sin\\theta$. Therefore $\\cos\\theta = \\operatorname{Re}\\{e^{j\\theta}\\}$ and $\\sin\\theta = \\operatorname{Im}\\{e^{j\\theta}\\}$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Exponential (polar) form of $z = a + jb$.',
         'answer': '$z = r e^{j\\theta}$, where $r = |z|$ and $\\theta = \\arg(z)$. Equivalent to $z = r(\\cos\\theta + j\\sin\\theta)$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Multiply two complex numbers in polar form: $z_1 = r_1 e^{j\\theta_1}$ and $z_2 = r_2 e^{j\\theta_2}$.',
         'answer': '$z_1 z_2 = r_1 r_2\\, e^{j(\\theta_1+\\theta_2)} = r_1 r_2 \\angle(\\theta_1+\\theta_2)$. Magnitudes multiply; angles add.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Divide two complex numbers in polar form.',
         'answer': '$\\dfrac{z_1}{z_2} = \\dfrac{r_1}{r_2}\\, e^{j(\\theta_1-\\theta_2)} = \\dfrac{r_1}{r_2}\\angle(\\theta_1-\\theta_2)$. Magnitudes divide; angles subtract.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Divide $z_1 = 2 + j$ by $z_2 = 1 + 2j$ in rectangular form.',
         'answer': 'Multiply by conjugate: $\\dfrac{(2+j)(1-2j)}{(1+2j)(1-2j)} = \\dfrac{2-4j+j-2j^2}{1+4} = \\dfrac{4-3j}{5} = 0.8 - 0.6j$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Multiply by conjugate of denominator', 'detail': 'Conjugate of $(1+2j)$ is $(1-2j)$'},
                   {'move': 'Expand numerator', 'detail': '$(2+j)(1-2j) = 2-4j+j-2j^2 = 2-3j+2 = 4-3j$'},
                   {'move': 'Expand denominator', 'detail': '$(1+2j)(1-2j) = 1+4 = 5$'},
                   {'move': 'Simplify', 'detail': '$(4-3j)/5 = 0.8 - 0.6j$'}]},
        {"question": "De Moivre's Theorem.",
         'answer': '$(r e^{j\\theta})^n = r^n e^{jn\\theta}$, i.e. $(r\\angle\\theta)^n = r^n\\angle(n\\theta)$. Used to compute powers and roots of complex numbers.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the two square roots of $j$.',
         'answer': 'Write $j = e^{j\\pi/2}$. Roots: $e^{j\\pi/4}$ and $e^{j5\\pi/4}$, i.e. $\\dfrac{1+j}{\\sqrt{2}}$ and $-\\dfrac{1+j}{\\sqrt{2}}$.',
         'difficulty': 'hard', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Express $j$ in exponential form', 'detail': '$j = e^{j\\pi/2} = 1\\angle 90^\\circ$'},
                   {'move': 'Apply root formula', 'detail': 'Roots: $e^{j(\\pi/2 + 2\\pi k)/2}$ for $k = 0, 1$'},
                   {'move': '$k=0$', 'detail': '$e^{j\\pi/4} = \\cos 45^\\circ + j\\sin 45^\\circ = (1+j)/\\sqrt{2}$'},
                   {'move': '$k=1$', 'detail': '$e^{j5\\pi/4} = -(1+j)/\\sqrt{2}$'}]},
        {'question': 'How does a complex number represent a sinusoidal signal (phasor)?',
         'answer': '$A\\cos(\\omega t+\\phi) = \\operatorname{Re}\\{A e^{j\\phi} e^{j\\omega t}\\}$. The phasor $\\mathbf{X} = A e^{j\\phi} = A\\angle\\phi$ encodes amplitude $A$ and phase $\\phi$, dropping the $e^{j\\omega t}$ carrier.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Express $e^{j\\pi}$ in rectangular form.',
         'answer': "$e^{j\\pi} = \\cos\\pi + j\\sin\\pi = -1$. Euler's identity: $e^{j\\pi} + 1 = 0$.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Impedance of a capacitor $C$ at angular frequency $\\omega$.',
         'answer': '$Z_C = \\dfrac{1}{j\\omega C}$. In polar form: $\\dfrac{1}{\\omega C}\\angle{-90^\\circ}$. Voltage lags current by $90^\\circ$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Impedance of an inductor $L$ at angular frequency $\\omega$.',
         'answer': '$Z_L = j\\omega L$. In polar form: $\\omega L\\angle{90^\\circ}$. Voltage leads current by $90^\\circ$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 004B — Vectors in 2D & 3D
    # ------------------------------------------------------------------ #
    add_cards('Vectors in 2D & 3D', [
        {'question': 'Component form of a 3D vector from point $A$ to point $B$.',
         'answer': '$\\overrightarrow{AB} = B - A = \\langle b_1-a_1,\\, b_2-a_2,\\, b_3-a_3 \\rangle$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Magnitude of vector $\\mathbf{v} = \\langle a, b, c \\rangle$.',
         'answer': '$|\\mathbf{v}| = \\sqrt{a^2 + b^2 + c^2}$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Unit vector in the direction of $\\mathbf{v}$.',
         'answer': '$\\hat{\\mathbf{v}} = \\dfrac{\\mathbf{v}}{|\\mathbf{v}|}$. Has magnitude 1 and the same direction as $\\mathbf{v}$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Dot product: definition and formula.',
         'answer': '$\\mathbf{a} \\cdot \\mathbf{b} = |\\mathbf{a}||\\mathbf{b}|\\cos\\theta = a_1 b_1 + a_2 b_2 + a_3 b_3$. Scalar result.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'When are two non-zero vectors perpendicular?',
         'answer': 'When $\\mathbf{a} \\cdot \\mathbf{b} = 0$. Since $\\cos 90^\\circ = 0$, the dot product is zero.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the angle between $\\mathbf{a} = \\langle 1, 0, 1 \\rangle$ and $\\mathbf{b} = \\langle 0, 1, 1 \\rangle$.',
         'answer': '$\\mathbf{a} \\cdot \\mathbf{b} = 1$. $|\\mathbf{a}| = |\\mathbf{b}| = \\sqrt{2}$. $\\cos\\theta = \\dfrac{1}{2} \\Rightarrow \\theta = 60^\\circ$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Cross product $\\mathbf{a} \\times \\mathbf{b}$: direction and magnitude.',
         'answer': 'Direction: perpendicular to both $\\mathbf{a}$ and $\\mathbf{b}$ (right-hand rule). Magnitude: $|\\mathbf{a} \\times \\mathbf{b}| = |\\mathbf{a}||\\mathbf{b}|\\sin\\theta$ = area of parallelogram.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Cross product formula for $\\mathbf{a} = \\langle a_1,a_2,a_3\\rangle$ and $\\mathbf{b} = \\langle b_1,b_2,b_3\\rangle$.',
         'answer': '$\\mathbf{a} \\times \\mathbf{b} = \\langle a_2 b_3 - a_3 b_2,\\; a_3 b_1 - a_1 b_3,\\; a_1 b_2 - a_2 b_1 \\rangle$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Scalar projection of $\\mathbf{a}$ onto $\\mathbf{b}$.',
         'answer': '$\\operatorname{comp}_{\\mathbf{b}}(\\mathbf{a}) = \\dfrac{\\mathbf{a} \\cdot \\mathbf{b}}{|\\mathbf{b}|}$. The signed length of the shadow of $\\mathbf{a}$ in direction $\\mathbf{b}$.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Vector projection of $\\mathbf{a}$ onto $\\mathbf{b}$.',
         'answer': '$\\operatorname{proj}_{\\mathbf{b}}(\\mathbf{a}) = \\dfrac{\\mathbf{a} \\cdot \\mathbf{b}}{|\\mathbf{b}|^2}\\, \\mathbf{b}$. The component of $\\mathbf{a}$ in the direction of $\\mathbf{b}$ as a vector.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # 005B — Systems of Linear Equations
    # ------------------------------------------------------------------ #
    add_cards('Systems of Linear Equations', [
        {'question': 'What is an augmented matrix?',
         'answer': '$[A \\mid \\mathbf{b}]$ — the coefficient matrix $A$ with the constant column $\\mathbf{b}$ appended. Encodes the system $A\\mathbf{x} = \\mathbf{b}$.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Three elementary row operations.',
         'answer': '1. Swap two rows ($R_i \\leftrightarrow R_j$). 2. Multiply a row by a non-zero scalar ($R_i \\to c R_i$). 3. Add a multiple of one row to another ($R_i \\to R_i + c R_j$).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is row echelon form (REF)?',
         'answer': 'Each row has a leading 1 (pivot) further right than the row above; rows of zeros are at the bottom. Used as intermediate form for back substitution.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is reduced row echelon form (RREF)?',
         'answer': 'REF where each pivot is 1 and every other entry in the pivot column is 0. Gives the solution directly without back substitution.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Three possible solution types for a linear system.',
         'answer': '1. Unique solution (consistent, independent). 2. Infinitely many solutions (consistent, dependent). 3. No solution (inconsistent).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Solve using Gaussian elimination: $x + y = 3$, $2x - y = 0$.',
         'answer': 'Augmented matrix $\\to R_2 - 2R_1$: $-3y = -6 \\Rightarrow y = 2$; $x = 3-2 = 1$. Solution: $(1, 2)$.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Write augmented matrix', 'detail': '$[1\\; 1 \\mid 3;\\; 2\\; {-1} \\mid 0]$'},
                   {'move': 'Eliminate $x$ from row 2', 'detail': '$R_2 \\to R_2 - 2R_1$: $[0\\; {-3} \\mid {-6}]$'},
                   {'move': 'Back substitute', 'detail': '$y = 2$, then $x = 3 - 2 = 1$'}]},
        {'question': 'What is a free variable?',
         'answer': 'A variable corresponding to a column without a pivot in RREF. It can take any value; basic (pivot) variables are expressed in terms of free variables.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Rank of a matrix: definition and role in solution existence.',
         'answer': 'Rank $=$ number of pivot rows. System $A\\mathbf{x} = \\mathbf{b}$ is consistent iff $\\operatorname{rank}(A) = \\operatorname{rank}([A \\mid \\mathbf{b}])$. Unique solution iff rank $=$ number of unknowns.',
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
