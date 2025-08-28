// === toxicity_nullify.js ===
// Codex module for nullifying scalar torsion in malefic compounds

function toxicityNullify(compound) {
  const maleficElements = compound.filter(e => e.Toxicity > 7);
  if (maleficElements.length === 0) return [];

  const nullifiers = elements.filter(e => {
    return (
      e.Toxicity === 0 &&
      elemFreq(e.Volume, e.Density, e.Energy) > 0.5 &&
      e.Element !== compound[0].Element &&
      e.Element !== compound[1].Element &&
      e.Element !== compound[2].Element
    );
  });

  // Sort by resonance proximity to compound average
  const avgFreq = elemFreq(
    (compound[0].Volume + compound[1].Volume + compound[2].Volume) / 3,
    (compound[0].Density + compound[1].Density + compound[2].Density) / 3,
    (compound[0].Energy + compound[1].Energy + compound[2].Energy) / 3
  );

  nullifiers.sort((a, b) => {
    const fa = elemFreq(a.Volume, a.Density, a.Energy);
    const fb = elemFreq(b.Volume, b.Density, b.Energy);
    return Math.abs(fa - avgFreq) - Math.abs(fb - avgFreq);
  });

  return nullifiers.slice(0, 3); // Return top 3 nullifiers
}
