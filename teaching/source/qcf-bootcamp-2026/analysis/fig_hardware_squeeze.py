"""AI demand vs crypto: memory prices up, crypto energy claim down or flat.

Slide: "AI's Second Squeeze Is in Hardware". Left panel: DDR5 PC/server
memory spot prices ~+110% Q1 2026, DRAM contract prices projected ~+60%
Q2 (TrendForce, industry press, early 2026). Right panel: Ethereum
pre-Merge ~112 TWh/yr vs ~0.01 after (CCRI/Digiconomist), Bitcoin
~140 TWh/yr (CBECI, 2026).
"""
import matplotlib.pyplot as plt
from common import NAVY, GOLD, RED, STEEL, HUMAN, style, save

style()

fig, (b1, b2) = plt.subplots(1, 2, figsize=(10.5, 4.2))

mem_vals = [110, 60]
bars = b1.bar(['PC/server memory\n(DDR5), Q1 2026',
               'memory contracts\n(DRAM), Q2 proj.'],
              mem_vals, color=[RED, RED], width=0.5)
for b, v in zip(bars, mem_vals):
    b1.text(b.get_x() + b.get_width() / 2, v + 3, f'+{v}%',
            ha='center', fontsize=16, fontweight='bold')
b1.set_ylabel('price change (%)')
b1.set_ylim(0, 135)
b1.set_title('AI demand hits memory prices')
b1.tick_params(axis='x', labelsize=11)

en_vals = [112, 0.01, 140]
bars = b2.bar(['Ethereum\npre-Merge', 'Ethereum\ntoday', 'Bitcoin\ntoday'],
              en_vals, color=[STEEL, GOLD, NAVY], width=0.5)
b2.set_yscale('log')
b2.set_ylim(0.005, 400)
b2.yaxis.set_major_formatter(HUMAN)
for b, v, lab in zip(bars, en_vals, ['112', '~0', '140']):
    b2.text(b.get_x() + b.get_width() / 2, v * 1.4, lab,
            ha='center', fontsize=15, fontweight='bold')
b2.set_ylabel('TWh/yr (log)')
b2.set_title("crypto's energy claim, down or flat")
fig.tight_layout()
save(fig, 'fig_hardware_squeeze.png')
