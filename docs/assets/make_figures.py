# make_figures.py — génère les figures SVG du README (python docs/assets/make_figures.py)
import math, os, sys
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(OUT, "badges"), exist_ok=True)

SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"
INK, DIM, CARD, EDGE, ARROW = "#E6F1F5", "#8FA9B8", "#0B2530", "#1E3A45", "#2C4A57"
COPPER, BLUE, TEAL, RED, GREEN = "#E88C55", "#3B82F6", "#2DD4BF", "#F87171", "#4FD092"

def defs(extra=""):
    return f'''<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#03111C"/><stop offset="0.55" stop-color="#072833"/>
      <stop offset="1" stop-color="#0A3433"/></linearGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#5EEAD4" opacity="0.10"/></pattern>
    <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ARROW}"/></marker>{extra}</defs>'''

def frame(w, h, label, body, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">\n'
            f'  {defs(extra)}\n  <rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>\n'
            f'  <rect width="{w}" height="{h}" rx="18" fill="url(#dots)"/>\n  {body}\n</svg>\n')

def T(x, y, s, size=13.5, fill=DIM, weight=None, font=SANS, anchor=None, extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    a = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}"{w}{a} fill="{fill}"{extra}>{escape(s)}</text>'

def fade(i, body):
    return f'<g>{body}</g>'

def card(x, y, w, h, color, bar=True, stroke=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{CARD}" stroke="{stroke or EDGE}"{" stroke-width=\"1.4\"" if stroke else ""}/>'
    if bar:
        s += f'<rect x="{x}" y="{y}" width="4" height="{h}" rx="2" fill="{color}"/>'
    return s

def flow(path, begin=0.0, dur=1.2, color=TEAL):
    return (f'<path d="{path}" fill="none" stroke="{ARROW}" stroke-width="3" marker-end="url(#arr)"/>'
            f'<circle r="4" fill="{color}"><animateMotion dur="{dur}s" begin="{begin:.2f}s" repeatCount="indefinite" path="{path}"/></circle>')

def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)

# ---------------------------------------------------------------- géométrie de la pièce
def room_dist(a_deg, cx, cy):
    """Distance du centre (cx, cy) au mur d'une pièce rectangulaire avec une armoire, pour un angle (0 = droite, 90 = haut)."""
    a = math.radians(a_deg)
    dx, dy = math.cos(a), -math.sin(a)
    walls = [("x", cx - 118), ("x", cx + 122), ("y", cy - 112)]
    best = 1e9
    for kind, v in walls:
        if kind == "x" and abs(dx) > 1e-6:
            t = (v - cx) / dx
        elif kind == "y" and abs(dy) > 1e-6:
            t = (v - cy) / dy
        else:
            continue
        if t > 0:
            best = min(best, t)
    # armoire : rectangle [cx+40, cx+122] x [cy-112, cy-62]
    bx0, bx1, by0, by1 = cx + 45, cx + 122, cy - 112, cy - 66
    for t in [k * 0.5 for k in range(1, int(best * 2))]:
        px, py = cx + dx * t, cy + dy * t
        if bx0 <= px <= bx1 and by0 <= py <= by1:
            return t
    return best

