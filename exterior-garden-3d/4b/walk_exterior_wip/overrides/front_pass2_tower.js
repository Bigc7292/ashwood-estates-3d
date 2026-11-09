// Front view, pass 2 (critic's one fix): tall stone fin / tower at the front right.
// Footprint: mismatch_log M2 "STONE_FIN 0.5 m blade on the CAD GF right edge" (x = gf_wall max 16.0 minus 0.5).
// Height: 10.1 m, image-read from ELEV-FRONT at the locked camera (~38.5 px/m at the facade plane).
//   CONFLICT: M2 records top 11.6 m image-read from another view. ELEV-FRONT is the reference for this view, so 10.1 m is used here.
// Depth: 4.0 m in z, assumption, set so the lit side face width matches ELEV-FRONT. Concept visualisation only.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.add.push(
  {id:'stone-fin-pass2', cat:'canopy', mat:'stone', x0:15.5, x1:16.0, z0:22.9, z1:26.9, y0:0.0, y1:10.1, status:'pass2_M2_footprint_top_image_read_ELEV-FRONT_conflicts_M2_11.6_depth_assumption'}
);
