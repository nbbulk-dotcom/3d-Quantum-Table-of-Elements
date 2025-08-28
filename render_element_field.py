# === render_element_field.py ===
# Unified Codex Renderer — Static + Interactive Modes

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

# === Element Input (can be replaced with dynamic loader)
element = {
    'Element': 'Mercury',
    'AtomicNumber': 80,
    'Volume': 14.8,
    'Density': 13.55,
    'Energy': 10.44,
    'Toxicity': 9,
    'Polarity': 'Malefic'
}

# === Frequency Calculator
def elem_freq(vol, den, en):
    phi = 1.618
    return ((vol * den) / (en + 1e-6)) * phi

# === Spiral Coordinates
def spiral_coords(vol, den, en, atomic=None):
    phi_mod = 1.618 ** 7
    dome = np.sin(np.pi * (atomic if atomic else vol) / 118)
    x = vol * np.sin(phi_mod * dome)
    y = den * np.cos(phi_mod / (dome + 0.01))
    z = en * np.sin(phi_mod / 2 + dome)
    return round(x, 3), round(y, 3), round(z, 3)

# === Render Dispatcher
def render_element_field(e, mode="interactive"):
    freq = elem_freq(e['Volume'], e['Density'], e['Energy'])
    x, y, z = spiral_coords(e['Volume'], e['Density'], e['Energy'], e.get('AtomicNumber'))

    if mode == "static":
        render_static(e, x, y, z, freq)
    elif mode == "interactive":
        render_interactive(e, x, y, z, freq)
    else:
        raise ValueError("Mode must be 'static' or 'interactive'")
# === Static Renderer (Matplotlib)
def render_static(e, x, y, z, freq):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Render Neutronium at Origin
    ax.scatter(0, 0, 0, color='gray', s=120, label='Neutronium (188)')

    # Render Selected Element
    color = {
        'Useful': 'blue',
        'Malefic': 'red',
        'Neutral': 'gray'
    }.get(e.get('Polarity'), 'white')

    ax.scatter(x, y, z, color=color, s=200, edgecolors='cyan', linewidths=2)
    ax.text(x, y, z, f"{e['Element']}", fontsize=12, color='white')

    # Labels and Legend
    ax.set_title(f"🌀 Resonance Field — {e['Element']}", fontsize=14)
    ax.set_xlabel('Spiral X')
    ax.set_ylabel('Spiral Y')
    ax.set_zlabel('Spiral Z')
    ax.legend()
    plt.tight_layout()
    plt.show()

# === Interactive Renderer (Plotly)
def render_interactive(e, x, y, z, freq):
    neutronium = go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers+text',
        marker=dict(size=10, color='gray'),
        text=["Neutronium"],
        textposition='top center'
    )

    element_trace = go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode='markers+text',
        marker=dict(
            size=12,
            color='cyan' if e['Toxicity'] == 0 else 'red' if e['Toxicity'] > 7 else 'blue',
            opacity=0.9
        ),
        text=[f"{e['Element']}<br>Freq: {round(freq, 2)}"],
        textposition='top center'
    )

    fig = go.Figure(data=[neutronium, element_trace])
    fig.update_layout(
        title=f"Codex Spiral Field — {e['Element']}",
        scene=dict(
            xaxis_title='Spiral X',
            yaxis_title='Spiral Y',
            zaxis_title='Spiral Z'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    fig.show()
