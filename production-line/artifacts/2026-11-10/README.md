# Published artifact builds, 2026-11-10

Single-file, self-contained pages: three.js, model data and textures are inlined, so they make no external requests. These are the exact pages published to Colin's artifact links. Each one was checked in headless Chromium: no console errors, no failed requests.

| File | Artifact |
|---|---|
| `exterior.html` | https://claude.ai/artifact/3dty5cFKAgW29MkQVLpAtJ (tabs: front v2, left, right, site + pool v3, rear WIP, side-by-sides) |
| `ground-floor_r3.html` | https://claude.ai/artifact/ABhzr2yy6MKMWfQXY3tB2v |
| `first-floor_r6F.html` | https://claude.ai/artifact/MAPDK4oRWv1EJJ1dMPfiHo (WIP banner) |
| `progress.html` | https://claude.ai/artifact/XZnAbwEKiLHGLLaWnqBq1C |
| `pictures.html` | https://claude.ai/artifact/77CUbtNzDqqUYUW75GFiuq |

Build tools: `bundle.mjs` (esbuild; run `node bundle.mjs <repoRoot> <relHtml> x <out.html> [dropSubstring...]`; set `PATCH=ext_patch.json` for exterior views to swap walk mode for orbit) and `hub.py` (exterior tab page). Sources stay in their lane folders; these files are snapshots. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
