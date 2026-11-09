# Axis3D: plan (v0.1, 2026-11-08). Plan only: nothing is built yet.

**What it is:** a web app (SaaS) for real-estate developers and agencies. A client uploads one brochure PDF of an off-plan project, plus an optional link to the project's web page. The app checks whether there is enough to work with, extracts the facts, plans, layouts and images, and produces an interactive 3D model of each unit type, a fact sheet, and a shareable link.

**Quality bar:** the Legacy project viewer (live: legacy-house-viewer.vercel.app) and the Kimi "Courtyard Residence" template. Both are walkable, with time-of-day lighting, preset cameras, interiors and a dollhouse view.

**Where this lives:** branch `axis3d-plan` of `legacy-archive`, folder `axis3d/`. This session cannot create new GitHub repositories. Once Colin creates an empty private repo `Bigc7292/axis3d`, this folder moves there with its history, and all work continues on branches. `main` there is only updated when Colin says.

## 1. Decisions taken (Colin, 2026-11-08)
| Topic | Decision |
|---|---|
| Repo | New repo `axis3d`. Carry over all Legacy rules, pipeline, lessons and tricks (see `AGENTS.md` here). |
| AI reading | For now, Opus 5.5 inside Claude does the AI reading and checking during development and the scenario tests. Once deployed outside Claude, the app uses open-source models through an OpenAI-compatible endpoint (Ollama, vLLM, or a free/self-hosted provider). A rule-based extractor always runs first, free. |
| Accounts | v1 has no login. Projects are saved in the browser (IndexedDB). Accounts and a database come in v2. |
| Process | Plan first, build only after Colin approves this plan. 5 real-world scenario tests; Ashwood Estates is test 1. |

## 2. What the client sees (user flow)
1. **Landing:** what you get, the minimum requirements (up front), example output, pricing (copy from the investor pitch, later).
2. **New project:** one PDF drop zone (required) and one URL field (optional), with "What we need" printed beside them (section 3). No separate uploads for plans, photos or facts: the app finds those itself.
3. **Analysis (live progress):** reading the PDF, then finding plans, finding images, reading facts, then visiting the URL, then checking requirements. Each step shows what it found.
4. **Report:** **Accepted** or **Rejected**, with a reason per requirement. Every fact shows its source ("brochure p.24", "website", or "assumption"). Conflicts between sources are listed for the client to confirm.
5. **3D model:** one per unit type (for example 4 / 5 / 6 bed). Exterior, interior walk-through, floor-by-floor dollhouse, time of day, room labels and sizes, and the source plan shown next to the model.
6. **Outputs:** a fact sheet (print to PDF), a share link, and a GLB download.

## 3. Minimum requirements (the gate), measured, not guessed
| # | Requirement | How the app checks it | Ashwood result (from Claude's read, 2026-11-08) |
|---|---|---|---|
| R1 | A brochure PDF with selectable text (not a scan) | pdf.js text layer: at least 200 words over the document | ✔ 38 pages, text on most pages (some decorative fonts come out garbled and are ignored) |
| R2 | At least one floor plan per unit type, with printed room dimensions (at least 3 rooms "W x L m") or a printed floor area, so the model can be scaled | page classifier, room-dimension pattern, area pattern | ✔ 4/5/6-bed plans on pp.27–28, 31–32, 35–36. Rooms printed, e.g. "FAMILY LIVING/DINING 12.40m x 5.10m"; GF/FF/roof areas printed |
| R3 | At least 8 photos or CG renders, 1920 px or more on the long edge | embedded image sizes; renders told apart from plans and maps | ✔ 13 full-page renders at 1920×1080 (pp.2, 8, 12–14, 16–17, 25–26, 29–30, 33–34), plus smaller ones. Pp.1 and 3 are paper textures at the same size and must not count. |
| R4 | Core facts: project name, developer, location, unit types | text patterns, then an AI pass | ✔ Ashwood Estates; Wasl (from the website); Jumeirah Golf Estates, Dubai; 4/5/6-bed villas |
| R5 (optional) | Building height or storeys, specification, unit counts | same | ✔ "G+1+R (14m)"; 185 villas = 108 / 47 / 30 plus clubhouse; stone cladding, WPC fluted, aluminium frames, laminated glass balustrade |

**If something is missing,** the app tries in this order. Only after all of these fails does it reject:
1. The URL.
2. The rest of that website (same domain: gallery, floor-plan and brochure pages).
3. A web search for the project.
4. For imagery only: clearly labelled *concept* visuals. These are never presented as developer renders.

