"""Felt-style SVG assets for 大象的口袋海. Each piece stands on its bottom edge (pop-up hinge)."""
import os, math
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'art', 'svg')
os.makedirs(OUT, exist_ok=True)

def felt(seed=3, disp=6):
    return f'''<filter id="f" x="-4%" y="-4%" width="108%" height="108%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="{seed}" result="w"/>
<feDisplacementMap in="SourceGraphic" in2="w" scale="{disp}" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" seed="{seed+11}" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0.55 0 0 0 -0.24" result="na"/>
<feComposite in="na" in2="d" operator="in" result="sp"/>
<feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="2" seed="{seed+4}" result="h"/>
<feColorMatrix in="h" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0.4 0 0 0 -0.26" result="ha"/>
<feComposite in="ha" in2="d" operator="in" result="hi"/>
<feMerge><feMergeNode in="d"/><feMergeNode in="sp"/><feMergeNode in="hi"/></feMerge>
</filter>
<filter id="s" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="#2a1a10" flood-opacity=".28"/></filter>'''

ST = 'fill="none" stroke="#fffaf0" stroke-opacity=".75" stroke-width="3.2" stroke-dasharray="9 7" stroke-linecap="round"'
STD = 'fill="none" stroke="#3b2a1c" stroke-opacity=".35" stroke-width="3" stroke-dasharray="9 7" stroke-linecap="round"'

def svg(name, w, h, body, seed=3, disp=6):
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>{felt(seed, disp)}</defs>
<g filter="url(#f)">{body}</g>
</svg>'''
    open(f'{OUT}/{name}.svg', 'w').write(s)

def wave_path(w, y, amp, n, h, phase=0):
    pts = []
    for i in range(0, n * 8 + 1):
        x = w * i / (n * 8)
        pts.append(f'{x:.1f},{y + amp * math.sin(i / 8 * 2 * math.pi + phase):.1f}')
    return f'M0,{h} L' + ' L'.join(pts) + f' L{w},{h} Z'

def scallop(w, y, r, h):
    d = f'M0,{h} L0,{y}'
    x = 0
    while x < w:
        d += f' a{r},{r*0.8} 0 0 1 {2*r},0'
        x += 2 * r
    return d + f' L{w},{h} Z'

# ---------- sun ----------
rays = ''.join(f'<rect x="188" y="14" width="24" height="70" rx="12" fill="#f0a33a" transform="rotate({a} 200 200)"/>' for a in range(0, 360, 30))
svg('sun', 400, 400, f'''{rays}
<circle cx="200" cy="200" r="128" fill="#f7c948" filter="url(#s)"/>
<circle cx="200" cy="200" r="106" {ST}/>
<ellipse cx="160" cy="165" rx="34" ry="22" fill="#fde79a" opacity=".7"/>''', seed=5)

# ---------- cloud ----------
svg('cloud', 520, 260, f'''<path d="M60,240 C10,240 10,170 70,165 C70,100 150,80 185,120 C205,50 320,40 340,115 C380,80 470,100 460,170 C510,175 510,240 460,240 Z" fill="#fbf6ec" filter="url(#s)"/>
<path d="M75,222 C40,220 42,185 85,182 C88,125 150,110 182,145 C208,82 305,78 322,138 C362,108 440,125 438,185 C476,190 476,222 450,222 Z" {STD}/>''', seed=8)

# ---------- far sea with sailboat ----------
svg('sea_far', 2000, 360, f'''<path d="{wave_path(2000, 120, 14, 9, 360)}" fill="#2d6a96"/>
<path d="{wave_path(2000, 180, 16, 11, 360, 1.3)}" fill="#3b89b6" filter="url(#s)"/>
<path d="{wave_path(2000, 245, 15, 13, 360, 2.4)}" fill="#5fb0cf" filter="url(#s)"/>
<path d="{wave_path(2000, 236, 15, 13, 360, 2.4).replace('Z','')}" {ST}/>
<g transform="translate(1480,40)" filter="url(#s)">
 <path d="M60,0 L60,120 L-10,120 Z" fill="#fbf6ec"/><path d="M70,20 L70,120 L130,120 Z" fill="#f2d9a8"/>
 <path d="M-30,124 L160,124 L135,160 L-5,160 Z" fill="#d9594c"/>
 <path d="M-15,138 L148,138" {ST}/>
