#!/usr/bin/env python3
"""Headless offline verification of active/floorplan3d-spike/FP-4B-GF (SPIKE QA).
Serves the folder on 127.0.0.1, renders in headless Chrome (Playwright), blocks + logs every
non-localhost request, captures screenshots, and compares the 3D top view with the approved V4 walls."""
import base64, functools, http.server, io, json, socketserver, threading, time, sys, datetime
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as nd
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parents[1]
S = R / 'active/floorplan3d-spike/FP-4B-GF'
V = S / 'verify'; V.mkdir(exist_ok=True)
for _old in V.glob('*.png'): _old.unlink()
UP = Path('/workspace/floorplan-3d')
plan = json.loads((S / 'data/fp-4b-gf.plan.json').read_text())
P = plan['plan']; SS = 2
mask = np.array(Image.open(S / 'data/wall_mask_2x.png').convert('L')) < 128

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
import tempfile, shutil, re, hashlib
DEMO = Path(tempfile.mkdtemp(prefix='fp3d-upstream-demo-'))
# Untouched upstream demo, rendered locally: ONLY the importmap is pointed at the same vendored three r160 and a read-only
# camera/capture hook is appended (identical helpers to the spike). Demo data, furniture, materials, lighting unchanged.
_up = (UP / 'index.html').read_text()
_up = _up.replace('"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"', '"three":"./vendor/three/build/three.module.js"')
_up = _up.replace('"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"', '"three/addons/":"./vendor/three/examples/jsm/"')
_HOOK = '''window.__FP3D_QA__ = {
  settle(){ cancelAnimationFrame(raf); raf = 0; if (anim){ anim.fn(1); const r = anim.res; anim = null; r(); } fly = null; grow = 1; furnGrow = 1; applyGrow(); doors.forEach(d => { d.cur = d.open ? d.a1 : d.a0; d.pivot.rotation.y = d.cur; }); return true; },
  still(){ this.settle(); orbit.update(); renderer.render(scene, camera); return {png:renderer.domElement.toDataURL('image/png'), w:renderer.domElement.width, h:renderer.domElement.height}; },
  look(p, t, fovDeg = 55){ fly = null; camera.fov = fovDeg; camera.updateProjectionMatrix(); camera.up.set(0,1,0); camera.position.set(wx(p[0]), p[2], wz(p[1])); orbit.target.set(wx(t[0]), t[2], wz(t[1])); camera.lookAt(orbit.target); orbit.update(); return camera.position.toArray(); },
  setCut(c){ opt.cut = c; buildArch(); return opt.cut; },
  labels(v){ labelG.visible = v; labelG.children.forEach(o => { o.visible = v; o.element.style.display = v ? '' : 'none'; }); return v; },
  furniture: () => ({state:state.furniture.length, meshes:furnG.children.length}),
};
window.View3D = {enter, exit,'''
assert _up.count('window.View3D = {enter, exit,') == 1
_up = _up.replace('window.View3D = {enter, exit,', _HOOK)
assert 'cdn.jsdelivr' not in _up.split('<script type="importmap">')[1].split('</script>')[0]
(DEMO / 'index.html').write_text(_up); shutil.copytree(S / 'vendor', DEMO / 'vendor')
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=str(S)))
dsrv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=str(DEMO)))
DBASE = f'http://127.0.0.1:{dsrv.server_address[1]}/'; threading.Thread(target=dsrv.serve_forever, daemon=True).start()
port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{port}/'
requests, blocked, console = [], [], []

def guard(route):
    u = route.request.url; requests.append(u)
    if u.startswith(BASE) or u.startswith(DBASE) or u.startswith('data:') or u.startswith('blob:'):
        route.continue_()
    else:
        blocked.append(u); route.abort()

ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']
res = {'started_Asia_Dubai': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'base': BASE}

def save_png(data_url, path):
    Image.open(io.BytesIO(base64.b64decode(data_url.split(',', 1)[1]))).convert('RGB').save(path)

