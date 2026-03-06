from django.db import migrations


NEW_TOPICS = [
    {
        'name': 'Semiconductors',
        'code': '002B',
        'order': 11,
        'description': (
            'Intrinsic and extrinsic semiconductors, carrier transport (drift and diffusion), '
            'the pn junction at equilibrium and under bias, depletion region, built-in voltage, '
            'and junction capacitance. Foundation for understanding all semiconductor devices.'
        ),
        'prerequisites': ['Signals & Amplifiers'],
    },
    {
        'name': 'Differential Amplifiers',
        'code': '006B',
        'order': 12,
        'description': (
            'MOS and BJT differential pairs, small-signal differential and common-mode gain, '
            'CMRR, half-circuit analysis, active (current-mirror) loads, offset voltage, '
            'and the instrumentation amplifier. Core building block of all op-amp ICs.'
        ),
        'prerequisites': ['Transistor Amplifiers'],
    },
    {
        'name': 'Output Stages & Power Amplifiers',
        'code': '008B',
        'order': 13,
        'description': (
            'Class A, B, and AB output stages; push-pull complementary pairs; crossover distortion; '
            'efficiency analysis; V_BE multiplier biasing; thermal considerations and heat sinking; '
            'Class D switching amplifiers and CMOS output stages.'
        ),
        'prerequisites': ['Transistor Amplifiers', 'Feedback Amplifiers'],
    },
]