</g>
<g transform="translate(380,70)" filter="url(#s)">
 <path d="M30,0 L30,70 L-10,70 Z" fill="#fbf6ec"/><path d="M-20,74 L80,74 L66,96 L-6,96 Z" fill="#f0a33a"/>
</g>''', seed=4)

# ---------- front foam row ----------
svg('sea_front', 2000, 200, f'''<path d="{wave_path(2000, 70, 22, 8, 200)}" fill="#7cc8de"/>
<path d="{scallop(2000, 140, 25, 200)}" fill="#e9f7fa" filter="url(#s)"/>
<path d="{wave_path(2000, 92, 18, 8, 200, .4).replace('Z','')}" {ST}/>''', seed=12)

# ---------- beach hut ----------
stripes = ''.join(f'<rect x="{150+i*50}" y="330" width="25" height="300" fill="#5aa3c8"/>' for i in range(8))
svg('hut', 700, 820, f'''<rect x="170" y="600" width="26" height="210" fill="#8a5a3a"/><rect x="504" y="600" width="26" height="210" fill="#8a5a3a"/>
<rect x="330" y="600" width="26" height="210" fill="#7a4e32"/>
<rect x="120" y="580" width="460" height="40" rx="8" fill="#a8774e" filter="url(#s)"/>
<rect x="150" y="330" width="400" height="300" fill="#eef4f2"/>{stripes}
<rect x="150" y="330" width="400" height="300" {STD}/>
<path d="M100,350 L350,120 L600,350 Z" fill="#e06d5a" filter="url(#s)"/>
<path d="M140,335 L350,145 L560,335" {ST}/>
<circle cx="350" cy="270" r="34" fill="#f7d36a" stroke="#a8774e" stroke-width="10"/>
<rect x="300" y="450" width="100" height="160" rx="50" ry="50" fill="#a8774e" filter="url(#s)"/>
<rect x="300" y="450" width="100" height="160" rx="46" {ST}/>
<circle cx="480" cy="480" r="42" fill="none" stroke="#e45b4f" stroke-width="22"/>
<circle cx="480" cy="480" r="42" fill="none" stroke="#fbf6ec" stroke-width="22" stroke-dasharray="33 33"/>''', seed=6)

# ---------- parasol ----------
segs = ''
for i in range(6):
    a0 = math.pi + i * math.pi / 6; a1 = a0 + math.pi / 6
    x0, y0 = 300 + 260 * math.cos(a0), 300 + 150 * math.sin(a0)
    x1, y1 = 300 + 260 * math.cos(a1), 300 + 150 * math.sin(a1)
    segs += f'<path d="M300,300 L{x0:.1f},{y0:.1f} Q{(x0+x1)/2:.1f},{(y0+y1)/2+30:.1f} {x1:.1f},{y1:.1f} Z" fill="{["#e06d5a","#fbf1dc"][i%2]}"/>'
svg('parasol', 600, 720, f'''<path d="M120,700 Q300,610 480,700 Z" fill="#e8cf9a"/>
<rect x="290" y="150" width="20" height="560" rx="8" fill="#8a5a3a"/>
<g filter="url(#s)">{segs}</g><path d="M60,300 Q300,110 540,300" {ST}/>
<circle cx="300" cy="150" r="16" fill="#f0a33a"/>''', seed=7)

# ---------- gull ----------
svg('gull', 420, 260, f'''<path d="M200,140 Q110,30 20,70 Q120,80 180,160 Z" fill="#dfe6ea" filter="url(#s)"/>
<path d="M210,140 Q300,20 400,60 Q300,80 230,160 Z" fill="#dfe6ea" filter="url(#s)"/>
<path d="M20,70 Q50,64 70,68 L60,84 Z" fill="#5a6670"/><path d="M400,60 Q370,58 350,64 L362,80 Z" fill="#5a6670"/>
<ellipse cx="210" cy="170" rx="80" ry="40" fill="#fbfbf7" filter="url(#s)"/>
<circle cx="268" cy="150" r="30" fill="#fbfbf7"/><circle cx="278" cy="144" r="6" fill="#2b2420"/>
<path d="M296,152 L336,160 L296,168 Z" fill="#f0a33a"/>
<path d="M140,170 Q210,205 280,175" {STD}/>''', seed=9)

# ---------- rowboat ----------
svg('rowboat', 720, 300, f'''<path d="M40,110 L680,110 Q640,280 360,280 Q90,280 40,110 Z" fill="#d9594c" filter="url(#s)"/>
<path d="M60,150 L660,150" stroke="#fbf6ec" stroke-width="20"/>
<path d="M70,128 L650,128 Q610,262 360,262 Q120,262 70,128" {ST}/>
<rect x="120" y="40" width="16" height="190" rx="8" fill="#a8774e" transform="rotate(-24 128 135)"/>
<rect x="560" y="40" width="16" height="190" rx="8" fill="#a8774e" transform="rotate(24 568 135)"/>''', seed=10)

# ---------- pine ----------
svg('pine', 320, 620, f'''<rect x="145" y="470" width="30" height="140" rx="6" fill="#7a4e32"/>
<path d="M160,250 L300,500 L20,500 Z" fill="#3f7a52" filter="url(#s)"/>
<path d="M160,140 L270,360 L50,360 Z" fill="#4c8c5e" filter="url(#s)"/>
<path d="M160,30 L240,220 L80,220 Z" fill="#5ca06c" filter="url(#s)"/>
<path d="M60,480 L160,280 L260,480" {ST}/><path d="M95,340 L160,190 L225,340" {ST}/>''', seed=13)

# ---------- moving truck ----------
svg('truck', 960, 640, f'''<g filter="url(#s)">
 <rect x="60" y="120" width="170" height="150" rx="10" fill="#c99a66"/><path d="M60,190 L230,190" stroke="#e9cf9a" stroke-width="16"/>
 <rect x="85" y="20" width="140" height="110" rx="10" fill="#b78452"/><path d="M85,72 L225,72" stroke="#e9cf9a" stroke-width="14"/>
 <rect x="240" y="170" width="120" height="100" rx="10" fill="#d4a774"/>
