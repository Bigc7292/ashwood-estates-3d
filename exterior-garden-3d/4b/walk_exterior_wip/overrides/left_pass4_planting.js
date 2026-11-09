// Left view, step 3 blockout pass 4 (critic on 6f55371): layered planting at the wall foot.
// ELEV-LEFT: dense layered planting (tall shrubs at the wall, lower shrubs and grasses in front) plus four small multi-stem trees
// in front of the wall rising above it. Tree positions read at the locked left camera (x px 150/370/540/740 of 1280 -> z 2.5/8.1/12.5/17.7 m),
// tops ~3.4 m. Species unknown; all positions and sizes are image-read display assumptions, off the CAD plot (x < -0.25).
// Replaces pass 3's single row. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
const L4 = 'left_pass4_image_read_assumption';
window.MODEL_OVERRIDES.shrubRows = (window.MODEL_OVERRIDES.shrubRows || []).filter(r => r.id !== 'left-wall-planting').concat([
  {id:'left-planting-back',  x0:-0.6,  z0:0.4, x1:-0.6,  z1:23.4, h:1.35, r:0.42, color:0x445f2c, status:L4},
  {id:'left-planting-mid',   x0:-0.95, z0:0.7, x1:-0.95, z1:23.2, h:0.75, r:0.28, color:0x58733a, status:L4},
  {id:'left-planting-front', x0:-1.25, z0:0.9, x1:-1.25, z1:23.0, h:0.45, r:0.17, color:0x6b8446, status:L4}
]);
window.MODEL_OVERRIDES.multiStemTrees = (window.MODEL_OVERRIDES.multiStemTrees || []).concat([
  {id:'left-tree-1', x:-1.0, z:2.5,  top:3.3, spread:2.6, stems:5, clusters:300, color:0x4a6a30, status:L4},
  {id:'left-tree-2', x:-1.0, z:8.1,  top:3.5, spread:2.8, stems:5, clusters:320, color:0x4a6a30, status:L4},
  {id:'left-tree-3', x:-1.0, z:12.5, top:3.4, spread:2.7, stems:5, clusters:320, color:0x4a6a30, status:L4},
  {id:'left-tree-4', x:-1.0, z:17.7, top:3.4, spread:2.7, stems:5, clusters:300, color:0x4a6a30, status:L4}
]);
