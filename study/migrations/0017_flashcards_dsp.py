from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return
    course = Course.objects.filter(name='Digital Signal Processing', created_by=system_user).first()
    if not course:
        return
    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    def add_cards(topic_name, cards):
        topic = topics.get(topic_name)
        if not topic or Flashcard.objects.filter(topic=topic).exists():
            return
        for card in cards:
            Flashcard.objects.create(topic=topic, **card)

    add_cards('Sinusoids & Phasors', [
        {'question': 'General form of a real sinusoid.',
         'answer': 'x(t) = A cos(2πf₀t + φ) = A cos(ω₀t + φ). A = amplitude, f₀ = frequency (Hz), ω₀ = 2πf₀ (rad/s), φ = phase.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'State Euler\'s formula.',
         'answer': 'e^(jθ) = cos θ + j sin θ. Therefore cos θ = Re{e^(jθ)} = (e^(jθ) + e^(−jθ))/2.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Express a sinusoid A cos(ω₀t + φ) as a complex exponential (rotating phasor).',
         'answer': 'A cos(ω₀t + φ) = Re{A e^(jφ) e^(jω₀t)}. Phasor X = A e^(jφ) = A∠φ captures amplitude and phase.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How do you add two sinusoids of the same frequency: A cos(ω₀t) + B cos(ω₀t + φ)?',
         'answer': 'Add as phasors: X₁ = A∠0°, X₂ = B∠φ. Sum X = X₁ + X₂ in rectangular form, then convert back to A_total∠θ.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the beating phenomenon?',
         'answer': 'Adding two sinusoids of slightly different frequencies f₁ and f₂: result oscillates at average frequency (f₁+f₂)/2 with amplitude modulated at beat frequency |f₁−f₂|.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is an analytic signal?',
         'answer': 'z(t) = x(t) + jx̂(t), where x̂(t) is the Hilbert transform of x(t). Equivalently z(t) = A(t)e^(jψ(t)) (instantaneous amplitude and phase).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'For x(t) = 3cos(2π·100t − π/4), identify amplitude, frequency, and phase.',
         'answer': 'A = 3, f₀ = 100 Hz, φ = −π/4 = −45°.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Period of x(t) = cos(2π × 50t).',
         'answer': 'T = 1/f₀ = 1/50 = 20 ms.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is amplitude modulation (AM)?',
         'answer': 'x_AM(t) = [1 + m·m(t)]·cos(2πfct). Message m(t) modulates amplitude of carrier cos(2πfct). Spectrum: carrier ± message sidebands.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'MATLAB: how do you generate x(t) = cos(2π×1000×t) sampled at fs=8000 Hz for 0.01s?',
         'answer': 'fs=8000; t=0:1/fs:0.01-1/fs; x=cos(2*pi*1000*t);',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('Spectrum Representation', [
        {'question': 'Two-sided spectrum of x(t) = A cos(ω₀t + φ).',
         'answer': 'x(t) = (A/2)e^(jφ)e^(jω₀t) + (A/2)e^(−jφ)e^(−jω₀t). Spectral lines at ±f₀, each with magnitude A/2.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What does the amplitude spectrum show?',
         'answer': '|X(f)| vs f: magnitude of each frequency component. The phase spectrum shows ∠X(f) vs f.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Spectrum of sum: x(t) = 3cos(2πt) + cos(6πt).',
         'answer': 'Lines at ±1Hz (magnitude 3/2) and ±3Hz (magnitude 1/2).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Spectrum of an AM signal x(t) = [1 + 0.5cos(2π·1000t)]·cos(2π·10000t).',
         'answer': 'Carrier at ±10kHz (magnitude 1/2) + sidebands at ±9kHz and ±11kHz (magnitude 0.25 each).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Define bandwidth of a signal.',
         'answer': 'The range of positive frequencies that contain significant energy. For a signal with components from f₁ to f₂: BW = f₂ − f₁.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is a line spectrum vs a continuous spectrum?',
         'answer': 'Line (discrete): periodic signals have components at discrete harmonics. Continuous: aperiodic signals have continuous spectral density.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Spectrum of periodic square wave with fundamental f₀.',
         'answer': 'Harmonics at f₀, 3f₀, 5f₀, ... (odd harmonics only). Amplitudes decrease as 1/n.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('Sampling & Aliasing', [
        {'question': 'State the Nyquist sampling theorem.',
         'answer': 'A signal with highest frequency fmax can be exactly reconstructed if sampling frequency fs ≥ 2fmax. The Nyquist rate is 2fmax.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is aliasing?',
         'answer': 'When fs < 2fmax, high-frequency components appear as lower frequencies (aliases) in the sampled signal. The alias frequency is |f − k·fs| for integer k.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'A 1200 Hz sinusoid is sampled at fs = 1000 Hz. What alias frequency appears?',
         'answer': 'f_alias = |1200 − 1000| = 200 Hz.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the purpose of an anti-aliasing filter?',
         'answer': 'A lowpass filter with cutoff at fs/2 applied before sampling. Removes frequency components above fs/2 that would alias.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'ADC pipeline: list the stages in order.',
         'answer': 'Anti-aliasing filter → Sample & Hold → Quantiser (ADC) → Digital output.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'SNR formula for an ideal N-bit ADC.',
         'answer': 'SNR ≈ 6.02N + 1.76 dB. Each additional bit adds ~6 dB SNR.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is oversampling and what advantage does it provide?',
         'answer': 'Sampling at fs >> 2fmax. Spreads quantisation noise over wider bandwidth; after lowpass filtering, effective SNR increases.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Ideal reconstruction: how is a sampled signal reconstructed to continuous-time?',
         'answer': 'Convolution with sinc function: x(t) = Σ x[n] sinc(fs(t − n/fs)). In practice: lowpass filter (ideal LPF at fs/2) applied to impulse train.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('FIR Filters', [
        {'question': 'Define discrete-time convolution (FIR filter operation).',
         'answer': 'y[n] = Σₖ h[k]·x[n−k] where h[k] is the impulse response (filter coefficients).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the impulse response h[n] of an FIR filter?',
         'answer': 'The output when input is the unit impulse δ[n]. FIR has h[n] = 0 for n < 0 and n > M (finite length M+1).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Difference equation of a 3-tap FIR filter.',
         'answer': 'y[n] = h[0]x[n] + h[1]x[n−1] + h[2]x[n−2]. Only current and past inputs (no feedback).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Moving average filter: h[n] for M-point average.',
         'answer': 'h[n] = 1/M for n = 0, 1, ..., M−1; zero otherwise. Smooths the signal; attenuates high frequencies.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Linear phase property of FIR filters.',
         'answer': 'Symmetric impulse response h[n] = h[M−n] gives linear phase: φ(ω) = −Mω/2. All frequencies delayed by same time M/2 samples.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Compute y[0], y[1], y[2] for x[n] = {1,2,3} and h[n] = {1,−1}.',
         'answer': 'y[0]=1×1=1; y[1]=2×1+1×(−1)=1; y[2]=3×1+2×(−1)=1; y[3]=3×(−1)=−3.',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'y[0] = h[0]x[0]', 'detail': '1×1 = 1'},
                   {'move': 'y[1] = h[0]x[1] + h[1]x[0]', 'detail': '1×2 + (−1)×1 = 1'},
                   {'move': 'y[2] = h[0]x[2] + h[1]x[1]', 'detail': '1×3 + (−1)×2 = 1'},
                   {'move': 'y[3] = h[1]x[2]', 'detail': '(−1)×3 = −3'}]},
        {'question': 'FIR filter length vs transition bandwidth: how are they related?',
         'answer': 'Narrower transition band requires longer filter (more taps). Rule of thumb: N ≈ (stopband_attenuation in dB) × fs / (22 × Δf).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'MATLAB: apply a 5-tap FIR filter h to signal x.',
         'answer': 'y = filter(h, 1, x); or y = conv(h, x) (conv gives full length). filter() preserves length.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('Frequency Response of FIR Filters', [
        {'question': 'Define the frequency response H(e^jω) of a discrete-time filter.',
         'answer': 'H(e^jω) = Σₙ h[n]e^(−jωn). Complex function of ω (rad/sample). ω = 0 to π covers DC to Nyquist.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How is digital frequency ω (rad/sample) related to analog frequency f (Hz)?',
         'answer': 'ω = 2πf/fs. Nyquist: f = fs/2 → ω = π. DC: f=0 → ω=0.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Magnitude response of 2-point average filter h[n] = {0.5, 0.5}.',
         'answer': 'H(e^jω) = 0.5 + 0.5e^(−jω) = e^(−jω/2) cos(ω/2). |H| = |cos(ω/2)|. LP filter: |H(0)|=1, |H(π)|=0.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What does an ideal lowpass filter have as its frequency response?',
         'answer': 'H(e^jω) = 1 for |ω| < ωc and 0 otherwise. Has infinite impulse response h[n] = (ωc/π)sinc(ωcn/π).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'How does cascading two filters affect their frequency responses?',
         'answer': 'H_total(e^jω) = H₁(e^jω) × H₂(e^jω). Convolution in time → multiplication in frequency.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'MATLAB: compute and plot frequency response of h = [1 2 1]/4.',
         'answer': '[H,w] = freqz(h, 1, 512); plot(w/pi, abs(H)); xlabel("Normalised freq"); ylabel("|H|");',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('DTFT', [
        {'question': 'Define the Discrete-Time Fourier Transform (DTFT).',
         'answer': 'X(e^jω) = Σₙ₌₋∞^∞ x[n]e^(−jωn). Continuous in ω, periodic with period 2π.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'DTFT inverse formula.',
         'answer': 'x[n] = (1/2π) ∫₋π^π X(e^jω) e^(jωn) dω.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'DTFT time-shift property.',
         'answer': 'DTFT{x[n−n₀]} = e^(−jωn₀) X(e^jω). Shift by n₀ → multiply by linear phase e^(−jωn₀).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'DTFT convolution theorem.',
         'answer': 'DTFT{x[n]*h[n]} = X(e^jω)·H(e^jω). Convolution in time ↔ multiplication in frequency.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'DTFT of unit impulse δ[n].',
         'answer': 'X(e^jω) = 1 (all frequencies, flat spectrum).',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'DTFT of unit step u[n].',
         'answer': 'X(e^jω) = 1/(1−e^(−jω)) + π·δ(ω). (More complex due to non-absolutely-summable sequence)',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Parseval\'s theorem for DTFT.',
         'answer': 'Σₙ |x[n]|² = (1/2π) ∫₋π^π |X(e^jω)|² dω. Total energy in time = total energy in frequency.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'DTFT of x[n] = aⁿu[n], |a| < 1.',
         'answer': 'X(e^jω) = 1/(1 − ae^(−jω)). Geometric series sum.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('DFT & FFT', [
        {'question': 'Define the N-point DFT.',
         'answer': 'X[k] = Σₙ₌₀^(N−1) x[n] e^(−j2πkn/N), for k = 0, 1, ..., N−1.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'DFT inverse formula.',
         'answer': 'x[n] = (1/N) Σₖ₌₀^(N−1) X[k] e^(j2πkn/N).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is the frequency resolution of an N-point DFT with sample rate fs?',
         'answer': 'Δf = fs/N Hz. Longer records (larger N) give finer frequency resolution.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is zero-padding in DFT?',
         'answer': 'Appending zeros to x[n] before taking DFT. Increases N → interpolates spectrum (smoother plot) but does NOT improve resolution — actual resolution depends on record length.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is spectral leakage?',
         'answer': 'Occurs when a non-integer number of cycles fits in the DFT window. Energy from a sinusoid leaks into neighbouring frequency bins. Windowing reduces leakage.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Hann window: what trade-off does it offer vs rectangular window?',
         'answer': 'Hann: lower sidelobe level (better leakage rejection), but wider main lobe (reduced frequency resolution). Rectangular: best resolution but high leakage.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'Computational complexity: DFT vs FFT.',
         'answer': 'DFT: O(N²). Cooley-Tukey FFT: O(N log₂ N). For N=1024: DFT ~10⁶, FFT ~10⁴ operations.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'MATLAB: compute and plot one-sided magnitude spectrum of x at fs=1000Hz.',
         'answer': 'N=length(x); X=fft(x); f=(0:N/2)*fs/N; plot(f, abs(X(1:N/2+1))/N*2);',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'X[0] in the DFT equals what?',
         'answer': 'X[0] = Σ x[n] = N × (mean of x). Represents the DC component.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
    ])

    add_cards('z-Transforms', [
        {'question': 'Define the z-transform.',
         'answer': 'X(z) = Σₙ₌₋∞^∞ x[n] z^(−n). z is a complex variable.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'z-transform of unit impulse δ[n].',
         'answer': 'Z{δ[n]} = 1.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'z-transform of unit step u[n].',
         'answer': 'Z{u[n]} = z/(z−1) = 1/(1−z⁻¹), ROC: |z| > 1.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'z-transform of aⁿu[n].',
         'answer': 'Z{aⁿu[n]} = z/(z−a) = 1/(1−az⁻¹), ROC: |z| > |a|.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'z-transform time-delay property.',
         'answer': 'Z{x[n−k]} = z^(−k) X(z). Delay by k samples → multiply by z^(−k).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Relation between z-transform and DTFT.',
         'answer': 'Evaluate X(z) on the unit circle: z = e^(jω). X(e^jω) = X(z)|z=e^(jω).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'IIR stability condition using z-transform poles.',
         'answer': 'Causal LTI system is stable if and only if all poles of H(z) lie inside the unit circle (|poles| < 1).',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Inverse z-transform via partial fractions: find x[n] for X(z) = z/(z−0.5).',
         'answer': 'X(z)/z = 1/(z−0.5). X(z) = z/(z−0.5). Recognise: Z{0.5ⁿu[n]} = z/(z−0.5). So x[n] = 0.5ⁿu[n].',
         'difficulty': 'medium', 'question_type': 'step_by_step', 'uses_latex': True,
         'steps': [{'move': 'Form X(z)/z', 'detail': 'X(z)/z = 1/(z−0.5)'},
                   {'move': 'Match to z-transform table', 'detail': 'Z{aⁿu[n]} = z/(z−a) → here a = 0.5'},
                   {'move': 'Inverse transform', 'detail': 'x[n] = (0.5)ⁿ u[n]'}]},
        {'question': 'What does the region of convergence (ROC) determine for a z-transform?',
         'answer': 'ROC determines whether the system is causal, anti-causal, or two-sided, and whether it is stable. The DTFT exists only if ROC includes the unit circle.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('IIR Filters', [
        {'question': 'General IIR filter difference equation.',
         'answer': 'y[n] = Σₖ bₖx[n−k] − Σₖ aₖy[n−k]. Has feedback (past output) terms → infinite impulse response.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'System function H(z) of an IIR filter.',
         'answer': 'H(z) = B(z)/A(z) = (Σbₖz^(−k))/(1 + Σaₖz^(−k)). Poles determine stability.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'IIR vs FIR: four key differences.',
         'answer': '1) IIR: fewer coefficients for same sharpness. 2) IIR: can be unstable (poles outside unit circle). 3) FIR: guaranteed linear phase. 4) IIR: analogous to analog filter design.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What is the bilinear transform?',
         'answer': 's = (2/T)(z−1)/(z+1). Maps the s-plane to z-plane: LHP→inside unit circle, jω→unit circle. Avoids aliasing (unlike impulse invariant method).',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'What is frequency prewarping in bilinear transform design?',
         'answer': 'Critical frequencies must be prewarped: ωa = (2/T)tan(ωd·T/2). Ensures the filter cutoff is at the desired digital frequency after the nonlinear s→z mapping.',
         'difficulty': 'hard', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'First-order IIR lowpass filter: H(z) = (1−a)/(1−az^(−1)), 0 < a < 1.',
         'answer': 'As a→1: narrower bandwidth (more averaging). Pole at z=a. Time constant τ ≈ −1/(fs·ln a) samples.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'Stability condition for IIR filter.',
         'answer': 'All poles of H(z) must lie strictly inside the unit circle: |pₖ| < 1 for all poles pₖ.',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': True},
        {'question': 'MATLAB: design a 4th-order Butterworth lowpass IIR at fc = 0.2 (normalised).',
         'answer': '[b,a] = butter(4, 0.2); y = filter(b, a, x); freqz(b,a); % plots response',
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
    ])

    add_cards('MATLAB for DSP', [
        {'question': 'How do you create a time vector from 0 to 1s at fs=8000Hz in MATLAB?',
         'answer': "fs = 8000; t = 0:1/fs:1-1/fs;  % 8000 samples",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'MATLAB: generate and play a 440Hz sine wave for 1 second.',
         'answer': "fs=44100; t=0:1/fs:1-1/fs; x=sin(2*pi*440*t); sound(x, fs);",
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What does abs(fft(x)) give you?',
         'answer': 'The magnitude spectrum (not normalised). Divide by N for correct amplitude. Use fftshift() to centre at DC.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'MATLAB: plot the one-sided power spectrum.',
         'answer': "N=length(x); X=fft(x,N); P=abs(X(1:N/2+1)).^2/N; f=(0:N/2)*fs/N; plot(f,P);",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'MATLAB: apply zero-phase filtering to avoid phase distortion.',
         'answer': "y = filtfilt(b, a, x);  % zero-phase IIR filtering (forward + backward pass)",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'MATLAB: plot spectrogram of signal x.',
         'answer': "spectrogram(x, hamming(256), 128, 256, fs, 'yaxis');",
         'difficulty': 'medium', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'MATLAB element-wise vs matrix multiplication: .* vs *.',
         'answer': '.* multiplies element-by-element; * is matrix multiplication. For signals, always use .* and .^.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
        {'question': 'What does length() vs size() return in MATLAB?',
         'answer': 'length(x): max dimension (for vector = N). size(x): returns [rows, cols]. numel(x): total elements.',
         'difficulty': 'easy', 'question_type': 'standard', 'uses_latex': False},
    ])


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0016_flashcards_analog_electronics'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
