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
        name='Power Systems', created_by=system_user
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
    # 1. Power System Structure
    # -------------------------------------------------------------------------
    add_cards('Power System Structure', [
        {
            'question': 'Describe the main components of a bulk power system from generation to the consumer.',
            'answer': 'Generation → Step-up transformer → Transmission (HV: 66–500 kV) → Sub-transmission (33–132 kV) → Distribution substation → Distribution network (11 kV/415 V) → Consumer. Voltage is stepped up to reduce I²R transmission losses.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Why is AC power transmitted at high voltage?',
            'answer': 'Transmission losses P_loss = I²R. For the same power P = V·I, higher V means lower I, so losses ∝ 1/V². Doubling voltage reduces losses by 75% for the same power transferred.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is a busbar in a power system?',
            'answer': 'A busbar is a low-impedance node where multiple circuits (generators, lines, loads, transformers) are connected. Busbars serve as junction points in substations. Common configurations: single busbar, double busbar, ring bus, breaker-and-a-half.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Define real power (P), reactive power (Q), and apparent power (S) in a power system context.',
            'answer': 'P (W or MW): average power doing real work. Q (VAr or MVAr): reactive power exchanged between source and reactive elements. S (VA or MVA): S = V·I* = P + jQ, |S| = √(P²+Q²). Power factor PF = P/S = cosφ.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is the role of reactive power in a power system?',
            'answer': 'Reactive power maintains voltage levels throughout the network. Insufficient Q causes voltage collapse. Excess Q raises voltages above limits. Sources: generators (over-excited), capacitor banks, FACTS devices. Loads (inductive motors) consume Q.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a SCADA system in power systems?',
            'answer': 'Supervisory Control And Data Acquisition: monitors and controls the power system in real time via RTUs and IEDs. Provides: telemetry of voltage, current, power; remote switching; alarm management; historian data. Managed from an Energy Management System (EMS).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Explain why most power systems use three-phase AC rather than single-phase or DC.',
            'answer': 'Three-phase: constant instantaneous power (no double-frequency pulsation); more efficient use of conductors (higher power/conductor ratio); rotating magnetic field for motors without extra starting circuits. DC requires power electronics for voltage conversion — now used for HVDC long-distance links.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 2. Per-Unit Analysis
    # -------------------------------------------------------------------------
    add_cards('Per-Unit Analysis', [
        {
            'question': 'Define the per-unit (p.u.) system.',
            'answer': 'A normalisation: quantity_pu = actual_quantity / base_quantity. Common bases: MVAbase (3-phase), kVbase (line-to-line). Derived: Ibase = MVAbase / (√3·kVbase), Zbase = kV²base / MVAbase. Per-unit removes transformer turns ratios from calculations.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'How do you convert impedance from one base to another in the per-unit system?',
            'answer': 'Z_pu_new = Z_pu_old × (MVAbase_new / MVAbase_old) × (kVbase_old / kVbase_new)²',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Perform a per-unit analysis: A 50 MVA, 11/132 kV transformer has 10% leakage reactance. Find Xpu on 100 MVA, 11 kV base.',
            'answer': '',
            'hint': 'Convert X from old base (50 MVA, 11 kV) to new base (100 MVA, 11 kV)',
            'difficulty': 'hard',
            'question_type': 'step_by_step',
            'uses_latex': True,
            'steps': [
                {'move': 'Identify old base', 'detail': 'MVAbase_old = 50 MVA, kVbase_old = 11 kV, X_pu_old = 0.10'},
                {'move': 'Identify new base', 'detail': 'MVAbase_new = 100 MVA, kVbase_new = 11 kV'},
                {'move': 'Apply conversion formula', 'detail': 'X_pu_new = 0.10 × (100/50) × (11/11)² = 0.10 × 2 × 1 = 0.20 p.u.'},
                {'move': 'Interpretation', 'detail': 'On the new 100 MVA base, the transformer has 20% leakage reactance'},
            ],
        },
        {
            'question': 'What are the advantages of using the per-unit system in power systems analysis?',
            'answer': '1) Transformer turns ratios disappear — circuit looks uniform. 2) Equipment ratings are in a consistent range (~0.05–1.5 p.u.). 3) Easy error checking — quantities should be near 1 p.u. 4) Simplifies three-phase calculations.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are the rules for choosing base quantities in a multi-zone power system?',
            'answer': 'Choose one MVA base throughout the system. Choose one kV base in one zone; bases in other zones are set by transformer turns ratios to maintain consistency. Never choose different MVA bases in different zones.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 3. Load Flow Analysis
    # -------------------------------------------------------------------------
    add_cards('Load Flow Analysis', [
        {
            'question': 'What is the purpose of load flow (power flow) analysis?',
            'answer': 'Load flow determines the steady-state operating condition of a power system: voltage magnitudes and angles at each bus, real and reactive power flows in each line/transformer. Used for: system planning, operational control, N-1 contingency analysis.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are the three types of buses in load flow analysis?',
            'answer': '1) Slack (swing) bus: reference; V and δ specified (V=1∠0°); P and Q calculated. 2) PV bus (generator bus): P and |V| specified; Q and δ calculated. 3) PQ bus (load bus): P and Q specified; |V| and δ calculated.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is the Gauss-Seidel load flow method?',
            'answer': 'An iterative method: start with a flat start (V=1∠0°), update each bus voltage sequentially using the power mismatch equations until convergence. Simple to implement; slow convergence for large systems. Has been largely replaced by Newton-Raphson.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Why is Newton-Raphson preferred for large load flow problems?',
            'answer': 'Newton-Raphson (NR) has quadratic convergence — the number of correct decimal places roughly doubles each iteration. Typically converges in 3–5 iterations for large systems, compared to 50–100 for Gauss-Seidel. NR uses the Jacobian matrix of partial derivatives.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Define the power flow equations at a PQ bus.',
            'answer': 'Pi = Σ|Vi||Vk|(Gik·cosθik + Bik·sinθik), Qi = Σ|Vi||Vk|(Gik·sinθik − Bik·cosθik), where Ybus = G + jB, θik = δi − δk. These are solved iteratively for |Vi| and δi.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is a voltage collapse and how is it related to load flow?',
            'answer': 'Voltage collapse: voltage at load buses drops uncontrollably due to insufficient reactive power support, usually under heavy load or reactive power demand. In load flow, it appears as failure to converge or multiple solutions. Proximity to collapse is measured by the voltage stability index.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 4. Fault Analysis
    # -------------------------------------------------------------------------
    add_cards('Fault Analysis', [
        {
            'question': 'List the four types of faults in three-phase power systems in order of frequency of occurrence.',
            'answer': '1) Single line-to-ground (SLG) — most common (~80%). 2) Line-to-line (LL). 3) Double line-to-ground (DLG). 4) Three-phase (3Φ) balanced — least common but most severe (~5%). SLG and 3Φ are the basis of most protection settings.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the method of symmetrical components used for in fault analysis?',
            'answer': 'Symmetrical components (Fortescue) transform unbalanced three-phase quantities into three balanced sets: positive sequence (+), negative sequence (−), and zero sequence (0). Each sequence has its own network/impedance. This decouples the three-phase problem into independent sequence networks.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Write the fault current formula for a three-phase fault at a bus with pre-fault voltage V0 and Thevenin impedance Zth.',
            'answer': 'If = V0 / Zth (p.u.). The three-phase fault current is symmetrical. In actual values: If_actual = If_pu × Ibase = (V0 / Zth) × (MVAbase / (√3·kVbase)). Zth is the positive-sequence Thevenin impedance.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is subtransient reactance (X"d) and why is it used in fault calculations?',
            'answer': 'X"d is the very small initial reactance of a synchronous generator (first few cycles after fault). It determines the maximum fault current. X\'d (transient) and Xd (synchronous) are larger and govern the decaying fault current. Protection must be designed for X"d-based currents.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'Calculate the fault MVA for a three-phase fault given the system impedance.',
            'answer': '',
            'hint': 'Fault MVA = MVAbase / Z_pu',
            'difficulty': 'medium',
            'question_type': 'step_by_step',
            'uses_latex': True,
            'steps': [
                {'move': 'State formula', 'detail': 'Fault MVA = MVAbase / Z_pu (p.u. impedance to fault)'},
                {'move': 'Example', 'detail': 'System: 100 MVA base, Zth = 0.1 p.u.'},
                {'move': 'Calculate', 'detail': 'Fault MVA = 100 / 0.1 = 1000 MVA'},
                {'move': 'Convert to current', 'detail': 'If = Fault MVA / (√3 × kV) — at 11 kV: If = 1000 / (1.732 × 11) = 52.5 kA'},
            ],
        },
        {
            'question': 'What is the purpose of neutral grounding in power systems?',
            'answer': 'Neutral grounding limits transient overvoltages during ground faults and provides a return path for fault current, enabling protective relays to detect and clear faults. Methods: solid grounding (high fault current), resistance grounding (limited fault current), reactance grounding, isolated neutral (no fault current but high overvoltage).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 5. Power System Protection
    # -------------------------------------------------------------------------
    add_cards('Power System Protection', [
        {
            'question': 'What are the four fundamental requirements of power system protection?',
            'answer': '1) Reliability: operates when required (dependability) and does not operate unnecessarily (security). 2) Selectivity: isolates only the faulted section. 3) Speed: clears faults fast to limit damage and maintain stability. 4) Sensitivity: detects minimum fault levels.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the principle of overcurrent protection?',
            'answer': 'An overcurrent relay (OCR) operates when current exceeds a set threshold (pickup). Time-overcurrent relays have inverse time characteristics (IDMT): higher current ⟹ faster trip. Coordination: upstream relay has longer time delay than downstream (graded protection).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How does a differential protection relay work?',
            'answer': 'Compares currents entering and leaving a protected zone (transformer, generator, busbar). Under normal conditions or external fault: I_in ≈ I_out, differential current ≈ 0. On internal fault: differential current spikes → relay trips. Very sensitive and fast; immune to load current.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a distance (impedance) relay and where is it used?',
            'answer': 'A distance relay measures the impedance seen from its location (Z = V/I). If Z falls within the relay\'s impedance characteristic (mho, reactance, or quadrilateral), it trips. Used to protect transmission lines: Zone 1 (80–85% of line, instantaneous), Zone 2 (extends to next bus + margin, time delayed), Zone 3 (backup).',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is auto-reclosing and why is it used on transmission lines?',
            'answer': 'After a fault clears (breaker trips), an auto-reclose scheme automatically recloses the breaker after a short dead time. ~80% of transmission line faults are transient (lightning, temporary flashover) and self-clear. Auto-reclosing restores supply without operator intervention. Typically 1–3 shots before lock-out.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Explain the role of current transformers (CTs) in protection.',
            'answer': 'CTs step down high primary current to a standard secondary level (1 A or 5 A) for relay inputs. Important parameters: ratio (e.g. 400/5 = 80:1), accuracy class (e.g. 5P20: 5% error at 20× rated, protected class), knee-point voltage (must not saturate during fault). CT saturation causes relay mal-operation.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is an Earth Fault (EF) relay and how is it set?',
            'answer': 'Detects zero-sequence (residual) current from CTs: I0 = (Ia + Ib + Ic)/3 ≠ 0 during ground fault. Typical settings: pickup at 10–40% of rated current (much lower than phase overcurrent). Provides sensitive detection of high-impedance ground faults.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
    ])

    # -------------------------------------------------------------------------
    # 6. Power Electronics in Power Systems
    # -------------------------------------------------------------------------
    add_cards('Power Electronics in Power Systems', [
        {
            'question': 'What is HVDC transmission and when is it preferred over AC?',
            'answer': 'High Voltage Direct Current: power converted to DC for transmission, then back to AC at the other end. Preferred when: cable distances >50 km (no charging current issues), asynchronous AC system interconnection, submarine cables, long overhead lines >600 km (lower losses). Examples: inter-country links.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are FACTS devices? Give three examples.',
            'answer': 'Flexible AC Transmission Systems: power electronics-based controllers that improve power system controllability and increase power transfer capacity. Examples: SVC (Static VAr Compensator), STATCOM (Static Synchronous Compensator), TCSC (Thyristor Controlled Series Capacitor).',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How does a Static VAr Compensator (SVC) regulate bus voltage?',
            'answer': 'An SVC combines thyristor-controlled reactors (TCR) and thyristor-switched capacitors (TSC). By varying the firing angle of the TCR, the reactive power absorbed can be continuously adjusted. At low voltage: capacitors switch in (inject Q). At high voltage: inductors absorb more Q. Response time ~20–50 ms.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a grid-connected inverter and what control modes does it operate in?',
            'answer': 'Converts DC (from PV, battery, wind converter) to AC and injects into the grid. Control modes: 1) Grid-following (PQ control): tracks grid voltage/frequency, injects set P and Q. 2) Grid-forming (droop/virtual synchronous machine): provides voltage and frequency reference, used in weak grids or islanded microgrids.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Explain the impact of distributed generation (DG) on distribution network protection.',
            'answer': 'Traditional networks are radial — fault current flows from one direction (source). DG reverses this assumption: fault current now flows from multiple directions. Problems: 1) Loss of protection coordination (time-graded schemes fail). 2) Sympathetic tripping. 3) Anti-islanding: DG must disconnect during grid fault (IEEE 1547). Requires adaptive or directional protection.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is reactive power compensation and how does a capacitor bank provide it?',
            'answer': 'Inductive loads (motors) absorb Q from the grid, causing low PF and high reactive current in feeders. Shunt capacitor banks supply local Q (Qc = V²/Xc), reducing feeder current, improving PF, and raising voltage. Power factor correction penalty avoidance is a key economic driver.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': True,
        },
    ])


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0020_flashcards_electrical_machines'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
