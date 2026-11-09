#!/usr/bin/env python3
"""Build the ENHANCED 4B first-floor presentation plan (FF-E1).

Concept visualisation, not survey-verified, not construction-ready, not certified CAD.

Inputs (ACTIVE_PIPELINE.json only, sha256-checked):
  active/approved-cad-v4/svg/FP-4B-FF_V4_portrait.svg   (base: wall poche, furniture symbols, labels, calibration frame)
  active/approved-cad-v4/reports/FP-4B-FF_V4_record.json (calibration px_per_m)
  source-evidence/plan-crops/FP-4B-FF_untouched_board_crop.png (brochure p28 board crop; doors/stairs/fixtures line-art)
  active/approved-cad-v4/svg/FP-4B-GF_V4_portrait.svg   (STYLE template only: palette, trees, cars, dimension chains, legend)
No AI image generation. Geometry stays in the V4 FF native 650x1000 source frame with the V4 transform,
so walls/openings overlay the V4 plan exactly.
Free tools: python3, numpy, opencv-python-headless, cairosvg.
"""
import hashlib, json, math, re, sys, random
from pathlib import Path
import numpy as np, cv2, cairosvg

REPO = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1]
AP = json.loads((REPO / "ACTIVE_PIPELINE.json").read_text())
def plan(pid): return [p for p in AP["plans"] if p["id"] == pid][0]
FF, GF = plan("4B-FF"), plan("4B-GF")
def sha(p): return hashlib.sha256((REPO / p).read_bytes()).hexdigest()
for p, key in ((FF, "svg"), (GF, "svg")):
    assert sha(p[key]) == p["sha256"][key], f"hash mismatch {p[key]}"
assert "superseded" not in FF["source_crop"]
V4 = (REPO / FF["svg"]).read_text()
GFS = (REPO / GF["svg"]).read_text()
REC = json.loads((REPO / "active/approved-cad-v4/reports/FP-4B-FF_V4_record.json").read_text())
PXM = REC["calibration"]["px_per_m"]          # 29.356 native px per metre (approx_calibrated)
SRC = cv2.imread(str(REPO / FF["source_crop"]))
assert SRC.shape[:2] == (1000, 650)

# ---------- palette (from the GF V4 template) ----------
C = dict(plot="#e3dfcf", plotline="#8d9582", grass="#9caf73", floor="#e7dfd0", wet="#dce4df",
         poche="#34403e", fine="#737e78", plate="#eee7d8", ink="#263a34", dim="#3c4c43", warn="#886c3a",
         bed="#ebe0cb", dress="#e3d8c2", core="#d3d8d2", balc="#d9d3c1", void="#f6f4ee", stair="#e9e5d9")

# ---------- zones (native source px, read from V4 wall poche + source line-art) ----------
Z = [  # name, kind, x0,y0,x1,y1
 ("balc_top","balc",151,143,511,195), ("master","bed",151,199,267,348), ("family","floor",272,199,390,348),
 ("bed1","bed",395,199,511,364), ("corridor","floor",272,348,370,643), ("corr_lift","floor",370,348,424,422),
 ("lift","core",374,354,420,402), ("bath1","wet",424,367,511,418), ("mdress","dress",151,350,267,452),
 ("mbath","wet",151,458,267,538), ("stair","stair",273,398,315,592), ("bath2","wet",151,545,198,619),
 ("dress","dress",199,545,251,619), ("bed2pass","bed",251,545,267,621), ("bed2","bed",151,621,264,747),
 ("balc_ll","balc",158,750,268,790), ("otb1","void",272,643,369,738), ("otb2","void",272,740,369,779),
 ("junior","bed",378,560,511,760), ("jdress","dress",378,558,437,610), ("jbath","wet",440,558,511,638),
 ("balc_lr","balc",378,764,511,840),
]
KIND_FILL = dict(floor=C["floor"], bed=C["bed"], dress=C["dress"], wet=C["wet"], core=C["core"],
                 balc=C["balc"], void=C["void"], stair=C["stair"])

