"""
====================================================
  BFS SHORTEST PATH - Kecerdasan Buatan
  Algoritma: Breadth-First Search (BFS)
  Peta: Kota-Kota Nyata di Pulau Jawa
====================================================

Pulau Jawa mencakup 6 provinsi:
  - Banten
  - DKI Jakarta
  - Jawa Barat
  - Jawa Tengah
  - DI Yogyakarta
  - Jawa Timur

Koordinat menggunakan longitude (BT) & latitude (LS)
yang dikonversi ke sistem koordinat plot.
"""

from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np


# ============================================================
# PETA KOTA NYATA PULAU JAWA
# Format: "Nama Kota": (Longitude BT, Latitude LS)
# ============================================================
KOORDINAT_KOTA = {
    # ── BANTEN ──────────────────────────────────────────────
    "Merak":         (105.98, -5.93),
    "Cilegon":       (106.00, -6.00),
    "Serang":        (106.15, -6.12),
    "Pandeglang":    (106.10, -6.30),
    "Rangkasbitung": (106.25, -6.35),

    # ── DKI JAKARTA ─────────────────────────────────────────
    "Jakarta":       (106.82, -6.20),

    # ── JAWA BARAT ──────────────────────────────────────────
    "Bekasi":        (106.99, -6.24),
    "Depok":         (106.82, -6.40),
    "Bogor":         (106.80, -6.60),
    "Sukabumi":      (106.93, -6.92),
    "Karawang":      (107.30, -6.31),
    "Purwakarta":    (107.44, -6.56),
    "Subang":        (107.76, -6.57),
    "Bandung":       (107.61, -6.91),
    "Sumedang":      (107.92, -6.85),
    "Cirebon":       (108.56, -6.73),
    "Garut":         (107.90, -7.22),
    "Tasikmalaya":   (108.22, -7.33),
    "Ciamis":        (108.35, -7.33),
    "Banjar":        (108.54, -7.37),

    # ── JAWA TENGAH ─────────────────────────────────────────
    "Brebes":        (109.00, -6.87),
    "Tegal":         (109.12, -6.87),
    "Pemalang":      (109.38, -6.90),
    "Pekalongan":    (109.67, -6.89),
    "Batang":        (109.73, -6.91),
    "Kendal":        (110.20, -6.92),
    "Semarang":      (110.42, -6.97),
    "Demak":         (110.63, -6.89),
    "Kudus":         (110.84, -6.80),
    "Jepara":        (110.67, -6.59),
    "Pati":          (111.04, -6.75),
    "Rembang":       (111.34, -6.71),
    "Blora":         (111.41, -6.96),
    "Grobogan":      (110.89, -7.01),
    "Purwokerto":    (109.24, -7.43),
    "Cilacap":       (108.99, -7.73),
    "Kebumen":       (109.65, -7.67),
    "Banjarnegara":  (109.69, -7.38),
    "Wonosobo":      (109.90, -7.36),
    "Temanggung":    (110.17, -7.32),
    "Magelang":      (110.22, -7.47),
    "Purworejo":     (110.02, -7.71),
    "Boyolali":      (110.60, -7.53),
    "Salatiga":      (110.50, -7.33),
    "Solo":          (110.83, -7.57),
    "Klaten":        (110.61, -7.71),
    "Sukoharjo":     (110.84, -7.68),
    "Wonogiri":      (110.92, -7.81),
    "Sragen":        (110.99, -7.43),

    # ── DI YOGYAKARTA ───────────────────────────────────────
    "Yogyakarta":    (110.37, -7.80),
    "Sleman":        (110.35, -7.72),
    "Bantul":        (110.33, -7.89),
    "Wates":         (110.16, -7.87),
    "Wonosari":      (110.60, -7.98),

    # ── JAWA TIMUR ──────────────────────────────────────────
    "Tuban":         (111.91, -6.90),
    "Bojonegoro":    (111.88, -7.15),
    "Lamongan":      (112.42, -7.12),
    "Gresik":        (112.65, -7.15),
    "Surabaya":      (112.75, -7.25),
    "Sidoarjo":      (112.71, -7.45),
    "Mojokerto":     (112.43, -7.47),
    "Jombang":       (112.24, -7.55),
    "Ngawi":         (111.44, -7.40),
    "Madiun":        (111.52, -7.63),
    "Nganjuk":       (111.89, -7.60),
    "Kediri":        (112.01, -7.82),
    "Blitar":        (112.17, -8.10),
    "Tulungagung":   (111.90, -8.06),
    "Trenggalek":    (111.71, -8.05),
    "Ponorogo":      (111.46, -7.87),
    "Pacitan":       (111.10, -8.20),
    "Malang":        (112.63, -7.98),
    "Pasuruan":      (112.91, -7.64),
    "Probolinggo":   (113.22, -7.75),
    "Lumajang":      (113.22, -8.13),
    "Jember":        (113.70, -8.17),
    "Bondowoso":     (113.82, -7.91),
    "Situbondo":     (114.01, -7.71),
    "Banyuwangi":    (114.37, -8.22),
}


