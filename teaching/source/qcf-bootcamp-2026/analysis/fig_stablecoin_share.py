"""Waffle: stablecoins' ~0.3% share of cross-border retail payment volume.

Slide: stablecoin payments scorecard. Share from FXC Intelligence-Allium
analysis of 2025 cross-border retail volume (~0.3%); 1,000 squares, 3 red.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from common import RED, style, save

style()

grid = np.zeros((10, 100))
grid.reshape(-1)[:3] = 1

fig, ax = plt.subplots(figsize=(9.6, 4.4))
ax.imshow(grid, cmap=matplotlib.colors.ListedColormap(['#e8e4d8', RED]),
          aspect='auto')
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_title('1,000 squares = all cross-border retail payment volume.\n'
             'Red = the stablecoin share (~0.3%).', fontsize=15)
fig.tight_layout()
save(fig, 'fig_stablecoin_share.png')
