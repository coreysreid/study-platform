from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return
    course = Course.objects.filter(name='Circuit Analysis Fundamentals', created_by=system_user).first()
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
    # Topic 1: DC Circuit Analysis
    # ------------------------------------------------------------------ #
    add_cards('DC Circuit Analysis', [
        {'question': "State Ohm's Law.",
         'answer': 'V = IR. Voltage (V) equals current (I) times resistance (R).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State Kirchhoff\'s Voltage Law (KVL).',
         'answer': 'The sum of all voltages around any closed loop is zero: ΣV = 0.',
         'hint': 'Conservation of energy', 'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State Kirchhoff\'s Current Law (KCL).',
         'answer': 'The sum of currents entering a node equals the sum leaving: ΣIᵢₙ = ΣIₒᵤₜ.',
         'hint': 'Conservation of charge', 'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Formula for resistors in series.',
         'answer': 'Rₜₒₜₐₗ = R₁ + R₂ + ... + Rₙ.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Formula for resistors in parallel.',
         'answer': '1/Rₜₒₜₐₗ = 1/R₁ + 1/R₂ + ... For two resistors: R = R₁R₂/(R₁+R₂).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Voltage divider rule: two resistors R₁ and R₂ in series with supply V.',
         'answer': 'V₂ = V × R₂/(R₁+R₂). Voltage splits in proportion to resistance.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Current divider rule: two resistors R₁ and R₂ in parallel with total current I.',
         'answer': 'I₁ = I × R₂/(R₁+R₂). Current divides inversely to resistance.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Three power formulas for a resistor.',
         'answer': 'P = VI = I²R = V²/R.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Outline the nodal analysis method.',
         'answer': '1) Choose reference node (ground). 2) Label unknown node voltages. 3) Apply KCL at each non-reference node. 4) Solve system of equations.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Outline the mesh analysis method.',
         'answer': '1) Identify meshes (independent loops). 2) Assign mesh currents (clockwise). 3) Apply KVL around each mesh. 4) Solve for mesh currents.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Apply KVL to solve: 12V source with R₁=4Ω and R₂=8Ω in series. Find current and power dissipated in R₂.',
         'answer': 'Total R = 12Ω. I = 12/12 = 1A. V₂ = 1×8 = 8V. P₂ = 1²×8 = 8W.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Find total resistance', 'detail': 'R_total = 4 + 8 = 12Ω'},
                   {'move': 'Apply Ohm\'s law', 'detail': 'I = V/R = 12/12 = 1A'},
                   {'move': 'Voltage across R₂', 'detail': 'V₂ = IR₂ = 1×8 = 8V'},
                   {'move': 'Power in R₂', 'detail': 'P₂ = V₂²/R₂ = 64/8 = 8W'}]},
        {'question': 'Two resistors 6Ω and 3Ω are in parallel. Find the equivalent resistance.',
         'answer': 'Rₑq = (6×3)/(6+3) = 18/9 = 2Ω.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a super-node in nodal analysis?',
         'answer': 'A super-node is formed when a voltage source connects two non-reference nodes. Treat both nodes together: write one KCL equation and use the voltage source constraint.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is a super-mesh in mesh analysis?',
         'answer': 'A super-mesh is formed when a current source is shared by two meshes. Write one KVL around the outer perimeter; use the current source as a constraint equation.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is the short-circuit current if V=10V is applied to R=5Ω?',
         'answer': 'With the output shorted, Isc = V/R = 10/5 = 2A.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Define conductance G and its units.',
         'answer': 'G = 1/R. Units: siemens (S). I = GV.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # Topic 2: Network Theorems
    # ------------------------------------------------------------------ #
    add_cards('Network Theorems', [
        {'question': 'State the Superposition theorem.',
         'answer': 'In a linear circuit, the response due to multiple independent sources equals the sum of responses due to each source acting alone (others replaced by their internal resistance).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'How do you deactivate a voltage source for superposition?',
         'answer': 'Replace it with a short circuit (0V = wire).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'How do you deactivate a current source for superposition?',
         'answer': 'Replace it with an open circuit (0A = break).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'State Thevenin\'s theorem.',
         'answer': 'Any linear two-terminal network can be replaced by a voltage source Vth in series with resistance Rth.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How do you find Vth (Thevenin voltage)?',
         'answer': 'Vth = open-circuit voltage at the terminals (remove the load).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'How do you find Rth (Thevenin resistance)?',
         'answer': 'Deactivate all independent sources. Measure/calculate resistance looking into the terminals. (Or: Rth = Voc/Isc)',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the Thevenin equivalent of: 12V in series with 4Ω, connected to terminals A-B.',
         'answer': 'Vth = 12V (no load current → no drop across 4Ω). Rth = 4Ω (short the source). Equivalent: 12V with 4Ω series.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Find Voc (open circuit)', 'detail': 'No current flows without load → Vth = 12V'},
                   {'move': 'Find Rth', 'detail': 'Short the 12V source: Rth = 4Ω'},
                   {'move': 'Thevenin circuit', 'detail': '12V source in series with 4Ω'}]},
        {'question': 'State Norton\'s theorem.',
         'answer': 'Any linear two-terminal network can be replaced by a current source IN in parallel with resistance RN.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Relationship between Thevenin and Norton equivalents.',
         'answer': 'RN = Rth; IN = Vth/Rth = Isc. They are interchangeable via source transformation.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State the Maximum Power Transfer theorem.',
         'answer': 'Maximum power is delivered to a load RL when RL = Rth. Maximum power: Pmax = Vth²/(4Rth).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is source transformation?',
         'answer': 'A voltage source V in series with R can be converted to a current source I=V/R in parallel with R, and vice versa.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Find the Norton equivalent of: 6A source in parallel with 3Ω.',
         'answer': 'IN = 6A; RN = 3Ω. Thevenin equivalent: Vth = 6×3 = 18V in series with 3Ω.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'A circuit has Vth = 10V and Rth = 5Ω. What load RL gives maximum power, and what is that power?',
         'answer': 'RL = Rth = 5Ω. Pmax = Vth²/(4Rth) = 100/20 = 5W.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # Topic 3: AC Phasor Analysis
    # ------------------------------------------------------------------ #
    add_cards('AC Phasor Analysis', [
        {'question': 'Express a sinusoid v(t) = Vm cos(ωt + φ) in phasor form.',
         'answer': 'V = Vm∠φ (or Vm e^(jφ)). Phasors capture amplitude and phase; the ωt factor is implicit.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the RMS value of v(t) = Vm cos(ωt)?',
         'answer': 'Vrms = Vm/√2 ≈ 0.707 Vm.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Impedance of a resistor R in the phasor domain.',
         'answer': 'ZR = R. Purely real — voltage and current are in phase.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Impedance of an inductor L at angular frequency ω.',
         'answer': 'ZL = jωL. Purely imaginary — voltage leads current by 90°.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Impedance of a capacitor C at angular frequency ω.',
         'answer': 'ZC = 1/(jωC) = −j/(ωC). Purely imaginary — voltage lags current by 90°.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the mnemonic for inductor/capacitor phase?',
         'answer': '"ELI the ICE man": E leads I in an L (inductor); I leads E in a C (capacitor).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Convert V = 5∠30° to rectangular form.',
         'answer': 'V = 5cos30° + j5sin30° = 4.33 + j2.5.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Convert V = 3 + j4 to polar form.',
         'answer': '|V| = √(9+16) = 5; ∠V = arctan(4/3) = 53.13°. V = 5∠53.13°.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Series RL circuit: R=3Ω, L=4Ω (i.e. XL=4Ω). Find total impedance.',
         'answer': 'Z = 3 + j4 = 5∠53.13° Ω.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Apply voltage divider in phasor domain: V across Z₂ in series with Z₁ and Z₂.',
         'answer': 'V₂ = Vs × Z₂/(Z₁+Z₂). Same rule as DC but with complex impedances.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'A series RLC circuit: R=10Ω, XL=20Ω, XC=5Ω. Find Z.',
         'answer': 'Z = R + j(XL − XC) = 10 + j15 Ω. |Z| = √(100+225) = √325 ≈ 18.03Ω.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Combine reactances', 'detail': 'Net reactance X = XL − XC = 20 − 5 = 15Ω'},
                   {'move': 'Total impedance', 'detail': 'Z = 10 + j15 Ω'},
                   {'move': 'Magnitude', 'detail': '|Z| = √(10² + 15²) = √325 ≈ 18.03Ω'},
                   {'move': 'Phase', 'detail': 'θ = arctan(15/10) = 56.3°'}]},
        {'question': 'Define power factor.',
         'answer': 'PF = cos φ, where φ is the angle between voltage and current phasors. PF = P/S.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is admittance Y?',
         'answer': 'Y = 1/Z = G + jB. G = conductance, B = susceptance. Units: siemens (S).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Parallel admittances add: Y₁∥Y₂.',
         'answer': 'Ytotal = Y₁ + Y₂. This is why parallel admittances are easier to combine than parallel impedances.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # Topic 4: Transient Analysis
    # ------------------------------------------------------------------ #
    add_cards('Transient Analysis', [
        {'question': 'What is the time constant τ of an RC circuit?',
         'answer': 'τ = RC. At t = τ, the capacitor charges to 63.2% of the final value.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the time constant τ of an RL circuit?',
         'answer': 'τ = L/R. At t = τ, the inductor current reaches 63.2% of its final value.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Write the step response of a series RC circuit: v_C(t) after switch closes at t=0.',
         'answer': 'v_C(t) = V_s(1 − e^(−t/RC)) for t ≥ 0. Starts at 0, asymptotes to Vs.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Write the step response of an RL circuit: i_L(t) after switch closes at t=0.',
         'answer': 'i_L(t) = (V_s/R)(1 − e^(−t/τ)), τ = L/R.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How do you find initial and final conditions for a transient circuit?',
         'answer': 'Initial: at t=0⁻, capacitor voltage and inductor current cannot change instantaneously. Final: at t=∞, capacitor = open circuit, inductor = short circuit (DC steady-state).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'General form of the transient response for a first-order circuit.',
         'answer': 'x(t) = x(∞) + [x(0) − x(∞)]e^(−t/τ). Valid for any voltage or current.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Write the characteristic equation for a series RLC circuit.',
         'answer': 's² + (R/L)s + 1/(LC) = 0. Roots: s = −α ± √(α²−ωₙ²), where α = R/2L, ωₙ = 1/√(LC).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Define damping ratio ζ for a second-order RLC circuit.',
         'answer': 'ζ = α/ωₙ = (R/2L)/( 1/√(LC)) = (R/2)√(C/L). ζ<1 underdamped, ζ=1 critically damped, ζ>1 overdamped.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What does underdamped RLC response look like?',
         'answer': 'Oscillatory, exponentially decaying sinusoid. Roots are complex conjugates: s = −α ± jωd where ωd = √(ωn²−α²).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What does overdamped RLC response look like?',
         'answer': 'Non-oscillatory, two decaying exponentials. Roots are real and distinct: s₁, s₂ both negative real.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'An RC circuit has R=1kΩ, C=1μF. After how many time constants is the voltage within 1% of its final value?',
         'answer': 'At 5τ, e^(-5) ≈ 0.0067 (0.67% error). Practically "settled" at 5τ = 5ms.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the natural response of a circuit?',
         'answer': 'The response due to initial stored energy (capacitor charge or inductor current), with no external source. Decays exponentially.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is the forced response of a circuit?',
         'answer': 'The response due to external sources (particular solution), with zero initial conditions. Matches the forcing function at steady state.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
    ])

    # ------------------------------------------------------------------ #
    # Topic 5: Frequency Response & Resonance
    # ------------------------------------------------------------------ #
    add_cards('Frequency Response & Resonance', [
        {'question': 'Define the transfer function H(jω) of a circuit.',
         'answer': 'H(jω) = Vout(jω)/Vin(jω). Complex ratio of output to input phasors as a function of frequency.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the resonant frequency of a series RLC circuit?',
         'answer': 'ω₀ = 1/√(LC) rad/s, or f₀ = 1/(2π√(LC)) Hz. At resonance, XL = XC and Z = R (minimum).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Define the Q factor (quality factor) for a series RLC circuit.',
         'answer': 'Q = ω₀L/R = 1/(ω₀CR) = (1/R)√(L/C). Higher Q → sharper resonance peak.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Define bandwidth (BW) of a resonant circuit.',
         'answer': 'BW = ω₂ − ω₁ = R/L (series RLC), where ω₁ and ω₂ are the −3dB frequencies. BW = ω₀/Q.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'At the −3dB frequency, the magnitude of H(jω) is?',
         'answer': '|H| = |H|max / √2 ≈ 0.707 × peak. Power is half of maximum.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the slope of a Bode magnitude plot for a single pole (1/(1+jω/ωp))?',
         'answer': '−20 dB/decade for ω >> ωp. Phase: 0° at low freq, −45° at ω=ωp, −90° at high freq.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Convert a gain ratio of 100 to dB.',
         'answer': '20 log₁₀(100) = 20 × 2 = 40 dB.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Convert a gain of −6 dB to a voltage ratio.',
         'answer': '−6 dB = 20 log₁₀(ratio). ratio = 10^(−6/20) = 10^(−0.3) ≈ 0.5.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the resonant frequency of a series RLC with L=10mH and C=100nF?',
         'answer': 'ω₀ = 1/√(10×10⁻³ × 100×10⁻⁹) = 1/√(10⁻⁹) = 10⁴·⁵ ≈ 31.6 krad/s. f₀ ≈ 5.03 kHz.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'For a parallel RLC circuit, what is the resonant frequency and what happens to impedance?',
         'answer': 'ω₀ = 1/√(LC), same as series. At resonance, parallel impedance is MAXIMUM (= R), not minimum.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State the asymptotic Bode slope rules for a double pole (two equal poles).',
         'answer': '−40 dB/decade above the pole frequency. Phase swings −180° total (−90° per pole).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a low-pass filter\'s transfer function H(s) = ωc/(s+ωc)?',
         'answer': 'First-order low-pass: passes frequencies below ωc, attenuates above. |H| = 1/√2 at ω = ωc (−3dB point).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    # ------------------------------------------------------------------ #
    # Topic 6: AC Power Analysis
    # ------------------------------------------------------------------ #
    add_cards('AC Power Analysis', [
        {'question': 'Formula for instantaneous power p(t).',
         'answer': 'p(t) = v(t) × i(t). For sinusoidal: p(t) = VmIm/2 · [cos φ + cos(2ωt − φ)].',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Formula for average (real) power P.',
         'answer': 'P = ½VmIm cos φ = VrmsIrms cos φ. Units: watts (W). Only resistive components dissipate real power.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Formula for reactive power Q.',
         'answer': 'Q = ½VmIm sin φ = VrmsIrms sin φ. Units: VAR. Positive for inductive loads, negative for capacitive.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Formula for apparent power S.',
         'answer': 'S = VrmsIrms. Units: VA. S = P + jQ (complex power). |S| = apparent power magnitude.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State the power triangle relationship.',
         'answer': 'S² = P² + Q². Power factor PF = P/S = cos φ.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'A load draws 5kW at PF = 0.6 lagging. Find Q and S.',
         'answer': 'cos φ = 0.6 → sin φ = 0.8. S = P/PF = 5k/0.6 = 8.33 kVA. Q = S sin φ = 8.33×0.8 = 6.67 kVAR.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Find S from P and PF', 'detail': 'S = P/cos φ = 5000/0.6 = 8333 VA'},
                   {'move': 'Find sin φ', 'detail': 'sin φ = √(1−0.36) = 0.8'},
                   {'move': 'Find Q', 'detail': 'Q = S sin φ = 8333 × 0.8 = 6667 VAR'}]},
        {'question': 'How do you correct (improve) power factor using a capacitor?',
         'answer': 'Add a capacitor in parallel with the load. The capacitor supplies reactive power (QC < 0), reducing the net Q and increasing PF.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'A load has P=10kW and Q=7.5kVAR (lagging). What capacitor (at 50Hz, 230V) corrects PF to unity?',
         'answer': 'Need QC = −7.5kVAR. C = Q/(ω V²) = 7500/(2π×50×230²) = 7500/16614 ≈ 451μF.',
         'difficulty': 'hard', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Identify required QC', 'detail': 'QC = −7.5 kVAR to cancel load Q'},
                   {'move': 'Use QC = V²ωC', 'detail': '7500 = 230² × 2π × 50 × C'},
                   {'move': 'Solve for C', 'detail': 'C = 7500/16614 ≈ 451 μF'}]},
        {'question': 'For a balanced three-phase system, state the relationship between line and phase voltage.',
         'answer': 'VL = √3 × Vph ≈ 1.732 × Vph. In Australia: VL = 415V, Vph = 240V.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Three-phase power formula (balanced, line quantities).',
         'answer': 'P = √3 × VL × IL × cos φ. Also P = 3 × Vph × Iph × cos φ.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the maximum efficiency theorem for power transfer?',
         'answer': 'Maximum average power transfer to a complex load ZL occurs when ZL = Zth* (conjugate of Thevenin impedance).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
    ])


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0014_flashcards_engineering_mathematics'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
