#!/usr/bin/env node
/**
 * Arma la página única de propuesta a partir de las placas del sistema 26/27.
 *
 * Fuente de verdad: cada docs/placas/*.html que trae <script class="hs-meta">
 * (copy, hashtags, horario, pauta, fuentes, opciones). Esta página no repite
 * nada a mano: si cambiás una placa o su texto, volvés a correr esto.
 *
 * Uso:
 *   npm run propuesta
 *       -> docs/propuesta/index.html (links relativos, para GitHub Pages)
 *   node scripts/armar-propuesta.mjs --autocontenida salida.html [--livianos dir]
 *       -> un solo archivo con todo adentro (fuentes, imágenes, CSS y JS),
 *          para abrir sin internet o mandar por WhatsApp.
 *   node scripts/armar-propuesta.mjs --posts
 *       -> además escribe los posts/2026-Wxx/*.md del plan (formato de la plantilla).
 */

import { readdir, readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DOCS = path.join(RAIZ, 'docs');
const DIR_PLACAS = path.join(DOCS, 'placas');
const PAGES = 'https://henderseedsrepositorio.github.io/Campa-aMKT-26-27/';
const RAMA = 'claude/gallant-hawking-qbdjlf';
const RAW = `https://github.com/HenderseedsRepositorio/Campa-aMKT-26-27/raw/${RAMA}/`;

const args = process.argv.slice(2);
const AUTO = args.includes('--autocontenida') ? args[args.indexOf('--autocontenida') + 1] : null;
const LIVIANOS = args.includes('--livianos') ? args[args.indexOf('--livianos') + 1] : null;
const POSTS = args.includes('--posts');

/* ── Orden y grupos de la galería ─────────────────────────────────────── */
const ORDEN = [
  'girasol-ventana', 'refugio-ns7800', 'somos-de-aca', 'historias-interactivas',
  'girasol-carrusel', 'calculadora-maiz-girasol', 'maiz-tardio-ranking', 'ns7925-spiroplasma',
  'rinde-indiferencia', 'dia-de-la-madre', 'ns7765-dos-fechas', 'implantacion',
  'finanzas-pesos-dolares', 'como-leer-un-marbete', 'ns7624-malezas', 'dia-de-la-tradicion',
];
const GRUPO = {
  'girasol-ventana': 'girasol', 'girasol-carrusel': 'girasol',
  'refugio-ns7800': 'maiz', 'maiz-tardio-ranking': 'maiz', 'ns7925-spiroplasma': 'maiz',
  'ns7765-dos-fechas': 'maiz', 'ns7624-malezas': 'maiz',
  'calculadora-maiz-girasol': 'herramientas', 'rinde-indiferencia': 'herramientas', 'finanzas-pesos-dolares': 'herramientas',
  'somos-de-aca': 'institucional', 'implantacion': 'institucional', 'como-leer-un-marbete': 'institucional',
  'dia-de-la-madre': 'institucional', 'dia-de-la-tradicion': 'institucional',
  'historias-interactivas': 'historias',
};

/* ── Plan de 7 semanas (W40–W46) ──────────────────────────────────────── */
const PLAN = [
  { sem: 'W40', rango: '28/09 – 04/10', foco: 'Volver con lo útil', items: [
    { dia: 'lun 28/09', hora: '7–9 h', pieza: 'girasol-ventana', slide: 'girasol-ventana-A', tipo: 'Placa', nota: 'Pauta liviana 5 días' },
    { dia: 'mié 30/09', hora: 'historia', pieza: 'historias-interactivas', slide: 'hist-1', tipo: 'Historia', nota: 'Encuesta' },
    { dia: 'jue 01/10', hora: '12–14 h', pieza: 'refugio-ns7800', slide: 'ref-A', tipo: 'Placa' },
    { dia: 'vie 02/10', hora: '20–22 h', pieza: 'girasol-ventana', slide: 'girasol-ventana-R', tipo: 'Reel',
      caption: '¿Cuándo va el girasol en el oeste? 🌻\n\nDel 15/10 al 15/11, con fecha límite el 20/11. Lo dice el marbete Nidera para el Oeste de Buenos Aires.\n\nGuardalo para la siembra. ¿Cuál va en tu lote? Mandanos un DM.',
      pauta: 'No: la pauta de la semana va en la placa del lunes.' },
    { dia: 'sáb 03/10', hora: '8–10 h', pieza: 'somos-de-aca', slide: 'aca-A', tipo: 'Placa', nota: '+ reel del mapa en historias' },
  ] },
  { sem: 'W41', rango: '05/10 – 11/10', foco: 'Girasol y la decisión del lote', items: [
    { dia: 'mar 06/10', hora: '20–22 h', pieza: 'girasol-carrusel', slide: 'gc-1', tipo: 'Carrusel' },
    { dia: 'mié 07/10', hora: '20–22 h', pieza: 'calculadora-maiz-girasol', slide: 'calc-A', tipo: 'Placa', nota: '+ historia con link' },
    { dia: 'jue 08/10', hora: '12–14 h', pieza: 'maiz-tardio-ranking', slide: 'tardio-A', tipo: 'Placa' },
    { dia: 'vie 09/10', hora: 'historia', pieza: 'historias-interactivas', slide: 'hist-2', tipo: 'Historia', nota: 'Encuesta tardío' },
    { dia: 'dom 11/10', hora: '20–22 h', pieza: 'maiz-tardio-ranking', slide: 'tardio-R', tipo: 'Reel', nota: 'Pautado 7 días',
      caption: '5 marbetes, un mismo criterio: así rinden en siembra tardía. 🌽\n\nKilos por hectárea arriba del promedio de cada sitio de ensayo, según los marbetes Nidera 26/27. Todas diferencias significativas.\n\n¿Cuál va en tu lote tardío? Mandanos un DM y lo vemos.' },
  ] },
  { sem: 'W42', rango: '12/10 – 18/10', foco: 'Abre la ventana del girasol', items: [
    { dia: 'lun 12/10', hora: 'historia', pieza: 'historias-interactivas', slide: 'hist-3', tipo: 'Historia', nota: 'Caja de preguntas' },
    { dia: 'mar 13/10', hora: '7–9 h', pieza: 'ns7925-spiroplasma', slide: 's7925-A', tipo: 'Placa' },
    { dia: 'mié 14/10', hora: 'historia', pieza: 'historias-interactivas', slide: 'hist-4', tipo: 'Historia', nota: 'Cuenta regresiva al 15/10' },
    { dia: 'jue 15/10', hora: '20–22 h', pieza: 'rinde-indiferencia', slide: 'rind-A', tipo: 'Placa' },
    { dia: 'dom 18/10', hora: '8–10 h', pieza: 'dia-de-la-madre', slide: 'madre-A', tipo: 'Efeméride' },
  ] },
  { sem: 'W43', rango: '19/10 – 25/10', foco: 'Tardío y servicio', items: [
    { dia: 'lun 19/10', hora: '7–9 h', pieza: 'ns7765-dos-fechas', slide: 'n7765-A', tipo: 'Placa' },
    { dia: 'mié 21/10', hora: '7–9 h', pieza: 'implantacion', slide: 'impl-A', tipo: 'Placa', nota: 'Mejor con 1–3 fotos reales' },
    { dia: 'jue 22/10', hora: '20–22 h', pieza: 'ns7925-spiroplasma', slide: 's7925-R', tipo: 'Reel',
      caption: 'Tardío y chicharrita: mirá este número. 🌽\n\nSpiroplasma 3 en la escala del marbete Nidera (1 es excelente, 9 deficiente): el mejor puntaje del portafolio de maíz. Es el NS 7925 VIPTERA3, lanzamiento 26/27.\n\nEl híbrido suma; el manejo integrado sigue siendo la base. ¿Lo vemos para tu lote? Mandanos un DM.',
      pauta: 'Opcional: segundo reel para pautar si el del ranking dio buen costo por conversación.' },
    { dia: 'sáb 24/10', hora: '8–10 h', pieza: null, tipo: 'Foto real', nota: '[COMPLETAR] el equipo sembrando o recorriendo un lote' },
  ] },
  { sem: 'W44', rango: '26/10 – 01/11', foco: 'Enseñar a leer el dato', items: [
    { dia: 'mar 27/10', hora: '12–14 h', pieza: 'finanzas-pesos-dolares', slide: 'fin-A', tipo: 'Placa' },
    { dia: 'jue 29/10', hora: '20–22 h', pieza: 'como-leer-un-marbete', slide: 'lm-1', tipo: 'Carrusel', nota: 'Fijarlo en el perfil' },
    { dia: 'sáb 31/10', hora: '8–10 h', pieza: null, tipo: 'Foto real', nota: '[COMPLETAR] un lote de girasol recién nacido' },
  ] },
  { sem: 'W45', rango: '02/11 – 08/11', foco: 'Tardío: el lote difícil', items: [
    { dia: 'lun 02/11', hora: '7–9 h', pieza: 'ns7624-malezas', slide: 'n7624-A', tipo: 'Placa' },
    { dia: 'mié 04/11', hora: '20–22 h', pieza: 'refugio-ns7800', slide: 'ref-R', tipo: 'Reel', nota: 'Para quien planifica el tardío',
      caption: '¿Ya pensaste el refugio del tardío? 🌽\n\n1 de cada 10 plantas: así se ve el refugio en el lote. Es lo que hace que VIPTERA3 siga funcionando campaña tras campaña.\n\nEl refugio del portafolio es el NS 7800 CLTG. ¿Lo planificamos juntos? Mandanos un DM.' },
    { dia: 'vie 06/11', hora: 'historia', pieza: 'calculadora-maiz-girasol', slide: 'calc-S', tipo: 'Historia', nota: 'Con sticker de link' },
  ] },
  { sem: 'W46', rango: '09/11 – 15/11', foco: 'Cierre de ventana', items: [
    { dia: 'mar 10/11', hora: '8–10 h', pieza: 'dia-de-la-tradicion', slide: 'trad-S', tipo: 'Historia' },
    { dia: 'mié 11/11', hora: '7–9 h', pieza: 'girasol-ventana', slide: 'girasol-ventana-B', tipo: 'Placa', nota: 'Recordatorio: límite 20/11',
      objetivo: 'Último empujón para el girasol que todavía no se sembró: recordatorio con dato de marbete.', pauta: 'No.',
      caption: 'Última semana de la ventana óptima del girasol en el oeste. 🌻\n\nSegún el marbete Nidera, la fecha óptima de siembra va hasta el 15/11 y la fecha límite es el 20/11. Si todavía te queda girasol por sembrar, es ahora.\n\nGuardá el almanaque y, si tenés dudas con el híbrido para ese lote, mandanos un DM.\n\n📲 WhatsApp: wa.me/5492314530691' },
    { dia: 'jue 12/11', hora: '20–22 h', pieza: 'maiz-tardio-ranking', slide: 'tardio-R', tipo: 'Reel', nota: 'Re-pauta: diciembre se define en noviembre',
      objetivo: 'Último empujón del tardío antes de diciembre.', pauta: 'Sí: re-pauta 5 días, excluyendo a quienes ya escribieron.',
      caption: 'Diciembre se define en noviembre. 🌽\n\nSi vas a sembrar maíz tardío, este es el momento de elegir el híbrido para cada lote. Los marbetes Nidera 26/27 dicen esto en siembra tardía templada (kg/ha sobre el promedio de cada sitio):\n\nNS 7765 · +324 · NS 7925 · +228 · NS 7852 · +194 · NS 7921 CL · +179 · NS 7624 CL · +163\n\nEl ambiente y el manejo mandan: por eso lo vemos lote por lote.\n📩 Mandanos un DM con tu lote tardío.' },
  ] },
];

/* ── utilidades ───────────────────────────────────────────────────────── */
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const MIME = { '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2' };

async function dataUri(ruta) {
  const buf = await readFile(ruta);
  return `data:${MIME[path.extname(ruta)]};base64,${buf.toString('base64')}`;
}

async function leerPiezas() {
  const archivos = (await readdir(DIR_PLACAS)).filter((f) => f.endsWith('.html')).sort();
  const piezas = {};
  for (const archivo of archivos) {
    const html = await readFile(path.join(DIR_PLACAS, archivo), 'utf8');
    const m = html.match(/<script type="application\/json" class="hs-meta">([\s\S]*?)<\/script>/);
    if (!m) continue; // placas viejas: no son del sistema 26/27
    const meta = JSON.parse(m[1]);
    const estilo = ((html.match(/<style>([\s\S]*?)<\/style>/) || [])[1] || '')
      .split('\n').filter((l) => !/^\s*body\s*\{/.test(l)).join('\n');
    const simbolos = [...html.matchAll(/<(symbol|pattern)\b[^>]*\bid="([^"]+)"[\s\S]*?<\/\1>/g)]
      .map((x) => ({ id: x[2], markup: x[0] }));
    const slides = {};
    for (const s of html.matchAll(/<section class="slide hs([^"]*)" id="([^"]+)" data-name="([^"]+)"([^>]*)>[\s\S]*?<\/section>/g)) {
      slides[s[2]] = {
        markup: s[0], id: s[2], nombre: s[3],
        story: /\bstory\b/.test(s[1]), anim: /\banim\b/.test(s[1]),
        dur: (s[4].match(/data-dur="([^"]+)"/) || [])[1],
      };
    }
    piezas[meta.id] = { archivo, meta, estilo, simbolos, slides };
  }
  return piezas;
}

/* ── bloques de la página ─────────────────────────────────────────────── */
function descargas(p, s, modo) {
  const baseImg = modo === 'auto' ? PAGES + 'placas/img/' : '../placas/img/';
  const baseVid = modo === 'auto' ? RAW + 'docs/placas/video/' : '../placas/video/';
  const baseHtml = modo === 'auto' ? PAGES + 'placas/' : '../placas/';
  const links = [];
  if (s.anim) links.push(`<a href="${baseVid}${s.nombre}.mp4">MP4</a>`);
  if (!s.story) links.push(`<a href="${baseImg}${s.nombre}-feed-1080x1350.jpg">JPG feed</a>`);
  links.push(s.story
    ? `<a href="${baseImg}${s.nombre}-1080x1920.jpg">JPG 9:16</a>`
    : `<a href="${baseImg}${s.nombre}-historia-1080x1920.jpg">JPG historia</a>`);
  links.push(`<a href="${baseHtml}${p.archivo}">HTML</a>`);
  return links.join('');
}

function tarjetaPieza(p, modo) {
  const { meta } = p;
  const grupo = GRUPO[meta.id] || 'otros';
  const ops = meta.opciones.map((o) => {
    const s = p.slides[o.slide];
    if (!s) throw new Error(`Falta la slide ${o.slide} en ${p.archivo}`);
    const replay = s.anim ? `<button class="pp-replay" type="button" data-slide="${s.id}" aria-label="Repetir animación">↻ Repetir</button>` : '';
    return `<figure class="pp-op${s.story ? ' is-story' : ''}">
        <div class="pv">${s.markup}</div>
        <figcaption>
          <b>${esc(o.nombre)}</b>${o.nota ? `<span>${esc(o.nota)}</span>` : ''}
          <span class="pp-dl">${replay}${descargas(p, s, modo)}</span>
        </figcaption>
      </figure>`;
  }).join('\n');
  const texto = meta.caption + (meta.hashtags ? '\n\n' + meta.hashtags : '');
  const extras = PLAN.flatMap((w) => w.items.filter((it) => it.pieza === meta.id && it.caption).map((it) => ({ ...it, sem: w.sem })));
  const bloquesExtra = extras.map((it, i) => `
    <div class="pp-texto">
      <div class="pp-texto-hd"><span class="pp-eyebrow">Texto ${({ Reel: 'del reel', Placa: 'de la placa', Historia: 'de la historia', Carrusel: 'del carrusel' })[it.tipo] || ''} · ${esc(it.dia)}</span><button class="pp-copy" type="button" data-target="cap-${meta.id}-${i}">Copiar texto</button></div>
      <pre class="pp-caption" id="cap-${meta.id}-${i}">${esc(it.caption + (meta.hashtags ? '\n\n' + meta.hashtags : ''))}</pre>
    </div>`).join('');
  return `<article class="pp-pieza" id="p-${meta.id}" data-grupo="${grupo}">
    <header class="pp-pieza-hd">
      <div>
        <div class="pp-eyebrow">${esc(meta.semana)} · ${esc(meta.pilar)}</div>
        <h3 class="pp-h3">${esc(meta.concepto)}</h3>
      </div>
      <div class="pp-when">${esc(meta.fecha)}</div>
    </header>
    <p class="pp-porque">${esc(meta.porque)}</p>
    <div class="pp-ops">${ops}</div>
    <div class="pp-texto">
      <div class="pp-texto-hd"><span class="pp-eyebrow">Texto para publicar</span><button class="pp-copy" type="button" data-target="cap-${meta.id}">Copiar texto</button></div>
      <pre class="pp-caption" id="cap-${meta.id}">${esc(texto)}</pre>
    </div>${bloquesExtra}
    <dl class="pp-kv">
      <div><dt>Pauta</dt><dd>${esc(meta.pauta)}</dd></div>
      <div><dt>Fuentes</dt><dd>${esc(meta.fuentes)}</dd></div>
    </dl>
  </article>`;
}

function bloquePlan(piezas) {
  const chip = { 'Placa': 'c-placa', 'Carrusel': 'c-carrusel', 'Reel': 'c-reel', 'Historia': 'c-historia', 'Efeméride': 'c-efe', 'Foto real': 'c-foto' };
  return PLAN.map((w) => `<div class="pp-sem">
      <div class="pp-sem-hd"><b>${w.sem}</b><span>${w.rango}</span><em>${esc(w.foco)}</em></div>
      <ul class="pp-sem-items">
        ${w.items.map((it) => {
          const p = it.pieza && piezas[it.pieza];
          // Historias: el nombre de la opción dice más que el concepto general.
          const op = p && p.meta.opciones.find((o) => o.slide === it.slide);
          const nombre = !p ? '' : it.pieza === 'historias-interactivas' && op ? op.nombre.replace(/\s*\(W\d+\)$/, '')
            : p.meta.concepto + (it.tipo === 'Reel' ? ' · reel' : '');
          const titulo = p ? `<a href="#p-${it.pieza}">${esc(nombre)}</a>` : `<span class="pp-falta">${esc(it.nota)}</span>`;
          const nota = p && it.nota ? `<small>${esc(it.nota)}</small>` : '';
          return `<li><span class="pp-dia">${esc(it.dia)}<small>${esc(it.hora)}</small></span><span class="pp-chip ${chip[it.tipo] || ''}">${esc(it.tipo)}</span><span class="pp-que">${titulo}${nota}</span></li>`;
        }).join('\n        ')}
      </ul>
    </div>`).join('\n');
}

/* ── posts .md del plan (formato posts/_plantilla-post.md) ───────────── */
async function escribirPosts(piezas) {
  const hechos = [];
  for (const w of PLAN) {
    const carpeta = path.join(RAIZ, 'posts', `2026-${w.sem}`);
    await mkdir(carpeta, { recursive: true });
    let n = 0;
    const vistos = new Set();
    for (const it of w.items) {
      if (!it.pieza || it.tipo === 'Historia') continue;
      const clave = it.pieza + '|' + it.slide;
      if (vistos.has(clave)) continue;
      vistos.add(clave);
      n++;
      const p = piezas[it.pieza];
      const s = p.slides[it.slide];
      const op = p.meta.opciones.find((o) => o.slide === it.slide) || p.meta.opciones[0];
      const formato = { Placa: 'placa simple (1080×1350)', Carrusel: 'carrusel (1080×1350 por slide)', Reel: 'reel 9:16 (MP4)', 'Efeméride': 'placa efeméride (1080×1350)' }[it.tipo] || it.tipo;
      const archivoMd = path.join(carpeta, `post-${String(n).padStart(2, '0')}-${it.pieza}${it.tipo === 'Reel' ? '-reel' : ''}.md`);
      const pieza = s.anim
        ? `\`docs/placas/${p.archivo}\` → slide \`${s.id}\` · video: \`docs/placas/video/${s.nombre}.mp4\``
        : `\`docs/placas/${p.archivo}\` → slide \`${s.id}\` · JPG: \`docs/placas/img/${s.nombre}-feed-1080x1350.jpg\` (lo genera \`npm run placas\`)`;
      const caption = it.caption || p.meta.caption;
      const notaOp = (op.nota || '').replace(/\.\s*$/, '');
      const md = `# Post ${String(n).padStart(2, '0')} — ${p.meta.concepto}${it.tipo === 'Reel' ? ' (reel)' : ''}

- **Semana:** 2026-${w.sem} · publicación tentativa: ${it.dia} · ${it.hora}
- **Pilar:** ${p.meta.pilar}
- **Formato:** ${formato} → ${pieza}
- **Objetivo:** ${it.objetivo || p.meta.porque}
- **Pauta:** ${it.pauta || p.meta.pauta}${it.nota ? `\n- **Nota del plan:** ${it.nota}` : ''}

## Copy (Instagram/Facebook)
${caption.split('\n').map((l) => '> ' + l).join('\n')}

## Pieza visual
Opción elegida en el plan: **${op.nombre}**${notaOp ? ` — ${notaOp}` : ''}. Sistema visual "Siembra 26/27"
(\`docs/assets/hs2627.css\`): navy + ámbar, Archivo Black / DM Sans / DM Mono, logo HenderSeeds arriba a la derecha,
sello RED.IN Nidera abajo. Todas las opciones de la pieza: \`docs/placas/${p.archivo}\` y la página
\`docs/propuesta/index.html#p-${p.meta.id}\`.

## Hashtags (máx 8)
${p.meta.hashtags || '—'}

## CTA
Primario: 📩 Mandanos un DM. · Secundario: WhatsApp wa.me/5492314530691 (va en la placa y en la bio).

## Fuentes de los datos usados
- ${p.meta.fuentes}

## Estado
- [x] ✍️ Borrador (propuesta 24/09/2026)
- [ ] ✅ Aprobado
- [ ] 📤 Publicado → link:
- [ ] 📣 Pautado → brief:
`;
      await writeFile(archivoMd, md, 'utf8');
      hechos.push(path.relative(RAIZ, archivoMd));
    }
  }
  return hechos;
}

/* ── armado ───────────────────────────────────────────────────────────── */
async function main() {
  const piezas = await leerPiezas();
  const faltan = ORDEN.filter((id) => !piezas[id]);
  if (faltan.length) throw new Error('Faltan piezas: ' + faltan.join(', '));

  const modo = AUTO ? 'auto' : 'repo';
  const orden = [...ORDEN, ...Object.keys(piezas).filter((id) => !ORDEN.includes(id))];

  // Símbolos SVG (íconos, tramas) sin repetir ids.
  const simbolos = new Map();
  for (const id of orden) for (const s of piezas[id].simbolos) if (!simbolos.has(s.id)) simbolos.set(s.id, s.markup);
  const sprite = `<svg width="0" height="0" style="position:absolute" aria-hidden="true">${[...simbolos.values()].join('\n')}</svg>`;

  // La placa del NS 7765 aparece dos veces (galería y "antes y después"): la copia
  // lleva otro id, así que se duplican sus reglas para ese id.
  const estilosPiezas = orden.map((id) => `/* ${piezas[id].archivo} */\n${piezas[id].estilo}`).join('\n')
    + '\n' + piezas['ns7765-dos-fechas'].estilo.replaceAll('#n7765-A', '#n7765-A-cmp');
  let galeria = orden.map((id) => tarjetaPieza(piezas[id], modo)).join('\n');
  let antes = 'antes-w31-ns7765.jpg';
  const n7765 = piezas['ns7765-dos-fechas'].slides['n7765-A'].markup.replace('id="n7765-A"', 'id="n7765-A-cmp"');

  let head, scriptAnim;
  const cssPagina = await readFile(path.join(RAIZ, 'scripts/lib/propuesta.css'), 'utf8');
  const jsPagina = await readFile(path.join(RAIZ, 'scripts/lib/propuesta.js'), 'utf8');

  let cuerpo = (await readFile(path.join(RAIZ, 'scripts/lib/propuesta.html'), 'utf8'))
    .replace('{{PLAN}}', bloquePlan(piezas))
    .replace('{{PIEZAS}}', galeria)
    .replaceAll('{{N_PIEZAS}}', String(orden.length))
    .replaceAll('{{N_PLACAS}}', String(orden.reduce((a, id) => a + Object.keys(piezas[id].slides).length, 0)))
    .replaceAll('{{N_VIDEOS}}', String(orden.reduce((a, id) => a + Object.values(piezas[id].slides).filter((s) => s.anim).length, 0)))
    .replace('{{COMPARA_NUEVA}}', n7765)
    .replace('{{SPRITE}}', sprite);

  if (modo === 'repo') {
    head = `<link rel="stylesheet" href="../assets/fonts/fuentes.css">
<link rel="stylesheet" href="../assets/hs2627.css">
<style>${cssPagina}
/* ── estilos propios de cada placa ── */
${estilosPiezas}</style>`;
    scriptAnim = `<script src="../assets/hs-anim.js"></script>`;
    cuerpo = cuerpo.replace('{{ANTES}}', antes);
  } else {
    // Todo adentro: fuentes, CSS, JS e imágenes como data URI.
    let fuentes = await readFile(path.join(DOCS, 'assets/fonts/fuentes.css'), 'utf8');
    for (const m of [...fuentes.matchAll(/url\(([^)]+\.woff2)\)/g)]) {
      fuentes = fuentes.replace(m[0], `url(${await dataUri(path.join(DOCS, 'assets/fonts', m[1]))})`);
    }
    const hs = await readFile(path.join(DOCS, 'assets/hs2627.css'), 'utf8');
    head = `<style>${fuentes}\n${hs}\n${cssPagina}\n${estilosPiezas}</style>`;
    scriptAnim = `<script>${await readFile(path.join(DOCS, 'assets/hs-anim.js'), 'utf8')}</script>`;
    const cache = new Map();
    const refs = [...new Set([...cuerpo.matchAll(/\.\.\/assets\/([\w.-]+\.(?:png|svg|jpg))/g)].map((m) => m[1]))];
    for (const f of refs) {
      const liviano = LIVIANOS && existsSync(path.join(LIVIANOS, f)) ? path.join(LIVIANOS, f) : path.join(DOCS, 'assets', f);
      cache.set(f, await dataUri(liviano));
    }
    cuerpo = cuerpo.replace(/\.\.\/assets\/([\w.-]+\.(?:png|svg|jpg))/g, (_, f) => cache.get(f));
    cuerpo = cuerpo.replace('{{ANTES}}', await dataUri(path.join(DOCS, 'propuesta', antes)));
  }

  const html = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Relanzamiento Siembra 26/27</title>
<meta name="description" content="Propuesta HenderSeeds: diagnóstico del repo, plan de 7 semanas (W40–W46) y placas, carruseles, historias y animaciones listas para publicar.">
${head}
</head>
<body class="pp">
${cuerpo}
${scriptAnim}
<script>${jsPagina}</script>
</body>
</html>
`;
  const salida = AUTO ? path.resolve(AUTO) : path.join(DOCS, 'propuesta', 'index.html');
  await mkdir(path.dirname(salida), { recursive: true });
  await writeFile(salida, html, 'utf8');
  console.log(`  propuesta -> ${path.relative(RAIZ, salida) || salida}  (${(html.length / 1024).toFixed(0)} KB)`);

  if (POSTS) {
    const hechos = await escribirPosts(piezas);
    console.log(`  ${hechos.length} posts .md:`);
    hechos.forEach((h) => console.log('   - ' + h));
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