</g>
<rect x="40" y="270" width="560" height="190" rx="18" fill="#4d9a8f" filter="url(#s)"/>
<rect x="58" y="288" width="524" height="154" rx="14" {ST}/>
<path d="M600,460 L600,250 Q600,200 650,200 L780,200 Q820,200 850,260 L910,350 Q920,370 920,400 L920,460 Z" fill="#e2b34a" filter="url(#s)"/>
<path d="M650,230 L770,230 Q795,230 812,262 L860,340 L650,340 Z" fill="#cfe9f0"/>
<path d="M620,440 L620,262 Q622,222 655,220 L775,220 Q808,222 828,262 L898,372 L900,440" {ST}/>
<rect x="880" y="390" width="40" height="26" rx="6" fill="#fff3b0"/>
<rect x="20" y="450" width="920" height="40" rx="14" fill="#5a4a3a"/>
<circle cx="200" cy="520" r="78" fill="#3a3330"/><circle cx="200" cy="520" r="34" fill="#cfc4b4"/><circle cx="200" cy="520" r="56" {ST}/>
<circle cx="760" cy="520" r="78" fill="#3a3330"/><circle cx="760" cy="520" r="34" fill="#cfc4b4"/><circle cx="760" cy="520" r="56" {ST}/>''', seed=14)

# ---------- signpost ----------
svg('sign', 340, 520, f'''<rect x="155" y="150" width="30" height="360" rx="8" fill="#7a4e32"/>
<path d="M20,60 L260,60 L320,125 L260,190 L20,190 Z" fill="#c99a66" filter="url(#s)"/>
<path d="M36,76 L254,76 L298,125 L254,174 L36,174 Z" {ST}/>
<text x="150" y="146" font-family="PingFang SC,Hiragino Sans GB,Noto Sans CJK SC,Microsoft YaHei,sans-serif" font-size="66" font-weight="700" fill="#4a2e1a" text-anchor="middle">山坡</text>''', seed=15, disp=3)

# ---------- room wall ----------
dots = ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="#e9c9a0"/>' for x in range(60, 2000, 120) for y in range(70, 760, 120))
dots += ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="#c9dccf"/>' for x in range(120, 2000, 120) for y in range(130, 760, 120))
svg('wall', 2000, 900, f'''<rect x="0" y="0" width="2000" height="900" rx="30" fill="#f4e3c6"/>{dots}
<rect x="0" y="790" width="2000" height="110" fill="#a8774e"/><path d="M0,812 L2000,812" {ST}/>
<g filter="url(#s)">
 <circle cx="1380" cy="380" r="230" fill="#a8774e"/>
 <circle cx="1380" cy="380" r="190" fill="#24315f"/>
