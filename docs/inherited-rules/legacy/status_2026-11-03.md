# Current status

Checked 2026-11-03 17:00 Asia/Dubai. This is the handoff. Read it with [legacy/AGENTS.md](legacy/AGENTS.md) and [legacy/SCORE_PLAN.md](legacy/SCORE_PLAN.md).

## Where the work is

- GitHub: https://github.com/Bigc7292/legacy-archive (private, Bigc7292)
- Live viewer: https://legacy-house-viewer.vercel.app
- Bot disk: `/workspace/legacy/`
- Release snapshot that seeded this repo: tag `legacy-full-2026-11-03`, commit `bb65e67`

The old note that this repo was "transcripts only" is wrong. The tree is the Legacy workspace plus `vercel-live/`.

## What the public URL is actually serving

Checked with curl on 2026-11-03. Do not guess from a local file.

| File | Live bytes | What it is |
|---|---|---|
| `app.js?v=19` | 1,219,782 | Freeze fix, classic script, dollhouse lid hide |
| `hero.glb` | 1,927,812 | Textured baked hero. 3 meshes, 5 images, 39,276 verts. This is the good building. |
| `hero_m.glb` | 1,740,244 | Mobile copy of that hero |
| `twobed.glb` | 1,476,656 | Older flat. Not the 19 MB BlenderKit flat |
| `twobed_m.glb` | 1,340,160 | Mobile flat |

`vercel-live/index.html` in git is already `app.js?v=21` and the desktop flat URL is `twobed.glb?v=3` (the 19 MB file). That bundle is in the repo. The public URL is still on `v=19` and the 1.5 MB flat. Do not deploy unless Colin says deploy.

## Why the building looked worse

Commit `315f85b` replaced the web hero with an unbaked door-test export: 2,402,120 bytes, 1,618 meshes, 2 images. That file is a test, not the scored building. Commit `2abe4ed` put the textured hero back and cache-busted the URLs (`hero.glb?v=2`, `hero_m.glb?v=2`). The live site is serving the restored files.

Do not copy `tests/door_r5/` or `tests/door_r6/` over `vercel-live/hero.glb` or `legacy/web/hero.glb`.

## Scores

Target is **8/10** on a locked camera against the named photo. A bot does not score its own still. Under 8 goes back for one fix.

| Check | Score | Against |
|---|---|---|
| Exterior, street | about 6 | Commons 2015, Geograph Jul 2025 |
| Door pieces only | 5.3 (lions 5, jambs 3, transom 8) | `legacy/refs/door.jpg` |
| Flat, Blender | 5 | Rightmove CGI |
| Flat, viewer | 4 | same |

The door 5.3 is not the building score. The building is still about 6. The "3" people remember is Critic Round 1 (3/10, then an interior critic at 2/10) from before the Round 2–4 fixes. It is not a regression from 6.

## Open pass

**Interior.** The viewer still loads the 1.5 MB flat (`twobed.glb?v=4`). The Home Builder file `legacy/tests/interior/hb_flat.blend` has the kitchen on the south wall (worktop, splash, island, appliances) and a bathroom in the south-west room. The WC and the shower are stand-ins. Home Builder has no product for either. Not merged.

## Tests on disk that are not merged

None of these replace `out/` or the live hero. They were missing from git until the documentation commit that added this file's date.

| Pass | Evidence | State |
|---|---|---|
| E1 portal | `legacy/tests/door_r6/` | Camera locked. Not a pass. |
| E5 one arch | `legacy/tests/arcade/arch.png` | Fan of bars reads. Voussoirs are blocky. Not merged. |
| E6 fire escape | `legacy/tests/escape/escape.png` | Switchback on a stand-in wall. Tread size is a stand-in (going 250 mm, rise 200 mm). Not merged. |
| E7 viaduct brick | `legacy/tests/surr/viaduct_r5.png` | Sunlit parapet reads red, not salmon. Not merged. |
| I1 dollhouse | viewer | Live `v=19` hides a mesh named `Ceiling*` when the preset is `interior` or the camera is at or above 2.95 m. The blue box was that lid (`Ceiling_BAKED`, about `#44526b`). |
| I2 bathroom | `legacy/tests/bath/bath.png` | Basin, mirror, WC, rail, shower are in the test. The light is blown out. Not in the flat. |
| Home Builder shell | `legacy/tests/interior/hb_flat.png` | Kitchen on the south wall, bathroom in `hb_bath.png`. WC and shower are stand-ins. Not merged. |

## Interior furniture

The 19 MB BlenderKit swap is reverted in git (`5e9ecda`). The viewer file is the 1.5 MB flat again. The BlenderKit API key is in the local Blender 5.2 preferences only. It is not in this repo.

## Rules

`legacy/AGENTS.md` is the pipeline. `CLAUDE.md` and `GROK.md` are the same text.

- Free tools only.
- No invented measurements. Stand-ins are labelled. Missing facts stay `NOT FOUND`.
- One change set, then a locked-camera render, then an independent critic. Log the round in `critic_log.md`.
- Commit and push to this repo after every code or asset change.
- Do not deploy or alias Vercel unless Colin says deploy.
- Never commit API keys. Never add a file over 99 MB.

## Continue from here

1. Clone this repo.
2. Read this file, then `legacy/AGENTS.md`, then `legacy/SCORE_PLAN.md`, then the last round in `legacy/critic_log.md`.
3. Next build step is E1 only, same camera as `legacy/tests/door_r6/portal.png`.
4. Leave the live textured hero alone.
