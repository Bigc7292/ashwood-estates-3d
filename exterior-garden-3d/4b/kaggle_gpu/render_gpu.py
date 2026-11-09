"""GPU Cycles render for a saved Ashwood 4B scene (headless Blender).

Run on a Kaggle GPU notebook (or any Linux box with an NVIDIA GPU):
    blender -b <scene.blend> -P render_gpu.py -- <out.png> [samples]

Only reads the scene and writes one image. Does not modify the .blend on disk.
Source scene is produced by blender_wip/build_scene_f1.py (build_scene_ORIG_backup.py stays unchanged).
Output is WIP evidence (concept visualisation, not survey-verified, not construction-ready).
"""
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
SAMPLES = int(argv[1]) if len(argv) > 1 else 128

# Pick the best available GPU backend; fall back to CPU only if no GPU is found.
prefs = bpy.context.preferences.addons["cycles"].preferences
device_found = False
for backend in ("OPTIX", "CUDA", "HIP", "METAL"):
    try:
        prefs.compute_device_type = backend
    except TypeError:
        continue
    prefs.get_devices()
    gpus = [d for d in prefs.devices if d.type != "CPU"]
    if gpus:
        for d in prefs.devices:
            d.use = d.type != "CPU"
        device_found = True
        print(f"[gpu] backend={backend} devices={[g.name for g in gpus]}")
        break
if not device_found:
    print("[gpu] WARNING: no GPU found, rendering on CPU")

sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "GPU" if device_found else "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.render.resolution_x = 1280
sc.render.resolution_y = 720
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print(f"[gpu] wrote {OUT}")