# ---------- room labels: brochure transcripts as in V4 (name, dims, cx, cy) ----------
# dims strings copied from the V4 FF label layer (sourced); † = V4 disagreement flag.
# parsed from the V4 FF label layer (bold 6.3 name + 5.3 dims); positions and values are V4's, not new.
_V4L = re.findall(r'<text x="([\d.]+)" y="([\d.]+)" font-family="sans-serif" font-size="6.3"[^>]*font-weight="bold">([^<]+)</text>\s*'
                  r'<text x="[\d.]+" y="[\d.]+" font-family="sans-serif" font-size="5.3"[^>]*>([^<]+)</text>', V4)
LAB = []
for x_, y_, nm, dm in _V4L:
    nums = [float(t) for t in re.findall(r"\d+\.\d+", dm)]; assert len(nums) == 2, dm
    LAB.append((nm, tuple(nums), "†" if "†" in dm else "", float(x_), float(y_)))
assert len(LAB) == 14, LAB
OUT_LAB = [("BALCONY","UNKNOWN",331,170), ("BALCONY","UNKNOWN",213,770), ("BALCONY","UNKNOWN",444,812),
           ("OPEN TO BELOW","GF DOUBLE-HEIGHT ENTRY",320,692), ("OPEN TO BELOW","",320,760),
           ("OPEN TO COURTYARD BELOW","",447,540), ("SWIMMING POOL · GF","9.50 × 2.40 m",284,103)]
# raster text in the source crop that is replaced by the vector labels above (native px boxes)
TEXT_MASK_FIXED = [(150,312,262,335),(282,312,382,335),(415,322,505,345),(170,392,250,412),(170,470,250,490),
 (322,530,370,552),(378,370,418,392),(440,380,505,398),(150,585,200,605),(205,585,260,605),(205,630,262,650),
 (385,584,440,606),(455,584,510,606),(398,646,470,668),(305,163,355,180),(185,762,240,780),(415,808,465,825),
 (295,695,350,712),(295,764,350,782),(205,110,305,138),(130,950,230,972),(285,950,380,972),(525,950,615,972),
 (108,870,145,884),(190,870,228,884)]

TEXT_MASK = TEXT_MASK_FIXED + [(int(cx-30), int(cy-16), int(cx+30), int(cy+14)) for _,_,_,cx,cy in LAB]
# ---------- derive measured lines from the V4 wall poche ----------
walls = re.findall(r'<ns0:g[^>]*id="(?:source_wall_poche|structural_poche_visibility_restore)".*?</ns0:g>', V4, re.S)
assert len(walls) == 2
def denorm(s): return s.replace("ns0:", "").replace(' xmlns:ns0="http://www.w3.org/2000/svg"', "")
walls = [denorm(w).replace('fill="#35463c"', f'fill="{C["poche"]}"').replace('stroke="#35463c"', f'stroke="{C["poche"]}"') for w in walls]
wsvg = f'<svg xmlns="http://www.w3.org/2000/svg" width="2600" height="4000" viewBox="0 0 650 1000"><rect width="650" height="1000" fill="white"/>{"".join(walls)}</svg>'
WM = cv2.imdecode(np.frombuffer(cairosvg.svg2png(bytestring=wsvg.encode()), np.uint8), 0) < 128
S = 4
def wall_runs(axis, a0, a1):
    v = WM[a0*S:a1*S, :].mean(0) if axis == "x" else WM[:, a0*S:a1*S].mean(1)
    on = v >= 0.6; out = []; i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]: j += 1
            out.append((i/S, j/S)); i = j
        else: i += 1
    return out
MEAS = dict(cols_y220_330=wall_runs("x",220,330), cols_y660_740=wall_runs("x",660,740),
            rows_x160_175=wall_runs("y",160,175), rows_x470_490=wall_runs("y",470,490))
def centre(runs, lo, hi):
    c = [ (a+b)/2 for a,b in runs if lo <= (a+b)/2 <= hi ]; assert c, (lo,hi,runs); return c[0]

