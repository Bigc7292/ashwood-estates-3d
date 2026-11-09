# Critic report: exterior rear and garden step 6 passes 1-3, Blender F1 render, step 7 provisional video

Date: 2026-11-10 (Asia/Dubai). Critic: lane 5 (independent). Builder: lane 2 exterior (lane/exterior; I read `/workspace/wt-exterior` and my own worktree at `cc26030` / `ff8315a` and made no edits).
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

**Pool and Water2 are out of scope here.** A separate review covers the pool views (garden pass 3 `pool_pass3_side_by_side.png`, Blender `sbs_pool.png`) in `production-line/critic/2026-11-10_pool_review.md`. Cite that report for the pool.

## (b) Rear and garden web views, passes 1-3: **CRITIC-FAIL, score 4/10**
Evidence: I made my own renders of `rear_pass.html` at `cc26030` from the builder's cameras (`views/rear/cams/rear.json`, `views/garden/cams/garden_back.json`). They load READY with no console errors.
- `2026-11-10_exterior-rear-garden/rear_ref_vs_critic_render.png` (ELEV-REAR | render)
- `2026-11-10_exterior-rear-garden/garden_back_ref_vs_critic_render.png` (GARDEN-BACK | render)
- The builder's `views/rear/shots/rear_pass3_side_by_side.png` and `views/garden/shots/garden_back_pass3_side_by_side.png` match my renders.

Per-pass notes:
| Pass | Commit | Change | Verdict | Note |
|---|---|---|---|---|
| 1 | 2a446d0 | palms on 4 plan tree symbols; context lawn; side hedges | **CRITIC-PASS on palm positions; FAIL on planting** | The palms sit exactly on the CAD tree symbols: tree-1 (1.03, 1.386), tree-2 (16.415, 1.67), tree-3 (0.888, 7.959) and tree-7 (17.978, 9.06), matching `overrides/rear_pass1_base.js` against `model/data/model.js` trees. But `remove_plain_trees` deletes the other 8 plan tree symbols (tree-4/5/6/8/9/10/11/12), so plan content disappears from these views and the planting is thinner than the plan. The context lawn is correctly labelled off-plot. |
| 2 | e322991 | rear glazing: dark clear glass, lit rooms, slim frames | **CRITIC-FAIL** | The glass still reads as opaque brown/orange panels. In the render (1280 frame), the FF bays are at x 650-890, y 120-180 and the GF bays at x 665-880, y 185-250. In ELEV-REAR (x 690-860, y 115-150 and y 170-225) you see pale lit rooms with white ceilings, curtains and furniture. |
| 3 | b14a910 | pool Water2 tuning | see `2026-11-10_pool_review.md` | Not judged here. |