# ---------------------------------------------------------------- bannière
def banner():
    cx, cy, R, dur = 168, 248, 150, 4.0
    b = []
    for r in (50, 100, 150):
        b.append(f'<path d="M{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy}" fill="none" stroke="#5EEAD4" stroke-opacity="0.14"/>')
    b.append(f'<line x1="{cx - R}" x2="{cx + R}" y1="{cy}" y2="{cy}" stroke="#5EEAD4" stroke-opacity="0.14"/>')
    # points du balayage : s'allument au passage du faisceau (0° → 180°)
    for k in range(0, 181, 6):
        d = room_dist(k, cx, cy) * 0.85      # la pièce tient dans le dernier arc
        px, py = cx + d * math.cos(math.radians(k)), cy - d * math.sin(math.radians(k))
        t = k / 180 * 0.9
        col = COPPER if px > cx + 34 and py < cy - 50 and d < 128 else TEAL
        b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.2" fill="{col}" opacity="0.3">'
                 f'<animate attributeName="opacity" dur="{dur}s" repeatCount="indefinite" keyTimes="0;{t:.3f};{t + 0.01:.3f};0.97;1" values="0.3;0.3;1;0.6;0.3"/></circle>')
    # faisceau
    b.append(f'<g><animateTransform attributeName="transform" type="rotate" dur="{dur}s" repeatCount="indefinite" keyTimes="0;0.9;1" values="0 {cx} {cy};-180 {cx} {cy};-180 {cx} {cy}"/>'
             f'<path d="M{cx},{cy} L{cx + R},{cy} A{R},{R} 0 0 0 {cx + R * math.cos(math.radians(14)):.1f},{cy - R * math.sin(math.radians(14)):.1f} Z" fill="{TEAL}" opacity="0.10"/>'
             f'<line x1="{cx}" y1="{cy}" x2="{cx + R}" y2="{cy}" stroke="{TEAL}" stroke-width="2" opacity="0.8"/></g>')
    # robot
    b.append(f'<rect x="{cx - 20}" y="{cy - 12}" width="40" height="30" rx="7" fill="{CARD}" stroke="{TEAL}" stroke-width="1.6"/>'
             f'<rect x="{cx - 27}" y="{cy - 6}" width="6" height="18" rx="2" fill="{DIM}"/><rect x="{cx + 21}" y="{cy - 6}" width="6" height="18" rx="2" fill="{DIM}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="4" fill="{TEAL}"/>')

    # titre
    b.append(f'<text x="352" y="140" font-family="{SANS}" font-size="42" font-weight="700" fill="{INK}" letter-spacing="-0.5">Robot Cartographe<tspan fill="{TEAL}">-SLAM</tspan></text>')
    b.append(T(354, 176, "Un robot qui dessine la carte d'une pièce, se recale par la vision et s'y déplace seul", 17, DIM))
    b.append(f'<rect x="354" y="198" width="120" height="3" rx="1.5" fill="{TEAL}"/>')
    b.append(T(354, 236, "ESP32  /  Python  /  14 TPs guidés  /  UDP sur Wi-Fi  /  ~100 €", 12.5, INK, font=MONO, extra=' opacity="0.85"'))

    # carte d'occupation + chemin A* (à droite)
    gx, gy, c, nc, nr = 1000, 40, 22, 11, 11
    walls = {(i, 0) for i in range(nc)} | {(i, nr - 1) for i in range(nc)} | {(0, j) for j in range(nr)} | {(nc - 1, j) for j in range(nr)}
    walls |= {(5, j) for j in range(0, 6)} | {(8, 7), (9, 7), (8, 8), (9, 8)}
    unknown = {(9, 1), (9, 2), (8, 1), (1, 9), (2, 9)}
    for i in range(nc):
        for j in range(nr):
            if (i, j) in walls:
                f, o = "#C9D7DE", 0.9
            elif (i, j) in unknown:
                f, o = "#0B2530", 1
            else:
                f, o = "#123C45", 1
            b.append(f'<rect x="{gx + i * c + 1}" y="{gy + j * c + 1}" width="{c - 2}" height="{c - 2}" rx="3" fill="{f}" opacity="{o}"/>')
    # marqueur ArUco sur le mur du haut
    mx, my = gx + 2 * c + 3, gy + 3
    b.append(f'<rect x="{mx}" y="{my}" width="16" height="16" fill="#03111C" stroke="{COPPER}" stroke-width="1.5"/>'
             f'<rect x="{mx + 4}" y="{my + 4}" width="4" height="4" fill="#fff"/><rect x="{mx + 8}" y="{my + 8}" width="4" height="4" fill="#fff"/>')
    b.append(T(mx + 8, gy - 8, "ArUco", 11, COPPER, anchor="middle", font=MONO))
    path = "M" + " L".join(f"{gx + i * c + c / 2:.0f},{gy + j * c + c / 2:.0f}" for i, j in [(2, 8), (3, 7), (4, 7), (6, 7), (7, 6), (7, 4), (8, 3)])
    b.append(f'<path d="{path}" fill="none" stroke="{TEAL}" stroke-width="2.4" stroke-dasharray="5 5"><animate attributeName="stroke-dashoffset" values="20;0" dur="0.8s" repeatCount="indefinite"/></path>')
    ex, ey = gx + 8 * c + c / 2, gy + 3 * c + c / 2
    b.append(f'<path d="M{ex - 6},{ey - 6} L{ex + 6},{ey + 6} M{ex + 6},{ey - 6} L{ex - 6},{ey + 6}" stroke="{COPPER}" stroke-width="2.5"/>')
    b.append(f'<circle r="7" fill="{TEAL}" stroke="#03111C" stroke-width="2"><animateMotion dur="5s" repeatCount="indefinite" path="{path}"/></circle>')
    b.append(T(gx + nc * c / 2, gy + nr * c + 22, "A*  ·  grille 5 cm", 12, TEAL, anchor="middle", font=MONO))
    extra = f'<radialGradient id="glow" cx="0.82" cy="0.5" r="0.45"><stop offset="0" stop-color="{TEAL}" stop-opacity="0.16"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>'
    svg = frame(1280, 320, "Robot Cartographe SLAM", '<rect width="1280" height="320" rx="18" fill="url(#glow)"/>\n  ' + "\n  ".join(b), extra)
    write("banner.svg", svg)

