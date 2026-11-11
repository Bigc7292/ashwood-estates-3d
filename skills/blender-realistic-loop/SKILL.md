---
name: blender-realistic-loop
description: "Autonomous photoreal loop for architectural and hard-surface work. Parse the shot, change the scene, have a fresh critic score the picture, apply only the top fixes, and repeat. Use for villa exteriors, interiors, product shots, or any request to keep iterating in Blender or the live three.js viewer until it looks photographed. Triggers: ultra-realistic, keep iterating, photoreal, without stopping to ask, blender-realistic-loop."
---

# Blender realistic loop

Drive a photoreal pass without pausing for small approvals. The picture is the only score. Code, node trees and material names are not evidence.

## Where the work lands

- If the user is looking at a live page, the loop scores that page. For Ashwood that page is `public/ashwood/exterior-garden-3d/4b/villa.html`. A Blender still that the page does not show does not count.
- Blender 5.1 is on this machine at `/usr/local/bin/blender`. Use headless `blender --background <file> --python <script>` when the fix is a mesh, a baked map or a Cycles check.
- There is no Blender MCP socket here. Do not wait for one. Fall back to bpy.
- The three.js viewer is the delivery surface for this villa. Port a Blender look into the viewer in the same iteration, or the user will not see it.

## The cycle

Repeat until stop. Do not ask the user between iterations.

1. **Parse.** Name the shot (camera, time of day, what must read). Open the latest render or browser frame. Do not describe the code.
2. **Act.** Change the one or two worst visible problems. Numbers, not adjectives: light direction, roughness, plane height, colour hex, texture scale.
3. **Render.** Capture the same camera again. Save the frame next to the previous one.
4. **Critic.** Spawn a fresh critic that is given only the new frame and `references/realism-checklist.md`. The critic has not seen the scene file. It must start with one word, **PASS** or **FAIL**.
   - PASS only if the frame looks photographed: average at least 8, and no score under 6.
   - FAIL otherwise.
   - Then five scores 0–10 (geometry, materials, light, reflections, vegetation), the average, at most three problems worst first each with a numeric fix, and one thing that is already good.
5. **Apply.** On FAIL, fix the worst problem first, then the other two if they are the same surface. Render the same camera. Send that new frame to a new critic. Do not argue with a FAIL. If the frame shows the fix and the critic missed it, make the fix larger so the next critic cannot miss it.
6. **Repeat.** The builder never grades its own frame.

## Stop

Stop only when the critic says **PASS**, or when eight rounds have been sent to a critic. A flat or lower score is not a reason to stop. Do not ask the user between rounds.

## Hard rules

- Never ask the user mid-loop.
- Never score your own frame. The critic is a separate pass.
- Do not invent a room, a tree or a finish that is not already in the model or the plans. Dress what is there.
- Do not download models. Procedural materials, the existing GLB, and maps already in `tex/` are allowed.
- One facade at a time. The rear terrace is the money shot until the critic says it holds.
- Keep day and evening as a switch. Do not destroy the other one.
- Main branch stays untouched. Commit the viewer change on `lane/villa-draco-fix`.

## Read next

| Need | File |
|---|---|
| How to score | `references/realism-checklist.md` |
| Sun, sky, interior practicals | `references/lighting-setup.md` |
| Principled numbers | `references/materials-pbr.md` |
| What to model vs what to shade | `references/geometry-best-practices.md` |
