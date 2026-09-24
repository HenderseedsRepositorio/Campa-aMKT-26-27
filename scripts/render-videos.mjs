#!/usr/bin/env node
/**
 * Render de animaciones: HTML -> MP4 listo para reel / historia.
 *
 * Toma cada placa animada (<section class="slide hs anim" data-dur="…">) de
 * docs/placas/*.html y la graba cuadro por cuadro:
 *   1. abre la página con ?capture (hs-anim.js congela las animaciones),
 *   2. para cada cuadro llama a HS.seek(t) y saca un screenshot,
 *   3. le pasa los cuadros a ffmpeg, que arma un MP4 H.264 + audio mudo.
 *
 * Por qué cuadro por cuadro y no "grabar la pantalla": así el video sale
 * idéntico a lo que se ve en el navegador, sin saltos ni cuadros perdidos,
 * y no depende de la velocidad de la máquina.
 *
 * Salida: docs/placas/video/<data-name>.mp4 (1080×1920, 30 fps, AAC mudo;
 * Instagram lo acepta tal cual). Se commitea: pesa poco y así se puede bajar
 * desde GitHub sin correr nada.
 *
 * Requisitos: ffmpeg con libx264 en el PATH (o FFMPEG=/ruta/a/ffmpeg).
 * Uso:
 *   npm run videos              # todas las animaciones
 *   npm run videos -- tardio    # solo las que matcheen "tardio"
 */

import { chromium } from 'playwright';
import { readdir, mkdir, readFile } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR_PLACAS = path.join(RAIZ, 'docs/placas');
const DIR_SALIDA = path.join(DIR_PLACAS, 'video');
const CSS_FUENTES = path.join(RAIZ, 'docs/assets/fonts/fuentes.css');
const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const FPS = 30;
const COLA = 1.5; // segundos quietos al final, para que el cierre se lea

const filtro = process.argv.slice(2).filter((a) => !a.startsWith('-'));

function ffmpeg(salida, ancho, alto) {
  const args = [
    '-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
    '-shortest',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-profile:v', 'high',
    '-pix_fmt', 'yuv420p', '-r', String(FPS), '-s', `${ancho}x${alto}`,
    '-c:a', 'aac', '-b:a', '128k',
    '-movflags', '+faststart',
    salida,
  ];
  const p = spawn(FFMPEG, args, { stdio: ['pipe', 'inherit', 'inherit'] });
  const fin = new Promise((ok, mal) => p.on('close', (c) => (c === 0 ? ok() : mal(new Error(`ffmpeg salió con ${c}`)))));
  return { stdin: p.stdin, fin };
}

async function main() {
  const archivos = (await readdir(DIR_PLACAS))
    .filter((f) => f.endsWith('.html'))
    .filter((f) => !filtro.length || filtro.some((t) => f.includes(t)))
    .sort();

  await mkdir(DIR_SALIDA, { recursive: true });

  const cssFuentes = (await readFile(CSS_FUENTES, 'utf8')).replace(
    /url\((?!['"]?(?:data:|file:|https?:))['"]?([^)'"]+)['"]?\)/g,
    (_, f) => `url("file://${path.join(path.dirname(CSS_FUENTES), f)}")`
  );

  const navegador = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  let total = 0;

  for (const archivo of archivos) {
    const html = await readFile(path.join(DIR_PLACAS, archivo), 'utf8');
    if (!/class="slide hs[^"]*\banim\b/.test(html)) continue;

    const pagina = await navegador.newPage({ viewport: { width: 1200, height: 2000 }, deviceScaleFactor: 1 });
    await pagina.goto('file://' + path.join(DIR_PLACAS, archivo) + '?capture', { waitUntil: 'load' });
    await pagina.addStyleTag({ content: cssFuentes });
    await pagina.evaluate(() => document.fonts.ready);
    await pagina.waitForFunction(() => window.HS && window.HS.ready, null, { timeout: 10000 });

    const slides = await pagina.$$eval('.slide.hs.anim', (els) =>
      els.map((e) => ({ id: e.id, nombre: e.dataset.name || e.id, dur: parseFloat(e.dataset.dur || '10') }))
    );

    for (const s of slides) {
      const el = pagina.locator('#' + s.id);
      const caja = await el.boundingBox();
      const ancho = Math.round(caja.width), alto = Math.round(caja.height);
      const salida = path.join(DIR_SALIDA, `${s.nombre}.mp4`);
      const cuadros = Math.round((s.dur + COLA) * FPS);
      const { stdin, fin } = ffmpeg(salida, ancho, alto);
      const t0 = Date.now();

      for (let i = 0; i < cuadros; i++) {
        const t = Math.min(i / FPS, s.dur);
        await pagina.evaluate((t) => window.HS.seek(t), t);
        const buf = await el.screenshot({ type: 'jpeg', quality: 92, animations: 'allow' });
        if (!stdin.write(buf)) await new Promise((r) => stdin.once('drain', r));
      }
      stdin.end();
      await fin;
      total++;
      console.log(`  ${s.nombre}.mp4  ${ancho}×${alto}  ${(cuadros / FPS).toFixed(1)} s  (${((Date.now() - t0) / 1000).toFixed(0)} s de render)`);
    }
    await pagina.close();
  }

  await navegador.close();
  console.log(`\n  ${total} video(s) -> docs/placas/video/`);
}

main().catch((e) => { console.error(e); process.exit(1); });
