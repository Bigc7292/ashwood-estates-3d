// Front v2 pass 6 (critic on 17cef22 / 9d4cb99): one more frond ring per palm crown so the crowns read dense and layered.
// The new ring (16 fronds, 0.9 of crown length, angles between the outer and middle rings, slightly less droop) fills the
// gaps between the existing rings. Outer length is unchanged (len <= 1.0), so the crown width/scale from pass 4 holds; colour
// from pass 5, trunks and camera unchanged. Display assumption. Concept visualisation, not survey-verified, not construction-ready.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
(function(){ const PS = window.MODEL_OVERRIDES.palm_style; if (!PS || !PS.rings) return;
  PS.rings.splice(1, 0, {n:16, len:0.9, up:[0.8,1.0,1.2], droop:0.6, w:1.8}); })();
