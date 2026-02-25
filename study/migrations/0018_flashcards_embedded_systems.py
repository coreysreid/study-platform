from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return
    course = Course.objects.filter(name='Embedded Systems', created_by=system_user).first()
    if not course:
        return
    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    def add_cards(topic_name, cards):
        topic = topics.get(topic_name)
        if not topic or Flashcard.objects.filter(topic=topic).exists():
            return
        for card in cards:
            Flashcard.objects.create(topic=topic, **card)

    add_cards('Microcontroller Architecture', [
        {'question': 'Harvard vs von Neumann architecture: key difference.',
         'answer': 'Harvard: separate instruction and data memory buses (faster, can fetch both simultaneously). Von Neumann: shared bus for instructions and data (simpler, potential bottleneck).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What registers are in the ARM Cortex-M core?',
         'answer': 'R0-R12 (general purpose), R13=SP (stack pointer), R14=LR (link register, stores return address), R15=PC (program counter), xPSR (status register).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What does the Program Counter (PC) hold?',
         'answer': 'Address of the next instruction to be fetched and executed.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is a clock cycle and CPI?',
         'answer': 'Clock cycle = 1/f_clk seconds. CPI = Cycles Per Instruction (Cortex-M: many instructions take 1 cycle). Execution time = CPI × N_instructions / f_clk.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Typical memory map of ARM Cortex-M microcontroller.',
         'answer': '0x0000_0000: Flash (code). 0x2000_0000: SRAM (data). 0x4000_0000: Peripherals (GPIO, UART, etc). 0xE000_0000: System (NVIC, SysTick).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is CMSIS?',
         'answer': 'Cortex Microcontroller Software Interface Standard. ARM-defined API for NVIC, SysTick, and core functions, portable across Cortex-M devices.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is a pipeline in a CPU?',
         'answer': 'Overlapping of instruction stages (Fetch-Decode-Execute) to increase throughput. Cortex-M3/M4 has 3-stage pipeline. Branch misprediction flushes pipeline.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Describe the reset sequence of a Cortex-M microcontroller.',
         'answer': '1) PC loaded from address 0x0000_0004 (reset vector). 2) SP loaded from 0x0000_0000. 3) Execution starts at reset handler.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is memory-mapped I/O?',
         'answer': 'Peripheral registers are placed in the same address space as memory. Accessing a peripheral register = reading/writing a specific memory address.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('GPIO & Digital I/O', [
        {'question': 'How do you configure a GPIO pin as output in a typical microcontroller?',
         'answer': 'Set the corresponding bit in the Data Direction Register (DDR) or Mode Register (MODER). Then write 0 or 1 to the Output Data Register (ODR).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'How do you read a digital input from a GPIO pin?',
         'answer': 'Configure as input (clear mode bits), optionally enable pull-up/pull-down. Read the Input Data Register (IDR) bit.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is a pull-up resistor and when do you need it?',
         'answer': 'Pulls the pin to VCC when no driver is connected. Needed for open-drain outputs or switch inputs (floating pin → undefined logic level).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Difference between push-pull and open-drain output.',
         'answer': 'Push-pull: drives HIGH (VCC) and LOW (GND) actively. Open-drain: only pulls LOW (transistor to GND); external pull-up drives HIGH. Used for wire-OR and I2C.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'How do you toggle a GPIO pin without affecting others?',
         'answer': 'Use XOR with a mask: ODR ^= (1 << pin_num). Or write to the BSRR (bit set/reset register) on STM32.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is switch debouncing and two common methods?',
         'answer': 'Mechanical switches bounce (rapid on/off) for ~1-20ms. Solutions: 1) Hardware RC filter (+ Schmitt trigger). 2) Software delay (ignore transitions < 20ms after first edge).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'How do you enable a GPIO interrupt on a rising edge (STM32)?',
         'answer': '1) Configure EXTI line for the pin. 2) Set rising trigger in EXTI_RTSR. 3) Enable EXTI line in EXTI_IMR. 4) Enable NVIC for the EXTI IRQ.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is the maximum sink/source current per GPIO pin (typical)?',
         'answer': 'Typically 8-25mA per pin (e.g. STM32: 25mA max). Port total also limited (~100mA). Always use a transistor driver for loads > 20mA (relays, motors).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('Interrupts & Timers', [
        {'question': 'What is an interrupt?',
         'answer': 'A hardware signal that pauses the main program to execute an ISR (Interrupt Service Routine). After ISR completes, main program resumes.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is the NVIC?',
         'answer': 'Nested Vectored Interrupt Controller. ARM Cortex-M hardware that manages interrupt priority, enabling/disabling, and vectoring to the correct ISR.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Why must variables shared between ISR and main be declared volatile?',
         'answer': "volatile tells the compiler not to cache the variable in a register — always read from memory. Without it, the compiler may use a stale cached value in main.",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Timer prescaler formula.',
         'answer': 'Timer frequency = f_clk / (PSC + 1). If f_clk = 72MHz and PSC = 71: timer ticks at 1MHz (1μs/tick).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Auto-reload register (ARR) and timer period.',
         'answer': 'Timer period T = (ARR + 1) × (PSC + 1) / f_clk. Overflow interrupt fires when counter reaches ARR.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Calculate ARR for 1kHz interrupt with f_clk=72MHz and PSC=71.',
         'answer': 'f_timer = 72M/72 = 1MHz. For 1kHz: ARR = f_timer/f_int − 1 = 1000000/1000 − 1 = 999.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Timer clock after prescaler', 'detail': 'f_timer = 72MHz / (71+1) = 1MHz'},
                   {'move': 'ARR for desired interrupt rate', 'detail': 'ARR = 1MHz / 1kHz − 1 = 999'}]},
        {'question': 'What is output compare mode in a timer?',
         'answer': 'Timer compares counter value to CCR (capture/compare register). On match, output pin toggles/sets/clears → used for PWM generation.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is input capture mode in a timer?',
         'answer': 'Timer captures current counter value into CCR when an edge is detected on the input pin. Used to measure pulse width or frequency.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is SysTick and how is it typically used?',
         'answer': 'A 24-bit countdown timer built into Cortex-M core. Generates periodic interrupt — used for OS tick (e.g. 1ms in FreeRTOS) and delay_ms() functions.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('PWM Generation', [
        {'question': 'Define PWM duty cycle.',
         'answer': 'D = t_on / T × 100%. A 25% duty cycle at 5V delivers average 1.25V.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How do you set PWM duty cycle using CCR and ARR?',
         'answer': 'Duty = CCR / (ARR + 1). For 50% at ARR=999: CCR = 500.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Typical PWM frequency for DC motor speed control.',
         'answer': '1-20kHz. Below audible range (>20kHz) preferred. Higher frequency → smoother current but more switching losses.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'How do you control a DC motor with PWM?',
         'answer': 'Use H-bridge (e.g. L298N). Two PWM signals control motor direction and speed: higher duty cycle → higher average voltage → faster speed.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Servo motor control pulse widths.',
         'answer': '1ms pulse = 0°, 1.5ms = 90°, 2ms = 180°. Repeated at 50Hz (20ms period).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is complementary PWM and why is dead time needed?',
         'answer': 'Complementary PWM: two signals that are inverses of each other for H-bridge high/low side. Dead time prevents shoot-through (both switches on simultaneously → short circuit).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'LED brightness control: what average voltage for 30% duty cycle, 3.3V supply?',
         'answer': 'Vavg = 0.30 × 3.3 = 0.99V ≈ 1V. Perceived brightness ≈ 30% (approximately linear for LED).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('ADC & DAC', [
        {'question': 'Resolution of an N-bit ADC.',
         'answer': '2^N levels. LSB = Vref / 2^N. Example: 12-bit ADC with Vref=3.3V: LSB = 3.3/4096 ≈ 0.806mV.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How does a Successive Approximation Register (SAR) ADC work?',
         'answer': 'Binary search: MSB first, compares DAC output to input, sets/clears bits to converge to the closest digital code in N clock cycles.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'ADC conversion time for 12-bit SAR at 14MHz ADC clock.',
         'answer': 'Typically 12 + sampling cycles. At 14MHz with 12 cycles: ~857ns conversion time.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is an ADC trigger source?',
         'answer': 'Signal that starts an ADC conversion: timer output compare, external pin, software trigger. Using timer trigger synchronises ADC with control loops.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is DMA and why use it with ADC?',
         'answer': 'Direct Memory Access: transfers data between ADC and RAM without CPU. Allows continuous ADC sampling without interrupt overhead.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'R-2R ladder DAC: how many resistors for an 8-bit DAC?',
         'answer': '2N resistors: N resistors of value R and N resistors of value 2R. 8-bit: 16 resistors total (8 of R, 8 of 2R).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a sample-and-hold circuit?',
         'answer': 'Captures and holds the input voltage at the sampling instant while the ADC converts. Prevents the input from changing during the (slow) conversion process.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('Serial Communication Protocols', [
        {'question': 'UART frame format.',
         'answer': 'Start bit (LOW) + 8 data bits (LSB first) + optional parity + 1-2 stop bits (HIGH). No clock line — baud rate must match both ends.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'UART baud rate register formula (STM32).',
         'answer': 'BRR = f_PCLK / baud_rate. Example: 72MHz / 9600 = 7500 → BRR = 7500.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'SPI: four signals and their purpose.',
         'answer': 'MOSI: Master Out Slave In. MISO: Master In Slave Out. SCK: Clock (master provides). CS/NSS: Chip Select (active LOW selects slave).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'SPI CPOL and CPHA: what do they define?',
         'answer': 'CPOL: clock polarity at idle (0=low, 1=high). CPHA: data captured on first (0) or second (1) clock edge. 4 modes: 00, 01, 10, 11.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'I2C addressing: how many bits for the slave address?',
         'answer': '7-bit address (standard) + 1 R/W bit = 8-bit first byte. 10-bit addressing also exists. Up to 127 devices on bus.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'I2C ACK/NACK: what do they indicate?',
         'answer': 'ACK (acknowledge, SDA pulled LOW by receiver): byte received OK. NACK (SDA HIGH): error, device not ready, or end of read.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'RS-485: what advantage does differential signalling give?',
         'answer': 'Common-mode noise rejection. Signal = V+ − V−. Noise affects both lines equally, cancels out. Allows long cable runs (>1km) and higher noise immunity than RS-232.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Compare SPI, I2C, UART: speed and number of wires.',
         'answer': 'SPI: 4+ wires, fastest (10s of MHz). I2C: 2 wires, medium (100kHz/400kHz/1MHz). UART: 2 wires (TX/RX), async, no master/slave (peer-to-peer).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is CAN bus and what makes it suitable for automotive/industrial use?',
         'answer': 'Two-wire differential bus (CAN-H, CAN-L), multi-master, collision detection via arbitration (lowest ID wins), error detection and automatic retransmission. Up to 1Mbps.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('Memory & Storage', [
        {'question': 'Flash memory: key constraint.',
         'answer': 'Must erase (set all bits to 1) before programming (writing 0s). Erase granularity is page or sector (typically 2-128KB). Cannot write individual bits to 0→1.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Difference between SRAM and DRAM.',
         'answer': 'SRAM: flip-flops, fast, no refresh needed, expensive, used in MCU. DRAM: capacitors, slower, needs periodic refresh, cheap, used in main PC memory.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What memory sections are in a typical embedded binary?',
         'answer': '.text: code (flash). .rodata: read-only constants (flash). .data: initialised globals (copied to SRAM at startup). .bss: zero-initialised globals (SRAM). .stack: function call stack (SRAM). .heap: dynamic allocation (SRAM).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is EEPROM and when is it used over flash?',
         'answer': 'Electrically Erasable Programmable ROM — can erase and write individual bytes (no sector erase needed). Used for storing configuration that changes frequently (wear level better than flash).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is wear leveling in flash storage?',
         'answer': 'Distributing writes evenly across flash blocks to prevent individual blocks from wearing out (each block: ~10k-100k erase cycles). Done by filesystem (e.g. FAT with FatFS on SD cards).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is a bootloader in embedded systems?',
         'answer': 'Small program in protected flash that runs first on boot. Can update application firmware over UART/USB/CAN (in-field updates) and then jumps to application.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('RTOS Concepts', [
        {'question': 'What is a real-time operating system (RTOS)?',
         'answer': 'An OS where task scheduling guarantees timely response to events. Hard RTOS: missed deadline = system failure. Soft RTOS: occasional missed deadlines tolerable.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'FreeRTOS task states.',
         'answer': 'Running, Ready (can run, waiting for CPU), Blocked (waiting for event/time), Suspended (manually halted).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'FreeRTOS: create a task.',
         'answer': 'xTaskCreate(vTaskFunction, "Name", stack_size, params, priority, &handle); Priority: higher number = higher priority.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'vTaskDelay() vs vTaskDelayUntil(): difference.',
         'answer': 'vTaskDelay(n): delays n ticks from NOW (jitter accumulates). vTaskDelayUntil(&lastWake, n): delays until lastWake+n (fixed-rate execution, no drift).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Binary semaphore vs mutex: difference.',
         'answer': 'Binary semaphore: signalling between tasks or ISR→task (no ownership). Mutex: resource protection with priority inheritance (only owner can release).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is priority inversion and how does mutex handle it?',
         'answer': 'Low-priority task holds mutex needed by high-priority task → high-priority task blocked by low. Mutex with priority inheritance temporarily boosts low-priority task to high priority.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'FreeRTOS message queue: send and receive.',
         'answer': 'xQueueSend(handle, &data, timeout_ticks): sends. xQueueReceive(handle, &data, timeout_ticks): receives. Blocks if queue full/empty.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is a counting semaphore used for in RTOS?',
         'answer': 'Managing a pool of N resources. Count = available resources. xSemaphoreTake() decrements, xSemaphoreGive() increments. Blocks when count = 0.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is a context switch?',
         'answer': 'Saving current task state (registers, PC, SP) to its TCB (Task Control Block) and loading next task\'s state. Takes ~1μs on Cortex-M at 100MHz.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('IoT & Connectivity', [
        {'question': 'What is MQTT?',
         'answer': 'Message Queuing Telemetry Transport. Lightweight pub/sub protocol over TCP/IP. Client subscribes to topics; broker routes messages from publishers to subscribers.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'MQTT QoS levels: 0, 1, 2.',
         'answer': 'QoS 0: at most once (fire and forget, may lose). QoS 1: at least once (acknowledged, may duplicate). QoS 2: exactly once (4-step handshake, guaranteed delivery).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'How do you connect ESP32 to a Wi-Fi access point (Arduino)?',
         'answer': 'WiFi.begin("SSID", "password"); while(WiFi.status() != WL_CONNECTED) delay(500);',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is TLS and why use it for embedded IoT?',
         'answer': 'Transport Layer Security — encrypts MQTT/HTTP traffic. Prevents eavesdropping and tampering. Essential for production IoT (use MQTT over port 8883 for TLS).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is OTA (Over-The-Air) firmware update?',
         'answer': 'Downloading new firmware over network (Wi-Fi/cellular), storing in inactive flash partition, verifying integrity (CRC/hash), then switching to new image on reboot.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is JSON and how is it parsed on embedded (cJSON)?',
         'answer': 'JavaScript Object Notation: text-based data format {key: value}. cJSON library: cJSON_Parse(str) → cJSON tree, cJSON_GetObjectItem(obj, "key") → value.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is BLE advertising?',
         'answer': 'Bluetooth Low Energy device broadcasts periodic advertisement packets (31 bytes) on channels 37/38/39. Scanner receives without pairing. Used for beacons and sensors.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is an MQTT topic naming convention?',
         'answer': 'Hierarchical: home/bedroom/temperature. Wildcard + matches single level: home/+/temperature. # matches all levels: home/#.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
    ])


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0017_flashcards_dsp'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
