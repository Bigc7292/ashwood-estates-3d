// Left view, step 3 blockout pass 3 (critic on 435f6c3): the base band.
// ELEV-LEFT: travertine boundary wall with its top on row ~487 of 720, a low planting band at its foot, a pale gravel strip and lawn in front.
// The model's grey placeholder 'boundary-left' (x -0.25-0, 1.8 m) is replaced by a stone wall on the same line, top 2.0 m (image-read at the
// locked left camera: 1.8 m sat ~7 px high at 960x540; display assumption). Off-plot lawn/gravel and the planting band are context, outside
// the CAD plot (x < -0.25). Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.remove.push('boundary-left');
const L3 = 'left_pass3_image_read_context_assumption';
window.MODEL_OVERRIDES.add.push(
  {id:'left-boundary-stone', cat:'boundary', mat:'stone',  x0:-0.25, x1:0.0,   z0:0.0,  z1:29.88, y0:0.0, y1:2.0,  status:L3},
  {id:'left-boundary-cap',   cat:'boundary', mat:'coping', x0:-0.30, x1:0.05,  z0:0.0,  z1:29.88, y0:2.0, y1:2.05, status:L3},
  {id:'left-gravel-strip',   cat:'ground',   mat:'paving', x0:-1.4,  x1:-0.25, z0:-4.0, z1:32.0,  y0:-0.04, y1:0.0, status:L3},
  {id:'left-context-lawn',   cat:'lawn',     mat:'lawn',   x0:-14.0, x1:-1.4,  z0:-4.0, z1:32.0,  y0:0.0, y1:0.03, status:L3}
);
window.MODEL_OVERRIDES.shrubRows = (window.MODEL_OVERRIDES.shrubRows || []).concat([
  {id:'left-wall-planting', x0:-0.6, z0:0.6, x1:-0.6, z1:23.4, h:0.9, r:0.32, color:0x4f6b33, status:L3}
]);
