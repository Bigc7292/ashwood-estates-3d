// Right view, step 3 blockout pass 2 (critic on 86c4d87): ELEV-RIGHT shows nothing above the FF slab line except the roof canopy.
// The model's RF walls and RF roofs (rf_wall, rf_roof; RF is NTS, M12 open) are hidden in this view only. Canopy, camera and lock unchanged.
// Display assumption (same treatment as M26 front / M33 left). Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.hide_cats = (window.MODEL_OVERRIDES.hide_cats || []).concat(['rf_wall', 'rf_roof']);
