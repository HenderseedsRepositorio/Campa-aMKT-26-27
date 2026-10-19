"""Girasol realista en SVG (para reels y placas).

Tres piezas, pensadas para ir juntas:

  defs   degradés compartidos. Van UNA vez por página, dentro del <svg> oculto de
         símbolos (no en una escena con display:none: ahí Chrome no pinta los degradés).
  flor   un girasol "de verdad", en coordenadas fijas (disco de radio 200 centrado en 0,0;
         pétalos hasta r≈450; tallo hasta y≈840). Se escala con el viewBox del <svg>
         que lo contiene: viewBox="-470 -470 940 1340" muestra flor + tallo completos.
           - disco con semillas en filotaxis (ángulo áureo 137,508°): centro oliva,
             anillo marrón y borde dorado (las flores del disco que ya abrieron),
           - brácteas verdes, dos coronas de pétalos con degradé, nervadura y variación,
           - brillo del disco, tallo, dos hojas y resplandor cálido atrás.
         Cada pieza trae su retardo (--d) para "florecer" con hs2627.css: semillas en
         espiral de adentro hacia afuera y pétalos que se despliegan. El tallo se mece.
  campo  lote de girasol a contraluz para el fondo (1080 × 520, horizonte arriba):
         filas de capítulos con pétalos encendidos por el sol, en perspectiva.

    python3 scripts/lib/girasol.py defs
    python3 scripts/lib/girasol.py flor --t0 0 --t1 .7
    python3 scripts/lib/girasol.py flor --estatico
    python3 scripts/lib/girasol.py campo

Para meterlo en una pieza sin copiar a mano: marcá el lugar con
<!--@girasol flor --t0 0--><!--/@girasol--> y corré scripts/lib/inyectar-girasol.py.
"""
import math, random, argparse

GOLD = math.radians(137.508)
RD = 200          # radio del disco (todo el dibujo escala con el viewBox)
BASE = RD * 4.2   # pie del tallo


