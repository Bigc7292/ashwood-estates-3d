// Right view, step 4 finish pass 1 (critic close of step 3 on d954a47): planting bed in front of the boundary wall.
// ELEV-RIGHT: a continuous bed of spiky grasses/low shrubs against the outer face of the wall, either side of the entry steps and from
// the gate toward the rear; its top sits at ~1/3 of the wall height (rows ~490 vs wall 425-520 at 1280x720 -> ~0.6 m on a 1.8 m wall,
// derived). Colours from the reference bed (olive, ~RGB 61-83, 55-74, 19-38), lifted ~40% because the model shades the bed darker than the sampled tone. Bed gaps left at the entry (z 15.68-18.55) and the
// gate (z 24.60-27.78). Positions on the verge in front of the CAD wall line (x 19.15-19.6): assumption. This view only.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
(function(){
  const st = 'right_step4_pass1_image_read_assumption';
  const segs = [[0.3, 15.5], [18.75, 24.45]];
  const shrubs = [], grass = [];
  segs.forEach(([a, b], i) => {
    shrubs.push({id:'right-bed-shrub-' + i, x0:19.15, z0:a, x1:19.15, z1:b, h:0.55, r:0.24, color:0x6b6a32, status:st});
    grass.push({id:'right-bed-grass-' + i, x0:19.45, z0:a + 0.2, x1:19.45, z1:b - 0.2, h:0.62, gap:0.4, blades:22, color:0x7d7a3c, status:st});
  });
  window.MODEL_OVERRIDES.shrubRows = (window.MODEL_OVERRIDES.shrubRows || []).concat(shrubs);
  window.MODEL_OVERRIDES.grassRows = (window.MODEL_OVERRIDES.grassRows || []).concat(grass);
})();
