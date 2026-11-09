# Hand-off: Lane 4 viewer optimization (Q-lane4)

**Lane:** 4-viewer (Optimizer Bot)  
**Branch:** `lane/4-viewer`  
**Status:** REVIEW-PENDING  
**Date:** 2026-11-10 (Asia/Dubai)

## What changed
New files under `production-line/viewer/` only. Builders' sources untouched.

### Live exterior (this update)
- Optimized fork of `lane/exterior` `walk_exterior_wip/front_pass.html` + 16 overrides → `production-line/viewer/exterior-front/`.
- Shared local three.js vendor; `data/model.min.js`; PR cap; one-shot shadow bake; demand-render; no CDN; no geometry edits.
- `production-line/viewer/exterior/` (walkable_v6-based) marked **SUPERSEDED** (`exterior/SUPERSEDED.md`); kept, not deleted.

### Also present
- GF / FF optimized forks (unchanged this turn).
- `check.sh` PASS (gates exterior-front as live exterior).

## Evidence
- `baseline/front_pass_before_after.json`
- `baseline/before.json` / `after.json`
- `bash production-line/viewer/check.sh` → PASS

## front_pass before → after
| Metric | Source (lane/exterior) | Lane4 opt |
|---|---|---|
| HTML | 28,869 B | 31,575 B |
| MODEL JS | 123,732 B | 107,945 B (min) |
| Headless load (`?view=front`) | 22,817 ms | 19,239 ms |
| Draw calls | 1,201 | 1,201 |
| Tris | 68,656 | 68,656 |
| Console errors | 0 | 0 |
| shadow autoUpdate | true | false (baked) |
| pixelRatio | 1 | ≤1.5/1 (headless 1) |

## Open / blocked
- RF viewer still absent.
- FF opt fork unchanged this turn.
- Walkable_v6 fork superseded but retained.

## Ask of critic
Confirm exterior-front matches live front_pass look (overrides 1–16). Geometry must be unchanged (calls/tris equal).

## Ask of integrator
Merge `lane/4-viewer` when critic passes. Use `exterior-front/` as the live exterior viewer path; ignore superseded `exterior/`.