# ============================================================
# KONEKSI JALAN ANTAR KOTA
# Berdasarkan jalur nyata: Pantura, Jalur Selatan, Trans-Jawa
# ============================================================
KONEKSI = {
    # ── BANTEN ──────────────────────────────────────────────
    "Merak":         ["Cilegon", "Serang"],
    "Cilegon":       ["Merak", "Serang"],
    "Serang":        ["Merak", "Cilegon", "Pandeglang", "Rangkasbitung", "Jakarta"],
    "Pandeglang":    ["Serang", "Rangkasbitung"],
    "Rangkasbitung": ["Serang", "Pandeglang", "Bogor"],

    # ── DKI JAKARTA ─────────────────────────────────────────
    "Jakarta":       ["Serang", "Bekasi", "Depok", "Bogor", "Karawang"],

    # ── JAWA BARAT ──────────────────────────────────────────
    "Bekasi":        ["Jakarta", "Karawang", "Depok"],
    "Depok":         ["Jakarta", "Bekasi", "Bogor"],
    "Bogor":         ["Jakarta", "Depok", "Sukabumi", "Bandung", "Rangkasbitung"],
    "Sukabumi":      ["Bogor", "Bandung", "Ciamis"],
    "Karawang":      ["Jakarta", "Bekasi", "Purwakarta", "Subang"],
    "Purwakarta":    ["Karawang", "Subang", "Bandung"],
    "Subang":        ["Karawang", "Purwakarta", "Cirebon", "Sumedang"],
    "Bandung":       ["Bogor", "Purwakarta", "Sumedang", "Garut", "Tasikmalaya"],
    "Sumedang":      ["Bandung", "Subang", "Cirebon", "Garut"],
    "Cirebon":       ["Subang", "Sumedang", "Brebes", "Banjar"],
    "Garut":         ["Bandung", "Sumedang", "Tasikmalaya"],
    "Tasikmalaya":   ["Bandung", "Garut", "Ciamis"],
    "Ciamis":        ["Tasikmalaya", "Sukabumi", "Banjar"],
    "Banjar":        ["Ciamis", "Cirebon", "Cilacap"],

    # ── JAWA TENGAH ─────────────────────────────────────────
    "Brebes":        ["Cirebon", "Tegal", "Purwokerto"],
    "Tegal":         ["Brebes", "Pemalang", "Purwokerto"],
    "Pemalang":      ["Tegal", "Pekalongan"],
    "Pekalongan":    ["Pemalang", "Batang"],
    "Batang":        ["Pekalongan", "Kendal"],
    "Kendal":        ["Batang", "Semarang", "Temanggung"],
    "Semarang":      ["Kendal", "Demak", "Salatiga", "Grobogan", "Magelang", "Boyolali"],
    "Demak":         ["Semarang", "Kudus", "Grobogan"],
    "Kudus":         ["Demak", "Jepara", "Pati"],
    "Jepara":        ["Kudus"],
    "Pati":          ["Kudus", "Rembang", "Grobogan"],
    "Rembang":       ["Pati", "Blora", "Tuban"],
    "Blora":         ["Rembang", "Grobogan", "Bojonegoro"],
    "Grobogan":      ["Semarang", "Demak", "Pati", "Blora", "Solo"],
    "Purwokerto":    ["Brebes", "Tegal", "Banjarnegara", "Cilacap", "Kebumen"],
    "Cilacap":       ["Banjar", "Purwokerto", "Kebumen"],
    "Kebumen":       ["Cilacap", "Purwokerto", "Purworejo", "Banjarnegara"],
    "Banjarnegara":  ["Purwokerto", "Kebumen", "Wonosobo"],
    "Wonosobo":      ["Banjarnegara", "Temanggung", "Magelang"],
    "Temanggung":    ["Kendal", "Wonosobo", "Magelang", "Semarang"],
    "Magelang":      ["Temanggung", "Wonosobo", "Sleman", "Boyolali", "Purworejo"],
    "Purworejo":     ["Kebumen", "Magelang", "Wates"],
    "Boyolali":      ["Magelang", "Semarang", "Salatiga", "Solo", "Klaten"],
    "Salatiga":      ["Semarang", "Boyolali"],
    "Solo":          ["Boyolali", "Klaten", "Sukoharjo", "Wonogiri", "Sragen", "Grobogan"],
    "Klaten":        ["Boyolali", "Solo", "Yogyakarta", "Wonosari"],
    "Sukoharjo":     ["Solo", "Wonogiri"],
    "Wonogiri":      ["Solo", "Sukoharjo", "Pacitan", "Ponorogo"],
    "Sragen":        ["Solo", "Ngawi"],

    # ── DI YOGYAKARTA ───────────────────────────────────────
    "Yogyakarta":    ["Klaten", "Sleman", "Bantul", "Wates", "Wonosari"],
    "Sleman":        ["Yogyakarta", "Magelang"],
    "Bantul":        ["Yogyakarta"],
    "Wates":         ["Yogyakarta", "Purworejo"],
    "Wonosari":      ["Yogyakarta", "Klaten", "Pacitan"],

    # ── JAWA TIMUR ──────────────────────────────────────────
    "Tuban":         ["Rembang", "Bojonegoro", "Lamongan"],
    "Bojonegoro":    ["Blora", "Tuban", "Lamongan", "Ngawi"],
    "Lamongan":      ["Tuban", "Bojonegoro", "Gresik", "Jombang"],
    "Gresik":        ["Lamongan", "Surabaya"],
    "Surabaya":      ["Gresik", "Sidoarjo", "Mojokerto"],
    "Sidoarjo":      ["Surabaya", "Mojokerto", "Pasuruan"],
    "Pasuruan":      ["Sidoarjo", "Malang", "Probolinggo"],
    "Probolinggo":   ["Pasuruan", "Lumajang", "Bondowoso", "Situbondo"],
    "Lumajang":      ["Probolinggo", "Jember", "Malang"],
    "Jember":        ["Lumajang", "Banyuwangi", "Bondowoso"],
    "Bondowoso":     ["Probolinggo", "Jember", "Situbondo"],
    "Situbondo":     ["Probolinggo", "Bondowoso", "Banyuwangi"],
    "Banyuwangi":    ["Jember", "Situbondo"],
    "Mojokerto":     ["Surabaya", "Sidoarjo", "Jombang", "Malang"],
    "Jombang":       ["Lamongan", "Mojokerto", "Kediri", "Nganjuk"],
    "Malang":        ["Mojokerto", "Pasuruan", "Lumajang", "Blitar", "Kediri"],
    "Blitar":        ["Malang", "Kediri", "Tulungagung"],
    "Kediri":        ["Jombang", "Malang", "Blitar", "Nganjuk", "Tulungagung", "Madiun"],
    "Tulungagung":   ["Blitar", "Kediri", "Trenggalek"],
    "Trenggalek":    ["Tulungagung", "Ponorogo"],
    "Ponorogo":      ["Wonogiri", "Trenggalek", "Madiun", "Pacitan"],
    "Madiun":        ["Ngawi", "Jombang", "Kediri", "Ponorogo", "Nganjuk"],
    "Ngawi":         ["Sragen", "Bojonegoro", "Madiun"],
    "Nganjuk":       ["Jombang", "Kediri", "Madiun"],
    "Pacitan":       ["Wonogiri", "Wonosari", "Ponorogo", "Trenggalek"],
}


