# Step 2: Layout

Target: `../../refs/exterior_target.png`, used for **look only** (Colin, 2026-11-03). The building's shape stays as sourced; the street layout around it is read from the image and mapped onto the real site already in the scene (OSM roads, kerbs and lamps; LIDAR terrain).

Script: `../step2_layout.py` (re-runnable). Scene: `../legacy_ext7.blend`, collection `EXT7_Layout` (guides only, hidden in final renders).

## Cameras framed like the target
| Camera | Target panel | Notes |
|---|---|---|
| `CAM_T1_front` | 1 (top left), square-on front | Placed on the far kerb at y −27. The real viaduct runs across the street at about y −35, so the target's distance can't be matched from the street. |
| `CAM_T6_corner` | 6/7 (bottom middle and right), raised 3/4 down the street | 6.5 m up, like the target |
| `CAM_T5_aerial` | 5 (bottom left), high 3/4 aerial | |
| `CAM_PLAN` | — | Top-down check view |

Comparisons: `compare_T1_front.png`, `compare_T6_corner.png`, `compare_T5_aerial.png`.

## Site facts read from the scene
- Front facade line: y = −12.9 m (`HERO_body`).
- Front pavement: y −15.6 to −12.9, so about 2.7 m deep (`road_1423359051`, Paving).
- Carriageway: Whitworth Street West (`road_155768981`, Asphalt). Viaduct beyond it.

## Layout read from the target, mapped to the site
| Element in target | Where it goes here | Source / status | Built in |
|---|---|---|---|
| Wide pale stone-flag pavement | Front pavement zone (blue marker) | Paving material swap. Flag size is stand-in. | Step 3 materials |
| Granite kerb along the pavement edge | `LAY_kerb_line`, y −15.6 (yellow) | No kerb mesh along the front today | Step 3 |
| Double yellow lines at the kerb | `LAY_double_yellow` | Seen in target and in `refs/critic1/real_geograph.jpg` | Step 3 |
| Black lamp columns along the kerb | `LAY_lamp_column_0..2` | Spacing stand-in | Step 3 |
| Traffic signal pole by the entrance | `LAY_signal_pole` | Real: `refs/door.jpg`, `refs/critic1/real_commons.jpg` | Step 3 |
| Dark asphalt road with white lane markings | Existing carriageway and markings | Exists; colour and wear in Step 3/4 | Step 3–4 |
| Bright sky with broken cloud | `LAY_sky_dome_note` (green) | Sky dome and world | Step 3 materials |
| Warm cream stone and faience | Hero materials | Look from target; shape unchanged | Step 3 materials, Step 4 grime |
| Cars and vans in the street | Road lanes | Motion | Step 7 |

Left out on purpose (in the target, not on the real front): bollard rows, front railings, street trees, the balustraded parapet, the brick ground floor.

## Defects found
- `lamp_post.051` and `lamp_post.052` (with their heads and lights) stand **inside** the building: a raycast from above at each post hits `HERO_body`. Marked `LAY_FIX_*` (red). Move or remove in Step 3.
- `Cylinder`–`Cylinder.005` in front of the arches are boolean cutters in `HERO_cutters`, hidden in renders. Not a defect.

## Not done in this step
No geometry, materials or sky changes. Those are Step 3.