k_ = P['mm_per_crop_px']; ox_, oy_ = P['origin_crop_px']
def MM(x, y, h): return [round((x - ox_) * k_), round((y - oy_) * k_), h]   # crop px -> plan mm (+ height m)
LBL = 'Ashwood 4B GF - Floorplan 3D spike v2 - display-only heights/finishes/furniture models - approx +/-3% - NOT survey-verified - NOT construction-ready - NOT certified CAD'
# name, camera [x,y,h], target [x,y,h], fov, cut, caption
HERO = [
 ('v2_01_hero_living_dining_pool', MM(372, 328, 1.6), MM(320, 190, 1.0), 60, 3, 'Living / dining toward the pool (eye level 1.6 m)'),
 ('v2_02_hero_living_sofa_pool', MM(538, 322, 1.5), MM(380, 150, 0.9), 62, 3, 'Living: sectional sofa, coffee table, dining beyond, pool through glazing'),
 ('v2_03_hero_show_kitchen_island', MM(392, 300, 1.6), MM(255, 372, 0.9), 62, 3, 'Show kitchen: island + 3 stools, back counter'),
 ('v2_04_hero_kitchen', MM(234, 392, 1.6), MM(292, 505, 0.8), 68, 3, 'Kitchen: U counters, tall storage run (from pantry)'),
 ('v2_05_hero_entry_stair', MM(402, 706, 1.6), MM(338, 585, 1.4), 66, 3, 'Double-height entry toward the stair (display-only stair massing)'),
 ('v2_06_hero_maid_room', MM(262, 642, 1.6), MM(214, 706, 0.5), 72, 3, 'Maid room: bed + nightstand as drawn (bed length as traced)'),
 ('v2_07_hero_pool_terrace', MM(600, 70, 1.7), MM(330, 150, 0.2), 58, 3, 'Pool terrace: Water2 pool, terrace chairs, living glazing'),
 ('v2_08_birdseye_full_walls', MM(700, 960, 27), MM(372, 440, 0), 40, 3, "Bird's-eye oblique, full-height walls (3.0 m display-only)"),
 ('v2_09_birdseye_cut_walls', MM(700, 960, 27), MM(372, 440, 0), 40, 1.2, "Bird's-eye oblique, cut walls (1.2 m)"),
]
# upstream demo apartment (plan mm of the upstream data), same lens/heights
DEMO_SHOTS = [
 ('demo_01_living', [9900, 10250, 1.6], [6000, 7300, 0.9], 60, 2.8, 'UPSTREAM DEMO (untouched data) - living, eye level'),
 ('demo_02_bedroom', [9950, 3150, 1.6], [7400, 700, 0.5], 72, 2.8, 'UPSTREAM DEMO - master bedroom'),
 ('demo_03_kitchen', [2050, 7800, 1.6], [500, 5600, 0.8], 68, 2.8, 'UPSTREAM DEMO - kitchen'),
 ('demo_08_birdseye_full_walls', [5900 + 7600, 5300 + 12500, 21], [5900, 5300, 0], 40, 2.8, 'UPSTREAM DEMO - bird\'s-eye, full walls'),
 ('demo_09_birdseye_cut_walls', [5900 + 7600, 5300 + 12500, 21], [5900, 5300, 0], 40, 1.2, 'UPSTREAM DEMO - bird\'s-eye, cut walls'),
]
try: FNT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20); FNTs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
except Exception: FNT = FNTs = None
def caption(im, title, label):
    im = im.convert('RGBA'); ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rectangle([0, 0, im.width, 34], fill=(20, 24, 24, 170)); d.text((12, 6), title, fill='white', font=FNT)
    if label: d.rectangle([0, im.height - 28, im.width, im.height], fill=(52, 64, 62, 200)); d.text((12, im.height - 24), label, fill='white', font=FNTs)
    return Image.alpha_composite(im, ov).convert('RGB')
