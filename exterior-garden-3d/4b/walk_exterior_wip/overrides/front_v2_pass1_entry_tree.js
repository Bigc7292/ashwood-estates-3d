// Front v2 pass 1 (critic on dc1edac: the entry tree from pass 16 is unverified Grok input).
// Checked against ELEV-FRONT at the locked camera (views/front_v2/shots/front_v2_tree_crop.png): the reference DOES show a small multi-stem
// tree behind the low wall right of the entry (thin stems, loose leafy dome), canopy top at row ~412 of 720 -> 3.35 m at the tree line
// (z 28.6, d 16.8 m; derived), so the tree is kept, not replaced by low planting. Its column already matches the reference (canopy centre at crop
// x ~337 vs ~335; a first try at x 13.85 overshot by ~55 px and was reverted). Fix: the canopy reads as a flat band of round blobs; top set
// to 3.35 m, spread narrowed 3.6 -> 3.2 m and more, smaller clusters so the dome reads looser. Position unchanged (x 12.85).
// The reference canopy also hangs down to the low wall on its right side (rows ~412-540): a second, lower multi-stem crown (top 2.4 m,
// x 13.9; assumption) fills that, so the tree reads as one loose dome from the wall top up, not a band on bare stems. Position/size: derived/assumption. Concept visualisation, not survey-verified.
(function(){
  for (const t of (window.MODEL_OVERRIDES.multiStemTrees || [])) if (t.id === 'front-right-multistem-tree') {
    Object.assign(t, {top:3.35, spread:3.2, clusters:560, status:t.status + '; front_v2_pass1 looser dome, top 3.35 m (derived)'});
  }
  window.MODEL_OVERRIDES.multiStemTrees.push({id:'front-right-multistem-tree-low', x:13.9, z:28.7, top:2.4, spread:2.6, stems:4, clusters:380, color:0x4a6a30, status:'front_v2_pass1 lower crown, image-read assumption'});
})();
