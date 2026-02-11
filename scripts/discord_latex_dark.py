"""
Discord LaTeX Renderer - DARK MODE
Renders LaTeX math to PNG with dark background and white text

Usage:
    python discord_latex_dark.py "Your LaTeX here" output.png
    python discord_latex_dark.py "line1" "line2" "line3" output.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mathtext as mathtext
import sys
import os
import textwrap

def render_latex(latex_code, output_path, fontsize=20, dpi=150):
    """Render single LaTeX expression to PNG with dark background."""
    
    # Clean up
    latex = latex_code.strip()
    if latex.startswith('$') and latex.endswith('$'):
        latex = latex[1:-1]
    
    # Create figure with DARK background
    fig = plt.figure(figsize=(10, 2.5), dpi=dpi, facecolor='#1a1a2e')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#1a1a2e')
    
    try:
        # Render with WHITE text
        ax.text(0.5, 0.5, f"${latex}$", fontsize=fontsize,
                ha='center', va='center', transform=ax.transAxes,
                color='white', family='serif')
        
        ax.axis('off')
        
        # Save
        fig.savefig(output_path, dpi=dpi, facecolor='#1a1a2e',
                   bbox_inches='tight', pad_inches=1)
        plt.close()
        
        return True, output_path
        
    except Exception as e:
        plt.close()
        return False, str(e)


def render_multiline(latex_lines, output_path, fontsize=18, dpi=150):
    """Render multiple LaTeX lines to a single PNG with dark background."""
    
    if not latex_lines:
        return False, "No content to render"
    
    # Clean each line - KEEP EVERYTHING
    cleaned_lines = []
    for line in latex_lines:
        line = line.strip()
        # Remove $...$ wrapper if present
        if line.startswith('$') and line.endswith('$'):
            line = line[1:-1]
        if line:
            cleaned_lines.append(line)
    
    if not cleaned_lines:
        return False, "No valid content after cleaning"
    
    # Figure dimensions - taller for full equations
    height_per_line = 1.5  # More space!
    width = 14  # Wider!
    height = len(cleaned_lines) * height_per_line + 1.5
    
    fig = plt.figure(figsize=(width, height), dpi=dpi, facecolor='#1a1a2e')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#1a1a2e')
    
    # Render each line - WHITE TEXT
    for i, line in enumerate(cleaned_lines):
        y_pos = 1 - (i + 0.7) * (height_per_line / height)
        ax.text(0.02, y_pos, f"${line}$", fontsize=fontsize,
                ha='left', va='center', transform=ax.transAxes,
                color='white', family='serif')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    fig.savefig(output_path, dpi=dpi, facecolor='#1a1a2e',
               bbox_inches='tight', pad_inches=1)
    plt.close()
    
    return True, output_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n" + "="*60)
        print("DARK MODE LATEX RENDERER")
        print("="*60)
        print('\nUsage:')
        print('  python discord_latex_dark.py "\\int_a^b f(x) dx" output.png')
        print('  python discord_latex_dark.py "f(x) = x^2" "g(x) = 2x" combined.png')
        print()
        print('Features:')
        print('  - Dark background (#1a1a2e)')
        print('  - White text')
        print('  - Large font for readability')
        print('  - Full equations preserved!')
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
        output = "latex_dark.png"
        success, result = render_latex(sys.argv[1], output)
        
    elif len(sys.argv) == 3:
        success, result = render_latex(sys.argv[1], sys.argv[2])
        
    else:
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
