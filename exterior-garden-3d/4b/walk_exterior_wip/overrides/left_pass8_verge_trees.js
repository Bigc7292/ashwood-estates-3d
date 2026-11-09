// Left view, step 3 blockout pass 8 (critic on 55ebb19): trees that read as trees, with trunks and a clear gap above the hedge.
// Geometry check: the CAD plan trees stand inside the plot (x ~0.9-1.8 m), behind the 2.0 m boundary wall, so from this camera their trunks are
// hidden by the wall and a crown top on row ~365 leaves only ~1 m of crown above the wall. They cannot show trunks rising out of the planting.
// ELEV-LEFT's four trunked trees therefore stand on the verge in front of the wall (off the CAD plot = context, like the lawn). They are restored
// here at the image-read columns (z 2.5/8.1/12.5/17.7, x -1.0) with open crowns from ~2.3 m to ~3.4 m (top on row ~365) and bare trunks below.
// The CAD plan trees stay at their positions behind the wall (pass 5-7). Display assumptions. Concept visualisation, not survey-verified,
// not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
const L8 = 'left_pass8_image_read_offplot_context_assumption';
window.MODEL_OVERRIDES.multiStemTrees = (window.MODEL_OVERRIDES.multiStemTrees || []).concat(
  [[2.5,3.3],[8.1,3.5],[12.5,3.4],[17.7,3.4]].map(([z,top], i) => ({id:'left-verge-tree-' + (i+1), x:-1.0, z, top, spread:2.9, stems:4, clusters:480,
    leaf:1.25, depth:0.8, color:[0x6b7f45, 0x768a4e, 0x627a40][i % 3], status:L8}))
);
