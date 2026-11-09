# Barclay House (Manchester) – FREE photoreal archviz workflows from X
Sources: Colin's X bookmarks (signed in as @topcdawg777, 36 bookmarks scanned, about 15 on 3D) plus a public X search for photogrammetry/splat/OSM/LIDAR posts. Paid items are dropped or swapped for a free alternative. Scanned 3 Nov 2026 (UTC+4).

## From X (bookmarks unless marked)
1. https://x.com/sorenxet/status/2116912025825616083 – Opus + Blender over MCP: reference shots in, a camera matched and locked to the reference, then the scene built in about 8 prompts (1,876 objects). **Why:** the camera-match-then-block-out method suits matching Barclay House facade photos. **Free swap:** the open-source Blender MCP add-on with a local Ollama model, or just run our Python build script.
2. https://x.com/RoundtableSpace/status/2112751982633205983 – mcp-for-blender-pro, an open-source add-on: 21 scene tools and works with local **Ollama** (free). **Why:** a free AI helper inside Blender for repetitive facade, window-grid and material edits.
3. https://x.com/emmanuel_2m/status/2110342352665473156 and https://x.com/emmanuel_2m/status/2116188727579918358 – Scenario plugin / "3D OS" for Blender, open-sourced. **Caveat:** its generation calls go to Scenario's credit-based API (paid), so use only the free, open skills/scripts structure. Low priority.
4. https://x.com/AnatoliKopadze/status/2115044206322368698 – Hi3D, an open-source photo-to-3D model. **Why:** quick free props (street furniture, bins, signage) for the street level. Not suitable for the main building.
5. https://x.com/cutetoxicguy/status/2116194416482263277 (public search) – Idol, an open-weight image-to-3D model that runs on an 8GB GPU. **Why:** a local, free alternative to #4 for props.
6. https://x.com/lyzzz97/status/2117246558962057515 – Gaussian-Splat-Lite, an open-source Three.js/WebGPU 3DGS renderer and converter. **Why:** if Colin captures a phone video of the site, it gives a free way to show a splat of the surroundings on the web.
7. https://x.com/FreeGaussian/status/2116923218707800310 (public) – a city-scale 3D Gaussian Splat example (Panama City Beach). **Why:** shows that splats work for neighbouring blocks and a backdrop. **Free toolchain:** COLMAP, then Nerfstudio splatfacto or the original gaussian-splatting repo, then Blender (KIRI 3DGS Render add-on, free).
8. https://x.com/FablessBridge/status/2115839828587876840 (public) – COLMAP running in a browser. **Why:** confirms COLMAP as the free structure-from-motion step for photogrammetry or splats of Barclay House from street photos.
9. https://x.com/techxsarfraj/status/2108821963494105366 and https://x.com/pascal/status/2115809363151773979 – Pascal Editor, an open-source browser building editor (R3F/WebGPU). **Why:** an optional free way to share an interactive web view or blockout. Blender stays the main tool.
10. https://x.com/0x0SojalSec/status/2108683699130970241 – SpatialLM, an open model that turns phone video into a labelled 3D layout. Mostly for interiors, so limited use for the exterior. Low priority.
11. https://x.com/Qianying_Lin_X/status/2115805729768579309 (public) – a thread listing 95+ free 3D tools around Blender and CC0 libraries. **Why:** a checklist of free asset sources. Ignore the AI generators' paid tiers.
12. https://x.com/Cipher_twt/status/2117288122736095407 (public) – 17 free 3D resource sites. Same use as #11 for props and textures.
13. https://x.com/SimbasJungles/status/2109095401273938072 – a real property modelled from a few photos plus a 2D plan (Blender, then UE5, which is free). **Why:** the same photos-plus-plan workflow Colin's data will support.

Dropped as paid or irrelevant: SUAPP AI (SketchUp, paid), Planner 5D AI Studio, Kimi 3D Make, Hyper3D, the "free tokens" and "free Claude Code" proxy posts (ToS risk), plus crypto and giveaway bookmarks.

## Free core stack (not from X; standard free tools to fill the gaps)
- **Context:** Blender OSM import via the free tier of Blosm (OSM buildings and rails) or the OSM importer in BlenderGIS (free). The train line is the OSM railway=rail way, and the Network Rail line next to the site is in OSM.
- **LIDAR/DSM:** DEFRA Survey Data Download / environment.data.gov.uk, with 1m/50cm DSM/DTM under the Open Government Licence. Load in BlenderGIS or QGIS. nDSM = DSM − DTM gives roof heights for checking the building height.
- **Photogrammetry:** COLMAP or Meshroom (AliceVision) from street photos (≥60% overlap), then decimate and retopo in Blender.
- **Splats:** Nerfstudio splatfacto / gaussian-splatting, viewed in SuperSplat (free, browser).
- **PBR/HDRI:** Poly Haven (CC0 HDRIs, use an overcast one for Manchester), ambientCG (CC0 brick, concrete, glass), Sketchfab CC-BY for trains.
- **AI textures:** Material Maker (free) or Blender's built-in bake from photos. Local Stable Diffusion with a tileable/seamless setting through ComfyUI is free if a GPU is available.
- **Render:** Cycles with OptiX/OIDN denoise, AgX view transform, Sky texture or Poly Haven HDRI, and Scatter via Geometry Nodes for trees and cars.