A missing R2 (no dimensioned plan) is never filled by invention: the project is rejected with "send a dimensioned plan for unit type X".

## 4. Pipeline (each stage is a module with a test, and each output carries its source)
**A. Ingest (in the browser, pdf.js, free).** Text with positions for each page, each page rendered at 2× and 4× (for plans), and the embedded images extracted.

**B. Classify pages.** Each page gets a label: plan, render, facts, map, masterplan or divider. Signals:
- room-dimension pattern (`\d+\.\d+m x \d+\.\d+m`)
- "FLOOR" together with "Sq.m"
- one large image with fewer than 15 words
- a light background with dark-grey line work

For Ashwood, the plans are pp.27–28, 31–32 and 35–36; p.24 is the facts table; p.5 is the location map; p.6 is the masterplan.

**C. Facts.** Pattern rules first: units, bedrooms, plot area, saleable area, floor areas, heights, price, payment plan, handover, amenities, spec. Then an AI pass that fills gaps and resolves wording, and must quote its source text. Rules:
- Numbers keep units and source page.
- Conflicts are kept, not overwritten. Ashwood examples:
  - The 4-bed ground floor is 263.01 m² in p.27's panel, but 266.2 m² in p.27's text layer.
  - The website says Dubai International Airport is 40 min away, which the brochure doesn't mention.
  - The website lists Palm Jumeirah at 25 min; the brochure says 30 min.

**D. URL agent (Vercel serverless function, free tier).** The browser cannot fetch other sites (CORS), so a small function does it. It:
- fetches the page, follows same-domain links to gallery, plan and brochure pages, and respects robots.txt
- collects images (converting AVIF/WebP), plan images, the brochure link, a Google Maps link or coordinates, and the facts
- de-duplicates images against the PDF (perceptual hash)

For Ashwood, the website adds:
- the 3 floor-plan images, as AVIF (4-, 5- and 6-bed)
- 5 project images
- prices: from AED 11.8M, 15.9M and 20.2M
- the 50/50 payment plan and Q4 2028 handover
- the developer, Wasl Properties
- a Maps search link (no coordinates)

**E. Decision.** Rule-based, using section 3, plus a written report.

**F. Plan to 3D (the core).** For each unit type and floor:
1. Crop the plan from the page render at 4×.
2. Make colour masks: walls (the solid dark grey), glazing and thin lines, pool (cyan), planting (green), and the plot outline.
3. Place each room label at its text position, then flood-fill the room around it inside the wall mask to get the room's pixel box.
4. Work out the **scale (px per metre)** from every printed room size ("4.00m x 5.10m"), using the median and dropping outliers.
5. **Check against the printed floor area** (Ashwood GF 263.01 m²). If they differ by more than 5%, flag it and do not ship that floor without review.
6. Line floors up (GF / FF / roof) on stairs, lift and outer walls.
7. Extrude: wall height comes from the storey height. Ashwood gives only "G+1+R (14m)", so the per-floor height is an **assumption** and labelled as one.
8. Openings: door gaps in the mask become doors. Facade glazing follows the renders and spec ("floor-to-ceiling windows"); it is labelled where assumed.
9. Pools, terraces, balconies, courtyard and planting come from the masks.

Output: one GLB per unit type, plus a JSON "evidence map" (which plan pixels and which text made each wall or room).

**G. Look (Legacy 7-step process, adapted).**
1. Reference: the developer's renders.
2. Layout: from F.
3. Blockout.
4. Finish: materials from the spec and colours sampled from the renders (travertine-look stone, WPC fluted panels, bronze aluminium frames, glass balustrades). These are new builds, so there is no grime step; instead there are clean-finish details (shadow gaps, reveals, lighting).
5. Printed matter: the project name and logo at the entrance, if shown in the renders.
6. Critique: side by side with the renders.
7. Motion: an optional flythrough video.

**H. Viewer.** Built from the Legacy viewer:
- three.js, AgX tone mapping, SSAO, bloom
- a sky shader with time of day
- presets: street, garden, aerial, each room, dollhouse
- a floor toggle and a unit-type switch
- room labels with printed sizes
- an evidence panel (source plan or render next to the model)
- phone files and a phone layout

**I. Fact sheet.** A printable HTML page, saved as PDF: facts with sources, unit schedule, plan thumbnails, gaps and assumptions.

