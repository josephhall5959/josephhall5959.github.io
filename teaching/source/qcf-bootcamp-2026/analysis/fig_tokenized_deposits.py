"""Stablecoin issuer vs bank with tokenized deposits (conceptual).

Slide: stablecoins vs tokenized deposits (Pauline's suggestion). The
economic contrast: stablecoin reserves sit outside the banking system
(parked, not lent); tokenized deposits stay on the bank balance sheet
and keep funding credit.
"""
import matplotlib.pyplot as plt
from common import NAVY, BRIGHT_RED, STEEL, GREEN, style, save

style(parse_math=False)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.8))
for ax, title in [(a1, 'STABLECOIN ISSUER'),
                  (a2, 'BANK WITH TOKENIZED DEPOSITS')]:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.text(5, 9.5, title, ha='center', fontsize=14, fontweight='bold')

a1.bar(2.6, 6.4, 4.0, bottom=1.2, color=NAVY)
a1.text(2.6, 4.4, 'T-bills', ha='center', color='white', fontsize=14)
a1.bar(7.4, 6.4, 4.0, bottom=1.2, color=STEEL)
a1.text(7.4, 4.4, 'tokens', ha='center', color='white', fontsize=14)
a1.text(2.6, 0.4, 'assets', ha='center', fontsize=12)
a1.text(7.4, 0.4, 'liabilities', ha='center', fontsize=12)
a1.text(5, 8.5, 'reserves sit outside the banking\nsystem -- parked, not lent',
        ha='center', fontsize=12, color=BRIGHT_RED, style='italic')

a2.bar(2.6, 4.4, 4.0, bottom=3.2, color=GREEN)
a2.text(2.6, 5.4, 'loans', ha='center', color='white', fontsize=14)
a2.bar(2.6, 2.0, 4.0, bottom=1.2, color=NAVY)
a2.text(2.6, 2.2, 'reserves', ha='center', color='white', fontsize=13)
a2.bar(7.4, 6.4, 4.0, bottom=1.2, color=STEEL)
a2.text(7.4, 4.4, 'tokenized\ndeposits', ha='center', color='white',
        fontsize=14)
a2.text(2.6, 0.4, 'assets', ha='center', fontsize=12)
a2.text(7.4, 0.4, 'liabilities', ha='center', fontsize=12)
a2.text(5, 8.5, 'deposits stay on the balance\nsheet -- still funding credit',
        ha='center', fontsize=12, color=GREEN, style='italic')
fig.tight_layout()
save(fig, 'fig_tokenized_deposits.png')
