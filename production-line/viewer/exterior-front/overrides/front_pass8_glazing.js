// Front view, step 6 loop 1, single fix: glazing.
// Critic: the glass read as flat beige; ELEV-FRONT shows dark glass with warm-lit rooms behind it (timber/stone back walls,
// ceiling glow) on the FF behind the slat screen and at the GF entry. Image-read appearance only; the interior panel depths
// (about 3 m behind the glass) and finishes are DISPLAY ASSUMPTIONS. Plan geometry is not changed.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.glass_mode = 'interior';
const GLZ_A = 'step6_glazing_display_assumption';
window.MODEL_OVERRIDES.add.push(
  // FF: rooms behind the three front glass runs
  {id:'int-ff-back-c', cat:'interior', mat:'interior_wood',    x0:7.42,  x1:10.63, z0:21.0, z1:21.1, y0:4.0,  y1:7.4, status:GLZ_A},
  {id:'int-ff-ceil-c', cat:'interior', mat:'interior_ceiling', x0:7.42,  x1:10.63, z0:21.1, z1:24.4, y0:7.25, y1:7.3, status:GLZ_A},
  {id:'int-ff-floor-c',cat:'interior', mat:'interior_floor',   x0:7.42,  x1:10.63, z0:21.1, z1:24.4, y0:4.0,  y1:4.04,status:GLZ_A},
  {id:'int-ff-back-l', cat:'interior', mat:'interior_stone',   x0:3.3,   x1:7.08,  z0:21.0, z1:21.1, y0:4.0,  y1:7.4, status:GLZ_A},
  {id:'int-ff-ceil-l', cat:'interior', mat:'interior_ceiling', x0:3.3,   x1:7.08,  z0:21.1, z1:23.8, y0:7.25, y1:7.3, status:GLZ_A},
  {id:'int-ff-back-r', cat:'interior', mat:'interior_stone',   x0:11.0,  x1:15.2,  z0:21.0, z1:21.1, y0:4.0,  y1:7.4, status:GLZ_A},
  {id:'int-ff-ceil-r', cat:'interior', mat:'interior_ceiling', x0:11.0,  x1:15.2,  z0:21.1, z1:23.9, y0:7.25, y1:7.3, status:GLZ_A},
  // GF entry (gf-glass-11): lit lobby behind the glass
  {id:'int-gf-back-entry', cat:'interior', mat:'interior_wood',    x0:7.5, x1:9.6, z0:20.4, z1:20.5, y0:0.0,  y1:3.6, status:GLZ_A},
  {id:'int-gf-ceil-entry', cat:'interior', mat:'interior_ceiling', x0:7.5, x1:9.6, z0:20.5, z1:23.0, y0:3.5,  y1:3.55,status:GLZ_A}
);
