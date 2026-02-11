"""
Study Computation Toolbox
Quick calculations for math & physics
"""

import math
import cmath
import statistics
from fractions import Fraction

def calculate():
    """Interactive calculation mode."""
    print("="*60)
    print("STUDY COMPUTATION TOOLBOX")
    print("="*60)
    print()
    print("Available calculations:")
    print("  1. Basic math ( +, -, *, /, ** )")
    print("  2. Square root (sqrt)")
    print("  3. Trigonometry (sin, cos, tan)")
    print("  4. Logarithms (log, ln)")
    print("  5. Complex numbers")
    print("  6. Statistics (mean, std, variance)")
    print("  7. Derivatives (numerical)")
    print("  8. Integrals (numerical)")
    print("  9. Matrix operations")
    print(" 10. Solve equations")
    print(" 11. Unit conversions")
    print(" 12. Base conversions")
    print()
    print("Type 'exit' to quit")
    print()

def basic_calc(expression):
    """Evaluate basic math expression."""
    try:
        # Safe evaluation
        allowed = {
            'abs': abs, 'max': max, 'min': min, 'round': round,
            'sum': sum, 'len': len,
            'math': math, 'Fraction': Fraction
        }
        result = eval(expression, {"__builtins__": {}}, allowed)
        return result
    except Exception as e:
        return f"Error: {e}"

def trig_calc(func, value, degrees=True):
    """Trigonometry calculations."""
    import math
    if degrees:
        rad = math.radians(value)
    else:
        rad = value
    
    func = func.lower()
    if func == 'sin':
        return math.sin(rad)
    elif func == 'cos':
        return math.cos(rad)
    elif func == 'tan':
        return math.tan(rad)
    elif func == 'arcsin':
        return math.degrees(math.asin(value))
    elif func == 'arccos':
        return math.degrees(math.acos(value))
    elif func == 'arctan':
        return math.degrees(math.atan(value))
    else:
        return "Unknown function"

def complex_calc(a, b, op):
    """Complex number calculations."""
    z1 = complex(a[0], a[1])
    z2 = complex(b[0], b[1])
    
    if op == '+':
        return z1 + z2
    elif op == '-':
        return z1 - z2
    elif op == '*':
        return z1 * z2
    elif op == '/':
        return z1 / z2
    else:
        return "Unknown operation"

def statistics_calc(data, func):
    """Statistical calculations."""
    data = list(map(float, data))
    func = func.lower()
    
    if func == 'mean' or func == 'avg':
        return statistics.mean(data)
    elif func == 'median':
        return statistics.median(data)
    elif func == 'mode':
        return statistics.mode(data)
    elif func == 'std' or func == 'stdev':
        return statistics.stdev(data)
    elif func == 'variance':
        return statistics.variance(data)
    elif func == 'sum':
        return sum(data)
    elif func == 'min':
        return min(data)
    elif func == 'max':
        return max(data)
    elif func == 'range':
        return max(data) - min(data)
    else:
        return "Unknown function"

def numerical_derivative(f, x, h=0.0001):
    """Calculate numerical derivative."""
    return (f(x + h) - f(x - h)) / (2 * h)

def numerical_integral(f, a, b, n=1000):
    """Calculate numerical integral using Simpson's rule."""
    h = (b - a) / n
    s = f(a) + f(b)
    
    for i in range(1, n):
        x = a + i * h
        s += 4 * f(x) if i % 2 == 1 else 2 * f(x)
    
    return s * h / 3

def matrix_multiply(A, B):
    """Multiply two matrices."""
    if len(A[0]) != len(B):
        return "Error: Matrix dimensions incompatible"
    
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(A[0])):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def matrix_add(A, B):
    """Add two matrices."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return "Error: Matrix dimensions incompatible"
    
    result = [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    return result

def determinant(A):
    """Calculate determinant of matrix."""
    n = len(A)
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        # Use expansion by minors
        det = 0
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * determinant(minor)
        return det

def solve_quadratic(a, b, c):
    """Solve quadratic equation ax² + bx + c = 0."""
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        x1 = (-b + discriminant**0.5) / (2*a)
        x2 = (-b - discriminant**0.5) / (2*a)
        return f"x = {x1:.4f}, x = {x2:.4f}"
    elif discriminant == 0:
        x = -b / (2*a)
        return f"x = {x:.4f}"
    else:
        real = -b / (2*a)
        imag = abs(discriminant)**0.5 / (2*a)
        return f"x = {real:.4f} ± {imag:.4f}i"

def unit_convert(value, from_unit, to_unit):
    """Convert between units."""
    # Length
    length_units = {
        'm': 1, 'cm': 0.01, 'mm': 0.001, 'km': 1000,
        'ft': 0.3048, 'in': 0.0254, 'yd': 0.9144, 'mi': 1609.34
    }
    
    # Mass
    mass_units = {
        'kg': 1, 'g': 0.001, 'mg': 0.000001,
        'lb': 0.453592, 'oz': 0.0283495
    }
    
    # Time
    time_units = {
        's': 1, 'min': 60, 'hr': 3600, 'day': 86400
    }
    
    # Temperature
    def temp_convert(val, from_u, to_u):
        if from_u == to_u:
            return val
        # Convert to Celsius first
        if from_u == 'C':
            c = val
        elif from_u == 'F':
            c = (val - 32) * 5/9
        elif from_u == 'K':
            c = val - 273.15
        
        # Convert from Celsius
        if to_u == 'C':
            return c
        elif to_u == 'F':
            return c * 9/5 + 32
        elif to_u == 'K':
            return c + 273.15
    
    # Check which category
    if from_unit in length_units and to_unit in length_units:
        base = value * length_units[from_unit]
        return base / length_units[to_unit]
    elif from_unit in mass_units and to_unit in mass_units:
        base = value * mass_units[from_unit]
        return base / mass_units[to_unit]
    elif from_unit in time_units and to_unit in time_units:
        base = value * time_units[from_unit]
        return base / time_units[to_unit]
    elif from_unit in ['C', 'F', 'K'] and to_unit in ['C', 'F', 'K']:
        return temp_convert(value, from_unit, to_unit)
    else:
        return "Unknown units"

def base_convert(number, from_base, to_base):
    """Convert number between bases."""
    try:
        # Convert to decimal first
        decimal = int(number, from_base)
        
        # Convert to target base
        if to_base == 10:
            return str(decimal)
        elif to_base in [2, 8, 16]:
            if to_base == 16:
                return hex(decimal)[2:].upper()
            else:
                return format(decimal, f'0{to_base}b' if to_base == 2 else f'0{to_base}o')
        else:
            return "Unsupported base"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    calculate()
