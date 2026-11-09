# Critic L5: Ashwood 4B pool review (priority), 2026-11-10 (Asia/Dubai)

Reviewer: Ashwood Critic (lane 5, independent; never builds). Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.
Inputs (read-only, own worktree of `lane/exterior` @ ff8315a): hand-off `production-line/handoffs/L2-exterior_2026-11-10.md`; `walk_exterior_wip/views/garden/shots/pool_pass3_side_by_side.png` (pass 3, b14a910); `blender_wip/f1_box_render/sbs_pool.png` + `view_swimming_pool.png` (F1, cc26030).
References: approved `EXT-4b-POOL_GENERATED-SOURCE-CONDITIONED.png`, `EXT-4b-GARDEN-BACK_...png`; brochure p26 (`source-refs/REF-4b-p26-rear-render-crop_no-title-logo.png`, `4b/evidence/crop_p26_4B_pool_detail.png`); V4 CAD `active/approved-cad-v4/png/FP-4B-GF_V4_preview.png` (via ACTIVE_PIPELINE.json). p25 is the front/street view (no pool); backups p29/30, p33/34 not re-opened this pass.

## Verdicts
| Item | Verdict | Score |
|---|---|---|
| three.js garden pass 3 (`rear_pass.html`, b14a910) | **CRITIC-FAIL** | 2/10 |
| Blender F1 pool (`view_swimming_pool.png`, cc26030) | **CRITIC-FAIL** (close; water good, edge/materials/context wrong) | 5/10 |

