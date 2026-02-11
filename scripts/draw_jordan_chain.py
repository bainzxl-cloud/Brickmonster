"""
Jordan Chain Diagram - Why Initial Elements Form Basis for ker(N)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.set_aspect('equal')
ax.axis('off')

# Title
ax.text(8, 11.5, 'JORDAN CHAIN: Why Initial Elements Form Basis for ker(N)',
        fontsize=18, fontweight='bold', ha='center', va='center')
ax.text(8, 10.9, 'Nilpotent Operator N (N^m = 0 for some m)',
        fontsize=12, ha='center', va='center', style='italic')

# Draw main Jordan chain
chain_x = [2, 5, 8, 11]
chain_y = [5, 5, 5, 5]

# Draw chain boxes
for i, (x, y) in enumerate(zip(chain_x, chain_y)):
    box = FancyBboxPatch((x-0.8, y-0.4), 1.6, 0.8,
                         boxstyle="round,pad=0.05",
                         facecolor='lightblue', edgecolor='navy', linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, f'v{i+1}', fontsize=14, fontweight='bold',
            ha='center', va='center')

# Draw N arrows between chain elements
for i in range(len(chain_x)-1):
    ax.annotate('', xy=(chain_x[i+1]-1, chain_y[i+1]), 
                xytext=(chain_x[i]+1, chain_y[i]),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    mid_x = (chain_x[i] + chain_x[i+1]) / 2
    ax.text(mid_x, chain_y[i] + 0.5, 'N', fontsize=12, color='red', 
            ha='center', fontweight='bold')

# Label nilpotent condition
ax.text(6.5, 4.3, 'Nᵏv₁ = 0 (nilpotent!)', fontsize=10, 
        ha='center', style='italic', color='darkred')

# Draw ker(N), ker(N²), ker(N³) regions
ker_regions = [
    (1.5, 8, 'ker(N)\n{BASIS: v₁, w₁, ...}', 'yellow'),
    (5, 8, 'ker(N²)\n{Span: v₁, Nv₁, w₁, ...}', 'lightyellow'),
    (10, 8, 'ker(N³) ⊃ ... ⊃ ker(N)\n{All generalized eigenvectors}', 'lightyellow'),
]

for x, y, text, color in ker_regions:
    box = FancyBboxPatch((x-0.1, y-0.1), 3.2, 1.2,
                         boxstyle="round,pad=0.1",
                         facecolor=color, edgecolor='orange', linewidth=2)
    ax.add_patch(box)
    ax.text(x + 1.5, y + 0.5, text, fontsize=9, ha='center', va='center')

# Draw arrows showing inclusion
ax.annotate('', xy=(4, 8.7), xytext=(2.5, 8.7),
           arrowprops=dict(arrowstyle='->', color='green', lw=2))
ax.annotate('', xy=(8, 8.7), xytext=(6, 8.7),
           arrowprops=dict(arrowstyle='->', color='green', lw=2))
ax.annotate('', xy=(12, 8.7), xytext=(10, 8.7),
           arrowprops=dict(arrowstyle='->', color='green', lw=2))

ax.text(5.2, 9.1, '⊂', fontsize=14, ha='center', color='green')
ax.text(7.2, 9.1, '⊂', fontsize=14, ha='center', color='green')
ax.text(11.2, 9.1, '⊂', fontsize=14, ha='center', color='green')

# Key insight box
insight_box = FancyBboxPatch((0.5, 0.3), 6.5, 2.2,
                              boxstyle="round,pad=0.1",
                              facecolor='lightgreen', edgecolor='darkgreen', linewidth=2)
ax.add_patch(insight_box)
ax.text(3.8, 2.2, 'KEY INSIGHT', fontsize=12, fontweight='bold', 
        ha='center', color='darkgreen')
ax.text(3.8, 1.5, '• Initial element v₁ generates ENTIRE chain', fontsize=10, ha='center')
ax.text(3.8, 1.0, '• v₁ ∈ ker(N) because Nᵏv₁ = 0', fontsize=10, ha='center')
ax.text(3.8, 0.5, '• All initial elements are linearly independent', fontsize=10, ha='center')

# Chain decomposition example
chain_box = FancyBboxPatch((8, 0.3), 7.5, 2.2,
                            boxstyle="round,pad=0.1",
                            facecolor='lightblue', edgecolor='navy', linewidth=2)
ax.add_patch(chain_box)
ax.text(11.75, 2.2, 'CHAIN DECOMPOSITION', fontsize=12, fontweight='bold', 
        ha='center', color='navy')
ax.text(11.75, 1.5, 'Any w ∈ ker(N) = c₁v₁ + c₂w₁ + ...', fontsize=10, ha='center')
ax.text(11.75, 1.0, 'Chain 1: v₁ → v₂ → v₃ → 0', fontsize=9, ha='center')
ax.text(11.75, 0.6, 'Chain 2: w₁ → w₂ → 0', fontsize=9, ha='center')
ax.text(11.75, 0.4, 'ker(N) basis = {v₁, w₁} (initial elements!)', fontsize=10, 
        ha='center', fontweight='bold', color='red')

# Draw arrow from insight to chain
ax.annotate('', xy=(8.5, 2.5), xytext=(7.5, 2.5),
           arrowprops=dict(arrowstyle='->', color='purple', lw=2))

# Legend
legend_elements = [
    mpatches.Patch(facecolor='lightblue', edgecolor='navy', label='Jordan Chain Elements'),
    mpatches.Patch(facecolor='yellow', edgecolor='orange', label='Kernel Spaces'),
    mpatches.Patch(facecolor='lightgreen', edgecolor='darkgreen', label='Key Insights'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)

plt.tight_layout()
plt.savefig('jordan_chain_diagram.png', dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.close()

print("Diagram saved: jordan_chain_diagram.png")
