"""
Physics Problem Solver
Solve common physics problems
"""

import math

def projectile_motion(v0, theta, h0=0, g=9.81):
    """Calculate projectile motion parameters."""
    theta_rad = math.radians(theta)
    
    vx = v0 * math.cos(theta_rad)
    vy = v0 * math.sin(theta_rad)
    
    # Time of flight
    t_flight = (vy + math.sqrt(vy**2 + 2*g*h0)) / g
    
    # Maximum height
    h_max = h0 + vy**2 / (2*g)
    
    # Range
    R = vx * t_flight
    
    return {
        'v0': v0,
        'theta': theta,
        'vx': vx,
        'vy_initial': vy,
        'time_of_flight': t_flight,
        'max_height': h_max,
        'range': R
    }

def kinematics_1d(d0, v0, a, t):
    """1D kinematics equations."""
    return {
        'position': d0 + v0*t + 0.5*a*t**2,
        'velocity': v0 + a*t
    }

def kinematics_2d(vx0, vy0, ax, ay, t):
    """2D kinematics."""
    return {
        'x': vx0*t + 0.5*ax*t**2,
        'y': vy0*t + 0.5*ay*t**2,
        'vx': vx0 + ax*t,
        'vy': vy0 + ay*t,
        'speed': math.sqrt((vx0+ax*t)**2 + (vy0+ay*t)**2)
    }

def circular_motion(r, omega):
    """Circular motion parameters."""
    v = r * omega
    T = 2*math.pi / omega
    f = 1/T
    a = r * omega**2
    
    return {
        'radius': r,
        'angular_velocity': omega,
        'linear_velocity': v,
        'period': T,
        'frequency': f,
        'centripetal_acceleration': a
    }

def force_newton(m, a):
    """Newton's second law: F = ma."""
    return m * a

def gravitational_force(m1, m2, r, G=6.674e-11):
    """Newton's law of gravitation."""
    return G * m1 * m2 / r**2

def kinetic_energy(m, v):
    """Kinetic energy: KE = ½mv²."""
    return 0.5 * m * v**2

def potential_energy(m, h, g=9.81):
    """Potential energy: PE = mgh."""
    return m * g * h

def spring_force(k, x):
    """Hooke's law: F = -kx."""
    return -k * x

def spring_energy(k, x):
    """Spring potential energy: ½kx²."""
    return 0.5 * k * x**2

def wave_speed(f, wavelength):
    """Wave equation: v = fλ."""
    return f * wavelength

def wave_period(f):
    """Period from frequency: T = 1/f."""
    return 1 / f

def momentum(m, v):
    """Momentum: p = mv."""
    return m * v

def impulse(F, dt):
    """Impulse: J = FΔt."""
    return F * dt

def conservation_momentum(m1, v1, m2, v2):
    """Elastic collision (1D)."""
    v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
    return v1_final, v2_final

def work(F, d, angle=0):
    """Work: W = Fd cos(θ)."""
    return F * d * math.cos(math.radians(angle))

def power(W, t):
    """Power: P = W/t."""
    return W / t

def efficiency(output, input_pct):
    """Efficiency calculation."""
    return (output / input_pct) * 100

def resistance_series(R1, R2):
    """Series resistance: R = R₁ + R₂."""
    return R1 + R2

def resistance_parallel(R1, R2):
    """Parallel resistance: R = (R₁R₂)/(R₁+R₂)."""
    return (R1 * R2) / (R1 + R2)

def ohm_law(V, I, R):
    """Ohm's law: V = IR."""
    if I == 0:
        return V / R if R != 0 else 0
    elif R == 0:
        return V / I if I != 0 else 0
    else:
        return I * R

def electric_power(V, I, R):
    """Electric power: P = VI = I²R = V²/R."""
    return V * I

def capacitor_energy(C, V):
    """Capacitor energy: ½CV²."""
    return 0.5 * C * V**2

def inductor_energy(L, I):
    """Inductor energy: ½LI²."""
    return 0.5 * L * I**2

def solve_thermodynamics(T1, T2, m, c):
    """Heat transfer: Q = mcΔT."""
    return m * c * (T2 - T1)

def ideal_gas(P, V, n, R=8.314):
    """Ideal gas law: PV = nRT."""
    return {
        'P': P,
        'V': V,
        'n': n,
        'R': R,
        'T': (P * V) / (n * R)
    }

def wavelength_photon(E, h=6.626e-34, c=3e8):
    """Wavelength from energy: λ = hc/E."""
    E_joules = E * 1.602e-19  # Convert eV to J
    return (h * c) / E_joules

def photon_energy(f, h=6.626e-34):
    """Photon energy: E = hf."""
    return h * f

def doppler_effect(f_source, v_source, v_obs, v_sound=343):
    """Doppler effect."""
    if v_source == 0:
        return f_source
    return f_source * (v_sound + v_obs) / (v_sound + v_source)

def relativistic_time_dilation(t, v, c=3e8):
    """Time dilation: t' = t/√(1-v²/c²)."""
    gamma = 1 / math.sqrt(1 - (v/c)**2)
    return t * gamma

def relativistic_mass(m0, v, c=3e8):
    """Relativistic mass."""
    gamma = 1 / math.sqrt(1 - (v/c)**2)
    return m0 * gamma

def examples():
    """Show examples of physics calculations."""
    print("="*60)
    print("PHYSICS PROBLEM EXAMPLES")
    print("="*60)
    print()
    
    # Projectile motion
    print("1. PROJECTILE MOTION")
    result = projectile_motion(30, 45)
    print(f"   v₀ = 30 m/s, θ = 45°")
    print(f"   Range = {result['range']:.2f} m")
    print(f"   Max Height = {result['max_height']:.2f} m")
    print(f"   Time of Flight = {result['time_of_flight']:.2f} s")
    print()
    
    # Circular motion
    print("2. CIRCULAR MOTION")
    result = circular_motion(2, math.pi)  # r=2m, ω=π rad/s
    print(f"   r = 2 m, ω = π rad/s")
    print(f"   Linear Velocity = {result['linear_velocity']:.2f} m/s")
    print(f"   Period = {result['period']:.2f} s")
    print()
    
    # Forces
    print("3. NEWTON'S LAWS")
    F = force_newton(5, 9.81)  # m=5kg, a=g
    print(f"   m = 5 kg, a = 9.81 m/s²")
    print(f"   F = ma = {F:.2f} N")
    print()
    
    # Energy
    print("4. ENERGY")
    KE = kinetic_energy(2, 10)  # m=2kg, v=10m/s
    PE = potential_energy(2, 5)  # m=2kg, h=5m
    print(f"   KE = ½mv² = {KE:.2f} J")
    print(f"   PE = mgh = {PE:.2f} J")
    print(f"   Total = {KE + PE:.2f} J")
    print()
    
    # Ohm's law
    print("5. ELECTRICITY")
    V = ohm_law(I=2, R=10)  # I=2A, R=10Ω
    print(f"   I = 2 A, R = 10 Ω")
    print(f"   V = IR = {V:.2f} V")
    print()
    
    # Relativistic
    print("6. RELATIVITY")
    gamma = relativistic_time_dilation(1, 0.866*c)  # v = 0.866c
    print(f"   v = 0.866c")
    print(f"   γ (gamma) = {gamma:.2f}")
    print(f"   Time dilation factor = {gamma:.2f}x")
    print()

if __name__ == "__main__":
    examples()
