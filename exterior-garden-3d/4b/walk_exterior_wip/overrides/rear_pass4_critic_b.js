// Rear + garden step 6 pass 4 (critic batch (b), 2026-11-10; report production-line/critic/2026-11-10_exterior-rear-garden.md).
// 1. Restore the 8 approved-plan tree symbols removed in pass 1 (palms stay on the 4 CAD positions nearest the rear garden).
//    Drawn as open multi-stem trees (species/height unknown: assumption) at the CAD symbol positions.
// 2. Terrace step: two wide steps were added in the pool pass (rear_pool2.js, pool-step-1/2).
// 3. Grey roof block: the grey placeholder RF canopy is removed; the RF core stays as the small set-back box ELEV-REAR shows, in pale render (not grey).
// 4. FF balcony: thick white slab edge under the existing glass rail (ff-balustrade-rear), per ELEV-REAR / EXT-4b-POOL. Thickness assumed 0.32 m.
// 5. Thicker planting along both side boundaries and the rear lawn edge, per ELEV-REAR / GARDEN-BACK (hedge band, bougainvillea, ornamental grasses).
// Concept visualisation only; positions of new planting are image-read assumptions.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
const _O4 = window.MODEL_OVERRIDES, _s4 = 'rear_pass4_critic_b';
const _palmXZ = (_O4.palms || []).map(p => [p.x, p.z]);
const _restored = window.MODEL.trees.filter(t => !t.courtyard && !_palmXZ.some(([x,z]) => Math.hypot(t.x-x, t.z-z) < 0.05));
_O4.multiStemTrees = (_O4.multiStemTrees || []).concat(_restored.map((t,i) => ({id:`cad-tree-${i}`, x:t.x, z:t.z, top:4.6, spread:3.0, stems:5, clusters:300, color:0x4f6e33, status:'CAD tree symbol restored (critic b); species/height assumption'})));
_O4.remove.push('rf-canopy');
_O4.add.push({id:'ff-balcony-slab-rear', cat:'balcony', mat:'soffit', x0:2.95, x1:15.78, z0:2.96, z1:4.6, y0:3.68, y1:4.0, status:_s4+' slab edge, thickness assumed'});
_O4.rf_core_mat = 'soffit';
_O4.shrubRows = (_O4.shrubRows || []).concat([
  {id:'rear-hedge-band-left',  x0:0.35,  z0:10.0, x1:0.35,  z1:16.0, h:1.8, r:0.45, color:0x40602a, status:_s4},
  {id:'rear-hedge-band-right', x0:18.35, z0:10.0, x1:18.35, z1:16.0, h:1.8, r:0.45, color:0x40602a, status:_s4},
  {id:'bougainvillea-left',    x0:0.5,   z0:3.0,  x1:0.5,   z1:6.5,  h:2.2, r:0.55, color:0x4a6a2e, flowers:0xc2307a, status:_s4},
  {id:'bougainvillea-right',   x0:18.2,  z0:3.5,  x1:18.2,  z1:7.0,  h:2.2, r:0.55, color:0x4a6a2e, flowers:0xd04a8a, status:_s4},
  {id:'grasses-lawn-edge-l',   x0:-1.2,  z0:-3.5, x1:-1.2,  z1:-12,  h:0.7, r:0.25, color:0x8a9450, status:_s4+' off-plot context'},
  {id:'grasses-lawn-edge-r',   x0:19.9,  z0:-3.5, x1:19.9,  z1:-12,  h:0.7, r:0.25, color:0x8a9450, status:_s4+' off-plot context'}
]);
