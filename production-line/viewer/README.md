# Lane 4 — Viewer (Optimizer Bot)

Owns only `production-line/viewer/` (and may update `optimizer/` helpers). Never edits builders' files.

## Optimized forks (offline, fast)

| Viewer | Path | Source (untouched) |
|---|---|---|
| GF v2 | `gf/index.html` | `active/floorplan3d-spike/FP-4B-GF/` |
| FF r4 | `ff/index.html` + `ff/data/fp-4b-ff.plan.r4.js` | `lane/first-floor` plan **r4** (filename is the revision; not r1) |
| **Exterior front (LIVE)** | `exterior-front/index.html` | `lane/exterior` `walk_exterior_wip/front_pass.html` + overrides |
| Exterior walkable_v6 | `exterior/` | **SUPERSEDED** — see `exterior/SUPERSEDED.md` |
| RF | `rf/README.md` | blocked — no viewer yet |

Shared local three.js r160: `vendor/three/` (no CDN).

### Optimizer behaviour
- Pixel ratio capped at **1.5** desktop / **1** mobile (intentional sharpness trade-off vs source PR≤2 on GF/FF; exterior source was 1).
- `shadowMap.autoUpdate=false` with **re-bake** (`needsUpdate=true`) on sun/light, door swing, and furniture moves.
- Demand-render when the scene is truly static; **continuous (≈30 fps throttle)** while water is present; keep looping while orbit damping returns true / doors animate / walk mode.
- Offline import maps to shared vendor; exterior MODEL also as `data/model.min.js`.

## Commands
```bash
bash production-line/viewer/check.sh          # includes sun/door/water regression
node production-line/viewer/bench.mjs         # like-for-like median bench → baseline/bench.json
LANE4_SKIP_REGRESSION=1 bash production-line/viewer/check.sh   # sizes/CDN only
```

Evidence: `baseline/bench.json` (authoritative). `before.json` / `after.json` point at it.
