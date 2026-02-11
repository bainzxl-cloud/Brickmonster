"""
Physics Experiment Test: Simple Pendulum
Calculating gravitational acceleration with uncertainty analysis
"""

import numpy as np
from scipy import stats
import json

# Sample pendulum data (length in meters, period in seconds)
L = np.array([0.500, 0.550, 0.600, 0.650, 0.700])  # Length (m)
T = np.array([1.420, 1.490, 1.555, 1.615, 1.672])  # Period (s)

# Calculate g for each measurement: g = 4π²L/T²
g_values = 4 * np.pi**2 * L / T**2

# Statistics
g_mean = np.mean(g_values)
g_std = np.std(g_values, ddof=1)  # Sample standard deviation
n = len(g_values)
g_sem = g_std / np.sqrt(n)  # Standard error of mean

# 95% Confidence Interval (t-distribution, since n is small)
t_critical = stats.t.ppf(0.975, df=n-1)  # t(0.975, df=4)
g_ci = t_critical * g_sem

# Relative uncertainty
relative_uncertainty = (g_std / g_mean) * 100

print("=" * 60)
print("SIMPLE PENDULUM EXPERIMENT ANALYSIS")
print("=" * 60)
print()
print(f"Number of measurements: {n}")
print()
print("Raw Data:")
print("-" * 40)
for i in range(n):
    print(f"  L = {L[i]:.3f} m, T = {T[i]:.3f} s, g = {g_values[i]:.4f} m/s²")
print()
print("Results:")
print("-" * 40)
print(f"  Mean g:              {g_mean:.4f} m/s²")
print(f"  Standard deviation:    {g_std:.4f} m/s²")
print(f"  Standard error (SEM):  {g_sem:.4f} m/s²")
print(f"  95% CI:               ±{g_ci:.4f} m/s²")
print()
print(f"Final Result:")
print("-" * 40)
print(f"  g = {g_mean:.2f} ± {g_ci:.2f} m/s² (95% CI)")
print()
print(f"Relative uncertainty: {relative_uncertainty:.2f}%")
print()

# Compare to accepted value
g_accepted = 9.81
deviation = abs(g_mean - g_accepted)
deviation_sigma = deviation / g_std

print("Validation:")
print("-" * 40)
print(f"  Accepted value:       {g_accepted} m/s²")
print(f"  Deviation:           {deviation:.4f} m/s²")
print(f"  Deviation (σ):       {deviation_sigma:.2f} σ")
print()

if deviation_sigma < 2:
    print("✓ Result is consistent with accepted value (< 2σ)")
else:
    print("⚠ Result differs from accepted value (> 2σ)")

# Linear regression: T² vs L (should be linear: T² = 4π²L/g)
T_squared = T**2
slope, intercept, r_value, p_value, std_err = stats.linregress(L, T_squared)

g_from_fit = 4 * np.pi**2 / slope
g_from_fit_err = (std_err / slope) * g_from_fit

print("Linear Regression Analysis:")
print("-" * 40)
print(f"  Slope (4π²/g):     {slope:.4f}")
print(f"  R² value:         {r_value**2:.6f}")
print()
print(f"g from linear fit:  {g_from_fit:.4f} ± {g_from_fit_err:.4f} m/s²")
print()
print("=" * 60)
