// Right view, step 3 blockout pass 3 (critic on 7ad022f): thin roof canopy.
// At the locked right camera (row = 270 - 742*((Y-1.6)/d - 0.1145), 960x540 panel): ELEV-RIGHT's canopy edge top at panel row ~153 and its soffit's
// far edge at ~180. With the near edge on the right facade line (x 14.93, d 27.67 m) that gives top 9.13 m, a 0.30 m slab (underside 8.83 m) and a
// depth back to x ~11.94 (far soffit edge at d 30.66 m). Columns kept (z 3.2-8.4). This view only; derived, display assumption (M36).
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  for (const b of window.MODEL_OVERRIDES.add) if (b.id === 'right-rf-canopy') {
    b.x0 = 11.94; b.x1 = 14.93; b.y0 = 8.83; b.y1 = 9.13; b.mat = 'soffit'; b.status += '; right_pass3_thin_slab_derived';
  }
})();
