"""Apply the r2 critic fix to production-line/interior-refs/4b-gf in place (9 rooms).
Usage: python3 apply_r2.py <repo_root>. Old r1 images must already be at images/_superseded-r1/."""
import sys, os, json, csv, hashlib, datetime
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r2_rooms import R2
REPO = os.path.abspath(sys.argv[1]); REL = "production-line/interior-refs/4b-gf"; D = os.path.join(REPO, REL)
RAW = "/workspace/irw/raw_r2"
LABEL = "CONCEPT VISUALISATION - AI-generated - not survey-verified - not construction-ready - not certified CAD"
CRITIC = "claude/rules-and-status @ 1f58518 production-line/critic/2026-11-10_q11-gf-refs.md"
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=4))).isoformat(timespec="seconds")
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
man = json.load(open(f"{D}/manifest.json")); A = {a["room_id"].split("/")[-1]: a for a in man["assets"]}
REFS = {"p15-living": "style-guide/refs/style-p15-living.png", "p17": "style-guide/refs/style-p17-materials_swatches.png"}
USES_P15 = {"office-gym", "living-dining"}

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
    l1, l2 = wrap(title, f1), wrap(LABEL, f2); lh1, lh2 = f1.size + 6, f2.size + 6
    bh = 10 + lh1 * len(l1) + lh2 * len(l2)
    o = Image.new("RGB", (W, H + bh), "white"); o.paste(im, (0, 0)); d = ImageDraw.Draw(o)
    d.rectangle((0, H, W, H + bh), fill=(25, 25, 25)); y = H + 5
    for t in l1: d.text((10, y), t, font=f1, fill="white"); y += lh1
    for t in l2: d.text((10, y), t, font=f2, fill=(255, 210, 120)); y += lh2
    o.save(out_path); return o

new_imgs = {}
for room, r in R2.items():
    a = A[room]; old_file = a["file"]; base = os.path.basename(old_file)[:-4]
    stem = base + "_r2"; vid = a["view_id"].split("/")[-1]
    raw = f"{RAW}/4b-gf-{room}_r2_RAW.jpg"
    out_rel = f"{REL}/images/{stem}.png"
    o = burn(raw, f"Ashwood 4B GF - {a['room_label']} - {vid} - {a['method']} - r2 (critic fix) - needs-review", os.path.join(REPO, out_rel))
    new_imgs[room] = o
    a.update(superseded_file=f"{REL}/images/_superseded-r1/{base}.png", file=out_rel, sha256=sha(os.path.join(REPO, out_rel)),
             size_px=list(o.size), result="regenerated-r2", generation_pass="r2", generation_attempts_r2=r["attempts"], chosen_attempt=r["chosen"],
             raw_source_box_path=raw, raw_sha256=sha(raw),
             references=["V4 plan crop"] + ([REFS["p15-living"]] if room in USES_P15 else []) + [REFS["p17"]] + (["brochure p24 'Interior (Summary)' text (applied via prompt)"] if room in {"powder", "bath"} else []),
             observed=r["observed"], assumed=r["assumed"], mismatches=r["residual"], critic_defect=r["critic"], critic_report=CRITIC,
             review_status="needs-review", label=LABEL)

# pass-2 result, recorded accurately: 6 layout regenerations + bath style-only
P2 = {"pantry": "regenerated", "powder": "regenerated", "kitchen": "regenerated", "office-gym": "regenerated",
      "maid-room": "regenerated", "maid-bath": "regenerated", "bath": "regenerated-style-only"}
CV = {"kitchen": "PASS", "maid-room": "PASS", "maid-bath": "PASS", "double-height-entry": "PASS", "dress": "PASS", "lift": "PASS (concept)"}
rows = list(csv.DictReader(open(f"{D}/index.csv")))
for row in rows:
    room = row["room"].split("/")[-1]; a = A[room]
    row["result"] = P2.get(room, "pass")
    row["critic_1f58518"] = CV.get(room, "FAIL")
    if room in R2:
        r = R2[room]; row["file"] = a["file"]; row["observed"] = r["observed"]; row["assumed"] = r["assumed"]
        row["mismatches"] = r["residual"]
        row["r2_critic_fix"] = f"regenerated-r2 ({r['attempts']} attempt(s), chose {r['chosen']}); critic defect: {r['critic']}"
        row["evidence"] = row["evidence"].replace("p15-living; ", "p15-living; ") + "; critic " + CRITIC
    else:
        row["r2_critic_fix"] = "kept (critic PASS)"
    a["pass2_result"] = row["result"]; a["critic_1f58518"] = row["critic_1f58518"]