## Method / evidence (critic's own renders)
- Headless Chromium (playwright-core, SwiftShader/ANGLE, same renderer as the builder's `tools/shoot.cjs`), `rear_pass.html?view=<cams/pool.json>`, 1280x720. Scripts: `critic/pool/shoot2.cjs`, `probe.cjs`, `probe2.cjs`.
- Frames t=5 s and t=6 s via the page's own `window.__frame(t)` (drives Water2 flow `config`, caustics, palms). Pool box x358-773, y476-579 (15,208 water px).
- Results: pool-box |t5-t6| **max 0, mean 0.0** (palms change, so frames did advance; Water2 `config` uniform did change 0.025 -> 0.06). Pool colour mean RGB (52,106,113), std 1.8-2.0 per channel, luminance p5-p95 91.7-97.8 = a flat plane.
- Water2 mesh hidden (`visible=false`): pool box **identical** (diff 0) -> the Water2 surface contributes **zero pixels**; what reads as "water" is the tile basin seen through nothing.
- Water2 forced `transparent=false`: water becomes a flat pale plane (mean 160,160,151) with no reflection of house/sky and still 0 change t5->t6. So the reflection/refraction targets are effectively empty/alpha 0 in this renderer.
- Still mode also stops rendering after 12 frames (`if(++n>=12 && view) return`), so any still-mode capture 1 s apart is identical by construction (measured 0). Walk mode keeps animating.
- Caveat: SwiftShader, not a GPU. The builder's own pass-3 evidence uses the same renderer and looks the same, so the claim "visibly reflects and ripples" is not supported by any evidence in the repo.
- Side-by-sides: `production-line/critic/pool/pool_threejs_pass3_critic_sbs.png`, `production-line/critic/pool/pool_blender_f1_critic_sbs.png`; raw: `threejs_pool_t5.png`, `threejs_pool_t6.png`, `threejs_pool_diff_t5_t6_x6.png`, `threejs_pool_water2_hidden.png`, `threejs_pool_water2_forced_opaque.png`.

## CAD check (footprint, position)
- model.js water `swimming-pool` x 3.162-12.649, z 1.172-3.553 = 9.487 x 2.381 m vs V4 GF label "SWIMMING POOL 9.50 x 2.40 m" (CAD) - **OK** (within 2 cm). Position: rear of plot, ~1.2 m from rear plot line, ~1.0 m paving to the living/dining glass (z 4.57), left end ~2.9 m from the left plot line - matches the V4 preview (24.4 px/m derived from the 18.7 m dimension). Both renderers keep this footprint. **PASS.**
- CAD draws a TERRACE with **two loungers and a side table** at the pool's right (east) end (V4 GF preview, label "TERRACE", x ~13-15.8 m). The builder's note "no terrace furniture (none drawn on plan)" is **wrong**: the plan draws them (illustrative furniture per legend). Both renders omit them.
- CAD shows paving all round the pool inside the plot (no lawn at the coping); the references show lawn meeting a raised basin face. Image decides look, CAD footprint: keep the lawn outside the plot line / 1.2 m strip as a logged mismatch (check `mismatches/mismatch_log.md` carries it).

## Integrator's 4 points: ruling
1. **Flat teal water - CONFIRMED (three.js).** Measured 0 change in 1 s, std ~2 RGB, Water2 contributes 0 px. Blender F1: REFUTED - its water shows house/sky reflection and a turquoise gradient (pool px mean RGB 19,100,95 vs reference 39,93,95).
2. **Coping and terrace wrong - CONFIRMED (both).** three.js: two coincident copings (model `pool-coping-*` 0.30 m at y -0.05..0.05 and the page's BASIN ring 0.30 m at y 0.005-0.075) -> doubled/raised band; grey square paving with dark grout. Blender: coping a thick white double-layer lip and a bright white terrace. Reference: thin flush light-travertine coping; warm cream large-format paving running parallel to the facade (EXT-4b-POOL foreground; p26).
3. **Blender basin raised rather than flush - REFUTED.** p26 pool detail shows the basin standing **above the lawn** with an exposed stone face, water near terrace level. Derived from the crop: face ~45 px vs pool 9.5 m over ~938 px -> **~0.45 m** (derived, crop-scale assumption). EXT-4b-POOL and GARDEN-BACK show the same raised face and steps down to the lawn. Blender F1 is right to raise it; the **three.js pass is the one that is wrong** (flush with grade, no face, no steps). Blender's defect is the face material/colour and the paved strip, not the height.
4. **No waterline band or caustics - CONFIRMED (both).** p26 detail shows a bright aqua LED/tile glow line along the inner coping on all visible sides; neither render has it. three.js has caustic code (emissive floor) but none is visible (std ~2, 0 change). Blender: no caustics/light (Cycles could do it).

## Defect list - three.js pass 3 (CRITIC-FAIL)
T1. Water2 not rendering (0 px contribution; 0 change over 1 s). Fix in `rear_pass.html` water block: prove the Reflector/Refractor targets are filled and output alpha is 1 (e.g. `material.transparent=false` or clear targets with alpha 1); then re-shoot. Gate evidence: hide-water diff > 0 in the pool box AND two frames 1 s apart with pool-box diff > 0, on SwiftShader and named.
T2. Basin flush with grade. Raise terrace + pool to ~0.45 m (derived, p26) above the lawn on the garden (z0) side with an exposed warm stone face; water ~5 cm below coping. Evidence: p26 pool detail full width; EXT-4b-POOL right half.
T3. Double coping. Keep one coping: ~0.3 m (assumption; ref reads narrow), light warm travertine, flush with terrace. Remove either the model `pool-coping-*` boxes or the BASIN ring in the page. Evidence: p26 detail top edge.
T4. Terrace paving grey squares with dark grout. Change to warm cream/beige large-format plank paving, joints parallel to the facade, low-contrast grout. Evidence: EXT-4b-POOL lower-left terrace.
T5. No steps/entry from terrace to lawn. Add 2-3 wide steps at the pool's left end / terrace front (EXT-4b-POOL bottom; p26 left of pool; Blender F1 already has them).
T6. No waterline band / LED glow; caustics invisible. Add an aqua emissive strip just under the coping inside the basin; make caustics visible once T1 works. Evidence: p26 pool detail.
T7. Water colour: shipped teal mean RGB (52,106,113), dark/grey and uniform. Reference pool mean (39,93,95) with p10-p90 spread (27,77,82)-(51,108,108) plus bright reflections; aim for a lighter edge -> darker centre gradient. Evidence: EXT-4b-POOL water region.
T8. CAD terrace loungers + side table at the pool's east end missing (V4 GF "TERRACE" symbols). Add them (illustrative, plan-sourced). The p26 in-pool loungers on a shallow ledge at the left end are image-only: optional, log as a mismatch rather than invent a ledge depth.
T9. Surroundings: one palm and a bare green plane with a hard edge, flat tan context plane at the horizon right. Reference: 3-4 date palms, dense hedge band, shrubs, bougainvillea, neighbouring villas. Add planting along the boundary hedge line and context massing; remove the blank tan plane. Evidence: EXT-4b-POOL right third; GARDEN-BACK.
T10. Lighting: midday blue-white sun with hard shadows; reference is warm late-afternoon light with warm interior glow. Shift sun lower/warmer for this still. Evidence: EXT-4b-POOL.
T11. FF balcony slab reads as a thin 4 cm line (`ff-balcony-rear` y 3.98-4.02) over the pool terrace; reference shows a thick white slab edge with a glass balustrade. (Already known open; affects the pool frame.)
T12. Process: the pass-3 caption/log says Water2 "visibly reflects and ripples"; evidence does not show it. Do not claim an effect without a two-frame diff.

## Defect list - Blender F1 (CRITIC-FAIL)
B1. Coping: thick white double-layer lip. Make it one thin flush travertine coping. Evidence: p26 detail; critic zoom in `pool_blender_f1_critic_sbs.png`.
B2. Basin face cream-white and smooth; reference face is warm sand/travertine with visible texture. Height is right (see point 3).
B3. Paved white strip between basin face and lawn; reference lawn meets the face directly (p26 detail, GARDEN-BACK). Remove the strip (within CAD paving width, image look).
B4. Terrace and steps bright white; change to warm cream travertine (EXT-4b-POOL).
B5. No LED waterline glow / caustics (p26). Add an emissive strip under the coping.
B6. CAD terrace loungers + side table at the pool's east end missing (V4 GF).
B7. Lawn is rows of grass tufts on a flat green base - reads as a crop field; reference is a mown lawn. Use a fine lawn material or dense short scatter.
B8. Palms: flat umbrella crowns with drooping fronds read as cycads/tree ferns; reference date palms have a rounded crown of arching fronds and a skirt (EXT-4b-POOL right).
B9. Foreground hedge box (lower left) and white bench slab are not in the reference framing; the reference has a low sofa with cushions under the slab (p26, GARDEN-BACK). Use a cushioned sofa or drop it.
B10. Boundary: bare grey wall above the hedge; reference shows dense hedge and planting with palms behind. Raise planting density (scatter 0.3 was a light test).

## Out of scope / not judged
Step 7 provisional video (not opened; it waits on step 6 anyway). Front pass 16 and rear/garden passes 1-2 are left to the backlog critic.
