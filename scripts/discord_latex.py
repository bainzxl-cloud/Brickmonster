"""
Discord LaTeX Renderer
Renders LaTeX math to PNG images for Discord display

Usage:
    # Single equation
    python discord_latex.py "Your LaTeX here" output.png
    
    # Multiple lines
    python discord_latex.py "line1" "line2" "line3" output.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mathtext as mathtext
import sys
import os
import textwrap

def render_latex(latex_code, output_path, fontsize=24, dpi=150, dark_mode=False):
    """Render single LaTeX expression to PNG."""
    
    # Clean up
    latex = latex_code.strip()
    if latex.startswith('$') and latex.endswith('$'):
        latex = latex[1:-1]
    
    # Create figure
    fig = plt.figure(figsize=(10, 2), dpi=dpi, facecolor='none')
    ax = fig.add_subplot(111)
    ax.set_facecolor('none')
    
    text_color = 'white' if dark_mode else 'black'
    
    try:
        # Render
        ax.text(0.5, 0.5, f"${latex}$", fontsize=fontsize,
                ha='center', va='center', transform=ax.transAxes,
                color=text_color)
        
        ax.axis('off')
        
        # Save
        fig.savefig(output_path, dpi=dpi, transparent=True,
                   bbox_inches='tight', pad_inches=0.5)
        plt.close()
        
        return True, output_path
        
    except Exception as e:
        plt.close()
        return False, str(e)


def render_multiline(latex_lines, output_path, fontsize=20, dpi=150, dark_mode=False):
    """Render multiple LaTeX lines to a single PNG."""
    
    if not latex_lines:
        return False, "No content to render"
    
    # Clean each line
    cleaned_lines = []
    for line in latex_lines:
        line = line.strip()
        if line.startswith('$') and line.endswith('$'):
            line = line[1:-1]
        if line:
            cleaned_lines.append(line)
    
    if not cleaned_lines:
        return False, "No valid content after cleaning"
    
    # Figure dimensions
    height_per_line = 1.0
    width = 12
    height = len(cleaned_lines) * height_per_line + 1
    
    fig = plt.figure(figsize=(width, height), dpi=dpi, facecolor='none')
    ax = fig.add_subplot(111)
    ax.set_facecolor('none')
    
    text_color = 'white' if dark_mode else 'black'
    
    # Render each line
    for i, line in enumerate(cleaned_lines):
        y_pos = 1 - (i + 0.5) * (height_per_line / height)
        ax.text(0.5, y_pos, f"${line}$", fontsize=fontsize,
                ha='center', va='center', transform=ax.transAxes,
                color=text_color)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    fig.savefig(output_path, dpi=dpi, transparent=True,
               bbox_inches='tight', pad_inches=1)
    plt.close()
    
    return True, output_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n" + "="*50)
        print("EXAMPLES:")
        print("="*50)
        print('# Single equation:')
        print('python discord_latex.py "\\int_a^b f(x) dx" integral.png')
        print()
        print('# Multiple lines (last arg is output):')
        print('python discord_latex.py "f(x) = x^2" "g(x) = 2x" "h(x) = f(x) + g(x)" combined.png')
        print()
        print('# From file:')
        print('python discord_latex.py --file equations.txt output.png')
        sys.exit(1)
    
    # Check for file input
    if sys.argv[1] == '--file':
        if len(sys.argv) < 4:
            print("Error: --file requires input file and output path")
            sys.exit(1)
        
        with open(sys.argv[2], 'r') as f:
            lines = f.readlines()
        output = sys.argv[3]
        
        success, result = render_multiline(lines, output)
        
    elif len(sys.argv) == 2:
        # Single line, default output
        output = "latex_output.png"
        success, result = render_latex(sys.argv[1], output)
        
    elif len(sys.argv) == 3:
        # Single line, custom output
        success, result = render_latex(sys.argv[1], sys.argv[2])
        
    else:
        # Multiple lines (last arg is output)
        output = sys.argv[-1]
        latex_lines = sys.argv[1:-1]
        success, result = render_multiline(latex_lines, output)
    
    if success:
        print(f"SUCCESS: {result}")
        print(f"File size: {os.path.getsize(result)} bytes")
    else:
        print(f"ERROR: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
