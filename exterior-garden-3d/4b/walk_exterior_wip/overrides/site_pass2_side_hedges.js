// Site/aerial view, step 3 blockout pass 2 (critic on 29e3a1a; content independent of the M42 house scale): hedge lines along the
// side boundaries. OUTDOOR-SITE shows a continuous clipped hedge with taller tree crowns against the inside of both side walls, from
// the rear wall to near the front. Hedge 1.5 m high (assumption; reads about level with/above the 1.8 m wall top in the reference),
// 0.9 m deep, along x 0.5 (left) and x 18.2 (right), z 0.6-23.0 (left, stops at the carport) and z 0.6-28.6 (right). Olive tones from
// the reference hedge. Positions: assumption on the CAD plot. This view only.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
(function(){
  const st = 'site_pass2_image_read_assumption', O = window.MODEL_OVERRIDES;
  O.shrubRows = (O.shrubRows || []).concat([
    {id:'site-hedge-left',  x0:0.5,  z0:0.6, x1:0.5,  z1:23.0, h:1.5, r:0.45, color:0x4f5a2a, status:st},
    {id:'site-hedge-right', x0:18.2, z0:0.6, x1:18.2, z1:28.6, h:1.5, r:0.45, color:0x4f5a2a, status:st}
  ]);
})();
