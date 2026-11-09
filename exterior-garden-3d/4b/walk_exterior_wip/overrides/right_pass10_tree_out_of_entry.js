// Right view, step 3 blockout pass 10 (critic on b5d8603): plan tree trunk out of the boundary-wall entry opening.
// Plan tree tree-9 (x 18.049, z 18.476) has its trunk inside the pass 9 opening (z 15.68-18.55), where it reads as a dark bar at panel
// x ~325-335. ELEV-RIGHT has no trunk at the entry edge. Display shift, this view only: trunk moved +0.55 m in z to 19.03 so it sits behind
// the wall piece beyond the opening edge (column ~312 vs edge ~320 at d 24.55 m, derived); canopy kept. Plan symbol position is otherwise
// unchanged in the model; logged with M40. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  for (const t of (window.MODEL.trees || [])) if (t.id === 'tree-9') {
    t.z = 19.03; t.status = (t.status || '') + '; right_pass10_display_shift_+0.55z_M40';
  }
})();
