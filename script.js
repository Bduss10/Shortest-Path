// ═══════════════════════════════════════════════════════
// DATA: Node — lokasi kampus UNIB
// ═══════════════════════════════════════════════════════
const NODES = {
  n0:  { id:'n0',  name:'Gerbang Utama UNIB',        lat:-3.7591745, lng:102.2666268 },
  n1:  { id:'n1',  name:'Rektorat UNIB',             lat:-3.7592081, lng:102.2723468 },
  n2:  { id:'n2',  name:'Fakultas Ekonomi & Bisnis', lat:-3.7616591, lng:102.2684465 },
  n3:  { id:'n3',  name:'Fakultas Hukum',            lat:-3.7606463, lng:102.2684596 },
  n4:  { id:'n4',  name:'Dekanat FKIP',              lat:-3.7576645, lng:102.2750427 },
  n5:  { id:'n5',  name:'Fakultas Pertanian',        lat:-3.7594384, lng:102.2692367 },
  n6:  { id:'n6',  name:'Fakultas Teknik',           lat:-3.7591222, lng:102.2767678 },
  n7:  { id:'n7',  name:'Fakultas MIPA',             lat:-3.7560456, lng:102.2748258 },
  n8:  { id:'n8',  name:'Perpustakaan Pusat',        lat:-3.7569399, lng:102.2748278 },
  n9:  { id:'n9',  name:'Auditorium UNIB',           lat:-3.7592747, lng:102.2679845 },
  n10: { id:'n10', name:'Asrama PGSD',               lat:-3.7617728, lng:102.2715465 },
  n11: { id:'n11', name:'Masjid Baitul Hikmah UNIB', lat:-3.7590152, lng:102.2759418 },
  n12: { id:'n12', name:'GOR / Lapangan Olahraga',  lat:-3.7607354, lng:102.2677112 },
  n13: { id:'n13', name:'Kantin FISIP',              lat:-3.7591171, lng:102.2740872 },
  n14: { id:'n14', name:'Klinik Pratama UNIB',       lat:-3.7614798, lng:102.2717748 },
  n15: { id:'n15', name:'Fakultas Kedokteran',       lat:-3.7552293, lng:102.2780086 },
  n16: { id:'n16', name:'Gedung Pascasarjana',       lat:-3.7580219, lng:102.2748307 },
  n17: { id:'n17', name:'LPPM UNIB',                 lat:-3.7588563, lng:102.2679222 },
  n18: { id:'n18', name:'UPA TIK UNIB',              lat:-3.7585102, lng:102.2749453 },
  n19: { id:'n19', name:'Gerbang Belakang UNIB',     lat:-3.7630000, lng:102.2695000 },
};

// ═══════════════════════════════════════════════════════
// DATA: Edge (bobot haversine — untuk Dijkstra)
// ═══════════════════════════════════════════════════════
const EDGES = [
  ['n0','n17'],['n0','n9'], ['n0','n3'],
  ['n9','n17'],['n9','n12'],['n9','n5'],
  ['n1','n17'],['n1','n5'], ['n1','n13'],['n1','n18'],
  ['n5','n2'], ['n5','n3'], ['n5','n14'],
  ['n2','n14'],['n2','n10'],
  ['n3','n12'],
  ['n14','n10'],
  ['n13','n18'],['n13','n1'],
  ['n18','n16'],['n18','n8'], ['n18','n11'],['n18','n6'],
  ['n16','n8'], ['n16','n4'],
  ['n8','n4'],  ['n8','n7'],
  ['n4','n7'],  ['n4','n11'],
  ['n7','n15'], ['n7','n11'],
  ['n11','n6'],
  ['n6','n15'],
  ['n19','n2'], ['n19','n12'],
  ['n12','n17'],['n12','n9'],
];

// ═══════════════════════════════════════════════════════
// ALGORITMA: Haversine + buildGraph
// ═══════════════════════════════════════════════════════
function haversine(a, b) {
  const R = 6371000;
  const dLat = (b.lat - a.lat) * Math.PI / 180;
  const dLng = (b.lng - a.lng) * Math.PI / 180;
  const s = Math.sin(dLat/2)**2 + Math.cos(a.lat*Math.PI/180)*Math.cos(b.lat*Math.PI/180)*Math.sin(dLng/2)**2;
  return R * 2 * Math.asin(Math.sqrt(s));
}

