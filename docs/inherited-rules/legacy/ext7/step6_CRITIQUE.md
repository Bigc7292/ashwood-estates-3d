# Step 6: Critique

Colin left no notes this round, so the critique is against `refs/exterior_target.png` (look) and `refs/critic1/real_geograph.jpg` / `real_commons.jpg` (facts), using close-ups. Each defect was found in a render and traced to its cause with a raycast before it was fixed. Script: `../step6_critique.py`. Renders: `step6_CAM_*.png`. Comparisons: `compare_T6_corner.png`, `compare_T1_front.png`.

| # | Defect (where seen) | Cause (how found) | Fix |
|---|---|---|---|
| D1 | White patches on the road; the double yellows hidden (T6) | Raycast: `Terrain_EA_DTM` poking through the asphalt at (−15.0, −24.4) and (4.7, −17.5); the Step 3 flags made it read white | Terrain lowered 0.15 m. It's only base ground. |
| D2 | Pale blue bands on the curved concrete side (T6) | Raycast: upward ledges in `Concrete_block_sides_rear` mirroring the sky | Concrete made matte |
| D3 | Right-hand neighbour near-black (T6, T1) | Raycast: `Neighbour_grey_cladding` | Lifted, then superseded by D9 |
| D4 | White marble-like speckles on the entrance doors (lintel close-up) | Step 4 door grime mixed toward light grey | Grime colour set darker than the paint |
| D5 | Found-cat notice too small to read as paper (pole close-up) | 0.13 × 0.19 m | Scaled to A5, 0.148 × 0.21 m |
| D6 | Upper faience nearly new from the street (T1) vs target and photos | Step 4 streak strength | Faience streaks 0.42 → 0.6 |
| D7 | Fine streaks like falling rain on big walls (aerial) | Suspected Step 4 rain-streak noise too fine | Streaks broadened and halved on neighbours and concrete sides. Not the main cause; see D9 |
| D8 | Same pattern | Suspected AO grain (8 samples) | AO reach on plain neighbour walls cut to 0.05 m. Not the main cause; see D9 |
| D9 | Same pattern | The neighbours' concrete photo texture, stretched up tall walls by their UVs and revealed by the earlier lightening | Photo swapped for flat colour on plain neighbour walls (project lesson: tiled photo textures read badly) |

## Still short of the target (not fixed this round)
- The faience shows no block joints from the street; the real photos do. The project lesson warns against tiled stone, so this needs a joint mask driven by geometry, not a texture.
- Glass reads near-black with little reflection. The target and photos show sky and interiors.
- The hero's concrete side and rear read brown and streaky.
- No people, cars or street clutter yet (cars come in Step 7).
- Lamp, signal, kerb and flag sizes are stand-ins.

## Score
Not scored here. Project rule: a bot doesn't score its own still. Needs Colin's notes or an independent critic.

## Colin's notes, 2026-11-08 (`step6b_colin_notes.py`, renders in `step6b/`)
- C1, window glazing bars read white (windows and arches). The real photos (`refs/critic1/real_geograph.jpg`, `refs/door.jpg`) and Google Street View show them dark. The cause was that `Window_frame_dark` had a near-white colour (0.78), and `export_glb.py` mapped it to "Window_frame_white_painted". The fix: dark painted steel (0.016 linear) in the Blender scene, and in the live viewer files through `fix_frames_glb.py`. In `hero.glb` that is palette swatch 4; in `hero_m.glb` it is the material colour. Both still pass the validator.
- C2, "LEGACY HOUSE" over the entrance was not clearly visible. Ours was dark text printed on pale stone. `refs/door.jpg` shows pale raised serif capitals on a dark, polished, speckled granite band, and the same granite frames the door opening. The fix: granite facings on the lintel and the inner jambs, plus real 3D letters (DejaVu Serif, free, 0.11 m caps). The letters are centred in the 0.18 m of granite that shows below the fanlight sill. These are exported to the viewer in `ext7_street.glb` (collection `EXT7_Colin`). The viewer also gets an "Entrance" camera button.
