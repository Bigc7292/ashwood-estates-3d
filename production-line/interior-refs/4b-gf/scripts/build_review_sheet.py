"""Build contact-sheet/critic-fix_plan-vs-image.png: V4 plan crop | old r1 | new r2 for the 9 critic-fix rooms.
Usage: python3 build_review_sheet.py <repo_root> (reads manifest.json after apply_r2.py)."""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r2_rooms import R2
REPO = os.path.abspath(sys.argv[1]); D = os.path.join(REPO, "production-line/interior-refs/4b-gf")
LABEL = "CONCEPT VISUALISATION - AI-generated - not survey-verified - not construction-ready - not certified CAD"
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
man = json.load(open(f"{D}/manifest.json")); A = {a["room_id"].split("/")[-1]: a for a in man["assets"]}
H = 400; GAP = 20; fT = ImageFont.truetype(FB, 20); fN = ImageFont.truetype(F, 16); fC = ImageFont.truetype(FB, 16)
def wrap(txt, font, W):
    out, cur = [], ""
    for w in txt.split(" "):
        t = (cur + " " + w).strip()
        if font.getlength(t) > W and cur: out.append(cur); cur = w
        else: cur = t
    return out + [cur]
blocks = []
for room, r in R2.items():
    a = A[room]
    ims = [Image.open(os.path.join(REPO, p)).convert("RGB") for p in (a["cad_check_crop"], a["superseded_file"], a["file"])]
    ims = [im.resize((int(im.width * H / im.height), H)) for im in ims]
    Wb = sum(im.width for im in ims) + 2 * GAP
    title = wrap(f"{a['room_label']} ({room}) - plan {a.get('dimension_transcript') or 'size UNKNOWN'}", fT, Wb)
    crit = wrap("Critic defect (1f58518): " + r["critic"], fN, Wb)
    res = wrap("Residual after r2 (" + r["chosen"] + ", " + str(r["attempts"]) + " attempt(s)): " + r["residual"], fN, Wb)
    th = 26 * len(title) + 22 * len(crit) + 6
    b = Image.new("RGB", (Wb, th + H + 28 + 22 * len(res) + 10), "white"); db = ImageDraw.Draw(b); y = 2
    for t in title: db.text((0, y), t, font=fT, fill="black"); y += 26
    for t in crit: db.text((0, y), t, font=fN, fill=(150, 0, 0)); y += 22
    x = 0; y = th
    for im, cap, col in zip(ims, ["V4 plan crop (cad-check)", "OLD r1 (critic FAIL)", "NEW r2 (critic fix)"], [(0, 0, 0), (150, 0, 0), (0, 110, 0)]):
        b.paste(im, (x, y)); db.text((x + 4, y + H + 4), cap, font=fC, fill=col); x += im.width + GAP
    y += H + 28
    for t in res: db.text((0, y), t, font=fN, fill=(50, 50, 50)); y += 22
    blocks.append(b)
Wmax = max(b.width for b in blocks) + 40
rs = Image.new("RGB", (Wmax, 100 + sum(b.height + 30 for b in blocks)), "white"); dr = ImageDraw.Draw(rs)
dr.text((20, 12), "Ashwood 4B GF interior refs - critic fix r2: plan crop | old | new (9 rooms). needs-review, not self-approved", font=ImageFont.truetype(FB, 26), fill="black")
dr.text((20, 50), LABEL, font=ImageFont.truetype(F, 17), fill=(150, 60, 0))
dr.text((20, 72), "Critic report: claude/rules-and-status @ 1f58518, production-line/critic/2026-11-10_q11-gf-refs.md", font=ImageFont.truetype(F, 15), fill=(60, 60, 60))
y = 100
for b in blocks:
    rs.paste(b, (20, y)); y += b.height + 30
    dr.line((20, y - 15, Wmax - 20, y - 15), fill=(200, 200, 200), width=2)
rs.save(f"{D}/contact-sheet/critic-fix_plan-vs-image.png", optimize=True); print(rs.size)
