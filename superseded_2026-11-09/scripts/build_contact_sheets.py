#!/usr/bin/env python3
"""Build contact sheets from extracts/pages/page72-*.png"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ARCH = Path(__file__).resolve().parents[1]
pages = sorted((ARCH/'extracts'/'pages').glob('page72-*.png'))
if not pages:
    raise SystemExit('No page72-*.png renders found')
tw, th = 320, 180
cols = 5
rows = (len(pages)+cols-1)//cols
sheet = Image.new('RGB', (cols*tw+(cols+1)*8, rows*th+(rows+1)*24+40), (245,245,245))
draw = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    font_sm = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
except Exception:
    font = font_sm = ImageFont.load_default()
draw.text((8,8), f'Contact sheet — {len(pages)} pages @72dpi', fill=(20,20,20), font=font)
for i,p in enumerate(pages):
    im = Image.open(p).convert('RGB'); im.thumbnail((tw,th))
    r,c = divmod(i, cols)
    x=8+c*(tw+8); y=40+r*(th+24)
    sheet.paste(im,(x,y)); draw.text((x,y+im.height+2), f'p{i+1:02d}', fill=(0,0,0), font=font_sm)
out = ARCH/'extracts'/'contact-sheets'/'all_pages_72dpi.png'
out.parent.mkdir(parents=True, exist_ok=True)
sheet.save(out, optimize=True)
sheet.resize((sheet.width//2, sheet.height//2), Image.Resampling.LANCZOS).save(
    ARCH/'previews'/'contact_all_pages.png', optimize=True)
print('wrote', out)