def hero_shots(br, base, shots, tag, console):
    out = {'base': base, 'shots': []}
    ctx = br.new_context(viewport={'width': 1920, 'height': 1206}, device_scale_factor=1); ctx.route('**/*', guard)
    pg = ctx.new_page(); pg.set_default_timeout(300000)
    pg.on('pageerror', lambda e: console.append(f'pageerror({tag}): {e}'))
    pg.on('console', lambda m: console.append(f'{m.type}({tag}): {m.text}') if m.type == 'error' else None)
    pg.goto(base + 'index.html'); pg.wait_for_timeout(1500)
    pg.keyboard.press('['); pg.keyboard.press(']'); pg.wait_for_timeout(500)   # upstream shortcut: collapse library + panel
    pg.evaluate("setView('3d')"); pg.wait_for_timeout(6000); pg.evaluate('__FP3D_QA__.settle()'); pg.evaluate('__FP3D_QA__.labels(false)')
    out['furniture'] = pg.evaluate('__FP3D_QA__.furniture()')
    for name, p, t, fov, cut, cap in shots:
        pg.evaluate(f'__FP3D_QA__.setCut({cut})'); pg.evaluate(f'__FP3D_QA__.look({json.dumps(p)}, {json.dumps(t)}, {fov})')
        r = pg.evaluate('__FP3D_QA__.still()')
        raw = Image.open(io.BytesIO(base64.b64decode(r['png'].split(',', 1)[1]))).convert('RGB')
        raw.save(V / f'{name}_raw.png') if tag == 'v2' else None
        caption(raw, cap, LBL if tag == 'v2' else 'Upstream wy51ai/floorplan-3d demo apartment, MIT (c) 2026 wuyi - rendered locally, same renderer/lens - reference only').save(V / f'{name}.png')
        out['shots'].append({'name': name, 'png': f'verify/{name}.png', 'canvas': [r['w'], r['h']], 'camera_mm_m': p, 'target_mm_m': t, 'fov': fov, 'cut_m': cut, 'caption': cap})
    ctx.close(); return out
