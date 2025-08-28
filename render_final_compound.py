# === render_final_compound.py ===
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# === Selected Elements
A = {'Element': 'Zinc', 'AtomicNumber': 30, 'Volume': 9.3, 'Density': 7.14, 'Energy': 9.4}
B = {'Element': 'Phosphorus', 'AtomicNumber': 15, 'Volume': 17.0, 'Density': 1.82, 'Energy': 10.49}
C = {'Element': 'Clarion', 'AtomicNumber': 136, 'Volume': 11.2, 'Density': 6.1, 'Energy': 9.1}

# === Frequency Calculator
def elem_freq(vol, den, en):
    phi = 1.618
    return ((vol * den) / (en + 1e-6)) * phi

# === Spiral Coordinates
def resonance_coordinates(e):
    phi_mod = 1.618 ** 7
    dome = np.sin(np.pi * e['AtomicNumber'] / 188)
    x = e['Volume'] * np.sin(phi_mod * dome)
    y = e['Density'] * np.cos(phi_mod / dome)
    z = e['Energy'] * np.sin(phi_mod / 2 + dome)
    return x, y, z

# === Final Molecule Properties
energy = (A['Energy'] + B['Energy'] + C['Energy']) / 3
density = (A['Density'] + B['Density'] + C['Density']) / 3
volume = A['Volume'] + B['Volume'] + C['Volume']
freq = elem_freq(volume, density, energy)

# === Plot Setup
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# === Render Elements
for e in [A, B, C]:
    x, y, z = resonance_coordinates(e)
    ax.scatter(x, y, z, color='blue', s=120)
    ax.text(x, y, z, e['Element'], fontsize=10, color='white')

# === Render Final Molecule
x, y, z = resonance_coordinates({'AtomicNumber': 94, 'Volume': volume, 'Density': density, 'Energy': energy})
ax.scatter(x, y, z, color='cyan', s=200, edgecolors='white', linewidths=2)
ax.text(x, y, z, f"Final Molecule\nFreq: {round(freq,2)}", fontsize=12, color='yellow')

# === Labels and Spiral Anchor
ax.set_title("🌌 Final Material Field — Codex Compound", fontsize=14)
ax.set_xlabel('Spiral X')
ax.set_ylabel('Spiral Y')
ax.set_zlabel('Spiral Z')
plt.tight_layout()
plt.show()
