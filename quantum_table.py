import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# === φⁿ Harmonic Modulation ===
phi = 1.618
phi_mod = phi ** 7  # φ⁷ for sovereign resonance

# === Load Elemental Data ===
data = pd.read_csv('data/elements.csv')

# === Normalize and Encode Metadata ===
def normalize_column(col):
    return (col - col.min()) / (col.max() - col.min())

data['Volume_norm'] = normalize_column(data['Volume'])
data['Density_norm'] = normalize_column(data['Density'])
data['Energy_norm'] = normalize_column(data['Energy'])

# === Spatial Superposition Logic ===
def resonance_coordinates(row, phi_mod):
    # Dome-world curvature factor
    dome_factor = np.sin(np.pi * row['AtomicNumber'] / 118)

    # Harmonic spiral transformation
    x = row['Volume_norm'] * np.sin(phi_mod * dome_factor)
    y = row['Density_norm'] * np.cos(phi_mod / dome_factor)
    z = row['Energy_norm'] * np.sin(phi_mod / 2 + dome_factor)

    return x, y, z

# Apply transformation
data['x'], data['y'], data['z'] = zip(*data.apply(lambda row: resonance_coordinates(row, phi_mod), axis=1))

# === Visual Rendering ===
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Color coding by elemental family (optional)
families = data['Family'].unique()
colors = plt.cm.viridis(np.linspace(0, 1, len(families)))
family_color_map = dict(zip(families, colors))

for _, row in data.iterrows():
    ax.scatter(row['x'], row['y'], row['z'],
               color=family_color_map[row['Family']],
               s=80,
               label=row['Element'] if row['AtomicNumber'] % 10 == 0 else "",
               alpha=0.8)

# === Annotate Key Elements ===
for _, row in data.iterrows():
    if row['AtomicNumber'] in [1, 8, 79, 118]:  # H, O, Au, Og
        ax.text(row['x'], row['y'], row['z'],
                f"{row['Element']} ({row['AtomicNumber']})",
                fontsize=9, color='white')

# === Axis Labels and Title ===
ax.set_title('🌐 3D Quantum Table of Elements – φ⁷ Resonance in Dome-World Void', fontsize=14)
ax.set_xlabel('Spiral X (Volume × sin(φ⁷))')
ax.set_ylabel('Spiral Y (Density × cos(φ⁷))')
ax.set_zlabel('Spiral Z (Energy × sin(φ⁷/2))')

# === Legend and Grid ===
ax.grid(True)
plt.tight_layout()
plt.show()
