"""Total stablecoins outstanding over time.

Slide: "What Is a Stablecoin?" evidence. Data: DefiLlama
stablecoincharts/all, peggedUSD circulating (snapshot
data/stablecoincharts.json). ~$306B at retrieval (Aug 2026).
"""
import datetime
import json
import matplotlib.pyplot as plt
from common import NAVY, style, save, cached_fetch

style()

d = json.loads(cached_fetch('stablecoincharts.json',
                            'https://stablecoins.llama.fi/stablecoincharts/all'))
t = [datetime.datetime.fromtimestamp(int(v['date'])) for v in d]
y = [v['totalCirculating']['peggedUSD'] / 1e9 for v in d]

fig, ax = plt.subplots(figsize=(10, 4.4))
ax.fill_between(t, y, color=NAVY, alpha=0.85)
ax.set_ylabel('total stablecoins outstanding, $B')
ax.set_title('A ~$300B bank, assembled in eight years')
fig.tight_layout()
save(fig, 'fig_stablecoin_mcap.png')
print(f'  latest: ${y[-1]:.0f}B')
