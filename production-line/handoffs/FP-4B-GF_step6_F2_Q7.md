# Hand-off: FP-4B-GF (4-bed ground floor), F2 + Q7 + step 6 critique pack, loop 1

Lane: L3 Interior builder. Branch: `lane/gf-interior`. Written 2026-11-10 (Asia/Dubai).
**Status: REVIEW-PENDING.** Nothing is marked DONE. Step 7 (walkthrough video) not started.
Concept visualisation, not survey-verified, not construction-ready, not certified CAD.

## What changed
All new files. `index.html`, `data/`, `ACTIVE_PIPELINE.json`, `active/approved-cad-v4/`, `superseded_2026-11-09/` are untouched (sha256 of the index.html the build reads is stamped in `index_r3.html` line 2).

| Item | Files (all under `active/floorplan3d-spike/FP-4B-GF/`) | What |
|---|---|---|
| F2 entry travertine streak (Q4 FIX) | `f2_entry_travertine.js` | New procedural texture used only on the entry west wall clad (plan x 6040, y 16113-19169) and its double-height void lining. Soft partial-width mottling, faint short veins, 1.2 x 0.6 m slabs in stretcher bond, mipmapped. Replaces ~90 full-width high-contrast stripes that aliased into radial streaks in perspective. Dining wall travertine (Q4 PASS) unchanged. |
| Q7 courtyard as a separate build file | `q7_courtyard_wire.js` | Wires `courtyard_feature_r2.js` (F3 pine + long low bench) into the viewer. Pond and island come from the V4 `PLAN.WATER` rectangles. Water is the vendored three.js r160 Water2 (`vendor/three/examples/jsm/objects/Water2.js`). In the r3 build it replaces the interim lite pond, island planter and olive tree. `?q7=0` switches back to the interim feature, and `?bench=0` hides the bench. |
| r3 build | `build_r3/build_index_r3.py` -> `index_r3.html` | 11 anchored string patches on a copy of `index.html` (imports, `travEntry` material, entry clad, void lining UV and material, skip interim pond, skip interim olive, add courtyard, per-frame sway, QA hook `__FP3D_QA__.r3()`, banner). The build fails if an anchor is missing, and the output is written to a temp file and then moved. Run from `FP-4B-GF/`: `python3 build_r3/build_index_r3.py`. |
| Step 6 critique pack | `build_r3/capture_r3.cjs`, `build_r3/compose_sbs.py`, `verify/r3_2026-11-10/` | 37 eye-level cameras, each rendered on index.html (before) and index_r3.html (after). Side-by-side sheets show the V4 plan crop with the room polygon and view cone, the r3 render, and the brochure or concept reference, with a p17 board and p24 Interior (Summary) strip. Gate log: `verify/r3_2026-11-10/STEP6_GATE_LOG.md`. |

## Evidence: side-by-sides (`active/floorplan3d-spike/FP-4B-GF/verify/r3_2026-11-10/sbs/`)
- Rooms (all 16 GF rooms; entry and courtyard included): `sbs_living-dining.jpg`, `sbs_living-dining_rev.jpg`, `sbs_show-kitchen.jpg`, `sbs_kitchen_rev.jpg`, `sbs_pantry_rev.jpg`, `sbs_k-store_rev.jpg`, `sbs_powder_rev.jpg`, `sbs_laundry.jpg`, `sbs_dress_rev.jpg`, `sbs_maid-room.jpg`, `sbs_maid-bath_rev.jpg`, `sbs_double-height-entry.jpg`, `sbs_office-gym.jpg`, `sbs_bath.jpg`, `sbs_multipurpose_rev.jpg`, `sbs_lift_rev.jpg`, `sbs_outdoor-terrace.jpg`
- F2 before/after (same camera): `f2_before_after_f2_entry_wall_oblique.jpg`, `f2_before_after_f2_entry_void_up.jpg`, `f2_before_after_room_double-height-entry.jpg`
- Q7 before/after/concept: `q7_courtyard_q7_courtyard_from_living.jpg`, `q7_courtyard_q7_courtyard_from_south.jpg`, `q7_courtyard_q7_courtyard_from_entry_side.jpg`, `q7_courtyard_room_outdoor-terrace.jpg`
- Reference board: `ref_board_p15_p16_p17_p24.jpg`
- Raw renders: `before/*.png`, `after/*.png` (both directions per room, `_rev` = reverse). Cameras and run info: `after/capture_meta.json`, `before/capture_meta.json`

