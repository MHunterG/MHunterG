import os, random, math
S=os.path.dirname(os.path.abspath(__file__))  # writes v2-*.svg next to this file
tr, d = open(S+'/head.txt').read().split('\n',1)
THEMES = {'dark': dict(ink='#f2efe8', dim='#6e7681', spark='#f4cf3a'),
          'light': dict(ink='#111110', dim='#8c959f', spark='#d9a600')}
W,H=1200,280; CX,CY,R=600,140,96
def head(c): 
    s=R*2/460*1.12
    return f'<g class="head" transform="translate({CX-230*s} {CY-230*s}) scale({s})"><path fill="{c["ink"]}" transform="{tr}" d="{d}"/></g>'
def ring(c, extra_cls='ring'):
    return f'<circle class="{extra_cls}" cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{c["ink"]}" stroke-width="8"/>'
BASE='''@media (prefers-reduced-motion:reduce){*{animation:none!important}}
@keyframes fade{to{opacity:1}}@keyframes draw{to{stroke-dashoffset:0}}'''
def svg(c, style, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><style>{BASE}{style}</style>{body}</svg>'
circ=2*math.pi*R

def mane(c):
    random.seed(7); pts=[]; x=20; up=True
    while x<W-20:
        if CX-R-14 < x < CX+R+14: x=CX+R+14; pts.append(None); continue
        pts.append((x, CY+10 if up else CY+10-random.choice([10,16,26,38,54]))); x+=random.choice([12,16,20]); up=not up
    segs=[]; cur=[]
    for p in pts:
        if p is None: segs.append(cur); cur=[]
        else: cur.append(p)
    segs.append(cur)
    left='M'+' L'.join(f'{a},{b}' for a,b in segs[0]); right='M'+' L'.join(f'{a},{b}' for a,b in segs[1])
    Ll=3000
    st=f'''.m{{stroke-dasharray:{Ll};stroke-dashoffset:{Ll};animation:draw 2.2s cubic-bezier(.5,0,.2,1) .6s forwards}}
.ring{{stroke-dasharray:{circ:.0f};stroke-dashoffset:{circ:.0f};animation:draw 1.2s cubic-bezier(.6,0,.2,1) forwards;transform:rotate(-90deg);transform-origin:{CX}px {CY}px}}
.head{{opacity:0;animation:fade .8s ease-out .9s forwards}}'''
    body=f'''<path class="m" d="{left}" fill="none" stroke="{c['ink']}" stroke-width="2.5"/><path class="m" d="{right}" fill="none" stroke="{c['ink']}" stroke-width="2.5"/>
{ring(c)}{head(c)}
<circle r="5" fill="{c['spark']}" opacity="0"><set attributeName="opacity" to="1" begin="2.8s"/><animateMotion dur="3.2s" begin="2.8s" repeatCount="indefinite" path="{left}"/></circle>
<circle r="5" fill="{c['spark']}" opacity="0"><set attributeName="opacity" to="1" begin="4.4s"/><animateMotion dur="3.2s" begin="4.4s" repeatCount="indefinite" path="{right}"/></circle>'''
    return svg(c,st,body)

def bugs(c):
    random.seed(3); b=''; st=''
    for i in range(28):
        a=random.uniform(0,2*math.pi); rr=random.uniform(R+24,R+150)
        x=CX+math.cos(a)*rr*1.9; y=CY+math.sin(a)*rr*0.55
        x=min(max(x,30),W-30); y=min(max(y,20),H-20)
        dx,dy=random.uniform(-40,40),random.uniform(-18,18); dur=random.uniform(4,8); dl=random.uniform(0,4); sz=random.uniform(2,4.2)
        st+=f'.b{i}{{animation:f{i} {dur:.1f}s ease-in-out {dl:.1f}s infinite alternate,tw {random.uniform(1.2,2.6):.1f}s ease-in-out {dl:.1f}s infinite alternate}}@keyframes f{i}{{to{{transform:translate({dx:.0f}px,{dy:.0f}px)}}}}'
        b+=f'<circle class="b{i}" cx="{x:.0f}" cy="{y:.0f}" r="{sz:.1f}" fill="{c["spark"]}"/>'
    st+=f'''@keyframes tw{{from{{opacity:.25}}to{{opacity:1}}}}
.charge{{stroke-dasharray:{circ*0.08:.0f} {circ:.0f};animation:spin 2.4s linear infinite;transform-origin:{CX}px {CY}px}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.glow{{opacity:0;animation:pulse 4s ease-in-out 1s infinite}}@keyframes pulse{{0%,70%,100%{{opacity:0}}80%{{opacity:.9}}}}'''
    body=f'''{b}{ring(c)}<circle class="glow" cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{c['spark']}" stroke-width="8"/>
<circle class="charge" cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{c['spark']}" stroke-width="8"/>{head(c)}'''
    return svg(c,st,body)

def recompile(c):
    random.seed(5)
    hexrows=[' '.join(f'{random.randrange(256):02X}' for _ in range(40)) for _ in range(5)]
    cpp=['ctx.a0 = mem.load32(ctx.sp + 16);','ctx.v0 = ctx.a0 + ctx.a1;','if (ctx.v0 != 0) goto L_0880;','ctx.ra = 0x088E6268;','call(0x08878B70);']
    mono='font:500 17px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace'
    st=f'''.hx{{{mono};fill:{c['dim']}}}.cp{{{mono};fill:{c['ink']}}}.kw{{fill:{c['spark']}}}
.in{{animation:inflow 14s linear infinite}}.out{{animation:outflow 4s ease-in-out infinite}}
@keyframes inflow{{from{{transform:translateX(0)}}to{{transform:translateX(420px)}}}}
@keyframes outflow{{0%{{opacity:0;transform:translateX(-30px)}}15%{{opacity:1}}85%{{opacity:1}}100%{{opacity:0;transform:translateX(90px)}}}}
.ring{{stroke-dasharray:{circ*0.1:.0f} {circ*0.05:.0f};animation:spin 12s linear infinite;transform-origin:{CX}px {CY}px}}@keyframes spin{{to{{transform:rotate(360deg)}}}}'''
    L=''.join(f'<text class="hx" x="{-700+ (i%2)*40}" y="{64+i*40}">{r}</text>' for i,r in enumerate(hexrows))
    Rr=''.join(f'<text class="cp" x="{CX+R+30+(i%2)*30}" y="{64+i*40}"><tspan class="kw">›</tspan> {s}</text>' for i,s in enumerate(cpp))
    body=f'''<defs><clipPath id="lc"><rect x="0" y="0" width="{CX-R-20}" height="{H}"/></clipPath><clipPath id="rc"><rect x="{CX+R+20}" y="0" width="{W}" height="{H}"/></clipPath>
<linearGradient id="fl"><stop offset="0" stop-color="{c['ink']}" stop-opacity="0"/><stop offset=".35" stop-color="{c['ink']}" stop-opacity="1"/></linearGradient></defs>
<g clip-path="url(#lc)"><g class="in">{L}</g></g>
<g clip-path="url(#rc)"><g class="out">{Rr}</g></g>
{ring(c)}{head(c)}'''
    return svg(c,st,body)

for name,fn in [('mane',mane),('bugs',bugs),('recompile',recompile)]:
    for th,c in THEMES.items(): open(f'{S}/v2-{name}-{th}.svg','w').write(fn(c))
html='<!doctype html><meta charset=utf-8><title>Banner variants</title><style>body{margin:0;font:15px system-ui}section{padding:24px 32px}.d{background:#0d1117;color:#e6edf3}.l{background:#fff;color:#1f2328}img{width:100%;max-width:1000px;display:block;margin:8px 0 28px}</style><button onclick="document.querySelectorAll(\'img\').forEach(i=>i.src=i.src.split(\'?\')[0]+\'?\'+Date.now())">Replay</button>'
for th,cls in [('dark','d'),('light','l')]:
    html+=f'<section class="{cls}"><h3>GitHub {th}</h3>'+''.join(f'<b>{i+1}. {n}</b><img src="v2-{n}-{th}.svg">' for i,n in enumerate(['mane','bugs','recompile']))+'</section>'
open(S+'/preview2.html','w').write(html)
