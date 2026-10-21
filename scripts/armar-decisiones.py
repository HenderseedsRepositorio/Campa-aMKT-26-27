#!/usr/bin/env python3
"""
Página de la sesión "Decisiones 26/27" (versión simple): 5 reels cortos + 5 placas 4:5.

  python3 scripts/armar-decisiones.py                    → docs/decisiones/index.html (GitHub Pages, con videos)
  python3 scripts/armar-decisiones.py --artifact ruta    → misma página para Claude (imágenes embebidas,
                                                           videos con link al sitio)

Piezas: produccion/decisiones/sN-*.html (reel + ?formato=placa). Las fichas completas (dN-*.html) quedaron
solo para el cuaderno PDF, para el que pide más detalle. Ver reels/2026-W44-decisiones.md.
"""
import base64, html, os, subprocess, sys, tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = 'https://henderseedsrepositorio.github.io/Campa-aMKT-26-27/'
PDF = 'cuaderno-de-decisiones-26-27.pdf'

FICHAS = [
 dict(n='01', slug='01-sembradora', titulo='¿Te alcanza la sembradora?', pilar='Girasol',
      regla='Si no llega, decidí hoy qué lotes van primero.',
      fuente='Ventana del girasol, Oeste de Buenos Aires: marbetes oficiales Nidera 26/27. Ejemplo rotulado (560 ha ÷ 14 días).',
      cap='''¿Te alcanza la sembradora para el girasol? 🌻
La ventana óptima en el oeste cierra el 15/11 (límite 20/11, marbetes Nidera).
La cuenta: hectáreas que te faltan ÷ días hábiles que quedan = ha por día.
Si tu sembradora no llega, decidí hoy qué lotes van primero.
¿Lo vemos juntos? Mandanos un DM o escribinos 📲 wa.me/5492314530691

#Henderseeds #Nidera #Girasol #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='02', slug='02-girasol', titulo='¿Qué girasol va? Empezá por tu lote.', pilar='Girasol',
      regla='Primero el problema del lote. Después, el rinde.',
      fuente='Marbetes oficiales Nidera 26/27. NS 1113 CL: +2,11 qq/ha y 74 % de éxito en 225 comparaciones Sur + Oeste.',
      cap='''¿Qué girasol va? Empezá por tu lote. 🌻
¿Tuvo Phomopsis? NS 1115 CL o NS 1117 CL (Phomopsis 2).
¿No tuvo? NS 1113 CL, techo de rinde y aceite: +2,11 qq/ha y 74 % de éxito en 225 comparaciones Sur + Oeste.
¿Te pagan alto oleico? NS 1227 CL HO.
Datos de los marbetes oficiales Nidera 26/27. ¿Dudas con tu lote? Mandanos un DM · wa.me/5492314530691

#Henderseeds #Nidera #Girasol #NS1113CL #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='03', slug='03-maiz-tardio', titulo='¿Qué te preocupa más del tardío?', pilar='Maíz tardío',
      regla='Elegí por tu mayor riesgo, no por el promedio.',
      fuente='Perfil sanitario de los marbetes oficiales Nidera 26/27 (1 excelente – 9 deficiente). Sin números de ensayo de maíz.',
      cap='''¿Qué te preocupa más del maíz tardío? 🌽
Chicharrita → NS 7925 (Spiroplasma 3, el mejor del portafolio).
Viento → NS 7765 (Quebrado 1).
Malezas difíciles → NS 7921 CL (3 herramientas herbicidas).
Perfil de los marbetes Nidera: 1 excelente, 9 deficiente. Elegí por tu mayor riesgo y, si querés, lo vemos juntos: Mandanos un DM · wa.me/5492314530691

#Henderseeds #Nidera #MaizTardio #Viptera3 #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='04', slug='04-ambiente', titulo='¿En qué ambiente está tu lote?', pilar='Diagnóstico',
      regla='Clasificalo con varias campañas, no con la mejor.',
      fuente='Escala de ambientes del girasol en los marbetes oficiales Nidera 26/27.',
      cap='''¿En qué ambiente está tu lote? 📍
En girasol, el marbete Nidera los separa por rinde: menos de 1.500, de 1.500 a 2.500, de 2.500 a 3.500 y más de 3.500 kg/ha.
Clasificalo con el promedio de varias campañas, no con la mejor. De eso dependen el híbrido, las plantas y la inversión.
Mandanos los rindes de tus lotes y los clasificamos juntos · wa.me/5492314530691

#Henderseeds #Nidera #Girasol #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='05', slug='05-girasol-o-maiz', titulo='¿Girasol o maíz tardío en ese lote?', pilar='Márgenes',
      regla='Decidí con los dos márgenes al lado, no con el precio de hoy.',
      fuente='Límite del girasol: marbetes oficiales Nidera 26/27, Oeste de Buenos Aires. Calculadora: margen.henderseeds.com.',
      cap='''¿Girasol o maíz tardío en ese lote? 🌻🌽
Que decida la cuenta: rinde, precio, costo y flete, los mismos 4 datos para los dos.
Y ojo: el girasol tiene límite el 20/11 (marbete) y el tardío, el riesgo de chicharrita.
Cargalos en margen.henderseeds.com y compará. ¿La hacemos juntos? Mandanos un DM · wa.me/5492314530691

#Henderseeds #Nidera #Girasol #MaizTardio #Margenes #Siembra2627 #Henderson #Bolivar'''),
]

