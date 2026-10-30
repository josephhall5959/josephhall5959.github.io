"""Arbitrum DAO: forum debate predicted vote margins before Claude 3, and much less after.

Slide: "AI Writing Weakened a $3.5 Billion DAO's Forum".
Each dot is one of the 102 matched proposals of Huang and Hall (2026):
human-written posts in the proposal's forum thread (x) against the vote's
margin of victory (y), split at the Claude 3 release (2024-03-04), with an
OLS line per period. Data: data/matched_proposals.csv, copied from
~/arbitrum-governance/data/.
"""
import csv
import os
import matplotlib.pyplot as plt
from common import NAVY, RED, MUTED, DATA, style, save

style(font_size=17)
rows = list(csv.DictReader(open(os.path.join(DATA, 'matched_proposals.csv'))))
BREAK = '2024-03-04'


def ols(pts):
    n = len(pts); mx = sum(x for x, _ in pts) / n; my = sum(y for _, y in pts) / n
    b = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)
    return my - b * mx, b


groups = [('Before Claude 3', NAVY, 'o', [r for r in rows if r['created'][:10] < BREAK]),
          ('After Claude 3', RED, '^', [r for r in rows if r['created'][:10] >= BREAK])]
fig, ax = plt.subplots(figsize=(12, 5.2))
for lab, c, m, g in groups:
    pts = [(float(r['human_posts']), 100 * float(r['margin'])) for r in g]
    a, b = ols(pts)
    xs = [x for x, _ in pts]
    ax.scatter(*zip(*pts), color=c, marker=m, s=55, alpha=0.75, label=f'{lab} ({len(pts)} proposals)')
    lo, hi = min(xs), max(xs)
    ax.plot([lo, hi], [a + b * lo, a + b * hi], color=c, lw=3)
    print(f'  {lab}: n={len(pts)} slope={b:.3f} pts per post, intercept={a:.1f}')
ax.set_xlabel('Human-written posts in the proposal\'s forum thread')
ax.set_ylabel('Margin of victory (%)')
ax.set_ylim(-3, 105)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, handletextpad=0.3)
fig.tight_layout()
save(fig, 'fig_forum_scatter.png')
