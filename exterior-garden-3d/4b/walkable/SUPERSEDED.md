# walkable_v4 (and v5/v6): FROZEN, SUPERSEDED (2026-11-10, lane 2, per critic batch (e))

`walkable_v4.html` (on `claude/rules-and-status`, not on `lane/exterior`) is frozen: no further edits, not an input, not shown as current.
Critic verdict: CRITIC-FAIL 3/10 (Water2 not visible). The root cause also affected the lane-2 pages: Water2 was built on geometry rotated in place,
so its Reflector/Refractor planes were wrong and contributed nothing.
Current exterior web pages: `walk_exterior_wip/front_pass.html` (front) and `walk_exterior_wip/rear_pass.html` (rear, garden, pool; Water2 fixed and
proven by frame diffs in `pool_pass/water2_proof/RESULT.txt`).
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.
