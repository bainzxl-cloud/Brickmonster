"""
Quick Calculation Examples
"""

import sys
sys.path.insert(0, 'skills/python-code-interpreter')
from code_interpreter import CodeInterpreter, calc

print("="*60)
print("PYTHON CODE INTERPRETER - QUICK EXAMPLES")
print("="*60)
print()

# Math examples
examples = [
    ("2 + 2", "Basic addition"),
    ("sqrt(144)", "Square root"),
    ("2**10", "2^10 = 1024"),
    ("pi", "Pi constant"),
    ("sin(30)", "Sine of 30 degrees"),
    ("cos(45)", "Cosine of 45 degrees"),
    ("tan(60)", "Tangent of 60 degrees"),
    ("log(100)", "Log base 10"),
    ("ln(e)", "Natural log"),
    ("mean([85, 90, 78, 92, 88])", "Statistics - Mean"),
    ("std([1, 2, 3, 4, 5])", "Statistics - Std Dev"),
    ("det([[1, 2], [3, 4]])", "Matrix - 2x2 determinant"),
    ("det([[1, 2, 3], [4, 5, 6], [7, 8, 9]])", "Matrix - 3x3 determinant"),
    ("eigvals([[4, 0], [0, 3]])", "Eigenvalues"),
    ("projectile_range(30, 45)", "Physics - Range (v0=30, θ=45°)"),
    ("projectile_time(30, 45)", "Physics - Time of flight"),
    ("ke(2, 10)", "Physics - KE (m=2kg, v=10m/s)"),
    ("momentum(5, 3)", "Physics - Momentum (m=5kg, v=3m/s)"),
    ("wave_speed(100, 3.43)", "Physics - Wave speed (f=100Hz, λ=3.43m)"),
    ("force(5, 9.81)", "Physics - Force (m=5kg, a=9.81m/s²)"),
]

for code, desc in examples:
    result = calc(code)
    print(f"{desc:35} {code:40} → {result}")

print()
print("="*60)
print("READY FOR USE!")
print("="*60)
