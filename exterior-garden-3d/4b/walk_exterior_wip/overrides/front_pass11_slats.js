// Front view, step 6 loop 2, single fix (critic on 8aba267): first-floor slat screen tone and openness.
// ELEV-FRONT: the screen reads as warm lit timber with interior light between the slats; the model's two staggered dark
// layers closed the gaps. This keeps the front layer (pitch 0.13 m, 0.045 m slats, extent unchanged from pass 5), recolours it
// to warm timber, and drops the staggered back layer so the lit rooms (pass 8) show through. Rails stay dark bronze.
// Tone and spacing are image-read display assumptions. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const O = window.MODEL_OVERRIDES; if (!O) return;
  O.add = O.add.filter(b => !b.id.startsWith('ff-slat-1-'));
  for (const b of O.add) if (b.id.startsWith('ff-slat-0-')) { b.mat = 'slat_timber'; b.status = 'pass11_image_read_tone_assumption'; }
})();
