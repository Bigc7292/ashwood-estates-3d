# Barclay House: street-life-animation
Date: 2026-11-03 · Source note: notes/2117240312439742479.md
Status: proposed · Owner: Barclay House 3D (89b1b343-058f-4753-a2d5-801060c14f25) · Briefed: not yet (draft in report)

WHAT: add one moving car on Whitworth St W and one train crossing the viaduct to the flythrough, plus interior window glow at dusk — the "finished image → car departs" mood clip (https://x.com/uncle_render/status/2117240312439742479) done in free Blender.
WHY: /workspace/barclay renders and fly.mp4 are static; scene already has roads (scene_data.json roads, Whitworth Street West ids 155768981…), rails + `Rail_Viaduct` collection (deck 8.55 m from LIDAR), `GLOW` value nodes on window materials (build_scene.py ~l.69/81) and dusk preset in tod_panel.py. Lenses: visualization gain; quality/UX/efficiency none.
HOW:
1) On tests/scene_copy.blend: build a curve from the Whitworth St W road pts (scene_data.json, hero-local m) and one from the OSM railway pts at viaduct z.
2) Car/train = CC0 model (Poly Haven / Kenney) or primitive blocks; Follow Path constraint, offset driven by a pure function of t (same rule as flythrough.py: no hand keyframes, deterministic).
3) Add to flythrough.py: optional `--life` flag that sets path offsets per frame from t; `--tod dusk` sets GLOW=1 on a fixed random-seeded 40% of windows.
4) Render low-res (`--res 320x180 --fps 6 --samples 8`), ffmpeg → mp4, teardown sheet.mjs contact sheet; check no vehicle intersects hero/piers.
CHANGES: flythrough.py (+--life), new life_paths.py (curves from scene_data.json), tests/fly_life/. Never edits hero numbers or out/barclay_scene.blend until approved.
EFFORT S · RISK low (set dressing; label as illustrative) · ROLLBACK drop --life flag.
LICENSE: Blender GPL; vehicles CC0 only (no Sketchfab unless CC-BY credited).
COST: £0. Avoided: paid AI render kit/video credits.
SUCCESS: 8–10 s clip where car leaves frame and train crosses viaduct, sheet passes visual review, ref_check.py precision on hero beat unchanged (±0.02).
