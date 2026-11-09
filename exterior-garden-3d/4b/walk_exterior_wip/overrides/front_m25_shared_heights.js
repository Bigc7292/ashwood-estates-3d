// M25 height set (per Archivist (integrator), stated as delegated by Colin, 2026-11-10; reversible).
// One shared set of heights across every view: front tower top 11.6 m (M2 value; the instruction calls it CAD) and the model's FF level
// (FF 4.0-7.4 m, roof slab 7.4-7.85 m, model.js). Replaces pass 14 (9.73 m tower) and pass 15 (+0.50 m FF raise), whose scripts are no longer
// loaded. Image-read 10.1 m (pass 2) and 9.73 m (pass 14) are REJECTED. Where ELEV-FRONT's silhouette now disagrees, it is logged (M25), not bent.
(window.MODEL_OVERRIDES = window.MODEL_OVERRIDES || {remove:[], add:[]});
window.MODEL_OVERRIDES.add = window.MODEL_OVERRIDES.add.filter(b => !['stone-fin-pass2','stone-fin-cap','stone-fin-pass14','stone-fin-cap-pass14'].includes(b.id));
window.MODEL_OVERRIDES.add.push(
  {id:'stone-fin-m25', cat:'canopy', mat:'stone', x0:15.5, x1:16.0, z0:22.9, z1:26.9, y0:0.0, y1:11.52, status:'M25 shared height 11.6 m top (per Archivist, delegated by Colin, 2026-11-10; reversible)'},
  {id:'stone-fin-cap-m25', cat:'canopy', mat:'bronze_dark', x0:15.48, x1:16.02, z0:22.88, z1:26.92, y0:11.52, y1:11.6, status:'pass12 cap kept, moved to the 11.6 m top'}
);
