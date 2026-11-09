# Hand-off: FP-4B-FF r6, step 2 (Layout) only

Lane 3 (interior builder), branch `lane/first-floor`. Date 2026-11-10 (Asia/Dubai).
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.
**Status: REVIEW-PENDING (critic + Colin). Not DONE. Step 3 not started.**
Answers `production-line/critic/2026-11-10_ff-r5-step2.md` (origin/claude/rules-and-status @ d3e35b0), fixes 1-6. The r5 transform, scale, stair, labels and walls are unchanged (they passed).

## Evidence
| Item | Path (under `active/floorplan3d-spike/FP-4B-FF/`) |
|---|---|
| Approved CAD used | `active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png` (from `.../svg/FP-4B-FF_V4_portrait.svg`, ACTIVE_PIPELINE 4B-FF, pt16u), unmodified |
| Clean CAD export (plan area, 4 px per SVG unit) | `r6_step2/FP-4B-FF_V4_cad_clean.png` |
| r6 trace overlay (walls, labels, stair, doors + hinge ticks, windows, fixtures, voids, closures dashed, E1) | `r6_step2/FP-4B-FF_r6_trace_on_V4.png` |
| Rooms-fill overlay (14 polygons with traced vs plan area, closures labelled "derived") | `r6_step2/FP-4B-FF_r6_rooms_fill_on_V4.png` |
| Critic-script self-check (critic_overlay_r5.py repointed to r6 JSON) | `r6_step2/selfcheck/selfcheck_r6_{full,north,south}.png`, `selfcheck/critic_selfcheck_r6.py` |
| Evidence crops (SVG-unit grid) | `r6_step2/evidence/{D4_lift_door,W9_bed2_south,E1_void_west_edge,W1_N_glazing_symbol_compare,Bath1_area_miss,D12_dress_door}.png` |
| Data | `data/fp-4b-ff.plan.r6.json` (+ `.r6.js`, `const PLAN_R6`) |
| Builder and inputs | `r6_step2/build_r6_layout.py`; `rooms_u.json`, `closures_u.json`, `openings_u.json`, `openings_other_u.json`, `furniture_u.json`; arc scoring `arc_score.py` → `arcs.json`. Work helpers `wall_face_scan.py` and `evidence_zoom.py` expect the 4 px/u crop (= `FP-4B-FF_V4_cad_clean.png`) as `work.png`. |

## Fix 1: room polygons (14 of 14)
Each polygon sits on wall faces measured by scan lines across the V4 raster poche. Door and window gaps are closed on the wall line. Where the plan has no wall, I closed the polygon on a drawn line and labelled the segment DERIVED in `CLOSURES`:
- **C1** Family Living / Corridor (open plan): y = 349 u, on the line of the M. Dressing north wall and the lift north wall.
- **C2** Corridor / courtyard-void edge: on the drawn double line at x 370.8 u.
- **C3** Corridor / OPEN TO BELOW: on the drawn top edge of the void box.
- **C4** J. Dress / Junior Suite: on the continuation of the J. Bath south wall (y 640 u).

| Room | Plan (stated) | Plan m² | r6 m² | Δ | ±5 % |
|---|---|---|---|---|---|
| Master Suite | 4.00 × 5.10 | 20.40 | 19.75 | -3.2 % | ok |
| Family Living | 4.00 × 5.10 | 20.40 | 20.47 | +0.3 % | ok (C1) |
| Bedroom 1 | 4.00 × 5.10 † | 20.40 | 20.82 | +2.1 % | ok (includes the wardrobe recess) |
| M. Dressing | 4.00 × 3.50 | 14.00 | 13.84 | -1.2 % | ok |
| M. Bath | 4.00 × 2.70 | 10.80 | 10.70 | -0.9 % | ok |
| Corridor | 3.30 × 10.10 | 33.33 | 32.71 | -1.9 % | ok (C1, C2, C3; stair inside) |
| Lift | 1.50 × 1.70 | 2.55 | 2.44 | -4.4 % | ok |
| **Bath 1** | 3.00 × 2.30 † | 6.90 | **5.61** | **-18.7 %** | **MISS** |
| Bath 2 | 2.30 × 2.50 | 5.75 | 5.64 | -1.9 % | ok (includes the WC cubicle) |
| Dress | 1.70 × 2.00 | 3.40 | 3.44 | +1.1 % | ok |
| Bedroom 2 | 3.90 × 4.30 | 16.77 | 16.88 | +0.6 % | ok |
| J. Dress | 2.00 × 2.80 | 5.60 | 5.43 | -3.1 % | ok (C4) |
| J. Bath | 2.50 × 2.60 | 6.50 | 6.24 | -4.0 % | ok |
| Junior Suite | 4.60 × 4.00 † | 18.40 | 18.30 | -0.5 % | ok (C4) |

Flags:
- **Bath 1 MISS.** Measured between walls, the main bay is 2.94 × 1.46 m (x 424.8-511.2, y 368-417.5 u) and the door bay is 1.08 × 0.61 m. The plan label carries †, so the plan itself marks the value as uncertain. Giving Bath 1 the wardrobe recess (x 459.8-511.2, y 350-368 u) would bring it to about 6.58 m² (-4.6 %). But that recess is drawn as a wardrobe opening into Bedroom 1, and Bedroom 1 matches only with it. Left as a MISS for Colin. Crop: `evidence/Bath1_area_miss.png`.
- **Junior Suite label on C4.** The SVG label text (y 634-649 u) straddles C4. C4 is placed where both J. Dress (2.00 × 2.80) and Junior Suite (4.60 × 4.00) match their stated sizes; moving it below the label puts both rooms outside ±5 % (+9 % and -9 %). The anchor sits about 2.5 u north of C4, inside J. Dress.
- **Unassigned strip.** The strip between the drawn void-edge line and the courtyard void rect (x 376-389, y 420-552 u) is in no room; it is beyond C2.

