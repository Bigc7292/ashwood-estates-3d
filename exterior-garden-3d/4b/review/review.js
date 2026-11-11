/* Temporary review tab. Screenshot, draw, note, save with camera place. */
(function () {
  const ZONES = [
    { name: "Swimming pool", x: 7.92, z: 2.35, r: 7 },
    { name: "Rear terrace", x: 13.8, z: 4.0, r: 6 },
    { name: "Courtyard", x: 13.54, z: 13.36, r: 6 },
    { name: "Driveway", x: 4.02, z: 27.22, r: 7 },
    { name: "Carport", x: 3.66, z: 25.8, r: 6 },
    { name: "Front approach", x: 9, z: 38, r: 14 }
  ];
  function floorOf(y) {
    if (y < 3.9) return "Ground";
    if (y < 7.7) return "First floor";
    return "Roof";
  }
  function nearest(x, z) {
    let best = null, bestD = 1e9;
    for (const z1 of ZONES) {
      const d = Math.hypot(x - z1.x, z - z1.z);
      if (d < bestD) { bestD = d; best = z1; }
    }
    if (!best || bestD > best.r + 8) return "Open exterior";
    return bestD <= best.r ? best.name : "Near " + best.name;
  }
  function context() {
    if (typeof window.__reviewContext === "function") {
      try {
        const extra = window.__reviewContext();
        if (extra && extra.floor) return extra;
      } catch (e) {}
    }
    const cam = window.__cam;
    const controls = window.__controls;
    const p = cam ? cam.position : null;
    let target = null;
    if (controls && controls.target) target = { x: +controls.target.x.toFixed(2), y: +controls.target.y.toFixed(2), z: +controls.target.z.toFixed(2) };
    else if (cam) {
      cam.updateMatrixWorld();
      const e = cam.matrixWorld.elements;
      target = { x: +(p.x - e[8] * 8).toFixed(2), y: +(p.y - e[9] * 8).toFixed(2), z: +(p.z - e[10] * 8).toFixed(2) };
    }
    const walk = new URLSearchParams(location.search).get("walk") === "1";
    const external = /villa\.html$/.test(location.pathname);
    const interior = /ground-floor\.html$/.test(location.pathname) || /\/ff\//.test(location.pathname);
    const mode = interior ? (walk || (document.body.classList.contains("m3d") && document.querySelector("#modes3d .btn.on")?.dataset.mode === "walk") ? "interior-walk" : "interior") : external ? "external" : walk ? "walk" : "exterior";
    const y = p ? p.y : 0, x = p ? p.x : 0, z = p ? p.z : 0;
    const floor = /ground-floor\.html$/.test(location.pathname) ? "Ground floor" : /\/ff\//.test(location.pathname) ? "First floor" : floorOf(y);
    const viewBtn = document.querySelector("#cams a, #vname");
    return {
      mode,
      floor,
      place: nearest(x, z),
      view: (document.getElementById("vname") && document.getElementById("vname").textContent) || document.title,
      camera: p ? { x: +x.toFixed(2), y: +y.toFixed(2), z: +z.toFixed(2) } : null,
      target,
      fov: cam && cam.fov ? +cam.fov.toFixed(1) : null,
      url: location.href
    };
  }

  const css = document.createElement("style");
  css.textContent = `
#revTab{position:absolute;z-index:40;left:8px;bottom:18px;border:0;border-radius:999px;padding:8px 12px;background:#1c1916;color:#fff;font:13px/1 Arial,sans-serif;opacity:.92}
#revBox{position:absolute;z-index:50;inset:0;background:rgba(12,14,16,.72);display:none;flex-direction:column}
#revBox.on{display:flex}
#revTools{display:flex;gap:6px;flex-wrap:wrap;padding:8px;align-items:center}
#revTools button,#revTools input,#revTools textarea{font:13px/1.2 Arial,sans-serif}
#revTools button{border:0;border-radius:999px;padding:8px 10px;background:#243028;color:#fff}
#revTools button.on{background:#9a4e28}
#revColors{display:flex;gap:6px;align-items:center}
#revColors button{width:26px;height:26px;padding:0;border-radius:50%;border:2px solid #fff}
#revColors button.on{outline:2px solid #111;outline-offset:2px}
#revStage{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;padding:0 8px}
#revStage canvas{max-width:100%;max-height:100%;background:#111;touch-action:none}
#revNote{margin:8px;border:0;border-radius:10px;padding:8px;min-height:52px}
#revMeta{color:#efe6d6;font:12px/1.3 Arial,sans-serif;padding:0 10px}
@media(max-width:800px){#revTab{bottom:74px}}
`;
  document.head.appendChild(css);

  const tab = document.createElement("button");
  tab.id = "revTab";
  tab.type = "button";
  tab.textContent = "Review feedback";
  const box = document.createElement("div");
  box.id = "revBox";
  box.innerHTML = `
<div id="revTools">
  <button type="button" data-tool="pen" class="on">Pen</button>
  <button type="button" data-tool="line">Line</button>
  <button type="button" data-tool="arrow">Arrow</button>
  <button type="button" data-tool="circle">Circle</button>
  <button type="button" data-tool="label">Label</button>
  <span id="revColors">
    <button type="button" data-color="#e23b2b" class="on" style="background:#e23b2b" aria-label="Red"></button>
    <button type="button" data-color="#f5d90a" style="background:#f5d90a" aria-label="Yellow"></button>
    <button type="button" data-color="#ffffff" style="background:#ffffff" aria-label="White"></button>
    <button type="button" data-color="#111111" style="background:#111111" aria-label="Black"></button>
    <button type="button" data-color="#2f6fed" style="background:#2f6fed" aria-label="Blue"></button>
    <button type="button" data-color="#3c9a4a" style="background:#3c9a4a" aria-label="Green"></button>
  </span>
  <button type="button" id="revUndo">Undo</button>
  <button type="button" id="revClose">Close</button>
  <button type="button" id="revSave" style="background:#9a4e28">Save</button>
</div>
<div id="revMeta"></div>
<div id="revStage"><canvas id="revCanvas"></canvas></div>
<textarea id="revNote" placeholder="What should change here"></textarea>`;
  document.body.appendChild(tab);
  if (document.getElementById("view3d")) {
    tab.style.left = "auto";
    tab.style.right = "10px";
    tab.style.bottom = "auto";
    tab.style.top = "62px";
  }
  document.body.appendChild(box);

  const canvas = box.querySelector("#revCanvas");
  const ctx = canvas.getContext("2d");
  const meta = box.querySelector("#revMeta");
  let tool = "pen", drawing = false, start = null, snap = null;
  const history = [];
  function shotSize() {
    const src = document.querySelector("#view3d canvas") || document.querySelector("canvas");
    const w = Math.min(1280, src ? src.width : innerWidth);
    const h = Math.round(w * (innerHeight / innerWidth));
    return { w, h, src };
  }
  function grab() {
    if (window.__renderer && window.__scene && window.__cam) window.__renderer.render(window.__scene, window.__cam);
    const { w, h, src } = shotSize();
    canvas.width = w; canvas.height = h;
    if (src) ctx.drawImage(src, 0, 0, w, h);
    else { ctx.fillStyle = "#888"; ctx.fillRect(0, 0, w, h); }
    history.length = 0;
    pushHist();
    const c = context();
    meta.textContent = c.mode + " · " + c.floor + " · " + c.place + " · camera " + (c.camera ? c.camera.x + ", " + c.camera.y + ", " + c.camera.z : "unknown");
    box._ctx = c;
  }
  function pushHist() { history.push(ctx.getImageData(0, 0, canvas.width, canvas.height)); if (history.length > 20) history.shift(); }
  function pos(e) {
    const r = canvas.getBoundingClientRect();
    const src = e.touches ? e.touches[0] : e;
    return { x: (src.clientX - r.left) * canvas.width / r.width, y: (src.clientY - r.top) * canvas.height / r.height };
  }
  function arrow(a, b) {
    const ang = Math.atan2(b.y - a.y, b.x - a.x);
    ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(b.x, b.y);
    ctx.lineTo(b.x - 16 * Math.cos(ang - 0.4), b.y - 16 * Math.sin(ang - 0.4));
    ctx.lineTo(b.x - 16 * Math.cos(ang + 0.4), b.y - 16 * Math.sin(ang + 0.4));
    ctx.closePath(); ctx.fill();
  }
  let ink = "#e23b2b";
  function useInk(){ ctx.strokeStyle = ink; ctx.fillStyle = ink; ctx.lineWidth = 4; ctx.lineCap = "round"; }
  useInk();
  function down(e) {
    drawing = true; start = pos(e); snap = ctx.getImageData(0, 0, canvas.width, canvas.height);
    if (tool === "pen") { useInk(); ctx.beginPath(); ctx.moveTo(start.x, start.y); }
    if (tool === "label") {
      const text = (box.querySelector("#revNote").value || "Note").slice(0, 80);
      ctx.font = "bold 22px Arial"; useInk(); ctx.fillText(text, start.x, start.y);
      pushHist(); drawing = false;
    }
    e.preventDefault();
  }
  function move(e) {
    if (!drawing || tool === "label") return;
    const p = pos(e);
    if (tool === "pen") { ctx.lineTo(p.x, p.y); ctx.stroke(); return; }
    ctx.putImageData(snap, 0, 0);
    useInk();
    if (tool === "line") { ctx.beginPath(); ctx.moveTo(start.x, start.y); ctx.lineTo(p.x, p.y); ctx.stroke(); }
    if (tool === "arrow") arrow(start, p);
    if (tool === "circle") {
      const rx = Math.abs(p.x - start.x), ry = Math.abs(p.y - start.y);
      ctx.beginPath(); ctx.ellipse((start.x + p.x) / 2, (start.y + p.y) / 2, Math.max(rx, 2), Math.max(ry, 2), 0, 0, Math.PI * 2); ctx.stroke();
    }
    e.preventDefault();
  }
  function up() {
    if (!drawing) return;
    drawing = false;
    if (tool !== "label") pushHist();
  }
  canvas.addEventListener("pointerdown", down);
  canvas.addEventListener("pointermove", move);
  window.addEventListener("pointerup", up);
  box.querySelectorAll("[data-color]").forEach((b) => b.onclick = () => {
    ink = b.dataset.color;
    useInk();
    box.querySelectorAll("[data-color]").forEach((x) => x.classList.toggle("on", x === b));
  });
  box.querySelectorAll("[data-tool]").forEach((b) => b.onclick = () => {
    tool = b.dataset.tool;
    box.querySelectorAll("[data-tool]").forEach((x) => x.classList.toggle("on", x === b));
  });
  box.querySelector("#revUndo").onclick = () => { if (history.length < 2) return; history.pop(); ctx.putImageData(history[history.length - 1], 0, 0); };
  box.querySelector("#revClose").onclick = () => box.classList.remove("on");
  tab.onclick = () => { box.classList.add("on"); grab(); };
  box.querySelector("#revSave").onclick = async () => {
    const btn = box.querySelector("#revSave");
    btn.textContent = "Saving";
    const payload = {
      note: box.querySelector("#revNote").value.trim(),
      context: box._ctx || context(),
      image: canvas.toDataURL("image/jpeg", 0.72)
    };
    try {
      const res = await fetch("/api/review-feedback", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(payload) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "save failed");
      btn.textContent = "Saved";
      meta.textContent = "Saved " + data.id + " · " + payload.context.floor + " · " + payload.context.place;
    } catch (err) {
      btn.textContent = "Not saved";
      meta.textContent = "Could not save. " + err.message;
    }
    setTimeout(() => { btn.textContent = "Save"; }, 1600);
  };
})();
