# === render_element_field.py ===
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# === Element Data (Example: Mercury)
element = {
    'Element': 'Mercury',
    'AtomicNumber': 80,
    'Volume': 14.8,
    'Density': 13.55,
    'Energy': 10.44,
    'Polarity': 'Malefic'
}

# === Frequency Calculator
def elem_freq(vol, den, en):
    phi = 1.618
    return ((vol * den) / (en + 1e-6)) * phi

# === Spiral Coordinates
def resonance_coordinates(e):
    phi_mod = 1.618 ** 7
    dome = np.sin(np.pi * e['AtomicNumber'] / 118)
    x = e['Volume'] * np.sin(phi_mod * dome)
    y = e['Density'] * np.cos(phi_mod / dome)
    z = e['Energy'] * np.sin(phi_mod / 2 + dome)
    return x, y, z

# === Plot Setup
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# === Render Neutronium at Origin
ax.scatter(0, 0, 0, color='gray', s=120, label='Neutronium (188)')

# === Render Selected Element
x, y, z = resonance_coordinates(element)
color = {'Useful': 'blue', 'Malefic': 'red', 'Neutral': 'gray'}.get(element['Polarity'], 'white')
ax.scatter(x, y, z, color=color, s=200, edgecolors='cyan', linewidths=2)
ax.text(x, y, z, f"{element['Element']}", fontsize=12, color='white')

# === Labels and Legend
ax.set_title(f"🌀 Resonance Field — {element['Element']}", fontsize=14)
ax.set_xlabel('Spiral X')
ax.set_ylabel('Spiral Y')
ax.set_zlabel('Spiral Z')
ax.legend()
plt.tight_layout()
plt.show()
