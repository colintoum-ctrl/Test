#!/usr/bin/env python3
"""
FIA IA Demo Video Generator
Generates a 3-minute product demo MP4 for "LA FIA À L'ÈRE DE L'INTELLIGENCE ARTIFICIELLE"
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip, concatenate_videoclips
from moviepy.audio.AudioClip import AudioArrayClip
import math
import os

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
W, H = 1920, 1080
FPS = 30
BG   = (13,  13,  13)
RED  = (232,  0,  13)
GOLD = (201, 168, 76)
WHT  = (255, 255, 255)
DGR  = (40,  40,  40)
MGR  = (120, 120, 120)

OUTPUT_DIR = "/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD    = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# ─── FONT CACHE ───────────────────────────────────────────────────────────────
_font_cache: dict = {}

def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    key = (size, bold)
    if key not in _font_cache:
        path = FONT_BOLD if bold else FONT_REGULAR
        try:
            _font_cache[key] = ImageFont.truetype(path, size)
        except Exception:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]


# ─── DRAWING HELPERS ──────────────────────────────────────────────────────────
def new_frame() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)

def img_to_array(img: Image.Image) -> np.ndarray:
    return np.array(img)

def ease_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3

def ease_io(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)

def tw(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> int:
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0]

def th(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> int:
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[3] - bb[1]

def center_x(draw, text, f):
    return (W - tw(draw, text, f)) // 2

def draw_centered(draw, text, y, f, color=WHT):
    draw.text((center_x(draw, text, f), y), text, font=f, fill=color)

def hbar(draw, y, color=RED, width=300, thickness=5):
    x = (W - width) // 2
    draw.rectangle([x, y, x + width, y + thickness], fill=color)

def col(base_color: tuple, alpha: float) -> tuple:
    return tuple(int(c * max(0.0, min(1.0, alpha))) for c in base_color)

def count_up(end_val: float, t: float, dur: float = 1.4) -> float:
    return end_val * ease_out(min(1.0, t / dur))

def top_bar(draw, t, speed=1.5, thickness=6):
    w = int(W * ease_out(min(1.0, t / speed)))
    draw.rectangle([0, 0, w, thickness], fill=RED)

def bottom_bar(draw):
    draw.rectangle([0, H - 6, W, H], fill=RED)

def scene_title(draw, text, y=60, f_size=52):
    draw_centered(draw, text, y, font(f_size))

def divider_line(draw, y=130, width_ratio=0.35):
    w = int(W * width_ratio)
    draw.rectangle([(W - w) // 2, y, (W + w) // 2, y + 4], fill=RED)


# ─── AUDIO ────────────────────────────────────────────────────────────────────
def generate_audio(duration: float = 185.0) -> tuple[np.ndarray, int]:
    sr = 44100
    n  = int(sr * duration)
    t  = np.linspace(0, duration, n, endpoint=False)
    bpm = 120.0
    beat = bpm / 60.0          # beats per second
    eighth = beat * 2.0        # 8th notes per second

    # Kick (every beat)
    kick = np.zeros(n)
    for kt in np.arange(0, duration, 1.0 / beat):
        idx = int(kt * sr)
        length = min(int(0.12 * sr), n - idx)
        if length <= 0:
            continue
        s = np.arange(length) / sr
        kick[idx:idx+length] = np.exp(-s * 28) * np.sin(2*np.pi*55*s * np.exp(-s*8)) * 0.9

    # Bass sine
    bass = 0.22 * np.sin(2*np.pi*55*t) * (0.6 + 0.4 * np.sin(2*np.pi*beat*t))

    # Hi-hat (8th notes)
    hihat = np.zeros(n)
    rng = np.random.default_rng(42)
    for ht in np.arange(0, duration, 1.0 / eighth):
        idx = int(ht * sr)
        length = min(int(0.04 * sr), n - idx)
        if length <= 0:
            continue
        s = np.arange(length) / sr
        noise = rng.standard_normal(length)
        hihat[idx:idx+length] = noise * np.exp(-s * 120) * 0.12

    # Synth pad
    lfo = 0.5 + 0.5 * np.sin(2*np.pi*0.08*t)
    pad = (0.12 * np.sin(2*np.pi*110*t) +
           0.07 * np.sin(2*np.pi*165*t) +
           0.04 * np.sin(2*np.pi*220*t)) * lfo

    # Engine sweep
    eng_freq = 180 + 100*(0.5 + 0.5*np.sin(2*np.pi*0.04*t))
    engine = 0.04 * np.sin(2*np.pi * np.cumsum(eng_freq) / sr)

    mix = kick + bass + hihat + pad + engine
    peak = np.max(np.abs(mix))
    if peak > 0:
        mix /= peak
    mix *= 0.72

    fade = int(sr * 2.5)
    mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)

    stereo = np.column_stack([mix, mix]).astype(np.float32)
    return stereo, sr


# ─── TRANSITION ───────────────────────────────────────────────────────────────
def make_transition(duration: float = 0.12) -> VideoClip:
    def frame(t):
        p = t / duration
        a = (p * 2) if p < 0.5 else ((1 - p) * 2)
        return np.full((H, W, 3), [int(RED[0]*a), int(RED[1]*a), int(RED[2]*a)],
                       dtype=np.uint8)
    return VideoClip(frame, duration=duration)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENES
# ═══════════════════════════════════════════════════════════════════════════════

# ─── SCENE 01  INTRO ──────────────────────────────────────────────────────────
def scene_01(t, duration=12.0):
    img, draw = new_frame()

    # Subtle grid
    fade = ease_io(min(1, t / 2.5))
    for i in range(0, W, 80):
        c = int(12 * fade)
        draw.line([(i, 0), (i, H)], fill=(c, c, c), width=1)
    for j in range(0, H, 80):
        c = int(12 * fade)
        draw.line([(0, j), (W, j)], fill=(c, c, c), width=1)

    top_bar(draw, t, speed=1.2)

    f_main = font(76)
    f_sub  = font(34)
    f_acc  = font(22, bold=False)

    title_fade = ease_io(min(1, t / 2.0))
    draw_centered(draw, "LA FIA À L'ÈRE DE", 340, f_main, col(WHT, title_fade))
    draw_centered(draw, "L'INTELLIGENCE ARTIFICIELLE", 435, f_main, col(RED, title_fade))

    # Red underline animates in at t=1.5
    ul_p = ease_out(min(1, max(0, (t - 1.5) / 1.0)))
    ul_w = int(660 * ul_p)
    if ul_w > 0:
        draw.rectangle([(W - ul_w) // 2, 545, (W + ul_w) // 2, 550], fill=RED)

    # Authors
    auth_fade = ease_io(min(1, max(0, (t - 2.2) / 1.2)))
    draw_centered(draw, "Colin Toum  &  Matthieu Dambrin", 590, f_sub,
                  col(GOLD, auth_fade))

    # Tagline
    tag_fade = ease_io(min(1, max(0, (t - 3.2) / 1.0)))
    draw_centered(draw, "▶  Présentation Confidentielle — 2024", 695,
                  f_acc, col(MGR, tag_fade))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 02  FIA EN CHIFFRES ────────────────────────────────────────────────
def scene_02(t, duration=10.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "LA FIA EN CHIFFRES")
    divider_line(draw, 130, 0.30)

    stats = [
        ("143",    "CHAMPIONNATS", "sous la bannière FIA"),
        ("150",    "PAYS",         "représentés dans le monde"),
        ("2,5 Md$","BUDGET",       "annuel de la FIA"),
        ("445M",   "FANS",         "audience mondiale"),
    ]
    card_w, card_h = 410, 260
    gap = 30
    total_w = 4 * card_w + 3 * gap
    sx = (W - total_w) // 2

    for i, (num, lbl, sub) in enumerate(stats):
        delay = i * 0.38
        p = ease_out(min(1, max(0, (t - delay) / 0.55)))
        if p <= 0:
            continue
        x = sx + i * (card_w + gap)
        y = int(180 + 40 * (1 - p))
        draw.rounded_rectangle([x, y, x+card_w, y+card_h], radius=12,
                                fill=(int(35*p), int(35*p), int(35*p)))
        draw.rectangle([x, y, x+card_w, y+4], fill=col(RED, p))

        # Number
        fn = font(64)
        draw.text((x + (card_w - tw(draw, num, fn))//2, y+18), num,
                  font=fn, fill=col(RED, p))
        # Label
        fl = font(26)
        draw.text((x + (card_w - tw(draw, lbl, fl))//2, y+105), lbl,
                  font=fl, fill=col(GOLD, p))
        # Sub
        fs = font(19, bold=False)
        draw.text((x + (card_w - tw(draw, sub, fs))//2, y+148), sub,
                  font=fs, fill=col(MGR, p))

    # Pyramid F3→F2→F1
    pyr_p = ease_out(min(1, max(0, (t - 2.2) / 1.2)))
    if pyr_p > 0:
        cy = 650
        for lbl, half_w, c in [("F1",80,RED),("F2",140,GOLD),("F3",200,(90,90,90))]:
            draw.rectangle([W//2-half_w, cy-22, W//2+half_w, cy+22],
                           fill=col(c, pyr_p))
            fw = font(26)
            draw.text((W//2 - tw(draw,lbl,fw)//2, cy-11), lbl, font=fw,
                      fill=col(WHT, pyr_p))
            cy += 58
        fp = font(19, bold=False)
        draw.text((W//2+215, 648), "← Pyramide FIA", font=fp,
                  fill=col(MGR, pyr_p))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 03  LE PROBLÈME ────────────────────────────────────────────────────
def scene_03(t, duration=13.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "LE PROBLÈME")
    divider_line(draw, 130, 0.22)

    problems = [
        ("✗ TÉLÉMÉTRIE\nSOUS-EXPLOITÉE",  "1200+ pts/sec\nnon analysés en RT"),
        ("✗ SCOUTING\nÀ L'INSTINCT",      "Aucun modèle\nprédictif pilotes"),
        ("✗ REVENUS\nFIGÉS",              "Pricing statique\nopportunités data manquées"),
        ("✗ FAN ENGAGEMENT\nGÉNÉRIQUE",   "Contenu non perso\n445M fans sous-exploités"),
    ]
    card_w, card_h = 412, 320
    gap = 24
    total_w = 4*card_w + 3*gap
    sx = (W - total_w) // 2

    for i, (head, body) in enumerate(problems):
        delay = i * 0.48
        p = ease_out(min(1, max(0, (t - delay) / 0.55)))
        if p <= 0:
            continue
        x = sx + i*(card_w+gap)
        y = int(190 + 45*(1-p))
        draw.rounded_rectangle([x, y, x+card_w, y+card_h], radius=12,
                                fill=(28,6,6))
        draw.rectangle([x, y, x+card_w, y+4], fill=(int(200*p),0,0))
        fh = font(28)
        cy = y+22
        for ln in head.split('\n'):
            draw.text((x+18, cy), ln, font=fh, fill=col(RED, p))
            cy += 38
        fb = font(22, bold=False)
        cy = y+140
        for ln in body.split('\n'):
            draw.text((x+18, cy), ln, font=fb, fill=col(MGR, p))
            cy += 34

    # Cost callout
    cp = ease_out(min(1, max(0, (t - 2.8) / 0.9)))
    if cp > 0:
        msg = "▶  +30% de valeur perdue chaque saison faute d'analyse IA"
        fm = font(26)
        draw.text(((W - tw(draw,msg,fm))//2, 625), msg, font=fm, fill=col(GOLD, cp))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 04  L'OPPORTUNITÉ ──────────────────────────────────────────────────
def scene_04(t, duration=12.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "L'OPPORTUNITÉ")
    divider_line(draw, 130, 0.24)

    big_stats = [
        ("1200", "pts/sec", "de télémétrie\nnon exploitée", RED),
        ("+22%",  "",       "croissance annuelle\ndu marché IA Sport", GOLD),
        ("20/22", "",       "pilotes F1 issus\nde programmes IA", WHT),
    ]
    xs = [320, 960, 1600]

    for i, (val, unit, desc, color) in enumerate(big_stats):
        delay = i * 0.42
        p = ease_out(min(1, max(0, (t - delay) / 0.75)))
        if p <= 0:
            continue
        cx = xs[i]
        fn = font(86)
        draw.text((cx - tw(draw,val,fn)//2, 190), val, font=fn, fill=col(color, p))
        if unit:
            fu = font(32, bold=False)
            draw.text((cx - tw(draw,unit,fu)//2, 295), unit, font=fu, fill=col(GOLD, p))
        fd = font(23, bold=False)
        cy = 345
        for ln in desc.split('\n'):
            draw.text((cx - tw(draw,ln,fd)//2, cy), ln, font=fd, fill=col(MGR, p))
            cy += 32

    # Divider
    if t > 1.6:
        draw.line([(80, 490), (W-80, 490)], fill=(50,50,50), width=2)

    bullets = [
        "◆  Marché IA Sport estimé à 8,4 Md$ d'ici 2028 (CAGR +22%)",
        "◆  FIA — données exclusives sur 143 championnats dans 150 pays",
        "◆  Équipes F1 investissent déjà 200M$+ / an en analyse de performance",
        "◆  Fenêtre idéale avant le prochain cycle réglementaire FIA",
    ]
    for i, b in enumerate(bullets):
        delay = 1.9 + i*0.32
        bp = ease_out(min(1, max(0, (t - delay) / 0.45)))
        if bp <= 0:
            continue
        fb = font(26, bold=False)
        y = 525 + i*68
        sx = int(80 + 40*(1-bp))
        draw.text((sx, y), b, font=fb, fill=col((210,210,210), bp))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 05  FIA DATAHUB ────────────────────────────────────────────────────
def scene_05(t, duration=13.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "NOTRE SOLUTION — FIA DATAHUB", f_size=46)
    divider_line(draw, 130, 0.42)

    cx, cy = W//2, 560
    pulse = 1.0 + 0.04 * math.sin(t * 2.8)

    # Center node
    cf = ease_out(min(1, t / 0.8))
    if cf > 0:
        for ring in range(4):
            rr = int((100 + ring*18) * pulse)
            a = int(30*(1-ring/4)*cf)
            draw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=(a//2,0,0))
        draw.ellipse([cx-95, cy-95, cx+95, cy+95],
                     fill=(int(70*cf),0,0), outline=col(RED, cf), width=3)
        fh = font(28)
        draw.text((cx - tw(draw,"◆ FIA ◆",fh)//2, cy-24), "◆ FIA ◆",
                  font=fh, fill=col(RED, cf))
        fdb = font(22)
        draw.text((cx - tw(draw,"DATAHUB",fdb)//2, cy+10), "DATAHUB",
                  font=fdb, fill=col(WHT, cf))

    # Orbiting modules
    modules = [
        ("EXCELLENCE\nSPORTIVE",   0,   RED),
        ("OPTIMISATION\nREVENUS",   1,  GOLD),
        ("FAN\nENGAGEMENT",         2, (100,200,255)),
        ("SCOUTING\nPILOTES",       3, (100,255,150)),
    ]
    orbit_r = 290

    for label, idx, color in modules:
        delay = 0.5 + idx * 0.38
        mf = ease_out(min(1, max(0, (t - delay) / 0.55)))
        if mf <= 0:
            continue
        angle = -math.pi/2 + idx * math.pi/2
        mx = cx + int(orbit_r * math.cos(angle))
        my = cy + int(orbit_r * math.sin(angle))

        # Connector
        lx = cx + int((mx-cx)*mf)
        ly = cy + int((my-cy)*mf)
        draw.line([(cx,cy),(lx,ly)], fill=col(color, mf*0.5), width=2)

        # Box
        bw, bh = 196, 88
        draw.rounded_rectangle([mx-bw//2, my-bh//2, mx+bw//2, my+bh//2],
                                radius=10, fill=(30,30,30))
        draw.rectangle([mx-bw//2, my-bh//2, mx+bw//2, my-bh//2+3],
                       fill=col(color, mf))
        fm = font(20)
        cy2 = my - 20
        for ln in label.split('\n'):
            draw.text((mx - tw(draw,ln,fm)//2, cy2), ln, font=fm, fill=col(WHT, mf))
            cy2 += 26

    bottom_bar(draw)
    return img_to_array(img)


# ─── PILLAR HELPER ────────────────────────────────────────────────────────────
def _pillar_scene(t, title, accent_color, bullets_left, stat1_text, stat1_label,
                  stat1_note, stat2_text, stat2_label, stat2_note):
    img, draw = new_frame()
    top_bar(draw, t)
    ft = font(44)
    draw.text((80, 58), title, font=ft, fill=WHT)
    tlen = tw(draw, title, ft)
    draw.rectangle([80, 128, 80+tlen, 132], fill=accent_color)

    # Left bullets
    fb = font(25, bold=False)
    for i, b in enumerate(bullets_left):
        delay = i * 0.28
        p = ease_out(min(1, max(0, (t - delay) / 0.48)))
        if p <= 0:
            continue
        y = 195 + i*68
        draw.text((int(80 + 30*(1-p)), y), b, font=fb, fill=col((215,215,215), p))

    # Divider
    if t > 1.4:
        draw.line([(975,155),(975,H-80)], fill=(50,50,50), width=2)

    # Right stats
    rx = 1040
    # Stat 1
    p1 = ease_out(min(1, max(0, (t - 1.7) / 0.8)))
    if p1 > 0:
        fst = font(74)
        draw.text((rx, 195), stat1_text, font=fst, fill=col(RED, p1))
        fl = font(24, bold=False)
        draw.text((rx, 295), stat1_label, font=fl, fill=col((175,175,175), p1))
        fn2 = font(19, bold=False)
        draw.text((rx, 335), stat1_note, font=fn2, fill=col(MGR, p1))

    # Stat 2
    p2 = ease_out(min(1, max(0, (t - 2.5) / 0.8)))
    if p2 > 0:
        fst2 = font(74)
        draw.text((rx, 480), stat2_text, font=fst2, fill=col(GOLD, p2))
        fl2 = font(24, bold=False)
        draw.text((rx, 580), stat2_label, font=fl2, fill=col((175,175,175), p2))
        fn3 = font(19, bold=False)
        draw.text((rx, 618), stat2_note, font=fn3, fill=col(MGR, p2))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 06  PILIER 1 ───────────────────────────────────────────────────────
def scene_06(t, duration=12.0):
    val = count_up(1.8, max(0, t-2.5))
    return _pillar_scene(t,
        "PILIER 1 — EXCELLENCE SPORTIVE", RED,
        ["● Analyse temps réel de la télémétrie",
         "● Modèles prédictifs de performance",
         "● Détection d'anomalies mécaniques",
         "● Optimisation stratégie pit stop",
         "● Simulation scénarios de course"],
        "-23%",   "réduction des DNF",          "PoC en conditions réelles",
        f"+{val:.1f}s", "gain moyen par tour",  "sur simulation stratégie pit")


# ─── SCENE 07  PILIER 2 ───────────────────────────────────────────────────────
def scene_07(t, duration=10.0):
    val = count_up(18, max(0, t-1.7))
    return _pillar_scene(t,
        "PILIER 2 — OPTIMISATION DES REVENUS", GOLD,
        ["● Pricing dynamique des droits data",
         "● Analyse valeur sponsor en temps réel",
         "● Matching automatisé sponsors/équipes",
         "● Prévision ROI campagnes marketing",
         "● Détection opportunités partenariats"],
        f"+{val:.0f}%", "revenus sponsoring",   "estimation sur accords pilotes",
        "x3",           "valeur droits data",    "projection sur 3 ans")


# ─── SCENE 08  PILIER 3 ───────────────────────────────────────────────────────
def scene_08(t, duration=10.0):
    val = count_up(25, max(0, t-1.7))
    return _pillar_scene(t,
        "PILIER 3 — FAN ENGAGEMENT", (100,200,255),
        ["● Contenu personnalisé par profil fan",
         "● Statistiques live enrichies",
         "● Prédictions de course interactives",
         "● Push notifications intelligentes",
         "● Gamification et challenges IA"],
        f"+{val:.0f}%", "engagement fan",       "vs expérience générique",
        "x4",           "croissance F1 TV",      "abonnés sur 5 ans (benchmark)")


# ─── SCENE 09  PILIER 4 ───────────────────────────────────────────────────────
def scene_09(t, duration=10.0):
    val = count_up(40, max(0, t-2.5))
    return _pillar_scene(t,
        "PILIER 4 — SCOUTING PILOTES", (100,255,150),
        ["● Analyse 500+ métriques par pilote",
         "● Comparaison cross-championnats IA",
         "● Score de potentiel F1 (0-100)",
         "● Détection précoce des talents juniors",
         "● Rapport recrutement automatisé"],
        "20/22", "pilotes F1 identifiés",       "rétro-test cohorte 2020-2023",
        f"-{val:.0f}%", "risque recrutement",   "vs méthodes traditionnelles")


# ─── SCENE 10  ARCHITECTURE ───────────────────────────────────────────────────
def scene_10(t, duration=10.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "ARCHITECTURE PLATEFORME")
    divider_line(draw, 130, 0.36)

    steps = [
        ("COLLECTE",       RED,            ["Télémétrie F1-F3","GPS & capteurs","APIs externes"]),
        ("TRAITEMENT IA",  GOLD,           ["ML Pipeline","NLP Reports","Prédictions RT"]),
        ("DASHBOARD",      (100,200,255),  ["Équipes sportives","Management FIA","Sponsors & médias"]),
        ("DÉCISION",       (100,255,150),  ["Actions auto","Alertes smart","Rapports strat."]),
    ]
    sw = 380; gap = 40
    total = 4*sw + 3*gap
    sx = (W - total) // 2

    for i, (title, color, subs) in enumerate(steps):
        delay = i * 0.48
        p = ease_out(min(1, max(0, (t - delay) / 0.55)))
        if p <= 0:
            continue
        x = sx + i*(sw+gap)
        y = 230

        # Arrow
        if i > 0:
            ap = ease_out(min(1, max(0, (t - delay + 0.15) / 0.25)))
            fa = font(34)
            draw.text((x-gap+2, y+56), "▶", font=fa, fill=col(RED, ap))

        draw.rounded_rectangle([x, y, x+sw, y+185], radius=12, fill=(24,24,24))
        draw.rectangle([x, y, x+sw, y+5], fill=col(color, p))

        # Step number
        fn = font(26, bold=False)
        draw.text((x+14, y+12), f"0{i+1}", font=fn, fill=col(color, p*0.6))

        # Title
        ftt = font(28)
        draw.text((x + (sw - tw(draw,title,ftt))//2, y+52), title,
                  font=ftt, fill=col(WHT, p))

        # Sub-items
        fs = font(19, bold=False)
        for j, sub in enumerate(subs):
            sd = delay + 0.28 + j*0.18
            sp = ease_out(min(1, max(0, (t - sd) / 0.35)))
            if sp > 0:
                draw.text((x + (sw - tw(draw,sub,fs))//2, y+108+j*28), sub,
                          font=fs, fill=col((155,155,155), sp))

    # Stack info
    dp = ease_out(min(1, max(0, (t - 3.0) / 0.9)))
    if dp > 0:
        fd = font(22, bold=False)
        draw_centered(draw, "Stack : Python / TensorFlow / Kafka / PostgreSQL / React.js",
                      605, fd, col((140,140,140), dp))
        draw_centered(draw, "Infrastructure cloud AWS — failover automatique — SLA 99.9%",
                      645, font(20, bold=False), col((100,100,100), dp))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 11  MARCHÉ ─────────────────────────────────────────────────────────
def scene_11(t, duration=10.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "MARCHÉ ADRESSABLE")
    divider_line(draw, 130, 0.28)

    circles = [
        ("TAM", "8,4 Md$", "Marché Total\nIA Sport mondial", WHT,  158),
        ("SAM", "1,2 Md$", "Marché Accessible\nFIA + Partenaires", GOLD, 118),
        ("SOM", "45 M€",   "Objectif Année 1-3\nFIA DATAHUB",      RED,   80),
    ]
    pxs = [390, 960, 1530]

    for i, (lbl, val, desc, color, max_r) in enumerate(circles):
        delay = i * 0.48
        p = ease_out(min(1, max(0, (t - delay) / 1.0)))
        r = int(max_r * p)
        if r <= 0:
            continue
        cx = pxs[i]; cy = 400
        draw.ellipse([cx-r, cy-r, cx+r, cy+r],
                     fill=col(color, p*0.25), outline=col(color, p), width=3)
        fl = font(28)
        draw.text((cx - tw(draw,lbl,fl)//2, cy-28), lbl, font=fl, fill=col(color, p))
        fv = font(40)
        draw.text((cx - tw(draw,val,fv)//2, cy+8), val, font=fv, fill=col(WHT, p))
        fd = font(19, bold=False)
        cy2 = cy + max_r + 18
        for ln in desc.split('\n'):
            draw.text((cx - tw(draw,ln,fd)//2, cy2), ln, font=fd, fill=col(MGR, p))
            cy2 += 27

    # Phases
    phases = [("PHASE 1","F3 + académies","M1-M12"),
              ("PHASE 2","Premium FIA","M13-M24"),
              ("PHASE 3","Global","M25-M36")]
    road_y = 715; total_w = 1380; ssl = (W-total_w)//2; pw = total_w//3

    if t > 2.4:
        draw.line([(ssl, road_y+18),(ssl+total_w, road_y+18)], fill=(50,50,50), width=3)
        for i,(pht,phs,phm) in enumerate(phases):
            delay = 2.4 + i*0.38
            pp = ease_out(min(1, max(0, (t - delay) / 0.45)))
            if pp <= 0:
                continue
            px = ssl + i*pw + pw//2
            draw.ellipse([px-12, road_y+6, px+12, road_y+30], fill=col(RED, pp))
            fp1 = font(22)
            draw.text((px - tw(draw,pht,fp1)//2, road_y+40), pht,
                      font=fp1, fill=col(GOLD, pp))
            fp2 = font(18, bold=False)
            draw.text((px - tw(draw,phs,fp2)//2, road_y+70), phs,
                      font=fp2, fill=col((175,175,175), pp))
            draw.text((px - tw(draw,phm,fp2)//2, road_y+96), phm,
                      font=fp2, fill=col(MGR, pp))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 12  CONCURRENTIEL ──────────────────────────────────────────────────
def scene_12(t, duration=10.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "ANALYSE CONCURRENTIELLE")
    divider_line(draw, 130, 0.34)

    headers = ["SOLUTION","TEMPS RÉEL","MULTI-SPORT","SCOUTING IA","TARIF","INTÉGR. FIA"]
    col_w   = [310, 150, 155, 150, 155, 190]
    sx = (W - sum(col_w)) // 2
    hy = 180

    fh = font(23)
    x = sx
    for j,h in enumerate(headers):
        draw.text((x + (col_w[j]-tw(draw,h,fh))//2, hy), h, font=fh, fill=GOLD)
        x += col_w[j]
    draw.line([(sx, hy+40),(sx+sum(col_w), hy+40)], fill=(55,55,55), width=2)

    rows = [
        ("McLaren Applied", "✓","✗","✗","500k€+","✗"),
        ("AWS F1",          "✓","✗","✗","Custom","✗"),
        ("Catapult Sports", "✓","✓","✗","300k€+","✗"),
        ("◆ Notre Solution","✓","✓","✓","60-180k€","✓ NATIF"),
    ]
    row_h = 90

    for i,row in enumerate(rows):
        delay = 0.3 + i*0.38
        rp = ease_out(min(1, max(0, (t - delay) / 0.48)))
        if rp <= 0:
            continue
        y = hy + 50 + i*row_h
        is_us = (i == 3)
        if is_us:
            draw.rounded_rectangle([sx-8, y-4, sx+sum(col_w)+8, y+row_h-8],
                                    radius=8, fill=(40,10,10))
            draw.rectangle([sx-8, y-4, sx-2, y+row_h-8], fill=RED)

        x = sx
        for j,cell in enumerate(row):
            c = WHT
            if cell == "✓":      c = (100,255,100)
            elif cell == "✗":    c = (255,80,80)
            elif is_us and j==0: c = RED
            fc = font(21, bold=is_us)
            draw.text((x + (col_w[j]-tw(draw,cell,fc))//2, y+22),
                      cell, font=fc, fill=col(c, rp))
            x += col_w[j]

    lp = ease_out(min(1, max(0, (t - 2.6) / 0.7)))
    if lp > 0:
        fl = font(22, bold=False)
        msg = "◆  Avantage concurrentiel durable : seule solution conçue nativement pour l'écosystème FIA"
        draw.text(((W-tw(draw,msg,fl))//2, 850), msg, font=fl, fill=col(GOLD, lp))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 13  MODÈLE ÉCONOMIQUE ─────────────────────────────────────────────
def scene_13(t, duration=10.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "MODÈLE ÉCONOMIQUE")
    divider_line(draw, 130, 0.28)

    packages = [
        ("PERFORMANCE", "180k€", RED,          ["Télémétrie temps réel","Prédictions course","Dashboard équipes"]),
        ("SCOUTING",    "95k€",  GOLD,          ["Score pilotes IA","Rapports auto","Base juniors"]),
        ("REVENUS",     "120k€", (100,200,255), ["Pricing dynamique","Matching sponsors","Analytics ROI"]),
        ("FAN",         "60k€",  (100,255,150), ["Perso contenu","API mobile","Gamification"]),
    ]
    cw = 386; gap = 30
    total = 4*cw + 3*gap; sx = (W-total)//2

    for i,(name,price,color,items) in enumerate(packages):
        delay = i*0.32
        p = ease_out(min(1, max(0, (t-delay)/0.55)))
        if p <= 0:
            continue
        x = sx + i*(cw+gap)
        y = int(190 + 85*(1-p))
        draw.rounded_rectangle([x, y, x+cw, y+420], radius=12, fill=(20,20,20))
        draw.rectangle([x, y, x+cw, y+5], fill=col(color, p))

        fn = font(26)
        draw.text((x+(cw-tw(draw,name,fn))//2, y+18), name, font=fn, fill=col(color,p))
        fp = font(44)
        draw.text((x+(cw-tw(draw,price,fp))//2, y+68), price, font=fp, fill=col(WHT,p))
        fy = font(18, bold=False)
        draw.text((x+(cw-tw(draw,"/ an",fy))//2, y+128), "/ an", font=fy,
                  fill=col(MGR, p))

        fi = font(21, bold=False)
        for j,item in enumerate(items):
            id2 = delay + 0.28 + j*0.14
            ip = ease_out(min(1, max(0, (t-id2)/0.28)))
            if ip > 0:
                draw.text((x+18, y+175+j*52), f"✓  {item}", font=fi,
                          fill=col((175,175,175), ip))

    # Footer
    fp2 = ease_out(min(1, max(0, (t-2.6)/0.8)))
    if fp2 > 0:
        draw.line([(80,700),(W-80,700)], fill=(45,45,45), width=1)
        ff = font(23, bold=False)
        draw.text((80,718), "◆  Revenue Share : 2% sur contrats sponsoring générés", font=ff,
                  fill=col(GOLD, fp2))
        draw.text((80,756), "◆  Data Licensing : 50 – 200k€ / an selon volume et usage", font=ff,
                  fill=col((175,175,175), fp2))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 14  GO-TO-MARKET ───────────────────────────────────────────────────
def scene_14(t, duration=8.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "GO-TO-MARKET")
    divider_line(draw, 130, 0.22)

    phases = [
        ("PHASE 1","M1 — M12","Pilote F3",       RED,
         ["MVP télémétrie lancé","3-5 équipes F3","Validation KPIs","Objectif : 420k€ ARR"]),
        ("PHASE 2","M13 — M24","Premium FIA",     GOLD,
         ["Scouting + Revenus","Intégr. FIA officielle","8-12 championnats","Objectif : 1,8M€ ARR"]),
        ("PHASE 3","M25 — M36","Expansion Globale",(100,255,150),
         ["Fan Engagement lancé","143 championnats","Partenariats médias","Objectif : 4,2M€ ARR"]),
    ]
    pw = 500; gap = 55; total = 3*pw+2*gap; sx = (W-total)//2
    tl_y = 330

    if t > 0.3:
        tp = ease_out(min(1,(t-0.3)/0.5))
        draw.line([(sx,tl_y),(int(sx+total*tp),tl_y)], fill=(55,55,55), width=4)

    for i,(phn,pht,phs,color,items) in enumerate(phases):
        delay = 0.5 + i*0.48
        p = ease_out(min(1, max(0, (t-delay)/0.55)))
        if p <= 0:
            continue
        x = sx + i*(pw+gap)
        dot_x = x + pw//2

        draw.ellipse([dot_x-14,tl_y-14,dot_x+14,tl_y+14], fill=col(color,p))

        fp = font(30)
        draw.text((dot_x-tw(draw,phn,fp)//2, tl_y+26), phn, font=fp, fill=col(color,p))
        ft = font(20, bold=False)
        draw.text((dot_x-tw(draw,pht,ft)//2, tl_y+68), pht, font=ft,
                  fill=col((175,175,175),p))
        fs = font(24)
        draw.text((dot_x-tw(draw,phs,fs)//2, tl_y+100), phs, font=fs, fill=col(WHT,p))

        fi = font(21, bold=False)
        for j,item in enumerate(items):
            id2 = delay + 0.28 + j*0.14
            ip = ease_out(min(1, max(0,(t-id2)/0.28)))
            if ip > 0:
                draw.text((x+18, 465+j*52), f"▶  {item}", font=fi,
                          fill=col((175,175,175),ip))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 15  TRACTION ───────────────────────────────────────────────────────
def scene_15(t, duration=8.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "TRACTION & PREUVES")
    divider_line(draw, 130, 0.28)

    pocs = [
        ("-23%",   "DNF réduits",      "PoC équipe F3\n(simulation)",        RED),
        ("9/10",   "pilotes prédits",  "Rétro-test\ncohorte 2020-2023",       GOLD),
        ("+18%",   "sponsoring",       "Étude cas\nGP de Monaco",            (100,200,255)),
        ("2",      "écuries en\ndiscussion","Contrats\npré-signés",           (100,255,150)),
    ]
    cw = 390; gap = 28; total = 4*cw+3*gap; sx = (W-total)//2

    for i,(num,lbl,sub,color) in enumerate(pocs):
        delay = i*0.38
        p = ease_out(min(1, max(0, (t-delay)/0.65)))
        if p <= 0:
            continue
        x = sx+i*(cw+gap); y = 215
        draw.rounded_rectangle([x,y,x+cw,y+360], radius=12, fill=(20,20,20))
        draw.rectangle([x,y,x+cw,y+5], fill=col(color,p))

        fn = font(64)
        draw.text((x+(cw-tw(draw,num,fn))//2, y+28), num, font=fn, fill=col(color,p))

        fl = font(26)
        cy2 = y+115
        for ln in lbl.split('\n'):
            draw.text((x+(cw-tw(draw,ln,fl))//2, cy2), ln, font=fl, fill=col(WHT,p))
            cy2 += 34

        fs = font(20, bold=False)
        cy3 = y+195
        for ln in sub.split('\n'):
            draw.text((x+(cw-tw(draw,ln,fs))//2, cy3), ln, font=fs, fill=col(MGR,p))
            cy3 += 28

        # Pulse dot
        pulse = 0.5 + 0.5*math.sin(t*3.5 + i*math.pi/2)
        dr = int(5+3*pulse)
        draw.ellipse([x+cw//2-dr,y+300-dr,x+cw//2+dr,y+300+dr],
                     fill=col(color, p*0.85))

    vp = ease_out(min(1, max(0, (t-2.6)/0.8)))
    if vp > 0:
        msg = "✓  Résultats validés en conditions réelles — données disponibles sur demande"
        fv = font(24, bold=False)
        draw.text(((W-tw(draw,msg,fv))//2, 700), msg, font=fv, fill=col(GOLD,vp))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 16  PROJECTIONS ────────────────────────────────────────────────────
def scene_16(t, duration=8.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "PROJECTIONS FINANCIÈRES")
    divider_line(draw, 130, 0.32)

    revenues = [420_000, 1_800_000, 4_200_000]
    costs    = [350_000, 1_100_000, 1_400_000]
    years    = ["AN 1", "AN 2", "AN 3"]

    cl = 120; cr = 1100; cb = 780; ct = 210
    ch = cb - ct; cw_chart = cr - cl
    max_v = 4_600_000
    bar_w = 110

    # Axes
    ap = ease_out(min(1, t/0.4))
    if ap > 0:
        draw.line([(cl,ct),(cl,cb)], fill=(70,70,70), width=2)
        draw.line([(cl,cb),(cr,cb)], fill=(70,70,70), width=2)
        fs = font(18, bold=False)
        for v,lbl in [(0,"0"),(1e6,"1M€"),(2e6,"2M€"),(3e6,"3M€"),(4e6,"4M€")]:
            y = cb - int(v/max_v*ch)
            draw.line([(cl,y),(cr,y)], fill=(28,28,28), width=1)
            draw.text((cl - tw(draw,lbl,fs) - 8, y-9), lbl, font=fs,
                      fill=col((110,110,110),ap))

    # Bars
    for i,(rev,cost,year) in enumerate(zip(revenues,costs,years)):
        delay = 0.45 + i*0.38
        bp = ease_out(min(1, max(0, (t-delay)/0.75)))
        if bp <= 0:
            continue
        gx = cl + 80 + i*300

        rh = int(rev/max_v*ch*bp)
        draw.rounded_rectangle([gx, cb-rh, gx+bar_w, cb], radius=4, fill=GOLD)

        ch2 = int(cost/max_v*ch*bp)
        draw.rounded_rectangle([gx+bar_w+12, cb-ch2, gx+bar_w*2+12, cb],
                                radius=4, fill=RED)

        fy = font(22, bold=False)
        draw.text((gx + bar_w - tw(draw,year,fy)//2 + 6, cb+10), year,
                  font=fy, fill=col((195,195,195),bp))

        if bp > 0.4:
            fs2 = font(18, bold=False)
            rev_s = f"{int(rev*bp/1000)}k€"
            draw.text((gx + (bar_w-tw(draw,rev_s,fs2))//2, cb-rh-22), rev_s,
                      font=fs2, fill=GOLD)

    # Legend
    leg_x = cr + 45
    fl = font(20, bold=False)
    draw.rectangle([leg_x, ct+45, leg_x+18, ct+63], fill=GOLD)
    draw.text((leg_x+26, ct+47), "Revenus", font=fl, fill=(190,190,190))
    draw.rectangle([leg_x, ct+82, leg_x+18, ct+100], fill=RED)
    draw.text((leg_x+26, ct+84), "Coûts",   font=fl, fill=(190,190,190))

    # Metrics
    metrics = [("Break-even","18 mois",RED),("ARR An3","4,2M€",GOLD),("Marge nette","68%",(100,255,150))]
    for i,(lbl,val,color) in enumerate(metrics):
        mp = ease_out(min(1, max(0,(t-2.0-i*0.28)/0.45)))
        if mp > 0:
            y = 400 + i*128
            fml = font(20, bold=False)
            draw.text((leg_x, y), lbl, font=fml, fill=col((165,165,165),mp))
            fmv = font(34)
            draw.text((leg_x, y+28), val, font=fmv, fill=col(color,mp))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 17  L'ÉQUIPE ───────────────────────────────────────────────────────
def scene_17(t, duration=6.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "L'ÉQUIPE")
    divider_line(draw, 130, 0.16)

    team = [
        ("CEO",              "Colin Toum",       "Stratégie & Vision\nEx-FIA consultant\nHEC Paris",          RED),
        ("CTO",              "Matthieu Dambrin",  "Architecture IA\nML Engineer ex-AWS\nÉcole Polytechnique", GOLD),
        ("HEAD OF SALES",    "Sophie Laurent",   "Business Dev\n8 ans sport auto\nFIA Network",             (100,200,255)),
        ("ING. TÉLÉMÉTRIE",  "Marc Dubois",      "Data Engineering\nEx-Ferrari F1\n15 ans expérience",       (100,255,150)),
    ]
    cw = 398; gap = 28; total = 4*cw+3*gap; sx = (W-total)//2

    for i,(role,name,skills,color) in enumerate(team):
        delay = i*0.32
        p = ease_out(min(1, max(0, (t-delay)/0.55)))
        if p <= 0:
            continue
        x = sx+i*(cw+gap); y = 218
        draw.rounded_rectangle([x,y,x+cw,y+420], radius=12, fill=(20,20,20))
        draw.rectangle([x,y,x+cw,y+5], fill=col(color,p))

        # Avatar
        ax = x+cw//2; ay = y+88; ar = 52
        draw.ellipse([ax-ar,ay-ar,ax+ar,ay+ar], fill=col(color,p*0.35),
                     outline=col(color,p), width=3)
        initials = "".join(w[0] for w in name.split())
        fi = font(30)
        draw.text((ax-tw(draw,initials,fi)//2, ay-15), initials, font=fi,
                  fill=col(WHT,p))

        fr = font(22)
        draw.text((x+(cw-tw(draw,role,fr))//2, y+155), role, font=fr,
                  fill=col(color,p))
        fn2 = font(21, bold=False)
        draw.text((x+(cw-tw(draw,name,fn2))//2, y+194), name, font=fn2,
                  fill=col(WHT,p))

        fs = font(19, bold=False)
        cy2 = y+248
        for ln in skills.split('\n'):
            draw.text((x+(cw-tw(draw,ln,fs))//2, cy2), ln, font=fs,
                      fill=col((155,155,155),p))
            cy2 += 36

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 18  ROADMAP 36 MOIS ────────────────────────────────────────────────
def scene_18(t, duration=6.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "ROADMAP 36 MOIS")
    divider_line(draw, 130, 0.26)

    milestones = [
        ("M3",  "MVP\nPlateforme",   RED),
        ("M6",  "Pilote F3\nLancé",  GOLD),
        ("M9",  "Premiers\nContrats",(100,200,255)),
        ("M12", "Break-even\nAtteint",(100,255,150)),
        ("M18", "F2\nIntégration",   RED),
        ("M24", "FIA Officiel\nPartner",GOLD),
        ("M30", "Fan App\nLancée",   (100,200,255)),
        ("M36", "143\nChamp.",       (100,255,150)),
    ]
    tl_y = 500; tl_sx = 100; tl_ex = W-100; tl_len = tl_ex - tl_sx

    tp = ease_out(min(1, t/0.9))
    draw.line([(tl_sx,tl_y),(int(tl_sx+tl_len*tp),tl_y)], fill=(55,55,55), width=4)

    n = len(milestones)
    for i,(month,desc,color) in enumerate(milestones):
        delay = 0.28 + i*0.28
        mp = ease_out(min(1, max(0,(t-delay)/0.38)))
        if mp <= 0:
            continue
        mx = tl_sx + int(tl_len*i/(n-1))

        draw.ellipse([mx-14,tl_y-14,mx+14,tl_y+14], fill=col(color,mp))

        fm = font(20)
        draw.text((mx-tw(draw,month,fm)//2, tl_y-56), month,
                  font=fm, fill=col(color,mp))

        desc_y = tl_y - 165 if i%2==0 else tl_y+42
        fd = font(17, bold=False)
        for j,ln in enumerate(desc.split('\n')):
            draw.text((mx-tw(draw,ln,fd)//2, desc_y+j*24), ln, font=fd,
                      fill=col((195,195,195),mp))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 19  FINANCEMENT ────────────────────────────────────────────────────
def scene_19(t, duration=6.0):
    img, draw = new_frame()
    top_bar(draw, t)
    scene_title(draw, "BESOIN DE FINANCEMENT")
    divider_line(draw, 130, 0.32)

    segs = [
        ("TECH IA",    45, RED),
        ("COMMERCIAL", 25, GOLD),
        ("TÉLÉMÉTRIE", 20, (100,200,255)),
        ("OPS",        10, (100,255,150)),
    ]
    cx, cy, r = 480, 540, 210
    cp = ease_out(min(1, t/1.4))

    if cp > 0:
        start = -90.0
        for lbl,pct,color in segs:
            sweep = pct/100*360*cp
            draw.pieslice([cx-r, cy-r, cx+r, cy+r],
                          start=start, end=start+sweep,
                          fill=col(color,0.65), outline=col(color,1.0), width=2)
            mid = math.radians(start + sweep/2)
            lx = cx + int(r*0.62*math.cos(mid))
            ly = cy + int(r*0.62*math.sin(mid))
            fp = font(22)
            draw.text((lx-tw(draw,f"{pct}%",fp)//2, ly-10),
                      f"{pct}%", font=fp, fill=WHT)
            start += sweep

    # Legend
    fl = font(21, bold=False)
    for i,(lbl,pct,color) in enumerate(segs):
        ly2 = cy - 60 + i*48
        draw.rounded_rectangle([130,ly2,150,ly2+20], radius=3, fill=color)
        draw.text((162,ly2+1), lbl, font=fl, fill=(195,195,195))

    # Right panel
    rx = 1040
    tp2 = ease_out(min(1, max(0,(t-1.0)/0.8)))
    if tp2 > 0:
        ft = font(70)
        draw.text((rx,195), "600 000 €", font=ft, fill=col(RED,tp2))
        fl2 = font(24, bold=False)
        draw.text((rx,295), "levée de fonds cible", font=fl2,
                  fill=col((170,170,170),tp2))

    goals = [
        ("◆","Contrat FIA signé en 12 mois",     GOLD),
        ("◆","ROI x5 sur horizon 3 ans",          (100,255,150)),
        ("◆","Équipe de 8 personnes recrutée",    (100,200,255)),
        ("◆","Break-even en 18 mois",              WHT),
    ]
    fg = font(22, bold=False)
    for i,(icon,text,color) in enumerate(goals):
        delay2 = 1.5 + i*0.28
        gp = ease_out(min(1, max(0,(t-delay2)/0.38)))
        if gp > 0:
            draw.text((rx, 405+i*65), f"{icon}  {text}", font=fg,
                      fill=col(color,gp))

    bottom_bar(draw)
    return img_to_array(img)


# ─── SCENE 20  OUTRO ──────────────────────────────────────────────────────────
def scene_20(t, duration=6.0):
    img, draw = new_frame()

    # Radial glow
    for ring in range(6):
        rr = int((180+ring*65)*(0.92+0.08*math.sin(t*2)))
        a = max(0,int(18*(1-ring/6)*ease_out(min(1,t/1.2))))
        if a > 0:
            draw.ellipse([W//2-rr, H//2-rr, W//2+rr, H//2+rr],
                         fill=(a//3, 0, 0))

    fade = ease_io(min(1, t/1.4))
    top_bar(draw, t, speed=0.8, thickness=8)

    f1 = font(78)
    f2 = font(78)
    draw_centered(draw, "LA COURSE VERS LA DATA", 295, f1, col(WHT, fade))
    draw_centered(draw, "COMMENCE ICI.", 388, f2, col(RED, fade))

    ulp = ease_out(min(1, max(0,(t-1.0)/0.8)))
    if ulp > 0:
        uw = int(720*ulp)
        draw.rectangle([(W-uw)//2, 500, (W+uw)//2, 505], fill=RED)

    cfade = ease_io(min(1, max(0,(t-1.5)/0.9)))
    if cfade > 0:
        contacts = "contact@fia-ia.fr  •  fia-ia.fr  •  Paris, France"
        fc = font(26, bold=False)
        draw_centered(draw, contacts, 568, fc, col((175,175,175),cfade))

    # CTA button
    bfade = ease_out(min(1, max(0,(t-2.0)/0.8)))
    if bfade > 0:
        btn = "Prendre contact →"
        bw2, bh2 = 368, 62
        bx = (W-bw2)//2; by2 = 670
        pulse = 1.0 + 0.018*math.sin(t*4)
        bw3 = int(bw2*pulse); bh3 = int(bh2*pulse)
        bx2 = (W-bw3)//2; by3 = by2+(bh2-bh3)//2
        draw.rounded_rectangle([bx2,by3,bx2+bw3,by3+bh3], radius=8,
                                fill=col(RED,bfade))
        fb = font(28)
        draw.text(((W-tw(draw,btn,fb))//2, by3+(bh3-th(draw,btn,fb))//2),
                  btn, font=fb, fill=col(WHT,bfade))

    afade = ease_out(min(1, max(0,(t-2.6)/0.8)))
    if afade > 0:
        auth = "Colin Toum & Matthieu Dambrin — Projet IA FIA 2024"
        fa = font(20, bold=False)
        draw_centered(draw, auth, 815, fa, col((95,95,95),afade))

    draw.rectangle([0, H-8, W, H], fill=RED)
    return img_to_array(img)


# ═══════════════════════════════════════════════════════════════════════════════
# THUMBNAIL EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_thumbnail(fn, filename, t=4.0, duration=12.0):
    arr = fn(t, duration=duration)
    img = Image.fromarray(arr)
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path, "PNG")
    print(f"  Thumbnail saved: {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("FIA IA DEMO VIDEO GENERATOR")
    print("=" * 60)

    scenes = [
        (scene_01, 12.0),
        (scene_02, 10.0),
        (scene_03, 13.0),
        (scene_04, 12.0),
        (scene_05, 13.0),
        (scene_06, 12.0),
        (scene_07, 10.0),
        (scene_08, 10.0),
        (scene_09, 10.0),
        (scene_10, 10.0),
        (scene_11, 10.0),
        (scene_12, 10.0),
        (scene_13, 10.0),
        (scene_14,  8.0),
        (scene_15,  8.0),
        (scene_16,  8.0),
        (scene_17,  6.0),
        (scene_18,  6.0),
        (scene_19,  6.0),
        (scene_20,  6.0),
    ]

    total = sum(d for _, d in scenes)
    print(f"Planned duration  : {total:.0f}s ({total/60:.1f} min)")
    print(f"Scenes            : {len(scenes)}")
    print(f"FPS               : {FPS}")
    print(f"Resolution        : {W}×{H}")

    # ── Thumbnails
    print("\n[1/4] Exporting thumbnails...")
    export_thumbnail(scene_01, "thumbnail_scene01_intro.png",    t=4.5, duration=12.0)
    export_thumbnail(scene_05, "thumbnail_scene05_datahub.png",  t=5.0, duration=13.0)
    export_thumbnail(scene_20, "thumbnail_scene20_outro.png",    t=3.2, duration=6.0)

    # ── Build clips
    print("\n[2/4] Building scene clips...")
    clips = []
    for i, (fn, dur) in enumerate(scenes):
        print(f"  Scene {i+1:02d}/{len(scenes)}: {fn.__name__} ({dur}s)", end=" ", flush=True)

        def make_frame(t, _fn=fn, _dur=dur):
            return _fn(t, duration=_dur)

        clip = VideoClip(make_frame, duration=dur)
        clips.append(clip)
        print("✓")

    # ── Audio
    print("\n[3/4] Generating audio track...")
    audio_arr, sr = generate_audio(duration=total + 4.0)
    audio_clip = AudioArrayClip(audio_arr, fps=sr)

    # ── Concatenate
    print("\n[4/4] Concatenating and encoding...")
    final_clips = []
    for i, clip in enumerate(clips):
        final_clips.append(clip)
        if i < len(clips) - 1:
            final_clips.append(make_transition(0.10))

    video = concatenate_videoclips(final_clips)
    actual_dur = video.duration
    print(f"  Final duration: {actual_dur:.1f}s")

    audio_clip = audio_clip.with_duration(min(actual_dur, audio_clip.duration))
    video = video.with_audio(audio_clip)

    out_path = os.path.join(OUTPUT_DIR, "FIA_IA_demo_video.mp4")
    video.write_videofile(
        out_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="5000k",
        logger="bar",
    )

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"\n{'='*60}")
    print(f"VIDEO SAVED:  {out_path}")
    print(f"Duration   :  {actual_dur:.1f}s")
    print(f"File size  :  {size_mb:.1f} MB")
    print(f"Thumbnails :  /output/thumbnail_scene0*.png")
    print("=" * 60)


if __name__ == "__main__":
    main()
