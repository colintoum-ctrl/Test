#!/usr/bin/env python3
"""
FIA IA - Product Demo Video Generator  (optimised build)
"LA FIA À L'ÈRE DE L'INTELLIGENCE ARTIFICIELLE"
Colin Toum & Matthieu Dambrin — cinematic 3-min MP4 1920×1080 @ 30fps
"""

import os, sys, math, wave, time
import requests, numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

try:
    from moviepy import VideoClip, concatenate_videoclips, AudioFileClip
    MOVIEPY_OK = True
except Exception as e:
    MOVIEPY_OK = False
    print(f"moviepy unavailable: {e}")

try:
    import cv2; CV2_OK = True
except Exception:
    CV2_OK = False

# ── Constants ────────────────────────────────────────────────────
W, H   = 1920, 1080
FPS    = 30
SD     = 9        # scene duration seconds
NS     = 20

BG    = (13,  13,  13)
RED   = (232,   0,  13)
GOLD  = (201, 168,  76)
WHITE = (255, 255, 255)
GRAY  = (150, 150, 150)
DARK  = ( 18,  18,  28)

ASSETS = Path('/tmp/assets')
ASSETS.mkdir(exist_ok=True)

FONT_BOLD   = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_NORMAL = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'

IMAGE_URLS = {
    'f1_car':           'https://images.unsplash.com/photo-1629385700892-9c91dac6f4a4?w=1920',
    'f1_cockpit':       'https://images.unsplash.com/photo-1541773367336-d3f28e3e37a3?w=1920',
    'f1_circuit':       'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1920',
    'f1_pitstop':       'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=1920',
    'data_dashboard':   'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1920',
    'data_network':     'https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920',
    'crowd_stadium':    'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=1920',
    'night_circuit':    'https://images.unsplash.com/photo-1504983875-d3b163aba9e6?w=1920',
    'telemetry_screen': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920',
    'podium_trophy':    'https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?w=1920',
}

