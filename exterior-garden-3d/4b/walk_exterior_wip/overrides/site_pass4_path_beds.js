// Site/aerial view, step 3 blockout pass 4 (critic on 5e53566): low clipped shrub beds either side of the entry path.
// OUTDOOR-SITE: dark clipped shrub beds on both sides of the path. CAD front garden: lawn-8 (x 9.735-15.42, z 27.71-29.74) right of the
// path, and the strip between the path (x 7.50) and the carport edge (x 7.39) on the left, which is only ~0.1 m in CAD, so the left bed is
// a narrow single row on the carport edge (x 7.30). Beds ~0.6 m high (critic/reference), olive tones from the reference. Right bed: rows
// along the path edge (x 9.85, z 23.8-27.6) and across lawn-8 (z 28.2 / 29.2, x 9.9-15.2). Positions on the CAD front garden; row layout
// assumption. This view only. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
(function(){
  const st = 'site_pass4_CAD_front_garden_reference_planting', O = window.MODEL_OVERRIDES;
  O.shrubRows = (O.shrubRows || []).concat([
    {id:'site-bed-left',         x0:7.30, z0:23.9, x1:7.30, z1:29.5, h:0.6,  r:0.2,  color:0x4f5a2a, status:st},
    {id:'site-bed-right-path',   x0:9.85, z0:23.8, x1:9.85, z1:27.6, h:0.6,  r:0.28, color:0x55602e, status:st},
    {id:'site-bed-right-back',   x0:9.9,  z0:28.2, x1:15.2, z1:28.2, h:0.62, r:0.3,  color:0x4f5a2a, status:st},
    {id:'site-bed-right-front',  x0:9.9,  z0:29.2, x1:15.2, z1:29.2, h:0.55, r:0.28, color:0x5d6632, status:st}
  ]);
})();
