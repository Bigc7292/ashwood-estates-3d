// Right view, step 4 finish pass 2 (critic FAIL on aa77d21): the bed as separate shrub masses, not one flat strip.
// Replaces pass 1's continuous right-bed-shrub/right-bed-grass rows with clumps 0.6-1.1 m long, 0.55-0.9 m high (critic range, read from
// ELEV-RIGHT), gaps 0.25-0.5 m, a few grass tufts in the gaps. Same olive tones, same entry/gate gaps. Positions/sizes: assumption
// (deterministic pseudo-random, seed fixed, so every render is identical). This view only.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const O = window.MODEL_OVERRIDES, st = 'right_step4_pass2_image_read_assumption';
  O.shrubRows = (O.shrubRows || []).filter(r => !/^right-bed-shrub-/.test(r.id));
  O.grassRows = (O.grassRows || []).filter(r => !/^right-bed-grass-/.test(r.id));
  let s = 4242; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  const shades = [0x6b6a32, 0x5f6230, 0x76703a, 0x646a36];
  [[0.3, 15.5], [18.75, 24.45]].forEach(([a, b], si) => {
    let z = a, i = 0;
    while (z < b - 0.4) {
      const len = Math.min(0.6 + 0.5 * rnd(), b - z), h = 0.55 + 0.35 * rnd(), x = 19.15 + 0.25 * rnd();
      O.shrubRows.push({id:`right-bed-clump-${si}-${i}`, x0:x, z0:z, x1:x, z1:z + len, h, r:Math.min(0.42, 0.26 + h * 0.18),
                        color:shades[i % shades.length], status:st});
      z += len;
      const gap = 0.25 + 0.25 * rnd();
      if (gap > 0.38 && z + gap < b) O.grassRows.push({id:`right-bed-tuft-${si}-${i}`, x0:19.45, z0:z + 0.05, x1:19.45, z1:z + gap - 0.05,
                        h:0.45 + 0.2 * rnd(), gap:0.2, blades:14, color:0x7d7a3c, status:st});
      z += gap; i++;
    }
  });
})();
