"""Capítulo de girasol por filotaxis (ángulo áureo 137,508°).

Genera las semillas de un capítulo real: la semilla n va a radio c*sqrt(n)
y ángulo n*137,508°. Se usa como motivo gráfico de las placas de girasol.

    python3 scripts/lib/capitulo.py svg  > docs/assets/girasol-capitulo.svg
    python3 scripts/lib/capitulo.py anim > fragmento con retardos para reels
"""
import math, sys

N = 560          # semillas
C = 13.2         # separación
GOLD = math.radians(137.508)

def semillas():
    for n in range(1, N + 1):
        r = C * math.sqrt(n)
        a = n * GOLD
        x, y = r * math.cos(a), r * math.sin(a)
        s = 3.2 + 3.9 * (r / (C * math.sqrt(N)))   # las de afuera, más grandes
        yield n, x, y, s

def svg(color='#F5A623'):
    R = C * math.sqrt(N) + 12
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-R:.0f} {-R:.0f} {2*R:.0f} {2*R:.0f}" fill="{color}">']
    for n, x, y, s in semillas():
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s:.1f}"/>')
    out.append('</svg>')
    return '\n'.join(out)

def anim(t_total=2.4, color='currentColor'):
    """Semillas con --d creciente: el capítulo 'crece' de adentro hacia afuera."""
    R = C * math.sqrt(N) + 12
    out = [f'<svg class="capitulo" viewBox="{-R:.0f} {-R:.0f} {2*R:.0f} {2*R:.0f}" fill="{color}">']
    for n, x, y, s in semillas():
        d = t_total * math.sqrt(n / N)
        out.append(f'<circle class="a-pop" style="--d:{d:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="{s:.1f}"/>')
    out.append('</svg>')
    return '\n'.join(out)

if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'svg'
    print(svg() if modo == 'svg' else anim())
