"""Build one Ashwood 4B floor's interior reference set (FF or RF) into a temp folder, then mv into place.
Usage: python3 build_floor_refs.py <repo_root> <rooms_module>   e.g. rooms_4b_ff
Same labels, naming, index columns and layout as production-line/interior-refs/4b-gf/ (built by build_4b_gf_refs.py)."""
import sys, os, json, csv, hashlib, shutil, datetime, importlib, glob
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(sys.argv[1]); M = importlib.import_module(sys.argv[2])
FL = M.FLOOR; OUT_REL = f"production-line/interior-refs/4b-{FL}"
OVERLAY = "/workspace/plan-visuals-archive/optimizer/handoff_overlay.json"
CROPS = f"/workspace/irw/{FL}/crops"
STYLE_GUIDE = "production-line/interior-refs/4b-gf/style-guide/ashwood-4b_interior_style_guide.json"
LABEL = "CONCEPT VISUALISATION - AI-generated - not survey-verified - not construction-ready - not certified CAD"
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=4))).isoformat(timespec="seconds")
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
ap = json.load(open(os.path.join(REPO, "ACTIVE_PIPELINE.json")))
plan = next(p for p in ap["plans"] if p["id"] == M.PLAN_ID)
assert sha(os.path.join(REPO, plan["long7680"])) == plan["sha256"]["long7680"], "approved plan hash mismatch"
assert os.path.exists(os.path.join(REPO, STYLE_GUIDE)), "4b style guide missing"
ov = {r["room_id"]: r for r in json.load(open(OVERLAY))["records"]}
want = sorted(k for k, r in ov.items() if r["villa_id"] == "4b" and r["floor_id"] == FL)
assert sorted(f"ashwood-estates/4b/{FL}/{r['room']}" for r in M.ROOMS) == want, "room list differs from overlay"
tmp = os.path.join(REPO, f"production-line/interior-refs/.tmp-4b-{FL}"); shutil.rmtree(tmp, ignore_errors=True)
for d in ["images", "cad-check", "contact-sheet", "scripts"]: os.makedirs(f"{tmp}/{d}")
REFMAP = {"p15-living": "4b-gf/style-guide/refs/style-p15-living.png", "p15-dressing": "4b-gf/style-guide/refs/style-p15-dressing.png",
          "p16-bedroom": "4b-gf/style-guide/refs/style-p16-bedroom_nologo.png", "p17-materials": "4b-gf/style-guide/refs/style-p17-materials_swatches.png",
          "p24-spec-text": "brochure p24 'Interior (Summary)' text, applied via prompt (extracts/text/pages/page_24.txt)", "plan-crop": "V4 plan crop (cad-check/)"}