# envelope / site from the V4 guide lines (sourced V4 graphics)
ENV = dict(x0=138, x1=523, y0=141, y1=844); SITE = dict(x0=54, x1=607, y0=55, y1=932)
X_TOP = [SITE["x0"], ENV["x0"], centre(MEAS["cols_y220_330"],260,280), centre(MEAS["cols_y220_330"],385,400), ENV["x1"], SITE["x1"]]
X_BOT = [SITE["x0"], ENV["x0"], centre(MEAS["cols_y660_740"],260,275), centre(MEAS["cols_y660_740"],365,380), ENV["x1"], SITE["x1"]]
rl = MEAS["rows_x160_175"]; rr = MEAS["rows_x470_490"]
Y_L = [SITE["y0"], ENV["y0"], 197, centre(rl,340,355), centre(rl,450,460), centre(rl,535,548), centre(rl,615,625), centre(rl,744,752), 790, SITE["y1"]]
Y_R = [SITE["y0"], ENV["y0"], 197, centre(rr,360,370), centre(rr,415,430), 556, centre(rr,635,645), 761.5, ENV["y1"], SITE["y1"]]

def m(px): return px / PXM
def fmt(v): return f"≈ {v:.1f} m"
DIMLOG = []

# ---------- line-art from the untouched source crop ----------
R = cv2.resize(SRC, (650*S, 1000*S), interpolation=cv2.INTER_CUBIC).astype(np.float32)
b, g, r = R[...,0], R[...,1], R[...,2]
lum = 0.299*r + 0.587*g + 0.114*b
bg = cv2.GaussianBlur(lum, (0,0), S*4)
line = (lum < bg - 14) & (lum < 215) & ~((g - r > 6) & (g - b > 10))
line &= ~cv2.dilate(WM.astype(np.uint8), np.ones((5,5), np.uint8)).astype(bool)
for x0,y0,x1,y1 in TEXT_MASK: line[y0*S:y1*S, x0*S:x1*S] = False
line[1100*S:, :] = False
# drop vegetation outlines outside the envelope (replaced by template-style trees); keep paving/cars/pool edge
outside = np.ones_like(line); outside[ENV["y0"]*S-12:ENV["y1"]*S+12, ENV["x0"]*S-12:ENV["x1"]*S+12] = False
car = np.zeros_like(line); car[780*S:910*S, 105*S:260*S] = True
poolz = np.zeros_like(line); poolz[85*S:150*S, 140*S:440*S] = True
line &= ~(outside & ~car & ~poolz)
line = cv2.morphologyEx(line.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2,2), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(line, 8)
keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 10
line = keep[lab].astype(np.uint8)
cs, hier = cv2.findContours(line, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
def cpath(c):
    c = cv2.approxPolyDP(c, 0.6, True).reshape(-1, 2) / S
    return "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in c) + "Z"
LINEART = "".join(cpath(c) for c in cs if len(c) >= 3)

# ---------- svg helpers ----------
E = []
def add(s): E.append(s)
def rect(x,y,w,h,fill,stroke="none",sw=0.6,rx=0,extra=""): add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
def text(x,y,s,size,fill=C["ink"],anchor="middle",weight="normal",extra=""): add(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT(s)}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}" {extra}>{s}</text>')
def line_(x1,y1,x2,y2,stroke,sw,op=1,extra=""): add(f'<path d="M{x1:.2f},{y1:.2f}L{x2:.2f},{y2:.2f}" stroke="{stroke}" stroke-width="{sw}" fill="none" opacity="{op}" {extra}/>')

def FONT(s): return 'DejaVu Sans, sans-serif' if ('≈' in s or '≠' in s) else 'sans-serif'
rnd = random.Random(4)
defs = ['<linearGradient id="pool" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#78bacf"/><stop offset=".5" stop-color="#9cd0df"/><stop offset="1" stop-color="#66a9c4"/></linearGradient>',
        '<linearGradient id="seat" x1="0" x2="1"><stop stop-color="#d9cdbb"/><stop offset=".4" stop-color="#eee6d8"/><stop offset="1" stop-color="#c9bba7"/></linearGradient>',
        '<linearGradient id="car" x1="0" x2="1"><stop stop-color="#e0e3df"/><stop offset=".4" stop-color="#fffef7"/><stop offset=".7" stop-color="#f0f1e9"/><stop offset="1" stop-color="#c8d1cc"/></linearGradient>',
        '<radialGradient id="tree"><stop stop-color="#8b9d49"/><stop offset=".55" stop-color="#617e35"/><stop offset="1" stop-color="#344f26"/></radialGradient>',
        '<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0,0L0,6" stroke="#c9c2b0" stroke-width="0.5"/></pattern>']

