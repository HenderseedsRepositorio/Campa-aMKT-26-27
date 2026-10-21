#!/usr/bin/env python3
"""
Página del estudio de motion (docs/estudio/index.html) a partir de:
  produccion/estudio/estudio.xml        el prompt: rol, plantillas y reglas (fuente de verdad)
  produccion/estudio/revision/*.json    controles automáticos de scripts/revisar-reel.mjs
  produccion/estudio/puntajes.json      puntaje de director creativo de cada plantilla

  python3 scripts/armar-estudio.py
"""
import html, json, os, re
import xml.etree.ElementTree as ET

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(RAIZ, 'produccion/estudio')
VID = '../placas/video'
e = html.escape

xml_txt = open(os.path.join(E, 'estudio.xml'), encoding='utf-8').read()
raiz = ET.fromstring(xml_txt)
puntajes = json.load(open(os.path.join(E, 'puntajes.json'), encoding='utf-8'))


def texto(tag):
    return ' '.join(raiz.find(tag).text.split())


def portada(video):
    m = re.match(r'(.*?-(?:reel|opcion)-\d+)', video)
    return (m.group(1) if m else video[:-4]) + '-portada.jpg'


def revision(ref):
    archivo, _, q = ref.partition('?')
    nombre = os.path.basename(archivo)[:-5] + (('-v' + q.split('=')[1]) if q.startswith('v=') else '')
    ruta = os.path.join(E, 'revision', nombre + '.json')
    return json.load(open(ruta, encoding='utf-8')) if os.path.exists(ruta) else None


def chips_revision(r):
    if not r:
        return '<span class="ck no">sin revisar</span>'
    k = r['controles']
    def ck(ok, txt):
        return f'<span class="ck {"si" if ok else "no"}">{"✓" if ok else "✗"} {txt}</span>'
    g = k['gancho_cuadro_0']
    out = ['<span class="ck na">— gancho</span>' if g.get('no_aplica') else ck(g['ok'], 'gancho en el cuadro 0'),
           ck(k['fuera_de_zona']['ok'], 'zona segura'),
           ck(k['letra_menor_19px']['ok'] and k['lectura_menor_30px']['ok'], 'letra'),
           ck(k['palabras_en_pantalla']['ok'], f'{k["palabras_en_pantalla"]["max"]} palabras máx')]
    return ''.join(out)


def chips_puntaje(p):
    if not p:
        return ''
    nombres = [('g', 'gancho'), ('l', 'legibilidad'), ('c', 'continuidad'), ('t', 'terminación'), ('m', 'marca')]
    celdas = ''.join(f'<span class="pt{" bajo" if (p.get(k) or 10) < 8 else ""}" title="{n}"><b>{p[k] if p.get(k) is not None else "—"}</b>{n[:4]}</span>' for k, n in nombres)
    flojo = ''.join(f'<li>{e(f)}</li>' for f in p.get('flojo', []))
    return f'<div class="pts">{celdas}</div>' + (f'<ul class="flojo">{flojo}</ul>' if flojo else '')


tarjetas = []
for i, p in enumerate(raiz.iter('plantilla'), 1):
    nombre, video = p.get('nombre'), p.get('video')
    escenas = ''.join(f'<li>{e(" ".join(x.text.split()))}</li>' for x in p.findall('escena'))
    debe = e(' '.join(p.find('debe').text.split()))
    tarjetas.append(f'''
  <article class="pl" id="{nombre}">
    <div class="cab"><span class="n">{i:02d}</span><span class="meta">{e(p.get("dur")).upper()} · {e(p.get("formato"))}</span></div>
    <code class="tag">&lt;plantilla<br>nombre="{e(nombre)}"&gt;</code>
    <video muted loop playsinline preload="none" poster="{VID}/{portada(video)}" src="{VID}/{video}" aria-label="Ejemplo de la plantilla {e(nombre)}"></video>
    <ul class="esc">{escenas}</ul>
    <p class="debe"><b>debe:</b> {debe}</p>
    <div class="rev">{chips_revision(revision(p.get("ref")))}</div>
    {chips_puntaje(puntajes.get(nombre))}
    <p class="ref">ref: {e(p.get("ref"))}</p>
    <button class="btn sec" data-copiar="corré {e(nombre)} para [tema]">Copiar pedido</button>
  </article>''')

