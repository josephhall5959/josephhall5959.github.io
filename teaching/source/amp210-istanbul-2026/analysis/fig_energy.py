"""Annual electricity use: Bitcoin, Ethereum before and after the Merge,
and data centers, in TWh.

Slide: appendix "Bitcoin and AI Both Draw Heavily on the World's Energy".
Sources: Bitcoin 138 TWh (Cambridge Digital Mining Industry Report, 2025).
Data centers 415 TWh in 2024, ~945 TWh projected for 2030 (IEA, Energy and
AI, 2025). Shares of world electricity (30,856 TWh, Ember 2024) and world
energy (164,400 TWh, Energy Institute 2025) are computed in
data/energy_denominators.md: Bitcoin 0.4% and 0.08%, data centers 1% and 0.3%. Ethereum
~21 TWh/yr before the Merge and 0.0026 TWh/yr after (ethereum.org,
citing CCRI).
"""
import matplotlib.pyplot as plt
from common import NAVY, GOLD, STEEL, RED, style, save

style()
rows = [('Ethereum after the Merge (2022)', 0.0026, GOLD),
        ('Ethereum before the Merge', 21, GOLD),
        ('Bitcoin mining', 138, NAVY),
        ('Data centers, 2024', 415, STEEL),
        ('Data centers, 2030 (IEA projection)', 945, STEEL)]
fig, ax = plt.subplots(figsize=(10.5, 4.6))
names = [r[0] for r in rows]
vals = [r[1] for r in rows]
bars = ax.barh(names, vals, color=[r[2] for r in rows])
for b, v in zip(bars, vals):
    lab = f'{v:g} TWh' if v >= 1 else '0.0026 TWh (-99.99%)'
    ax.text(v + 12, b.get_y() + b.get_height() / 2, lab, va='center', fontsize=14)
ax.set_xlim(0, 1150)
ax.set_xlabel('electricity per year, TWh')
fig.tight_layout()
save(fig, 'fig_energy.png')
