"""Monthly closes for BTC-USD and ETH-USD from Yahoo Finance snapshots
(data/yahoo_<SYM>_monthly_raw.json, chart API, interval=1mo, fetched 2026-10-06;
BTC range=max, ETH range=3y because range=max returns weekly ETH bars).

A Yahoo monthly bar is time-stamped at the first day of the month and closes at
that month's last close, so each value is labeled with its own month. This
replaces the earlier btc_monthly.csv, which labeled every close one month early.
The current (incomplete) month is dropped.
"""
import csv, datetime, json, os
from common import DATA

def monthly(sym):
    r = json.load(open(os.path.join(DATA, f'yahoo_{sym}_monthly_raw.json')))['chart']['result'][0]
    assert r['meta']['dataGranularity'] == '1mo', (sym, r['meta']['dataGranularity'])  # Yahoo silently returns weekly bars for long ranges
    out = {}
    for t, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
        if c:
            out[datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m')] = c
    out.pop(max(out), None)  # drop the month in progress
    return out

if __name__ == '__main__':
    for sym, fn in [('BTC-USD', 'btc_monthly.csv'), ('ETH-USD', 'eth_monthly.csv')]:
        m = monthly(sym)
        with open(os.path.join(DATA, fn), 'w', newline='') as f:
            csv.writer(f).writerows(sorted(m.items()))
        print(fn, min(m), max(m), len(m))
