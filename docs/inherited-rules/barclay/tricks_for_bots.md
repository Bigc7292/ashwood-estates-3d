# Certified tricks per bot (2026-11-03, from tricks_register.md)
## Barclay House Interior (viewer)
- #2 meshopt: load out/mobile/*_mobile_v2.glb (-47%/-62%). MUST host web/meshopt_decoder.js locally: model-viewer `meshoptDecoderLocation='./meshopt_decoder.js'` or three `loader.setMeshoptDecoder(MeshoptDecoder)`; CDN default failed in test.
- #3 glass: swap Glass_dark to MeshPhysicalMaterial (transmission 0.9 desktop / off on phones) + RoomEnvironment; faience clearcoat already in GLB. Code: tests/trickcheck/snippets.js
- #10 canal: three Water.js (MIT) on Canal_water, 256px reflections on phones. Snippet in snippets.js.
- #5 floor/unit click: waits for Floor_* nodes (none yet).
- NOT KTX2 (bigger files).
## Surroundings Bot
- #7: share mesh data for repeated lamps/bollards/trees/windows (linked duplicates) so `gltf-transform instance` actually instances (currently 0 repeats found, 5453 draw calls).
- #2: run dedup + meshopt on your GLB (surroundings 34.5→14.3 MB in test).
- #10: name the canal mesh Canal_water. #9 street life deferred to Round 5 (CC0 only).
- #11: splat backdrop only once real photos exist (gsl-build-lod tested, -87%).
## Optimizer Bot
- Run make_mobile_v2.sh then validate.sh; budget check v2 files. Add a headless load check (tests/trickcheck/load.cjs) — a meshopt file without local decoder fails silently with ERR.
- Track draw calls (hero 1466, surr 5453) until linked-duplicates/join-by-material lands.
- Never adopt a trick without a register row (AGENTS.md intake gate).
