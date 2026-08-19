"""Pump.fun token outcomes: 98.6% abandoned or rug-pulled.

Slide: rug pull definition. Statistic from Solidus Labs' analysis of
7M+ tokens launched on Pump.fun 2024-25; "collapse" operationalized as
liquidity below $1,000 (the measure is stated on the chart).
"""
import matplotlib.pyplot as plt
from common import RED, GOLD, save

import matplotlib
matplotlib.use('Agg')
plt.rcParams.update({'font.size': 14})

fig, ax = plt.subplots(figsize=(5.2, 4.8))
ax.pie([98.6, 1.4], colors=[RED, GOLD], startangle=90, counterclock=False,
       wedgeprops=dict(width=0.42))
ax.text(0, 0.10, '98.6%', ha='center', fontsize=30, fontweight='bold',
        color=RED)
ax.text(0, -0.30, 'abandoned or\nrug-pulled', ha='center', fontsize=13)
ax.set_title('Tokens launched on Pump.fun, 2024-25\n'
             '(collapse = liquidity below \\$1,000)', fontsize=13)
fig.tight_layout()
save(fig, 'fig_rugpull_donut.png')