## Value labels
| Value | Label |
|---|---|
| Room layout, walls, openings, pond 10019-14177 x 8723-12418 mm, island 11228-12649 x 9860-11281 mm, entry wall x 6040 y 16113-19169 | source: approved V4 GF trace (`data/fp-4b-gf.plan.js`) |
| Room polygons, areas | derived (README) |
| Tree position = island centre | derived (V4 draws a tree symbol on the island) |
| Wall height 3.0 m, eye height 1.6 m, entry lining 6.0 m | display assumption (the 6.0 m lining is unsourced, per Q4) |
| Travertine slab 1.2 x 0.6 m, stretcher bond, tone | slab size and bond: assumption. Tone: read by eye from the p17 travertine swatch |
| Pond depth 0.35 m, water line -0.045 m, coping +0.25 m, tree ~2.5 m tall / ~3.3 m crown, Water2 res 512 | assumption (DA1-DA11 in `courtyard_feature_r2.js`; res = perf assumption) |
| Bench 2.00 x 0.38 x 0.40 m at plan (9775, 9153) | ASSUMPTION: only in the approved concept image, not drawn on the V4 plan |
| QA camera positions | assumption (auto rule in `capture_r3.cjs`) |
| Lift finish | NOT FOUND |

## Checks
- `python3 scripts/verify_active_pipeline.py`: exit 0, approved_input_count 9, approved_artwork_hashes_unchanged true, missing_referenced_paths [], fallback_enabled false, retired_archive_is_input false.
- `python3 optimizer/handoff_guard.py`: records 112, breaches 0, blocked 0, warnings 35 (style_overlap 35, ambiguous 35, unknown 77, verified 0). These are the overlay's standing style-overlap flags, not new.
- `python3 optimizer/verify_incremental.py` (full): 2448 refs checked, missing 0, stale 0, warnings 0.
- The optimizer outputs rewrite tracked files outside this lane (`optimizer/*.json`, `active/pipeline_verification.json`). Copies are saved in `verify/r3_2026-11-10/optimizer/` and the tracked originals were restored, so the integrator can decide whether to commit refreshed reports.
- `node --check` passes on both new modules. Headless run: 0 console errors and 0 external requests on both builds.
- SwiftShader bench at the last courtyard camera: before 2.0 ms/frame, after 5.6 ms/frame (the courtyard Water2 adds reflection and refraction passes). These are CPU-renderer numbers, not phone or GPU numbers.

## Commits
- `7bde426`: F2 + Q7 r3 build (code)
- the critique-pack commit that adds this note (see `git log` on `lane/gf-interior`)

## Open issues (for the critic and integrator)
1. **Tree species conflict:** `index.html` and README cite brochure p12 for an olive tree in the courtyard, but the approved concept image (and Q4) shows a cloud-pruned pine. r3 uses the pine. This needs a mismatch-log row (lane 1) and Colin's call.
2. **Bench** is an assumption from the concept image only. Keep or drop (`?bench=0`).
3. **Pool water** stays on the existing `lite` default (`?water=water2` gives Water2). Only the courtyard is always Water2. The lane rule says "water surfaces use Water2", so this needs a decision on perf vs rule.
4. **Water2 frame cost:** the courtyard Water2 raises the frame time about 2.8x on SwiftShader. Check on a phone before promoting r3.
5. **p24 says "Feature Wall: Calacatta marble"**, while the entry and dining feature walls are travertine (p17 board, p12). This conflict was already there and is shown on every sheet.
6. **Dress:** the p15 dressing render shows glass-front wardrobes and an island, which the viewer does not model (only what the V4 plan draws). The critic should check whether the V4 dress symbol supports joinery.
7. **Rooms with no interior render** in p15-p17 (kitchen, pantry, K. store, wet rooms, lift, office/gym, multipurpose) are compared only against the p17 board and the p24 text.
8. Entry ceiling 6.0 m and walk speed 3.2/7.0 m/s are still unsourced (Q4). r3 does not change them.
9. `production-line/interior/gf/STEPS.md` is not updated (outside this lane's write scope for this item). The gate is logged in `verify/r3_2026-11-10/STEP6_GATE_LOG.md`.
10. `index_r3.html` is a generated copy. If `index.html` changes, re-run the build. If the critic passes, the integrator decides whether to fold the patches into `index.html`.
