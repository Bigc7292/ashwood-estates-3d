// Right view, step 3 blockout pass 9 (critic on 54af843): entry opening in the boundary wall, with steps in front of it.
// ELEV-RIGHT sees the lit GF entry through a gap in the boundary wall at side-by-side x ~320-410, steps at rows ~460-515 standing on the
// ground in front of the wall line. On the wall's outer face (x 18.97, d 23.63 m, 0.03185 m/px): z = 13.45 + (480 - col) * 0.03185
// -> opening z 15.68-18.55 (derived). The opening follows the reference COLUMNS, not its wall height: the wall keeps the CAD line and the
// 1.8 m height, so its top stays ~37 px above the reference's (M37). Steps: 4 risers of 0.15 m (assumption) on the verge paving in front of
// the wall, landing at 0.60 m through the opening; rows cannot match the reference exactly because of the M37 ground-row drift.
// This view only, logged as M40. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const O = window.MODEL_OVERRIDES, Z0 = 15.68, Z1 = 18.55;
  const split = [];
  O.add = O.add.filter(b => {
    if (b.id === 'right-boundary-stone' || b.id === 'right-boundary-cap') {
      split.push(Object.assign({}, b, {id: b.id + '-a', z1: Z0, status: b.status + '; right_pass9_entry_opening_M40'}));
      split.push(Object.assign({}, b, {id: b.id + '-b', z0: Z1, status: b.status + '; right_pass9_entry_opening_M40'}));
      return false;
    }
    return true;
  });
  O.add.push(...split);
  const st = 'right_pass9_entry_steps_assumption_M40';
  O.add.push(
    {id:'right-entry-step-1',  cat:'ground', mat:'paving', x0:20.05, x1:20.40, z0:Z0, z1:Z1, y0:0, y1:0.15, status:st},
    {id:'right-entry-step-2',  cat:'ground', mat:'paving', x0:19.70, x1:20.05, z0:Z0, z1:Z1, y0:0, y1:0.30, status:st},
    {id:'right-entry-step-3',  cat:'ground', mat:'paving', x0:19.35, x1:19.70, z0:Z0, z1:Z1, y0:0, y1:0.45, status:st},
    {id:'right-entry-landing', cat:'ground', mat:'paving', x0:18.20, x1:19.35, z0:Z0, z1:Z1, y0:0, y1:0.60, status:st}
  );
})();
