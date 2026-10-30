"""Shared style and data plumbing for the QCF bootcamp deck figures.

Every figure script imports from here. Figures are written to the deck
folder (the parent of analysis/). Remote data goes through cached_fetch(),
which stores the raw API response in data/ on first use and reads the
snapshot thereafter -- so the package reproduces the shipped charts
offline, and the snapshots ARE the data behind the deck.
"""
import json
import os
import urllib.request

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
DECK = os.path.dirname(HERE)

# Georgia Tech palette
NAVY = '#003057'
GOLD = '#B3A369'
RED = '#8b0000'
BRIGHT_RED = '#c62828'
STEEL = '#5a7a99'
GREEN = '#2e6e46'
GRAY = '#8a8a8a'

# Aug-12 price-chart palette (fig_btc_log / _drawdown / _recent)
BLUE = '#2a78d6'
ORANGE = '#eb6834'
INK = '#1a1a1a'
MUTED = '#555555'
GRID = '#e6e6e6'


def style(font_size=15, parse_math=True):
    plt.rcParams.update({'font.size': font_size,
                         'axes.spines.top': False,
                         'axes.spines.right': False,
                         'text.parse_math': parse_math})


def human(x, pos=None):
    """1500000 -> '1.5 M'. Used on every log axis instead of 10^x ticks."""
    for div, suf in [(1e12, 'T'), (1e9, 'B'), (1e6, 'M'), (1e3, 'K')]:
        if x >= div:
            return f'{x / div:g} {suf}'
    return f'{x:g}' if x >= 1 else ''


HUMAN = FuncFormatter(human)


def cached_fetch(name, url, timeout=60):
    """Return bytes of url, snapshotting to data/<name> on first fetch."""
    path = os.path.join(DATA, name)
    if os.path.exists(path):
        return open(path, 'rb').read()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    raw = urllib.request.urlopen(req, timeout=timeout).read()
    os.makedirs(DATA, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(raw)
    print(f'  fetched + snapshotted {name} ({len(raw):,} bytes)')
    return raw


def blockchain_chart(chart):
    """blockchain.info chart as {unix_ts: value}."""
    raw = cached_fetch(f'{chart}.json',
                       f'https://api.blockchain.info/charts/{chart}'
                       '?timespan=all&format=json')
    return {v['x']: v['y'] for v in json.loads(raw)['values']}


def yahoo_chart(name, symbol, interval, period1=1279317600):
    """Yahoo Finance chart as ([date, ...], [close, ...])."""
    import datetime
    raw = cached_fetch(name,
                       f'https://query1.finance.yahoo.com/v8/finance/chart/'
                       f'{symbol}?period1={period1}&period2=9999999999'
                       f'&interval={interval}')
    r = json.loads(raw)['chart']['result'][0]
    pairs = [(datetime.date.fromtimestamp(t), p)
             for t, p in zip(r['timestamp'],
                             r['indicators']['quote'][0]['close']) if p]
    return [d for d, _ in pairs], [p for _, p in pairs]


def save(fig, filename):
    out = os.path.join(DECK, filename)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f'  wrote {filename}')
