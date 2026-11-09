# Critic report: exterior front view (ELEV-FRONT), step 6, passes 8 to 15

Date: 2026-11-10 (Asia/Dubai). Critic: lane 5 (independent, not the builder). Builder: lane 2 exterior.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

**Verdict: CRITIC-FAIL. Score 4/10** (look vs the approved ELEV-FRONT image). Footprint is still on the CAD rows. Steps 1 to 5 were logged in order, and none were skipped.

## What was checked
- Branch `lane/exterior` @ `ba038ea` (pass 15). Files: `exterior-garden-3d/4b/walk_exterior_wip/views/front/STEP_LOG.md`, `front_pass.html`, `overrides/front_pass8..15*.js`, `cameras/front_pass8..15_side_by_side.png`.
- Reference: `step1_reference/generated_approved/EXT-4b-ELEV-FRONT_GENERATED-SOURCE-CONDITIONED.png`. Locked camera `cameras/front_lock.json` with `shift:true` (pass 13).
- I re-rendered it myself (headless Chromium with SwiftShader), with no page errors. My 960x540 render matches the builder's pass-15 still, apart from random palm variation (`2026-11-10_exterior-front-step6/builder_pass15_vs_critic_rerender.png`), so the builder's side-by-sides are honest.

## Evidence (opened and judged)
- `2026-11-10_exterior-front-step6/front_ref_vs_render_rows.png` (reference | render, with red rows at 60/145/465 in 540 px space)
- `2026-11-10_exterior-front-step6/front_facade_crop_ref_vs_render.png` (FF facade crop, reference x 290-860 / render x 260-830)
- `2026-11-10_exterior-front-step6/builder_pass15_vs_critic_rerender.png`

## Rows and footprint (pass 13-15 targets)
Roof slab top, tower top and facade base sit on the reference rows within about 5 px at 960x540. The pass 14 and 15 row targets are met.

