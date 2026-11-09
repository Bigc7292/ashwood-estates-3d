# Ashwood Estates: 4-bed villa, ground floor. Floorplan 3D viewer spike (FP-4B-GF), **v2**

**Status: REVIEW-PENDING SPIKE. One floor only.** Not survey-verified, not construction-ready, not certified CAD.

v2 rebuild (2026-11-09, Asia/Dubai) after the user rejected v1 as "still 2D". v1 sits in `v1/` for comparison and is superseded. v2 turns the upstream Floorplan 3D features back on, so the floor reads as a furnished 3D interior: room floors with materials, furniture models, ceilings and ceiling lamps, shadows, RoomEnvironment reflections and warm daylight. Walls stay at full height by default, and eye-level renders are used. Every addition is tied to source evidence or flagged as derived or assumed below.

## Use
```bash
cd active/floorplan3d-spike/FP-4B-GF
python3 -m http.server 8000 --bind 127.0.0.1   # open http://127.0.0.1:8000/
```
Fully offline: three.js r160 + Water2 are vendored in `vendor/`, with no CDN and no account. Press `T` or use the top switch for 2D / 3D. In 3D, **Full walls** (3.0 m, display-only) is the default and **Cut walls** is 1.2 m. Use Orbit or Walk (WASD + mouse, or the joystick on touch). Click a room in the list to fly to it. The sun slider defaults to 16:00, a display-only value because site orientation is unknown. Night mode turns the ceiling lamps on. `[` and `]` hide the side panels. Furniture can be moved, rotated or deleted in the viewer, which is the upstream behaviour, and edits are stored in localStorage under `ashwood-fp3d-spike-4b-gf-v2`. `?water=flat` forces the flat-water fallback.

## What v2 re-enabled from the upstream viewer
- **ROOMS**: 16 closed room polygons with per-room floor material (MATS), derived ~areas, ceilings and a ceiling lamp at each label point, and the upstream room panel (floor material picker, area).
- **Furniture**: `buildFurniture()` models from the upstream LIB, placed only where the source draws a symbol (see below). In v1 this was empty.
- **Lighting and materials**: upstream HemisphereLight, shadow-casting DirectionalLight sun (4096 shadow map, extent widened to 17 m for this larger floor), PMREM RoomEnvironment reflections, ACES tone mapping and procedural floor textures, all unchanged. Warm daylight comes from the sun defaulting to 16:00.
- **Full-height walls** are the default view. Eye-level and low-oblique cameras are used for the renders.
- **Stairs**: display-only stair massing. The 16 treads come from the V4 tread lines. Riser height is the display wall height divided by 16, and the rise direction is assumed.
- Kept from v1: traced walls, 6 doors that open and close, 12 glazing runs, Water2 on the pool and courtyard water with a labelled flat fallback, walk mode and the offline vendoring.

## Room polygons (DERIVED, not stated in source)
Room polygon = traced V4 wall inner faces, read from the 2x wall raster, closed with straight segments across openings (closures_px). Derived, not stated in source. Areas are approximate (~). "Wall/opening fit" is the share of each polygon edge (excluding closures) that lies within about 0.1 m of a traced wall, glazing or door cue.

