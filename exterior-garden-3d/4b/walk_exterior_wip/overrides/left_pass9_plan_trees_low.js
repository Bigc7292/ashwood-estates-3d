// Left view, step 3 blockout pass 9 (critic on 58538c2): lower and thin the CAD plan-tree crowns (behind the wall) so they sit at the planting
// line and the verge trees' crowns read on their own. Plan-tree tops 2.6 m x variation -> 2.15 m x variation (just above the 2.0 m wall),
// half the leaf clusters, narrower spread. CAD trunk positions unchanged; verge trees unchanged. Display assumptions.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const O = window.MODEL_OVERRIDES; if (!O || !O.multiStemTrees) return;
  for (const t of O.multiStemTrees) if (/^left-canopy-/.test(t.id)) {
    t.top *= 2.15 / 2.6; t.clusters = Math.round(t.clusters * 0.5); t.spread *= 0.8; t.status += '; pass9_low_thin_behind_wall_assumption';
  }
})();
