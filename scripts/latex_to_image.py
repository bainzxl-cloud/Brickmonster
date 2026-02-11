"""
LaTeX to Image Renderer
Converts LaTeX math expressions to PNG images for Discord display

Usage:
    python latex_to_image.py "Your LaTeX here" output.png
    python latex_to_image.py "$\int_a^b f(x) dx$" integral.png
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.mathtext as mathtext
import sys
import os

def latex_to_image(latex_code, output_path, fontsize=20, dpi=150):
    """
    Convert LaTeX math expression to PNG image.
    
    Args:
        latex_code: LaTeX expression (with or without $...$)
        output_path: Path to save PNG
        fontsize: Font size (default: 20)
        dpi: Image resolution (default: 150)
    """
    
    # Clean up latex code
    latex = latex_code.strip()
    
    # Remove outer $...$ if present
    if latex.startswith('$') and latex.endswith('$'):
        latex = latex[1:-1]
    
    # Create figure with transparent background
    fig = plt.figure(figsize=(8, 2), dpi=dpi)
    ax = fig.add_subplot(111)
    
    # Set transparent background
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    
    # Render math text
    try:
        text = ax.text(
            0.5, 0.5, 
            f"${latex}$",
            fontsize=fontsize,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            color='white' if 'dark' in output_path.lower() else 'black'
        )
        
        # Adjust figure size to fit content
        fig.canvas.draw()
        bbox = text.get_window_extent(renderer=fig.canvas.get_renderer())
        
        # Convert to figure coordinates
        bbox_inches = bbox.transformed(fig.dpi_scale_trans.inverted())
        
        # Add some padding
        pad = 0.1
        fig.set_size_inches(
            bbox_inches.width + pad,
            bbox_inches.height + pad
        )
        
        # Re-render with correct size
        ax.set_position([0.5 - bbox_inches.width/2, 0.5 - bbox_inches.height/2, bbox_inches.width, bbox_inches.height])
        fig.canvas.draw()
        
        # Save
        fig.savefig(output_path, dpi=dpi, transparent=True, bbox_inches='tight', pad_inches=0.2)
        plt.close(fig)
        
        return True, f"Image saved: {output_path}"
        
    except Exception as e:
        plt.close(fig)
        return False, f"Error: {str(e)}"


def render_multiline(latex_lines, output_path, fontsize=18, dpi=150):
    """Render multiple lines of LaTeX."""
    
    fig = plt.figure(figsize=(10, len(latex_lines) * 0.8), dpi=dpi)
    ax = fig.add_subplot(111)
    
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    
    y_positions = [0.9 - (i * 0.25) for i in range(len(latex_lines))]
    
    for i, line in enumerate(latex_lines):
        line = line.strip()
        if line.startswith('$') and line.endswith('$'):
            line = line[1:-1]
            
        ax.text(
            0.05, y_positions[i],
            f"${line}$",
            fontsize=fontsize,
            color='white' if 'dark' in output_path.lower() else 'black',
            transform=ax.transAxes,
            verticalalignment='center'
        )
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    fig.savefig(output_path, dpi=dpi, transparent=True, bbox_inches='tight', pad_inches=0.5)
    plt.close(fig)
    
    return True, f"Multiline image saved: {output_path}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExamples:")
        print('  python latex_to_image.py "\\int_a^b f(x) dx" integral.png')
        print('  python latex_to_image.py "\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}" quadratic.png')
        sys.exit(1)
    
    latex_code = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "latex_output.png"
    
    success, message = latex_to_image(latex_code, output_path)
    print(message)
