"""Register the Unreal interior walls to an approved V4 CAD sheet and draw an overlay.

    uv run --no-project --with pillow --with numpy python overlay_cad.py <repo> <Saved/Pipeline> gf|ff

Inputs: active/approved-cad-v4/png/FP-4B-<FL>_V4_preview.png (approved, unchanged) and
plan_<fl>.json from extract_plan_geometry.py. Searches scale (px per metre) and offset so model
wall points land on CAD wall pixels (chamfer score on a blurred wall mask). Writes
overlay_<fl>.png (CAD faded, model walls red, stair treads blue) and register_<fl>.json.
CAD px = (tx + s * x_m, ty + s * y_m), with world +Y pointing down the sheet (pool at top).
"""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def wall_mask(img):
    a = np.asarray(img).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (r < 75) & (g < 85) & (b < 85) & (abs(g - r) < 20) & (abs(b - g) < 15)
    m[:150, :] = False
    m[1500:, :] = False
    m[:, 1040:] = False
    return m


def wall_points(walls, step_cm=10.0):
    pts = []
    for x0, y0, x1, y1, *_ in walls:
        n = max(1, int(np.hypot(x1 - x0, y1 - y0) / step_cm))
        for k in range(n + 1):
            pts.append((x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n))
    return np.array(pts) / 100.0  # metres


def score(field, pts, s, tx, ty):
    px = (tx + s * pts[:, 0]).astype(int)
    py = (ty + s * pts[:, 1]).astype(int)
    ok = (px >= 0) & (py >= 0) & (px < field.shape[1]) & (py < field.shape[0])
    return field[py[ok], px[ok]].sum() / len(pts)


def register(field, pts):
    best = (-1, None)
    # coarse: scale 40..46 px/m, offsets over the sheet
    for s in np.arange(40.0, 46.01, 0.5):
        for tx in range(-200, 400, 6):
            for ty in range(0, 500, 6):
                sc = score(field, pts, s, tx, ty)
                if sc > best[0]:
                    best = (sc, (s, tx, ty))
    s0, tx0, ty0 = best[1]
    for s in np.arange(s0 - 0.5, s0 + 0.51, 0.1):
        for tx in range(tx0 - 6, tx0 + 7):
            for ty in range(ty0 - 6, ty0 + 7):
                sc = score(field, pts, s, tx, ty)
                if sc > best[0]:
                    best = (sc, (float(s), tx, ty))
    return best


def main(repo, out, fl):
    sheet = Image.open(f"{repo}/active/approved-cad-v4/png/FP-4B-{fl.upper()}_V4_preview.png").convert("RGB")
    mask = wall_mask(sheet)
    field = np.asarray(Image.fromarray((mask * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(4))) / 255.0
    data = json.load(open(f"{out}/plan_{fl}.json", encoding="utf-8"))
    pts = wall_points(data["walls"])
    sub = pts[:: max(1, len(pts) // 3000)]
    sc, (s, tx, ty) = register(field, sub)
    full = score(field, pts, s, tx, ty)
    faded = Image.blend(sheet, Image.new("RGB", sheet.size, "white"), 0.55)
    d = ImageDraw.Draw(faded)
    m = lambda x, y: (tx + s * x / 100.0, ty + s * y / 100.0)
    for tri in data["steps"]:
        d.polygon([m(*p) for p in tri[:3]], fill=(60, 120, 255))
    for x0, y0, x1, y1, *_ in data["walls"]:
        d.line([m(x0, y0), m(x1, y1)], fill=(230, 0, 0), width=2)
    faded.save(f"{out}/overlay_{fl}.png")
    rec = {"floor": fl, "px_per_m": s, "tx": tx, "ty": ty, "score_sample": sc, "score_all": full}
    json.dump(rec, open(f"{out}/register_{fl}.json", "w"), indent=1)
    print(rec)


if __name__ == "__main__":
    main(*sys.argv[1:4])