function buildGraph() {
  const g = {};
  Object.keys(NODES).forEach(id => g[id] = []);
  EDGES.forEach(([a, b]) => {
    const d = haversine(NODES[a], NODES[b]);
    g[a].push({ node: b, w: d });
    g[b].push({ node: a, w: d });
  });
  return g;
}

// ── Dijkstra standar (untuk routing) ──
function dijkstra(graph, start, end) {
  const dist = {}, prev = {};
  const visited = new Set();
  Object.keys(graph).forEach(n => { dist[n] = Infinity; prev[n] = null; });
  dist[start] = 0;
  const q = [...Object.keys(graph)];
  while (q.length) {
    q.sort((a, b) => dist[a] - dist[b]);
    const u = q.shift();
    if (u === end) break;
    if (dist[u] === Infinity) break;
    visited.add(u);
    graph[u].forEach(({ node: v, w }) => {
      if (visited.has(v)) return;
      const alt = dist[u] + w;
      if (alt < dist[v]) { dist[v] = alt; prev[v] = u; }
    });
  }
  const path = []; let cur = end;
  while (cur !== null) { path.unshift(cur); cur = prev[cur]; }
  if (path[0] !== start) return null;
  return { path, distance: dist[end] };
}

// ── Dijkstra + rekam langkah (untuk animasi) ──
function dijkstraWithSteps(graph, start, end) {
  const dist = {}, prev = {};
  const visited = new Set();
  const steps = [];
  Object.keys(graph).forEach(n => { dist[n] = Infinity; prev[n] = null; });
  dist[start] = 0;
  const q = [...Object.keys(graph)];
  while (q.length) {
    q.sort((a, b) => dist[a] - dist[b]);
    const u = q.shift();
    if (dist[u] === Infinity) break;
    visited.add(u);
    const updated = [];
    graph[u].forEach(({ node: v, w }) => {
      if (visited.has(v)) return;
      const alt = dist[u] + w;
      if (alt < dist[v]) { dist[v] = alt; prev[v] = u; updated.push(v); }
    });
    steps.push({ current: u, visited: [...visited], updated });
    if (u === end) break;
  }
  const path = []; let cur = end;
  while (cur !== null) { path.unshift(cur); cur = prev[cur]; }
  if (path[0] !== start) return null;
  return { path, distance: dist[end], steps };
}

const graph = buildGraph();

// ═══════════════════════════════════════════════════════
// TRANSPORT MODE
// ═══════════════════════════════════════════════════════
let transportMode = 'foot';
const TRANSPORT_ICONS  = { foot: '🚶' };
const TRANSPORT_LABELS = { foot: 'Jalan Kaki' };
const SPEED_LABELS     = ['', 'Lambat', 'Pelan', 'Sedang', 'Cepat', 'Kilat'];
const ANIM_DELAYS      = [900, 550, 300, 140, 60];

// Kecepatan rata-rata jalan kaki (meter/detik)
const TRANSPORT_SPEED_MS = {
  foot: 5 / 3.6,   // ±5 km/jam (jalan kaki)
};

function setTransport(mode) {
  transportMode = 'foot'; // Hanya jalan kaki
  document.getElementById('t-foot').className = 'btn-transport active-transport';
}

// ═══════════════════════════════════════════════════════
// PETA: Inisialisasi Leaflet
// ═══════════════════════════════════════════════════════
const map = L.map('map', { center: [-3.7590, 102.2720], zoom: 16 });
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 19,
}).addTo(map);

function makeIcon(color, size = 12) {
  return L.divIcon({
    className: '',
    html: `<div style="background:${color};width:${size}px;height:${size}px;border-radius:50%;border:2px solid rgba(255,255,255,0.85);box-shadow:0 0 6px rgba(0,0,0,0.6);transition:background 0.25s,width 0.2s,height 0.2s;"></div>`,
    iconSize: [size, size], iconAnchor: [size/2, size/2],
  });
}

// Buat marker semua node kampus
const nodeMarkers = {};
Object.values(NODES).forEach(n => {
  const m = L.marker([n.lat, n.lng], { icon: makeIcon('#38bdf8') })
    .addTo(map)
    .bindTooltip(n.name, { permanent: false, direction: 'top', className: 'map-tip' })
    .on('click', () => handlePointSelect(n.lat, n.lng, n.name, n.id));
  nodeMarkers[n.id] = m;
});

