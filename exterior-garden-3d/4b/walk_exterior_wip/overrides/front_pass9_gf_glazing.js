// Front view, step 6 loop 2, single fix (critic on bbe1b36): ground-floor glazing.
// ELEV-FRONT shows lit GF glass across the recess from the carport column to the right side wall; the model had a narrow
// glass strip (gf-glass-11, plan cue x 7.50-9.59) and a brown interior panel behind it. This widens the lit glass band to
// the recess walls (x 7.50-10.70, the existing GF wall faces) and replaces the brown panel with a lit lobby.
// Appearance is image-read; the wider glass is logged as M27 (image vs plan cue). Interior depth and finishes are display assumptions.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.remove.push('gf-glass-11', 'int-gf-back-entry', 'int-gf-ceil-entry');
const GF9 = 'step6_gf_glazing_image_read_assumption';
window.MODEL_OVERRIDES.add.push(
  {id:'gf-glass-front-band', cat:'gf_glass', mat:'glass',          x0:7.50, x1:10.70, z0:23.55, z1:23.60, y0:0.0,  y1:3.5,  status:GF9},
  {id:'gf-mullion-1',        cat:'gf_frame', mat:'bronze_dark',    x0:8.54, x1:8.59,  z0:23.60, z1:23.66, y0:0.0,  y1:3.5,  status:GF9},
  {id:'gf-mullion-2',        cat:'gf_frame', mat:'bronze_dark',    x0:9.61, x1:9.66,  z0:23.60, z1:23.66, y0:0.0,  y1:3.5,  status:GF9},
  {id:'gf-transom',          cat:'gf_frame', mat:'bronze_dark',    x0:7.50, x1:10.70, z0:23.60, z1:23.66, y0:3.45, y1:3.5,  status:GF9},
  {id:'int-gf-lobby-back',   cat:'interior', mat:'interior_lobby', x0:7.50, x1:10.70, z0:20.40, z1:20.50, y0:0.0,  y1:3.5,  status:GF9},
  {id:'int-gf-lobby-ceil',   cat:'interior', mat:'interior_ceiling', x0:7.50, x1:10.70, z0:20.50, z1:23.50, y0:3.45, y1:3.5, status:GF9},
  {id:'int-gf-lobby-floor',  cat:'interior', mat:'interior_floor', x0:7.50, x1:10.70, z0:20.50, z1:23.50, y0:0.0,  y1:0.04, status:GF9}
);
