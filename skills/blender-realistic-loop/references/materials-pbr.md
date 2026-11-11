# Materials

Principled / MeshPhysical numbers that read in a terrace shot. Change one at a time.

| Surface | Base | Roughness | Metal | Notes |
|---|---|---|---|---|
| Limestone wall | `0xd4c0a0` | 0.72 | 0 | Triplanar, tile under 2 m, darken the foot |
| Terrace slab | `0xe6dcc8` | 0.55 | 0 | Joints every 0.6–1.2 m, not the wall texture |
| Pool water | `0x082833` at dusk, `0x0c7490` by day | 0.02 | 0 | Mirror of the house, then a small ripple. IOR 1.33 |
| Glass | reflection of outside | — | — | Dusk adds a warm room at under 0.5 mix |
| Bronze frame | `0x4a3424` | 0.28 | 0.86 | Thin, in front of the glass |
| Teak | `0x9b6d43` | 0.62 | 0 | Grain along the long axis |
| Cushion | `0xece5d8` | 0.95 | 0 | A cushion is a soft volume, not a box |
| Leaf | greens around `0x3e6a32` | 0.6 | 0 | Two or three greens, alpha cards, not a solid |

Do not set transmission on a window that has nothing built behind it. A mirror plus a weak warm interior reads better than a view into an empty shell.
