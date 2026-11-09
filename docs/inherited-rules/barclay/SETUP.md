# Setup (all free)
- Blender 4.2.3: download https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz, extract to ~/apps/blender-4.2.3-linux-x64; run scripts with `blender -b -y file.blend --python script.py`. Add-ons: BlenderGIS (github.com/domlysz/BlenderGIS), blender-mcp (github.com/ahujasid/blender-mcp, port 9876, run under xvfb-run).
- COLMAP 3.13: `conda create -n colmap -c conda-forge colmap`. OpenSplat 1.2.2 (CPU build, github.com/pierotofy/opensplat).
- KTX-Software in ~/apps/ktx (github.com/KhronosGroup/KTX-Software releases).
- Node 18+: `npx gltf-transform` (meshopt/resize), `npx gltf-validator` (used by validate.sh), `vercel` CLI for viewer deploy.
- Python 3: numpy, rasterio/GDAL, requests (OSM Overpass, LIDAR processing).
- Data: EA LIDAR 1 m DSM/DTM (OGL) https://environment.data.gov.uk/survey ; OSM via Overpass; textures ambientCG / Poly Haven (CC0).
- MCPs/plugins used by agents: Blender MCP, Playwright, GitHub, Vercel, Google Drive, X (bookmark analyst).
- Python venv (.venv, not committed, regenerable): `python3 -m venv .venv && .venv/bin/pip install -r requirements-venv.txt`