# ---------------------------------------------------------------- texte « tapé »
def typing():
    lines = ["Balayer une pièce au laser sur 360°",
             "Construire une grille d'occupation en direct",
             "Se recaler sur des marqueurs ArUco avec un EKF",
             "Rejoindre plusieurs points grâce à A*"]
    size, cw, W, period = 20, 12.0, 760, 4.0
    total = period * len(lines)
    out, clips = [], []
    for k, s in enumerate(lines):
        w = len(s) * cw
        x = (W - w) / 2
        t0, t1, t2, t3 = k * period, k * period + 1.6, k * period + 3.2, k * period + 3.7
        kt = lambda *ts: ";".join(f"{t / total:.4f}" for t in ts)
        times = [0, t0, t1, t2, t3, total] if k else [0, t1, t2, t3, total]
        wv = ["0", "0", f"{w:.0f}", f"{w:.0f}", "0", "0"] if k else ["0", f"{w:.0f}", f"{w:.0f}", "0", "0"]
        clips.append(f'<clipPath id="c{k}"><rect x="{x:.1f}" y="0" height="50" width="0"><animate attributeName="width" dur="{total}s" repeatCount="indefinite" keyTimes="{kt(*times)}" values="{";".join(wv)}"/></rect></clipPath>')
        out.append(f'<text x="{x:.1f}" y="32" clip-path="url(#c{k})" font-family="{MONO}" font-size="{size}" textLength="{w:.0f}" lengthAdjust="spacingAndGlyphs" fill="{TEAL}">{escape(s)}</text>')
        cx = [f"{x + float(v):.1f}" for v in wv]
        vis = ["0", "1", "1", "1", "0", "0"] if k else ["1", "1", "1", "0", "0"]
        out.append(f'<rect y="12" width="2.5" height="26" fill="{TEAL}" x="{x:.1f}" opacity="0">'
                   f'<animate attributeName="x" dur="{total}s" repeatCount="indefinite" keyTimes="{kt(*times)}" values="{";".join(cx)}"/>'
                   f'<animate attributeName="opacity" dur="{total}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt(*times)}" values="{";".join(vis)}"/></rect>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="50" viewBox="0 0 {W} 50" role="img" aria-label="{escape(" / ".join(lines))}">\n'
           f'  <defs>{"".join(clips)}</defs>\n  ' + "\n  ".join(out) + "\n</svg>\n")
    write("typing.svg", svg)

# ---------------------------------------------------------------- badges
def badge(name, label, value, color, dark_text=True):
    lw, vw = len(label) * 7.6 + 22, len(value) * 7.6 + 22
    W = lw + vw
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.1f}" height="28" role="img" aria-label="{escape(label)}: {escape(value)}"><title>{escape(label)}: {escape(value)}</title>'
           f'<g shape-rendering="crispEdges"><rect width="{lw:.1f}" height="28" fill="#0b2a33"/><rect x="{lw:.1f}" width="{vw:.1f}" height="28" fill="{color}"/></g>'
           f'<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="100">'
           f'<text transform="scale(.1)" x="{lw * 5:.0f}" y="175" textLength="{(lw - 22) * 10:.0f}">{escape(label)}</text>'
           f'<text transform="scale(.1)" x="{(lw + vw / 2) * 10:.0f}" y="175" textLength="{(vw - 22) * 10:.0f}" font-weight="bold" fill="{"#0b1f26" if dark_text else "#fff"}">{escape(value)}</text></g></svg>\n')
    write(f"badges/{name}.svg", svg)

def badges():
    badge("tps", "TPS", "14 GUIDÉS", COPPER)
    badge("phases", "PHASES", "TABLE + VOITURE", TEAL)
    badge("budget", "BUDGET", "≈ 100 €", "#F5B700")
    badge("esp32", "ESP32", "ARDUINO CORE 3.X", "#E7352C", False)
    badge("python", "PYTHON", "3.10+", BLUE, False)
    badge("opencv", "OPENCV", "ARUCO", "#8B5CF6", False)
    badge("reseau", "RÉSEAU", "UDP / WI-FI", TEAL)
    badge("langue", "LANGUE", "FRANÇAIS", "#C9D7DE")

