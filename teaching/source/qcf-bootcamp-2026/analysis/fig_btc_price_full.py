"""Full Bitcoin price history, weekly closes, log scale.

Slide: Part II price evidence. Data: Yahoo Finance BTC-USD weekly
(snapshot data/btc_weekly.json).
"""
import matplotlib.pyplot as plt
from common import NAVY, HUMAN, style, save, yahoo_chart

style()

ts, px = yahoo_chart('btc_weekly.json', 'BTC-USD', '1wk')

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(ts, px, lw=1.2, color=NAVY)
ax.set_yscale('log')
ax.grid(alpha=0.3)
ax.yaxis.set_major_formatter(HUMAN)
ax.set_title('Bitcoin price (log scale)  --  Yahoo Finance, retrieved Aug 2026')
ax.set_ylabel('USD')
fig.tight_layout()
save(fig, 'fig_btc_price_full.png')
