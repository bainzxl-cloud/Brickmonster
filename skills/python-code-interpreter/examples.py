"""
Code Interpreter Examples
Example computations and use cases
"""

from code_interpreter import CodeInterpreter, math_functions, physics_functions

interpreter = CodeInterpreter()


def run_examples():
    """Run example computations."""
    print("="*60)
    print("CODE INTERPRETER EXAMPLES")
    print("="*60)
    print()
    
    # Example 1: Basic Math
    print("1. BASIC MATH")
    result = interpreter.execute("2 + 2")
    print(f"   2 + 2 = {result['result']}")
    print()
    
    # Example 2: Matrix Operations
    print("2. MATRIX MULTIPLICATION")
    code = "matmul([[1,2],[3,4]], [[5,6],[7,8]])"
    result = interpreter.execute(code)
    print(f"   [[1,2],[3,4]] × [[5,6],[7,8]] =")
    for row in result['result']:
        print(f"   {row}")
    print()
    
    # Example 3: Statistics
    print("3. STATISTICS")
    data = [85, 90, 78, 92, 88, 95, 82]
    result = interpreter.execute(f"mean({data})")
    print(f"   Data: {data}")
    print(f"   Mean: {result['result']:.2f}")
    print()
    
    # Example 4: Physics Calculation
    print("4. PHYSICS - PROJECTILE MOTION")
    code = "projectile_range(30, 45)"
    result = interpreter.execute(code)
    print(f"   v₀ = 30 m/s, θ = 45°")
    print(f"   Range = {result['result']:.2f} m")
    print()
    
    # Example 5: Eigenvalues
    print("5. EIGENVALUES")
    import numpy as np
    code = """
import numpy as np
A = np.array([[4, 1], [2, 3]])
np.linalg.eigvals(A)
"""
    result = interpreter.execute(code)
    print(f"   Eigenvalues of [[4,1],[2,3]]: {result['result']}")
    print()
    
    # Example 6: Complex Numbers
    print("6. COMPLEX NUMBERS")
    result = interpreter.execute("(3 + 4j) * (2 - 1j)")
    print(f"   (3 + 4i) × (2 - i) = {result['result']}")
    print()
    
    # Example 7: Quadratic Formula
    print("7. QUADRATIC SOLVER")
    code = """
a, b, c = 1, 5, 6
d = b**2 - 4*a*c
x1 = (-b + d**0.5) / (2*a)
x2 = (-b - d**0.5) / (2*a)
f"x = {x1:.2f}, x = {x2:.2f}"
"""
    result = interpreter.execute(code)
    print(f"   x² + 5x + 6 = 0 → {result['result']}")
    print()
    
    # Example 8: Integration
    print("8. NUMERICAL INTEGRATION")
    code = "integral(lambda x: x**2, 0, 3)"
    result = interpreter.execute(code)
    print(f"   ∫₀³ x² dx = {result['result']:.4f}")
    print()


def demo_visualization():
    """Demo visualization capability."""
    print("="*60)
    print("VISUALIZATION EXAMPLE")
    print("="*60)
    print()
    
    # This would create a plot
    code = """
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 4*np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y1, label='sin(x)', linewidth=2)
plt.plot(x, y2, label='cos(x)', linewidth=2)
plt.xlabel('x (radians)')
plt.ylabel('y')
plt.title('Sin and Cos Functions')
plt.legend()
plt.grid(True, alpha=0.3)
savefig('sin_cos_plot.png')
'Plot saved!'
"""
    
    result = interpreter.execute_with_visualization(code, "sin_cos_demo.png")
    
    if result['success']:
        print(f"   {result['result']}")
        if result['plot_generated']:
            print(f"   Plot saved: {result['plot_path']}")
    else:
        print(f"   Error: {result['error']}")


def demo_physics():
    """Demo physics calculations."""
    print("="*60)
    print("PHYSICS CALCULATIONS")
    print("="*60)
    print()
    
    calculations = [
        ("KE of 2kg at 10m/s", "ke(2, 10)"),
        ("Momentum of 5kg at 3m/s", "momentum(5, 3)"),
        ("Wave speed (f=100Hz, λ=3.43m)", "wave_speed(100, 3.43)"),
        ("Force on 5kg at 9.81m/s²", "force(5, 9.81)"),
    ]
    
    for desc, code in calculations:
        result = interpreter.execute(code)
        print(f"   {desc}: {result['result']:.2f}")


if __name__ == "__main__":
    run_examples()
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)
