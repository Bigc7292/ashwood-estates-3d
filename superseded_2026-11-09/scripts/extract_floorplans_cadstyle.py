#!/usr/bin/env python3
"""
Ashwood-oriented floorplan crop + CAD-style raster helper.
Clips are evidence-based for the Ashwood Estates brochure layout
(sidebar left, plans right; dual FF|RF on one page). For other PDFs,
edit CLIPS / FLOORPLANS or supply --config JSON.
Does NOT invent geometry. Outputs are source-based raster illustrations,
NOT certified/native CAD.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pymupdf
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont

ARCH = Path(__file__).resolve().parents[1]
DUBAI = timezone(timedelta(hours=4))

# Default evidence-based clips for Ashwood brochure (1920x1080 pts)
DEFAULT_CLIPS = {
    27: {'Ground Floor': [640, 30, 1900, 1055]},
    28: {'First Floor': [640, 30, 1320, 1055], 'Roof Floor': [1320, 30, 1905, 1055]},
    31: {'Ground Floor': [640, 30, 1900, 1055]},
    32: {'First Floor': [640, 30, 1320, 1055], 'Roof Floor': [1320, 30, 1905, 1055]},
    35: {'Ground Floor': [640, 30, 1900, 1055]},
    36: {'First Floor': [640, 30, 1320, 1055], 'Roof Floor': [1320, 30, 1905, 1055]},
}
DEFAULT_FLOORPLANS = [
  {'asset_id':'FP-4B-GF','page':27,'villa_type':'4 Bedroom Villa','floor':'Ground Floor','confidence':0.92,
   'ambiguity':'Area figure conflicts vs p24 schedule possible; marketing furniture present.'},
  {'asset_id':'FP-4B-FF','page':28,'villa_type':'4 Bedroom Villa','floor':'First Floor','confidence':0.9,'ambiguity':'Shares page with Roof.'},
  {'asset_id':'FP-4B-RF','page':28,'villa_type':'4 Bedroom Villa','floor':'Roof Floor','confidence':0.88,'ambiguity':'Shares page with First.'},
  {'asset_id':'FP-5B-GF','page':31,'villa_type':'5 Bedroom Villa','floor':'Ground Floor','confidence':0.92,'ambiguity':'Marketing illustration style.'},
  {'asset_id':'FP-5B-FF','page':32,'villa_type':'5 Bedroom Villa','floor':'First Floor','confidence':0.9,'ambiguity':'Shares page with Roof.'},
  {'asset_id':'FP-5B-RF','page':32,'villa_type':'5 Bedroom Villa','floor':'Roof Floor','confidence':0.88,'ambiguity':'Shares page with First.'},
  {'asset_id':'FP-6B-GF','page':35,'villa_type':'6 Bedroom Villa','floor':'Ground Floor','confidence':0.92,'ambiguity':'Marketing illustration style.'},
  {'asset_id':'FP-6B-FF','page':36,'villa_type':'6 Bedroom Villa','floor':'First Floor','confidence':0.9,'ambiguity':'Shares page with Roof.'},
  {'asset_id':'FP-6B-RF','page':36,'villa_type':'6 Bedroom Villa','floor':'Roof Floor','confidence':0.88,'ambiguity':'Shares page with First.'},
]

def cad_style_from_source(img: Image.Image) -> Image.Image:
    g = ImageOps.grayscale(img)
    g = ImageOps.autocontrast(g, cutoff=1)
    g = g.filter(ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=2))
    rgb = Image.merge('RGB', (g,g,g))
    return ImageEnhance.Contrast(ImageEnhance.Brightness(rgb).enhance(1.05)).enhance(1.15)

def annotate_banner(img, lines):
    pad = 40 + 18*len(lines)
    out = Image.new('RGB', (img.width, img.height+pad), (255,255,255))
    out.paste(img, (0, pad))
    draw = ImageDraw.Draw(out)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
        font_b = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
    except Exception:
        font = font_b = ImageFont.load_default()
    y=6
    for i,line in enumerate(lines):
        draw.text((8,y), line, fill=(20,20,20), font=font_b if i==0 else font); y+=17
    draw.rectangle([0,pad-2,out.width,pad], fill=(160,160,160))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', required=True)
    ap.add_argument('--config', help='Optional JSON overriding clips/floorplans')
    ap.add_argument('--dpi', type=int, default=180)
    args = ap.parse_args()
    pdf = Path(args.pdf)
    sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
    now = datetime.now(DUBAI).strftime('%Y-%m-%d %H:%M:%S Asia/Dubai (UTC+4)')
    clips, floorplans = DEFAULT_CLIPS, DEFAULT_FLOORPLANS
    if args.config:
        cfg = json.loads(Path(args.config).read_text())
        clips = {int(k): v for k,v in cfg.get('clips', clips).items()}
        floorplans = cfg.get('floorplans', floorplans)
    doc = pymupdf.open(pdf)
    PAGE_H = float(doc[0].rect.height)
    rows=[]
    for fp in floorplans:
        pn=fp['page']; floor=fp['floor']
        box=clips[pn][floor]
        clip=pymupdf.Rect(*box)
        mat=pymupdf.Matrix(args.dpi/72, args.dpi/72)
        pix=doc[pn-1].get_pixmap(matrix=mat, clip=clip, alpha=False)
        img=Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        src_path=ARCH/'extracts'/'plans'/f"{fp['asset_id']}_source_crop.png"
        src_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(src_path, optimize=True)
        cad=annotate_banner(cad_style_from_source(img), [
            f"{fp['asset_id']} | {fp['villa_type']} — {fp['floor']}",
            'SOURCE-BASED CAD-STYLE RASTER — NOT certified CAD / NOT DXF/DWG.',
            f"From page {pn} crop only; no invented geometry.",
            f"Ambiguity: {fp.get('ambiguity','')[:140]}",
            f"SHA256 {sha[:20]}… | {now}",
        ])
        cad_path=ARCH/'cad-style'/f"{fp['asset_id']}_cadstyle_raster.png"
        cad_path.parent.mkdir(parents=True, exist_ok=True)
        cad.save(cad_path, optimize=True)
        villa_slug=re.sub(r'[^A-Za-z0-9]+','-',fp['villa_type']).strip('-').lower()
        floor_slug=re.sub(r'[^A-Za-z0-9]+','-',floor).strip('-').lower()
        for dest in [ARCH/'floors'/villa_slug/floor_slug, ARCH/'plans'/villa_slug]:
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest/src_path.name)
            shutil.copy2(cad_path, dest/cad_path.name)
        x0,y0,x1,y1=box
        rows.append({
            'asset_id': fp['asset_id'], 'page': pn, 'villa_type': fp['villa_type'], 'floor': floor,
            'bbox_x0_pt_topleft': x0, 'bbox_y0_pt_topleft': y0, 'bbox_x1_pt_topleft': x1, 'bbox_y1_pt_topleft': y1,
            'bbox_y0_pt_bottomleft_origin': PAGE_H-y1, 'bbox_y1_pt_bottomleft_origin': PAGE_H-y0,
            'confidence': fp.get('confidence',0.8), 'ambiguity': fp.get('ambiguity',''),
            'source_sha256': sha, 'source_crop_path': str(src_path.relative_to(ARCH)),
            'cadstyle_raster_path': str(cad_path.relative_to(ARCH)),
            'cad_disclaimer': 'Source-based CAD-style raster only; NOT native CAD.',
        })
        print('wrote', fp['asset_id'])
    (ARCH/'manifests').mkdir(exist_ok=True)
    (ARCH/'manifests'/'floorplans_manifest.json').write_text(json.dumps({'source_sha256':sha,'generated_at':now,'assets':rows}, indent=2))
    with open(ARCH/'manifests'/'floorplans_manifest.csv','w',newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print('manifests updated')

if __name__ == '__main__':
    main()
