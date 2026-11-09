// Front view, step 6 loop 2, pass 15 (critic on ca7c9d6): roof slab top to the ELEV-FRONT row.
// The slab top (7.85 m at the front edge z 26.88) sat ~19 px low at 960x540 (row 136 vs reference 117, image rows).
// Derived top that lands on the row with the shift-lens camera: 8.35 m, so the FF storey is raised by 0.50 m and the slab keeps
// its 0.45 m thickness. Everything that ran to the old FF ceiling (FF walls, glass, slats, interiors, soffit LEDs) is stretched
// or lifted with it. In-memory only, front-view build only: model data unchanged. Levels are already display assumptions (NTS);
// logged as M28. Colin can overrule. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const D = 0.50, M = window.MODEL, O = window.MODEL_OVERRIDES || {add:[]};
  const adjust = b => { if (b.y0 >= 3.9 && b.y1 >= 7.2 && b.y1 <= 7.41) { if (b.y0 >= 7.2) b.y0 += D; b.y1 += D; } };
  M.boxes.forEach(adjust); O.add.forEach(adjust);
  const slab = M.polys.find(p => p.id === 'ff-roof-slab'); if (slab) { slab.y0 += D; slab.y1 += D; slab.status = 'pass15_front_view_level_assumption_M28'; }
})();
