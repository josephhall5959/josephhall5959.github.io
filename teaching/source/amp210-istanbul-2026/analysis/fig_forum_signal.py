"""Arbitrum DAO: did forum discussion predict how close the vote was?

Slide: "Cheap AI Text Erased the Signal in a $3.5 Billion DAO's Forum".
Correlation between human-written forum posts and the vote's margin of
victory, before and after the Claude 3 release (2024-03-04), with 95%
confidence intervals (Fisher z). Data: data/matched_proposals.csv, the
102 matched proposals from Huang and Hall (2026), copied from
~/arbitrum-governance/data/.
"""
import csv
import math
import os
import matplotlib.pyplot as plt
from common import NAVY, RED, MUTED, DATA, style, save

style(font_size=17)
rows = list(csv.DictReader(open(os.path.join(DATA, 'matched_proposals.csv'))))
BREAK = '2024-03-04'


def corr_ci(pairs):
    n = len(pairs)
    xs, ys = zip(*pairs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in pairs)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    r = sxy / math.sqrt(sxx * syy)
    z, se = math.atanh(r), 1 / math.sqrt(n - 3)
    return r, math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se), n


pre = [(float(r['human_posts']), float(r['margin'])) for r in rows if r['created'][:10] < BREAK]
post = [(float(r['human_posts']), float(r['margin'])) for r in rows if r['created'][:10] >= BREAK]
res = [corr_ci(pre), corr_ci(post)]
for lab, (r, lo, hi, n) in zip(['pre', 'post'], res):
    print(f'  {lab}: r={r:.3f} [{lo:.3f}, {hi:.3f}] n={n}')

fig, ax = plt.subplots(figsize=(7.2, 5.4))
labels = [f'Before Claude 3\n({res[0][3]} proposals)', f'After Claude 3\n({res[1][3]} proposals)']
for i, ((r, lo, hi, n), c) in enumerate(zip(res, [NAVY, RED])):
    ax.errorbar(i, r, yerr=[[r - lo], [hi - r]], fmt='o', color=c, ms=12,
                capsize=10, lw=2.5)
    ax.text(i + 0.1, r, f'{r:.2f}', color=c, fontsize=19, va='center')
ax.axhline(0, color=MUTED, lw=1, ls='--')
ax.set_xticks([0, 1])
ax.set_xticklabels(labels)
ax.set_xlim(-0.5, 1.5)
ax.set_ylabel('correlation: forum posts\nvs. vote margin')
ax.text(0.5, 0.02, 'zero = no signal', color=MUTED,
        fontsize=14, ha='center', va='bottom')
fig.tight_layout()
save(fig, 'fig_forum_signal.png')
