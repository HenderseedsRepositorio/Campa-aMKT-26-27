#!/usr/bin/env python3
"""
Kit de publicación: una página para el celular con cada video listo para subir
(video, portada, pasos, caption para copiar y botón para bajar el MP4).

  python3 scripts/armar-kit.py            → docs/kit/index.html  (GitHub Pages, con videos)
  python3 scripts/armar-kit.py --artifact ruta.html  → misma página con portadas embebidas y sin
                                                       videos (para compartir como página suelta)

Los videos y portadas viven en docs/placas/video/ (se commitean, igual que los demás reels del sitio).
Los textos salen de reels/2026-W43-reels-semana.md: si cambia un caption, cambiarlo en los dos lados.
"""
import base64, html, os, subprocess, sys, tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID = 'placas/video'          # relativo a docs/
PAGES = 'https://henderseedsrepositorio.github.io/Campa-aMKT-26-27/'

CAP_R1 = '''¿Quién sigue de cerca tu lote? 🌽🌻
Con Experiencia Nidera, el equipo HenderSeeds te acompaña en cada etapa:
— Antes de sembrar: híbrido y densidad para cada zona del lote, con la base de ensayos de Nidera.
— Al sembrar: mapa de siembra variable para tu sembradora, con la recomendación Nidera o a medida.
— Con el cultivo nacido: control de calidad de siembra con dron (Nidera Vuela).
— Hasta la cosecha: recorridas e informe de cada visita.
¿Querés que recorramos tu lote? Mandanos un DM o escribinos por WhatsApp 📲 wa.me/5492314530691

#Henderseeds #Nidera #ExperienciaNidera #Maiz #Girasol #Henderson #Daireaux #Bolivar'''

