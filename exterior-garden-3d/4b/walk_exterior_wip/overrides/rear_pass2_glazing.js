// Rear + garden step 6 pass 2 (lane 2 self-critique): "glazing reads as tan opaque slabs".
// ELEV-REAR / GARDEN-BACK / POOL / p26 show clear dark glass with warm-lit rooms behind and slim dark frames.
// Same approach as front pass 8: dark clear glass + lit interior surfaces behind the CAD glass lines (gf-glass-0/1, ff-glass-rear).
// Interior depths, finishes and mullion spacing are display assumptions (not on plan). Glass positions/widths = CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.glass_mode = 'interior';
const _A = window.MODEL_OVERRIDES.add, _s = 'rear_pass2_display_assumption';
for (const [x0,x1] of [[3.23,10.7],[12.69,15.06]]) {         // GF rear glass spans (CAD gf-glass-0, gf-glass-1)
  _A.push({id:`rear-gf-floor-${x0}`, cat:'interior', mat:'interior_floor',   x0, x1, z0:4.9, z1:9.0, y0:0.0,  y1:0.04, status:_s},
          {id:`rear-gf-ceil-${x0}`,  cat:'interior', mat:'interior_ceiling', x0, x1, z0:4.9, z1:9.0, y0:3.5,  y1:3.56, status:_s},
          {id:`rear-gf-back-${x0}`,  cat:'interior', mat:'interior_stone',   x0, x1, z0:9.0, z1:9.1, y0:0.0,  y1:3.5,  status:_s});
  for (let x = x0; x <= x1 + 1e-6; x += (x1 - x0) / Math.max(1, Math.round((x1 - x0) / 2.4)))   // slim dark frames ~2.4 m
    _A.push({id:`rear-gf-mull-${x.toFixed(2)}`, cat:'gf_glass', mat:'bronze_dark', x0:x-0.03, x1:x+0.03, z0:4.5, z1:4.56, y0:0.0, y1:3.6, status:_s});
}
_A.push({id:'rear-ff-floor', cat:'interior', mat:'interior_floor',   x0:2.95, x1:15.78, z0:4.85, z1:8.6, y0:4.0, y1:4.04, status:_s},
        {id:'rear-ff-ceil',  cat:'interior', mat:'interior_ceiling', x0:2.95, x1:15.78, z0:4.85, z1:8.6, y0:7.3, y1:7.36, status:_s},
        {id:'rear-ff-back',  cat:'interior', mat:'interior_wood',    x0:2.95, x1:15.78, z0:8.6,  z1:8.7, y0:4.0, y1:7.3,  status:_s});
for (let x = 2.95; x <= 15.79; x += (15.78 - 2.95) / 5)
  _A.push({id:`rear-ff-mull-${x.toFixed(2)}`, cat:'ff_glass', mat:'bronze_dark', x0:x-0.03, x1:x+0.03, z0:4.68, z1:4.73, y0:4.0, y1:7.4, status:_s});
