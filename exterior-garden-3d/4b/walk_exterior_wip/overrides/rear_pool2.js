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
// critic pool review T8 (2026-11-10): the V4 GF plan draws 2 loungers and a side table on the TERRACE at the pool's east end (x ~13-15.8 m).
// Placed on the east-end terrace at the plan x; z moved with the pool (Colin override M29/M30). Sizes are assumptions (lounger 0.70 x 2.00 m).
_O.add.push(
  {id:'lounger-1',      cat:'furniture', mat:'lounger', x0:13.05, x1:13.75, z0:1.60, z1:3.60, y0:0.0, y1:0.32, status:'CAD V4 GF terrace symbol (illustrative), z moved with pool'},
  {id:'lounger-1-back', cat:'furniture', mat:'lounger', x0:13.05, x1:13.75, z0:1.60, z1:2.10, y0:0.32, y1:0.62, status:'CAD symbol, back rest assumption'},
  {id:'lounger-2',      cat:'furniture', mat:'lounger', x0:14.30, x1:15.00, z0:1.60, z1:3.60, y0:0.0, y1:0.32, status:'CAD V4 GF terrace symbol (illustrative), z moved with pool'},
  {id:'lounger-2-back', cat:'furniture', mat:'lounger', x0:14.30, x1:15.00, z0:1.60, z1:2.10, y0:0.32, y1:0.62, status:'CAD symbol, back rest assumption'},
  {id:'side-table',     cat:'furniture', mat:'bronze_dark', x0:13.85, x1:14.20, z0:2.00, z1:2.35, y0:0.0, y1:0.45, status:'CAD V4 GF terrace symbol (illustrative)'}
);
// critic T9: denser surroundings beyond the rear boundary (tree/hedge belt standing in for neighbouring gardens); image-read, off-plot context
_O.shrubRows = (_O.shrubRows || []).concat([
  {id:'context-tree-belt', x0:-6, z0:-16, x1:24, z1:-16, h:4.5, r:1.3, color:0x3f5f2a, status:'off-plot context (critic T9)'},
  {id:'context-hedge-rear', x0:-4, z0:-12, x1:22, z1:-12, h:1.6, r:0.5, color:0x46662e, flowers:0xc8407e, status:'off-plot context (critic T9)'}
]);
