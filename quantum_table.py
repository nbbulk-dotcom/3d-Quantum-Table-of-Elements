import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# === Load Codex Registry ===
data = pd.read_csv('data/elements_codex.csv')

# === Normalize Core Fields ===
def normalize_column(col):
    return (col - col.min()) / (col.max() - col.min())

data['Volume_norm'] = normalize_column(data['Volume'])
data['Density_norm'] = normalize_column(data['Density'])
data['Energy_norm'] = normalize_column(data['Energy'])

# === Resonance Coordinate Generator ===
def resonance_coordinates(row):
    phi = 1.618
    tier = row.get('ResonanceTier', 'Core')
    phi_mod = phi ** {'Core': 7, 'Transdimensional': 8, 'Isotopic': 9, 'Archetypal': 9, 'Boundary': 9}.get(tier, 7)
    polarity_scale = {'Useful': 1, 'Malific': -1, 'Neutral': 0}.get(row.get('FunctionPolarity', 'Neutral'), 0)
    dome_factor = np.sin(np.pi * row['AtomicNumber'] / 188)
    x = polarity_scale * row['Volume_norm'] * np.sin(phi_mod * dome_factor)
    y = polarity_scale * row['Density_norm'] * np.cos(phi_mod / dome_factor)
    z = polarity_scale * row['Energy_norm'] * np.sin(phi_mod / 2 + dome_factor)
    return x, y, z

# === Apply Spiral Transformation ===
data['x'], data['y'], data['z'] = zip(*data.apply(resonance_coordinates, axis=1))

# === Polarity Color Mapping ===
polarity_colors = {'Useful': 'blue', 'Malific': 'red', 'Neutral': 'gray'}

# === Spiral Plot ===
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

for _, row in data.iterrows():
    color = polarity_colors.get(row.get('FunctionPolarity'), 'gray')
    ax.scatter(row['x'], row['y'], row['z'], color=color, s=80, alpha=0.8)

# === Annotate Neutronium ===
neutronium = data[data['AtomicNumber'] == 188]
if not neutronium.empty:
    x, y, z = neutronium.iloc[0][['x', 'y', 'z']]
    ax.text(x, y, z, "Neutronium (188)", fontsize=10, color='white')

# === Transmutation Function ===
def elem_freq(vol, den, en):
    return round((vol * den) / (en + 1e-6), 2)

def transmutate():
    pairs = [
        ('Obscurium', 'Clarion'),
        ('Severon', 'Bindra'),
        ('Collapseon', 'Vaulton'),
        ('Oblivium', 'Neutronium'),
        ('Fracturonite', 'Loopion'),
        ('Disruptium', 'Resonex'),
        ('Arsenic', 'Phosphorus'),
        ('Mercury', 'Zinc'),
        ('Lead', 'Calcium'),
        ('Polonium', 'Selenium'),
        ('Thallium', 'Magnesium'),
        ('Radon', 'Argon'),
        ('Technetium', 'Molybdenum'),
        ('Astatine', 'Iodine')
    ]
    for malefic, partner in pairs:
        m = data[data['Element'] == malefic].iloc[0]
        p = data[data['Element'] == partner].iloc[0]
        mf = elem_freq(m['Volume'], m['Density'], m['Energy'])
        pf = elem_freq(p['Volume'], p['Density'], p['Energy'])
        ax.plot([m['x'], p['x']], [m['y'], p['y']], [m['z'], p['z']], color='lightblue', linewidth=2, alpha=0.6)
        print(f"{malefic} → {partner} | ΔFreq = {abs(mf - pf)}")

# === Coupling Graph Function ===
def coupling_graph():
    for _, row in data.iterrows():
        glyph = row.get('FunctionName', '')[:3]
        ax.text(row['x'], row['y'], row['z'], glyph, fontsize=8, color='white', alpha=0.6)

# === Execute Enhancements ===
transmutate()
coupling_graph()

# === Axis Labels and Title ===
ax.set_title('🌀 Quantum Table of Elements — Codex Spiral with Transmutation & Glyphs', fontsize=14)
ax.set_xlabel('Spiral X')
ax.set_ylabel('Spiral Y')
ax.set_zlabel('Spiral Z')
ax.grid(True)
plt.tight_layout()
plt.show()
