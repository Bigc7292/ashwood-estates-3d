// Right view, step 3 blockout pass 4 (critic on 8c982ef): the right boundary reads as a grey kerb band.
// Geometry check at the locked right camera (row = 270 - 742*((Y-1.6)/d - 0.1145), 960x540 panel): on the CAD boundary line (x 18.72-18.97,
// d 23.63 m) the ground is at panel row 405 and a 1.8 m top at row 349 (389 in the side-by-side). ELEV-RIGHT's wall runs from row ~472 (base) to
// ~386 (top), i.e. ~2.7 m tall with its base ~67 px lower than the CAD ground line: in the image the wall is much nearer the camera than the CAD
// boundary (or the image's ground is lower). On the CAD line, a top at the reference row would be a 0.64 m wall. So this pass keeps the CAD line and
// the model's 1.8 m height and makes it read as a wall: travertine with coping, and the off-plot ground beyond it as lawn/paving context.
// The row difference is logged as a residual for the critic/Colin. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.remove.push('boundary-right');
window.MODEL_OVERRIDES.add.push(
  {id:'right-boundary-stone', cat:'boundary', mat:'stone',  x0:18.72, x1:18.97, z0:0.0, z1:29.88, y0:0.0, y1:1.8,  status:'CAD boundary line, model height; travertine (right pass 4)'},
  {id:'right-boundary-cap',   cat:'boundary', mat:'coping', x0:18.67, x1:19.02, z0:0.0, z1:29.88, y0:1.8, y1:1.85, status:'right_pass4_assumption'},
  {id:'right-verge-paving',   cat:'ground',   mat:'paving', x0:18.97, x1:20.4,  z0:-4.0, z1:32.0, y0:-0.04, y1:0.0, status:'right_pass4_offplot_context'},
  {id:'right-context-lawn',   cat:'lawn',     mat:'lawn',   x0:20.4,  x1:34.0,  z0:-4.0, z1:32.0, y0:0.0, y1:0.03, status:'right_pass4_offplot_context'}
);
