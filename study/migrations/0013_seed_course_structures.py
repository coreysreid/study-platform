# Generated migration — seeds all 11 public course structures and back-fills
# CourseEnrollment for every existing non-system user.
#
# Supersedes management commands:
#   - populate_math_curriculum
#   - populate_comprehensive_math_cards  (flashcards come in 0014+)

from django.db import migrations


# ---------------------------------------------------------------------------
# Helper — called by RunPython
# ---------------------------------------------------------------------------

def seed_courses(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Skill = apps.get_model('study', 'Skill')
    CourseEnrollment = apps.get_model('study', 'CourseEnrollment')

    # ------------------------------------------------------------------
    # 1. Ensure system user exists
    # ------------------------------------------------------------------
    system_user, _ = User.objects.get_or_create(
        username='system',
        defaults={
            'is_staff': False,
            'is_active': True,
            'email': 'system@system.local',
            'first_name': 'System',
            'last_name': 'Content',
        }
    )

    # ------------------------------------------------------------------
    # 2. Skills used across courses
    # ------------------------------------------------------------------
    skill_names = [
        # Mathematics
        'basic_arithmetic', 'fraction_operations', 'decimal_operations',
        'order_of_operations', 'scientific_notation', 'algebraic_manipulation',
        'equation_solving', 'exponent_rules', 'polynomial_operations',
        'factoring', 'quadratic_equations',
        'geometric_reasoning', 'pythagorean_theorem', 'area_volume_calculations',
        'coordinate_geometry', 'angle_relationships',
        'trigonometric_ratios', 'right_triangle_solving', 'trigonometric_identities',
        'unit_circle', 'trig_equation_solving',
        'function_analysis', 'exponential_logarithmic', 'complex_numbers',
        'sequences_series', 'limit_concepts',
        'derivative_calculation', 'differentiation_rules', 'implicit_differentiation',
        'optimization', 'curve_analysis', 'related_rates', 'integration_techniques',
        'definite_integrals', 'area_calculations', 'volume_of_revolution',
        'applications_of_integration',
        'partial_derivatives', 'multiple_integrals', 'vector_calculus',
        'multivariable_optimization', 'coordinate_transformations', 'matrix_operations',
        'determinants', 'solving_linear_systems', 'eigenvalue_problems',
        'vector_spaces', 'linear_transformations', 'ode_classification',
        'first_order_ode_solving', 'second_order_ode_solving', 'systems_of_odes',
        'modeling_with_odes', 'pde_classification', 'separation_of_variables',
        'boundary_value_problems', 'method_of_characteristics', 'pde_applications',
        'fourier_series', 'fourier_coefficients', 'fourier_transform',
        'signal_analysis', 'frequency_domain', 'laplace_transform_calculation',
        'inverse_laplace_transform', 'solving_odes_with_laplace',
        'transfer_functions', 'system_analysis',
        # Circuits
        'ohms_law', 'kirchhoff_voltage_law', 'kirchhoff_current_law',
        'series_parallel_circuits', 'thevenin_norton', 'superposition',
        'phasor_analysis', 'impedance', 'ac_power', 'resonance',
        'rc_rl_transients', 'bode_plots',
        # Electronics
        'diode_operation', 'bjt_operation', 'mosfet_operation',
        'op_amp_ideal', 'amplifier_gain', 'feedback_theory',
        'filter_design', 'oscillator_design',
        # DSP
        'sampling_theorem', 'dft_fft', 'z_transform', 'fir_filter_design',
        'iir_filter_design', 'dtft', 'convolution_discrete',
        # Embedded
        'gpio_programming', 'interrupt_handling', 'pwm_generation',
        'adc_dac', 'uart_spi_i2c', 'rtos_concepts',
        # Control
        'block_diagram_algebra', 'root_locus', 'nyquist_criterion',
        'pid_tuning', 'state_space', 'stability_analysis',
        # Machines
        'transformer_theory', 'dc_machine_analysis', 'induction_motor_analysis',
        'synchronous_machine', 'motor_control', 'variable_speed_drives',
        # Power
        'per_unit_system', 'load_flow', 'fault_analysis',
        'power_protection', 'power_electronics',
        # Linux
        'linux_cli', 'file_permissions', 'process_management',
        'shell_scripting', 'package_management', 'linux_networking',
        'linux_security',
        # Networking
        'osi_model', 'ip_addressing', 'subnetting', 'routing_protocols',
        'switching_vlans', 'network_security', 'network_troubleshooting',
        'industrial_networking',
        # Automation
        'plc_programming', 'ladder_logic', 'structured_text',
        'scada_hmi', 'industrial_protocols', 'motion_control',
        'robot_kinematics', 'ros_basics', 'functional_safety',
    ]

    skills = {}
    for name in skill_names:
        skill, _ = Skill.objects.get_or_create(
            name=name,
            defaults={'description': name.replace('_', ' ').title()}
        )
        skills[name] = skill

    # ------------------------------------------------------------------
    # 3. Course definitions (name → {code, description, topics[]})
    # ------------------------------------------------------------------
    courses_data = [
        {
            'name': 'Engineering Mathematics',
            'code': 'ENGMATH',
            'description': (
                'Comprehensive mathematics curriculum for Bachelor of Engineering students. '
                'Starting from Year 6 foundation, progressing through calculus, linear algebra, '
                'differential equations, Fourier analysis, and Laplace transforms.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'Basic Arithmetic & Number Sense',
                    'description': (
                        'Master operations with whole numbers, fractions, decimals, and percentages. '
                        'Understand order of operations (PEMDAS/BODMAS), work with positive and '
                        'negative numbers, scientific notation and significant figures.'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'Algebra Fundamentals',
                    'description': (
                        'Manipulate algebraic expressions, solve linear equations and inequalities, '
                        'work with exponents and roots, factor polynomials, solve systems of equations.'
                    ),
                    'prerequisites': ['Basic Arithmetic & Number Sense'],
                },
                {
                    'order': 3, 'name': 'Geometry',
                    'description': (
                        'Understand geometric shapes and their properties, apply the Pythagorean theorem, '
                        'calculate areas, volumes, and surface areas, work with angles and triangles, '
                        'understand coordinate geometry basics.'
                    ),
                    'prerequisites': ['Basic Arithmetic & Number Sense', 'Algebra Fundamentals'],
                },
                {
                    'order': 4, 'name': 'Trigonometry Fundamentals',
                    'description': (
                        'Understand trigonometric ratios, solve right triangles, apply trigonometric '
                        'identities, work with the unit circle, and solve trigonometric equations.'
                    ),
                    'prerequisites': ['Geometry', 'Algebra Fundamentals'],
                },
                {
                    'order': 5, 'name': 'Pre-Calculus',
                    'description': (
                        'Master functions and their properties, understand limits and continuity concepts, '
                        'work with complex numbers, analyze sequences and series, study conic sections.'
                    ),
                    'prerequisites': ['Algebra Fundamentals', 'Geometry', 'Trigonometry Fundamentals'],
                },
                {
                    'order': 6, 'name': 'Differential Calculus',
                    'description': (
                        'Understand the concept of derivatives, master differentiation techniques, '
                        'apply derivatives to real-world problems, analyze function behavior using '
                        'derivatives, and solve optimization problems.'
                    ),
                    'prerequisites': ['Pre-Calculus'],
                },
                {
                    'order': 7, 'name': 'Integral Calculus',
                    'description': (
                        'Understand the concept of integration, master integration techniques, '
                        'apply integrals to calculate areas, volumes, and other quantities, '
                        'understand the Fundamental Theorem of Calculus.'
                    ),
                    'prerequisites': ['Differential Calculus'],
                },
                {
                    'order': 8, 'name': 'Multivariable Calculus',
                    'description': (
                        'Extend calculus to functions of several variables, calculate partial derivatives '
                        'and multiple integrals, work with vector calculus.'
                    ),
                    'prerequisites': ['Differential Calculus', 'Integral Calculus'],
                },
                {
                    'order': 9, 'name': 'Linear Algebra',
                    'description': (
                        'Understand vector spaces and linear transformations, master matrix operations, '
                        'solve systems of linear equations, calculate eigenvalues and eigenvectors.'
                    ),
                    'prerequisites': ['Algebra Fundamentals', 'Pre-Calculus'],
                },
                {
                    'order': 10, 'name': 'Ordinary Differential Equations (ODEs)',
                    'description': (
                        'Classify and solve different types of ODEs, understand solution methods for '
                        'first and higher-order equations, apply ODEs to model physical systems.'
                    ),
                    'prerequisites': ['Differential Calculus', 'Integral Calculus'],
                },
                {
                    'order': 11, 'name': 'Partial Differential Equations (PDEs)',
                    'description': (
                        'Understand the nature of PDEs, classify PDEs, solve common PDEs, '
                        'apply PDEs to engineering problems.'
                    ),
                    'prerequisites': ['Multivariable Calculus', 'Ordinary Differential Equations (ODEs)'],
                },
                {
                    'order': 12, 'name': 'Fourier Analysis',
                    'description': (
                        'Understand Fourier series and their applications, compute Fourier coefficients, '
                        'apply Fourier transforms, use Fourier methods in signal processing.'
                    ),
                    'prerequisites': ['Integral Calculus', 'Trigonometry Fundamentals'],
                },
                {
                    'order': 13, 'name': 'Laplace Transforms',
                    'description': (
                        'Understand and compute Laplace transforms, apply inverse Laplace transforms, '
                        'use Laplace transforms to solve ODEs, apply transforms to engineering problems.'
                    ),
                    'prerequisites': ['Integral Calculus', 'Ordinary Differential Equations (ODEs)'],
                },
            ],
        },
        {
            'name': 'Circuit Analysis Fundamentals',
            'code': 'ENG301',
            'description': (
                'Systematic analysis of DC and AC circuits using fundamental laws and network theorems. '
                'Covers KVL/KCL, Thevenin/Norton equivalents, phasor analysis, and transient response.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'DC Circuit Analysis',
                    'description': (
                        "Ohm's Law, KVL, KCL, series/parallel resistors, voltage and current dividers, "
                        'nodal and mesh analysis, power calculations.'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'Network Theorems',
                    'description': (
                        'Superposition, Thevenin and Norton equivalents, maximum power transfer theorem, '
                        'source transformation, reciprocity and substitution theorems.'
                    ),
                    'prerequisites': ['DC Circuit Analysis'],
                },
                {
                    'order': 3, 'name': 'AC Phasor Analysis',
                    'description': (
                        'Sinusoidal signals, RMS values, phasors, impedance of R/L/C elements, '
                        'phasor domain KVL/KCL, impedance combinations.'
                    ),
                    'prerequisites': ['DC Circuit Analysis'],
                },
                {
                    'order': 4, 'name': 'Transient Analysis',
                    'description': (
                        'First-order RC and RL circuits, time constants, step response, '
                        'second-order RLC circuits, natural and forced response, damping.'
                    ),
                    'prerequisites': ['DC Circuit Analysis'],
                },
                {
                    'order': 5, 'name': 'Frequency Response & Resonance',
                    'description': (
                        'Transfer functions, Bode magnitude and phase plots, resonance in series '
                        'and parallel RLC, bandwidth, Q factor, filter fundamentals.'
                    ),
                    'prerequisites': ['AC Phasor Analysis', 'Transient Analysis'],
                },
                {
                    'order': 6, 'name': 'AC Power Analysis',
                    'description': (
                        'Instantaneous power, average power, reactive power, apparent power, '
                        'power factor and correction, three-phase circuits basics.'
                    ),
                    'prerequisites': ['AC Phasor Analysis'],
                },
            ],
        },
        {
            'name': 'Analog Electronics',
            'code': 'ENG571',
            'description': (
                'Fundamentals of analog electronic devices and circuits, following Sedra/Smith 8th edition. '
                'Covers diodes, MOSFETs, BJTs, op-amps, amplifiers, feedback, filters, and oscillators.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'Signals & Amplifiers',
                    'description': (
                        'Signal types, amplifier models, voltage/current/power gain in dB, '
                        'frequency response, bandwidth, ideal vs. real amplifier characteristics.'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'Operational Amplifiers',
                    'description': (
                        'Ideal op-amp model, virtual short and virtual open, inverting and non-inverting '
                        'amplifiers, summing, difference, integrator, differentiator, instrumentation amp.'
                    ),
                    'prerequisites': ['Signals & Amplifiers'],
                },
                {
                    'order': 3, 'name': 'Diodes',
                    'description': (
                        'P-N junction theory, diode equation, small-signal model, rectifiers (half/full-wave), '
                        'clippers, clampers, zener regulators, LED and photodiode basics.'
                    ),
                    'prerequisites': ['Signals & Amplifiers'],
                },
                {
                    'order': 4, 'name': 'MOSFETs',
                    'description': (
                        'MOSFET structure and operation (nMOS/pMOS), IV characteristics, '
                        'large-signal model, small-signal model (gm, ro), biasing circuits.'
                    ),
                    'prerequisites': ['Diodes'],
                },
                {
                    'order': 5, 'name': 'Bipolar Junction Transistors (BJTs)',
                    'description': (
                        'BJT structure and operation (NPN/PNP), IV characteristics, '
                        'large-signal model (active/saturation/cutoff), small-signal model (rπ, gm, ro).'
                    ),
                    'prerequisites': ['Diodes'],
                },
                {
                    'order': 6, 'name': 'Transistor Amplifiers',
                    'description': (
                        'Common-source, common-gate, common-drain MOSFET amplifiers; '
                        'common-emitter, common-base, common-collector BJT amplifiers; '
                        'gain, input/output resistance, biasing for linear operation.'
                    ),
                    'prerequisites': ['MOSFETs', 'Bipolar Junction Transistors (BJTs)'],
                },
                {
                    'order': 7, 'name': 'Frequency Response of Amplifiers',
                    'description': (
                        'Miller theorem, low-frequency response (coupling/bypass capacitors), '
                        'high-frequency response (Cgs, Cgd, Cπ, Cμ), dominant-pole approximation, '
                        'gain-bandwidth product.'
                    ),
                    'prerequisites': ['Transistor Amplifiers'],
                },
                {
                    'order': 8, 'name': 'Feedback Amplifiers',
                    'description': (
                        'Feedback topologies (series-series, series-shunt, shunt-series, shunt-shunt), '
                        'effect on gain, bandwidth, input/output resistance, stability basics.'
                    ),
                    'prerequisites': ['Transistor Amplifiers'],
                },
                {
                    'order': 9, 'name': 'Filters & Tuned Amplifiers',
                    'description': (
                        'Active filter types (LP/HP/BP/BR), Butterworth and Chebyshev approximations, '
                        'Sallen-Key topology, second-order filter design, tuned amplifier basics.'
                    ),
                    'prerequisites': ['Operational Amplifiers', 'Frequency Response of Amplifiers'],
                },
                {
                    'order': 10, 'name': 'Oscillators',
                    'description': (
                        'Barkhausen criterion, RC oscillators (Wien bridge, phase shift), '
                        'LC oscillators (Colpitts, Hartley), crystal oscillators, 555 timer.'
                    ),
                    'prerequisites': ['Feedback Amplifiers'],
                },
            ],
        },
        {
            'name': 'Digital Signal Processing',
            'code': 'ENG572',
            'description': (
                'Discrete-time signals and systems, frequency analysis, filter design, and spectral '
                'computation. Based on DSP First 2nd edition. Includes MATLAB applications throughout.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'Sinusoids & Phasors',
                    'description': (
                        'Complex exponentials, sinusoid representation, phasors, '
                        'adding sinusoids of the same frequency, beating phenomena.'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'Spectrum Representation',
                    'description': (
                        'Two-sided spectrum, spectral lines, amplitude and phase spectrum, '
                        'spectrum of AM and FM signals, bandwidth definition.'
                    ),
                    'prerequisites': ['Sinusoids & Phasors'],
                },
                {
                    'order': 3, 'name': 'Sampling & Aliasing',
                    'description': (
                        'Sampling theorem (Nyquist), aliasing, reconstruction, '
                        'ideal sampling, anti-aliasing filters, practical ADC considerations.'
                    ),
                    'prerequisites': ['Spectrum Representation'],
                },
                {
                    'order': 4, 'name': 'FIR Filters',
                    'description': (
                        'Convolution sum, impulse response, FIR filter structure, '
                        'linear phase FIR, windowed sinc design, difference equation.'
                    ),
                    'prerequisites': ['Sampling & Aliasing'],
                },
                {
                    'order': 5, 'name': 'Frequency Response of FIR Filters',
                    'description': (
                        'Frequency response H(e^jω), magnitude and phase response, '
                        'ideal filters, moving average filter, cascade filters.'
                    ),
                    'prerequisites': ['FIR Filters'],
                },
                {
                    'order': 6, 'name': 'DTFT',
                    'description': (
                        'Discrete-time Fourier Transform definition, properties (linearity, shift, '
                        'convolution, Parseval), DTFT pairs, frequency-domain analysis.'
                    ),
                    'prerequisites': ['Frequency Response of FIR Filters'],
                },
                {
                    'order': 7, 'name': 'DFT & FFT',
                    'description': (
                        'DFT definition and matrix form, DFT as sampled DTFT, zero-padding, '
                        'FFT algorithm (Cooley-Tukey), MATLAB fft(), spectral leakage, windowing.'
                    ),
                    'prerequisites': ['DTFT'],
                },
                {
                    'order': 8, 'name': 'z-Transforms',
                    'description': (
                        'z-Transform definition and region of convergence, z-Transform pairs and properties, '
                        'inverse z-Transform, poles and zeros, relation to DTFT.'
                    ),
                    'prerequisites': ['DTFT'],
                },
                {
                    'order': 9, 'name': 'IIR Filters',
                    'description': (
                        'IIR filter structure, recursive difference equations, pole-zero design, '
                        'bilinear transform from analog prototypes, Butterworth IIR, stability condition.'
                    ),
                    'prerequisites': ['z-Transforms', 'FIR Filters'],
                },
                {
                    'order': 10, 'name': 'MATLAB for DSP',
                    'description': (
                        'MATLAB syntax and workspace, vectors and matrices, plotting, '
                        'signal generation, fft/ifft, filter(), freqz(), spectrogram basics.'
                    ),
                    'prerequisites': ['FIR Filters'],
                },
            ],
        },
        {
            'name': 'Embedded Systems',
            'code': 'ENG320',
            'description': (
                'Microcontroller-based embedded system design covering hardware peripherals, '
                'firmware programming, real-time concepts, and IoT connectivity.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'Microcontroller Architecture',
                    'description': (
                        'Harvard vs von Neumann, CPU registers, ALU, memory map, '
                        'clock systems, reset sources, ARM Cortex-M overview.'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'GPIO & Digital I/O',
                    'description': (
                        'Port registers, input/output configuration, pull-up/pull-down resistors, '
                        'open-drain vs push-pull, debouncing, GPIO register programming.'
                    ),
                    'prerequisites': ['Microcontroller Architecture'],
                },
                {
                    'order': 3, 'name': 'Interrupts & Timers',
                    'description': (
                        'Interrupt request (IRQ), NVIC, interrupt priority, ISR writing, '
                        'timer modes (output compare, input capture), systick timer.'
                    ),
                    'prerequisites': ['GPIO & Digital I/O'],
                },
                {
                    'order': 4, 'name': 'PWM Generation',
                    'description': (
                        'PWM principles, duty cycle, frequency, timer-based PWM, '
                        'motor speed control, servo control, LED dimming applications.'
                    ),
                    'prerequisites': ['Interrupts & Timers'],
                },
                {
                    'order': 5, 'name': 'ADC & DAC',
                    'description': (
                        'ADC resolution, sampling rate, input voltage range, SAR ADC, '
                        'ADC triggering, DMA with ADC, DAC operation, R-2R ladder.'
                    ),
                    'prerequisites': ['GPIO & Digital I/O'],
                },
                {
                    'order': 6, 'name': 'Serial Communication Protocols',
                    'description': (
                        'UART framing and baud rate calculation, SPI (CPOL/CPHA modes), '
                        'I2C addressing and ACK/NACK, RS-485 basics, CAN bus introduction.'
                    ),
                    'prerequisites': ['GPIO & Digital I/O'],
                },
                {
                    'order': 7, 'name': 'Memory & Storage',
                    'description': (
                        'Flash memory, SRAM, EEPROM, wear leveling, memory-mapped I/O, '
                        'stack and heap layout, linker script basics, bootloaders.'
                    ),
                    'prerequisites': ['Microcontroller Architecture'],
                },
                {
                    'order': 8, 'name': 'RTOS Concepts',
                    'description': (
                        'Task scheduling, preemption, context switching, semaphores and mutexes, '
                        'message queues, FreeRTOS API basics, priority inversion.'
                    ),
                    'prerequisites': ['Interrupts & Timers'],
                },
                {
                    'order': 9, 'name': 'IoT & Connectivity',
                    'description': (
                        'Wi-Fi and BLE modules (ESP32/Nordic), MQTT protocol, HTTP REST APIs, '
                        'JSON parsing on embedded targets, OTA firmware updates.'
                    ),
                    'prerequisites': ['Serial Communication Protocols', 'RTOS Concepts'],
                },
            ],
        },
        {
            'name': 'Control Systems',
            'code': 'ENG325',
            'description': (
                'Analysis and design of feedback control systems, including time-domain, '
                'frequency-domain, and state-space methods. MATLAB/Simulink used throughout.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'Laplace Transforms & Transfer Functions',
                    'description': (
                        'Laplace transform review, transfer function derivation from differential equations, '
                        'poles, zeros, and system order, standard first and second-order forms.'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'Block Diagram Algebra',
                    'description': (
                        'Series, parallel, and feedback block reductions, Mason\'s gain formula, '
                        'signal flow graphs, closed-loop transfer function derivation.'
                    ),
                    'prerequisites': ['Laplace Transforms & Transfer Functions'],
                },
                {
                    'order': 3, 'name': 'Time-Domain Response',
                    'description': (
                        'Step and impulse response, rise time, settling time, overshoot, '
                        'steady-state error, system type and error constants.'
                    ),
                    'prerequisites': ['Block Diagram Algebra'],
                },
                {
                    'order': 4, 'name': 'Stability Analysis',
                    'description': (
                        'BIBO stability, Routh-Hurwitz criterion, marginal stability, '
                        'characteristic equation roots, gain and phase margins definitions.'
                    ),
                    'prerequisites': ['Time-Domain Response'],
                },
                {
                    'order': 5, 'name': 'Root Locus',
                    'description': (
                        'Root locus rules (breakaway, asymptotes, angles), sketching root locus, '
                        'gain selection for desired pole placement, compensator design via root locus.'
                    ),
                    'prerequisites': ['Stability Analysis'],
                },
                {
                    'order': 6, 'name': 'Bode & Nyquist Analysis',
                    'description': (
                        'Bode magnitude and phase plots, gain and phase margins graphically, '
                        'Nyquist plot and criterion, minimum-phase vs. non-minimum-phase.'
                    ),
                    'prerequisites': ['Stability Analysis'],
                },
                {
                    'order': 7, 'name': 'PID Controllers',
                    'description': (
                        'P, I, D action effects, PID transfer function, Ziegler-Nichols tuning rules, '
                        'anti-windup, derivative filter, practical PID implementation.'
                    ),
                    'prerequisites': ['Time-Domain Response', 'Stability Analysis'],
                },
                {
                    'order': 8, 'name': 'State-Space Representation',
                    'description': (
                        'State variables, A/B/C/D matrices, conversion from transfer function, '
                        'state transition matrix, controllability and observability, Lyapunov stability.'
                    ),
                    'prerequisites': ['Laplace Transforms & Transfer Functions'],
                },
                {
                    'order': 9, 'name': 'MATLAB & Simulink for Control',
                    'description': (
                        'tf(), ss(), bode(), rlocus(), step() in MATLAB, building Simulink block diagrams, '
                        'PID tuner app, linearisation, simulation of nonlinear systems.'
                    ),
                    'prerequisites': ['PID Controllers', 'Bode & Nyquist Analysis'],
                },
            ],
        },
        {
            'name': 'Electrical Machines & Motors',
            'code': 'ENG574',
            'description': (
                'Principles and analysis of transformers, DC machines, AC induction motors, '
                'synchronous machines, and variable-speed drives for industrial applications.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'Transformer Theory',
                    'description': (
                        'Ideal transformer, turns ratio, impedance transformation, '
                        'equivalent circuit, voltage regulation, efficiency, losses.'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'DC Machines',
                    'description': (
                        'DC generator/motor construction, EMF equation, armature reaction, '
                        'separately excited and shunt motors, speed-torque characteristics.'
                    ),
                    'prerequisites': ['Transformer Theory'],
                },
                {
                    'order': 3, 'name': 'AC Induction Motors',
                    'description': (
                        'Rotating magnetic field, slip, equivalent circuit, torque-speed curve, '
                        'starting methods, losses, efficiency, nameplate data interpretation.'
                    ),
                    'prerequisites': ['Transformer Theory'],
                },
                {
                    'order': 4, 'name': 'Synchronous Machines',
                    'description': (
                        'Synchronous generator construction, EMF phasor diagram, salient pole vs round rotor, '
                        'synchronous motor operation, V-curves, power angle characteristic.'
                    ),
                    'prerequisites': ['AC Induction Motors'],
                },
                {
                    'order': 5, 'name': 'Motor Starting & Protection',
                    'description': (
                        'Direct-on-line starting, star-delta starter, soft starter, overload protection, '
                        'thermal protection, contactors and motor control centres (MCC).'
                    ),
                    'prerequisites': ['AC Induction Motors', 'DC Machines'],
                },
                {
                    'order': 6, 'name': 'Variable Speed Drives',
                    'description': (
                        'V/Hz control, vector control (FOC), inverter basics, PWM switching, '
                        'drive parameters and commissioning, regenerative braking.'
                    ),
                    'prerequisites': ['Motor Starting & Protection'],
                },
                {
                    'order': 7, 'name': 'Special Machines',
                    'description': (
                        'Stepper motor (full/half step), BLDC motor, servo motors, '
                        'linear motors, switched reluctance motors, applications in robotics.'
                    ),
                    'prerequisites': ['Variable Speed Drives'],
                },
            ],
        },
        {
            'name': 'Power Systems',
            'code': 'ENG574B',
            'description': (
                'Analysis of electric power generation, transmission, and distribution systems, '
                'including load flow, fault analysis, and protection.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'Power System Structure',
                    'description': (
                        'Generation, transmission, and distribution overview, '
                        'voltage levels, single-line diagrams, NEM basics (Australian grid).'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'Per-Unit Analysis',
                    'description': (
                        'Per-unit system definition, base quantities, converting between bases, '
                        'per-unit equivalent circuits, advantages of per-unit analysis.'
                    ),
                    'prerequisites': ['Power System Structure'],
                },
                {
                    'order': 3, 'name': 'Load Flow Analysis',
                    'description': (
                        'Bus types (slack, PV, PQ), Newton-Raphson load flow, Gauss-Seidel method, '
                        'Jacobian matrix, convergence, power flow results interpretation.'
                    ),
                    'prerequisites': ['Per-Unit Analysis'],
                },
                {
                    'order': 4, 'name': 'Fault Analysis',
                    'description': (
                        'Symmetrical three-phase faults, subtransient/transient/steady-state fault currents, '
                        'sequence networks (positive/negative/zero), unsymmetrical fault analysis.'
                    ),
                    'prerequisites': ['Per-Unit Analysis'],
                },
                {
                    'order': 5, 'name': 'Power System Protection',
                    'description': (
                        'Relay types (overcurrent, distance, differential), CT and VT ratios, '
                        'relay co-ordination, protection zones, circuit breakers, SCADA monitoring.'
                    ),
                    'prerequisites': ['Fault Analysis'],
                },
                {
                    'order': 6, 'name': 'Power Electronics in Power Systems',
                    'description': (
                        'FACTS devices (SVC, STATCOM), HVDC basics, thyristor rectifiers, '
                        'grid-connected inverters, active filters, harmonic analysis.'
                    ),
                    'prerequisites': ['Power System Protection'],
                },
            ],
        },
        {
            'name': 'Linux Fundamentals (LFCA)',
            'code': 'LFCA',
            'description': (
                'Practical Linux skills targeting the Linux Foundation Certified Associate (LFCA) exam. '
                'Covers CLI, file system, processes, networking, scripting, and system security.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'Linux Basics & CLI',
                    'description': (
                        'Linux distributions, kernel and shell overview, terminal navigation, '
                        'essential commands (ls, cd, pwd, cp, mv, rm, mkdir), man pages, tab completion.'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'File System & Permissions',
                    'description': (
                        'Linux FHS (Filesystem Hierarchy Standard), absolute and relative paths, '
                        'file permissions (rwx), chmod, chown, chgrp, SUID/SGID/sticky bit, ACLs.'
                    ),
                    'prerequisites': ['Linux Basics & CLI'],
                },
                {
                    'order': 3, 'name': 'Process Management',
                    'description': (
                        'Process lifecycle, PID, foreground/background, ps, top, htop, kill signals, '
                        'nice and renice, systemd services, journalctl, cron jobs.'
                    ),
                    'prerequisites': ['Linux Basics & CLI'],
                },
                {
                    'order': 4, 'name': 'Networking in Linux',
                    'description': (
                        'ip addr/route, ping, traceroute, ss/netstat, /etc/hosts, DNS resolution, '
                        'SSH basics, scp/rsync, firewall with iptables/nftables/ufw.'
                    ),
                    'prerequisites': ['Linux Basics & CLI'],
                },
                {
                    'order': 5, 'name': 'Shell Scripting',
                    'description': (
                        'Bash scripting basics, variables, conditionals (if/case), loops (for/while), '
                        'functions, positional parameters, exit codes, pipes and redirection.'
                    ),
                    'prerequisites': ['File System & Permissions'],
                },
                {
                    'order': 6, 'name': 'Package Management',
                    'description': (
                        'APT (Debian/Ubuntu): apt install/remove/update/upgrade, dpkg, '
                        'RPM/YUM/DNF (RHEL/CentOS/Fedora), snap and flatpak, compiling from source.'
                    ),
                    'prerequisites': ['Linux Basics & CLI'],
                },
                {
                    'order': 7, 'name': 'System Security',
                    'description': (
                        'User and group management, sudo configuration, PAM, SSH key-based authentication, '
                        'SELinux/AppArmor basics, auditd, fail2ban, common hardening steps.'
                    ),
                    'prerequisites': ['File System & Permissions', 'Networking in Linux'],
                },
                {
                    'order': 8, 'name': 'LFCA Exam Preparation',
                    'description': (
                        'LFCA exam domains and weightings, practice questions, common pitfalls, '
                        'lab exercises covering all exam objectives.'
                    ),
                    'prerequisites': [
                        'Linux Basics & CLI', 'File System & Permissions', 'Process Management',
                        'Networking in Linux', 'Shell Scripting', 'Package Management', 'System Security',
                    ],
                },
            ],
        },
        {
            'name': 'Networking Fundamentals',
            'code': 'NET101',
            'description': (
                'Comprehensive networking course aligned with CompTIA Network+ and CCNA objectives. '
                'Includes industrial networking protocols relevant to automation.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'OSI Model & TCP/IP',
                    'description': (
                        '7-layer OSI model functions and PDU names, TCP/IP 4-layer model, '
                        'encapsulation and de-encapsulation, comparison of OSI and TCP/IP.'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'IP Addressing & Subnetting',
                    'description': (
                        'IPv4 address classes, private ranges, subnet masks, CIDR notation, '
                        'subnetting calculations (VLSM), IPv6 addressing basics.'
                    ),
                    'prerequisites': ['OSI Model & TCP/IP'],
                },
                {
                    'order': 3, 'name': 'Routing Protocols',
                    'description': (
                        'Static routing, dynamic routing (RIP, OSPF, BGP), routing tables, '
                        'administrative distance, OSPF cost calculation, default gateway.'
                    ),
                    'prerequisites': ['IP Addressing & Subnetting'],
                },
                {
                    'order': 4, 'name': 'Switching & VLANs',
                    'description': (
                        'Ethernet frames and MAC addresses, switches vs hubs, STP, '
                        'VLAN configuration, 802.1Q tagging, inter-VLAN routing, port security.'
                    ),
                    'prerequisites': ['OSI Model & TCP/IP'],
                },
                {
                    'order': 5, 'name': 'Wireless Networking',
                    'description': (
                        '802.11 standards (a/b/g/n/ac/ax), SSID and BSS, WPA2/WPA3 security, '
                        'AP placement, CSMA/CA, 2.4 GHz vs 5 GHz, channel planning.'
                    ),
                    'prerequisites': ['OSI Model & TCP/IP'],
                },
                {
                    'order': 6, 'name': 'Network Security',
                    'description': (
                        'Firewalls (stateful/stateless), ACLs, NAT/PAT, VPN (IPsec, SSL/TLS), '
                        'common attacks (ARP spoofing, MITM, DoS), IDS/IPS basics.'
                    ),
                    'prerequisites': ['Routing Protocols', 'Switching & VLANs'],
                },
                {
                    'order': 7, 'name': 'Network Troubleshooting',
                    'description': (
                        'OSI-layer troubleshooting methodology, ping, traceroute, nslookup/dig, '
                        'Wireshark basics, cable testing, common connectivity issues and fixes.'
                    ),
                    'prerequisites': ['Routing Protocols', 'Switching & VLANs'],
                },
                {
                    'order': 8, 'name': 'Industrial Networking',
                    'description': (
                        'Modbus TCP/RTU, EtherNet/IP, PROFINET, OPC-UA, MQTT for IIoT, '
                        'network segmentation in industrial environments, demilitarised zones (DMZ).'
                    ),
                    'prerequisites': ['Network Security', 'Network Troubleshooting'],
                },
            ],
        },
        {
            'name': 'Industrial Automation & Robotics',
            'code': 'ENG450',
            'description': (
                'PLC programming, SCADA systems, industrial protocols, motion control, '
                'robot kinematics, ROS, and functional safety standards for industrial automation.'
            ),
            'topics': [
                {
                    'order': 1, 'name': 'PLC Fundamentals',
                    'description': (
                        'PLC architecture (CPU, I/O modules, power supply, comms), scan cycle, '
                        'PLC vs microcontroller, Siemens S7/Allen-Bradley ControlLogix overview.'
                    ),
                    'prerequisites': [],
                },
                {
                    'order': 2, 'name': 'Ladder Logic',
                    'description': (
                        'Contacts (NO/NC), coils, latching, timers (TON/TOF/TP), counters (CTU/CTD), '
                        'comparison instructions, math instructions, program flow (JSR/RET).'
                    ),
                    'prerequisites': ['PLC Fundamentals'],
                },
                {
                    'order': 3, 'name': 'Structured Text (IEC 61131-3)',
                    'description': (
                        'IEC 61131-3 language overview (LD/FBD/ST/IL/SFC), Structured Text syntax, '
                        'variables and data types, IF/CASE/FOR/WHILE, function blocks, '
                        'OSCAT library functions.'
                    ),
                    'prerequisites': ['Ladder Logic'],
                },
                {
                    'order': 4, 'name': 'SCADA & HMI',
                    'description': (
                        'SCADA architecture (field devices → RTU/PLC → SCADA server → HMI), '
                        'historian, alarm management, HMI design principles, Ignition/WinCC basics.'
                    ),
                    'prerequisites': ['PLC Fundamentals'],
                },
                {
                    'order': 5, 'name': 'Industrial Protocols',
                    'description': (
                        'Modbus (RTU/TCP) registers and function codes, EtherNet/IP CIP objects, '
                        'PROFIBUS/PROFINET, OPC-UA server/client model, DH+ and DeviceNet legacy.'
                    ),
                    'prerequisites': ['SCADA & HMI'],
                },
                {
                    'order': 6, 'name': 'Motion Control',
                    'description': (
                        'Servo drives and motion axes, position/velocity/torque loops, '
                        'cam profiles, electronic gearing, trapezoidal motion profiles, '
                        'PLCopen Motion Control function blocks.'
                    ),
                    'prerequisites': ['Structured Text (IEC 61131-3)'],
                },
                {
                    'order': 7, 'name': 'Robot Kinematics',
                    'description': (
                        'DOF and joint types, DH parameters, forward kinematics, '
                        'inverse kinematics (analytical and numerical), workspace analysis, Jacobian.'
                    ),
                    'prerequisites': ['Motion Control'],
                },
                {
                    'order': 8, 'name': 'ROS Basics',
                    'description': (
                        'ROS 2 architecture (nodes, topics, services, actions), colcon build system, '
                        'rqt_graph, tf2 transforms, writing publisher/subscriber in Python/C++.'
                    ),
                    'prerequisites': ['Robot Kinematics'],
                },
                {
                    'order': 9, 'name': 'Functional Safety (IEC 61508)',
                    'description': (
                        'Safety lifecycle, Safety Integrity Levels (SIL 1-4), FMEA/HAZOP, '
                        'safe state design, SIL verification (PFD/PFH), safety PLC concepts, '
                        'IEC 62061 and ISO 13849 for machinery safety.'
                    ),
                    'prerequisites': ['SCADA & HMI', 'Structured Text (IEC 61131-3)'],
                },
            ],
        },
    ]

    # ------------------------------------------------------------------
    # 4. Create courses and topics idempotently
    # ------------------------------------------------------------------
    for course_data in courses_data:
        course, _ = Course.objects.get_or_create(
            name=course_data['name'],
            created_by=system_user,
            defaults={
                'code': course_data['code'],
                'description': course_data['description'],
            }
        )

        topics_by_name = {}
        for topic_data in course_data['topics']:
            topic, _ = Topic.objects.get_or_create(
                course=course,
                name=topic_data['name'],
                defaults={
                    'description': topic_data['description'],
                    'order': topic_data['order'],
                }
            )
            topics_by_name[topic_data['name']] = topic

        # Set up prerequisites (second pass so all topics exist)
        for topic_data in course_data['topics']:
            topic = topics_by_name[topic_data['name']]
            for prereq_name in topic_data['prerequisites']:
                if prereq_name in topics_by_name:
                    prereq = topics_by_name[prereq_name]
                    topic.prerequisites.add(prereq)

    # ------------------------------------------------------------------
    # 5. Back-fill CourseEnrollment for all existing non-system users
    # ------------------------------------------------------------------
    system_courses = Course.objects.filter(created_by=system_user)
    non_system_users = User.objects.exclude(username='system')

    for user in non_system_users:
        for course in system_courses:
            CourseEnrollment.objects.get_or_create(
                user=user,
                course=course,
                defaults={'status': 'studying'}
            )


def reverse_seed(apps, schema_editor):
    # Intentionally a no-op: course data is user-facing and should not be
    # automatically destroyed on migrate --backwards.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0012_learning_intelligence'),
    ]

    operations = [
        migrations.RunPython(seed_courses, reverse_seed),
    ]
