// Front view, pass 5 (critic's one fix, ranked above the hedge): layered timber/bronze slat screen on the first floor.
// Replaces the single dark block 'ff-slat-screen' (x 7.04-11.04). Extent back-projected from ELEV-FRONT through the
// locked camera: left edge x 5.4 (image-read, assumption), right edge at the projecting stone block x 11.04 (model).
// Height: FF floor 4.0 to roof soffit 7.4 (model levels). Two layers of vertical slats, staggered. Concept visualisation only.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.remove.push('ff-slat-screen');
(function(){
  const X0 = 5.4, X1 = 11.04, Y0 = 4.0, Y1 = 7.4, W = 0.045, P = 0.13;
  const layers = [ {z0:24.70, z1:24.76, off:0}, {z0:24.56, z1:24.61, off:P/2} ];
  layers.forEach((L, li) => { for (let x = X0 + L.off; x + W <= X1; x += P)
    window.MODEL_OVERRIDES.add.push({id:'ff-slat-'+li+'-'+x.toFixed(2), cat:'slats', mat:'bronze_dark', x0:x, x1:x+W, z0:L.z0, z1:L.z1, y0:Y0+0.08, y1:Y1-0.08, status:'pass5_image_read_extent_assumption'}); });
  window.MODEL_OVERRIDES.add.push(
    {id:'ff-slat-rail-top', cat:'slats', mat:'bronze_dark', x0:X0, x1:X1, z0:24.56, z1:24.76, y0:Y1-0.08, y1:Y1, status:'pass5_assumption'},
    {id:'ff-slat-rail-bottom', cat:'slats', mat:'bronze_dark', x0:X0, x1:X1, z0:24.56, z1:24.76, y0:Y0, y1:Y0+0.08, status:'pass5_assumption'});
})();
