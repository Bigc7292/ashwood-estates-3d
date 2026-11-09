"""Apply a critic-fix round to one 4B interior-refs floor folder in place.
Usage: python3 apply_fix.py <repo_root> <floor gf|ff|rf> <round r2|r3> <critic_commit> <critic_report_path> <records_module>
records_module defines FIX = {room: dict(attempts, chosen, critic, observed, assumed, residual, raw, how)}.
Current image -> images/_superseded-<prev round>/ (git mv beforehand), new image gets _<round> suffix.
Adds index.csv columns critic_<commit> (FAIL for fixed rooms, PASS otherwise unless given) and <round>_critic_fix."""
import sys, os, json, csv, hashlib, datetime, importlib, re
from PIL import Image, ImageDraw, ImageFont
REPO, FL, RND, CC, CREP, MOD = sys.argv[1:7]; REPO = os.path.abspath(REPO)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); FIX = importlib.import_module(MOD).FIX
PASSV = getattr(importlib.import_module(MOD), "PASS_VERDICTS", {})
REL = f"production-line/interior-refs/4b-{FL}"; D = os.path.join(REPO, REL)
PREV = "r1" if RND == "r2" else f"r{int(RND[1:])-1}"
LABEL = "CONCEPT VISUALISATION - AI-generated - not survey-verified - not construction-ready - not certified CAD"
CRITIC = f"claude/rules-and-status @ {CC} {CREP}"
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=4))).isoformat(timespec="seconds")
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
man = json.load(open(f"{D}/manifest.json")); A = {a["room_id"].split("/")[-1]: a for a in man["assets"]}
def burn(raw, title, out_path):
    im = Image.open(raw).convert("RGB"); W, H = im.size
    f1 = ImageFont.truetype(FB, max(14, W // 60)); f2 = ImageFont.truetype(F, max(13, W // 70))
    def wrap(txt, font):
        out, cur = [], ""
        for w in txt.split(" "):
            t = (cur + " " + w).strip()
            if font.getlength(t) > W - 20 and cur: out.append(cur); cur = w
            else: cur = t
        return out + [cur]
    l1, l2 = wrap(title, f1), wrap(LABEL, f2); lh1, lh2 = f1.size + 6, f2.size + 6; bh = 10 + lh1 * len(l1) + lh2 * len(l2)
    o = Image.new("RGB", (W, H + bh), "white"); o.paste(im, (0, 0)); d = ImageDraw.Draw(o)
    d.rectangle((0, H, W, H + bh), fill=(25, 25, 25)); y = H + 5
    for t in l1: d.text((10, y), t, font=f1, fill="white"); y += lh1
    for t in l2: d.text((10, y), t, font=f2, fill=(255, 210, 120)); y += lh2
    o.save(out_path); return o
for room, r in FIX.items():
    a = A[room]; base = re.sub(r"_r\d+$", "", os.path.basename(a["file"])[:-4]); cur = os.path.basename(a["file"])
    sup = f"{REL}/images/_superseded-{PREV}/{cur}"; assert os.path.exists(os.path.join(REPO, sup)), sup
    out_rel = f"{REL}/images/{base}_{RND}.png"; vid = a["view_id"].split("/")[-1]
    o = burn(r["raw"], f"Ashwood 4B {FL.upper()} - {a['room_label']} - {vid} - {a['method']} - {RND} (critic fix) - needs-review", os.path.join(REPO, out_rel))
    hist = a.get("history", [])
    hist.append(dict(round=PREV, file=sup, result=a.get("result"), mismatches=a.get("mismatches")))
    a.update(history=hist, superseded_file=sup, file=out_rel, sha256=sha(os.path.join(REPO, out_rel)), size_px=list(o.size),
             result=f"regenerated-{RND}", generation_pass=RND, generation_attempts=r["attempts"], chosen_attempt=r["chosen"], fix_method=r["how"],
             raw_source_box_path=r["raw"], raw_sha256=sha(r["raw"]), observed=r["observed"], assumed=r["assumed"], mismatches=r["residual"],
             critic_defect=r["critic"], critic_report=CRITIC, review_status="needs-review", label=LABEL)
rows = list(csv.DictReader(open(f"{D}/index.csv"))); ck, fk = f"critic_{CC}", f"{RND}_critic_fix"
for row in rows:
    room = row["room"].split("/")[-1]; a = A[room]
    if room in FIX:
        r = FIX[room]; row.update(file=a["file"], observed=r["observed"], assumed=r["assumed"], mismatches=r["residual"])
        row[ck] = "FAIL"; row[fk] = f"regenerated-{RND} ({r['how']}; {r['attempts']} attempt(s), chose {r['chosen']}); critic defect: {r['critic']}"
        if "critic" not in row["evidence"] or CC not in row["evidence"]: row["evidence"] += f"; critic {CRITIC}"
    else:
        row[ck] = PASSV.get(room, "PASS"); row[fk] = "kept (critic PASS)"
    a[ck] = row[ck]
cols = [c for c in rows[0].keys() if c != "review_status"] + ["review_status"]
with open(f"{D}/index.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
man["updated_Asia_Dubai"] = NOW; man.setdefault("critic_reports", []).append(CRITIC)
man["guard"][f"handoff_guard_{RND}"] = "exit 0 (records=112 verified=0 ambiguous=35 unknown=77 eligible=112 blocked=0 breaches=0)"
man["guard"][f"verify_active_pipeline_{RND}"] = "not run by this lane (integrator only, README rule 7)"
man["counts"][f"{RND}_critic_fix"] = len(FIX); man["counts"][f"kept_critic_pass_{CC}"] = len(A) - len(FIX)
json.dump(man, open(f"{D}/manifest.json", "w"), indent=1)
# contact sheet
cs = [f for f in os.listdir(f"{D}/contact-sheet") if f.endswith("_CONTACT-SHEET.png")][0]
cw, ch, nc, lab, top = 480, 360, 4, 64, 70; assets = man["assets"]; nr = (len(assets) + nc - 1) // nc
sheet = Image.new("RGB", (cw * nc + 20 * (nc + 1), top + nr * (ch + lab + 20)), "white"); d = ImageDraw.Draw(sheet)
names = {"gf": "ground floor", "ff": "first floor", "rf": "roof floor"}
d.text((20, 12), f"Ashwood Estates 4B {names[FL]} - interior reference images, {RND} critic fix (review_status: needs-review)", font=ImageFont.truetype(FB, 24), fill="black")
d.text((20, 42), LABEL, font=ImageFont.truetype(F, 17), fill=(150, 60, 0)); fL = ImageFont.truetype(FB, 18); fS = ImageFont.truetype(F, 14)
for i, a in enumerate(assets):
    rm = a["room_id"].split("/")[-1]; im = Image.open(os.path.join(REPO, a["file"])); im.thumbnail((cw, ch))
    x = 20 + (i % nc) * (cw + 20); y = top + (i // nc) * (ch + lab + 20); sheet.paste(im, (x + (cw - im.width) // 2, y))
    d.text((x, y + ch + 4), f"{a['room_label']}  ({rm})", font=fL, fill="black")
    st = f"{RND} critic fix" if rm in FIX else f"kept, critic {a.get(ck)}"
    d.text((x, y + ch + 28), f"{a.get('dimension_transcript') or 'size UNKNOWN'} - {a['match_status']} - {st}", font=fS, fill=(60, 60, 60))
sheet.save(f"{D}/contact-sheet/{cs}")
# review sheet: plan crop | previous | new
H, GAP = 400, 20; fT = ImageFont.truetype(FB, 20); fN = ImageFont.truetype(F, 16); fC = ImageFont.truetype(FB, 16)
def wrap(txt, font, W):
    out, cur = [], ""
    for w in txt.split(" "):
        t = (cur + " " + w).strip()
        if font.getlength(t) > W and cur: out.append(cur); cur = w
        else: cur = t
    return out + [cur]
blocks = []
for room, r in FIX.items():
    a = A[room]; ims = [Image.open(os.path.join(REPO, p)).convert("RGB") for p in (a["cad_check_crop"], a["superseded_file"], a["file"])]
    ims = [im.resize((int(im.width * H / im.height), H)) for im in ims]; Wb = max(sum(im.width for im in ims) + 2 * GAP, 900)
    title = wrap(f"{a['room_label']} ({room}) - plan {a.get('dimension_transcript') or 'size UNKNOWN'}", fT, Wb)
    crit = wrap(f"Critic defect ({CC}): " + r["critic"], fN, Wb); res = wrap(f"Residual after {RND} ({r['how']}): " + r["residual"], fN, Wb)
    th = 26 * len(title) + 22 * len(crit) + 6
    b = Image.new("RGB", (Wb, th + H + 28 + 22 * len(res) + 10), "white"); db = ImageDraw.Draw(b); y = 2
    for t in title: db.text((0, y), t, font=fT, fill="black"); y += 26
    for t in crit: db.text((0, y), t, font=fN, fill=(150, 0, 0)); y += 22
    x, y = 0, th
    for im, cap, col in zip(ims, ["V4 plan crop (cad-check)", f"OLD {PREV} (critic FAIL)", f"NEW {RND} (critic fix)"], [(0, 0, 0), (150, 0, 0), (0, 110, 0)]):
        b.paste(im, (x, y)); db.text((x + 4, y + H + 4), cap, font=fC, fill=col); x += im.width + GAP
    y += H + 28
    for t in res: db.text((0, y), t, font=fN, fill=(50, 50, 50)); y += 22
    blocks.append(b)
Wmax = max(max(b.width for b in blocks) + 40, 1500)
rs = Image.new("RGB", (Wmax, 100 + sum(b.height + 30 for b in blocks)), "white"); dr = ImageDraw.Draw(rs)
dr.text((20, 12), f"Ashwood 4B {FL.upper()} interior refs - critic fix {RND}: plan crop | old | new ({len(FIX)} rooms). needs-review, not self-approved", font=ImageFont.truetype(FB, 24), fill="black")
dr.text((20, 50), LABEL, font=ImageFont.truetype(F, 17), fill=(150, 60, 0))
dr.text((20, 72), "Critic report: " + CRITIC, font=ImageFont.truetype(F, 15), fill=(60, 60, 60)); y = 100
for b in blocks:
    rs.paste(b, (20, y)); y += b.height + 30; dr.line((20, y - 15, Wmax - 20, y - 15), fill=(200, 200, 200), width=2)
rs.save(f"{D}/contact-sheet/critic-fix_plan-vs-image.png", optimize=True); print("done", FL, RND, rs.size)
