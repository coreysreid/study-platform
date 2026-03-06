from django.db import migrations


def seed_flashcards(apps, schema_editor):
    """
    Extend DSP course flashcard content focused on:
    - DSP First 2nd Edition, Chapter 1 (Sinusoids & Phasors) — atomic gap-fill cards
    - DSP First 2nd Edition, Chapter 2 (Spectrum Representation) — atomic gap-fill cards
    - Kamen et al., Fundamentals of Signals and Systems, Chapter 1 — new topic 001B
    """
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return

    course = Course.objects.filter(
        name='Digital Signal Processing', created_by=system_user
    ).first()
    if not course:
        return

    # ------------------------------------------------------------------ #
    # Helper: add/update topic — keyed on (course, code) so metadata is
    # always correct even if a partial run previously created the topic.
    # ------------------------------------------------------------------ #
    def get_or_create_topic(name, code, order, description):
        topic, _ = Topic.objects.update_or_create(
            course=course,
            code=code,
            defaults={
                'name': name,
                'order': order,
                'description': description,
            },
        )
        return topic

    # ------------------------------------------------------------------ #
    # Helper: add cards to a topic — idempotent by question text.
    # Updates the in-memory `existing` set after each insert so that
    # duplicate questions within the same `cards` list are also skipped.
    # ------------------------------------------------------------------ #
    def add_extra_cards(topic, cards):
        existing = set(
            Flashcard.objects.filter(topic=topic).values_list('question', flat=True)
        )
        for card in cards:
            if card['question'] not in existing:
                Flashcard.objects.create(topic=topic, **card)
                existing.add(card['question'])

    # ------------------------------------------------------------------ #
    # Helper: populate a topic using per-question idempotent logic.
    # Self-healing: missing cards are backfilled if migration partially ran.
    # ------------------------------------------------------------------ #
    def add_cards_new(topic, cards):
        add_extra_cards(topic, cards)

    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    # ================================================================== #
    # NEW TOPIC 001B — Signal Fundamentals & Operations (Kamen Ch 1)
    # ================================================================== #
    topic_001b = get_or_create_topic(
        name='Signal Fundamentals & Operations',
        code='001B',
        order=11,
        description=(
            'Continuous-time and discrete-time signal types, elementary signals '
            '(unit step, ramp, impulse), signal operations (time shifting, scaling, '
            'reversal), energy and power, even and odd signals. '
            'Based on Kamen et al., Fundamentals of Signals and Systems, Chapter 1.'
        ),
    )

    add_cards_new(topic_001b, [
        # --- Signal types (one concept each) ---
        {
            'question': 'What is a continuous-time signal?',
            'answer': (
                'A signal $x(t)$ defined for all values of a continuous real variable $t$. '
                'The independent variable $t$ can take any value in an interval.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'What is a discrete-time signal?',
            'answer': (
                'A signal $x[n]$ defined only at integer indices $n$. '
                'Obtained by sampling a continuous-time signal: $x[n] = x(nT_s)$, '
                'where $T_s = 1/f_s$ is the sampling period.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'What distinguishes an analog signal from a digital signal?',
            'answer': (
                'Analog: continuous in both time and amplitude. '
                'Digital: discrete in time (sampled) AND discrete in amplitude (quantized). '
                'PCM: sampled (discrete-time) and quantized. '
                'Continuous-time but quantized = quantized analog; '
                'sampled but not quantized = discrete-time analog.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False,
        },
        # --- Periodicity ---
        {
            'question': 'Define a periodic continuous-time signal.',
            'answer': (
                '$x(t)$ is periodic with period $T > 0$ if $x(t + T) = x(t)$ for all $t$. '
                'The smallest such $T$ is the fundamental period $T_0$.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'What is the fundamental frequency $f_0$ of a periodic signal with period $T_0$?',
            'answer': (
                '$f_0 = 1/T_0$ Hz. The angular fundamental frequency is '
                '$\\omega_0 = 2\\pi f_0 = 2\\pi / T_0$ rad/s.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        # --- Elementary signals ---
        {
            'question': 'Define the unit step function $u(t)$.',
            'answer': (
                '$u(t) = 1$ for $t \\geq 0$ and $u(t) = 0$ for $t < 0$. '
                'Models a signal that is switched on at $t = 0$.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Define the unit ramp function $r(t)$.',
            'answer': (
                '$r(t) = t\\,u(t)$, i.e. $r(t) = t$ for $t \\geq 0$ and $0$ for $t < 0$. '
                'It is the integral of the unit step: $r(t) = \\int_{-\\infty}^{t} u(\\tau)\\,d\\tau$.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'State the sifting property of the Dirac delta $\\delta(t)$.',
            'answer': (
                '$\\int_{-\\infty}^{\\infty} f(t)\\,\\delta(t - t_0)\\,dt = f(t_0)$. '
                'The impulse "sifts out" the value of $f$ at the instant $t = t_0$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'How is the unit step $u(t)$ related to the Dirac delta $\\delta(t)$?',
            'answer': (
                '$u(t) = \\int_{-\\infty}^{t} \\delta(\\tau)\\,d\\tau$ '
                'and conversely $\\delta(t) = \\dfrac{d}{dt}u(t)$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        # --- Signal operations ---
        {
            'question': 'What does time shifting by $t_0$ do to a signal $x(t)$?',
            'answer': (
                'Produces $y(t) = x(t - t_0)$. '
                'Positive $t_0$: signal shifts right (delay). '
                'Negative $t_0$: signal shifts left (advance).'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'What does time reversal do to a signal $x(t)$?',
            'answer': (
                'Produces $y(t) = x(-t)$: reflects the waveform about $t = 0$. '
                'A delay in the original becomes an advance in the reversed signal.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'What does time scaling by factor $a$ do to $x(t)$?',
            'answer': (
                'Produces $y(t) = x(at)$. '
                'If $|a| > 1$: signal is compressed (speeds up). '
                'If $0 < |a| < 1$: signal is expanded (slows down). '
                'If $a < 0$: time reversal also occurs.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': (
                'Apply time shift then time scale: find $y(t) = x(2t - 3)$ in terms '
                'of shifted and scaled versions of $x(t)$.'
            ),
            'answer': (
                '$y(t) = x(2t - 3) = x\\!\\left(2\\left(t - \\tfrac{3}{2}\\right)\\right)$: '
                '$x(t)$ shifted right by $\\tfrac{3}{2}$ s, then time-compressed by a factor of 2.'
            ),
            'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
            'steps': [
                {
                    'move': 'Factor out the scaling constant',
                    'detail': '$x(2t - 3) = x\\!\\left(2\\left(t - \\tfrac{3}{2}\\right)\\right)$',
                },
                {
                    'move': 'Interpret as shift first, then scale',
                    'detail': (
                        'Shift $x(t)$ right by $\\tfrac{3}{2}$: $x\\!\\left(t - \\tfrac{3}{2}\\right)$. '
                        'Then compress by factor 2: replace $t$ with $2t$.'
                    ),
                },
                {
                    'move': 'State the result',
                    'detail': (
                        '$y(t) = x(2t-3)$ is $x(t)$ shifted right by $\\tfrac{3}{2}$ s, '
                        'then time-compressed by a factor of 2.'
                    ),
                },
            ],
        },
        # --- Energy and power ---
        {
            'question': 'Define the energy of a continuous-time signal $x(t)$.',
            'answer': (
                '$E_x = \\int_{-\\infty}^{\\infty} |x(t)|^2\\,dt$. '
                'An energy signal has $0 < E_x < \\infty$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Define the average power of a continuous-time signal $x(t)$.',
            'answer': (
                '$P_x = \\lim_{T \\to \\infty} \\dfrac{1}{2T} \\int_{-T}^{T} |x(t)|^2\\,dt$. '
                'A power signal has $0 < P_x < \\infty$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Is the sinusoid $x(t) = A\\cos(\\omega_0 t + \\phi)$ an energy or power signal?',
            'answer': (
                'A power signal. Its energy is infinite (it persists for all time). '
                'Its average power is $P = A^2/2$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        # --- Even and odd signals ---
        {
            'question': 'Define an even signal.',
            'answer': (
                '$x(t)$ is even if $x(-t) = x(t)$ for all $t$. '
                'Its waveform is symmetric about the vertical axis. '
                'Example: $\\cos(\\omega_0 t)$.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Define an odd signal.',
            'answer': (
                '$x(t)$ is odd if $x(-t) = -x(t)$ for all $t$. '
                'Its waveform is anti-symmetric about the origin. '
                'Example: $\\sin(\\omega_0 t)$. Note: $x(0) = 0$ for any odd signal.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'State the even-odd decomposition of an arbitrary signal $x(t)$.',
            'answer': (
                '$x(t) = x_e(t) + x_o(t)$, where '
                '$x_e(t) = \\dfrac{x(t) + x(-t)}{2}$ (even part) and '
                '$x_o(t) = \\dfrac{x(t) - x(-t)}{2}$ (odd part).'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
    ])

    # ================================================================== #
    # ADDITIONAL ATOMIC CARDS for 001A — Sinusoids & Phasors
    # (DSP First 2nd Ed., Chapter 1 gap-fill)
    # ================================================================== #
    topic_001a = topics.get('Sinusoids & Phasors')
    if topic_001a:
        add_extra_cards(topic_001a, [
            {
                'question': (
                    'State the three relationships connecting period $T$, '
                    'frequency $f_0$, and angular frequency $\\omega_0$.'
                ),
                'answer': (
                    '$T = 1/f_0$; $\\omega_0 = 2\\pi f_0$; $\\omega_0 = 2\\pi / T$. '
                    'Units: $T$ in seconds, $f_0$ in Hz, $\\omega_0$ in rad/s.'
                ),
                'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': (
                    'A sinusoid $x(t) = A\\cos(\\omega_0 t + \\phi)$ has phase $\\phi$. '
                    'What time delay $t_d$ does this correspond to?'
                ),
                'answer': (
                    'The phase shift $\\phi$ is equivalent to a time delay '
                    '$t_d = -\\phi / \\omega_0 = -\\phi / (2\\pi f_0)$. '
                    'Negative $\\phi$ (lag) → positive delay (waveform shifts right).'
                ),
                'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': 'Express the complex number $z = a + jb$ in polar form.',
                'answer': (
                    '$z = r\\,e^{j\\theta} = r\\angle\\theta$, where '
                    '$r = |z| = \\sqrt{a^2 + b^2}$ and '
                    '$\\theta = \\angle z = \\arctan(b/a)$ (adjusted for quadrant).'
                ),
                'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': 'Convert polar form $r\\angle\\theta$ to rectangular form $a + jb$.',
                'answer': (
                    '$a = r\\cos\\theta$ (real part); '
                    '$b = r\\sin\\theta$ (imaginary part). '
                    'So $r\\angle\\theta = r\\cos\\theta + j\\,r\\sin\\theta$.'
                ),
                'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': 'What is the complex conjugate of $z = a + jb$, and in polar form?',
                'answer': (
                    '$z^* = a - jb$. '
                    'In polar form: if $z = r\\,e^{j\\theta}$, then $z^* = r\\,e^{-j\\theta}$. '
                    'The magnitude is unchanged; the angle is negated.'
                ),
                'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': (
                    'Two phasors $\\mathbf{X}_1 = 3\\angle 30°$ and $\\mathbf{X}_2 = 4\\angle 90°$. '
                    'Find the magnitude and phase of their sum.'
                ),
                'answer': (
                    'The sum has magnitude $|\\mathbf{X}| \\approx 6.09$ and phase '
                    '$\\angle\\mathbf{X} \\approx 64.7°$.'
                ),
                'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
                'steps': [
                    {
                        'move': 'Convert to rectangular form',
                        'detail': (
                            '$\\mathbf{X}_1 = 3\\cos 30° + j\\,3\\sin 30° = 2.598 + j1.5$. '
                            '$\\mathbf{X}_2 = 4\\cos 90° + j\\,4\\sin 90° = 0 + j4$.'
                        ),
                    },
                    {
                        'move': 'Add real and imaginary parts separately',
                        'detail': 'Sum $= (2.598 + 0) + j(1.5 + 4) = 2.598 + j5.5$.',
                    },
                    {
                        'move': 'Convert back to polar',
                        'detail': (
                            '$|\\mathbf{X}| = \\sqrt{2.598^2 + 5.5^2} \\approx 6.09$. '
                            '$\\angle\\mathbf{X} = \\arctan(5.5/2.598) \\approx 64.7°$.'
                        ),
                    },
                ],
            },
            {
                'question': (
                    'What is the physical interpretation of the phasor '
                    '$\\mathbf{X} = A\\,e^{j\\phi}$?'
                ),
                'answer': (
                    '$\\mathbf{X}$ is a complex amplitude that encodes both magnitude $A$ and '
                    'phase $\\phi$ of the sinusoid $x(t) = A\\cos(\\omega_0 t + \\phi)$. '
                    'The physical signal is $x(t) = \\operatorname{Re}\\{\\mathbf{X}\\,e^{j\\omega_0 t}\\}$.'
                ),
                'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': (
                    'Why can phasors only be added when the signals share the same frequency?'
                ),
                'answer': (
                    'Phasor addition exploits linearity of $\\operatorname{Re}\\{\\cdot\\}$: '
                    '$\\operatorname{Re}\\{\\mathbf{X}_1 e^{j\\omega t}\\} + '
                    '\\operatorname{Re}\\{\\mathbf{X}_2 e^{j\\omega t}\\} = '
                    '\\operatorname{Re}\\{(\\mathbf{X}_1 + \\mathbf{X}_2)e^{j\\omega t}\\}$. '
                    'If frequencies differ, the $e^{j\\omega t}$ factors cannot be factored out.'
                ),
                'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True,
            },
        ])

    # ================================================================== #
    # ADDITIONAL ATOMIC CARDS for 002A — Spectrum Representation
    # (DSP First 2nd Ed., Chapter 2 gap-fill)
    # ================================================================== #
    topic_002a = topics.get('Spectrum Representation')
    if topic_002a:
        add_extra_cards(topic_002a, [
            {
                'question': (
                    'State the inverse Euler identity for cosine.'
                ),
                'answer': (
                    '$\\cos\\theta = \\dfrac{e^{j\\theta} + e^{-j\\theta}}{2}$. '
                    'Used to write a cosine as the sum of two complex exponentials '
                    'before reading off spectral lines.'
                ),
                'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': (
                    'State the inverse Euler identity for sine.'
                ),
                'answer': (
                    '$\\sin\\theta = \\dfrac{e^{j\\theta} - e^{-j\\theta}}{2j}$. '
                    'The coefficient at $+f_0$ is $1/(2j) = -j/2$ and at $-f_0$ is $+j/2$.'
                ),
                'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': (
                    'What spectral lines does a single complex exponential $e^{j2\\pi f_0 t}$ '
                    'produce?'
                ),
                'answer': (
                    'A single line at frequency $+f_0$ with complex amplitude $1$. '
                    'Unlike a real cosine, it has no negative-frequency component.'
                ),
                'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': (
                    'What is conjugate symmetry of the spectrum, and for which signals does it hold?'
                ),
                'answer': (
                    'For a real-valued signal, $c_{-k} = c_k^*$: the coefficient at $-f_0$ is '
                    'the complex conjugate of the coefficient at $+f_0$. '
                    'Consequence: magnitude spectrum is even ($|c_{-k}| = |c_k|$); '
                    'phase spectrum is odd ($\\angle c_{-k} = -\\angle c_k$).'
                ),
                'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': (
                    'How does adding a DC offset $C$ to a signal $x(t)$ change its spectrum?'
                ),
                'answer': (
                    'It adds a spectral line at $f = 0$ with complex amplitude $C$. '
                    'All other spectral components are unchanged.'
                ),
                'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': (
                    'Find the spectral lines of $x(t) = \\sin(2\\pi f_0 t)$.'
                ),
                'answer': (
                    'Two spectral lines: at $+f_0$ with coefficient $c_{+f_0} = -j/2$ '
                    'and at $-f_0$ with coefficient $c_{-f_0} = +j/2$, so '
                    '$|c_{\\pm f_0}| = 1/2$ with phases $-90°$ at $+f_0$ and $+90°$ at $-f_0$.'
                ),
                'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
                'steps': [
                    {
                        'move': 'Apply the inverse Euler identity for sine',
                        'detail': (
                            '$\\sin(2\\pi f_0 t) = \\dfrac{e^{j2\\pi f_0 t} - e^{-j2\\pi f_0 t}}{2j}$'
                        ),
                    },
                    {
                        'move': 'Identify each complex exponential term',
                        'detail': (
                            'At $+f_0$: coefficient $= \\dfrac{1}{2j} = -\\dfrac{j}{2}$. '
                            'At $-f_0$: coefficient $= -\\dfrac{1}{2j} = +\\dfrac{j}{2}$.'
                        ),
                    },
                    {
                        'move': 'State magnitude and phase at each frequency',
                        'detail': (
                            '$|c_{\\pm f_0}| = 1/2$. '
                            '$\\angle c_{+f_0} = -90°$; $\\angle c_{-f_0} = +90°$.'
                        ),
                    },
                ],
            },
            {
                'question': (
                    'How does a time shift $t_0$ affect the magnitude and phase spectra of a signal?'
                ),
                'answer': (
                    'Replacing $t$ with $t - t_0$ multiplies each spectral coefficient by '
                    '$e^{-j2\\pi f t_0}$. '
                    'Magnitude spectrum is unchanged. '
                    'Phase of each component at frequency $f$ is shifted by $-2\\pi f t_0$ rad.'
                ),
                'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': (
                    'What is the spectral line representation of the signal '
                    '$x(t) = 2 + 3\\cos(2\\pi \\cdot 4t) + \\sin(2\\pi \\cdot 7t)$?'
                ),
                'answer': (
                    'DC: magnitude $2$ at $f = 0$. '
                    'Cosine at 4 Hz: magnitude $3/2 = 1.5$ at $\\pm 4$ Hz (phase $0$). '
                    'Sine at 7 Hz: magnitude $1/2$ at $\\pm 7$ Hz '
                    '(phase $-90°$ at $+7$ Hz, $+90°$ at $-7$ Hz).'
                ),
                'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
            },
            {
                'question': (
                    'What is the fundamental frequency and period of the signal '
                    '$x(t) = \\cos(2\\pi \\cdot 6t) + \\cos(2\\pi \\cdot 10t)$?'
                ),
                'answer': (
                    'The fundamental frequency is $f_0 = \\gcd(6, 10) = 2$ Hz. '
                    'Both 6 Hz and 10 Hz are integer multiples of 2 Hz. '
                    'Fundamental period: $T_0 = 1/f_0 = 0.5$ s.'
                ),
                'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
            },
        ])


def reverse_fn(apps, schema_editor):
    pass  # intentional no-op


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0029_restructure_mathematics'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
