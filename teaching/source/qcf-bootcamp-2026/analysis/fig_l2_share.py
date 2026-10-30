"""Ethereum L1 vs the three largest rollups: DeFi TVL and daily activity.

Slide: L2 industry state, parallel panels (same categories, order,
colors in both; gray = Ethereum L1). Left panel: value locked in DeFi
apps per chain, DefiLlama chains endpoint (snapshot data/chains.json).
Right panel: operations per day -- rollups from L2BEAT activity API
(snapshot data/l2data.json, 7-day mean at retrieval); Ethereum L1
~1.6M/day approximate from Etherscan. The long tail of smaller rollups
(combined ~90M ops/day) is carried in the slide caption.
"""
import matplotlib.pyplot as plt
from common import NAVY, GRAY, style, save

style(font_size=14)

names = ['Ethereum L1', 'Coinbase\nBase', 'Arbitrum', 'OP Mainnet']
cols = [GRAY, NAVY, NAVY, NAVY]
# From the snapshots (values hardcoded at retrieval, Aug 2026):
tvl = [41.8, 4.8, 1.2, 0.3]      # $B, DefiLlama DeFi TVL by chain
ops = [1.6, 8.1, 1.2, 1.7]       # M ops/day; L1 approximate (Etherscan)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.3))
bars = a1.bar(names, tvl, color=cols, width=0.6)
for b, v in zip(bars, tvl):
    a1.text(b.get_x() + b.get_width() / 2, v + 0.7, f'${v:.1f}B',
            ha='center', fontsize=13, fontweight='bold')
a1.set_ylabel('value locked in DeFi apps, $B')
a1.set_ylim(0, 48)
a1.set_title('where the money sits')
a1.tick_params(axis='x', labelsize=12)

bars = a2.bar(names, ops, color=cols, width=0.6)
for b, v in zip(bars, ops):
    a2.text(b.get_x() + b.get_width() / 2, v + 0.15, f'{v}M',
            ha='center', fontsize=13, fontweight='bold')
a2.set_ylabel('operations per day, millions')
a2.set_ylim(0, 9.5)
a2.set_title('where the activity happens')
a2.tick_params(axis='x', labelsize=12)
fig.tight_layout()
save(fig, 'fig_l2_share.png')
