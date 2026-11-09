# Step 7 Motion (4B exterior, web): gate log

Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Inputs | Outputs | Review check | Status |
|---|---|---|---|
| `walk_exterior_wip/rear_pass.html` at rear/garden step 6 pass 3; camera `cam_step7.json` (GARDEN-BACK camera with a push-in) | `EXT-4b_STEP7_garden-pool_motion_PROVISIONAL.mp4` (10 s, 24 fps, 1280x720, H.264, 4.9 MB); `frame_first.png`, `frame_last.png`, `frame_first_vs_last.png` | independent critic | **PROVISIONAL / REVIEW-PENDING**: step 6 for front, rear and garden is not yet critic-passed, so this clip is a draft and will be re-rendered after the step 6 gate |

## What moves (all display assumptions)
- Pool water: three.js Water2 (r160, MIT, vendored) flow driven per frame (deterministic, `window.__T`), plus caustic drift on the pool floor.
- Palm sway: frond and trunk sway with a slow gust envelope (`window.__frame`).
- Sun change: sun moves lower and warmer (towards 0xff9a52) and dims 25 % across the clip; shadows lengthen.
- Camera: slow eased push-in from (18.4, 1.65, -14) to (15.2, 1.65, -6.5), target fixed.

## How it was made (box, free)
`node walk_exterior_wip/tools/shoot.cjs rear_pass.html ../step7_motion/cam_step7.json /tmp/s7 1280 720 240 24` (headless Chromium, swiftshader WebGL), then
`ffmpeg -framerate 24 -i /tmp/s7/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 22 -movflags +faststart EXT-4b_STEP7_garden-pool_motion_PROVISIONAL.mp4`.
Frames are not committed (rebuildable).

## Open
- No front-view clip yet (the front hook exists in front_pass.html; front step 6 not critic-passed).
- Planting density and FF balcony slab/balustrade gaps from rear step 6 carry into the clip.
