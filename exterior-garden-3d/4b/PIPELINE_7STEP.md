# Ashwood 4B exterior: Colin's 7-step pipeline (fixed)

Concept visualisation: not survey-verified, not construction-ready, not certified.

**Guide rule:** EXTERIOR work is guided by IMAGES: the 10 approved generated 4B images (`generated-views/4b/`, labelled deliverables only, never `_raw_unlabelled` or `_rejected_first_pass`) plus brochure renders p25/p26 (backups p29/30, p33/34). The approved CAD V4 plan is used only to check sizes and plan positions. Where images and CAD disagree, the mismatch is logged, and the image is used for appearance and the CAD for footprint dimensions (`mismatches/mismatch_log.md`).

**Goal:** improve external model quality. **Run order:** one step at a time with a gate/review after each. **Current hold:** STOP after step 4, report, and wait for the go-ahead before step 5.

Tooling: headless Blender 4.2.3 LTS (local, free, GPL), Cycles CPU, procedural shaders only, Python/PIL for captions. No paid tools, no network, nothing sent or pushed, no Stage 1 / pipeline files touched.

---

## Step 1: Reference
A 2D image of the finished scene: the 10 approved generated 4B images plus p25/p26.
- **Inputs:** `generated-views/4b/generated_visuals_manifest.json` + the 10 labelled PNGs; brochure p25/p26 (p29/30, p33/34 backup); CAD V4 GF/FF/RF previews (size check only).
- **Outputs:** `step1_reference/generated_approved/` (10, sha256 = manifest), `brochure_renders/`, `cad_v4_check/`, `reference_index.json`, `REFERENCE_BOARD.png`.
- **Review check:** all 10 hashes match the manifest; no raw/rejected images used; each model view is mapped to one reference (`blender/views_blender.json` "ref").
- **Status:** DONE, gate passed.

## Step 2: Layout
Read the layout from the image and build it in Blender (MCP or headless), with CAD checking dimensions. Free and local only.
- **Inputs:** step 1 refs; CAD V4 GF site diagram (28.145 px/m calibration).
- **Outputs:** `blender/4b_layout.blend` (+ `_register.json`), `step2_layout/layout.json`, `layout_top_render.png`, `STEP2_layout_check.png` (CAD | layout | overlay | OUTDOOR-SITE image).
- **Review check:** zones (plot, building, pool, terrace/deck, courtyard, lawn strips, carport, gates, RF terrace/core, off-plot context) fall on the CAD footprint in the overlay.
- **Status:** DONE, gate passed (overlay aligned).

## Step 3: Blockout
Boxes first, then the space, the models and the materials, in that order. Proportions must be fixed while everything is still boxes.
- **Inputs:** layout; image-read heights (no CAD sections); CAD footprint dims.
- **Outputs:** cumulative blends `blender/4b_boxes|space|models|materials.blend`; gate snapshots `step3_blockout/gates/<substage>/`; `step3_blockout/PROPORTION_CHECK.md`; full 19-view set `step3_blockout/renders/` (captioned) + `step3_blockout/comparisons/compare_*.png` (vs matching generated image).
- **Review check:** boxes stage matches CAD (site, GF, FF, pool, courtyard) and the image storey ratio before any detail; each sub-stage adds no massing change; side-by-sides read like the generated images in massing, materials and planting.
- **Status:** DONE, awaiting Colin's review.

## Step 4: Grime
All procedural, covering chipped paint, dust, drip marks, fingerprints, base dirt, and weathering on stone, render and metal.
- **Inputs:** step 3 materials blend.
- **Outputs:** `blender/4b_grime.blend`; `step4_grime/renders/` (19 captioned), `step4_grime/comparisons/compare_*.png`, `step4_grime/closeups/`.
- **Review check:** grime present but subtle (no textures/images): base dirt <0.75 m, drips under slab edges, dust on up-faces, edge chips, bronze patina, stone weathering, glass fingerprints at hand height. Still reads like the generated images.
- **Status:** DONE, awaiting Colin's review. **HOLD: waiting for the go-ahead to start step 5.**

## Step 5: Printed matter
Signs, plaques, house numbers and any labels, made as prints first, then faded and peeled. Only include items visible in the source images; if there are none, record "none in source" and skip.
- **Inputs (planned):** step 4 blend; the 10 images + p25/p26 checked for visible signage.
- **Outputs (planned):** prints, or a "none in source" record.
- **Review check (planned):** every printed item traces to a visible source item.
- **Status:** NOT STARTED, waiting for the go-ahead.

## Step 6: Critique
Self-check close-ups of every surface and junction against the reference images, list "looks unnatural" issues and fix them. Colin then reviews.
- **Status:** NOT STARTED.

## Step 7: Motion
Render to video, e.g. pool water ripple, tree/palm sway, a sun or light change, and a slow camera push-in, all free and local.
- **Status:** NOT STARTED.
