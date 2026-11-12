"""Render walk_grid.json (from walk_check.py) as one plan map per level.

    uv run --no-project --with pillow python walk_map.py <Saved/Pipeline dir>

Colours: light green = walkable, red = floor but blocked for a person, blue = reached from the front door,
black dot = start, yellow squares = room probe points. Pool at the top, 4 px per 20 cm cell.
"""
import json
import sys

from PIL import Image, ImageDraw

LEVELS = {"GF": (0, 300), "FF": (400, 700), "RF": (800, 1100)}


def main(d):
    g = json.load(open(f"{d}/walk_grid.json"))
    x0, y0, step = g["grid"]
    P = 4
    W = max(c[0] for c in g["cells"]) + 1
    H = max(c[1] for c in g["cells"]) + 1
    imgs = []
    for name, (za, zb) in LEVELS.items():
        im = Image.new("RGB", (W * P, H * P + 18), "white")
        dr = ImageDraw.Draw(im)
        best = {}  # per column, show the best state in this level band: reached > walkable > blocked
        for i, j, k, h, ok, reached in g["cells"]:
            if za <= h < zb:
                best[(i, j)] = max(best.get((i, j), 0), 2 if reached else (1 if ok else 0))
        for (i, j), st in best.items():
            col = [(225, 90, 80), (170, 225, 160), (40, 110, 230)][st]
            dr.rectangle([i * P, j * P + 18, i * P + P - 1, j * P + P - 1 + 18], fill=col)
        for rn, (px, py, pz) in g["rooms"].items():
            if za <= pz < zb:
                cx, cy = (px - x0) / step * P, (py - y0) / step * P + 18
                dr.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], outline=(0, 0, 0), fill=(250, 210, 0))
        sx, sy = (985 - x0) / step * P, (2840 - y0) / step * P + 18
        dr.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill="black")
        dr.text((4, 2), f"{name}  floors {za}-{zb} cm", fill="black")
        imgs.append(im)
    out = Image.new("RGB", (sum(i.width for i in imgs) + 20 * (len(imgs) - 1), max(i.height for i in imgs)), "white")
    x = 0
    for im in imgs:
        out.paste(im, (x, 0)); x += im.width + 20
    out.save(f"{d}/walk_map.png")


if __name__ == "__main__":
    main(sys.argv[1])
