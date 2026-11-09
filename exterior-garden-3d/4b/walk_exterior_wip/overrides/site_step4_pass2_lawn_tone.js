// Site/aerial view, step 4 finish pass 2 (critic on 1d7c1b7): muted lawn tone.
// Reference lawn (OUTDOOR-SITE rear and side strips) samples ~RGB 88-120, 71-102, 28-43 (olive, low warm sun). The model's textured lawn
// renders ~RGB 53, 88, 20 (bright saturated green). Lawn material set to a flat olive in this view (page hook mat_flat); extents unchanged.
// Hex chosen so the lit render lands in the sampled range (checked after render: 0x7a6e30 gave ~RGB 76,69,20, too dark; 0x948646 used). This view only.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.mat_flat = Object.assign(window.MODEL_OVERRIDES.mat_flat || {}, {lawn: 0x948646});