// ═══════════════════════════════════════════════════════
// DROPDOWN: Isi pilihan preset
// ═══════════════════════════════════════════════════════
const selStart = document.getElementById('sel-start');
const selEnd   = document.getElementById('sel-end');
Object.values(NODES).forEach(n => {
  [selStart, selEnd].forEach(sel => {
    const opt = document.createElement('option');
    opt.value = n.id; opt.textContent = n.name; sel.appendChild(opt);
  });
});

selStart.addEventListener('change', () => {
  const id = selStart.value; if (!id) return;
  setPoint('start', NODES[id].lat, NODES[id].lng, NODES[id].name, id);
});
selEnd.addEventListener('change', () => {
  const id = selEnd.value; if (!id) return;
  setPoint('end', NODES[id].lat, NODES[id].lng, NODES[id].name, id);
});

// ═══════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════
let clickMode   = null;       // 'start' | 'end' | 'waypoint' | null
let startPt     = null;       // { lat, lng, name, nodeId }
let endPt       = null;
let waypoints   = [];         // [{ lat, lng, name, nodeId }, ...]
let routeLayers = [];
let pinStart    = null;
let pinEnd      = null;
let waypointPins = [];

// ═══════════════════════════════════════════════════════
// CLICK MODE
// ═══════════════════════════════════════════════════════
function setClickMode(mode) {
  clickMode = mode;
  const hint  = document.getElementById('map-hint');
  const mapEl = document.getElementById('map');
  const btnS  = document.getElementById('btn-mode-start');
  const btnE  = document.getElementById('btn-mode-end');
  const btnWP = document.getElementById('btn-add-wp');

  btnS.className  = 'btn-mode'  + (mode === 'start'    ? ' active-start' : '');
  btnE.className  = 'btn-mode'  + (mode === 'end'      ? ' active-end'   : '');
  btnWP.className = 'btn-add-wp'+ (mode === 'waypoint' ? ' active-wp'    : '');

  const modeClass = { start:'mode-start', end:'mode-end', waypoint:'mode-waypoint' };
  mapEl.className = modeClass[mode] || '';

  const hints = {
    start:    '📍 Klik di peta untuk menentukan TITIK ASAL',
    end:      '📍 Klik di peta untuk menentukan TITIK TUJUAN',
    waypoint: '📍 Klik di peta atau node untuk menambah TITIK SINGGAH',
  };
  hint.textContent = hints[mode] || '';
  hint.className   = 'show';
}

function clearClickMode() {
  clickMode = null;
  document.getElementById('map-hint').className       = '';
  document.getElementById('map').className            = '';
  document.getElementById('btn-mode-start').className = 'btn-mode';
  document.getElementById('btn-mode-end').className   = 'btn-mode';
  document.getElementById('btn-add-wp').className     = 'btn-add-wp';
}

map.on('click', e => {
  if (!clickMode) return;
  const { lat, lng } = e.latlng;
  handlePointSelect(lat, lng, `Titik kustom (${lat.toFixed(5)}, ${lng.toFixed(5)})`, null);
});

function handlePointSelect(lat, lng, name, nodeId) {
  if (!clickMode) return;
  if (clickMode === 'waypoint') {
    addWaypoint(lat, lng, name, nodeId);
  } else {
    setPoint(clickMode, lat, lng, name, nodeId);
  }
  clearClickMode();
}

