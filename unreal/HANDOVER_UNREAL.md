# Ashwood 3D: Unreal Engine Agent Handover

Hey agent, read this first. This is everything you need to jump straight into Unreal Engine and carry on without hitting any of the snags or wasting context.

---

## 1. Golden Rules from Colin (DO NOT BREAK)
1. **Project Name**: Call it **Ashwood 3D** (or Ashwood Estates 3D).
2. **Git Branches**:
   - **NEVER** overwrite existing branches on GitHub.
   - **NEVER** force-push.
   - **NEVER** touch `main` without explicit approval.
   - Always push work to a clean new or dedicated branch (e.g. `lane/unreal-villa-photoreal`).
   - Every major step gets a `CHANGELOG.md` entry at the top, a commit, and a push.
   - Keep all committed files strictly **under 99 MB**.
3. **Design Rulings**:
   - **Courtyard**: Deep dark reflective water basin with planted pine island. **NOT pool blue**.
   - **Pool v3**: 4.80 m terrace between house and pool, pool water 9.50 x 3.60 m with seating.
   - **No balloon trees. No white grass cards.**
   - Villa structure: **GF, FF, and RF only (NO basement)**.
   - **Nanite must stay OFF** on imported villa/interior/planting meshes (otherwise UE draws corrupted low LOD fallback geometry).

---

