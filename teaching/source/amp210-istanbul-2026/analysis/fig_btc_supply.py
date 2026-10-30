"""Bitcoin supply schedule, 2009 to 2070 (cap reached ~2140), from the protocol's issuance rule.

Slide: "Issuance Halves Every Four Years Toward a 21 Million Cap".
The rule: block subsidy starts at 50 BTC and halves every 210,000
blocks; blocks target 10 minutes. Past halvings use their actual dates
(block 210,000 on 2012-11-28; 420,000 on 2016-07-09; 630,000 on
2020-05-11; 840,000 on 2024-04-20). After the last actual halving the
schedule assumes exactly 144 blocks per day. No external data.
"""
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from common import NAVY, GOLD, RED, MUTED, style, save

style()

GENESIS = dt.date(2009, 1, 3)
ACTUAL = [dt.date(2012, 11, 28), dt.date(2016, 7, 9),
          dt.date(2020, 5, 11), dt.date(2024, 4, 20)]
TALK = dt.date(2026, 10, 23)
ERA = 210_000

# era boundaries: actual dates, then 210,000 blocks / 144 per day
bounds = [GENESIS] + ACTUAL
while len(bounds) < 34:
    bounds.append(bounds[-1] + dt.timedelta(days=ERA / 144))


def supply(d):
    s = 0.0
    for k in range(len(bounds) - 1):
        a, b = bounds[k], bounds[k + 1]
        reward = int(50e8 / 2 ** k) / 1e8   # satoshi rounding, as in the code
        if d >= b:
            s += reward * ERA
        elif d > a:
            s += reward * ERA * (d - a).days / (b - a).days
            break
    return s


days = [GENESIS + dt.timedelta(days=i)
        for i in range(0, (dt.date(2140, 12, 31) - GENESIS).days, 30)]
s = [supply(d) / 1e6 for d in days]
now = supply(TALK) / 1e6

fig, ax = plt.subplots(figsize=(10.5, 4.6))
ax.plot(days, s, color=NAVY, lw=2.4)
ax.axhline(21, color=MUTED, lw=1, ls='--')
ax.text(dt.date(2032, 1, 1), 21.5,
        '21 million cap (last fraction issued around 2140)',
        color=MUTED, fontsize=13)
for d in ACTUAL:
    ax.axvline(d, color=GOLD, lw=1, alpha=0.8)
ax.text(ACTUAL[-1] + dt.timedelta(days=500), 3,
        'gold lines: past halvings', color=GOLD, fontsize=13)
ax.plot([TALK], [now], 'o', color=RED, ms=8)
ax.annotate(f'October 2026: {now:.1f} M issued ({now / 21:.0%})',
            (TALK, now), xytext=(dt.date(2036, 1, 1), 12),
            color=RED, fontsize=14,
            arrowprops=dict(arrowstyle='->', color=RED))
ax.set_ylim(0, 23)
ax.set_xlim(GENESIS, dt.date(2071, 1, 1))
ax.set_ylabel('bitcoin in existence (millions)')
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{x:g}'))
fig.tight_layout()
save(fig, 'fig_btc_supply.png')
print(f'  supply on {TALK}: {now:.3f} M')