# ---------- 1 site base + paving ----------
sx, sy, sw_, sh = SITE["x0"], SITE["y0"], SITE["x1"]-SITE["x0"], SITE["y1"]-SITE["y0"]
rect(sx, sy, sw_, sh, C["plot"], C["plotline"], 0.8)
defs.append(f'<clipPath id="siteclip"><rect x="{sx}" y="{sy}" width="{sw_}" height="{sh}"/></clipPath>')
add('<g clip-path="url(#siteclip)">')
for x in range(sx, SITE["x1"], 16): line_(x, sy, x, SITE["y1"], "#c3c0ad", 0.4)
for y in range(sy, SITE["y1"], 16): line_(sx, y, SITE["x1"], y, "#c3c0ad", 0.4)
add('</g>')
# landscape strips (positions read from green areas of the source crop)
GRASS = [(60,62,40,498),(100,590,38,150),(500,60,100,40),(556,100,44,260),(556,542,47,322),(364,888,141,38)]
for x,y,w,h in GRASS: rect(x,y,w,h,C["grass"])
# pool (GF level, visible past the FF balcony) — V4 pool frame 146,90,277,53
rect(145,89,279,55,"#e9e8d4","#829b96",0.75); rect(146,90,277,53,"url(#pool)","#4a879e",1)
for k in range(5): add(f'<path d="M146,{95+k*10}Q284.5,{93+k*10} 423,{95+k*10}" fill="none" stroke="#d1e8e9" stroke-width="0.35" opacity=".8"/>')
# courtyard below (V4 courtyard frame 389,428,129,107) — water + tree + planter, GF style
rect(378,422,140,131,"#dddccc"); rect(389,428,129,107,"url(#pool)","#88a5a2",0.6)
for k in range(6): add(f'<path d="M389,{434+k*17}Q453.5,{432+k*17} 518,{434+k*17}" fill="none" stroke="#d1e8e9" stroke-width="0.35" opacity=".8"/>')
add('<circle cx="450" cy="481" r="36" fill="url(#tree)"/>')
for _ in range(40):
    a = rnd.uniform(0, 2*math.pi); d = 30*math.sqrt(rnd.random()); rr_ = rnd.uniform(2.5, 5.5)
    add(f'<circle cx="{450+d*math.cos(a):.1f}" cy="{481+d*math.sin(a):.1f}" r="{rr_:.1f}" fill="{rnd.choice(["#546f31","#93a35d","#6f8a3c","#425f2c"])}"/>')
rect(430,461,40,40,"#e0d9c3","#677b62",0.7); rect(435,466,30,30,"#a6b28d","#6c7b5b",0.5)

# ---------- 2 zone fills + illustrative finishes ----------
for name, kind, x0,y0,x1,y1 in Z:
    rect(x0, y0, x1-x0, y1-y0, KIND_FILL[kind])
    cid = f"clip_{name}"; defs.append(f'<clipPath id="{cid}"><rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}"/></clipPath>')
    add(f'<g clip-path="url(#{cid})">')
    if kind == "floor":
        for x in range(x0, x1, 18): line_(x,y0,x,y1,"#bfb5a2",0.33,0.72)
        for y in range(y0, y1, 18): line_(x0,y,x1,y,"#bfb5a2",0.33,0.72)
    elif kind in ("bed","dress"):
        for y in range(y0, y1, 5): line_(x0,y,x1,y,"#d6c7aa" if kind=="bed" else "#cfc2a6",0.3,0.8)
    elif kind == "wet":
        for x in range(x0, x1, 9): line_(x,y0,x,y1,"#bfcbc5",0.3)
        for y in range(y0, y1, 9): line_(x0,y,x1,y,"#bfcbc5",0.3)
    elif kind == "balc":
        for x in range(x0, x1, 12): line_(x,y0,x,y1,"#bdb59f",0.35)
        for y in range(y0, y1, 12): line_(x0,y,x1,y,"#bdb59f",0.35)
    elif kind == "void":
        rect(x0,y0,x1-x0,y1-y0,"url(#hatch)")
    elif kind == "stair":
        pass
    add('</g>')