cols = list(rows[0].keys())
cols = [c for c in cols if c not in ("review_status", "critic_1f58518", "r2_critic_fix")] + ["critic_1f58518", "r2_critic_fix", "review_status"]
with open(f"{D}/index.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
for a in man["assets"]:
    rm = a["room_id"].split("/")[-1]
    if rm not in R2: a["result"] = P2.get(rm, "pass")
man["updated_Asia_Dubai"] = NOW
man["critic_report"] = CRITIC
man["guard"]["handoff_guard_r2"] = "python3 /workspace/plan-visuals-archive/optimizer/handoff_guard.py exit 0 at r2 (records=112 verified=0 ambiguous=35 unknown=77 eligible=112 blocked=0 breaches=0)"
man["guard"]["verify_active_pipeline_r2"] = "not run by this lane (integrator only, README rule 7)"
man["counts"] = dict(rooms_in_overlay=15, images=15, pass2_accepted_from_pass1=8, pass2_regenerated_layout=6, pass2_regenerated_style_only=1,
                     r2_regenerated_critic_fix=9, kept_critic_pass=6, new=0, verified_matches=0,
                     note="Earlier manifest/index said 7 'regenerated'; 6 were for layout and bath was for style only (p24). Corrected 2026-11-10.")
json.dump(man, open(f"{D}/manifest.json", "w"), indent=1)

# contact sheet
cw, ch = 480, 360; nc = 4; assets = man["assets"]; nr = (len(assets) + nc - 1) // nc; lab = 64; top = 70
sheet = Image.new("RGB", (cw * nc + 20 * (nc + 1), top + nr * (ch + lab + 20)), "white"); d = ImageDraw.Draw(sheet)
d.text((20, 12), "Ashwood Estates 4B ground floor - interior reference images, r2 critic fix (review_status: needs-review)", font=ImageFont.truetype(FB, 24), fill="black")
d.text((20, 42), LABEL, font=ImageFont.truetype(F, 17), fill=(150, 60, 0))
fL = ImageFont.truetype(FB, 18); fS = ImageFont.truetype(F, 14)
for i, a in enumerate(assets):
    rm = a["room_id"].split("/")[-1]; im = Image.open(os.path.join(REPO, a["file"])); im.thumbnail((cw, ch))
    x = 20 + (i % nc) * (cw + 20); y = top + (i // nc) * (ch + lab + 20); sheet.paste(im, (x + (cw - im.width) // 2, y))
    d.text((x, y + ch + 4), f"{a['room_label']}  ({rm})", font=fL, fill="black")
    st = "r2 critic fix" if rm in R2 else f"kept, critic {a['critic_1f58518']}"
    d.text((x, y + ch + 28), f"{a.get('dimension_transcript') or 'size UNKNOWN'} - {a['match_status']} - {st} - {a['method'].replace('GENERATED-','')}", font=fS, fill=(60, 60, 60))
sheet.save(f"{D}/contact-sheet/4b-gf_interior-refs_CONTACT-SHEET.png")

# review sheet: plan crop | old (r1) | new (r2)
H = 380; fT = ImageFont.truetype(FB, 20); fN = ImageFont.truetype(F, 15)
blocks = []
for room, r in R2.items():
    a = A[room]
    ims = [Image.open(os.path.join(REPO, a["cad_check_crop"])).convert("RGB"), Image.open(os.path.join(REPO, a["superseded_file"])).convert("RGB"), new_imgs[room]]
    ims = [im.resize((int(im.width * H / im.height), H)) for im in ims]
    Wb = sum(im.width for im in ims) + 40
    b = Image.new("RGB", (Wb, H + 110), "white"); db = ImageDraw.Draw(b)
    db.text((10, 6), f"{a['room_label']} ({room}) - {a.get('dimension_transcript') or 'size UNKNOWN'} - critic: {r['critic']}"[:230], font=fT, fill="black")
    x = 0
    for im, cap in zip(ims, ["V4 plan crop (cad-check)", "OLD r1 (critic FAIL)", f"NEW r2 ({r['chosen']})"]):
        b.paste(im, (x, 34)); db.text((x + 4, 34 + H + 4), cap, font=fN, fill=(150, 0, 0) if "OLD" in cap else (0, 100, 0) if "NEW" in cap else (0, 0, 0)); x += im.width + 20
    db.text((10, 34 + H + 28), ("Residual: " + r["residual"])[:260], font=fN, fill=(60, 60, 60))
    db.text((10, 34 + H + 50), ("" + r["residual"])[260:520], font=fN, fill=(60, 60, 60))
    blocks.append(b)
Wmax = max(b.width for b in blocks); Ht = 90 + sum(b.height + 16 for b in blocks)
rs = Image.new("RGB", (Wmax + 40, Ht), "white"); dr = ImageDraw.Draw(rs)
dr.text((20, 12), "Ashwood 4B GF interior refs - critic fix r2: plan crop | old | new (9 rooms). needs-review, not self-approved", font=ImageFont.truetype(FB, 26), fill="black")
dr.text((20, 50), LABEL + "   |   critic: " + CRITIC, font=ImageFont.truetype(F, 16), fill=(150, 60, 0))
y = 90
for b in blocks: rs.paste(b, (20, y)); y += b.height + 16
rs.save(f"{D}/contact-sheet/critic-fix_plan-vs-image.png")
print("done", rs.size, sheet.size)