# ---------------------------------------------------------------- cartes « ce que contient le dépôt »
def icon(kind, x, y, col):
    if kind == "doc":
        return (f'<rect x="{x}" y="{y - 14}" width="16" height="20" rx="2" fill="none" stroke="{col}" stroke-width="2"/>'
                + "".join(f'<line x1="{x + 4}" x2="{x + 12}" y1="{y - 8 + 4 * k}" y2="{y - 8 + 4 * k}" stroke="{col}" stroke-width="1.6" opacity="0.8"/>' for k in range(3)))
    if kind == "steps":
        return "".join(f'<circle cx="{x + 4 + 9 * k}" cy="{y - 4}" r="3.5" fill="{col}" opacity="{1 - 0.12 * k:.2f}"/>' for k in range(5))
    if kind == "phases":
        return (f'<rect x="{x}" y="{y - 12}" width="14" height="14" rx="3" fill="{COPPER}"/>'
                f'<path d="M{x + 17},{y - 5} L{x + 25},{y - 5}" stroke="{col}" stroke-width="2"/>'
                f'<rect x="{x + 27}" y="{y - 12}" width="14" height="14" rx="3" fill="{TEAL}"/>')
    if kind == "chip":
        s = f'<rect x="{x + 3}" y="{y - 13}" width="16" height="16" rx="2" fill="none" stroke="{col}" stroke-width="2"/>'
        for k in range(3):
            s += f'<line x1="{x}" x2="{x + 3}" y1="{y - 9 + 4 * k}" y2="{y - 9 + 4 * k}" stroke="{col}" stroke-width="1.6"/>'
            s += f'<line x1="{x + 19}" x2="{x + 22}" y1="{y - 9 + 4 * k}" y2="{y - 9 + 4 * k}" stroke="{col}" stroke-width="1.6"/>'
        return s
    if kind == "grid":
        cells = [1, 0, 1, 0, 0, 1, 1, 0, 0]
        return "".join(f'<rect x="{x + 7 * (k % 3)}" y="{y - 14 + 7 * (k // 3)}" width="6" height="6" rx="1" fill="{col}" opacity="{0.9 if v else 0.3}"/>' for k, v in enumerate(cells))
    if kind == "path":
        return (f'<path d="M{x},{y + 2} L{x + 8},{y - 6} L{x + 16},{y - 2} L{x + 26},{y - 12}" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="3 3"/>'
                f'<circle cx="{x}" cy="{y + 2}" r="3" fill="{col}"/><circle cx="{x + 26}" cy="{y - 12}" r="3.5" fill="{COPPER}"/>')
    return ""