# ---------- 3 V4 furniture symbols (copied verbatim from the V4 FF SVG, rugs/beds/sofa/table) ----------
i0 = V4.find('<rect x="156" y="226" width="89"'); i1 = V4.find('<g opacity="0.3">')
furn = V4[i0:i1]
furn = re.sub(r'<(ns0:)?path[^>]*stroke="#c9bfaa"[^>]*/>', '', furn)  # drop V4 rug stripe hairlines (kept rug panels)
add(denorm(furn))

# ---------- 4 source line-art (doors, swings, stairs, fixtures, glazing, balustrades) ----------
add(f'<path id="source_lineart_doors_stairs_fixtures" d="{LINEART}" fill="{C["fine"]}" fill-rule="evenodd" stroke="{C["fine"]}" stroke-width="0.12"/>')

# ---------- 5 cars (GF template symbol, scaled to FF calibration) and trees ----------
car_g = re.search(r'<g transform="translate\(164,754\)">(.*?)</g>', GFS, re.S).group(1)
k = PXM / 28.145127436281857  # FF px/m over GF px/m (independent_calibration.json)
for tx, ty in ((112, 786), (198, 788)):
    add(f'<g transform="translate({tx},{ty}) scale({k:.4f})">{car_g}</g>')
for idx, grp in enumerate(re.findall(r'<g opacity="0.3">(.*?)</g>', V4, re.S)):
    cc = [tuple(map(float, t)) for t in re.findall(r'cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', grp)]
    xs = [a for a,_,_ in cc]; ys = [b_ for _,b_,_ in cc]
    cx, cy = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2; rad = max(max(xs)-min(xs), max(ys)-min(ys))/2
    defs.append(f'<clipPath id="tree{idx}"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad:.1f}"/></clipPath>')
    add(f'<circle cx="{cx+2:.1f}" cy="{cy+3:.1f}" r="{rad:.1f}" fill="#82945d" opacity=".55"/>')
    add(f'<g clip-path="url(#tree{idx})"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad:.1f}" fill="url(#tree)"/>')
    for _ in range(60):
        a = rnd.uniform(0, 2*math.pi); d = rad*math.sqrt(rnd.random()); rr_ = rnd.uniform(3.5, 7)
        x_, y_ = cx+d*math.cos(a), cy+d*math.sin(a)
        add(f'<circle cx="{x_+1:.1f}" cy="{y_+1:.1f}" r="{rr_:.1f}" fill="#425f2c"/><circle cx="{x_:.1f}" cy="{y_:.1f}" r="{rr_:.1f}" fill="{rnd.choice(["#93a35d","#546f31","#6f8a3c","#7f9748"])}"/>')
    add('</g>')

# ---------- 6 walls (V4 source poche, verbatim geometry) ----------
for w in walls: add(w)

# ---------- 7 labels ----------
def plate(cx, cy, l1, l2, l3="", s1=7, s2=6.1):
    wch = max(len(l1)*s1*0.62, len(l2)*s2*0.56, len(l3)*5.2*0.56) + 6
    h = 15 + (7 if l3 else 0)
    rect(cx-wch/2, cy-7, wch, h, C["plate"], "#cfc5b0", 0.3)
    text(cx, cy-0.5, l1, s1, weight="bold"); text(cx, cy+6.5, l2, s2)
    if l3: text(cx, cy+13, l3, 5.2, fill="#6b6a55")
for name,(w,d),flag,cx,cy in LAB:
    plate(cx, cy+1, name, f"{w:.2f} × {d:.2f} m{(' '+flag) if flag else ''}", f"A {w*d:.2f} m²", s1=6.6 if len(name)>10 else 7)