// ═══════════════════════════════════════════════════════
// MANAJEMEN TITIK
// ═══════════════════════════════════════════════════════
function setPoint(which, lat, lng, name, nodeId) {
  if (which === 'start') {
    // Reset warna node lama
    if (startPt?.nodeId && nodeMarkers[startPt.nodeId]) {
      nodeMarkers[startPt.nodeId].setIcon(makeIcon('#38bdf8', 12));
    }
    startPt = { lat, lng, name, nodeId };
    const d = document.getElementById('disp-start');
    d.className = 'point-display set-start';
    document.getElementById('disp-start-name').textContent = name;
    document.getElementById('disp-start-name').style.color = '#22c55e';
    if (nodeId) selStart.value = nodeId; else selStart.value = '';
    if (pinStart) map.removeLayer(pinStart);
    pinStart = L.marker([lat, lng], { icon: makeIcon('#22c55e', 14), zIndexOffset: 900 })
      .addTo(map)
      .bindTooltip('▶ ' + name, { permanent: false, direction: 'top', className: 'map-tip' });
    if (nodeId && nodeMarkers[nodeId]) nodeMarkers[nodeId].setIcon(makeIcon('#22c55e', 14));
  } else {
    // Reset warna node lama
    if (endPt?.nodeId && nodeMarkers[endPt.nodeId]) {
      nodeMarkers[endPt.nodeId].setIcon(makeIcon('#38bdf8', 12));
    }
    endPt = { lat, lng, name, nodeId };
    const d = document.getElementById('disp-end');
    d.className = 'point-display set-end';
    document.getElementById('disp-end-name').textContent = name;
    document.getElementById('disp-end-name').style.color = '#ef4444';
    if (nodeId) selEnd.value = nodeId; else selEnd.value = '';
    if (pinEnd) map.removeLayer(pinEnd);
    pinEnd = L.marker([lat, lng], { icon: makeIcon('#ef4444', 14), zIndexOffset: 900 })
      .addTo(map)
      .bindTooltip('■ ' + name, { permanent: false, direction: 'top', className: 'map-tip' });
    if (nodeId && nodeMarkers[nodeId]) nodeMarkers[nodeId].setIcon(makeIcon('#ef4444', 14));
  }
  updateAnimBtn();
}

// ─── Waypoints ───
function startAddWaypoint() {
  setClickMode('waypoint');
}

function addWaypoint(lat, lng, name, nodeId) {
  waypoints.push({ lat, lng, name, nodeId });
  const pin = L.marker([lat, lng], { icon: makeIcon('#a855f7', 12), zIndexOffset: 800 })
    .addTo(map)
    .bindTooltip('◆ ' + name, { permanent: false, direction: 'top', className: 'map-tip' });
  waypointPins.push(pin);
  renderWaypointList();
}

function removeWaypoint(idx) {
  waypoints.splice(idx, 1);
  if (waypointPins[idx]) { map.removeLayer(waypointPins[idx]); }
  waypointPins.splice(idx, 1);
  renderWaypointList();
}

function renderWaypointList() {
  const list = document.getElementById('waypoint-list');
  if (!waypoints.length) { list.innerHTML = ''; return; }
  list.innerHTML = waypoints.map((wp, i) => `
    <div class="wp-item">
      <div class="wp-dot"></div>
      <span class="wp-name" title="${wp.name}">${wp.name}</span>
      <button class="wp-remove" onclick="removeWaypoint(${i})" title="Hapus singgahan">×</button>
    </div>`).join('');
}

// ═══════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════
function fmtDist(m) { return m >= 1000 ? (m/1000).toFixed(2)+' km' : Math.round(m)+' m'; }
function fmtDur(s) {
  const h = Math.floor(s/3600);
  const m = Math.floor((s%3600)/60);
  const sec = Math.round(s%60);
  if (h > 0) return `${h} jam ${m} mnt`;
  return m > 0 ? `${m} mnt ${sec} dtk` : `${sec} dtk`;
}
function fmtTimestamp(ts) {
  const d = new Date(ts);
  return d.toLocaleDateString('id-ID', {day:'numeric', month:'short'}) + ' ' +
         d.toLocaleTimeString('id-ID', {hour:'2-digit', minute:'2-digit'});
}
function clearRoute() {
  routeLayers.forEach(l => map.removeLayer(l));
  routeLayers = [];
}

// ═══════════════════════════════════════════════════════
// RIWAYAT PENCARIAN (localStorage)
// ═══════════════════════════════════════════════════════
const HIST_KEY = 'unib_route_history_v2';

function saveHistory(entry) {
  let hist = JSON.parse(localStorage.getItem(HIST_KEY) || '[]');
  hist.unshift(entry);
  hist = hist.slice(0, 5);
  localStorage.setItem(HIST_KEY, JSON.stringify(hist));
  renderHistory();
}

