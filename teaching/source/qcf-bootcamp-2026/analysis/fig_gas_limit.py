"""Ethereum gas-per-block steps, with the ~200M roadmap target.

Slide: L1 capacity. Step dates/levels from Etherscan gas-limit history
(30M Aug 2021 -> 36M Feb 2025 -> 45M Jul 2025 -> 60M Feb 2026); the
~200M target is the 2026 protocol roadmap (no fork codename on the
slide by design). Subtitle bridges gas to tps for the audience.
"""
import datetime
import matplotlib.pyplot as plt
from common import NAVY, GOLD, RED, style, save

style()

dates = [datetime.date(2021, 8, 1), datetime.date(2025, 2, 1),
         datetime.date(2025, 7, 1), datetime.date(2026, 2, 1),
         datetime.date(2026, 8, 1)]
lims = [30, 36, 45, 60, 60]

fig, ax = plt.subplots(figsize=(9.6, 4.2))
ax.step(dates, lims, where='post', color=NAVY, lw=2.5)
ax.scatter(dates[:-1], lims[:-1], color=GOLD, zorder=3, s=60)
ax.set_ylabel('gas per block (millions)')
ax.set_ylim(0, 90)
ax.annotate('2026 roadmap target: ~200M', xy=(datetime.date(2026, 8, 1), 60),
            xytext=(datetime.date(2024, 3, 1), 78), fontsize=13, color=RED,
            arrowprops=dict(arrowstyle='->', color=RED))
ax.set_title("Ethereum's capacity dial: gas per block\n(each block is ~12 "
             "seconds; more gas per block = more transactions per second)",
             fontsize=14)
fig.tight_layout()
save(fig, 'fig_gas_limit.png')
