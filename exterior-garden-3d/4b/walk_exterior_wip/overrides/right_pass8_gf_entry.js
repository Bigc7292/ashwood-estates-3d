// Right view, step 3 blockout pass 8 (critic on 2ecf383): lower GF glazed entry with a warm lit interior tone.
// ELEV-RIGHT: glazed entry at side-by-side x ~320-415, rows ~370-430 (panel rows 330-390). On the GF facade line (x 15.99, d 26.61 m,
// 0.0359 m/px): z = 13.45 + (480 - col) * 0.0359 -> z 15.78-19.19; y = 1.6 + 26.61*(0.1145 - (row-270)/742) -> y 0.34-2.49 (derived).
// Flat warm panel (MAT timber_lit: warm, emissive) just proud of the CAD GF wall line. This view only, logged with M39.
// NOTE: the CAD-line boundary wall (top 1.85 m, M37) hides the panel below panel row ~348; in the reference the entry is seen through an
// opening in the boundary wall (steps at rows ~460-515). Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.add.push(
  {id:'right-gf-entry-glass', cat:'gf_glass', mat:'timber_lit', x0:15.99, x1:16.02, z0:15.78, z1:19.19, y0:0.34, y1:2.49, status:'right_pass8_gf_entry_derived_M39'}
);
