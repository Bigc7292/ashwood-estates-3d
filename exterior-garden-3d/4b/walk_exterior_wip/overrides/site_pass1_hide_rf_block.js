// Site/aerial view, step 3 blockout pass 1 (critic on 72ce002): RF block hidden in this view only.
// OUTDOOR-SITE shows a flat roof with no roof-floor volume and no roof canopy above it. Same treatment as M26 (front) and M33 (left):
// hide_cats rf_wall/rf_roof and remove the rf-canopy box, this view only. Logged under M42.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.hide_cats = (window.MODEL_OVERRIDES.hide_cats || []).concat(['rf_wall', 'rf_roof']);
window.MODEL_OVERRIDES.remove.push('rf-canopy');