def features():
    cards = [
        ("doc", COPPER, "Un manuel, un seul fichier", ["index.html s'ouvre dans le navigateur, sans", "serveur : schémas, brochage, protocole et", "checklists mémorisées d'une séance à l'autre."]),
        ("steps", BLUE, "14 TPs guidés, pas à pas", ["Objectif, câblage, code complet, critères", "de validation chiffrés, pièges fréquents", "et checklist pour chaque séance."]),
        ("phases", TEAL, "Sur table, puis sur la voiture", ["Chaque brique est validée seule sur", "plaque d'essai (phase A) avant d'être", "assemblée sur le châssis (phase B)."]),
        ("chip", COPPER, "Firmware ESP32 temps réel", ["Régulateur PI à 50 Hz, encodeurs x4 sur", "interruptions, balayage non bloquant", "et chien de garde de 500 ms."]),
        ("grid", BLUE, "SLAM léger en Python", ["Odométrie, grille d'occupation, filtre", "de Kalman étendu et marqueurs ArUco,", "avec numpy et OpenCV seulement."]),
        ("path", TEAL, "Navigation multi-points", ["On clique des buts sur la carte : A*", "sur les obstacles gonflés, suivi du", "chemin et balayage à chaque arrivée."]),
    ]
    b = []
    for k, (ic, col, title, lines) in enumerate(cards):
        x, y = 30 + 410 * (k % 3), 24 + 176 * (k // 3)
        s = card(x, y, 396, 162, col) + icon(ic, x + 26, y + 62, col)
        s += T(x + 80, y + 64, title, 17, INK, 700)
        s += "".join(T(x + 26, y + 104 + 22 * n, l, 14.5) for n, l in enumerate(lines))
        b.append(fade(k, s))
    write("features.svg", frame(1280, 386, "Ce que contient le dépôt", "\n  ".join(b)))

# ---------------------------------------------------------------- « comment ça marche » : 4 étapes
def steps():
    W, H, pw, py0, ph = 1280, 380, 272, 70, 230
    xs = [30 + k * (pw + 39) for k in range(4)]
    b = []
    heads = [("1 · Balayer", COPPER), ("2 · Cartographier", BLUE), ("3 · Se recaler", TEAL), ("4 · Naviguer", GREEN)]
    caps = [["VL53L1X sur servo : 61 mesures", "sur 180°, puis demi-tour"],
            ["grille d'occupation log-odds,", "cases de 5 cm, en direct"],
            ["marqueur ArUco vu par l'ESP32-CAM :", "l'EKF corrige la dérive"],
            ["A* sur la carte, puis suivi", "des points jusqu'à chaque but"]]
    for k, x in enumerate(xs):
        name, col = heads[k]
        b.append(T(x + pw / 2, 44, name, 16, INK, 700, anchor="middle"))
        b.append(f'<rect x="{x}" y="{py0}" width="{pw}" height="{ph}" rx="14" fill="{CARD}" stroke="{EDGE}"/>')
        b.append(f'<rect x="{x + pw / 2 - 30}" y="52" width="60" height="3" rx="1.5" fill="{col}"/>')
        for n, l in enumerate(caps[k]):
            b.append(T(x + pw / 2, py0 + ph + 28 + 20 * n, l, 14, DIM, anchor="middle"))
        if k < 3:
            p = f"M{x + pw + 6},{py0 + ph / 2} L{x + pw + 31},{py0 + ph / 2}"
            b.append(flow(p, 0.3 * k))

    # 1. balayage
    x0 = xs[0]; cx, cy = x0 + pw / 2, py0 + 190
    sc = 0.95
    for a in range(0, 181, 6):
        d = room_dist(a, 0, 0) * sc * 0.95
        ra = math.radians(a)
        px, py = cx + d * math.cos(ra), cy - d * math.sin(ra)
        t = a / 180 * 0.9
        b.append(f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{COPPER}" stroke-width="1" opacity="0">'
                 f'<animate attributeName="opacity" dur="4s" repeatCount="indefinite" keyTimes="0;{t:.3f};{t + 0.01:.3f};{min(t + 0.08, 0.99):.3f};1" values="0;0;0.7;0;0"/></line>')
        b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="{COPPER}" opacity="0.35">'
                 f'<animate attributeName="opacity" dur="4s" repeatCount="indefinite" keyTimes="0;{t:.3f};{t + 0.01:.3f};0.97;1" values="0.35;0.35;1;0.7;0.35"/></circle>')
    b.append(f'<rect x="{cx - 16}" y="{cy - 8}" width="32" height="24" rx="6" fill="#03111C" stroke="{COPPER}" stroke-width="1.6"/><circle cx="{cx}" cy="{cy}" r="3.5" fill="{COPPER}"/>')

    # 2. grille
    x0 = xs[1]; c = 20; gx, gy = x0 + (pw - 12 * c) / 2, py0 + 15
    walls = {(i, 0) for i in range(12)} | {(0, j) for j in range(9)} | {(11, j) for j in range(9)} | {(5, j) for j in range(0, 5)} | {(8, 6), (9, 6)}
    unknown = {(i, j) for i in range(12) for j in range(7, 9) if i > 6} | {(i, 8) for i in range(12)} | {(1, 7), (2, 7)}
    for j in range(9):
        for i in range(12):
            if (i, j) in unknown:
                f, o = "#0F2E38", 1
            elif (i, j) in walls:
                f, o = "#C9D7DE", 0.9
            else:
                f, o = "#123C45", 1
            b.append(f'<rect x="{gx + i * c + 1}" y="{gy + j * c + 1}" width="{c - 2}" height="{c - 2}" rx="3" fill="{f}" opacity="{o}"/>')
    lx = x0 + 22
    for n, (f, l) in enumerate([("#123C45", "libre"), ("#C9D7DE", "mur"), ("#0F2E38", "inconnu")]):
        b.append(f'<rect x="{lx + n * 82}" y="{py0 + ph - 14}" width="10" height="10" rx="2" fill="{f}" stroke="{EDGE}"/>' + T(lx + n * 82 + 15, py0 + ph - 5, l, 12.5))

    # 3. recalage
    x0 = xs[2]; mx, my = x0 + pw / 2 - 12, py0 + 22
    b.append(f'<line x1="{x0 + 20}" x2="{x0 + pw - 20}" y1="{py0 + 22}" y2="{py0 + 22}" stroke="#C9D7DE" stroke-width="4" opacity="0.8"/>')
    b.append(f'<rect x="{mx}" y="{my + 4}" width="24" height="24" fill="#03111C" stroke="{TEAL}" stroke-width="1.5"/>'
             f'<rect x="{mx + 5}" y="{my + 9}" width="6" height="6" fill="#fff"/><rect x="{mx + 13}" y="{my + 17}" width="6" height="6" fill="#fff"/>')
    b.append(T(mx + 12, my + 46, "ArUco n° 2, position connue", 12.5, TEAL, font=MONO, anchor="middle"))
    rx, ry = x0 + pw / 2 + 10, py0 + 160
    b.append(f'<line x1="{rx}" y1="{ry}" x2="{mx + 12}" y2="{my + 30}" stroke="{TEAL}" stroke-width="1.6" stroke-dasharray="4 4">'
             f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.35;0.4;0.85;1" dur="4s" repeatCount="indefinite"/></line>')
    b.append(f'<ellipse cx="{rx}" cy="{ry}" fill="{TEAL}" fill-opacity="0.10" stroke="{TEAL}" stroke-dasharray="3 3">'
             f'<animate attributeName="rx" values="16;52;52;18;16" keyTimes="0;0.35;0.4;0.55;1" dur="4s" repeatCount="indefinite"/>'
             f'<animate attributeName="ry" values="12;34;34;13;12" keyTimes="0;0.35;0.4;0.55;1" dur="4s" repeatCount="indefinite"/></ellipse>')
    b.append(f'<g opacity="0.45"><animateTransform attributeName="transform" type="translate" values="0 0;-34 10;-34 10;0 0;0 0" keyTimes="0;0.35;0.4;0.55;1" dur="4s" repeatCount="indefinite"/>'
             f'<circle cx="{rx}" cy="{ry}" r="8" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="3 2"/></g>')
    b.append(f'<circle cx="{rx}" cy="{ry}" r="8" fill="{TEAL}" stroke="#03111C" stroke-width="2"/><line x1="{rx}" y1="{ry}" x2="{rx - 5}" y2="{ry - 14}" stroke="#03111C" stroke-width="2"/>')
    b.append(f'<line x1="{x0 + 24}" x2="{x0 + 40}" y1="{py0 + ph - 10}" y2="{py0 + ph - 10}" stroke="{RED}" stroke-width="1.6" stroke-dasharray="3 2"/>' + T(x0 + 46, py0 + ph - 6, "odométrie seule", 12.5))
    b.append(f'<circle cx="{x0 + 158}" cy="{py0 + ph - 10}" r="5" fill="{TEAL}"/>' + T(x0 + 168, py0 + ph - 6, "estimation EKF", 12.5))

    # 4. navigation
    x0 = xs[3]; c = 20; gx, gy = x0 + (pw - 12 * c) / 2, py0 + 15
    walls = {(i, 0) for i in range(12)} | {(i, 9) for i in range(12)} | {(0, j) for j in range(10)} | {(11, j) for j in range(10)} | {(4, j) for j in range(0, 6)} | {(8, j) for j in range(4, 9)}
    for j in range(10):
        for i in range(12):
            f, o = ("#C9D7DE", 0.9) if (i, j) in walls else ("#123C45", 1)
            b.append(f'<rect x="{gx + i * c + 1}" y="{gy + j * c + 1}" width="{c - 2}" height="{c - 2}" rx="3" fill="{f}" opacity="{o}"/>')
    P = lambda i, j: (gx + i * c + c / 2, gy + j * c + c / 2)
    route = [(2, 3), (2, 7), (3, 7), (5, 7), (6, 6), (6, 3), (7, 2), (9, 2), (10, 3), (10, 7)]
    path = "M" + " L".join(f"{P(i, j)[0]:.0f},{P(i, j)[1]:.0f}" for i, j in route)
    b.append(f'<path d="{path}" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-dasharray="5 5"><animate attributeName="stroke-dashoffset" values="20;0" dur="0.8s" repeatCount="indefinite"/></path>')
    for n, (i, j) in enumerate([(7, 2), (10, 7)]):
        px, py = P(i, j)
        b.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="9" fill="{COPPER}"/>' + T(px, py + 4, str(n + 1), 11, "#03111C", 700, anchor="middle"))
    b.append(f'<circle r="7" fill="{GREEN}" stroke="#03111C" stroke-width="2"><animateMotion dur="6s" repeatCount="indefinite" path="{path}"/></circle>')
    write("comment.svg", frame(W, H, "Balayer, cartographier, se recaler, naviguer", "\n  ".join(b)))

# ---------------------------------------------------------------- architecture
def node(x, y, w, h, title, sub, col, i=0, sub_font=MONO):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{CARD}" stroke="{col}" stroke-width="1.4"/>'
         f'<circle cx="{x + 18}" cy="{y + 24}" r="5" fill="{col}"><animate attributeName="opacity" values="1;0.35;1" dur="2s" begin="{0.3 * i:.1f}s" repeatCount="indefinite"/></circle>'
         + T(x + 31, y + 29, title, 15, INK, 700) + T(x + 18, y + h - 13, sub, 13, DIM, font=sub_font))
    return s

