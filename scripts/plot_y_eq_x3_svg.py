from pathlib import Path

W, H = 1200, 800
margin = 80

# Plot range
xmin, xmax = -3.0, 3.0
ymin, ymax = -27.0, 27.0

# Helpers

def sx(x):
    return margin + (x - xmin) * (W - 2*margin) / (xmax - xmin)

def sy(y):
    return H - margin - (y - ymin) * (H - 2*margin) / (ymax - ymin)

# Build path for y=x^3
pts = []
steps = 800
for i in range(steps + 1):
    x = xmin + (xmax - xmin) * i / steps
    y = x**3
    pts.append((sx(x), sy(y)))

d = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts)

# Axes
x0 = sx(0)
y0 = sy(0)

# Ticks
xticks = [-3,-2,-1,0,1,2,3]
yticks = [-20,-10,0,10,20]

tick_elems = []
for t in xticks:
    x = sx(t)
    tick_elems.append(f'<line x1="{x:.2f}" y1="{y0-6:.2f}" x2="{x:.2f}" y2="{y0+6:.2f}" stroke="#222" stroke-width="2"/>')
    tick_elems.append(f'<text x="{x:.2f}" y="{y0+28:.2f}" font-size="22" text-anchor="middle" fill="#111">{t}</text>')
for t in yticks:
    y = sy(t)
    tick_elems.append(f'<line x1="{x0-6:.2f}" y1="{y:.2f}" x2="{x0+6:.2f}" y2="{y:.2f}" stroke="#222" stroke-width="2"/>')
    if t != 0:
        tick_elems.append(f'<text x="{x0-18:.2f}" y="{y+8:.2f}" font-size="22" text-anchor="end" fill="#111">{t}</text>')

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>

  <!-- grid -->
  <g opacity="0.25">
    {''.join(f'<line x1="{sx(t):.2f}" y1="{margin}" x2="{sx(t):.2f}" y2="{H-margin}" stroke="#999" stroke-width="1"/>' for t in xticks)}
    {''.join(f'<line x1="{margin}" y1="{sy(t):.2f}" x2="{W-margin}" y2="{sy(t):.2f}" stroke="#999" stroke-width="1"/>' for t in yticks)}
  </g>

  <!-- axes -->
  <line x1="{margin}" y1="{y0:.2f}" x2="{W-margin}" y2="{y0:.2f}" stroke="#111" stroke-width="3"/>
  <line x1="{x0:.2f}" y1="{margin}" x2="{x0:.2f}" y2="{H-margin}" stroke="#111" stroke-width="3"/>

  <!-- ticks/labels -->
  <g>
    {''.join(tick_elems)}
  </g>

  <!-- curve -->
  <path d="{d}" fill="none" stroke="#1f4fff" stroke-width="5"/>

  <!-- title -->
  <text x="{W/2:.2f}" y="42" font-size="30" text-anchor="middle" fill="#111">Graph of y = x^3</text>
</svg>
'''

out_dir = Path(r'C:\Users\bainz\clawd\outputs\plots')
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / 'y_equals_x_cubed.svg'
out_path.write_text(svg, encoding='utf-8')
print(out_path)
