// Left view, step 3 blockout pass 1 (critic on the left lock, 334032a): RF volume vs the reference's low roof plant strip.
// ELEV-LEFT shows, above the FF roof slab (top 7.85 m, model), only a low recessed strip under a thin overhanging canopy slab, near the
// street end. Read at the locked left camera (about 29 px/m at the strip's depth, 960x540): canopy top row 143 (= 9.76 m), canopy soffit row 152
// (~9.45 m), z ~16.6-23.2 m (first try at 8.83 m sat 27 px low, corrected). The model's RF walls (7.85-10.85 m, z 9.95-22.5) and RF roofs/canopy are hidden in this view only and the strip
// is built inside the RF footprint. Positions/heights are image-read display assumptions; logged as M33 (relates to M12, M26). Colin can overrule.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.hide_cats = (window.MODEL_OVERRIDES.hide_cats || []).concat(['rf_wall', 'rf_roof']);
window.MODEL_OVERRIDES.remove.push('rf-canopy');
const L1 = 'left_pass1_image_read_assumption_M33';
window.MODEL_OVERRIDES.add.push(
  {id:'left-rf-strip',        cat:'canopy', mat:'stone',  x0:3.6, x1:11.0, z0:17.2, z1:22.5, y0:7.85, y1:9.45, status:L1},
  {id:'left-rf-canopy-slab',  cat:'canopy', mat:'soffit', x0:3.1, x1:11.6, z0:16.6, z1:23.2, y0:9.45, y1:9.76, status:L1}
);
