// Front v2 pass 7 (critic on e4f7758): entry gate bars from near-black to the reference's sampled dark bronze.
// The critic asked for warm timber-brown; a crop of ELEV-FRONT shows dark metal bars backlit by the warm lobby (the brightness is behind the
// bars, not on them), so the bars are matched to the sampled dark third, not the lit background. Crop: views/front_v2/shots/front_v2_pass7_gate_crop.png.
// Sample: ELEV-FRONT at the gate (side-by-side panel x 425-530, rows 420-495; 1280x720 source): brightest third
// median RGB 134,95,65 (mostly the lit lobby seen between the bars); darkest third (the bars) 36,25,17; this pass renders 32,17,8. Model pass 6 darkest third 3,1,0 (dark bar texture x dark tint x
// metalness 0.4 with no environment map). Box `boundary-front-gate` (CAD x 7.39-9.735) unchanged; slat pattern and position unchanged.
// Uses the mat_tune hook in front_v2.html. Display assumption. Concept visualisation, not survey-verified, not construction-ready.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.mat_tune = Object.assign(window.MODEL_OVERRIDES.mat_tune || {}, {
  bronze_bars: {barFill:'#ffffff', color:0x3a2c20, metalness:0.0, roughness:0.7, emissive:0x060403} });
