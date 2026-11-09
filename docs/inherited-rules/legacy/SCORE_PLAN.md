# Score plan

Gate: match the online photos. Working number is **8/10** on a locked camera against the named photo. A bot does not score its own still. The orchestrator looks, then an independent critic writes the number in `critic_log.md`. Under 8 goes back for one fix. No new idea.

Do not merge a `tests/` file into `out/` or the live viewer until that pass is at 8. Do not deploy the archive onto [legacy-house-viewer.vercel.app](https://legacy-house-viewer.vercel.app/).

## Current scores

| Check | Score | Photo |
|---|---|---|
| Exterior, street | about 6 | `refs/critic1/real_geograph.jpg`, `real_commons.jpg` |
| Door | 5.3 (lions 5, jambs 3, glass 8) | `refs/door.jpg` |
| Flat, Blender | 5 | Rightmove CGI in `refs/critic1/` |
| Flat, viewer | 4 | same |

## Order

One pass at a time on the exterior. Interior passes may run beside them only if they do not write `out/`, `web/`, or the hero GLB.

| # | Pass | Done when the still shows | Status |
|---|---|---|---|
| E1 | Open portal | No doors. Stairs inside. LEGACY HOUSE band. | `tests/door_r8/door.png` on the locked camera. Solid treads, dark risers, a landing, and side walls in the opening. Not scored. Not merged. |
| E2 | Jambs | Leaf trail on darker granite, both sides. Not diamond studs. | One overlapping trail per jamb in the same still. Still a stand-in, not a carved acanthus. Not scored. |
| E3 | Lions | Mane, ears, face, on the outer corners of the name band. | Radiating mane, ears, muzzle. Still geometric. Not scored. |
| E4 | Transom | Diamond lattice set in the stone frame. | Lattice exists. Leave it until E1–E3 pass. |
| E5 | One arch, then the row | Fan of white bars, dark lower panel, voussoirs that sit in the wall. | `tests/arcade/arch.png` fan reads. Voussoirs are blocky. Not merged. |
| E6 | Fire escape | Switchback on the real west wall, not a plain box. | `tests/escape/escape.png` is a stair on a stand-in wall. Not merged. |
| E7 | Viaduct brick | Sunlit parapet stays red. | `tests/surr/viaduct_r5.png` reads red. Not merged. |
| I1 | Dollhouse | No blue lid. Rooms still have a ceiling. | Fixed in `web/src/app.js` only. Not deployed. |
| I2 | Bathroom | Basin, mirror, WC, rail, shower, in the flat, not blown out. | `tests/bath/bath.png` has the fittings. Light is blown out. Not in the flat. |

## After a pass hits 8

Export hero and surroundings, `./make_mobile.sh`, `./validate.sh` must PASS, then deploy the viewer files only.

## Next

E1 is `tests/door_r8/door.png`. Rise, going, leaf size and the lions are still stand-ins. Do not copy that GLB over the live hero.
