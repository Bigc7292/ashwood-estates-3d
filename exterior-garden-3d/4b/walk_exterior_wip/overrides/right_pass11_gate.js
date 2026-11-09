// Right view, step 3 blockout pass 11 (critic on 7d090cb): vertical-slatted gate in the boundary wall, left of the entry.
// ELEV-RIGHT: slatted gate at side-by-side x ~30-130 (panel), rows ~425-505, its top ~12 px below the wall top (wall ~95 px tall there).
// On the wall's outer face (x 18.97, d 23.63 m, 0.03185 m/px): z = 13.45 + (480 - col) * 0.03185 -> gate z 24.60-27.78 (derived).
// Gate height 1.57 m (= 1.8 m * (1 - 12/95), derived from the reference ratio); rows follow the CAD-line wall, so they carry the M37 drift.
// Slats 0.08 m wide at 0.14 m pitch (assumption), door_timber (reference gate samples ~RGB 30-100, warm dark brown), on a dark backing set 0.05 m behind. This view only, logged as M41.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const O = window.MODEL_OVERRIDES, G0 = 24.60, G1 = 27.78, H = 1.57, st = 'right_pass11_gate_derived_M41';
  const split = [];
  O.add = O.add.filter(b => {
    if (b.id === 'right-boundary-stone-b' || b.id === 'right-boundary-cap-b') {
      split.push(Object.assign({}, b, {id: b.id + '1', z1: G0, status: b.status + '; right_pass11_gate_M41'}));
      split.push(Object.assign({}, b, {id: b.id + '2', z0: G1, status: b.status + '; right_pass11_gate_M41'}));
      return false;
    }
    return true;
  });
  O.add.push(...split);
  O.add.push({id:'right-gate-backing', cat:'boundary', mat:'window_dark', x0:18.76, x1:18.80, z0:G0, z1:G1, y0:0, y1:H, status:st});
  let i = 0;
  for (let z = G0 + 0.03; z + 0.08 <= G1 - 0.02; z += 0.14, i++)
    O.add.push({id:'right-gate-slat-' + i, cat:'boundary', mat:'door_timber', x0:18.85, x1:18.92, z0:z, z1:z + 0.08, y0:0, y1:H, status:st});
  O.add.push({id:'right-gate-frame', cat:'boundary', mat:'bronze_dark', x0:18.83, x1:18.94, z0:G0, z1:G1, y0:H - 0.05, y1:H, status:st});
})();
