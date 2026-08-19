"""Tether's balance sheet, to scale, Q2 2026.

Slide: "The Issuer Runs a Bank's Balance Sheet". Figures from Tether's
BDO attestation, Q2 2026: ~$188B total assets, of which ~$147B T-bills
and ~$41B riskier assets (gold, bitcoin, secured loans, other); ~$184B
tokens outstanding; ~$4.1B equity (2.2%).
"""
import matplotlib.pyplot as plt
from common import NAVY, GOLD, BRIGHT_RED, STEEL, style, save

style(parse_math=False)

TOT, SAFE, RISKY, TOKENS, EQ = 188.1, 147.1, 41.0, 184.0, 4.1
f = lambda v: v / TOT

fig, ax = plt.subplots(figsize=(6.6, 6.8))
ax.set_xlim(-0.25, 3.15)
ax.set_ylim(-0.17, 1.22)
ax.axis('off')
w = 0.95
ax.bar(0.55, f(SAFE), w, color=NAVY)
ax.bar(0.55, f(RISKY), w, bottom=f(SAFE), color=GOLD)
ax.bar(1.85, f(TOKENS), w, color=STEEL)
ax.bar(1.85, f(EQ), w, bottom=f(TOKENS), color=BRIGHT_RED)
ax.text(0.55, 1.08, 'ASSETS', ha='center', fontsize=19, fontweight='bold')
ax.text(1.85, 1.08, 'LIABILITIES', ha='center', fontsize=19, fontweight='bold')
ax.text(0.55, f(SAFE) / 2, 'T-bills\n~$147B', ha='center', color='white',
        fontsize=18)
ax.text(0.55, f(SAFE) + f(RISKY) / 2, 'risky stuff\n~$41B', ha='center',
        color='#3a3000', fontsize=15, fontweight='bold')
ax.text(1.85, f(TOKENS) / 2, 'tokens\n~$184B\n(= deposits)', ha='center',
        color='white', fontsize=17)
ycen = f(TOKENS) + f(EQ) / 2
ax.annotate('equity\n$4B\n(2.2%)', xy=(2.33, ycen), xytext=(3.08, ycen - 0.02),
            fontsize=15, color=BRIGHT_RED, fontweight='bold', ha='right',
            va='center',
            arrowprops=dict(arrowstyle='->', color=BRIGHT_RED, lw=1.6))
ax.text(1.20, 0.47, '=', ha='center', fontsize=40, fontweight='bold',
        color='#444444')
ax.text(1.45, -0.14, 'To scale: Tether, Q2 2026.\nRisky assets = 10x the '
        'equity behind them.', ha='center', fontsize=13, style='italic',
        color='#333333')
fig.tight_layout()
save(fig, 'fig_issuer_balance_sheet.png')
