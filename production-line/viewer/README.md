# Lane 4 — Viewer (Optimizer Bot)

Owns only `production-line/viewer/` (and may update `optimizer/` helpers). Never edits builders' files.

## Optimized forks (offline, fast)

| Viewer | Path | Source (untouched) |
|---|---|---|
| GF v2 | `gf/index.html` | `active/floorplan3d-spike/FP-4B-GF/` |
| FF r4 | `ff/index.html` + `ff/data/` | `lane/first-floor` (not on main) |
| **Exterior front (LIVE)** | `exterior-front/index.html` | `lane/exterior` `walk_exterior_wip/front_pass.html` + overrides |
| Exterior walkable_v6 | `exterior/` | **SUPERSEDED** — see `exterior/SUPERSEDED.md` |
| RF | `rf/README.md` | blocked — no viewer yet |

Shared local three.js r160: `vendor/three/` (no CDN).

### Optimizer patches
- `renderer.setPixelRatio` capped at **1.5** desktop / **1** mobile
- `shadowMap.autoUpdate = false` + one bake
- Render-on-demand (rAF stops when idle)
- Offline import maps to shared vendor; exterior MODEL also shipped as `data/model.min.js`

## Commands
```bash
bash production-line/viewer/check.sh
```

Evidence: `baseline/before.json`, `baseline/after.json`, `baseline/front_pass_*.json`.
