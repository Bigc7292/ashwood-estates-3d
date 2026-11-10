# Night handoff — 10 Nov 2026, 23:47 Asia/Dubai

Colin is stopping for the night. This file is the record of the Grok session that ran after Kimi paused. Read this before touching the exterior again.

The live preview that was being reviewed is not the old walk pages. It is:

`exterior-garden-3d/4b/villa.html`

It loads `villa-materials.glb` and the BlenderKit plants in `exterior-garden-3d/4b/tex/bk/`.

## What was already true before this session

Kimi paused because the agent quota was exhausted. Checkpoints that were already on GitHub:

- Exterior Water2, controls, evidence, changelog: `659436a`
- First-floor r8 rebuild: `7c4cdd3`
- Corrected exterior hub and cameras: `457ff80`
- Latest `main` before this handoff: `4a71466` (merge of `lane/exterior-quality`)

Kimi left unfinished: first-floor presentation captures, exterior realism, integration, and an independent review. No deploy was done.

## What this session changed

### Viewer

- `exterior-garden-3d/4b/villa.html` is the exterior the review was done on. It did not exist in the repo before tonight.
- Opens on the outside of the villa. Ground floor and first floor buttons stay available. Interior walk is opened with `?walk=1` from the interior pages.
- Pinch zoom was fixed: two-finger pinch is handled in the capture phase, pan is off, so the browser does not steal the gesture.
- A Review feedback tab is on the exterior and on the interior walk. It screenshots the view, draws with arrows, lines, circles and labels, records the camera, floor and place, and saves a note plus the image. Pen colours: red, yellow, white, black, blue, green.
- Saves go to `POST /api/review-feedback`. That route exists only in the Grok app dev server (`vite.config.ts` in the app sandbox), not in this repo. Tonight's saved reviews were copied to `handoff/2026-11-10-night/review-inbox/`.
- Shared review script: `exterior-garden-3d/4b/review/review.js`.

### Fixes already made from Colin's saved reviews

Only the reviews that were already saved were edited. The exterior walk-through was not finished.

1. Balloon trees. The round green spheres were the `broadleaf_*` canopies. They are hidden. Trees are now `tex/bk/garden.glb` (BlenderKit "Bush" / `SM_Tree_15`, asset `f38df39b-fb8d-46e4-973b-28f8fe287286`), scaled up and placed on the old trunk spots.
2. Courtyard water. `COURTYARD_water_(CAD)` is a dark still basin, not the swimming-pool blue. `COURTYARD_planter_island` is larger and planted so it reads as an island. The rear swimming pool was not turned into this.
3. Pool too close to the house, no seating. Every `POOL_*` mesh and `DECK_left_of_pool` is shifted `-3.78` on Z. A stone terrace, sofa, two chairs, a coffee table and two sun loungers sit in the gap. The rear pool water is more transparent so the pale basin shows.
4. Block grass. The `HEDGE_lawn-*` and `HEDGE_front_bed` boxes are hidden. They were solid green blocks.
5. White fairy plants. The first olive export (`tex/bk/olive.glb`) lost its leaf photo during decimation and rendered white. It is not used by the page any more. The grass cards (`tex/bk/grass.glb`) had a white background and also read as white bushes. They are not used any more.
6. Bushes. The hedge line no longer uses a shrunk copy of the tree. It uses `tex/bk/bush.glb`, a wider-than-tall shrub (BlenderKit "Shrub" `090b95d4-e297-481c-9f6e-b6f707bcebf8`). The black background of the leaf photo was turned into transparency, then the mesh was reduced from 34,840 faces to 7,664 so the page still loads. Bushes are overlapped along the old hedge boxes.

### What was not finished

- Colin had not finished walking the whole exterior when the first fixes started. More reviews may still be needed.
- The lawn is still a flat repeating texture. It is not individual blades.
- The rear pool is clearer than it was, but it is still a flat water plane, not a rendered pool.
- Furniture on the terrace is simple boxes, not real furniture models.
- Palms are still the original frond meshes.
- The courtyard pine is still the stacked-disc tree.
- Roof, first floor and ground floor were not part of tonight's last pass.
- BlenderKit assets are free-library downloads used inside this project. The API key is not in git. If the sandbox is new tomorrow, the key has to be pasted again. Do not commit it. This repo is public.

## Where to look

| Thing | Path |
|---|---|
| Exterior page | `exterior-garden-3d/4b/villa.html` |
| Model | `exterior-garden-3d/4b/villa-materials.glb` |
| Tree | `exterior-garden-3d/4b/tex/bk/garden.glb` |
| Bush | `exterior-garden-3d/4b/tex/bk/bush.glb` |
| Unused failed plants | `tex/bk/olive.glb`, `tex/bk/grass.glb` |
| Saved reviews | `handoff/2026-11-10-night/review-inbox/` |
| Site pages from the preview | `handoff/2026-11-10-night/site/` |
| First-floor page from the preview | `handoff/2026-11-10-night/ff/index.html` |
| Tomorrow's list | `docs/TODO_2026-11-11.md` |

## How the plants are placed

In `villa.html`, after the GLB loads:

- Meshes named `broadleaf_canopy`, `broadleaf_trunk` or `broadleaf_branch` are hidden. Trunk XZ is kept and a tree is cloned there.
- `HEDGE_lawn-*` and `HEDGE_front_bed` are hidden. Their boxes become the bush line.
- Pool meshes are moved with `position.z += -3.78`.
- Terrace furniture is built with boxes in the gap between the house and the moved pool.

Reload the preview after any change. The plant URLs are cache-busted (`garden.glb?v=1`, `bush.glb?v=2`).