pagina = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Estudio de motion HenderSeeds</title>
<meta name="description" content="11 plantillas de reel para HenderSeeds, con ejemplo, reglas y revisión.">
<link rel="stylesheet" href="../assets/fonts/fuentes.css">
<style>
/* Tablero oscuro de estudio: tarjetas por plantilla, todo en la tipografía de la marca */
:root {{ --bg:#0A0F1B; --card:#101827; --line:#22304A; --ink:#E8EEF7; --muted:#8FA0BE; --amber:#F5A623; --ok:#7FD3A0; --bad:#FF8A7A;
  --mono:'DM Mono',ui-monospace,Menlo,monospace; --sans:'DM Sans',system-ui,sans-serif; --arch:'Archivo Black','Arial Black',sans-serif; color-scheme:dark; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:var(--sans); font-size:15px; line-height:1.45; }}
.wrap {{ max-width:1320px; margin:0 auto; padding-block:22px 64px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); }}
.barra {{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; font-family:var(--mono); font-size:13px; color:var(--muted); border-bottom:1px solid var(--line); padding-bottom:14px; }}
.barra .pts3 {{ display:flex; gap:6px; }} .barra .pts3 i {{ width:11px; height:11px; border-radius:50%; display:block; background:#FF5F57; }} .barra .pts3 i:nth-child(2) {{ background:#FEBC2E; }} .barra .pts3 i:nth-child(3) {{ background:#28C840; }}
.barra .sp {{ flex:1; }}
.barra a {{ color:var(--muted); }}
.pill {{ font-family:var(--mono); font-size:12px; letter-spacing:1px; text-transform:uppercase; border:1px solid var(--amber); color:var(--amber); border-radius:6px; padding:5px 10px; }}
.btn {{ appearance:none; border:1px solid var(--line); background:#151F33; color:var(--ink); font-family:var(--mono); font-size:13px; border-radius:6px; padding:8px 12px; cursor:pointer; }}
.btn.pri {{ background:var(--amber); color:#0A0A0A; border-color:var(--amber); font-weight:500; }}
.btn:focus-visible {{ outline:2px solid var(--amber); outline-offset:2px; }}
h1 {{ font-family:var(--arch); font-weight:400; font-size:clamp(28px, 5vw, 46px); line-height:1.08; letter-spacing:-1px; margin:26px 0 8px; text-wrap:balance; }}
h1 em {{ font-style:normal; color:var(--amber); }}
.bajada {{ font-family:var(--mono); color:var(--muted); font-size:13.5px; max-width:80ch; }}
.dos {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 420px), 1fr)); gap:16px 28px; margin:24px 0; }}
.bloque {{ font-family:var(--mono); font-size:13.5px; color:var(--ink); }}
.bloque .t {{ color:var(--amber); }}
h2 {{ font-family:var(--mono); font-weight:500; font-size:14px; color:var(--amber); margin:28px 0 12px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(min(100%, 236px), 1fr)); gap:14px; }}
.pl {{ background:var(--card); border:1px solid var(--line); border-top:2px solid var(--amber); border-radius:10px; padding:14px; display:flex; flex-direction:column; gap:10px; min-width:0; }}
.cab {{ display:flex; justify-content:space-between; align-items:baseline; }}
.n {{ font-family:var(--arch); font-size:24px; color:var(--amber); }}
.meta {{ font-family:var(--mono); font-size:12px; color:var(--muted); letter-spacing:1px; }}
.tag {{ font-family:var(--mono); font-size:13.5px; line-height:1.4; color:var(--ink); font-weight:500; overflow-wrap:anywhere; }}
video {{ width:100%; aspect-ratio:9/16; object-fit:cover; border-radius:8px; background:#000; border:1px solid var(--line); cursor:pointer; }}
.esc {{ list-style:none; margin:0; padding:0; font-family:var(--mono); font-size:12.5px; color:var(--muted); display:grid; gap:5px; }}
.esc li::before {{ content:'› '; color:var(--amber); }}
.debe {{ margin:0; font-family:var(--mono); font-size:12.5px; color:#B8C6DE; }} .debe b {{ color:var(--amber); font-weight:500; }}
.rev {{ display:flex; flex-wrap:wrap; gap:5px; }}
.ck {{ font-family:var(--mono); font-size:11.5px; border-radius:5px; padding:3px 7px; background:#152338; }}
.ck.si {{ color:var(--ok); }} .ck.no {{ color:var(--bad); }} .ck.na {{ color:var(--muted); }}
.pts {{ display:grid; grid-template-columns:repeat(5, 1fr); gap:4px; }}
.pt {{ display:flex; flex-direction:column; align-items:center; background:#152338; border-radius:6px; padding:5px 0; font-family:var(--mono); font-size:10.5px; color:var(--muted); }}
.pt b {{ font-family:var(--arch); font-weight:400; font-size:18px; color:var(--ink); }}
.pt.bajo b {{ color:var(--amber); }}
.flojo {{ margin:0; padding-left:16px; font-size:12.5px; color:#B8C6DE; display:grid; gap:3px; }}
.ref {{ margin:0; font-family:var(--mono); font-size:11.5px; color:#5F6E89; word-break:break-all; }}
.reglas {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 420px), 1fr)); gap:14px; margin-top:26px; }}
.reglas div {{ border:1px solid var(--line); border-left:3px solid var(--amber); border-radius:8px; padding:14px; font-family:var(--mono); font-size:13px; line-height:1.55; }}
.reglas div:last-child {{ border-left-color:var(--ok); }}
.reglas .t {{ color:var(--amber); }} .reglas div:last-child .t {{ color:var(--ok); }}
.ok {{ font-family:var(--mono); font-size:12px; color:var(--ok); }}
@media (prefers-reduced-motion: reduce) {{ video {{ animation:none; }} }}
</style>
</head>
<body>
<div class="wrap">
  <div class="barra"><span class="pts3"><i></i><i></i><i></i></span><span>henderseeds · estudio de motion / <b style="color:var(--ink);font-weight:500">estudio.xml</b></span><span class="sp"></span>
    <a href="../">Dashboard</a> · <a href="../kit/">Kit de la semana</a>
    <span class="pill">Con revisión</span><button class="btn pri" id="copiar-prompt">Copiar prompt</button><span class="ok" aria-live="polite"></span></div>

  <h1>Tu estudio de motion: <em>11 plantillas</em> para HenderSeeds</h1>
  <p class="bajada">Pegá el bloque del estudio una vez en la sesión y pedí cualquier plantilla por nombre. Completá los [corchetes]; los logos, las letras y los datos salen del repo. Cada tarjeta tiene su ejemplo real, los controles automáticos y el puntaje de revisión.</p>

  <div class="dos">
    <p class="bloque"><span class="t">&lt;rol&gt;</span> {e(texto("rol"))} <span class="t">&lt;/rol&gt;</span></p>
    <p class="bloque"><span class="t">&lt;como_pedir&gt;</span> {e(texto("como_pedir"))} <span class="t">&lt;/como_pedir&gt;</span></p>
  </div>

  <h2>&lt;plantillas&gt;</h2>
  <div class="grid">{"".join(tarjetas)}
  </div>
  <h2>&lt;/plantillas&gt;</h2>

  <div class="reglas">
    <div><span class="t">&lt;cada_plantilla&gt;</span> {e(texto("cada_plantilla"))} <span class="t">&lt;/cada_plantilla&gt;</span></div>
    <div><span class="t">&lt;revision&gt;</span> {e(texto("revision"))} <span class="t">&lt;/revision&gt;</span></div>
  </div>
</div>
<textarea id="xml" hidden>{e(xml_txt)}</textarea>
<script>
(function () {{
  function copiar(txt, boton) {{
    var aviso = document.querySelector('.barra .ok');
    var ok = function () {{ aviso.textContent = 'Copiado'; boton.classList.add('copiado'); setTimeout(function () {{ aviso.textContent = ''; }}, 2000); }};
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, function () {{ aviso.textContent = 'No se pudo copiar'; }});
  }}
  var xml = document.getElementById('xml').value;
  document.getElementById('copiar-prompt').addEventListener('click', function () {{ copiar(xml, this); }});
  document.querySelectorAll('[data-copiar]').forEach(function (b) {{ b.addEventListener('click', function () {{ copiar(b.dataset.copiar, b); }}); }});
  // los ejemplos se reproducen solos cuando se ven en pantalla (mudos); tocar pausa o reanuda
  var videos = Array.prototype.slice.call(document.querySelectorAll('video'));
  var quieto = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !quieto) {{
    var io = new IntersectionObserver(function (es) {{ es.forEach(function (x) {{ if (x.isIntersecting) x.target.play().catch(function () {{}}); else x.target.pause(); }}); }}, {{ threshold: 0.6 }});
    videos.forEach(function (v) {{ io.observe(v); }});
  }}
  videos.forEach(function (v) {{ v.addEventListener('click', function () {{ if (v.paused) v.play().catch(function () {{}}); else v.pause(); }}); }});
}})();
</script>
</body>
</html>
'''
os.makedirs(os.path.join(RAIZ, 'docs/estudio'), exist_ok=True)
salida = os.path.join(RAIZ, 'docs/estudio/index.html')
open(salida, 'w', encoding='utf-8').write(pagina)
print('  listo ->', os.path.relpath(salida, RAIZ), f'({os.path.getsize(salida) // 1024} KB)')
