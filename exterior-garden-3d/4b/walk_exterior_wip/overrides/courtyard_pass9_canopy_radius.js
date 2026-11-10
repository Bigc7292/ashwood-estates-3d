// courtyard pass 9 (lane exterior-roof-courtyard): halve the courtyard tree canopy radius (tree-13 at the pool planter).
// Position of the tree (planter centre, CAD-derived) is unchanged; only the canopy display radius changes. ASSUMPTION for display.
(function () {
  if (!window.MODEL || !MODEL.trees) return;
  MODEL.trees.forEach(function (t) { if (t.courtyard) { t.r_orig = t.r; t.r = +(t.r * 0.5).toFixed(3); } });
})();
