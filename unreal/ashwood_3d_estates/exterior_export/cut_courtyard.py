import json
import struct
import os

inp = r'C:\Users\Alfa\.gemini\antigravity\scratch\ashwood-estates-3d\unreal\ashwood_3d_estates\exterior_export\villa_v4.glb'
out = r'C:\Users\Alfa\.gemini\antigravity\scratch\ashwood-estates-3d\unreal\ashwood_3d_estates\exterior_export\villa_v5.glb'

with open(inp, 'rb') as f:
    b = f.read()

magic, version, length = struct.unpack('<III', b[:12])
chunk_len, chunk_type = struct.unpack('<II', b[12:20])
gltf = json.loads(b[20:20+chunk_len].decode('utf-8'))
bin_data = bytearray(b[20+chunk_len+8:])

# Find node GF_plinth
plinth_node = None
for n in gltf['nodes']:
    if n.get('name') == 'GF_plinth':
        plinth_node = n
        break

if not plinth_node:
    raise Exception("GF_plinth node not found!")

orig_mesh = gltf['meshes'][plinth_node['mesh']]
mat_idx = orig_mesh['primitives'][0]['material']

# Courtyard cutout bounds in X and Z:
# X: 11.476 to 15.834 (cut right side)
# Z: 11.496 to 16.344 (cut middle section)
# Full plinth: X [3.076, 15.834], Z [4.756, 26.794], Y [0.0, 0.454]

boxes = [
    # Box 1: Rear plinth (Z from 4.756 to 11.496, full width)
    ([3.076, 0.0, 4.756], [15.834, 0.454, 11.496]),
    # Box 2: Front plinth (Z from 16.344 to 26.794, full width)
    ([3.076, 0.0, 16.344], [15.834, 0.454, 26.794]),
    # Box 3: Left plinth beside courtyard (X from 3.076 to 11.476, Z from 11.496 to 16.344)
    ([3.076, 0.0, 11.496], [11.476, 0.454, 16.344])
]

def make_box(mn, mx):
    x0, y0, z0 = mn
    x1, y1, z1 = mx
    P = []
    N = []
    def quad(a, b, c, d, norm):
        for v in [a, b, c, a, c, d]:
            P.extend(v)
            N.extend(norm)
    # Top (+Y)
    quad([x0, y1, z0], [x0, y1, z1], [x1, y1, z1], [x1, y1, z0], [0, 1, 0])
    # Bottom (-Y)
    quad([x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1], [0, -1, 0])
    # Front (+Z)
    quad([x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1], [0, 0, 1])
    # Back (-Z)
    quad([x1, y0, z0], [x0, y0, z0], [x0, y1, z0], [x1, y1, z0], [0, 0, -1])
    # Right (+X)
    quad([x1, y0, z1], [x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [1, 0, 0])
    # Left (-X)
    quad([x0, y0, z0], [x0, y0, z1], [x0, y1, z1], [x0, y1, z0], [-1, 0, 0])
    return P, N

all_P = []
all_N = []
for mn, mx in boxes:
    P, N = make_box(mn, mx)
    all_P.extend(P)
    all_N.extend(N)

# Append to bin_data
pad = (4 - len(bin_data) % 4) % 4
bin_data.extend(b'\x00' * pad)

pos_bytes = struct.pack(f'<{len(all_P)}f', *all_P)
pos_off = len(bin_data)
bin_data.extend(pos_bytes)

norm_bytes = struct.pack(f'<{len(all_N)}f', *all_N)
norm_off = len(bin_data)
bin_data.extend(norm_bytes)

# Add bufferViews
gltf['bufferViews'].append({
    'buffer': 0,
    'byteOffset': pos_off,
    'byteLength': len(pos_bytes),
    'target': 34962
})
pos_bv = len(gltf['bufferViews']) - 1

gltf['bufferViews'].append({
    'buffer': 0,
    'byteOffset': norm_off,
    'byteLength': len(norm_bytes),
    'target': 34962
})
norm_bv = len(gltf['bufferViews']) - 1

# Add accessors
min_x = min(all_P[0::3]); max_x = max(all_P[0::3])
min_y = min(all_P[1::3]); max_y = max(all_P[1::3])
min_z = min(all_P[2::3]); max_z = max(all_P[2::3])

gltf['accessors'].append({
    'bufferView': pos_bv,
    'componentType': 5126,
    'count': len(all_P) // 3,
    'type': 'VEC3',
    'min': [min_x, min_y, min_z],
    'max': [max_x, max_y, max_z]
})
pos_acc = len(gltf['accessors']) - 1

gltf['accessors'].append({
    'bufferView': norm_bv,
    'componentType': 5126,
    'count': len(all_N) // 3,
    'type': 'VEC3'
})
norm_acc = len(gltf['accessors']) - 1

# Create new mesh for GF_plinth
new_mesh = {
    'name': 'GF_plinth_courtyard_cutout',
    'primitives': [{
        'attributes': {
            'POSITION': pos_acc,
            'NORMAL': norm_acc
        },
        'material': mat_idx,
        'mode': 4
    }]
}
gltf['meshes'].append(new_mesh)
plinth_node['mesh'] = len(gltf['meshes']) - 1
if 'translation' in plinth_node: del plinth_node['translation']
if 'scale' in plinth_node: del plinth_node['scale']

# Update buffer length
gltf['buffers'][0]['byteLength'] = len(bin_data)

# Pack GLB
json_str = json.dumps(gltf)
json_bytes = json_str.encode('utf-8')
pad_j = (4 - len(json_bytes) % 4) % 4
json_bytes += b' ' * pad_j

total_len = 12 + 8 + len(json_bytes) + 8 + len(bin_data)

header = struct.pack('<III', 0x46546C67, 2, total_len)
json_chunk_hdr = struct.pack('<II', len(json_bytes), 0x4E4F534A)
bin_chunk_hdr = struct.pack('<II', len(bin_data), 0x004E4942)

with open(out, 'wb') as f:
    f.write(header)
    f.write(json_chunk_hdr)
    f.write(json_bytes)
    f.write(bin_chunk_hdr)
    f.write(bin_data)

print(f"Successfully created {out} (size {os.path.getsize(out)} bytes)")
