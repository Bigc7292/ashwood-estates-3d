// courtyard pass 12 (lane exterior-roof-courtyard): VIEW-ONLY glass treatment for the OUTDOOR-COURTYARD page.
// The model glazing (mat 'glass', e.g. gf-glass-6 behind the pond) reads as solid stone at this distance.
// This flag makes the page's glass material more opaque and double-sided for this view only. Model geometry unchanged.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {});
window.MODEL_OVERRIDES.courtyard_glass = true;
