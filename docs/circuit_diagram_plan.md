# Circuit Diagram Plan

Maps which topics need Schemdraw-generated SVG diagrams, what circuits are
required, and tracks completion status.

**Workflow**
1. Run `python scripts/circuits/<file>.py` → produces an SVG next to the script.
2. Read the SVG in the flashcard migration using `pathlib.Path(...).read_text()`.
3. Inline it in the `question` field as `<figure class="circuit-diagram">{svg}</figure>`.
4. Mark the row below ✅.

See `scripts/circuits/_template.py` for the drawing template and flashcard
integration pattern.

**Status key**
- ✅ Script written and SVG generated
- 🔲 Planned — not yet written
- — Not needed (formula-only topic)

---

## Circuit Analysis Fundamentals

| Topic | Circuit(s) needed | Script | Status |
|-------|-------------------|--------|--------|
| 001A DC Circuit Analysis | Series resistor divider; parallel resistors; KVL loop example (battery + 3 resistors) | `dc_circuit_basics.py` | 🔲 |
| 001A DC Circuit Analysis | Wheatstone bridge | `wheatstone_bridge.py` | 🔲 |
| 002A Network Theorems | Thevenin equivalent (source + R network → Vth + Rth) | `thevenin_equiv.py` | 🔲 |
| 002A Network Theorems | Norton equivalent | `norton_equiv.py` | 🔲 |
| 003A AC Phasor Analysis | Series RLC circuit | `series_rlc.py` | 🔲 |
| 003A AC Phasor Analysis | Parallel RLC circuit | `parallel_rlc.py` | 🔲 |
| 004A Transient Analysis | RC charging circuit (step input) | `rc_transient.py` | 🔲 |
| 004A Transient Analysis | RL transient circuit | `rl_transient.py` | 🔲 |
| 005A Frequency Response & Resonance | Series RLC resonance (same as `series_rlc.py`) | reuse | — |
| 006A AC Power Analysis | Load impedance circuit with source | `ac_power_circuit.py` | 🔲 |

**Estimated scripts:** ~8 unique diagrams

---

## Analog Electronics

| Topic | Circuit(s) needed | Script | Status |
|-------|-------------------|--------|--------|
| 001A Signals & Amplifiers | Ideal voltage amplifier model (controlled source + Rin + Rout) | `amplifier_model.py` | 🔲 |
| 002A Operational Amplifiers | Inverting amplifier | `opamp_inverting.py` | 🔲 |
| 002A Operational Amplifiers | Non-inverting amplifier | `opamp_noninverting.py` | 🔲 |
| 002A Operational Amplifiers | Summing amplifier (3-input) | `opamp_summing.py` | 🔲 |
| 002A Operational Amplifiers | Integrator | `opamp_integrator.py` | 🔲 |
| 002A Operational Amplifiers | Differentiator | `opamp_differentiator.py` | 🔲 |
| 003A Diodes | Half-wave rectifier | `diode_halfwave.py` | 🔲 |
| 003A Diodes | Full-wave bridge rectifier | `diode_bridge.py` | 🔲 |
| 003A Diodes | Zener voltage regulator | `zener_regulator.py` | 🔲 |
| 003A Diodes | Diode clipper (series + shunt) | `diode_clipper.py` | 🔲 |
| 004A MOSFETs | N-channel MOSFET switch (LED load) | `nmos_switch.py` | 🔲 |
| 004A MOSFETs | NMOS common-source amplifier | `nmos_cs_amp.py` | 🔲 |
| 005A BJTs | Common-emitter amplifier (voltage divider bias) | `bjt_common_emitter.py` | ✅ |
| 005A BJTs | Common-collector (emitter follower) | `bjt_emitter_follower.py` | 🔲 |
| 005A BJTs | Common-base amplifier | `bjt_common_base.py` | 🔲 |
| 006A Transistor Amplifiers | Two-stage CE amplifier (capacitor-coupled) | `bjt_two_stage.py` | 🔲 |
| 007A Frequency Response | Single-pole RC low-pass (for Bode plot discussion) | reuse `rc_transient.py` | — |
| 008A Feedback Amplifiers | Series-shunt feedback topology | `feedback_series_shunt.py` | 🔲 |
| 009A Filters & Tuned Amplifiers | Active low-pass filter (Sallen-Key) | `sallen_key_lpf.py` | 🔲 |
| 009A Filters & Tuned Amplifiers | Active high-pass filter | `sallen_key_hpf.py` | 🔲 |
| 010A Oscillators | RC phase-shift oscillator | `rc_phase_oscillator.py` | 🔲 |
| 010A Oscillators | Colpitts oscillator | `colpitts_oscillator.py` | 🔲 |

