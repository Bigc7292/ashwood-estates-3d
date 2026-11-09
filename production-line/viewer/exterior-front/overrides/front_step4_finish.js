// Front view, step 4 (finish) + M12 front-view display assumption.
// M12: ELEV-FRONT shows no roof-terrace volume above the front roof. Per Colin ("just do it, don't wait"), the RF block
// is hidden in the FRONT VIEW ONLY (display assumption, logged as M26 in the mismatch log; Colin can overrule).
// Finish: lit soffit LED lines (image-read from ELEV-FRONT: two lines in the carport soffit, one along its front edge,
// one along the roof soffit). Positions are assumptions. Concept visualisation only.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.hide_cats = ['rf_wall', 'rf_roof'];
window.MODEL_OVERRIDES.finish = true;
window.MODEL_OVERRIDES.add.push(
  {id:'led-carport-front', cat:'canopy', mat:'led', x0:0.3, x1:7.3, z0:29.0, z1:29.08, y0:2.57, y1:2.6, status:'step4_image_read_assumption'},
  {id:'led-carport-1',     cat:'canopy', mat:'led', x0:0.8, x1:6.8, z0:25.6, z1:25.68, y0:2.57, y1:2.6, status:'step4_image_read_assumption'},
  {id:'led-carport-2',     cat:'canopy', mat:'led', x0:0.8, x1:6.8, z0:27.3, z1:27.38, y0:2.57, y1:2.6, status:'step4_image_read_assumption'},
  {id:'led-roof-soffit',   cat:'canopy', mat:'led', x0:3.2, x1:15.4, z0:26.3, z1:26.38, y0:7.36, y1:7.4, status:'step4_image_read_assumption'}
);