# ── Semana: los 4 reels elegidos, en orden de publicación ──
SEMANA = [
 dict(id='r1', dia='Mar 20/10', hora='7–9 h o 20–22 h', fmt='Reel · 31 s',
      video='2026-W43-reel-1-quien-sigue-de-cerca.mp4', portada='2026-W43-reel-1-portada.jpg',
      titulo='¿Quién sigue de cerca tu lote?', obj='Institucional: el acompañamiento Experiencia Nidera en 4 etapas.',
      pasos=[('Portada', 'subí la portada (botón de abajo) o elegí el segundo 2,9.'),
             ('Música', 'instrumental tranquila de la biblioteca de IG, volumen bajo.'),
             ('Opciones', 'compartir en Facebook · ubicación Henderson · invitar a Nidera como colaborador · fijar en el perfil.'),
             ('Historia', 'compartirlo el mismo día con encuesta: "¿Ya medís la calidad de siembra?" Sí / Todavía no. A los "Todavía no", escribirles por DM.')],
      cap=CAP_R1),
 dict(id='r2', dia='Jue 22/10', hora='7–9 h o 20–22 h', fmt='Reel · 24 s',
      video='2026-W43-reel-2-girasol-tolva.mp4', portada='2026-W43-reel-2-portada.jpg',
      titulo='¿Ya tenés el girasol en la tolva?', obj='Arranca el girasol: ventana del oeste según marbete y qué girasol va en cada lote.',
      pasos=[('Portada', 'subí la portada (botón de abajo).'),
             ('Música', 'algo con más ritmo que el video 1, volumen bajo.'),
             ('Ojo', 'el calendario marca "hoy" el 22/10: si se publica otro día, hay que cambiarlo.'),
             ('Historia', 'encuesta: "¿Ya arrancaste con el girasol?" Sí / Esta semana / Todavía no.')],
      cap='''¿Ya tenés el girasol en la tolva? 🌻
En el oeste bonaerense la ventana óptima va del 15/10 al 15/11 (fecha límite 20/11), según los marbetes Nidera. Igual para los cuatro: NS 1113 CL, NS 1115 CL, NS 1117 CL y NS 1227 CL HO.
Cada uno tiene su lugar: techo de rinde y aceite, la sanidad más completa, máximo rinde con Phomopsis 2 o alto oleico.
Hay tiempo para sembrar bien. ¿Dudas de densidad o de qué girasol va en tu lote? Pedí tu recomendación por DM o escribinos 📲 wa.me/5492314530691

#Henderseeds #Nidera #Girasol #NS1113CL #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(id='r3', dia='Sáb 24/10', hora='8 h', fmt='Reel · 24 s · pauta desde lun 26',
      video='2026-W43-reel-3-cuantas-plantas.mp4', portada='2026-W43-reel-3-portada.jpg',
      titulo='¿Cuántas plantas lograste?', obj='Tutorial de conteo en 3 pasos que cierra con la planilla: cada comentario abre una conversación.',
      extra=[('Versión pauta', '2026-W43-reel-3-cuantas-plantas-pauta.mp4')],
      pasos=[('Portada', 'subí la portada (botón de abajo).'),
             ('1er comentario', 'fijá uno propio: "Comentá PLANILLA y te la mandamos 📋".'),
             ('Historia', 'compartir el reel con el texto "Comentá PLANILLA en el reel 👆".'),
             ('Pauta', 'desde el lunes 26/10 con la versión pauta (cierra con "Mandanos PLANILLA por DM"): $15.000 por día × 7 días. A las 72 h, si la frecuencia es menor a 2 y el costo por conversación está bien, subir a $20.000.')],
      cap='''¿Cuántas plantas lograste? 🌽
Con una cinta y 15 minutos lo sabés: medís 19,05 m de surco (si sembraste a 52,5 cm; 14,29 m a 70), contás las plantas y multiplicás por 1.000. Eso son tus plantas por hectárea.
Repetilo en 4 o 5 puntos, lomas y bajos por separado, y fijate si nacieron parejas: cuando parte de las plantas nace unos 10 días tarde, el maíz pierde entre 6 y 9 % de rinde (Nafziger y col., 1991, citado por INTA).
📋 Armamos una planilla para llevar al lote, con el logro de implantación, dobles y fallas. Comentá PLANILLA y te la mandamos por DM.
¿Preferís que lo contemos juntos en tu lote? Escribinos 📲 wa.me/5492314530691

#Henderseeds #Nidera #Maiz #Siembra2627 #Implantacion #Henderson #Daireaux #Bolivar'''),
 dict(id='r4', dia='Mar 27/10', hora='7–9 h o 20–22 h', fmt='Reel · 22 s',
      video='2026-W44-reel-4-maiz-tardio.mp4', portada='2026-W44-reel-4-portada.jpg',
      titulo='¿Te queda maíz tardío por definir?', obj='Producto: tres Viptera3 para la tardía, con su diferencial del marbete (sin números de ensayo, regla del 25/09).',
      pasos=[('Portada', 'subí la portada (botón de abajo).'),
             ('Música', 'instrumental, volumen bajo.'),
             ('Historia', 'encuesta: "¿Ya tenés definido el tardío?" Sí / Todavía no. A los "Todavía no", escribirles por DM.')],
      cap='''¿Te queda el maíz tardío por definir? 🌽

Tres opciones Nidera para la siembra tardía, según sus marbetes:

• NS 7765 VIPTERA3: el más completo del portafolio, para temprana y tardía. Quebrado 1.
• NS 7925 VIPTERA3: lanzamiento, con el mejor Spiroplasma del portafolio (3).
• NS 7921 VIPTERA3 CL: el más versátil, con 3 herramientas herbicidas.

Cuál va depende del lote, de las malezas que vengas peleando y de la presión de chicharrita en la zona. Eso lo vemos juntos.

📩 Pedí tu recomendación por DM · wa.me/5492314530691

#Henderseeds #Nidera #MaizTardio #NS7765 #Siembra2627 #Henderson #Daireaux #Bolivar'''),
]

# ── Más opciones: se completa en BANCO (ver abajo) ──
BANCO = []
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from kit_banco import BANCO  # opciones extra, en archivo aparte
except ImportError:
    pass


def uri(path, ancho):
    with tempfile.NamedTemporaryFile(suffix='.jpg') as t:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', f'scale={ancho}:-2', '-q:v', '5', t.name], check=True)
        return 'data:image/jpeg;base64,' + base64.b64encode(open(t.name, 'rb').read()).decode()


def ficha(f, modo, publicado=True):
    e = html.escape
    portada_src = uri(os.path.join(RAIZ, 'docs', VID, f['portada']), 240) if modo == 'artifact' else f'../{VID}/{f["portada"]}'
    if modo == 'pages':
        media = (f'<video controls playsinline preload="none" poster="../{VID}/{f["portada"]}" src="../{VID}/{f["video"]}"></video>')
        bajar = (f'<a class="btn sec" href="../{VID}/{f["video"]}" download>Bajar video</a>'
                 f'<a class="btn sec" href="../{VID}/{f["portada"]}" download>Bajar portada</a>')
        for nom, arch in f.get('extra', []):
            bajar += f'<a class="btn sec" href="../{VID}/{arch}" download>Bajar {e(nom.lower())}</a>'
    else:
        media = f'<img src="{portada_src}" alt="Portada: {e(f["titulo"])}">'
        bajar = f'<a class="btn sec" href="{PAGES}kit/#{f["id"]}" target="_blank" rel="noopener">Bajar video (sitio)</a>'
    pasos = ''.join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a, b in f.get('pasos', []))
    chips = (f'<span class="chip dia">{e(f["dia"])}</span><span class="chip">{e(f["hora"])}</span>' if f.get('dia') else '') + f'<span class="chip">{e(f["fmt"])}</span>'
    marca = f'<label class="hecho"><input type="checkbox" id="hecho-{f["id"]}"> Publicado</label>' if publicado else ''
    cap = (f'<div class="cap"><pre id="cap-{f["id"]}">{e(f["cap"])}</pre>'
           f'<div class="acciones"><button class="btn" data-copiar-de="cap-{f["id"]}">Copiar caption</button>{bajar}<span class="ok" aria-live="polite"></span></div></div>') if f.get('cap') else f'<div class="acciones">{bajar}</div>'
    nota = f'<p class="nota">{f["nota"]}</p>' if f.get('nota') else ''
    return f'''
    <article class="ficha" id="{f['id']}" data-id="{f['id'] if publicado else ''}">
      <div class="top">{chips}{marca}</div>
      <div class="cab"><div class="media">{media}</div>
        <div><h3>{e(f['titulo'])}</h3><p>{e(f['obj'])}</p></div></div>
      {f'<ul class="pasos">{pasos}</ul>' if pasos else ''}{nota}
      {cap}
    </article>'''