</g>
<circle cx="1440" cy="320" r="62" fill="#f6edd2"/><circle cx="1420" cy="300" r="12" fill="#d9cfb0"/><circle cx="1460" cy="345" r="9" fill="#d9cfb0"/>
<path d="M1250,250 l6,14 14,2 -10,10 3,15 -13,-7 -13,7 3,-15 -10,-10 14,-2z" fill="#f7d36a"/>
<path d="M1300,450 l4,10 10,1 -7,7 2,10 -9,-5 -9,5 2,-10 -7,-7 10,-1z" fill="#f7d36a"/>
<path d="M1500,470 l4,10 10,1 -7,7 2,10 -9,-5 -9,5 2,-10 -7,-7 10,-1z" fill="#f7d36a"/>
<path d="M1380,190 L1380,570 M1190,380 L1570,380" stroke="#a8774e" stroke-width="22"/>
<circle cx="1380" cy="380" r="210" {ST}/>
<g filter="url(#s)"><rect x="330" y="200" width="420" height="300" rx="12" fill="#c99a66"/></g>
<rect x="360" y="230" width="360" height="240" fill="#bfe6f2"/>
<circle cx="640" cy="290" r="36" fill="#f7c948"/>
<path d="{wave_path(360, 380, 12, 3, 240).replace('M0,', 'M0,')}" fill="#3b89b6" transform="translate(360,230)"/>
<path d="M430,380 L470,380 L460,350 Z" fill="#fbf6ec"/>
<rect x="352" y="222" width="376" height="256" rx="8" {ST}/>
<path d="M540,200 L540,150" stroke="#7a4e32" stroke-width="6"/><circle cx="540" cy="146" r="10" fill="#7a4e32"/>
<g filter="url(#s)"><rect x="850" y="250" width="240" height="22" rx="6" fill="#a8774e"/>
<rect x="880" y="180" width="50" height="70" rx="12" fill="#e06d5a"/><rect x="950" y="160" width="40" height="90" rx="10" fill="#5aa3c8"/>
<circle cx="1040" cy="222" r="28" fill="#f7c948"/></g>''', seed=16, disp=4)

# ---------- bed ----------
squares = ''
cols = ['#e2b34a', '#4d9a8f', '#e06d5a', '#f4e3c6', '#5aa3c8']
for i in range(6):
    for j in range(2):
        squares += f'<rect x="{230+i*90}" y="{250+j*90}" width="90" height="90" fill="{cols[(i+j*2)%5]}"/>'
svg('bed', 860, 560, f'''<rect x="40" y="80" width="60" height="460" rx="20" fill="#8a5a3a" filter="url(#s)"/>
<rect x="760" y="230" width="60" height="310" rx="20" fill="#8a5a3a" filter="url(#s)"/>
<rect x="80" y="360" width="700" height="110" rx="14" fill="#a8774e"/>
<rect x="100" y="180" width="200" height="110" rx="50" fill="#fbf6ec" filter="url(#s)"/>
<rect x="116" y="196" width="168" height="78" rx="38" {STD}/>
<g filter="url(#s)"><path d="M210,240 L770,240 L770,430 L210,430 Z" fill="#4d9a8f"/>{squares}</g>
<path d="M226,256 L754,256 L754,414 L226,414 Z" {ST}/>''', seed=17)

# ---------- floor lamp ----------
svg('lamp', 280, 720, f'''<ellipse cx="140" cy="690" rx="90" ry="22" fill="#7a4e32"/>
<rect x="130" y="180" width="20" height="510" rx="8" fill="#8a5a3a"/>
<path d="M50,200 L90,40 L190,40 L230,200 Z" fill="#f7d36a" filter="url(#s)"/>
<path d="M68,186 L100,56 L180,56 L212,186" {ST}/>
<path d="M50,200 L230,200" stroke="#e2a33a" stroke-width="14"/>''', seed=18)

# ---------- boxes ----------
svg('boxes', 620, 580, f'''<g filter="url(#s)">
 <rect x="40" y="300" width="300" height="270" rx="8" fill="#c99a66"/>
 <rect x="320" y="340" width="260" height="230" rx="8" fill="#b78452"/>
 <rect x="110" y="80" width="260" height="230" rx="8" fill="#d4a774"/>
