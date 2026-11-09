// Front v2 pass 3 (critic on 5c7fced): palm crowns as filled, fewer, wider fronds.
// Critic: fronds read as spiky wireframe; ELEV-FRONT's palms have soft, filled, warm-green drooping crowns. Read by front_v2.html's palm
// builder (palm_style hook): leaflets drawn densely and thick so each frond reads as a filled blade, warmer greens, slight emissive lift, and
// fewer, wider fronds in three rings. Trunk positions, heights and crown sizes unchanged (front pass 3). Appearance is image-read; display
// assumption. Based on the lane's parked pass 18 (never committed). Concept visualisation, not survey-verified, not construction-ready.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.palm_style = {
  leaf: {spacing:3, lineWidth:4.2, colours:['#6f8d3b','#7f9c46','#5f7e33'], midrib:'#55692c', reach:30},
  emissive: 0x1c2608,
  rings: [ {n:22, len:1.00, up:[1.0,1.25,1.5], droop:0.75, w:1.9},
           {n:10, len:0.78, up:[0.6,0.8,1.0], droop:0.45, w:1.6},
           {n:5,  len:0.50, up:[0.3,0.45,0.6], droop:0.2, w:1.1} ]
};
