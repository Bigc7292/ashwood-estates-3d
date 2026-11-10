#!/usr/bin/env python3
"""Add a phone-only layout layer to a published Ashwood 3D artifact page.

Layout and viewing only: CSS overrides plus one srcdoc tweak for the exterior
hub. Model data (DATA/SBS/VIEWS, geometry, camera, furniture, scale) is untouched.

Usage: apply_mobile_shell.py <src.html> <dst.html> ext|ff
"""
import sys

EXT_CSS = """
@media (max-width:640px){
  html,body{height:100%;overflow:hidden;overscroll-behavior:none}
  .wrap{height:100dvh;position:relative}
  header,.note,.help{display:none}
  .tabs{position:absolute;top:8px;left:0;right:0;z-index:5;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;padding:0 8px;gap:6px}
  .tabs::-webkit-scrollbar{display:none}
  .tab{flex:0 0 auto;min-height:36px;padding:6px 12px;font-size:13px;background:rgba(255,255,255,.88);box-shadow:0 1px 4px rgba(0,0,0,.2)}
  .tab[aria-selected="true"]{background:var(--accent);color:var(--accent-fg)}
  .stage{position:absolute;inset:0;margin:0;border:0;border-radius:0;min-height:0}
  .wrap::after{content:"Concept visualisation · not survey-verified · not certified CAD";position:absolute;left:0;right:0;bottom:4px;z-index:5;text-align:center;font:10px/1.2 sans-serif;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.8);pointer-events:none}
  .sbs{padding:48px 8px 24px}
}
"""

FF_CSS = """
@media (max-width:640px){
  #phoneTools{display:inline-flex;min-height:40px;align-items:center;white-space:nowrap}
  header{flex-wrap:nowrap;overflow:visible;padding:6px 8px;gap:6px;position:relative;z-index:20}
  header > *:not(#phoneTools):not(#viewSeg):not(.only2d):not(.only3d){display:none!important}
  header > .only2d,header > .only3d{display:none!important}
  body.tools-open header{position:fixed;left:0;right:0;top:calc(env(safe-area-inset-top,0px) + 56px);max-height:calc(100dvh - 120px);overflow-y:auto;flex-wrap:wrap;background:var(--panel);box-shadow:0 8px 24px rgba(40,30,20,.2);padding:8px;border-bottom:1px solid var(--line);z-index:40}
  body.tools-open header > *:not(#phoneTools):not(.only2d):not(.only3d):not(.brand):not(.spacer){display:flex!important}
  body.tools-open header > .brand,body.tools-open header > .spacer{display:none!important}
  body:not(.m3d).tools-open header > .only2d{display:flex!important}
  body.m3d.tools-open header > .only3d{display:flex!important}
  #wipNote{left:8px!important;right:8px!important;top:auto!important;bottom:36px!important;transform:none!important;width:auto!important;max-width:none!important;font-size:10.5px!important;line-height:1.25!important;padding:4px 26px 4px 8px!important;border-radius:6px!important;text-align:left!important;opacity:.92;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  #wipNote.wip-open{white-space:normal;overflow:visible}
  #spikeBanner{display:none!important}
  .wip-x{display:inline-block;position:absolute;right:4px;top:50%;transform:translateY(-50%);background:none;border:0;color:#fff;font-size:18px;line-height:1;padding:2px 6px;cursor:pointer}
}
.wip-x{display:none}
"""

CAP_CSS = "@media (max-width:640px){#cap,#title{display:none}}"

PROGRESS_CSS = """
@media (max-width:640px){
  table, tbody, tr, td { display:block; width:100%; }
  thead { display:none; }
  .wrap { overflow:visible; }
  tr { border-bottom:1px solid var(--line); padding:6px 4px; }
  tr:last-child { border-bottom:none; }
  td { border:0; padding:3px 6px; }
  td small { display:inline; margin-left:4px; }
  h1 { font-size:21px; }
  .box { border-radius:8px; }
}
"""

GEN_CSS = """
@media (max-width:640px){
  body { padding-inline:12px; }
  h1 { font-size:20px; line-height:1.25; }
  img { max-width:100%; height:auto; }
}
"""

def must_once(html, s):
    n = html.count(s)
    if n != 1:
        sys.exit(f"expected exactly one match, found {n}: {s[:60]!r}")

def main():
    src, dst, kind = sys.argv[1], sys.argv[2], sys.argv[3]
    html = open(src, encoding="utf-8").read()
    if kind == "ext":
        marker = "</style></head><body><div class=\"wrap\">"
        must_once(html, marker)
        html = html.replace(marker, EXT_CSS + marker)  # rules go inside the page's own <style>
        old = "f.srcdoc=DATA[k].replace('<!--SHIM-->',SHIM+"
        must_once(html, old)
        html = html.replace(old, "f.srcdoc=DATA[k].replace('<!--SHIM-->',SHIM+'<style>" + CAP_CSS + "</style>'+")
    elif kind in ("ff", "gf"):  # kind decides the head marker
        # Floor viewers share one shell: CSS, a Tools toggle, a collapsible tools panel, a dismissible WIP line.
        marker = "</style>\n</head>" if kind == "ff" else "</style>\n\n</head>"
        must_once(html, marker)
        html = html.replace(marker, FF_CSS + marker)
        must_once(html, "<header>")
        html = html.replace("<header>", '<header>\n<button id="phoneTools" class="btn chip" type="button" aria-expanded="false">Tools ▾</button>', 1)
        wip = "<div style=\"position:fixed;left:50%;transform:translateX(-50%);bottom:34px;z-index:9999;"
        if wip in html:  # the first floor has the brown WIP note; the ground floor does not
            i = html.index(wip); j = html.index(">", i) + 1
            html = html[:i] + '<div id="wipNote" onclick="this.classList.toggle(\'wip-open\')" ' + html[i+5:j] + '<button class="wip-x" type="button" aria-label="Dismiss note" onclick="this.parentNode.remove()">×</button>' + html[j:]
        end = html.rfind("</body>")
        html = html[:end] + "<script>document.getElementById('phoneTools').onclick=function(){var o=document.body.classList.toggle('tools-open');this.setAttribute('aria-expanded',o)};</script>\n" + html[end:]
    elif kind in ("progress", "gen"):
        css = PROGRESS_CSS if kind == "progress" else GEN_CSS
        end = html.rfind("</body>")
        if end < 0:
            sys.exit("no </body> found")
        html = html[:end] + '<style id="mobile-shell">' + css + "</style>\n" + html[end:]
    else:
        sys.exit("kind must be ext, ff, gf, progress or gen")
    open(dst, "w", encoding="utf-8").write(html)
    print("wrote", dst, len(html), "bytes")

if __name__ == "__main__":
    main()
