# Barclay House: gpu-instancing-web
Date: 2026-11-03 · Source note: notes/2117289699694055771.md
Status: proposed · Owner: Barclay House 3D · Briefed: not yet

WHAT: GPU instancing of repeated meshes (EXT_mesh_gpu_instancing) in the web GLBs — the reason the pure three.js city runs 60 fps on an RTX 3060 (reply on https://x.com/zavrenn/status/2117289699694055771).
WHY: build_scene.py builds windows/arches/cornice blocks/lamps/tree crowns as separate objects; web viewer (web/app.js, hero.glb, context.glb, exterior.glb) and make_mobile.sh currently do no instancing (make_mobile.sh comment: no Draco/meshopt/KTX2). Many identical meshes = many draw calls on phones. Lenses: efficiency gain, UX gain (smoother mobile).
HOW:
1) Export with linked mesh data: in build_scene.py create one window/lamp/tree mesh and link duplicates (obj.data shared) — or rely on step 2 dedup.
2) make_mobile.sh: after make_mobile.mjs add `gltf-transform dedup in.glb tmp.glb` then `gltf-transform instance tmp.glb out.glb --min 5` (CLI in .gltf/node_modules/.bin).
3) Validate (`gltf-transform validate`), load in web/index.html (three GLTFLoader / model-viewer read EXT_mesh_gpu_instancing).
4) Measure: renderer.info.render.calls and file size before/after; mobile_shots.cjs screenshots for visual diff.
CHANGES: make_mobile.sh (+2 lines), optionally build_scene.py (linked duplicates). Combines with x_tricks #2 (meshopt/KTX2).
EFFORT S · RISK low (instancing breaks per-object names used by floor raycast → exclude Floor_* nodes) · ROLLBACK remove the two lines.
LICENSE: gltf-transform MIT.
COST: £0.
SUCCESS: draw calls −50%+ on context/hero, identical screenshots, validator 0 errors.