# ============================================================
# ALGORITMA BFS
# ============================================================
def bfs_shortest_path(graf, mulai, tujuan):
    """
    Mencari jalur terpendek menggunakan BFS.

    Parameter:
        graf  : dict - graf berupa adjacency list
        mulai : str  - kota asal
        tujuan: str  - kota tujuan

    Return:
        jalur    : list - urutan kota dari mulai ke tujuan
        urutan   : list - semua kota yang dikunjungi BFS
        logs     : list - log setiap langkah BFS
    """
    if mulai not in graf:
        return None, [], [f"Kota '{mulai}' tidak ada dalam graf!"]
    if tujuan not in graf:
        return None, [], [f"Kota '{tujuan}' tidak ada dalam graf!"]
    if mulai == tujuan:
        return [mulai], [mulai], ["Asal sama dengan Tujuan!"]

    queue   = deque([[mulai]])
    visited = {mulai}
    urutan  = [mulai]
    logs    = []

    logs.append(f"[MULAI] BFS dari '{mulai}' menuju '{tujuan}'")
    logs.append(f"        Queue: [{mulai}]")
    logs.append("")

    step = 1
    while queue:
        path = queue.popleft()
        curr = path[-1]

        logs.append(f"[Step {step:3}] Proses node : '{curr}'")
        logs.append(f"            Path saat ini: {' → '.join(path)}")

        if curr == tujuan:
            logs.append("            ✓ TUJUAN DITEMUKAN!")
            return path, urutan, logs

        tambah = []
        for nb in graf.get(curr, []):
            if nb not in visited:
                visited.add(nb)
                urutan.append(nb)
                queue.append(path + [nb])
                tambah.append(nb)

        if tambah:
            logs.append(f"            → Tambah ke queue: {tambah}")
        else:
            logs.append("            → Tidak ada tetangga baru")
        logs.append("")
        step += 1

    logs.append("[HASIL] Jalur tidak ditemukan!")
    return None, urutan, logs


