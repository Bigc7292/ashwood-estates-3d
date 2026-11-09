# Hand-off: FP-4B-FF r5, step 2 (Layout) only

Lane 3 (interior builder), branch `lane/first-floor`. Date 2026-11-10 (Asia/Dubai).
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.
**Status: REVIEW-PENDING (critic + Colin). Not DONE. Step 3 not started** (no materials, lighting or furniture models).
Answers critic report `production-line/critic/2026-11-10_ff-r4.md` (on `claude/rules-and-status`), defects 1-6 at layout level.

## Evidence
| Item | Path |
|---|---|
| Approved CAD used | `active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png` (render of `active/approved-cad-v4/svg/FP-4B-FF_V4_portrait.svg`; ACTIVE_PIPELINE.json id 4B-FF, approval pt16u). Unmodified. |
| (i) Clean CAD export (plan area, 4 px per SVG unit, crop of long7680 only) | `active/floorplan3d-spike/FP-4B-FF/r5_step2/FP-4B-FF_V4_cad_clean.png` |
| (ii) r5 trace on the same CAD, same scale, scale bar + envelope annotation | `active/floorplan3d-spike/FP-4B-FF/r5_step2/FP-4B-FF_r5_trace_on_V4.png` |
| r5 layout data | `active/floorplan3d-spike/FP-4B-FF/data/fp-4b-ff.plan.r5.json` (+ `.r5.js`, `const PLAN_R5`) |
| Builder (reproducible) | `active/floorplan3d-spike/FP-4B-FF/r5_step2/build_r5_layout.py` + `openings_u.json`, `furniture_u.json`; `_trace_u.json` = intermediate in SVG units |

Overlay colours: red walls, magenta label anchors, blue stair box + tread pitch, green doors, light-blue glazing, purple furniture footprints, cyan voids, orange room polygon, black envelope box.

## One transform (defects 1, 2)
All of WALLS, VOIDS, ANCHORS, ROOMS, STAIRS, DOORS, WINS and FURNITURE use one mapping from the SVG `source_diagram` group units (u = source crop px):
`X_mm = (u - 138) * 34.026`, `Y_mm = (v - 141) * 34.026` (x east, y plan-down; origin = NW corner of the envelope dimension lines).
- Scale SOURCE: SVG dimension line `M138,123 L523,123` (385 u) labelled "ENVELOPE ~ 13.1 m" → 13100 / 385 = **34.026 mm/u**.
- Cross-checks: vertical line `M120,141 L120,844` (703 u) labelled "~23.9 m" → 33.997 mm/u (-0.09 %); sheet scale bar (1 m = 33.670 page u, group scale 1.14695) → 34.064 mm/u (+0.11 %). r4 used 35.53 mm/u (+4.4 %).
- Labels are the SVG `<text>` positions through the same transform (previously a separate scale/origin). Check run: 0 anchors outside the envelope, 0 on the stair, 0 on a wall.

## (iii) Key dimensions: plan vs r5
| Dimension | Plan (V4) | r5 | Label |
|---|---|---|---|
| Envelope width | ~13.1 m (annotation) | 13.10 m (scale set to it) | SOURCE |
| Envelope depth | ~23.9 m (annotation) | 23.92 m | DERIVED (703 u × 34.026) |
| Traced wall bbox | (inside the envelope lines) | 12.98 × 23.89 m | MEASURED (raster poche) |
| r4 for comparison | — | 13.50-13.61 × 24.94 m | r4 (critic: +3-4 %) |
| Stair length | ~6.5 m (critic estimate) | 6.33 m (y 8.85-15.18 m) | MEASURED tread-box hairlines |
| Stair width | ~1.5 m | 1.51 m | MEASURED |
| Stair treads | not stated | ~21 at ~298 mm (15 lines visible) | DERIVED from pitch |
| Stair rise direction | no arrow | — | NOT FOUND |
| Master Suite clear span | 4.00 × 5.10 m | 3.95 × 5.07 m | label SOURCE / span MEASURED |
| M. Dressing clear span | 4.00 × 3.50 m | 3.98 × 3.49 m | as above |
| M. Bath clear span | 4.00 × 2.70 m | 3.95 × 2.71 m | as above |
| Family Living width | 4.00 m | 3.98 m | as above (depth open to corridor) |
| Bedroom 1 polygon | 4.00 × 5.10 † m (20.4 m²) | 3.96 × 5.60 m bbox, 20.84 m² | DERIVED polygon (bbox includes door recess) |
| Master Suite label anchor | text at SVG (199, 322) | (2.08, 6.07) m | r4 had (-1.24, 2.33) m |
| Junior Suite label anchor | text at SVG (415, 640) | (9.43, 16.89) m | r4 had (5.46, 12.18) m, on the stair |

The room spans land within 0-1.3 % of the stated room sizes, which supports the scale.

## Openings (defect 4: positions only, no 3D detailing)
11 doors and 10 glazing runs in `DOORS` / `WINS`, each with ends in mm, width, rooms, evidence and confidence (MEASURED on the raster, ±34 mm).
- Doors: Master Suite, Bedroom 1, Bath 1, Lift (low), M. Dressing passage, M. Bath (low), Bath 2, Bedroom 2, Junior Suite, J. Dress, J. Bath.
- Glazing: N facade Master Suite ×2, Family Living ×2, Bedroom 1; W windows M. Bath and Bath 2; E window Bath 1; S facade Bedroom 2 and Junior Suite.
- NOT FOUND or unconfirmed: the Dress door (a swing arc is visible near (3.3, 15.9) m, but the leaf position is not resolved). Swing directions are not recorded.

## Furniture footprints (defect 5: 2D only)
9 footprints from the V4 SVG vector symbols: double beds (Master Suite, Bedroom 2, Junior Suite), 2 singles (Bedroom 1), L-sofa (2 rects), coffee table, round table (Family Living).
NOT TRACED in r5 (raster-only symbols): bath tub, WCs, basins, wardrobes or joinery, armchair and side table in the Master Suite. These are listed for the next pass. No models were made.

## Defect 6
No potted plants anywhere in the r5 data (`excluded` field). r5 has no viewer, so nothing is rendered.

## Voids
- Courtyard void: from the SVG overlay rect (389, 428, 129 × 107 u). Walls on N/W/S traced.
- Two "OPEN TO BELOW" boxes: measured on the raster (±1-1.5 u).

## Open items / blockers
- **Room polygons (critic defect 2):** only Bedroom 1 seals cleanly. 13 rooms are in `ROOMS_NOT_DERIVED` with the reason. Family Living opens onto the corridor in the plan, and several bath and dress partitions are thin or unpoched joinery, so the flood fill leaks. Anchors are exact; polygons are deferred, not invented.
- No `standalone_r5.html`. The r4 viewer has hard-coded GF furniture, including the plants, so a viewer is step 3 work.
- `STEPS.md` is not updated (step 2 stays WIP until the critic and Colin pass it).
- Optimizer checks (run on this worktree): `verify_incremental.py` gave 0 warnings and 0 missing paths. `handoff_guard.py` gave 0 breaches, 0 blocked and 35 style-overlap warnings. Output files were restored and not committed.
