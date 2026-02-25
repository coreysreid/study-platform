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
        name='Industrial Automation & Robotics', created_by=system_user
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
    # 1. PLC Fundamentals
    # -------------------------------------------------------------------------
    add_cards('PLC Fundamentals', [
        {
            'question': 'What is a PLC and what are its main hardware components?',
            'answer': 'A PLC (Programmable Logic Controller) is an industrial digital computer for controlling manufacturing equipment. Components: CPU (processor + memory), Power Supply, Input modules (digital/analogue), Output modules (digital/analogue), Communication interfaces. Housed in a rack or as compact unit.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Describe the PLC scan cycle.',
            'answer': 'Repeating cycle: 1) Read inputs: sample all input signals into the input image table. 2) Execute program: run the control program using the input image. 3) Write outputs: update outputs from the output image table. 4) Housekeeping: comms, diagnostics. Typical scan time: 1–100 ms. The output image is not updated during program execution.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are the IEC 61131-3 programming languages?',
            'answer': '1) Ladder Diagram (LD): relay logic graphical representation. 2) Function Block Diagram (FBD): interconnected function blocks. 3) Structured Text (ST): Pascal-like high-level language. 4) Instruction List (IL): assembly-like (deprecated in new standard). 5) Sequential Function Chart (SFC): state-machine diagram. Most PLCs support all five.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How does a PLC handle digital input filtering and debouncing?',
            'answer': 'Input filters apply a time delay (typically 1–20 ms, configurable) before registering an input change, filtering electrical noise and contact bounce. Some PLCs allow individual channel filter times. High-speed inputs (encoder, counter) bypass filters or use dedicated hardware counters.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are the key PLC safety features for industrial environments?',
            'answer': 'Watchdog timer: resets CPU if scan cycle exceeds limit (detects infinite loops). Redundancy: dual CPUs, hot-standby. Battery backup: retains memory during power loss. Input/output diagnostics: wire-break detection on smart modules. Fail-safe outputs: de-energise on CPU fault. Safety PLCs: comply with IEC 61508 SIL.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the difference between a safety PLC and a standard PLC?',
            'answer': 'Safety PLC (SIL/PLe rated): certified to IEC 61508/ISO 13849. Features: dual redundant CPUs with cross-checking, certified software, safe I/O modules with diagnostics (short-circuit, wire-break), certified programming environment, SIL-rated communication. Used where failures could injure people. Standard PLC is not certified for safety functions.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 2. Ladder Logic
    # -------------------------------------------------------------------------
    add_cards('Ladder Logic', [
        {
            'question': 'Explain the basic elements of a ladder logic rung.',
            'answer': 'A rung consists of: Left power rail — contacts (conditions) — output coil — right power rail. Contacts: Normally Open (NO, ──┤ ├──): passes power when bit=1. Normally Closed (NC, ──┤/├──): passes power when bit=0. Coil (──( )──): sets/resets a bit based on rung condition. Power flows left to right if all contacts are energised.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Implement a motor start-stop seal circuit in ladder logic.',
            'answer': 'Rung: [Start_NO] parallel with [Motor_Run_NO] in series with [Stop_NC] → (Motor_Run coil). Logic: pressing Start momentarily closes the NO contact. Motor_Run coil energises and seals (latches) via the parallel Motor_Run contact. Stop NC opens the rung, de-energising the coil. The parallel contact maintains the coil energised after Start is released.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are TON and TOF timer instructions in ladder logic?',
            'answer': 'TON (Timer On Delay): output turns ON after input has been continuously ON for preset time (PT). Used for delays before activation. TOF (Timer Off Delay): output turns OFF after input has gone OFF for preset time. Used for delayed shutdowns. Both have: Preset (PT), Accumulated (ET), Enable output, Done output.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do CTU (Count Up) and CTD (Count Down) counters work?',
            'answer': 'CTU: counts rising edges on CU input. When accumulated count CV ≥ preset PV, Q output goes HIGH. Reset input R clears CV to 0. CTD: counts down from PV on CD input. When CV ≤ 0, Q output goes HIGH. LD input loads CV with PV. Both track accumulated value.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Describe how to implement a three-phase motor with interlocking in ladder logic.',
            'answer': '',
            'hint': 'Use interlocking contacts to prevent simultaneous forward/reverse',
            'difficulty': 'hard',
            'question_type': 'step_by_step',
            'uses_latex': False,
            'steps': [
                {'move': 'Forward rung', 'detail': '[FWD_Start NO] ∥ [FWD_Run NO] + [Stop NC] + [REV_Run NC] → (FWD_Run)'},
                {'move': 'Reverse rung', 'detail': '[REV_Start NO] ∥ [REV_Run NO] + [Stop NC] + [FWD_Run NC] → (REV_Run)'},
                {'move': 'Interlock explanation', 'detail': 'REV_Run NC in forward rung, FWD_Run NC in reverse rung prevent simultaneous energisation'},
                {'move': 'Contactor outputs', 'detail': 'FWD_Run coil drives FWD_KM contactor; REV_Run drives REV_KM; REV_KM swaps two supply phases'},
                {'move': 'Safety note', 'detail': 'Hardware interlocking (mechanical or electrical) also required — ladder software interlock alone is insufficient for safety'},
            ],
        },
        {
            'question': 'What is the difference between SET/RESET (latch) coils and normal output coils?',
            'answer': 'Normal coil: output state follows rung condition — ON when rung is true, OFF when false. SET coil (S): latches bit ON when rung goes true; does not reset when rung goes false. RESET coil (R): clears bit when rung goes true. SET/RESET pairs implement latching (bistable) memory without a seal circuit.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 3. Structured Text (IEC 61131-3)
    # -------------------------------------------------------------------------
    add_cards('Structured Text (IEC 61131-3)', [
        {
            'question': 'What is Structured Text and what are its key language constructs?',
            'answer': 'ST is a high-level, Pascal-like IEC 61131-3 language. Constructs: IF/THEN/ELSIF/ELSE/END_IF, CASE/OF/END_CASE, FOR/TO/BY/DO/END_FOR, WHILE/DO/END_WHILE, REPEAT/UNTIL/END_REPEAT. Supports functions, function blocks, data types (INT, REAL, BOOL, STRING, ARRAY, STRUCT), and standard operators.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a Function Block (FB) in IEC 61131-3?',
            'answer': 'A Function Block is a reusable software module with: input variables (VAR_INPUT), output variables (VAR_OUTPUT), internal state variables (VAR). Unlike a function, FBs retain state between calls (instances have memory). Used for: PID controllers, timers, counters, communication blocks. Multiple instances of one FB can run independently.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Write a Structured Text IF-ELSE example for a temperature alarm.',
            'answer': 'IF Temperature > HighLimit THEN\n    AlarmHigh := TRUE;\n    AlarmLow := FALSE;\nELSIF Temperature < LowLimit THEN\n    AlarmLow := TRUE;\n    AlarmHigh := FALSE;\nELSE\n    AlarmHigh := FALSE;\n    AlarmLow := FALSE;\nEND_IF;',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you implement a PID controller using Structured Text?',
            'answer': 'Use the standard OSCAT or vendor PID function block: MyPID(Enable := TRUE, SetPoint := SP, Actual := PV, KP := 1.2, TI := 0.5, TD := 0.1, Y_MIN := 0.0, Y_MAX := 100.0); Output := MyPID.Y; Alternatively, implement discrete PID: error := SP - PV; integral := integral + error * dt; derivative := (error - prev_error) / dt; output := Kp*error + Ki*integral + Kd*derivative;',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a CASE statement and when should you use it over IF-ELSE?',
            'answer': 'CASE variable OF\n  0: (* state 0 actions *);\n  1: (* state 1 actions *);\n  2, 3: (* combined states *);\n  ELSE: (* default *);\nEND_CASE;\nUse CASE when switching on a single integer variable with multiple values — cleaner than nested IF-ELSE chains. Ideal for state machine implementations.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are global variables and how are they shared between PLCs in IEC 61131-3?',
            'answer': 'VAR_GLOBAL: variables accessible from any POU (Program Organisation Unit) within the same PLC. In most systems, only one PLC runtime per processor. Between PLCs: use communication (OPC UA, EtherNet/IP I/O, PROFINET, data exchange blocks). VAR_EXTERNAL: locally declares a global variable for use within a POU.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 4. SCADA & HMI
    # -------------------------------------------------------------------------
    add_cards('SCADA & HMI', [
        {
            'question': 'What is SCADA and what are its main components?',
            'answer': 'SCADA (Supervisory Control and Data Acquisition): software system for monitoring and controlling industrial processes over large geographic areas. Components: HMI (operator interface), SCADA server/historian, Communication infrastructure, RTUs/PLCs at field level, Engineering workstation. Examples: Ignition (Inductive Automation), Wonderware, WinCC.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is an HMI and what makes a good HMI screen design?',
            'answer': 'HMI (Human-Machine Interface): the operator\'s graphical interface to the process. Good design principles (ISA-101): use grey/muted process background (not bright), highlight abnormalities in colour (normal = grey), clear process flow representation, consistent navigation, alarm management integrated, critical values readable at a glance. ASM Consortium guidelines.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a historian in SCADA and why is it important?',
            'answer': 'A historian is a time-series database that records process tag values at configured rates. Uses: trend analysis, production reporting, regulatory compliance, process optimisation, root cause analysis. Modern historians (OSIsoft PI, Ignition Tag Historian) can handle millions of data points per second with compression.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is alarm management and what is an alarm flood?',
            'answer': 'Alarm management: systematic approach to configuring, documenting, and monitoring process alarms. Alarm flood: sudden burst of alarms (>10/minute) overwhelming the operator — often during upsets when they need attention most. Addressed by: alarm rationalisation (remove nuisance alarms), suppression, alarm shelving, priority schemes, ANSI/ISA-18.2 standard.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What cybersecurity measures are essential for SCADA systems?',
            'answer': 'Network segmentation (OT/IT separation, DMZ). Remove/disable unnecessary services and protocols. Patch management (carefully tested). Role-based access control. Encrypted communications (OPC UA security). Application whitelisting. Regular backups. Incident response plan. IEC 62443 standard for industrial cybersecurity.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 5. Industrial Protocols
    # -------------------------------------------------------------------------
    add_cards('Industrial Protocols', [
        {
            'question': 'Compare Modbus TCP, EtherNet/IP, and PROFINET for industrial networking.',
            'answer': 'Modbus TCP: simple, widely supported, no device profiles, TCP port 502. EtherNet/IP: CIP over Ethernet, device profiles (motor drives, I/O), UDP for real-time I/O, Rockwell ecosystem. PROFINET: Siemens ecosystem, three classes (RT, IRT, TSN), sub-millisecond timing possible, device profiles, replaces PROFIBUS.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the CAN bus protocol and where is it used?',
            'answer': 'CAN (Controller Area Network): multi-master serial bus using differential signalling (CAN-H, CAN-L). Up to 1 Mbps. CSMA/CD with bit arbitration (priority-based). Message-based, not address-based. Originally automotive; also industrial, medical, marine. CANopen and DeviceNet are higher-layer protocols built on CAN.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is AS-Interface (AS-i) and when would you use it?',
            'answer': 'AS-Interface (Actuator-Sensor Interface): two-wire, flat cable connecting binary sensors and actuators to PLCs. Very simple — power and data on same two wires (26.5V DC). Cycle time: 5 ms. Up to 62 slaves, 248 digital I/O per master. Used for: limit switches, pushbuttons, solenoids at field level beneath PROFIBUS/PROFINET.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is IO-Link and what problem does it solve?',
            'answer': 'IO-Link: point-to-point communication protocol between PLC/controller and smart sensors/actuators over standard 3-wire cable. Provides: bidirectional communication (configuration, diagnostics, process data), device parameterisation, event messages. Solves analogue sensor limitations: digital, precise, self-describing. IEC 61131-9.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is TSN (Time-Sensitive Networking) and its relevance to industrial automation?',
            'answer': 'TSN: IEEE 802.1 standards extending Ethernet with: deterministic timing (802.1AS time sync), traffic scheduling (802.1Qbv), frame preemption (802.1Qbu). Enables standard Ethernet hardware to deliver guaranteed latency for real-time control — closing the gap between IT and OT. Adopted by PROFINET (CC-D), EtherNet/IP, and OPC UA.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 6. Motion Control
    # -------------------------------------------------------------------------
    add_cards('Motion Control', [
        {
            'question': 'What are the three main types of motion control systems?',
            'answer': '1) Open-loop (stepper motors): commands steps without position feedback — cheap but loses steps under overload. 2) Closed-loop (servo): encoder feedback to controller, corrects position error continuously — precise and responsive. 3) Semi-closed loop: encoder on motor shaft, not load — common compromise.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Explain the components of a servo drive system.',
            'answer': 'Motion Controller (PLC, CNC, or dedicated): generates position/velocity/torque commands. Servo Drive (amplifier): receives commands, closes the current/velocity/position loops, drives motor current. Servo Motor: high-torque, low-inertia AC/DC motor. Encoder: position/velocity feedback to drive and controller. Feedback loop: position error → drive → motor → encoder → controller.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the difference between position, velocity, and torque control modes in a servo drive?',
            'answer': 'Torque mode: drive controls motor current (∝ torque) — outer loop (position/velocity) handled by external controller. Velocity mode: drive closes the velocity loop; position controlled externally. Position mode: drive closes both velocity and position loops from step/direction or encoder input. Choose based on what the motion controller handles.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is an S-curve (jerk-limited) motion profile and why is it preferred?',
            'answer': 'An S-curve profile limits jerk (rate of change of acceleration) in addition to acceleration and velocity. Result: smooth, gradual changes in acceleration rather than abrupt steps. Benefits: reduced mechanical stress and vibration, better settling, less wear. Contrast with trapezoidal profile (abrupt acceleration/deceleration).',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'How is encoder resolution related to positioning accuracy?',
            'answer': 'Encoder resolution: pulses per revolution (PPR) or counts per revolution (CPR = 4×PPR for quadrature). Positioning accuracy ≈ one encoder count. E.g. 1000 PPR encoder on 5 mm/rev lead screw: 1 count = 5mm/4000 = 1.25 µm. Accuracy also limited by mechanical backlash, drive stiffness, and thermal effects.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
    ])

    # -------------------------------------------------------------------------
    # 7. Robot Kinematics
    # -------------------------------------------------------------------------
    add_cards('Robot Kinematics', [
        {
            'question': 'What is the difference between forward and inverse kinematics?',
            'answer': 'Forward kinematics (FK): given joint angles/positions, calculate the end-effector position and orientation in Cartesian space. Closed-form solution always exists. Inverse kinematics (IK): given desired end-effector pose, calculate the required joint values. May have multiple solutions, no solution, or require numerical methods.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the Denavit-Hartenberg (DH) convention?',
            'answer': 'A systematic method to define coordinate frames at each robot joint using 4 parameters per link: θi (joint angle), di (link offset), ai (link length), αi (link twist). The homogeneous transformation matrix Ti relates frame i to frame i-1. Multiplying successive Ti matrices gives the complete FK solution.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is the Jacobian matrix in robotics?',
            'answer': 'The Jacobian J relates joint velocities to end-effector Cartesian velocities: ẋ = J·θ̇. Used for: velocity kinematics, force mapping (F = J^T·τ), singularity detection (det(J)=0 → kinematic singularity). Inverse Jacobian or pseudoinverse used for differential IK control.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is a singularity in robot kinematics and why does it matter?',
            'answer': 'A singularity occurs when the robot loses one or more DOF — the Jacobian becomes rank-deficient. Physically: the robot cannot move in certain Cartesian directions, or small Cartesian velocities require infinite joint velocities. Types: workspace boundary singularities, internal singularities (wrist, elbow). Must be avoided in trajectory planning.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Compare serial (articulated) and parallel robot configurations.',
            'answer': 'Serial: links in chain — high workspace, simple FK/IK, lower stiffness, error accumulates through chain. Examples: 6-DOF articulated arm (FANUC, KUKA). Parallel: multiple kinematic chains from base to end-effector — high stiffness and speed, complex IK, smaller workspace. Examples: delta robot (pick-and-place), Stewart platform.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is trajectory planning and what is the difference between joint-space and Cartesian-space planning?',
            'answer': 'Trajectory planning: specifying position as a function of time to achieve smooth, collision-free motion. Joint-space planning: interpolate joint angles directly — simple, predictable joint motion, but Cartesian path is curved and hard to predict. Cartesian-space planning: specify straight-line or curved path in Cartesian space, compute IK at each waypoint — predictable path but requires singularity avoidance.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 8. ROS Basics
    # -------------------------------------------------------------------------
    add_cards('ROS Basics', [
        {
            'question': 'What is ROS and what does it provide?',
            'answer': 'ROS (Robot Operating System): an open-source middleware framework for robot software development. Provides: a communication infrastructure (nodes, topics, services, actions), a build system (colcon/catkin), package management, debugging/visualisation tools (rviz, rqt), a large ecosystem of robot-specific packages. Not a real RTOS — runs on Linux.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Explain the ROS 2 node/topic publish-subscribe model.',
            'answer': 'Nodes: independent processes performing computation. Topics: named communication channels. Publishers: nodes that send data to a topic. Subscribers: nodes that receive data from a topic. Decoupled — publisher doesn\'t know subscribers. Messages: typed data structures (e.g. sensor_msgs/Image). ROS 2 uses DDS (Data Distribution Service) as the underlying transport.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the difference between ROS topics, services, and actions?',
            'answer': 'Topics: asynchronous, continuous publish-subscribe (sensor data, control commands). Services: synchronous request-response (one-time queries, configuration). Actions: for long-running tasks with feedback and cancellation (navigate to goal, pick up object). ROS 2 actions built on topics internally.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a ROS 2 launch file and why is it used?',
            'answer': 'A launch file (Python or XML in ROS 2) starts multiple nodes with specified parameters, remappings, and namespaces in a single command. Eliminates running each node manually. Supports: conditional logic, including other launch files, setting parameters from YAML files, node composition.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is TF2 in ROS and why is it important?',
            'answer': 'TF2 is ROS\'s transform library — tracks and broadcasts coordinate frame relationships over time. Every sensor, link, and body has a frame. TF2 allows querying: "Where is the camera frame relative to the map frame at time t?" Essential for: sensor fusion, path planning, and visualisation in rviz. Transforms broadcast as TF messages on the /tf topic.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is Nav2 and what components does it include?',
            'answer': 'Nav2 (Navigation2): ROS 2 navigation stack for autonomous mobile robot navigation. Components: map server (static/SLAM maps), localisation (AMCL, SLAM Toolbox), costmap (obstacle/inflation layers), global planner (NavFn, Smac Planner), local planner (DWB, RPP), recovery behaviours, behaviour tree executor. Replaces ROS 1 move_base.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 9. Functional Safety (IEC 61508 / ISO 13849)
    # -------------------------------------------------------------------------
    add_cards('Functional Safety (IEC 61508)', [
        {
            'question': 'What is functional safety and what international standard governs it?',
            'answer': 'Functional safety: the part of overall safety that depends on a system (E/E/PE — electrical/electronic/programmable electronic) functioning correctly in response to its inputs. Governed by IEC 61508 (general E/E/PE safety). Sector-specific: IEC 62061 (machinery), ISO 13849 (machinery), IEC 61511 (process), ISO 26262 (automotive).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a Safety Integrity Level (SIL) and what does each level represent?',
            'answer': 'SIL is a measure of risk reduction provided by a Safety Instrumented Function. SIL 1: probability of failure on demand (PFD) 10⁻¹–10⁻², risk reduction 10–100×. SIL 2: PFD 10⁻²–10⁻³. SIL 3: PFD 10⁻³–10⁻⁴. SIL 4: PFD 10⁻⁴–10⁻⁵ (rarely required, extremely demanding). Higher SIL = higher reliability requirement.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': True,
        },
        {
            'question': 'What is a Safety Instrumented Function (SIF) and Safety Instrumented System (SIS)?',
            'answer': 'SIF: a specific safety function implemented by a SIS — e.g. "trip the pump if temperature exceeds 150°C". Consists of: sensor(s) + logic solver (safety PLC) + final element(s) (valve, contactor). SIS: the complete system implementing one or more SIFs. Must be independent of the Basic Process Control System (BPCS).',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is Performance Level (PL) in ISO 13849?',
            'answer': 'PL (Performance Level): machinery safety standard equivalent of SIL. Levels a–e (a=lowest, e=highest reliability). Determined by: Category (hardware architecture), DC (Diagnostic Coverage), MTTFd (Mean Time To dangerous Failure). PL e ≈ SIL 3, PL d ≈ SIL 2, PL c ≈ SIL 1. Used for machinery safety functions (emergency stop, guard interlocking).',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is an Emergency Stop (E-stop) and what category should it be?',
            'answer': 'E-stop: a manually actuated device to stop a machine quickly to prevent or reduce harm. ISO 13850 governs E-stop design. Must be: red/yellow, prominent, latching. Stop category 0 (power removal) or 1 (controlled stop then power removal). Requires assessment to determine required PL/SIL. Typically PLe / SIL 3 for collaborative robots, PLd for most industrial machines.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is LOTO (Lockout/Tagout) and when is it required?',
            'answer': 'LOTO: a safety procedure to ensure hazardous energy (electrical, pneumatic, hydraulic, stored) is isolated before maintenance work. Steps: Notify → Identify energy sources → Isolate → Apply lock and tag → Verify isolation (test) → Perform work → Remove lock and restore. Required whenever workers could contact hazardous energy during maintenance. Governed by AS/NZS 4024 (Australia) and OSHA 29 CFR 1910.147 (USA).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are the IEC 61508 lifecycle phases for safety system development?',
            'answer': 'IEC 61508 safety lifecycle: 1) Concept. 2) Overall scope definition. 3) Hazard and risk analysis. 4) Overall safety requirements. 5) Safety requirements allocation. 6) Operation & maintenance planning. 7) Validation planning. 8–11) E/E/PE system realisation (design, implement, integrate, test). 12) Installation & commissioning. 13) Validation. 14) Operation & maintenance. 15) Decommissioning.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0023_flashcards_networking'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
