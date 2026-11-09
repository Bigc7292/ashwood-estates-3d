# Barclay House 3D (35 Whitworth St W, Manchester M1 5NG)
Photorealistic exterior + surroundings model (Blender -> GLB) and web viewer (`web/`, deployed at https://barclay-house-viewer.vercel.app). Interior/apartments in `interior/`.
## Resume
1. Read `AGENTS.md` (= CLAUDE.md = GROK.md) first: hard rules (free only, no estimates, sourced facts), fixed pipeline, lessons.
2. Then the repo-root `status.md`, `SCORE_PLAN.md`, `critic_log.md`, `tricks_register.md`, `x_tricks.md`, `optimizer_log.md`, `PLAN.md`, `TOOLS.md`.
3. Pipeline: source facts -> one change set -> locked-camera render + `ref_check.py` -> independent critic -> export, `./make_mobile.sh`, `./validate.sh` (must PASS) -> commit and push to https://github.com/Bigc7292/barclay-house-archive. Deploy the viewer only when Colin says deploy.
Layout: `out/` exports (GLB/FBX/renders), `out/mobile/` phone GLBs, `web/` viewer, `lidar/` EA LIDAR, `textures/`, `refs/` reference photos, `docs/`, `tests/` experiments. See SETUP.md.
Do not copy a `tests/door_*` hero over `web/hero.glb`. The live building is the textured 3-mesh file. See `CHANGELOG.md`.
