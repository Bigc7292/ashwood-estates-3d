# Lane 5-critic: Critic

Read first: `AGENTS.md`, `STATUS.md`, `production-line/README.md`, `production-line/QUEUE.md`.

**Owns:** production-line/critic/

**Task:** Independent review, never the builder's own. Compare each change against the references (generated images, brochure renders, V4 plans) using side-by-side renders. Score it and list defects. Output: CRITIC-PASS or CRITIC-FAIL with a defect list. Never edit model files.

**Done when:** a hand-off note exists in `production-line/handoffs/` for each item, with status and evidence paths, and the integrator has logged it.
