"""
Common Emitter Amplifier — Schemdraw 0.22
Q-point: VCC=12V, R1=47kΩ, R2=10kΩ, RC=4.7kΩ, RE=1kΩ  →  IC≈1.4mA, VC≈5.5V

Install: pip install schemdraw matplotlib
Run:     python ce_amp_final.py
Outputs: common_emitter.svg  (10 KB, inline into HTML)
    # PNG: pip install cairosvg  →  cairosvg bjt_common_emitter.svg -o bjt_common_emitter.png
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(fontsize=12, show=False) as d:
    d.config(unit=4.0)

    # ── BJT (everything anchors off its three pins) ──────────────────────
    Q = d.add(elm.BjtNpn(circle=True).at((6, 4))
              .label('Q1\n2N3904', loc='right'))

    # ── Collector  →  RC  →  VCC ─────────────────────────────────────────
    d.add(elm.Line().at(Q.collector).up().length(0.4))
    col_node = d.add(elm.Dot())                          # Cout taps here
    rc = d.add(elm.Resistor().up()
               .label('$R_C = 4.7$ kΩ', loc='right'))
    d.add(elm.Line().up().length(0.5))                   # stub: clears label
    d.add(elm.Vdd().label('$V_{CC}$', loc='right'))

    # ── Cout  →  v_out ───────────────────────────────────────────────────
    cout = d.add(elm.Capacitor().at(col_node.center).right()
                 .label('$C_{out} = 10$ µF', loc='top'))
    vout = d.add(elm.Line().right().length(0.7)
                 .label('$v_{out}$', loc='right'))
    d.add(elm.Dot(open=True).at(vout.end))

    # ── Emitter  →  RE  →  GND ───────────────────────────────────────────
    d.add(elm.Line().at(Q.emitter).down().length(0.4))
    emt_node = d.add(elm.Dot())                          # CE taps here
    re = d.add(elm.Resistor().down()
               .label('$R_E = 1$ kΩ', loc='right'))
    d.add(elm.Line().down().length(0.3))                 # stub: clears label
    d.add(elm.Ground())

    # ── CE bypass  (parallel with RE) ────────────────────────────────────
    ce_arm = d.add(elm.Line().at(emt_node.center).left().length(2.5))
    ce = d.add(elm.Capacitor().down()
               .label('$C_E = 100$ µF', loc='right'))
    d.add(elm.Line().down().length(0.3))
    d.add(elm.Ground())

    # ── Bias divider: R1 up to VCC,  R2 down to GND ─────────────────────
    base_arm = d.add(elm.Line().at(Q.base).left().length(2.5))
    bias_pt = base_arm.end
    d.add(elm.Dot().at(bias_pt))

    r2 = d.add(elm.Resistor().at(bias_pt).down()
               .label('$R_2 = 10$ kΩ', loc='right'))
    d.add(elm.Line().down().length(0.3))
    d.add(elm.Ground())

    r1 = d.add(elm.Resistor().at(bias_pt).up()
               .label('$R_1 = 47$ kΩ', loc='right'))
    d.add(elm.Line().up().length(0.5))                   # stub: clears label
    d.add(elm.Vdd().label('$V_{CC}$', loc='right'))

    # ── Cin  →  v_in ─────────────────────────────────────────────────────
    cin = d.add(elm.Capacitor().at(bias_pt).left()
                .label('$C_{in} = 10$ µF', loc='top'))
    vin = d.add(elm.Line().left().length(0.7)
                .label('$v_{in}$', loc='left'))
    d.add(elm.Dot(open=True).at(vin.end))

    d.save('bjt_common_emitter.svg')
    # PNG: pip install cairosvg  →  cairosvg bjt_common_emitter.svg -o bjt_common_emitter.png

    # PNG: pip install cairosvg  →  cairosvg bjt_common_emitter.svg -o bjt_common_emitter.png

# ── Operating point (printed, not drawn) ────────────────────────────────
VCC, R1, R2, RC, RE, VBE, beta = 12, 47e3, 10e3, 4.7e3, 1e3, 0.7, 100
VB  = VCC * R2 / (R1 + R2)
VE  = VB - VBE
IC  = VE / RE          # IC ≈ IE (beta >> 1)
VC  = VCC - IC * RC
VT  = 26e-3            # thermal voltage at 25°C
gm  = IC / VT
r_pi = beta / gm
Av  = -gm * RC
Rin = 1 / (1/R1 + 1/R2 + 1/r_pi)
Rout = RC

print(f"""
Q-point
  VB  = {VB:.2f} V    VE  = {VE:.2f} V    VC  = {VC:.2f} V
  IC  = {IC*1e3:.2f} mA  (good midpoint: VC ≈ VCC/2)

Small-signal (mid-band, CE bypass active)
  gm   = IC/VT        = {gm*1e3:.1f} mA/V
  rπ   = β/gm         = {r_pi:.0f} Ω
  Av   = −gm·RC       = {Av:.0f}  (≈ −{abs(Av):.0f}×)
  Rin  = R1‖R2‖rπ     = {Rin:.0f} Ω
  Rout ≈ RC           = {Rout:.0f} Ω
""")