CALENDARIO = [
 ('Mar 27/10', 'Decisión 01 · ¿Te alcanza la sembradora?', 'Lo que vence primero: la ventana del girasol.'),
 ('Sáb 31/10', 'Decisión 03 · ¿Qué te preocupa más del tardío?', 'Reemplaza al reel 4 (mismos híbridos, ordenados por riesgo).'),
 ('Mar 3/11', 'Decisión 05 · ¿Girasol o maíz tardío?', 'Cuando se asignan los últimos lotes.'),
 ('Jue 5/11', 'Decisión 02 · ¿Qué girasol va?', 'Para reposición y lotes sin híbrido.'),
 ('Mar 10/11', 'Decisión 04 · ¿En qué ambiente está tu lote?', 'Abre la charla del diagnóstico.'),
]


def uri(path, ancho):
    with tempfile.NamedTemporaryFile(suffix='.jpg') as t:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', f'scale={ancho}:-2', '-q:v', '5', t.name], check=True)
        return 'data:image/jpeg;base64,' + base64.b64encode(open(t.name, 'rb').read()).decode()


def ficha(f, modo):
    e = html.escape
    vid = f'../placas/video/2026-W44-decision-{f["slug"]}.mp4'
    portada = f'../placas/video/2026-W44-decision-{f["slug"]}-portada.jpg'
    placa = f'img/decision-{f["n"]}-feed.jpg'
    if modo == 'pages':
        media = (f'<figure class="m9"><video controls playsinline preload="none" poster="{portada}" src="{vid}"></video><figcaption>Reel 18 s</figcaption></figure>'
                 f'<figure class="m45"><img src="{placa}" alt="Placa: {e(f["titulo"])}" loading="lazy"><figcaption>Placa 4:5</figcaption></figure>')
        bajar = f'<a class="btn sec" href="{vid}" download>Bajar reel</a><a class="btn sec" href="{placa}" download>Bajar placa</a>'
    else:
        media = (f'<figure class="m9"><img src="{uri(os.path.join(RAIZ, "docs/placas/video", portada.split("/")[-1]), 360)}" alt="Reel: {e(f["titulo"])}"><figcaption>Reel 18 s · <a href="{PAGES}decisiones/#f{f["n"]}" target="_blank" rel="noopener">ver en el sitio</a></figcaption></figure>'
                 f'<figure class="m45"><img src="{uri(os.path.join(RAIZ, "docs/decisiones", placa), 480)}" alt="Placa: {e(f["titulo"])}"><figcaption>Placa 4:5</figcaption></figure>')
        bajar = f'<a class="btn sec" href="{PAGES}decisiones/#f{f["n"]}" target="_blank" rel="noopener">Bajar reel y placa (sitio)</a>'
    return f'''
  <article class="ficha" id="f{f['n']}">
    <div class="num" aria-hidden="true">{f['n']}</div>
    <div class="cuerpo">
      <p class="eyebrow">Decisión {f['n']} · {e(f['pilar'])}</p>
      <h3>{e(f['titulo'])}</h3>
      <div class="media">{media}</div>
      <p class="se-lleva"><span>Se lleva</span>{e(f['regla'])}</p>
      <details class="cap"><summary>Texto para publicar</summary><pre id="cap-{f['n']}">{e(f['cap'])}</pre></details>
      <div class="acciones"><button type="button" class="btn" data-copiar="cap-{f['n']}">Copiar texto</button>{bajar}<span class="ok" aria-live="polite"></span></div>
      <p class="fuente">{e(f['fuente'])}</p>
    </div>
  </article>'''