for l1,l2,cx,cy in OUT_LAB:
    if l2: plate(cx, cy, l1, l2, s1=5.8, s2=5.0)
    else:
        wch = len(l1)*5.8*0.62+6; rect(cx-wch/2, cy-6, wch, 9, C["plate"], "#cfc5b0", 0.3); text(cx, cy+1, l1, 5.8, weight="bold")
for s, x in (("VEHICULAR ENTRANCE",180),("PEDESTRIAN ENTRANCE",333),("SERVICE ENTRANCE",570)):
    text(x, 962, s, 6.2, fill="#5c7161"); add(f'<path d="M{x-4},{952}L{x},{945}L{x+4},{952}Z" fill="#b9ae8f"/>')

# ---------- 8 dimension chains (≈ derived from V4 calibration) ----------
def hchain(xs, y, tag):
    line_(xs[0], y, xs[-1], y, C["dim"], 0.55)
    for x in xs:
        line_(x, y-5, x, y+5, C["dim"], 0.4); line_(x-2.5, y+2.5, x+2.5, y-2.5, C["dim"], 0.8)
    for a, b_ in zip(xs, xs[1:]):
        v = m(b_-a); text((a+b_)/2, y-3, fmt(v), 6.6, fill=C["dim"]); DIMLOG.append((tag, f"x {a:.1f}→{b_:.1f}", round(b_-a,1), round(v,2)))
def vchain(ys, x, tag):
    line_(x, ys[0], x, ys[-1], C["dim"], 0.55)
    for y in ys:
        line_(x-5, y, x+5, y, C["dim"], 0.4); line_(x-2.5, y+2.5, x+2.5, y-2.5, C["dim"], 0.8)
    for a, b_ in zip(ys, ys[1:]):
        v = m(b_-a); cy = (a+b_)/2
        text(x-3, cy, fmt(v), 6.6, fill=C["dim"], extra=f'transform="rotate(-90 {x-3:.2f} {cy:.2f})"'); DIMLOG.append((tag, f"y {a:.1f}→{b_:.1f}", round(b_-a,1), round(v,2)))
def overall_h(x0, x1, y, label, col):
    line_(x0, y, x1, y, col, 0.6); line_(x0-2,y+2,x0+2,y-2,col,0.8); line_(x1-2,y+2,x1+2,y-2,col,0.8)
    line_(x0, y-4, x0, y+4, col, 0.4); line_(x1, y-4, x1, y+4, col, 0.4); text((x0+x1)/2, y-3, label, 7.4, fill=col)
def overall_v(y0, y1, x, label, col):
    line_(x, y0, x, y1, col, 0.6); line_(x-2,y0+2,x+2,y0-2,col,0.8); line_(x-2,y1+2,x+2,y1-2,col,0.8)
    line_(x-4, y0, x+4, y0, col, 0.4); line_(x-4, y1, x+4, y1, col, 0.4); cy=(y0+y1)/2
    text(x-3, cy, label, 7.4, fill=col, extra=f'transform="rotate(-90 {x-3:.2f} {cy:.2f})"')
hchain(X_TOP, 30, "top chain"); hchain(X_BOT, 980, "bottom chain")
vchain(Y_L, 36, "left chain"); vchain(Y_R, 625, "right chain")
overall_h(SITE["x0"], SITE["x1"], 10, "SITE DIAGRAM ~ 18.8 m (V4)", "#9a8358"); overall_h(SITE["x0"], SITE["x1"], 997, "SITE DIAGRAM ~ 18.8 m (V4)", "#9a8358")
overall_v(SITE["y0"], SITE["y1"], 14, "SITE DIAGRAM ~ 29.9 m (V4)", "#9a8358"); overall_v(SITE["y0"], SITE["y1"], 647, "SITE DIAGRAM ~ 29.9 m (V4)", "#9a8358")
overall_h(ENV["x0"], ENV["x1"], 123, "ENVELOPE ~ 13.1 m (V4)", "#697b6d"); overall_h(ENV["x0"], ENV["x1"], 862, "ENVELOPE ~ 13.1 m (V4)", "#697b6d")
overall_v(ENV["y0"], ENV["y1"], 120, "ENVELOPE ~ 23.9 m (V4)", "#697b6d"); overall_v(ENV["y0"], ENV["y1"], 541, "ENVELOPE ~ 23.9 m (V4)", "#697b6d")
text(330.5, 1010, "≈ CHAIN SPANS: CALIBRATION-DERIVED (V4 RECORD 29.36 px/m), WALL CENTRELINES · NOT A VERIFIED PLOT SURVEY", 6.2, fill=C["warn"])

