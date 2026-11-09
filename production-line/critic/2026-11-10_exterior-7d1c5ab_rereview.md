# Critic L5: exterior re-review of lane/exterior 7d1c5ab (pool + rear/garden), 2026-11-10 (Asia/Dubai)

**Status: WIP.** Pushed per Colin's commit-every-edit order (01:28). Verdicts are not final yet.

Scope: answers to `2026-11-10_pool_review.md` (T1-T12, B1-B10) and `2026-11-10_exterior-rear-garden.md` (a, b, c, e). Pending, not judged: the water clip, the v6 side-by-side, Blender light/levels, and front item (d).
Standing rulings: M25 (CAD heights, 11.6 m tower); the olive per p12 applies to the GF courtyard only.

## Progress
- Own worktree `/workspace/pool-critic-ext` checked out at 7d1c5ab (detached, read-only).
- Builder claims (`pool_pass/water2_proof/RESULT.txt`): t5/t6 mean 5.27, shown/hidden mean 23.45. Critic note: their t5/t6 run uses `__frame(t, 10)`, which also moves the sun (k = t/T), and the glint layer scrolls separately, so their t5/t6 figure is not Water2-only. The critic re-test isolates them (T=0, glints frozen, Water2 hidden).
- Critic headless runs on this box: the SwiftShader GPU process crashed (dmesg: `Chrome_InProcGp trap int3`) on 3 attempts while a Blender job was using the CPU. Retrying with the GPU watchdog disabled.
- Pool footprint changed to 8.40 x 2.80 m and moved 1.84 m past the rear site line "per Colin override" (M29/M30). The critic cannot see Colin's message; the M29/M30 rows record it.