def armar(modo):
    t = open(os.path.join(RAIZ, 'scripts/lib/kit.html')).read()
    semana = ''.join(ficha(f, modo) for f in SEMANA)
    banco = ''.join(f'<h3 class="grupo">{html.escape(g["grupo"])}</h3><p class="grupo-d">{g["desc"]}</p>' + ''.join(ficha(f, modo, publicado=False) for f in g['items']) for g in BANCO)
    planilla = '../recursos/planilla-conteo-plantas.jpg' if modo == 'pages' else uri(os.path.join(RAIZ, 'docs/recursos/out/planilla-conteo-plantas.jpg'), 900)
    bajar_pl = ('<a class="btn sec" href="../recursos/planilla-conteo-plantas.jpg" download>Bajar imagen</a>'
                '<a class="btn sec" href="../recursos/planilla-conteo-plantas.pdf" download>Bajar PDF</a>') if modo == 'pages' else ''
    sitio = '' if modo == 'pages' else f'<p class="lead">Videos para bajar: <a href="{PAGES}kit/" target="_blank" rel="noopener">{PAGES}kit/</a></p>'
    return (t.replace('<!--SEMANA-->', semana).replace('<!--BANCO-->', banco or '<p class="lead">—</p>')
             .replace('{{PLANILLA}}', planilla).replace('<!--BAJAR_PLANILLA-->', bajar_pl).replace('<!--SITIO-->', sitio)
             .replace('{{CABEZA}}', '<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">' if modo == 'pages' else '')
             .replace('{{CIERRE_HEAD}}', '</head><body>' if modo == 'pages' else '')
             .replace('{{PIE}}', '</body></html>' if modo == 'pages' else ''))


if __name__ == '__main__':
    if '--artifact' in sys.argv:
        salida = sys.argv[sys.argv.index('--artifact') + 1]
        open(salida, 'w').write(armar('artifact'))
    else:
        os.makedirs(os.path.join(RAIZ, 'docs/kit'), exist_ok=True)
        salida = os.path.join(RAIZ, 'docs/kit/index.html')
        open(salida, 'w').write(armar('pages'))
    print('  listo ->', os.path.relpath(salida, RAIZ), f'({os.path.getsize(salida) // 1024} KB)')
