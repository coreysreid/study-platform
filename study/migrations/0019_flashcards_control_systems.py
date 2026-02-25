from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return
    course = Course.objects.filter(name='Control Systems', created_by=system_user).first()
    if not course:
        return
    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    def add_cards(topic_name, cards):
        topic = topics.get(topic_name)
        if not topic or Flashcard.objects.filter(topic=topic).exists():
            return
        for card in cards:
            Flashcard.objects.create(topic=topic, **card)

    add_cards('Laplace Transforms & Transfer Functions', [
        {'question': 'Transfer function definition.',
         'answer': 'G(s) = L{output}/L{input} with zero initial conditions. G(s) = Y(s)/U(s).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'First-order system transfer function and time constant.',
         'answer': 'G(s) = K/(τs + 1). τ = time constant. DC gain = K (as s→0). Pole at s = −1/τ.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Standard second-order transfer function.',
         'answer': 'G(s) = Kωₙ²/(s² + 2ζωₙs + ωₙ²). ωₙ = natural frequency, ζ = damping ratio.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Derive the transfer function for a mass-spring-damper: m·ẍ + b·ẋ + kx = F.',
         'answer': 'Take Laplace: (ms² + bs + k)X(s) = F(s). G(s) = X(s)/F(s) = 1/(ms² + bs + k).',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Write ODE', 'detail': 'mẍ + bẋ + kx = F'},
                   {'move': 'Apply Laplace (zero ICs)', 'detail': '(ms² + bs + k)X(s) = F(s)'},
                   {'move': 'Transfer function', 'detail': 'G(s) = X(s)/F(s) = 1/(ms² + bs + k)'}]},
        {'question': 'What are the poles of G(s) = 10/(s² + 3s + 2)?',
         'answer': 'Denominator: s² + 3s + 2 = (s+1)(s+2) = 0. Poles at s = −1 and s = −2.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'DC gain of a transfer function.',
         'answer': 'G(0) = lim(s→0) G(s). Example: G(s) = 5/(s+2) → G(0) = 5/2 = 2.5.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the system order?',
         'answer': 'Order = degree of denominator polynomial. Second-order: denominator is s². Determines response complexity.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Step response of a first-order system G(s) = 1/(τs+1).',
         'answer': 'y(t) = K(1 − e^(−t/τ)) for unit step input. Reaches 63.2% at t=τ, 99.3% at t=5τ.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('Block Diagram Algebra', [
        {'question': 'Transfer function of blocks G₁ and G₂ in series (cascade).',
         'answer': 'G_total = G₁ × G₂.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Transfer function of blocks G₁ and G₂ in parallel.',
         'answer': 'G_total = G₁ + G₂.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Closed-loop transfer function with forward gain G and feedback H.',
         'answer': 'T(s) = G/(1 + GH). Negative feedback assumed. The denominator (1+GH) is the characteristic polynomial.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Reduce: forward path G = 5/s, unity feedback (H=1). Find closed-loop TF.',
         'answer': 'T(s) = G/(1+G×1) = (5/s)/(1+5/s) = 5/(s+5).',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Apply closed-loop formula', 'detail': 'T = G/(1+GH) with H=1'},
                   {'move': 'Substitute G=5/s', 'detail': 'T = (5/s)/(1 + 5/s)'},
                   {'move': 'Simplify', 'detail': 'T = 5/(s + 5)'}]},
        {'question': 'What is the error signal in a negative feedback loop?',
         'answer': 'E(s) = R(s) − Y(s)H(s). The difference between reference and (scaled) output.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State Mason\'s Gain Formula.',
         'answer': 'T = (1/Δ) Σₖ Pₖ Δₖ, where Pₖ = forward path gain, Δ = 1 − Σ(loop gains) + Σ(products of non-touching loops), Δₖ = Δ with loops touching path k removed.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Move a summing junction past a block G: what changes?',
         'answer': 'Moving summing junction from output to input: signal on the path gains 1/G. Moving from input to output: signal gains G.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('Time-Domain Response', [
        {'question': 'Rise time tr of underdamped second-order system.',
         'answer': 'tr ≈ (1.8)/ωₙ (10%-90%). More precisely: tr = (π − θ)/ωd, where θ = arctan(ωd/(ζωₙ)).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Peak time tp of underdamped second-order system.',
         'answer': 'tp = π/ωd, where ωd = ωₙ√(1−ζ²) is the damped natural frequency.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Percent overshoot (PO) formula.',
         'answer': 'PO = e^(−πζ/√(1−ζ²)) × 100%. Example: ζ=0.5 → PO ≈ 16.3%.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Settling time ts (2% criterion).',
         'answer': 'ts ≈ 4/(ζωₙ). (The signal stays within 2% of final value after ts.)',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Steady-state error for unit step input to Type 0 system.',
         'answer': 'ess = 1/(1+Kp), where Kp = lim(s→0) G(s) is the position error constant.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'System type: what determines it?',
         'answer': 'Number of pure integrators (poles at s=0) in the open-loop TF G(s)H(s). Type 0: no integrators; Type 1: one integrator (zero SS error to step); Type 2: two integrators.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'For G(s) = 10/((s+1)(s+2)), find the position error constant Kp.',
         'answer': 'Kp = lim(s→0) G(s) = 10/(1×2) = 5. SS error for step input: ess = 1/(1+5) = 1/6.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Underdamped step response formula.',
         'answer': 'y(t) = 1 − (e^(−ζωₙt)/√(1−ζ²)) sin(ωdt + φ), where φ = arccos(ζ), ωd = ωₙ√(1−ζ²).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('Stability Analysis', [
        {'question': 'BIBO stability condition.',
         'answer': 'A system is BIBO stable if every bounded input produces a bounded output. For LTI: all poles must be in the left-half s-plane (Re(pₖ) < 0).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Routh-Hurwitz criterion: how to form the Routh array.',
         'answer': 'Arrange polynomial coefficients in first two rows, then fill each subsequent row using 2×2 determinants from previous two rows. System stable if all first-column elements > 0.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Apply Routh-Hurwitz to s³ + 2s² + 3s + 6 = 0.',
         'answer': 'Row1: [1, 3]. Row2: [2, 6]. Row3: [(2×3−1×6)/2, 0] = [0, 0]. Zero row → roots on jω axis → marginally stable.',
         'difficulty': 'hard', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Set up rows', 'detail': 'Row1: [1, 3], Row2: [2, 6]'},
                   {'move': 'Row3', 'detail': 'b₁ = (2×3 − 1×6)/2 = 0 → entire row is zero'},
                   {'move': 'Interpretation', 'detail': 'Zero row from s² auxiliary polynomial → roots on jω axis → marginal stability'}]},
        {'question': 'What does a sign change in the first column of the Routh array indicate?',
         'answer': 'Each sign change in the first column indicates one root in the right-half plane (unstable root).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Define gain margin (GM).',
         'answer': 'GM = 20log(1/|G(jωpc)|) dB, where ωpc is the phase crossover frequency (where ∠G = −180°). GM > 0 → stable.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Define phase margin (PM).',
         'answer': 'PM = ∠G(jωgc) + 180°, where ωgc is the gain crossover frequency (where |G| = 0dB). PM > 0° → stable. Typical design: PM > 45°.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is marginal stability?',
         'answer': 'Poles exactly on the jω axis (imaginary axis). System oscillates indefinitely — not practically stable. Routh: entire row of zeros.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('Root Locus', [
        {'question': 'What is the root locus?',
         'answer': 'Locus of closed-loop poles as proportional gain K varies from 0 to ∞ (for negative feedback). Shows how stability changes with gain.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Root locus rule: starting and ending points.',
         'answer': 'Locus starts at open-loop poles (K=0) and ends at open-loop zeros (K→∞) or at infinity.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Number of branches of root locus.',
         'answer': 'Equal to the number of open-loop poles n. (Number going to infinity = n − m, where m = number of zeros).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Asymptote angles for n poles, m zeros.',
         'answer': 'Angles = (2k+1)×180°/(n−m) for k = 0, 1, ..., n−m−1.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Asymptote centroid (σa).',
         'answer': 'σa = (Σpoles − Σzeros)/(n − m). All asymptotes originate from this real-axis point.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Breakaway point condition.',
         'answer': 'dK/ds = 0 along the real axis, or equivalently: Σ 1/(s−pᵢ) = Σ 1/(s−zⱼ).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How to use root locus for controller design.',
         'answer': 'Choose desired closed-loop pole location (based on PO and ts specs). Add gain K or pole/zero (lead/lag compensator) to bring root locus through the desired point.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('Bode & Nyquist Analysis', [
        {'question': 'Bode magnitude: contribution of a real pole at s = −a.',
         'answer': '|H| = 1/|1+jω/a|. Asymptote: 0dB for ω<<a; −20dB/decade for ω>>a. Corner at ω=a.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Bode phase: contribution of a real pole at s = −a.',
         'answer': 'Phase = −arctan(ω/a). Asymptote: 0° for ω<<a, −45° at ω=a, −90° for ω>>a.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Bode slope contribution of a zero at s = 0 (integrator/differentiator).',
         'answer': 'jω zero (differentiator): +20dB/decade, +90° constant phase. 1/jω pole (integrator): −20dB/decade, −90° constant.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How do you find gain margin from a Bode plot?',
         'answer': 'Find ωpc where phase = −180°. GM = −|G(jωpc)|dB (negative of the magnitude in dB at that frequency).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How do you find phase margin from a Bode plot?',
         'answer': 'Find ωgc where |G| = 0dB. PM = ∠G(jωgc) + 180°.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Nyquist stability criterion (simplified).',
         'answer': 'Number of unstable closed-loop poles Z = N + P, where N = clockwise encirclements of −1, P = open-loop RHP poles. Stable if Z = 0.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a minimum-phase system?',
         'answer': 'All zeros are in the LHP. Phase is uniquely related to magnitude (Bode gain-phase relationship). Non-minimum-phase: RHP zeros — more phase lag, harder to control.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('PID Controllers', [
        {'question': 'PID parallel form transfer function.',
         'answer': 'C(s) = Kp + Ki/s + Kds = Kp(1 + 1/(Tis) + Tds), where Ti = Kp/Ki (integral time), Td = Kd/Kp (derivative time).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Effect of proportional gain Kp.',
         'answer': 'Increases response speed, reduces SS error (but not to zero for Type 0 plant). Too high: oscillation or instability.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Effect of integral gain Ki.',
         'answer': 'Eliminates steady-state error (adds integrator → Type increases by 1). Can cause windup and slow response if too large.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Effect of derivative gain Kd.',
         'answer': 'Predicts future error, reduces overshoot and damping. Amplifies high-frequency noise — always use with a derivative filter.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Ziegler-Nichols step response method: parameters L and T.',
         'answer': 'Apply step input, fit tangent at inflection point of S-curve response. L = apparent dead time, T = apparent time constant. Then: Kp=1.2T/L, Ti=2L, Td=0.5L.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Ziegler-Nichols ultimate frequency method.',
         'answer': 'Increase Kp until sustained oscillation (Ku). Measure period Pu. PID: Kp=0.6Ku, Ti=0.5Pu, Td=0.125Pu.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is integral windup?',
         'answer': 'When actuator saturates (e.g. valve fully open), integrator keeps accumulating error → large overshoot when error reverses. Fix: back-calculation anti-windup or clamping.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Derivative filter: why is it needed?',
         'answer': 'Pure derivative C(s) = Kd·s → infinite gain at high frequencies → amplifies noise. Filtered: Kd·s/(τf·s+1), limiting gain at high frequencies.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is derivative kick and how do you avoid it?',
         'answer': 'Sudden step in setpoint causes large derivative spike (kicking the actuator). Solution: apply derivative to measurement only, not error: u_d = −Kd·dy/dt.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('State-Space Representation', [
        {'question': 'State-space equations.',
         'answer': 'ẋ = Ax + Bu (state equation); y = Cx + Du (output equation). x: state vector, u: input, y: output.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Dimensions of A, B, C, D matrices for n states, m inputs, p outputs.',
         'answer': 'A: n×n, B: n×m, C: p×n, D: p×m.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Convert G(s) = 1/(s²+3s+2) to controllable canonical form.',
         'answer': 'A=[[0,1],[-2,-3]], B=[[0],[1]], C=[1,0], D=0. State variables: x₁=y, x₂=ẏ.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State transition matrix.',
         'answer': 'Φ(t) = e^(At). Solution: x(t) = Φ(t)x(0) + ∫₀ᵗ Φ(t−τ)Bu(τ)dτ.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Controllability matrix and what it means.',
         'answer': 'Co = [B, AB, A²B, ..., A^(n-1)B]. System is controllable if rank(Co) = n (can drive any state to any other state using input u).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Observability matrix and what it means.',
         'answer': 'Ob = [C; CA; CA²; ...; CA^(n-1)]. System is observable if rank(Ob) = n (can determine initial state from output measurements).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Stability of state-space system.',
         'answer': 'System is stable if all eigenvalues of A have negative real parts (λᵢ in LHP). Eigenvalues of A = poles of the transfer function.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State feedback control: u = −Kx.',
         'answer': 'Closed-loop eigenvalues are eigenvalues of (A−BK). Choose K to place closed-loop poles at desired locations (pole placement/Ackermann\'s formula).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('MATLAB & Simulink for Control', [
        {'question': 'Create a transfer function in MATLAB.',
         'answer': "G = tf([10], [1, 3, 2]);  % G(s) = 10/(s²+3s+2)",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Create a state-space system in MATLAB.',
         'answer': "sys = ss(A, B, C, D);",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Plot Bode diagram in MATLAB.',
         'answer': "bode(G); grid on; % or bode(G, {w_min, w_max});",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Get gain and phase margin in MATLAB.',
         'answer': "[gm, pm, wpc, wgc] = margin(G); % gm in linear ratio, pm in degrees",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Plot root locus in MATLAB.',
         'answer': "rlocus(G); sgrid; % sgrid adds damping ratio and natural frequency lines",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Plot step response and get characteristics in MATLAB.',
         'answer': "step(T); stepinfo(T)  % stepinfo: RiseTime, SettlingTime, Overshoot, etc.",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Form closed-loop TF in MATLAB.',
         'answer': "T = feedback(G, H);  % negative feedback: T = G/(1+G*H). Unity: feedback(G, 1)",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Cascade and parallel combination in MATLAB.',
         'answer': "Gseries = series(G1, G2);  % or G1*G2\nGparallel = parallel(G1, G2);  % or G1+G2",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Design PID in MATLAB using pidTuner.',
         'answer': "C = pid(Kp, Ki, Kd);  % create PID\npidTuner(G, C);  % interactive tuning GUI",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0018_flashcards_embedded_systems'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
