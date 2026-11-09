## 2026-11-03 19:48 +04 — smaller files, then deploy

Desktop now loads the compressed surroundings (3.1 MB, was 12 MB) and the compressed flat (2.1 MB, was 5.1 MB). The reflection map is the 1.5 MB file again, not the 6 MB one. First load is about 13.2 MB. Pushed so the live site can update.

## 2026-11-03 19:45 +04 — surroundings by material

The context blocks are no longer one flat colour. Short blocks are red brick, cream render or grey panels. Blocks taller than 22 m are glass. Roofs are dark. OSM only tags a material on 5 of 98 buildings, so the choice is a stand-in from height and position, not a survey. Not deployed.

## 2026-11-03 19:32 +04 — interior light and the street outside

The room exposure is held at 0.9 so the cream does not blow out. The fill is warm, the ceiling lamps are warm, and a soft shadow sits under the sofa and the table. The sofa uses a fabric normal and roughness instead of the blurry navy tile. The window shows a photograph of Whitworth Street West. That photo was not taken from this flat. Not deployed.

## 2026-11-03 19:28 +04 — stone, faience and glass

The facade now has a normal, a roughness and an occlusion map, plus mortar lines and a small colour change from block to block. Portland stone is rougher. The faience above it is smoother. The glass is set 45 mm back and reflects the sky, with a dim room behind it that shifts as you move. The course size and that room are stand-ins. Not deployed.

## 2026-11-03 19:25 +04 — AgX, sun shadow, bloom

Desktop now uses AgX and sRGB, with a separate exposure for each time of day. The sun casts a soft shadow. Contact shade is SSAO, and only the brightest spots bloom. The reflection map is a 2K extract of the full HDRI. Phones skip the shadow and the extra passes. Not deployed.

## 2026-11-03 19:22 +04 — living room uses real materials

The flat is no longer one blurry lightmap on desktop. Walls, the navy sofa, the oak table and the floor each have their own material, the ceiling spots are small warm lamps with a dark trim, and the shade under the furniture comes from the room lights. The shapes are still simple. The television is dark glass. Phones still load the smaller baked file. Not deployed.

## 2026-11-03 19:20 +04 — interior is no longer blown out

The flat was being lit twice, so the cream baked light and the viewer light stacked. The bake is now shown on its own, darker, with the ceiling spots pulled to a warm lamp colour. Contact shade sits under the sofa and the table. The window is a brick building instead of a flat blue card. That view is a stand-in. The television has a bezel. The furniture meshes are still the simple bake. Not deployed.

## 2026-11-03 19:10 +04 — facade is no longer flat plastic

The close view was one cream colour with a hard sun disc. The viewer now draws Portland stone courses on the ground floor, smoother faience above, a dark glass that reflects the sky, and a darker underside on the cornice. The clearcoat that made the hotspot is off. The joint size is a stand-in. The surrounding flat boxes get a brick repeat. Not deployed.

## 2026-11-03 17:46 +04 — kitchen run and a bathroom

The Home Builder flat now has the kitchen on the south wall: base cabinets, uppers, a worktop, a tiled splash, a sink, a dishwasher, a range, a hood, a fridge and an island. Widths are stand-ins.

The bathroom is the south-west room. Home Builder supplies the vanity, the basin and the wall cabinet. It has no WC and no shower, so those are labelled stand-ins in `hb_bath.png`. Not the viewer flat.

## 2026-11-03 17:40 +04 — doors and a kitchen run

Same Home Builder file, `legacy/tests/interior/hb_flat.blend`. Five openings are cut with the addon's wall boolean: the entrance and the doors into both bedrooms, the store and the bathroom. Each has a Home Builder entry door. Width 0.82 m and height 2.04 m are stand-ins. The kitchen run is Home Builder base cabinets, uppers, a sink, a dishwasher, a range and a fridge, on the plan's kitchen side. Not the viewer flat.

## 2026-11-03 17:22 +04 — Home Builder flat shell

`legacy/tests/interior/hb_flat.blend` was built in Blender 5.2 with Home Builder 5. 15 geometry-node walls (the Apt 02 outline at 63 m2, plus the bedroom, storage and bathroom partitions), a floor, a ceiling, and four default base cabinets. Clear height 3.0 m is a stand-in. Door openings are not cut. The still is `hb_flat.png`. This is not the viewer flat. `twobed.glb` was not replaced.

## 2026-11-03 17:18 +04 — flat put back

The 19 MB BlenderKit `twobed.glb` is off the viewer again. Desktop loads the previous 1.5 MB flat (`ffd3ff4^`). Cache query is `twobed.glb?v=4`. Home Builder was not used for this file. Not deployed.

# Changelog

## 2026-11-03 17:15 +04 — door still, second pass

`tests/door_r8/door.png`, same locked camera as `e1_stairs.py`. Not in `out/`, `web/`, or on the live viewer.

