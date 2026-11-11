# Exterior live Blender scene, 2026-11-11 (WIP, REVIEW-PENDING)

Concept visualisation, not survey-verified, not construction-ready, not certified CAD.

`villa_exterior_live.blend` (Blender 5.2.2 LTS, compressed) is the scene built live on Colin's PC through the Blender Lab MCP extension. Scene name: `Ashwood_Exterior_Live`.

Contents:
- Import of `exterior-garden-3d/4b/villa-materials.glb` at commit `ec29d41`. Pool parts (`POOL_*`, `DECK_left_of_pool`) moved +3.78 m on Blender Y, the same set-back as `villa.html`.
- `LIVE_terrace`: terrace slab, sofa, two armchairs, coffee table, two sun loungers (bevelled boxes, built by Python).
- `LIVE_trees`: eight trees on the `TREE_*_broadleaf_trunk` spots, two shapes (olive type, upright broadleaf), branching trunks and separate leaf quads. The old `broadleaf` spheres are hidden, not deleted.
- `LIVE_hedges`: nine leafy hedges on the `HEDGE_lawn-*` and `HEDGE_front_bed` boxes (about 57,000 leaf quads over a dark core). The old boxes are hidden, not deleted.

No downloaded models or textures, no BlenderKit assets.

ASSUMPTIONS (not from the plan): tree heights and crown sizes, furniture dimensions.
Not done here: palms, courtyard pine, lawn, pool water and tiles (those pool changes exist only in the web page, `exterior-garden-3d/4b/garden_three.js`).
No independent critic pass yet. This is separate from the official `4b_*.blend` files, which are untouched.
