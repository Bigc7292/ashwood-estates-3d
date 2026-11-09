# Step 5: Printed matter

Scripts: `../step5_prints.py` makes the prints as flat images in `../prints/`. `../step5_place.py` puts them in the scene (collection `EXT7_Prints`) and ages them in the shader. Renders: `step5_CAM_*.png`, with close-ups `CAM_close_lintel` and `CAM_close_pole`.

| Print | Where | Source | Ageing |
|---|---|---|---|
| BARCLAY HOUSE lettering | Entrance lintel (`HERO_door_lintel`), placed by raycast | Real: carved on the lintel in `refs/door.jpg` | Incised: darker, rough, bumped in; slightly broken by noise |
| Street nameplate "WHITWORTH STREET WEST" | Front stone base near the east end, 2.6 m up | UK nameplate pattern; placement **stand-in** | Light fade and grime |
| "FOUND GREY CAT" notice | Signal pole | Invented; the phone digits use the 07700 range, which is reserved for fiction | Faded, dirtied, torn edges with white paper fringe |
| Stickers: MOTH, NORTHERN SKATE CO., LOUD RECORDS, code square, smiley | Signal pole and the three lamp columns | Invented. No real brands | Faded, desaturated, peeled edges |

How the ageing works: the print colour is desaturated and washed toward paper in noisy patches, then dirt is multiplied over it. Peeling cuts the alpha wherever the distance to the print's edge falls below a noisy threshold, and leaves a white torn-paper fringe just inside the tear.

The target's "R. BARCLAY & CO" fascia band was left out: it isn't on the real building.