</g>
<path d="M190,300 L190,570" stroke="#e9cf9a" stroke-width="26"/><path d="M450,340 L450,570" stroke="#e9cf9a" stroke-width="24"/>
<path d="M240,80 L240,310" stroke="#e9cf9a" stroke-width="24"/>
<rect x="60" y="320" width="260" height="230" rx="6" {STD}/><rect x="130" y="100" width="220" height="190" rx="6" {STD}/>
<text x="460" y="470" font-family="PingFang SC,Hiragino Sans GB,Noto Sans CJK SC,Microsoft YaHei,sans-serif" font-size="40" fill="#5a3a22" text-anchor="middle">海边</text>''', seed=19, disp=4)

# ---------- reeds / cattails ----------
blades = ''
import random
random.seed(4)
for i in range(11):
    x = 60 + i * 38 + random.randint(-10, 10); top = 120 + random.randint(0, 220); bend = random.randint(-60, 60)
    blades += f'<path d="M{x-14},600 Q{x+bend/3},{(top+600)/2} {x+bend},{top} Q{x+bend/3+10},{(top+600)/2} {x+14},600 Z" fill="{["#4c8c5e","#5ca06c","#3f7a52"][i%3]}"/>'
tails = ''
for x, y in [(150, 90), (270, 50), (370, 130)]:
    tails += f'<rect x="{x-3}" y="{y}" width="6" height="{560-y}" fill="#6a8a4a"/><rect x="{x-17}" y="{y+10}" width="34" height="110" rx="17" fill="#8a5a3a"/>'
svg('reeds', 520, 610, f'''<g filter="url(#s)">{tails}{blades}</g>''', seed=20)

# ---------- paper boat ----------
svg('paperboat', 420, 280, f'''<path d="M20,150 L400,150 L330,260 L90,260 Z" fill="#fbfbf7" filter="url(#s)"/>
<path d="M210,20 L300,150 L120,150 Z" fill="#f0efe8" filter="url(#s)"/>
<path d="M210,20 L210,150" stroke="#d8d4c8" stroke-width="4"/>
<path d="M60,170 L360,170" stroke="#d8d4c8" stroke-width="4" stroke-dasharray="10 8"/>
<path d="M300,196 l8,-14 8,14 -8,8z" fill="#e06d5a"/>''', seed=21, disp=3)

# ---------- lighthouse (beach) ----------
svg('lighthouse', 420, 760, f'''<path d="M50,750 Q110,640 210,640 Q310,640 370,750 Z" fill="#9e9585" filter="url(#s)"/>
<path d="M90,740 Q210,670 330,740" {STD}/>
<g filter="url(#s)">
 <path d="M145,250 L275,250 L308,670 L112,670 Z" fill="#fbf6ec"/>
 <path d="M138,340 L282,340 L292,440 L128,440 Z" fill="#d9594c"/>
 <path d="M122,530 L298,530 L306,630 L114,630 Z" fill="#d9594c"/>
