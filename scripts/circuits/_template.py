"""
Circuit Diagram Template — Schemdraw 0.22
==========================================

Copy this file, rename it (e.g. voltage_divider.py), fill in the sections
marked with TODO, then run:

    python scripts/circuits/your_circuit.py

Output: an SVG file ready to inline into a flashcard migration.

Install dependency (development only — not required on Railway):
    pip install schemdraw

To convert SVG → PNG (optional):
    pip install cairosvg
    cairosvg output.svg -o output.png
"""

import schemdraw
import schemdraw.elements as elm

# ── METADATA ────────────────────────────────────────────────────────────────
# TODO: fill these in
CIRCUIT_NAME   = "Circuit Name"          # used in the output filename
COURSE         = "Course Name"           # e.g. "Circuit Analysis Fundamentals"
TOPIC_CODE     = "001A"                  # e.g. "002A"
TOPIC_NAME     = "Topic Name"            # e.g. "Network Theorems"
OUTPUT_FILE    = "output.svg"            # saved next to this script

# ── DRAWING ──────────────────────────────────────────────────────────────────
with schemdraw.Drawing(fontsize=12, show=False) as d:
    d.config(unit=4.0)

    # TODO: draw the circuit here.
    #
    # Key patterns:
    #
    #   Elements chain off previous .end, or use .at() to jump to a new point.
    #
    #   # Place a component
    #   R = d.add(elm.Resistor().right().label('$R = 1$ kΩ'))
    #
    #   # Jump to a known anchor (e.g. BJT pin)
    #   Q = d.add(elm.BjtNpn(circle=True).at((4, 3)))
    #   rc = d.add(elm.Resistor().at(Q.collector).up().label('$R_C$', loc='right'))
    #
    #   # Junction dot (node where ≥3 wires meet)
    #   node = d.add(elm.Dot())          # saves .center for later .at() calls
    #
    #   # Power / ground
    #   d.add(elm.Vdd().label('$V_{CC}$', loc='right'))
    #   d.add(elm.Ground())
    #
    #   # Open terminal (signal port)
    #   d.add(elm.Dot(open=True))
    #
    #   # Label positioning for vertical elements
    #   #   loc='right'  → to the right of the element (standard for vertical R/C/L)
    #   #   loc='top'    → above the element (good for horizontal caps)
    #   #   loc=0.5      → centred along the element
    #
    #   # Always add a short stub (.length(0.3–0.5)) before Ground() or Vdd()
    #   # so the power symbol doesn't crowd the component label.

    d.save(OUTPUT_FILE)

print(f"Saved: {OUTPUT_FILE}")


# ── FLASHCARD INTEGRATION ────────────────────────────────────────────────────
# To embed the SVG in a flashcard migration, read it as a string:
#
#   import pathlib
#   svg = pathlib.Path('scripts/circuits/output.svg').read_text()
#
#   Flashcard.objects.get_or_create(
#       topic=topic,
#       question_type='standard',
#       question=f'<figure class="circuit-diagram">{svg}</figure>'
#                '<p>Question text here.</p>',
#       defaults={
#           'answer': '<p>Answer text with MathJax: $A_v = -g_m R_C$</p>',
#       },
#   )
#
# The SVG is stored as plain text in the DB — no static files, no image serving.
# It scales perfectly at any zoom level in the browser.


# ── OPERATING POINT / VERIFICATION (optional) ────────────────────────────────
# Use this section to verify component values before writing card answers.
# Print results here; hard-code the verified numbers into the flashcard answer.
#
# Example for a BJT bias calculation:
#
#   VCC, R1, R2, RC, RE, VBE, beta = 12, 47e3, 10e3, 4.7e3, 1e3, 0.7, 100
#   VB  = VCC * R2 / (R1 + R2)
#   VE  = VB - VBE
#   IC  = VE / RE
#   VC  = VCC - IC * RC
#   gm  = IC / 26e-3
#   Av  = -gm * RC
#   print(f"IC={IC*1e3:.2f}mA  VC={VC:.2f}V  Av={Av:.0f}")
