# Unreal model vs approved V4 CAD: plan check (4-bed villa)

Date: 2026-11-12 (Asia/Dubai). Branch `lane/unreal-villa-courtyard`.
References: `active/approved-cad-v4/png/FP-4B-GF_V4_preview.png` and `FP-4B-FF_V4_preview.png` (approval `pt16u`, unchanged).
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

## Method (repeatable)
1. `extract_plan_geometry.py` (in editor) writes walls (vertical faces 120 cm or taller), floor plates and stair treads per floor, in world cm.
2. `overlay_cad.py` (outside, `uv run --with pillow --with numpy`) extracts the dark CAD wall mask and searches scale and offset so the model walls land on the CAD walls. It writes `overlay_<floor>.png`.
3. Stacking check: FF walls drawn over GF walls in world coordinates (`reports/stack_*.png`). Stair, lift and courtyard are vertical cores and must stack.

## Results

| Check | Result | Evidence |
|---|---|---|
| GF rooms vs CAD | PASS. All rooms and walls in place. Registered at 43.5 px/m against the sheet's scale bar of 42.8 px/m (1.6%). | `reports/overlay_gf.png` |
| FF rooms vs CAD (old mesh) | FAIL. The interior was about 5.8% oversized and shifted; the footprint clip had cut away the west strip (master suite, bath 2, bedroom 2 west wall). The cores did not stack: stair 156 cm west, lift about 120 cm west, courtyard offset. | `reports/overlay_ff.png`, `reports/stack_gf_ff.png` |
| FF rooms vs CAD (v2) | FIXED. Refit from the unclipped capture: plan scale 0.94483 with offset +1.19375 / -1.40523 m (glTF x/z), then clipped to the FF envelope (world X 300-1590, Y 320-2680). Fit score at the GF-verified sheet mapping went from 0.092 to 0.262. Outer walls, lift, courtyard and open-to-below now stack on GF. | `reports/overlay_ffv2.png`, `reports/stack_gf_ffv2.png` |
| GF to FF stair | FAIL, OPEN. The GF flight (slot 15, X 758-893) has 16 risers of about 18.8 cm and rises from Z 45 to Z 345, the GF ceiling. The FF floor is at Z 445 (the shell uses 4.0 m floor to floor; the interior captures assume 3.0 m). The flight stops 1.0 m short, under the GF ceiling, with the shell slab (Z 395-445) above it. | geometry query |
| FF to RF stair | FAIL, OPEN. Same 3.0 m flight (Z 464 to 726). It meets the FF ceiling at Z 745, below the roof slab (Z 775-845). The RF interior is not placed in the level. | geometry query |
| Courtyard light-well | FAIL, OPEN. The shell slab at Z 395-445 and the roof (Z 775-845) span the courtyard, as do the FF floor plate and the GF ceiling. CAD shows it open on FF. | geometry query, earlier captures |
| Double-height entry ("OPEN TO BELOW") | FAIL, OPEN. Covered by the GF ceiling, the shell slab and the FF floor plate. | geometry query |
| Doors and room access | NOT YET RUN. Planned as a navigation-mesh reachability test from the pedestrian entry to every room, up both stairs. | |

Measured offset of the refitted FF stair against the CAD: X 736-866 against CAD X 752-897 (about 20 cm), within the sheet's declared ±3% working uncertainty.

## Update: stairs, voids, doors and access (later the same day)

Walk test (`walk_check.py`): a person capsule (radius 22 cm, clear from 30 to 190 cm above the floor) on a 20 cm grid, steps of 25 cm or less, flood fill from the street; a room passes when reached floor lies within 1.5 m of its V4 label point. Map: `reports/walk_map.png`.

**Result: 35 of 35 places reachable** (34 before the north balcony fix): all 16 GF spaces including the pool terrace, the full FF (corridor, lift, master suite, M.dressing, M.bath, family living, bedroom 1, bath 1, bedroom 2, dress, bath 2, junior suite group, SW and SE balconies), and the RF stair arrival and roof terrace.

| Item | Fix |
|---|---|
| Stairs | Two stacked 21-riser flights, 4.0 m each. GF to FF climbs north from Y 1984 to Y 1438; FF to RF climbs north from Y 1855 to Y 1309 so the corridor passage to bedroom 2 stays free. Headroom is 2.1 m or more everywhere (arrival 2.5 m, between flights 2.7 m). |
| Voids | Courtyard light-well and double-height entry opened through ceilings, floor, slab and roof. |
| Shell phantom walls | The massing boxes' shared faces are clipped away exactly. |
| Doors | Front door plus 3 entrance steps (the plinth is 45 cm with no steps), living slider, master and bedroom 1 to the N balcony, bedroom 2 to SW, junior suite to SE, roof pavilion door. FF interior: master suite to dressing (through joinery), dressing to bath, bedroom 2 door, bath 2 door, dress open to bedroom 2, all at V4 positions. |
| Site | Planting collision was one box over the whole site; set to NoCollision. |

**North balcony (resolved, 35 of 35).** In the master suite the bed wall group was 144 cm east of the outer wall and the bed was turned head-north across the room. Both were moved to the V4 arrangement: bed head on the west wall between the bedside tables, chair and side table in the north-east corner. The bedroom 1 door was moved east of the low unit (X 1370-1475). Both doors are now walked through (16 and 9 reached cells in the doorways).
