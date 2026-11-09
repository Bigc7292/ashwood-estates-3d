# Step 3 proportion check (boxes stage, before any detail)

Proportions were fixed at the BOXES stage; later stages add no massing changes except image-read detail (slats, glazing, trees).

| Element | CAD V4 (m) | Blender boxes (m) | Result |
|---|---|---|---|
| Site (plot) | 18.72 x 29.88 | 18.72 x 29.88 (WALL_side_*, GROUND_paving_plot) | match |
| GF footprint | 12.65 x 22.03 (3.13..15.78 x 4.76..26.79) | 12.65 x 22.03 (GF_rear/mid/front/multipurpose) | match |
| FF envelope | ~12.96 x ~21.07 (2.92..15.88 x 2.93..24.0) | 12.96 x 21.07 + front balconies to 26.79 | match (FF trace ±3%) |
| Pool | 9.49 x 2.38 | same (POOL_water from model.json) | match; image POOL ~3:1 logged as image error |
| Courtyard | 4.30 x 3.69 (11.48..15.78 x 12.65..16.34) | same; FF void snapped | match |
| Storey heights | no CAD sections | GF 0.45..3.95, slab 0.50, FF 4.45..7.75, roof fascia 0.70 to 8.45, RF core to 11.45 (image-read) | image-read. ELEV-REAR measured (px 208..745 wide, deck 485 to roof top 130): width/height = 1.51 (perspective, camera below soffits, approximate). Boxes first pass was 1.69 with a 0.45 m roof; roof fascia deepened to 0.70 m and slab to 0.50 m per image, giving 12.96/8.0 = 1.62. Remaining ~7% is within image-reading tolerance; logged, not forced. |
| Carport | not on plan | 7.6 x 5.7 on CAD parking zone, top 3.45 | render-sourced |
| Stone fin | not on plan | 0.5 x 7.85, top 11.6 | render-sourced |