# ============================================================
# VISUALISASI BERGAYA GOOGLE MAPS
# ============================================================

# Warna per provinsi
PROVINSI_WARNA = {
    "Merak": "#c8e6c9",         "Cilegon": "#c8e6c9",
    "Serang": "#c8e6c9",        "Pandeglang": "#c8e6c9",
    "Rangkasbitung": "#c8e6c9",
    "Jakarta": "#fff9c4",
    "Bekasi": "#bbdefb",        "Depok": "#bbdefb",
    "Bogor": "#bbdefb",         "Sukabumi": "#bbdefb",
    "Karawang": "#bbdefb",      "Purwakarta": "#bbdefb",
    "Subang": "#bbdefb",        "Bandung": "#bbdefb",
    "Sumedang": "#bbdefb",      "Cirebon": "#bbdefb",
    "Garut": "#bbdefb",         "Tasikmalaya": "#bbdefb",
    "Ciamis": "#bbdefb",        "Banjar": "#bbdefb",
    "Brebes": "#e1bee7",        "Tegal": "#e1bee7",
    "Pemalang": "#e1bee7",      "Pekalongan": "#e1bee7",
    "Batang": "#e1bee7",        "Kendal": "#e1bee7",
    "Semarang": "#e1bee7",      "Demak": "#e1bee7",
    "Kudus": "#e1bee7",         "Jepara": "#e1bee7",
    "Pati": "#e1bee7",          "Rembang": "#e1bee7",
    "Blora": "#e1bee7",         "Grobogan": "#e1bee7",
    "Purwokerto": "#e1bee7",    "Cilacap": "#e1bee7",
    "Kebumen": "#e1bee7",       "Banjarnegara": "#e1bee7",
    "Wonosobo": "#e1bee7",      "Temanggung": "#e1bee7",
    "Magelang": "#e1bee7",      "Purworejo": "#e1bee7",
    "Boyolali": "#e1bee7",      "Salatiga": "#e1bee7",
    "Solo": "#e1bee7",          "Klaten": "#e1bee7",
    "Sukoharjo": "#e1bee7",     "Wonogiri": "#e1bee7",
    "Sragen": "#e1bee7",
    "Yogyakarta": "#f8bbd0",    "Sleman": "#f8bbd0",
    "Bantul": "#f8bbd0",        "Wates": "#f8bbd0",
    "Wonosari": "#f8bbd0",
    "Tuban": "#b2ebf2",         "Bojonegoro": "#b2ebf2",
    "Lamongan": "#b2ebf2",      "Gresik": "#b2ebf2",
    "Surabaya": "#b2ebf2",      "Sidoarjo": "#b2ebf2",
    "Mojokerto": "#b2ebf2",     "Jombang": "#b2ebf2",
    "Ngawi": "#b2ebf2",         "Madiun": "#b2ebf2",
    "Nganjuk": "#b2ebf2",       "Kediri": "#b2ebf2",
    "Blitar": "#b2ebf2",        "Tulungagung": "#b2ebf2",
    "Trenggalek": "#b2ebf2",    "Ponorogo": "#b2ebf2",
    "Pacitan": "#b2ebf2",       "Malang": "#b2ebf2",
    "Pasuruan": "#b2ebf2",      "Probolinggo": "#b2ebf2",
    "Lumajang": "#b2ebf2",      "Jember": "#b2ebf2",
    "Bondowoso": "#b2ebf2",     "Situbondo": "#b2ebf2",
    "Banyuwangi": "#b2ebf2",
}


