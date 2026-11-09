#!/usr/bin/env python3
"""Build index_r3.html = index.html + F2 (entry travertine) + Q7 (courtyard_feature_r2 wired in) + F3 (olive, no bench, pool Water2).

index.html is NOT edited (lane 3 rule: new files only until the critic passes the change).
Each patch is an exact, anchored string replacement; the build fails if any anchor is missing or not unique,
so a later change to index.html cannot silently drop a fix. Output written to a temp file, then moved.
Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
Usage: python3 build_r3/build_index_r3.py   (from FP-4B-GF/)
"""
import hashlib, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC, OUT = os.path.join(ROOT, 'index.html'), os.path.join(ROOT, 'index_r3.html')

BLOCKS = [   # (name, start anchor, end anchor, replacement): replaces start..end inclusive; each anchor must be unique
 ('F3 remove lite + flat water paths', "    if (!mesh && mode === 'lite'){\n",
  "opacity:.8})); }\n",
  "    if (!mesh){ waterState.error = waterState.error || 'Water2 unavailable'; console.error('Water2 failed for ' + w.id + ': ' + waterState.error + ' (no fallback water by design, F3)'); return; }   // F3: no lite / flat fallback\n"),
 ('F3 badge', "  if (fb) fb.textContent = waterState.count ? (waterState.mode === 'flat'", "'Water: none in source';\n",
  "  if (fb) fb.textContent = waterState.error ? 'Water: Water2 FAILED (' + waterState.error + '), no fallback water shown' : 'Water: three.js Water2 (r160, vendored), ' + WATER2_RES + ' px targets, passes on camera move' + (court ? ' + courtyard Water2' : '') + ' · ' + waterState.count + ' plan surface(s)';\n"),
]

