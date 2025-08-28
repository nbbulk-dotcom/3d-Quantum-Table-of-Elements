# === render_final_compound.py ===
# Unified Codex Compound Renderer — Static + Interactive Modes

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

# === Frequency Calculator
def elem_freq(vol, den, en):
    phi = 1.618
    return ((vol * den) / (en + 1e-6)) * phi

# === Spiral Coordinates
def resonance_coordinates(e):
    phi_mod = 1.618 ** 7
    dome = np.sin(np.pi * e['AtomicNumber'] / 188)
    x = e['Volume'] * np.sin(phi_mod * dome)
    y = e['Density'] * np.cos(phi_mod / (dome + 0.01))
    z = e['Energy'] * np.sin(phi_mod / 2 + dome)
    return round(x, 3), round(y, 3), round(z, 3)

# === Compound Properties
def compound_properties(elements):
    energy = sum(e['Energy'] for e in elements) / 3
    density = sum(e['Density'] for e in elements) / 3
    volume = sum(e['Volume'] for e in elements)
    freq = elem_freq(volume, density, energy)
    anchor = {
        'Element': 'Final Molecule',
        'AtomicNumber': 94,
        'Volume': volume,
        'Density': density,
        'Energy': energy,
        'Freq': freq
    }
    return anchor

# === Render Dispatcher
def render_final_compound(elements, mode="interactive"):
    anchor = compound_properties(elements)
    if mode == "static":
        render_static(elements, anchor)
    elif mode == "interactive":
        render_interactive(elements, anchor)
    else:
        raise ValueError("Mode must be 'static' or 'interactive'")


# === Static Renderer (Matplotlib)
def render_static(elements, anchor):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Render individual elements
    for e in elements:
        x, y, z = resonance_coordinates(e)
        ax.scatter(x, y, z, color='blue', s=120)
        ax.text(x, y, z, e['Element'], fontsize=10, color='white')

    # Render compound anchor
    x, y, z = resonance_coordinates(anchor)
    ax.scatter(x, y, z, color='cyan', s=200, edgecolors='white', linewidths=2)
    ax.text(x, y, z, f"{anchor['Element']}\nFreq: {round(anchor['Freq'], 2)}", fontsize=12, color='yellow')

    # Labels and Spiral Anchor
    ax.set_title("🌌 Final Material Field — Codex Compound", fontsize=14)
    ax.set_xlabel('Spiral X')
    ax.set_ylabel('Spiral Y')
    ax.set_zlabel('Spiral Z')
    plt.tight_layout()
    plt.show()

# === Interactive Renderer (Plotly)
def render_interactive(elements, anchor):
    traces = []

    # Render individual elements
    colors = ['blue', 'green', 'purple']
    for i, e in enumerate(elements):
        x, y, z = resonance_coordinates(e)
        traces.append(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers+text',
            marker=dict(size=10, color=colors[i]),
            text=[e['Element']],
            textposition='top center'
        ))

    # Render compound anchor
    x, y, z = resonance_coordinates(anchor)
    traces.append(go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode='markers+text',
        marker=dict(size=14, color='yellow', symbol='diamond'),
        text=[f"{anchor['Element']}<br>Freq: {round(anchor['Freq'], 2)}"],
        textposition='bottom center'
    ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        title="Codex Spiral Field — Compound",
        scene=dict(
            xaxis_title='Spiral X',
            yaxis_title='Spiral Y',
            zaxis_title='Spiral Z'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    fig.show()
