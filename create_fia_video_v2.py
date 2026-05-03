#!/usr/bin/env python3
"""
FIA IA — Cinematic Product Demo  v2  (real synthetic visuals)
"LA FIA À L'ÈRE DE L'INTELLIGENCE ARTIFICIELLE"
Colin Toum & Matthieu Dambrin
1920×1080 @ 30fps · 3 min · H.264/AAC
"""

import os, sys, math, wave, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
from scipy.ndimage import gaussian_filter

try:
    from moviepy import VideoClip, concatenate_videoclips, AudioFileClip
    MOVIEPY_OK = True
except Exception as e:
    MOVIEPY_OK = False

# ── Constants ────────────────────────────────────────────────────
W, H   = 1920, 1080
FPS    = 30
SD     = 9
NS     = 20

RED   = (232,   0,  13)
GOLD  = (201, 168,  76)
WHITE = (255, 255, 255)
GRAY  = (150, 150, 150)
DARK  = ( 14,  14,  22)

FONT_BOLD   = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_NORMAL = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'

_FONT_CACHE: dict = {}

def fnt(size: int, bold: bool = True):
    key = (size, bold)
    if key not in _FONT_CACHE:
        path = FONT_BOLD if bold else FONT_NORMAL
        try:   _FONT_CACHE[key] = ImageFont.truetype(path, size)
        except: _FONT_CACHE[key] = ImageFont.load_default()
    return _FONT_CACHE[key]

# ══════════════════════════════════════════════════════════════════
#  CINEMATIC BACKGROUND GENERATORS
# ══════════════════════════════════════════════════════════════════

def bg_speed_lines(color1=(80,0,0), color2=(20,0,5), accent=RED,
                   cx=None, cy=None, n_lines=220, blur=2.5):
    """Radial speed lines from vanishing point — classic F1 motion blur."""
    arr = np.zeros((H, W, 3), dtype=np.float32)
    if cx is None: cx = W * 0.55
    if cy is None: cy = H * 0.48
    rng = np.random.RandomState(42)
    img = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(img)
    # dark vignette base
    for y in range(H):
        t = abs(y/H - 0.5)*2
        r = int(color1[0]*(1-t*0.6)+color2[0]*t*0.6)
        g = int(color1[1]*(1-t*0.6)+color2[1]*t*0.6)
        b = int(color1[2]*(1-t*0.6)+color2[2]*t*0.6)
        d.line([(0,y),(W,y)], fill=(r,g,b))
    for _ in range(n_lines):
        angle = rng.uniform(0, 2*math.pi)
        length = rng.uniform(400, 1400)
        width  = rng.choice([1,1,1,2,2,3])
        alpha  = rng.uniform(0.06, 0.28)
        x2 = cx + math.cos(angle)*length
        y2 = cy + math.sin(angle)*length
        x1 = cx + math.cos(angle)*rng.uniform(0, 60)
        y1 = cy + math.sin(angle)*rng.uniform(0, 60)
        col = (int(accent[0]*alpha), int(accent[1]*alpha+80*alpha), int(accent[2]*alpha+30*alpha))
        d.line([(x1,y1),(x2,y2)], fill=col, width=width)
    arr = np.array(img).astype(np.float32)
    arr[:,:,0] = gaussian_filter(arr[:,:,0], sigma=blur)
    arr[:,:,1] = gaussian_filter(arr[:,:,1], sigma=blur)
    arr[:,:,2] = gaussian_filter(arr[:,:,2], sigma=blur)
    return np.clip(arr, 0, 255).astype(np.uint8)


def bg_bokeh(base_col=(5,5,25), light_cols=None, n=180, blur=22):
    """Bokeh light circles — stadium / night atmosphere."""
    if light_cols is None:
        light_cols = [RED, GOLD, WHITE, (255,140,0), (200,200,255)]
    arr = np.zeros((H, W, 3), dtype=np.float32)
    for y in range(H):
        t = y/H
        arr[y] = [base_col[0]*(1+t*0.4), base_col[1]*(1+t*0.4), base_col[2]*(1+t*0.4)]
    img = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    rng = np.random.RandomState(7)
    for _ in range(n):
        r   = rng.randint(20, 180)
        x   = rng.randint(0, W)
        y   = rng.randint(0, H)
        col = light_cols[rng.randint(0, len(light_cols))]
        alpha = rng.uniform(0.05, 0.35)
        fc = tuple(int(c*alpha) for c in col)
        d.ellipse([(x-r,y-r),(x+r,y+r)], fill=fc)
    arr = np.array(img).astype(np.float32)
    for c in range(3):
        arr[:,:,c] = gaussian_filter(arr[:,:,c], sigma=blur)
    # centre brightness
    yy, xx = np.mgrid[0:H, 0:W]
    vignette = np.exp(-((xx-W/2)**2/(W*0.6)**2 + (yy-H/2)**2/(H*0.6)**2))
    arr = arr * (0.5 + 0.5*vignette[:,:,None])
    return np.clip(arr, 0, 255).astype(np.uint8)


def bg_circuit(line_col=RED, bg_col=(8,8,18)):
    """Schematic F1 circuit track drawn with PIL — Spa-like layout."""
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    arr[:] = bg_col
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img)
    # draw track outline (simplified Spa-like circuit)
    scale = 1.7; ox, oy = 300, 140
    pts = [
        (200,400),(300,200),(500,150),(700,180),(820,300),
        (860,420),(900,350),(980,260),(1100,200),(1280,220),
        (1400,300),(1500,400),(1520,520),(1480,640),(1380,720),
        (1200,780),(1000,800),(800,780),(650,720),(520,680),
        (400,680),(300,640),(220,560),(200,480),(200,400),
    ]
    pts_s = [(int(x*scale*0.62+ox), int(y*scale*0.52+oy)) for x,y in pts]
    # glow layers
    for width, alpha in [(28,15),(18,30),(10,60),(5,120),(3,200)]:
        a_col = tuple(int(c*alpha/255) for c in line_col)
        d.line(pts_s+[pts_s[0]], fill=a_col, width=width, joint='curve')
    # grid dots
    for i in range(0, W, 80):
        for j in range(0, H, 80):
            d.point((i,j), fill=(30,30,50))
    arr = np.array(img).astype(np.float32)
    arr[:,:,0] = gaussian_filter(arr[:,:,0], sigma=1.5)
    arr[:,:,1] = gaussian_filter(arr[:,:,1], sigma=1.5)
    arr[:,:,2] = gaussian_filter(arr[:,:,2], sigma=1.5)
    return np.clip(arr, 0, 255).astype(np.uint8)