FLASHCARDS = {
    'Semiconductors': [
        {
            'question': 'What is an intrinsic semiconductor?',
            'answer': (
                'A pure semiconductor (e.g. Si, Ge) with no intentional doping. '
                'At room temperature, thermal energy breaks covalent bonds, generating '
                'electron-hole pairs (EHPs). Carrier concentration: $n = p = n_i$.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'Intrinsic carrier concentration $n_i$ for silicon at 300\,K.',
            'answer': r'$n_i \approx 1.5 \times 10^{10}\,\mathrm{cm^{-3}}$. Doubles roughly every 11\,K rise in temperature.',
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'What is an n-type semiconductor? State the majority carrier and approximate electron concentration.',
            'answer': (
                r'Doped with donor atoms (e.g. phosphorus, arsenic) that donate electrons. '
                r'Majority carriers: electrons. $n \approx N_D$ (donor concentration). '
                r'Minority carriers: holes, $p = n_i^2/N_D$.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'What is a p-type semiconductor? State the majority carrier and approximate hole concentration.',
            'answer': (
                r'Doped with acceptor atoms (e.g. boron) that accept electrons, creating holes. '
                r'Majority carriers: holes. $p \approx N_A$ (acceptor concentration). '
                r'Minority carriers: electrons, $n = n_i^2/N_A$.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'State the drift current density formula for a semiconductor.',
            'answer': (
                r'$J_{drift} = q(\mu_n n + \mu_p p)\,\mathcal{E}$, '
                r'where $\mu_n$, $\mu_p$ are electron and hole mobilities, '
                r'$n$, $p$ are carrier concentrations, and $\mathcal{E}$ is the electric field.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'State the diffusion current density formulas for electrons and holes.',
            'answer': (
                r'$J_n = qD_n\,\dfrac{dn}{dx}$ (electrons, in direction of increasing $n$). '
                r'$J_p = -qD_p\,\dfrac{dp}{dx}$ (holes, opposite sign). '
                r'$D_n$, $D_p$ are diffusion coefficients.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'State the Einstein relation connecting diffusivity and mobility.',
            'answer': (
                r'$\dfrac{D_n}{\mu_n} = \dfrac{D_p}{\mu_p} = \dfrac{kT}{q} = V_T$. '
                r'At 300\,K, $V_T \approx 26\,\mathrm{mV}$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'What is the built-in voltage $V_0$ of a pn junction?',
            'answer': (
                r'$V_0 = V_T \ln\!\left(\dfrac{N_A N_D}{n_i^2}\right)$. '
                r'Typically 0.6\u20130.8\,V for silicon. Arises from the charge double-layer '
                r'(depletion region) at the metallurgical junction.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Describe the pn junction under forward bias.',
            'answer': (
                r'Applied voltage $V_F$ reduces the barrier from $V_0$ to $V_0 - V_F$. '
                r'Depletion width narrows, minority carriers are injected across the junction, '
                r'and current increases exponentially: $I_D = I_S(e^{V_D/V_T} - 1)$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Describe the pn junction under reverse bias.',
            'answer': (
                r'Applied reverse voltage widens the depletion region, increasing the barrier to $V_0 + V_R$. '
                r'Only a small reverse saturation current $I_S$ flows (minority carrier drift). '
                r'Approximation: $I \approx -I_S$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Junction (depletion) capacitance: formula and how it varies with reverse bias.',
            'answer': (
                r'$C_j = \dfrac{C_{j0}}{\sqrt{1 + V_R/V_0}}$, where $C_{j0}$ is the zero-bias capacitance. '
                r'Capacitance decreases as reverse bias $V_R$ increases (wider depletion region). '
                r'Used in varactor diodes for voltage-controlled tuning.'
            ),
            'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Distinguish Zener breakdown from avalanche breakdown.',
            'answer': (
                r'Zener ($< 5\,\mathrm{V}$): quantum tunnelling of electrons across narrow depletion region '
                r'(high doping). Avalanche ($> 7\,\mathrm{V}$): impact ionisation — carriers accelerated by '
                r'field create new EHPs. Between 5\u20137\,V, both mechanisms contribute.'
            ),
            'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True,
        },
    ],

    'Differential Amplifiers': [
        {
            'question': r'Define differential input voltage $v_d$ and common-mode voltage $v_{cm}$ for a diff pair.',
            'answer': (
                r'$v_d = v_1 - v_2$ (difference between the two inputs). '
                r'$v_{cm} = \dfrac{v_1 + v_2}{2}$ (average of the two inputs). '
                r'Hence $v_1 = v_{cm} + v_d/2$ and $v_2 = v_{cm} - v_d/2$.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'MOS differential pair at equilibrium ($v_d = 0$): how does the tail current split?',
            'answer': (
                r'Current splits equally: $I_{D1} = I_{D2} = I_{SS}/2$, '
                r'where $I_{SS}$ is the tail current source. '
                r'Output voltages are equal: $V_{out1} = V_{out2} = V_{DD} - I_{SS}R_D/2$.'
            ),
            'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'Differential voltage gain $A_d$ of a resistively loaded MOS differential pair.',
            'answer': (
                r'$A_d = \dfrac{v_{od}}{v_d} = -g_m R_D$. '
                r'Each half-circuit is a common-source amplifier with gain $-g_m R_D$; '
                r'the differential output doubles the single-ended gain.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'Differential voltage gain $A_d$ of a resistively loaded BJT differential pair.',
            'answer': (
                r'$A_d = -g_m R_C$, where $g_m = I_C/V_T$. '
                r'Input resistance: $R_{id} = 2r_\pi$. Same form as MOS but with $R_C$ instead of $R_D$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'Common-mode gain $A_{cm}$ of a differential pair with tail resistance $R_{SS}$.',
            'answer': (
                r'$A_{cm} = -\dfrac{R_D}{2R_{SS} + 1/g_m} \approx -\dfrac{R_D}{2R_{SS}}$. '
                r'A large tail resistance $R_{SS}$ (ideally $\infty$ for a current source) '
                r'suppresses common-mode signals.'
            ),
            'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'State the CMRR of a differential pair in terms of circuit parameters.',
            'answer': (
                r'$CMRR = \left|\dfrac{A_d}{A_{cm}}\right| = g_m \cdot 2R_{SS}$. '
                r'A high-impedance tail current source maximises $R_{SS}$ and thus CMRR.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Explain the half-circuit concept for differential pair analysis.',
            'answer': (
                r'For a purely differential input, the tail node is a virtual ground. '
                r'Each transistor can be analysed as a standalone CS (or CE) amplifier '
                r'with input $v_d/2$. Differential output = $2 \times$ single-ended half-circuit output.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'How does an active (current-mirror) load improve the differential pair?',
            'answer': (
                r'A current-mirror load performs differential-to-single-ended conversion while '
                r'preserving both halves of the signal. Differential gain doubles to '
                r'$A_v = -g_m(r_{o1} \| r_{o3})$, where $r_{o1}$ and $r_{o3}$ are the output '
                r'resistances of the amplifying and mirror transistors respectively.'
            ),
            'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'What causes input offset voltage $V_{OS}$ in a differential pair?',
            'answer': (
                r'Mismatch between the two transistors: differences in $V_{tn}$ (MOS) or $V_{BE}$ (BJT), '
                r'or in $(W/L)$ ratios (MOS) or emitter areas (BJT) and load resistors. '
                r'$V_{OS}$ is the input voltage needed to force $v_{out} = 0$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'Instrumentation amplifier: topology and gain formula.',
            'answer': (
                r'Three op-amp topology: two input buffers with gain, one difference amplifier. '
                r'$A_v = \left(1 + \dfrac{2R_1}{R_G}\right)\dfrac{R_3}{R_2}$. '
                r'Gain set by single resistor $R_G$. Very high input impedance and CMRR.'
            ),
            'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True,
        },
    ],

    'Output Stages & Power Amplifiers': [
        {
            'question': 'Define a Class A output stage. What is its maximum power-conversion efficiency?',
            'answer': (
                r'The transistor conducts for the full 360\textdegree{} of the input cycle. '
                r'Max efficiency with a resistive load: $\eta_{max} = 25\%$. '
                r'With a transformer/inductive load: $\eta_{max} = 50\%$. '
                r'High linearity but poor efficiency — transistor dissipates power even with no signal.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Define a Class B output stage and describe its main drawback.',
            'answer': (
                r'Each transistor conducts for 180\textdegree{} (half cycle). '
                r'NPN handles positive half, PNP handles negative half of the output. '
                r'Drawback: crossover distortion \u2014 a dead zone near $v_{out} = 0$ '
                r'where neither transistor conducts (requires $|v_{in}| > V_{BE}$).'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'How does a Class AB output stage eliminate crossover distortion?',
            'answer': (
                r'A small quiescent bias current $I_Q$ is passed through both transistors at rest, '
                r'keeping both just on at zero input. Each transistor still handles approximately '
                r'one half-cycle, but the transition through zero is smooth. '
                r'Achieved with diode biasing or a $V_{BE}$ multiplier.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'Maximum power-conversion efficiency of a Class B output stage.',
            'answer': (
                r'$\eta_{max} = \dfrac{\pi}{4} \approx 78.5\%$, achieved when '
                r'the output amplitude $\hat{V}_o = V_{CC}$. '
                r'In general: $\eta = \dfrac{\pi}{4} \cdot \dfrac{\hat{V}_o}{V_{CC}}$.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'Power dissipated per transistor in a Class B stage. At what $\hat{V}_o$ is it maximum?',
            'answer': (
                r'$P_{D,transistor} = \dfrac{V_{CC}\hat{V}_o}{\pi R_L} - \dfrac{\hat{V}_o^2}{4R_L}$. '
                r'Maximum dissipation occurs at $\hat{V}_o = \dfrac{2V_{CC}}{\pi}$: '
                r'$P_{D,max} = \dfrac{V_{CC}^2}{\pi^2 R_L}$.'
            ),
            'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'What is the $V_{BE}$ multiplier and how is it used in Class AB biasing?',
            'answer': (
                r'A transistor $Q$ with resistors $R_1$ and $R_2$ from collector to emitter. '
                r'$V_{BB} = V_{BE}\!\left(1 + R_1/R_2\right)$. '
                r'Provides a stable, temperature-tracking bias voltage to bias both output transistors '
                r'into Class AB. The bias tracks $V_{BE}$ of the output devices, compensating for temperature.'
            ),
            'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'What is thermal runaway and how is it prevented in power amplifier stages?',
            'answer': (
                r'Thermal runaway: rising temperature increases $I_C$ \u2192 more power dissipated \u2192 '
                r'further temperature rise \u2192 device destruction. '
                r'Prevention: emitter degeneration resistors ($R_E$), $V_{BE}$ multiplier biasing '
                r'(tracks temperature), and adequate heat sinking.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': r'Thermal resistance: define $\theta_{JA}$ and write the junction temperature equation.',
            'answer': (
                r'$\theta_{JA}$ (\textdegree C/W) is the total thermal resistance from junction to ambient. '
                r'$T_J = T_A + P_D \cdot \theta_{JA}$. '
                r'To keep $T_J$ below the maximum rating, a heat sink reduces $\theta_{JA}$: '
                r'$\theta_{JA} = \theta_{JC} + \theta_{CS} + \theta_{SA}$.'
            ),
            'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Describe a Class D amplifier. What is its theoretical efficiency?',
            'answer': (
                r'A switching amplifier: output transistors operate as on/off switches driven by '
                r'a PWM signal representing the audio input. An LC reconstruction filter removes '
                r'the switching frequency. Theoretical efficiency approaches 100\% '
                r'(no voltage across a closed switch, no current through an open switch).'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
        {
            'question': 'Compare the CMOS source-follower and common-source output stages.',
            'answer': (
                r'Source follower: $A_v \approx 1$, low $R_{out} \approx 1/g_m$, low distortion, '
                r'limited output swing. Common-source: higher voltage gain, larger output swing, '
                r'but higher output resistance and more distortion. '
                r'Source follower preferred for linear output stages; CS used in Class D.'
            ),
            'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True,
        },
    ],
}


def seed_topics_and_cards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return
    course = Course.objects.filter(name='Analog Electronics', created_by=system_user).first()
    if not course:
        return

    existing_topics = {t.name: t for t in Topic.objects.filter(course=course)}

    for topic_spec in NEW_TOPICS:
        topic, created = Topic.objects.get_or_create(
            course=course,
            name=topic_spec['name'],
            defaults={
                'code': topic_spec['code'],
                'order': topic_spec['order'],
                'description': topic_spec['description'],
            }
        )

        # Set prerequisites (idempotent)
        for prereq_name in topic_spec['prerequisites']:
            prereq = existing_topics.get(prereq_name)
            if prereq:
                topic.prerequisites.add(prereq)

        # Seed flashcards (skip if already present)
        if Flashcard.objects.filter(topic=topic).exists():
            continue
        for card in FLASHCARDS.get(topic_spec['name'], []):
            Flashcard.objects.create(topic=topic, **card)


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0032_fix_analog_electronics_latex'),
    ]

    operations = [
        migrations.RunPython(seed_topics_and_cards, reverse_fn),
    ]
