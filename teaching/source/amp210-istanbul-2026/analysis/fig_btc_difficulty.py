"""Mining difficulty vs BTC price, 2014+, each series autoscaled full-panel.

Slide: Money Pot / difficulty adjacency. The co-movement design: both
series on log axes, each stretched to its own full panel height so the
common shape is visible. Difficulty index 1 = January 2009 (first block).
Data: blockchain.info difficulty series (snapshot data/difficulty.json)
and monthly BTC closes (data/btc_monthly.csv, Yahoo Finance).
"""
import csv
import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from common import NAVY, RED, DATA, human, save, blockchain_chart

import matplotlib
plt.rcParams.update({'font.size': 15, 'axes.spines.top': False})

diff = blockchain_chart('difficulty')
td = [datetime.datetime.fromtimestamp(x) for x in sorted(diff)]
yd = [diff[x] for x in sorted(diff)]

btc = {r[0]: float(r[1])
       for r in csv.reader(open(os.path.join(DATA, 'btc_monthly.csv')))}
mk = sorted(btc)
tp = [datetime.datetime.strptime(m + '-15', '%Y-%m-%d') for m in mk]
pp = [btc[m] for m in mk]

t0 = tp[0]
win = [(t, y) for t, y in zip(td, yd) if t >= t0]
tdw, ydw = zip(*win)

fig, ax = plt.subplots(figsize=(10.5, 4.9))
ax.plot(tdw, ydw, color=NAVY, lw=1.9, label='Mining difficulty (left)')
ax.set_yscale('log')
ax.set_ylabel('difficulty (index)', color=NAVY)
ax.yaxis.set_major_formatter(FuncFormatter(human))
ax.tick_params(axis='y', colors=NAVY)
ax.set_ylim(min(ydw) / 1.3, max(ydw) * 1.3)

ax2 = ax.twinx()
ax2.plot(tp, pp, color=RED, lw=1.6, alpha=0.9, label='BTC price (right)')
ax2.set_yscale('log')
ax2.set_ylim(min(pp) / 1.3, max(pp) * 1.3)
ax2.set_ylabel('BTC price, USD', color=RED)
ax2.yaxis.set_major_formatter(FuncFormatter(human))
ax2.tick_params(axis='y', colors=RED)
ax2.spines['top'].set_visible(False)

lines = [ax.get_lines()[0], ax2.get_lines()[0]]
ax.legend(lines, [l.get_label() for l in lines], frameon=False,
          loc='upper left')
fig.tight_layout()
save(fig, 'fig_btc_difficulty.png')