def make_side_by_sides(res):
    pairs = [('v2_01_hero_living_dining_pool', 'demo_01_living'), ('v2_06_hero_maid_room', 'demo_02_bedroom'), ('v2_04_hero_kitchen', 'demo_03_kitchen'),
             ('v2_08_birdseye_full_walls', 'demo_08_birdseye_full_walls'), ('v2_09_birdseye_cut_walls', 'demo_09_birdseye_cut_walls')]
    W, Hh = 960, 540; sheet = Image.new('RGB', (W * 2 + 20, 70 + len(pairs) * (Hh + 16)), 'white'); d = ImageDraw.Draw(sheet)
    d.text((10, 8), 'LEFT: Ashwood 4B GF spike v2   |   RIGHT: untouched upstream Floorplan 3D demo, rendered locally the same way', fill='black', font=FNT)
    d.text((10, 38), 'SPIKE - not survey-verified, not construction-ready, not certified CAD', fill=(150, 60, 30), font=FNTs)
    for i, (a, b) in enumerate(pairs):
        y = 70 + i * (Hh + 16)
        sheet.paste(Image.open(V / f'{a}.png').resize((W, Hh)), (0, y)); sheet.paste(Image.open(V / f'{b}.png').resize((W, Hh)), (W + 20, y))
    sheet.save(V / 'v2_20_side_by_side_spike_vs_upstream_demo.png')
    v1p = S / 'v1/verify/02_3d_perspective_iso.png'
    if v1p.exists():
        a = Image.open(v1p).convert('RGB'); b = Image.open(V / 'v2_08_birdseye_full_walls.png'); c = Image.open(V / 'v2_01_hero_living_dining_pool.png')
        sh = Image.new('RGB', (W * 3 + 40, Hh + 60), 'white'); d = ImageDraw.Draw(sh)
        d.text((10, 8), 'v1 (rejected: no rooms, no furniture, high view)', fill='black', font=FNTs); d.text((W + 30, 8), 'v2 bird\'s-eye, full walls', fill='black', font=FNTs); d.text((2 * W + 50, 8), 'v2 eye level, living/dining', fill='black', font=FNTs)
        d.text((10, 32), 'SPIKE - not survey-verified, not construction-ready, not certified CAD', fill=(150, 60, 30), font=FNTs)
        sh.paste(a.resize((W, Hh)), (0, 56)); sh.paste(b.resize((W, Hh)), (W + 20, 56)); sh.paste(c.resize((W, Hh)), (2 * W + 40, 56)); sh.save(V / 'v2_21_v1_vs_v2.png')

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', headless=True, args=ARGS)
    # ---------------- desktop ----------------
    ctx = br.new_context(viewport={'width': 1600, 'height': 1000}, device_scale_factor=1)
    ctx.route('**/*', guard)
    pg = ctx.new_page(); pg.set_default_timeout(240000)
    pg.on('console', lambda m: console.append(f'{m.type}: {m.text}'))
    pg.on('pageerror', lambda e: console.append(f'pageerror: {e}'))
    # Under SwiftShader the render loop is slow, so each step: let the loop run briefly, then settle (finish
    # animations, stop the loop, render one frame) and capture. Clicks are dispatched via DOM to avoid waiting on frames.
    def frame(p_, ms=2500):
        p_.evaluate('__FP3D_QA__.restore()'); p_.wait_for_timeout(ms); p_.evaluate('__FP3D_QA__.settle(); __FP3D_QA__.still(); 0')
    def jsclick(p_, sel): p_.evaluate(f"document.querySelector({json.dumps(sel)}).click()")
    pg.goto(BASE + 'index.html'); pg.wait_for_timeout(1500)
    pg.screenshot(path=str(V / '01_2d_plan_view.png'))
    pg.evaluate("setView('3d')"); pg.wait_for_timeout(6000); pg.evaluate('__FP3D_QA__.settle(); __FP3D_QA__.still(); 0')
    res['webgl2'] = pg.evaluate("(() => { const c = document.createElement('canvas'); return !!c.getContext('webgl2'); })()")
    res['info_after_enter'] = pg.evaluate('__FP3D_QA__.info()')
    pg.screenshot(path=str(V / '02_3d_perspective_iso_ui.png'))
    jsclick(pg, '#vTop'); frame(pg); pg.screenshot(path=str(V / '03_3d_top_view_ui.png'))
    jsclick(pg, '#roomList button[data-room="swimming-pool"]'); frame(pg); pg.screenshot(path=str(V / '04_flyto_swimming_pool_water2_ui.png'))
    cam_before = pg.evaluate('__FP3D_QA__.info().cam')
    jsclick(pg, '#roomList button[data-room="kitchen"]'); frame(pg)
    cam_after = pg.evaluate('__FP3D_QA__.info().cam'); pg.screenshot(path=str(V / '05_flyto_kitchen_ui.png'))
    res['flyto'] = {'kitchen_cam_before': cam_before, 'kitchen_cam_after': cam_after, 'moved': cam_before != cam_after}
    d0 = pg.evaluate('__FP3D_QA__.info().doorsOpen'); pg.evaluate('__FP3D_QA__.toggleDoor(3)'); frame(pg, 1200)
    d1 = pg.evaluate('__FP3D_QA__.info().doorsOpen'); pg.evaluate('__FP3D_QA__.toggleDoor(3)'); frame(pg, 800)
    res['doors'] = {'before': d0, 'after_toggle_door4': d1, 'changed': d0 != d1}
    jsclick(pg, '[data-cut="1.2"]'); jsclick(pg, '#vIso'); frame(pg); pg.screenshot(path=str(V / '06_cut_walls_iso_ui.png'))
    res['cut_after_click'] = pg.evaluate('__FP3D_QA__.info().cut')
    jsclick(pg, '[data-cut="3"]'); frame(pg, 1000)
    pg.evaluate('__FP3D_QA__.settle(); __FP3D_QA__.furn(false)')
    geo = pg.evaluate('__FP3D_QA__.topOrtho(1)')
    save_png(pg.evaluate('__FP3D_QA__.png()'), V / '09_qa_top_ortho_3d.png')
    pg.evaluate('__FP3D_QA__.furn(true)')
    res['furniture_runtime'] = pg.evaluate('__FP3D_QA__.furniture()'); res['rooms_runtime'] = pg.evaluate('__FP3D_QA__.rooms()')
    res['qa_top_ortho'] = geo
    res['info_final_desktop'] = pg.evaluate('__FP3D_QA__.info()')
    ctx.close()
    # ---------------- flat fallback ----------------
    ctx = br.new_context(viewport={'width': 1600, 'height': 1000}); ctx.route('**/*', guard); pg = ctx.new_page(); pg.set_default_timeout(240000)
    pg.on('pageerror', lambda e: console.append(f'pageerror(flat): {e}'))
    pg.goto(BASE + 'index.html?water=flat'); pg.wait_for_timeout(1200); pg.evaluate("setView('3d')"); pg.wait_for_timeout(5000); pg.evaluate('__FP3D_QA__.settle(); 0')
    jsclick(pg, '#roomList button[data-room="swimming-pool"]'); frame(pg)
    pg.screenshot(path=str(V / '10_flat_water_fallback_pool_ui.png'))
    res['flat_fallback_info'] = pg.evaluate('__FP3D_QA__.info().water')
    ctx.close()
    # ---------------- mobile touch walk (joystick) ----------------
    ctx = br.new_context(viewport={'width': 900, 'height': 1200}, has_touch=True, is_mobile=True, device_scale_factor=1)
    ctx.route('**/*', guard); pg = ctx.new_page(); pg.set_default_timeout(240000)
    pg.on('pageerror', lambda e: console.append(f'pageerror(mobile): {e}'))
    pg.goto(BASE + 'index.html'); pg.wait_for_timeout(1200)
    res['mobile_coarse_pointer'] = pg.evaluate("matchMedia('(pointer:coarse)').matches")
    pg.evaluate("setView('3d')"); pg.wait_for_timeout(3500)
    pg.evaluate("document.querySelector('[data-mode=\"walk\"]').click()"); pg.wait_for_timeout(600)
    pg.evaluate("document.getElementById('walkOverlay').click()"); pg.wait_for_timeout(600)
    c0 = pg.evaluate('__FP3D_QA__.info().cam')
    pg.screenshot(path=str(V / '11_walk_start_entry_joystick.png'))
    box = pg.locator('#joy').bounding_box()
    if box:
        cx, cy = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
        pg.mouse.move(cx, cy); pg.mouse.down(); pg.mouse.move(cx, cy - box['height'] * .45, steps=5)
        pg.wait_for_timeout(6000); pg.mouse.up(); pg.wait_for_timeout(300)
    c1 = pg.evaluate('__FP3D_QA__.info().cam')
    pg.screenshot(path=str(V / '12_walk_after_joystick.png'))
    res['walk'] = {'joystick_box': box, 'cam_before': c0, 'cam_after': c1, 'moved_m': float(np.linalg.norm(np.array(c1) - np.array(c0))) if c0 and c1 else None,
                   'mode': pg.evaluate('__FP3D_QA__.info().mode')}
    ctx.close()
    res['hero'] = hero_shots(br, BASE, HERO, 'v2', console)
    res['upstream_demo'] = hero_shots(br, DBASE, DEMO_SHOTS, 'demo', console)
    br.close()
