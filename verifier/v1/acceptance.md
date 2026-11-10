# Ashwood visual-quality acceptance — v1

Created 2026-11-10 (Asia/Dubai). Scope: Colin's requested first-floor, exterior, pool and rear-quality pass. All outputs remain concept visualisation, not survey-verified, not construction-ready, not certified CAD.

## Release gate

The integrated branch is ready for Colin's review only when every applicable check below passes. “Seven-star” is treated as a visual-quality target, not a claim of certification or a guarantee of perfection on untested hardware. No known critical/major defect may remain open.

### A. Source and geometry integrity
- `ACTIVE_PIPELINE.json`, approved V4 artwork, and retired inputs are unchanged.
- FF uses the approved `FP-4B-FF_V4_portrait.svg` lineage and documents 35.53012869683798 mm/u as an ASSUMPTION.
- FF r8 preserves the source-aligned r6 evidence: 417 wall rectangles, 14 explicit room polygons, 12 doors, 10 windows, 41 furniture records, one stair and three voids. Any intentional deviation is individually logged.
- No GF-only ceiling outline, furniture placement or feature-wall coordinates remain active in FF.
- M30 enlarged rear garden (`z -9.0`) and M44 pool/terrace/seating geometry are preserved. Rear changes, if any, affect only the element implicated by locked-view evidence and are logged as image-derived or CAD-derived.

### B. First-floor presentation
- The active FF viewer loads the r8 data, not r6F or an older fallback.
- Full-height 3D walls, real door/window openings, correctly positioned source-aligned furniture, stair and all three voids are visible in their intended views.
- Eye-level and isometric captures show no blank canvas, black voids, obvious wall/floor gaps, furniture outside its assigned room, severe z-fighting, unreadable room framing or GF-specific decor.
- Room materials and decor not established by evidence are labelled as display assumptions.

### C. Exterior, pool and interaction
- Front, left, right, site/pool and rear source views use the same active water implementation and coherent lighting/material treatment.
- Water2 is genuinely visible over modelled basins: hide/show and two-time-pixel probes must both show non-zero differences in a pool crop. A material existing in code is not a pass.
- Water settings are active in source (target starting point: reflectivity 0.32, scale 1.1, flowSpeed 0.035; subsequent evidence-backed tuning is allowed and must be logged).
- Drag changes the camera orientation and wheel/pinch changes camera distance in locked hub views. Instructions match actual behaviour.
- Deterministic capture support renders one requested frame without continuous animation in capture mode.
- All five locked exterior angles are inspected at full size and thumbnail size; at least two local crops cover architecture and pool/landscape detail. No clipped villa, visible ground edge, floating vegetation, missing balcony, opaque/flat pool or obvious rear projection defect remains unresolved.

### D. Runtime and reproducibility
- Zero uncaught browser errors and zero failed asset requests on the tested GF, FF and exterior pages.
- No runtime CDN/external asset dependency; Three.js and Water2 remain vendored.
- No bare unseeded `Math.random()` is introduced.
- Capture reports include renderer info (draw calls/triangles), viewport, camera/view identifier and source commit/change-set identifier.
- Before/after captures use identical cameras and viewport sizes.

### E. Independent review and delivery
- At least one documented build → capture → inspect → fix → recapture round occurs for FF and exterior.
- An independent critic, not either builder, reviews the final before/after evidence. Critical/major findings are fixed and re-reviewed; minor limitations are explicitly disclosed.
- Root `CHANGELOG.md` records every integrated change set; `STATUS.md` records final lane/step status and remaining limits.
- All changes are committed and pushed to `colin/viewer-quality-2026-11-10`; no `main` merge and no deployment.
