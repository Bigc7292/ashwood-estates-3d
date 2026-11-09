#!/usr/bin/env python3
"""QA for FF-E1: (1) V4 vs enhanced wall overlay, (2) zone-edge check, (3) GF-vs-FF style side-by-side."""
import json, re
from pathlib import Path
import numpy as np, cv2, cairosvg
REPO = Path(__file__).resolve().parents[4]; OUT = Path(__file__).resolve().parents[1]; QA = OUT / "qa"
V4 = (REPO / "active/approved-cad-v4/svg/FP-4B-FF_V4_portrait.svg").read_text()
EN = (OUT / "FP-4B-FF_ENHANCED_FF-E1_portrait.svg").read_text()
W = 2000
def wall_only(svg, gid_re):
    walls = re.findall(r'<(?:ns0:)?g[^>]*id="(?:%s)".*?</(?:ns0:)?g>' % gid_re, svg, re.S)
    tr = re.search(r'<g id="source_diagram" transform="([^"]+)"', svg).group(1)
    doc = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:ns0="http://www.w3.org/2000/svg" viewBox="0 0 1000 1414.141414141414"><rect width="1000" height="1414.15" fill="white"/><g transform="{tr}">{"".join(walls)}</g></svg>'
    return cv2.imdecode(np.frombuffer(cairosvg.svg2png(bytestring=doc.encode(), output_width=W), np.uint8), 0) < 128
a = wall_only(V4, "source_wall_poche|structural_poche_visibility_restore")
b = wall_only(EN, "source_wall_poche|structural_poche_visibility_restore")
iou = (a & b).sum() / max((a | b).sum(), 1)
# full-render overlay: V4 preview (red) vs enhanced dark strokes (cyan)
v4r = cv2.imdecode(np.frombuffer(cairosvg.svg2png(bytestring=V4.encode(), output_width=W), np.uint8), 1)
enr = cv2.imdecode(np.frombuffer(cairosvg.svg2png(bytestring=EN.encode(), output_width=W), np.uint8), 1)
ov = np.full_like(enr, 255)
ov[cv2.cvtColor(enr, cv2.COLOR_BGR2GRAY) < 90] = (200, 170, 0)
ov[a] = (40, 40, 220); ov[a & b] = (30, 30, 30)
cv2.imwrite(str(QA / "FF-E1_vs_V4_wall_overlay.png"), ov)
blend = cv2.addWeighted(v4r, 0.5, enr, 0.5, 0); cv2.imwrite(str(QA / "FF-E1_vs_V4_blend.png"), blend)
# zone-edge check: each zone rect edge should sit on a drawn barrier (poche or traced line-art) within 3 px native
log = json.loads((QA / "build_log.json").read_text())
zones = log["zones"]; bar = cv2.imread(str(QA / "_barrier4x.png"), 0) > 0
S = 4; issues = []
for name, kind, x0, y0, x1, y1 in zones:
    for edge, pts in (("top", [(x, y0) for x in range(x0+2, x1-2)]), ("bottom", [(x, y1) for x in range(x0+2, x1-2)]),
                      ("left", [(x0, y) for y in range(y0+2, y1-2)]), ("right", [(x1, y) for y in range(y0+2, y1-2)])):
        hit = 0
        for x, y in pts:
            ys, xs = slice(max(0,(y-3)*S), (y+3)*S), slice(max(0,(x-3)*S), (x+3)*S)
            hit += bar[ys, xs].any()
        cov = hit / max(len(pts), 1)
        if cov < 0.6: issues.append(dict(zone=name, edge=edge, barrier_coverage=round(cov, 2)))
# side-by-side GF V4 vs FF-E1
gf = cv2.imread(str(REPO / "active/approved-cad-v4/png/FP-4B-GF_V4_preview.png"))
ff = cv2.imread(str(OUT / "FP-4B-FF_ENHANCED_FF-E1_preview.png"))
v4p = cv2.imread(str(REPO / "active/approved-cad-v4/png/FP-4B-FF_V4_preview.png"))
H = 1414
def fit(im): return cv2.resize(im, (int(im.shape[1]*H/im.shape[0]), H), interpolation=cv2.INTER_AREA)
def cap(im, t):
    pad = np.full((60, im.shape[1], 3), 255, np.uint8); cv2.putText(pad, t, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (52,58,38), 2); return np.vstack([pad, im])
gap = np.full((H+60, 30, 3), 255, np.uint8)
sbs = np.hstack([cap(fit(gf), "TEMPLATE: FP-4B-GF V4 (presentation prototype 04)"), gap, cap(fit(ff), "NEW: FP-4B-FF ENHANCED FF-E1")])
cv2.imwrite(str(OUT / "FP-4B-GF_V4_vs_FF-E1_side_by_side.png"), sbs)
sbs2 = np.hstack([cap(fit(v4p), "BASE: FP-4B-FF V4 (source-limited)"), gap, cap(fit(ff), "NEW: FP-4B-FF ENHANCED FF-E1")])
cv2.imwrite(str(QA / "FF_V4_base_vs_FF-E1.png"), sbs2)
rep = dict(wall_poche_iou_vs_V4=round(float(iou), 5), wall_pixels_v4=int(a.sum()), wall_pixels_enh=int(b.sum()), zone_edge_issues=issues)
(QA / "qa_report.json").write_text(json.dumps(rep, indent=1)); print(json.dumps(rep, indent=1))
