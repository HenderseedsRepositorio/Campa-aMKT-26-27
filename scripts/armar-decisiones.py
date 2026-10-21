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

WA = 'Pasamos por tu lote: Mandanos un DM · wa.me/5492314530691'
FICHAS = [
 dict(n='01', slug='01-sembradora', titulo='Girasol: la ventana cierra el 15/11.', pilar='Girasol',
      regla='Si no llega, decidí hoy qué lotes van primero.',
      fuente='Ventana del girasol, Oeste de Buenos Aires: marbetes oficiales Nidera 26/27. Ejemplo rotulado (560 ha ÷ 14 días).',
      cap=f'''Girasol: la ventana óptima cierra el 15/11. 🌻
En el oeste, el límite es el 20/11 (marbetes Nidera).
Tu ritmo: hectáreas que faltan ÷ días de siembra que quedan = ha por día.
Si no llega, decidí hoy qué lotes van primero. {WA}

#Henderseeds #Nidera #Girasol #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='02', slug='02-girasol', titulo='Girasol: el híbrido depende del lote.', pilar='Girasol',
      regla='Primero el problema del lote. Después, el rinde.',
      fuente='Marbetes oficiales Nidera 26/27. NS 1113 CL: 74 % de éxito en 225 comparaciones, ensayos Sur + Oeste.',
      cap=f'''Girasol: el híbrido depende del lote. 🌻
Si tuvo Phomopsis: NS 1115 CL o NS 1117 CL (Phomopsis 2).
Si no tuvo: NS 1113 CL, techo de rinde y aceite (74 % de éxito en 225 comparaciones Sur + Oeste).
Si te pagan alto oleico: NS 1227 CL HO.
Primero el problema del lote; después, el rinde. {WA}

#Henderseeds #Nidera #Girasol #NS1113CL #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='03', slug='03-maiz-tardio', titulo='Tardío: tres riesgos, tres híbridos.', pilar='Maíz tardío',
      regla='Elegí por tu mayor riesgo, no por el promedio.',
      fuente='Perfil sanitario de los marbetes oficiales Nidera 26/27 (1 excelente – 9 deficiente). Sin números de ensayo de maíz.',
      cap=f'''Maíz tardío: tres riesgos, tres híbridos. 🌽
Chicharrita: NS 7925 (Spiroplasma 3, el mejor del portafolio).
Quebrado por viento: NS 7765 (Quebrado 1).
Malezas difíciles: NS 7921 CL (3 herramientas herbicidas).
Perfil de los marbetes Nidera: 1 excelente, 9 deficiente. Elegí por tu mayor riesgo. {WA}

#Henderseeds #Nidera #MaizTardio #Viptera3 #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='04', slug='04-ambiente', titulo='Girasol: cuatro ambientes según el rinde.', pilar='Diagnóstico',
      regla='Clasificalo con varias campañas, no con la mejor.',
      fuente='Escala de ambientes del girasol en los marbetes oficiales Nidera 26/27.',
      cap='''Girasol: cuatro ambientes según el rinde. 📍
El marbete Nidera los separa en menos de 1.500, de 1.500 a 2.500, de 2.500 a 3.500 y más de 3.500 kg/ha.
Clasificá cada lote con el promedio de varias campañas, no con la mejor: de eso dependen el híbrido, la densidad y la inversión.
Mandanos tus rindes y lo vemos juntos · wa.me/5492314530691

#Henderseeds #Nidera #Girasol #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='05', slug='05-girasol-o-maiz', titulo='Girasol o maíz tardío: misma cuenta.', pilar='Márgenes',
      regla='Compará los dos márgenes antes de decidir.',
      fuente='Límite del girasol: marbetes oficiales Nidera 26/27, Oeste de Buenos Aires. Calculadora: margen.henderseeds.com.',
      cap=f'''Girasol o maíz tardío: misma cuenta. 🌻🌽
Cuatro datos para los dos: rinde de tu ambiente, precio, costo y flete.
Límites y riesgos: el girasol, hasta el 20/11 (marbete); el tardío, riesgo de chicharrita.
Hacé la cuenta en margen.henderseeds.com y compará los dos márgenes antes de decidir. {WA}

#Henderseeds #Nidera #Girasol #MaizTardio #Margenes #Siembra2627 #Henderson #Bolivar'''),
]

