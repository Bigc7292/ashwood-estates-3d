// Right view, step 3 blockout pass 1 (critic on the right lock, 3ce23e6): roof-level canopy position.
// The model's rf-canopy (z 4.6-9.95, plan-envelope assumption) projects at panel columns ~567-717; ELEV-RIGHT has it at ~610-750, i.e. ~40 px
// toward the rear (~26.8 px/m at the canopy edge x 14.93) -> z ~3.2-8.4 m. Moved in this view only; size kept (~5.2 m), height unchanged.
// NOTE: the generated images disagree on the roof element: ELEV-LEFT puts its roof strip near the street end (z ~16.6-23.2, M33), ELEV-RIGHT near
// the rear (here). Logged as M36; each view follows its own image until Colin rules. Concept visualisation, not survey-verified,
// not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.remove.push('rf-canopy');
window.MODEL_OVERRIDES.add.push(
  {id:'right-rf-canopy', cat:'canopy', mat:'placeholder', x0:3.928, x1:14.932, z0:3.2, z1:8.4, y0:10.85, y1:11.2, status:'right_pass1_image_read_position_M36'}
);
