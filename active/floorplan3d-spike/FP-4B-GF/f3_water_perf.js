/* f3_water_perf.js - F3: keep three.js Water2 (vendored r160) fast in the GF viewer.
 * Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
 * 1. Full-quality targets: WATER2_RES = 1024 px for pool and courtyard (Colin 2026-11-10: top-quality Water2, no lower resolution;
 *    1024 = courtyard_feature_r2.js default and above the old PLAN.DISPLAY 512).
 * 2. Render the reflection + refraction passes only when the water is in view AND (the camera moved, or a refresh is due):
 *    - in view: Water2's onBeforeRender only fires when the mesh passes three.js frustum culling, so off-screen water costs nothing;
 *    - camera unchanged: the passes are skipped and the last targets are reused; flow (normal-map scroll) keeps animating,
 *      because the flow offset is driven here from our own clock and written to the shader every frame;
 *    - refresh: every WATER_PERF.refreshMs while still, so door / sway / sun changes still reach the reflections (assumption).
 * WATER_PERF.force = true renders the passes every frame (used by the QA bench to measure the "camera moving" cost).
 */
export const WATER2_RES = 1024;
export const WATER_PERF = {force:false, refreshMs:1000, stats:{passes:0, skipped:0}};
export function throttleWater(water, {flowSpeed = .03} = {}){
  const orig = water.onBeforeRender, cfg = water.material.uniforms.config.value, half = cfg.z, cycle = 2*half;
  const lastM = new Float32Array(16), lastP = new Float32Array(16); let last = -1e9, tPrev = performance.now(), off = 0, primed = false;
  const same = (a, m) => { for (let i = 0; i < 16; i++) if (Math.abs(a[i] - m[i]) > 1e-6) return false; return true; };
  water.onBeforeRender = function(renderer, scene, camera){
    const now = performance.now(), dt = Math.min(1, (now - tPrev)/1000); tPrev = now;
    off = (off + flowSpeed*dt) % cycle;
    const moved = !primed || !same(lastM, camera.matrixWorld.elements) || !same(lastP, camera.projectionMatrix.elements);
    if (WATER_PERF.force || moved || now - last > WATER_PERF.refreshMs){
      orig.call(this, renderer, scene, camera); lastM.set(camera.matrixWorld.elements); lastP.set(camera.projectionMatrix.elements); last = now; primed = true; WATER_PERF.stats.passes++;
    } else WATER_PERF.stats.skipped++;
    cfg.x = off; cfg.y = (off + half) % cycle;   // own flow clock (continuous whether or not the passes ran)
  };
  water.userData.throttled = true; return water;
}
