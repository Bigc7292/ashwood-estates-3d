# Legacy project – project rules (AGENTS.md)
Read this FIRST on every task. CLAUDE.md and GROK.md are copies/symlinks of this file so any agent tool finds it.

## Hard rules
1. FREE ONLY. No paid tools, subscriptions, credits or paid APIs. A cost = blocker; propose a zero-cost path.
2. NO ESTIMATES for building facts. Only sourced numbers with URL (LIDAR counts). Stand-ins must be labelled "stand-in". Log in dossier.
3. Don't ask Colin for data. Do research/build yourself. Message Colin only with finished results or a hard blocker.
4. Don't burn tokens: short replies, no duplicate research, no ack ping-pong.
5. Never overwrite a good export: write to temp, then mv. Never save over legacy_scene.blend while the Blender MCP session has it open.
6. GITHUB ON EVERY CHANGE. Commit and push to https://github.com/Bigc7292/legacy-archive after every code or asset change. Do not deploy or alias Vercel unless Colin explicitly says deploy. Never commit API keys.

## Tool map (use these, in this order)
- Facts: dossier Page + listings_findings.md + docs/ (planning drawings). Data: area.osm, scene_data.json, lidar/.
- Build: build_scene.py, tod_panel.py via Blender 4.2.3 (-y). Blender MCP (port 9876) for live inspection/edits.
- Check: camera_match.py -> ref_check.py against refs/. Render: Cycles 128 samples + denoise.
- Export: export_glb.py -> make_mobile.sh (hero + surroundings, full + mobile). Then ./validate.sh (Khronos validator + size budgets + stale-mobile check; must PASS).
- Ideas: x_tricks.md and x_workflows.md (from X Bookmark Analyst). Skills: teardown, canvas, box-desktop.

## The pipeline (same order every time)
0. READ: AGENTS.md, SCORE_PLAN.md (the open pass), critic_log.md (last round), x_tricks.md. Note which tricks apply this round.
1. FACTS: any new dimension/material? Source it (URL) or mark NOT FOUND; keep searching before reporting missing.
2. BUILD: one change set only, from the latest critic defect list. One thing per pass where possible (locked camera).
3. CHECK: render preview from locked camera, run ref_check.py vs reference photo. Compare to refs/ side by side.
4. CRITIC: independent critic (separate executor or Interior bot) scores and lists defects. Log in critic_log.md (round, score, defects, fix, applied tricks, skipped tricks + why).
5. EXPORT: GLB hero + surroundings, then make_mobile.sh; validate; commit and push to GitHub. Do not deploy to Vercel unless Colin says deploy.
6. DELIVER: 4K stills only when critic score meets target (>= online photos). One short message to Colin.
Loop 2-5 until target met. Every round the critic_log must list which rules/MCPs/skills/tricks were used.

## Improving this file
After each round, add any repeated mistake as a rule (one line) under "Lessons". Keep the pipeline short.

## Exterior 7-step process (Colin's rule, 2026-11-03, set in stone)
All exterior work follows these steps in order, one step at a time. Finish, render and log each step before starting the next. Run the steps straight through without waiting for Colin's go-ahead between them (Colin, 2026-11-03 23:25). No skipping, no excuses.
Reference for all exterior work: `refs/exterior_target.png` (Colin's ChatGPT target image). Check every exterior change against it.
1. Reference: the 2D target image (`refs/exterior_target.png`). Done by Colin.
2. Layout: read the layout from the image and build the scene in Blender (Blender MCP).
3. Blockout: boxes first, then the space, the models, the materials, in that order. Fix proportions while it is still boxes.
4. Grime: procedural wear on every surface: chipped paint, dust, soot, drip and rain streaks, stains.
5. Printed matter: signs, lettering, posters and stickers made as prints, then faded and peeled.
6. Critique: Colin's notes, then check close-ups in the viewport and fix what is found.
7. Motion: add motion last (traffic, light flicker, rain, clouds, a camera move), then render to video.
Note: the target image is an AI collage and does not match the real building (`refs/critic1/real_geograph.jpg`, `real_commons.jpg`). Until Colin says otherwise, use it for look and finish; keep sourced geometry from the photos and drawings (hard rule 2).

## Lessons
- Cutters must stay until booleans applied; check windows/arches aren't solid in the GLB.
- Tiled stone textures read as rubble in the GLB; use flat colours.
- Phones: use out/mobile/ files, not full ones (36 MB surroundings GLB blanks Samsung).
- Executors can't spawn subagents; the orchestrator runs the critic loop.
- Don't message a running executor mid-task; it interrupts.
- A bot's own "it reads" claim is not a score. The orchestrator looks at the still before it counts.
- Do not run backup.sh onto the viewer deploy. Tests stay in tests/ until a critic pass is merged.

## Bookmark-trick intake gate (Colin's rule, 2026-11-03)
Every item X Bookmark Analyst adds to x_tricks.md is NOT adopted until Legacy project has: (1) read the source + doc, (2) verified it's free and licence-OK, (3) checked where it fits (script/step/bot), (4) tested it on a copy in tests/, (5) certified it (PASS/FAIL with measured result, validate.sh must pass for exports), (6) integrated it into AGENTS.md pipeline or tool map, and (7) told all bots. Record each in /workspace/legacy/tricks_register.md: id, source, status (NEW/TESTING/CERTIFIED/REJECTED), test result, where integrated, date. Never leave a trick as NEW for more than one round.
- Certified tricks (see tricks_register.md / tricks_for_bots.md): phone files via ./make_mobile_v2.sh (dedup+meshopt; viewer must use LOCAL meshopt_decoder.js); KTX2 off (bigger downloads); instancing needs linked mesh data in build_scene.py first.

## Backup rule
- After EVERY change set or round, commit and push to legacy-archive and confirm the push. Never add files >99 MB. Never commit API keys. Do not deploy to Vercel unless Colin says deploy.
