# Lane 4 — Viewer (Optimizer Bot)

Owns only `production-line/viewer/` (and may update `optimizer/` helpers). Never edits builders' `active/floorplan3d-spike/*/index.html` or exterior builder files.

## Optimized forks (offline, fast)

| Viewer | Path | Source (untouched) |
|---|---|---|
| GF v2 | `gf/index.html` | `active/floorplan3d-spike/FP-4B-GF/` |
| FF r4 | `ff/index.html` + `ff/data/` (copied from `lane/first-floor`) | not on `main` yet |
| Walkable exterior | `exterior/index.html` + `model.js` | MODEL from `walkable_v6.html` |
| RF | `rf/README.md` | blocked — no viewer yet |

Shared local three.js r160: `vendor/three/` (no CDN).

### Optimizer patches applied
- `renderer.setPixelRatio` capped at **1.5** desktop / **1** mobile
- `shadowMap.autoUpdate = false` + one bake (`needsUpdate` once)
- Render-on-demand (rAF stops when idle; orbit/pointer/keys re-request)
- Offline import maps to shared vendor

## Commands
```bash
bash production-line/viewer/check.sh
# optional headless metrics (needs Playwright browsers):
# node /tmp/... or python production-line/viewer/measure.py
```

Evidence: `baseline/before.json`, `baseline/after.json`.