srv.shutdown(); dsrv.shutdown()
make_side_by_sides(res)

res['network'] = {'total_requests': len(requests), 'non_localhost_requests': blocked, 'offline_pass': not blocked,
                  'distinct_paths': sorted({u.replace(BASE, '/') for u in requests})}
res['console_errors'] = [c for c in console if c.startswith(('error', 'pageerror'))]
res['console_warnings'] = [c for c in console if c.startswith('warning')][:20]

# ---------------- geometry comparison (3D top render vs approved V4 wall trace) ----------------
img = np.array(Image.open(V / '09_qa_top_ortho_3d.png').convert('RGB')).astype(int)
Hc, Wc = img.shape[:2]; smm = geo['visH_m'] * 1000 / Hc
lum = img.mean(axis=2); dark = (lum < 95) & (np.abs(img[..., 0] - img[..., 2]) < 40)
k = P['mm_per_crop_px']; ox, oy = P['origin_crop_px']
uu, vv = np.meshgrid(np.arange(Wc), np.arange(Hc))
xmm = geo['cx'] + (uu + .5 - Wc / 2) * smm; ymm = geo['cy'] + (vv + .5 - Hc / 2) * smm
cxp = ((xmm / k + ox) * SS).astype(int); cyp = ((ymm / k + oy) * SS).astype(int)
inside = (cxp >= 0) & (cxp < mask.shape[1]) & (cyp >= 0) & (cyp < mask.shape[0])
ref = np.zeros_like(dark); ref[inside] = mask[cyp[inside], cxp[inside]]
b = P['WALL_BBOX_MM']; roi = (xmm >= b[0] - 300) & (xmm <= b[2] + 300) & (ymm >= b[1] - 300) & (ymm <= b[3] + 300)
d, r = dark & roi, ref & roi
inter, union = (d & r).sum(), (d | r).sum()
tol = max(1, int(round(60 / smm)))  # ~60 mm tolerance band
dil = lambda m: nd.binary_dilation(m, iterations=tol)
prec_t = (d & dil(r)).sum() / max(d.sum(), 1); rec_t = (r & dil(d)).sum() / max(r.sum(), 1)
res['geometry_comparison'] = {'pixel_mm': round(smm, 2), 'tolerance_px': tol, 'tolerance_mm': round(tol * smm, 1),
    'v4_wall_px': int(r.sum()), '3d_dark_cap_px': int(d.sum()), 'IoU_exact': round(inter / max(union, 1), 4),
    'precision_within_tol': round(float(prec_t), 4), 'recall_within_tol': round(float(rec_t), 4),
    'note': '3D wall caps segmented by darkness (lum<95, neutral); glazing frames/door leaves/shadows can add or hide a few pixels.'}
