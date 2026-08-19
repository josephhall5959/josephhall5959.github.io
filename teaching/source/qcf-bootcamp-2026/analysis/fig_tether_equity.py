"""Tether group equity, Q4 2025 vs Q2 2026.

Slide: stablecoin issuer risk. Figures from Tether's published BDO
attestations: ~$6.3B (Q4 2025) -> ~$4.1B (Q2 2026), a -33% drop in
two quarters.
"""
import matplotlib.pyplot as plt
from common import NAVY, RED, style, save

style()

vals = [6.3, 4.1]
fig, ax = plt.subplots(figsize=(4.6, 4.2))
bars = ax.bar(['Q4 2025', 'Q2 2026'], vals, color=[NAVY, RED], width=0.55)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.12, f'${v}B',
            ha='center', fontsize=16, fontweight='bold')
ax.set_ylim(0, 7.6)
ax.set_ylabel('Tether equity, $B')
ax.set_title('-33% in two quarters')
fig.tight_layout()
save(fig, 'fig_tether_equity.png')
