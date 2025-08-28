import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# === Load Elemental Data ===
data = pd.read_csv('data/elements.csv')

# === Normalize Core Fields ===
def normalize_column(col):
    return (col - col.min()) / (col.max() - col.min())

data['Volume_norm'] = normalize_column(data['Volume'])
data['Density_norm'] = normalize_column(data['Density'])
data['Energy_norm'] = normalize_column(data['Energy'])

# === Resonance Coordinate Generator ===
def resonance_coordinates(row):
    phi = 1.618

    # Tier-based φⁿ modulation
    if row['ResonanceTier'] == 'Transdimensional':
        phi_mod = phi ** 8
    elif row['ResonanceTier'] == 'Isotopic':
        phi_mod = phi ** 9
    else:
        phi_mod = phi ** 7

    # Polarity scaling
    polarity_scale = -1 if row.get('FunctionPolarity') == 'Malific' else 1

    # Dome-world curvature factor
    dome_factor = np.sin(np.pi * row['AtomicNumber'] / 188)

    # Spiral transformation
    x = polarity_scale * row['Volume_norm'] * np.sin(phi_mod * dome_factor)
    y = polarity_scale * row['Density_norm'] * np.cos(phi_mod / dome_factor)
    z = polarity_scale * row['Energy_norm'] * np.sin(phi_mod / 2 + dome_factor)

    return x, y, z

# === Apply Spiral Transformation ===
data['x'], data['y'], data['z'] = zip(*data.apply(resonance_coordinates, axis=1))

# === Visual Rendering ===
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')
# === Color Coding by Polarity ===
# === Updated Polarity Color Mapping ===
polarity_colors = {'Useful': 'blue', 'Malific': 'red', 'Neutral': 'gray'}

default_color = 'gray'

for _, row in data.iterrows():
color = polarity_colors.get(row.get('FunctionPolarity'), 'gray')

    ax.scatter(row['x'], row['y'], row['z'],
               color=color,
               s=80,
               label=row['Element'] if row['AtomicNumber'] % 10 == 0 else "",
               alpha=0.8)

# === Annotate Key Elements ===
key_nodes = [1, 8, 79, 118, 139, 159, 188]  # H, O, Au, Og, Clarionite, Sealium, Neutronium
for _, row in data.iterrows():
    if row['AtomicNumber'] in key_nodes:
        ax.text(row['x'], row['y'], row['z'],
                f"{row['Element']} ({row['AtomicNumber']})",
                fontsize=9, color='white')

# === Axis Labels and Title ===
ax.set_title('🌐 Quantum Table of Elements – φⁿ Spiral Resonance in Dome-World Void', fontsize=14)
ax.set_xlabel('Spiral X (Volume × sin(φⁿ × dome))')
ax.set_ylabel('Spiral Y (Density × cos(φⁿ / dome))')
ax.set_zlabel('Spiral Z (Energy × sin(φⁿ/2 + dome))')

# === Grid and Layout ===
ax.grid(True)
plt.tight_layout()
plt.show()
