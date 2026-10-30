"""Regenerate every original figure in the QCF bootcamp deck.

    python3 make_all.py

Runs each fig_*.py plus btc_inflation_surprises.py in this folder.
First run with an empty data/ fetches from public APIs and snapshots
the responses; subsequent runs are fully offline. Figures are written
to the deck folder (parent directory); recompile main.tex afterward.
"""
import runpy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)

SCRIPTS = [
    'fig_btc_price_history.py',   # fig_btc_log, fig_btc_drawdown, fig_btc_recent
    'fig_btc_price_full.py',
    'fig_halving_floors.py',
    'fig_btc_fees.py',
    'fig_btc_difficulty.py',
    'fig_gas_limit.py',
    'fig_hardware_squeeze.py',
    'fig_quantum_gap.py',
    'fig_stablecoin_mcap.py',
    'fig_stablecoin_share.py',
    'fig_tether_equity.py',
    'fig_issuer_balance_sheet.py',
    'fig_tokenized_deposits.py',
    'fig_l2_share.py',
    'fig_hacks.py',
    'fig_rugpull_donut.py',
    'fig_gold_vs_gdp.py',
    'fig_password_redflag.py',
    'fig_qr_site.py',
    'btc_inflation_surprises.py',  # fig_inflation_hedge
]

failed = []
for script in SCRIPTS:
    print(f'== {script}')
    try:
        runpy.run_path(os.path.join(HERE, script), run_name='__main__')
    except Exception as e:
        print(f'  FAILED: {e!r}')
        failed.append(script)

if failed:
    print('\nFAILED:', ', '.join(failed))
    sys.exit(1)
print('\nall figures regenerated')
