#!/usr/bin/env node
/**
 * Render de videos: HTML animado -> MP4 listo para publicar.
 *
 * Toma un HTML de docs/videos/ cuya animacion esta hecha con CSS
 * (animation-delay = linea de tiempo) y lo convierte en video:
 * pausa todas las animaciones, avanza el tiempo cuadro a cuadro con
 * getAnimations()[i].currentTime y captura el .slide en cada paso.
 * Los cuadros se encodean a H.264 (el codec que Instagram espera).
 *
 * La duracion la declara el propio HTML en data-duracion (ms) del .slide.
 *
 * Uso:
 *   npm run video -- docs/videos/archivo.html          # -> archivo.mp4 al lado
 *   npm run video -- docs/videos/archivo.html salida.mp4
 *
 * Requiere un ffmpeg con libx264. El script busca, en orden:
 *   1. FFMPEG_PATH (variable de entorno)
 *   2. ffmpeg del sistema
 *   3. el de imageio-ffmpeg (pip install imageio-ffmpeg)
 * (El ffmpeg que trae Playwright NO sirve: solo encodea VP8/webm.)
 */

import { chromium } from 'playwright';
import { spawn, execSync } from 'node:child_process';
import path from 'node:path';

const FPS = 30;
const CRF = 20; // calidad H.264 (menos = mejor/mas pesado); 20 va sobrado para IG

const FUENTES_MARCA = ['Archivo Black', 'DM Sans', 'DM Mono'];

const args = process.argv.slice(2).filter((a) => !a.startsWith('-'));
if (!args.length) {
  console.error('Uso: npm run video -- docs/videos/archivo.html [salida.mp4]');
  process.exit(1);
}
const entrada = path.resolve(args[0]);
const salida = path.resolve(args[1] || entrada.replace(/\.html$/, '.mp4'));

function encontrarFfmpeg() {
  if (process.env.FFMPEG_PATH) return process.env.FFMPEG_PATH;
  try { execSync('ffmpeg -version', { stdio: 'ignore' }); return 'ffmpeg'; } catch {}
  try {
    return execSync('python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"')
      .toString().trim();
  } catch {}
  throw new Error('No hay ffmpeg con libx264: setea FFMPEG_PATH o corre `pip install imageio-ffmpeg`.');
}

async function main() {
  const ffmpeg = encontrarFfmpeg();

  const navegador = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  const pagina = await navegador.newPage({
    viewport: { width: 1160, height: 1990 },
    deviceScaleFactor: 1,
  });
  await pagina.goto('file://' + entrada, { waitUntil: 'load' });
  await pagina.evaluate(() => document.fonts.ready);

  // Igual que en render-placas: sin las tipografias de marca el video sale
  // con letra generica y no se nota hasta verlo publicado -> se aborta.
  const faltantes = await pagina.evaluate((fuentes) => {
    const cargadas = new Set();
    document.fonts.forEach((f) => {
      if (f.status === 'loaded') cargadas.add(f.family.replace(/["']/g, ''));
    });
    return fuentes.filter((f) => !cargadas.has(f));
  }, FUENTES_MARCA);
  if (faltantes.length) {
    console.error(`ABORTADO: no cargaron las tipografias de marca: ${faltantes.join(', ')}`);
    console.error('Corre: node scripts/bajar-fuentes.mjs');
    await navegador.close();
    process.exit(1);
  }

  const slide = pagina.locator('.slide');
  const duracion = await slide.evaluate((el) => Number(el.dataset.duracion) || 10000);
  const cuadros = Math.round((duracion / 1000) * FPS);

  // Congelar la linea de tiempo: de aca en mas el tiempo lo maneja el loop.
  await pagina.evaluate(() => document.getAnimations().forEach((a) => a.pause()));

  const enc = spawn(ffmpeg, [
    '-y', '-hide_banner', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', String(CRF),
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    salida,
  ], { stdio: ['pipe', 'inherit', 'inherit'] });
  const encTermina = new Promise((res, rej) => {
    enc.on('close', (c) => (c === 0 ? res() : rej(new Error(`ffmpeg salio con codigo ${c}`))));
    enc.on('error', rej);
  });

  console.log(`  ${path.basename(entrada)} -> ${cuadros} cuadros @ ${FPS} fps (${(duracion / 1000).toFixed(1)} s)`);

  for (let i = 0; i < cuadros; i++) {
    const t = (i / FPS) * 1000;
    await pagina.evaluate((ms) => document.getAnimations().forEach((a) => { a.currentTime = ms; }), t);
    const png = await slide.screenshot({ type: 'png' });
    if (!enc.stdin.write(png)) await new Promise((res) => enc.stdin.once('drain', res));
    if ((i + 1) % FPS === 0) console.log(`  ${i + 1}/${cuadros} cuadros`);
  }

  enc.stdin.end();
  await encTermina;
  await navegador.close();
  console.log(`\n  Video listo -> ${path.relative(process.cwd(), salida)}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
