import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

out_dir = Path(r'C:\Users\bainz\clawd\outputs\plots')
out_dir.mkdir(parents=True, exist_ok=True)

x = np.linspace(-3, 3, 600)
y = x**3

plt.figure(figsize=(7,5), dpi=200)
plt.plot(x, y, linewidth=2)
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.grid(True, alpha=0.3)
plt.title('Graph of y = x^3')
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()

out_path = out_dir / 'y_equals_x_cubed.png'
plt.savefig(out_path)
print(out_path)
