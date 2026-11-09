// Right view, step 3 blockout pass 6 (critic on bb544f1): entrance recess on the reference columns.
// The model's FF right facade has its glazed gap at z 12.68-16.90 (CAD gap between ff-wall-32 and ff-wall-72; panel x ~384-501 at the
// locked camera, 0.0361 m/px on the facade line, d 26.75 m). ELEV-RIGHT draws the tall glazed entry ~65 px further left (panel x ~320-415),
// i.e. 65 * 0.0361 = 2.35 m toward the street (derived). Same size kept (4.22 m): opening z 15.03-19.25.
// CAD wall LINES are kept (x 15.47-15.81); only which part of the line reads as stone vs glass changes, in this view only, the same way the
// left view's FF openings were handled (M35). Logged as M39. ff-glass-right (z 4.67-24.02) already sits behind the whole line.
//   - stone skin over the old gap's rear part: z 12.675-15.03
//   - ff-wall-72 (z 17.24-26.883) replaced by z 19.25-26.883 so the opening runs to 19.25
//   - ff-wall-70 (cross wall stub x 14.90-15.81, z 16.90-17.24) hidden here; it would read as a stone mullion mid-opening
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.remove.push('ff-wall-72', 'ff-wall-70');
window.MODEL_OVERRIDES.add.push(
  {id:'right-ff-skin-rear', cat:'ff_wall', mat:'stone', x0:15.474, x1:15.812, z0:12.675, z1:15.03, y0:4, y1:7.4, status:'right_pass6_recess_shift_derived_M39'},
  {id:'right-ff-wall-72-cut', cat:'ff_wall', mat:'stone', x0:15.474, x1:15.812, z0:19.25, z1:26.883, y0:4, y1:7.4, status:'right_pass6_recess_shift_derived_M39'}
);