rows, assets, thumbs = [], [], []
for r in M.ROOMS:
    rid = f"ashwood-estates/4b/{FL}/{r['room']}"; o = ov[rid]; vid = o["view_id"].split("/")[-1]
    p = 2 if r["result"] == "regenerated" else 1
    raw = f"{M.RAW}/4b-{FL}-{r['room']}_pass{p}_RAW.jpg"
    stem = f"4b-{FL}-{r['room']}__{vid}__{r['method']}"
    im = Image.open(raw).convert("RGB"); W, H = im.size
    f1 = ImageFont.truetype(FB, max(14, W // 60)); f2 = ImageFont.truetype(F, max(13, W // 70))
    def wrap(txt, font):
        out, cur = [], ""
        for w_ in txt.split(" "):
            t = (cur + " " + w_).strip()
            if font.getlength(t) > W - 20 and cur: out.append(cur); cur = w_
            else: cur = t
        return out + [cur]
    l1 = wrap(f"Ashwood 4B {FL.upper()} - {r['label']} - {vid} - {r['method']} - needs-review", f1); l2 = wrap(LABEL, f2)
    lh1, lh2 = f1.size + 6, f2.size + 6; bh = 10 + lh1 * len(l1) + lh2 * len(l2)
    out = Image.new("RGB", (W, H + bh), "white"); out.paste(im, (0, 0)); d = ImageDraw.Draw(out)
    d.rectangle((0, H, W, H + bh), fill=(25, 25, 25)); y = H + 5
    for t in l1: d.text((10, y), t, font=f1, fill="white"); y += lh1
    for t in l2: d.text((10, y), t, font=f2, fill=(255, 210, 120)); y += lh2
    img_rel = f"images/{stem}.png"; out.save(f"{tmp}/{img_rel}")
    crop_rel = f"cad-check/{stem}__V4-plan-crop__EVIDENCE.png"; shutil.copy(f"{CROPS}/4b-{FL}-{r['room']}_V4-plan-crop.png", f"{tmp}/{crop_rel}")
    thumbs.append((out, r, o))
    ev = f"V4 plan {plan['long7680']} (source PDF p{plan['source_pdf_page']}); refs: " + "; ".join(r["refs"])
    rows.append(dict(file=f"{OUT_REL}/{img_rel}", villa="4b", floor=FL, room=rid, view=o["view_id"], method=r["method"], cad_view_checked="y",
                     match_status=o["match_status"], generation_eligibility=o["generation_eligibility"], result=r["result"], evidence=ev,
                     observed=r["observed"], assumed=r["assumed"], mismatches=r["mismatches"], review_status="needs-review"))
    assets.append(dict(room_id=rid, view_id=o["view_id"], room_label=r["label"], method=r["method"], file=f"{OUT_REL}/{img_rel}",
                       sha256=sha(f"{tmp}/{img_rel}"), size_px=list(out.size), cad_check_crop=f"{OUT_REL}/{crop_rel}", result=r["result"],
                       generation_pass=p, raw_source_box_path=raw, raw_sha256=sha(raw), references=[REFMAP[x] for x in r["refs"]],
                       match_status=o["match_status"], generation_eligibility=o["generation_eligibility"],
                       dimension_transcript=o.get("dimension_transcript"), ceiling_height=o.get("ceiling_height"), room_polygon=None,
                       observed=r["observed"], assumed=r["assumed"], mismatches=r["mismatches"], review_status="needs-review", label=LABEL))
cols = ["file","villa","floor","room","view","method","cad_view_checked","match_status","generation_eligibility","result","evidence","observed","assumed","mismatches","review_status"]
with open(f"{tmp}/index.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
cw, ch, cn, lab, top = 480, 360, 4, 64, 70; rn = (len(thumbs) + cn - 1) // cn
sheet = Image.new("RGB", (cw * cn + 20 * (cn + 1), top + rn * (ch + lab + 20)), "white"); d = ImageDraw.Draw(sheet)
names = {"ff": "first floor", "rf": "roof floor"}
d.text((20, 12), f"Ashwood Estates 4B {names[FL]} - interior reference images (review_status: needs-review)", font=ImageFont.truetype(FB, 24), fill="black")
d.text((20, 42), LABEL, font=ImageFont.truetype(F, 17), fill=(150, 60, 0))
fL = ImageFont.truetype(FB, 18); fS = ImageFont.truetype(F, 14)
for i, (im, r, o) in enumerate(thumbs):
    t = im.copy(); t.thumbnail((cw, ch)); x = 20 + (i % cn) * (cw + 20); y = top + (i // cn) * (ch + lab + 20)
    sheet.paste(t, (x + (cw - t.width) // 2, y))
    d.text((x, y + ch + 4), f"{r['label']}  ({r['room']})", font=fL, fill="black")
    d.text((x, y + ch + 28), f"{o.get('dimension_transcript') or 'size UNKNOWN'} - {o['match_status']} - CAD: {r['result']} - {r['method'].replace('GENERATED-','')}", font=fS, fill=(60, 60, 60))
sheet.save(f"{tmp}/contact-sheet/4b-{FL}_interior-refs_CONTACT-SHEET.png")
here = os.path.dirname(os.path.abspath(__file__))
for f in ["build_floor_refs.py", f"{sys.argv[2]}.py", "prompts_ff_rf.py"]: shutil.copy(os.path.join(here, f), f"{tmp}/scripts/")
shutil.copy("/workspace/irw/prompts_ff_rf_record.json", f"{tmp}/scripts/prompts_ff_rf_record.json")
n_reg = sum(a["result"] == "regenerated" for a in assets)
open(f"{tmp}/README.md", "w").write(f"""# Ashwood 4B {names[FL]}: interior reference images

**concept visualisation, not survey-verified, not construction-ready, not certified CAD.** AI-generated. review_status: needs-review. Not approved.

Lane: interior reference images (branch `lane/interior-refs`). Same process, labels and layout as `../4b-gf/`. Materials and style only; the approved V4 plan decides dimensions.

- `images/`: {len(assets)} labelled images, one per 4B {FL.upper()} interior/service room in the optimizer overlay. Name: `4b-{FL}-<room>__<view>__<METHOD>.png`.
- `cad-check/`: the V4 plan crop each image was checked against (from `{plan['long7680']}`, hash-checked against `ACTIVE_PIPELINE.json`; plan artwork unchanged).
- `index.csv`: villa, floor, room, CAD check, match_status, evidence, observed, assumed, mismatches, review_status.
- `manifest.json`: hashes, raw sources, references, guard results.
- `contact-sheet/`: all images with room labels.
- `scripts/`: room records, build script and prompts (pass 1 plus pass-2 changes).
- Style guide: the shared 4B guide at `../4b-gf/style-guide/` (no new items for this floor).

All {len(assets)} images are new for this floor ({len(assets)-n_reg} accepted at pass 1, {n_reg} regenerated once after the CAD check). Inputs: `ACTIVE_PIPELINE.json` and `active/approved-cad-v4/` only; `superseded_2026-11-09/` not used. match_status is copied from `optimizer/handoff_overlay.json`; no room has a verified source photo.
""" + getattr(M, "README_EXTRA", ""))
man = dict(schema="ashwood_interior_refs_v1", project_id="ashwood-estates", villa_id="4b", floor_id=FL, created_Asia_Dubai=NOW, label=LABEL,
           branch="lane/interior-refs", guard=dict(handoff_guard="exit 0 (records=112 verified=0 ambiguous=35 unknown=77 eligible=112 breaches=0)",
           verify_active_pipeline="exit 0; active/pipeline_verification.json restored after run"), overlay=OVERLAY,
           approved_plan=dict(path=plan["long7680"], svg=plan["svg"], sha256=plan["sha256"]["long7680"], source_pdf_page=plan["source_pdf_page"]),
           style_guide=STYLE_GUIDE, counts=dict(rooms_in_overlay=len(want), images=len(assets), pass1_accepted=len(assets)-n_reg, regenerated=n_reg, verified_matches=0),
           excluded=getattr(M, "EXCLUDED", []), assets=assets)
json.dump(man, open(f"{tmp}/manifest.json", "w"), indent=1)
dst = os.path.join(REPO, OUT_REL)
if os.path.exists(dst): shutil.move(dst, f"/workspace/irw/prev-4b-{FL}-" + NOW.replace(":", ""))
shutil.move(tmp, dst); print("wrote", dst, len(assets), "images")
