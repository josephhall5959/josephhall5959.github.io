"""Leading hexadecimal zeros a Bitcoin block hash needs, 2009-2026.

Slide: "Writing the Next Verse Now Takes About 20 Leading Zeros".
At difficulty D the expected number of hash attempts per block is
D * 2^32 (difficulty 1 = 2^32 attempts). Each leading hex zero cuts the
odds by 16, so the required zeros are log16(D * 2^32). Data: blockchain.info
difficulty series (data/difficulty.json). Cross-check: the tip block on
2026-09-29 (mempool.space) began with 19 zeros; the formula gives 19.7 at
difficulty 132.76 T.
"""
import datetime
import math
import matplotlib.pyplot as plt
from common import NAVY, RED, MUTED, style, save, blockchain_chart

style()
d = blockchain_chart('difficulty')
ts = sorted(x for x in d if d[x] > 0)
t = [datetime.datetime.fromtimestamp(x) for x in ts]
z = [math.log(d[x] * 2 ** 32, 16) for x in ts]

fig, ax = plt.subplots(figsize=(10.5, 4.6))
ax.plot(t, z, color=NAVY, lw=2.4)
ax.set_ylabel('leading zeros required\n(hex digits)')
ax.set_ylim(7, 21.5)
ax.axhline(19.7, color=MUTED, lw=1, ls='--')
ax.text(t[0], 20.1, 'difficulty 132.76 T (Sep 29, 2026): 19.7 zeros', color=MUTED,
        fontsize=13)
ax.annotate('each extra zero = 16x more attempts', xy=(t[len(t) // 3], z[len(z) // 3]),
            xytext=(datetime.datetime(2014, 6, 1), 10), color=RED, fontsize=14,
            arrowprops=dict(arrowstyle='->', color=RED))
fig.tight_layout()
save(fig, 'fig_leading_zeros.png')
print(f'  latest: {z[-1]:.2f} zeros at difficulty {d[ts[-1]] / 1e12:.1f} T')
