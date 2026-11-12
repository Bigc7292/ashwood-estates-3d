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