def architecture():
    W, H = 1280, 440
    b = []
    # cadres
    b.append(f'<rect x="24" y="24" width="510" height="392" rx="16" fill="none" stroke="{COPPER}" stroke-opacity="0.5" stroke-dasharray="6 6"/>' + T(46, 54, "ROBOT", 13, COPPER, 700, extra=' letter-spacing="2"') + T(110, 54, "temps réel", 13, DIM))
    b.append(f'<rect x="700" y="24" width="556" height="392" rx="16" fill="none" stroke="{TEAL}" stroke-opacity="0.5" stroke-dasharray="6 6"/>' + T(722, 54, "PC · PYTHON", 13, TEAL, 700, extra=' letter-spacing="2"') + T(840, 54, "mémoire et calcul", 13, DIM))
    # robot
    sensors = [("Laser + servo", "VL53L1X · SG90", 76), ("2 encodeurs", "quadrature x4", 152), ("Gyroscope", "MPU6050 · I2C", 228), ("Batterie 2S", "ADC · 7,4 V", 304)]
    for n, (t, s, y) in enumerate(sensors):
        b.append(fade(n, node(44, y, 200, 62, t, s, COPPER, n)))
        b.append(f'<path d="M244,{y + 31} C272,{y + 31} 270,170 296,170" fill="none" stroke="{ARROW}" stroke-width="2" marker-end="url(#arr)"/>')
    b.append(fade(4, node(300, 110, 214, 112, "ESP32", "balayage non bloquant", COPPER, 4)
                  + T(318, 174, "PI 50 Hz · ticks · cap", 13, DIM, font=MONO)))
    b.append(f'<path d="M407,222 L407,250" stroke="{ARROW}" stroke-width="3" marker-end="url(#arr)"/>')
    b.append(fade(5, node(300, 254, 214, 62, "TB6612 + moteurs", "PWM 20 kHz", COPPER, 5)))
    b.append(fade(6, node(300, 336, 214, 62, "ESP32-CAM", "HTTP /capture", COPPER, 6)))
    # PC
    pc = {"udp": (722, 82, "Réception UDP", "link.py"), "odo": (910, 82, "Odométrie", "odometry.py"), "ekf": (1086, 82, "Kalman (EKF)", "ekf.py"),
          "astar": (722, 206, "A* + suivi", "planner.py"), "grid": (910, 206, "Grille", "grid_map.py"),
          "aruco": (722, 330, "Vision ArUco", "aruco_cam.py")}
    for n, (k, (x, y, t, s)) in enumerate(pc.items()):
        b.append(fade(n, node(x, y, 158, 66, t, s, TEAL, n)))
    b.append(flow("M880,115 L906,115", 0.0, 0.9))
    b.append(flow("M1068,115 L1082,115", 0.3, 0.9))
    b.append(flow("M1150,148 L1150,239 L1072,239", 0.6, 1.4))
    b.append(flow("M910,239 L892,239", 0.9, 0.9))
    b.append(flow("M888,363 L1214,363 L1214,152", 0.2, 1.8))
    b.append(T(1226, 300, "recalage", 13, DIM, font=MONO, extra=' transform="rotate(90 1226 300)"'))
    b.append(T(1111, 230, "pose", 13, DIM, font=MONO, anchor="middle"))
    # liaisons
    b.append(flow("M514,140 C610,140 620,115 718,115", 0.0, 1.4, COPPER))
    b.append(T(617, 112, "UDP 5005 · O, S", 13.5, COPPER, font=MONO, anchor="middle"))
    b.append(flow("M722,239 C620,239 610,196 518,196", 0.5, 1.4, TEAL))
    b.append(T(617, 248, "UDP 5006 · V, C, X", 13.5, TEAL, font=MONO, anchor="middle"))
    b.append(flow("M514,367 L718,363", 0.8, 1.4, BLUE))
    b.append(T(617, 354, "HTTP · JPEG", 13.5, BLUE, font=MONO, anchor="middle"))
    write("architecture.svg", frame(W, H, "Architecture : le robot fait le temps réel, le PC la carte et la navigation", "\n  ".join(b)))