def lon_to_x(lon):
    return (lon - 105.5) * 55.0


def lat_to_y(lat):
    return (-lat - 5.75) * 55.0


def visualisasi_peta(jalur, mulai, tujuan, semua_dikunjungi):
    """Tampilkan peta Pulau Jawa bergaya Google Maps."""

    fig = plt.figure(figsize=(22, 10))
    fig.patch.set_facecolor('#1a1a2e')

    # ── PANEL KIRI: PETA ─────────────────────────────────────
    ax = fig.add_axes([0.0, 0.0, 0.65, 1.0])
    ax.set_facecolor('#a8d5e2')  # warna laut
    ax.axis('off')

    coord_xy = {k: (lon_to_x(v[0]), lat_to_y(v[1]))
                for k, v in KOORDINAT_KOTA.items()}

    xs = [v[0] for v in coord_xy.values()]
    ys = [v[1] for v in coord_xy.values()]
    margin = 1.8
    ax.set_xlim(min(xs) - margin, max(xs) + margin)
    ax.set_ylim(min(ys) - margin, max(ys) + margin)

    # Daratan Pulau Jawa (garis pantai kasar)
    garis_pantai_lon = [
        105.2, 105.7, 106.0, 106.5, 106.8, 107.2, 107.8, 108.3,
        108.7, 109.0, 109.4, 109.8, 110.2, 110.6, 111.0, 111.4,
        111.8, 112.2, 112.6, 113.0, 113.4, 113.8, 114.2, 114.5,
        114.5, 114.2, 113.8, 113.4, 113.0, 112.6, 112.2, 111.8,
        111.4, 111.0, 110.6, 110.2, 109.8, 109.4, 109.0, 108.6,
        108.2, 107.8, 107.4, 107.0, 106.6, 106.2, 105.8, 105.4, 105.2
    ]
    garis_pantai_lat = [
        -5.80, -5.85, -5.95, -6.00, -6.05, -6.10, -6.10, -6.50,
        -6.65, -6.80, -6.85, -6.88, -6.90, -6.88, -6.90, -6.92,
        -6.95, -6.92, -6.90, -7.10, -7.50, -7.75, -8.00, -8.25,
        -8.45, -8.60, -8.55, -8.40, -8.30, -8.25, -8.20, -8.10,
        -8.00, -8.20, -7.90, -7.75, -7.70, -7.65, -7.75, -7.40,
        -7.35, -7.20, -7.10, -7.00, -6.80, -6.55, -6.30, -6.00, -5.80
    ]
    px = [lon_to_x(l) for l in garis_pantai_lon]
    py = [lat_to_y(l) for l in garis_pantai_lat]
    ax.fill(px, py, color='#eef5e8', edgecolor='#9ab58a',
            linewidth=1.2, zorder=1, alpha=0.95)

    # ── Semua jalan (edge) ────────────────────────────────────
    drawn = set()
    for kota, neighbors in KONEKSI.items():
        for nb in neighbors:
            key = tuple(sorted([kota, nb]))
            if key in drawn:
                continue
            drawn.add(key)
            if kota not in coord_xy or nb not in coord_xy:
                continue
            x1, y1 = coord_xy[kota]
            x2, y2 = coord_xy[nb]
            ax.plot([x1, x2], [y1, y2],
                    color='#b0bec5', linewidth=1.2,
                    solid_capstyle='round', zorder=2, alpha=0.85)

    # ── Node dikunjungi BFS (kuning) ─────────────────────────
    for kota in semua_dikunjungi:
        if kota in (mulai, tujuan):
            continue
        if jalur and kota in jalur:
            continue
        x, y = coord_xy[kota]
        ax.scatter(x, y, s=110, c='#fff176',
                   edgecolors='#f9a825', linewidths=1.5,
                   zorder=5, alpha=0.9)

    # ── Jalur BFS ditemukan (biru tebal) ─────────────────────
    if jalur:
        for i in range(len(jalur) - 1):
            x1, y1 = coord_xy[jalur[i]]
            x2, y2 = coord_xy[jalur[i+1]]
            ax.plot([x1, x2], [y1, y2],
                    color='#1976D2', linewidth=7,
                    solid_capstyle='round', zorder=6, alpha=0.25)
            ax.plot([x1, x2], [y1, y2],
                    color='#1976D2', linewidth=3.5,
                    solid_capstyle='round', zorder=7)
        for kota in jalur[1:-1]:
            x, y = coord_xy[kota]
            ax.scatter(x, y, s=180, c='white',
                       edgecolors='#1976D2', linewidths=2.5, zorder=9)
            ax.scatter(x, y, s=60, c='#1976D2', zorder=10)

    # ── Semua node kota ──────────────────────────────────────
    for kota, (x, y) in coord_xy.items():
        if kota in (mulai, tujuan):
            continue
        if kota in semua_dikunjungi:
            continue
        warna = PROVINSI_WARNA.get(kota, 'white')
        ax.scatter(x, y, s=80, c=warna,
                   edgecolors='#78909c', linewidths=1.0,
                   zorder=4, alpha=0.9)

    # ── Titik ASAL (hijau, seperti Google Maps) ──────────────
    sx, sy = coord_xy[mulai]
    ax.scatter(sx, sy, s=500, c='#43a047',
               edgecolors='white', linewidths=2.5, zorder=11)
    ax.scatter(sx, sy, s=110, c='white', zorder=12)
    ax.text(sx, sy, 'A', fontsize=9, fontweight='bold',
            color='#43a047', ha='center', va='center', zorder=13)

    # ── Titik TUJUAN (merah, pin Google Maps) ────────────────
    tx, ty = coord_xy[tujuan]
    ax.scatter(tx, ty + 0.55, s=600, c='#e53935',
               edgecolors='white', linewidths=2.5, zorder=11)
    ax.scatter(tx, ty + 0.55, s=100, c='white', zorder=12)
    ax.plot([tx, tx], [ty, ty + 0.28],
            color='#e53935', linewidth=3, zorder=11)

    # ── Label nama kota ──────────────────────────────────────
    for kota, (x, y) in coord_xy.items():
        dy   = 0.28
        fs   = 6.2
        fw   = 'normal'
        col  = '#455a64'

        if kota == mulai:
            dy = -0.36; fs = 8.5; fw = 'bold'; col = '#1b5e20'
        elif kota == tujuan:
            dy = 0.90; fs = 8.5; fw = 'bold'; col = '#b71c1c'
        elif jalur and kota in jalur:
            fs = 7.5; fw = 'bold'; col = '#0d47a1'
        elif kota in semua_dikunjungi:
            col = '#e65100'; fs = 6.5

        ax.text(x, y + dy, kota,
                fontsize=fs, fontweight=fw, color=col,
                ha='center', va='bottom', zorder=15,
                path_effects=[pe.withStroke(linewidth=2.5,
                                            foreground='white')])

    # ── Label Provinsi ───────────────────────────────────────
    label_prov = [
        (106.08, -6.18, "BANTEN"),
        (106.82, -6.00, "JAKARTA"),
        (107.50, -6.55, "JAWA BARAT"),
        (110.00, -6.65, "JAWA TENGAH"),
        (110.37, -8.10, "DI YOGYAKARTA"),
        (112.70, -7.00, "JAWA TIMUR"),
    ]
    for lon, lat, nm in label_prov:
        ax.text(lon_to_x(lon), lat_to_y(lat), nm,
                fontsize=8, fontweight='bold',
                color='#607d8b', alpha=0.5,
                ha='center', va='center',
                style='italic', zorder=3)

    # ── Judul & Legenda ──────────────────────────────────────
    status = "✓ Jalur Ditemukan!" if jalur else "✗ Jalur Tidak Ditemukan"
    warna_status = '#1976D2' if jalur else '#e53935'
    ax.set_title(f"BFS Shortest Path — Peta Kota Pulau Jawa\n{status}",
                 fontsize=13, fontweight='bold',
                 color=warna_status, pad=10)

    legenda = [
        mpatches.Patch(color='#43a047',  label=f'Asal: {mulai}'),
        mpatches.Patch(color='#e53935',  label=f'Tujuan: {tujuan}'),
        mpatches.Patch(color='#1976D2',  label='Jalur BFS Terpendek'),
        mpatches.Patch(color='#fff176',  label=f'Node Dikunjungi ({len(semua_dikunjungi)})'),
        mpatches.Patch(color='#b0bec5',  label='Jalan'),
        mpatches.Patch(color='#c8e6c9',  label='Banten'),
        mpatches.Patch(color='#bbdefb',  label='Jawa Barat'),
        mpatches.Patch(color='#e1bee7',  label='Jawa Tengah'),
        mpatches.Patch(color='#f8bbd0',  label='DI Yogyakarta'),
        mpatches.Patch(color='#b2ebf2',  label='Jawa Timur'),
    ]
    ax.legend(handles=legenda, loc='lower left',
              fontsize=6.5, framealpha=0.92,
              fancybox=True, shadow=True, ncol=2)

    # ── PANEL KANAN: INFO ────────────────────────────────────
    ax2 = fig.add_axes([0.65, 0.0, 0.35, 1.0])
    ax2.set_facecolor('#1a1a2e')
    ax2.axis('off')

    lines = []
    lines.append("=" * 40)
    lines.append("  HASIL BFS SHORTEST PATH")
    lines.append("  Peta Kota Pulau Jawa")
    lines.append("=" * 40)
    lines.append(f"  Asal    : {mulai}")
    lines.append(f"  Tujuan  : {tujuan}")
    lines.append("")

    if jalur:
        lines.append(f"  STATUS  : ✓ Jalur Ditemukan!")
        lines.append(f"  Panjang : {len(jalur)-1} langkah")
        lines.append(f"  Dikunjungi: {len(semua_dikunjungi)} kota")
        lines.append("")
        lines.append("  Rute Lengkap:")
        for i, k in enumerate(jalur):
            if i == 0:
                tag = "  ◉ (Asal)"
            elif i == len(jalur) - 1:
                tag = "  ◉ (Tujuan)"
            else:
                tag = f"  {i}."
            lines.append(f"    {tag} {k}")
    else:
        lines.append("  STATUS  : ✗ Tidak Ditemukan")
        lines.append(f"  Dikunjungi: {len(semua_dikunjungi)} kota")

    lines.append("")
    lines.append("─" * 40)
    lines.append("  CARA KERJA BFS:")
    lines.append("─" * 40)
    lines.append("  1. Masukkan node awal ke QUEUE")
    lines.append("  2. Ambil dari depan queue (FIFO)")
    lines.append("  3. Tandai sebagai 'dikunjungi'")
    lines.append("  4. Tambahkan semua tetangga ke queue")
    lines.append("  5. Ulangi hingga tujuan ditemukan")
    lines.append("  ✓ Menjamin jalur TERPENDEK!")
    lines.append("")
    lines.append("─" * 40)
    lines.append("  STATISTIK GRAF:")
    lines.append("─" * 40)
    lines.append(f"  Jumlah kota  : {len(KOORDINAT_KOTA)}")
    lines.append(f"  Jumlah jalan : {sum(len(v) for v in KONEKSI.values())//2}")
    lines.append(f"  Provinsi     : 6")
    lines.append("")
    lines.append("  Kompleksitas Waktu : O(V + E)")
    lines.append("  Kompleksitas Ruang : O(V)")

    ax2.text(0.05, 0.97, "\n".join(lines),
             transform=ax2.transAxes,
             fontsize=8, verticalalignment='top',
             fontfamily='monospace', color='#e0e0e0',
             bbox=dict(boxstyle='round,pad=0.6',
                       facecolor='#16213e',
                       edgecolor='#1976D2',
                       linewidth=1.5))

    plt.savefig('bfs_hasil.png', dpi=150, bbox_inches='tight',
                facecolor='#1a1a2e')
    plt.show()
    print("\n[INFO] Peta berhasil disimpan: 'bfs_hasil.png'")


