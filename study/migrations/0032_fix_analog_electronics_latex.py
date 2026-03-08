from django.db import migrations

# Maps each Analog Electronics topic to a list of card updates.
# 'q'      — exact question text as seeded in 0016 (used to find the card)
# 'a'      — new answer with proper $...$ LaTeX
# 'new_q'  — (optional) replacement question text when the question itself had math
# 'steps'  — (optional) replacement steps list for step_by_step cards
LATEX_UPDATES = {
    'Signals & Amplifiers': [
        {
            'q': 'Define voltage gain Av of an amplifier.',
            'a': r'$A_v = V_{out}/V_{in}$. Often expressed in dB: $A_{dB} = 20\log_{10}|A_v|$.',
        },
        {
            'q': 'What is the power gain in dB?',
            'a': r'$A_p\,(\mathrm{dB}) = 10\log_{10}(P_{out}/P_{in}) = 10\log_{10}(A_v \times A_i)$.',
        },
        {
            'q': 'An amplifier has Av = 200. What is the gain in dB?',
            'a': r'$20\log_{10}(200) = 20 \times 2.301 = 46\,\mathrm{dB}$.',
        },
        {
            'q': 'Describe the Thevenin amplifier model.',
            'a': r'Input: $R_{in}$ in parallel with input terminals. Output: dependent voltage source $A_v V_{in}$ in series with $R_{out}$.',
        },
        {
            'q': 'Why does high input resistance and low output resistance matter?',
            'a': r'High $R_{in}$: minimal loading of source ($V_{in} \approx V_{source}$). Low $R_{out}$: delivers maximum voltage to load ($V_{out} \approx A_v V_{in}$ even with small $R_L$).',
        },
        {
            'q': 'Define the \u22123dB bandwidth of an amplifier.',
            'a': r'The frequency range over which gain $\geq A_{max}/\sqrt{2}$ (i.e., power $\geq$ half max). $BW = f_H - f_L$.',
        },
        {
            'q': 'Define gain-bandwidth product (GBP).',
            'a': r'$GBP = A_v \times BW$. For a single-pole amplifier, GBP is constant \u2014 increasing gain reduces bandwidth.',
        },
        {
            'q': 'What is the difference between a voltage amplifier, current amplifier, and transconductance amplifier?',
            'a': r'Voltage amp: $V_{in} \to V_{out}$ ($A_v$). Current amp: $I_{in} \to I_{out}$ ($A_i$). Transconductance: $V_{in} \to I_{out}$ ($G_m$). Transresistance: $I_{in} \to V_{out}$ ($R_m$).',
        },
    ],

    'Operational Amplifiers': [
        {
            'q': 'State the two ideal op-amp rules.',
            'a': r'1) $V^+ = V^-$ (virtual short: input differential voltage = 0). 2) $I^+ = I^- = 0$ (infinite input impedance: no current into inputs).',
        },
        {
            'q': 'Gain of the inverting op-amp amplifier.',
            'a': r'$A_v = -R_f/R_1$. Output is inverted relative to input.',
        },
        {
            'q': 'Gain of the non-inverting op-amp amplifier.',
            'a': r'$A_v = 1 + R_f/R_1$. Output is in phase with input.',
        },
        {
            'q': 'What is a unity-gain buffer (voltage follower)?',
            'a': r'Non-inverting amp with $R_f = 0$ and $R_1 = \infty$: $A_v = 1$. Very high $R_{in}$, very low $R_{out}$ \u2014 used for impedance matching.',
        },
        {
            'q': 'Summing amplifier output with inputs V\u2081, V\u2082 through R\u2081, R\u2082, feedback Rf.',
            'a': r'$V_{out} = -R_f\!\left(\dfrac{V_1}{R_1} + \dfrac{V_2}{R_2}\right)$. Weighted sum (inverted).',
        },
        {
            'q': 'Difference amplifier: output for V\u2081 on inverting, V\u2082 on non-inverting (all equal resistors R).',
            'a': r'$V_{out} = V_2 - V_1$. CMRR is key \u2014 rejects common-mode signals.',
        },
        {
            'q': 'Ideal integrator op-amp circuit: output in terms of input.',
            'a': r'$V_{out}(t) = -\dfrac{1}{RC}\int V_{in}\,dt$. Feedback element is capacitor $C$; input resistor $R$.',
        },
        {
            'q': 'Ideal differentiator op-amp circuit: output.',
            'a': r'$V_{out}(t) = -RC\,\dfrac{dV_{in}}{dt}$. Input element is capacitor $C$; feedback resistor $R$.',
        },
        {
            'q': 'Define CMRR (Common Mode Rejection Ratio).',
            'a': r'$CMRR = A_d/A_{cm}$, where $A_d$ = differential gain, $A_{cm}$ = common-mode gain. High CMRR rejects noise common to both inputs.',
        },
        {
            'q': 'Define slew rate of an op-amp.',
            'a': r'Maximum rate of change of output voltage: $SR = \left.\dfrac{dV_{out}}{dt}\right|_{max}$. Typically measured in V/\u03bcs. Limits performance at high frequencies.',
        },
        {
            'q': 'An inverting amplifier has R\u2081=1k\u03a9, Rf=10k\u03a9. Find Av and output for Vin=0.5V.',
            'new_q': r'An inverting amplifier has $R_1 = 1\,\mathrm{k\Omega}$, $R_f = 10\,\mathrm{k\Omega}$. Find $A_v$ and output for $V_{in} = 0.5\,\mathrm{V}$.',
            'a': r'$A_v = -10$. $V_{out} = -10 \times 0.5 = -5\,\mathrm{V}$.',
        },
    ],

    'Diodes': [
        {
            'q': 'State the Shockley diode equation.',
            'a': r'$I_D = I_S\!\left(e^{V_D/V_T} - 1\right)$, where $V_T = kT/q \approx 26\,\mathrm{mV}$ at room temperature (300\,K).',
        },
        {
            'q': 'Half-wave rectifier: peak output voltage (ideal diode, Vs = Vm sin \u03c9t).',
            'a': r'$V_p = V_m$ (ideal) or $V_m - 0.7\,\mathrm{V}$ (constant $V_D$ model). Conducts only positive half cycles.',
        },
        {
            'q': 'Full-wave bridge rectifier: peak output voltage.',
            'a': r'$V_p = V_m - 2 \times 0.7 = V_m - 1.4\,\mathrm{V}$ (two diodes in series conduct each half cycle).',
        },
        {
            'q': 'Ripple voltage formula for a rectifier with capacitor filter.',
            'a': r'$V_r \approx V_p/(fRC)$ where $f$ = supply frequency (100\,Hz for full-wave at 50\,Hz), $R$ = load, $C$ = filter cap.',
        },
        {
            'q': 'Design a Zener regulator: Vs=12V, Vz=5V, IL=20mA. Find series resistor R.',
            'new_q': r'Design a Zener regulator: $V_s = 12\,\mathrm{V}$, $V_z = 5\,\mathrm{V}$, $I_L = 20\,\mathrm{mA}$. Find series resistor $R$.',
            'a': r'$V_R = 7\,\mathrm{V}$. Assume $I_Z(\min) \approx 5\,\mathrm{mA}$. $I_{total} = 25\,\mathrm{mA}$. $R = 7/0.025 = 280\,\Omega$.',
            'steps': [
                {'move': 'Voltage across R',
                 'detail': r'$V_R = V_s - V_z = 12 - 5 = 7\,\mathrm{V}$'},
                {'move': 'Total current (load + min Zener)',
                 'detail': r'$I = I_L + I_Z = 20 + 5 = 25\,\mathrm{mA}$'},
                {'move': 'Find R',
                 'detail': r'$R = V_R/I = 7\,\mathrm{V}/0.025\,\mathrm{A} = 280\,\Omega$'},
            ],
        },
        {
            'q': 'What is the small-signal diode resistance rd?',
            'a': r'$r_d = V_T/I_D$. At $I_D = 1\,\mathrm{mA}$: $r_d = 26\,\mathrm{mV}/1\,\mathrm{mA} = 26\,\Omega$. Lower $I_D \to$ higher $r_d$.',
        },
    ],

    'MOSFETs': [
        {
            'q': 'What is the threshold voltage Vtn of an nMOS transistor?',
            'a': r'The minimum $V_{GS}$ required to create an inversion layer (channel) and allow drain current to flow.',
        },
        {
            'q': 'What are the two operating regions of a MOSFET (above threshold)?',
            'a': r'Triode (linear): $V_{DS} < V_{GS} - V_{tn}$. Saturation: $V_{DS} \geq V_{GS} - V_{tn}$ (channel pinched off).',
        },
        {
            'q': 'Drain current in MOSFET saturation region.',
            'a': r'$I_D = \dfrac{k_n}{2}(V_{GS} - V_{tn})^2$, where $k_n = \mu_n C_{ox}(W/L)$. Independent of $V_{DS}$ (ideal).',
        },
        {
            'q': 'Drain current in MOSFET triode region.',
            'a': r'$I_D = k_n\!\left[(V_{GS} - V_{tn})V_{DS} - \dfrac{V_{DS}^2}{2}\right]$. Increases with $V_{DS}$.',
        },
        {
            'q': 'Define transconductance gm of a MOSFET.',
            'a': r'$g_m = \left.\dfrac{\partial I_D}{\partial V_{GS}}\right|_{V_{DS}} = k_n(V_{GS} - V_{tn}) = \dfrac{2I_D}{V_{GS} - V_{tn}} = \sqrt{2k_n I_D}$.',
        },
        {
            'q': 'Define output resistance ro of a MOSFET (Early effect).',
            'a': r'$r_o = |V_A|/I_D$ where $V_A$ is the Early voltage. Accounts for channel-length modulation (slight increase in $I_D$ with $V_{DS}$).',
        },
        {
            'q': 'Describe the MOSFET small-signal model.',
            'a': r'Gate: open circuit. $g_m v_{gs}$ dependent current source from drain to source. $r_o$ from drain to source. No $C_{gs}/C_{gd}$ in mid-band model.',
        },
        {
            'q': 'How does a pMOS transistor differ from nMOS?',
            'a': r'pMOS: $V_{GS} < V_{tp}$ ($V_{tp} < 0$), $V_{SD} > 0$, current flows from source to drain. Holes are carriers. IV characteristic mirrors nMOS.',
        },
        {
            'q': 'What is the body effect in MOSFETs?',
            'a': r'Source-to-body reverse bias increases $V_{tn}$ (for nMOS). $V_{tn} = V_{tn0} + \gamma\!\left(\sqrt{2\phi_F + V_{SB}} - \sqrt{2\phi_F}\right)$.',
        },
        {
            'q': 'A MOSFET has kn=2mA/V\u00b2, Vtn=1V. Find ID when VGS=3V in saturation.',
            'new_q': r'A MOSFET has $k_n = 2\,\mathrm{mA/V^2}$, $V_{tn} = 1\,\mathrm{V}$. Find $I_D$ when $V_{GS} = 3\,\mathrm{V}$ in saturation.',
            'a': r'$I_D = \dfrac{2}{2}(3-1)^2 = 1 \times 4 = 4\,\mathrm{mA}$.',
        },
    ],

    'Bipolar Junction Transistors (BJTs)': [
        {
            'q': 'State the conditions for BJT active (forward-active) region.',
            'a': r'BE junction forward biased ($V_{BE} \approx 0.7\,\mathrm{V}$); BC junction reverse biased ($V_{CE} > V_{CE,sat} \approx 0.2\,\mathrm{V}$).',
        },
        {
            'q': 'BJT collector current equation in active region.',
            'a': r'$I_C = I_S\,e^{V_{BE}/V_T}$. Also $I_C = \beta I_B$.',
        },
        {
            'q': 'Define \u03b2 (current gain) and \u03b1 for a BJT.',
            'a': r'$\beta = I_C/I_B$ (common-emitter current gain). $\alpha = I_C/I_E = \beta/(\beta+1)$ (common-base current gain). $I_E = I_C + I_B$.',
        },
        {
            'q': 'BJT transconductance gm.',
            'a': r'$g_m = I_C/V_T$. At $I_C = 1\,\mathrm{mA}$: $g_m = 1\,\mathrm{mA}/26\,\mathrm{mV} \approx 38.5\,\mathrm{mA/V}$.',
        },
        {
            'q': 'BJT small-signal input resistance r\u03c0.',
            'a': r'$r_\pi = \beta/g_m = V_T/I_B$.',
        },
        {
            'q': 'BJT small-signal model (T-model or hybrid-\u03c0).',
            'a': r'Hybrid-$\pi$: $r_\pi$ between B and E; $g_m v_{be}$ current source from C to E; $r_o$ from C to E.',
        },
        {
            'q': 'Describe the four-resistor bias network for a BJT.',
            'a': r'$R_1$ and $R_2$ form a voltage divider to set $V_B$. $R_E$ provides emitter degeneration for stability. $R_C$ is the collector load. $V_B \approx V_{CC} \times R_2/(R_1 + R_2)$.',
        },
        {
            'q': 'DC bias analysis: find IC for BJT with VCC=12V, R1=10k\u03a9, R2=5k\u03a9, RE=1k\u03a9, \u03b2=100.',
            'new_q': r'DC bias analysis: find $I_C$ for BJT with $V_{CC}=12\,\mathrm{V}$, $R_1=10\,\mathrm{k\Omega}$, $R_2=5\,\mathrm{k\Omega}$, $R_E=1\,\mathrm{k\Omega}$, $\beta=100$.',
            'a': r'$V_B = 4\,\mathrm{V}$. $V_E = 3.3\,\mathrm{V}$. $I_E = 3.3\,\mathrm{mA}$. $I_C \approx 3.3\,\mathrm{mA}$.',
            'steps': [
                {'move': 'Find $V_B$ via voltage divider',
                 'detail': r'$V_B = 12 \times 5\,\mathrm{k\Omega}/(10\,\mathrm{k\Omega}+5\,\mathrm{k\Omega}) = 4\,\mathrm{V}$'},
                {'move': 'Find $V_E$',
                 'detail': r'$V_E = V_B - V_{BE} = 4 - 0.7 = 3.3\,\mathrm{V}$'},
                {'move': 'Find $I_E$',
                 'detail': r'$I_E = V_E/R_E = 3.3\,\mathrm{V}/1\,\mathrm{k\Omega} = 3.3\,\mathrm{mA}$'},
                {'move': 'Approximate $I_C$',
                 'detail': r'$I_C \approx \alpha I_E \approx I_E = 3.3\,\mathrm{mA}$ (for large $\beta$)'},
            ],
        },
        {
            'q': 'What is the Early effect in BJTs?',
            'a': r'$I_C$ increases slightly with $V_{CE}$ due to base-width modulation. $r_o = V_A/I_C$ where $V_A$ is Early voltage (typically 50\u2013200\,V).',
        },
        {
            'q': 'BJT in saturation: what are the conditions and VCE,sat?',
            'a': r'Both BE and BC junctions are forward biased. $V_{CE,sat} \approx 0.1$\u2013$0.2\,\mathrm{V}$. $I_B > I_C/\beta$ (forced $\beta$ < rated $\beta$).',
        },
    ],

    'Transistor Amplifiers': [
        {
            'q': 'Voltage gain of common-emitter (CE) BJT amplifier (no RE bypass).',
            'a': r'$A_v = -g_m(R_C \| r_o) \approx -g_m R_C$. Negative sign = phase inversion.',
        },
        {
            'q': 'Input resistance of common-emitter BJT amplifier.',
            'a': r'$R_{in} = R_1 \| R_2 \| r_\pi$.',
        },
        {
            'q': 'Voltage gain of common-base (CB) BJT amplifier.',
            'a': r'$A_v \approx +g_m R_C$ (positive). Very low input resistance ($\approx 1/g_m$), high output resistance.',
        },
        {
            'q': 'Voltage gain of emitter follower (common-collector) BJT.',
            'a': r'$A_v \approx \dfrac{R_E}{R_E + 1/g_m} \approx 1$ for large $R_E$. High $R_{in}$, low $R_{out}$ \u2014 used as buffer.',
        },
        {
            'q': 'Voltage gain of common-source (CS) MOSFET amplifier.',
            'a': r'$A_v = -g_m(R_D \| r_o) \approx -g_m R_D$.',
        },
        {
            'q': 'Voltage gain of source follower (common-drain) MOSFET.',
            'a': r'$A_v \approx \dfrac{g_m R_S}{1 + g_m R_S} \approx 1$. Low $R_{out} \approx 1/g_m$, high $R_{in}$.',
        },
        {
            'q': 'How does a current mirror work?',
            'a': r'Reference transistor $Q_1$ is diode-connected ($V_{BE1}$ set by $I_{ref}$). $Q_2$ copies this $V_{BE}$ \u2192 $I_{C2} = I_{C1} \times (W/L)_2/(W/L)_1$.',
        },
        {
            'q': 'Effect of emitter degeneration resistance RE on CE amplifier.',
            'a': r'$A_v \approx -R_C/R_E$ (reduced gain but improved linearity and stability). $R_{in}$ increases: $R_{in} \approx \beta(R_E + 1/g_m)$.',
        },
    ],

    'Frequency Response of Amplifiers': [
        {
            'q': 'What is the Miller effect?',
            'a': r'An impedance $Z$ connected between input and output of an inverting amplifier appears at the input as $Z/(1-A_v)$, effectively multiplying capacitance by $(1-A_v)$.',
        },
        {
            'q': 'Miller capacitance for Cgd in a CS amplifier with gain Av.',
            'a': r'$C_{in,Miller} = C_{gd}(1 - A_v) = C_{gd}(1 + |A_v|)$. Dominates high-frequency input capacitance.',
        },
        {
            'q': 'What limits the high-frequency response of an amplifier?',
            'a': r'Parasitic capacitances ($C_{gs}$, $C_{gd}$ for MOSFETs; $C_\pi$, $C_\mu$ for BJTs) and Miller effect. Create poles that reduce gain above $f_H$.',
        },
        {
            'q': 'What limits the low-frequency response of an amplifier?',
            'a': r'Coupling capacitors (block DC) and bypass capacitors create poles at low frequencies. Gain rolls off below $f_L$.',
        },
        {
            'q': 'Unity-gain frequency fT of a BJT.',
            'a': r'$f_T = \dfrac{g_m}{2\pi(C_\pi + C_\mu)}$. Frequency at which current gain $|h_{fe}| = 1$.',
        },
        {
            'q': 'State the open-circuit time constant method for finding fH.',
            'a': r'$f_H \approx \dfrac{1}{2\pi \sum_i C_i R_i}$ where $R_i$ is the resistance seen by each capacitor $C_i$ with all other caps open-circuited.',
        },
        {
            'q': 'Why does gain-bandwidth product remain constant?',
            'a': r'A single dominant pole: $\text{gain} \times BW = g_m/(2\pi C_L) = \text{constant}$. Reducing gain increases bandwidth by the same factor.',
        },
    ],

    'Feedback Amplifiers': [
        {
            'q': 'How does negative feedback affect gain?',
            'a': r'Closed-loop gain $A_f = A/(1 + A\beta)$. The factor $(1+A\beta)$ is the desensitivity factor \u2014 gain reduced but more stable.',
        },
        {
            'q': 'How does negative feedback affect bandwidth?',
            'a': r'Bandwidth increases by $(1+A\beta)$: $BW_f = BW(1+A\beta)$. GBP remains constant.',
        },
        {
            'q': 'How does negative feedback affect nonlinear distortion?',
            'a': r'Distortion is reduced by factor $(1+A\beta)$. Feedback linearises the amplifier.',
        },
        {
            'q': 'State the Barkhausen criterion for oscillation.',
            'a': r'Loop gain $|A\beta| = 1$ and total phase shift around loop = 0\u00b0 (or 360\u00b0). If $|A\beta| > 1$, oscillations grow; $< 1$, they decay.',
        },
    ],

    'Filters & Tuned Amplifiers': [
        {
            'q': 'First-order low-pass filter transfer function.',
            'a': r'$H(s) = \dfrac{K\omega_p}{s + \omega_p}$, or $H(j\omega) = \dfrac{K}{1 + j\omega/\omega_p}$. $-20\,\mathrm{dB/dec}$ roll-off above $\omega_p$.',
        },
        {
            'q': 'Second-order Butterworth low-pass: H(s) with \u03c9n = 1 rad/s (normalised).',
            'a': r'$H(s) = \dfrac{1}{s^2 + \sqrt{2}\,s + 1}$. Maximally flat in passband ($Q = 1/\sqrt{2} = 0.707$).',
        },
        {
            'q': 'Sallen-Key LP filter: component relationships for Butterworth response.',
            'a': r'With equal $R$ and $C$: $Q = 0.5/(2-K)$, where $K = 1 + R_f/R_g$. For Butterworth: $K = 1.586$, giving $Q = 0.707$.',
        },
        {
            'q': 'Band-pass filter Q factor definition.',
            'a': r'$Q = f_0/BW = \omega_0/(\omega_2 - \omega_1)$. High $Q$ \u2192 narrow bandwidth, sharp selectivity.',
        },
        {
            'q': 'Describe an active second-order BP filter using op-amp.',
            'a': r'Multiple feedback (MFB) topology: two capacitors and three resistors. $H(s) = -\dfrac{(R_2/R_1)\,s}{s^2 + 2\alpha s + \omega_0^2}$.',
        },
    ],

    'Oscillators': [
        {
            'q': 'State the Barkhausen criterion for a sinusoidal oscillator.',
            'a': r'Loop gain $= 1$: $|A(j\omega)\beta(j\omega)| = 1$ and $\angle A(j\omega)\beta(j\omega) = 0°$ at the oscillation frequency.',
        },
        {
            'q': 'Wien bridge oscillator frequency.',
            'a': r'$f_0 = \dfrac{1}{2\pi RC}$. Requires op-amp gain of 3 ($R_f = 2R_1$).',
        },
        {
            'q': 'Colpitts oscillator: tank circuit and frequency.',
            'a': r'Two capacitors $C_1$, $C_2$ in series with inductor $L$. $f_0 = \dfrac{1}{2\pi\sqrt{LC_{eq}}}$, $C_{eq} = \dfrac{C_1 C_2}{C_1 + C_2}$.',
        },
        {
            'q': 'Hartley oscillator: tank circuit and frequency.',
            'a': r'Two inductors $L_1$, $L_2$ in series with capacitor $C$. $f_0 = \dfrac{1}{2\pi\sqrt{(L_1 + L_2)C}}$.',
        },
        {
            'q': '555 timer in astable mode: frequency formula.',
            'a': r'$f = \dfrac{1.44}{(R_1 + 2R_2)C}$. Duty cycle $= \dfrac{R_1 + R_2}{R_1 + 2R_2} \times 100\%$.',
        },
    ],
}


def fix_latex(apps, schema_editor):
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
    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    for topic_name, updates in LATEX_UPDATES.items():
        topic = topics.get(topic_name)
        if not topic:
            continue
        for spec in updates:
            old_q = spec['q']
            new_a = spec['a']
            new_q = spec.get('new_q')
            new_steps = spec.get('steps')

            qs = Flashcard.objects.filter(topic=topic, question=old_q)
            if not qs.exists():
                continue

            if new_steps is not None:
                # JSONField update — do on the instance for reliability
                card = qs.first()
                if new_q:
                    card.question = new_q
                card.answer = new_a
                card.uses_latex = True
                card.steps = new_steps
                card.save()
            else:
                kwargs = {'answer': new_a, 'uses_latex': True}
                if new_q:
                    kwargs['question'] = new_q
                qs.update(**kwargs)


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0031_flashcards_dsp_extended'),
    ]

    operations = [
        migrations.RunPython(fix_latex, reverse_fn),
    ]
