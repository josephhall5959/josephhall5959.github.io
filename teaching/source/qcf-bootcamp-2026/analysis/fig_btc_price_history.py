"""Three price-evidence charts: full log history, drawdowns, current cycle.

Slides: "First, the Asset Everyone Asks About" (fig_btc_log),
"...and Traders' 'Price Halving' Is a Regular Event" (fig_btc_drawdown),
"The Current Cycle" (fig_btc_recent). Data: Yahoo Finance BTC-USD and
ETH-USD daily closes (snapshots data/btc_daily.json, data/eth_daily.json),
collapsed to monthly (last close per month). Pre-2014 landmarks on the
log chart are documented prices (Mt. Gox $0.06 Jul 2010; $1 parity
Feb 2011; $13 Jan 2013; $1,100 Nov 2013).
These charts keep their original (Aug 12) palette, distinct from the
GT-palette charts made later.
"""
import datetime
import json
import matplotlib.pyplot as plt
from common import BLUE, ORANGE, INK, MUTED, GRID, save, cached_fetch

plt.rcParams.update({'font.size': 12})


def load(name, symbol):
    raw = cached_fetch(name,
                       f'https://query1.finance.yahoo.com/v8/finance/chart/'
                       f'{symbol}?period1=1279317600&period2=9999999999'
                       f'&interval=1d')
    d = json.loads(raw)['chart']['result'][0]
    out = [(datetime.date.fromtimestamp(t), p)
           for t, p in zip(d['timestamp'],
                           d['indicators']['quote'][0]['close']) if p]
    monthly = {}
    for dt, p in out:
        monthly[(dt.year, dt.month)] = (dt, p)
    pairs = [v for _, v in sorted(monthly.items())]
    return [d for d, _ in pairs], [p for _, p in pairs]


bd, bp = load('btc_daily.json', 'BTC-USD')
ed, ep = load('eth_daily.json', 'ETH-USD')


def style_ax(ax):
    ax.set_facecolor('white')
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    for s in ['left', 'bottom']:
        ax.spines[s].set_color(GRID)
    ax.grid(axis='y', color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=MUTED, labelsize=11)


# ---- 1. full history, log scale, pre-2014 landmarks dotted ----
fig, ax = plt.subplots(figsize=(10.5, 5.4), dpi=200)
early_d = [datetime.date(2010, 7, 18), datetime.date(2011, 2, 9),
           datetime.date(2013, 1, 1), datetime.date(2013, 11, 29)]
early_p = [0.06, 1.0, 13.0, 1100.0]
ax.plot(early_d + [bd[0]], early_p + [bp[0]], color=BLUE, lw=2, ls=(0, (2, 3)))
ax.plot(bd, bp, color=BLUE, lw=2)
ax.set_yscale('log')
style_ax(ax)
ax.yaxis.set_major_formatter(
    lambda v, _: f'${v:,.2f}' if v < 1 else f'${v:,.0f}')
for d, p, txt, dy in [(early_d[0], 0.06,
                       'First exchange price: $0.06\n(Mt. Gox, Jul 2010)', 18),
                      (early_d[1], 1.0, '$1 parity (Feb 2011)', 14),
                      (bd[bp.index(max(bp))], max(bp),
                       f'All-time high: ${max(bp):,.0f}', 10),
                      (bd[-1], bp[-1], f'Today: ${bp[-1]:,.0f}', -26)]:
    ax.annotate(txt, (d, p), textcoords='offset points', xytext=(6, dy),
                fontsize=10, color=INK)
ax.set_title('Bitcoin price, 2010–2026 (log scale) — up ~1,000,000× from '
             'its first exchange price', fontsize=13, color=INK, loc='left',
             pad=12)
ax.text(0.0, -0.13, 'Monthly closes, Yahoo Finance (2014–). Dotted: '
        'documented landmark prices pre-2014.', transform=ax.transAxes,
        fontsize=8.5, color=MUTED)
fig.tight_layout()
save(fig, 'fig_btc_log.png')

