"""
Simple Physics Experiment Test - Standard Deviation & Uncertainty
Using basic Python only (no external dependencies)
"""

import math

# Sample pendulum data
L = [0.500, 0.550, 0.600, 0.650, 0.700]  # Length (m)
T = [1.420, 1.490, 1.555, 1.615, 1.672]  # Period (s)

# Calculate g for each measurement
g_values = []
for i in range(len(L)):
    g = 4 * math.pi**2 * L[i] / T[i]**2
    g_values.append(g)

# Calculate statistics
n = len(g_values)
mean = sum(g_values) / n

# Standard deviation
squared_diffs = [(g - mean)**2 for g in g_values]
variance = sum(squared_diffs) / (n - 1)  # Sample variance
std_dev = math.sqrt(variance)

# Standard error
sem = std_dev / math.sqrt(n)

# 95% CI (t ≈ 2.776 for df=4, α/2=0.025)
t_critical = 2.776
ci = t_critical * sem

print("=" * 60)
print("SIMPLE PENDULUM EXPERIMENT - UNCERTAINTY ANALYSIS")
print("=" * 60)
print(f"\nNumber of measurements: {n}")

print("\nRaw Data:")
print("-" * 40)
for i in range(n):
    print(f"  L = {L[i]:.3f} m, T = {T[i]:.3f} s, g = {g_values[i]:.4f} m/s²")

print(f"\nResults:")
print("-" * 40)
print(f"  Mean g:           {mean:.4f} m/s²")
print(f"  Std deviation:    {std_dev:.4f} m/s²")
print(f"  Std error (SEM):  {sem:.4f} m/s²")
print(f"  95% CI:           ±{ci:.4f} m/s²")
print(f"\nFinal Result:")
print("-" * 40)
print(f"  g = {mean:.2f} ± {ci:.2f} m/s²  (95% CI)")

print("\nValidation:")
print("-" * 40)
g_accepted = 9.81
deviation = abs(mean - g_accepted)
deviation_sigma = deviation / std_dev
print(f"  Accepted value:  {g_accepted} m/s^2")
print(f"  Deviation:        {deviation:.4f} m/s^2")
print(f"  Deviation:        {deviation_sigma:.2f} standard deviations")

if deviation_sigma < 2:
    print("\n[OK] Result consistent with accepted value (< 2 sigma)")
else:
    print("\n[WARNING] Result differs from accepted value (> 2 sigma)")

print("\n============================================================")
print("Standard Deviation & Uncertainty Analysis Complete!")
print("============================================================")