function renderHistory() {
  const hist = JSON.parse(localStorage.getItem(HIST_KEY) || '[]');
  const list = document.getElementById('history-list');
  if (!hist.length) {
    list.innerHTML = '<div class="hist-empty">Belum ada riwayat pencarian</div>';
    return;
  }
  list.innerHTML = hist.map((h, i) => {
    const wpLabel = h.waypoints?.length
      ? `<span class="wp-badge"> [${h.waypoints.length}×singgah]</span>` : '';
    return `
      <div class="history-item" onclick="restoreFromHistory(${i})">
        <button class="hist-delete" onclick="deleteHistory(event,${i})" title="Hapus">✕</button>
        <div class="hist-route">
          ${TRANSPORT_ICONS[h.transport]||'🚗'}
          <strong>${h.startName}</strong>${wpLabel} → <strong>${h.endName}</strong>
        </div>
        <div class="hist-meta">
          <span class="hist-dist">${fmtDist(h.distance)}</span>·
          <span>~${fmtDur(h.duration)}</span>·
          <span class="hist-transport">${TRANSPORT_LABELS[h.transport]||'Kendaraan'}</span>·
          <span class="hist-time">${fmtTimestamp(h.timestamp)}</span>
        </div>
      </div>`;
  }).join('');
}

function deleteHistory(e, idx) {
  e.stopPropagation();
  let hist = JSON.parse(localStorage.getItem(HIST_KEY) || '[]');
  hist.splice(idx, 1);
  localStorage.setItem(HIST_KEY, JSON.stringify(hist));
  renderHistory();
}

function restoreFromHistory(idx) {
  const hist = JSON.parse(localStorage.getItem(HIST_KEY) || '[]');
  const h = hist[idx];
  if (!h) return;

  // Reset bersih dulu
  resetAll(true); // true = jangan clear history

  setTransport('foot');

  if (h.startLat != null) setPoint('start', h.startLat, h.startLng, h.startName, h.startId || null);
  (h.waypoints || []).forEach(wp => addWaypoint(wp.lat, wp.lng, wp.name, wp.nodeId || null));
  if (h.endLat != null) setPoint('end', h.endLat, h.endLng, h.endName, h.endId || null);

  // Auto-cari rute
  setTimeout(() => document.getElementById('btn-find').click(), 150);
}

// ═══════════════════════════════════════════════════════
// OSRM — Routing multi-titik
// ═══════════════════════════════════════════════════════
// Catatan: Menggunakan profil 'foot' untuk rute jalan kaki.
async function fetchOSRM(points) {
  const coords = points.map(p => `${p.lng},${p.lat}`).join(';');
  // Gunakan profil 'foot' untuk jalur pejalan kaki
  const url = `https://router.project-osrm.org/route/v1/foot/${coords}?overview=full&geometries=geojson&steps=false`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  const data = await resp.json();
  if (data.code !== 'Ok' || !data.routes?.length) throw new Error('OSRM: no route');

  const route = data.routes[0];

  // Hitung ulang durasi berdasarkan moda transportasi yang dipilih
  const speedMs = TRANSPORT_SPEED_MS[transportMode] ?? TRANSPORT_SPEED_MS.driving;
  route.duration = route.distance / speedMs;  // detik

  return route;
}

// ═══════════════════════════════════════════════════════
// DIJKSTRA ANIMATION
// ═══════════════════════════════════════════════════════
let animTimeout = null;
let animRunning = false;

function updateAnimBtn() {
  const btn = document.getElementById('btn-animate');
  const canAnimate = startPt?.nodeId && endPt?.nodeId && startPt.nodeId !== endPt.nodeId;
  btn.disabled = !canAnimate;
  if (!canAnimate && !animRunning) {
    const el = document.getElementById('anim-status');
    el.textContent = 'Pilih dua titik preset berbeda untuk animasi Dijkstra';
    el.className = 'anim-status';
  }
}

