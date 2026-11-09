#!/bin/bash
B=/home/box/apps/blender-4.2.3-linux-x64/blender
cd /workspace/exterior-garden-3d/4b/blender
for s in boxes space models; do rm -rf ../step3_blockout/gates/$s; $B -b 4b_$s.blend -P render_views.py -- ../step3_blockout/gates/$s 12 640 360 aerial,front_approach,elev_front,garden_pool 2>&1 | grep -E "Saved|Error"; done
$B -b 4b_materials.blend -P render_views.py -- ../step3_blockout/renders_raw 24 1280 720 2>&1 | grep -E "Saved|Error"
echo STEP3_DONE
$B -b 4b_grime.blend -P render_views.py -- ../step4_grime/renders_raw 24 1280 720 2>&1 | grep -E "Saved|Error"
echo STEP4_DONE