| Room | ~Area m² (derived) | Brochure label | Floor (upstream MATS) | Evidence status | Closures | Wall/opening fit | Note |
|---|---|---|---|---|---|---|---|
| Living / Dining | ~63.62 | 12.40 × 5.10 m | `tile800` | observed (project-wide, not room-specific) | 1 | 1.0 |  |
| Show Kitchen | ~10.55 | 5.70 × 2.70 m | `tile800` | observed (project-wide, not room-specific) | 3 | 1.0 | brochure labels overlap in the open plan (5.10 + 2.70 m > traced depth); derived area is smaller than label 5.70 x 2.70 |
| Pantry | ~4.38 | 1.70 × 2.45 m | `tile800` | observed (project-wide, not room-specific) | 2 | 1.0 |  |
| Powder | ~6.18 | 3.65 × 1.70 m | `terrazzo` | observed (project-wide wet-area spec, decoded text) | 1 | 1.0 |  |
| Kitchen | ~11.98 | 4.00 × 3.00 m | `tile800` | observed (project-wide, not room-specific) | 1 | 1.0 |  |
| Laundry | ~3.72 | 2.20 × 1.80 m | `terrazzo` | observed (project-wide wet-area spec, decoded text) | 1 | 1.0 |  |
| K. Store | ~2.9 | 2.20 × 1.40 m | `tile800` | observed (project-wide, not room-specific) | 1 | 1.0 |  |
| Dress | ~1.94 | 1.90 × 1.10 m | `tile800` | observed (project reference render, not matched to this villa) | 2 | 0.782 |  |
| Maid Room | ~6.14 | UNKNOWN* | `tile800` | observed (project-wide, not room-specific) | 2 | 0.95 | V4 shows UNKNOWN*; brochure crop label reads 2.10 x 3.10 m. East side = thin traced wall x258-261. |
| Maid Bath | ~3.13 | 1.70 × 1.90 m | `terrazzo` | observed (project-wide wet-area spec, decoded text) | 1 | 0.886 | west side = thin traced wall x258-261; includes the narrow fixture strip |
| Double-Height Entry | ~10.68 | 3.29 × 3.30 m | `tile800` | observed (project-wide, not room-specific) | 2 | 0.852 |  |
| Office / Gym | ~15.1 | 4.60 × 3.40 m | `tile800` | observed (project-wide, not room-specific) | 0 | 0.97 |  |
| Bath | ~5.07 | 2.90 × 1.70 m | `terrazzo` | observed (project-wide wet-area spec, decoded text) | 1 | 0.961 |  |
| Multipurpose | ~18.05 | 4.60 × 3.90 m | `tile800` | observed (project-wide, not room-specific) | 1 | 1.0 |  |
| Lift | ~1.67 | 1.50 × 1.70 m | `tile800` | assumed | 1 | 0.69 |  |
| Outdoor Terrace | ~30.63 | not stated | `antislip` | assumed | 1 | 0.926 | courtyard; water feature sits on this floor |

No polygon: swimming-pool (water surface (Water2), not a room floor); terrace (outdoor, no enclosing walls in trace). The unlabelled corridors and stair hall stay on the display floor plate (light tile, no ceiling).

### Floor material evidence

- `tile800`: **observed (project-wide, not room-specific)**. p17 materials board: "Light Beige Marble or Porcelain - General Flooring"; p24 Interior (Summary): "Floors: Porcelain". Mapped to upstream "tile800" (large-format light tile). Rooms: Living / Dining, Show Kitchen, Pantry, Kitchen, K. Store, Maid Room, Double-Height Entry, Office / Gym, Multipurpose.
- `terrazzo`: **observed (project-wide wet-area spec, decoded text)**. p24 Interior (Summary) wet-area line, glyph-shifted in the PDF text layer, decodes to "Wet areas: Terrazzo Porcelain / Porcelain Concrete Look". Mapped to upstream "terrazzo". Rooms: Powder, Laundry, Maid Bath, Bath.
- `tile800`: **observed (project reference render, not matched to this villa)**. p15 dressing render (canonical/references/ref-p15-dressing.png): light beige floor; plus p24 "Floors: Porcelain". Mapped to "tile800". Rooms: Dress.
- `tile800`: **assumed**. No lift-car finish evidence; upstream "tile800" used. Rooms: Lift.
- `antislip`: **assumed**. No outdoor-floor finish evidence in brochure text; upstream "antislip" (300 anti-slip tile) used. Rooms: Outdoor Terrace.

All brochure finish statements are project-wide (p17 materials board, p24 interior summary, p15/p16 reference renders). None names a specific villa room, so every room assignment is an interpretation. The p24 wet-area line is glyph-shifted in the PDF text layer and was decoded.

## Furniture (43 items, all "source plan symbol, size approximate")
Each item read from an approved V4 furniture glyph or V4 fine-detail trace and cross-checked against the brochure crop; type mapped to the nearest upstream Floorplan 3D model. rot: degrees clockwise in plan (upstream Floorplan 3D convention); rot 0 = back/headboard/tank toward plan north (-y). size_px_object_frame = [width along front, depth front-to-back] in crop px; mm = px x 1000/px_per_m.

