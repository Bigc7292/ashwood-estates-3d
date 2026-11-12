# Ashwood 3D: Unreal Engine handover

Last updated 2026-11-12 (Asia/Dubai). Branch `lane/unreal-villa`. Read this before touching the Unreal project.

## Rules from Colin (do not break)

- Call the project **Ashwood 3D**.
- Never overwrite existing code on GitHub, never force-push, never touch `main` without Colin's go-ahead. Work on `lane/unreal-villa` or a new branch.
- Every edit gets a `CHANGELOG.md` entry at the top, a commit and a push. The repo is public: no keys or tokens. Keep every file under 99 MB.
- Design rulings: the courtyard is a **dark water basin with a planted island**, not pool blue. Pool v3: **4.8 m terrace** between house and pool, **pool 9.50 x 3.60 m**, with seating. **No white grass cards. No balloon trees.** The 4-bed villa has **GF, FF and RF only, no basement**.
- Colin watches the Unreal editor live. Before each change, frame the viewport tightly on the thing being changed and tell him what he should see. Post a still after each step.
- No pauses for confirmation on ordinary steps. Keep replies short.
- Blender on the same PC is shared with other work: never reset its file.

## Where things are

| What | Where |
|---|---|
| Unreal project (live, on Colin's PC) | `C:\Users\Alfa\Documents\Unreal Projects\ashwood_3d_estates` (not a git repo) |
| Copy of the project in git | `unreal/ashwood_3d_estates/` (`Content`, `Config`, `.uproject`; `Saved`, `Intermediate`, `DerivedDataCache` left out) |
| Level | `/Game/Main` |
| Engine | UE 5.9.0 |
| MCP server | the editor's built-in MCP, `http://127.0.0.1:8001/mcp` (`.mcp.json` in the project folder; port 8000 was taken) |
| Capture and build scripts | `unreal/ashwood_3d_estates/interior_export/` and `exterior_export/` |

To sync the git copy after working in Unreal: save in the editor, then copy `Content` from the live project over `unreal/ashwood_3d_estates/Content`, log, commit, push.

## Level contents (`/Game/Main`)

| Actor | Mesh | Location (cm) | Notes |
|---|---|---|---|
| `Villa_Exterior` | `/Game/Villa/villa_v4/StaticMeshes/SM_Villa_Exterior` | 0, 0, 0 | Nanite off. Window openings cut, pool v3, balloon trees and old hedges removed (`villa_v4.glb`) |
| `Interior_GF` | `/Game/Rooms/GF/gf_house/StaticMeshes/SM_GF_House` | 878, 1547, 45 | 345k tris, 142 materials, Nanite off |
| `Interior_FF` | `/Game/Rooms/FF/ff_house/StaticMeshes/SM_FF_House` | 878, 1547, 445 | 203k tris, 104 materials, Nanite off |
| `Planting` | `/Game/Villa/Planting/planting_set/StaticMeshes/SM_Planting` | 0, 0, 0 | Viewer trees, hedges, palms, pine; leaf cutout. Nanite off |
| `Terrace_Furniture` | `/Game/Villa/Terrace/terrace_set/StaticMeshes/SM_Terrace_Furniture` | 0, 0, 38 | Sofa, 2 armchairs, coffee table, 2 loungers, side table, parasol |
| `IL_GF_*`, `IL_FF_*` (29) | point lights | ceiling height | 3000 K, 15,000 lm, no shadows (staging value) |
| `SunSky`, `ExponentialHeightFog`, `PostProcessVolume` | | | Post-process overrides: AO 0.6, bloom 0.5 |
| `Floor` | template floor | | Leftover from the blank map, small, can be deleted |

`/Game/Rooms/RF` holds the roof-floor capture, but it is **not placed**: it was rough massing that duplicated the exterior roof.

## Materials (`/Game/Villa/Mat`)

- `M_WorldAligned`: world-space projected colour, normal and roughness, with `Tint`, `TileSizeCm`, `RoughnessScale`. Needs no UVs. Instances: `MI_Stone`, `MI_Paving`, `MI_Lawn`, `MI_Ground`, `MI_Bark`, `MI_Bronze`. Textures in `/Game/Villa/Tex` come from `exterior-garden-3d/4b/tex/`.
- `M_Water`: two panning engine ripple normals. Pool teal by default; the dark basin colour applies within 5.6 m of `BasinCenter` (courtyard).
- `M_Glass`: translucent with Fresnel opacity. Instances: `MI_GlassBalcony`, `MI_GlassInterior`, `MI_SheerCurtain`.
- Slot mapping on the villa mesh, used every time it is re-imported: stone and stone_rf to Stone; paving, deck and coping to Paving; lawn and context_lawn to Lawn; ground to Ground; bark to Bark; bronze to Bronze; water to `M_Water`; glass to `M_Glass`; balglass to `MI_GlassBalcony`. The rest (soffit, pooltile, furniture, cushion, led, hedge, palmleaf, leaf) are still the flat imported glTF materials.

## Pipeline (how the assets were made)

1. **Exterior:** `exterior-garden-3d/4b/villa-materials.glb` (unchanged) goes through `exterior_export/openings.js` (holes behind the 23 glass panes), then `exterior_export/pool_v3.js` (pool and terrace), producing `villa_v3.glb`.
2. **Interiors:** the walkable web viewers in `production-line/artifacts/2026-11-10/ground-floor_r3.html` and `2026-11-10b/first-floor_r6F.html` are loaded in headless Chrome by `interior_export/extract.js`. It hooks three.js scene creation, clicks "3D Scene", resets the walls' 0.001 rise-animation scale, and writes a GLB merged by material. Then `clip.js` gives materials unique names (Unreal merges sections by material name) and cuts each floor to the house footprint, about 8 cm inside the shell.
   - GF: `node clip.js gf_interior.glb gf_house.glb -5.62 6.97 -10.74 11.29`
   - FF: `node clip.js ff_interior.glb ff_house.glb -5.83 7.07 -12.46 11.24`
3. **Terrace furniture:** `exterior_export/serve.js` serves `exterior-garden-3d/4b/` (it needs the vendored three.js under `model/vendor`). Then run `FILTER='^PROC_(sofa|armchair|coffee_table|lounger|side_table|parasol)' node extract.js http://127.0.0.1:8765/villa.html terrace_furniture.glb`, then `clip.js` to rename materials.
4. **Lights:** `interior_export/lights.js` reads the viewer light positions into `gf_lights.json` and `ff_lights.json`. Lights at 2.75 m height become `IL_*` point lights at viewer x * 100 + 878, viewer z * 100 + 1547.

The viewer frame maps to Unreal as: Unreal X = viewer x * 100 + 878, Unreal Y = viewer z * 100 + 1547, Unreal Z = viewer y * 100 + floor (GF 45, FF 445). The exterior GLB maps as Unreal X = glTF x, Unreal Y = glTF z, both in cm.

## Working with the MCP (lessons learned)

- Imports and Nanite toggles on the big interior meshes (GF especially) take 1 to 4 minutes, and the MCP call times out first. The work still finishes. Wait on the editor log (`Saved/Logs/ashwood_3d_estates_2.log`, line `Built static mesh [..s] /Game/...`) before the next call, or calls return "slow task".
- **Turn Nanite off** on every imported mesh. Otherwise the viewport draws a low fallback mesh (the villa showed 978 triangles with slanted walls).
- `SetCameraTransform` moves whichever viewport was last clicked, which may be Colin's second viewport. For checks, use `SceneCaptureToolset.CaptureEditorViewport` with `viewportId` set to Viewport 1's id (from `ListEditorViewports`) and a `captureTransform`. That moves no camera.
- The capture fails when the viewport tab is hidden or minimized. Ask Colin to bring the editor forward.
- Re-importing to a new folder name (for example `villa_v3`) creates a new mesh. Point the actor at it, re-apply the slot mapping above, turn Nanite off, then delete the old folder.

## State and what is next

Done: villa import and mesh fix; GF and FF interiors with materials, walls and floors; interior ceiling lights; textured stone, paving, lawn, ground, bark and bronze; glass and water; window openings; pool v3 with terrace seating.

Not verified:
- FF alignment from inside.
- Front, side and FF facades through the new openings (rough wall ends may show).
- Courtyard basin up close.
- Pool steps and the far pool edge.

To do, in Colin's priority order ("everything outside and inside ultra realistic"):
1. **Planting:** balloon trees replaced (`prune.js`, `planting_set.glb`). Still to do: courtyard island planting, leaf colour variety (viewer vertex colours are lost), context palms beyond the plot.
2. **Remaining flat materials:** soffit, pool tile, outdoor furniture, cushions.
3. **Interiors:** surfaces that were vertex-coloured in the viewer import white. The ceilings are cold. Furniture fabrics and wood have no detail. Check FF from inside.
4. **Lighting:** exposure and sun angle, interior light levels (15,000 lm is a staging value), shadows.
5. **Context:** the large grey ground outside the plot, and the leftover `Floor` actor.