# water surfaces: blue-tinted pixels in the 3D top render vs the approved V4 water outlines (minus islands)
wref = np.zeros_like(dark)
for w in P['WATER']:
    xs_ = [q[0] for q in w['outer']]; ys_ = [q[1] for q in w['outer']]
    m_ = (xmm >= min(xs_)) & (xmm <= max(xs_)) & (ymm >= min(ys_)) & (ymm <= max(ys_))
    for h in w['holes']:
        hx = [q[0] for q in h]; hy = [q[1] for q in h]
        m_ &= ~((xmm >= min(hx)) & (xmm <= max(hx)) & (ymm >= min(hy)) & (ymm <= max(hy)))
    wref |= m_
blue = (img[..., 2] - img[..., 0] > 8) & (img[..., 1] - img[..., 0] > 4)
res['water_comparison'] = {'v4_water_px': int(wref.sum()), '3d_blue_px': int(blue.sum()), 'IoU': round(float((blue & wref).sum() / max((blue | wref).sum(), 1)), 4),
    'note': 'Water2 tint segmented as blue>red+8 and green>red+4 (pale reflective tint); walls/shadows can occlude water edges in the top render.'}
# per-component wall match (13 V4 contours -> connected components of the mask)
labc, ncomp = nd.label(r)
comp = []
for i in range(1, ncomp + 1):
    cm = labc == i
    if cm.sum() < 20: continue
    comp.append(round(float((cm & dil(d)).sum() / cm.sum()), 3))
