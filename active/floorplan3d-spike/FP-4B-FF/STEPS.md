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