PLAN = "\n".join(E)
TR = re.search(r'<g id="source_diagram" transform="([^"]+)"', V4).group(1)

# ---------- page ----------
P = []
def pt(x,y,s,size,fill=C["ink"],anchor="start",weight="normal"): P.append(f'<text x="{x}" y="{y}" font-family="{FONT(s)}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}">{s}</text>')
def pr(x,y,w,h,fill,stroke="none",sw=0.5,extra=""): P.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
pt(40,33,"ASHWOOD ESTATES",20,weight="bold"); pt(40,55,"4-BEDROOM VILLA  /  FIRST FLOOR",11)
pt(965,33,"ENHANCED PRESENTATION · FF-E1",9,"#7b725e","end"); pt(965,52,"SOURCE WALLS · ILLUSTRATIVE FINISHES",8,"#7b725e","end")
P.append('<path d="M40,66L965,66" stroke="#52645a" stroke-width="0.8" fill="none"/>')
pt(502,79,"CONCEPT VISUALISATION · NOT SURVEY-VERIFIED · NOT CONSTRUCTION-READY · NOT CERTIFIED CAD",7.2,C["warn"],"middle","bold")
# legend + schedule column
LX, LY = 836, 150
pr(LX-8, LY-22, 144, 318, "#fffef9", "#aab49e", 0.7)
pt(LX, LY-4, "LEGEND", 10, weight="bold")
items = [(C["floor"],"Living / circulation"),(C["bed"],"Bedrooms / suites"),(C["dress"],"Dressing"),(C["wet"],"Wet zones"),
         (C["core"],"Lift / core"),(C["balc"],"Balcony (outdoor)"),("url(#hatchL)","Open to below (void)"),(C["stair"],"Stair"),
         ("#d7cbb8","Illustrative furniture"),("#7e994a","Source landscape"),("#8ec6d9","Source water (GF, below)"),(C["poche"],"Source wall poche")]
for i_,(f,t) in enumerate(items):
    y = LY + 8 + i_*19; pr(LX, y, 12, 12, f, "#91a085", 0.4); pt(LX+19, y+10, t, 7.1)
y = LY + 8 + len(items)*19 + 4
P.append(f'<path d="M{LX},{y}L{LX+124},{y}" stroke="#aab49e" stroke-width="0.5"/>')
pt(LX, y+20, "FIRST FLOOR (V4 legend)", 7.8, weight="bold"); pt(LX, y+40, "260.19 m²", 12, weight="bold")
# area schedule
AY = LY + 312
pr(LX-8, AY, 144, 30 + len(LAB)*14 + 40, "#fffef9", "#aab49e", 0.7)
pt(LX, AY+16, "ROOM SCHEDULE", 9, weight="bold"); pt(LX, AY+26, "brochure label w × d · A = w × d (arithmetic)", 5.4, "#6b6a55")
for i_,(name,(w,d),flag,_,_) in enumerate(LAB):
    yy = AY + 40 + i_*14
    if i_ % 2 == 0: pr(LX-4, yy-9, 136, 14, "#f3efe5")
    pt(LX, yy, name.title().replace("M. ","M. ").replace("J. ","J. "), 6.3)
    pt(LX+78, yy, f"{w:.2f}×{d:.2f}{flag}", 6.0, anchor="end" if False else "start")
    pt(LX+130, yy, f"{w*d:.1f}", 6.3, anchor="end", weight="bold")
