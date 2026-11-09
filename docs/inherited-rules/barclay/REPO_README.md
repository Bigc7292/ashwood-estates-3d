# Barclay House Archive

Private archive of the Barclay House 3D work (35 Whitworth Street West, Manchester). Use this repo to continue in Claude, Cursor, or another agent.

## Start here

1. [status.md](status.md) — what is live, the scores, and the next pass.
2. [barclay/AGENTS.md](barclay/AGENTS.md) — the pipeline. `CLAUDE.md` and `GROK.md` are copies.
3. [barclay/SCORE_PLAN.md](barclay/SCORE_PLAN.md) — the open exterior pass. Target is 8/10 on a locked camera.
4. [CHANGELOG.md](CHANGELOG.md) — what changed, including the hero swap that made the building look worse.

Live viewer: https://barclay-house-viewer.vercel.app

The public site is serving the restored textured hero (1.9 MB, 3 meshes). It is not serving the newer 19 MB flat that sits in `vercel-live/`. Do not deploy unless asked.

## Layout

| Path | What it is |
|---|---|
| `barclay/` | Scripts, critic logs, references, tests, interior, viewer source |
| `vercel-live/` | Files last prepared for the Vercel project. Not the same as what the URL is serving. See status.md. |
| `status.md` | Handoff |
| `CHANGELOG.md` | Change record. `barclay/CHANGELOG.md` is the same text. |

## Bots that produced this

| Bot | Agent ID | Role |
|---|---|---|
| Barclay House 3D | 89b1b343-058f-4753-a2d5-801060c14f25 | Exterior, Blender, critic loop |
| Barclay House Interior | cf945d95-b847-42b1-a8cf-d9e10fdc72bd | Two-bed flat and the viewer |
| Surroundings | ce76ae6f-a141-4509-a971-0757e7768a23 | 120 m context, viaduct, canal |
| Optimizer | ef5c7d31-1d8f-4e40-9f4b-9cfc8977bdfc | Size budgets and audits |

Those bots ran out of usage. The files are in this repo. Do not wait for the bots.

## Rules that override old notes

- Commit and push here after every code or asset change.
- Do not deploy to Vercel unless Colin says deploy.
- Do not replace `hero.glb` with a door-test export. That already happened once (`315f85b`) and was reverted (`2abe4ed`).
- Free tools only. No invented measurements. Stand-ins stay labelled.
