// Right view, step 4 finish pass 3 (critic on acf9b31): gate darkened to the reference's shaded tone.
// Finding: pass 11's slat material door_timber is only defined in this page when glass_mode === 'interior', so the slats fell back to the
// grey placeholder. Slats now use drive (0x8f8578, warm grey-brown, renders ~RGB 95-105, 85-90, 75-80 in this light) on the dark backing;
// bronze_dark (0x3a2c20) was tried first and read solid black. Reference gate: slats ~RGB 80-100, 66-80, 57-66 with gaps ~RGB 28-40, 16-29, 10-25. Backing and frame unchanged. Steps unchanged. This view only.
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  for (const b of window.MODEL_OVERRIDES.add) if (/^right-gate-slat-/.test(b.id)) {
    b.mat = 'drive'; b.status += '; right_step4_pass3_shaded_tone';
  }
})();
