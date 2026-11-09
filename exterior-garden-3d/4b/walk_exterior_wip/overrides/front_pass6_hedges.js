// Front view, pass 6 (critic's order: hedge row after the slat screen): planting along the front boundary.
// Positions and heights back-projected from ELEV-FRONT through the locked camera (assumptions, not survey).
// Rows are lines of clumped shrubs: from (x0,z0) to (x1,z1), top height h, clump radius r, colour.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.shrubRows = [
  {id:'front-flower-bed',      x0:10.0, z0:30.55, x1:18.7, z1:30.55, h:0.38, r:0.24, color:0x55703a, flowers:0xd98aa8, status:'pass5_image_read_assumption'},
  {id:'shrub-mass-behind-wall',x0:11.8, z0:28.6,  x1:13.9, z1:28.6,  h:3.4,  r:0.75, color:0x4c6a32, status:'pass5_image_read_assumption'},
  {id:'shrubs-behind-right',   x0:15.2, z0:29.2,  x1:18.5, z1:29.2,  h:1.4,  r:0.42,  color:0x48652f, status:'pass5_image_read_assumption'},
  {id:'carport-left-grasses',  x0:0.45, z0:24.2,  x1:0.45, z1:29.2,  h:0.9,  r:0.22, color:0x7f8f45, status:'pass5_image_read_assumption'}
];
