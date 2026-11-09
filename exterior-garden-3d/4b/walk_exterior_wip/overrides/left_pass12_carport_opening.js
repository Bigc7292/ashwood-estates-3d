// Left view, step 3 blockout pass 12 (critic on f3f9341): carport opening and pillar in the left boundary wall.
// ELEV-LEFT at the locked left camera, projected at the wall line x 0 (d 22.5 m, 742 px focal at 960x540): the wall ends at panel column 675
// (z ~21.0 m), the opening runs to column 855 (z ~26.45 m),
// then a travertine pillar to column 895 (z ~27.66 m), its top level with the wall coping. Opening and pillar are image-read display assumptions
// on the CAD boundary line (x -0.25-0); the planting and grass rows stop at the opening. Concept visualisation, not survey-verified,
// not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
(function(){
  const O = window.MODEL_OVERRIDES, A = 'left_pass12_image_read_assumption', ZW = 21.0, ZP0 = 26.45, ZP1 = 27.66;
  for (const b of O.add) if (b.id === 'left-boundary-stone' || b.id === 'left-boundary-cap') { b.z1 = ZW; b.status += '; pass12_ends_at_carport_opening'; }
  O.add.push(
    {id:'left-carport-pillar',     cat:'boundary', mat:'stone',  x0:-0.40, x1:0.10, z0:ZP0, z1:ZP1, y0:0.0, y1:2.0,  status:A},
    {id:'left-carport-pillar-cap', cat:'boundary', mat:'coping', x0:-0.45, x1:0.15, z0:ZP0 - 0.05, z1:ZP1 + 0.05, y0:2.0, y1:2.05, status:A},
    {id:'left-carport-apron',      cat:'ground',   mat:'paving', x0:-1.4,  x1:0.0,  z0:ZW, z1:ZP0, y0:-0.035, y1:0.005, status:A}
  );
  for (const r of (O.shrubRows || [])) if (/^left-planting-/.test(r.id)) r.z1 = Math.min(r.z1, ZW - 0.3);
  for (const r of (O.grassRows || [])) if (/^left-tall-grass-/.test(r.id)) r.z1 = Math.min(r.z1, ZW - 0.3);
})();
