# Current status (handoff)

Checked 2026-11-10 02:10 Asia/Dubai. Read with `AGENTS.md`. Update this file at the end of every session.

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
Refreshed 2026-11-10 02:10 Dubai by the integrator, from the lane step logs after the catch-up merge.
| Lane / item | Current step | Loop | Latest output | Gate |
|---|---|---|---|---|
| Exterior front view | 6 Critique, loop 2: **WAITING ON COLIN'S DECISION** | 2 | Last lane pass is 16 (`50ec220`). Pass 17 (`front_pass17_critic_d.js`, loaded by `front_pass.html`) came from an outside Grok agent on lane/exterior. It failed step 6 (terracotta instead of cream travertine, dusk light, camera off lock) and is **not** the accepted front state. It stays in the tree, and nothing is overwritten | CRITIC-FAIL (pass 17) |
| Exterior left side view (our exterior lane, now working here) | started | 1 | — | — |
| Exterior rear + garden (lane/exterior) | 6 Critique, pass 3 (Water2 pool reflections) | 1 | `walk_exterior_wip/rear_pass.html`, `views/rear`, `views/garden` | REVIEW-PENDING. The integrator's headless check crashed in software GL, so not yet verified |
| Exterior step 7 motion | 7, provisional 10 s video | 1 | `4b/step7_motion/EXT-4b_STEP7_garden-pool_motion_PROVISIONAL.mp4` | Provisional, critic reviewed with the rear passes |
| Exterior Blender (F1) | Box render of the F1 script done | 1 | `blender_wip/f1_box_render/`, `build_scene_f2_pool.py` | REVIEW-PENDING |
| Pool (M29/M30, Colin: image overrides CAD, garden enlarged) | 6 | 1 | `4b/pool_pass/` (Water2 proven by frame diffs) | REVIEW-PENDING |
| GF interior (lane/gf-interior) | 6 Critique (5 none in source); r3 with F2 + Q7 courtyard | 1 | `FP-4B-GF/index_r3.html` | r3 step 6 CRITIC-FAIL, back to fixes |
| FF interior (lane/first-floor) | 2 Layout, r5L; steps 3–7 cleared to go | 2 | r5L files (label anchors fixed), `FP-4B-FF/STEPS.md`. Scale settled at 35.53 mm/px (assumption); the outside r6/r7 files used 34.03 and are not applied | REVIEW-PENDING |
| RF (lane/roof-floor) | 3 Blockout (step 2 passed on the dimension check; RF walls extracted from the approved sheet) | 1 | `FP-4B-RF/STEPS.md`, `b3b889e` | In progress |
| Interior refs (lane/interior-refs) | Q11 reference sets GF/FF/RF | 1 | `production-line/interior-refs/` | GF r2 9 pass / 6 fail; FF/RF 14 pass / 4 fail |
| Viewer hub (lane/4-viewer) | Checks + hub pages | 1 | `production-line/viewer/` | REVIEW-PENDING |
| Public WIP preview (lane/preview) | Deployed by that lane (says Colin authorised, pt65u) | — | https://ashwood-preview.vercel.app | — |

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