# ============================================================
# FUNGSI UTAMA
# ============================================================
def tampilkan_daftar_kota():
    provinsi = {
        "BANTEN":        ["Merak","Cilegon","Serang","Pandeglang","Rangkasbitung"],
        "DKI JAKARTA":   ["Jakarta"],
        "JAWA BARAT":    ["Bekasi","Depok","Bogor","Sukabumi","Karawang",
                          "Purwakarta","Subang","Bandung","Sumedang","Cirebon",
                          "Garut","Tasikmalaya","Ciamis","Banjar"],
        "JAWA TENGAH":   ["Brebes","Tegal","Pemalang","Pekalongan","Batang",
                          "Kendal","Semarang","Demak","Kudus","Jepara","Pati",
                          "Rembang","Blora","Grobogan","Purwokerto","Cilacap",
                          "Kebumen","Banjarnegara","Wonosobo","Temanggung",
                          "Magelang","Purworejo","Boyolali","Salatiga","Solo",
                          "Klaten","Sukoharjo","Wonogiri","Sragen"],
        "DI YOGYAKARTA": ["Yogyakarta","Sleman","Bantul","Wates","Wonosari"],
        "JAWA TIMUR":    ["Tuban","Bojonegoro","Lamongan","Gresik","Surabaya",
                          "Sidoarjo","Mojokerto","Jombang","Ngawi","Madiun",
                          "Nganjuk","Kediri","Blitar","Tulungagung","Trenggalek",
                          "Ponorogo","Pacitan","Malang","Pasuruan","Probolinggo",
                          "Lumajang","Jember","Bondowoso","Situbondo","Banyuwangi"],
    }
    print(f"\n📍 DAFTAR KOTA ({len(KOORDINAT_KOTA)} kota di Pulau Jawa):\n")
    for prov, kota_list in provinsi.items():
        print(f"  [{prov}]")
        # Cetak 4 kota per baris
        for i in range(0, len(kota_list), 4):
            print("   " + ", ".join(kota_list[i:i+4]))
        print()


