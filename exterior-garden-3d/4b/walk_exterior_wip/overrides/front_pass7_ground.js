// Front view, pass 7 (critic's order: ground relief after the hedge): pavement, kerb and street in front of the plot.
// Driveway under the carport: darker warm paving (image-read finish, CAD vehicle-entry zone per M1).
// Off-plot context (NOT PLOT): the site ends at z 29.88. Depths back-projected from ELEV-FRONT rows through the
// locked camera (assumptions): pavement to z 31.8, kerb 0.12 m high, asphalt beyond. Concept visualisation only.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.add.push(
  {id:'ctx-pavement', cat:'ground', mat:'paving', x0:-20, x1:40, z0:30.13, z1:31.8, y0:-0.05, y1:0.02, status:'pass7_context_not_plot_assumption'},
  {id:'ctx-kerb',     cat:'ground', mat:'kerb',   x0:-20, x1:40, z0:31.8,  z1:32.0, y0:-0.05, y1:0.12, status:'pass7_context_not_plot_assumption'},
  {id:'driveway-paving', cat:'ground', mat:'drive', x0:0.0, x1:7.39, z0:23.6, z1:29.88, y0:-0.04, y1:0.025, status:'pass7_image_read_finish_CAD_vehicle_zone_M1'},
  {id:'ctx-street',   cat:'ground', mat:'asphalt',x0:-20, x1:40, z0:32.0,  z1:60.0, y0:-0.06, y1:-0.02, status:'pass7_context_not_plot_assumption'}
);
