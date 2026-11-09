// Rear + garden views (ELEV-REAR, GARDEN-BACK, POOL), step 6 pass 1, lane 2, 2026-11-10.
// Appearance from the approved generated images + brochure p26; footprint/pool from approved CAD V4 via model.js (pool 9.50 x 2.40 m brochure / 9.49 x 2.38 CAD).
// Concept visualisation only. All heights, species and the off-plot lawn are display assumptions.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.finish = true;            // step 4 warm finish (same as front)
// Palms ("looks unnatural": generic ball trees). The references show date palms flanking the rear garden.
// Palms placed on the approved-plan tree symbols nearest the rear garden (CAD positions; height/species image-read assumption).
window.MODEL_OVERRIDES.remove_plain_trees = true;
window.MODEL_OVERRIDES.palms = [
  {id:'palm-rear-left',   x:1.03,   z:1.386, trunk:7.2, crown:3.6, lean:[ 0.03, -0.02], status:'plan tree symbol; palm look image-read (ELEV-REAR/GARDEN-BACK)'},
  {id:'palm-rear-right',  x:16.415, z:1.67,  trunk:7.8, crown:3.8, lean:[-0.03, -0.01], status:'plan tree symbol; palm look image-read'},
  {id:'palm-side-left',   x:0.888,  z:7.959, trunk:6.4, crown:3.2, lean:[ 0.02,  0.02], status:'plan tree symbol; palm look image-read'},
  {id:'palm-side-right',  x:17.978, z:9.06,  trunk:6.8, crown:3.4, lean:[-0.02,  0.01], status:'plan tree symbol; palm look image-read'}
];
// Off-plot context lawn behind the rear boundary: ELEV-REAR and p26 show a deep lawn; the plan's site outline ends ~1.2 m behind the pool.
// Shown as CONTEXT ONLY (logged in the mismatch log, image for look, CAD for footprint). Not part of the plot.
window.MODEL_OVERRIDES.add.push(
  {id:'context-lawn-rear', cat:'lawn', mat:'lawn', x0:-8, x1:26.7, z0:-26, z1:0, y0:-0.09, y1:-0.04, status:'off-plot context (image look), NOT PLOT'}
);
// Low hedge planting along the side boundaries (GARDEN-BACK shows planted edges, not bare walls). Image-read assumption.
window.MODEL_OVERRIDES.shrubRows = [
  {id:'rear-hedge-left',  x0:0.35,  z0:0.4, x1:0.35,  z1:10.0, h:1.3, r:0.40, color:0x4b6a31, status:'image_read_assumption'},
  {id:'rear-hedge-right', x0:18.35, z0:0.4, x1:18.35, z1:10.0, h:1.3, r:0.40, color:0x4b6a31, status:'image_read_assumption'}
];