CSS = '''
/* Hoja crema, tinta navy, rótulos en DM Mono, marcador ámbar: el registro Técnico de brand/identidad.md.
   Una columna de lectura con el número de cada decisión al margen. */
:root { --papel:#F6F4EE; --papel2:#EFEAE0; --blanco:#FFFFFF; --tinta:#15181E; --navy:#0D2D5E; --gris:#4A5264; --gris2:#6E7689;
  --amber:#F5A623; --amber-osc:#9A6206; --linea:rgba(13,45,94,.14);
  --display:'Archivo Black', 'Arial Black', sans-serif; --body:'DM Sans', system-ui, sans-serif; --mono:'DM Mono', ui-monospace, monospace;
  color-scheme:light; }
* { box-sizing:border-box; }
body { margin:0; background:var(--papel); color:var(--tinta); font:400 17px/1.55 var(--body); -webkit-font-smoothing:antialiased;
  background-image:linear-gradient(rgba(13,45,94,.04) 1px, transparent 1px), linear-gradient(90deg, rgba(13,45,94,.04) 1px, transparent 1px); background-size:36px 36px; }
.wrap { max-width:1080px; margin:0 auto; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); padding-block:0 64px; }
a { color:var(--navy); text-decoration-color:var(--amber); text-decoration-thickness:3px; text-underline-offset:3px; }
.top { display:flex; justify-content:space-between; align-items:center; gap:16px; padding-block:18px; border-bottom:3px solid var(--navy); }
.eyebrow { font:500 12.5px/1.3 var(--mono); letter-spacing:.14em; text-transform:uppercase; color:var(--amber-osc); margin:0; }
.top nav { display:flex; gap:16px; flex-wrap:wrap; font:500 13px var(--mono); }
.top nav a { text-decoration:none; color:var(--gris); }
.hero { padding-block:40px 28px; display:grid; gap:18px; }
h1 { font:400 clamp(44px, 9vw, 104px)/.92 var(--display); letter-spacing:-.035em; color:var(--navy); margin:0; text-wrap:balance; }
h1 .mk { background:linear-gradient(transparent 56%, var(--amber) 56%, var(--amber) 94%, transparent 94%); padding:0 .06em; }
.lead { font-size:clamp(18px, 2.4vw, 22px); line-height:1.45; max-width:58ch; margin:0; color:var(--tinta); }
section { padding-block:34px; border-top:2px solid var(--linea); }
h2 { font:400 clamp(28px, 4.6vw, 44px)/1 var(--display); letter-spacing:-.025em; color:var(--navy); margin:0 0 18px; text-wrap:balance; }
.sub { color:var(--gris); max-width:60ch; margin:0 0 20px; }
.ficha { display:grid; grid-template-columns:120px minmax(0, 1fr); gap:24px; padding-block:34px; border-top:2px solid var(--linea); }
.ficha:first-of-type { border-top:0; padding-top:8px; }
.ficha .num { font:400 96px/.8 var(--display); letter-spacing:-.06em; color:var(--navy); position:sticky; top:calc(env(safe-area-inset-top, 0px) + 16px); align-self:start; }
.ficha .num::after { content:''; display:block; width:56px; height:8px; background:var(--amber); border-radius:3px; margin-top:12px; }
.cuerpo { display:grid; gap:16px; min-width:0; }
.cuerpo h3 { font:400 clamp(26px, 4vw, 40px)/1.02 var(--display); letter-spacing:-.025em; color:var(--navy); margin:0; text-wrap:balance; }
.media { display:flex; gap:14px; align-items:flex-start; flex-wrap:wrap; }
.media figure { margin:0; display:grid; gap:6px; }
.media .m9 { width:min(250px, 44%); }
.media .m45 { width:min(330px, 52%); }
.media video, .media img { width:100%; display:block; border-radius:10px; background:var(--navy); box-shadow:0 14px 34px rgba(13,45,94,.16); }
.media .m9 video, .media .m9 img { aspect-ratio:9/16; object-fit:cover; }
.media .m45 img { aspect-ratio:4/5; object-fit:cover; }
.media figcaption { font:500 12px var(--mono); letter-spacing:.08em; text-transform:uppercase; color:var(--gris2); }
.se-lleva { margin:0; background:var(--navy); color:var(--blanco); border-radius:12px; padding:14px 18px; font-weight:700; font-size:20px; line-height:1.3; display:grid; gap:4px; max-width:600px; }
.se-lleva span { font:500 12px var(--mono); letter-spacing:.12em; text-transform:uppercase; color:var(--amber); }
.fuente { margin:0; font:400 13px/1.5 var(--mono); color:var(--gris2); }
details.cap { border:1.5px solid var(--linea); border-radius:12px; background:var(--papel2); }
details.cap summary { cursor:pointer; padding:12px 16px; font:500 13px var(--mono); letter-spacing:.08em; text-transform:uppercase; color:var(--navy); }
details.cap pre { margin:0; padding:0 16px 16px; white-space:pre-wrap; overflow-wrap:anywhere; font:400 15px/1.5 var(--body); color:var(--tinta); }
.acciones { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
.btn { appearance:none; border:0; cursor:pointer; font:700 15px var(--body); padding:11px 16px; border-radius:8px; background:var(--amber); color:#0A0F1B; text-decoration:none; display:inline-flex; align-items:center; }
.btn.sec { background:var(--blanco); color:var(--navy); font-weight:500; font-size:14px; border:1.5px solid var(--linea); padding:9px 12px; }
.btn:focus-visible, .btn.sec:focus-visible, summary:focus-visible { outline:3px solid var(--navy); outline-offset:2px; }
.ok { font:500 13px var(--mono); color:#2E7D4F; }
.tabla-x { overflow-x:auto; }
.cal { width:100%; border-collapse:collapse; background:var(--blanco); border:1.5px solid var(--linea); }
.cal th, .cal td { text-align:left; padding:11px 14px; border-top:1.5px solid var(--linea); vertical-align:top; }
.cal th { font:500 12px var(--mono); letter-spacing:.1em; text-transform:uppercase; color:var(--papel); background:var(--navy); border:0; }
.cal td:first-child { font:500 14px var(--mono); white-space:nowrap; color:var(--navy); }
.cal td:nth-child(2) { font-weight:700; color:var(--navy); }
.cal td:last-child { color:var(--gris); font-size:15px; }
.extra { display:flex; flex-wrap:wrap; gap:12px; align-items:center; }
footer { font:500 12px var(--mono); color:var(--gris2); padding-top:24px; border-top:2px solid var(--linea); letter-spacing:.04em; }
@media (max-width:820px) {
  .ficha { grid-template-columns:minmax(0, 1fr); gap:10px; }
  .ficha .num { position:static; font-size:64px; }
}
'''

