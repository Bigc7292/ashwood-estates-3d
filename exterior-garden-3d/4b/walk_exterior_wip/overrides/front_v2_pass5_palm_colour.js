// Front v2 pass 5 (critic on 6cd14bc): palm crown colour matched to ELEV-FRONT's sampled crown colour.
// Sample: ELEV-FRONT left crown, side-by-side panel x 120-250, y 170-240 (1280x720 source), green-dominant pixels, median RGB 74,80,61
// (deep, muted olive in shade). Model pass 4 median at the same window: RGB 53,67,11 (over-saturated lime). Frond leaflet colours,
// midrib and emissive retuned so the rendered median lands near the sample. Shape, scale, trunks and camera unchanged. Display assumption.
// Concept visualisation, not survey-verified, not construction-ready.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
(function(){ const PS = window.MODEL_OVERRIDES.palm_style; if (!PS) return;
  PS.leaf = Object.assign({}, PS.leaf, {colours:['#727d66','#7b856e','#69735c'], midrib:'#545b46'}); PS.emissive = 0x080a06; })();