FICHAS2 = [
 dict(n='06', slug='06-indiferencia', titulo='Todo lote tiene un rinde de indiferencia.', pilar='Márgenes',
      regla='Primero el número, después la bolsa.',
      fuente='Sin cifras: los datos son los del lote. Calculadora de márgenes HenderSeeds: margen.henderseeds.com.',
      cap=f'''Todo lote tiene un rinde de indiferencia. 📈
Costos por hectárea ÷ precio neto: los qq/ha que necesitás para cubrir los costos.
Si tu ambiente apenas lo supera, revisá el planteo antes de sembrar.
La cuenta, en margen.henderseeds.com. {WA}

#Henderseeds #Nidera #Margenes #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='07', slug='07-alto-oleico', titulo='Alto oleico: la bonificación la paga el comprador.', pilar='Girasol',
      regla='Primero el contrato, después la bolsa.',
      fuente='NS 1227 CL HO (bonificación por calidad de aceite, Downy Mildew R) y ventana del oeste: marbetes oficiales Nidera 26/27.',
      cap=f'''Alto oleico: la bonificación la paga el comprador. 🌻
NS 1227 CL HO es el alto oleico del portafolio Nidera, resistente a Downy Mildew.
Ventana en el oeste: óptima hasta el 15/11, límite 20/11 (marbete).
Primero el contrato, después la bolsa. {WA}

#Henderseeds #Nidera #Girasol #AltoOleico #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='08', slug='08-lomas-y-bajos', titulo='Un lote. Dos ambientes.', pilar='Ambientes',
      regla='Una sola densidad no le sirve a los dos.',
      fuente='Recomendación Asista por ambiente, con siembra variable opcional: paso 2 del Plan de Campaña HenderSeeds.',
      cap=f'''Un lote. Dos ambientes. 📍
Cada ambiente, su híbrido y su densidad.
En el Plan de Campaña, la Recomendación Asista va por ambiente, con siembra variable opcional.
Una sola densidad no le sirve a los dos. {WA}

#Henderseeds #Nidera #Maiz #Girasol #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='09', slug='09-maiz-fecha', titulo='Maíz: no todo híbrido va en tardía.', pilar='Maíz',
      regla='El híbrido va con la fecha.',
      fuente='Posicionamiento por fecha de los marbetes oficiales Nidera 26/27. Sin números de ensayo de maíz.',
      cap=f'''Maíz: no todo híbrido va en tardía. 🌽
Mejor en temprana: NS 7621 (no es primera opción en tardía).
Para tardía: NS 7925, NS 7624 CL y NS 7818.
Para las dos fechas: NS 7765, NS 7852 y NS 7921 CL.
Posicionamiento de los marbetes Nidera 26/27. El híbrido va con la fecha. {WA}

#Henderseeds #Nidera #Maiz #MaizTardio #Siembra2627 #Henderson #Daireaux #Bolivar'''),
 dict(n='10', slug='10-encharcado', titulo='Lote encharcado después de sembrar: hay seguro.', pilar='Plan de Campaña',
      regla='La resiembra se decide con números.',
      fuente='Seguro de resiembra de Nidera, ante granizo o encharcamiento: paso 4 del Plan de Campaña. Sin condiciones del seguro.',
      cap=f'''Lote encharcado después de sembrar: hay seguro. 🌧️
Tenés el seguro de resiembra de Nidera, ante granizo o encharcamiento.
Antes de decidir, contá las plantas que quedaron: la resiembra se decide con números.
Si te pasa, escribinos. {WA}

#Henderseeds #Nidera #Siembra2627 #Resiembra #Henderson #Daireaux #Bolivar'''),
]

CALENDARIO = [
 ('Mar 27/10', '01 · Girasol: la ventana cierra el 15/11', 'Lo que vence primero.'),
 ('Jue 29/10', '02 · Girasol: el híbrido depende del lote', 'Lotes de girasol sin híbrido asignado.'),
 ('Sáb 31/10', '07 · Alto oleico', 'El contrato se cierra antes de sembrar.'),
 ('Mar 3/11', '03 · Tardío: tres riesgos, tres híbridos', 'Reemplaza al reel 4 (mismos híbridos).'),
 ('Jue 5/11', '09 · Maíz: no todo híbrido va en tardía', 'Cuando se cierra el híbrido del tardío.'),
 ('Sáb 7/11', '05 · Girasol o maíz tardío', 'Antes del límite del girasol (20/11).'),
 ('Mar 10/11', '06 · Rinde de indiferencia', 'Márgenes: vale todo el año.'),
 ('Jue 12/11', '08 · Un lote, dos ambientes', 'Abre la charla del Plan de Campaña.'),
 ('Sáb 14/11', '04 · Cuatro ambientes según el rinde', 'Diagnóstico para la próxima campaña.'),
 ('Comodín', '10 · Lote encharcado: hay seguro', 'Usarlo cuando llueva fuerte con lotes recién sembrados.'),
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
.tono { margin:0; padding:0; list-style:none; display:grid; gap:10px; max-width:760px; }
.tono li { background:var(--blanco); border:1.5px solid var(--linea); border-radius:12px; padding:14px 18px; display:grid; gap:4px; }
.tono b { color:var(--navy); font-size:18px; }
.tono span { font:400 14px/1.5 var(--mono); color:var(--gris); }
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
    <p class="lead">Diez reels cortos y diez placas, en dos ondas para comparar. Cada uno responde una decisión de estas semanas con pocas palabras: el dato del marbete y una regla para llevarse.</p>
  </div>

  <section>
    <h2>Cómo suena HenderSeeds</h2>
    <ul class="tono">
      <li><b>El gancho es un dato o una afirmación técnica.</b> No una pregunta que pone en duda al productor. <span>"¿Te alcanza la sembradora?" → "Girasol: la ventana cierra el 15/11."</span></li>
      <li><b>Nada de preguntas de sí o no en pantalla.</b> <span>"¿El lote tuvo Phomopsis?" → "Si el lote tuvo Phomopsis".</span></li>
      <li><b>Una pantalla, una idea.</b> Pocas palabras, voseo y sin signos de exclamación.</li>
      <li><b>La calidez va en una sola línea, al cierre.</b> <span>"Pasamos por tu lote. Mandanos un DM."</span></li>
    </ul>
  </section>

  <section>
    <h2>01–05 · Hoja crema</h2>
    <p class="sub">Una idea por pantalla, letra grande, cortina navy entre escenas.</p>
    {''.join(ficha(f, modo) for f in FICHAS)}
  </section>

  <section>
    <h2>06–10 · Charla de lote</h2>
    <p class="sub">Otra onda: fondo noche, la frase entra palabra por palabra como si la dijera alguien en el lote, y cierra en una tarjeta crema.</p>
    {''.join(ficha(f, modo) for f in FICHAS2)}
  </section>

  <section>
    <h2>Orden para publicar</h2>
    <p class="sub">Tres por semana, primero lo que vence: el girasol. Cada uno, el mismo día, como Estado de WhatsApp. El 10 queda de comodín para una lluvia fuerte.</p>
    <div class="tabla-x"><table class="cal">
      <thead><tr><th scope="col">Día</th><th scope="col">Pieza</th><th scope="col">Por qué</th></tr></thead>
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
                '<title>Decisiones 26/27 · HenderSeeds</title>\n<meta name="description" content="Diez reels cortos y diez placas en dos ondas: una decisión de siembra por pieza, con pocas palabras.">\n'
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
