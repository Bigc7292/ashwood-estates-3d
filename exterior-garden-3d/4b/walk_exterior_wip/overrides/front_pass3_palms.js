// Front view, pass 3 (critic's one fix): palms replace the round placeholder trees.
// Positions and heights are image-read from ELEV-FRONT by back-projecting through the locked camera
// (front_lock.json): left palm group at the site's left edge, one palm at the right edge. Assumptions, not survey.
// Species: date palm look per the reference images. Concept visualisation only.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.remove_plain_trees = true;   // keep courtyard trees only
window.MODEL_OVERRIDES.palms = [
  {id:'palm-left-main',  x:0.0,  z:24.0, trunk:7.0, crown:3.6, lean:[ 0.04,0.00], status:'pass3_image_read_assumption'},
  {id:'palm-left-back',  x:-1.6, z:21.5, trunk:6.0, crown:3.0, lean:[-0.05,0.02], status:'pass3_image_read_assumption'},
  {id:'palm-right',      x:18.4, z:26.0, trunk:7.4, crown:3.6, lean:[-0.03,0.00], status:'pass3_image_read_assumption'}
];