</g>
<path d="M158,266 L262,266 L292,654 L128,654 Z" {STD}/>
<rect x="120" y="232" width="180" height="28" rx="10" fill="#5a4a3a" filter="url(#s)"/>
<rect x="148" y="138" width="124" height="96" rx="10" fill="#ffe694" filter="url(#s)"/>
<path d="M180,138 L180,234 M240,138 L240,234" stroke="#5a4a3a" stroke-width="10"/>
<path d="M124,142 Q210,40 296,142 Z" fill="#d9594c" filter="url(#s)"/>
<path d="M148,132 Q210,64 272,132" {ST}/>
<circle cx="210" cy="70" r="14" fill="#f7c948"/>
<rect x="186" y="565" width="48" height="72" rx="24" fill="#7a4e32"/>
<circle cx="210" cy="390" r="22" fill="#2d6a96" stroke="#fbf6ec" stroke-width="8"/>''', seed=22)

# ---------- starfish (beach) ----------
sf_pts = []
for i in range(10):
    ang = -math.pi/2 + i * math.pi / 5
    rr = 145 if i % 2 == 0 else 64
    sf_pts.append(f'{180 + rr*math.cos(ang):.1f},{185 + rr*math.sin(ang):.1f}')
sf_dots = ''.join(f'<circle cx="{180+r*math.cos(-math.pi/2+k*2*math.pi/5):.1f}" cy="{185+r*math.sin(-math.pi/2+k*2*math.pi/5):.1f}" r="9" fill="#fde3c8"/>' for k in range(5) for r in (48, 86))
svg('starfish', 360, 340, f'''<polygon points="{' '.join(sf_pts)}" fill="#eb7a53" stroke="#eb7a53" stroke-width="26" stroke-linejoin="round" filter="url(#s)"/>
{sf_dots}<circle cx="180" cy="185" r="16" fill="#fde3c8"/>
<circle cx="164" cy="176" r="6" fill="#3b2f25"/><circle cx="196" cy="176" r="6" fill="#3b2f25"/>
<path d="M172,194 Q180,202 188,194" fill="none" stroke="#3b2f25" stroke-width="4" stroke-linecap="round"/>''', seed=23, disp=4)

# ---------- bucket & shovel (beach) ----------
svg('bucket', 380, 380, f'''<g transform="rotate(24 275 180)" filter="url(#s)">
 <rect x="262" y="75" width="24" height="175" rx="12" fill="#f0a33a"/>
 <path d="M236,42 Q274,10 312,42 L302,86 L246,86 Z" fill="#f7c948"/>
</g>
<path d="M90,150 Q175,55 260,150" fill="none" stroke="#7a4e32" stroke-width="12" stroke-linecap="round"/>
<g filter="url(#s)">
 <path d="M74,142 L276,142 L248,354 Q175,368 102,354 Z" fill="#5aa3c8"/>
 <rect x="64" y="128" width="222" height="32" rx="14" fill="#3b89b6"/>
</g>
<path d="M92,174 L258,174 L236,338 Q175,350 114,338 Z" {ST}/>
<path d="M150,248 l14,-28 14,28 30,4 -22,20 6,30 -28,-14 -28,14 6,-30 -22,-20 z" fill="#f7d36a"/>''', seed=24, disp=4)

# ---------- windmill (road) ----------
svg('windmill', 520, 680, f'''<g filter="url(#s)">
 <path d="M170,220 L350,220 L395,650 L125,650 Z" fill="#f3e5cc"/>
 <path d="M148,228 Q260,90 372,228 Z" fill="#d9594c"/>
</g>
<path d="M184,242 L336,242 L374,632 L146,632 Z" {STD}/>
<path d="M170,214 Q260,114 350,214" {ST}/>
<rect x="220" y="510" width="80" height="140" rx="40" fill="#8a5a3a"/>
<rect x="234" y="524" width="52" height="114" rx="26" {ST}/>
<circle cx="260" cy="360" r="30" fill="#5aa3c8" stroke="#8a5a3a" stroke-width="10"/>
<g transform="translate(260,215)" filter="url(#s)">
 <g transform="rotate(28)">
  <rect x="-12" y="-210" width="24" height="420" rx="8" fill="#8a5a3a"/>
  <rect x="-210" y="-12" width="420" height="24" rx="8" fill="#8a5a3a"/>
  <rect x="12" y="-195" width="54" height="150" rx="8" fill="#f7d36a"/>
  <rect x="-66" y="45" width="54" height="150" rx="8" fill="#f7d36a"/>
  <rect x="45" y="12" width="150" height="54" rx="8" fill="#e9cf9a"/>
  <rect x="-195" y="-66" width="150" height="54" rx="8" fill="#e9cf9a"/>
 </g>
 <circle cx="0" cy="0" r="24" fill="#d9594c"/>
</g>''', seed=25)

# ---------- bush with berries (road / hill / pond) ----------
svg('bush', 520, 320, f'''<g filter="url(#s)">
 <circle cx="135" cy="215" r="95" fill="#4c8c5e"/>
 <circle cx="385" cy="215" r="90" fill="#3f7a52"/>
 <circle cx="260" cy="170" r="120" fill="#5ca06c"/>
 <rect x="65" y="240" width="390" height="72" rx="34" fill="#4c8c5e"/>
