#!/usr/bin/env bash
# Ashwood Estates 3D — public WIP preview builder + Vercel deploy (Hobby free tier).
# Usage: from any checkout of this repo that has the lane remotes fetched:
#   tools/preview/build_and_deploy.sh
# Requires: git, VERCEL_TOKEN (or an already-linked vercel CLI), npx.
# Does NOT switch branches in shared checkouts; uses git archive / temporary extract.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="${ASHWOOD_PREVIEW_OUT:-/workspace/ashwood-preview/build}"
TEAM_SCOPE="${VERCEL_SCOPE:-colin-loaders-projects}"
PROJECT_NAME="${VERCEL_PROJECT:-ashwood-preview}"
BUILT_AT="$(TZ=Asia/Dubai date '+%Y-%m-%d %H:%M Asia/Dubai')"

need() { command -v "$1" >/dev/null || { echo "missing: $1" >&2; exit 1; }; }
need git; need npx

EXT_REF="${EXT_REF:-origin/lane/exterior}"
GF_REF="${GF_REF:-origin/lane/gf-interior}"
FF_REF="${FF_REF:-origin/lane/first-floor}"

EXT_HASH="$(git -C "$ROOT" rev-parse --short "$EXT_REF")"
GF_HASH="$(git -C "$ROOT" rev-parse --short "$GF_REF")"
FF_HASH="$(git -C "$ROOT" rev-parse --short "$FF_REF")"

echo "Building preview at $OUT"
echo "  exterior $EXT_HASH  gf $GF_HASH  ff $FF_HASH"
echo "  built $BUILT_AT"

rm -rf "$OUT"
mkdir -p "$OUT"/{exterior,gf-interior,first-floor/r5_step2,first-floor/data,gallery,media}

TMP="$(mktemp -d)"
cleanup(){ rm -rf "$TMP"; }
trap cleanup EXIT

# Extract sparse trees via git archive (no checkout switch)
git -C "$ROOT" archive "$EXT_REF" \
  exterior-garden-3d/4b/walk_exterior_wip \
  exterior-garden-3d/4b/model/data \
  exterior-garden-3d/4b/model/vendor/three/build/three.module.js \
  exterior-garden-3d/4b/model/vendor/three/examples/jsm/objects/Water2.js \
  exterior-garden-3d/4b/model/vendor/three/examples/jsm/objects/Reflector.js \
  exterior-garden-3d/4b/model/vendor/three/examples/jsm/objects/Refractor.js \
  exterior-garden-3d/4b/model/vendor/three/examples/jsm/controls/OrbitControls.js \
  exterior-garden-3d/4b/model/vendor/three/examples/textures/water \
  exterior-garden-3d/4b/step7_motion/EXT-4b_STEP7_garden-pool_motion_PROVISIONAL.mp4 \
  exterior-garden-3d/4b/pool_pass/EXT-4b_POOL_water_clip_7s_720p.mp4 \
  | tar -x -C "$TMP"

# Keep only latest side-by-sides (drop older pass PNGs to stay under size caps)
EXT_DEST="$OUT/exterior"
mkdir -p "$EXT_DEST"
cp -a "$TMP/exterior-garden-3d" "$EXT_DEST/"
# Prune bulky camera archives: keep latest SBS only
CAM="$EXT_DEST/exterior-garden-3d/4b/walk_exterior_wip/cameras"
if [ -d "$CAM" ]; then
  find "$CAM" -type f ! -name 'front_pass16_*' ! -name 'front_m25_*' -delete || true
fi
# Gallery copies
G="$EXT_DEST/exterior-garden-3d/4b/walk_exterior_wip"
cp -f "$G/cameras/front_pass16_side_by_side.png" "$OUT/gallery/" 2>/dev/null || true
cp -f "$G/cameras/front_m25_side_by_side.png" "$OUT/gallery/" 2>/dev/null || true
cp -f "$G/views/rear/shots/rear_pass3_side_by_side.png" "$OUT/gallery/" 2>/dev/null || true
cp -f "$G/views/garden/shots/pool_pass3_side_by_side.png" "$OUT/gallery/" 2>/dev/null || true
cp -f "$G/views/garden/shots/garden_back_pass3_side_by_side.png" "$OUT/gallery/" 2>/dev/null || true
cp -f "$EXT_DEST/exterior-garden-3d/4b/step7_motion/"*.mp4 "$OUT/media/" 2>/dev/null || true
cp -f "$EXT_DEST/exterior-garden-3d/4b/pool_pass/"*.mp4 "$OUT/media/" 2>/dev/null || true