def mezcla(c1, c2, t):
    c1 = [int(c1[i:i+2], 16) for i in (1, 3, 5)]
    c2 = [int(c2[i:i+2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


def color_semilla(t):
    # t: 0 centro → 1 borde del disco
    tramos = [(0.00, '#6b6a22'), (0.14, '#4a4a18'), (0.22, '#2c1d0c'), (0.62, '#3d2710'),
              (0.78, '#6a4212'), (0.88, '#b87818'), (1.00, '#f0b52a')]
    for (a, ca), (b, cb) in zip(tramos, tramos[1:]):
        if t <= b:
            return mezcla(ca, cb, (t - a) / (b - a))
    return tramos[-1][1]


def defs():
    return ('<defs>'
            '<radialGradient id="gs-glow"><stop offset="0" stop-color="#FFB23A" stop-opacity=".55"/>'
            '<stop offset=".45" stop-color="#F5A623" stop-opacity=".18"/><stop offset="1" stop-color="#F5A623" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="gs-pf" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#C87404"/>'
            '<stop offset=".18" stop-color="#EE9E12"/><stop offset=".5" stop-color="#FDBB26"/><stop offset="1" stop-color="#FFDF78"/></linearGradient>'
            '<linearGradient id="gs-pb" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#9A5503"/>'
            '<stop offset=".5" stop-color="#DC9416"/><stop offset="1" stop-color="#F2B940"/></linearGradient>'
            '<radialGradient id="gs-disco"><stop offset="0" stop-color="#3a3413"/><stop offset=".7" stop-color="#23160a"/>'
            '<stop offset="1" stop-color="#5a3810"/></radialGradient>'
            '<radialGradient id="gs-brillo" cx=".36" cy=".3" r=".75"><stop offset="0" stop-color="#FFF3C4" stop-opacity=".22"/>'
            '<stop offset=".5" stop-color="#FFF3C4" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></radialGradient>'
            '<linearGradient id="gs-tallo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2F5A22"/>'
            '<stop offset=".5" stop-color="#4E8A34"/><stop offset="1" stop-color="#2A4F1D"/></linearGradient>'
            '<linearGradient id="gs-hoja" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5C9A3C"/>'
            '<stop offset="1" stop-color="#2C5520"/></linearGradient>'
            '<linearGradient id="gs-pf2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#B8760C"/>'
            '<stop offset=".25" stop-color="#E0A018"/><stop offset=".7" stop-color="#F2B92E"/><stop offset="1" stop-color="#F7CB55"/></linearGradient>'
            '<linearGradient id="gs-pb2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#8E5808"/>'
            '<stop offset=".5" stop-color="#C98C14"/><stop offset="1" stop-color="#E3AE35"/></linearGradient>'
            '<linearGradient id="gs-hoja2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#557F35"/>'
            '<stop offset=".55" stop-color="#3D6526"/><stop offset="1" stop-color="#27461A"/></linearGradient>'
            '<linearGradient id="gs-tallo2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2E4F1E"/>'
            '<stop offset=".45" stop-color="#5B8A3A"/><stop offset="1" stop-color="#284519"/></linearGradient>'
            '<linearGradient id="gs-cielo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1a10"/>'
            '<stop offset="1" stop-color="#0d0906"/></linearGradient>'
            + simbolos_lote() +
            '</defs>')


def _petalos(n, r0, r1, w, rnd, desde=0, hasta=360):
    out = []
    for k in range(n):
        a = desde + (hasta - desde) * (k + 0.5) / n + rnd.uniform(-4, 4)
        L1 = r1 * rnd.uniform(0.92, 1.06)
        out.append(f'<path transform="rotate({a:.0f})" d="M 0 {-r0} C {w} {-r0 - (L1 - r0)*0.35:.1f} {w*0.6:.1f} {-L1*0.92:.1f} 0 {-L1:.1f} '
                   f'C {-w*0.6:.1f} {-L1*0.92:.1f} {-w} {-r0 - (L1 - r0)*0.35:.1f} 0 {-r0} Z"/>')
    return ''.join(out)


def simbolos_lote():
    """Capítulos para el lote de fondo: se dibujan una vez y se reusan con <use> (liviano)."""
    rnd = random.Random(5)
    grad = lambda i, a, b, c: (f'<radialGradient id="{i}" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="50">'
                               f'<stop offset=".52" stop-color="{a}"/><stop offset=".76" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></radialGradient>')
    return (grad('gs-lp', '#8A4E0E', '#E6961F', '#FFD36A') + grad('gs-lpo', '#2e1b0a', '#7A4512', '#B8721F') +
            f'<g id="gs-cab"><g fill="url(#gs-lp)">{_petalos(18, 26, 50, 7, rnd)}</g>'
            '<circle r="29" fill="#1d130a"/><circle r="28" fill="none" stroke="#7a4a14" stroke-width="3"/></g>'
            f'<g id="gs-cab-o"><g fill="url(#gs-lpo)">{_petalos(18, 26, 50, 7, rnd)}</g>'
            '<circle r="29" fill="#150e07"/><circle r="28" fill="none" stroke="#4a2c0c" stroke-width="3"/></g>'
            f'<g id="gs-cab-dorso"><g fill="#C47A1C">{_petalos(11, 28, 47, 7, rnd, -80, 80)}</g>'
            '<circle r="33" fill="#120d08"/><path d="M -30 -13 A 33 33 0 0 1 24 -23" stroke="#FFB23A" stroke-opacity=".55" stroke-width="3" fill="none"/></g>'
            '<path id="gs-hoja-s" d="M 0 0 C 14 -15 38 -15 58 -4 C 40 9 16 11 0 0 Z" fill="#100b07"/>')


def flor(N=720, petalos=34, t0=0.0, t_sem=1.5, t1=1.0, tallo=True, semilla=7, anim=True, mece=True):
    """t0: arranque de las semillas · t1: arranque de los pétalos.
    El disco y el tallo ya están en el cuadro 0 (así el primer cuadro ya dice 'girasol')."""
    rnd = random.Random(semilla)
    o = []
    cls = lambda c: f' class="{c}"' if anim else ''
    Rd = RD
    if anim and mece:
        o.append(f'<g class="gs-mece" style="transform-origin:0px {BASE:.0f}px">')
    o.append(f'<circle{cls("gs-glow")} r="{Rd*2.7:.0f}" fill="url(#gs-glow)"/>')
    if tallo:
        L = BASE
        o.append('<g>'
                 f'<path d="M -22 {Rd*0.8:.0f} C -36 {Rd*1.8:.0f} 20 {Rd*2.8:.0f} -13 {L:.0f} L 19 {L:.0f} C 48 {Rd*2.8:.0f} 16 {Rd*1.8:.0f} 22 {Rd*0.8:.0f} Z" fill="url(#gs-tallo)"/>'
                 f'<path d="M 4 {Rd*2.3:.0f} C 90 {Rd*1.9:.0f} 230 {Rd*2.0:.0f} 300 {Rd*2.35:.0f} C 220 {Rd*2.7:.0f} 90 {Rd*2.75:.0f} 4 {Rd*2.3:.0f} Z" fill="url(#gs-hoja)"/>'
                 f'<path d="M 4 {Rd*2.3:.0f} C 110 {Rd*2.28:.0f} 200 {Rd*2.3:.0f} 290 {Rd*2.35:.0f}" stroke="#244a18" stroke-width="3" fill="none" opacity=".6"/>'
                 f'<path d="M -2 {Rd*3.05:.0f} C -90 {Rd*2.65:.0f} -230 {Rd*2.75:.0f} -300 {Rd*3.1:.0f} C -220 {Rd*3.45:.0f} -90 {Rd*3.5:.0f} -2 {Rd*3.05:.0f} Z" fill="url(#gs-hoja)"/>'
                 f'<path d="M -2 {Rd*3.05:.0f} C -110 {Rd*3.03:.0f} -200 {Rd*3.05:.0f} -290 {Rd*3.1:.0f}" stroke="#244a18" stroke-width="3" fill="none" opacity=".6"/>'
                 '</g>')
    o.append(f'<g{cls("gs-cabeza")}>')
    # brácteas: puntas verdes que asoman entre los pétalos de atrás
    for k in range(26):
        ang = 360 * (k + 0.25) / 26 + rnd.uniform(-3, 3)
        L = Rd * rnd.uniform(0.34, 0.46)
        w = Rd * 0.11
        y0 = -Rd * 0.9
        o.append(f'<path transform="rotate({ang:.1f})" d="M {-w:.1f} {y0:.1f} Q {-w*0.5:.1f} {y0 - L*0.7:.1f} 0 {y0 - L:.1f} '
                 f'Q {w*0.5:.1f} {y0 - L*0.7:.1f} {w:.1f} {y0:.1f} Z" fill="#3E6B26"/>')

    # coronas de pétalos (atrás más larga y oscura, adelante desfasada medio paso)
    def corona(n, r0, largo, ancho, grad, desf, tb, capa):
        for k in range(n):
            ang = 360 * (k + desf) / n + rnd.uniform(-2.2, 2.2)
            L = largo * rnd.uniform(0.9, 1.08)
            w = ancho * rnd.uniform(0.86, 1.1)
            dx = rnd.uniform(-8, 8)
            y0, y1 = -r0, -r0 - L
            d = (f'M 0 {y0:.1f} C {w:.1f} {y0 - L*0.28:.1f} {w*0.72:.1f} {y0 - L*0.86:.1f} {dx:.1f} {y1:.1f} '
                 f'C {-w*0.72:.1f} {y0 - L*0.86:.1f} {-w:.1f} {y0 - L*0.28:.1f} 0 {y0:.1f} Z')
            rib = f'M 0 {y0 - 6:.1f} Q {dx*0.4:.1f} {y0 - L*0.5:.1f} {dx*0.8:.1f} {y0 - L*0.78:.1f}'
            dd = tb + rnd.uniform(0, 0.45)
            st = f' style="--d:{dd:.2f}s"' if anim else ''
            o.append(f'<g transform="rotate({ang:.1f})"><g{cls("gs-p")}{st}>'
                     f'<path d="{d}" fill="url(#{grad})"/>'
                     f'<path d="{rib}" stroke="#B86A04" stroke-width="3" fill="none" opacity="{.35 if capa else .25}"/></g></g>')
    corona(petalos, Rd*0.93, Rd*1.12, Rd*0.19, 'gs-pb', 0.5, t1, 0)
    corona(petalos, Rd*0.95, Rd*1.0, Rd*0.18, 'gs-pf', 0.0, t1 + 0.15, 1)

    # disco y semillas
    o.append(f'<circle r="{Rd*1.0:.0f}" fill="url(#gs-disco)"/>')
    c = (Rd * 0.97) / math.sqrt(N)
    for n in range(1, N + 1):
        r = c * math.sqrt(n)
        a = n * GOLD
        x, y = r * math.cos(a), r * math.sin(a)
        t = r / (Rd * 0.97)
        s = c * (0.8 + 0.36 * t)
        ux, uy = (math.cos(a), math.sin(a))
        vx, vy = -uy, ux
        Lh, Wh = s * 0.95, s * 0.62
        pts = [(x + ux*Lh, y + uy*Lh), (x + vx*Wh, y + vy*Wh), (x - ux*Lh, y - uy*Lh), (x - vx*Wh, y - vy*Wh)]
        path = 'M ' + ' L '.join(f'{px:.1f} {py:.1f}' for px, py in pts) + ' Z'
        st = f' style="--d:{t0 + t_sem * math.sqrt(n / N):.2f}s"' if anim else ''
        col = color_semilla(t)
        v = rnd.uniform(-0.16, 0.12)
        col = mezcla(col, '#000000', -v) if v < 0 else mezcla(col, '#ffe9a8', v)
        o.append(f'<path{cls("gs-s")}{st} d="{path}" fill="{col}"/>')
    # florcitas del disco abiertas, con polen, en el anillo de afuera
    pol = []
    for k in range(150):
        a = rnd.uniform(0, 2 * math.pi)
        r = Rd * math.sqrt(rnd.uniform(0.74, 0.95))
        pol.append(f'<circle cx="{r*math.cos(a):.1f}" cy="{r*math.sin(a):.1f}" r="{rnd.uniform(1.8, 3.4):.1f}"/>')
    st = f' style="--d:{t0 + t_sem*0.9:.2f}s"' if anim else ''
    o.append(f'<g{cls("a-fade")}{st} fill="#FFD76A" opacity=".75">{"".join(pol)}</g>')
    # volumen: luz arriba a la izquierda, sombra abajo
    o.append(f'<circle r="{Rd*0.99:.0f}" fill="url(#gs-brillo)"/>')
    o.append(f'<circle r="{Rd*0.985:.0f}" fill="none" stroke="#F5A623" stroke-opacity=".2" stroke-width="3"/>')
    o.append('</g>')
    if anim and mece:
        o.append('</g>')
    return '\n'.join(o)


def _hoja_real(L, W, rnd, n=32):
    """Hoja de girasol: acorazonada (dos lóbulos detrás de la inserción del pecíolo), más ancha
    en el primer tercio, punta aguda, borde aserrado, nervadura central y 5 pares de laterales.
    Coordenadas locales: inserción del pecíolo en 0,0 y la punta en (L*0.88, 0)."""
    def ancho(t):
        if t < 0.36:
            return W * (0.3 + 0.7 * math.sin(math.pi / 2 * t / 0.36))
        return W * (math.cos(math.pi / 2 * (t - 0.36) / 0.64) ** 0.85)
    arriba, abajo = [], []
    for i in range(n + 1):
        t = i / n
        x = L * (t - 0.12)
        hw = ancho(t) * (1 + (0.04 if i % 2 else -0.02) * (0.4 + t))
        arriba.append((x, -hw))
        abajo.append((x, hw))
    contorno = [(0, 0), (-L * 0.05, -W * 0.13)] + arriba + abajo[::-1] + [(-L * 0.05, W * 0.13)]
    d = 'M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in contorno) + ' Z'
    venas = [f'M 0 0 Q {L*0.42:.1f} {W*0.04:.1f} {L*0.84:.1f} 0']
    for k in range(1, 6):
        t = 0.1 + k * 0.12
        x0 = L * (t - 0.12)
        hw = ancho(t) * 0.8
        venas.append(f'M {x0:.1f} 0 Q {x0 + hw*0.3:.1f} {-hw*0.6:.1f} {x0 + hw*0.75:.1f} {-hw:.1f}')
        venas.append(f'M {x0:.1f} 0 Q {x0 + hw*0.3:.1f} {hw*0.6:.1f} {x0 + hw*0.75:.1f} {hw:.1f}')
    return d, ' '.join(venas)


def flor2(N=1100, petalos=46, t0=0.0, t_sem=1.5, t1=0.3, tallo=True, semilla=11, anim=True, mece=True):
    """Girasol 'serio': proporciones de un girasol de lote (disco grande, pétalos cortos y finos),
    brácteas verdes, capítulo apenas inclinado, tallo grueso con cuello y hojas acorazonadas
    aserradas con nervaduras. Mismas coordenadas que flor(): centro del capítulo en 0,0 y pie
    del tallo en y = 840 (viewBox="-470 -470 940 1340")."""
    rnd = random.Random(semilla)
    o = []
    cls = lambda c: f' class="{c}"' if anim else ''
    Rd = 232
    if anim and mece:
        o.append(f'<g class="gs-mece" style="transform-origin:0px {BASE:.0f}px">')
    o.append(f'<circle{cls("gs-glow")} r="{Rd*2.2:.0f}" fill="url(#gs-glow)" opacity=".7"/>')
    if tallo:
        L = BASE
        # tallo grueso, con el cuello que se curva bajo el capítulo
        o.append('<g>'
                 f'<path d="M -36 {Rd*0.62:.0f} C -48 {Rd*1.4:.0f} -12 {Rd*2.3:.0f} -24 {L:.0f} L 28 {L:.0f} '
                 f'C 34 {Rd*2.3:.0f} 22 {Rd*1.4:.0f} 38 {Rd*0.62:.0f} Z" fill="url(#gs-tallo2)"/>'
                 f'<path d="M -6 {Rd*0.7:.0f} C -14 {Rd*1.5:.0f} 6 {Rd*2.4:.0f} 0 {L:.0f}" stroke="#7FA85A" stroke-opacity=".35" stroke-width="4" fill="none"/>')
        for (y, lado, Lh, Wh, ang) in [(Rd*1.75, 1, 330, 104, 38), (Rd*2.5, -1, 350, 110, 44), (Rd*3.2, 1, 300, 96, 50)]:
            d, venas = _hoja_real(Lh, Wh, rnd)
            px = lado * 78
            o.append(f'<path d="M {lado*16:.0f} {y:.0f} Q {lado*46:.0f} {y - 34:.0f} {px:.0f} {y - 20:.0f}" stroke="#3D6526" stroke-width="11" stroke-linecap="round" fill="none"/>')
            o.append(f'<g transform="translate({px:.0f} {y - 20:.0f}) scale({lado} 1) rotate({ang})">'
                     f'<path d="{d}" fill="url(#gs-hoja2)"/>'
                     f'<path d="{venas}" stroke="#86B060" stroke-opacity=".45" stroke-width="3" fill="none" stroke-linecap="round"/></g>')
        o.append('</g>')
    o.append(f'<g{cls("gs-cabeza")}>')
    o.append('<g transform="rotate(-7) scale(1 .94)">')
    # brácteas: puntas verdes entre los pétalos
    for k in range(34):
        ang = 360 * (k + 0.5) / 34 + rnd.uniform(-3, 3)
        Lb = Rd * rnd.uniform(0.2, 0.3)
        w = Rd * 0.07
        y0 = -Rd * 0.96
        o.append(f'<path transform="rotate({ang:.1f})" d="M {-w:.1f} {y0:.1f} Q {-w*0.4:.1f} {y0 - Lb*0.7:.1f} 0 {y0 - Lb:.1f} '
                 f'Q {w*0.4:.1f} {y0 - Lb*0.7:.1f} {w:.1f} {y0:.1f} Z" fill="#3B5F24"/>')

    def corona(n, r0, largo, ancho, grad, desf, tb, capa):
        for k in range(n):
            ang = 360 * (k + desf) / n + rnd.uniform(-2.5, 2.5)
            Lp = largo * rnd.uniform(0.82, 1.12)
            w = ancho * rnd.uniform(0.85, 1.15)
            dx = rnd.uniform(-6, 6)
            y0, y1 = -r0, -r0 - Lp
            d = (f'M 0 {y0:.1f} C {w:.1f} {y0 - Lp*0.22:.1f} {w*0.8:.1f} {y0 - Lp*0.78:.1f} {dx:.1f} {y1:.1f} '
                 f'C {-w*0.8:.1f} {y0 - Lp*0.78:.1f} {-w:.1f} {y0 - Lp*0.22:.1f} 0 {y0:.1f} Z')
            rib = (f'M {-w*0.3:.1f} {y0 - 4:.1f} Q {dx*0.2 - w*0.25:.1f} {y0 - Lp*0.5:.1f} {dx*0.6 - w*0.1:.1f} {y0 - Lp*0.85:.1f} '
                   f'M {w*0.3:.1f} {y0 - 4:.1f} Q {dx*0.2 + w*0.25:.1f} {y0 - Lp*0.5:.1f} {dx*0.6 + w*0.1:.1f} {y0 - Lp*0.85:.1f}')
            dd = tb + rnd.uniform(0, 0.5)
            st = f' style="--d:{dd:.2f}s"' if anim else ''
            o.append(f'<g transform="rotate({ang:.1f})"><g{cls("gs-p")}{st}>'
                     f'<path d="{d}" fill="url(#{grad})"/>'
                     f'<path d="{rib}" stroke="#9C6408" stroke-width="2" fill="none" opacity="{.3 if capa else .22}"/></g></g>')
    corona(petalos, Rd*0.95, Rd*0.66, Rd*0.085, 'gs-pb2', 0.5, t1, 0)
    corona(petalos, Rd*0.97, Rd*0.58, Rd*0.08, 'gs-pf2', 0.0, t1 + 0.12, 1)

    # disco
    o.append(f'<circle r="{Rd*1.0:.0f}" fill="url(#gs-disco)"/>')
    c = (Rd * 0.97) / math.sqrt(N)
    for n in range(1, N + 1):
        r = c * math.sqrt(n)
        a = n * GOLD
        x, y = r * math.cos(a), r * math.sin(a)
        t = r / (Rd * 0.97)
        sz = c * (0.82 + 0.3 * t)
        ux, uy = (math.cos(a), math.sin(a))
        vx, vy = -uy, ux
        Lh, Wh = sz * 0.95, sz * 0.62
        pts = [(x + ux*Lh, y + uy*Lh), (x + vx*Wh, y + vy*Wh), (x - ux*Lh, y - uy*Lh), (x - vx*Wh, y - vy*Wh)]
        path = 'M ' + ' L '.join(f'{px:.1f} {py:.1f}' for px, py in pts) + ' Z'
        st = f' style="--d:{t0 + t_sem * math.sqrt(n / N):.2f}s"' if anim else ''
        col = color_semilla(t)
        v = rnd.uniform(-0.18, 0.08)
        col = mezcla(col, '#000000', -v) if v < 0 else mezcla(col, '#ffe9a8', v)
        o.append(f'<path{cls("gs-s")}{st} d="{path}" fill="{col}"/>')
    pol = []
    for k in range(220):
        a = rnd.uniform(0, 2 * math.pi)
        r = Rd * math.sqrt(rnd.uniform(0.8, 0.96))
        pol.append(f'<circle cx="{r*math.cos(a):.1f}" cy="{r*math.sin(a):.1f}" r="{rnd.uniform(1.6, 3.0):.1f}"/>')
    st = f' style="--d:{t0 + t_sem*0.9:.2f}s"' if anim else ''
    o.append(f'<g{cls("a-fade")}{st} fill="#E9C25A" opacity=".7">{"".join(pol)}</g>')
    o.append(f'<circle r="{Rd*0.99:.0f}" fill="url(#gs-brillo)"/>')
    o.append('</g></g>')
    if anim and mece:
        o.append('</g>')
    return '\n'.join(o)


def disco(N=900, t0=0.0, t_sem=2.0, semilla=8):
    """Solo el disco (macro): semillas en filotaxis y florcitas con polen, sin pétalos.
    Radio 200 centrado en 0,0: se agranda con el viewBox para llenar la pantalla."""
    rnd = random.Random(semilla)
    Rd = RD
    o = [f'<circle r="{Rd*1.0:.0f}" fill="url(#gs-disco)"/>']
    c = (Rd * 0.97) / math.sqrt(N)
    for n in range(1, N + 1):
        r = c * math.sqrt(n)
        a = n * GOLD
        x, y = r * math.cos(a), r * math.sin(a)
        t = r / (Rd * 0.97)
        s = c * (0.8 + 0.36 * t)
        ux, uy = (math.cos(a), math.sin(a))
        vx, vy = -uy, ux
        Lh, Wh = s * 0.95, s * 0.62
        pts = [(x + ux*Lh, y + uy*Lh), (x + vx*Wh, y + vy*Wh), (x - ux*Lh, y - uy*Lh), (x - vx*Wh, y - vy*Wh)]
        col = color_semilla(t)
        v = rnd.uniform(-0.16, 0.12)
        col = mezcla(col, '#000000', -v) if v < 0 else mezcla(col, '#ffe9a8', v)
        path = 'M ' + ' L '.join(f'{px:.1f} {py:.1f}' for px, py in pts) + ' Z'
        o.append(f'<path class="gs-s" style="--d:{t0 + t_sem * math.sqrt(n / N):.2f}s" d="{path}" fill="{col}" stroke="#F5A623" stroke-opacity="{0.25 + 0.3*t:.2f}" stroke-width=".7"/>')
    pol = []
    for k in range(260):
        a = rnd.uniform(0, 2 * math.pi)
        r = Rd * math.sqrt(rnd.uniform(0.72, 0.96))
        pol.append(f'<circle cx="{r*math.cos(a):.1f}" cy="{r*math.sin(a):.1f}" r="{rnd.uniform(0.9, 1.8):.1f}"/>')
    o.append(f'<g class="a-fade" style="--d:{t0 + t_sem*0.9:.2f}s" fill="#FFD76A" opacity=".8">{"".join(pol)}</g>')
    return '\n'.join(o)


def campo(ancho=1080, alto=520, horizonte=34, semilla=3):
    """Lote de girasol a contraluz. Devuelve el contenido de un <svg viewBox="0 0 ancho alto">.
    Filas en perspectiva: en el horizonte capítulos chicos y encendidos por el sol; adelante,
    grandes, oscuros y algunos de espaldas (el capítulo del girasol cae: "muy decumbente")."""
    rnd = random.Random(semilla)
    o = [f'<rect y="{horizonte}" width="{ancho}" height="{alto - horizonte}" fill="url(#gs-cielo)"/>',
         f'<rect y="{horizonte - 2}" width="{ancho}" height="3" fill="#FFB23A" opacity=".55"/>']
    filas = [(3, 5, 15), (9, 6.5, 19), (18, 8.5, 24), (31, 11, 30), (50, 14, 38), (78, 18.5, 48),
             (118, 24, 62), (178, 31, 80), (268, 41, 104), (400, 55, 138)]
    for i, (dy, R, sep) in enumerate(filas):
        y = horizonte + dy
        tallos, capas = [], []
        x = -rnd.uniform(0, sep)
        while x < ancho + sep:
            xx = x + rnd.uniform(-sep * 0.2, sep * 0.2)
            yy = y + rnd.uniform(-R * 0.3, R * 0.3)
            rr = R * rnd.uniform(0.85, 1.12)
            k = rr / 40
            inc = rnd.uniform(-24, 24)
            tallos.append(f'M {xx:.0f} {yy:.0f} L {xx + rr*0.12:.0f} {alto + 10}')
            if R >= 11:
                lado = rnd.choice((-1, 1))
                capas.append(f'<use href="#gs-hoja-s" transform="translate({xx:.0f} {yy + rr*1.9:.0f}) scale({lado*k*1.15:.2f} {k*1.15:.2f}) rotate({rnd.uniform(-20, 10):.0f})"/>')
            if i < 5:
                ref = 'gs-cab'
            elif i < 8:
                ref = rnd.choice(('gs-cab', 'gs-cab-o', 'gs-cab-o', 'gs-cab-dorso'))
            else:
                ref = rnd.choice(('gs-cab-o', 'gs-cab-dorso', 'gs-cab-dorso'))
            capas.append(f'<use href="#{ref}" transform="translate({xx:.0f} {yy:.0f}) rotate({inc:.0f}) scale({k:.3f} {k*rnd.uniform(0.72, 0.9):.3f})"/>')
            x += sep
        o.append(f'<path d="{" ".join(tallos)}" stroke="#0e0a07" stroke-width="{max(1.5, R*0.2):.1f}"/>')
        o.extend(capas)
    return '\n'.join(o)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('que', nargs='?', default='flor', choices=('defs', 'flor', 'flor2', 'campo', 'disco'))
    ap.add_argument('--n', type=int, default=900)
    ap.add_argument('--sin-tallo', action='store_true')
    ap.add_argument('--estatico', action='store_true')
    ap.add_argument('--quieto', action='store_true', help='florece pero no se mece')
    ap.add_argument('--t0', type=float, default=0.0)
    ap.add_argument('--t1', type=float, default=0.8)
    ap.add_argument('--tsem', type=float, default=1.5)
    ap.add_argument('--semilla', type=int, default=7)
    a = ap.parse_args()
    if a.que == 'defs':
        print(defs())
    elif a.que == 'campo':
        print(campo(semilla=a.semilla))
    elif a.que == 'flor2':
        print(flor2(t0=a.t0, t1=a.t1, t_sem=a.tsem, tallo=not a.sin_tallo, anim=not a.estatico, mece=not a.quieto))
    elif a.que == 'disco':
        print(disco(N=a.n, t0=a.t0, t_sem=a.tsem, semilla=a.semilla))
    else:
        print(flor(t0=a.t0, t1=a.t1, t_sem=a.tsem, tallo=not a.sin_tallo, semilla=a.semilla,
                   anim=not a.estatico, mece=not a.quieto))
