# === codex_scroll_export.py ===
# Codex module for exporting compound synthesis to ceremonial scroll

import datetime
import json

def elem_freq(vol, den, en):
    phi = 1.618
    return ((vol * den) / (en + 1e-6)) * phi

def spiral_coords(vol, den, en):
    phi_mod = 1.618 ** 7
    dome = abs(vol / 188)
    x = vol * (phi_mod * dome)
    y = den * (phi_mod / (dome + 0.01))
    z = en * (phi_mod / 2 + dome)
    return round(x, 2), round(y, 2), round(z, 2)

def export_codex_scroll(elements):
    compound_id = f"Codex-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    avg_energy = sum(e['Energy'] for e in elements) / 3
    avg_density = sum(e['Density'] for e in elements) / 3
    total_volume = sum(e['Volume'] for e in elements)
    freq = elem_freq(total_volume, avg_density, avg_energy)
    x, y, z = spiral_coords(total_volume, avg_density, avg_energy)

    scroll = {
        "CompoundID": compound_id,
        "TimestampUTC": datetime.datetime.utcnow().isoformat(),
        "Elements": [e['Element'] for e in elements],
        "ResonanceFrequency": round(freq, 3),
        "SpiralCoordinates": {"X": x, "Y": y, "Z": z},
        "Polarity": "Malefic" if any(e['Toxicity'] > 7 for e in elements) else "Useful",
        "ToxicityFlags": [e['Element'] for e in elements if e['Toxicity'] > 7]
    }

    with open(f"{compound_id}.json", "w") as f:
        json.dump(scroll, f, indent=2)

    return scroll