**Estimated scripts:** ~20 unique diagrams

---

## Embedded Systems

Primarily software-oriented; a few hardware interface circuits are useful.

| Topic | Circuit(s) needed | Script | Status |
|-------|-------------------|--------|--------|
| 002A GPIO & Digital I/O | LED + current-limiting resistor driven by MCU pin | `gpio_led_driver.py` | 🔲 |
| 002A GPIO & Digital I/O | Pull-up resistor + button (debounce context) | `gpio_button_pullup.py` | 🔲 |
| 004A PWM Generation | H-bridge motor drive (conceptual) | `hbridge_motor.py` | 🔲 |
| 005A ADC & DAC | R-2R ladder DAC | `r2r_dac.py` | 🔲 |
| 006A Serial Communication Protocols | I²C pull-up topology | `i2c_pullup.py` | 🔲 |

**Estimated scripts:** ~5 unique diagrams

---

## Electrical Machines & Motors

| Topic | Circuit(s) needed | Script | Status |
|-------|-------------------|--------|--------|
| 001A Transformer Theory | Transformer equivalent circuit (referred to primary) | `transformer_equiv.py` | 🔲 |
| 002A DC Machines | DC motor equivalent circuit (back-EMF model) | `dc_motor_equiv.py` | 🔲 |
| 003A AC Induction Motors | Induction motor equivalent circuit (per-phase) | `induction_motor_equiv.py` | 🔲 |
| 005A Motor Starting & Protection | DOL starter circuit (contactor + overload relay) | `dol_starter.py` | 🔲 |
| 006A Variable Speed Drives | VSI inverter topology (3-phase H-bridge) | `vsi_inverter.py` | 🔲 |

**Estimated scripts:** ~5 unique diagrams

---

## Power Systems

| Topic | Circuit(s) needed | Script | Status |
|-------|-------------------|--------|--------|
| 002A Per-Unit Analysis | Simple two-bus equivalent circuit | `two_bus_equiv.py` | 🔲 |
| 004A Fault Analysis | Thevenin equivalent at fault point | reuse `thevenin_equiv.py` | — |
| 006A Power Electronics | Boost converter (inductor + switch + diode + cap) | `boost_converter.py` | 🔲 |
| 006A Power Electronics | Buck converter | `buck_converter.py` | 🔲 |
| 006A Power Electronics | Half-wave controlled rectifier (SCR) | `scr_rectifier.py` | 🔲 |

**Estimated scripts:** ~4 unique diagrams

---

## Summary

| Course | Diagrams needed | Done |
|--------|----------------|------|
| Circuit Analysis Fundamentals | ~8 | 0 |
| Analog Electronics | ~20 | 1 |
| Embedded Systems | ~5 | 0 |
| Electrical Machines & Motors | ~5 | 0 |
| Power Systems | ~4 | 0 |
| **Total** | **~42** | **1** |

---

## Suggested Build Order

Work course-by-course in this order, since topics build on each other:

1. **Circuit Analysis Fundamentals** — diagrams are simple (passive components
   only) and reused across all subsequent courses. Build these first.

2. **Analog Electronics** — most diagram-heavy course; start with the op-amp
   circuits (easy in Schemdraw) then BJT, then MOSFET.

3. **Embedded Systems** — only a handful needed; mostly GPIO interface circuits.

4. **Electrical Machines & Motors** — equivalent-circuit style diagrams;
   moderate complexity.

5. **Power Systems** — converter topologies; some complexity with switches/diodes.

---

## Schemdraw Component Cheat Sheet

| Component | Schemdraw element |
|-----------|-------------------|
| Resistor | `elm.Resistor()` |
| Capacitor | `elm.Capacitor()` |
| Inductor | `elm.Inductor2()` |
| Diode | `elm.Diode()` |
| Zener diode | `elm.Zener()` |
| NPN BJT | `elm.BjtNpn(circle=True)` |
| PNP BJT | `elm.BjtPnp(circle=True)` |
| N-channel MOSFET | `elm.NFet(circle=True)` |
| P-channel MOSFET | `elm.PFet(circle=True)` |
| Op-amp | `elm.Opamp()` |
| Transformer | `elm.Transformer()` |
| Battery / DC source | `elm.Battery()` |
| AC voltage source | `elm.SourceSin()` |
| Current source | `elm.SourceI()` |
| Dependent source (VCVS) | `elm.SourceControlledV()` |
| Ground | `elm.Ground()` |
| VCC/VDD | `elm.Vdd()` |
| Junction dot | `elm.Dot()` |
| Open terminal | `elm.Dot(open=True)` |
| Switch (SPST) | `elm.Switch()` |

---

*Last updated: 2026-02-26*
