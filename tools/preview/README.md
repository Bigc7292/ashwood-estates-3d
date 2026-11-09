# Ashwood public WIP preview

Read-only static preview of the current Ashwood Estates 3D production-line work, published on Vercel Hobby.

## Live URL

**https://ashwood-preview.vercel.app**

(Stable production alias for project `ashwood-preview` on team `colin-loaders-projects`. Deployment Protection / SSO / password are off.)

## What is included

| Path | Source lane | Critic (as of first publish) |
|---|---|---|
| `/exterior/.../front_pass.html` | `lane/exterior` | CRITIC-FAIL 4/10 step 6 |
| `/exterior/.../rear_pass.html` | `lane/exterior` | CRITIC-FAIL (pool 2/10, rear 4/10) step 6 |
| `/gf-interior/` | `lane/gf-interior` | CRITIC-FAIL 6/10 step 6 |
| `/first-floor/` | `lane/first-floor` | CRITIC-FAIL 6/10 step 2 |
| `/gallery/*.png` | latest side-by-sides + FF overlay | — |
| `/media/*.mp4` | provisional step 7 + pool clip | step 7 not critic-passed |

Every page carries the banner: *Concept visualisation — work in progress — not survey-verified, not construction-ready, not certified CAD.*

## Rebuild / redeploy

```bash
# from a fetch of the lane remotes (do not switch shared checkouts)
export VERCEL_TOKEN=...
tools/preview/build_and_deploy.sh
```

Optional: `ASHWOOD_PREVIEW_OUT`, `VERCEL_SCOPE`, `VERCEL_PROJECT`, `SKIP_DEPLOY=1`, `EXT_REF` / `GF_REF` / `FF_REF`.

## Excluded

`.venv`, source PDFs/brochures, full `approved-cad-v4`, Blender blends/raw render trees, `verify/` archives, files over ~50 MB, and anything not needed to run the viewers. `main` and lane branches are not modified by this script (script lives on `lane/preview` only).

## Labels

Concept visualisation only. Not survey-verified, not construction-ready, not certified CAD.
