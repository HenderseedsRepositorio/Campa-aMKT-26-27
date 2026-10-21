#!/usr/bin/env node
/**
 * Placas de la serie "Decisiones 26/27": produccion/decisiones/dN-*.html?formato=placa -> JPG 1080x1350.
 *   docs/decisiones/img/ficha-0N-feed.jpg
 * Controla que la ficha entre en su caja (si algo se sale, lo avisa y sale con error).
 * Uso: node scripts/render-fichas.mjs [filtro]
 * Los reels salen con scripts/render-reel.mjs (misma ficha, sin ?formato).
 */
import { chromium } from 'playwright';
import { readdir, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(RAIZ, 'produccion/decisiones');
const OUT = path.join(RAIZ, 'docs/decisiones/img');
const filtro = process.argv.slice(2);
const archivos = (await readdir(DIR)).filter((f) => /^d\d-.*\.html$/.test(f)).filter((f) => !filtro.length || filtro.some((t) => f.includes(t))).sort();
await mkdir(OUT, { recursive: true });

const nav = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
let mal = 0;
for (const f of archivos) {
  const pag = await nav.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  const errores = [];
  pag.on('pageerror', (e) => errores.push(e.message));
  await pag.addInitScript(() => { window.__RENDER_MODE__ = true; });
  await pag.goto(pathToFileURL(path.join(DIR, f)).href + '?formato=placa');
  await pag.evaluate(() => (window.LISTO ? window.LISTO.then(() => true) : true));
  await pag.waitForTimeout(150);
  // ¿algo se sale de la ficha?
  const fuera = await pag.evaluate(() => {
    const fi = document.querySelector('.ficha').getBoundingClientRect(), malos = [];
    document.querySelectorAll('.ficha *').forEach((n) => { const r = n.getBoundingClientRect(); if (r.width && (r.bottom > fi.bottom + 2 || r.right > fi.right + 2)) malos.push((n.className || n.tagName) + ' ' + Math.round(r.bottom - fi.bottom) + 'px'); });
    return malos.slice(0, 5);
  });
  const n = f.match(/^d(\d)/)[1];
  const salida = path.join(OUT, `ficha-0${n}-feed.jpg`);
  await pag.locator('#stage').screenshot({ path: salida, type: 'jpeg', quality: 92 });
  const ok = !fuera.length && !errores.length;
  if (!ok) mal++;
  console.log(`  ${ok ? 'ok ' : 'MAL'} ${f} -> ${path.relative(RAIZ, salida)}${fuera.length ? '  se sale: ' + fuera.join(', ') : ''}${errores.length ? '  errores: ' + errores.join(' | ') : ''}`);
  await pag.close();
}
await nav.close();
process.exit(mal ? 1 : 0);
