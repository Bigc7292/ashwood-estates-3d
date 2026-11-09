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
  .wrap{height:100vh;height:100dvh}
  header{padding:8px 12px 2px}
  h1{font-size:16px;line-height:1.2}
  .sub{font-size:11px;line-height:1.35}
  .tabs{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:6px 10px;gap:6px}
  .tabs::-webkit-scrollbar{display:none}
  .tab{flex:0 0 auto;min-height:40px;padding:8px 14px;font-size:14px}
  .note{padding:0 12px 4px;font-size:12px}
  .help{padding:0 12px 2px;font-size:11px}
  .stage{flex:1 1 auto;min-height:0;margin:0 6px 6px;border-radius:8px}
  .sbs{padding:8px}
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

CAP_CSS = "@media (max-width:640px){#cap{font-size:11.5px;padding:5px 8px;line-height:1.2}}"

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
        html = html.replace(marker, '<style id="mobile-shell">' + EXT_CSS + "</style>" + marker)
        old = "f.srcdoc=DATA[k].replace('<!--SHIM-->',SHIM+"
        must_once(html, old)
        html = html.replace(old, "f.srcdoc=DATA[k].replace('<!--SHIM-->',SHIM+'<style>" + CAP_CSS + "</style>'+")
    elif kind == "ff":
        marker = "</style>\n</head>"
        must_once(html, marker)
        html = html.replace(marker, FF_CSS + "</style>\n</head>")  # rules go inside the page's own <style>
    else:
        sys.exit("kind must be ext or ff")
    open(dst, "w", encoding="utf-8").write(html)
    print("wrote", dst, len(html), "bytes")

if __name__ == "__main__":
    main()
