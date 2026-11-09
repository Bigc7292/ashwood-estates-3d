# F1 render on the box (2026-11-10, lane 2)

First render of `blender_wip/build_scene_f1.py` (the fixed copy; `blender/build_scene.py` still does not compile).
- Blender 4.2.3 headless on the box (`/home/box/apps/blender-4.2.3-linux-x64/blender`), free/local. Blender MCP not needed.
- Build: `AW_SCATTER=0.3 blender -b -P build_scene_f1.py -- grime /tmp/f1_grime.blend` -> "BUILT grime 434", exit 0 (`build_f1.log`). Scatter 0.3 = lighter grass test build; full density is 1.0.
- Render: `blender -b /tmp/f1_grime.blend -P render_views_wip.py -- f1_box_render 32 1280 720 elev_front,elev_rear,back_garden,pool` -> exit 0, ~35 s per view on CPU (`render_f1.log`).
- Outputs: `elevation_front.png`, `elevation_rear.png`, `view_back_garden.png`, `view_swimming_pool.png`; side-by-sides `sbs_*.png` vs the approved generated images.
- The .blend is not committed (temp file, rebuildable from the script). Official `4b_*.blend` untouched. WIP, not critic-reviewed.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.
