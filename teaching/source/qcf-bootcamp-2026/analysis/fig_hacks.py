"""The biggest thefts in crypto history, USD at time of theft.

Slide: "Open Design Invites Predators". Amounts from contemporaneous
reporting: Bybit $1.5B (2025), Ronin $620M (2022), Poly $610M (2021),
Coincheck $530M (2018), FTX $450M (2022), Mt. Gox ~$450M (2014),
Kelp DAO $292M (2026). Uniform navy; the Kelp/Arbitrum point is made
in the slide caption, not by singling out a bar.
"""
import matplotlib.pyplot as plt
from common import NAVY, style, save

style()

hacks = [('Bybit (2025)', 1500), ('Ronin (2022)', 620), ('Poly (2021)', 610),
         ('Coincheck (2018)', 530), ('FTX (2022)', 450),
         ('Mt. Gox (2014)', 450), ('Kelp DAO (2026)', 292)]
hacks = sorted(hacks, key=lambda t: t[1])

names = [h[0] for h in hacks]
v = [h[1] for h in hacks]
fig, ax = plt.subplots(figsize=(10, 4.8))
bars = ax.barh(names, v, color=NAVY)
for b, val in zip(bars, v):
    ax.text(val + 18, b.get_y() + b.get_height() / 2,
            f'${val}M' if val < 1000 else f'${val / 1000:.1f}B',
            va='center', fontsize=14)
ax.set_xlabel('stolen, USD millions (at time of theft)')
ax.set_title('The biggest thefts in crypto history')
ax.set_xlim(0, 1750)
fig.tight_layout()
save(fig, 'fig_hacks.png')
