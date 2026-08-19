"""Fabricated 'off by one character' login screen for the hash pop quiz.

Slide: "Pop Quiz: Why Is This a Red Flag?". Entirely fictional mock
(totally-secure-bank.com); the pedagogical point is that a server that
knows your guess was close is storing passwords in plain text.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from common import save

import matplotlib
matplotlib.use('Agg')

fig, ax = plt.subplots(figsize=(7.2, 4.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.add_patch(FancyBboxPatch((0.4, 0.5), 9.2, 9.0, boxstyle='round,pad=0.1',
                            fc='white', ec='#c8c8c8', lw=1.5))
ax.add_patch(FancyBboxPatch((0.4, 8.5), 9.2, 1.0, boxstyle='round,pad=0.1',
                            fc='#003057', ec='none'))
ax.text(0.9, 8.95, '● ● ●', color='#B3A369', fontsize=11, va='center')
ax.text(5.0, 8.95, 'https://totally-secure-bank.com/login', color='white',
        fontsize=11, ha='center', va='center', family='monospace')
ax.text(5.0, 7.6, 'Sign in to Online Banking', fontsize=15, ha='center',
        fontweight='bold', color='#222222')
for y, label, content in [(6.3, 'Username', 'jhall390'),
                          (4.9, 'Password', '••••••••••')]:
    ax.text(1.2, y + 0.75, label, fontsize=10, color='#666666')
    ax.add_patch(FancyBboxPatch((1.2, y), 7.6, 0.62,
                                boxstyle='round,pad=0.05', fc='#f4f4f4',
                                ec='#bbbbbb'))
    ax.text(1.5, y + 0.30, content, fontsize=12, va='center',
            family='monospace', color='#333333')
ax.add_patch(FancyBboxPatch((1.2, 2.6), 7.6, 1.5, boxstyle='round,pad=0.08',
                            fc='#fdecea', ec='#c62828', lw=1.5))
ax.text(1.55, 3.55, '✗  Incorrect password — but SO close!', fontsize=13,
        color='#c62828', fontweight='bold', va='center')
ax.text(1.55, 2.95, "You're off by just one character. Try again!",
        fontsize=12, color='#c62828', va='center')
ax.add_patch(FancyBboxPatch((3.6, 1.1), 2.8, 0.85, boxstyle='round,pad=0.08',
                            fc='#003057', ec='none'))
ax.text(5.0, 1.52, 'Sign in', fontsize=13, color='white', ha='center',
        va='center', fontweight='bold')
fig.tight_layout()
save(fig, 'fig_password_redflag.png')
