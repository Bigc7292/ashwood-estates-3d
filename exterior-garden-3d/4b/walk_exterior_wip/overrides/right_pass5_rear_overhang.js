// Right view, step 3 blockout pass 5 (critic on fe0b1f0, fix (b)): the lower rear overhang beyond the main wall end.
// ELEV-RIGHT (1280x720) shows a flat slab projecting past the main wall end (x 1036) out to x ~1122, fascia rows ~260-278, with its soffit
// running back to meet the wall at row ~325. At the locked right camera (960x540 panel, row = 270 - 742*((Y-1.6)/d - 0.1145)):
//   fascia on the right facade line (x 15.85, d 26.75 m): rows 195-208 -> y 7.38 top, 6.91 underside (derived);
//   right end, panel col 841 vs wall end 777 at d 26.75 -> 64 px * 0.0361 m/px = 2.31 m past z 2.84 -> z 0.53 (derived);
//   soffit meets the wall at panel row ~244 -> d 35.5 m -> x ~7.1 (derived).
// The V4 CAD draws no slab here (rear FF balcony x 2.95-15.78, z 2.96-4.6 only), so this is an image-read display assumption, this view
// only, logged as M38. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.add.push(
  {id:'right-rear-overhang', cat:'canopy', mat:'soffit', x0:7.1, x1:15.85, z0:0.53, z1:2.84, y0:6.91, y1:7.38, status:'right_pass5_image_read_derived_M38'}
);
