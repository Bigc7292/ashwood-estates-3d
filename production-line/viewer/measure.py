#!/usr/bin/env python3
"""Headless metrics for lane-4 viewers (free Playwright)."""
from __future__ import annotations
import json, threading, time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "baseline"
OUT.mkdir(parents=True, exist_ok=True)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)
    def log_message(self, *args):
        pass

def main():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    from playwright.sync_api import sync_playwright

    targets = [
        ("gf-source", "/active/floorplan3d-spike/FP-4B-GF/index.html", "active/floorplan3d-spike/FP-4B-GF/index.html", "fp3d"),
        ("gf-opt", "/production-line/viewer/gf/index.html", "production-line/viewer/gf/index.html", "fp3d"),
        ("ff-opt", "/production-line/viewer/ff/index.html", "production-line/viewer/ff/index.html", "fp3d"),
        ("exterior-source-v6", "/exterior-garden-3d/4b/walkable/walkable_v6.html", "exterior-garden-3d/4b/walkable/walkable_v6.html", "ext-embed"),
        ("exterior-opt", "/production-line/viewer/exterior/index.html", "production-line/viewer/exterior/index.html", "ext-opt"),
    ]
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--use-gl=swiftshader", "--ignore-gpu-blocklist"])
        for tid, url, rel, kind in targets:
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            errors, failed = [], []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("requestfailed", lambda r: failed.append(r.url))
            t0 = time.time()
            status, metrics = "ok", {}
            try:
                page.goto(f"http://127.0.0.1:{port}{url}", wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(800)
                try:
                    page.wait_for_function("document.title.includes('READY') || !!document.querySelector('canvas')", timeout=45000)
                except Exception:
                    pass
                page.wait_for_timeout(1200)
                if kind == "fp3d":
                    page.evaluate("""() => {
                      const b = [...document.querySelectorAll('button')].find(x => /3D/.test(x.textContent||''));
                      if (b) b.click();
                    }""")
                    page.wait_for_timeout(2200)
                    metrics = page.evaluate("""async () => {
                      const qa = window.__FP3D_QA__;
                      const opt = window.__LANE4_OPT__;
                      let fps = null;
                      if (qa && qa.fps) fps = await qa.fps(1000);
                      return {
                        qa: qa ? qa.info() : null,
                        opt: opt ? {pixelRatio: opt.pixelRatio(), shadowAutoUpdate: opt.shadowAutoUpdate(), shadowBaked: opt.shadowBaked(), looping: opt.looping()} : null,
                        fps,
                        canvases: document.querySelectorAll('canvas').length,
                      };
                    }""")
                elif kind == "ext-opt":
                    metrics = page.evaluate("""() => ({
                      ext: window.__LANE4_EXT__ ? window.__LANE4_EXT__.info() : null,
                      canvases: document.querySelectorAll('canvas').length,
                      title: document.title,
                    })""")
                else:
                    metrics = page.evaluate("""() => ({
                      canvases: document.querySelectorAll('canvas').length,
                      title: document.title,
                    })""")
            except Exception as e:
                status, metrics = "error", {"error": str(e)}
            load_ms = int((time.time() - t0) * 1000)
            path = ROOT / rel
            results.append({
                "id": tid,
                "htmlBytes": path.stat().st_size if path.exists() else None,
                "loadMs": load_ms,
                "status": status,
                "consoleErrors": errors[:8],
                "failedRequests": [u for u in failed if "favicon" not in u][:8],
                "metrics": metrics,
            })
            print(f"measured {tid} {load_ms}ms {status}")
            page.close()
        browser.close()
    httpd.shutdown()

    def sz(rel):
        p = ROOT / rel
        return p.stat().st_size if p.exists() else None

    summary = {
        "measured_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "zone_label": "Asia/Dubai",
        "results": results,
        "sizes": {
            "gf_source_html": sz("active/floorplan3d-spike/FP-4B-GF/index.html"),
            "gf_opt_html": sz("production-line/viewer/gf/index.html"),
            "ff_opt_html": sz("production-line/viewer/ff/index.html"),
            "exterior_v6_html": sz("exterior-garden-3d/4b/walkable/walkable_v6.html"),
            "exterior_opt_html": sz("production-line/viewer/exterior/index.html"),
            "exterior_opt_model_js": sz("production-line/viewer/exterior/model.js"),
            "shared_vendor_three_module": sz("production-line/viewer/vendor/three/build/three.module.js"),
            "shared_vendor_total": sum(p.stat().st_size for p in (ROOT/"production-line/viewer/vendor").rglob("*") if p.is_file()),
        },
    }
    before = {
        "note": "Source baselines (builders untouched)",
        "gf_html_bytes": summary["sizes"]["gf_source_html"],
        "gf_pixelRatio_cap": 2,
        "gf_shadow_autoUpdate": True,
        "gf_loop": "continuous requestAnimationFrame",
        "exterior_v6_html_bytes": summary["sizes"]["exterior_v6_html"],
        "exterior_v6": "single-file embedded three + textures",
        "ff_on_main": False,
        "rf_viewer": False,
    }
    (OUT / "before.json").write_text(json.dumps(before, indent=2))
    (OUT / "after.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary["sizes"], indent=2))

if __name__ == "__main__":
    main()
