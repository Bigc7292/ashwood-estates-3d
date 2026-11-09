# QA register: real-world scenario tests

One section per test. Columns: id, stage, severity (HIGH / MED / LOW), what happened (with evidence), fix, verified (how, when).
Each test closes with an optimisation pass aimed at the defect classes it found.

## Test 1: Ashwood Estates (brochure PDF 38 pp + https://www.eva.realestate/projects/ashwood-estates)
Status: not started (planning). Pre-build findings, from Claude reading the inputs on 2026-11-08:

| id | stage | severity | finding | planned handling |
|---|---|---|---|---|
| T1-P1 | facts | MED | The 4-bed ground floor area reads 263.01 m² in the p.27 panel but 266.2 m² in the p.27 text layer | Keep both and flag. Use the panel value (matches the p.24 total) for the area check |
| T1-P2 | facts | LOW | Drive times differ: Palm Jumeirah is 30 min (brochure p.5) vs 25 min (website) | Show both, with sources |
| T1-P3 | ingest | MED | Pp.1 and 3 are paper textures at 1920×1080, which look like renders by size | Classifier: reject low-detail images; don't count them for R3 |
| T1-P4 | ingest | LOW | Some headings use a decorative font whose text layer comes out garbled (e.g. p.9) | Ignore runs of non-Latin glyphs; the AI pass may read the page image instead |
| T1-P5 | URL | MED | Website images and plans are AVIF; the "Download All Floor Plans" button links to "#" | Convert AVIF server-side; take the plan images from the page instead |
| T1-P6 | facts | LOW | The developer (Wasl) is named on the website, not in the brochure | The URL fills R4; source shown as website |
