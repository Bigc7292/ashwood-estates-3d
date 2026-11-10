// Front v2 pass 9 (critic on 51f4d84): entry gate widened to the V4 CAD pedestrian-entry span.
// CAD read: the approved V4 GF sheet's front dimension strip (work/v4_GF_x3.png) reads ~2.9 | ~4.4 | ~3.4 | ~5.2 | ~2.7 m (total ~18.7 m),
// with "PEDESTRIAN ENTRY" over the ~3.4 m span. Measured tick positions along the strip give that span as x 7.40-10.76 m (derived; the
// sheet's spans are calibration-derived, +/-3 %). The model's gate (build_model.py, gx(315)-gx(381) = x 7.39-9.735) was narrower than
// that span, so the gate now runs x 7.39-10.76 and the central front wall starts at 10.76. ELEV-FRONT shows the gate continuing to about
// x 11.5 m (panel x ~620, derived from the locked camera); the remaining ~0.7 m is past the CAD span and is logged as M90, not built.
// Height, rail, bar pitch and colour from passes 7-8. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
(function(){ const O = window.MODEL_OVERRIDES, X1 = 10.76;
  for (const b of O.add) if (b.id === 'boundary-front-gate-v2p8' || b.id === 'boundary-front-gate-rail-v2p8') { b.x1 = X1; b.status += '_width_cad_span_v2p9'; }
  O.remove.push('boundary-front-wall-c');
  O.add.push({id:'boundary-front-wall-c-v2p9', cat:'boundary', mat:'stone', x0:X1, x1:15.42, z0:29.881, z1:30.131, y0:0, y1:1.2, status:'render_p25_observed_height_assumed_start_cad_span_v2p9'});
})();