def main():
    print("=" * 60)
    print("   BFS SHORTEST PATH — PETA KOTA PULAU JAWA")
    print("   Mata Kuliah: Kecerdasan Buatan")
    print("=" * 60)

    tampilkan_daftar_kota()

    print("─" * 60)
    while True:
        asal = input("\n🟢 Kota ASAL   : ").strip().title()
        if asal in KOORDINAT_KOTA:
            break
        print(f"   ⚠  '{asal}' tidak ditemukan. Coba lagi.")

    while True:
        tujuan = input("🔴 Kota TUJUAN : ").strip().title()
        if tujuan in KOORDINAT_KOTA:
            break
        print(f"   ⚠  '{tujuan}' tidak ditemukan. Coba lagi.")

    print(f"\n{'='*60}")
    print(f"   Mencari jalur: {asal} → {tujuan}")
    print(f"{'='*60}\n")

    jalur, dikunjungi, logs = bfs_shortest_path(KONEKSI, asal, tujuan)

    print("📋 LOG LANGKAH BFS:")
    print("─" * 60)
    for log in logs:
        print(log)

    print("=" * 60)
    print("📊 HASIL AKHIR:")
    print("=" * 60)
    if jalur:
        print(f"\n✅ Jalur terpendek ditemukan!")
        print(f"   Rute   : {' → '.join(jalur)}")
        print(f"   Panjang: {len(jalur)-1} langkah")
        print(f"   Total kota dikunjungi BFS: {len(dikunjungi)}")
    else:
        print(f"\n❌ Tidak ada jalur dari '{asal}' ke '{tujuan}'")

    print("\n🗺  Membuka visualisasi peta Pulau Jawa...")
    visualisasi_peta(jalur, asal, tujuan, dikunjungi)