</g>
<path d="M90,260 Q140,145 260,115 Q380,145 430,260" {ST}/>
<circle cx="145" cy="195" r="13" fill="#e06d5a"/><circle cx="170" cy="218" r="11" fill="#f7d36a"/>
<circle cx="268" cy="145" r="13" fill="#e06d5a"/><circle cx="298" cy="168" r="10" fill="#f3a7b8"/>
<circle cx="368" cy="205" r="13" fill="#e06d5a"/><circle cx="342" cy="226" r="11" fill="#f7d36a"/>''', seed=26)

# ---------- butterfly (road / hill / pond) ----------
svg('butterfly', 260, 220, f'''<g filter="url(#s)">
 <ellipse cx="82" cy="82" rx="56" ry="46" transform="rotate(-24 82 82)" fill="#f7d36a"/>
 <ellipse cx="178" cy="82" rx="56" ry="46" transform="rotate(24 178 82)" fill="#f7d36a"/>
 <ellipse cx="92" cy="146" rx="40" ry="34" transform="rotate(18 92 146)" fill="#f3a7b8"/>
 <ellipse cx="168" cy="146" rx="40" ry="34" transform="rotate(-18 168 146)" fill="#f3a7b8"/>
</g>
<circle cx="76" cy="78" r="14" fill="#fffaf0"/><circle cx="184" cy="78" r="14" fill="#fffaf0"/>
<rect x="118" y="64" width="24" height="104" rx="12" fill="#4a3728"/>
<path d="M124,66 Q106,24 86,32 M136,66 Q154,24 174,32" fill="none" stroke="#4a3728" stroke-width="6" stroke-linecap="round"/>''', seed=27, disp=3)

# ---------- mailbox (hill) ----------
svg('mailbox', 340, 500, f'''<rect x="150" y="210" width="38" height="280" rx="10" fill="#8a5a3a" filter="url(#s)"/>
<g filter="url(#s)">
 <path d="M62,215 L62,135 Q62,65 135,65 L235,65 Q282,65 282,135 L282,215 Z" fill="#4d9a8f"/>
 <path d="M62,215 L62,135 Q62,65 120,65 Q172,65 172,135 L172,215 Z" fill="#3b8278"/>
</g>
<rect x="84" y="112" width="66" height="16" rx="8" fill="#1f2c55"/>
<path d="M188,88 L266,88 L266,196 L188,196" {ST}/>
<path d="M262,126 L262,56 L302,56 L302,84 L274,84" fill="#e06d5a" stroke="#e06d5a" stroke-width="8" stroke-linejoin="round"/>
<circle cx="262" cy="126" r="10" fill="#f7d36a"/>
<text x="220" y="162" font-family="PingFang SC,Hiragino Sans GB,Noto Sans CJK SC,Microsoft YaHei,sans-serif" font-size="34" font-weight="700" fill="#fffaf0" text-anchor="middle">豆豆</text>''', seed=28, disp=3)

# ---------- fence (hill) ----------
posts = ''.join(f'<rect x="{40+i*128}" y="48" width="44" height="240" rx="14" fill="#c99a66" filter="url(#s)"/>' for i in range(5))
posts_st = ''.join(f'<path d="M{62+i*128},70 L{62+i*128},265" {STD}/>' for i in range(5))
svg('fence', 640, 300, f'''<rect x="20" y="106" width="600" height="32" rx="10" fill="#a8774e" filter="url(#s)"/>
<rect x="20" y="196" width="600" height="32" rx="10" fill="#a8774e" filter="url(#s)"/>
{posts}{posts_st}''', seed=29, disp=4)

# ---------- whale plushie toy (room) ----------
svg('whale_toy', 440, 300, f'''<g filter="url(#s)">
 <path d="M65,220 Q60,90 190,82 Q305,78 332,168 Q355,172 385,126 Q408,162 372,196 Q410,218 380,248 Q340,226 320,218 Q280,262 175,264 Q80,264 65,220 Z" fill="#5aa3c8"/>
 <path d="M74,218 Q155,212 255,222 Q220,262 155,262 Q92,262 74,218 Z" fill="#e9f4f8"/>
