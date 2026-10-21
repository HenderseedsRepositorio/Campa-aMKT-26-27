#!/usr/bin/env python3
"""
Página de la sesión "Decisiones 26/27" (5 fichas de decisión: reel + placa + Estado + cuaderno PDF).

  python3 scripts/armar-decisiones.py                    → docs/decisiones/index.html (GitHub Pages, con videos)
  python3 scripts/armar-decisiones.py --artifact ruta    → misma página para Claude (imágenes embebidas,
                                                           videos y PDF con link al sitio)

Las piezas salen de produccion/decisiones/ (ver reels/2026-W44-decisiones.md).
"""
import base64, html, os, subprocess, sys, tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = 'https://henderseedsrepositorio.github.io/Campa-aMKT-26-27/'
PDF = 'cuaderno-de-decisiones-26-27.pdf'
WA = 'wa.me/5492314530691'

FICHAS = [
 dict(n='01', slug='01-sembradora', titulo='¿Te alcanza la sembradora para el girasol?', pilar='Girasol · ritmo de siembra',
      herramienta='Calendario de días hábiles y la cuenta de hectáreas por día.',
      sirve='Ahora: la ventana óptima del oeste cierra el 15/11. Sirve de nuevo después de cada lluvia.',
      regla='Si tu sembradora no llega, decidí hoy qué lotes van antes del 15/11.',
      fuente='Marbetes oficiales Nidera 26/27, Oeste de Buenos Aires (los 4 girasoles). Ejemplo rotulado: 560 ha ÷ 14 días hábiles = 40 ha por día.',
      cap='''¿Te alcanza la sembradora para el girasol? 🌻
En el oeste bonaerense la ventana óptima cierra el 15/11 y el límite es el 20/11 (marbetes Nidera 26/27).
La cuenta es corta: hectáreas que te faltan ÷ días hábiles que quedan. Ejemplo: 560 ha y 21 días; si se pierde 1 de cada 3 por lluvia, piso o roturas, quedan 14 días hábiles: 40 ha por día.
Si tu sembradora no llega a ese número, decidí hoy qué lotes van antes del 15/11.
📌 Guardala para rehacer la cuenta después de cada lluvia.
Comentá FICHAS y te mandamos las 5 fichas de decisión por DM. ¿Tu caso es otro? Escribinos 📲 wa.me/5492314530691

#Henderseeds #Nidera #Girasol #Siembra2627 #Henderson #Daireaux #Bolivar #Agro'''),
 dict(n='02', slug='02-girasol', titulo='¿Qué girasol va? Empezá por tu lote.', pilar='Girasol · qué híbrido',
      herramienta='Árbol de decisión: alto oleico, Phomopsis y prioridad, con los datos de ensayo Sur + Oeste.',
      sirve='Para los lotes de girasol que todavía no tienen híbrido asignado y para la reposición.',
      regla='Primero el problema del lote; después, el techo de rinde.',
      fuente='Marbetes oficiales Nidera 26/27: ensayos a campo Sur + Oeste (diferencia de rinde, % de éxito, comparaciones) y perfil sanitario 1–9.',
      cap='''¿Qué girasol va en tu lote? Empezá por el problema, no por la bolsa. 🌻
• ¿Te pagan alto oleico? → NS 1227 CL HO.
• ¿El lote no tuvo Phomopsis? → NS 1113 CL, techo de rinde y aceite: +2,11 qq/ha y 74 % de éxito en 225 comparaciones Sur + Oeste.
• ¿Tuvo Phomopsis y buscás rinde? → NS 1117 CL (Phomopsis 2): +1,75 qq/ha, 67 % en 73 comparaciones.
• ¿Tuvo Phomopsis y querés la sanidad más completa? → NS 1115 CL (Phomopsis 2, Sclerotinia 2): +1,64 qq/ha, 69 % en 192 comparaciones.
Los cuatro son Clearfield y resistentes a Downy Mildew. Datos: marbetes oficiales Nidera 26/27.
📌 Guardala para la próxima vez que elijas girasol.
Comentá FICHAS y te mandamos las 5 por DM · wa.me/5492314530691

#Henderseeds #Nidera #Girasol #NS1113CL #NS1115CL #NS1117CL #Siembra2627 #Henderson'''),
 dict(n='03', slug='03-maiz-tardio', titulo='Maíz tardío: elegí por tu mayor riesgo.', pilar='Maíz tardío · sanidad',
      herramienta='Mapa de calor con el perfil sanitario de los 6 maíces con lugar en tardía; se marca la columna de cada riesgo.',
      sirve='Antes de cerrar el híbrido del tardío (noviembre y diciembre).',
      regla='Mirá la columna de tu riesgo, no el promedio.',
      fuente='Perfil sanitario y agronómico de los marbetes oficiales Nidera 26/27 (1 excelente – 9 deficiente). Sin números de ensayo de maíz.',
      cap='''Maíz tardío: elegí por tu mayor riesgo. 🌽
Pusimos los seis maíces con lugar en tardía uno al lado del otro, con el perfil del marbete (1 excelente, 9 deficiente):
• Chicharrita (achaparramiento) → Spiroplasma: NS 7925 VIPTERA3, con 3.
• Mal de Río Cuarto → NS 7925 y NS 7765, con 3.
• Viento y quebrado → NS 7765 VIPTERA3, con 1.
• Roya → NS 7818 VIP3, con 1.
• Malezas difíciles → NS 7921 VIPTERA3 CL y NS 7624 VIPTERA3 CL: glifosato, glufosinato e imidazolinonas.
La regla: mirá la columna de tu riesgo, no el promedio.
📌 Guardala. Comentá FICHAS y te mandamos las 5 por DM · wa.me/5492314530691

#Henderseeds #Nidera #MaizTardio #Viptera3 #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='04', slug='04-ambiente', titulo='¿En qué ambiente está tu lote?', pilar='Diagnóstico · ambiente',
      herramienta='Las dos escalas de ambiente del marbete (girasol y maíz) y un lote que cae en su tramo con el promedio de 3 campañas.',
      sirve='Siempre: es el paso 1 del Plan de Campaña. Abre la charla para clasificar los lotes juntos.',
      regla='Clasificá cada lote con varias campañas, no con la mejor.',
      fuente='Escala de ambientes de los marbetes oficiales Nidera 26/27 (girasol; maíz en temprana y tardía). Ejemplo rotulado: (2.100 + 2.600 + 1.900) ÷ 3 = 2.200 kg/ha.',
      cap='''¿En qué ambiente está tu lote? 📍
Antes del híbrido, la densidad o cuánto invertir, va el ambiente. La escala de los marbetes Nidera:
• Girasol: bajo, menos de 1.500 · medio-bajo, 1.500 a 2.500 · medio-alto, 2.500 a 3.500 · alto, más de 3.500 kg/ha.
• Maíz: bajo, menos de 6.000 · medio-bajo, 6.001 a 9.000 · medio-alto, 9.001 a 12.000 · alto, más de 12.000 kg/ha.
Clasificá cada lote con el promedio de varias campañas, no con la mejor.
¿Lo hacemos juntos? Mandanos los rindes de tus lotes por DM y los clasificamos: es el primer paso del Plan de Campaña HenderSeeds.
📌 Guardala. Comentá FICHAS y te mandamos las 5 · wa.me/5492314530691

#Henderseeds #Nidera #Girasol #Maiz #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='05', slug='05-girasol-o-maiz', titulo='¿Girasol o maíz tardío en ese lote?', pilar='Márgenes · el lote que queda',
      herramienta='La misma cuenta para los dos cultivos (4 datos y el margen) y la calculadora de márgenes.',
      sirve='Para el lote que todavía no tiene cultivo asignado, antes del 20/11.',
      regla='Decidí con los dos márgenes al lado, no con el precio de hoy.',
      fuente='Límite del girasol: marbetes oficiales Nidera 26/27, Oeste de Buenos Aires. Sin precios ni costos: van los del lote. Calculadora: margen.henderseeds.com.',
      cap='''¿Girasol o maíz tardío en ese lote que te queda? 🌻🌽
Que decida la cuenta, con los mismos cuatro datos para los dos:
1. Rinde esperado de tu ambiente (ficha 04).
2. Precio a cosecha.
3. Costo directo: semilla, fertilizante, protección y labores.
4. Flete y comercialización: el flete se paga por tonelada y en maíz movés más toneladas por hectárea.
Y dos cosas que no entran en la cuenta: el girasol tiene límite de siembra el 20/11 (marbete) y el maíz tardío, el riesgo de chicharrita (ficha 03).
Hacé la cuenta en margen.henderseeds.com
La regla: decidí con los dos márgenes al lado, no con el precio de hoy.
Comentá FICHAS y te mandamos las 5 por DM · wa.me/5492314530691

#Henderseeds #Nidera #Girasol #MaizTardio #Margenes #Siembra2627 #Henderson #Bolivar'''),
]

