"""
Python Code Interpreter - FIXED VERSION
Execute Python code safely and return results
"""

import io
import sys
import traceback
import os
from datetime import datetime

class CodeInterpreter:
    """Execute Python code and capture output."""
    
    def __init__(self):
        self.output_dir = "generated_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def execute(self, code):
        """
        Execute Python code and return results.
        
        Args:
            code: Python code to execute
            
        Returns:
            dict with 'success', 'result', 'output', 'error'
        """
        # Import what we need
        import math
        import numpy as np
        
        # Create a namespace with common functions
        namespace = {
            '__name__': '__main__',
            '__builtins__': __builtins__,
            'math': math,
            'np': np,
            'datetime': datetime,
            
            # Basic operations
            'sqrt': lambda x: x**0.5 if x >= 0 else complex(0, (-x)**0.5),
            'abs': abs,
            'round': round,
            'sum': sum,
            'len': len,
            'min': min,
            'max': max,
            
            # Trig (degrees)
            'sin': lambda x: math.sin(math.radians(x)),
            'cos': lambda x: math.cos(math.radians(x)),
            'tan': lambda x: math.tan(math.radians(x)),
            'asin': lambda x: math.degrees(math.asin(x)),
            'acos': lambda x: math.degrees(math.acos(x)),
            'atan': lambda x: math.degrees(math.atan(x)),
            
            # Log/Exp
            'log': math.log10,
            'ln': math.log,
            'exp': math.exp,
            
            # Constants
            'pi': math.pi,
            'e': math.e,
            'c': 3e8,        # speed of light
            'g': 9.81,       # gravity
            'h': 6.626e-34,  # Planck's constant
            
            # Matrix operations
            'matmul': lambda A, B: np.dot(A, B).tolist(),
            'det': lambda A: round(np.linalg.det(np.array(A))),
            'transpose': lambda A: np.array(A).T.tolist(),
            'eigvals': lambda A: np.linalg.eigvals(np.array(A)).tolist(),
            'inv': lambda A: np.linalg.inv(np.array(A)).tolist(),
            
            # Calculus
            'derivative': lambda f, x, h=0.001: (f(x+h) - f(x-h))/(2*h),
            'integral': lambda f, a, b, n=1000: np.trapz([f(x) for x in np.linspace(a, b, n)], np.linspace(a, b, n)),
            
            # Statistics
            'mean': lambda x: np.mean(x),
            'std': lambda x: np.std(x),
            'median': lambda x: np.median(x),
            'variance': lambda x: np.var(x),
            
            # Physics
            'ke': lambda m, v: 0.5 * m * v**2,
            'pe': lambda m, h: m * 9.81 * h,
            'momentum': lambda m, v: m * v,
            'force': lambda m, a: m * a,
            'projectile_range': lambda v0, theta: (v0**2 * math.sin(2*math.radians(theta))) / 9.81,
            'projectile_time': lambda v0, theta: (2 * v0 * math.sin(math.radians(theta))) / 9.81,
            'wave_speed': lambda f, lam: f * lam,
            'frequency': lambda v, lam: v / lam,
        }
        
        # Capture stdout
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        result = None
        error = None
        output = ""
        error_output = ""
        
        try:
            # Execute with exec() for statements and eval() for expressions
            try:
                result = eval(code, namespace)
            except SyntaxError:
                # If eval fails, try exec
                exec(code, namespace)
                result = "Code executed successfully"
            
            output = sys.stdout.getvalue()
            error_output = sys.stderr.getvalue()
                
        except Exception as e:
            error = str(e)
            error_output = traceback.format_exc()
            output = sys.stdout.getvalue()
        
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        return {
            'success': error is None,
            'result': result,
            'output': output,
            'error': error,
            'error_trace': error_output if error else None
        }
    
    def execute_with_plot(self, code, filename="plot.png"):
        """
        Execute code and save any matplotlib plots.
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        
        namespace = {
            '__name__': '__main__',
            '__builtins__': __builtins__,
            'math': math,
            'np': np,
            'plt': plt,
            'savefig': lambda name: plt.savefig(os.path.join(self.output_dir, name), dpi=150, bbox_inches='tight'),
            'datetime': datetime,
        }
        
        # Add common functions
        namespace.update({
            'sin': lambda x: np.sin(np.radians(x)),
            'cos': lambda x: np.cos(np.radians(x)),
            'tan': lambda x: np.tan(np.radians(x)),
            'pi': np.pi,
            'linspace': lambda a, b, n: np.linspace(a, b, n),
            'arange': lambda a, b, s: np.arange(a, b, s),
        })
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        result = None
        error = None
        plot_path = None
        
        try:
            exec(code, namespace)
            output = sys.stdout.getvalue()
            error_output = sys.stderr.getvalue()
            
            # Check for plots
            if plt.get_fignums():
                plot_path = os.path.join(self.output_dir, filename)
                plt.savefig(plot_path, dpi=150, bbox_inches='tight')
            
        except Exception as e:
            error = str(e)
            output = sys.stdout.getvalue()
            error_output = traceback.format_exc()
        
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            plt.close('all')
        
        return {
            'success': error is None,
            'result': result,
            'output': output,
            'error': error,
            'plot_path': plot_path,
            'plot_generated': plot_path is not None
        }


# Quick function for instant results
def calc(expression):
    """Quick calculation: calc('2 + 2') → 4"""
    interpreter = CodeInterpreter()
    result = interpreter.execute(expression)
    return result['result']


if __name__ == "__main__":
    print("="*60)
    print("PYTHON CODE INTERPRETER")
    print("="*60)
    print()
    print("Usage:")
    print('  result = calc("2 + 2")  # Returns 4')
    print('  result = calc("sqrt(144)")  # Returns 12.0')
    print('  result = calc("det([[1,2],[3,4]])")  # Returns -2')
    print()
    print("Quick examples:")
    print(f"  2 + 2 = {calc('2 + 2')}")
    print(f"  sqrt(144) = {calc('sqrt(144)')}")
    print(f"  mean([1,2,3,4,5]) = {calc('mean([1,2,3,4,5])')}")
    print(f"  sin(30) = {calc('sin(30)')}")
    print(f"  pi = {calc('pi')}")
