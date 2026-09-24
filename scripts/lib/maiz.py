"""Planta de maíz en SVG (para reels y placas).

  defs   símbolos: mz-planta (a color: caña con nudos, 11 hojas que se arquean,
         panoja y espiga con barbas) y mz-sil (la misma planta en silueta, para el
         lote de fondo). Van UNA vez por página, dentro del <svg> oculto de símbolos.
         La planta mide 1000 de alto: base en (0,0), panoja en y = -1000.
  lote   fila de plantas en silueta para el horizonte (1080 × 260).

    python3 scripts/lib/maiz.py defs
    python3 scripts/lib/maiz.py lote

Con inyectar-girasol.py: <!--@maiz defs--><!--/@maiz-->
"""
import math, random, argparse


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u**3 * a + 3 * u*u*t * b + 3 * u*t*t * c + t**3 * d for a, b, c, d in zip(p0, p1, p2, p3))


def hoja(y, L, lado, W, rnd, n=18):
    """Contorno de una hoja que sale del nudo (0, y), sube, se arquea y cae."""
    s = lado
    p0 = (s * 6, y)
    p1 = (s * L * 0.22, y - L * 0.5)
    p2 = (s * L * 0.72, y - L * rnd.uniform(0.34, 0.46))
    p3 = (s * L * 0.98, y + L * rnd.uniform(-0.02, 0.14))
    pts = [bez(p0, p1, p2, p3, i / n) for i in range(n + 1)]
    izq, der = [], []
    for i, (x, yy) in enumerate(pts):
        t = i / n
        a = pts[min(i + 1, n)]
        b = pts[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        m = math.hypot(dx, dy) or 1
        nx, ny = -dy / m, dx / m
        w = W * (0.55 + 1.8 * t) if t < 0.25 else W * (1 - (t - 0.25) / 0.75) ** 0.85
        izq.append((x + nx * w / 2, yy + ny * w / 2))
        der.append((x - nx * w / 2, yy - ny * w / 2))
    contorno = izq + der[::-1]
    d = 'M ' + ' L '.join(f'{x:.0f} {yy:.0f}' for x, yy in contorno) + ' Z'
    nerv = 'M ' + ' L '.join(f'{x:.0f} {yy:.0f}' for x, yy in pts[1:-2])
    return d, nerv


def planta(color=True, semilla=4):
    rnd = random.Random(semilla)
    o = []
    # hojas de atrás (las del lado izquierdo quedan atrás de la caña)
    hojas = []
    for i in range(11):
        y = -70 - i * 66
        L = 300 + 260 * math.sin(math.pi * (i + 1.5) / 13)
        lado = -1 if i % 2 == 0 else 1
        hojas.append((i, hoja(y, L, lado, 44 - i * 1.6, rnd)))
    caña = 'M -16 0 C -14 -300 -10 -600 -7 -800 L 7 -800 C 10 -600 14 -300 16 0 Z'
    if color:
        for i, (d, nerv) in hojas:
            f = 'url(#mz-hoja)' if i % 3 else 'url(#mz-hoja2)'
            o.append(f'<path d="{d}" fill="{f}"/><path d="{nerv}" fill="none" stroke="#A9D47A" stroke-opacity=".55" stroke-width="3"/>')
        o.append(f'<path d="{caña}" fill="url(#mz-cana)"/>')
        for k in range(10):
            y = -60 - k * 72
            o.append(f'<path d="M -13 {y} Q 0 {y + 5} 13 {y}" stroke="#2C5A1E" stroke-width="3" fill="none"/>')
        # espiga con chala y barbas
        o.append('<g transform="translate(10 -430) rotate(24)">'
                 '<path d="M 0 0 C 30 -20 40 -120 12 -200 C -8 -150 -22 -60 0 0 Z" fill="url(#mz-chala)"/>'
                 '<path d="M 4 -10 C 18 -60 22 -130 12 -196" stroke="#B9DC8A" stroke-opacity=".5" stroke-width="3" fill="none"/>'
                 '<g stroke="#B7823F" stroke-width="2.4" fill="none" opacity=".95">'
                 '<path d="M 12 -198 q -10 -30 -26 -40"/><path d="M 12 -198 q -2 -34 -14 -52"/><path d="M 12 -198 q 8 -30 2 -56"/>'
                 '<path d="M 12 -198 q 16 -24 18 -48"/><path d="M 12 -198 q 22 -14 32 -34"/></g></g>')
        # panoja
        o.append('<g stroke="#D9C27A" fill="none" stroke-linecap="round">'
                 '<path d="M 0 -800 L 0 -1000" stroke-width="7"/>')
        for k in range(7):
            y = -835 - k * 12
            lado = -1 if k % 2 == 0 else 1
            L = rnd.uniform(90, 140)
            o.append(f'<path d="M 0 {y} q {lado*L*0.5:.0f} {-L*0.35:.0f} {lado*L:.0f} {L*0.25:.0f}" stroke-width="4.5"/>')
        o.append('</g>')
    else:
        for i, (d, nerv) in hojas:
            o.append(f'<path d="{d}"/>')
        o.append(f'<path d="{caña}"/>')
        o.append('<path d="M 10 -430 l 60 -190 l 14 6 z"/>')
        o.append('<g stroke="currentColor" fill="none" stroke-width="7"><path d="M 0 -800 L 0 -1000"/>'
                 '<path d="M 0 -840 q -40 -30 -95 18"/><path d="M 0 -860 q 40 -30 95 18"/><path d="M 0 -880 q -30 -25 -70 10"/></g>')
    return ''.join(o)


def defs():
    return ('<defs>'
            '<linearGradient id="mz-hoja" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6FAE45"/><stop offset="1" stop-color="#2F6420"/></linearGradient>'
            '<linearGradient id="mz-hoja2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8CC05A"/><stop offset="1" stop-color="#3C7427"/></linearGradient>'
            '<linearGradient id="mz-cana" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2E5E20"/><stop offset=".5" stop-color="#6DA844"/><stop offset="1" stop-color="#2A551C"/></linearGradient>'
            '<linearGradient id="mz-chala" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4E8A34"/><stop offset=".6" stop-color="#8FC260"/><stop offset="1" stop-color="#5E9A3E"/></linearGradient>'
            f'<g id="mz-planta">{planta(True)}</g>'
            f'<g id="mz-sil">{planta(False, semilla=9)}</g>'
            '</defs>')


def lote(ancho=1080, alto=260, semilla=2):
    """Maíz en silueta para el horizonte (viewBox 0 0 ancho alto): tres filas, las de atrás
    más chicas y más claras (bruma), la de adelante oscura y sólida hasta abajo."""
    rnd = random.Random(semilla)
    o = []
    for esc, sep, base, col in [(0.11, 30, 150, '#2a1f18'), (0.16, 44, 205, '#1a1410'), (0.23, 64, 262, '#0e0b09')]:
        x = -rnd.uniform(0, sep)
        while x < ancho + sep:
            k = esc * rnd.uniform(0.85, 1.12)
            o.append(f'<use href="#mz-sil" color="{col}" fill="{col}" transform="translate({x + rnd.uniform(-8, 8):.0f} {base + rnd.uniform(-5, 5):.0f}) scale({k * rnd.choice((-1, 1)):.3f} {k:.3f})"/>')
            x += sep
        o.append(f'<rect y="{base - 6}" width="{ancho}" height="{max(0, alto - base + 6)}" fill="{col}"/>')
    return '\n'.join(o)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('que', nargs='?', default='defs', choices=('defs', 'lote'))
    a = ap.parse_args()
    print(defs() if a.que == 'defs' else lote())