PATCHES = [
 ('imports', "import {Water} from 'three/addons/objects/Water2.js';   // three.js r160 Water2 (MIT), vendored locally\n",
  "import {Water} from 'three/addons/objects/Water2.js';   // three.js r160 Water2 (MIT), vendored locally\n"
  "// r3 build (build_r3/build_index_r3.py): F2 entry travertine + Q7 courtyard. REVIEW-PENDING, not critic-passed.\n"
  "import {texEntryTravertine, ENTRY_TRAV_REPEAT_M} from './f2_entry_travertine.js';\n"
  "import {wireCourtyard} from './q7_courtyard_wire.js';\n"
  "import {WATER2_RES, WATER_PERF, throttleWater} from './f3_water_perf.js';\n"
  "import {calacattaWallParams, CAL_REPEAT_M} from './f3_calacatta_wall.js';\n"
  "import {buildDressWardrobe} from './f3_dress_wardrobe.js';\n"
  "const R3Q = new URLSearchParams(location.search), Q7_ON = R3Q.get('q7') !== '0';\n"
  "let court = null;\n"),
 ('F2 material', "    trav: smat({map:texTravertine(), roughness:.62}, .3),\n",
  "    trav: smat({map:texTravertine(), roughness:.62}, .3),\n"
  "    travEntry: smat({map:texEntryTravertine(THREE, renderer ? Math.min(8, renderer.capabilities.getMaxAnisotropy()) : 4), roughness:.6}, .25),   // F2\n"
  "    calWall: smat(calacattaWallParams(THREE, renderer ? Math.min(8, renderer.capabilities.getMaxAnisotropy()) : 4), .7),   // F3 G2: p24 / p15 Calacatta feature wall (ambientCG Marble012, CC0)\n"),
 ('F3 living Calacatta wall', "  clad(14137, 1650, 14159, 5250, .09, top, S0.cal, 1.6, 1.6);\n  clad(14141, 1013, 14159, 1650, .09, top, S0.oak, .6, 2.4); clad(14141, 5250, 14159, 5987, .09, top, S0.oak, .6, 2.4);\n",
  "  clad(14137, 1013, 14159, 5987, .09, top, S0.calWall, ...CAL_REPEAT_M);   // F3 G2: Calacatta across the whole living east wall (p24 Feature Wall: Calacatta marble; p15 living); oak flanks removed\n"),
 ('F2 entry clad', "  clad(6040, 16113, 6060, 19169, .09, top, S0.trav, 1.2, .6);\n",
  "  clad(6040, 16113, 6060, 19169, .09, top, S0.travEntry, ...ENTRY_TRAV_REPEAT_M);   // F2: entry wall uses the streak-free texture\n"),
 ('F2 void lining UV', "if (m.map) planeUV(g, pw, ph, m === S0.trav ? 1.2 : 1, m === S0.trav ? .6 : 1);",
  "if (m.map) planeUV(g, pw, ph, m === S0.travEntry ? ENTRY_TRAV_REPEAT_M[0] : m === S0.trav ? 1.2 : 1, m === S0.travEntry ? ENTRY_TRAV_REPEAT_M[1] : m === S0.trav ? .6 : 1);"),
 ('F2 void lining mat', "      const m = trav ? S0.trav : S0.paint;\n",
  "      const m = trav ? S0.travEntry : S0.paint;   // F2\n"),
 ('Q7 skip interim pond', "    const B = /pool/i.test(w.id) ? BASIN.pool : BASIN.pond;\n    buildBasin(w, B);\n",
  "    if (Q7_ON && !/pool/i.test(w.id)) return;   // Q7: courtyard pond comes from courtyard_feature_r2.js\n"
  "    const B = /pool/i.test(w.id) ? BASIN.pool : BASIN.pond;\n    buildBasin(w, B);\n"),
 ('Q7 skip interim olive', "  (PLAN.WATER || []).forEach(w => (w.holes || []).forEach(h => {\n    const cx = h.reduce(",
  "  if (!Q7_ON) (PLAN.WATER || []).forEach(w => (w.holes || []).forEach(h => {   // Q7: replaced by the r2 pine\n    const cx = h.reduce("),
 ('Q7 add to scene', "  scene.add(archFloor, archUp, furnG, labelG, lampG, decorG);\n",
  "  scene.add(archFloor, archUp, furnG, labelG, lampG, decorG);\n"
  "  if (Q7_ON){ try { court = wireCourtyard(THREE, {PLAN, wx, wz, renderer}); scene.add(court.group); } catch(e){ console.error('Q7 courtyard failed:', e); court = null; } }\n"),
 ('Q7 per-frame', "  for (let i = 0; i < animTex.length; i++){ animTex[i].offset.set(now*1.6e-5*(i + 1), now*0.9e-5); }   // pool caustics drift\n",
  "  for (let i = 0; i < animTex.length; i++){ animTex[i].offset.set(now*1.6e-5*(i + 1), now*0.9e-5); }   // pool caustics drift\n"
  "  if (court) court.update(dt, now/1000);   // Q7 tree sway (<= 0.25 deg)\n"),
 ('QA hook', "window.__FP3D_QA__ = {\n",
  "window.__FP3D_QA__ = {\n  r3: () => ({build:'r3', f2:true, q7:Q7_ON, f3:true, water:waterState, water2_res:WATER2_RES, court:court ? court.meta : null}),\n"
  "  waterPerf(force){ if (force !== undefined) WATER_PERF.force = !!force; return {force:WATER_PERF.force, refreshMs:WATER_PERF.refreshMs, ...WATER_PERF.stats}; },\n"),
 ('banner', "Ashwood 4B GF · Floorplan 3D SPIKE (MIT viewer) · approx ±3% ·",
  "Ashwood 4B GF · r3 build (F2 + Q7, REVIEW-PENDING) · concept visualisation · approx ±3% ·"),
 ('F3 water comment', "Default is now 'lite': a transparent, normal-mapped, env-reflective surface", "[r3 build, F3: the lite and flat water paths are REMOVED; Water2 only, passes throttled by f3_water_perf.js]"),
 ('F3 water comment 2', "?water=water2 restores Water2, ?water=flat the flat fallback.", "(original index.html notes; no ?water option in r3)"),
 ('F3 G4 dress wardrobe', "  state.furniture.forEach(f => furnG.add(buildFurniture(f)));\n",
  "  state.furniture.forEach(f => furnG.add(/^Dress wardrobe$/.test(f.name || '') ? buildDressWardrobe(THREE, wx, wz) : buildFurniture(f)));   // F3 G4: glass-front wardrobe on the V4 joinery block\n"),
 ('F3 Water2 only', "const WATER_Q = new URLSearchParams(location.search).get('water'), WATER_MODE = WATER_Q === 'flat' ? 'flat' : WATER_Q === 'water2' ? 'water2' : 'lite';",
  "const WATER_MODE = 'water2';   // F3 (Colin 2026-11-10): full Water2 only for pool and courtyard; no lite / flat water path, no ?water option"),
 ('F3 Water2 res', "textureWidth:D.textureWidth, textureHeight:D.textureHeight,", "textureWidth:WATER2_RES, textureHeight:WATER2_RES,"),
 ('F3 pool reflectivity', "const BASIN = {pool:{depth:1.4, tile:true, coping:.3, waterY:-.06, color:0xd8f4f6, scale:2.2, reflect:.04},",
  "const BASIN = {pool:{depth:1.4, tile:true, coping:.3, waterY:-.06, color:0xd8f4f6, scale:2.2, reflect:.2},   // F3: reflect .04 -> .2 (display assumption) so Water2 reflections read"),
 ('F3 throttle pool', "mesh.rotation.x = -Math.PI/2; mesh.position.y = B.waterY; mesh.userData.water = w.id; mesh.userData.waterMode = mode;",
  "mesh.rotation.x = -Math.PI/2; mesh.position.y = B.waterY; mesh.userData.water = w.id; mesh.userData.waterMode = mode; if (mode === 'water2') throttleWater(mesh, {flowSpeed:.02});   // F3"),
]

def main():
    src = open(SRC, encoding='utf-8').read(); out = src
    for name, a, b in PATCHES:
        n = out.count(a)
        if n != 1: sys.exit(f'build_r3: anchor "{name}" found {n}x (need exactly 1). index.html changed? Not writing output.')
        out = out.replace(a, b)
    for name, a, e, b in BLOCKS:
        if out.count(a) != 1: sys.exit(f'build_r3: block start "{name}" found {out.count(a)}x (need 1). Not writing output.')
        i = out.index(a); j = out.find(e, i)
        if j < 0 or j - i > 4000: sys.exit(f'build_r3: block end "{name}" not found near start. Not writing output.')
        out = out[:i] + b + out[j + len(e):]
    head = ('<!-- GENERATED by build_r3/build_index_r3.py from index.html sha256 %s (sha256sum of the file bytes). Do not hand-edit. '
            'Concept visualisation, not survey-verified, not construction-ready, not certified CAD. -->\n') % hashlib.sha256(open(SRC, 'rb').read()).hexdigest()
    i = out.find('>') + 1 if out[:15].lower().startswith('<!doctype') else 0
    out = out[:i] + ('\n' if i else '') + head + out[i:]
    fd, tmp = tempfile.mkstemp(dir=ROOT, suffix='.tmp'); os.write(fd, out.encode('utf-8')); os.close(fd); os.replace(tmp, OUT)
    print(f'build_r3: {len(PATCHES)} patches + {len(BLOCKS)} blocks applied -> {os.path.relpath(OUT, ROOT)} ({len(out)} bytes)')
main()
