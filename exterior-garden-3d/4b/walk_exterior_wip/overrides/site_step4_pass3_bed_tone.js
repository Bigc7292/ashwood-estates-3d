// Site/aerial view, step 4 finish pass 3 (critic on 4ce757d): darker shaded bed tones.
// Reference front beds (OUTDOOR-SITE) sample ~RGB 30-46, 25-38, 8-16 (near-black olive in shade); the model's beds rendered ~RGB 44, 56, 17
// and brighter on the sunlit rows. Bed rows site-bed-* recoloured darker and warmer; shapes and positions unchanged. Hex checked after
// render. This view only. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const tones = {'site-bed-left':0x3a3418, 'site-bed-right-path':0x3e381a, 'site-bed-right-back':0x3a3418, 'site-bed-right-front':0x423c1c};
  for (const r of (window.MODEL_OVERRIDES.shrubRows || [])) if (tones[r.id] !== undefined) { r.color = tones[r.id]; r.status += '; site_step4_pass3_shaded_tone'; }
})();
