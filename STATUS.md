# Current status (handoff)

Checked 2026-11-09 21:30 Asia/Dubai. Read with `AGENTS.md`. Update this file at the end of every session.

## Where the work is
- GitHub: `Bigc7292/ashwood-estates-3d` (private). Last work snapshot: `main` @ `6f55b79` (2026-11-09 16:39 Dubai, "WIP: final agent reports").
- Origin: Axis3D plan, Ashwood = scenario test 1 (`Bigc7292/legacy-archive`, branch `axis3d-plan`, folder `axis3d/`).
- Earlier work ran in Claude desktop sessions "Legacy project setup" and its fork; those chats are not needed to continue.

## Done
| Area | State | Where |
|---|---|---|
| Brochure + 9 approved V4 floor plans (4/5/6-bed × GF/FF/RF) | Approved (`pt16u`), backed up | `active/approved-cad-v4/`, `ACTIVE_PIPELINE.json` |
| 4-bed exterior steps 1–4 (reference, layout, blockout, grime) | Done, revised after review, awaiting Colin's review | `exterior-garden-3d/4b/`, `PIPELINE_7STEP.md` |
| Exterior step 5 (printed matter) | **GO** (Colin, 2026-11-09 17:40): run through to step 7 | |
| 4-bed GF web viewer v2 | Built (v1 rejected as "too 2D"); review-pending | `active/floorplan3d-spike/FP-4B-GF/` |
| Pool basin (browser sketch) | Built | `exterior-garden-3d/4b/model/` |

## Unreviewed WIP (from interrupted sub-agents; needs critic review before sign-off)
| Item | What exists | Evidence |
|---|---|---|
| GF viewer polish (furniture styling, feature walls, entry ceiling, pool basin, lighting, faster walk) | Code in the viewer | `active/floorplan3d-spike/FP-4B-GF/verify/gf_polish_2026-11-09/` (before/after/compare) |
| Courtyard module | `courtyard_feature.js` + `courtyard_test.html`; **not integrated** into the viewer; no written notes | `verify/courtyard_2026-11-09/` |
| Blender realism pass M20–M24 (sky, grass, interiors behind glass, hedges, trees, palms, pool edge, eye-level cameras) | Built only into `exterior-garden-3d/4b/blender_wip/`; official blends untouched | `exterior-garden-3d/CHANGELOG.md`, mismatch log |
| Explorable 4-bed web model | Only the ground floor exists; FF and RF not started | |

## 7-step loop tracker (Colin, 2026-11-09 23:07: start at 1, run to 7, loop until done)
Updated 2026-11-09 23:15 Dubai by the integrator. These are the integrator's reading of each lane, and the lanes have been asked to confirm.
| Lane / item | Current step | Loop | Latest output | Gate |
|---|---|---|---|---|
| Exterior 4B, Blender (official renders) | 6 Critique (step 5: none in source) | 1 | `blender_wip/build_scene_f1.py`, not rendered | Needs a render on Colin's PC |
| Exterior 4B, walkable web (exterior lane; fixer's v5/v6 retired in its favour) | 6 Critique, front camera passes | 1 | `walk_exterior_wip/front_pass.html` | REVIEW-PENDING |
| Fixer: F2 entry streak (GF) / F1 glazing (ext) | 3 and 6 / 4 | 1 | in progress / not started | — |
| Interior GF viewer v2 | 4 Finish done; 5 Printed matter next | 1 | `FP-4B-GF/index.html`, `courtyard_feature_r2.js` not integrated | REVIEW-PENDING |
| Interior FF | 2 Layout (lane-confirmed; doorways closed by hand, ASSUMED); step 1 logged in `FP-4B-FF/STEPS.md` | 1 | `FP-4B-FF/standalone_r4.html` | CRITIC-FAIL on the last check; r4 not re-checked |
| Interior RF | 1 Reference not started | 0 | — | — |

## Open issues
- **M24 OPEN:** rear GF stone pier / FF stone panel may be mirrored vs brochure p26 (check the M16 reading first).
- M12 open (RF core position).
- Step 3/4 re-render was interrupted: some step-3 raw renders and all step-4 renders/comparisons are from the earlier pass.
- `exterior-garden-3d/4b/blender/build_scene.py` does not compile (missing comma, `palmleaf=` line). The fixed copy is `blender_wip/build_scene_f1.py`; run that one for F1 renders.
- First-floor walls viewer (`FP-4B-FF/`) merged but CRITIC-FAIL: interior partitions and courtyard void walls missing, scale unreconciled. Re-trace in progress. Review bar (Colin): FF must match GF viewer v2 in rooms, furniture, materials, full-height walls and lighting, as well as the approved FF plan.
- Walkable exterior v3: aerial view uses generic trees and grey ground, not the approved palms; other angles unchecked.
- `.venv/` is committed (Colin's choice, 2026-11-09), so the repo is ~2.4 GB.

## Agreed plan (draft, 2026-11-09, waiting for Colin's edits)
1. Critic review of the 16:39 WIP snapshot against the V4 plans and brochure.
2. Fix review findings, then integrate the courtyard module into GF viewer v2.
3. Finish the explorable 4-bed web model (all floors, walkable).
4. Exterior steps 5–7 (printed matter, critique, motion), run straight through; then write up Ashwood lessons for the Axis3D QA register.
