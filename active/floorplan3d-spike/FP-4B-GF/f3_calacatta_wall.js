/* f3_calacatta_wall.js - F3 (critic G2): living feature (media) wall in Calacatta marble.
 * Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
 * Evidence: brochure p24 "Interior (Summary)": "Walls: Textured Paint / Feature Wall: Calacatta marble"  [source: p24 text]
 *           brochure p15 living render (canonical/references/ref-p15-living.png): white, grey-veined marble media wall with TV  [source: p15 image]
 * Texture: ambientCG Marble012 (CC0 1.0), levels brightened toward Calacatta white; see assets/credits.csv  [free asset, credited]
 * Slab repeat 1.6 x 1.6 m (assumption). Polished: effective roughness ~0.16 (assumption). Wall extent = the existing living east wall
 * span in index.html (x 14137-14159, y 1013-5987, from the V4 trace); the oak-veneer flanks are replaced (p15 shows marble across).
 */
export const CAL_REPEAT_M = [1.6, 1.6];
export function calacattaWallParams(THREE, anisotropy = 8){
  const tl = new THREE.TextureLoader(), u = n => new URL('./assets/ambientcg/Marble012/' + n, import.meta.url).href;
  const map = tl.load(u('Marble012_2K_Color_calacatta-levels.jpg')), rough = tl.load(u('Marble012_1K_Roughness.jpg'));
  [map, rough].forEach(t => { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = anisotropy; });
  map.colorSpace = THREE.SRGBColorSpace;
  return {map, roughnessMap:rough, roughness:2.5, color:'#ffffff'};   // map mean ~0.066 -> effective ~0.16 (polished, assumption)
}
