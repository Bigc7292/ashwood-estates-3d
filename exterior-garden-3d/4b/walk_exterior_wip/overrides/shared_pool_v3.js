// SHARED pool, terrace seating and enlarged rear garden (lane 2 cloud builder, 2026-11-10). Load in every exterior page that shows the rear.
// Source: Colin 2026-11-09 23:29 (via coordinator): "The pool needs to be further away from the back of the building and wider and i was
// missin sit down area". His ruling overrides the CAD pool position/width. Earlier Colin rulings carried: M29 (pool wider/shorter per
// EXT-4b-POOL), M30 (garden enlarged beyond the CAD rear boundary so terrace + pool + lawn fit). Grok's rear_pool2.js / rear_garden_enlarged.js
// are NOT used (worker retired, unverified); this file is the lane's own version.
//   Pool water: x 3.15-12.65 (length 9.50 m = brochure/CAD length, kept), z -3.83..-0.23 (width 3.60 m: ASSUMPTION for "wider"; CAD 2.38 m,
//   Grok 2.80 m; ratio ~2.6:1, EXT-4b-POOL reads ~3:1 or less). Coping 0.30 m (CAD) drawn by the page's basin builder. Depth 1.4 m display.
//   Terrace: GF rear glazing z 4.57 to the house-side coping z -0.23-0.30 = ~4.8 m of pale stone terrace (CAD 0.72 m) -> room for the seating
//   area (ASSUMPTION, from EXT-4b-GARDEN-BACK / EXT-4b-POOL: deep pale terrace with a lounge sofa set, loungers at the pool end).
//   Pool platform: x 2.85-15.06, z -4.13..0 (pale stone, flush with the terrace).
//   Rear garden: lawn z -9.0..-4.13 beyond the pool; side walls continued and a new rear wall at z -9.0..-9.25 (M30 extent, Colin ruling).
//   Seating (ASSUMPTION, sizes typical): lounge sofa 2.4 x 0.9 m facing the pool, two armchairs, coffee table on the terrace (x 4.2-7.8,
//   z 1.4-3.9); the two CAD terrace loungers + side table (V4 GF plan symbols at x ~13-15, M31) moved to the pool's east end.
// All levels flat at y 0 (the reference's raised pool edge / lawn drop is not modelled yet). Concept visualisation, not survey-verified,
// not construction-ready, not certified CAD.
(function(){
  const O = (window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]}), st = 'shared_pool_v3: Colin 23:29 ruling (further, wider, seating); values assumption';
  const P = window.MODEL.water.find(w => w.id === 'swimming-pool');
  if (P) { P.cad_rect = [P.x0, P.z0, P.x1, P.z1]; Object.assign(P, {x0:3.15, x1:12.65, z0:-3.83, z1:-0.23, status:st}); }
  O.remove.push('pool-coping-n','pool-coping-s','pool-coping-w','pool-coping-e');
  const ZB = -9.0;
  O.add.push(
    {id:'pool-platform-v3', cat:'ground', mat:'paving_inner', x0:2.85, x1:15.06, z0:-4.13, z1:0.0, y0:-0.05, y1:0.0, status:st},
    {id:'rear-lawn-v3', cat:'lawn', mat:'lawn', x0:0.0, x1:18.724, z0:ZB, z1:-4.13, y0:-0.02, y1:0.01, status:st+' (M30 garden extent)'},
    {id:'rear-lawn-side-l-v3', cat:'lawn', mat:'lawn', x0:0.0, x1:2.85, z0:-4.13, z1:0.0, y0:-0.02, y1:0.01, status:st},
    {id:'rear-lawn-side-r-v3', cat:'lawn', mat:'lawn', x0:15.06, x1:18.724, z0:-4.13, z1:0.0, y0:-0.02, y1:0.01, status:st},
    {id:'boundary-left-ext-v3',  cat:'boundary', mat:'stone', x0:-0.25,  x1:0,      z0:ZB-0.25, z1:0,  y0:0, y1:1.8, status:st+' (M30)'},
    {id:'boundary-right-ext-v3', cat:'boundary', mat:'stone', x0:18.724, x1:18.974, z0:ZB-0.25, z1:0,  y0:0, y1:1.8, status:st+' (M30)'},
    {id:'boundary-rear-v3',      cat:'boundary', mat:'stone', x0:-0.25,  x1:18.974, z0:ZB-0.25, z1:ZB, y0:0, y1:1.8, status:st+' (M30)'},
    // seating area on the terrace (faces the pool, -z)
    {id:'seat-sofa-base',  cat:'furniture', mat:'bronze_dark', x0:4.6, x1:7.0, z0:3.0, z1:3.9, y0:0.0, y1:0.22, status:st},
    {id:'seat-sofa-cush',  cat:'furniture', mat:'curtain',     x0:4.65, x1:6.95, z0:3.05, z1:3.85, y0:0.22, y1:0.42, status:st},
    {id:'seat-sofa-back',  cat:'furniture', mat:'curtain',     x0:4.65, x1:6.95, z0:3.6, z1:3.9, y0:0.42, y1:0.80, status:st},
    {id:'seat-arm-l-base', cat:'furniture', mat:'bronze_dark', x0:3.6, x1:4.4, z0:1.6, z1:2.4, y0:0.0, y1:0.22, status:st},
    {id:'seat-arm-l-cush', cat:'furniture', mat:'curtain',     x0:3.63, x1:4.37, z0:1.63, z1:2.37, y0:0.22, y1:0.42, status:st},
    {id:'seat-arm-l-back', cat:'furniture', mat:'curtain',     x0:3.6, x1:3.85, z0:1.6, z1:2.4, y0:0.42, y1:0.78, status:st},
    {id:'seat-arm-r-base', cat:'furniture', mat:'bronze_dark', x0:7.2, x1:8.0, z0:1.6, z1:2.4, y0:0.0, y1:0.22, status:st},
    {id:'seat-arm-r-cush', cat:'furniture', mat:'curtain',     x0:7.23, x1:7.97, z0:1.63, z1:2.37, y0:0.22, y1:0.42, status:st},
    {id:'seat-arm-r-back', cat:'furniture', mat:'curtain',     x0:7.75, x1:8.0, z0:1.6, z1:2.4, y0:0.42, y1:0.78, status:st},
    {id:'seat-coffee-table', cat:'furniture', mat:'coping',    x0:5.2, x1:6.4, z0:1.7, z1:2.3, y0:0.0, y1:0.36, status:st},
    // CAD terrace loungers + side table (M31), moved to the pool's east end
    {id:'lounger-1-v3',      cat:'furniture', mat:'curtain',     x0:13.1, x1:13.8, z0:-3.5, z1:-1.5, y0:0.0, y1:0.32, status:'CAD V4 GF terrace symbol, moved with the pool (Colin 23:29)'},
    {id:'lounger-1-back-v3', cat:'furniture', mat:'curtain',     x0:13.1, x1:13.8, z0:-2.0, z1:-1.5, y0:0.32, y1:0.62, status:'CAD symbol; back rest assumption'},
    {id:'lounger-2-v3',      cat:'furniture', mat:'curtain',     x0:14.2, x1:14.9, z0:-3.5, z1:-1.5, y0:0.0, y1:0.32, status:'CAD V4 GF terrace symbol, moved with the pool (Colin 23:29)'},
    {id:'lounger-2-back-v3', cat:'furniture', mat:'curtain',     x0:14.2, x1:14.9, z0:-2.0, z1:-1.5, y0:0.32, y1:0.62, status:'CAD symbol; back rest assumption'},
    {id:'side-table-v3',     cat:'furniture', mat:'bronze_dark', x0:13.85, x1:14.15, z0:-1.2, z1:-0.9, y0:0.0, y1:0.45, status:'CAD V4 GF terrace symbol'}
  );
  O.shrubRows = (O.shrubRows || []).concat([
    {id:'garden-rear-hedge-v3', x0:0.7, z0:ZB+0.6, x1:18.0, z1:ZB+0.6, h:1.8, r:0.5, color:0x4f5a2a, status:st+' (M30 boundary planting, image-read)'}
  ]);
})();
