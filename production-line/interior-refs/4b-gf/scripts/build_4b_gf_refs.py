"""Build the Ashwood 4B GF interior reference set into a temp folder, then mv into place.
Usage: python3 build_4b_gf_refs.py <repo_root>
Inputs: approved V4 plan raster (via ACTIVE_PIPELINE.json), pass-1/pass-2 raw generations, optimizer overlay."""
import sys, os, json, glob, csv, hashlib, shutil, datetime
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rooms_4b_gf import ROOMS, OLD, NEW
REPO = os.path.abspath(sys.argv[1])
OUT_REL = "production-line/interior-refs/4b-gf"
OVERLAY = "/workspace/plan-visuals-archive/optimizer/handoff_overlay.json"
CROPS = "/workspace/irw/crops"
LABEL = "CONCEPT VISUALISATION - AI-generated - not survey-verified - not construction-ready - not certified CAD"
TZ = datetime.timezone(datetime.timedelta(hours=4))
NOW = datetime.datetime.now(TZ).isoformat(timespec="seconds")
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

ap = json.load(open(os.path.join(REPO, "ACTIVE_PIPELINE.json")))
plan = next(p for p in ap["plans"] if p["id"] == "4B-GF")
plan_png = os.path.join(REPO, plan["long7680"])
assert sha(plan_png) == plan["sha256"]["long7680"], "approved plan hash mismatch"
assert "superseded" not in plan_png
ov = {r["room_id"]: r for r in json.load(open(OVERLAY))["records"]}

tmp = os.path.join(REPO, "production-line/interior-refs/.tmp-4b-gf")
shutil.rmtree(tmp, ignore_errors=True)
for d in ["images", "cad-check", "contact-sheet", "style-guide/refs", "scripts"]: os.makedirs(f"{tmp}/{d}")

REFMAP = {"p15-living": "style-guide/refs/style-p15-living.png", "p15-dressing": "style-guide/refs/style-p15-dressing.png",
          "p17-materials": "style-guide/refs/style-p17-materials_swatches.png",
          "p24-spec-text": "brochure p24 'Interior (Summary)' text (applied via prompt, extracts/text/pages/page_24.txt)"}