JS = '''
document.querySelectorAll('[data-copiar]').forEach(function (b) {
  b.addEventListener('click', function () {
    var pre = document.getElementById(b.getAttribute('data-copiar')), ok = b.parentNode.querySelector('.ok');
    var hecho = function () { if (ok) { ok.textContent = 'Copiado'; setTimeout(function () { ok.textContent = ''; }, 2200); } };
    var elegir = function () { var d = pre.closest('details'); if (d) d.open = true; var r = document.createRange(); r.selectNodeContents(pre); var s = getSelection(); s.removeAllRanges(); s.addRange(r); if (ok) ok.textContent = 'Seleccionado: copialo'; };
    try { navigator.clipboard.writeText(pre.textContent).then(hecho, elegir); } catch (e) { elegir(); }
  });
});
'''


def armar(modo):
    e = html.escape
    fuentes = ('<link rel="stylesheet" href="../assets/fonts/fuentes.css">' if modo == 'pages' else
               '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&display=swap">')
    pdf = PDF if modo == 'pages' else PAGES + 'decisiones/' + PDF
    nav = ('<nav aria-label="Otras páginas"><a href="../kit/">Kit</a><a href="../estudio/">Estudio</a><a href="../">Dashboard</a></nav>' if modo == 'pages' else
           f'<nav aria-label="Sitio"><a href="{PAGES}decisiones/" target="_blank" rel="noopener">Ver en el sitio</a></nav>')
    cuerpo = f'''
<div class="wrap">
  <header class="top"><p class="eyebrow">HenderSeeds · Siembra 26/27</p>{nav}</header>
  <div class="hero">
    <h1>Decisiones <span class="mk">26/27</span></h1>
    <p class="lead">Cinco reels cortos y cinco placas. Cada uno responde una decisión de estas semanas con pocas palabras: la pregunta, el dato del marbete y una regla para llevarse.</p>
  </div>

  <section>
    {''.join(ficha(f, modo) for f in FICHAS)}
  </section>

  <section>
    <h2>Orden para publicar</h2>
    <p class="sub">Primero lo que vence, que es la ventana del girasol. Cada uno, el mismo día, como Estado de WhatsApp.</p>
    <div class="tabla-x"><table class="cal">
      <thead><tr><th scope="col">Día</th><th scope="col">Reel</th><th scope="col">Por qué</th></tr></thead>
      <tbody>{''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in CALENDARIO)}</tbody>
    </table></div>
  </section>

  <section>
    <h2>Si alguien pide más detalle</h2>
    <p class="sub">Las fichas completas, con todos los datos, quedaron en un PDF para mandar por DM. No van al feed.</p>
    <div class="extra"><a class="btn sec" href="{pdf}" {"download" if modo == "pages" else 'target="_blank" rel="noopener"'}>Bajar las fichas completas (PDF)</a></div>
  </section>

  <footer>HenderSeeds · Distribuidor RED.IN Nidera · Henderson, Daireaux y Bolívar · WhatsApp 2314 53-0691</footer>
</div>
<script>{JS}</script>'''
    if modo == 'pages':
        return ('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                '<title>Decisiones 26/27 · HenderSeeds</title>\n<meta name="description" content="Cinco reels cortos y cinco placas: una decisión de siembra por pieza, con pocas palabras.">\n'
                f'{fuentes}\n<style>{CSS}</style>\n</head>\n<body>{cuerpo}\n</body>\n</html>\n')
    return (f'<title>Decisiones 26/27</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{fuentes}\n<style>{CSS}</style>\n{cuerpo}\n')


if __name__ == '__main__':
    if '--artifact' in sys.argv:
        salida = sys.argv[sys.argv.index('--artifact') + 1]
        open(salida, 'w').write(armar('artifact'))
    else:
        salida = os.path.join(RAIZ, 'docs/decisiones/index.html')
        open(salida, 'w').write(armar('pages'))
    print('  listo ->', os.path.relpath(salida, RAIZ), f'({os.path.getsize(salida) // 1024} KB)')