def demo():
    """Demo otomatis: Merak → Banyuwangi (ujung barat ke ujung timur)."""
    asal, tujuan = "Merak", "Banyuwangi"
    print("=" * 60)
    print(f"   DEMO: {asal} → {tujuan}")
    print(f"   (Ujung Barat → Ujung Timur Pulau Jawa)")
    print("=" * 60)

    jalur, dikunjungi, logs = bfs_shortest_path(KONEKSI, asal, tujuan)

    print("\n📋 LOG BFS (ringkas):")
    for log in logs[:30]:  # tampilkan 30 langkah pertama
        print(log)
    if len(logs) > 30:
        print(f"  ... ({len(logs)-30} langkah berikutnya)")

    if jalur:
        print(f"\n✅ Rute  : {' → '.join(jalur)}")
        print(f"   Panjang: {len(jalur)-1} langkah")
        print(f"   Dikunjungi: {len(dikunjungi)} kota")

    visualisasi_peta(jalur, asal, tujuan, dikunjungi)


# ============================================================
if __name__ == "__main__":
    print("\nPilih mode:")
    print("  1. Input manual (pilih kota sendiri)")
    print("  2. Demo otomatis (Merak → Banyuwangi)")
    pilihan = input("Pilihan (1/2): ").strip()
    if pilihan == "2":
        demo()
    else:
        main()