// Left view, step 3 blockout pass 7 (critic on 353274e): canopy tops to the reference row and softer green.
// ELEV-LEFT's tree tops sit ~row 365 of the 960x540 panel (~1.3 m above the 2.0 m wall top at the plan-tree depth, ~31 px/m), under the FF slab line;
// pass 6 tops reached ~315. Tops scaled to 2.6 m x the per-tree variation (3.2 m first try still ~20 px high) (was 3.9 m x variation); width and mass kept; colours moved toward the
// reference's soft olive green. CAD trunk positions unchanged. Display assumptions. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const O = window.MODEL_OVERRIDES; if (!O || !O.multiStemTrees) return;
  const greens = [0x6b7f45, 0x768a4e, 0x627a40]; let i = 0;
  for (const t of O.multiStemTrees) if (/^left-canopy-/.test(t.id)) {
    t.top *= 2.6 / 3.9; t.color = greens[(i++) % 3]; t.status += '; pass7_top_row_and_tone_assumption';
  }
})();
