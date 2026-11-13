"""Cut an interior floor GLB into ~4 x 4 m tiles so each gets its own Lumen cards and distance field.

    python make_tiles.py <in.glb> <out dir> <prefix> <ox> <oy> <oz> <x0> <x1> <y0> <y1> <z0> <z1> [tile cm]

Coordinates in Unreal world cm (same convention as edit_glb.js). Writes <prefix>_r<row>_c<col>.glb (empty tiles skipped)
and <prefix>_tiles.json listing them.
"""
import json, math, os, subprocess, sys, tempfile

inp, out, prefix = sys.argv[1:4]
ox, oy, oz, x0, x1, y0, y1, z0, z1 = map(float, sys.argv[4:13])
T = float(sys.argv[13]) if len(sys.argv) > 13 else 400.0
here = os.path.dirname(os.path.abspath(__file__))
edit = os.path.join(here, '..', '..', 'ashwood_3d_estates', 'interior_export', 'edit_glb.js')
nx, ny = math.ceil((x1 - x0) / T), math.ceil((y1 - y0) / T)
tiles = []
for r in range(ny):
    for c in range(nx):
        b = [x0 + c * T, min(x1, x0 + (c + 1) * T), y0 + r * T, min(y1, y0 + (r + 1) * T), z0, z1]
        name = f'{prefix}_r{r}_c{c}'
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump({'tile': {'origin': [ox, oy, oz], 'ops': [{'op': 'clipTo', 'box': b}]}}, f); ops = f.name
        res = subprocess.run(['node', edit, inp, os.path.join(out, name + '.glb'), ops, 'tile'], capture_output=True, text=True)
        os.unlink(ops)
        info = json.loads(res.stdout)
        if info['tris'] == 0:
            os.unlink(os.path.join(out, name + '.glb')); continue
        tiles.append({'name': name, 'box': b, 'tris': info['tris']})
        print(name, info['tris'])
json.dump({'source': inp, 'origin': [ox, oy, oz], 'tile_cm': T, 'tiles': tiles}, open(os.path.join(out, prefix + '_tiles.json'), 'w'), indent=1)
print(len(tiles), 'tiles')
