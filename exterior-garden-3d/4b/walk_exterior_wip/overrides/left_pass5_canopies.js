// Left view, step 3 blockout pass 5 (critic on 13fff91): tree canopies.
// The round lollipop canopies are the model's plain plan trees (plan symbols; species and height unknown). Keep the CAD trunk positions and
// replace the spheres with irregular, feathered multi-stem canopies of varied size (front pass 16 builder). The left-side plan trees
// (tree-1, 3, 4, 5, 6) sit at nearly the same z as pass 4's four image-read trees in front of the wall, so those four are dropped to avoid
// doubles: CAD decides positions. Sizes are display assumptions. Courtyard tree kept. Other plan trees (right side) also get the new canopy.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.remove_plain_trees = true;   // spheres off; courtyard tree kept
const L5 = 'left_pass5_plan_position_canopy_size_assumption';
window.MODEL_OVERRIDES.multiStemTrees = (window.MODEL_OVERRIDES.multiStemTrees || []).filter(t => !/^left-tree-/.test(t.id));
const plainTrees = (window.MODEL.trees || []).filter(t => !t.courtyard);
plainTrees.forEach((t, i) => {
  const v = [1.0, 0.82, 1.12, 0.9, 1.05, 0.86][i % 6];
  window.MODEL_OVERRIDES.multiStemTrees.push({id:'left-canopy-' + t.id, x:t.x, z:t.z, top:3.9 * v, spread:2.2 * t.r * v, stems:4 + (i % 3),
    clusters:Math.round(300 * v), color:[0x4a6a30, 0x55733a, 0x46632c][i % 3], status:L5});
});
