"""Render the extracted Unreal plan geometry (plan_<floor>.json) as a scaled plan image.

    uv run --no-project --with pillow --with numpy python render_plan.py <Saved/Pipeline dir>

Orientation matches the V4 CAD sheets: pool (world -Y) at the top, world +X to the right.
Scale: 2 cm per pixel. Floors light grey, stair/landing treads blue, walls black.
Also writes plan_<floor>_bbox.json with the wall bounding box in world cm.
"""
import json
import sys

from PIL import Image, ImageDraw

CM_PER_PX = 2.0
X0, X1, Y0, Y1 = 200, 1700, -100, 2800  # world-cm window


def to_px(x, y):
    return ((x - X0) / CM_PER_PX, (y - Y0) / CM_PER_PX)


def render(src_dir, floor):
    data = json.load(open(f"{src_dir}/plan_{floor}.json", encoding="utf-8"))
    w, h = int((X1 - X0) / CM_PER_PX), int((Y1 - Y0) / CM_PER_PX)
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    for tri in data["floors"]:
        d.polygon([to_px(*p) for p in tri[:3]], fill=(222, 222, 222))
    for tri in data["steps"]:
        d.polygon([to_px(*p) for p in tri[:3]], fill=(120, 170, 230))
    xs, ys = [], []
    for x0, y0, x1, y1, *_ in data["walls"]:
        d.line([to_px(x0, y0), to_px(x1, y1)], fill="black", width=3)
        xs += [x0, x1]
        ys += [y0, y1]
    # 1 m grid ticks for reading positions
    for gx in range(X0 - X0 % 100, X1, 100):
        d.line([to_px(gx, Y0), to_px(gx, Y0 + 30)], fill=(200, 0, 0))
        d.text((to_px(gx, Y0 + 40)), str(gx), fill=(200, 0, 0))
    for gy in range(Y0 - Y0 % 100, Y1, 100):
        d.line([to_px(X0, gy), to_px(X0 + 30, gy)], fill=(200, 0, 0))
        d.text((to_px(X0 + 40, gy)), str(gy), fill=(200, 0, 0))
    img.save(f"{src_dir}/plan_{floor}.png")
    bbox = {"xmin": min(xs), "xmax": max(xs), "ymin": min(ys), "ymax": max(ys)}
    json.dump(bbox, open(f"{src_dir}/plan_{floor}_bbox.json", "w"))
    return bbox


if __name__ == "__main__":
    for fl in ("gf", "ff"):
        print(fl, render(sys.argv[1], fl))