# ---------------------------------------------------------------- parcours des TPs
def parcours():
    A = [("0", "Installer l'environnement", "tp0_blink"), ("1", "GPIO, PWM, interruptions, timers", "tp1_pwm"),
         ("2", "Laser VL53L1X et filtre médian", "tp2_laser"), ("3", "Radar 2D : servo + laser", "tp3_radar"),
         ("4", "Radar vers le PC en Wi-Fi (UDP)", "tp4_radar_wifi"), ("5", "Caméra, calibration, ArUco", "calibrate.py"),
         ("6", "Gyroscope MPU6050 : le cap", "tp6_cap"), ("7", "Moteurs, encodeurs, régulateur PI", "tp7_banc_moteur")]
    B = [("8", "Montage mécanique et alimentation", "config.h"), ("9", "Firmware complet, odométrie, clavier", "teleop.py"),
         ("10", "Cartographie par grille d'occupation", "map_live.py"), ("11", "Fusion : Kalman + ArUco", "fusion_test.py"),
         ("12", "Navigation A* vers plusieurs points", "app.py"), ("13", "Intégration, tests, soutenance", "mesures/")]
    cols = [(30, "Phase A · sur table", "chaque brique validée seule", COPPER, A), (660, "Phase B · sur la voiture", "tout assemblé sur le châssis", TEAL, B)]
    b, rh = [], 50
    for x, title, sub, col, rows in cols:
        b.append(T(x, 44, title, 16, col, 700) + T(x + 590, 44, sub, 12.5, DIM, anchor="end"))
        b.append(f'<line x1="{x}" x2="{x + 590}" y1="58" y2="58" stroke="{col}" stroke-width="1.5" opacity="0.8"/>')
        for n, (num, t, code) in enumerate(rows):
            y = 74 + n * (rh + 8)
            pw = len(code) * 7.8 + 26
            s = card(x, y, 590, rh, col)
            s += f'<circle cx="{x + 34}" cy="{y + rh / 2}" r="15" fill="none" stroke="{col}" stroke-width="1.6"/>' + T(x + 34, y + rh / 2 + 5, num, 13, col, 700, anchor="middle")
            s += T(x + 62, y + rh / 2 + 6, t, 16, INK, 600)
            s += f'<rect x="{x + 570 - pw:.0f}" y="{y + 13}" width="{pw:.0f}" height="24" rx="12" fill="none" stroke="{col}"/>' + T(x + 570 - pw / 2, y + 30, code, 13, col, font=MONO, anchor="middle")
            b.append(fade(n, s))
    b.append(T(1250, 74 + 8 * (rh + 8) + 8, "pastille : dossier ou script principal du TP", 12.5, DIM, anchor="end"))
    write("parcours.svg", frame(1280, 74 + 8 * (rh + 8) + 24, "Les 14 TPs en deux phases", "\n  ".join(b)))