CAP_CUADERNO = '''Cuaderno de decisiones 26/27 📒
Cinco fichas para decidir en el lote estas semanas, con datos de los marbetes oficiales Nidera:
01 ¿Te alcanza la sembradora para el girasol?
02 ¿Qué girasol va? Empezá por tu lote.
03 Maíz tardío: elegí por tu mayor riesgo.
04 ¿En qué ambiente está tu lote?
05 ¿Girasol o maíz tardío en ese lote?
📌 Guardalo. Y si tu lote no encaja en ninguna, lo vemos juntos: Mandanos un DM o escribinos 📲 wa.me/5492314530691

#Henderseeds #Nidera #Girasol #Maiz #Siembra2627 #Henderson #Daireaux #Bolivar'''

DM_FICHAS = '''¡Hola! Acá tenés las 5 fichas: ''' + PAGES + 'decisiones/' + PDF + '''
¿Qué estás por decidir, girasol o maíz tardío? Si querés, lo vemos para tu lote.'''

CALENDARIO = [
 ('Mar 27/10', 'Reel', 'Ficha 01 · ¿Te alcanza la sembradora?', 'Urgente: quedan menos de 3 semanas de ventana óptima. Reemplaza al reel 4.'),
 ('Jue 29/10', 'Carrusel', 'Cuaderno de decisiones (tapa + 5 fichas)', 'La pieza para guardar. Si llega la foto real, el parte de siembra pasa al sábado.'),
 ('Sáb 31/10', 'Reel', 'Ficha 03 · Maíz tardío por riesgo', 'Reemplaza a la opción del sábado: es el mismo tema, con más decisión.'),
 ('Mar 3/11', 'Reel', 'Ficha 05 · ¿Girasol o maíz tardío?', 'Cuando se asignan los últimos lotes. Historia con link a la calculadora.'),
 ('Jue 5/11', 'Reel', 'Ficha 02 · ¿Qué girasol va?', 'Para reposición y lotes sin híbrido asignado.'),
 ('Mar 10/11', 'Reel', 'Ficha 04 · ¿En qué ambiente está tu lote?', 'Abre la charla del diagnóstico (paso 1 del Plan) para la 27/28.'),
]


