# Exterior live Blender scene, 2026-11-11 (WIP, REVIEW-PENDING)

Concept visualisation, not survey-verified, not construction-ready, not certified CAD.

`villa_exterior_live.blend` (Blender 5.2.2 LTS, compressed) is the scene built live on Colin's PC through the Blender Lab MCP extension. Scene name: `Ashwood_Exterior_Live`.

Contents:
- Import of `exterior-garden-3d/4b/villa-materials.glb` at commit `ec29d41`. Pool parts (`POOL_*`, `DECK_left_of_pool`) moved +3.78 m on Blender Y, the same set-back as `villa.html`.
- `LIVE_terrace`: terrace slab, sofa, two armchairs, coffee table, two sun loungers (bevelled boxes, built by Python).
- `LIVE_trees`: eight trees on the `TREE_*_broadleaf_trunk` spots, two shapes (olive type, upright broadleaf), branching trunks and separate leaf quads. The old `broadleaf` spheres are hidden, not deleted.
- `LIVE_pool`: the existing `POOL_water (CAD 9.50 x 2.40)` plane now uses `MAT_pool_water_live` (cyan #5fc2cf, roughness 0.06, transmission 1, IOR 1.333, alpha 0.55, noise ripple). Floor and the four walls use `MAT_pool_basin`, a pale procedural tile. Courtyard water stays on `MAT_water`. Coping stays on `MAT_coping`. No mesh was moved.

No downloaded models or textures, no BlenderKit assets.

ASSUMPTIONS (not from the plan): tree heights and crown sizes, furniture dimensions.
Not in this Blender file: palms, courtyard pine, and the drawn lawn. Those are on the web page only (`exterior-garden-3d/4b/garden_three.js`).
No independent critic pass yet. This is separate from the official `4b_*.blend` files, which are untouched.
