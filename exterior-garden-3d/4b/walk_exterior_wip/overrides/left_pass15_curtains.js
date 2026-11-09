// Left view, step 4 pass 15 (critic on 31ee909): the three tall FF windows read as black holes; ELEV-LEFT shows pale curtains behind glass.
// The opaque dark panes from pass 11 become clear glass (model 'glass' material) and a flat pale curtain panel sits just inside the glazing line
// (x 3.00-3.03, in front of the CAD FF glass at x 3.05). Openings' position and size unchanged. Reference median RGB inside the three windows
// ~140-150 grey-cream; curtain colour tuned to that. Flat colour, display assumption.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const O = window.MODEL_OVERRIDES; if (!O) return;
  for (const b of O.add) if (/^l11-window-/.test(b.id)) {
    b.mat = 'glass'; b.status += '; pass15_clear_glass';
    O.add.push({id:b.id.replace('l11-window-', 'l15-curtain-'), cat:'interior', mat:'curtain', x0:3.00, x1:3.03, z0:b.z0, z1:b.z1, y0:b.y0, y1:b.y1, status:'left_pass15_flat_curtain_assumption'});
  }
})();
