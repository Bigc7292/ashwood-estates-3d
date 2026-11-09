# Tricks register: exterior lane (4b)

Concept visualisation only. It is not survey-verified, not construction-ready and not certified CAD.

## T-W2: three.js Water2 pool water (rear_pass.html + overrides/rear_pass3_water2.js, rear_pool2.js)

- **Source:** the vendored `model/vendor/three/examples/jsm/objects/Water2.js` (three.js r160, MIT; see `model/vendor/three/LICENSE`, © 2010-2024 three.js authors). No CDN. The licence notice is kept in the vendored tree.
- **Technique:**
  - two scrolling normal maps (`Water_1_M_Normal`/`Water_2_M_Normal`, vendored), scale 3.2, flowSpeed 0.025, giving fine, gentle ripples
  - reflector plus refractor, reflectivity 0.06, so the light mosaic basin shows through
  - tint 0xbff0f2 (aqua)
  - sun glints from an additive black-base MeshStandardMaterial layer that uses the same normals
  - deterministic flow (`onBeforeRender` sets `uniforms.config` from `window.__T`), so captures are repeatable
- **Root-cause fix:** Water2 builds its Reflector and Refractor plane from the mesh transform, so the geometry must be XY with `rotation.x = -PI/2`. Rotating the geometry in place gave a zero contribution, which was the critic's "Water2 renders nothing" finding. The proof is in `water2_proof/RESULT.txt`: shown vs hidden mean delta 24.9, and t5 vs t6 mean delta 4.07.
- **Caustics:** blurred-Voronoi canvas textures (tCau / tCau2) used as emissive maps on the basin floor and walls and animated by UV offset. No extra pass, and they cost about 0 ms.
- **Waterline:** an aqua mosaic band plus an emissive glow strip (y -0.075) under the thin flush coping.

| build | Water2 RT size | RT memory (2 targets, RGBA8 + depth) | ms/frame (SwiftShader, 1280×720, bench.cjs, 40 frames) | fps |
|---|---|---|---|---|
| before: b14a910 (flat pool material) | none | 0 | 171.8 | 5.8 |
| pool WIP (Water2 1024, before the orientation fix) | 1024² | ~8 MB | 208.5 | 4.8 |
| after (Water2 1024, fixed) | 1024² | ~8 MB | BENCH_DESKTOP | |
| phone `?phone=1` (Water2 256, pixel ratio ≤1.5) | 256² | ~0.5 MB | BENCH_PHONE | |

The SwiftShader numbers are relative only, because it is CPU rasterisation. A real GPU will be much faster. The phone profile drops the targets to 256 and caps the pixel ratio.