rows, assets, thumbs = [], [], []
for r in ROOMS:
    rid = f"ashwood-estates/4b/gf/{r['room']}"; o = ov[rid]
    vid = o["view_id"].split("/")[-1]
    if r["src"] == "old":
        raw = glob.glob(f"{OLD}/{r['room']}/view-unassigned-001/_raw_unlabelled/*RAW*")[0]
    else:
        raw = f"{NEW}/4b-gf-{r['room']}_pass2_RAW.jpg"
    stem = f"4b-gf-{r['room']}__{vid}__{r['method']}"
    im = Image.open(raw).convert("RGB")
    W, H = im.size
    f1 = ImageFont.truetype(FB, max(14, W // 60)); f2 = ImageFont.truetype(F, max(13, W // 70))
    def wrap(txt, font):
        out, cur = [], ""
        for w_ in txt.split(" "):
            t = (cur + " " + w_).strip()
            if font.getlength(t) > W - 20 and cur: out.append(cur); cur = w_
            else: cur = t
        return out + [cur]
    l1 = wrap(f"Ashwood 4B GF - {r['label']} - {vid} - {r['method']} - needs-review", f1); l2 = wrap(LABEL, f2)
    lh1, lh2 = f1.size + 6, f2.size + 6; bh = 10 + lh1 * len(l1) + lh2 * len(l2)
    out = Image.new("RGB", (W, H + bh), "white"); out.paste(im, (0, 0))
    d = ImageDraw.Draw(out); d.rectangle((0, H, W, H + bh), fill=(25, 25, 25)); y = H + 5
    for t in l1: d.text((10, y), t, font=f1, fill="white"); y += lh1
    for t in l2: d.text((10, y), t, font=f2, fill=(255, 210, 120)); y += lh2
    img_rel = f"images/{stem}.png"; out.save(f"{tmp}/{img_rel}")
    crop_rel = f"cad-check/{stem}__V4-plan-crop__EVIDENCE.png"
    shutil.copy(f"{CROPS}/4b-gf-{r['room']}_V4-plan-crop.png", f"{tmp}/{crop_rel}")
    thumbs.append((out, r, vid))
    ev = f"V4 plan {plan['long7680']} (source PDF p{plan['source_pdf_page']}); refs: " + "; ".join(r["refs"])
    rows.append(dict(file=f"{OUT_REL}/{img_rel}", villa="4b", floor=o["floor_id"], room=rid, view=o["view_id"], method=r["method"],
                     cad_view_checked="y", match_status=o["match_status"], generation_eligibility=o["generation_eligibility"],
                     result=r["result"], evidence=ev, observed=r["observed"], assumed=r["assumed"], mismatches=r["mismatches"],
                     review_status="needs-review"))
    assets.append(dict(room_id=rid, view_id=o["view_id"], room_label=r["label"], method=r["method"], file=f"{OUT_REL}/{img_rel}",
                       sha256=sha(f"{tmp}/{img_rel}"), size_px=list(out.size), cad_check_crop=f"{OUT_REL}/{crop_rel}",
                       result=r["result"], generation_pass=2 if r["src"] == "new" else 1,
                       raw_source_box_path=raw, raw_sha256=sha(raw), references=[REFMAP.get(x, "V4 plan crop") for x in r["refs"]],
                       match_status=o["match_status"], generation_eligibility=o["generation_eligibility"],
                       dimension_transcript=o.get("dimension_transcript"), ceiling_height=o.get("ceiling_height"),
                       room_polygon=None, observed=r["observed"], assumed=r["assumed"], mismatches=r["mismatches"],
                       review_status="needs-review", label=LABEL))

cols = ["file","villa","floor","room","view","method","cad_view_checked","match_status","generation_eligibility","result","evidence","observed","assumed","mismatches","review_status"]
with open(f"{tmp}/index.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)

# contact sheet: 4 columns, readable labels
cw, ch = 480, 360; cols_n = 4; rows_n = (len(thumbs) + cols_n - 1) // cols_n; lab = 64; top = 70
sheet = Image.new("RGB", (cw * cols_n + 20 * (cols_n + 1), top + rows_n * (ch + lab + 20)), "white")
d = ImageDraw.Draw(sheet)
d.text((20, 12), "Ashwood Estates 4B ground floor - interior reference images (review_status: needs-review)", font=ImageFont.truetype(FB, 24), fill="black")
d.text((20, 42), LABEL, font=ImageFont.truetype(F, 17), fill=(150, 60, 0))
fL = ImageFont.truetype(FB, 18); fS = ImageFont.truetype(F, 14)
for i, (im, r, vid) in enumerate(thumbs):
    t = im.copy(); t.thumbnail((cw, ch)); x = 20 + (i % cols_n) * (cw + 20); y = top + (i // cols_n) * (ch + lab + 20)
    sheet.paste(t, (x + (cw - t.width) // 2, y))
    o = ov[f"ashwood-estates/4b/gf/{r['room']}"]
    d.text((x, y + ch + 4), f"{r['label']}  ({r['room']})", font=fL, fill="black")
    d.text((x, y + ch + 28), f"{o.get('dimension_transcript') or 'size UNKNOWN'} - {o['match_status']} - CAD: {r['result']} - {r['method'].replace('GENERATED-','')}", font=fS, fill=(60, 60, 60))
sheet.save(f"{tmp}/contact-sheet/4b-gf_interior-refs_CONTACT-SHEET.png")

# style guide + refs + scripts
for f in glob.glob("/workspace/irw/refs/*.png"): shutil.copy(f, f"{tmp}/style-guide/refs/")
shutil.copy("/workspace/irw/style_guide_4b.json", f"{tmp}/style-guide/ashwood-4b_interior_style_guide.json")
shutil.copy("/workspace/irw/style_guide_4b.md", f"{tmp}/style-guide/ashwood-4b_interior_style_guide.md")
for f in glob.glob("/workspace/irw/scripts/*.py") + ["/workspace/irw/scripts/prompts_pass2.json"]: shutil.copy(f, f"{tmp}/scripts/")
shutil.copy("/workspace/irw/README_4b-gf.md", f"{tmp}/README.md")

man = dict(schema="ashwood_interior_refs_v1", project_id="ashwood-estates", villa_id="4b", floor_id="gf", created_Asia_Dubai=NOW,
           label=LABEL, branch="lane/interior-refs",
           guard=dict(handoff_guard="python3 /workspace/plan-visuals-archive/optimizer/handoff_guard.py exit 0 (records=112 verified=0 ambiguous=35 unknown=77 eligible=112 breaches=0)",
                      verify_active_pipeline="python3 scripts/verify_active_pipeline.py exit 0"),
           overlay=OVERLAY, approved_plan=dict(path=plan["long7680"], svg=plan["svg"], sha256=plan["sha256"]["long7680"], source_pdf_page=plan["source_pdf_page"]),
           style_guide=f"{OUT_REL}/style-guide/ashwood-4b_interior_style_guide.json",
           counts=dict(rooms_in_overlay=len(ROOMS), images=len(assets), passed=sum(a["result"]=="pass" for a in assets),
                       regenerated=sum(a["result"]=="regenerated" for a in assets), new=0, verified_matches=0),
           previous_set="Bigc7292/ashwood-plan-visuals-archive @ af451f3 generated-interiors/ashwood-estates/4b/ (pass 1)",
           assets=assets)
json.dump(man, open(f"{tmp}/manifest.json", "w"), indent=1)

dst = os.path.join(REPO, OUT_REL)
if os.path.exists(dst): shutil.move(dst, "/workspace/irw/prev-4b-gf-" + NOW.replace(":", ""))
shutil.move(tmp, dst)
print("wrote", dst, len(assets), "images")
