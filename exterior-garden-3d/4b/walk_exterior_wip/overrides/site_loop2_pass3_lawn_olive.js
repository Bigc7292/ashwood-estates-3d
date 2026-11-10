// Site loop 2 pass 3 (critic on 474bc05): lawn strips from khaki to the reference's green-olive.
// Sample: OUTDOOR-SITE rear lawn strip beside the pool (side-by-side panel x 1330-1590, rows 68-80; green-dominant pixels):
// median RGB 71,69,33 (R ~ G, green-olive). Model before (site step 4 pass 2, 0x948646): right strip median 104,95,40 (R > G, khaki).
// The step 4 pass 2 sample (lawn ~RGB 88-120, 71-102, 28-43) included sun-washed patches; this pass follows the critic's read of
// the inner lawns. Lawn extents unchanged (CAD + shared pool v3). Uses the site page's mat_flat hook. Display assumption.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.mat_flat = Object.assign(window.MODEL_OVERRIDES.mat_flat || {}, {lawn: 0x777643});
