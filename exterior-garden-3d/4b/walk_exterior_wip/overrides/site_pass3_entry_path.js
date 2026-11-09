// Site/aerial view, step 3 blockout pass 3 (critic on 4195dd5): paved entry path from the front gate to the entry.
// CAD: main front gate boundary-front-gate x 7.39-9.735 at z 29.88; GF entry glazing gf-glass-11 x 7.50-9.59 at z 23.1-23.6 (the front
// door position used in the front view, M27). OUTDOOR-SITE draws a light paved path between them with planting either side. Path
// x 7.50-9.59 (CAD entry width), z 23.6-29.88, as a lighter flat paving tone (paving_inner 0xe8dfcf) 1 cm proud of the site paving.
// Width/position from CAD; tone from the reference (assumption). This view only.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
// The reference path reads as large light slabs with dark joints, so: a darker joint bed (drive) with light slabs 0.92 m deep and 0.08 m
// joints on top (slab module: assumption).
window.MODEL_OVERRIDES.add.push(
  {id:'site-entry-path-bed', cat:'ground', mat:'drive', x0:7.50, x1:9.59, z0:23.6, z1:29.88, y0:0, y1:0.01, status:'site_pass3_CAD_entry_width_reference_tone'}
);
for (let z = 23.64, i = 0; z + 0.5 < 29.88; z += 1.0, i++)
  window.MODEL_OVERRIDES.add.push({id:'site-entry-slab-' + i, cat:'ground', mat:'paving_inner', x0:7.54, x1:9.55, z0:z, z1:Math.min(z + 0.92, 29.84), y0:0.01, y1:0.02, status:'site_pass3_slab_module_assumption'});
