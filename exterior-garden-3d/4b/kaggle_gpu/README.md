# Kaggle GPU render (Ashwood 4B exterior, WIP)

Status: **WIP, not run.** The Kaggle connector is signed out and the sandbox proxy blocks kaggle.com (403 on CONNECT), so nothing here has executed yet.

## Files
- `install_blender.sh`: installs headless Blender on a GPU notebook.
- `render_gpu.py`: opens a saved scene and renders one Cycles frame on GPU.

## Steps (private notebook only)
1. Create a **private** Kaggle notebook, accelerator GPU. Turn on internet only if needed for apt.
2. Upload the scene `.blend` as a **private** dataset (or generate it in the notebook from `blender_wip/build_scene_f1.py`, which must stay as is; `build_scene_ORIG_backup.py` is not edited).
3. `bash install_blender.sh`
4. `blender -b scene.blend -P render_gpu.py -- /kaggle/working/villa_gpu.png 128`
5. Log the Kaggle GPU quota used before and after the run.

## Labels
Concept visualisation. Not survey-verified. Not construction-ready. Not certified CAD.