</g>
<path d="M88,195 Q110,104 195,100 Q288,96 312,175" {ST}/>
<circle cx="132" cy="170" r="11" fill="#1f2c55"/><circle cx="136" cy="166" r="4" fill="#fff"/>
<ellipse cx="156" cy="192" rx="14" ry="8" fill="#f3a7b8" opacity=".8"/>
<path d="M180,82 Q170,38 140,46 M186,82 Q196,36 226,46" fill="none" stroke="#9ad4ea" stroke-width="10" stroke-linecap="round"/>''', seed=30, disp=4)

# ---------- potted plant (room) ----------
svg('plant', 340, 460, f'''<g filter="url(#s)">
 <path d="M170,295 Q85,205 64,125 Q142,140 176,250 Z" fill="#4c8c5e"/>
 <path d="M170,295 Q255,205 276,125 Q198,140 164,250 Z" fill="#3f7a52"/>
 <path d="M170,295 Q128,160 170,48 Q212,160 170,295 Z" fill="#5ca06c"/>
 <path d="M170,295 Q95,255 48,225 Q112,212 166,275 Z" fill="#5ca06c"/>
 <path d="M170,295 Q245,255 292,225 Q228,212 174,275 Z" fill="#4c8c5e"/>
</g>
<path d="M170,84 L170,275" {ST}/>
<g filter="url(#s)">
 <path d="M88,288 L252,288 L230,446 L110,446 Z" fill="#d97b59"/>
 <rect x="76" y="268" width="188" height="34" rx="12" fill="#e08a68"/>
</g>
<path d="M104,316 L236,316 L220,432 L120,432 Z" {ST}/>''', seed=31, disp=4)

# ---------- pond lantern (pond) ----------
svg('lantern', 320, 560, f'''<g filter="url(#s)">
 <rect x="80" y="90" width="28" height="460" rx="12" fill="#7a4e32"/>
 <path d="M90,104 L218,104 Q236,104 236,126 L236,150" fill="none" stroke="#7a4e32" stroke-width="20" stroke-linecap="round"/>
</g>
<circle cx="236" cy="235" r="78" fill="#ffe694" opacity=".28"/>
<g filter="url(#s)">
 <path d="M192,164 L280,164 L268,144 L204,144 Z" fill="#4a3728"/>
 <rect x="196" y="164" width="80" height="118" rx="18" fill="#ffe694"/>
 <rect x="192" y="276" width="88" height="22" rx="10" fill="#4a3728"/>
</g>
<ellipse cx="236" cy="222" rx="22" ry="34" fill="#fffaf0" opacity=".85"/>
<rect x="206" y="174" width="60" height="96" rx="12" {STD}/>''', seed=32, disp=3)

# ---------- frog (pond) ----------
svg('frog', 320, 260, f'''<g filter="url(#s)">
 <ellipse cx="95" cy="215" rx="56" ry="30" fill="#4c8c5e"/>
 <ellipse cx="225" cy="215" rx="56" ry="30" fill="#4c8c5e"/>
 <ellipse cx="160" cy="166" rx="92" ry="74" fill="#63ab6e"/>
 <ellipse cx="160" cy="190" rx="64" ry="44" fill="#dcefc9"/>
 <circle cx="114" cy="96" r="34" fill="#63ab6e"/>
 <circle cx="206" cy="96" r="34" fill="#63ab6e"/>
</g>
<circle cx="114" cy="96" r="20" fill="#fffaf0"/><circle cx="206" cy="96" r="20" fill="#fffaf0"/>
<circle cx="118" cy="96" r="10" fill="#2b2420"/><circle cx="202" cy="96" r="10" fill="#2b2420"/>
<circle cx="121" cy="92" r="3.5" fill="#fff"/><circle cx="205" cy="92" r="3.5" fill="#fff"/>
<ellipse cx="92" cy="148" rx="14" ry="8" fill="#f3a7b8" opacity=".85"/>
<ellipse cx="228" cy="148" rx="14" ry="8" fill="#f3a7b8" opacity=".85"/>
<path d="M126,148 Q160,174 194,148" fill="none" stroke="#2f5a38" stroke-width="7" stroke-linecap="round"/>
<path d="M108,192 Q160,224 212,192" {STD}/>''', seed=33, disp=4)

print(sorted(os.listdir(OUT)))
