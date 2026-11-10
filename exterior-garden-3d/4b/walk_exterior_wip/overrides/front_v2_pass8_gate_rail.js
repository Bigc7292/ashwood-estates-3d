// Front v2 pass 8 (critic on 90848d9): entry gate top rail and finer bar pitch, from ELEV-FRONT.
// Read from ELEV-FRONT at the locked camera (side-by-side panel, 1280x720 source rows): the gate's dense dark band starts at panel row ~442
// (top rail ~442-446) with the ground line at ~505; the model's 1.8 m gate top sits at row ~418 with ground at ~503, i.e. ~47.2 px/m, so the
// reference gate top is ~1.33 m (derived). Bars: ~19 dark minima across ~160 source px of the gate in the reference vs ~12 in the model,
// so the bar pitch goes from 21 to 14 texture px (bar width 8 -> 6). The gate's CAD footprint (x 7.39-9.735, z 29.881-29.961) is unchanged;
// only its display height (meta.heights_display_only.gate 1.8, an assumption) is replaced by the image-read 1.33 m. Colour from pass 7.
// Display assumption. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
(function(){ const O = window.MODEL_OVERRIDES, T = O.mat_tune || (O.mat_tune = {});
  Object.assign(T.bronze_bars || (T.bronze_bars = {}), {barPitch:14, barWidth:6});
  T.gate_rail = {from:'paving_inner', color:0x3a2c20, metalness:0.0, roughness:0.7, emissive:0x060403};
  O.remove.push('boundary-front-gate');
  O.add.push({id:'boundary-front-gate-v2p8', cat:'gate', mat:'bronze_bars', x0:7.39, x1:9.735, z0:29.881, z1:29.961, y0:0.0, y1:1.26, status:'cad_footprint_height_image_read_v2p8'},
             {id:'boundary-front-gate-rail-v2p8', cat:'gate', mat:'gate_rail', x0:7.39, x1:9.735, z0:29.871, z1:29.971, y0:1.26, y1:1.33, status:'image_read_v2p8_assumption'});
})();
