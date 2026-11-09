// Front view, step 6 loop 2, pass 14 (critic on 8fda529, coordinator relaying Colin's "don't wait"): tower top to the reference row.
// With the shift lens (level camera), the 10.1 m top sat ~18 px above the ELEV-FRONT top row at 960x540.
// Derived height that puts the top of the cap on the row: 9.73 m (row 60/540, front face z 26.92, d 18.48 m, vFOV 40).
// ASSUMPTION for the front view build only, logged in views/front/M25_assumption_2026-11-09.md; Colin can overrule (M25 stays open).
// Footprint unchanged. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
// earlier overrides live in add[], which remove[] does not filter, so drop them from add[] directly
window.MODEL_OVERRIDES.add = window.MODEL_OVERRIDES.add.filter(b => !['stone-fin-pass2','stone-fin-cap'].includes(b.id));
window.MODEL_OVERRIDES.add.push(
  {id:'stone-fin-pass14', cat:'canopy', mat:'stone', x0:15.5, x1:16.0, z0:22.9, z1:26.9, y0:0.0, y1:9.65, status:'pass14_M25_front_view_assumption_derived_9.73_top'},
  {id:'stone-fin-cap-pass14', cat:'canopy', mat:'bronze_dark', x0:15.48, x1:16.02, z0:22.88, z1:26.92, y0:9.65, y1:9.73, status:'pass14_image_read_cap_assumption'}
);
