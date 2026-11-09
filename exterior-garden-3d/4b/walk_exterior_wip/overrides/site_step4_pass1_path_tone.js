// Site/aerial view, step 4 finish pass 1 (critic close of step 3 on b375162): warmer path tone.
// Reference path (OUTDOOR-SITE, low warm sun) samples ~RGB 105-150, 92-110, 75-87: warm beige-brown. The model's paving_inner slabs
// render neutral ~RGB 177-218, 176-214, 172-205 (grey-white). Slabs switched to the page's warm beige material 'curtain'
// (0xbea894, slight warm emissive); joint bed unchanged. Material choice: assumption to match the sampled hue. This view only.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  for (const b of window.MODEL_OVERRIDES.add) if (/^site-entry-slab-/.test(b.id)) {
    b.mat = 'curtain'; b.status += '; site_step4_pass1_warm_tone';
  }
})();
