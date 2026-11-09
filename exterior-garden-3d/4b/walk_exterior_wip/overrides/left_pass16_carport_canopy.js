// Left view, step 4 pass 16 (critic on f54126e): carport canopy colour.
// The model's carport canopy and post are grey placeholders; ELEV-LEFT shows the canopy in the same cream stone as the roof and balcony slabs.
// Recoloured in memory, this view only, to the 'soffit' material the slabs use. Size and position unchanged (model data untouched).
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  for (const b of (window.MODEL.boxes || [])) if (b.id === 'carport-canopy' || b.id === 'carport-canopy-post') {
    b.mat = 'soffit'; b.status = (b.status || '') + '; left_pass16_colour_soffit';
  }
})();