# ── Pre-compute gradient mask once ───────────────────────────────
_GRAD = np.zeros((H, W), dtype=np.float32)
for _y in range(H//2, H):
    _a = (((_y - H//2) / (H//2)) ** 1.4) * 0.72
    _GRAD[_y, :] = _a
_GRAD = np.stack([_GRAD]*3, axis=-1)   # (H, W, 3)
_BG_F = np.array(BG, dtype=np.float32)  # broadcast fill colour

# ── Base-image cache (non-KB) ─────────────────────────────────────
_BASE_CACHE: dict = {}

# ── Font cache ────────────────────────────────────────────────────
_FONT_CACHE: dict = {}

def fnt(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    key = (size, bold)
    if key not in _FONT_CACHE:
        path = FONT_BOLD if bold else FONT_NORMAL
        try:
            _FONT_CACHE[key] = ImageFont.truetype(path, size)
        except Exception:
            _FONT_CACHE[key] = ImageFont.load_default()
    return _FONT_CACHE[key]

# ── Image helpers ─────────────────────────────────────────────────

def placeholder(key: str) -> np.ndarray:
    seed = {'f1_car':(30,5,5),'f1_cockpit':(5,5,30),'f1_circuit':(5,20,10),
            'f1_pitstop':(25,5,5),'data_dashboard':(5,10,35),
            'data_network':(5,5,40),'crowd_stadium':(35,5,5),
            'night_circuit':(5,5,18),'telemetry_screen':(5,25,35),
            'podium_trophy':(40,30,5)}.get(key,(15,15,15))
    arr = np.zeros((H,W,3),dtype=np.uint8)
    for y in range(H):
        f = 1 + y/H*2
        arr[y] = [min(255,int(c*f)) for c in seed]
    return arr


def download_images() -> dict:
    imgs = {}
    hdrs = {'User-Agent': 'Mozilla/5.0'}
    for key, url in IMAGE_URLS.items():
        fp = ASSETS / f"{key}.jpg"
        if fp.exists():
            try:
                im = Image.open(fp).convert('RGB').resize((W,H), Image.BILINEAR)
                imgs[key] = np.array(im); print(f"  cached  {key}"); continue
            except Exception:
                pass
        print(f"  download {key} …", end=' ', flush=True)
        try:
            r = requests.get(url, timeout=15, headers=hdrs); r.raise_for_status()
            fp.write_bytes(r.content)
            im = Image.open(fp).convert('RGB').resize((W,H), Image.BILINEAR)
            imgs[key] = np.array(im); print("✓")
        except Exception as e:
            print(f"✗ ({e}) → placeholder")
            imgs[key] = placeholder(key)
    return imgs


def _make_base_np(bg: np.ndarray, opacity: float) -> np.ndarray:
    """Dark overlay + gradient vignette — returns float32 ready to pass to PIL."""
    f = bg.astype(np.float32) * (1 - opacity)
    f = f * (1 - _GRAD) + _BG_F * _GRAD
    return np.clip(f, 0, 255).astype(np.uint8)


def get_base_cached(imgs: dict, key: str, opacity: float) -> np.ndarray:
    ck = (key, opacity)
    if ck not in _BASE_CACHE:
        _BASE_CACHE[ck] = _make_base_np(imgs.get(key, placeholder(key)), opacity)
    return _BASE_CACHE[ck]


def new_frame(imgs: dict, key: str, opacity: float,
              t: float = 0, kb: bool = False,
              kb0: float = 1.0, kb1: float = 1.08) -> tuple:
    """Return (PIL Image RGB, ImageDraw) for this frame."""
    if kb:
        scale = kb0 + (kb1 - kb0) * (t / SD)
        nw, nh = int(W*scale), int(H*scale)
        raw = Image.fromarray(imgs.get(key, placeholder(key)))
        raw = raw.resize((nw, nh), Image.BILINEAR)
        l, tp = (nw-W)//2, (nh-H)//2
        raw = np.array(raw.crop((l, tp, l+W, tp+H)))
        base_np = _make_base_np(raw, opacity)
    else:
        base_np = get_base_cached(imgs, key, opacity)
    img = Image.fromarray(base_np)
    return img, ImageDraw.Draw(img)


# ── Draw helpers ──────────────────────────────────────────────────

def fade(col: tuple, a: float) -> tuple:
    """Multiply colour by alpha [0-1] → dark-fade effect on dark bg."""
    return tuple(int(c * a) for c in col)


def txt_c(draw, text, y, font, col, a=1.0):
    """Draw centred text with shadow."""
    f = fade(col, a)
    bb = draw.textbbox((0,0), text, font=font)
    x = (W - (bb[2]-bb[0])) // 2
    draw.text((x+2, y+2), text, font=font, fill=fade((0,0,0), a*0.7))
    draw.text((x,   y),   text, font=font, fill=f)
    return x


def txt(draw, text, x, y, font, col, a=1.0):
    fc = fade(col, a)
    draw.text((x+2, y+2), text, font=font, fill=fade((0,0,0), a*0.6))
    draw.text((x,   y),   text, font=font, fill=fc)


def card_rect(draw, x, y, w, h, border_col, a=1.0, filled=True):
    """Draw a dark card with coloured left bar."""
    if filled:
        draw.rectangle([(x, y), (x+w, y+h)], fill=fade(DARK, a*0.85))
    draw.rectangle([(x, y), (x+5, y+h)],  fill=fade(border_col, a))


def ea(t, delay, dur=0.5) -> float:
    """Eased progress 0→1 starting at `delay`."""
    if t <= delay: return 0.0
    return min(1.0, (t-delay)/max(dur, 0.001))

# ── Scene generators ──────────────────────────────────────────────

def s01(imgs, t):
    img, d = new_frame(imgs,'f1_car',0.50,t,kb=True,kb0=1.0,kb1=1.08)
    a = ea(t,0,1.5)
    txt_c(d,"LA FIA À L'ÈRE",        370, fnt(90), WHITE, a)
    txt_c(d,"DE L'INTELLIGENCE ARTIFICIELLE", 475, fnt(90), RED,   a)
    if t>1.5:
        lw=int(ea(t,1.5,1.0)*800); lx=(W-800)//2
        d.rectangle([(lx,604),(lx+lw,611)], fill=RED)
    if t>2.2:
        txt_c(d,"Colin Toum  &  Matthieu Dambrin",662,fnt(28,False),WHITE,ea(t,2.2,1.0))
    return np.array(img)


def s02(imgs, t):
    img, d = new_frame(imgs,'f1_circuit',0.60)
    txt(d,"La FIA en Chiffres",80,55,fnt(64),WHITE)
    prog = min(1.0, t/3.0)
    stats = [("143","Championnats",RED),("150","Pays membres",RED),
             ("2,5 Md€","Revenus annuels",GOLD),("445M","Fans mondiaux",RED)]
    for i,(num,lbl,col) in enumerate(stats):
        cx = 80+i*460; cy = 220
        card_rect(d,cx,cy,420,195,col)
        try:
            raw=float(num.replace('M','').replace('Md€','').replace(',','.'))
            v=raw*prog
            disp=f"{v:.1f} Md€" if 'Md€' in num else (f"{int(v)}M" if 'M' in num else str(int(v)))
        except Exception: disp=num
        txt(d,disp,cx+18,cy+20,fnt(58),col)
        txt(d,lbl, cx+18,cy+100,fnt(22,False),(195,195,195))
    if t>4.5:
        a=ea(t,4.5,1.0)
        levels=[("F3",560,52,(90,90,100)),("F2",360,64,GOLD),("F1",180,78,RED)]
        py=490
        for ln,lw,lh,lc in levels:
            lx=(W-lw)//2
            d.rectangle([(lx,py),(lx+lw,py+lh)], fill=fade(lc,a*0.88))
            bb=d.textbbox((0,0),ln,font=fnt(30))
            d.text((lx+(lw-(bb[2]-bb[0]))//2, py+(lh-30)//2),ln,font=fnt(30),fill=fade(WHITE,a))
            py+=lh+6
    return np.array(img)


def s03(imgs, t):
    img, d = new_frame(imgs,'data_network',0.65)
    txt(d,"Le Problème",80,55,fnt(64),WHITE)
    txt(d,"La FIA dispose de données extraordinaires — et ne les exploite pas",
        80,152,fnt(29,False),RED)
    items=[("Télémétrie sous-exploitée","1 200 pts/s non analysés"),
           ("Scouting à l'instinct","Décisions sans données"),
           ("Revenus sponsoring figés","Pas de pricing dynamique"),
           ("Fan engagement générique","Contenu non personnalisé")]
    pos=[(80,272),(550,272),(80,490),(550,490)]
    for i,((ti,de),(cx,cy)) in enumerate(zip(items,pos)):
        a=ea(t,i*0.4)
        card_rect(d,cx,cy,418,168,RED,a); txt(d,ti,cx+18,cy+18,fnt(26),WHITE,a)
        txt(d,de,cx+18,cy+74,fnt(20,False),(190,190,190),a)
    return np.array(img)


def s04(imgs, t):
    img, d = new_frame(imgs,'telemetry_screen',0.55)
    txt(d,"L'Opportunité",80,40,fnt(64),WHITE)
    for val,lbl,col,x in [("1 200","pts/seconde télémétrie",RED,80),
                           ("+22%","Croissance F1 2024",GOLD,700),
                           ("20/22","Pilotes F1 junior",RED,1300)]:
        a=ea(t,0.5,1.0); txt(d,val,x,195,fnt(100),col,a); txt(d,lbl,x,325,fnt(22,False),WHITE,a*0.85)
    bullets=["• Chaque course génère 3 To de données",
             "• 75% des équipes sans outil IA centralisé",
             "• Marché SportTech IA : 8,4 Md$ d'ici 2028",
             "• La FIA = agrégateur naturel de la data motorsport"]
    for i,b in enumerate(bullets):
        txt(d,b,80,500+i*55,fnt(24,False),WHITE,ea(t,2+i*0.5))
    return np.array(img)


def s05(imgs, t):
    img, d = new_frame(imgs,'data_dashboard',0.60)
    txt(d,"◉  FIA DATAHUB",80,40,fnt(72),WHITE)
    modules=[("Excellence Sportive","IA Télémétrie",RED,120,220),
             ("Optimisation Revenus","Sponsoring Dynamique",GOLD,1020,220),
             ("Fan Engagement","Personnalisation IA",RED,120,550),
             ("Scouting Pilotes","Algorithme Multi-Critères",GOLD,1020,550)]
    cx,cy=W//2,430
    for i,(ti,de,col,mx,my) in enumerate(modules):
        a=ea(t,i*0.5)
        card_rect(d,mx,my,400,158,col,a)
        txt(d,ti,mx+18,my+18,fnt(26),WHITE,a); txt(d,de,mx+18,my+70,fnt(20,False),(180,180,180),a)
        if a>0.25:
            d.line([(mx+200,my+79),(cx,cy)],fill=fade(col,a*0.35),width=2)
    r=64
    d.ellipse([(cx-r,cy-r),(cx+r,cy+r)],fill=fade(RED,0.9))
    txt(d,"FIA",cx-18,cy-20,fnt(22),WHITE); txt(d,"DATA",cx-20,cy+2,fnt(16),WHITE)
    return np.array(img)


def _pilier(imgs, bg, title, sub, bullets, stats, t, op=0.60):
    img, d = new_frame(imgs,bg,op)
    txt(d,title,80,45,fnt(54),WHITE)
    if sub: txt(d,sub,80,122,fnt(28,False),RED)
    for i,b in enumerate(bullets):
        txt(d,b,80,240+i*58,fnt(24,False),(215,215,215),ea(t,1+i*0.3))
    for i,(num,lbl,col) in enumerate(stats):
        sx,sy=1290,280+i*230; card_rect(d,sx,sy,510,188,col)
        txt(d,num,sx+18,sy+18,fnt(66),col); txt(d,lbl,sx+18,sy+128,fnt(22,False),WHITE)
    return np.array(img)


def s06(imgs,t): return _pilier(imgs,'f1_cockpit',"Pilier 1 — Excellence Sportive",
    "1 200 points/seconde. Enfin exploités.",
    ["• Analyse temps réel de la télémétrie","• Optimisation stratégies de course",
     "• Détection anomalies mécaniques","• Prédiction performance pneus","• Comparaison inter-écuries sécurisée"],
    [("-23%","Réduction des DNF",RED),("+1,8s","Gain/Tour moyen",GOLD)],t)

def s07(imgs,t): return _pilier(imgs,'f1_pitstop',"Pilier 2 — Optimisation des Revenus",None,
    ["• Sponsoring dynamique basé sur l'audience","• Monétisation des droits data",
     "• Pricing intelligence partenaires","• Analyse ROI temps réel sponsors","• Nouveaux produits data"],
    [("+18%","Revenus sponsoring",RED),("x3","Valeur droits data",GOLD)],t)

def s08(imgs,t): return _pilier(imgs,'crowd_stadium',"Pilier 3 — Fan Engagement",None,
    ["• Contenu personnalisé par profil fan","• Prédictions temps réel interactives",
     "• Second screen experience","• Gamification basée sur les données","• Notifications push intelligentes"],
    [("+25%","Engagement fans",RED),("x4","Croissance F1 TV",GOLD)],t,0.55)

def s09(imgs,t): return _pilier(imgs,'night_circuit',"Pilier 4 — Scouting Pilotes",
    "Détecter le prochain Verstappen dès la F3.",
    ["• Scoring IA multi-critères","• Analyse comparative F3/F2/F1",
     "• Prédiction progression 3 ans","• Détection talents sous-évalués","• Matching pilote/écurie optimal"],
    [("20/22","Pilotes F1 détectables",RED),("-40%","Risque recrutement",GOLD)],t)


def s10(imgs, t):
    img, d = new_frame(imgs,'data_network',0.65)
    txt(d,"Architecture de la Plateforme",80,45,fnt(58),WHITE)
    steps=[("COLLECTE",["Télémétrie live","IoT capteurs","Données hist."]),
           ("TRAITEMENT IA",["ML Pipeline","Neural Nets","Edge Computing"]),
           ("DASHBOARD",["Temps réel","Alertes","Rapports auto"]),
           ("DÉCISION",["Recommand. IA","Automation","API Export"])]
    sw,sh,sx0,sp=378,298,70,458
    for i,(step,subs) in enumerate(steps):
        a=ea(t,i*0.7); sx=sx0+i*sp; sy=222
        card_rect(d,sx,sy,sw,sh,RED,a)
        d.rectangle([(sx,sy),(sx+sw,sy+52)],fill=fade(RED,a*0.85))
        bb=d.textbbox((0,0),step,font=fnt(24)); tw=bb[2]-bb[0]
        txt(d,step,sx+(sw-tw)//2,sy+12,fnt(24),WHITE,a)
        for j,sub in enumerate(subs):
            txt(d,f"• {sub}",sx+14,sy+70+j*62,fnt(20,False),(195,195,195),a)
        if i<3 and a>0.15:
            ax=sx+sw+8; ay=sy+sh//2
            d.line([(ax,ay),(ax+sp-sw-14,ay)],fill=fade(RED,a),width=3)
            d.polygon([(ax+sp-sw-8,ay-10),(ax+sp-sw-8,ay+10),(ax+sp-sw+2,ay)],fill=fade(RED,a))
    return np.array(img)


def s11(imgs, t):
    img, d = new_frame(imgs,'f1_circuit',0.60)
    txt(d,"Marché Adressable",80,45,fnt(64),WHITE)
    pcx,pcy=450,560
    circles=[(270,(50,50,80),"TAM","8,4 Md$",GRAY),
             (190,(80,30,30),"SAM","1,2 Md$",RED),
             (110,RED,"SOM","45 M€",WHITE)]
    for i,(r,col,nm,val,tc) in enumerate(circles):
        delay=i*0.7
        if t>delay:
            prog=min(1.0,(t-delay)/0.7); ar=int(r*prog)
            d.ellipse([(pcx-ar,pcy-ar),(pcx+ar,pcy+ar)],fill=fade(col,0.8))
            if prog>0.88:
                txt(d,nm,pcx-18,pcy-14,fnt(22),tc); txt(d,val,pcx-28,pcy+10,fnt(18,False),tc)
    bullets=["Phase 1 (2025) : FIA F3 — 5 circuits",
             "Phase 2 (2026) : Formule E + F2",
             "Phase 3 (2027+) : 143 Championnats FIA",
             "","Croissance SportTech IA : +22%/an",
             "Pas d'équivalent sur le marché global"]
    for i,b in enumerate(bullets):
        if b: txt(d,f"• {b}",950,200+i*62,fnt(23,False),WHITE,ea(t,2.5+i*0.35))
    return np.array(img)


def s12(imgs, t):
    img, d = new_frame(imgs,'data_dashboard',0.65)
    txt(d,"Analyse Concurrentielle",80,45,fnt(58),WHITE)
    hdrs=["Critère","McLaren Applied","AWS F1","Catapult","Notre Solution"]
    rows=[["Données FIA natives","✗","Partiel","✗","✓"],
          ["IA Scouting","✗","✗","Partiel","✓"],
          ["Fan Engagement","✗","Partiel","✗","✓"],
          ["Multi-championnats","✗","✗","✗","✓"],
          ["Open API","✗","Partiel","✗","✓"]]
    cws=[340,280,212,212,286]; rh=72; sx=60; sy0=193
    if t>0.3:
        d.rectangle([(sx,sy0),(sx+sum(cws),sy0+rh)],fill=(50,50,65))
        x=sx
        for h,cw in zip(hdrs,cws): txt(d,h,x+10,sy0+22,fnt(22),WHITE); x+=cw
    for ri,row in enumerate(rows):
        a=ea(t,0.7+ri*0.4); ry=sy0+(ri+1)*rh
        d.rectangle([(sx,ry),(sx+sum(cws),ry+rh)],fill=fade((22,22,32),a*0.9))
        x=sx
        for ci,(cell,cw) in enumerate(zip(row,cws)):
            if ci==0:   fc=fade((195,195,195),a)
            elif cell=="✓": fc=fade((50,200,80),a)
            elif cell=="✗": fc=fade((200,60,60),a)
            else:        fc=fade((200,180,50),a)
            txt(d,cell,x+12,ry+22,fnt(20,ci>0),fc,1.0)
            x+=cw
    return np.array(img)


def s13(imgs, t):
    img, d = new_frame(imgs,'f1_pitstop',0.60)
    txt(d,"Modèle Économique",80,40,fnt(64),WHITE)
    pricing=[("FIA HQ","180k€/an",RED,"Accès complet\n+ IA personnalisée"),
             ("Écuries F1","95k€/an",GOLD,"Télémétrie + scouting"),
             ("Médias/TV","120k€/an",RED,"Fan analytics + droits"),
             ("Sponsors","60k€/an",GOLD,"ROI tracking + activation")]
    cw,ch=410,305
    for i,(plan,price,col,desc) in enumerate(pricing):
        a=ea(t,i*0.45); prog=min(1.0,max(0,(t-i*0.45)/0.45))
        cy2=int(130+(1-prog)*80); cx2=65+i*460
        card_rect(d,cx2,cy2,cw,ch,col,a)
        txt(d,plan,cx2+18,cy2+22,fnt(28),col,a)
        txt(d,price,cx2+18,cy2+78,fnt(52),WHITE,a)
        for li,line in enumerate(desc.split('\n')):
            txt(d,line,cx2+18,cy2+183+li*40,fnt(20,False),(170,170,170),a)
    if t>4.5:
        a2=ea(t,4.5)
        d.rectangle([(0,910),(W,985)],fill=fade((40,8,8),a2*0.9))
        ft="Revenue Share 2%  •  Data Licensing 50–200k€  •  Modules SaaS à la carte"
        bb=d.textbbox((0,0),ft,font=fnt(24,False)); tw=bb[2]-bb[0]
        txt(d,ft,(W-tw)//2,930,fnt(24,False),WHITE,a2)
    return np.array(img)


def s14(imgs, t):
    img, d = new_frame(imgs,'night_circuit',0.60)
    txt(d,"Go-To-Market",80,40,fnt(64),WHITE)
    tly=290; d.line([(80,tly),(W-80,tly)],fill=(90,90,110),width=3)
    phases=[("Phase 1","M1–M12",RED,
             ["F3 PoC — 5 circuits","Signature FIA Board","3 écuries pilotes","MVP Dashboard"]),
            ("Phase 2","M13–M24",GOLD,
             ["F2 + Formula E","10 écuries clientes","Lancement commercial","Break-even atteint"]),
            ("Phase 3","M25–M36",RED,
             ["143 championnats FIA","Scale international","M&A potentiel","ARR 4,2 M€"])]
    cw=(W-200)//3
    for i,(ph,period,col,buls) in enumerate(phases):
        a=ea(t,i*0.65); x=80+i*cw
        d.ellipse([(x+cw//2-13,tly-13),(x+cw//2+13,tly+13)],fill=fade(col,a))
        card_rect(d,x,tly+28,cw-18,380,col,a)
        d.rectangle([(x,tly+28),(x+cw-18,tly+80)],fill=fade(col,a*0.85))
        txt(d,ph,x+14,tly+36,fnt(28),WHITE,a); txt(d,period,x+14,tly+94,fnt(22,False),(195,195,195),a)
        for bi,b in enumerate(buls):
            txt(d,f"• {b}",x+14,tly+142+bi*54,fnt(20,False),(195,195,195),a)
    return np.array(img)


def s15(imgs, t):
    img, d = new_frame(imgs,'podium_trophy',0.55)
    txt(d,"Traction & Preuves de Concept",80,45,fnt(58),WHITE)
    poc=[("-23%","Réduction DNF","PoC Télémétrie Monaco 2024",RED),
         ("9/10","Pilotes prédits","Algorithme Scouting F3 2023",GOLD),
         ("+18%","Revenus sponsoring","Test avec écurie cliente",RED),
         ("2","Écuries en discussion","Négociations avancées",GOLD)]
    pos=[(80,195),(540,195),(80,500),(540,500)]
    for i,((num,lbl,desc,col),(cx,cy)) in enumerate(zip(poc,pos)):
        a=ea(t,i*0.45); card_rect(d,cx,cy,418,268,col,a)
        txt(d,num,cx+18,cy+18,fnt(76),col,a)
        txt(d,lbl,cx+18,cy+130,fnt(26),WHITE,a); txt(d,desc,cx+18,cy+180,fnt(20,False),(155,155,155),a)
    return np.array(img)


def s16(imgs, t):
    img, d = new_frame(imgs,'data_dashboard',0.60)
    txt(d,"Projections Financières",80,25,fnt(54),WHITE)
    txt(d,"Break-even à 18 mois — ARR 4,2 M€ en an 3",80,98,fnt(26,False),GOLD)
    years=["An 1","An 2","An 3"]; arr_v=[420,1800,4200]; cost_v=[680,1100,1900]
    mv=max(max(arr_v),max(cost_v))
    chx,chy,chw,chh=70,162,860,400; bsp=240; bw=78
    d.line([(chx,chy+chh),(chx+chw,chy+chh)],fill=(90,90,100),width=2)
    d.line([(chx,chy),(chx,chy+chh)],fill=(90,90,100),width=2)
    for i,(yr,av,cv) in enumerate(zip(years,arr_v,cost_v)):
        delay=1.2+i*0.7
        if t>delay:
            prog=min(1.0,(t-delay)/0.7); bx=chx+58+i*bsp
            ah=int((av/mv)*chh*prog)
            d.rectangle([(bx,chy+chh-ah),(bx+bw,chy+chh)],fill=RED)
            ch2=int((cv/mv)*chh*prog)
            d.rectangle([(bx+bw+10,chy+chh-ch2),(bx+bw*2+10,chy+chh)],fill=(115,115,115))
            if prog>0.9:
                f18=fnt(18,False)
                d.text((bx,chy+chh-ah-28),f"{av}k€",font=f18,fill=RED)
                d.text((bx+bw+10,chy+chh-ch2-28),f"{cv}k€",font=f18,fill=GRAY)
                d.text((bx+28,chy+chh+12),yr,font=f18,fill=WHITE)
    leg_y=chy+chh+50
    d.rectangle([(chx,leg_y),(chx+18,leg_y+18)],fill=RED)
    d.text((chx+24,leg_y),"ARR",font=fnt(18,False),fill=WHITE)
    d.rectangle([(chx+88,leg_y),(chx+106,leg_y+18)],fill=(115,115,115))
    d.text((chx+112,leg_y),"Coûts",font=fnt(18,False),fill=WHITE)
    kpis=[("Championnats An1","3"),("Championnats An3","143"),("ARR An3","4,2 M€"),
          ("Break-even","M18"),("Marge An3","55%"),("CAC","< 50k€")]
    for i,(kn,kv) in enumerate(kpis):
        a=ea(t,2+i*0.28); card_rect(d,1058,162+i*110,380,88,RED,a)
        txt(d,kn,1074,170+i*110,fnt(18,False),(160,160,160),a)
        txt(d,kv,1074,196+i*110,fnt(30),WHITE,a)
    return np.array(img)


def s17(imgs, t):
    img, d = new_frame(imgs,'f1_cockpit',0.60)
    txt(d,"L'Équipe",80,45,fnt(64),WHITE)
    team=[("CEO / Sport Business","Colin Toum","Ex-consultant FIA\nStrategy & Partenariats"),
          ("CTO / Data Science","Matthieu Dambrin","ML Engineer — Ex-AWS\n8 ans data"),
          ("Head of Sales","N.N.","Expertise sport pro\nB2B SaaS — 12 ans"),
          ("Ing. Télémétrie","N.N.","10 ans F1/F2\nSpécialiste données course")]
    pos=[(80,210),(980,210),(80,485),(980,485)]
    for i,((role,name,desc),(cx,cy)) in enumerate(zip(team,pos)):
        a=ea(t,i*0.4); card_rect(d,cx,cy,840,222,RED,a)
        txt(d,name,cx+22,cy+20,fnt(34),WHITE,a); txt(d,role,cx+22,cy+68,fnt(24),RED,a)
        for li,line in enumerate(desc.split('\n')):
            txt(d,line,cx+22,cy+128+li*38,fnt(20,False),(160,160,160),a)
    return np.array(img)


def s18(imgs, t):
    img, d = new_frame(imgs,'f1_circuit',0.60)
    txt(d,"Roadmap 36 mois",80,28,fnt(64),WHITE)
    tly=400; ts=110; te=W-110
    d.line([(ts,tly),(te,tly)],fill=(65,65,85),width=4)
    milestones=[("M3","MVP",RED),("M6","F3 Live",RED),
                ("M9","Scouting",GOLD),("M12","FIA Board",RED),
                ("M18","Break-even",(50,200,70)),("M24","Formula E",GOLD),
                ("M30","Data F1",RED),("M36","143 Champ.",GOLD)]
    nm=len(milestones); sp=(te-ts)/(nm-1)
    for i,(mo,lbl,col) in enumerate(milestones):
        a=ea(t,i*0.48); mx=int(ts+i*sp)
        d.ellipse([(mx-13,tly-13),(mx+13,tly+13)],fill=fade(col,a))
        txt(d,mo,mx-14,tly+20,fnt(20,False),(195,195,195),a)
        ly=tly-75 if i%2==0 else tly+55
        txt(d,lbl,mx-38,ly,fnt(20),col,a)
    phases=[("An1 — F3 PoC",ts,int(ts+3*sp)),
            ("An2 — Expansion",int(ts+3*sp),int(ts+5.5*sp)),
            ("An3 — Scale Global",int(ts+5.5*sp),te)]
    if t>5:
        a=ea(t,5)
        for pn,px0,px1 in phases:
            d.rectangle([(px0+4,tly+135),(px1-4,tly+177)],fill=fade((28,28,48),a*0.82))
            pcx=(px0+px1)//2; bb=d.textbbox((0,0),pn,font=fnt(20,False))
            txt(d,pn,pcx-(bb[2]-bb[0])//2,tly+144,fnt(20,False),(190,190,190),a)
    return np.array(img)


def s19(imgs, t):
    img, d = new_frame(imgs,'data_network',0.60)
    txt(d,"Besoin de Financement",80,28,fnt(60),WHITE)
    pcx,pcy,pr=430,530,215
    segs=[("Développement IA","45%",0.45,RED),
          ("Commercial & Mktg","25%",0.25,GOLD),
          ("Infrastructure Cloud","20%",0.20,(115,115,135)),
          ("Opérations & Légal","10%",0.10,(65,65,85))]
    angle=-90.0
    for i,(nm,pct,ratio,col) in enumerate(segs):
        delay=i*0.5
        if t>delay:
            prog=min(1.0,(t-delay)/0.5); sweep=ratio*360*prog
            pts=[(pcx,pcy)]
            steps=max(3,int(sweep/2))
            for k in range(steps+1):
                rad=math.radians(angle+k*(sweep/max(steps,1)))
                pts.append((pcx+pr*math.cos(rad),pcy+pr*math.sin(rad)))
            if len(pts)>=3: d.polygon(pts,fill=fade(col,0.82))
            if prog>=1.0: angle+=sweep
    for i,(nm,pct,_,col) in enumerate(segs):
        if t>i*0.5+0.5:
            a=ea(t,i*0.5+0.5); lx=80+i*460; ly=802
            d.rectangle([(lx,ly),(lx+22,ly+22)],fill=fade(col,a)); txt(d,f"{nm} ({pct})",lx+30,ly,fnt(20,False),WHITE,a)
    budget=[("Développement IA / Data","270 000 €"),
            ("Commercial & Marketing","150 000 €"),
            ("Infrastructure Cloud","120 000 €"),("Opérations & Légal","60 000 €")]
    for i,(it,val) in enumerate(budget):
        a=ea(t,1.8+i*0.4); card_rect(d,1058,193+i*92,718,70,RED,a,filled=True)
        txt(d,it,1074,200+i*92,fnt(20,False),(175,175,175),a)
        bb=d.textbbox((0,0),val,font=fnt(30)); tw=bb[2]-bb[0]
        txt(d,val,1768-tw,208+i*92,fnt(30),WHITE,a)
    if t>4.8:
        a3=ea(t,4.8); txt(d,"TOTAL",1058,578,fnt(22,False),(190,190,190),a3)
        txt(d,"600 000 €",1058,616,fnt(58),RED,a3)
    if t>6.0:
        a4=ea(t,6.0); d.rectangle([(0,910),(W,985)],fill=fade((35,8,8),a4*0.9))
        ft="Objectif : contrat FIA en 12 mois  •  ROI x5 sur 5 ans"
        bb=d.textbbox((0,0),ft,font=fnt(24,False)); tw=bb[2]-bb[0]
        txt(d,ft,(W-tw)//2,938,fnt(24,False),WHITE,a4)
    return np.array(img)


def s20(imgs, t):
    img, d = new_frame(imgs,'f1_car',0.40,t,kb=True,kb0=1.0,kb1=1.12)
    a=ea(t,0,1.2)
    txt_c(d,"LA COURSE VERS",268,fnt(72),WHITE,a)
    txt_c(d,"LA DATA COMMENCE ICI.",366,fnt(80),RED,a)
    if t>1.5:
        lp=ea(t,1.5,1.0); lw=int(lp*650); lx=(W-650)//2
        d.rectangle([(lx,488),(lx+lw,496)],fill=RED)
    if t>2.2:
        txt_c(d,"Merci Pour Votre Attention",528,fnt(48,False),WHITE,ea(t,2.2,0.9))
    if t>3.0:
        a3=ea(t,3.0,0.7); bw,bh=420,70; bx=(W-bw)//2; by=648
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
    sr=44100; n=int(sr*dur); t=np.arange(n)/sr
    env=0.5+0.5*np.sin(2*np.pi*2.0*t)
    audio=0.28*np.sin(2*np.pi*60*t)*env+0.10*np.sin(2*np.pi*120*t)
    audio+=0.08*np.sin(2*np.pi*90*t)*(0.5+0.5*np.sin(2*np.pi*0.4*t))
    step=int(0.5*sr)
    for i in range(0,n,step):
        cl=int(0.018*sr); end=min(i+cl,n)
        noise=np.random.randn(end-i)*0.14
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
    print("  FIA IA — Cinematic Product Demo Video")
    print("  « LA FIA À L'ÈRE DE L'INTELLIGENCE ARTIFICIELLE »")
    print("=" * 64)

    print("\n▶ Step 1 — Downloading background images …")
    imgs = download_images()
    print(f"  {len(imgs)} images ready\n")

    # Pre-warm base cache (runs once, fast)
    print("▶ Pre-computing base frames …")
    bg_map=[('f1_car',0.50),('f1_circuit',0.60),('data_network',0.65),
            ('telemetry_screen',0.55),('data_dashboard',0.60),('f1_cockpit',0.60),
            ('f1_pitstop',0.60),('crowd_stadium',0.55),('night_circuit',0.60),
            ('podium_trophy',0.55)]
    for k,op in bg_map: get_base_cached(imgs,k,op)
    print("  done\n")

    if not MOVIEPY_OK:
        print("moviepy unavailable — using OpenCV"); _cv2_render(imgs); return

    print("▶ Step 2 — Building VideoClips …")
    all_clips=[]
    for i,sf in enumerate(SCENES):
        def make_frame(t, _sf=sf, _imgs=imgs): return _sf(_imgs,t)
        clip=VideoClip(make_frame,duration=SD).with_fps(FPS)
        all_clips.append(clip); print(f"  Scene {i+1:02d}/20 ✓")

    print("\n▶ Step 3 — Concatenating …")
    final=concatenate_videoclips(all_clips,method='compose')

    print("\n▶ Step 4 — Generating audio …")
    ap=gen_audio(final.duration+3)
    audio=AudioFileClip(ap).subclipped(0,final.duration)
    final=final.with_audio(audio)

    out='/tmp/FIA_IA_ProductDemo.mp4'
    print(f"\n▶ Step 5 — Exporting {out}")
    print(f"  Duration : {final.duration:.1f}s ({final.duration/60:.1f} min)")
    t0=time.time()
    final.write_videofile(out,fps=FPS,codec='libx264',audio_codec='aac',
                          bitrate='8000k',preset='fast',logger='bar')
    dt=time.time()-t0
    if os.path.exists(out):
        mb=os.path.getsize(out)/(1024*1024)
        print("\n"+"="*64)
        print(f"  ✅  VIDEO EXPORTED: {out}")
        print(f"  Size       : {mb:.1f} MB")
        print(f"  Duration   : {final.duration:.1f}s")
        print(f"  Resolution : {W}×{H} @ {FPS} fps")
        print(f"  Render time: {dt:.0f}s")
        print("="*64)
    else:
        print("❌ Export failed")


def _cv2_render(imgs):
    import cv2
    out='/tmp/FIA_IA_ProductDemo.mp4'
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    wr=cv2.VideoWriter(out,fourcc,FPS,(W,H))
    for i,sf in enumerate(SCENES):
        for fi in range(SD*FPS):
            frame=sf(imgs,fi/FPS)
            wr.write(cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
        print(f"  Scene {i+1:02d}/20 ✓")
    wr.release()
    mb=os.path.getsize(out)/(1024*1024) if os.path.exists(out) else 0
    print(f"\n✅ OpenCV export: {out}  |  {mb:.1f} MB")


if __name__=='__main__':
    main()
