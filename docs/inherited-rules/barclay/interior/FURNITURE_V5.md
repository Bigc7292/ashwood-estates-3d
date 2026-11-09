# Two Bed v5: furniture upgrade (2026-11-08)

Colin's note: "the quality of the furniture is very block style, not realistic".
The live interior had been `twobed_lit_opt.glb` (from `build_twobed_v3.py`), where every piece was built from boxes.

## What changed
| Item | Before | Now | Source / licence |
|---|---|---|---|
| Sofa | box sofa | rounded 3-seater, baked texture recoloured navy (listing: navy velvet 3-seat) | BlenderKit "Peru 3-Seater Sofa", royalty-free (`assets/blenderkit/LICENCE.json`) |
| Dining chairs (4) | box tub chairs | moulded shell chairs, cream shell, black legs | BlenderKit "ikea odger dining chair", royalty-free |
| Mattresses, duvets, pillows, throws, cushions | boxes | soft modelled: bevel + subdivision + slight wrinkle displacement, turn-down band, puffed and tilted pillows | modelled in `upgrade_furniture_v5.py` |
| Bedsides, TV bench, coffee and dining tables, wardrobes, kitchen units, peninsula, headboards, rug | sharp boxes | 8 mm bevels (rug 4 mm) | same script |

Room shell, kitchen, bathroom, positions and floor plan are unchanged. Furniture sizes are the assets' own and not measured from the flat; positions are the v3 ones (illustrative, as before).
Also fixed: v3 left textured parts without UV maps (dining table top, headboard flutes). The live file had 3 glTF validator errors; v5 has 0.

## Files
- `upgrade_furniture_v5.py`: runs on `web/twobed_lit.glb` and writes `web/twobed_lit_v5.glb` (raw).
- `undraco.mjs`: the BlenderKit files are Draco-compressed and this Blender build has no Draco decoder. Decode them first: `node undraco.mjs assets/blenderkit/sofa.glb <dir>/sofa.glb` (same for `dining_chair.glb`), then `python3 upgrade_furniture_v5.py <dir>`.
- Compression (glTF-Transform, free): dedup, prune, textures 1024 px JPEG, quantize, meshopt: `vercel-live/twobed_v5.glb` (2.5 MB). The phone file merges meshes by material with 512 px textures: `vercel-live/twobed_v5_m.glb` (2.0 MB). Both pass the Khronos validator with 0 errors.
- The viewer loads `twobed_v5.glb?v=1` (desktop) and `twobed_v5_m.glb?v=1` (phone).

## Not done yet
- The bathroom fittings and kitchen appliances are still simple shapes.
- The street photo seen through the windows (the `Window_*_backdrop` image) appears upside down in places. That backdrop is from v3 and was not changed here.