- Stairs are solid blocks with a dark front face, then a landing. Rise 155 mm and going 270 mm are stand-ins.
- The opening has stone side walls and a set-back granite reveal, so it is not only a black card. The top of the opening is still dark.
- Each jamb is one overlapping leaf trail. It is not an acanthus carving. Leaf size is a stand-in.
- Each lion is a face, a ring of mane tufts, ears and a muzzle. Still geometric. Stand-in.
- LEGACY HOUSE is cut out of the stone band (boolean), with a dark recess behind the letters. The typeface is Blender's default.

Script: `legacy/tests/door_r8/build_door.py`. The diamond transom was not changed.

## 2026-11-03 17:10 +04 — door test, not the live hero

`tests/door_r7/door.png` is a new still on the locked door camera (45.65 mm, the same pose as `e1_stairs.py`). It is not in `out/`, `web/`, or on https://legacy-house-viewer.vercel.app.

What changed from the 5.6 still (`tests/door_r6/e1_stairs.png`):

- The bright ladder is gone. Twelve stone treads with dark risers start at the threshold and run back into the opening. Rise 160 mm and going 280 mm are stand-ins. NOT FOUND on the photo.
- A dark speckled inner border frames the opening. The stone species is NOT FOUND.
- Both pale jambs carry a leaf trail. Leaf size is a stand-in. They read as a carved repeat, not a smooth upright.
- The corner blobs are replaced by a mane, ears, muzzle and eyes. Stand-in, not a scan.
- The lintel carries the words LEGACY HOUSE. The typeface is Blender's default, not a measured carving.
- The diamond transom was not touched.

Script: `legacy/tests/door_r7/build_door.py`. GLB: `legacy/tests/door_r7/door.glb`.

## 2026-11-03 17:00 +04 — write the handoff into the repo

The root README still said this repo was transcripts only. `status.md` still described the flat as box furniture and a surroundings bot that had just been created. `SCORE_PLAN.md` and the unmerged test stills were only on the bot disk.

Recorded, from a live curl, not from a local guess:

- Public URL serves `app.js?v=19`, textured `hero.glb` at 1,927,812 bytes, and `twobed.glb` at 1,476,656 bytes.
- Git already has `app.js?v=21` and a 19 MB BlenderKit `twobed.glb`. That is not what the URL is serving. Not deployed.

Added the files that were missing from git: `SCORE_PLAN.md`, the door / arch / fire-escape / bath / viaduct test stills and stand-in GLBs, the door and west-elevation photos, and the dollhouse note at the end of `interior/critic_log.md`.

`legacy/README.md` no longer says to redeploy the viewer at the end of every pass. Deploy only when Colin says so. That matches `AGENTS.md`.

## 2026-11-03 16:37 +04 — BlenderKit furniture in the flat

Replaced the box sofa, box beds, tub chairs, and the old coffee table with free BlenderKit models (royalty-free): Peru 3-seat sofa, Odger dining chair x4, a double bed x2, and a coffee table. Source files are in `interior/assets/blenderkit/`. The desktop flat is `web/twobed.glb` (19 MB, unbaked). Mobile `twobed_m.glb` is unchanged. Not deployed.

## 2026-11-03 16:31 +04 — time of day no longer walks every street lamp

Night and dusk turned on 53 point lights (intensity 60). That recompiled the scene shader and made the viewer stall on a time-of-day change. The viewer now keeps 4 lamps nearest the building, intensity 30 at night and 12 at dusk, and redraws once.

BlenderKit 3.21.3 is installed in local Blender 5.2 and 4.5. The API key is stored in the Blender 5.2 user preferences only. It is not in this repo.

## 2026-11-03 16:22 +04 — restore the textured hero

The live building looked worse because commit `315f85b` replaced the web hero with an unbaked door-test export.

| File | Before (correct) | Deployed by mistake |
|---|---|---|
| `vercel-live/hero.glb` | 1,927,812 bytes, 3 meshes, 5 images, 39,276 verts | 2,402,120 bytes, 1,618 meshes, 2 images |
| `vercel-live/hero_m.glb` | 1,740,244 bytes | same unbaked file as desktop |

Restored both files from `bb65e67`. The viewer still has the freeze fix and the classic-script rebuild (`4f450bb`). Hero URLs are `hero.glb?v=2` and `hero_m.glb?v=2` so the browser does not keep the bad file. Page script on the public URL is `app.js?v=19`.

Not in this repo: the in-chat preview (`src/viewer/LegacyStage.tsx`) now requests the same `?v=2` hero. That file lives in the app sandbox, not here.

## 2026-11-03 — Undo the facade regression (Claude)
The c2f1308 glass pushed a painted stand-in room out over the glazing bars and fanlights, and the procedural stone tiles drew a square grid on the hero. Hero stone and faience are back on the exported GLB materials; the glass keeps its geometry and only gets a reflective material. Context blocks use flat brick, render and grey colours (tiled maps read as rubble, see Lessons); glass blocks and roofs are lighter so the aerial no longer reads navy. Interior ambient and bake tint warmed. Checks: legacy/tests/fix_r1/. Not deployed.
