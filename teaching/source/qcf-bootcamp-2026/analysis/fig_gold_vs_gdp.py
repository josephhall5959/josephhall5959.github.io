"""World real GDP vs the above-ground gold stock, indexed to 1900 = 1.

Slides: History of Fintech "Gold ('M') Cannot Keep Up with GDP ('Y')"
and the bootcamp digital-gold slide. GDP: Maddison Project world real
GDP via OWID grapher (snapshot data/wgdp.csv). Gold: USGS world mine
production benchmarks, linearly interpolated, cumulated onto the World
Gold Council's ~30,000 t above-ground stock through 1900. Sanity check:
cumulation reaches ~213k t by 2024 vs WGC's ~216k t estimate.
Also copies the figure to the History of Fintech deck's Figure/ folder.
"""
import csv
import os
import shutil
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from common import NAVY, GOLD, DATA, DECK, style, save

style()

wgdp = {}
for r in csv.DictReader(open(os.path.join(DATA, 'wgdp.csv'))):
    y = int(r['Year'])
    if y >= 1900:
        wgdp[y] = float(r['GDP'])
gyears = sorted(wgdp)

# USGS world gold mine production anchors (tonnes/yr), interpolated
anchors = [(1900, 386), (1912, 705), (1922, 480), (1940, 1310), (1945, 760),
           (1950, 880), (1960, 1190), (1970, 1480), (1980, 1220),
           (1990, 2180), (2001, 2600), (2008, 2290), (2014, 2860),
           (2020, 3030), (2024, 3300)]
prod = {}
for (y0, v0), (y1, v1) in zip(anchors, anchors[1:]):
    for y in range(y0, y1 + 1):
        prod[y] = v0 + (v1 - v0) * (y - y0) / (y1 - y0)

stock = {}
s = 30000.0   # World Gold Council: ~30k tonnes mined through 1900
for y in range(1900, 2025):
    s += prod.get(y, prod[2024])
    stock[y] = s
print(f'  sanity: stock 2024 = {stock[2024] / 1000:.0f}k tonnes (WGC ~216k)')

g0 = wgdp[gyears[0]]
s0 = stock[1900]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(gyears, [wgdp[y] / g0 for y in gyears], color=NAVY, lw=2.4,
        label='World real GDP ("Y")')
ys = sorted(stock)
ax.plot(ys, [stock[y] / s0 for y in ys], color=GOLD, lw=2.4,
        label='World gold stock ("M")')
ax.set_yscale('log')
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{x:g}x'))
ax.set_ylabel('multiple of 1900 level (log scale)')
ax.legend(frameon=False, loc='upper left', fontsize=14)
gdp_end = wgdp[gyears[-1]] / g0
gold_end = stock[2024] / s0
ax.text(2025.5, gdp_end, f'{gdp_end:.0f}x', color=NAVY, fontsize=15,
        fontweight='bold', va='center')
ax.text(2025.5, gold_end, f'{gold_end:.1f}x', color=GOLD, fontsize=15,
        fontweight='bold', va='center')
ax.set_xlim(1898, 2038)
ax.set_title('The economy outgrew the gold that would have backed its money')
fig.tight_layout()
save(fig, 'fig_gold_vs_gdp.png')

history_fig = os.path.join(DECK, '..', 'decks', 'History of Fintech',
                           'Figure', 'fig_gold_vs_gdp.png')
if os.path.isdir(os.path.dirname(history_fig)):
    shutil.copy(os.path.join(DECK, 'fig_gold_vs_gdp.png'), history_fig)
    print('  copied to History of Fintech deck')