| # | Upstream model | Item | Size w×d mm | rot° | Status | Evidence |
|---|---|---|---|---|---|---|
| 1 | `chair` | Dining chair 1 | 462×462 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3444 (chair glyph translate(273,239) rotate(0)); 10 chairs drawn around the table in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 2 | `chair` | Dining chair 2 | 462×462 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element #3445 (chair glyph translate(273,284) rotate(180)); 10 chairs drawn around the table in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 3 | `chair` | Dining chair 3 | 462×462 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3446 (chair glyph translate(293,239) rotate(0)); 10 chairs drawn around the table in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 4 | `chair` | Dining chair 4 | 462×462 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element #3447 (chair glyph translate(293,284) rotate(180)); 10 chairs drawn around the table in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 5 | `chair` | Dining chair 5 | 462×462 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3448 (chair glyph translate(314,239) rotate(0)); 10 chairs drawn around the table in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 6 | `chair` | Dining chair 6 | 462×462 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element #3449 (chair glyph translate(314,284) rotate(180)); 10 chairs drawn around the table in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 7 | `chair` | Dining chair 7 | 462×462 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3450 (chair glyph translate(334,239) rotate(0)); 10 chairs drawn around the table in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 8 | `chair` | Dining chair 8 | 462×462 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element #3451 (chair glyph translate(334,284) rotate(180)); 10 chairs drawn around the table in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 9 | `chair` | Dining chair 9 | 462×462 | 270 | source plan symbol, size approximate | approved V4 SVG source_space element #3452 (chair glyph translate(253,261) rotate(-90)); 10 chairs drawn around the table in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 10 | `chair` | Dining chair 10 | 462×462 | 90 | source plan symbol, size approximate | approved V4 SVG source_space element #3453 (chair glyph translate(355,261) rotate(90)); 10 chairs drawn around the table in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 11 | `table` | Dining table | 2949×1101 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3455 rect 83x31 px; table drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 12 | `sofa` | Sectional sofa - long side | 3091×782 | 270 | source plan symbol, size approximate | approved V4 SVG source_space element #3463-3466,3470 (seat + 3 cushions; back side inferred as the outer side of the L, seats facing the coffee table); L-sofa drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 13 | `sofa` | Sectional sofa - short side | 1990×746 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element #3467-3469,3471 (seat + 2 cushions; back on outer (south) side, inferred) |
| 14 | `coffeetable` | Coffee table | 1208×1208 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3472-3473 square 34 px; square table drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 15 | `armchair` | Armchair (north) | 782×782 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3474 chair glyph; chair drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 16 | `sidetable` | Round side table | 568×568 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3475 circle r=8; round table drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 17 | `armchair` | Armchair (south-east) | 1066×1066 | 20 | source plan symbol, size approximate | approved V4 SVG source_space element #3476 chair glyph rotate(20); round item drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 18 | `island` | Kitchen island (cooktop symbol on top, not modelled separately) | 3873×817 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element #3478-3483 island 109x23 px with 4-ring cooktop; island drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 19 | `barstool` | Bar stool 1 | 391×355 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3484 stool glyph; 3 stools drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 20 | `barstool` | Bar stool 2 | 391×355 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3485 stool glyph; 3 stools drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 21 | `barstool` | Bar stool 3 | 391×355 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3486 stool glyph; 3 stools drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 22 | `counter` | Show-kitchen back counter (with sink notch) | 3766×497 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element fine-detail trace (group doors_stairs_glazing_and_fine_detail) white counter with sink notch; counter drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 23 | `counter` | Kitchen counter - north run | 2167×533 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element fine-detail trace U-shaped counter; light counter shape in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 24 | `counter` | Kitchen counter - east run | 1812×533 | 90 | source plan symbol, size approximate | approved V4 SVG source_space element fine-detail trace U-shaped counter |
| 25 | `counter` | Kitchen counter - south run | 2167×462 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element fine-detail trace U-shaped counter |
| 26 | `cabinet` | Pantry / kitchen tall storage run | 5223×320 | 270 | source plan symbol (type interpreted as storage), size approximate | approved V4 SVG source_space element fine-detail trace white strip x206-215; white band drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 27 | `washer` | Washer | 497×497 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element fine-detail trace square; two appliances drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 28 | `dryer` | Dryer | 533×497 | 180 | source plan symbol (washer vs dryer not distinguishable), size approximate | approved V4 SVG source_space element fine-detail trace square; two appliances drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 29 | `wardrobe` | Dress wardrobe | 1101×568 | 90 | source plan symbol, size approximate | approved V4 SVG source_space element fine-detail trace two stacked units on east wall; drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 30 | `bed` | Maid-room bed | 1279×1101 | 180 | source plan symbol; traced length 1.10 m is short for a bed - kept as drawn, size approximate | approved V4 SVG source_space element #3493-3496 bed with pillow strip at south; bed drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 31 | `nightstand` | Maid-room nightstand | 391×497 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element fine-detail trace small unit beside bed |
| 32 | `table` | Office / meeting table | 888×2167 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3488 rect 25x61 px; table drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 33 | `chair` | Office chair 1 | 391×462 | 270 | source plan symbol, size approximate | approved V4 SVG source_space element #3489 chair glyph rotate(-90); 3+1 chairs drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 34 | `chair` | Office chair 2 | 391×462 | 270 | source plan symbol, size approximate | approved V4 SVG source_space element #3490 chair glyph rotate(-90); 3+1 chairs drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 35 | `chair` | Office chair 3 | 391×462 | 270 | source plan symbol, size approximate | approved V4 SVG source_space element #3491 chair glyph rotate(-90); 3+1 chairs drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 36 | `chair` | Office chair 4 | 391×462 | 90 | source plan symbol, size approximate | approved V4 SVG source_space element #3492 chair glyph rotate(90); 3+1 chairs drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 37 | `vanity` | Powder vanity | 1599×355 | 270 | source plan symbol, size approximate | approved V4 SVG source_space element fine-detail trace counter on powder west wall; drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 38 | `toilet` | Powder WC | 400×650 | 180 | source plan symbol; symbol too small to measure, upstream default 400x650 mm used | approved V4 SVG source_space element fine-detail trace WC shape at x281-288,y429-438; WC drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 39 | `toilet` | Bath WC | 400×650 | 180 | source plan symbol; upstream default 400x650 mm used | approved V4 SVG source_space element fine-detail trace WC shape at x471-485,y673-685; drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 40 | `vanity` | Bath vanity | 1030×355 | 180 | source plan symbol, size approximate | approved V4 SVG source_space element fine-detail trace counter on bath south wall; drawn in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 41 | `armchair` | Pool-terrace chair 1 | 462×462 | 340 | source plan symbol, size approximate | approved V4 SVG source_space element #3497 chair glyph rotate(-20); chairs drawn by pool in brochure source crop source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png |
| 42 | `armchair` | Pool-terrace chair 2 | 462×462 | 20 | source plan symbol, size approximate | approved V4 SVG source_space element #3499 chair glyph rotate(20) |
| 43 | `sidetable` | Pool-terrace side table | 604×604 | 0 | source plan symbol, size approximate | approved V4 SVG source_space element #3498 square 17 px |

