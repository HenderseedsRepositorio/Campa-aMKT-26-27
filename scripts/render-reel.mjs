#!/usr/bin/env node
/**
 * Render de reels: HTML animado -> MP4 1080x1920 listo para Instagram.
 *
 * El HTML expone window.render(t) (t en segundos) y window.REEL_DURACION.
 * Este script llama render(t) cuadro por cuadro, captura cada cuadro con Chromium
 * y ffmpeg los une en un MP4 H.264. No se graba la pantalla en tiempo real: cada
 * cuadro es exacto, así que el video sale nítido y siempre igual.
 *
 * Uso:
 *   node scripts/render-reel.mjs produccion/sintetico/reel-siembra-motion.html [salida.mp4] [--fps 30] [--preview]
 *   --preview  saca solo 6 cuadros sueltos (para revisar sin esperar el render completo)
 */
import { chromium } from 'playwright';
import { mkdtemp, readFile, rm, mkdir } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CSS_FUENTES = path.join(RAIZ, 'docs/assets/fonts/fuentes.css');
const FUENTES_MARCA = ['Archivo Black', 'DM Sans', 'DM Mono'];

const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const valor = (n, d) => (args.includes(n) ? args[args.indexOf(n) + 1] : d);
const posicionales = args.filter((a, i) => !a.startsWith('--') && !(args[i - 1] || '').startsWith('--fps'));
const entrada = path.resolve(posicionales[0] || '');
const salida = path.resolve(posicionales[1] || entrada.replace(/\.html$/, '.mp4').replace('/sintetico/', '/sintetico/out/'));
const FPS = Number(valor('--fps', 30));

const cssFuentes = (await readFile(CSS_FUENTES, 'utf8')).replace(
  /url\((?!['"]?(?:data:|file:|https?:))['"]?([^)'"]+)['"]?\)/g,
  (_, f) => `url("file://${path.join(path.dirname(CSS_FUENTES), f)}")`
);

const nav = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const pag = await nav.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await pag.addInitScript(() => { window.__RENDER_MODE__ = true; });
await pag.goto('file://' + entrada, { waitUntil: 'load' });
await pag.addStyleTag({ content: cssFuentes });
await pag.evaluate(() => document.fonts.ready);
const faltan = await pag.evaluate((fs) => {
  const ok = new Set(); document.fonts.forEach((f) => { if (f.status === 'loaded') ok.add(f.family.replace(/["']/g, '')); });
  return fs.filter((f) => !ok.has(f));
}, FUENTES_MARCA);
// Las fuentes cargan recién cuando se usan: forzar un cuadro con todo el texto visible
if (faltan.length) {
  await pag.evaluate(() => window.render(window.REEL_DURACION * 0.5));
  await pag.evaluate(() => document.fonts.ready);
}
const dur = await pag.evaluate(() => window.REEL_DURACION);
const escenario = pag.locator('#stage');

if (flag('--preview')) {
  const dir = path.join(path.dirname(salida), 'preview');
  await mkdir(dir, { recursive: true });
  const ts = valor('--ts', '').split(',').filter(Boolean).map(Number);
  const tiempos = ts.length ? ts : [0.2, 2.5, 6.5, 12.5, 18, 23, dur - 1.5].filter((x) => x < dur);
  for (const t of tiempos) {
    await pag.evaluate((x) => window.render(x), t);
    await escenario.screenshot({ path: path.join(dir, `t${t.toFixed(1)}.jpg`), type: 'jpeg', quality: 85 });
  }
  console.log(`  preview: ${tiempos.length} cuadros -> ${dir}`);
  await nav.close();
  process.exit(0);
}

const tmp = await mkdtemp(path.join(os.tmpdir(), 'reel-'));
const total = Math.round(dur * FPS);
for (let i = 0; i < total; i++) {
  await pag.evaluate((x) => window.render(x), i / FPS);
  await escenario.screenshot({ path: path.join(tmp, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
  if (i % FPS === 0) process.stdout.write(`\r  cuadro ${i}/${total}`);
}
await nav.close();
console.log(`\r  ${total} cuadros capturados, codificando…`);

await mkdir(path.dirname(salida), { recursive: true });
const ff = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(tmp, 'f%05d.jpg'),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', salida], { stdio: 'inherit' });
await rm(tmp, { recursive: true, force: true });
if (ff.status !== 0) { console.error('  ffmpeg falló'); process.exit(1); }
console.log(`  listo -> ${path.relative(RAIZ, salida)} (${dur}s @ ${FPS} fps)`);