def uri(path, ancho):
    with tempfile.NamedTemporaryFile(suffix='.jpg') as t:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', f'scale={ancho}:-2', '-q:v', '5', t.name], check=True)
        return 'data:image/jpeg;base64,' + base64.b64encode(open(t.name, 'rb').read()).decode()


def ficha(f, modo):
    e = html.escape
    vid = f'../placas/video/2026-W44-ficha-{f["slug"]}.mp4'
    estado = f'img/ficha-{f["n"]}-estado.jpg'
    placa = f'img/ficha-{f["n"]}-feed.jpg'
    if modo == 'pages':
        media = (f'<figure class="m9"><video controls playsinline preload="none" poster="{estado}" src="{vid}"></video><figcaption>Reel 22 s</figcaption></figure>'
                 f'<figure class="m45"><img src="{placa}" alt="Placa de la ficha {f["n"]}: {e(f["titulo"])}" loading="lazy"><figcaption>Placa 4:5</figcaption></figure>')
        bajar = (f'<a class="btn sec" href="{vid}" download>Bajar reel</a><a class="btn sec" href="{placa}" download>Bajar placa</a>'
                 f'<a class="btn sec" href="{estado}" download>Bajar Estado</a>')
    else:
        media = (f'<figure class="m9"><img src="{uri(os.path.join(RAIZ, "docs/decisiones", estado), 360)}" alt="Reel de la ficha {f["n"]}"><figcaption>Reel 22 s · <a href="{PAGES}decisiones/#f{f["n"]}" target="_blank" rel="noopener">ver en el sitio</a></figcaption></figure>'
                 f'<figure class="m45"><img src="{uri(os.path.join(RAIZ, "docs/decisiones", placa), 480)}" alt="Placa de la ficha {f["n"]}: {e(f["titulo"])}"><figcaption>Placa 4:5</figcaption></figure>')
        bajar = f'<a class="btn sec" href="{PAGES}decisiones/#f{f["n"]}" target="_blank" rel="noopener">Bajar reel, placa y Estado (sitio)</a>'
    return f'''
  <article class="ficha" id="f{f['n']}">
    <div class="num" aria-hidden="true">{f['n']}</div>
    <div class="cuerpo">
      <p class="eyebrow">Ficha {f['n']} · {e(f['pilar'])}</p>
      <h3>{e(f['titulo'])}</h3>
      <div class="media">{media}</div>
      <dl class="datos">
        <div><dt>En pantalla</dt><dd>{e(f['herramienta'])}</dd></div>
        <div><dt>Cuándo sirve</dt><dd>{e(f['sirve'])}</dd></div>
        <div class="regla"><dt>Se lleva</dt><dd>{e(f['regla'])}</dd></div>
        <div><dt>Fuente</dt><dd>{e(f['fuente'])}</dd></div>
      </dl>
      <details class="cap"><summary>Texto para publicar</summary><pre id="cap-{f['n']}">{e(f['cap'])}</pre></details>
      <div class="acciones"><button type="button" class="btn" data-copiar="cap-{f['n']}">Copiar texto</button>{bajar}<span class="ok" aria-live="polite"></span></div>
    </div>
  </article>'''


