"""Rellena los bloques <!--@girasol ARGS--> … <!--/@girasol--> (y <!--@maiz ARGS--> … <!--/@maiz-->)
de una o más piezas HTML con la salida de girasol.py (defs, flor, campo) o maiz.py (defs, lote).
Se puede correr las veces que haga falta: reemplaza lo que haya entre las marcas.

    python3 scripts/lib/inyectar-girasol.py docs/placas/2026-W40-reel-girasol-fecha.html
"""
import re, shlex, subprocess, sys, pathlib

AQUI = pathlib.Path(__file__).parent
BLOQUE = re.compile(r'(<!--@(girasol|maiz) ([^>]*?)-->)(.*?)(<!--/@\2-->)', re.S)

def generar(script, args):
    return subprocess.run([sys.executable, str(AQUI / f'{script}.py'), *shlex.split(args)],
                          check=True, capture_output=True, text=True).stdout.rstrip('\n')

for ruta in sys.argv[1:]:
    p = pathlib.Path(ruta)
    html = p.read_text(encoding='utf-8')
    n = 0
    def reemplazo(m):
        global n
        n += 1
        return f'{m.group(1)}\n{generar(m.group(2), m.group(3))}\n{m.group(5)}'
    nuevo = BLOQUE.sub(reemplazo, html)
    p.write_text(nuevo, encoding='utf-8')
    print(f'{ruta}: {n} bloque(s)')
