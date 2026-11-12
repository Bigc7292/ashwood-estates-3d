"""Redraw the planting leaf/bark textures at high resolution, same style and colours as the originals.

    uv run --no-project --with pillow --with numpy python make_leaf_textures.py <dir with img0..img6.png> <out dir>

The originals (planting_set.glb, 128 px, procedural) are sampled for mean colour and leaf coverage so the
planting design does not change; only the resolution and edge quality do. Output: planting_tex_<i>.png.
img0 = bark (64x128 -> 512x1024), img1 olive, img2 broad, img3 hedge, img4 column (cypress), img5 palm, img6 pine.
"""
import math
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 2  # supersampling factor for anti-aliased edges


def stats(path):
    a = np.asarray(Image.open(path).convert("RGBA")).astype(float)
    m = a[..., 3] > 127
    col = a[..., :3][m].mean(0) if m.any() else a[..., :3].reshape(-1, 3).mean(0)
    return col, m.mean()


def jitter(c, amt, rng):
    k = 1 + rng.uniform(-amt, amt)
    h = rng.uniform(-amt / 2, amt / 2)
    return tuple(int(max(0, min(255, v * k + h * 255 * (i == 1)))) for i, v in enumerate(c))


def leaf(draw, cx, cy, length, width, ang, col, rng, rib=True):
    # lanceolate/oval leaf as a polygon, darker edge, lighter midrib
    pts = []
    for t in np.linspace(0, 2 * math.pi, 40):
        x = length / 2 * math.cos(t)
        y = width / 2 * math.sin(t) * (1 - 0.35 * math.cos(t)) ** 0.5  # slightly wider near the base
        pts.append((cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)))
    edge = tuple(int(v * 0.72) for v in col)
    draw.polygon(pts, fill=col + (255,), outline=edge + (255,))
    # light side: half the leaf a touch brighter (fake lighting)
    half = [p for p, t in zip(pts, np.linspace(0, 2 * math.pi, 40)) if t <= math.pi] + [pts[0]]
    hi = tuple(min(255, int(v * 1.12)) for v in col)
    draw.polygon(half, fill=hi + (255,))
    if rib:
        rc = tuple(min(255, int(v * 1.35)) for v in col)
        x0, y0 = cx - length / 2 * 0.9 * math.cos(ang), cy - length / 2 * 0.9 * math.sin(ang)
        x1, y1 = cx + length / 2 * 0.85 * math.cos(ang), cy + length / 2 * 0.85 * math.sin(ang)
        draw.line([(x0, y0), (x1, y1)], fill=rc + (255,), width=max(1, int(width * 0.06)))


def cluster(path, size, kind, seed):
    col, cover = stats(path)
    rng = random.Random(seed)
    W = size * SS
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    spec = {  # leaf length, width (fraction of tile), target coverage scale, rib
        "olive": (0.20, 0.045, 1.0, True), "broad": (0.20, 0.10, 1.0, True), "hedge": (0.10, 0.055, 1.0, True),
        "column": (0.26, 0.07, 1.0, True), "palm": (0.85, 0.06, 1.0, True), "pine": (0.13, 0.010, 1.0, False),
    }[kind]
    L, Wd, _, rib = spec
    target = cover  # keep the original alpha coverage so the canopy density reads the same
    n = 0
    while True:
        a = np.asarray(im.split()[3].resize((128, 128)))
        if (a > 127).mean() >= target or n > 4000:
            break
        if kind == "palm":
            # a few long blades fanning from the lower left, as in the original
            cx, cy = rng.uniform(0.3, 0.7) * W, rng.uniform(0.25, 0.75) * W
            ang = rng.uniform(-2.2, -0.6)
        else:
            r = rng.random() ** 0.6 * 0.42
            t = rng.uniform(0, 2 * math.pi)
            cx, cy = (0.5 + r * math.cos(t)) * W, (0.5 + r * math.sin(t)) * W
            ang = rng.uniform(0, math.pi)
        s = rng.uniform(0.75, 1.2)
        leaf(d, cx, cy, L * W * s, Wd * W * s, ang, jitter(tuple(col), 0.18, rng), rng, rib)
        n += 1
    return im.resize((size, size), Image.LANCZOS), n, cover


def bark(path, w, h, seed):
    col, _ = stats(path)
    rng = np.random.default_rng(seed)
    W, H = w * SS, h * SS
    base = np.ones((H, W, 3)) * col
    x = np.arange(W)
    streak = np.zeros(W)
    for f in (3, 7, 17, 41):  # vertical fibres at several scales
        streak += rng.normal(0, 1, W // f + 2).repeat(f)[:W] / math.sqrt(f)
    streak = (streak - streak.min()) / (np.ptp(streak) + 1e-6) - 0.5
    noise = rng.normal(0, 0.05, (H // 8 + 1, W // 2 + 1)).repeat(8, 0).repeat(2, 1)[:H, :W]
    img = base * (1 + 0.55 * streak[None, :, None] + noise[..., None])
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").filter(ImageFilter.GaussianBlur(0.6))
    return im.resize((w, h), Image.LANCZOS).convert("RGBA")


def main(src, out):
    kinds = {1: "olive", 2: "broad", 3: "hedge", 4: "column", 5: "palm", 6: "pine"}
    b = bark(f"{src}/img0.png", 512, 1024, 0)
    b.save(f"{out}/planting_tex_0.png")
    print("0 bark 512x1024")
    for i, k in kinds.items():
        im, n, cover = cluster(f"{src}/img{i}.png", 1024, k, i)
        im.save(f"{out}/planting_tex_{i}.png")
        a = np.asarray(im.split()[3].resize((128, 128)))
        print(i, k, "leaves", n, "coverage original %.2f new %.2f" % (cover, (a > 127).mean()))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
