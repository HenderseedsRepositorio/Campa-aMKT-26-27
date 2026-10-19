#!/usr/bin/env node
/**
 * Render de las placas de la estrategia: docs/estrategia/piezas/*.html -> JPG.
 *
 * Cada HTML trae dos <section class="slide"> con data-name y data-fmt (feed | historia):
 *   feed     -> img/{name}-feed-1080x1350.jpg
 *   historia -> img/{name}-historia-1080x1920.jpg
 *
 * Los JPG se commitean (el robot del sitio solo renderiza docs/placas/).
 * Uso: node scripts/render-piezas-estrategia.mjs [filtro]
 * El HTML lo genera scripts/armar-piezas-estrategia.py.
 */
import { chromium } from 'playwright';
import { readdir, mkdir, rm } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(RAIZ, process.env.PIEZAS_DIR || 'docs/estrategia/piezas'); // PIEZAS_DIR=docs/estrategia/gusto/estilos para el panel
const OUT = path.join(DIR, 'img');
// Las placas de marca usan las tres; los estilos del panel pueden usar otras (se controla que ninguna falle).
const FUENTES = process.env.PIEZAS_DIR ? [] : ['DM Sans']; // toda placa de marca usa DM Sans; las otras se controlan por error de carga
const filtro = process.argv.slice(2);

const archivos = (await readdir(DIR))
  .filter((f) => f.endsWith('.html') && f !== 'index.html')
  .filter((f) => !filtro.length || filtro.some((t) => f.includes(t)))
  .sort();

await mkdir(OUT, { recursive: true });
if (!filtro.length) {
  // Sin filtro se regenera todo: se borran los JPG viejos para no dejar opciones que ya no existen.
  for (const f of await readdir(OUT)) if (f.endsWith('.jpg')) await rm(path.join(OUT, f));
}

const nav = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const avisos = [];
for (const f of archivos) {
  const p = await nav.newPage({ viewport: { width: 1200, height: 2000 }, deviceScaleFactor: 1 });
  const fallas = [];
  p.on('requestfailed', (r) => fallas.push(r.url().split('/').slice(-2).join('/')));
  await p.goto('file://' + path.join(DIR, f), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  const cargadas = await p.evaluate(() => {
    const s = new Set();
    document.fonts.forEach((x) => x.status === 'loaded' && s.add(x.family.replace(/["']/g, '')));
    return [...s];
  });
  const rotas = await p.evaluate(() => { const r = []; document.fonts.forEach((x) => x.status === 'error' && r.push(x.family)); return r; });
  const faltan = FUENTES.filter((x) => !cargadas.includes(x)).concat(rotas);
  if (faltan.length) { console.error(`ABORTADO en ${f}: no cargaron ${faltan.join(', ')}`); process.exit(1); }
  if (fallas.length) avisos.push(`${f}: no cargó ${fallas.join(', ')}`);

  for (const s of await p.locator('section.slide').all()) {
    const name = await s.getAttribute('data-name');
    const fmt = await s.getAttribute('data-fmt');
    const m = await s.evaluate((el) => ({ h: el.scrollHeight, v: el.clientHeight }));
    if (m.h > m.v + 2) avisos.push(`${name} (${fmt}): se pasa ${m.h - m.v}px`);
    const sufijo = fmt === 'historia' ? 'historia-1080x1920' : 'feed-1080x1350';
    await s.screenshot({ path: path.join(OUT, `${name}-${sufijo}.jpg`), type: 'jpeg', quality: 92 });
  }
  console.log('  ' + f);
  await p.close();
}
await nav.close();
if (avisos.length) { console.log('\nAVISOS:'); avisos.forEach((a) => console.log(' - ' + a)); }