# ---- 2. drawdown from running peak ----
dd, mx = [], 0
for p in bp:
    mx = max(mx, p)
    dd.append(100 * (p / mx - 1))
fig, ax = plt.subplots(figsize=(10.5, 5.4), dpi=200)
ax.fill_between(bd, dd, 0, color=BLUE, alpha=0.18, lw=0)
ax.plot(bd, dd, color=BLUE, lw=2)
ax.axhline(-50, color=MUTED, lw=1.2, ls=(0, (4, 3)))
ax.text(bd[2], -54.5, 'price cut in half', fontsize=10, color=MUTED)
style_ax(ax)
ax.yaxis.set_major_formatter(lambda v, _: f'{v:.0f}%')
eps, cur = [], None
for dt, v in zip(bd, dd):
    if v <= -50 and cur is None:
        cur = [dt, v, dt]
    elif cur is not None and v <= -50:
        if v < cur[1]:
            cur[1], cur[2] = v, dt
    elif cur is not None and v > -33:
        eps.append(cur)
        cur = None
if cur:
    eps.append(cur)
for d0, v, dmin in eps:
    ax.annotate(f'{dmin.year}: {v:.0f}%', (dmin, v),
                textcoords='offset points', xytext=(-16, -15), fontsize=10,
                color=INK)
ax.annotate(f'today: {dd[-1]:.0f}%', (bd[-1], dd[-1]),
            textcoords='offset points', xytext=(-4, 10), fontsize=10,
            color=INK)
ax.set_ylim(-95, 8)
ax.set_title(f'Drawdown from prior peak — Bitcoin has halved in price '
             f'{len(eps)} times since 2014 (and is close again now)',
             fontsize=12.5, color=INK, loc='left', pad=12)
ax.text(0.0, -0.13, 'Monthly closes, Yahoo Finance. Drawdown = % below prior '
        'all-time-high close. The 2011 (−93%) and 2013–15 episodes predate '
        'the series.', transform=ax.transAxes, fontsize=8.5, color=MUTED)
fig.tight_layout()
save(fig, 'fig_btc_drawdown.png')
print('  episodes:', [(e[2].isoformat(), round(e[1])) for e in eps],
      '| today:', round(dd[-1]))

# ---- 3. BTC vs ETH indexed to 100 at Jan 2024 ----
start = datetime.date(2024, 1, 1)


def index_from(dates, prices):
    base = next(p for d, p in zip(dates, prices) if d >= start)
    return [(d, 100 * p / base) for d, p in zip(dates, prices) if d >= start]


bi, ei = index_from(bd, bp), index_from(ed, ep)
fig, ax = plt.subplots(figsize=(10.5, 5.4), dpi=200)
ax.plot([d for d, _ in bi], [v for _, v in bi], color=BLUE, lw=2)
ax.plot([d for d, _ in ei], [v for _, v in ei], color=ORANGE, lw=2)
ax.axhline(100, color=GRID, lw=1)
style_ax(ax)
ax.annotate(f'Bitcoin  ({100 * (bp[-1] / max(bp) - 1):.0f}% from ATH)',
            (bi[-1][0], bi[-1][1]), textcoords='offset points', xytext=(8, 0),
            fontsize=11, color=BLUE, fontweight='bold')
ax.annotate(f'Ether  ({100 * (ep[-1] / max(ep) - 1):.0f}% from ATH)',
            (ei[-1][0], ei[-1][1]), textcoords='offset points',
            xytext=(8, -6), fontsize=11, color=ORANGE, fontweight='bold')
ax.set_xlim(start, datetime.date(2027, 5, 1))
ax.set_title('The current cycle: major cryptocurrencies, indexed to 100 at '
             'Jan 2024', fontsize=13, color=INK, loc='left', pad=12)
ax.text(0.0, -0.13, 'Monthly closes, Yahoo Finance, through Aug 2026.',
        transform=ax.transAxes, fontsize=8.5, color=MUTED)
fig.tight_layout()
save(fig, 'fig_btc_recent.png')
