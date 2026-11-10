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
  header{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;padding:6px 8px;gap:6px}
  header::-webkit-scrollbar{display:none}
  .brand{display:none}
  .spacer{display:none}
  header .btn,header .grp .btn{min-height:40px;padding:8px 10px}
  footer{font-size:11px;gap:10px;padding:0 10px}
  #toast{bottom:96px;max-width:90vw;white-space:normal;text-align:center}
  main{min-height:0}
}
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
    elif kind == "ff":
        marker = "</style>\n</head>"
        must_once(html, marker)
        html = html.replace(marker, FF_CSS + "</style>\n</head>")  # rules go inside the page's own <style>
    elif kind == "gf":
        # Same floorplan app as the first floor. Its own <style> closes just before </head>.
        marker = "</style>\n\n</head>"
        must_once(html, marker)
        html = html.replace(marker, FF_CSS + marker)
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
