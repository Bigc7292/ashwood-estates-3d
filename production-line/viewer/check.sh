#!/usr/bin/env bash
# Lane 4 one-command viewer check: size budgets, offline refs, basic validator.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
FAIL=0
note(){ printf '%s\n' "$*"; }
fail(){ printf 'FAIL: %s\n' "$*"; FAIL=1; }
pass(){ printf 'PASS: %s\n' "$*"; }

MAX_HTML=400000          # modular viewers should stay well under embedded 1.7MB
MAX_EMBED=1900000        # legacy walkable_v6 allowance (source, not lane4)
MAX_FILE=95000000        # hard GitHub-safe cap for anything we add

note "== lane4 viewer check =="

# 1) required files
for f in \
  production-line/viewer/gf/index.html \
  production-line/viewer/ff/index.html \
  production-line/viewer/exterior/index.html \
  production-line/viewer/exterior/model.js \
  production-line/viewer/vendor/three/build/three.module.js \
  production-line/viewer/check.sh
do
  [[ -f "$f" ]] && pass "exists $f" || fail "missing $f"
done

# 2) size budgets for lane4 outputs
sz(){ wc -c < "$1" | tr -d ' '; }
for f in production-line/viewer/gf/index.html production-line/viewer/ff/index.html production-line/viewer/exterior/index.html; do
  s=$(sz "$f")
  if (( s > MAX_HTML )); then fail "$f is ${s}B > ${MAX_HTML}B"; else pass "$f size ${s}B"; fi
done
s=$(sz production-line/viewer/exterior/model.js)
if (( s > 500000 )); then fail "model.js ${s}B too large"; else pass "model.js ${s}B"; fi

# 3) no file we own over 95MB
while IFS= read -r -d '' f; do
  s=$(sz "$f")
  if (( s > MAX_FILE )); then fail "oversize $f (${s}B)"; fi
done < <(find production-line/viewer -type f -print0)
pass "no lane4 file over 95MB"

# 4) offline: no CDN in lane4 HTML
if rg -n "cdn\.jsdelivr|unpkg\.com|cdnjs\.cloudflare|ajax\.googleapis|esm\.sh" production-line/viewer --glob '*.html' ; then
  fail "CDN reference found in lane4 HTML"
else
  pass "no CDN refs in lane4 HTML"
fi

# 5) importmap points at local vendor
for f in production-line/viewer/gf/index.html production-line/viewer/ff/index.html production-line/viewer/exterior/index.html; do
  if rg -q 'vendor/three/build/three.module.js' "$f"; then pass "local three importmap/path in $f"; else fail "missing local three path in $f"; fi
done

# 6) optimizer patches present
for f in production-line/viewer/gf/index.html production-line/viewer/ff/index.html; do
  rg -q 'shadowMap.autoUpdate = false' "$f" && pass "shadow bake flag in $f" || fail "missing shadow bake in $f"
  rg -q '__lane4RequestRender|__LANE4' "$f" && pass "demand-render hooks in $f" || fail "missing demand-render in $f"
done
rg -q 'shadowMap.autoUpdate = false' production-line/viewer/exterior/index.html && pass "exterior shadow bake" || fail "exterior missing shadow bake"

# 7) optional gltf validator if any glb under lane4 (none expected yet)
glb_count=$(find production-line/viewer -name '*.glb' | wc -l | tr -d ' ')
if [[ "$glb_count" == "0" ]]; then
  pass "no GLB in lane4 yet (procedural viewers); glTF validator skipped"
else
  if command -v gltf-validator >/dev/null 2>&1; then
    find production-line/viewer -name '*.glb' -print0 | while IFS= read -r -d '' g; do
      gltf-validator "$g" || fail "validator $g"
    done
  else
    note "WARN: glbs present but gltf-validator not installed"
  fi
fi

# 8) static evidence files
[[ -f production-line/viewer/baseline/before.json ]] && pass "baseline before.json" || fail "missing before.json"
[[ -f production-line/viewer/baseline/after.json ]] && pass "baseline after.json" || fail "missing after.json"

if (( FAIL )); then
  note "RESULT: FAIL"
  exit 1
fi
note "RESULT: PASS"
