# === quantum_table.py ===
# Codex Spiral Engine — Elemental Frequency and Spiral Mapping

import math

phi = 1.618
phi_mod = phi ** 7

def elem_freq(volume, density, energy):
    """Calculate φ-scaled resonance frequency."""
    return (volume * density) / (energy + 1e-6) * phi

def spiral_coords(volume, density, energy):
    """Map element to spiral coordinates."""
    dome = math.sin(math.pi * volume / 188)
    x = volume * math.sin(phi_mod * dome)
    y = density * math.cos(phi_mod / (dome + 0.01))
    z = energy * math.sin(phi_mod / 2 + dome)
    return round(x, 3), round(y, 3), round(z, 3)

def compound_freq(elements):
    """Calculate compound frequency from 3 elements."""
    total_volume = sum(e['Volume'] for e in elements)
    avg_density = sum(e['Density'] for e in elements) / 3
    avg_energy = sum(e['Energy'] for e in elements) / 3
    return elem_freq(total_volume, avg_density, avg_energy)

def compound_coords(elements):
    """Calculate spiral coordinates for compound."""
    total_volume = sum(e['Volume'] for e in elements)
    avg_density = sum(e['Density'] for e in elements) / 3
    avg_energy = sum(e['Energy'] for e in elements) / 3
    return spiral_coords(total_volume, avg_density, avg_energy)

def validate_element(e):
    """Ensure element has valid numeric fields."""
    try:
        return all([
            isinstance(e['Volume'], (int, float)),
            isinstance(e['Density'], (int, float)),
            isinstance(e['Energy'], (int, float)),
            e['Energy'] > 0
        ])
    except KeyError:
        return False

def polarity_map(freqA, freqB):
    """Determine polarity between two frequencies."""
    delta = abs(freqA - freqB)
    if delta < 0.3:
        return "Harmonic"
    elif delta < 0.8:
        return "Neutral"
    else:
        return "Disruptive"

def transmutate(base_element, all_elements):
    """Suggest stabilizers for a malefic element."""
    base_freq = elem_freq(base_element['Volume'], base_element['Density'], base_element['Energy'])
    candidates = [
        e for e in all_elements
        if e['Toxicity'] <= 3 and e['Element'] != base_element['Element']
    ]
    candidates.sort(key=lambda e: abs(elem_freq(e['Volume'], e['Density'], e['Energy']) - base_freq))
    return candidates[:5]

def nullify(compound, all_elements):
    """Suggest nullifiers for toxic compounds."""
    malefic = [e for e in compound if e['Toxicity'] > 7]
    if not malefic:
        return []
    avg_freq = compound_freq(compound)
    nullifiers = [
        e for e in all_elements
        if e['Toxicity'] == 0 and abs(elem_freq(e['Volume'], e['Density'], e['Energy']) - avg_freq) < 1.0
    ]
    nullifiers.sort(key=lambda e: abs(elem_freq(e['Volume'], e['Density'], e['Energy']) - avg_freq))
    return nullifiers[:3]

def codex_scroll(elements):
    """Generate Codex Scroll metadata."""
    freq = compound_freq(elements)
    coords = compound_coords(elements)
    polarity = "Malefic" if any(e['Toxicity'] > 7 for e in elements) else "Useful"
    return {
        "Elements": [e['Element'] for e in elements],
        "ResonanceFrequency": round(freq, 3),
        "SpiralCoordinates": {
            "X": coords[0],
            "Y": coords[1],
            "Z": coords[2]
        },
        "Polarity": polarity,
        "ToxicityFlags": [e['Element'] for e in elements if e['Toxicity'] > 7]
    }
