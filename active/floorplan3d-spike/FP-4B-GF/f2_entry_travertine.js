/* f2_entry_travertine.js - F2 fix (Q4 critic): entry travertine wall without the radial streak artifact.
 * Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
 *
 * Problem (Q4, verify/gf_polish_2026-11-09/after_entry_void.png): index.html texTravertine() paints ~90 full-width,
 * high-contrast horizontal bands 4-30 px tall in a 1024x512 canvas (= 1.2 x 0.6 m slab). On the 6 m entry wall seen
 * obliquely, those thin full-width stripes converge in perspective and alias into "radial stretched streaks".
 *
 * Fix (appearance only, no geometry change): a separate procedural texture used ONLY on the entry west wall clad
 * (plan x 6040, y 16113-19169) and its double-height void lining. Dining wall travertine (Q4 PASS) is unchanged.
 *   - base tone from the p17 materials board "Travertine Stone Feature Material" swatch (warm light beige)  [source: brochure p17 image; tone read by eye = assumption]
 *   - broad, soft, LOW-contrast mottling (blurred, partial-width lenses), no full-width stripes            [assumption: display]
 *   - few short faint veins (alpha <= .10), small pits                                                      [assumption: display]
 *   - visible slab joints 1.2 x 0.6 m, stretcher bond (half-slab offset every other course)                 [slab size: same DA as index.html texTravertine; bond = assumption]
 * The canvas holds 2 x 2 slabs (2.4 x 1.2 m), so the caller's repeat is 2.4 x 1.2 m.
 * Free / procedural only: no downloaded assets.
 */
export const ENTRY_TRAV_REPEAT_M = [2.4, 1.2];
function rng(seed){ let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
export function texEntryTravertine(THREE, anisotropy = 8, seed = 113){
  const W = 2048, H = 1024, c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d'), R = rng(seed);
  const sw = W/2, sh = H/2;   // one slab = 1024 x 512 px = 1.2 x 0.6 m
  for (let row = 0; row < 2; row++){
    const off = row ? sw/2 : 0;
    for (let k = -1; k < 2; k++){
      const x0 = k*sw + off, y0 = row*sh, d = (R() - .5)*10;
      g.save(); g.beginPath(); g.rect(x0, y0, sw, sh); g.clip();
      g.fillStyle = `rgb(${206 + d|0},${192 + d|0},${168 + d*1.1|0})`; g.fillRect(x0, y0, sw, sh);
      g.filter = 'blur(10px)';
      for (let i = 0; i < 26; i++){ const cx = x0 + R()*sw, cy = y0 + R()*sh, rx = 60 + R()*240, ry = 6 + R()*22, lt = R() < .5;
        g.fillStyle = lt ? `rgba(236,226,206,${.10 + R()*.12})` : `rgba(168,148,118,${.05 + R()*.08})`;
        g.beginPath(); g.ellipse(cx, cy, rx, ry, (R() - .5)*.06, 0, 6.2832); g.fill(); }
      g.filter = 'blur(1px)';
      for (let i = 0; i < 10; i++){ const y = y0 + R()*sh, xa = x0 + R()*sw, L = 80 + R()*260;
        g.strokeStyle = `rgba(140,118,90,${.04 + R()*.06})`; g.lineWidth = .8 + R()*1.2; g.beginPath(); g.moveTo(xa, y);
        for (let s = 1; s <= 5; s++) g.lineTo(xa + L*s/5, y + (R() - .5)*3); g.stroke(); }
      g.filter = 'none';
      for (let i = 0; i < 160; i++){ g.fillStyle = `rgba(128,106,80,${.12 + R()*.18})`; g.beginPath(); g.ellipse(x0 + R()*sw, y0 + R()*sh, 1 + R()*4, .6 + R()*1.1, 0, 0, 6.2832); g.fill(); }
      g.restore();
      g.fillStyle = 'rgba(150,134,112,.55)'; g.fillRect(x0, y0, sw, 2); g.fillRect(x0, y0, 2, sh);   // 2 px (~2.3 mm) joint
    }
  }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = anisotropy; t.generateMipmaps = true; t.minFilter = THREE.LinearMipmapLinearFilter;
  return t;
}
