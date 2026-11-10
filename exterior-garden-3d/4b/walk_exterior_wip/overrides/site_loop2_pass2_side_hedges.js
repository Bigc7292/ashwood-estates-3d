// Site loop 2 pass 2 (critic on 07a2881): continuous clipped hedges along both side boundaries in place of the round lollipop trees.
// OUTDOOR-SITE shows a continuous dark clipped hedge along the inside of both side walls from the rear wall to the front, with taller
// rounded clipped crowns rising out of it at intervals. The garden now runs to the rear wall at z -9.0 (shared pool v3 / M44), so both
// hedge rows (site pass 2) are extended from z 0.6 to z -8.7. The round trees along the sides are V4 plan tree symbols (tree-1..11), so
// their positions are kept (CAD) and only their look changes (side trees only: x < 3 or x > 15.5; the front-garden tree-12 keeps its spreading crown) (image): no visible trunk, one dense clipped crown from 0.6 m to 3.2 m in the
// hedge's olive, reading as the taller crowns in the hedge line (logged as M91). Heights and colour are image-read display assumptions.
// House, pool, carport and the camera lock unchanged. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
(function(){ const O = window.MODEL_OVERRIDES;
  for (const r of (O.shrubRows || [])) if (r.id === 'site-hedge-left' || r.id === 'site-hedge-right') { r.z0 = -8.7; r.status += '_extended_loop2p2'; }
  O.side_tree_style = {base:0.6, top:3.2, rScale:0.7, color:0x46532a};
})();