CSS = '''
/* Cuaderno de campo: hoja crema, tinta navy, rótulos en DM Mono, marcador ámbar. Una sola columna de lectura
   con el número de ficha al margen, como una libreta. Registro Técnico de brand/identidad.md. */
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
.lead { font-size:clamp(18px, 2.4vw, 22px); line-height:1.45; max-width:62ch; margin:0; color:var(--tinta); }
.meta { display:flex; flex-wrap:wrap; gap:8px; }
.meta span { font:500 13px var(--mono); letter-spacing:.06em; text-transform:uppercase; color:var(--navy); border:1.5px solid var(--linea); border-radius:6px; padding:6px 10px; background:var(--blanco); }
section { padding-block:34px; border-top:2px solid var(--linea); }
h2 { font:400 clamp(28px, 4.6vw, 44px)/1 var(--display); letter-spacing:-.025em; color:var(--navy); margin:0 0 18px; text-wrap:balance; }
.sub { color:var(--gris); max-width:64ch; margin:0 0 20px; }
.cambio { width:100%; border-collapse:collapse; background:var(--blanco); border:1.5px solid var(--linea); border-radius:12px; overflow:hidden; }
.cambio th { font:500 12px var(--mono); letter-spacing:.12em; text-transform:uppercase; text-align:left; padding:12px 16px; background:var(--navy); color:var(--papel); }
.cambio td { padding:14px 16px; border-top:1.5px solid var(--linea); vertical-align:top; }
.cambio td:first-child { color:var(--gris); width:46%; }
.cambio td:last-child { font-weight:600; color:var(--navy); }
.tabla-x { overflow-x:auto; }
.pasos { list-style:none; padding:0; margin:0; display:grid; grid-template-columns:repeat(5, minmax(0, 1fr)); gap:10px; counter-reset:p; }
.pasos li { counter-increment:p; background:var(--blanco); border:1.5px solid var(--linea); border-radius:12px; padding:14px 14px 16px; display:grid; gap:6px; align-content:start; }
.pasos li::before { content:counter(p, decimal-leading-zero); font:500 13px var(--mono); color:var(--amber-osc); letter-spacing:.1em; }
.pasos b { font:400 19px/1.1 var(--display); color:var(--navy); letter-spacing:-.01em; }
.pasos span { font-size:14.5px; color:var(--gris); line-height:1.4; }
.ficha { display:grid; grid-template-columns:120px minmax(0, 1fr); gap:24px; padding-block:34px; border-top:2px solid var(--linea); }
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
.datos { margin:0; display:grid; gap:0; border:1.5px solid var(--linea); border-radius:12px; background:var(--blanco); overflow:hidden; }
.datos div { display:grid; grid-template-columns:140px minmax(0, 1fr); gap:14px; padding:12px 16px; border-top:1.5px solid var(--linea); }
.datos div:first-child { border-top:0; }
.datos dt { font:500 12px/1.6 var(--mono); letter-spacing:.1em; text-transform:uppercase; color:var(--gris2); }
.datos dd { margin:0; }
.datos .regla { background:var(--navy); }
.datos .regla dt { color:var(--amber); }
.datos .regla dd { color:var(--blanco); font-weight:700; font-size:19px; line-height:1.3; }
details.cap { border:1.5px solid var(--linea); border-radius:12px; background:var(--papel2); }
details.cap summary { cursor:pointer; padding:12px 16px; font:500 13px var(--mono); letter-spacing:.08em; text-transform:uppercase; color:var(--navy); }
details.cap pre { margin:0; padding:0 16px 16px; white-space:pre-wrap; overflow-wrap:anywhere; font:400 15px/1.5 var(--body); color:var(--tinta); }
.acciones { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
.btn { appearance:none; border:0; cursor:pointer; font:700 15px var(--body); padding:11px 16px; border-radius:8px; background:var(--amber); color:#0A0F1B; text-decoration:none; display:inline-flex; align-items:center; }
.btn.sec { background:var(--blanco); color:var(--navy); font-weight:500; font-size:14px; border:1.5px solid var(--linea); padding:9px 12px; }
.btn:focus-visible, .btn.sec:focus-visible, summary:focus-visible { outline:3px solid var(--navy); outline-offset:2px; }
.ok { font:500 13px var(--mono); color:#2E7D4F; }
.cuaderno { display:grid; grid-template-columns:minmax(0, 330px) minmax(0, 1fr); gap:24px; align-items:start; }
.cuaderno img { width:100%; border-radius:10px; box-shadow:0 14px 34px rgba(13,45,94,.2); display:block; }
.cuaderno .txt { display:grid; gap:14px; min-width:0; }
.cuaderno pre { margin:0; white-space:pre-wrap; overflow-wrap:anywhere; font:400 15px/1.5 var(--body); background:var(--blanco); border:1.5px dashed var(--amber); border-radius:12px; padding:14px 16px; }
.cal { width:100%; border-collapse:collapse; background:var(--blanco); border:1.5px solid var(--linea); }
.cal th, .cal td { text-align:left; padding:11px 14px; border-top:1.5px solid var(--linea); vertical-align:top; }
.cal th { font:500 12px var(--mono); letter-spacing:.1em; text-transform:uppercase; color:var(--papel); background:var(--navy); border:0; }
.cal td:first-child { font:500 14px var(--mono); white-space:nowrap; color:var(--navy); }
.cal td:nth-child(2) { font:500 12px var(--mono); text-transform:uppercase; letter-spacing:.08em; color:var(--amber-osc); }
.cal td:nth-child(3) { font-weight:700; color:var(--navy); }
.cal td:last-child { color:var(--gris); font-size:15px; }
.notas { margin:0; padding-left:20px; display:grid; gap:8px; color:var(--tinta); max-width:70ch; }
footer { font:500 12px var(--mono); color:var(--gris2); padding-top:24px; border-top:2px solid var(--linea); letter-spacing:.04em; }
@media (max-width:820px) {
  .pasos { grid-template-columns:minmax(0, 1fr); }
  .ficha { grid-template-columns:minmax(0, 1fr); gap:10px; }
  .ficha .num { position:static; font-size:64px; }
  .datos div { grid-template-columns:minmax(0, 1fr); gap:2px; }
  .cuaderno { grid-template-columns:minmax(0, 1fr); }
  .cuaderno img { max-width:340px; }
}
@media (prefers-reduced-motion: reduce) { * { scroll-behavior:auto; } }
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
    tapa = 'img/ficha-00-feed.jpg' if modo == 'pages' else uri(os.path.join(RAIZ, 'docs/decisiones/img/ficha-00-feed.jpg'), 520)
    pdf = PDF if modo == 'pages' else PAGES + 'decisiones/' + PDF
    nav = ('<nav aria-label="Otras páginas"><a href="../kit/">Kit</a><a href="../estudio/">Estudio</a><a href="../">Dashboard</a></nav>' if modo == 'pages' else
           f'<nav aria-label="Sitio"><a href="{PAGES}decisiones/" target="_blank" rel="noopener">Ver en el sitio</a></nav>')
    carrusel = ''.join(f'<a class="btn sec" href="img/ficha-0{i}-feed.jpg" download>Placa {i:02d}</a>' for i in range(6)) if modo == 'pages' else ''
    cuerpo = f'''
