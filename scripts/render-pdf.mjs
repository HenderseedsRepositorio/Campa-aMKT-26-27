#!/usr/bin/env node
/**
 * Render de hojas A4: HTML -> PDF (para imprimir o mandar por WhatsApp) + JPG (para mandar por DM,
 * porque Instagram no acepta PDF).
 *
 * El HTML tiene que tener un .hoja de 794x1123 px (A4 a 96 dpi).
 *
 * Uso:
 *   node scripts/render-pdf.mjs docs/recursos/planilla-conteo-plantas.html
 * Salida: docs/recursos/out/<nombre>.pdf y <nombre>.jpg (no se commitea).
 */
import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';

const FUENTES_MARCA = ['Archivo Black', 'DM Sans', 'DM Mono'];
const entrada = path.resolve(process.argv[2] || '');
const dir = path.join(path.dirname(entrada), 'out');
const base = path.join(dir, path.basename(entrada, '.html'));
await mkdir(dir, { recursive: true });

const nav = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const pag = await nav.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
await pag.goto('file://' + entrada, { waitUntil: 'load' });
await pag.evaluate(() => document.fonts.ready);
const faltan = await pag.evaluate((fs) => {
  const ok = new Set(); document.fonts.forEach((f) => { if (f.status === 'loaded') ok.add(f.family.replace(/["']/g, '')); });
  return fs.filter((f) => !ok.has(f));
}, FUENTES_MARCA);
if (faltan.length) { console.error('  faltan tipografías de marca: ' + faltan.join(', ')); process.exit(1); }

await pag.locator('.hoja').screenshot({ path: base + '.jpg', type: 'jpeg', quality: 92 });
await pag.pdf({ path: base + '.pdf', width: '210mm', height: '297mm', printBackground: true, pageRanges: '1' });
console.log('  listo -> ' + path.relative(process.cwd(), base) + '.pdf / .jpg');
await nav.close();