## 2. Where Things Live On Disk
| Item | Absolute Path |
|---|---|
| **Live Unreal Project** (Working, not git) | `C:\Users\Alfa\Documents\Unreal Projects\ashwood_3d_estates` |
| **Git Working Repo** | `C:\Users\Alfa\.gemini\antigravity\scratch\ashwood-estates-3d` |
| **Unreal Engine Level** | `/Game/Main` |
| **Engine Version** | Unreal Engine 5.9.0 |
| **Editor MCP Server** | Built-in MCP at `http://127.0.0.1:8001/mcp` (session ID in scratch scripts) |
| **Python MCP Bridge Script** | `C:\Users\Alfa\.gemini\antigravity\scratch\ue_mcp.py` |
| **Screenshots / Viewport Captures** | `C:\Users\Alfa\.gemini\antigravity\brain\aba31526-b06f-475e-83d5-31004e393d02\` |

---

## 3. How to Talk to Unreal (The MCP Shortcut)
Do NOT struggle with lazy MCP tool discovery. In this environment:
- Port 8001 is the active editor process.
- Use the ready-to-run helper: `python C:\Users\Alfa\.gemini\antigravity\scratch\ue_mcp.py --eval "<code>"`
- Or execute a file: `python C:\Users\Alfa\.gemini\antigravity\scratch\ue_mcp.py --file "<path>"`
- To capture a viewport without moving Colin's camera:
  ```python
  import ue_mcp
  ue_mcp.capture_viewport("path.png", {"translation": {"x": 1363, "y": 1300, "z": 80}, "rotation": {"pitch": -15, "yaw": 90, "roll": 0}})
  ```
- If calling `execute_python` in UE, **NEVER** make HTTP requests back to port 8001 from inside UE python (it will deadlock on socket timeout). Call viewport captures from outside in shell python!

---

## 4. Current Scene Hierarchy & Actors in `/Game/Main`
- `Villa_Exterior`: Points to `/Game/Villa/villa_v5/villa_v5/StaticMeshes/SM_Villa_Exterior` at `(0, 0, 0)`.
  - **All 18 material slots mapped to PBR!**
  - Includes `M_PoolTile` (mosaic pool tile), `MI_Soffit` (stucco), `M_LED` (warm 3000K strip lights), `MI_Hedge` (dense boxwood), `MI_OutdoorWood`, `MI_OutdoorCushion`, `M_Water` (dark courtyard + pool teal), `M_Glass`.
  - **Courtyard Plinth is cut open!** In `villa_v5.glb`, `GF_plinth` was split into 3 boxes, opening up the recessed courtyard water basin (`[11.48..15.78] x [11.50..16.34]`) so the dark water and planter island are fully exposed!
- `Planting`: `/Game/Villa/Planting/planting_set/StaticMeshes/SM_Planting` at `(0, 0, 0)`.
  - Upgraded to `M_FoliageLeaf` (two-sided masked foliage with subsurface scattering) + `MI_Bark` on trunks.
  - 7 tuned leaf instances: olive, broadleaf1, broadleaf2, palm fronds, hedge leaves, pine needles, canopy.
- `Terrace_Furniture`: `/Game/Villa/Terrace/terrace_set/StaticMeshes/SM_Terrace_Furniture` at `(0, 0, 38)`.
  - Mapped with teak wood, linen cushions, and bronze frames.
- `Interior_GF`: `/Game/Rooms/GF/gf_house/StaticMeshes/SM_GF_House` at `(878, 1547, 45)`.
- `Interior_FF`: `/Game/Rooms/FF/ff_house/StaticMeshes/SM_FF_House` at `(878, 1547, 445)`.
- `IL_GF_*` and `IL_FF_*`: 29 warm interior point lights (currently 15,000 lm staging value).
- `SunSky_C_1`, `ExponentialHeightFog_2`, `PostProcessVolume_1`: Lighting and atmosphere.
- Leftover template `Floor` and empty `InstancedFoliageActor` have been **deleted**.

---

## 5. What Was Just Done in This Session
1. **Material System Upgrade**:
   - Created procedural mosaic pool tile `M_PoolTile`.
   - Created stucco soffit `MI_Soffit`.
   - Created architectural warm LED strip `M_LED` (3000K emissive glow).
   - Created boxwood hedge `MI_Hedge`.
   - Created master foliage shader `M_FoliageLeaf` (`MSM_TWO_SIDED_FOLIAGE`, alpha masked, waxy roughness, translucent subsurface scattering) and 7 leaf instances.
   - Mapped all terrace furniture materials.
2. **Courtyard Water Basin Solved (`villa_v5.glb`)**:
   - We discovered why the courtyard looked like solid stone: `GF_plinth` was an un-cut solid block covering the basin at height 45.4 cm while the water was at 33 cm.
   - Built `exterior_export/cut_courtyard.py` to subtract the courtyard box.
   - Imported `villa_v5.glb` with `bCombineMeshes=True`.
   - Now the dark, calm, reflective water basin (`M_Water`) completely surrounds the raised planter island and pine tree.
3. **Saved and Synced**:
   - Packages and map saved.
   - Synced to git working copy.

---

## 6. What You Should Tackle Next (In Priority Order)
1. **Courtyard Island Mulch & Secondary Planting**:
   - The pine tree is standing on the raised island. In `SM_GF_House`, there are white needle cards under the tree that can be removed or textured with dark pine bark mulch/pebbles.
   - Add low architectural groundcover / Japanese boxwood or stones around the island base.
2. **Interiors Detail & Wall Tints**:
   - The interior walls facing the window cutouts are plain white. Apply soft warm plaster or wood slat accent materials to the visible interior walls (e.g. master bedroom headboard wall, entrance feature wall).
   - Check FF alignment from inside the rooms.
3. **Lighting & Lumen Pass**:
   - Point lights (`IL_GF_*`, `IL_FF_*`) are at 15,000 lm staging intensity. Dial them down to realistic architectural values (~2,000 - 3,500 lm) and enable contact shadows.
   - Balance SunSky exposure in PostProcessVolume so interior views look naturally exposed without blowing out the pool outside.
4. **Context Ground**:
   - The large neutral ground outside the plot boundary is grey asphalt. Blend it with context sand/gravel or desert planting so the plot edges blend seamlessly into the horizon.

---

## 7. Syncing Your Work to Git
After making edits in the editor:
```python
# 1. In Unreal Python:
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
unreal.EditorLevelLibrary.save_current_level()

# 2. Run sync script:
python C:\Users\Alfa\.gemini\antigravity\scratch\save_and_sync.py

# 3. Add CHANGELOG.md entry, commit and push to a new branch!
```
Good luck, the villa is looking incredible!
