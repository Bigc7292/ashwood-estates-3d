// Rear + garden step 6 pass 3 (lane 2 self-critique): "pool reads as flat blue paint".
// POOL / ELEV-REAR show a glassy turquoise surface that reflects the house and sky with small ripples.
// three.js Water2 (examples/jsm/objects/Water2.js, r160, MIT, vendored under ../model/vendor) on the CAD pool outline (9.49 x 2.38 m CAD; 9.50 x 2.40 m brochure).
// Tuning only (display assumptions): stronger reflectivity, finer ripple scale, slightly faster flow. Pool size/position unchanged.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.water2 = {reflectivity: 0.32, scale: 1.1, flowSpeed: 0.035};
