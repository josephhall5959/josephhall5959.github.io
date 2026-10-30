"""Regenerate every original figure in the Istanbul crypto primer.

    python3 make_all.py

Fully offline with data/ populated. Figures are written to the deck
folder (parent directory); recompile main.tex afterward.
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)

for script in ['fig_leading_zeros.py', 'fig_energy.py', 'fig_issuer_balance_sheet.py',
               'fig_btc_supply.py', 'fig_btc_difficulty.py',
               'fig_stablecoin_share.py', 'fig_forum_scatter.py',
               'fig_qr_site.py', 'fig_crypto_prices.py']:
    print(script)
    runpy.run_path(script, run_name='__main__')