function runDijkstraAnimation() {
  if (animRunning) { stopAnimation(); return; }
  const sId = startPt?.nodeId, eId = endPt?.nodeId;
  if (!sId || !eId || sId === eId) return;

  // Stop route & reset warna
  clearRoute();
  resetNodeColors();

  const result = dijkstraWithSteps(graph, sId, eId);
  if (!result) {
    showAnimStatus('Tidak ada jalur yang ditemukan antara dua titik ini.', false);
    return;
  }

  const { steps, path } = result;
  animRunning = true;
  document.getElementById('btn-animate').style.display = 'none';
  document.getElementById('btn-stop-anim').style.display = '';
  showAnimStatus(`Memulai animasi: "${NODES[sId].name}" → "${NODES[eId].name}"`, true);

  let stepIdx = 0;

  function playStep() {
    if (!animRunning) return;

    if (stepIdx >= steps.length) {
      // Selesai — tampilkan jalur optimal
      resetNodeColors();
      path.forEach(id => nodeMarkers[id]?.setIcon(makeIcon('#22c55e', 13)));
      if (nodeMarkers[sId]) nodeMarkers[sId].setIcon(makeIcon('#22c55e', 16));
      if (nodeMarkers[eId]) nodeMarkers[eId].setIcon(makeIcon('#ef4444', 16));

      showAnimStatus(
        `✓ Selesai! Dijkstra menjelajahi ${steps.length} node — jalur optimal: ${path.length} node.`,
        false
      );
      animRunning = false;
      document.getElementById('btn-animate').style.display = '';
      document.getElementById('btn-stop-anim').style.display = 'none';
      return;
    }

    const step = steps[stepIdx];

    // Abu: node yang sudah selesai diproses
    step.visited.forEach(id => {
      nodeMarkers[id]?.setIcon(makeIcon('#475569', 10));
    });

    // Ungu: node yang sedang diproses (current)
    nodeMarkers[step.current]?.setIcon(makeIcon('#a855f7', 15));

    // Amber: tetangga yang baru saja diperbarui jaraknya
    step.updated.forEach(id => {
      nodeMarkers[id]?.setIcon(makeIcon('#f59e0b', 12));
    });

    // Jaga agar start/end tetap terlihat
    if (step.current !== sId) nodeMarkers[sId]?.setIcon(makeIcon('#22c55e', 12));
    if (step.current !== eId) nodeMarkers[eId]?.setIcon(makeIcon('#ef4444', 12));

    const pct = Math.round((stepIdx + 1) / steps.length * 100);
    showAnimStatus(
      `Langkah ${stepIdx + 1}/${steps.length} (${pct}%) — Memproses: "${NODES[step.current].name}"`,
      true
    );

    stepIdx++;
    const speed = parseInt(document.getElementById('anim-speed').value);
    animTimeout = setTimeout(playStep, ANIM_DELAYS[speed - 1]);
  }

  setTimeout(playStep, 300);
}

function stopAnimation() {
  animRunning = false;
  if (animTimeout) { clearTimeout(animTimeout); animTimeout = null; }
  resetNodeColors();
  document.getElementById('btn-animate').style.display = '';
  document.getElementById('btn-stop-anim').style.display = 'none';
  showAnimStatus('Animasi dihentikan. Tekan ▶ Animasi untuk memulai lagi.', false);
}

function resetNodeColors() {
  Object.keys(NODES).forEach(id => nodeMarkers[id]?.setIcon(makeIcon('#38bdf8', 12)));
  if (startPt?.nodeId) nodeMarkers[startPt.nodeId]?.setIcon(makeIcon('#22c55e', 14));
  if (endPt?.nodeId)   nodeMarkers[endPt.nodeId]?.setIcon(makeIcon('#ef4444', 14));
}

function showAnimStatus(msg, running) {
  const el = document.getElementById('anim-status');
  el.textContent = msg;
  el.className = 'anim-status' + (running ? ' running' : '');
}

// Speed slider — update label
document.getElementById('anim-speed').addEventListener('input', function () {
  document.getElementById('speed-val').textContent = SPEED_LABELS[this.value];
});