yy = AY + 40 + len(LAB)*14 + 6
pt(LX, yy, "Balconies: UNKNOWN (no source dims)", 5.8, C["warn"]); pt(LX, yy+11, "† = V4 source disagreement flag", 5.8, C["warn"])
pt(LX, yy+22, "Sum of labels ≠ floor area (walls/circulation)", 5.4, "#6b6a55")
# scale bar (V4 FF geometry: 5 m = 50 mm at A3 → 168.35 units)
SB = 1000/297*10
for i_ in range(5): pr(60+i_*SB, 1270, SB, 6, "#354b3d" if i_%2==0 else "white", "#354b3d", 0.5)
for i_ in range(6): pt(60+i_*SB, 1288, f"{i_}{' m' if i_==5 else ''}", 9, anchor="middle")
pt(60,1262,"APPROX. 1:100 · A3 PORTRAIT · PRINT 100% / ACTUAL SIZE",10.5,weight="bold")
notes = [("≈ values are calibration-derived spans (V4 record 29.36 px/m, ±3% working allowance), wall centreline to centreline; not source-stated.",C["warn"]),
         ("~ values are the V4 site-diagram / envelope guides. Room dimensions transcribe brochure p28 labels as in V4; † flags disagreement. Plot boundary is not verified.","#5e715f"),
         ("Walls are the V4 source poche (unchanged geometry). Doors, swings, stairs and fixtures are traced from the brochure p28 board crop.","#5e715f"),
         ("Zone fills, finishes, furniture, trees and cars are illustrative, not design facts.","#5e715f"),
         ("CONCEPT VISUALISATION · NOT SURVEY-VERIFIED · NOT CONSTRUCTION-READY · NOT CERTIFIED CAD · Enhanced from V4 FP-4B-FF; style per FP-4B-GF V4 presentation prototype 04.","#7a806e")]
for i_,(t,c) in enumerate(notes): pt(60, 1314+i_*15, t, 7.4, c)

DEFS = "\n".join(defs) + '<pattern id="hatchL" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="4" fill="#f6f4ee"/><path d="M0,0L0,4" stroke="#b9b29f" stroke-width="0.6"/></pattern>'
SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="420mm" viewBox="0 0 1000 1414.141414141414">
<!-- Ashwood 4B-FF ENHANCED presentation plan FF-E1. Concept visualisation, not survey-verified, not construction-ready, not certified CAD. Built by production-line/enhanced-plans/4b-ff/scripts/build_enhanced_ff.py -->
<defs>{DEFS}</defs>
<rect x="0" y="0" width="1000" height="1414.141414141414" fill="white"/>
{''.join(P)}
<g id="source_diagram" transform="{TR}">
{PLAN}
</g>
</svg>'''
name = "FP-4B-FF_ENHANCED_FF-E1_portrait"
(OUT / f"{name}.svg").write_text(SVG)
cairosvg.svg2pdf(bytestring=SVG.encode(), write_to=str(OUT / f"{name}.pdf"))
cairosvg.svg2png(bytestring=SVG.encode(), write_to=str(OUT / "FP-4B-FF_ENHANCED_FF-E1_preview.png"), output_width=1600)
cairosvg.svg2png(bytestring=SVG.encode(), write_to=str(OUT / "FP-4B-FF_ENHANCED_FF-E1_hires3400.png"), output_width=3400)
cv2.imwrite(str(OUT/'qa'/'_barrier4x.png'), ((line>0)|WM).astype(np.uint8)*255)
json.dump(dict(zones=Z, transform=TR, px_per_m=PXM, X_TOP=X_TOP, X_BOT=X_BOT, Y_L=Y_L, Y_R=Y_R, dims=DIMLOG, meas=MEAS,
               inputs={FF["svg"]: FF["sha256"]["svg"], GF["svg"]: GF["sha256"]["svg"], FF["source_crop"]: sha(FF["source_crop"])}),
          open(OUT / "qa" / "build_log.json", "w"), indent=1, default=str) if (OUT / "qa").exists() else None
print("ok", len(SVG)//1024, "KB")
