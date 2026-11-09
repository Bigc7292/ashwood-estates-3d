# Exterior step 5 (printed matter) inventory, 4-bed (4B)

Status: REVIEW-PENDING. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
Checked 2026-11-09 by Lane 2 (Q1). Method: each image opened and viewed at full frame; no Blender render; no file edited.

## Result

**No in-scene signage, plaques, house numbers or lettering in any of the 10 approved generated 4B images.**
The only printed text in those images is the burned-in provenance caption (see section B), which is a review label added to the file, not part of the scene.

The two brochure renders (p25, p26) carry brochure overlay text (title and logo) that sits on top of the render, not on the building. No house number, plaque or sign is in the scene.

## A. Scene printed matter

| Image (file) | Location in image | Text | Result |
|---|---|---|---|
| All 10 generated images | - | none | none in source |
| `MARKETING_RENDER_p25.png` (1920x1080) | Top-left, over sky | "4 BEDROOM VILLA" (brochure title) | Brochure overlay, not scene |
| `MARKETING_RENDER_p25.png` | Top-right, over sky | Circular swirl logo mark (no legible text) | Brochure overlay, not scene |
| `MARKETING_RENDER_p25.png` | Car bumpers / golf cart | No legible plates or lettering at this resolution | none legible |
| `MARKETING_RENDER_p26.png` (1920x1080) | Top-left, over sky | "4 BEDROOM VILLA" (brochure title) | Brochure overlay, not scene |
| `MARKETING_RENDER_p26.png` | Top-right, over sky | Circular swirl logo mark (no legible text) | Brochure overlay, not scene |

Note: `source-refs/REF-4b-p25-front-render-crop_no-title-logo.png` and `REF-4b-p26-rear-render-crop_no-title-logo.png` are the crops with the title and logo removed. They are the versions to use as references for appearance.

## B. Burned-in provenance caption on the 10 generated images

Every approved generated image carries the same bottom-right caption, two lines:

- Line 1: "AI-generated concept visualisation, not survey-verified"
- Line 2: "EXT-4b-<VIEW-ID> | Ashwood 4B | needs review"

| File | Caption line 2 |
|---|---|
| EXT-4b-ELEV-FRONT_GENERATED-SOURCE-CONDITIONED.png | EXT-4b-ELEV-FRONT |
| EXT-4b-ELEV-REAR_GENERATED-SOURCE-CONDITIONED.png | EXT-4b-ELEV-REAR |
| EXT-4b-ELEV-LEFT_GENERATED-CONCEPT.png | EXT-4b-ELEV-LEFT |
| EXT-4b-ELEV-RIGHT_GENERATED-CONCEPT.png | EXT-4b-ELEV-RIGHT |
| EXT-4b-GARDEN-FRONT_GENERATED-SOURCE-CONDITIONED.png | EXT-4b-GARDEN-FRONT |
| EXT-4b-GARDEN-BACK_GENERATED-SOURCE-CONDITIONED.png | EXT-4b-GARDEN-BACK |
| EXT-4b-OUTDOOR-SITE_GENERATED-SOURCE-CONDITIONED.png | EXT-4b-OUTDOOR-SITE |
| EXT-4b-OUTDOOR-ROOF-TERRACE_GENERATED-CONCEPT.png | EXT-4b-OUTDOOR-ROOF-TERRACE |
| EXT-4b-OUTDOOR-COURTYARD_GENERATED-CONCEPT.png | EXT-4b-OUTDOOR-COURTYARD |
| EXT-4b-POOL_GENERATED-SOURCE-CONDITIONED.png | EXT-4b-POOL |

Decision for step 5: keep the caption on review copies. Before any presentation copy is made, Colin decides whether the caption stays. The caption is not scene signage and must not be read as one.

## Images checked (list)

Folder: `generated-exteriors/ashwood-estates/4b/`, labelled deliverables only (manifest `generated_visuals_manifest.json`, 10 assets). SHA-256 of all 10 files matches the manifest.

1. EXT-4b-ELEV-FRONT_GENERATED-SOURCE-CONDITIONED.png
2. EXT-4b-ELEV-REAR_GENERATED-SOURCE-CONDITIONED.png
3. EXT-4b-ELEV-LEFT_GENERATED-CONCEPT.png
4. EXT-4b-ELEV-RIGHT_GENERATED-CONCEPT.png
5. EXT-4b-GARDEN-FRONT_GENERATED-SOURCE-CONDITIONED.png
6. EXT-4b-GARDEN-BACK_GENERATED-SOURCE-CONDITIONED.png
7. EXT-4b-OUTDOOR-SITE_GENERATED-SOURCE-CONDITIONED.png
8. EXT-4b-OUTDOOR-ROOF-TERRACE_GENERATED-CONCEPT.png
9. EXT-4b-OUTDOOR-COURTYARD_GENERATED-CONCEPT.png
10. EXT-4b-POOL_GENERATED-SOURCE-CONDITIONED.png

Brochure renders: `exterior-garden-3d/4b/step1_reference/brochure_renders/MARKETING_RENDER_p25.png`, `MARKETING_RENDER_p26.png`.

Not checked (out of scope for Q1): `_raw_unlabelled/`, `_rejected_first_pass/` (excluded by rule); brochure p29, p30, p33, p34 backups; `EXT_4b_CONTACT-SHEET.png` (a contact sheet, not a deliverable view).

## Source
- Manifest: `generated-exteriors/ashwood-estates/4b/generated_visuals_manifest.json` (counts: generated_available 10, source_verified_views 0).
- Brochure: `exterior-garden-3d/4b/step1_reference/brochure_renders/`.
