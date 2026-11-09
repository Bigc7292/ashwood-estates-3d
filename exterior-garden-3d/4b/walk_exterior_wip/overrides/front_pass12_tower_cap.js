// Front view, step 6 loop 2, fix (critic on e62ad64): right tower top.
// Check at the locked camera (cameras/front_pass12_tower_crop.png): the sloping top edge of the tower's lit side face is
// perspective of a 4 m deep blade and is present in ELEV-FRONT as well. What the reference has and the model lacked is a
// crisp flat top: a thin dark coping cap across the blade. Footprint and height (10.1 m, M25) are unchanged.
// Cap thickness 0.08 m and colour are image-read display assumptions. Concept visualisation, not survey-verified,
// not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.add.push(
  {id:'stone-fin-cap', cat:'canopy', mat:'bronze_dark', x0:15.48, x1:16.02, z0:22.88, z1:26.92, y0:10.1, y1:10.18, status:'pass12_image_read_cap_assumption'}
);
