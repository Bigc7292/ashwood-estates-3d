# 4B first floor: 7-step log (interior rule set)

Status is per step. Nothing here is marked DONE until the critic and Colin pass the gate.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

## Step 1: Reference
- Inputs: brochure interior pages p15, p16, p17 (material boards and interior renders), p24 (summary: porcelain floors). Source: original/ashwood-residences_brochure.pdf.
- Outputs: ref_brochure_p15.png, ref_brochure_p16.png in this folder (40 dpi renders). p17 rendered, not copied.
- Review check: references show walk-in wardrobe, living space with chandelier, bedroom with bed, nightstands, armchair and rug, plus material boards (Recon veneer joinery, calacatta or porcelain feature, travertine feature).
- Status: DONE pending critic. Gate not passed.

## Step 2: Layout
- Inputs: approved V4 FF plan (active/approved-cad-v4/svg/FP-4B-FF_V4_portrait.svg, approval pt16u); room labels and stated dimensions from the SVG; canonical room records (canonical/villas/4b/floors/ff/index.json).
- Outputs so far: wall outlines (r4 walls, raster-derived); room labels with stated dimensions (MASTER SUITE 4.00 x 5.10 m, FAMILY LIVING 4.00 x 5.10 m, and the rest).
- Blocker: room polygons not yet separated. Flood fill and watershed from label seeds leak through open doorways. Doorway gaps must be found and closed first.
- Status: WIP, blocked on doorway closures.

### Step 2 review of the step-2 lane's r6/r7 output (unverified input, checked by me)
- Took as candidate inputs (not yet applied to my builds): 14 room polygons (rooms_u.json), 22 openings (openings_u.json), 44 furniture footprints (furniture_u.json), 4 closures (closures_u.json). Source: r7_step2/ and r6_step2/ in this folder, from the step-2 lane.
- Checked: room count is 14 and matches the source labels. Polygon areas compared with the stated room dimensions from the approved FF SVG labels, converting SVG units to m² at 35.53 mm per crop px (1 SVG unit = 1.147 crop px, so 30.98 mm per SVG unit).
- Failed check: every polygon comes out about 17% smaller in area than its stated dimensions (for example Master Suite 16.4 m² against 4.00 x 5.10 m = 20.4 m²; Junior Suite 15.2 m² against 18.4 m²). The error is consistent across rooms, which points to a unit or scale conversion in the step-2 builder, not to room shape. Not applied. Needs the fixer's verified factor before use.
- Not taken yet: furniture and openings. They depend on the polygon scale being fixed first.

### Scale check (loop 2, settled by me, not by the fixer)
- The r6/r7 builder does not use 35.53. Its MM_PER_U = 13100 / 385 = 34.03 mm per SVG unit, taken from the drawn "ENVELOPE ~ 13.1 m" dimension line (385 u wide). So the 17 to 20% area shortfall comes from r6/r7 using 34.03, not 35.53.
- Envelope at 35.53 mm per crop px (my raster outer walls, 379 x 646 px): width 13.47 m against the drawn 13.1 m (+2.8%, inside the 3% working allowance); height 22.95 m against 23.9 m (-4.0%, just outside it). Verdict: holds to within about 3 to 4%. Built at 35.53 as the GF calibration says, and the height gap is logged, not fixed.
- Per-room check at 35.53, polygon bounding box over stated size (width, depth): Master Suite 1.02, 1.04; Family Living 1.05, 1.05; Bedroom 1 1.03, 1.15; M. Dressing 1.04, 1.04; M. Bath 1.04, 1.04; Corridor 1.07, 1.02; Lift 1.03, 1.01; Bath 1 1.02, 1.04; Bath 2 1.04, 1.03; Dress 0.99, 1.11; Bedroom 2 1.02, 1.12; J. Dress 1.05, 1.00; J. Bath 1.01, 1.03; Junior Suite 1.03, 1.05.
- ASSUMPTION (Colin may overrule): at 35.53 the polygons are 1 to 5% larger than stated room sizes in most rooms (Bedroom 1 and Bedroom 2 depth about 12% over). The likely cause is that stated sizes are clear sizes inside finished faces, and the polygons are traced to wall centrelines or include wall thickness. Using 34.03 instead would make rooms about 10% under. 35.53 is kept.
- Status: scale settled at 35.53 as an ASSUMPTION. Steps 3 to 7 can proceed on this basis.

## Step 3: Blockout
- Not started (needs step 2 room polygons).

## Step 4: Clean-build finish
- Not started.

## Step 5: Printed matter
- Not started. No signage in the FF source; labels are room names only.

## Step 6: Critique
- Not started.

## Step 7: Motion
- Not started.

## Loop
- Pass 1: steps 1 to 2 in progress. Steps 3 to 7 pending.
- Loop 2 (step 2): labels corrected (r5L). Step-2 lane r6/r7 reviewed above, scale check failed, not applied.

## Loop 3 (step 2): doorway closures and room separation, result
- Applied the four step-2 closures as ASSUMED wall closures (C1 to C4, 4 crop px thick, crop px frame; C2 and C3 coincide with the traced lightwell and open-to-below outlines). Script and output: r6L_step2/sep.py, r6L_step2/diag_components.png.
- Result: FAIL. The r5L wall raster is not closed. Flood fill from the label seeds gives one component covering almost the whole plate, so rooms do not separate. The outer shell has gaps (top-left and top edge), and many interior partitions are thin or broken. Four closures are not enough.
- Also: 5 of 14 label seeds fall on wall pixels, so seeds need snapping to the nearest free pixel.
- Next: re-trace the r5L wall raster with a closed outer shell and full partition coverage, then re-run the separation. Not marked done. Step 2 stays WIP.

## Furniture pass (requested by Colin: the first floor showed no furniture)
- Source: approved V4 FP-4B-FF raster symbols (embedded plan, 650 x 1000 crop px). The SVG has no furniture vectors; the "Existing furniture" legend swatch is not drawn in the plan.
- Built: r6F_furniture/build_r6F.py -> data/fp-4b-ff.plan.r6F.js/.json, standalone_r6F.html. 36 items, listed in r6F_furniture/furniture_r6F.json with status per item.
- Positions: PLAN (drawn symbol location, read from the approved plan at 35.53 mm/px).
- Types: most are ASSUMED (symbol shape read by eye: wardrobe, dresser, nightstand, vanity). Sizes are derived from the symbol extent, so beds (about 3.1 m long) may be oversized because the symbol includes headboard and pillows. Not verified.
- Not done: the wall re-trace (step 2, still FAIL), the 3D view check, and the critic review. Viewer checked in 2D only (no page errors).
- Status: WIP, not critic-reviewed.

## Furniture r6F, loop 2 (2026-11-10)
- Beds set to the GF catalogue double bed, 1800 x 2000 mm (ASSUMED size). Previous symbol-extent sizes (about 3.1 m) were oversized.
- 3D view checked headless: renders, no page errors, 36 items visible (beds, sofa, wardrobes, bathtub, vanities, WCs). Walls still the r5L trace with stray partition pieces; step 2 wall re-trace not done.
- Status: WIP. Critic review not run. Steps 3 to 7 not done.
