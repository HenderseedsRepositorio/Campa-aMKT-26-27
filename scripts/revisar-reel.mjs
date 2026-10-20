#!/usr/bin/env node
/**
 * Revisión de un reel (paso <revision> del estudio, produccion/estudio/estudio.xml).
 *
 * Saca 20 cuadros repartidos en todo el video y arma una hoja de contacto, y controla solo lo que
 * se puede medir: texto fuera de la zona segura de Instagram, letra chica, palabras en pantalla,
 * gancho visible desde el cuadro 0 y cuadros sin texto. El puntaje de director creativo lo pone
 * una persona (o Claude) mirando la hoja; esto le ahorra buscar los errores a ojo.
 *
 * Uso:
 *   node scripts/revisar-reel.mjs produccion/sintetico/reel-op1-verdadero-falso.html [--n 20] [--v 3] [--q "a=1"]
 * Salida:
 *   produccion/sintetico/out/revision/<nombre>-hoja.jpg   (hoja de contacto, no se commitea)
 *   produccion/estudio/revision/<nombre>.json             (controles, se commitea)
 */
import { chromium } from 'playwright';
import { mkdtemp, readFile, rm, mkdir, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CSS_FUENTES = path.join(RAIZ, 'docs/assets/fonts/fuentes.css');
const ZONA = { x0: 80, x1: 930, y0: 250, y1: 1540 };   // zona segura de Instagram (canvas 1080x1920)
const MIN_PX = 19, LECTURA_PX = 30, MAX_PALABRAS = 30;

const args = process.argv.slice(2);
const valor = (n, d) => (args.includes(n) ? args[args.indexOf(n) + 1] : d);
const CON_VALOR = ['--n', '--v', '--q', '--modo'];
const entrada = path.resolve(args.find((a, i) => !a.startsWith('--') && !CON_VALOR.includes(args[i - 1])) || '');
const N = Number(valor('--n', 20));
const VERSION = valor('--v', ''), MODO = valor('--modo', '');
const QUERY = [MODO && 'modo=' + MODO, VERSION && 'v=' + VERSION, valor('--q', '')].filter(Boolean).join('&');
const nombre = path.basename(entrada, '.html') + (VERSION ? '-v' + VERSION : '') + (MODO ? '-' + MODO : '');

const cssFuentes = (await readFile(CSS_FUENTES, 'utf8')).replace(
  /url\((?!['"]?(?:data:|file:|https?:))['"]?([^)'"]+)['"]?\)/g,
  (_, f) => `url("file://${path.join(path.dirname(CSS_FUENTES), f)}")`
);
const nav = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const pag = await nav.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await pag.addInitScript(() => { window.__RENDER_MODE__ = true; });
await pag.goto('file://' + entrada + (QUERY ? '?' + QUERY : ''), { waitUntil: 'load' });
await pag.addStyleTag({ content: cssFuentes });
await pag.evaluate(() => document.fonts.ready);
await pag.evaluate(() => window.render(window.REEL_DURACION * 0.5));
await pag.evaluate(() => document.fonts.ready);
await pag.evaluate(() => window.reajustar && window.reajustar());
await pag.evaluate(() => (window.LISTO ? window.LISTO.then(() => true) : true));
const dur = await pag.evaluate(() => window.REEL_DURACION);

// Mide el texto visible en el cuadro actual: cada nodo de texto con su caja real y su opacidad efectiva
const medir = (z) => {
  const stage = document.getElementById('stage'), base = stage.getBoundingClientRect();
  const opac = (el) => { let o = 1; for (let e = el; e && e !== document.body; e = e.parentElement) { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden') return 0; o *= parseFloat(s.opacity); } return o; };
  const out = [];
  const w = document.createTreeWalker(stage, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const txt = n.textContent.replace(/\s+/g, ' ').trim();
    if (!txt) continue;
    const el = n.parentElement; if (!el || el.closest('script,style,[data-deco]')) continue;   // data-deco: texto decorativo a propósito (cintas, marcas de agua)
    const o = opac(el); if (o < 0.6) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const b = r.getBoundingClientRect(); if (b.width < 1 || b.height < 1) continue;
    const x0 = b.left - base.left, y0 = b.top - base.top, x1 = x0 + b.width, y1 = y0 + b.height;
    if (x1 < 0 || y1 < 0 || x0 > 1080 || y0 > 1920) continue;   // fuera del cuadro: no se ve
    // tamaño real en pantalla: font-size por la escala acumulada de las transformaciones
    const fs = parseFloat(getComputedStyle(el).fontSize);
    let esc = 1; for (let e = el; e && e !== stage; e = e.parentElement) { const t = getComputedStyle(e).transform; if (t && t !== 'none') { const d = new DOMMatrix(t); esc *= Math.hypot(d.a, d.b); } }
    if (el instanceof SVGElement) { const svg = el.ownerSVGElement; const vb = svg && svg.viewBox && svg.viewBox.baseVal; if (vb && vb.width) esc *= svg.getBoundingClientRect().width / vb.width; }
    const mono = /DM Mono/i.test(getComputedStyle(el).fontFamily);   // rótulos y fuentes al pie: pueden ser chicos
    out.push({
      txt: txt.slice(0, 60),
      palabras: txt.split(' ').filter((p) => /[A-Za-zÁÉÍÓÚáéíóúñÑ]{2,}/.test(p)).length,   // números y signos no cuentan como palabras
      fs: Math.round(fs * esc * 10) / 10, mono,
      fuera: x0 < z.x0 - 10 || x1 > z.x1 + 10 || y0 < z.y0 - 10 || y1 > z.y1 + 10,   // 10 px de tolerancia: el blanco propio de las letras grandes
      caja: [Math.round(x0), Math.round(y0), Math.round(x1), Math.round(y1)],
    });
  }
  return out;
};

const tmp = await mkdtemp(path.join(os.tmpdir(), 'revision-'));
const escenario = pag.locator('#stage');
const cuadros = [];
const tiempos = [0].concat(Array.from({ length: N - 1 }, (_, i) => +((i + 1) * dur / N).toFixed(2)));
for (let i = 0; i < tiempos.length; i++) {
  const t = tiempos[i];
  await pag.evaluate((x) => window.render(x), t);
  await escenario.screenshot({ path: path.join(tmp, `c${String(i).padStart(2, '0')}.png`) });
  const textos = await pag.evaluate(medir, ZONA);
  cuadros.push({ t, textos });
}
await nav.close();

// Hoja de contacto: 10 columnas x 2 filas, con el segundo de cada cuadro
const dirHoja = path.join(RAIZ, 'produccion/sintetico/out/revision');
await mkdir(dirHoja, { recursive: true });
const hoja = path.join(dirHoja, `${nombre}-hoja.jpg`);
const ff = spawnSync(process.env.FFMPEG || 'ffmpeg', ['-v', 'error', '-y', '-framerate', '1', '-i', path.join(tmp, 'c%02d.png'),
  '-vf', `scale=216:384,drawtext=text='%{frame_num}':start_number=0:x=6:y=6:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.55,tile=10x${Math.ceil(tiempos.length / 10)}:padding=6:color=0x222222`,
  '-frames:v', '1', '-q:v', '3', hoja], { stdio: 'inherit' });
if (ff.status !== 0) { console.error('ffmpeg no pudo armar la hoja'); }
await rm(tmp, { recursive: true, force: true });

// Controles
const fuera = [], transicion = [], chica = [], lectura = [];
let maxPal = 0, tMaxPal = 0, vacios = [];
// un texto que en algún cuadro está bien ubicado y en otro no, se está moviendo: es transición, no error
const enZona = new Set(cuadros.flatMap((c) => c.textos.filter((x) => !x.fuera).map((x) => x.txt)));
const grande = new Set(cuadros.flatMap((c) => c.textos.filter((x) => x.fs >= MIN_PX).map((x) => x.txt)));   // si en otro cuadro se ve bien, el tamaño chico es la animación
for (const c of cuadros) {
  const pal = c.textos.filter((x) => x.fs >= LECTURA_PX).reduce((a, x) => a + x.palabras, 0);   // palabras grandes
  if (pal > maxPal) { maxPal = pal; tMaxPal = c.t; }
  if (!c.textos.length) vacios.push(c.t);
  for (const x of c.textos) {
    if (x.fuera) (enZona.has(x.txt) ? transicion : fuera).push({ t: c.t, txt: x.txt, caja: x.caja });
    if (x.fs < MIN_PX) (grande.has(x.txt) ? transicion : chica).push({ t: c.t, txt: x.txt, px: x.fs, caja: x.caja });
    else if (!x.mono && x.fs < LECTURA_PX && x.palabras >= 6) lectura.push({ t: c.t, txt: x.txt, px: x.fs });
  }
}
const unico = (l) => Object.values(l.reduce((a, x) => { a[x.txt] = a[x.txt] || x; return a; }, {}));
const gancho = cuadros[0].textos.map((x) => x.txt).join(' ');
const sinGancho = await (async () => /data-sin-gancho/.test(await readFile(entrada, 'utf8')))();   // p. ej. el sello: va al final de otro video
const informe = {
  reel: path.relative(RAIZ, entrada) + (QUERY ? '?' + QUERY : ''), fecha: new Date().toISOString().slice(0, 10), duracion: dur, cuadros: tiempos.length,
  controles: {
    gancho_cuadro_0: { ok: sinGancho || gancho.length > 0, no_aplica: sinGancho, texto: gancho.slice(0, 80) },
    fuera_de_zona: { ok: unico(fuera).length === 0, casos: unico(fuera).slice(0, 8) },
    en_transicion: { casos: unico(transicion).slice(0, 8) },
    letra_menor_19px: { ok: unico(chica).length === 0, casos: unico(chica).slice(0, 8) },
    lectura_menor_30px: { ok: unico(lectura).length === 0, casos: unico(lectura).slice(0, 8) },
    palabras_en_pantalla: { ok: maxPal <= MAX_PALABRAS, max: maxPal, segundo: tMaxPal },
    cuadros_sin_texto: { segundos: vacios },
  },
};
const dirJson = path.join(RAIZ, 'produccion/estudio/revision');
await mkdir(dirJson, { recursive: true });
await writeFile(path.join(dirJson, `${nombre}.json`), JSON.stringify(informe, null, 2) + '\n');

const v = (o) => (o.ok ? 'ok ' : 'MAL');
const k = informe.controles;
console.log(`\n  ${nombre} · ${dur} s · ${tiempos.length} cuadros`);
console.log(sinGancho ? '  [ -- ] gancho: no aplica (pieza de cierre)' : `  [${v(k.gancho_cuadro_0)}] gancho en el cuadro 0: "${k.gancho_cuadro_0.texto}"`);
console.log(`  [${v(k.fuera_de_zona)}] texto fuera de la zona segura: ${k.fuera_de_zona.casos.length}`);
k.fuera_de_zona.casos.forEach((x) => console.log(`        ${x.t}s "${x.txt}" ${x.caja.join(',')}`));
if (k.en_transicion.casos.length) console.log(`  [aviso] fuera de zona o chico solo mientras se mueve: ${k.en_transicion.casos.map((x) => '"' + x.txt + '" ' + x.t + 's').join(', ')}`);
console.log(`  [${v(k.letra_menor_19px)}] letra < 19 px: ${k.letra_menor_19px.casos.length}`);
k.letra_menor_19px.casos.forEach((x) => console.log(`        ${x.t}s ${x.px}px "${x.txt}"`));
console.log(`  [${v(k.lectura_menor_30px)}] frases de lectura < 30 px: ${k.lectura_menor_30px.casos.length}`);
k.lectura_menor_30px.casos.forEach((x) => console.log(`        ${x.t}s ${x.px}px "${x.txt}"`));
console.log(`  [${v(k.palabras_en_pantalla)}] palabras grandes en pantalla (≥ ${LECTURA_PX} px): máx ${maxPal} (segundo ${tMaxPal})`);
console.log(`  cuadros sin texto: ${vacios.length ? vacios.join(', ') + ' s' : 'ninguno'}`);
console.log(`  hoja: ${path.relative(RAIZ, hoja)}\n`);
