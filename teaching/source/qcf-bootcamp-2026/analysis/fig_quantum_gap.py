"""Physical qubits: state of the art vs what breaking secp256k1 needs.

Slide: quantum threat. Benchmarks: Google Willow 105 physical qubits
(Google Quantum AI, Dec 2024); ~2,500 = largest announced superconducting
processors circa 2026; ~500,000 physical qubits is a round mid-range of
published resource estimates for breaking 256-bit ECC within hours
(estimates span ~10^5-10^7 depending on error rates and runtime).
The caption on the slide carries the error-rate caveat.
"""
import matplotlib.pyplot as plt
from common import NAVY, GOLD, RED, HUMAN, style, save

style()

items = ['Google Willow\n(2024)', 'Best hardware\ntoday',
         "Needed to break\nBitcoin's curve"]
vals = [105, 2500, 500000]
cols = [GOLD, NAVY, RED]

fig, ax = plt.subplots(figsize=(10, 4.6))
bars = ax.barh(items, vals, color=cols)
ax.set_xscale('log')
ax.set_xlabel('physical qubits (log scale)')
ax.xaxis.set_major_formatter(HUMAN)
for b, v in zip(bars, vals):
    ax.text(v * 1.15, b.get_y() + b.get_height() / 2, f'{v:,}',
            va='center', fontsize=15, fontweight='bold')
ax.set_xlim(50, 4e6)
ax.set_title('The quantum gap -- about 200x in hardware, plus error rates')
fig.tight_layout()
save(fig, 'fig_quantum_gap.png')
