"""Cycle peaks vs crash bottoms across Bitcoin's five halving cycles.

Slide: "The Money Pot" section, cycle chart. Peak/trough levels are
round-number cycle statistics from the Yahoo Finance BTC-USD series
(see fig_btc_price_full.py); drawdown percentages computed from them.
Red arrows run trough-to-trough: every crash bottom is higher than the
last (peak-to-trough claims fail for the 2021 and 2025 cycles).
"""
import matplotlib.pyplot as plt
from common import NAVY, GOLD, RED, HUMAN, style, save

style()

cycles = ['2011', '2013', '2017', '2021', '2025-26']
peaks = [31, 1150, 19700, 69000, 126200]
troughs = [2, 185, 3200, 15500, 59000]
dds = ['-93%', '-85%', '-84%', '-77%', '~-53%']

fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(cycles))
ax.bar([i - 0.2 for i in x], peaks, 0.38, color=NAVY, label='Cycle peak')
ax.bar([i + 0.2 for i in x], troughs, 0.38, color=GOLD, label='Crash bottom')
ax.set_yscale('log')
ax.set_xticks(list(x))
ax.set_xticklabels(cycles)
ax.set_ylabel('USD (log scale)')
ax.yaxis.set_major_formatter(HUMAN)
for i, dd in enumerate(dds):
    ax.text(i + 0.2, troughs[i] * 0.42, dd, ha='center', fontsize=13,
            fontweight='bold', color=RED)
for i in range(1, len(cycles)):
    ax.annotate('', xy=(i + 0.2, troughs[i]),
                xytext=(i - 1 + 0.2, troughs[i - 1]),
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.8, alpha=0.75))
ax.legend(frameon=False, loc='upper left')
ax.set_title('Every crash bottom is higher than the last')
ax.set_ylim(0.8, 7e5)
fig.tight_layout()
save(fig, 'fig_halving_floors.png')
