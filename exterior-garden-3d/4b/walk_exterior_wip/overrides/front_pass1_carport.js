// Front view, pass 1 (critic's one fix): carport rebuilt as a deep, low slab on two columns.
// Footprint: CAD vehicle-entry zone x 0-7.6, z 23.6-29.3 (mismatch_log M1).
// Heights: soffit 2.6 m (critic estimate from ELEV-FRONT, assumption); top 3.45 m (M1, image-read).
// Edge band: dark bronze canopy edge (M18, image-read). Columns: stone, image-read positions (assumption).
// Concept visualisation, not survey-verified, not construction-ready.
window.MODEL_OVERRIDES = {
  remove: ['carport-canopy', 'carport-canopy-post'],
  add: [
    {id:'carport-slab-pass1', cat:'canopy', mat:'soffit', x0:0.0, x1:7.6, z0:23.6, z1:29.3, y0:2.6, y1:3.45, status:'pass1_image_read_heights_assumption_cad_footprint'},
    {id:'carport-edge-band-pass1', cat:'canopy', mat:'bronze_slats', x0:0.0, x1:7.6, z0:29.3, z1:29.36, y0:3.25, y1:3.45, status:'pass1_M18_image_read'},
    {id:'carport-column-left-pass1', cat:'canopy', mat:'stone', x0:0.0, x1:0.5, z0:28.7, z1:29.2, y0:0.0, y1:2.6, status:'pass1_image_read_assumption'},
    {id:'carport-column-right-pass1', cat:'canopy', mat:'stone', x0:7.0, x1:7.6, z0:28.7, z1:29.2, y0:0.0, y1:2.6, status:'pass1_image_read_assumption'}
  ]
};
