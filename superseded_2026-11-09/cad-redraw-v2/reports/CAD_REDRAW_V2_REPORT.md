# CAD redraw v2 report

Generated: 2026-11-09 05:38:28 Asia/Dubai (UTC+4)

## Blocker (PDF vectors)
Poppler/PyMuPDF drawings on plan pages are sidebar/UI fills (~40–57 fills, few strokes). **Wall geometry is not in PDF vectors.** Plans exist as embedded raster boards (NAGA ARCHITECTS marketing floor-plan sheets).

## Method used (honest)
1. Extract embedded 3-up boards (4BR xref313/439, 5BR xref384, 6BR xref598).
2. Crop Ground / First / Roof panels; trim header/footer/branding colors.
3. **SVG:** OpenCV contour trace of dark wall poché from those rasters (geometry-preserving; may include some dark furniture blobs — uncertain).
4. **PNG presentation:** colored board panel retained (already matches requested muted green/blue CAD presentation style) on white surround; not B&W contrast crop.
5. Long-edge 7680 via Lanczos when native smaller — **no new detail invented**.
6. Overlay compare each panel vs brochure page plan clip (framing differs → residual |diff| expected).

## Style reference
Requested path `8d2454fb…png` was **not on disk** at run time. Applied style from user written brief + source boards' own presentation language. When style file arrives, treat as style-only.

## Assets
9 floors processed into `cad-redraw-v2/svg|png|overlays`.

## Not claimed
- Not native DXF/DWG CAD
- Not survey-certified
- Not generative AI redraw
- Dimension chains / north / scale bars only if present on source board (board states 1:100 on title — retained only as text on board pixels if visible; not independently verified against site survey)
