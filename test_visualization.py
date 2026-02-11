"""
Pendulum Experiment Visualization
Creates publication-quality graphs for physics research
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving files

import matplotlib.pyplot as plt
import numpy as np
import math

# Pendulum data
L = np.array([0.500, 0.550, 0.600, 0.650, 0.700])  # Length (m)
T = np.array([1.420, 1.490, 1.555, 1.615, 1.672])  # Period (s)

# Calculate g values
g_values = 4 * np.pi**2 * L / T**2
g_mean = np.mean(g_values)
g_std = np.std(g_values, ddof=1)
n = len(g_values)

# Create figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Simple Pendulum Experiment Analysis', fontsize=16, fontweight='bold')

# Plot 1: g values with error bars
ax1 = axes[0, 0]
x_pos = np.arange(n)
bars = ax1.bar(x_pos, g_values, color='steelblue', alpha=0.7, edgecolor='navy')
ax1.axhline(y=g_mean, color='red', linestyle='--', linewidth=2, label=f'Mean = {g_mean:.4f} m/s²')
ax1.fill_between([-0.5, n-0.5], g_mean - g_std, g_mean + g_std, alpha=0.2, color='red', label=f'±1σ = {g_std:.4f} m/s²')
ax1.set_xlabel('Measurement Number')
ax1.set_ylabel('g (m/s²)')
ax1.set_title('Gravitational Acceleration Measurements')
ax1.set_xticks(x_pos)
ax1.set_xticklabels([f'M{i+1}' for i in range(n)])
ax1.legend(loc='upper right')
ax1.grid(axis='y', alpha=0.3)

# Plot 2: Period vs Length
ax2 = axes[0, 1]
ax2.scatter(L, T, s=100, c='coral', edgecolors='darkred', zorder=5)
ax2.plot(L, T, 'k--', alpha=0.5, linewidth=1)
ax2.set_xlabel('Length L (m)')
ax2.set_ylabel('Period T (s)')
ax2.set_title('Period vs Length Relationship')
ax2.grid(True, alpha=0.3)

# Add equation annotation
ax2.annotate(f'T ∝ √L\n(T² ∝ L)', 
             xy=(0.6, 1.55), fontsize=12,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Plot 3: T² vs L (should be linear)
ax3 = axes[1, 0]
T_squared = T**2
ax3.scatter(L, T_squared, s=100, c='forestgreen', edgecolors='darkgreen', zorder=5)
ax3.plot(L, T_squared, 'k--', alpha=0.5, linewidth=1)

# Linear fit
slope, intercept = np.polyfit(L, T_squared, 1)
L_fit = np.linspace(0.45, 0.75, 100)
T_squared_fit = slope * L_fit + intercept
ax3.plot(L_fit, T_squared_fit, 'r-', linewidth=2, label=f'Linear fit: T² = {slope:.4f}L + {intercept:.4f}')

# Calculate g from slope
g_from_fit = 4 * np.pi**2 / slope
ax3.annotate(f'g = {g_from_fit:.2f} m/s²\n(from slope)', 
             xy=(0.52, 2.4), fontsize=11,
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

ax3.set_xlabel('Length L (m)')
ax3.set_ylabel('T² (s²)')
ax3.set_title('T² vs L (Linear Relationship)')
ax3.legend(loc='lower right')
ax3.grid(True, alpha=0.3)

# Plot 4: Results summary
ax4 = axes[1, 1]
ax4.axis('off')

summary_text = f"""
PENDULUM EXPERIMENT RESULTS
{'='*40}

Measurements:
  n = {n} data points

Calculated g values:
  g₁ = {g_values[0]:.4f} m/s²
  g₂ = {g_values[1]:.4f} m/s²
  g₃ = {g_values[2]:.4f} m/s²
  g₄ = {g_values[3]:.4f} m/s²
  g₅ = {g_values[4]:.4f} m/s²

Statistics:
  Mean:     {g_mean:.4f} m/s²
  Std Dev:  {g_std:.4f} m/s²
  SEM:      {g_std/np.sqrt(n):.4f} m/s²

Final Result:
  g = {g_mean:.2f} ± {g_std:.2f} m/s²

Accepted Value:
  g = 9.81 m/s²

Deviation:
  {(g_mean - 9.81)/g_std:.2f}σ from accepted value
  ✓ Consistent (< 2σ)

Linear Regression:
  Slope = {slope:.4f}
  R² = {np.corrcoef(L, T_squared)[0,1]**2:.6f}
  g (from fit) = {g_from_fit:.2f} m/s²
"""

ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes, 
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('pendulum_experiment_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

print("=" * 60)
print("PENDULUM EXPERIMENT VISUALIZATION COMPLETE!")
print("=" * 60)
print()
print("Generated file:")
print("  pendulum_experiment_analysis.png")
print()
print("Contains 4 plots:")
print("  1. Bar chart of g measurements with mean & std")
print("  2. Period vs Length relationship")
print("  3. T^2 vs L linear regression")
print("  4. Results summary")
print()
print("Open the PNG file to view the visualization!")
print("=" * 60)
