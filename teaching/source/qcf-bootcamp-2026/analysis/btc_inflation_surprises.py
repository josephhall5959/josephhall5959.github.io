#!/usr/bin/env python3
"""BTC monthly returns vs inflation surprises. See README.md.

Reads t5yie.csv / cpi.csv (FRED snapshots in this folder; refresh via
  curl -sL "https://fred.stlouisfed.org/graph/fredgraph.csv?id=T5YIE" -o t5yie.csv
  curl -sL "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL" -o cpi.csv
), fetches BTC-USD monthly from Yahoo (cached to btc_monthly.csv), prints the
correlation table, and writes fig_inflation_hedge.png for the deck.
"""
import urllib.request, json, datetime, math, csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')

def load_fred(fn):
    out = {}
    for row in csv.reader(open(os.path.join(DATA, fn))):
        if row[0] == 'observation_date' or row[1] in ('', '.'):
            continue
        out.setdefault(row[0][:7], []).append(float(row[1]))
    return {k: v[-1] for k, v in out.items()}

def load_btc():
    cache = os.path.join(DATA, 'btc_monthly.csv')
    if os.path.exists(cache):
        return {r[0]: float(r[1]) for r in csv.reader(open(cache))}
    req = urllib.request.Request(
        "https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD"
        "?period1=1279317600&period2=9999999999&interval=1mo",
        headers={'User-Agent': 'Mozilla/5.0'})
    r = json.load(urllib.request.urlopen(req, timeout=60))['chart']['result'][0]
    btc = {}
    for t, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
        if c:
            btc[datetime.datetime.fromtimestamp(t).strftime('%Y-%m')] = c
    with open(cache, 'w') as f:
        for k in sorted(btc):
            f.write(f"{k},{btc[k]}\n")
    return btc

def corr(pairs):
    x, y = zip(*pairs)
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    sx = math.sqrt(sum((a-mx)**2 for a in x))
    sy = math.sqrt(sum((b-my)**2 for b in y))
    return sum((a-mx)*(b-my) for a, b in zip(x, y))/(sx*sy), n

def nextm(m):
    y, mm = int(m[:4]), int(m[5:7]) + 1
    return f"{y+1}-01" if mm == 13 else f"{y}-{mm:02d}"

t5, cpi, btc = load_fred('t5yie.csv'), load_fred('cpi.csv'), load_btc()
months = sorted(btc)
ret = {m2: math.log(btc[m2]/btc[m1]) for m1, m2 in zip(months, months[1:])}
m5 = sorted(t5)
d_be = {m2: t5[m2]-t5[m1] for m1, m2 in zip(m5, m5[1:])}
mc = sorted(cpi)
infl = {m2: 12*math.log(cpi[m2]/cpi[m1]) for m1, m2 in zip(mc, mc[1:])}
mi = sorted(infl)
surp = {mi[i]: infl[mi[i]] - sum(infl[mi[j]] for j in range(i-12, i))/12
        for i in range(12, len(mi))}

def rep(name, pairs):
    c, n = corr(pairs)
    print(f"{name:55s} n={n:3d}  corr={c:+.3f}  (2se~{2/math.sqrt(n):.3f})")

com = sorted(m for m in ret if m in d_be)
rep("BTC ret vs d(5y breakeven), same month, FULL", [(d_be[m], ret[m]) for m in com])
rep("  pre-2020", [(d_be[m], ret[m]) for m in com if m < '2020-01'])
rep("  2020+", [(d_be[m], ret[m]) for m in com if m >= '2020-01'])
com2 = sorted(m for m in ret if m in surp)
rep("BTC ret vs CPI stat-surprise, same month", [(surp[m], ret[m]) for m in com2])
com3 = sorted(m for m in surp if nextm(m) in ret)
rep("BTC ret vs CPI stat-surprise, release month (t+1)", [(surp[m], ret[nextm(m)]) for m in com3])

hi = [m for m in com2 if surp[m] > 0.02]
lo = [m for m in com2 if surp[m] < -0.02]
mhi = sum(ret[m] for m in hi)/len(hi)
mlo = sum(ret[m] for m in lo)/len(lo)
ep = [m for m in sorted(ret) if '2021-11' <= m <= '2022-12']
tot = (math.exp(sum(ret[m] for m in ep)) - 1) * 100
print(f"\nbig + surprise months (n={len(hi)}): mean {mhi*100:+.1f}%/mo")
print(f"big - surprise months (n={len(lo)}): mean {mlo*100:+.1f}%/mo")
print(f"Nov 2021 - Dec 2022 cumulative: {tot:+.0f}%")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
NAVY = '#003057'; GOLD = '#B3A369'; RED = '#8b0000'
plt.rcParams.update({'font.size': 15, 'axes.spines.top': False,
                     'axes.spines.right': False})
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6),
                             gridspec_kw={'width_ratios': [1.4, 1]})
a1.scatter([d_be[m] for m in com], [ret[m]*100 for m in com],
           s=22, color=NAVY, alpha=0.55)
a1.axhline(0, color='#999999', lw=0.8)
a1.set_xlabel('monthly change in 5y breakeven inflation (pp)')
a1.set_ylabel('BTC monthly return (%)')
a1.set_title(f'corr = +0.08 (n = {len(com)}): no relationship')
bars = a2.bar(['big upside\nCPI surprises', 'big downside\nCPI surprises'],
              [mhi*100, mlo*100], color=[RED, NAVY], width=0.55)
for b, v in zip(bars, [mhi*100, mlo*100]):
    a2.text(b.get_x()+b.get_width()/2, v+0.15, f'{v:+.1f}%/mo',
            ha='center', fontweight='bold')
a2.set_title('mean BTC return, by surprise sign')
a2.set_ylim(0, max(mhi, mlo)*100*1.35)
fig.tight_layout()
fig.savefig(os.path.join(HERE, '..', 'fig_inflation_hedge.png'), dpi=150)
print('figure written')
