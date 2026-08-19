"""Average Bitcoin fee per transaction: total daily fees / daily tx count.

Slide: fees / 2140 transition discussion. Data: blockchain.info charts
API, series transaction-fees-usd and n-transactions (snapshots in data/).
The ratio of the two series avoids the level distortions in the site's
pre-averaged fees-usd-per-transaction series.
"""
import datetime
import matplotlib.pyplot as plt
from common import NAVY, RED, HUMAN, style, save, blockchain_chart

style()

fees = blockchain_chart('transaction-fees-usd')
ntx = blockchain_chart('n-transactions')
common_ts = sorted(set(fees) & set(ntx))
t = [datetime.datetime.fromtimestamp(v) for v in common_ts]
y = [fees[v] / max(ntx[v], 1) for v in common_ts]

fig, ax = plt.subplots(figsize=(10, 4.4))
ax.plot(t, y, color=NAVY, lw=1.0)
ax.set_yscale('log')
ax.set_ylabel('avg fee per tx, USD (log)')
ax.yaxis.set_major_formatter(HUMAN)
ax.axhline(y[-1], color=RED, lw=1.2, ls='--')
ax.text(t[len(t) // 12], y[-1] * 1.25, 'today: ~$%.2f' % y[-1],
        color=RED, fontsize=13)
ax.set_title('Bitcoin transaction fees')
fig.tight_layout()
save(fig, 'fig_btc_fees.png')
print(f'  latest fee: ${y[-1]:.2f}')
