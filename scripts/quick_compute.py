"""
Quick Computation Examples
Run these for instant results!
"""

import math
import sys

def run_example(num):
    """Run a computation example."""
    
    examples = {
        '1': ("Basic Math", "2**10 + 5*3"),
        '2': ("Square Root", "sqrt(144)"),
        '3': ("Trigonometry", "sin(30), cos(45), tan(60) in degrees"),
        '4': ("Logarithm", "log(100), ln(2.718)"),
        '5': ("Quadratic Solver", "x² + 5x + 6 = 0"),
        '6': ("Statistics", "[85, 90, 78, 92, 88] - mean, std"),
        '7': ("Derivative", "d/dx(x³ + 2x²) at x=2"),
        '8': ("Integral", "∫(x²)dx from 0 to 3"),
        '9': ("Matrix", "3×3 matrix determinant"),
        '10': ("Complex", "(3+4i) × (2-5i)"),
        '11': ("Units", "5 km to miles"),
        '12': ("Base Convert", "1010 (binary) to decimal"),
    }
    
    if num == 'all':
        for n, (name, desc) in examples.items():
            print(f"\n{n}. {name}")
            print(f"   {desc}")
        return
    
    if num not in examples:
        print("Available examples: 1-12 or 'all'")
        return
    
    name, desc = examples[num]
    print(f"\n{'='*50}")
    print(f"EXAMPLE {num}: {name}")
    print(f"{'='*50}")
    print(f"Task: {desc}\n")
    
    # Actually run the calculation
    if num == '1':
        result = 2**10 + 5*3
        print(f"2¹⁰ + 5×3 = {result}")
    elif num == '2':
        result = math.sqrt(144)
        print(f"√144 = {result}")
    elif num == '3':
        print(f"sin(30°) = {math.sin(math.radians(30)):.4f}")
        print(f"cos(45°) = {math.cos(math.radians(45)):.4f}")
        print(f"tan(60°) = {math.tan(math.radians(60)):.4f}")
    elif num == '4':
        print(f"log₁₀(100) = {math.log10(100):.4f}")
        print(f"ln(e) = {math.log(math.e):.4f}")
    elif num == '5':
        a, b, c = 1, 5, 6
        d = b**2 - 4*a*c
        x1 = (-b + d**0.5) / (2*a)
        x2 = (-b - d**0.5) / (2*a)
        print(f"x² + 5x + 6 = 0")
        print(f"x = {x1:.4f}, x = {x2:.4f}")
    elif num == '6':
        data = [85, 90, 78, 92, 88]
        print(f"Data: {data}")
        print(f"Mean = {sum(data)/len(data):.2f}")
        print(f"Std Dev = {statistics.stdev(data):.2f}")
    elif num == '7':
        # d/dx(x³ + 2x²) = 3x² + 4x
        x = 2
        result = 3*x**2 + 4*x
        print(f"d/dx(x³ + 2x²) at x=2 = {result}")
        print(f"(Using power rule: 3x² + 4x)")
    elif num == '8':
        # ∫x²dx from 0 to 3 = [x³/3]₀³ = 27/3 = 9
        print(f"∫₀³ x² dx = [x³/3]₀³ = 9")
    elif num == '9':
        A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        det = (1*(5*9-6*8) - 2*(4*9-6*7) + 3*(4*8-5*7))
        print(f"Matrix determinant:")
        print(f"| 1  2  3 |")
        print(f"| 4  5  6 | = {det}")
        print(f"| 7  8  9 |")
    elif num == '10':
        z1 = 3 + 4j
        z2 = 2 - 5j
        result = z1 * z2
        print(f"(3 + 4i) × (2 - 5i) = {result}")
    elif num == '11':
        km = 5
        miles = km * 0.621371
        print(f"{km} km = {miles:.2f} miles")
    elif num == '12':
        binary = "1010"
        decimal = int(binary, 2)
        print(f"1010₂ = {decimal}₁₀")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_example(sys.argv[1])
    else:
        print("="*60)
        print("STUDY COMPUTATION EXAMPLES")
        print("="*60)
        print()
        print("Usage: python quick_compute.py [number]")
        print()
        print("Examples:")
        run_example('all')
