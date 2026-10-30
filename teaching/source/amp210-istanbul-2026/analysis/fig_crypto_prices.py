"""Bitcoin and ether monthly closes, January 2024 to September 2026.

Slide: "Bitcoin Fell by Half and Ether by About 60% from 2025 to June 2026"
(section "Why hasn't crypto taken over?"). Data: Yahoo Finance monthly closes
(data/btc_monthly.csv, data/eth_monthly.csv, built by prices_from_yahoo.py).
Each panel marks the 2025 high and the 2026 low of the monthly close.
"""
import csv, datetime, os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from common import NAVY, GOLD, RED, DATA, style, save

style()
fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))
for ax, (fn, name, color) in zip(axes, [('btc_monthly.csv', 'Bitcoin', NAVY), ('eth_monthly.csv', 'Ether', GOLD)]):
    d = {k: float(v) for k, v in csv.reader(open(os.path.join(DATA, fn))) if k >= '2024-01'}
    ks = sorted(d)
    t = [datetime.datetime.strptime(k + '-28', '%Y-%m-%d') for k in ks]
    ax.plot(t, [d[k] for k in ks], color=color, lw=3)
    hi = max((k for k in ks if k.startswith('2025')), key=d.get)
    lo = min((k for k in ks if k.startswith('2026')), key=d.get)
    for k, va, off in [(hi, 'bottom', 1.04), (lo, 'top', 0.93)]:
        x = datetime.datetime.strptime(k + '-28', '%Y-%m-%d')
        ax.plot([x], [d[k]], 'o', color=RED, ms=8)
        ax.annotate(f"{datetime.datetime.strptime(k, '%Y-%m').strftime('%b %Y')}: ${d[k]:,.0f}",
                    (x, d[k] * off), ha='center', va=va, fontsize=13, color=RED)
    ax.set_title(f'{name}: {1 - d[lo] / d[hi]:.0%} below its 2025 high', fontsize=16)
    ax.set_ylim(0, max(d.values()) * 1.2)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f'${v/1000:.0f}K'))
    ax.spines[['top', 'right']].set_visible(False)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
fig.tight_layout()
save(fig, 'fig_crypto_prices.png')
