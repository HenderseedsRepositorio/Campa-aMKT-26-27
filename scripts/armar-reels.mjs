#!/usr/bin/env node
/**
 * Página "Reels para arrancar" → docs/reels-siembra/index.html
 *
 * Junta los reels de la serie (docs/placas/*-reel-*.html con su hs-meta) en una sola
 * página: cada reel corre en vivo dentro de un celular (con la interfaz de Instagram
 * encima si se quiere ver qué tapa), con su tapa, el texto para copiar, audio sugerido,
 * pauta, fuentes, descargas y botones para aprobar / cambiar / descartar.
 *
 *   node scripts/armar-reels.mjs                         # versión del repo (links relativos)
 *   node scripts/armar-reels.mjs --autocontenida x.html  # un solo archivo para mandar por WhatsApp/mail
 */
import { readdir, readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DOCS = path.join(RAIZ, 'docs');
const DIR_PLACAS = path.join(DOCS, 'placas');
const RAMA = 'claude/gallant-hawking-qbdjlf';
const RAW = `https://github.com/HenderseedsRepositorio/Campa-aMKT-26-27/raw/${RAMA}/`;
const args = process.argv.slice(2);
const AUTO = args.includes('--autocontenida') ? args[args.indexOf('--autocontenida') + 1] : null;

/* Orden de publicación (el mismo del plan W40–W41). */
const REELS = ['reel-girasol-fecha', 'reel-whatsapp-lote', 'reel-ns1113', 'reel-girasol-phomopsis', 'reel-ns7925', 'reel-calculadora'];

const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const MIME = { '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2' };
const dataUri = async (ruta) => `data:${MIME[path.extname(ruta)]};base64,${(await readFile(ruta)).toString('base64')}`;

async function leerReels() {
  const piezas = {};
  for (const archivo of (await readdir(DIR_PLACAS)).filter((f) => f.endsWith('.html'))) {
    const html = await readFile(path.join(DIR_PLACAS, archivo), 'utf8');
    const m = html.match(/<script type="application\/json" class="hs-meta">([\s\S]*?)<\/script>/);
    if (!m) continue;
    const meta = JSON.parse(m[1]);
    if (!REELS.includes(meta.id)) continue;
    const estilo = ((html.match(/<style>([\s\S]*?)<\/style>/) || [])[1] || '').split('\n').filter((l) => !/^\s*body\s*\{/.test(l)).join('\n');
    const sprite = (html.match(/<svg width="0" height="0"[^>]*>([\s\S]*?)<\/svg>\s*\n\s*<script/) || [])[1] || '';
    // piezas del sprite: símbolos, bloques generados (girasol/maíz) y <defs> sueltos
    const partes = [
      ...[...sprite.matchAll(/<symbol\b[\s\S]*?<\/symbol>/g)].map((x) => x[0]),
      ...[...sprite.matchAll(/<!--@(girasol|maiz) defs-->([\s\S]*?)<!--\/@\1-->/g)].map((x) => x[2].trim()),
      ...[...sprite.replace(/<!--@(girasol|maiz) defs-->[\s\S]*?<!--\/@\1-->/g, '').matchAll(/<defs>[\s\S]*?<\/defs>/g)].map((x) => x[0]),
    ];
    const slides = {};
    for (const s of html.matchAll(/<section class="slide hs([^"]*)" id="([^"]+)" data-name="([^"]+)"([^>]*)>[\s\S]*?<\/section>/g)) {
      slides[s[2]] = { markup: s[0], id: s[2], nombre: s[3], anim: /\banim\b/.test(s[1]), dur: (s[4].match(/data-dur="([^"]+)"/) || [])[1] };
    }
    piezas[meta.id] = { archivo, meta, estilo, partes, slides };
  }
  const faltan = REELS.filter((id) => !piezas[id]);
  if (faltan.length) throw new Error('Faltan reels: ' + faltan.join(', '));
  return REELS.map((id) => piezas[id]);
}

const ICONOS = {
  corazon: '<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.7 4.5c2.1 0 3.6 1.2 5.3 3.2 1.7-2 3.2-3.2 5.3-3.2 3.7 0 5.8 3.9 4.3 7.3C19.5 16.4 12 21 12 21z"/></svg>',
  comentario: '<svg viewBox="0 0 24 24"><path d="M20.5 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20.5l1.6-4.6A8.5 8.5 0 1 1 20.5 11.5z"/></svg>',
  enviar: '<svg viewBox="0 0 24 24"><path d="M22 3 11 14M22 3l-7 19-4-8-8-4 19-7z"/></svg>',
};

function tarjeta(p, i, modo) {
  const { meta } = p;
  const R = p.slides[meta.opciones[0].slide];
  const T = p.slides[meta.opciones[1].slide];
  const base = modo === 'auto' ? RAW + 'docs/placas/' : '../placas/';
  const titulo = meta.concepto.replace(/^Reel · /, '');
  const texto = meta.caption + (meta.hashtags ? '\n\n' + meta.hashtags : '');
  const primeraLinea = meta.caption.split('\n')[0];
  const [dia, hora] = meta.fecha.split(' · ');
  return `<article class="rp-reel" id="r-${meta.id}" data-id="${meta.id}" data-nombre="${esc(titulo)}">
  <div class="rp-cel" id="cel-${meta.id}">
    <div class="rp-pantalla">
      ${R.markup}
      <div class="rp-ig" aria-hidden="true">
        <div class="ig-top"><span>Reels</span><span>◎</span></div>
        <div class="ig-lado"><div>${ICONOS.corazon}<small>Me gusta</small></div><div>${ICONOS.comentario}<small>0</small></div><div>${ICONOS.enviar}</div></div>
        <div class="ig-pie"><span class="ig-av"></span><b>henderseeds</b><span class="ig-seg">Seguir</span><p>${esc(primeraLinea)}</p><div class="ig-audio">♫ Audio en tendencia · Henderseeds</div></div>
      </div>
    </div>
    <div class="rp-botones">
      <button class="rp-btn" type="button" data-repetir="${R.id}">↻ Repetir</button>
      <button class="rp-btn" type="button" data-ig="cel-${meta.id}" aria-pressed="false">Ver lo que tapa Instagram</button>
    </div>
    <div class="rp-tapa">
      <div class="mini">${T.markup}</div>
      <p><b>Tapa para la grilla.</b> Lo oscuro es lo que recorta el perfil (3:4). Subila en "Editar portada".</p>
    </div>
  </div>
  <div class="rp-info">
    <div class="rp-cuando"><span class="n">${String(i + 1).padStart(2, '0')}</span><span>${esc(dia)} · ${esc(hora || '')}</span><span>· ${esc(meta.opciones[0].nombre.replace(/^Reel 9:16 · /, ''))}</span></div>
    <h2>${esc(titulo)}</h2>
    <p class="rp-porque">${esc(meta.porque)}</p>
    <div class="rp-bloque">
      <div class="rp-bloque-hd"><span class="rp-eyebrow">Texto para publicar</span><button class="rp-btn" type="button" data-copiar="cap-${meta.id}">Copiar texto</button></div>
      <pre class="rp-caption" id="cap-${meta.id}">${esc(texto)}</pre>
    </div>
    <dl class="rp-kv">
      <div><dt>Audio</dt><dd>${esc(meta.audio || 'Audio en tendencia desde la biblioteca de Instagram.')}</dd></div>
      <div><dt>Pauta</dt><dd>${esc(meta.pauta)}</dd></div>
    </dl>
    <details class="rp-fuentes"><summary>De dónde sale cada dato</summary><p>${esc(meta.fuentes)}</p></details>
    <div class="rp-dl">
      <a class="rp-btn" href="${base}video/${R.nombre}.mp4" download>⬇ MP4 del reel</a>
      <a class="rp-btn" href="${base}img/${T.nombre}-1080x1920.jpg" download>⬇ Tapa JPG</a>
      ${modo === 'auto' ? '' : `<a class="rp-btn" href="../placas/${p.archivo}">Abrir la pieza</a>`}
    </div>
    <div class="rp-aprob" role="group" aria-label="Revisión de ${esc(titulo)}">
      <button type="button" class="rp-ap" data-estado="ok" aria-pressed="false">✓ Aprobar</button>
      <button type="button" class="rp-ap" data-estado="cambiar" aria-pressed="false">✎ Cambiar</button>
      <button type="button" class="rp-ap" data-estado="no" aria-pressed="false">✕ Descartar</button>
      <label class="rp-nota" for="nota-${meta.id}" hidden><textarea id="nota-${meta.id}" placeholder="¿Qué cambiarías? Ej: otro título, más corto, otra fecha…"></textarea></label>
    </div>
  </div>
</article>`;
}

async function main() {
  const modo = AUTO ? 'auto' : 'repo';
  const reels = await leerReels();
  const partes = new Map();
  for (const p of reels) for (const x of p.partes) partes.set(x, true);
  const sprite = `<svg width="0" height="0" style="position:absolute" aria-hidden="true">${[...partes.keys()].join('\n')}</svg>`;
  const estilos = reels.map((p) => `/* ${p.archivo} */\n${p.estilo}`).join('\n');
  const orden = reels.map((p, i) => {
    const [dia] = p.meta.fecha.split(' · ');
    return `<a href="#r-${p.meta.id}"><small>${String(i + 1).padStart(2, '0')} · ${esc(dia)}</small><span>${esc(p.meta.concepto.replace(/^Reel · /, ''))}</span></a>`;
  }).join('\n');
  const durs = reels.map((p) => Math.round(parseFloat(p.slides[p.meta.opciones[0].slide].dur) * 2) / 2);

  let cuerpo = `${sprite}
<header class="rp-hero"><div class="rp-w">
  <div class="rp-eyebrow">HenderSeeds · Siembra 26/27</div>
  <h1>Reels para <span>arrancar.</span></h1>
  <p>Seis reels directos: un dato del marbete, una sola idea y el cierre a WhatsApp. Nada de explicarle al productor lo que ya sabe. Girasol dibujado en serio (capítulo, hojas y lote a contraluz), un híbrido nuestro de maíz con su tecnología y la barra que muestra cómo se reparte la hectárea.</p>
  <div class="rp-stats"><span><b>${reels.length}</b> reels</span><span><b>${Math.min(...durs).toLocaleString('es-AR')}–${Math.max(...durs).toLocaleString('es-AR')} s</b> cada uno</span><span>gancho en el <b>primer cuadro</b></span><span>cierre a <b>WhatsApp</b></span><span>sin precios ni descuentos</span></div>
  <div class="rp-guia">
    <div class="rp-paso"><b>1 · Subí el MP4</b><p>Como reel. En "Editar portada" elegí la tapa (JPG) para que la grilla quede prolija.</p></div>
    <div class="rp-paso"><b>2 · Pegá el texto</b><p>Con "Copiar texto": ya trae los hashtags. No hace falta tocar nada.</p></div>
    <div class="rp-paso"><b>3 · Sumá audio</b><p>Los videos vienen mudos a propósito: elegí un audio en tendencia desde Instagram (cada reel dice qué ritmo le va).</p></div>
  </div>
  <div class="rp-eyebrow" style="margin-top:24px">Orden para publicar</div>
  <nav class="rp-orden" aria-label="Orden de publicación">${orden}</nav>
</div></header>
<main class="rp-w">
${reels.map((p, i) => tarjeta(p, i, modo)).join('\n')}
<footer class="rp-pie">
  <h3>Lo que sacamos y lo que viene</h3>
  <ul>
    <li>Afuera: el almanaque, el reel del refugio, "cómo leer un marbete" y el teaser del "3". El productor ya sabe leer un marbete: le damos el dato y el pedido de contacto.</li>
    <li>El reel de maíz muestra un híbrido nuestro (NS 7925 VIPTERA3) con los datos del marbete, sin comparar ensayos.</li>
    <li>El de márgenes muestra cómo se reparte la hectárea (ejemplo ilustrativo, sin números) y lleva a la calculadora: los números los pone cada uno.</li>
    <li>Próxima tanda: placas de girasol directas (dato útil + pedido de contacto), para intercalar desde la semana del 12/10.</li>
    <li>Sin música con derechos fuera de la biblioteca de Instagram. Sin precios, descuentos ni condiciones comerciales: la venta sigue en privado.</li>
  </ul>
</footer>
</main>
<div class="rp-barra" id="rp-barra" hidden><div class="rp-w">
  <div class="rp-cuenta"><b id="n-ok">0</b> aprobados · <b id="n-cambiar">0</b> a cambiar · <b id="n-no">0</b> descartados · <b id="n-pend">${reels.length}</b> sin ver</div>
  <button class="rp-btn" id="rp-resumen" type="button">Copiar resumen</button>
  <pre class="rp-resumen-txt" id="rp-resumen-txt"></pre>
</div></div>`;

  const cssPagina = await readFile(path.join(RAIZ, 'scripts/lib/reels.css'), 'utf8');
  const jsPagina = await readFile(path.join(RAIZ, 'scripts/lib/reels.js'), 'utf8');
  let head, runtime;
  if (modo === 'repo') {
    head = `<link rel="stylesheet" href="../assets/fonts/fuentes.css">\n<link rel="stylesheet" href="../assets/hs2627.css">\n<style>${cssPagina}\n${estilos}</style>`;
    runtime = '<script src="../assets/hs-anim.js"></script>';
  } else {
    let fuentes = await readFile(path.join(DOCS, 'assets/fonts/fuentes.css'), 'utf8');
    for (const m of [...fuentes.matchAll(/url\(([^)]+\.woff2)\)/g)]) fuentes = fuentes.replace(m[0], `url(${await dataUri(path.join(DOCS, 'assets/fonts', m[1]))})`);
    head = `<style>${fuentes}\n${await readFile(path.join(DOCS, 'assets/hs2627.css'), 'utf8')}\n${cssPagina}\n${estilos}</style>`;
    runtime = `<script>${await readFile(path.join(DOCS, 'assets/hs-anim.js'), 'utf8')}</script>`;
    const cache = new Map();
    for (const f of new Set([...cuerpo.matchAll(/\.\.\/assets\/([\w.-]+\.(?:png|svg|jpg))/g)].map((m) => m[1]))) cache.set(f, await dataUri(path.join(DOCS, 'assets', f)));
    cuerpo = cuerpo.replace(/\.\.\/assets\/([\w.-]+\.(?:png|svg|jpg))/g, (_, f) => cache.get(f));
  }

  const html = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Reels para arrancar</title>
<meta name="description" content="HenderSeeds · Siembra 26/27: seis reels directos con dato del marbete y cierre a WhatsApp, listos para publicar.">
${head}
</head>
<body class="rp">
${cuerpo}
${runtime}
<script>${jsPagina}</script>
</body>
</html>
`;
  const salida = AUTO ? path.resolve(AUTO) : path.join(DOCS, 'reels-siembra', 'index.html');
  await mkdir(path.dirname(salida), { recursive: true });
  await writeFile(salida, html, 'utf8');
  console.log(`  reels -> ${path.relative(RAIZ, salida) || salida}  (${(html.length / 1024).toFixed(0)} KB)`);
}

main().catch((e) => { console.error(e); process.exit(1); });
