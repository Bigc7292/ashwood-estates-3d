// Left view, step 4 pass 17 (critic on 9d4842f): thin dark frames around the three FF windows (ELEV-LEFT shows dark frame edges).
// 0.05 m flat dark bronze jambs and sill on each opening, at the openings' existing size and position (pass 11 already has the head bar).
// Curtain panels unchanged. Display assumption. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const O = window.MODEL_OVERRIDES; if (!O) return; const F = 0.05, A = 'left_pass17_frame_assumption', extra = [];
  for (const w of O.add) if (/^l11-window-/.test(w.id)) {
    const n = w.id.slice(-1), base = {cat:'ff_frame', mat:'bronze_dark', x0:2.86, x1:2.93, status:A};
    extra.push(Object.assign({id:'l17-jamb-a-' + n, z0:w.z0,     z1:w.z0 + F, y0:w.y0, y1:w.y1}, base));
    extra.push(Object.assign({id:'l17-jamb-b-' + n, z0:w.z1 - F, z1:w.z1,     y0:w.y0, y1:w.y1}, base));
    extra.push(Object.assign({id:'l17-sill-' + n,   z0:w.z0,     z1:w.z1,     y0:w.y0, y1:w.y0 + F}, base));
  }
  O.add.push(...extra);
})();
