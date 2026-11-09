// Front v2 pass 4 (critic on 114dca0): palm crowns scaled down to ELEV-FRONT's widths, centred on the same trunk tops.
// Critic: left crown ~300 px wide vs reference ~170 px (half-width side-by-side); right crown ~280+ px (runs off frame) vs ~130 px.
// Crown lengths x0.57 on the left palms and x0.40 on the right, and frond widths scale with crown (palm_style.wByCrown = 3.8, the
// pass 3 crown). Trunk positions, heights, lean and the locked camera unchanged. Colour unchanged (next pass). Display assumption.
// Concept visualisation, not survey-verified, not construction-ready.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
(function(){ const k = {'palm-left-main':0.57, 'palm-left-back':0.57, 'palm-right':0.40};
  for (const p of (window.MODEL_OVERRIDES.palms || [])) if (k[p.id]) p.crown = +(p.crown*k[p.id]).toFixed(2);
  if (window.MODEL_OVERRIDES.palm_style) window.MODEL_OVERRIDES.palm_style.wByCrown = 3.8; })();