# ---------------------------------------------------------------- pied de page
def footer():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="854" height="110" viewBox="0 0 854 110" role="img" aria-label="">
  <defs><linearGradient id="linear" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#0A3433"/><stop offset="50%" stop-color="{COPPER}" stop-opacity="0.6"/><stop offset="100%" stop-color="{TEAL}"/>
  </linearGradient></defs>
  <g transform="rotate(180 427 55)">
    <path fill="url(#linear)" opacity="0.4"><animate attributeName="d" dur="20s" repeatCount="indefinite" keyTimes="0;0.333;0.667;1" calcMode="spline" keySplines="0.2 0 0.2 1;0.2 0 0.2 1;0.2 0 0.2 1"
      values="M0 0L 0 30Q 213.5 70 427 40T 854 65L 854 0 Z;M0 0L 0 55Q 213.5 70 427 50T 854 40L 854 0 Z;M0 0L 0 75Q 213.5 45 427 75T 854 40L 854 0 Z;M0 0L 0 30Q 213.5 70 427 40T 854 65L 854 0 Z"/></path>
    <path fill="url(#linear)" opacity="0.4"><animate attributeName="d" dur="20s" begin="-10s" repeatCount="indefinite" keyTimes="0;0.333;0.667;1" calcMode="spline" keySplines="0.2 0 0.2 1;0.2 0 0.2 1;0.2 0 0.2 1"
      values="M0 0L 0 45Q 213.5 90 427 60T 854 70L 854 0 Z;M0 0L 0 60Q 213.5 30 427 30T 854 50L 854 0 Z;M0 0L 0 55Q 213.5 35 427 60T 854 75L 854 0 Z;M0 0L 0 45Q 213.5 90 427 60T 854 70L 854 0 Z"/></path>
  </g>
</svg>
'''
    write("footer.svg", svg)

banner(); typing(); badges(); features(); steps(); architecture(); parcours(); footer()
print("ok")
