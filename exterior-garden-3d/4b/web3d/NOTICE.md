# Third-party code in web3d/

All three.js files are from three.js **r160** (MIT licence, copyright 2010-2023 three.js authors; full text in
`vendor/three/LICENSE`). The viewer runs fully offline from these copies.

| file | source |
|---|---|
| vendor/three/build/three.module.js | copied from awroot/active/floorplan3d-spike/FP-4B-GF/vendor/three (three@0.160.0) |
| vendor/three/examples/jsm/controls/OrbitControls.js, PointerLockControls.js | same vendored copy (three@0.160.0) |
| vendor/three/examples/jsm/environments/RoomEnvironment.js | same vendored copy (three@0.160.0) |
| vendor/three/examples/jsm/objects/Water2.js, Reflector.js, Refractor.js | same vendored copy (three@0.160.0) |
| vendor/three/examples/textures/water/Water_1_M_Normal.jpg, Water_2_M_Normal.jpg | same vendored copy (three.js repo examples, MIT) |
| vendor/three/examples/jsm/loaders/GLTFLoader.js | downloaded 2026-11-09 from https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js (MIT) |
| vendor/three/examples/jsm/utils/BufferGeometryUtils.js | downloaded 2026-11-09 from https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/utils/BufferGeometryUtils.js (MIT) |

All textures in `tex/` and inside `ashwood_4b_exterior.glb` are baked by `export_glb.py` from the project's own procedural
Blender materials (no third-party image assets).
