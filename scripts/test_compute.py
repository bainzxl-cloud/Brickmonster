"""
Test computation scripts
"""

from physics_solver import projectile_motion, kinetic_energy, potential_energy, ohm_law

# Test calculations
r = projectile_motion(30, 45)
print('PROJECTILE MOTION (v0=30m/s, theta=45deg)')
print(f'  Range: {r["range"]:.2f} m')
print(f'  Max Height: {r["max_height"]:.2f} m')
print(f'  Time of Flight: {r["time_of_flight"]:.2f} s')
print()

KE = kinetic_energy(2, 10)
PE = potential_energy(2, 5)
print('ENERGY (m=2kg)')
print(f'  Kinetic: {KE:.2f} J')
print(f'  Potential: {PE:.2f} J')
print(f'  Total: {KE+PE:.2f} J')
print()

V = ohm_law(I=2, R=10)
print('ELECTRICITY (I=2A, R=10ohm)')
print(f'  Voltage: {V:.2f} V')
