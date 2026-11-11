# Boomtown on Ashwood

Vendored from https://github.com/0xwast3/boomtown (MIT). The three example films in docs/media are not in this copy. The stills and the code are.

Use this skill when a new house or estate concept is asked for as a measured code model: a construction terminal, an assembly film, or a house built part by part from a plan or a photo. Read SKILL.md, then docs/JOB_DESCRIPTION.md, before writing a house.

Do not use it to restyle the Ashwood villa viewer. That page stays the photoreal model in exterior-garden-3d/4b/. Boomtown's ink-and-flat-colour look is for a new concept build, not a replacement for the villa grass, water and stone.

A house outside this folder is one model.js. Build it with:

    node skills/boomtown/tools/build.mjs ./my-house

Run npm install inside skills/boomtown once before the first build. The film needs ffmpeg.
