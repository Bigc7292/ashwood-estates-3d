# Limitations (candid)

1. **Provenance:** Chat attachment verified byte-identical to processed original (SHA256 `a716d74af71a117145a12e058876220a185b6424bf06c082aded539fbb76ca1b`). Earlier interim caveat withdrawn (2026-11-09 05:30:00 Asia/Dubai (UTC+4)).
2. **Drawing type:** Floorplans are marketing illustrated plans (furniture, landscaping, soft fills), not construction CAD. CAD-style outputs are **source-crop + contrast rasters**, not DXF/DWG and not survey-certified.
3. **Clips:** Dual-plan pages use geometric left/right splits of the plan panel; embedded-image bboxes from the PDF were unreliable (off-page).
4. **Text layer:** Mojibake on many pages; room labels taken from text where readable and cross-checked visually. Some dimensions in auto image-captions may be wrong — prefer brochure text/sidebar and flag conflicts (e.g. 567.12 vs 564.73 Sq.m for 4-bed).
5. **Scale:** No clear scale bar; do not infer scale beyond labeled room dimensions.
6. **Coverage:** Only Ground / First / Roof disclosed per villa type. No basement, no clubhouse plans, no unit-level variants.
7. **Style refs:** None supplied.
8. **ZIP:** Excludes `.venv`, embedded `pdfimages` dump, and full `page110-*` set (72dpi pages + plan crops retained) to limit size; full 110dpi pages remain on disk under `extracts/pages/`.
