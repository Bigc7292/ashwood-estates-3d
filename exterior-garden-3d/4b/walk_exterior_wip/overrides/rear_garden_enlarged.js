// M30 resolved by Colin (chat 2026-11-10 ~01:25 Dubai): "make the garden bigger, but the outside area has to look right. The seating area,
// the swimming pool the size, the width, the decking... it's gotta look correct." The pool (~8.40 x 2.80 m) and the ~3.3 m terrace are NOT shrunk.
// The rear garden is enlarged beyond the CAD site-diagram rear boundary (z 0): new rear boundary at z -9.0 (wall to -9.25), so the plot reads
// 18.724 x ~38.9 m instead of 18.724 x 29.881 m. That leaves ~5.7 m of lawn beyond the far coping (z -2.14 to -7.8) and a ~1.2 m planting strip in
// front of the new rear wall, matching EXT-4b-POOL proportions (lawn beyond the pool, boundary planting behind). The side walls continue
// to the new rear wall. Concept only, not survey-verified. Extent and planting are image-read display assumptions.
(function(){
  const O = window.MODEL_OVERRIDES; if (!O) return;
  const ZB = -9.0, s = 'garden enlarged beyond the CAD plot boundary per Colin 2026-11-10 (M30); concept only, not survey-verified';
  O.add.push(
    {id:'boundary-left-ext',  cat:'boundary', mat:'stone', x0:-0.25,  x1:0,      z0:ZB-0.25, z1:0,  y0:-0.47, y1:1.8, status:s},
    {id:'boundary-right-ext', cat:'boundary', mat:'stone', x0:18.724, x1:18.974, z0:ZB-0.25, z1:0,  y0:-0.47, y1:1.8, status:s},
    {id:'boundary-rear-new',  cat:'boundary', mat:'stone', x0:-0.25,  x1:18.974, z0:ZB-0.25, z1:ZB, y0:-0.47, y1:1.8, status:s});
  // the old off-plot belts sat at z -12/-16, inside the enlarged garden or just past it: move the planting to the new boundary
  const drop = new Set(['context-hedge-rear','grasses-lawn-edge-l','grasses-lawn-edge-r']);
  O.shrubRows = (O.shrubRows || []).filter(r => !drop.has(r.id));
  for (const r of O.shrubRows) if (r.id === 'context-tree-belt') { r.z0 = r.z1 = -11.0; r.status = 'neighbouring gardens beyond the new rear wall (context)'; }
  O.shrubRows.push(
    {id:'garden-rear-hedge',      x0:0.7,  z0:ZB+0.6, x1:18.0, z1:ZB+0.6, h:2.1, r:0.55, color:0x40602a, status:s},
    {id:'garden-rear-flowering',  x0:1.5,  z0:ZB+1.2, x1:17.2, z1:ZB+1.2, h:1.0, r:0.35, color:0x4f7230, flowers:0xc8407e, status:s},
    {id:'garden-side-hedge-l',    x0:0.5,  z0:-2.6,   x1:0.5,  z1:ZB+0.6, h:2.0, r:0.5,  color:0x46662e, status:s},
    {id:'garden-side-hedge-r',    x0:18.2, z0:-3.6,   x1:18.2, z1:ZB+0.6, h:2.0, r:0.5,  color:0x46662e, flowers:0xd04a8a, status:s+' (starts behind the pool camera)'},
    {id:'garden-grasses-l',       x0:1.2,  z0:-3.0,   x1:1.2,  z1:ZB+1.4, h:0.7, r:0.25, color:0x8a9450, status:s},
    {id:'garden-grasses-r',       x0:17.5, z0:-4.2,   x1:17.5, z1:ZB+1.4, h:0.7, r:0.25, color:0x8a9450, status:s});
  O.multiStemTrees = (O.multiStemTrees || []).concat([
    {id:'garden-tree-rear-l', x:1.6,  z:ZB+1.2, top:4.4, spread:2.8, stems:4, clusters:260, color:0x4b6a30, status:s},
    {id:'garden-tree-rear-c', x:9.4,  z:ZB+0.9, top:3.8, spread:2.4, stems:4, clusters:220, color:0x55743a, status:s},
    {id:'garden-tree-rear-r', x:16.9, z:ZB+1.2, top:4.6, spread:2.8, stems:5, clusters:260, color:0x4b6a30, status:s}]);
})();
