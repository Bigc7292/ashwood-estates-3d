#!/usr/bin/env bash
# Install headless Blender on a Kaggle (or other Linux) GPU notebook.
# Uses the apt package to avoid extra downloads. Blender version is whatever apt provides;
# check `blender -v` and compare with the version used on Colin's PC before trusting renders.
set -euo pipefail

sudo apt-get update -y
sudo apt-get install -y blender libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1

blender -b --version
nvidia-smi || echo "[install] no NVIDIA GPU visible; render_gpu.py will fall back to CPU"
