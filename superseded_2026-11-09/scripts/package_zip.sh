#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/Ashwood_Estates_plan_visuals_archive.zip}"
if command -v zip >/dev/null 2>&1; then
  cd "$ROOT"
  rm -f "$OUT"
  zip -r "$OUT" original extracts plans floors rooms cad-style manifests missing reports previews scripts docs state \
    -x '*/.venv/*' '*.pyc' '*/__pycache__/*' 'extracts/images/embedded/*' 'extracts/pages/page110-*'
else
  python3 - <<PY
import zipfile, os
from pathlib import Path
ARCH=Path("$ROOT"); out=Path("$OUT")
include_roots=['original','extracts','plans','floors','rooms','cad-style','manifests','missing','reports','previews','scripts','docs','state']
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for root in include_roots:
    base=ARCH/root
    if not base.exists(): continue
    for p in base.rglob('*'):
      if not p.is_file(): continue
      rel=str(p.relative_to(ARCH))
      if '.venv' in rel.split(os.sep) or '__pycache__' in rel.split(os.sep): continue
      if rel.startswith('extracts/images/embedded/'): continue
      if rel.startswith('extracts/pages/') and 'page110-' in rel: continue
      z.write(p, rel)
print('wrote', out)
PY
fi
ls -lh "$OUT"
