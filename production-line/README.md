# Ashwood production line

Six lanes of AI workers run in parallel on separate tasks. Everything follows `AGENTS.md` (the 7-step rule set, the change log and push rule, and the Ashwood input rules).

## Lanes and ownership

| Lane | Brief | Owns (may write) | Never writes |
|---|---|---|---|
| 1 Facts | `lanes/1-facts.md` | `production-line/facts/` | any model or viewer file |
| 2 Exterior builder | `lanes/2-exterior.md` | `exterior-garden-3d/4b/` (new step folders and `blender_wip/` only) | official `4b_*.blend`, renders, or view files without critic sign-off |
| 3 Interior builder | `lanes/3-interior.md` | `active/floorplan3d-spike/FP-4B-GF/` (`courtyard_feature.js`, new build files) | `index.html` or `data/` without critic sign-off |
| 4 Viewer | `lanes/4-viewer.md` | viewer artifact build files under `production-line/viewer/` | source plans and approved V4 files |
| 5 Critic | `lanes/5-critic.md` | `production-line/critic/` (reports only) | any model, viewer or plan file |
| 6 Integrator | `lanes/6-integrator.md` | `CHANGELOG.md`, `STATUS.md`, `production-line/QUEUE.md` | nothing gets merged or pushed to `main` without Colin's go-ahead |

## Rules for every lane
1. Take one item at a time from `QUEUE.md`, marked with your lane name. Only one item per lane.
2. Write a hand-off note at the end of the item in `production-line/handoffs/<item-id>.md`: what changed, files touched, evidence (paths to renders or checks), open issues, and status (WIP / REVIEW-PENDING / DONE).
3. Never mark a step DONE. Only the critic (lane 5) and then Colin pass a gate.
4. Never touch `ACTIVE_PIPELINE.json`, `active/approved-cad-v4/`, or `superseded_2026-11-09/`.
5. Branch: `claude/rules-and-status`. Every change set is logged in `CHANGELOG.md` and pushed by the integrator in the same turn.
6. If two lanes need the same file, the queue says which lane goes first. The other lane waits.
7. Each lane may work on its own `lane/<name>` branch; the integrator merges into `claude/rules-and-status`. `scripts/verify_active_pipeline.py` rewrites `active/pipeline_verification.json`: only the integrator runs it, in its own worktree.

## Flow
Queue item → builder lane (2 or 3, or 4 for the viewer) → critic lane (5) reviews against the references → integrator (6) logs, commits and pushes → Colin's review.

## Status vocabulary
WIP / REVIEW-PENDING / CRITIC-PASS / CRITIC-FAIL / DONE (Colin's gate only).
