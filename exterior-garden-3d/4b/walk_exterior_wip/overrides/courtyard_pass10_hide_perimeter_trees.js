// courtyard pass 10 (lane exterior-roof-courtyard): VIEW-ONLY treatment for the OUTDOOR-COURTYARD page.
// Hides the perimeter placeholder trees (tree-1..12, outside the courtyard bay) so only walls and sky sit beyond the courtyard,
// as in the approved reference. The courtyard tree (courtyard:true) is kept. Uses the page's existing remove_plain_trees switch.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {});
window.MODEL_OVERRIDES.remove_plain_trees = true;
