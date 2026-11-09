# Step 4: Grime

Script: `../step4_grime.py` (runs on the Step 3 scene). Renders: `step4_CAM_*.png`, including the new close-up `CAM_close_entrance`.
All wear is procedural: world position, ambient occlusion and noise. Nothing tiles and nothing is painted by hand.

| Surface | Wear added |
|---|---|
| Faience, Portland stone, concrete block, neighbours, viaduct | Large weathering patches; soot in recesses and under ledges (AO, broken by noise); rain streaks a few metres long (noise stretched along Z); lighter rain-washed runs; splash and dust up to 1.4 m; dust on sills and cornice tops; rougher where sooty |
| Window frames | Dirt in corners, flaking paint, dust on sills |
| Glass | Dust film (rougher, slightly grey) |
| Stone flags | Gum spots, dark stains, slight patchiness |
| Asphalt | Oil stains (slightly glossier), patch repairs, faint lighter wheel paths |
| Road markings, double yellows | Worn through to the asphalt in patches, dirtied |
| Granite kerb | Road dirt on the face, grime in the arris |
| Lamp columns, signal pole | Chipped paint to grey primer, rust near the base, base dirt, dust on top |
| Door | Kick scuffs, grime |

## Fixes made in this step (found in the Step 4 renders)
- Portland stone: the old image texture read as rubble walling up close. Replaced with flat buff (lesson: tiled stone reads as rubble). The geometry's own rustication channels carry the block lines.
- Exposure set to −0.7. At 0, sunlit stone clipped and AgX drained its colour to grey-white.
- The sky's light is desaturated; the sky the camera sees stays blue. The strongly blue physical sky had turned the front facade grey-blue.
- Faience tint warmed slightly.
- Asphalt oil gloss and wheel-path lightening toned down; at first the road read wet and streaky.