res['geometry_comparison']['v4_wall_components'] = len(comp)
res['geometry_comparison']['components_recall_ge_0.95'] = sum(c >= .95 for c in comp)
res['geometry_comparison']['component_recalls'] = comp
# overlay image
ys, xs = np.where(roi); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
ov = np.full((Hc, Wc, 3), 255, np.uint8)
ov[r & d] = (40, 40, 40); ov[r & ~d] = (220, 30, 30); ov[d & ~r] = (30, 90, 230)
# water outlines (from data) in yellow-ish for reference
im = Image.fromarray(ov[y0:y1, x0:x1]); dr = ImageDraw.Draw(im)
def topx(xm, ym): return ((xm - geo['cx']) / smm + Wc / 2 - x0, (ym - geo['cy']) / smm + Hc / 2 - y0)
for w in P['WATER']:
    pts = [topx(*p) for p in w['outer']]; dr.polygon(pts, outline=(0, 150, 170))
    for h in w['holes']: dr.polygon([topx(*p) for p in h], outline=(0, 150, 170))
im.save(V / '13_overlay_3d_top_vs_v4_walls.png')
# side-by-side: approved V4 source-space crop vs 3D top render, same crop window
v4 = Image.open(R / 'active/approved-cad-v4/png/FP-4B-GF_V4_long7680.png').convert('RGB')
top3d = Image.open(V / '09_qa_top_ortho_3d.png').convert('RGB').crop((x0, y0, x1, y1))
# V4 sheet: source_space transform translate(-5,76) scale(1.1963) in a 1000-wide viewBox
sc = v4.width / 1000.0; f = 1.1963006295231644
def v4px(cxp_, cyp_): return ((-5 + cxp_ * f) * sc, (76 + cyp_ * f) * sc)
xa_mm, ya_mm = geo['cx'] + (x0 - Wc / 2) * smm, geo['cy'] + (y0 - Hc / 2) * smm
xb_mm, yb_mm = geo['cx'] + (x1 - Wc / 2) * smm, geo['cy'] + (y1 - Hc / 2) * smm
a_ = v4px(xa_mm / k + ox, ya_mm / k + oy); b_ = v4px(xb_mm / k + ox, yb_mm / k + oy)
v4c = v4.crop((int(a_[0]), int(a_[1]), int(b_[0]), int(b_[1]))).resize(top3d.size)
gap = 30; sbs = Image.new('RGB', (top3d.width * 3 + gap * 2, top3d.height + 60), 'white')
sbs.paste(v4c, (0, 60)); sbs.paste(top3d, (top3d.width + gap, 60)); sbs.paste(im, (2 * (top3d.width + gap), 60))
dd = ImageDraw.Draw(sbs)
try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
except Exception: fnt = None
dd.text((8, 8), 'Approved V4 2D (FP-4B-GF)', fill='black', font=fnt)
dd.text((top3d.width + gap + 8, 8), 'Floorplan3D spike - 3D top (near-ortho)', fill='black', font=fnt)
dd.text((2 * (top3d.width + gap) + 8, 8), 'Overlay: grey=match red=V4 only blue=3D only', fill='black', font=fnt)
dd.text((8, 34), 'SPIKE - not survey-verified, not construction-ready, not certified CAD', fill=(150, 60, 30), font=fnt)
sbs.save(V / '14_side_by_side_v4_vs_3d_top.png')
res['screenshots'] = sorted(str(p.relative_to(R)) for p in V.glob('*.png'))
(V / 'verification.json').write_text(json.dumps(res, indent=2) + '\n')
res['upstream_demo_harness'] = {'upstream_index_sha256': hashlib.sha256((UP / 'index.html').read_bytes()).hexdigest(), 'changes': ['importmap -> local vendored three r160 (same files as the spike)', 'read-only camera/capture hook appended before window.View3D'], 'served_from': 'temporary dir (not shipped)'}
(V / 'verification.json').write_text(json.dumps(res, indent=2) + '\n')
print(json.dumps({k_: res[k_] for k_ in ('water_comparison', 'network', 'console_errors', 'geometry_comparison', 'flyto', 'doors', 'walk', 'flat_fallback_info', 'webgl2', 'mobile_coarse_pointer')}, indent=1)[:6000])
print('water', res['info_final_desktop']['water'])