## 5. Architecture (all free tiers)
- **Front end:** Vite + vanilla JS modules (or Preact if the UI grows), three.js, pdf.js. Everything heavy runs in the browser, so there is no server cost per project.
- **Back end:** Vercel serverless functions only for what the browser can't do: `api/fetch-url` (page plus same-domain crawl), `api/image` (proxy and AVIF conversion), and later `api/ai` (an OpenAI-compatible relay to an open model; the key stays server-side and is never committed).
- **Storage v1:** IndexedDB in the browser (project, extracted pages, images, GLBs).
- **v2:** accounts and shared storage (Supabase free tier, or similar), share links that work for other people, and an admin view.
- **AI adapter:** one interface, `extract(pages, images) -> facts + sources`. Implementations:
  - (a) rules (always)
  - (b) "Claude in the loop": during development, Opus reads the same pages and writes the JSON, which the app imports
  - (c) an OpenAI-compatible endpoint (Qwen2.5-VL or Llama 3.2 Vision on Ollama/vLLM) for when the app is deployed

## 6. Five real-world scenario tests (QA programme)
Each test: run the real PDF and URL end to end, then:
- record every snag in `docs/QA_REGISTER.md` (id, stage, severity, evidence, fix, verified)
- fix
- run an **optimisation pass** aimed at that test's class of defects before the next test

Pass criteria for each test:
- correct accept/reject
- facts match sources, with conflicts flagged
- every unit type has a model that passes the area check (±5%)
- the viewer loads with no console errors on desktop and phone
- the model is compared side by side with the plan and with a render

| Test | Project | Inputs |
|---|---|---|
| 1 | Ashwood Estates, Jumeirah Golf Estates (villas, 3 types) | brochure PDF (38 pp) + eva.realestate URL |
| 2–5 | Colin to choose. Aim for variety: an apartment tower, a townhouse cluster, a scanned or weak brochure (should be rejected), a URL-only gap fill | |

Lessons already learned from the Kimi build, carried over so they aren't repeated:
- **Never fall back to a demo model:** if a project's model can't be built, say so.
- Accepted intake must unlock the model view. Status names must agree between stages.
- **Additive database migrations only** (v2).
- **Readiness signals for tests:** wait for "scene ready" and "images decoded", never "network idle".
- **Renderer cost:** cached static shadows, a capped pixel ratio, and redrawing only on change.
- **Phone first frame:** a wider camera on narrow screens; no opening animation overriding it.
- **No sample/demo projects in the product.**

## 7. Milestones (each ends with a commit, push and a short note to Colin)
| M | Deliverable | Done when |
|---|---|---|
| M0 | Repo, rules, CI checks (glTF validator, lint), empty app shell | Colin has approved this plan; the repo exists |
| M1 | Intake + ingest + page classifier + facts (rules) + report | Ashwood report matches section 3 with sources |
| M2 | URL agent | Ashwood URL adds plans, images, prices and Maps; dedupe works |
| M3 | Plan to 3D, ground floor of the 4-bed | walls, pool and rooms traced; scale from room sizes; area within 5% |
| M4 | All floors and all three unit types; viewer with presets, dollhouse and floors | test 1 passes the pass criteria |
| M5 | Look pass (materials from spec and renders); critic round vs renders | the critic score is logged |
| M6 | Fact sheet, share link (same device), GLB download; scenario test 1 closed and optimisation pass done | QA register closed for test 1 |

## 8. Risks and honest limits
- **"Ultra-realistic" is the target, not what v1 delivers on day one.** v1 gives *plan-accurate* geometry with good materials and lighting. Matching the developer's CGI exactly (furniture, landscaping and facade detail beyond the plan) takes the look pass, and per-project critique rounds after it.
- **Plan styles vary.** Ashwood's are clean (solid grey walls). Hatched, line-only or scanned plans need more tracing modes, and will be the subject of tests 2–5.
- **Website access:** some sites block automated fetches or need JavaScript; the URL agent reports this instead of failing silently. AVIF images need conversion.
- **Rights:** clients must own or have permission to use the brochure and website material. That goes in the terms of service. In the tests we use the material only to check the pipeline.
- **Cost:** everything above runs on free tiers. Open-model hosting for AI costs money if not self-hosted; flagged before switching on.

## 9. Questions for Colin (before M0)
1. Create the empty private repo `Bigc7292/axis3d` (or tell me another name), and attach it to this session.
2. Keep the name **Axis3D** and the Kimi brass-on-ink look, or a new brand?
3. Projects for scenario tests 2–5 (or should I pick them?).
