"""
Jordan Chain Detailed Proof Diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.suptitle('JORDAN CHAIN: Step-by-Step Proof', fontsize=20, fontweight='bold', y=0.98)

# ============================================
# TOP LEFT: Chain Structure
# ============================================
ax1 = axes[0, 0]
ax1.set_xlim(0, 14)
ax1.set_ylim(0, 10)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('1. Jordan Chain Structure', fontsize=14, fontweight='bold', pad=10)

# Draw chain
chain_x = [2, 5, 8, 11]
chain_y = [5, 5, 5, 5]

for i, (x, y) in enumerate(zip(chain_x, chain_y)):
    box = FancyBboxPatch((x-0.8, y-0.4), 1.6, 0.8,
                         boxstyle="round,pad=0.05",
                         facecolor='lightblue', edgecolor='navy', linewidth=2)
    ax1.add_patch(box)
    ax1.text(x, y, f'v{i+1}', fontsize=14, fontweight='bold', ha='center', va='center')

for i in range(len(chain_x)-1):
    ax1.annotate('', xy=(chain_x[i+1]-0.9, chain_y[i+1]), 
                xytext=(chain_x[i]+0.9, chain_y[i]),
                arrowprops=dict(arrowstyle='->', color='red', lw=2.5))
    mid_x = (chain_x[i] + chain_x[i+1]) / 2
    ax1.text(mid_x, chain_y[i] + 0.6, 'N', fontsize=11, color='red', 
            ha='center', fontweight='bold')

# Label nilpotent
ax1.text(6.5, 4.2, 'Nᵐv₁ = 0 (nilpotent!)', fontsize=11, 
        ha='center', color='darkred', fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='red'))

# Notation
ax1.text(7, 2, 'Nᵏ⁻¹v₁ ≠ 0, Nᵏv₁ = 0', fontsize=10, ha='center', style='italic')
ax1.text(7, 1.2, 'k = length of chain', fontsize=10, ha='center', style='italic')

# ============================================
# TOP RIGHT: Kernel Inclusion
# ============================================
ax2 = axes[0, 1]
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 10)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('2. Kernel Inclusion Chain', fontsize=14, fontweight='bold', pad=10)

# Nested ellipses
from matplotlib.patches import Ellipse
ellipses = [
    (7, 6.5, 3, 2, 'ker(Nᵐ)\n= Whole Space', 'lightyellow', 0.9),
    (7, 6.2, 2.5, 1.6, 'ker(N³)', 'lightyellow', 0.8),
    (7, 5.9, 2, 1.2, 'ker(N²)', 'lightyellow', 0.7),
    (7, 5.6, 1.5, 0.8, 'ker(N)', 'yellow', 0.6),
]

for x, y, w, h, text, color, alpha in ellipses:
    ellipse = Ellipse((x, y), w, h, facecolor=color, edgecolor='orange', 
                       linewidth=2, alpha=alpha)
    ax2.add_patch(ellipse)
    ax2.text(x, y, text, fontsize=8, ha='center', va='center')

# Arrows showing inclusion
ax2.annotate('', xy=(7, 4.8), xytext=(7, 4.3),
            arrowprops=dict(arrowstyle='->', color='green', lw=2))
ax2.annotate('', xy=(7, 4.0), xytext=(7, 3.5),
            arrowprops=dict(arrowstyle='->', color='green', lw=2))
ax2.annotate('', xy=(7, 3.2), xytext=(7, 2.7),
            arrowprops=dict(arrowstyle='->', color='green', lw=2))

ax2.text(8.2, 4.5, '⊂', fontsize=14, color='green', fontweight='bold')
ax2.text(8.2, 3.7, '⊂', fontsize=14, color='green', fontweight='bold')
ax2.text(8.2, 2.9, '⊂', fontsize=14, color='green', fontweight='bold')

# Key point
ax2.text(7, 1.2, 'Initial element v₁ ∈ ker(N)\nbut v₁ ∉ ker(Nᵏ) for k < m',
        fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightgreen', edgecolor='darkgreen'))

# ============================================
# BOTTOM LEFT: Linear Independence Proof
# ============================================
ax3 = axes[1, 0]
ax3.set_xlim(0, 14)
ax3.set_ylim(0, 10)
ax3.axis('off')
ax3.set_title('3. Linear Independence Proof', fontsize=14, fontweight='bold', pad=10)

# Proof steps
proof_steps = [
    ('Suppose:', 'c₁v₁ + c₂w₁ + ... = 0'),
    ('Apply N:', 'c₁Nv₁ + c₂Nw₁ + ... = 0'),
    ('⇒', 'c₁v₂ + c₂w₂ + ... = 0'),
    ('Apply N again:', 'c₁Nv₂ + ... = 0'),
    ('⇒', 'c₁v₃ + ... = 0'),
    ('Continue...', 'Eventually: c₁ × (chain element) = 0'),
    ('∴', 'c₁ = 0 (chain elements ≠ 0)'),
    ('Similarly:', 'c₂ = c₃ = ... = 0'),
    ('Conclusion:', 'Initial elements are LIN. INDEPENDENT! ✓'),
]

for i, (step, detail) in enumerate(proof_steps):
    y_pos = 8 - i * 0.9
    ax3.text(1, y_pos, step, fontsize=10, fontweight='bold', ha='left')
    ax3.text(4.5, y_pos, detail, fontsize=10, ha='left')
    if step == '∴' or step == 'Conclusion:':
        ax3.text(10, y_pos, '✓', fontsize=12, color='green', fontweight='bold')

# Highlight conclusion
ax3.text(7, 1, '⇒ All coefficients must be zero!', fontsize=11, 
        ha='center', fontweight='bold', color='darkgreen',
        bbox=dict(boxstyle='round', facecolor='lightgreen', edgecolor='darkgreen'))

# ============================================
# BOTTOM RIGHT: Summary & Example
# ============================================
ax4 = axes[1, 1]
ax4.set_xlim(0, 14)
ax4.set_ylim(0, 10)
ax4.axis('off')
ax4.set_title('4. Complete Example', fontsize=14, fontweight='bold', pad=10)

# Example chains
ax4.text(7, 9, 'Two Jordan Chains for Nilpotent N:', fontsize=11, ha='center')

# Chain 1
ax4.text(3.5, 7.5, 'Chain 1:', fontsize=10, fontweight='bold')
for i, (x, y) in enumerate([(5, 7.5), (7, 7.5), (9, 7.5)]):
    box = FancyBboxPatch((x-0.5, y-0.3), 1, 0.6,
                         boxstyle="round,pad=0.02",
                         facecolor='lightblue', edgecolor='navy', linewidth=1.5)
    ax4.add_patch(box)
    ax4.text(x, y, f'v{i+1}', fontsize=10, ha='center', va='center')
    if i < 2:
        ax4.annotate('', xy=(x+0.6, y), xytext=(x+0.4, y),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

# Chain 2
ax4.text(3.5, 5.5, 'Chain 2:', fontsize=10, fontweight='bold')
for i, (x, y) in enumerate([(5, 5.5), (7, 5.5)]):
    box = FancyBboxPatch((x-0.5, y-0.3), 1, 0.6,
                         boxstyle="round,pad=0.02",
                         facecolor='lightblue', edgecolor='navy', linewidth=1.5)
    ax4.add_patch(box)
    ax4.text(x, y, f'w{i+1}', fontsize=10, ha='center', va='center')
    if i == 0:
        ax4.annotate('', xy=(x+0.6, y), xytext=(x+0.4, y),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

# Result
ax4.text(7, 3.5, 'ker(N) = Span{v₁, w₁}', fontsize=12, ha='center', 
        fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='yellow', edgecolor='orange'))

ax4.text(7, 2.5, 'Initial elements {v₁, w₁} form a BASIS! ✓', 
        fontsize=11, ha='center', color='darkgreen', fontweight='bold')

ax4.text(7, 1.2, 'Because:\n• Both in ker(N) ✓\n• Span ker(N) ✓\n• Linearly independent ✓',
        fontsize=9, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightgreen', edgecolor='darkgreen'))

plt.tight_layout()
plt.savefig('jordan_chain_detailed.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Detailed diagram saved: jordan_chain_detailed.png")