<div class="wrap">
  <header class="top"><p class="eyebrow">HenderSeeds · Siembra 26/27 · sesión 3</p>{nav}</header>
  <div class="hero">
    <h1>Decisiones <span class="mk">26/27</span></h1>
    <p class="lead">Cinco piezas que el productor guarda porque le resuelven algo esta semana. El video arma la ficha delante de él, la placa es la ficha terminada y las cinco juntas son el cuaderno que se lleva quien comenta FICHAS.</p>
    <div class="meta"><span>5 reels de 22 s</span><span>5 placas 4:5</span><span>5 Estados</span><span>Cuaderno PDF</span><span>Datos de marbetes Nidera</span></div>
  </div>

  <section>
    <h2>Qué cambia</h2>
    <p class="sub">Miré lo que hicimos en octubre. Se ve bien y respeta las reglas, pero casi todo le pide algo al productor (que conteste, que adivine, que escriba) y le deja poco para usar en el lote. Esta sesión da vuelta eso.</p>
    <div class="tabla-x"><table class="cambio">
      <thead><tr><th scope="col">Hasta ahora</th><th scope="col">En esta sesión</th></tr></thead>
      <tbody>
        <tr><td>Preguntas para que respondan: ¿cuántos mm?, ¿verdadero o falso?</td><td>Una decisión resuelta por pieza, con su regla.</td></tr>
        <tr><td>El producto adelante: los 4 girasoles, los 3 maíces.</td><td>El problema del lote adelante; el híbrido es la respuesta.</td></tr>
        <tr><td>Dibujos que acompañan: tolva, balanza, lupa.</td><td>La herramienta es el dibujo: calendario, árbol, mapa de calor, escala, cuenta.</td></tr>
        <tr><td>Cierre "Pedí tu recomendación".</td><td>Cierre "Comentá FICHAS" (se lleva el cuaderno) y "Lo vemos juntos" si no encaja.</td></tr>
        <tr><td>Se mira el alcance y los me gusta.</td><td>Se miran guardados, comentarios FICHAS y charlas que terminan en visita.</td></tr>
      </tbody>
    </table></div>
  </section>

  <section>
    <h2>Cómo está hecha cada ficha</h2>
    <p class="sub">El mismo orden en las cinco, para que el productor aprenda a leerlas. Va también al estudio como plantilla nueva.</p>
    <ol class="pasos">
      <li><b>La decisión</b><span>Es el gancho: se lee entera en el primer cuadro.</span></li>
      <li><b>El dato</b><span>Del marbete, con la fuente al pie.</span></li>
      <li><b>La cuenta o el criterio</b><span>Se arma en pantalla; los ejemplos van rotulados.</span></li>
      <li><b>La regla</b><span>Una línea que se lleva al lote.</span></li>
      <li><b>Lo vemos juntos</b><span>Comentá FICHAS, DM o WhatsApp.</span></li>
    </ol>
  </section>

  <section>
    <h2>Las cinco fichas</h2>
    <p class="sub">Ordenadas por número. El orden para publicar, más abajo.</p>
    {''.join(ficha(f, modo) for f in FICHAS)}
  </section>

  <section id="cuaderno">
    <h2>El cuaderno</h2>
    <div class="cuaderno">
      <img src="{tapa}" alt="Tapa del Cuaderno de decisiones 26/27 con el índice de las 5 fichas">
      <div class="txt">
        <p class="sub" style="margin:0">Tapa y cinco fichas en un PDF de 6 páginas. Sirve para mandar a quien comenta FICHAS y, en el feed, como carrusel de 6 placas.</p>
        <div class="acciones"><a class="btn" href="{pdf}" {"download" if modo == "pages" else 'target="_blank" rel="noopener"'}>Bajar el cuaderno (PDF)</a>{carrusel}</div>
        <p class="eyebrow">Respuesta por DM a quien comenta FICHAS</p>
        <pre id="dm-fichas">{e(DM_FICHAS)}</pre>
        <div class="acciones"><button type="button" class="btn sec" data-copiar="dm-fichas">Copiar respuesta</button><span class="ok" aria-live="polite"></span></div>
        <details class="cap"><summary>Texto del carrusel</summary><pre id="cap-cuaderno">{e(CAP_CUADERNO)}</pre></details>
        <div class="acciones"><button type="button" class="btn sec" data-copiar="cap-cuaderno">Copiar texto del carrusel</button><span class="ok" aria-live="polite"></span></div>
      </div>
    </div>
  </section>

  <section>
    <h2>Orden para publicar</h2>
    <p class="sub">Por urgencia: primero lo que vence (la ventana del girasol), después el tardío y al final el diagnóstico, que abre la próxima campaña. Cada ficha sale el mismo día como Estado de WhatsApp. Si preferís otro orden, lo cambiamos.</p>
    <div class="tabla-x"><table class="cal">
      <thead><tr><th scope="col">Día</th><th scope="col">Formato</th><th scope="col">Pieza</th><th scope="col">Por qué</th></tr></thead>
      <tbody>{''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>' for a, b, c, d in CALENDARIO)}</tbody>
    </table></div>
  </section>

  <section>
    <h2>Antes de publicar</h2>
    <ul class="notas">
      <li>Santi revisa cada ficha con la checklist, como siempre.</li>
      <li>Ficha 04 muestra los cortes de ambiente del maíz en kg/ha. Es la escala del marbete, no un resultado de ensayo, pero conviene confirmar que entra en la regla del 25/09.</li>
      <li>Los ejemplos (560 ha, 1 de cada 3 días perdidos, 2.100 · 2.600 · 1.900 kg/ha) están rotulados EJEMPLO en pantalla.</li>
      <li>Ninguna pieza muestra precios, descuentos ni condiciones, ni números de ensayo de maíz.</li>
    </ul>
  </section>

  <footer>HenderSeeds · Distribuidor RED.IN Nidera · Henderson, Daireaux y Bolívar · WhatsApp 2314 53-0691 · {WA}</footer>
</div>
<script>{JS}</script>'''
    if modo == 'pages':
        return ('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                '<title>Decisiones 26/27 · HenderSeeds</title>\n<meta name="description" content="Sesión 3: cinco fichas de decisión para el productor (reel, placa, Estado y cuaderno PDF).">\n'
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
