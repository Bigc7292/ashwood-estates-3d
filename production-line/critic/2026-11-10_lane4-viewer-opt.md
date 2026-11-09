# Critic report: lane 4 viewer optimisation (Optimizer Bot)

Date: 2026-11-10 (Asia/Dubai). Critic: lane 5 (independent). Builder: Optimizer Bot (lane 4). Branch `lane/4-viewer` @ `6dd4fd2` (includes `47cac1b`).
Scope: `production-line/viewer/exterior-front/` (live), `gf/`, `ff/`. The walkable_v6 fork `exterior/` is SUPERSEDED and was not reviewed, per the integrator.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

**Verdict: CRITIC-FAIL. Score 6/10.** There are no geometry edits, and the stills look the same as the sources. But render-on-demand breaks three interactive behaviours: the sun slider, water animation and the shadow update. The before/after evidence also does not measure like for like.

## 1. No geometry edits: PASS
- Exterior: `data/model.js`, `data/model.min.js` and `data/model.json` evaluate to a MODEL **identical** to `lane/exterior:exterior-garden-3d/4b/model/data/model.js` (blob aa4ce04; I compared the JSON in node). All 16 `overrides/*.js` are blob-identical to lane/exterior at e322991..cc26030. The HTML diff against `front_pass.html` touches only the import paths, pixel ratio, `shadowMap.autoUpdate` and the loop.
- GF: `gf/data/fp-4b-gf.plan.js` is blob-identical to `active/floorplan3d-spike/FP-4B-GF/data/fp-4b-gf.plan.js` (8e480e3, the same on main, gf-interior and rules-and-status). The HTML diff (whitespace and CRLF ignored) changes only the vendor paths, pixel ratio, shadow bake and loop.
- FF: `ff/data/fp-4b-ff.plan.js` = `fp-4b-ff.plan.r4.js` = lane/first-floor r4 (da98e2a). Note that the fork renames r4 data to the r1 filename, so the source `FP-4B-FF/data/fp-4b-ff.plan.js` (854ecae, r1) is **not** what ff/ loads. Document this in the README.
- Draw calls and triangles are equal before and after for the exterior (1201 / 68,656) and GF (315 / 270,034), per after.json.

## 2. Look, same cameras: PASS for stills
- Exterior front (locked camera, shift, 960x540): `2026-11-10_lane4-viewer-opt/exterior_front_before_after.png`. 6 % of pixels differ by more than 30, all on palm fronds, procedural texture noise and palm shadows (`exterior_front_absdiff_x3.png`). These come from `Math.random` in both builds and are not an optimisation effect. Same materials, lighting and shadows.
- GF and FF 3D iso: `gf_before_after.png`, `ff_before_after.png`. Same materials and lighting, and textures are not downscaled (headless DPR 1 on both). The final iso camera differs slightly (after.json: GF source cam [0.11, 34.86, 0.65] vs opt [0, 35.44, -1.38]). The orbit or fly damping is cut off when the loop idles (defect 4).

## 3. Defects
1. **The sun slider does not redraw the 3D (GF and FF). Major.** Setting `#sun` to 09:00 changes 295,877 px (GF) and 330,069 px (FF) in the sources. In the forks only 637 px change, the slider label itself (bbox x 590-681, y 61-76). The canvas never re-renders (`gf_sun9_before_after.png`, `ff_sun9_before_after.png`). The Night toggle and other off-canvas UI have the same cause: only canvas pointerdown, keydown, orbit change and resize call `__lane4RequestRender`. Fix: call `__lane4RequestRender()` from `applyLight()` and from every UI handler that changes the scene, or hook the toolbar's `input`/`click` events.
2. **The shadows stay baked after scene changes. Major.** `shadowMap.autoUpdate=false` with a single `needsUpdate` means a sun move, door swing, or furniture drag or add in 3D leaves the shadows stale. Fix: set `renderer.shadowMap.needsUpdate = true` in `applyLight()`, on door animation frames and on furniture changes. (Exterior: `__frame` already forces it for step 7, which is OK.)
3. **The water stops animating when idle. Major (the ask required it to keep animating).** GF: the source pool and courtyard area (x 654-804, y 231-289) changes over 8 s; in the fork **0 px** change between the two frames. Cause: `animTex.length` lets a frame render, but the rAF continuation condition leaves water out, so the loop stops after 8 idle frames. Exterior-front: the loop stops after about 45 idle frames even with Water2 on screen. Fix: while any water surface is in the frustum, keep a throttled loop (for example 30 fps), or a slow timer, instead of stopping.
4. Minor: orbit damping and fly-to settle are cut short, so the final camera differs from the source. Keep the loop alive until `orbit.update()` returns false, or the fly completes.
5. Minor: the pixel-ratio cap drops GF and FF from 2 to 1.5 on retina desktops. That is a small, intended sharpness loss; record it as a choice in the README. The exterior goes from 1 to 1.5 on HiDPI, which is sharper and more costly. Mobile is capped at 1.

## 4. Evidence quality (before.json / after.json): FAIL
- `before.json` is a hand-written summary (byte sizes and flags) with no timestamp, load times, fps or draw calls. `after.json` is a measured run. They do not measure the same things.
- GF is the only like-for-like pair, and it shows the fork **slower**: loadMs 71,200 vs 75,065, fps 2.7 vs 1.3, and worst frame 675 vs 1507 ms. FPS is forced-continuous under SwiftShader, so it says nothing about the real benefit, which is idle cost. That benefit was not measured.
- The GF fork run logged a 404 console error. The notes say it was fixed on recheck, but after.json was not re-measured.
- There is no FF source measurement. The exterior-front pair is a single sample each (22.8 vs 19.2 s load); I measured 27.4 vs 26.4 s on the box, which is within noise.
- Fix: run one script that records, for every source/fork pair, the same fields (loadMs median of 3, calls, tris, PR, idle GPU time over 10 s with no input, frames rendered while idle, and console errors). Re-run after the fixes above.

## Next for the builder (Optimizer Bot)
Fix defects 1-3, re-measure as in section 4, and re-submit with the same before/after cameras. Not DONE. The integrator should not merge `lane/4-viewer` until this passes.
