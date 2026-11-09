// Pool pass (TOP priority, Colin 2026-11-10). Reference EXT-4b-POOL + p26.
// Colin override (image overrides CAD per Colin 2026-11-10, M29/M30): pool 8.40 x 2.80 m (3:1, read from EXT-4b-POOL) instead of CAD 9.49 x 2.38
// (brochure 9.50 x 2.40), centred on the CAD pool x (7.9), moved away from the house so a 3.31 m pale-stone terrace sits between the GF glazing
// (z 4.57) and the coping. Pool z -1.84..0.96: the far side crosses the site-diagram rear boundary (z 0) by 1.84 m (+0.30 coping), see M30.
// Appearance (image): bright clear aqua water over a light mosaic basin, dark-blue waterline band, thin pale coping flush with the terrace,
// lawn on the far side 0.45 m below the terrace with an exposed warm stone face (critic T2 / p26; see M30). Depth 1.4 m, tile, band height, glints and caustics are display assumptions. Loungers/daybed NOT added (M31).
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.pool2 = true;
window.MODEL_OVERRIDES.water2 = {reflectivity: 0.06, scale: 3.2, flowSpeed: 0.025, color: 0xbff0f2, tex: 1024, texPhone: 256}   // pool tuning: fine gentle ripples (two scrolling normal maps), mostly refraction of the light basin;
{ const P = window.MODEL.water.find(w => w.id === 'swimming-pool');
  P.cad_rect = [P.x0, P.z0, P.x1, P.z1]; Object.assign(P, {x0:3.70, x1:12.10, z0:-1.84, z1:0.96, status:'image overrides CAD per Colin 2026-11-10 (M29/M30)'}); }
const _O = window.MODEL_OVERRIDES, _ps = 'pool pass, image overrides CAD per Colin 2026-11-10';
_O.remove.push('pool-coping-n','pool-coping-s','pool-coping-w','pool-coping-e');   // CAD coping ring follows the CAD pool; the basin builder draws a 0.30 ring round the new pool
for (const b of _O.add) if (b.id === 'context-lawn-rear') b.cut_basin = true;
_O.add.push(
  // wide pale-stone seating terrace at house level (y 0), platform down to the rear lawn 0.45 m lower (critic T2: p26 shows the basin above the lawn
  // with an exposed warm stone face, ~0.45 m derived). Platform covers the pool surround out to the far coping (z -2.14).
  {id:'pool-terrace', cat:'ground', mat:'terrace_stone', x0:2.86, x1:15.06, z0:0.0, z1:4.57, y0:-0.02, y1:0.002, status:_ps},
  {id:'pool-platform-beyond-plot', cat:'ground', mat:'pool_face', x0:3.40, x1:15.06, z0:-2.14, z1:0.0, y0:-0.47, y1:0.002, status:_ps+' (beyond site-diagram boundary, M30)'},
  // two wide steps from the terrace down to the rear lawn at the east end (critic T5; EXT-4b-POOL foreground, Blender F1 steps)
  {id:'pool-step-1', cat:'ground', mat:'terrace_stone', x0:12.40, x1:15.06, z0:-2.49, z1:-2.14, y0:-0.47, y1:-0.15, status:_ps},
  {id:'pool-step-2', cat:'ground', mat:'terrace_stone', x0:12.40, x1:15.06, z0:-2.84, z1:-2.49, y0:-0.47, y1:-0.30, status:_ps}
);
for (const b of _O.add) if (b.id === 'context-lawn-rear') { b.y0 = -0.50; b.y1 = -0.45; }   // rear lawn at grade, 0.45 m below the terrace
// pool-platform top is the coping band on the far side; its z -2.14 face is the exposed basin face
