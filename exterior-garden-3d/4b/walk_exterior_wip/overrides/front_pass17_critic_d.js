// Front view, step 6 loop 2, pass 17: critic (d) (critic report production-line/critic/2026-11-10_exterior-front-step6.md, defects 2, 3, 4, 7).
// (2) FF screen: dark bronze (#3a2c20) slats at UNEVEN spacing with horizontal rails at uneven heights (irregular grid), lit glass behind
//     (CAD ff-glass-front-c at z 24.46 + pass 8 lit rooms). Extent unchanged from pass 5 (x 5.4-11.04, FF 4.0-7.4). Spacing pattern is image-read.
// (3) The stone parapet band across the FF front-right (ff-parapet-front-r, status 'render_p25_observed...') is removed; a 1.1 m glass rail
//     (brochure height NOT FOUND: assumption) with a slim bronze cap runs along the CAD balcony edge.
// (4) Right FF stone box: CAD check done first. The approved V4 FF plan traces a front-right BALCONY ff-balcony-front-r x 11.038-15.779,
//     z 24.021-26.848 (a real projection in front of the FF glass), but draws no enclosed volume. So the box is kept INSIDE that CAD balcony
//     rectangle (right part, x 12.90-15.38, against the tower) at the model's parapet height 1.1 m with a planter on top; the image reads a taller
//     travertine cube -> mismatch M32 (image look vs CAD open balcony), geometry not invented beyond the CAD footprint.
// (7) Dusk: window.MODEL_OVERRIDES.dusk -> low warm sun, warmer sky, stronger soffit/carport/lobby emissives (front_pass.html).
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
(function(){
  const O = window.MODEL_OVERRIDES; if (!O) return;
  O.add = O.add.filter(b => !b.id.startsWith('ff-slat-'));
  O.remove.push('ff-parapet-front-r');
  const X0 = 5.4, X1 = 11.04, Y0 = 4.0, Y1 = 7.4, Z0 = 24.68, Z1 = 24.76;
  const gaps = [0.07, 0.12, 0.07, 0.07, 0.17, 0.09, 0.07, 0.13, 0.08, 0.07, 0.21, 0.08, 0.11];   // irregular rhythm (image-read)
  let x = X0, i = 0;
  while (x + 0.05 <= X1) { const w = (i % 5 === 2) ? 0.08 : 0.04;
    O.add.push({id:'ff-grid-v-'+i, cat:'slats', mat:'bronze_dark', x0:x, x1:Math.min(x+w, X1), z0:Z0, z1:Z1, y0:Y0, y1:Y1, status:'pass17_image_read_irregular_grid'});
    x += w + gaps[i % gaps.length]; i++; }
  [[Y0, 0.08], [4.95, 0.05], [5.62, 0.07], [6.48, 0.05], [Y1-0.08, 0.08]].forEach(([y, h], k) =>
    O.add.push({id:'ff-grid-h-'+k, cat:'slats', mat:'bronze_dark', x0:X0, x1:X1, z0:Z0-0.04, z1:Z1, y0:y, y1:y+h, status:'pass17_image_read_irregular_grid'}));
  // (3) glass rail on the CAD front-right balcony edge, left of the stone box
  O.add.push({id:'ff-rail-glass-front-r', cat:'ff_glass', mat:'glass', x0:11.038, x1:12.90, z0:26.78, z1:26.81, y0:4.0, y1:5.1, status:'pass17: 1.1 m glass rail (height assumption, brochure NOT FOUND)'},
             {id:'ff-rail-cap-front-r', cat:'slats', mat:'bronze_dark', x0:11.038, x1:12.90, z0:26.77, z1:26.82, y0:5.07, y1:5.11, status:'pass17 assumption'},
             {id:'ff-rail-glass-side-r', cat:'ff_glass', mat:'glass', x0:11.038, x1:11.068, z0:24.021, z1:26.78, y0:4.0, y1:5.1, status:'pass17 assumption'});
  // (4) stone box inside the CAD balcony rectangle (M32)
  O.add.push({id:'ff-stone-box-front-r', cat:'parapet', mat:'stone', x0:12.90, x1:15.38, z0:26.50, z1:26.848, y0:4.0, y1:5.1, status:'pass17: inside CAD ff-balcony-front-r; height = model parapet 1.1 m; image reads taller (M32)'},
             {id:'ff-stone-box-side', cat:'parapet', mat:'stone', x0:12.90, x1:13.20, z0:24.021, z1:26.50, y0:4.0, y1:5.1, status:'pass17: inside CAD balcony (M32)'});
  O.dusk = true;
})();