## Defects (fix in this order; each is look-only unless marked)
1. **FF glazing reads as opaque brown boards (pass 8 is not achieved).** Render at 1280x720: the FF left and right bays (x 340-460 and 625-790, y 180-260) are flat brown/grey panels with no visible room depth. Reference (ELEV-FRONT 820x461, x 262-310 and 525-590, y 150-250) shows clear glass with a lit warm room, a planter and furniture behind it. Fix: make the glass transmissive or reflective, and show the lit interior volume behind it (front_pass8_glazing.js).
2. **The FF slat screen has the wrong colour and pattern (the pass 11 recolour went the wrong way).** In the facade crop the reference screen is a dark bronze frame with an irregular vertical and horizontal grid, with lit glass behind it. The render has even orange timber slats on a solid brown panel. Fix: use dark bronze slats (about #3a2c22) with uneven spacing and horizontal rails, keep the lit glass behind, and keep the extent as is (front_pass11_slats.js).
3. **The FF stone parapet band and missing glass balustrade are invented.** The render has a solid stone band across the FF front (crop x 650-800, y 210-245). The reference has a glass balustrade with the screen running down to the floor slab. Fix: replace the band with a 1.1 m glass rail (the brochure height is NOT FOUND, so log it as an assumption).
4. **The FF right stone box projecting in front of the tower is missing.** Reference x 498-618, y 193-345 (820 px frame) shows a solid travertine cube with a planter on top, in front of the tower and beside the screen. The render shows a flat wall with a brown window. Check CAD for the FF footprint first. If CAD has no projection there, log it as a mismatch (image look vs CAD) and do not invent it.
5. **The roof canopy lacks the deep lit soffit.** The reference roof is a thin blade with a deep, warm-lit underside and a chamfered fascia, overhanging the FF on the left with a stone return (x 232-262). The render roof is a plain flat slab with one LED line and no visible soffit depth. Fix: add soffit depth and warm uplight to the material and lighting, without changing the footprint.
6. **The front planting is cartoon balls.** Three low-poly green spheres (render x 640-800, y 320-410) stand where the reference has a multi-stem flowering tree (x 495-650) and low ornamental grasses. Fix: replace them with a multi-stem tree and low grasses. This reads as "looks unnatural".
7. **The lighting is midday, not dusk.** The reference is low warm dusk with lit soffits, a lit carport (LED lines at y 285-300) and a lit entry. The render reads flat daylight, and the carport LED lines are faint white. Step 4 was passed (981cafa), but in pass 15 the warm look is lost. Fix: lower the sun, warm the sky gradient and raise the emissive strength on the soffit, carport and lobby.
8. **The carport and left boundary are placeholders.** There is a grey block wall at the left (x 60-100) and a row of ball hedges. The reference has a stone side wall with planting and a lit planted wall inside the carport (x 65-205). The carport fascia is cream in the render and dark bronze in the reference.
9. **The front gate and boundary are wrong.** The black bar gate in the render (x 450-570) is narrower and black. The reference has a bronze vertical-bar gate spanning x 357-527 and a low stone wall with a bronze rail to the right (x 527-775). The render has a raised cream planter there instead.
10. **Minor:** the background is empty, where the reference has neighbouring houses and trees. The street (kerb, road) is a flat band. The palm crowns still read as sparse fern leaflets.

## Process and step-order findings
- **P1 (major, consistency):** passes 14 and 15 change heights in the front-view build only. The tower is 9.73 m here but 11.6 m (M2) elsewhere, and the FF storey is raised 0.50 m (M28) here but not in other views. The front view is now a different building from the other views and the walkable model. Both are logged as assumptions with Colin's "don't wait" go-ahead, so I don't fail them as invented. But before step 7, Colin must pick one height set for all views. Evidence: `views/front/M25_assumption_2026-11-09.md`, `mismatch_log.md` M25/M28, `overrides/front_pass15_roof_row.js`.
- **P2:** the per-pass "Critic (hash)" verdicts in STEP_LOG.md have no critic report files (`production-line/critic/` did not exist before this report). Their independence can't be verified from the repo. From now on, critic verdicts go here.
- **P3:** the loop numbering is inconsistent. Passes 9-15 say "loop 2", but the log footer says "step 6 (critique), loop 1". Fix the footer.
- **Step order:** steps 1 to 5 are logged in order, and step 7 is NOT STARTED. Pass 9 added a step 7 motion hook (`window.__frame`) while step 6 was still open. It is inactive in stills, so this is a note only, not a fail.

## Next for the builder (lane 2)
Fix defects 1-3 first (FF glazing, screen, balustrade), one per pass. Then 6 and 7, then 4 (CAD check first). Re-submit with the same locked camera and `shift:true`. Not DONE.

## Addendum (2026-11-10 00:35): pass 16 and per-pass gate notes 8 to 16
Pass 16 is lane/exterior `50ec220`; I checked it at `cc26030`. Evidence: `2026-11-10_exterior-front-step6/builder_renders_pass8_to_16_grid.png` (the builder's left-hand renders, passes 8 to 16) and `2026-11-10_exterior-front-step6/pass16_ref_vs_critic_render.png` (my own render at the locked camera with shift). Each note judges only that pass's one change. The overall view stays CRITIC-FAIL on the defect list above.

| Pass | Commit | Change | Pass verdict | Note |
|---|---|---|---|---|
| 8 | bbe1b36 | glazing: dark glass, lit rooms behind | **CRITIC-FAIL** | The FF side bays still read as opaque brown panels, with no room depth visible (defect 1). |
| 9 | f1cd5ad | GF glazing band widened (M27) | CRITIC-FAIL (superseded) | It broke the CAD width and was reverted in pass 10. |
| 10 | 8aba267 | GF glass back to the CAD width x 7.50-9.59, timber door | **CRITIC-PASS** | It holds the CAD width, and the door is a labelled image-read assumption. |
| 11 | e62ad64 | slat screen recoloured to warm timber, single layer | **CRITIC-FAIL** | The reference screen is dark bronze with an irregular grid; the render is even orange slats on a brown panel (defect 2). |
| 12 | 0eea0b2 | flat coping cap on the tower | **CRITIC-PASS** | The cap matches the reference, and the footprint and height are unchanged. |
| 13 | 8fda529 | shift lens (parallel verticals) | **CRITIC-PASS** | The verticals are parallel as in ELEV-FRONT, and the camera position is unchanged. |
| 14 | ca7c9d6 | tower top 9.73 m (M25) | **CRITIC-PASS on the row only** | The tower top sits on the reference row. This is still conditional on P1: the 9.73 m (front) vs 11.6 m (elsewhere) split needs Colin's single height set. |
| 15 | ba038ea | FF storey +0.50 m (M28) | **CRITIC-PASS on the row only** | The slab top is on the reference row (within 5 px at 960x540). Same P1 condition: this exists in the front-view build only. This is the missing pass 15 note. |
| 16 | 50ec220 | three shrub balls → one open multi-stem tree | **CRITIC-PASS** | It fixes defect 6's "cartoon balls". The canopy still reads as clumped blobs, and the low grasses and flowering shrubs at the base (reference x 520-650, y 380-420) are still missing. Next: looser foliage and add the base planting. |

The builder's open items also hold. The carport canopy is too deep and thick against the thin reference slab (defect 8). The left palms stand in front of the carport here, but behind it in the reference: move them back behind the carport line, at the plan tree positions (model.js trees).
Remaining order for step 6: defects 1, 2, 3, then 7, 4, 5, 8, 9.
