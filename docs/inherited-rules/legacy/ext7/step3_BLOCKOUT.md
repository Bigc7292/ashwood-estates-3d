# Step 3: Blockout

Script: `../step3_blockout.py` (re-runnable from the Step 2 scene). Helpers: `../ext7_common.py`. Renders: `step3_CAM_*.png` (Cycles CPU, 16 samples, denoised, 768×512).
Order followed: boxes → space → models → materials.

## Boxes
- Removed `lamp_post.051/.052`, their heads and `StreetLight.051/.052`: they stood inside the building (Step 2 raycast).
- Granite kerb along the front, 10 segments, top flush with the pavement and dropping to the road (heights raycast from the existing surfaces). 300 mm wide: **stand-in**.
- Double yellow lines: 100 mm lines with a 100 mm gap (UK road-marking standard), on the road surface beside the kerb.

## Space
- New world `EXT7_World`: a physical sky lights the scene; the camera sees a blue gradient sky with procedural cloud (noise on the sky dome, faded toward the horizon). They're split because the physical sky burned to white and went orange near the sun. Cloud cover is tunable through node `EXT7_cloud_cover`.

## Models
- Three black lamp columns along the kerb (`EXT7_lamp_*`): base, tapered shaft, arm, lantern with lens and a spot light (off by day). Positions and sizes are **stand-in**, following the target's look.
- Traffic signal by the entrance (`EXT7_signal_*`): pole, white backboard, black head, red/amber/green lenses with hoods. It's real (seen in `refs/door.jpg` and `refs/critic1/real_commons.jpg`). Sizes **stand-in**.

## Materials
- Faience and Portland stone tinted warm cream (`EXT7_tint` multiply node), per the target and both real photos. No new tiling, per the lesson that tiled stone reads as rubble.
- Paving: block pavers replaced with pale stone flags, procedural, laid in stretcher bond with per-flag variation, thin joints and bump. 600 mm flag: **stand-in**. Also applied to the open ground (`Terrain_EA_DTM`).
- Asphalt darkened; roofs made matte (they read glossy white from the air); the concrete-block sides lifted from near-black to mid-grey.
- Window frames stay white: that's what both real photos show. The target's dark frames aren't real.

## Left for later steps
Wear on every surface (Step 4), signs and stickers (Step 5), close-up critique (Step 6), motion (Step 7).