Builder's open items, confirmed:
1. **Sparse rear planting: confirmed.** The render shows 4 palms, 2 small ball-hedge rows and a flat lawn. ELEV-REAR and GARDEN-BACK show dense palm clusters on both sides, flowering bougainvillea (GARDEN-BACK x 30-90, y 160-200), ornamental grasses in the foreground, and hedges along the boundary walls. Fix: keep tree symbols 4-12 (don't remove them), add clustered understorey palms at the boundary corners, add a grass and shrub belt along the side walls (x 0.35 and 18.35, z 0.4-10), and add foreground grasses. Positions come from the plan tree symbols; density from the image is logged as an image-read assumption.
2. **The FF balcony slab and glass balustrade are missing: confirmed.** ELEV-REAR shows a white projecting slab across the full FF width with a continuous glass balustrade (y 135-160). The render has only a thin tan band at the FF floor and no rail. Fix: add a balcony slab about 0.25 m thick projecting from the FF rear face, plus about 1.1 m of clear glass (the height is NOT FOUND, so label it as an assumption). Check the projection depth against the FF plan "BALCONY UNKNOWN" zone at the rear of the V4 FF sheet.
3. **The interiors are brownish: confirmed.** The interior back walls and floors are mid-brown, where the references show pale greige walls, white ceilings and warm light. Fix: interior back wall about #e9e1d6, ceiling white with warm emissive, and floor light porcelain (p17/p24 tie-in). That also fixes the pass 2 glazing reading.
4. **New: the RF block is a grey placeholder box** (render x 675-865, y 55-100). ELEV-REAR shows a small set-back stone pavilion with a thin roof. Use travertine (M12 open).
5. **New: no terrace step or plinth.** The reference GF sits on a stepped stone terrace (x 90-430, y 225-240). The render has flat ground to the glass line. Check the terrace in the GF plan ("OUTDOOR TERRACE" label beside the lift) before adding it.

## (c) Blender F1 headless render (`blender_wip/f1_box_render/sbs_elev_rear.png`, cc26030): **CRITIC-FAIL, score 5/10**
- **Note:** there is no CAD rear elevation. `active/approved-cad-v4/` holds plans only (ACTIVE_PIPELINE.json). So the check is the footprint from the GF/FF plans plus the look from ELEV-REAR and p26.
- Better than Q4: the glazing now reads as clear glass with lit pale rooms, which fixes the Q4 glazing finding. The palms have fuller drooping crowns.
- Defects:
  1. **The roof and RF level are wrong.** A large cantilevered canopy floats a full storey above the FF roof (F1 x 205-385, y 35-75), with an RF railing level in between. In ELEV-REAR the main roof is a thin slab directly over the FF, and only a small set-back RF box sits above it. Check RF massing against M12 and the RF plan, and lower or remove the canopy.
  2. **The palms block the facade.** Two palms stand directly in front of the GF and FF glazing (F1 x 40-170 and 340-480). The references put the palms outside the facade edges. Move them to the plan tree symbols (tree-1 at x 1.03, tree-2 at x 16.415), as the web pass 1 does.
  3. **The pool and terrace are not visible.** The plan pool (x 3.16-12.65, z 1.17-3.55) sits right behind the house, and ELEV-REAR shows it with a stepped terrace and loungers. In F1, tall foreground meadow grass and hedges hide both. Lower the scatter in the camera foreground strip, or raise the camera to the reference height.
  4. The FF balcony glass balustrade is present only partially (centre slat bay); make it continuous across the full width as in the reference.
  5. The scatter is 0.3 (a test build, per README). Re-render at 1.0 before the next judgement.

## (d) Step 7 PROVISIONAL video: **CRITIC-FAIL (step order)**
- Full path: `/workspace/wt-exterior/exterior-garden-3d/4b/step7_motion/EXT-4b_STEP7_garden-pool_motion_PROVISIONAL.mp4` (lane/exterior b4d7459). 10.0 s, 1280x720, 24 fps, 240 frames.
- Frames: `2026-11-10_exterior-rear-garden/step7_video_frames_1fps_plus_last.png` (ffmpeg 1 fps plus the last frame). The mean absolute change from frame 1 rises 11 → 43 by 8 s, then flattens, so the push-in stops moving in the last 2 s.
- **Step order: FAIL.** Rear and garden step 6 has not passed (this report fails it), and front step 6 is also failed. A step 7 clip made before the step 6 gate skips a gate (AGENTS.md: "Each step still gets its gate log and critic check before the next step starts"). It is labelled PROVISIONAL, which is honest, but it cannot be gated.
- Visual defects (noted for the re-run): (1) It is called "garden-pool", but the pool is only a thin sliver at the bottom edge in all 11 frames. The push-in ends on a brown facade wall, so re-aim it at the pool or terrace. (2) A palm trunk crosses the left edge from 5 s onward and partly occludes the frame (frames 05-10, x 0-60). (3) It inherits the rear defects (brown interiors, missing balcony, sparse planting). (4) The sun change is barely visible across the 10 s. For water animation, see the pool review.
