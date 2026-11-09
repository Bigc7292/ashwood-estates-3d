// Left view, step 3 blockout pass 6 (critic on 3b5b382): canopy volume and density on the same CAD trunks.
// ELEV-LEFT's trees read as dense masses ~60-120 px wide along the wall line; pass 5's canopies were thin clusters.
// Same trunk positions and tops; wider spread (x1.5), 3x leaf clusters, larger clusters (leaf x1.5) and a deeper crown (depth x2.2, builder
// option added in left_pass.html). Sizes are display assumptions. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const O = window.MODEL_OVERRIDES; if (!O || !O.multiStemTrees) return;
  for (const t of O.multiStemTrees) if (/^left-canopy-/.test(t.id)) {
    t.spread *= 1.5; t.clusters = Math.round(t.clusters * 3); t.leaf = 1.5; t.depth = 2.2; t.status += '; pass6_volume_assumption';
  }
})();