def bg_data_grid(base=(3,6,20), accent=(0,180,255), density=40):
    """Glowing data-grid / holographic HUD background."""
    arr = np.zeros((H, W, 3), dtype=np.float32)
    arr[:] = base
    img = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(img)
    # perspective grid lines
    vp_x, vp_y = W//2, H*2
    for i in range(-density, density+1, 2):
        x = W//2 + i*(W//density)
        d.line([(x, 0),(vp_x, vp_y)], fill=(accent[0]//8, accent[1]//8, accent[2]//8), width=1)
    for j in range(0, H, H//18):
        scale = 1 - j/H*0.6
        hw = int(W/2 * (1+scale))
        d.line([(W//2-hw, j),(W//2+hw, j)],
               fill=(accent[0]//6, accent[1]//6, accent[2]//6), width=1)
    # floating data nodes
    rng = np.random.RandomState(3)
    for _ in range(60):
        x, y = rng.randint(0,W), rng.randint(0,H)
        r = rng.randint(2, 8)
        a = rng.uniform(0.3, 0.9)
        c = tuple(int(c*a) for c in accent)
        d.ellipse([(x-r,y-r),(x+r,y+r)], fill=c)
        # connection lines
        for _ in range(rng.randint(1,3)):
            tx, ty = rng.randint(0,W), rng.randint(0,H)
            ca = tuple(int(c*0.12) for c in accent)
            d.line([(x,y),(tx,ty)], fill=ca, width=1)
    arr = np.array(img).astype(np.float32)
    for c in range(3):
        arr[:,:,c] = gaussian_filter(arr[:,:,c], sigma=1.2)
    # glow overlay
    yy, xx = np.mgrid[0:H, 0:W]
    glow = np.exp(-((xx-W//2)**2/(W*0.7)**2 + (yy-H*0.3)**2/(H*0.5)**2))*30
    arr[:,:,2] = np.clip(arr[:,:,2] + glow, 0, 255)
    return np.clip(arr, 0, 255).astype(np.uint8)


def bg_carbon_fiber(tint=RED):
    """Carbon fibre weave texture with tint — F1 car aesthetic."""
    arr = np.zeros((H, W, 3), dtype=np.float32)
    for y in range(H):
        for_x = np.arange(W)
        # diamond weave pattern
        val = (np.sin(for_x*0.18 + y*0.18)*np.cos(for_x*0.18 - y*0.18) + 1)*0.5
        bright = val * 28 + 8
        arr[y,:,0] = bright + tint[0]*0.08
        arr[y,:,1] = bright + tint[1]*0.08
        arr[y,:,2] = bright + tint[2]*0.08
    # radial vignette
    yy, xx = np.mgrid[0:H, 0:W]
    v = 1 - np.sqrt(((xx-W/2)/(W*0.6))**2 + ((yy-H/2)/(H*0.6))**2)
    v = np.clip(v, 0, 1)
    arr = arr * v[:,:,None] * 2.5
    arr[:,:,0] = gaussian_filter(arr[:,:,0], sigma=0.8)
    arr[:,:,1] = gaussian_filter(arr[:,:,1], sigma=0.8)
    arr[:,:,2] = gaussian_filter(arr[:,:,2], sigma=0.8)
    return np.clip(arr, 0, 255).astype(np.uint8)


def bg_light_trails(base=(4,4,14), n=120):
    """Neon light trails — night race / long exposure feel."""
    arr = np.zeros((H, W, 3), dtype=np.float32)
    arr[:] = base
    rng = np.random.RandomState(11)
    cols = [RED, GOLD, (255,255,200), (200,100,255), (0,200,255)]
    img = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    for _ in range(n):
        col  = cols[rng.randint(0,len(cols))]
        x0   = rng.randint(-200, W+200)
        y0   = rng.randint(0, H)
        length = rng.randint(200, 900)
        angle  = rng.uniform(-0.25, 0.25)  # mostly horizontal
        x1 = x0 + int(math.cos(angle)*length)
        y1 = y0 + int(math.sin(angle)*length)
        for w2, a in [(12,0.04),(6,0.09),(3,0.18),(1,0.55)]:
            c = tuple(int(c*a) for c in col)
            d.line([(x0,y0),(x1,y1)], fill=c, width=w2)
    arr = np.array(img).astype(np.float32)
    arr[:,:,0] = gaussian_filter(arr[:,:,0], sigma=1.8)
    arr[:,:,1] = gaussian_filter(arr[:,:,1], sigma=1.8)
    arr[:,:,2] = gaussian_filter(arr[:,:,2], sigma=1.8)
    yy, xx = np.mgrid[0:H, 0:W]
    v = np.exp(-((yy-H*0.5)/(H*0.55))**2) * 0.5 + 0.5
    arr = arr * v[:,:,None]
    return np.clip(arr, 0, 255).astype(np.uint8)


def bg_telemetry(base=(3,10,18)):
    """Scrolling telemetry data aesthetic — green matrix style."""
    arr = np.zeros((H, W, 3), dtype=np.float32)
    arr[:] = base
    rng = np.random.RandomState(22)
    img = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(img)
    # horizontal scan lines
    for y in range(0, H, 6):
        a = rng.uniform(0.02, 0.12)
        d.line([(0,y),(W,y)], fill=(0,int(60*a),int(30*a)))
    # vertical data columns (like oscilloscope)
    n_cols = 24
    for i in range(n_cols):
        x = i * (W // n_cols) + rng.randint(0, W//n_cols)
        prev_y = H//2
        for step in range(0, W//n_cols, 4):
            ny = H//2 + int(rng.randn()*120)
            ny = max(50, min(H-50, ny))
            col_a = rng.uniform(0.15, 0.55)
            c = (int(232*col_a*0.2), int(255*col_a), int(120*col_a))
            d.line([(x+step, prev_y),(x+step+4, ny)], fill=c, width=1)
            prev_y = ny
    # bright horizontal sweep lines
    for _ in range(8):
        y = rng.randint(100, H-100)
        for w2, a in [(4,0.06),(2,0.15),(1,0.4)]:
            d.line([(0,y),(W,y)], fill=(int(0*a),int(220*a),int(100*a)), width=w2)
    arr = np.array(img).astype(np.float32)
    arr[:,:,1] = gaussian_filter(arr[:,:,1], sigma=1.2)
    arr[:,:,2] = gaussian_filter(arr[:,:,2], sigma=0.8)
    return np.clip(arr, 0, 255).astype(np.uint8)


def bg_podium(base=(15,10,3)):
    """Golden light rays — podium / trophy atmosphere."""
    arr = np.zeros((H, W, 3), dtype=np.float32)
    for y in range(H):
        t = y/H
        arr[y] = [base[0]*(1+t*3), base[1]*(1+t*2), base[2]*(1+t*0.5)]
    img = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    rng = np.random.RandomState(5)
    # golden light rays from top
    cx, cy = W//2, -200
    for _ in range(80):
        angle = rng.uniform(0.2, math.pi-0.2)
        length = rng.uniform(800, 1800)
        width  = rng.randint(3, 40)
        a = rng.uniform(0.015, 0.08)
        x2 = cx + int(math.cos(angle)*length)
        y2 = cy + int(math.sin(angle)*length)
        c = (int(GOLD[0]*a), int(GOLD[1]*a), int(GOLD[2]*a))
        d.line([(cx,cy),(x2,y2)], fill=c, width=width)
    arr2 = np.array(img).astype(np.float32)
    for c in range(3):
        arr2[:,:,c] = gaussian_filter(arr2[:,:,c], sigma=4)
    return np.clip(arr2, 0, 255).astype(np.uint8)


def bg_network_nodes(base=(4,4,20), accent=(80,0,220)):
    """Neural network / data nodes topology."""
    arr = np.zeros((H, W, 3), dtype=np.float32)
    arr[:] = base
    rng = np.random.RandomState(9)
    img = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(img)
    nodes = [(rng.randint(100,W-100), rng.randint(100,H-100)) for _ in range(55)]
    for i,(x1,y1) in enumerate(nodes):
        for j,(x2,y2) in enumerate(nodes[i+1:i+5], i+1):
            if j >= len(nodes): break
            dist = math.hypot(x2-x1, y2-y1)
            if dist < 380:
                a = max(0.03, 0.18*(1-dist/380))
                c = tuple(int(c*a) for c in accent)
                d.line([(x1,y1),(x2,y2)], fill=c, width=1)
    for (x,y) in nodes:
        r = rng.randint(3,14)
        a = rng.uniform(0.3,0.9)
        c_outer = tuple(int(c*a*0.4) for c in accent)
        c_inner = tuple(int(c*a) for c in accent)
        d.ellipse([(x-r*2,y-r*2),(x+r*2,y+r*2)], fill=c_outer)
        d.ellipse([(x-r,y-r),(x+r,y+r)],   fill=c_inner)
    arr = np.array(img).astype(np.float32)
    for c in range(3):
        arr[:,:,c] = gaussian_filter(arr[:,:,c], sigma=2)
    return np.clip(arr, 0, 255).astype(np.uint8)


# ── Pre-render all backgrounds once ──────────────────────────────
print("  Generating cinematic backgrounds …", flush=True)
_BG = {}

def build_backgrounds():
    global _BG
    _BG['f1_car']          = bg_speed_lines((90,5,5),(18,3,3),RED,cx=W*0.6,cy=H*0.45)
    print("    bg 1/10 speed lines ✓", flush=True)
    _BG['f1_cockpit']      = bg_carbon_fiber(tint=RED)
    print("    bg 2/10 carbon fiber ✓", flush=True)
    _BG['f1_circuit']      = bg_circuit(line_col=RED)
    print("    bg 3/10 circuit map ✓", flush=True)
    _BG['f1_pitstop']      = bg_speed_lines((60,25,0),(15,8,0),(255,100,0),cx=W*0.4)
    print("    bg 4/10 pit speed lines ✓", flush=True)
    _BG['data_dashboard']  = bg_data_grid(base=(3,6,20), accent=(0,180,255))
    print("    bg 5/10 data grid ✓", flush=True)
    _BG['data_network']    = bg_network_nodes(base=(4,4,20), accent=(80,0,220))
    print("    bg 6/10 network nodes ✓", flush=True)
    _BG['crowd_stadium']   = bg_bokeh(base_col=(8,4,4),
                                       light_cols=[RED,GOLD,WHITE,(255,100,0)])
    print("    bg 7/10 bokeh lights ✓", flush=True)
    _BG['night_circuit']   = bg_light_trails(base=(4,4,14))
    print("    bg 8/10 light trails ✓", flush=True)
    _BG['telemetry_screen']= bg_telemetry(base=(3,10,18))
    print("    bg 9/10 telemetry ✓", flush=True)
    _BG['podium_trophy']   = bg_podium(base=(15,10,3))
    print("    bg 10/10 podium rays ✓", flush=True)


# ── Gradient mask ─────────────────────────────────────────────────
_GRAD = np.zeros((H, W), dtype=np.float32)
for _y in range(H):
    _GRAD[_y, :] = (max(0, (_y/H - 0.35)/0.65)) ** 1.6 * 0.85
_GRAD3 = np.stack([_GRAD]*3, axis=-1)
_DARK_F = np.array(DARK, dtype=np.float32)
_BASE_CACHE: dict = {}

def get_base(key: str, opacity: float) -> np.ndarray:
    ck = (key, opacity)
    if ck not in _BASE_CACHE:
        bg = _BG.get(key, np.zeros((H,W,3),dtype=np.uint8)).astype(np.float32)
        dark = bg * (1 - opacity)
        dark = dark*(1-_GRAD3) + _DARK_F*_GRAD3
        _BASE_CACHE[ck] = np.clip(dark, 0, 255).astype(np.uint8)
    return _BASE_CACHE[ck]


def new_frame(key: str, opacity: float,
              t: float = 0, kb: bool = False,
              kb0: float = 1.0, kb1: float = 1.08):
    if kb:
        scale = kb0 + (kb1-kb0)*(t/SD)
        nw, nh = int(W*scale), int(H*scale)
        raw = Image.fromarray(_BG.get(key, np.zeros((H,W,3),dtype=np.uint8)))
        raw = raw.resize((nw,nh), Image.BILINEAR)
        l, tp = (nw-W)//2, (nh-H)//2
        raw = np.array(raw.crop((l,tp,l+W,tp+H))).astype(np.float32)
        dark = raw*(1-opacity)
        dark = dark*(1-_GRAD3) + _DARK_F*_GRAD3
        base_np = np.clip(dark, 0, 255).astype(np.uint8)
    else:
        base_np = get_base(key, opacity)
    img = Image.fromarray(base_np)
    return img, ImageDraw.Draw(img)


# ── Draw helpers ──────────────────────────────────────────────────

def fade(col, a):
    return tuple(max(0,min(255,int(c*a))) for c in col)

def txt_c(draw, text, y, font, col, a=1.0, shadow=True):
    f = fade(col, a)
    bb = draw.textbbox((0,0),text,font=font)
    x = (W-(bb[2]-bb[0]))//2
    if shadow:
        draw.text((x+3,y+3),text,font=font,fill=fade((0,0,0),a*0.8))
    draw.text((x,y),text,font=font,fill=f)
    return x

def txt(draw, text, x, y, font, col, a=1.0, shadow=True):
    if shadow:
        draw.text((x+2,y+2),text,font=font,fill=fade((0,0,0),a*0.7))
    draw.text((x,y),text,font=font,fill=fade(col,a))

def card_rect(draw, x, y, w, h, border_col, a=1.0, filled=True):
    if filled:
        draw.rectangle([(x,y),(x+w,y+h)], fill=fade(DARK, a*0.88))
    draw.rectangle([(x,y),(x+5,y+h)], fill=fade(border_col,a))

def glow_line(draw, x1, y1, x2, y2, col, a=1.0, width=2):
    """Draw a glowing line with halo."""
    for w2, fa in [(width*5,0.08),(width*3,0.14),(width,1.0)]:
        draw.line([(x1,y1),(x2,y2)], fill=fade(col,a*fa), width=w2)

def ea(t, delay, dur=0.5):
    if t<=delay: return 0.0
    return min(1.0,(t-delay)/max(dur,0.001))

# ══════════════════════════════════════════════════════════════════
#  SCENES
# ══════════════════════════════════════════════════════════════════

def s01(t):  # INTRO — f1_car speed lines
    img, d = new_frame('f1_car',0.45,t,kb=True,kb0=1.0,kb1=1.08)
    a = ea(t,0,1.5)
    # red glow behind title
    if a>0.1:
        for gw, ga in [(200,0.04),(100,0.08),(40,0.15)]:
            bb = d.textbbox((0,0),"LA FIA À L'ÈRE",font=fnt(90))
            tw = bb[2]-bb[0]; cx2 = W//2
            d.ellipse([(cx2-gw,380-gw//2),(cx2+gw,420+gw//2)],
                      fill=fade(RED, ga*a))
    txt_c(d,"LA FIA À L'ÈRE",      370, fnt(90), WHITE, a)
    txt_c(d,"DE L'INTELLIGENCE ARTIFICIELLE", 475, fnt(90), RED, a)
    if t>1.5:
        lw=int(ea(t,1.5,0.9)*860); lx=(W-860)//2
        glow_line(d, lx,608, lx+lw,608, RED, 1.0, 3)
    if t>2.2:
        a2=ea(t,2.2,1.0)
        txt_c(d,"Colin Toum  &  Matthieu Dambrin",665,fnt(28,False),WHITE,a2)
    return np.array(img)


def s02(t):  # LA FIA EN CHIFFRES — circuit background
    img, d = new_frame('f1_circuit',0.55)
    txt(d,"La FIA en Chiffres",80,55,fnt(64),WHITE)
    glow_line(d,80,138,560,138,RED,0.6,2)
    prog = min(1.0,t/3.0)
    stats=[("143","Championnats",RED),("150","Pays membres",RED),
           ("2,5 Md€","Revenus annuels",GOLD),("445M","Fans mondiaux",RED)]
    for i,(num,lbl,col) in enumerate(stats):
        cx2=80+i*460; cy2=220; a=ea(t,i*0.3,0.4)
        card_rect(d,cx2,cy2,420,195,col,a)
        try:
            raw=float(num.replace('M','').replace('Md€','').replace(',','.'))
            v=raw*prog
            disp=f"{v:.1f} Md€" if 'Md€' in num else (f"{int(v)}M" if 'M' in num else str(int(v)))
        except: disp=num
        txt(d,disp,cx2+18,cy2+22,fnt(58),col,a)
        txt(d,lbl, cx2+18,cy2+106,fnt(22,False),(210,210,210),a)
    if t>4.5:
        a3=ea(t,4.5,1.0)
        levels=[("F3",560,52,(90,90,110)),("F2",360,64,GOLD),("F1",180,78,RED)]
        py=490
        for ln,lw2,lh,lc in levels:
            lx=(W-lw2)//2
            d.rectangle([(lx,py),(lx+lw2,py+lh)],fill=fade(lc,a3*0.88))
            bb2=d.textbbox((0,0),ln,font=fnt(30)); tw2=bb2[2]-bb2[0]
            txt(d,ln,lx+(lw2-tw2)//2,py+(lh-30)//2,fnt(30),WHITE,a3)
            py+=lh+6
    return np.array(img)


def s03(t):  # LE PROBLÈME — data network
    img, d = new_frame('data_network',0.60)
    txt(d,"Le Problème",80,55,fnt(64),WHITE)
    glow_line(d,80,138,400,138,RED,0.7,2)
    txt(d,"La FIA dispose de données extraordinaires — et ne les exploite pas",
        80,155,fnt(28,False),RED)
    items=[("Télémétrie sous-exploitée","1 200 pts/s non analysés"),
           ("Scouting à l'instinct","Décisions sans données"),
           ("Revenus sponsoring figés","Pas de pricing dynamique"),
           ("Fan engagement générique","Contenu non personnalisé")]
    positions=[(80,272),(550,272),(80,490),(550,490)]
    for i,((ti,de),(cx2,cy2)) in enumerate(zip(items,positions)):
        a=ea(t,i*0.4)
        card_rect(d,cx2,cy2,418,168,RED,a)
        txt(d,ti,cx2+18,cy2+18,fnt(26),WHITE,a)
        txt(d,de,cx2+18,cy2+72,fnt(20,False),(195,195,195),a)
    return np.array(img)


def s04(t):  # L'OPPORTUNITÉ — telemetry
    img, d = new_frame('telemetry_screen',0.50)
    txt(d,"L'Opportunité",80,40,fnt(64),WHITE)
    glow_line(d,80,122,440,122,RED,0.7,2)
    for val,lbl,col,x in [("1 200","pts/seconde télémétrie",RED,80),
                           ("+22%","Croissance F1 2024",GOLD,700),
                           ("20/22","Pilotes F1 junior",RED,1300)]:
        a=ea(t,0.5,1.0)
        txt(d,val,x,195,fnt(100),col,a)
        txt(d,lbl,x,325,fnt(22,False),WHITE,a*0.88)
    bullets=["• Chaque course génère 3 To de données",
             "• 75% des équipes sans outil IA centralisé",
             "• Marché SportTech IA : 8,4 Md$ d'ici 2028",
             "• La FIA = agrégateur naturel de la data motorsport"]
    for i,b in enumerate(bullets):
        txt(d,b,80,500+i*55,fnt(24,False),WHITE,ea(t,2+i*0.5))
    return np.array(img)


def s05(t):  # FIA DATAHUB — data grid
    img, d = new_frame('data_dashboard',0.52)
    txt(d,"◉  FIA DATAHUB",80,40,fnt(72),WHITE)
    glow_line(d,80,130,500,130,RED,0.7,2)
    modules=[("Excellence Sportive","IA Télémétrie",RED,120,220),
             ("Optimisation Revenus","Sponsoring Dynamique",GOLD,1020,220),
             ("Fan Engagement","Personnalisation IA",RED,120,550),
             ("Scouting Pilotes","Algorithme Multi-Critères",GOLD,1020,550)]
    cx2,cy2=W//2,430
    for i,(ti,de,col,mx,my) in enumerate(modules):
        a=ea(t,i*0.5)
        card_rect(d,mx,my,400,158,col,a)
        txt(d,ti,mx+18,my+18,fnt(26),WHITE,a)
        txt(d,de,mx+18,my+70,fnt(20,False),(185,185,185),a)
        if a>0.2:
            glow_line(d,mx+200,my+79,cx2,cy2,col,a*0.3,1)
    r=64
    d.ellipse([(cx2-r,cy2-r),(cx2+r,cy2+r)],fill=fade(RED,0.88))
    glow_r=90
    d.ellipse([(cx2-glow_r,cy2-glow_r),(cx2+glow_r,cy2+glow_r)],fill=fade(RED,0.12))
    txt(d,"FIA", cx2-18,cy2-20,fnt(22),WHITE)
    txt(d,"DATA",cx2-22,cy2+2, fnt(16),WHITE)
    return np.array(img)


def _pilier(bg, opacity, title, sub, bullets, stats, t):
    img, d = new_frame(bg, opacity)
    txt(d,title,80,45,fnt(54),WHITE)
    glow_line(d,80,128,600,128,RED,0.5,2)
    if sub: txt(d,sub,80,132,fnt(28,False),RED)
    for i,b in enumerate(bullets):
        txt(d,b,80,248+i*58,fnt(24,False),(220,220,220),ea(t,1+i*0.3))
    for i,(num,lbl,col) in enumerate(stats):
        sx,sy=1290,280+i*230
        card_rect(d,sx,sy,510,188,col)
        # glow behind number
        d.rectangle([(sx+6,sy),(sx+510,sy+188)],fill=fade(col,0.06))
        txt(d,num,sx+18,sy+18,fnt(66),col)
        txt(d,lbl,sx+18,sy+128,fnt(22,False),WHITE)
    return np.array(img)


def s06(t): return _pilier('f1_cockpit',0.55,"Pilier 1 — Excellence Sportive",
    "1 200 points/seconde. Enfin exploités.",
    ["• Analyse temps réel de la télémétrie","• Optimisation stratégies de course",
     "• Détection anomalies mécaniques","• Prédiction performance pneus",
     "• Comparaison inter-écuries sécurisée"],
    [("-23%","Réduction des DNF",RED),("+1,8s","Gain/Tour moyen",GOLD)],t)

def s07(t): return _pilier('f1_pitstop',0.52,"Pilier 2 — Optimisation des Revenus",None,
    ["• Sponsoring dynamique basé sur l'audience","• Monétisation des droits data",
     "• Pricing intelligence partenaires","• Analyse ROI temps réel sponsors",
     "• Nouveaux produits data"],
    [("+18%","Revenus sponsoring",RED),("x3","Valeur droits data",GOLD)],t)

def s08(t): return _pilier('crowd_stadium',0.45,"Pilier 3 — Fan Engagement",None,
    ["• Contenu personnalisé par profil fan","• Prédictions temps réel interactives",
     "• Second screen experience","• Gamification basée sur les données",
     "• Notifications push intelligentes"],
    [("+25%","Engagement fans",RED),("x4","Croissance F1 TV",GOLD)],t)

def s09(t): return _pilier('night_circuit',0.48,"Pilier 4 — Scouting Pilotes",
    "Détecter le prochain Verstappen dès la F3.",
    ["• Scoring IA multi-critères","• Analyse comparative F3/F2/F1",
     "• Prédiction progression 3 ans","• Détection talents sous-évalués",
     "• Matching pilote/écurie optimal"],
    [("20/22","Pilotes F1 détectables",RED),("-40%","Risque recrutement",GOLD)],t)


def s10(t):  # ARCHITECTURE — data network
    img, d = new_frame('data_network',0.60)
    txt(d,"Architecture de la Plateforme",80,45,fnt(58),WHITE)
    glow_line(d,80,128,720,128,RED,0.5,2)
    steps=[("COLLECTE",    ["Télémétrie live","IoT capteurs","Données hist."]),
           ("TRAITEMENT IA",["ML Pipeline","Neural Nets","Edge Computing"]),
           ("DASHBOARD",   ["Temps réel","Alertes","Rapports auto"]),
           ("DÉCISION",    ["Recommand. IA","Automation","API Export"])]
    sw,sh,sx0,sp=378,298,70,458
    for i,(step,subs) in enumerate(steps):
        a=ea(t,i*0.7); sx=sx0+i*sp; sy=222
        card_rect(d,sx,sy,sw,sh,RED,a)
        d.rectangle([(sx,sy),(sx+sw,sy+52)],fill=fade(RED,a*0.85))
        bb=d.textbbox((0,0),step,font=fnt(24)); tw=bb[2]-bb[0]
        txt(d,step,sx+(sw-tw)//2,sy+12,fnt(24),WHITE,a)
        for j,sub in enumerate(subs):
            txt(d,f"• {sub}",sx+14,sy+70+j*62,fnt(20,False),(200,200,200),a)
        if i<3 and a>0.15:
            ax=sx+sw+8; ay=sy+sh//2
            glow_line(d,ax,ay,ax+sp-sw-14,ay,RED,a*0.8,2)
            d.polygon([(ax+sp-sw-8,ay-10),(ax+sp-sw-8,ay+10),(ax+sp-sw+2,ay)],
                      fill=fade(RED,a))
    return np.array(img)


def s11(t):  # MARCHÉ — circuit
    img, d = new_frame('f1_circuit',0.55)
    txt(d,"Marché Adressable",80,45,fnt(64),WHITE)
    glow_line(d,80,128,500,128,RED,0.5,2)
    pcx,pcy=450,580
    circles=[(270,(50,50,80),"TAM","8,4 Md$",GRAY),
             (190,(80,30,30),"SAM","1,2 Md$",RED),
             (110,RED,"SOM","45 M€",WHITE)]
    for i,(r,col,nm,val,tc) in enumerate(circles):
        delay=i*0.7
        if t>delay:
            prog=min(1.0,(t-delay)/0.7); ar=int(r*prog)
            d.ellipse([(pcx-ar,pcy-ar),(pcx+ar,pcy+ar)],fill=fade(col,0.82))
            if prog>0.88:
                txt(d,nm, pcx-18,pcy-15,fnt(22),tc)
                txt(d,val,pcx-30,pcy+10,fnt(18,False),tc)
    bullets=["Phase 1 (2025) : FIA F3 — 5 circuits",
             "Phase 2 (2026) : Formule E + F2",
             "Phase 3 (2027+) : 143 Championnats FIA",
             "","Croissance SportTech IA : +22%/an",
             "Pas d'équivalent sur le marché global"]
    for i,b in enumerate(bullets):
        if b: txt(d,f"• {b}",950,200+i*62,fnt(23,False),WHITE,ea(t,2.5+i*0.35))
    return np.array(img)


def s12(t):  # CONCURRENCE — data dashboard
    img, d = new_frame('data_dashboard',0.60)
    txt(d,"Analyse Concurrentielle",80,45,fnt(58),WHITE)
    glow_line(d,80,128,620,128,RED,0.5,2)
    hdrs=["Critère","McLaren Applied","AWS F1","Catapult","Notre Solution"]
    rows=[["Données FIA natives","✗","Partiel","✗","✓"],
          ["IA Scouting","✗","✗","Partiel","✓"],
          ["Fan Engagement","✗","Partiel","✗","✓"],
          ["Multi-championnats","✗","✗","✗","✓"],
          ["Open API","✗","Partiel","✗","✓"]]
    cws=[340,280,212,212,286]; rh=72; sx2=60; sy0=193
    if t>0.3:
        d.rectangle([(sx2,sy0),(sx2+sum(cws),sy0+rh)],fill=(50,50,65))
        x2=sx2
        for h,cw in zip(hdrs,cws):
            txt(d,h,x2+10,sy0+22,fnt(22),WHITE); x2+=cw
    for ri,row in enumerate(rows):
        a=ea(t,0.7+ri*0.4); ry=sy0+(ri+1)*rh
        d.rectangle([(sx2,ry),(sx2+sum(cws),ry+rh)],fill=fade((22,22,32),a*0.9))
        x2=sx2
        for ci,(cell,cw) in enumerate(zip(row,cws)):
            if ci==0:    fc=fade((200,200,200),a)
            elif cell=="✓": fc=fade((50,210,80),a)
            elif cell=="✗": fc=fade((200,60,60),a)
            else:            fc=fade((200,180,50),a)
            txt(d,cell,x2+12,ry+22,fnt(20,ci>0),fc,1.0)
            x2+=cw
    return np.array(img)


def s13(t):  # MODÈLE ÉCO — pitstop
    img, d = new_frame('f1_pitstop',0.52)
    txt(d,"Modèle Économique",80,40,fnt(64),WHITE)
    glow_line(d,80,122,500,122,RED,0.5,2)
    pricing=[("FIA HQ","180k€/an",RED,"Accès complet\n+ IA personnalisée"),
             ("Écuries F1","95k€/an",GOLD,"Télémétrie + scouting"),
             ("Médias/TV","120k€/an",RED,"Fan analytics + droits"),
             ("Sponsors","60k€/an",GOLD,"ROI tracking + activation")]
    cw,ch=410,305
    for i,(plan,price,col,desc) in enumerate(pricing):
        a=ea(t,i*0.45); prog=min(1.0,max(0,(t-i*0.45)/0.45))
        cy3=int(130+(1-prog)*80); cx3=65+i*460
        card_rect(d,cx3,cy3,cw,ch,col,a)
        d.rectangle([(cx3+6,cy3),(cx3+cw,cy3+6)],fill=fade(col,a*0.5))
        txt(d,plan, cx3+18,cy3+22,fnt(28),col,a)
        txt(d,price,cx3+18,cy3+78,fnt(52),WHITE,a)
        for li,line in enumerate(desc.split('\n')):
            txt(d,line,cx3+18,cy3+185+li*40,fnt(20,False),(175,175,175),a)
    if t>4.5:
        a2=ea(t,4.5)
        d.rectangle([(0,910),(W,985)],fill=fade((40,8,8),a2*0.9))
        ft="Revenue Share 2%  •  Data Licensing 50–200k€  •  Modules SaaS à la carte"
        bb=d.textbbox((0,0),ft,font=fnt(24,False)); tw=bb[2]-bb[0]
        txt(d,ft,(W-tw)//2,930,fnt(24,False),WHITE,a2)
    return np.array(img)


def s14(t):  # GTM — night circuit
    img, d = new_frame('night_circuit',0.52)
    txt(d,"Go-To-Market",80,40,fnt(64),WHITE)
    glow_line(d,80,122,380,122,RED,0.5,2)
    tly=290
    glow_line(d,80,tly,W-80,tly,(90,90,110),0.7,2)
    phases=[("Phase 1","M1–M12",RED,
             ["F3 PoC — 5 circuits","Signature FIA Board","3 écuries pilotes","MVP Dashboard"]),
            ("Phase 2","M13–M24",GOLD,
             ["F2 + Formula E","10 écuries clientes","Lancement commercial","Break-even atteint"]),
            ("Phase 3","M25–M36",RED,
             ["143 championnats FIA","Scale international","M&A potentiel","ARR 4,2 M€"])]
    cw=(W-200)//3
    for i,(ph,period,col,buls) in enumerate(phases):
        a=ea(t,i*0.65); x2=80+i*cw
        d.ellipse([(x2+cw//2-13,tly-13),(x2+cw//2+13,tly+13)],fill=fade(col,a))
        card_rect(d,x2,tly+28,cw-18,380,col,a)
        d.rectangle([(x2,tly+28),(x2+cw-18,tly+80)],fill=fade(col,a*0.85))
        txt(d,ph,x2+14,tly+36,fnt(28),WHITE,a)
        txt(d,period,x2+14,tly+94,fnt(22,False),(200,200,200),a)
        for bi,b in enumerate(buls):
            txt(d,f"• {b}",x2+14,tly+142+bi*54,fnt(20,False),(200,200,200),a)
    return np.array(img)


def s15(t):  # TRACTION — podium
    img, d = new_frame('podium_trophy',0.48)
    txt(d,"Traction & Preuves de Concept",80,45,fnt(58),WHITE)
    glow_line(d,80,128,680,128,GOLD,0.6,2)
    poc=[("-23%","Réduction DNF","PoC Télémétrie Monaco 2024",RED),
         ("9/10","Pilotes prédits","Algorithme Scouting F3 2023",GOLD),
         ("+18%","Revenus sponsoring","Test avec écurie cliente",RED),
         ("2","Écuries en discussion","Négociations avancées",GOLD)]
    positions=[(80,195),(540,195),(80,500),(540,500)]
    for i,((num,lbl,desc,col),(cx2,cy2)) in enumerate(zip(poc,positions)):
        a=ea(t,i*0.45)
        card_rect(d,cx2,cy2,418,268,col,a)
        d.rectangle([(cx2+6,cy2),(cx2+418,cy2+6)],fill=fade(col,a*0.6))
        txt(d,num, cx2+18,cy2+18,fnt(76),col,a)
        txt(d,lbl, cx2+18,cy2+130,fnt(26),WHITE,a)
        txt(d,desc,cx2+18,cy2+180,fnt(20,False),(160,160,160),a)
    return np.array(img)


def s16(t):  # FINANCES — data dashboard
    img, d = new_frame('data_dashboard',0.55)
    txt(d,"Projections Financières",80,25,fnt(54),WHITE)
    glow_line(d,80,105,580,105,GOLD,0.6,2)
    txt(d,"Break-even à 18 mois — ARR 4,2 M€ en an 3",80,108,fnt(26,False),GOLD)
    years=["An 1","An 2","An 3"]; arr_v=[420,1800,4200]; cost_v=[680,1100,1900]
    mv=max(max(arr_v),max(cost_v))
    chx,chy,chh=70,162,400; bsp=240; bw=78
    d.line([(chx,chy+chh),(chx+860,chy+chh)],fill=(90,90,100),width=2)
    d.line([(chx,chy),(chx,chy+chh)],fill=(90,90,100),width=2)
    for i,(yr,av,cv) in enumerate(zip(years,arr_v,cost_v)):
        delay=1.2+i*0.7
        if t>delay:
            prog=min(1.0,(t-delay)/0.7); bx2=chx+58+i*bsp
            ah=int((av/mv)*chh*prog)
            d.rectangle([(bx2,chy+chh-ah),(bx2+bw,chy+chh)],fill=RED)
            # glow
            d.rectangle([(bx2-2,chy+chh-ah-2),(bx2+bw+2,chy+chh)],fill=fade(RED,0.15))
            ch2=int((cv/mv)*chh*prog)
            d.rectangle([(bx2+bw+10,chy+chh-ch2),(bx2+bw*2+10,chy+chh)],fill=(115,115,115))
            if prog>0.9:
                f18=fnt(18,False)
                d.text((bx2,chy+chh-ah-28),f"{av}k€",font=f18,fill=RED)
                d.text((bx2+bw+10,chy+chh-ch2-28),f"{cv}k€",font=f18,fill=GRAY)
                d.text((bx2+28,chy+chh+12),yr,font=f18,fill=WHITE)
    leg_y=chy+chh+50
    d.rectangle([(chx,leg_y),(chx+18,leg_y+18)],fill=RED)
    d.text((chx+24,leg_y),"ARR",font=fnt(18,False),fill=WHITE)
    d.rectangle([(chx+88,leg_y),(chx+106,leg_y+18)],fill=(115,115,115))
    d.text((chx+112,leg_y),"Coûts",font=fnt(18,False),fill=WHITE)
    kpis=[("Championnats An1","3"),("Championnats An3","143"),("ARR An3","4,2 M€"),
          ("Break-even","M18"),("Marge An3","55%"),("CAC","< 50k€")]
    for i,(kn,kv) in enumerate(kpis):
        a=ea(t,2+i*0.28)
        card_rect(d,1058,162+i*110,380,88,RED,a)
        txt(d,kn,1074,170+i*110,fnt(18,False),(165,165,165),a)
        txt(d,kv,1074,196+i*110,fnt(30),WHITE,a)
    return np.array(img)


def s17(t):  # ÉQUIPE — carbon fiber cockpit
    img, d = new_frame('f1_cockpit',0.55)
    txt(d,"L'Équipe",80,45,fnt(64),WHITE)
    glow_line(d,80,128,260,128,RED,0.6,2)
    team=[("CEO / Sport Business","Colin Toum",
           "Ex-consultant FIA — Strategy & Partenariats"),
          ("CTO / Data Science","Matthieu Dambrin",
           "ML Engineer — Ex-AWS — 8 ans data"),
          ("Head of Sales","N.N.",
           "Expertise sport pro — B2B SaaS — 12 ans"),
          ("Ing. Télémétrie","N.N.",
           "10 ans F1/F2 — Spécialiste données course")]
    positions=[(80,210),(980,210),(80,485),(980,485)]
    for i,((role,name,desc),(cx2,cy2)) in enumerate(zip(team,positions)):
        a=ea(t,i*0.4)
        card_rect(d,cx2,cy2,840,222,RED,a)
        txt(d,name,cx2+22,cy2+20,fnt(34),WHITE,a)
        txt(d,role,cx2+22,cy2+68,fnt(24),RED,a)
        txt(d,desc,cx2+22,cy2+128,fnt(20,False),(165,165,165),a)
    return np.array(img)


def s18(t):  # ROADMAP — circuit
    img, d = new_frame('f1_circuit',0.55)
    txt(d,"Roadmap 36 mois",80,28,fnt(64),WHITE)
    glow_line(d,80,110,440,110,RED,0.5,2)
    tly=400; ts=110; te=W-110
    glow_line(d,ts,tly,te,tly,(65,65,85),0.9,3)
    milestones=[("M3","MVP",RED),("M6","F3 Live",RED),
                ("M9","Scouting",GOLD),("M12","FIA Board",RED),
                ("M18","Break-even",(50,200,70)),("M24","Formula E",GOLD),
                ("M30","Data F1",RED),("M36","143 Champ.",GOLD)]
    nm=len(milestones); sp=(te-ts)/(nm-1)
    for i,(mo,lbl,col) in enumerate(milestones):
        a=ea(t,i*0.48); mx=int(ts+i*sp)
        d.ellipse([(mx-14,tly-14),(mx+14,tly+14)],fill=fade(col,a))
        d.ellipse([(mx-20,tly-20),(mx+20,tly+20)],fill=fade(col,a*0.2))
        txt(d,mo, mx-15,tly+22,fnt(20,False),(200,200,200),a)
        ly=tly-80 if i%2==0 else tly+58
        txt(d,lbl,mx-40,ly,fnt(20),col,a)
    phases=[("An1 — F3 PoC",ts,int(ts+3*sp)),
            ("An2 — Expansion",int(ts+3*sp),int(ts+5.5*sp)),
            ("An3 — Scale Global",int(ts+5.5*sp),te)]
    if t>5:
        a=ea(t,5)
        for pn,px0,px1 in phases:
            d.rectangle([(px0+4,tly+135),(px1-4,tly+177)],fill=fade((28,28,48),a*0.82))
            pcx2=(px0+px1)//2; bb=d.textbbox((0,0),pn,font=fnt(20,False))
            txt(d,pn,pcx2-(bb[2]-bb[0])//2,tly+144,fnt(20,False),(195,195,195),a)
    return np.array(img)


def s19(t):  # FINANCEMENT — network nodes
    img, d = new_frame('data_network',0.55)
    txt(d,"Besoin de Financement",80,28,fnt(60),WHITE)
    glow_line(d,80,108,540,108,RED,0.5,2)
    pcx2,pcy2,pr=430,530,215
    segs=[("Développement IA","45%",0.45,RED),
          ("Commercial & Mktg","25%",0.25,GOLD),
          ("Infrastructure Cloud","20%",0.20,(115,115,135)),
          ("Opérations & Légal","10%",0.10,(65,65,85))]
    angle=-90.0
    for i,(_,_2,ratio,col) in enumerate(segs):
        delay=i*0.5
        if t>delay:
            prog=min(1.0,(t-delay)/0.5); sweep=ratio*360*prog
            pts=[(pcx2,pcy2)]
            steps=max(3,int(sweep/2))
            for k in range(steps+1):
                rad=math.radians(angle+k*(sweep/max(steps,1)))
                pts.append((pcx2+pr*math.cos(rad),pcy2+pr*math.sin(rad)))
            if len(pts)>=3:
                d.polygon(pts,fill=fade(col,0.88))
            if prog>=1.0: angle+=sweep
    for i,(nm,pct,_,col) in enumerate(segs):
        if t>i*0.5+0.5:
            a=ea(t,i*0.5+0.5); lx=80+i*460; ly=800
            d.rectangle([(lx,ly),(lx+22,ly+22)],fill=fade(col,a))
            txt(d,f"{nm} ({pct})",lx+30,ly,fnt(20,False),WHITE,a)
    budget=[("Développement IA / Data","270 000 €"),
            ("Commercial & Marketing","150 000 €"),
            ("Infrastructure Cloud","120 000 €"),
            ("Opérations & Légal","60 000 €")]
    for i,(it,val) in enumerate(budget):
        a=ea(t,1.8+i*0.4); card_rect(d,1058,193+i*92,718,70,RED,a)
        txt(d,it,  1074,200+i*92,fnt(20,False),(178,178,178),a)
        bb=d.textbbox((0,0),val,font=fnt(30)); tw=bb[2]-bb[0]
        txt(d,val,1768-tw,210+i*92,fnt(30),WHITE,a)
    if t>4.8:
        a3=ea(t,4.8)
        txt(d,"TOTAL",1058,578,fnt(22,False),(195,195,195),a3)
        txt(d,"600 000 €",1058,616,fnt(58),RED,a3)
    if t>6.0:
        a4=ea(t,6.0)
        d.rectangle([(0,910),(W,985)],fill=fade((35,8,8),a4*0.9))
        ft="Objectif : contrat FIA en 12 mois  •  ROI x5 sur 5 ans"
        bb=d.textbbox((0,0),ft,font=fnt(24,False)); tw=bb[2]-bb[0]
        txt(d,ft,(W-tw)//2,938,fnt(24,False),WHITE,a4)
    return np.array(img)


def s20(t):  # OUTRO — speed lines KB
    img, d = new_frame('f1_car',0.38,t,kb=True,kb0=1.0,kb1=1.14)
    a=ea(t,0,1.2)
    # big glow behind main text
    if a>0.1:
        d.ellipse([(W//2-400,310),(W//2+400,440)],fill=fade(RED,a*0.08))
    txt_c(d,"LA COURSE VERS",268,fnt(72),WHITE,a)
    txt_c(d,"LA DATA COMMENCE ICI.",366,fnt(80),RED,a)
    if t>1.5:
        lp=ea(t,1.5,0.9); lw=int(lp*700); lx=(W-700)//2
        glow_line(d,lx,490,lx+lw,490,RED,1.0,3)
    if t>2.2:
        txt_c(d,"Merci Pour Votre Attention",530,fnt(48,False),WHITE,ea(t,2.2,0.9))
    if t>3.0:
        a3=ea(t,3.0,0.7); bw,bh=440,72; bx=(W-bw)//2; by=648
        d.rectangle([(bx-2,by-2),(bx+bw+2,by+bh+2)],fill=fade(RED,a3*0.2))
        d.rectangle([(bx,by),(bx+bw,by+bh)],fill=fade(RED,a3*0.92))
        ct="Prendre contact  →"; bb=d.textbbox((0,0),ct,font=fnt(34)); tw=bb[2]-bb[0]
        txt(d,ct,(W-tw)//2,by+16,fnt(34),WHITE,a3)
    if t>4.0:
        a4=ea(t,4.0,0.8)
        ft="contact@fia-ia.fr  •  fia-ia.fr  •  Paris, France"
        bb=d.textbbox((0,0),ft,font=fnt(22,False)); tw=bb[2]-bb[0]
        txt(d,ft,(W-tw)//2,766,fnt(22,False),GRAY,a4)
    return np.array(img)


# ── Audio ─────────────────────────────────────────────────────────

def gen_audio(dur, path='/tmp/fia_audio.wav'):
    sr=44100; n=int(sr*dur); t_arr=np.arange(n)/sr
    env=0.5+0.5*np.sin(2*np.pi*2.0*t_arr)
    audio=0.28*np.sin(2*np.pi*60*t_arr)*env+0.10*np.sin(2*np.pi*120*t_arr)
    audio+=0.08*np.sin(2*np.pi*90*t_arr)*(0.5+0.5*np.sin(2*np.pi*0.4*t_arr))
    step=int(0.5*sr)
    rng=np.random.RandomState(1)
    for i in range(0,n,step):
        cl=int(0.018*sr); end=min(i+cl,n)
        noise=rng.randn(end-i)*0.14
        decay=np.exp(-np.arange(end-i)/(0.004*sr))
        audio[i:end]+=noise*decay
    fi=int(3*sr); fo=int(5*sr)
    audio[:fi]*=np.linspace(0,1,fi); audio[-fo:]*=np.linspace(1,0,fo)
    mv=np.max(np.abs(audio)); audio=audio/mv*0.78 if mv>0 else audio
    a16=(audio*32767).astype(np.int16)
    with wave.open(path,'w') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes(a16.tobytes())
    print(f"  ✓ audio → {path}")
    return path


# ── Main ──────────────────────────────────────────────────────────

SCENES=[s01,s02,s03,s04,s05,s06,s07,s08,s09,s10,
        s11,s12,s13,s14,s15,s16,s17,s18,s19,s20]


def main():
    print("=" * 64)
    print("  FIA IA v2 — Cinematic Demo  (synthetic visual backgrounds)")
    print("=" * 64)

    print("\n▶ Generating cinematic backgrounds …")
    t0=time.time()
    build_backgrounds()
    print(f"  done in {time.time()-t0:.1f}s\n")

    print("▶ Pre-warming base frame cache …")
    bg_ops=[('f1_car',0.45),('f1_circuit',0.55),('data_network',0.60),
            ('telemetry_screen',0.50),('data_dashboard',0.52),
            ('f1_cockpit',0.55),('f1_pitstop',0.52),('crowd_stadium',0.45),
            ('night_circuit',0.48),('podium_trophy',0.48),
            ('data_dashboard',0.55),('data_dashboard',0.60),('f1_circuit',0.55)]
    for k,op in set(bg_ops): get_base(k,op)
    print("  done\n")

    if not MOVIEPY_OK:
        print("moviepy unavailable — using OpenCV"); _cv2_render(); return

    print("▶ Building VideoClips …")
    all_clips=[]
    for i,sf in enumerate(SCENES):
        def make_frame(t,_sf=sf): return _sf(t)
        clip=VideoClip(make_frame,duration=SD).with_fps(FPS)
        all_clips.append(clip)
        print(f"  Scene {i+1:02d}/20 ✓")

    print("\n▶ Concatenating …")
    final=concatenate_videoclips(all_clips,method='compose')

    print("\n▶ Generating audio …")
    ap=gen_audio(final.duration+3)
    audio=AudioFileClip(ap).subclipped(0,final.duration)
    final=final.with_audio(audio)

    out='/tmp/FIA_IA_ProductDemo_v2.mp4'
    print(f"\n▶ Exporting → {out}")
    print(f"  {final.duration:.0f}s · {W}×{H} · {FPS}fps")
    t0=time.time()
    final.write_videofile(out,fps=FPS,codec='libx264',audio_codec='aac',
                          bitrate='8000k',preset='fast',logger='bar')
    dt=time.time()-t0

    if os.path.exists(out):
        mb=os.path.getsize(out)/(1024*1024)
        print("\n"+"="*64)
        print(f"  ✅  {out}")
        print(f"  {mb:.1f} MB · {final.duration:.0f}s · rendered in {dt:.0f}s")
        print("="*64)
    else:
        print("❌ Export failed")


def _cv2_render():
    import cv2
    out='/tmp/FIA_IA_ProductDemo_v2.mp4'
    wr=cv2.VideoWriter(out,cv2.VideoWriter_fourcc(*'mp4v'),FPS,(W,H))
    for i,sf in enumerate(SCENES):
        for fi in range(SD*FPS):
            wr.write(cv2.cvtColor(sf(fi/FPS),cv2.COLOR_RGB2BGR))
        print(f"  Scene {i+1:02d}/20 ✓")
    wr.release()
    mb=os.path.getsize(out)/(1024*1024) if os.path.exists(out) else 0
    print(f"\n✅ {out}  |  {mb:.1f} MB")


if __name__=='__main__':
    main()