# GF
rm -rf "$TMP"/*; mkdir -p "$TMP"
git -C "$ROOT" archive "$GF_REF" \
  active/floorplan3d-spike/FP-4B-GF/index_r3.html \
  active/floorplan3d-spike/FP-4B-GF/f2_entry_travertine.js \
  active/floorplan3d-spike/FP-4B-GF/f3_calacatta_wall.js \
  active/floorplan3d-spike/FP-4B-GF/f3_olive_tree.js \
  active/floorplan3d-spike/FP-4B-GF/f3_water_perf.js \
  active/floorplan3d-spike/FP-4B-GF/q7_courtyard_wire.js \
  active/floorplan3d-spike/FP-4B-GF/courtyard_feature_r2.js \
  active/floorplan3d-spike/FP-4B-GF/data \
  active/floorplan3d-spike/FP-4B-GF/assets \
  active/floorplan3d-spike/FP-4B-GF/vendor/three \
  active/floorplan3d-spike/FP-4B-GF/LICENSE-floorplan-3d.txt \
  | tar -x -C "$TMP"
GF_SRC="$TMP/active/floorplan3d-spike/FP-4B-GF"
cp -a "$GF_SRC/." "$OUT/gf-interior/"
mv -f "$OUT/gf-interior/index_r3.html" "$OUT/gf-interior/index.html"
# Drop verify archives if any slipped in
rm -rf "$OUT/gf-interior/verify" "$OUT/gf-interior/v1" "$OUT/gf-interior/build_r3"

# FF
rm -rf "$TMP"/*; mkdir -p "$TMP"
git -C "$ROOT" archive "$FF_REF" \
  active/floorplan3d-spike/FP-4B-FF/r5_step2/FP-4B-FF_V4_cad_clean.png \
  active/floorplan3d-spike/FP-4B-FF/r5_step2/FP-4B-FF_r5_trace_on_V4.png \
  active/floorplan3d-spike/FP-4B-FF/data/fp-4b-ff.plan.r5.json \
  | tar -x -C "$TMP"
cp -f "$TMP/active/floorplan3d-spike/FP-4B-FF/r5_step2/"*.png "$OUT/first-floor/r5_step2/"
cp -f "$TMP/active/floorplan3d-spike/FP-4B-FF/r5_step2/"*.png "$OUT/gallery/"
cp -f "$TMP/active/floorplan3d-spike/FP-4B-FF/data/fp-4b-ff.plan.r5.json" "$OUT/first-floor/data/"

python3 - <<PY
from pathlib import Path
import re
OUT = Path("$OUT")
banner = '''<div id="ashwood-wip-banner" style="position:fixed;top:0;left:0;right:0;z-index:99999;background:#7a1f1f;color:#fff;padding:8px 12px;font:600 13px/1.35 system-ui,sans-serif;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.35)">Concept visualisation — work in progress — not survey-verified, not construction-ready, not certified CAD.</div>
<style id="ashwood-wip-banner-pad">body{padding-top:40px !important}</style>
'''
for rel in [
  'exterior/exterior-garden-3d/4b/walk_exterior_wip/front_pass.html',
  'exterior/exterior-garden-3d/4b/walk_exterior_wip/rear_pass.html',
  'exterior/exterior-garden-3d/4b/walk_exterior_wip/index.html',
  'gf-interior/index.html',
]:
  p = OUT/rel
  if not p.exists():
    continue
  html = p.read_text(encoding='utf-8', errors='replace')
  if 'ashwood-wip-banner' in html:
    continue
  m = re.search(r'(<body[^>]*>)', html, flags=re.I)
  if m:
    i = m.end(); html = html[:i] + '\\n' + banner + html[i:]
  else:
    html = banner + html
  p.write_text(html, encoding='utf-8')
print('banners injected')
PY

# FF page + index written by companion generator in same dir if present; else emit here
python3 - <<PY
from pathlib import Path
OUT=Path("$OUT"); BUILT_AT="$BUILT_AT"; EXT="$EXT_HASH"; GF="$GF_HASH"; FF="$FF_HASH"
(OUT/'first-floor/index.html').write_text(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Ashwood 4B First Floor — Step 2 Layout (preview)</title>
<style>body{{margin:0;font-family:system-ui,sans-serif;background:#111;color:#eee}}.banner{{background:#7a1f1f;color:#fff;padding:10px 16px;font-weight:600;text-align:center;position:sticky;top:0;z-index:10}}main{{max-width:1200px;margin:0 auto;padding:24px}}img{{max-width:100%;border:1px solid #333}}a{{color:#9cf}}.meta{{color:#aaa}}</style></head><body>
<div class="banner">Concept visualisation — work in progress — not survey-verified, not construction-ready, not certified CAD.</div>
<main><p><a href="../index.html">← Preview index</a></p>
<h1>FP-4B-FF — Step 2 Layout</h1>
<p class="meta">Lane: lane/first-floor · Commit: {FF} · Critic: CRITIC-FAIL 6/10 (step 2) · Built: {BUILT_AT}</p>
<figure><img src="r5_step2/FP-4B-FF_V4_cad_clean.png" alt="V4 FF CAD"/><figcaption>Approved V4 first-floor CAD (clean crop).</figcaption></figure>
<figure><img src="r5_step2/FP-4B-FF_r5_trace_on_V4.png" alt="r5 overlay"/><figcaption>r5 step 2 trace overlay. CRITIC-FAIL pending polygon/door/fixture fixes.</figcaption></figure>
</main></body></html>''', encoding='utf-8')
(OUT/'index.html').write_text(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Ashwood Estates 3D — live preview (WIP)</title>
<style>
:root{{--bg:#0f1115;--card:#1a1f2b;--text:#e8ecf4;--muted:#9aa3b5;--accent:#5b9cff}}
body{{margin:0;font-family:system-ui,sans-serif;background:var(--bg);color:var(--text)}}
.banner{{background:#7a1f1f;color:#fff;padding:12px 16px;font-weight:700;text-align:center;position:sticky;top:0;z-index:20}}
main{{max-width:1100px;margin:0 auto;padding:28px 20px 60px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.card{{background:var(--card);border:1px solid #2a3142;border-radius:12px;padding:16px}}
.badge{{display:inline-block;background:#3a1520;color:#ffb4b4;border:1px solid #6a2a35;border-radius:999px;padding:2px 10px;font-size:.75rem;font-weight:700}}
a.btn{{display:inline-block;margin-top:6px;background:var(--accent);color:#061018;text-decoration:none;font-weight:700;padding:8px 12px;border-radius:8px}}
a.btn.secondary{{background:#2a3142;color:var(--text)}}.sub{{color:var(--muted)}}
.gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}}
.gallery img{{width:100%;height:150px;object-fit:cover}}video{{width:100%;max-width:720px}}
</style></head><body>
<div class="banner">Concept visualisation — work in progress — not survey-verified, not construction-ready, not certified CAD.</div>
<main>
<h1>Ashwood Estates 3D — preview</h1>
<p class="sub">Read-only public preview. Built <strong>{BUILT_AT}</strong>. Every viewer is CRITIC-FAIL (WIP).</p>
<div class="grid">
<div class="card"><h2>Exterior — front</h2><span class="badge">CRITIC-FAIL · 4/10 · step 6</span>
<p class="sub">lane/exterior · {EXT}</p>
<a class="btn" href="exterior/exterior-garden-3d/4b/walk_exterior_wip/front_pass.html">Open front viewer</a></div>
<div class="card"><h2>Exterior — rear / pool</h2><span class="badge">CRITIC-FAIL · pool 2/10 · rear 4/10 · step 6</span>
<p class="sub">lane/exterior · {EXT}</p>
<a class="btn" href="exterior/exterior-garden-3d/4b/walk_exterior_wip/rear_pass.html">Open rear / pool viewer</a></div>
<div class="card"><h2>Ground floor interior</h2><span class="badge">CRITIC-FAIL · 6/10 · step 6</span>
<p class="sub">lane/gf-interior · {GF}</p>
<a class="btn" href="gf-interior/index.html">Open GF viewer</a></div>
<div class="card"><h2>First floor CAD</h2><span class="badge">CRITIC-FAIL · 6/10 · step 2</span>
<p class="sub">lane/first-floor · {FF}</p>
<a class="btn" href="first-floor/index.html">Open FF CAD / overlay</a></div>
</div>
<section><h3>Gallery</h3><div class="gallery">
<a href="gallery/pool_pass3_side_by_side.png"><img src="gallery/pool_pass3_side_by_side.png" alt="pool"/></a>
<a href="gallery/front_pass16_side_by_side.png"><img src="gallery/front_pass16_side_by_side.png" alt="front"/></a>
<a href="gallery/rear_pass3_side_by_side.png"><img src="gallery/rear_pass3_side_by_side.png" alt="rear"/></a>
</div></section>
<section><h3>Provisional motion</h3>
<video controls src="media/EXT-4b_STEP7_garden-pool_motion_PROVISIONAL.mp4"></video></section>
</main></body></html>''', encoding='utf-8')
(OUT/'vercel.json').write_text('{"version":2,"headers":[{"source":"/(.*)","headers":[{"key":"X-Robots-Tag","value":"noindex"},{"key":"Cache-Control","value":"public, max-age=300"}]}]}\\n', encoding='utf-8')
(OUT/'package.json').write_text('{"name":"ashwood-preview","private":true,"version":"0.1.0"}\\n', encoding='utf-8')
print('index written')
PY

echo "Build size: $(du -sh "$OUT" | cut -f1)"
if [ "${SKIP_DEPLOY:-0}" = "1" ]; then
  echo "SKIP_DEPLOY=1 — build only"
  exit 0
fi
: "${VERCEL_TOKEN:?set VERCEL_TOKEN}"
npx --yes vercel deploy --prod --yes --token "$VERCEL_TOKEN" --scope "$TEAM_SCOPE" "$OUT"