// ═══════════════════════════════════════════════════════
// CARI RUTE — Event Handler Utama
// ═══════════════════════════════════════════════════════
document.getElementById('btn-find').addEventListener('click', async () => {
  const box = document.getElementById('result-box');
  const btn = document.getElementById('btn-find');

  // Resolve dari dropdown jika belum diklik di peta
  if (!startPt && selStart.value) {
    const n = NODES[selStart.value];
    startPt = { lat: n.lat, lng: n.lng, name: n.name, nodeId: selStart.value };
  }
  if (!endPt && selEnd.value) {
    const n = NODES[selEnd.value];
    endPt = { lat: n.lat, lng: n.lng, name: n.name, nodeId: selEnd.value };
  }

  if (!startPt || !endPt) {
    box.className = 'has-error';
    box.innerHTML = `<div class="result-error">
      <div class="result-error-icon">⚠</div>
      <div>Pilih titik asal dan tujuan terlebih dahulu!</div>
    </div>`;
    return;
  }
  if (startPt.lat === endPt.lat && startPt.lng === endPt.lng) {
    box.className = 'has-error';
    box.innerHTML = `<div class="result-error">
      <div class="result-error-icon">⚡</div>
      <div>Titik asal dan tujuan tidak boleh sama.</div>
    </div>`;
    return;
  }

  // Stop animasi jika berjalan
  if (animRunning) stopAnimation();
  clearRoute();

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Menghitung rute…';
  box.className = 'is-loading';
  box.innerHTML = `<div class="result-loading">
    <span class="spinner" style="width:18px;height:18px;margin:0 0 10px"></span>
    <div style="color:var(--cyan);font-weight:600;font-size:12px">Routing ${TRANSPORT_ICONS[transportMode]} ${TRANSPORT_LABELS[transportMode]}…</div>
    <div style="color:var(--text-muted);font-size:11px;margin-top:4px">Menghitung rute jalan kaki...</div>
  </div>`;

  // ── Dijkstra — chain melalui waypoints (hanya preset node) ──
  let dijkstraInfo = '';
  const presetChain = [startPt, ...waypoints, endPt]
    .filter(p => p.nodeId)
    .map(p => p.nodeId)
    .filter((id, i, arr) => i === 0 || id !== arr[i - 1]);

  if (presetChain.length >= 2) {
    let fullPath = [presetChain[0]];
    let valid = true;
    for (let i = 0; i < presetChain.length - 1; i++) {
      const dr = dijkstra(graph, presetChain[i], presetChain[i + 1]);
      if (!dr) { valid = false; break; }
      fullPath = [...fullPath, ...dr.path.slice(1)];
    }
    if (valid && fullPath.length > 1) {
      const segLabel = presetChain.length > 2
        ? ` · ${presetChain.length - 1} segmen` : '';
      dijkstraInfo = `
        <div class="dijkstra-section">
          <div class="dijkstra-header">
            <span class="dijkstra-title">Jalur Dijkstra</span>
            <span class="dijkstra-badge">${fullPath.length} node${segLabel}</span>
          </div>
          <ul class="path-list">
            ${fullPath.map((id, i) => {
              const isFirst = i === 0, isLast = i === fullPath.length - 1;
              const dotClass = isFirst ? 'step-dot s' : isLast ? 'step-dot e' : 'step-dot';
              const conn = isLast ? '' : '<div class="step-connector"></div>';
              return `<li class="path-item">
                <div class="step-wrap"><div class="${dotClass}"></div>${conn}</div>
                <span>${NODES[id].name}</span>
              </li>`;
            }).join('')}
          </ul>
        </div>`;
    }
  }

  try {
    const allPoints = [startPt, ...waypoints, endPt];
    const route = await fetchOSRM(allPoints);
    const { distance: dist, duration: dur, geometry: geom } = route;

    // Gambar rute di peta
    const glow = L.geoJSON(geom, {
      style: { color: '#7dd3fc', weight: 12, opacity: 0.15, lineJoin: 'round', lineCap: 'round' }
    }).addTo(map);
    const line = L.geoJSON(geom, {
      style: { color: '#38bdf8', weight: 5,  opacity: 0.95, lineJoin: 'round', lineCap: 'round' }
    }).addTo(map);
    routeLayers.push(glow, line);
    map.fitBounds(line.getBounds(), { padding: [50, 50] });

    // Buat daftar titik path
    const allPts = [startPt, ...waypoints, endPt];
    const pathItems = allPts.map((pt, i) => {
      const isFirst = i === 0, isLast = i === allPts.length - 1;
      const dotClass = isFirst ? 'step-dot s' : isLast ? 'step-dot e' : 'step-dot';
      const dotStyle = (!isFirst && !isLast) ? 'style="background:var(--purple)"' : '';
      const conn = isLast ? '' : '<div class="step-connector"></div>';
      return `<li class="path-item">
        <div class="step-wrap"><div class="${dotClass}" ${dotStyle}></div>${conn}</div>
        <span>${pt.name}</span>
      </li>`;
    }).join('');

    const wpBadge = waypoints.length
      ? `<span class="result-wp-badge">${waypoints.length}× singgah</span>` : '';

    box.className = 'has-result';
    box.innerHTML = `
      <div style="width:100%">
        <div class="result-stats">
          <div class="stat-card">
            <div class="stat-label">Jarak</div>
            <div class="stat-value" style="color:var(--cyan)">${fmtDist(dist)}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Estimasi Waktu</div>
            <div class="stat-value" style="color:var(--text-primary)">${fmtDur(dur)}</div>
          </div>
        </div>
        <div class="result-meta-row">
          <span class="result-mode-badge">${TRANSPORT_ICONS[transportMode]} ${TRANSPORT_LABELS[transportMode]}</span>
          ${wpBadge}
          <span class="result-osrm-badge">✓ OSRM</span>
        </div>
        <div class="route-path-section">
          <div class="route-path-title">Rute</div>
          <ul class="path-list">${pathItems}</ul>
        </div>
        ${dijkstraInfo}
      </div>`;

    // Simpan ke riwayat
    saveHistory({
      transport: transportMode,
      startName: startPt.name, startId: startPt.nodeId, startLat: startPt.lat, startLng: startPt.lng,
      endName:   endPt.name,   endId:   endPt.nodeId,   endLat:   endPt.lat,   endLng:   endPt.lng,
      waypoints: waypoints.map(wp => ({ name: wp.name, nodeId: wp.nodeId, lat: wp.lat, lng: wp.lng })),
      distance: dist, duration: dur, timestamp: Date.now(),
    });

  } catch (err) {
    console.warn('OSRM error:', err);
    // Fallback: garis lurus
    const allPts = [startPt, ...waypoints, endPt];
    const latlngs = allPts.map(p => [p.lat, p.lng]);
    const fb = L.polyline(latlngs, { color:'var(--amber)', weight:4, opacity:0.85, dashArray:'8 6' }).addTo(map);
    routeLayers.push(fb);
    map.fitBounds(fb.getBounds(), { padding: [50, 50] });
    const straightDist = haversine(startPt, endPt);
    box.className = 'has-result';
    box.innerHTML = `<div style="width:100%">
      <div class="result-stats">
        <div class="stat-card" style="border-color:rgba(245,158,11,0.2);background:rgba(245,158,11,0.05)">
          <div class="stat-label">Jarak Lurus</div>
          <div class="stat-value" style="color:var(--amber)">${fmtDist(straightDist)}</div>
        </div>
      </div>
      <div class="result-meta-row">
        <span style="color:var(--amber);font-size:11px;font-weight:600">⚠ OSRM tidak tersedia — jarak lurus ditampilkan</span>
      </div>
    </div>`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = '🔍 Cari Rute Jalan Kaki';
  }
});

