from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return

    course = Course.objects.filter(
        name='Electrical Machines & Motors', created_by=system_user
    ).first()
    if not course:
        return

    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    def add_cards(topic_name, cards):
        topic = topics.get(topic_name)
        if not topic or Flashcard.objects.filter(topic=topic).exists():
            return
        for card in cards:
            Flashcard.objects.create(topic=topic, **card)

    # -------------------------------------------------------------------------
    # 1. Transformer Theory
    # -------------------------------------------------------------------------
    add_cards('Transformer Theory', [
        {
            'question': 'State the ideal transformer voltage ratio.',
            'answer': 'V1/V2 = N1/N2 = a, where a is the turns ratio, V1 is primary voltage, V2 is secondary voltage, N1 and N2 are turns counts.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is the ideal transformer current ratio?',
            'answer': 'I1/I2 = N2/N1 = 1/a. Primary and secondary ampere-turns are equal: N1·I1 = N2·I2.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'How is the impedance reflected through an ideal transformer?',
            'answer': 'Z_primary = a²·Z_secondary. A load impedance ZL on the secondary appears as a²ZL at the primary terminals.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is the EMF equation of a transformer?',
            'answer': 'E = 4.44·f·N·Φm, where f is supply frequency (Hz), N is turns, Φm is peak flux (Wb). Derived from Faraday\'s law with sinusoidal flux.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Describe the transformer equivalent circuit referred to the primary side.',
            'answer': 'Series resistance R1 + a²R2, series leakage reactance X1 + a²X2, shunt magnetising reactance Xm, and core-loss resistance Rc — all in parallel at the primary terminals. The secondary load appears as a²ZL.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What information does the open-circuit (no-load) test on a transformer provide?',
            'answer': 'The no-load test gives core losses (Pcore = V0·I0·cosφ0) and the magnetising branch parameters Rc and Xm. It is performed at rated voltage on one winding with the other open.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What does the short-circuit test on a transformer determine?',
            'answer': 'The short-circuit test gives copper losses at rated current and the series parameters (Req = Psc/Isc², Zeq = Vsc/Isc). The test is performed at reduced voltage with the secondary short-circuited.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Define voltage regulation of a transformer.',
            'answer': 'VR = (V2_no-load − V2_full-load) / V2_full-load × 100%. Good transformers have low VR (1–5%). Approximate formula: VR ≈ εR·cosφ + εX·sinφ, where εR and εX are per-unit resistance and reactance.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'At what load does transformer efficiency reach its maximum?',
            'answer': 'Maximum efficiency occurs when variable copper losses equal fixed core losses: I²Req = Pcore. So the optimal load = rated load × √(Pcore/Pcu_rated).',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Explain the difference between core-type and shell-type transformer construction.',
            'answer': 'Core-type: windings surround the magnetic core limbs — simple construction, used for HV/large units. Shell-type: core surrounds the windings on three sides — better short-circuit strength, used for LV/distribution transformers.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Derive the per-unit efficiency of a transformer.',
            'answer': '',
            'hint': 'η = Output / Input = Output / (Output + Losses)',
            'difficulty': 'hard',
            'question_type': 'step_by_step',
            'uses_latex': True,
            'steps': [
                {'move': 'Write output power', 'detail': 'Pout = V2·I2·cosφ2'},
                {'move': 'Identify losses', 'detail': 'Plosses = Pcore + I2²·Req (copper loss)'},
                {'move': 'Write efficiency', 'detail': 'η = Pout / (Pout + Pcore + I2²·Req)'},
                {'move': 'Substitute x = load fraction', 'detail': 'η(x) = x·S·cosφ / (x·S·cosφ + Pcore + x²·Pcu_rated)'},
                {'move': 'Maximise', 'detail': 'dη/dx = 0 ⟹ x² · Pcu_rated = Pcore ⟹ x = √(Pcore/Pcu_rated)'},
            ],
            'teacher_explanation': 'The load fraction x = 1 corresponds to rated load. Maximum efficiency load is often 50–75% of rated load in distribution transformers.',
        },
        {
            'question': 'What is an autotransformer and what is its advantage over a two-winding transformer?',
            'answer': 'An autotransformer has a single tapped winding shared between primary and secondary. Advantage: smaller size and higher efficiency because part of the power is transferred conductively, not magnetically. Disadvantage: no electrical isolation between primary and secondary.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What conditions must be met for transformers to operate in parallel?',
            'answer': '1) Same voltage ratio (turns ratio). 2) Same per-unit impedance. 3) Same polarity (dot convention). 4) Same phase sequence (three-phase). If impedances differ, load sharing is inversely proportional to impedance.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Why are transformer cores laminated?',
            'answer': 'Lamination divides the core into thin insulated sheets, increasing path resistance for eddy currents. Eddy current loss ∝ (thickness)², so thin laminations drastically reduce these losses.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': True,
        },
    ])

    # -------------------------------------------------------------------------
    # 2. DC Machines
    # -------------------------------------------------------------------------
    add_cards('DC Machines', [
        {
            'question': 'Write the EMF equation for a DC generator.',
            'answer': 'E = (P·φ·N·Z) / (60·A), where P = poles, φ = flux per pole (Wb), N = speed (rpm), Z = total conductors, A = parallel paths (A=2 for wave winding, A=P for lap winding).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is the torque equation of a DC motor?',
            'answer': 'T = (P·φ·Ia·Z) / (2π·A). For a given machine, T ∝ φ·Ia. At constant flux (shunt motor), torque is proportional to armature current.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Write the voltage equation for a DC motor and explain back-EMF.',
            'answer': 'V = Eb + Ia·Ra, where V is supply voltage, Eb is back-EMF (Eb = kφN), Ia is armature current, Ra is armature resistance. Back-EMF opposes supply; it regulates current without external resistance losses.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Compare the speed-torque characteristics of DC shunt, series, and compound motors.',
            'answer': 'Shunt: nearly constant speed (slight droop) — good for fans, pumps. Series: speed falls sharply with load (high starting torque) — traction. Compound: intermediate — combines shunt stability with series starting torque.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Why should a DC series motor never be started at no load?',
            'answer': 'At no load, torque = 0 ⟹ Ia ≈ 0. Since Eb = V − Ia·Ra ≈ V, and Eb ∝ φ·N, with very low flux (series connection) N → ∞. The motor can reach dangerously high (runaway) speeds.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'List three methods of speed control for DC shunt motors.',
            'answer': '1) Field weakening — reduce field current ⟹ increase speed (above base speed). 2) Armature voltage control — reduce Va ⟹ reduce speed (below base speed). 3) Armature resistance insertion — inefficient, used for starting only.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the purpose of a starter for DC motors?',
            'answer': 'At standstill, Eb = 0, so Ia = V/Ra which is very large and can damage the armature. A starter inserts external resistance in series with the armature at startup, limiting current to a safe value, then progressively shorts out the resistance as speed (and Eb) builds up.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Define armature reaction in a DC machine and state its effects.',
            'answer': 'Armature reaction: the armature MMF distorts and weakens the main field flux. Effects: 1) Shifts the magnetic neutral axis (MNA) in the direction of rotation for motors. 2) Reduces average flux per pole (flux weakening). 3) Can cause commutation sparking.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Derive the efficiency of a DC generator given its losses.',
            'answer': '',
            'hint': 'η = Pout / Pin = Pout / (Pout + total losses)',
            'difficulty': 'hard',
            'question_type': 'step_by_step',
            'uses_latex': True,
            'steps': [
                {'move': 'Identify output', 'detail': 'Pout = VL·IL (terminal voltage × load current)'},
                {'move': 'List losses', 'detail': 'Copper: Ia²·Ra + field losses. Iron & mechanical: Pstray (constant)'},
                {'move': 'Note Ia = IL + If (shunt generator)', 'detail': 'Field current If = Vf/Rf drawn from armature terminals'},
                {'move': 'Input power', 'detail': 'Pin = Pout + Ia²·Ra + If·Vf + Pstray'},
                {'move': 'Efficiency', 'detail': 'η = Pout / Pin × 100%'},
            ],
        },
        {
            'question': 'What is the function of the commutator in a DC machine?',
            'answer': 'The commutator converts the AC generated in the rotating armature coils into DC at the output terminals (generator), or converts DC supply into AC for the rotating armature (motor). Brushes make sliding contact with the commutator segments.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 3. AC Induction Motors
    # -------------------------------------------------------------------------
    add_cards('AC Induction Motors', [
        {
            'question': 'What creates the rotating magnetic field (RMF) in a three-phase induction motor?',
            'answer': 'Three-phase balanced currents in spatially displaced (120°) stator windings produce an MMF that rotates at synchronous speed Ns = 120f/P, where f is supply frequency and P is poles.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Define slip in an induction motor.',
            'answer': 's = (Ns − Nr) / Ns, where Ns is synchronous speed and Nr is rotor speed. At standstill s = 1; at no load s ≈ 0. Full-load slip is typically 2–8%.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is the frequency of the induced rotor EMF and currents at slip s?',
            'answer': 'f_rotor = s·f, where f is stator supply frequency. At standstill (s=1): rotor frequency = supply frequency. At full load (s≈0.05): rotor frequency ≈ 0.05×50 = 2.5 Hz.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Explain the equivalent circuit of an induction motor.',
            'answer': 'The stator circuit: R1 + jX1 in series with the magnetising branch (Rc ∥ jXm). The rotor is modelled as R2/s + jX2 (all referred to stator). The resistive part R2(1−s)/s represents mechanical power output.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Derive the power flow in an induction motor.',
            'answer': '',
            'hint': 'Air-gap power splits between rotor copper loss and mechanical output',
            'difficulty': 'hard',
            'question_type': 'step_by_step',
            'uses_latex': True,
            'steps': [
                {'move': 'Input power', 'detail': 'Pin = √3·VL·IL·cosφ (three-phase)'},
                {'move': 'Stator copper loss', 'detail': 'Pcu1 = 3·I1²·R1'},
                {'move': 'Core loss', 'detail': 'Pcore (usually included in stator or treated separately)'},
                {'move': 'Air-gap power', 'detail': 'Pag = Pin − Pcu1 − Pcore'},
                {'move': 'Rotor copper loss', 'detail': 'Pcu2 = s·Pag'},
                {'move': 'Mechanical power', 'detail': 'Pmech = (1−s)·Pag'},
                {'move': 'Shaft power (deduct friction)', 'detail': 'Pshaft = Pmech − Pfriction&windage'},
                {'move': 'Torque', 'detail': 'T = Pag / ωs (synchronous angular speed)'},
            ],
        },
        {
            'question': 'What is the significance of the torque-speed curve of an induction motor?',
            'answer': 'The curve shows: starting torque at s=1, maximum (pull-out) torque at s_max_T = R2/X2, and stable operating region between s=0 and s_max_T. The motor operates on the falling-torque (stable) region under normal load.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'List four methods of starting large induction motors.',
            'answer': '1) DOL (direct-on-line): high starting current (6–8×FL). 2) Star-delta: reduces voltage to 1/√3, starting current reduced to 1/3 of DOL. 3) Autotransformer starter: variable reduction. 4) Soft starter (electronic): smooth ramp-up.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'How does rotor resistance affect the torque-speed curve?',
            'answer': 'Increasing rotor resistance shifts the peak torque to higher slip without changing its magnitude. Higher R2 ⟹ higher starting torque but more rotor copper loss. Wound-rotor motors use external resistance for speed control.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is the effect of changing supply voltage on induction motor performance?',
            'answer': 'Torque ∝ V². A 10% reduction in voltage reduces torque by ~19%. The motor draws more current to develop rated torque at reduced voltage, risking overheating. Starting torque is severely affected.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Why is the power factor of an induction motor poor at light loads?',
            'answer': 'At light load, the motor draws a large magnetising current (reactive) relative to the small active load current. The ratio of reactive to active power is high, giving a low (lagging) power factor, typically 0.2–0.4 at no load.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 4. Synchronous Machines
    # -------------------------------------------------------------------------
    add_cards('Synchronous Machines', [
        {
            'question': 'What is the synchronous speed formula?',
            'answer': 'Ns = 120f/P (rpm) or ωs = 2πf/(P/2) (rad/s), where f is supply frequency and P is number of poles.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Write the phasor equation for a synchronous generator.',
            'answer': 'Ef = Vt + Ia·(Ra + jXs), where Ef is internal EMF, Vt is terminal voltage, Ia is armature current, Ra is armature resistance, Xs is synchronous reactance.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Define the power angle δ of a synchronous machine.',
            'answer': 'δ is the angle between the internal EMF phasor Ef and the terminal voltage Vt. For a generator, Ef leads Vt by δ. For a motor, Vt leads Ef by δ. Stability requires δ < 90°.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Write the power-angle equation for a synchronous generator connected to an infinite bus.',
            'answer': 'P = (Ef·Vt / Xs)·sinδ. Maximum power (pull-out) = Ef·Vt / Xs at δ = 90°. (Assuming Ra ≈ 0)',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'How does a synchronous generator supply reactive power to the grid?',
            'answer': 'Over-excitation (Ef > Vt): machine exports lagging reactive power — acts as a capacitor to the grid. Under-excitation (Ef < Vt): machine absorbs reactive power — acts as an inductor. A synchronous compensator (no mechanical load) provides only reactive power.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'List the conditions required to synchronise a generator to the grid.',
            'answer': '1) Equal voltage magnitudes. 2) Equal frequencies. 3) Correct phase sequence. 4) Phase voltages in phase (zero phase difference). All four conditions must be met simultaneously before the breaker is closed.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the V-curve of a synchronous motor?',
            'answer': 'A plot of armature current vs field current at constant power. The minimum armature current occurs at unity power factor. Over-excitation (right) gives leading PF (capacitive); under-excitation (left) gives lagging PF (inductive). The curves shift up with increasing load.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a salient-pole synchronous machine and how does it differ from a cylindrical-rotor machine?',
            'answer': 'Salient-pole: projecting poles, non-uniform air gap ⟹ d-axis and q-axis reactances differ (Xd ≠ Xq). Used in slow-speed hydro generators and motors. Cylindrical (round rotor): uniform air gap, Xd = Xq = Xs. Used in high-speed turbogenerators.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Why are synchronous motors not self-starting?',
            'answer': 'The rotating stator field changes direction faster than the rotor (with rotor inertia) can follow. The net average starting torque is zero. Solutions: add damper windings (amortisseur) for induction starting, or use a VFD to ramp up frequency from zero.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 5. Motor Starting & Protection
    # -------------------------------------------------------------------------
    add_cards('Motor Starting & Protection', [
        {
            'question': 'What protection devices are typically used for three-phase induction motors?',
            'answer': '1) Overload relay (thermal/electronic) — trips on sustained over-current. 2) Short-circuit fuses or MCB. 3) Under-voltage relay. 4) Phase failure/unbalance relay. 5) Earth fault protection. Combined in a motor protection relay (MPR) for large motors.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the purpose of a thermal overload relay?',
            'answer': 'It monitors motor current and accumulates a thermal model. If current exceeds the set value for a time determined by the thermal curve (I²t characteristic), the relay trips the contactor to protect the motor windings from overheating.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Describe a star-delta (Y-Δ) starter and its limitation.',
            'answer': 'Motor starts in star connection: phase voltage = VL/√3. After reaching ~80% speed, switches to delta. Starting current and torque are each reduced to 1/3 of DOL values. Limitation: abrupt current transient at transition; unsuitable for high-inertia loads.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'How does a soft starter reduce starting current?',
            'answer': 'Back-to-back SCRs (thyristors) in each phase are phase-angle fired to gradually ramp up the RMS voltage applied to the motor, limiting in-rush current. Once at rated speed, they fully conduct or a bypass contactor closes.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the duty cycle (S1–S9) classification for motors?',
            'answer': 'IEC defines 9 duty types: S1=continuous, S2=short-time, S3=intermittent periodic, S4–S8=various intermittent/load/speed variations, S9=non-periodic. Duty cycle affects thermal sizing of the motor.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is IP rating for motors and what does IP55 mean?',
            'answer': 'IP (Ingress Protection) rating: IP XY. First digit X = solid particle protection (0–6). Second digit Y = liquid ingress protection (0–9). IP55: protected against dust ingress sufficient to prevent harmful deposits (5) and water jets from all directions (5).',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What causes single-phasing in a three-phase motor and what are its effects?',
            'answer': 'Single-phasing: one supply phase is lost (blown fuse, open contact). The motor continues to run on two phases, drawing unbalanced current — the remaining phases carry ~173% of rated current, causing rapid overheating and possible winding burnout.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
    ])

    # -------------------------------------------------------------------------
    # 6. Variable Speed Drives
    # -------------------------------------------------------------------------
    add_cards('Variable Speed Drives', [
        {
            'question': 'What is a Variable Speed Drive (VSD) and why is it used?',
            'answer': 'A VSD (also VFD — Variable Frequency Drive) controls motor speed by varying the supply frequency and voltage. Benefits: precise speed control, soft starting, energy savings (centrifugal fans/pumps: P ∝ N³), reduced mechanical stress.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Explain the V/f (volts per hertz) control strategy for induction motors.',
            'answer': 'Maintaining a constant V/f ratio keeps air-gap flux constant, preventing magnetic saturation at low frequencies and maintaining torque capability. Above base speed, voltage is limited at rated value while frequency increases (field weakening).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is the basic block structure of a standard VFD?',
            'answer': 'Rectifier (AC→DC) → DC link (capacitor/inductor filter) → Inverter (DC→variable frequency AC via PWM IGBTs). Single-phase or three-phase input; three-phase output.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is PWM (Pulse Width Modulation) in a VFD inverter?',
            'answer': 'The DC bus voltage is switched ON/OFF at high frequency (typically 2–16 kHz) using IGBTs. The duty cycle of the pulses is varied to create an averaged sinusoidal output at the desired frequency and voltage. Higher carrier frequency gives lower harmonic distortion but more switching losses.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is vector (field-oriented) control and how does it differ from V/f control?',
            'answer': 'Vector control independently controls flux-producing and torque-producing current components (d-q decomposition), mimicking separately-excited DC motor control. Provides fast dynamic response and accurate torque control, unlike V/f which is open-loop and slower.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Calculate the energy savings from using a VFD on a centrifugal pump running at 80% speed vs full speed.',
            'answer': '',
            'hint': 'Centrifugal law: P ∝ N³',
            'difficulty': 'medium',
            'question_type': 'step_by_step',
            'uses_latex': True,
            'steps': [
                {'move': 'State affinity laws', 'detail': 'Flow Q ∝ N, Head H ∝ N², Power P ∝ N³'},
                {'move': 'Power ratio', 'detail': 'P_80 / P_100 = (0.8)³ = 0.512'},
                {'move': 'Energy saving', 'detail': 'Saving = 1 − 0.512 = 0.488 = 48.8%'},
                {'move': 'Practical note', 'detail': 'Actual savings slightly less due to VFD losses (~2–5%)'},
            ],
            'teacher_explanation': 'This is the cubic law. Throttling a valve instead wastes power across the valve; a VFD reduces actual power consumption.',
        },
        {
            'question': 'What VFD parameters must be set when commissioning a motor?',
            'answer': 'Minimum: motor rated voltage, rated current, rated frequency, rated power (kW), number of poles (or rated speed). Additional: acceleration/deceleration ramp times, carrier frequency, control mode (V/f or vector), thermal overload setting.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What harmonic problems do VFDs cause and how are they mitigated?',
            'answer': 'VFD input rectifiers draw non-sinusoidal current, injecting low-order voltage harmonics (5th, 7th, 11th…) into the supply. Mitigation: AC/DC line reactors, 12-pulse rectifiers, passive/active harmonic filters, LCL filters on active front ends.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0019_flashcards_control_systems'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
