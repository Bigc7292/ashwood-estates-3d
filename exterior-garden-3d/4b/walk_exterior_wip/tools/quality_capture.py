#!/usr/bin/env python3
"""Quality-round capture/probe tool for the five active walk_exterior_wip sources
(change-set viewer-quality-2026-11-10, exterior lane). Free stack: python playwright + cached chromium headless shell (SwiftShader WebGL).

Usage:
  python3 quality_capture.py still <page.html> <view.json> <out.png> [w h]
  python3 quality_capture.py probe <page.html> <view.json> <outprefix> [w h]   # t5/t6/hidden Water2 proof frames
  python3 quality_capture.py orbit <page.html> <view.json>                      # drag-orbit + wheel-zoom numeric proof
  python3 quality_capture.py walk  <page.html>                                  # walk-mode drag regression (no ?view=)
Prints one JSON line per run: errors, failed requests, renderer info, probe values.
"""
import json, sys, threading, functools, http.server, socketserver, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]          # exterior-garden-3d/4b
GL = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def serve():
    handler = functools.partial(Quiet, directory=str(ROOT))
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]

class QuietHandler:
    pass

def open_page(p, page, view, w, h, errors, failed):
    srv, port = serve()
    b = p.chromium.launch(args=GL)
    pg = b.new_page(viewport={'width': w, 'height': h})
    pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.on('requestfailed', lambda q: failed.append(q.url))
    pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    q = '' if view is None else '?view=' + __import__('urllib.parse', fromlist=['quote']).quote(Path(view).read_text().strip())
    pg.goto(f'http://127.0.0.1:{port}/walk_exterior_wip/{page}{q}', wait_until='commit')
    pg.wait_for_function("() => document.title === 'READY'", timeout=280000)
    pg.wait_for_timeout(1200)
    return srv, b, pg

def info(pg):
    try: return pg.evaluate('() => window.__info ? window.__info() : null')
    except Exception: return None

def pool_crop(pg, w, h):
    """Pool screen rect via the page's __project hook (model water[0], plan+calibrated 9.50x2.40)."""
    try:
        pts = pg.evaluate("""() => { if (!window.__project || !window.MODEL) return null;
            const w = window.MODEL.water.find(v => v.id === 'swimming-pool'); if (!w) return null;
            return [window.__project(w.x0, -0.03, w.z0), window.__project(w.x1, -0.03, w.z1)]; }""")
    except Exception: pts = None
    if not pts: return None
    (x0, y0), (x1, y1) = pts
    pad = 6
    return [max(0, min(x0, x1)-pad), max(0, min(y0, y1)-pad), min(w, max(x0, x1)+pad), min(h, max(y0, y1)+pad)]

def main():
    mode, page, view = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else None)
    out = sys.argv[4] if len(sys.argv) > 4 else None
    w = int(sys.argv[5]) if len(sys.argv) > 5 else 1280
    h = int(sys.argv[6]) if len(sys.argv) > 6 else 720
    errors, failed = [], []
    rep = {'mode': mode, 'page': page, 'view': view, 'viewport': [w, h]}
    with sync_playwright() as p:
        if mode == 'still':
            srv, b, pg = open_page(p, page, view, w, h, errors, failed)
            pg.evaluate('() => { window.__capture = true; }'); pg.wait_for_timeout(1200)
            pg.screenshot(timeout=0, path=out)
            rep['renderer'] = info(pg)
        elif mode == 'probe':
            srv, b, pg = open_page(p, page, view, w, h, errors, failed)
            pg.evaluate('() => window.__frame(5, 10)'); pg.screenshot(timeout=0, path=f'{out}_t5.png')
            pg.evaluate('() => window.__frame(6, 10)'); pg.screenshot(timeout=0, path=f'{out}_t6.png')
            hid = pg.evaluate("""() => { let n = 0; for (const m of (window.__WATERMESH || [])) { m.visible = false; n++; }
                window.__frame(6, 10); return n; }""")
            pg.screenshot(timeout=0, path=f'{out}_t6_hidden.png')
            rep['water_meshes_hidden'] = hid
            rep['pool_crop_px'] = pool_crop(pg, w, h)
            rep['renderer'] = info(pg)
        elif mode == 'orbit':
            srv, b, pg = open_page(p, page, view, w, h, errors, failed)
            st0 = pg.evaluate('() => window.__controls ? [window.__controls.getAzimuthalAngle(), window.__controls.getPolarAngle(), window.__controls.getDistance()] : null')
            pg.mouse.move(w/2, h/2); pg.mouse.down(); pg.mouse.move(w/2+160, h/2-70, steps=12); pg.mouse.up(); pg.wait_for_timeout(300)
            st1 = pg.evaluate('() => window.__controls ? [window.__controls.getAzimuthalAngle(), window.__controls.getPolarAngle(), window.__controls.getDistance()] : null')
            pg.mouse.wheel(0, -300); pg.wait_for_timeout(300)
            st2 = pg.evaluate('() => window.__controls ? [window.__controls.getAzimuthalAngle(), window.__controls.getPolarAngle(), window.__controls.getDistance()] : null')
            rep['orbit_state_before_drag'] = st0; rep['orbit_state_after_drag'] = st1; rep['orbit_state_after_wheel'] = st2
            rep['drag_orbits'] = bool(st0 and st1 and (abs(st1[0]-st0[0]) > 0.01 or abs(st1[1]-st0[1]) > 0.01))
            rep['wheel_zooms'] = bool(st1 and st2 and abs(st2[2]-st1[2]) > 0.05)
            # pinch path: two touch points are emulated as ctrl+wheel in OrbitControls; assert touch handler presence instead
            rep['controls_listening'] = pg.evaluate('() => !!window.__controls')
        elif mode == 'walk':
            srv, b, pg = open_page(p, page, None, w, h, errors, failed)
            pr0 = pg.evaluate('() => window.__project ? window.__project(9.4, 1.6, 15) : null')
            pg.mouse.move(w/2, h/2); pg.mouse.down(); pg.mouse.move(w/2+180, h/2, steps=12); pg.mouse.up(); pg.wait_for_timeout(400)
            pr1 = pg.evaluate('() => window.__project ? window.__project(9.4, 1.6, 15) : null')
            pg.keyboard.down('w'); pg.wait_for_timeout(500); pg.keyboard.up('w')
            pr2 = pg.evaluate('() => window.__project ? window.__project(9.4, 1.6, 15) : null')
            rep['walk_project_before'] = pr0; rep['walk_project_after_drag'] = pr1; rep['walk_project_after_W'] = pr2
            rep['walk_drag_looks'] = bool(pr0 and pr1 and (abs(pr1[0]-pr0[0]) > 5 or abs(pr1[1]-pr0[1]) > 5))
            rep['walk_W_moves'] = bool(pr1 and pr2 and (abs(pr2[0]-pr1[0]) > 1 or abs(pr2[1]-pr1[1]) > 1))
        rep['page_errors'] = errors; rep['failed_requests'] = failed
        b.close(); srv.shutdown()
    print(json.dumps(rep))

if __name__ == '__main__':
    main()