// ═══════════════════════════════════════════════════════
// RESET
// ═══════════════════════════════════════════════════════
function resetAll(keepHistory = false) {
  selStart.value = ''; selEnd.value = '';
  startPt = null; endPt = null;

  // Hapus waypoints
  waypointPins.forEach(p => map.removeLayer(p));
  waypoints = []; waypointPins = [];
  renderWaypointList();

  clearRoute();
  clearClickMode();

  if (pinStart) { map.removeLayer(pinStart); pinStart = null; }
  if (pinEnd)   { map.removeLayer(pinEnd);   pinEnd   = null; }

  ['disp-start', 'disp-end'].forEach(id => {
    document.getElementById(id).className = 'point-display';
  });
  document.getElementById('disp-start-name').textContent = 'Belum dipilih';
  document.getElementById('disp-start-name').style.color = '#3b4e63';
  document.getElementById('disp-end-name').textContent   = 'Belum dipilih';
  document.getElementById('disp-end-name').style.color   = '#3b4e63';

  if (animRunning) stopAnimation();
  resetNodeColors();

  const box = document.getElementById('result-box');
  box.className = '';
  box.innerHTML = '<span>Klik peta atau pilih dropdown,<br>lalu klik "Cari Rute Terpendek"</span>';

  updateAnimBtn();
}

document.getElementById('btn-reset').addEventListener('click', () => resetAll(false));

// ═══════════════════════════════════════════════════════
// INISIALISASI
// ═══════════════════════════════════════════════════════
setTransport('foot');
renderHistory();
updateAnimBtn();
document.getElementById('speed-val').textContent = SPEED_LABELS[3]; // "Sedang"
