// Left view, step 3 blockout pass 11 (critic on 2122647): first-floor openings on the left facade.
// ELEV-LEFT at the locked left camera (38.9 px/m at the FF face x 2.95, 1280x720; row r -> Y = 7.85 - (r-250)/38.9):
//  - three tall windows in the central block, columns 522-565 / 710-737 / 817-846 -> z 12.0-13.1 / 16.9-17.6 / 19.6-20.4, rows 290-400 -> Y 4.0-6.82
//  - balconies at both ends, open to the FF glass behind: z 3.1-7.6 and z 21.7-24.4, glass rails rows 365-403 -> Y 4.0-4.95
// A thin stone skin (x 2.88-2.95, in front of the CAD wall line) carries the central block with the window holes; the CAD FF walls at the
// balcony bays (ff-wall-1, ff-wall-7, ff-wall-76, ff-wall-78) are hidden in this view and re-added only outside the bays, so the CAD FF glass
// (ff-glass-left, x 3.05) shows there. Footprint unchanged. Sizes/positions image-read, display assumptions (M35).
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.remove.push('ff-wall-1', 'ff-wall-7', 'ff-wall-76', 'ff-wall-78');
(function(){
  const A = 'left_pass11_image_read_assumption_M35', add = b => window.MODEL_OVERRIDES.add.push(Object.assign({status:A}, b));
  // CAD walls re-added outside the balcony bays
  add({id:'l11-ffwall-7-rest',  cat:'ff_wall', mat:'stone', x0:2.95, x1:3.25, z0:7.6,   z1:14.92, y0:4.0, y1:7.4});
  add({id:'l11-ffwall-76-rest', cat:'ff_wall', mat:'stone', x0:2.95, x1:3.25, z0:18.54, z1:21.7,  y0:4.0, y1:7.4});
  // central skin with three window holes
  const holes = [[12.0,13.1],[16.9,17.6],[19.6,20.4]], Z0 = 7.6, Z1 = 21.7, WY = 6.82; let z = Z0;
  holes.forEach(([h0,h1], i) => {
    add({id:'l11-skin-' + i, cat:'ff_wall', mat:'stone', x0:2.88, x1:2.95, z0:z, z1:h0, y0:4.0, y1:7.4});
    add({id:'l11-skin-head-' + i, cat:'ff_wall', mat:'stone', x0:2.88, x1:2.95, z0:h0, z1:h1, y0:WY, y1:7.4});
    add({id:'l11-window-' + i, cat:'ff_glass', mat:'window_dark', x0:2.93, x1:2.97, z0:h0, z1:h1, y0:4.0, y1:WY});
    add({id:'l11-frame-' + i, cat:'ff_frame', mat:'bronze_dark', x0:2.86, x1:2.90, z0:h0 - 0.04, z1:h1 + 0.04, y0:WY, y1:WY + 0.05});
    z = h1; });
  add({id:'l11-skin-3', cat:'ff_wall', mat:'stone', x0:2.88, x1:2.95, z0:z, z1:Z1, y0:4.0, y1:7.4});
  // glass rails at both balconies
  [[3.1,7.6],[21.7,24.4]].forEach(([z0,z1], i) => {
    add({id:'l11-rail-glass-' + i, cat:'balustrade', mat:'glass_balustrade', x0:2.86, x1:2.90, z0, z1, y0:4.0, y1:4.95});
    add({id:'l11-rail-cap-' + i,   cat:'balustrade', mat:'bronze_dark',      x0:2.85, x1:2.91, z0, z1, y0:4.95, y1:4.99}); });
})();
