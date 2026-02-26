from django.db import migrations


# Map of (course_name, topic_name) → code for all 95 system-owned topics.
# Topics not listed (e.g. "Special Machines") keep code=''.
TOPIC_CODES = {
    'Engineering Mathematics': {
        'Basic Arithmetic & Number Sense':             '001A',
        'Algebra Fundamentals':                        '001B',
        'Geometry':                                    '002A',
        'Trigonometry Fundamentals':                   '002B',
        'Pre-Calculus':                                '003A',
        'Differential Calculus':                       '004A',
        'Integral Calculus':                           '005A',
        'Multivariable Calculus':                      '006A',
        'Linear Algebra':                              '007A',
        'Ordinary Differential Equations (ODEs)':      '008A',
        'Partial Differential Equations (PDEs)':       '009A',
        'Fourier Analysis':                            '010A',
        'Laplace Transforms':                          '010B',
    },
    'Circuit Analysis Fundamentals': {
        'DC Circuit Analysis':                         '001A',
        'Network Theorems':                            '002A',
        'AC Phasor Analysis':                          '003A',
        'Transient Analysis':                          '004A',
        'Frequency Response & Resonance':              '005A',
        'AC Power Analysis':                           '006A',
    },
    'Analog Electronics': {
        'Signals & Amplifiers':                        '001A',
        'Operational Amplifiers':                      '002A',
        'Diodes':                                      '003A',
        'MOSFETs':                                     '004A',
        'Bipolar Junction Transistors (BJTs)':         '005A',
        'Transistor Amplifiers':                       '006A',
        'Frequency Response of Amplifiers':            '007A',
        'Feedback Amplifiers':                         '008A',
        'Filters & Tuned Amplifiers':                  '009A',
        'Oscillators':                                 '010A',
    },
    'Digital Signal Processing': {
        'Sinusoids & Phasors':                         '001A',
        'Spectrum Representation':                     '002A',
        'Sampling & Aliasing':                         '003A',
        'FIR Filters':                                 '004A',
        'Frequency Response of FIR Filters':           '005A',
        'DTFT':                                        '006A',
        'DFT & FFT':                                   '007A',
        'z-Transforms':                                '008A',
        'IIR Filters':                                 '009A',
        'MATLAB for DSP':                              '010A',
    },
    'Embedded Systems': {
        'Microcontroller Architecture':                '001A',
        'GPIO & Digital I/O':                          '002A',
        'Interrupts & Timers':                         '003A',
        'PWM Generation':                              '004A',
        'ADC & DAC':                                   '005A',
        'Serial Communication Protocols':              '006A',
        'Memory & Storage':                            '007A',
        'RTOS Concepts':                               '008A',
        'IoT & Connectivity':                          '009A',
    },
    'Control Systems': {
        'Laplace Transforms & Transfer Functions':     '001A',
        'Block Diagram Algebra':                       '002A',
        'Time-Domain Response':                        '003A',
        'Stability Analysis':                          '004A',
        'Root Locus':                                  '005A',
        'Bode & Nyquist Analysis':                     '006A',
        'PID Controllers':                             '007A',
        'State-Space Representation':                  '008A',
        'MATLAB & Simulink for Control':               '009A',
    },
    'Electrical Machines & Motors': {
        'Transformer Theory':                          '001A',
        'DC Machines':                                 '002A',
        'AC Induction Motors':                         '003A',
        'Synchronous Machines':                        '004A',
        'Motor Starting & Protection':                 '005A',
        'Variable Speed Drives':                       '006A',
    },
    'Power Systems': {
        'Power System Structure':                      '001A',
        'Per-Unit Analysis':                           '002A',
        'Load Flow Analysis':                          '003A',
        'Fault Analysis':                              '004A',
        'Power System Protection':                     '005A',
        'Power Electronics in Power Systems':          '006A',
    },
    'Linux Fundamentals (LFCA)': {
        'Linux Basics & CLI':                          '001A',
        'File System & Permissions':                   '002A',
        'Process Management':                          '003A',
        'Networking in Linux':                         '004A',
        'Shell Scripting':                             '005A',
        'Package Management':                          '006A',
        'System Security':                             '007A',
        'LFCA Exam Preparation':                       '008A',
    },
    'Networking Fundamentals': {
        'OSI Model & TCP/IP':                          '001A',
        'IP Addressing & Subnetting':                  '002A',
        'Routing Protocols':                           '003A',
        'Switching & VLANs':                           '004A',
        'Wireless Networking':                         '005A',
        'Network Security':                            '006A',
        'Network Troubleshooting':                     '007A',
        'Industrial Networking':                       '008A',
    },
    'Industrial Automation & Robotics': {
        'PLC Fundamentals':                            '001A',
        'Ladder Logic':                                '002A',
        'Structured Text (IEC 61131-3)':               '003A',
        'SCADA & HMI':                                 '004A',
        'Industrial Protocols':                        '005A',
        'Motion Control':                              '006A',
        'Robot Kinematics':                            '007A',
        'ROS Basics':                                  '008A',
        'Functional Safety (IEC 61508)':               '009A',
    },
}


def set_topic_codes(apps, schema_editor):
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    User = apps.get_model('auth', 'User')

    try:
        system_user = User.objects.get(username='system')
    except User.DoesNotExist:
        return  # No system user means no system courses; nothing to do.

    for course_name, topic_map in TOPIC_CODES.items():
        try:
            course = Course.objects.get(name=course_name, created_by=system_user)
        except Course.DoesNotExist:
            continue  # Course missing; skip silently (idempotent).

        for topic_name, code in topic_map.items():
            Topic.objects.filter(
                course=course,
                name=topic_name,
                code='',  # Only write if not already set (idempotent).
            ).update(code=code)


def reverse_fn(apps, schema_editor):
    pass  # Intentional no-op.


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0026_topic_code'),
    ]

    operations = [
        migrations.RunPython(set_topic_codes, reverse_fn),
    ]