## Fix 2: Dress door and swings
- **D12 Dress → Bedroom 2:** a gap in the Dress south wall, y 610 u, x 222-237 u (0.51 m). Confidence low. Crop: `evidence/D12_dress_door.png`.
- **How swings were read:** I scored 4 hypotheses per door (hinge at either jamb × opening to either side) by sampling the quarter arc of radius equal to the door width, from 12 to 78 degrees, for a drawn line darker than its surroundings. A swing is READ only when the best score is at least 0.65 and leads the runner-up by at least 0.25. Scores are in `r6_step2/arcs.json`.

| Door | Hinge (mm) | Opens toward | Score (runner-up) |
|---|---|---|---|
| D1 Master | south jamb (7685, 7008) | west, into Master Suite | 0.96 (0.65) |
| D2 Bedroom 1 | south jamb | east, into Bedroom 1 | 1.00 (0.43) |
| D3 Bath 1 | west jamb | south, into Bath 1 (the drawn leaf line agrees) | 0.91 (0.26) |
| D7 Bath 2 | north jamb | west, into Bath 2 | 1.00 (0.35) |
| D9 Corridor → J. Dress lobby | north jamb | east | 0.70 (0.43) |
| D8 Bedroom 2, D10, D11, D12 | — | **NOT FOUND**: arcs too faint or occluded to separate hypotheses | 0.43-0.65 (top two within 0.25) |
| D4 Lift, D5 M. Dressing, D6 M. Bath | — | no arc drawn (lift door; open passage; leaf hairline only) | — |

D10 is now recorded as an opening inside J. Dress (between the wardrobe zone and the lobby), because the stated 2.00 × 2.80 m needs J. Dress to run to C4.

## Fix 3: D4 lift door, resolved
The lift door is in the **west** wall of the lift, at x 371 u, y 365-390 u (0.85 m; mm a = (7928, 7622), b = (7928, 8472)). It opens to the corridor.
- Scan h360 shows the lift west wall present at x 368.5-375.
- Scan h380 shows no poche at x 368-375, which is the gap.
- The lift north wall at y 347-354 u is continuous poche from x 368 to 428 (scan v395: 344.5-353.8; v410: 347.5-353.8), so there is no door toward Bedroom 1.
- The r5 "D4" was the thin double line north of the lift (y 341-344 u), which is outside the lift wall.

Crop: `evidence/D4_lift_door.png`. The lift interior is 1.48 × 1.65 m (stated 1.50 × 1.70).

## Fix 4: W9 re-measured
- **W9 Bedroom 2 south:** the drawn window line with frame markers runs x 150-262 u at y 748 u. That gives mm (408, 20654) to (4219, 20654), 3.81 m, the full room width (r5 had 1.41 m). Crop: `evidence/W9_bed2_south.png`.
- **W10:** also re-located onto the drawn glazing line at y 759.5 u (it was 753).

## Fix 5: courtyard void west edge (E1), NOT FOUND
`OPENINGS_OTHER` E1, x ≈ 373 u, y 405-552 u, type "NOT FOUND: glazing or balustrade".
- **What is drawn:** a dark line (x 368.5-372) and a lighter parallel line (about x 376) with light infill, and panel ticks at about y 455 and 500.
- **Leans glazing:** the same double-line-with-ticks symbol is used for the north-facade sliding glazing (W1, x 170-220; compare crop).
- **Why it is not classified:** the V4 legend has no glazing or balustrade entry, and the sheet does not say whether the courtyard void is enclosed.

Crops: `evidence/E1_void_west_edge.png`, `evidence/W1_N_glazing_symbol_compare.png`.

## Fix 6: fixtures as 2D footprints (41 items in FURNITURE)
- **From before (9):** beds, L-sofa, coffee table, round table (SVG).
- **New, measured on the raster:**
  - Master Suite: armchair (bbox of the rotated symbol) and round side table.
  - M. Bath: tub, vanity with 2 basins, WC.
  - Bath 1: vanity, basin, WC.
  - Bath 2: vanity, basin, side cabinet, WC.
  - J. Bath: vanity, basin, WC.
  - Wardrobes: M. Dressing ×4, Bedroom 1 recess, Bedroom 2, Dress ×2, J. Dress ×2.
  - Joinery strips with function NOT FOUND (Master, Family Living, Bedroom 1, Bedroom 2, Junior).
- **Not traced:** showers and screens. Nothing invented.
- **Accuracy:** WC symbols and the tub are ±2 u (±70 mm); the others come from white-symbol bounding boxes.

## Not changed / still open
- Stair rise direction: NOT FOUND (no arrow on the FF sheet).
- No viewer (step 3). `STEPS.md` not edited.
- Optimizer: `verify_incremental.py` gave 0 warnings and 0 missing paths. `handoff_guard.py` gave 0 breaches, 0 blocked and 35 style-overlap warnings. The rewritten outputs were restored and not committed.
