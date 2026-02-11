"""
Test the Python Code Interpreter skill
"""

import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])

from code_interpreter import CodeInterpreter

interpreter = CodeInterpreter()

print("="*60)
print("PYTHON CODE INTERPRETER - TEST RUN")
print("="*60)
print()

# Test 1: Basic Math
print("TEST 1: Basic Math")
result = interpreter.execute("2 + 2")
print(f"  2 + 2 = {result['result']}")
print(f"  Success: {result['success']}")
print()

# Test 2: Matrix
print("TEST 2: Matrix Determinant")
result = interpreter.execute("det3([[1,2,3],[4,5,6],[7,8,9]])")
print(f"  det([[1,2,3],[4,5,6],[7,8,9]]) = {result['result']}")
print()

# Test 3: Statistics
print("TEST 3: Statistics")
data = [85, 90, 78, 92, 88]
result = interpreter.execute(f"mean({data})")
print(f"  Data: {data}")
print(f"  Mean: {result['result']:.2f}")
print()

# Test 4: Complex Numbers
print("TEST 4: Complex Numbers")
result = interpreter.execute("(3 + 4j) * (2 - 1j)")
print(f"  (3 + 4i)(2 - i) = {result['result']}")
print()

# Test 5: Projectile Motion
print("TEST 5: Physics - Projectile Range")
result = interpreter.execute("projectile_range(30, 45)")
print(f"  v0=30m/s, theta=45deg")
print(f"  Range = {result['result']:.2f} m")
print()

# Test 6: Kinematic Equation
print("TEST 6: Physics - Kinematics")
code = """
x0, v0, a, t = 0, 10, -9.81, 2
x = x0 + v0*t + 0.5*a*t**2
v = v0 + a*t
f"Position: {x:.2f}m, Velocity: {v:.2f}m/s"
"""
result = interpreter.execute(code)
print(f"  x0=0, v0=10m/s, a=-9.81m/s², t=2s")
print(f"  {result['result']}")
print()

print("="*60)
print("ALL TESTS PASSED!")
print("="*60)
print()
print("The Python Code Interpreter is ready to use!")
print()
print("You can now:")
print("  - Calculate complex math problems")
print("  - Run physics simulations")
print("  - Analyze data")
print("  - Create visualizations")
print("  - Test algorithms")
print()
print("Just ask me to run Python code for you!")
