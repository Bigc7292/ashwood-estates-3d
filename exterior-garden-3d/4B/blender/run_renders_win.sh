#!/bin/bash
# Windows (Git Bash) rebuild + re-render of step 3 (blockout) and step 4 (grime). Blender 5.2, Cycles CPU.
# Usage: bash run_renders_win.sh [blender.exe] [python.exe]
# Run it from a SHORT path (e.g. a junction to this 4B folder): deep paths exceed the Windows 260-char limit.
set -e
B="${1:-/c/Program Files/Blender Foundation/Blender 5.2/blender.exe}"
PY="${2:-python}"
cd "$(dirname "$0")"
# Blender on Windows did not write relative output paths (../step*/...) where expected - renders silently went missing.
# Use an absolute path, kept short by resolving from the (junction) folder the script is run from.
OUT="$(cygpath -m "$(cd .. && pwd)")"
log() { echo "[$(date +%H:%M:%S)] $*"; }

for s in boxes space models materials grime; do
  "$B" -b --factory-startup -P build_scene.py -- $s 4b_$s.blend 2>&1 | grep -E "BUILT|Traceback|Error" || true
done
log BUILT_ALL

# step 3 gates (low-res, 4 key views per sub-stage)
for s in boxes space models; do
  rm -rf ../step3_blockout/gates/$s
  "$B" -b --factory-startup 4b_$s.blend -P render_views.py -- $OUT/step3_blockout/gates/$s 12 640 360 aerial,front_approach,elev_front,garden_pool 2>&1 | grep -cE "RENDERED" || true
done
log GATES_DONE

# step 3 full set (materials) -> captions + side-by-sides
rm -rf ../step3_blockout/renders_raw
"$B" -b --factory-startup 4b_materials.blend -P render_views.py -- $OUT/step3_blockout/renders_raw 24 1280 720 2>&1 | grep -cE "RENDERED" || true
"$PY" caption_compare.py ../step3_blockout/renders_raw ../step3_blockout/renders ../step3_blockout/comparisons "step 3 materials"
log STEP3_DONE

# step 4 full set (grime) -> captions + side-by-sides
rm -rf ../step4_grime/renders_raw
"$B" -b --factory-startup 4b_grime.blend -P render_views.py -- $OUT/step4_grime/renders_raw 24 1280 720 2>&1 | grep -cE "RENDERED" || true
"$PY" caption_compare.py ../step4_grime/renders_raw ../step4_grime/renders ../step4_grime/comparisons "step 4 grime"
log STEP4_RENDERS_DONE

# step 4 grime close-ups -> captioned
rm -rf ../step4_grime/closeups_raw
VIEWS=views_closeups.json "$B" -b --factory-startup 4b_grime.blend -P render_views.py -- $OUT/step4_grime/closeups_raw 32 1280 720 2>&1 | grep -cE "RENDERED" || true
"$PY" caption_closeups.py ../step4_grime/closeups_raw ../step4_grime/closeups
log STEP4_DONE