**Skipped (drawn, but not modelled):**
- 2 cars (garage/driveway): vehicles, not furniture; no upstream model
- rug / console outline beside sofa: faint outline only in brochure crop, not in approved V4; ambiguous
- K. Store small fixture (x298-311,y590-597): too small/ambiguous to classify
- Maid-bath fixtures (incl. small fixture at x262-272): shapes ambiguous at source resolution (~28 px/m); not classified
- Bath east strip (x520-546,y681-686) and office west strip: too thin/ambiguous
- Pool steps/benches, trees, planting: landscape/water graphics, not furniture

Nothing was added that the source does not draw: no rugs, plants, TVs, lamps, beds or wardrobes beyond the symbols listed. The upstream demo-apartment furniture is not used.

## Renders (headless Chrome, SwiftShader WebGL2, offline)

- `verify/v2_01_hero_living_dining_pool.png`: Living / dining toward the pool (eye level 1.6 m) (canvas 1920×1080, fov 60°, walls 3 m)
- `verify/v2_02_hero_living_sofa_pool.png`: Living: sectional sofa, coffee table, dining beyond, pool through glazing (canvas 1920×1080, fov 62°, walls 3 m)
- `verify/v2_03_hero_show_kitchen_island.png`: Show kitchen: island + 3 stools, back counter (canvas 1920×1080, fov 62°, walls 3 m)
- `verify/v2_04_hero_kitchen.png`: Kitchen: U counters (north/east/south runs) and tall storage run (canvas 1920×1080, fov 75°, walls 3 m)
- `verify/v2_05_hero_entry_stair.png`: Double-height entry toward the stair (display-only stair massing) (canvas 1920×1080, fov 66°, walls 3 m)
- `verify/v2_06_hero_maid_room.png`: Maid room: bed + nightstand as drawn (bed length as traced) (canvas 1920×1080, fov 72°, walls 3 m)
- `verify/v2_07_hero_pool_terrace.png`: Pool terrace: Water2 pool, terrace chairs, living glazing (canvas 1920×1080, fov 58°, walls 3 m)
- `verify/v2_08_birdseye_full_walls.png`: Bird's-eye oblique, full-height walls (3.0 m display-only) (canvas 1920×1080, fov 38°, walls 3 m)
- `verify/v2_09_birdseye_cut_walls.png`: Bird's-eye oblique, cut walls (1.2 m) (canvas 1920×1080, fov 38°, walls 1.2 m)
- `verify/v2_20_side_by_side_spike_vs_upstream_demo.png`: spike v2 (left) vs the **untouched upstream demo**, rendered locally the same way (right).
  - `verify/demo_01_living.png`: UPSTREAM DEMO (untouched data) - living, eye level
  - `verify/demo_02_bedroom.png`: UPSTREAM DEMO - master bedroom
  - `verify/demo_03_kitchen.png`: UPSTREAM DEMO - kitchen
  - `verify/demo_08_birdseye_full_walls.png`: UPSTREAM DEMO - bird's-eye, full walls
  - `verify/demo_09_birdseye_cut_walls.png`: UPSTREAM DEMO - bird's-eye, cut walls
