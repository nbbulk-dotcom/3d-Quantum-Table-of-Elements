def render_gif(
    elements=None,              # List of dicts: {'label': str, 'coords': [V, D, E], 'color': str, 'size': int}
    out_file="spiral_field.gif",
    n_frames=192,               # ~8s at 24fps
    figsize=(8, 8),
    bg_color="#101020",
    torus_major=12,
    torus_minor=4
):
    """
    Render and animate a 3D spiraling quantum Codex field with toroidal overlay.
    - Elements are positioned in space and labeled.
    - Gold, Hydrogen, Oxygen, Uranium highlighted and color-coded.
    - Malefic resonance shown in red, beneficial in gold/blue/green.
    - Output is a GIF, suitable for use in Codex educator interface and curriculum deployment.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from PIL import Image

    # If no elements supplied, use Codex defaults
    if elements is None:
        elements = [
            {'label': 'Gold',      'coords': [10.2, 19.32, 9.22],  'color': '#FFD700', 'size': 150},
            {'label': 'Hydrogen',  'coords': [14.1, 0.0899, 13.6], 'color': '#00AEEF', 'size': 120},
            {'label': 'Uranium',   'coords': [12.0, 18.95, 6.51],  'color': '#FF2222', 'size': 130},
            {'label': 'Oxygen',    'coords': [16.4, 1.429, 13.6],  'color': '#26C485', 'size': 120}
        ]

    # Spiral coordinates for core animation
    n_points = 60
    theta = np.linspace(0, 6 * np.pi, n_points)
    volume = np.linspace(10, 18, n_points)
    density = np.linspace(0.1, 20, n_points)
    energy = np.linspace(5, 14, n_points)
    resonance = np.linspace(0, 1, n_points)
    phi_mod = 1.618

    # Helper: torus surface
    def torus(R, r, theta_count=60, phi_count=30):
        theta = np.linspace(0, 2*np.pi, theta_count)
        phi = np.linspace(0, 2*np.pi, phi_count)
        theta, phi = np.meshgrid(theta, phi)
        X = (R + r * np.cos(phi)) * np.cos(theta)
        Y = (R + r * np.cos(phi)) * np.sin(theta)
        Z = r * np.sin(phi)
        return X, Y, Z

    frames = []
    for i in range(n_frames):
        t = i / n_frames * 2 * np.pi

        # Spiral frame animation
        x = volume * np.cos(theta + t) + resonance * phi_mod
        y = density * np.sin(theta + t)
        z = energy + np.sin(theta + t)

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor(bg_color)
        fig.patch.set_facecolor(bg_color)
        ax.plot(x, y, z, color='#A6A6FF', linewidth=2, alpha=0.4)

        # Elements, labels, dynamic pulse
        for el in elements:
            ax.scatter(*el['coords'], color=el['color'], s=el['size'], edgecolor='black', zorder=10)
            ax.text(*(np.array(el['coords']) + [0.7, 0.7, 0.7]), el['label'],
                    color=el['color'], fontsize=20, fontweight='bold', zorder=11)

        # Torus field overlay
        torus_x, torus_y, torus_z = torus(torus_major, torus_minor)
        ax.plot_surface(torus_x, torus_y, torus_z, rstride=1, cstride=1, color='#326BFF', alpha=0.13, linewidth=0)
        ax.plot_wireframe(torus_x, torus_y, torus_z, color='#FFD700', alpha=0.11)

        ax.set_xlim(-20, 30)
        ax.set_ylim(-20, 30)
        ax.set_zlim(-5, 20)
        ax.set_axis_off()
        plt.tight_layout(pad=0)
        fig.canvas.draw()

        frame = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        frames.append(Image.fromarray(frame))
        plt.close(fig)

    frames[0].save(out_file, save_all=True, append_images=frames[1:], duration=42, loop=0)
    print(f"Quantum Codex spiral GIF saved to {out_file}")