- `verify/v2_21_v1_vs_v2.png`: rejected v1 vs v2.
- `verify/*_raw.png`: the same hero renders without caption bars.

## Verification (`verify/verification.json`)
- Offline: 57 requests, non-localhost 0. Console errors: 0.
- Furniture built at runtime: {'state': 43, 'meshes': 43, 'plan': 43}. Rooms at runtime: 17 (incl. display plate).
- 3D top render vs V4 walls (furniture hidden): recall within ±68.5 mm 0.9986, precision 0.8172, components ≥0.95 recall 14/14. Water IoU 0.9881.
- Water mode water2; flat fallback flat; fly-to moved True; joystick walk moved 0.84 m.

## Remaining quality gaps (honest)
- **Generic furniture models.** These are the upstream procedural models (sofa, chair, bed and so on), not the brochure's actual pieces, and their colours are upstream defaults. Only position, rotation and approximate footprint come from the plan.
- **Procedural finishes.** Floors use upstream procedural tile and terrazzo textures. Walls are the upstream flat off-white and are not the brochure's textured paint, Calacatta feature wall or Recon Veneer joinery. All finish evidence is project-wide, not per room.
- **Real-time WebGL quality, not offline renders.** There is no global illumination, real-time-only soft shadows and a basic ceiling. Headless renders use SwiftShader (CPU), so edges are not anti-aliased the way a GPU browser would draw them. On a normal GPU browser the viewer looks somewhat cleaner than these PNGs.
- **Room polygons are derived.** Show kitchen ~10.6 m² is smaller than its label (5.70 × 2.70) because the open-plan labels overlap. Lift ~1.7 m² is smaller than 1.50 × 1.70. Dress, maid bath, entry and lift have wall/opening fit below 0.9 (see table).
- **Maid-room bed** is modelled at the traced 1.28 × 1.10 m, which is short for a bed, because that is how the plan draws it.
- **Stair** is display-only massing. Riser height and rise direction are assumed, and walking does not climb it.
- **Double-height entry** has no void: corridors, stair hall and entry show open sky above the 3.0 m walls instead of a second floor. Pool has no depth or coping. The outdoor ground beyond the plate is plain.
- **Unknown site orientation**, so the sun direction and time are display-only.
- **Not modelled:** cars, rug or console outline, small store, bath and maid-bath fixtures, landscape (see the skipped list).

## Files
- `index.html`: patched upstream viewer (attribution header kept). `data/fp-4b-gf.plan.js` / `.plan.json`: generated data with per-room, per-item and per-opening provenance.
- `adapter/v4_to_floorplan3d.py`: copy of `scripts/v4_to_floorplan3d.py`, locked to `--plan 4B-GF`. Readings input: `source-evidence/floorplan3d-readings/FP-4B-GF.json`.
- `manifest.json`: sources and hashes, display-only defaults, room, furniture and material evidence, output hashes. `verify/`: verification output and renders. `v1/`: superseded first spike.
Regenerate from the archive root: `.venv/bin/python scripts/v4_to_floorplan3d.py && .venv/bin/python scripts/verify_floorplan3d_spike.py && .venv/bin/python scripts/write_floorplan3d_spike_readme.py`

## Attribution (MIT)
- **Floorplan 3D**, https://github.com/wy51ai/floorplan-3d (commit in the manifest). MIT License, Copyright (c) 2026 wuyi. Full text: `LICENSE-floorplan-3d.txt`. Demo apartment data replaced; furniture models, materials and lighting code are upstream.
- **three.js r160**, incl. Water2/Reflector/Refractor and the `examples/textures/water` normal maps. MIT, Copyright © 2010-2023 three.js authors. Full text: `vendor/three/LICENSE`.

**Not survey-verified, not construction-ready, not certified CAD.** All metric values are approximate (±3 %). Heights, finishes, furniture models and light are display-only.
