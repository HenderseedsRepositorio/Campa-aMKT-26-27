#!/usr/bin/env node
/**
 * Baja las tipografias de marca de Google Fonts a docs/assets/fonts/.
 *
 * Se corre UNA VEZ (o cuando cambie la paleta tipografica de brand/identidad.md).
 * Tenerlas en el repo hace que el render de placas sea hermetico: no depende de
 * que fonts.googleapis.com este accesible desde el navegador — que es justo lo
 * que falla dentro de un contenedor o de un runner de CI sin salida a internet.
 *
 * Uso:  node scripts/bajar-fuentes.mjs
 */

import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DESTINO = path.join(RAIZ, 'docs/assets/fonts');

// Chrome moderno: sin este User-Agent, Google Fonts devuelve TTF en vez de WOFF2.
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36';

// Pesos segun brand/identidad.md (+ los que usan las placas existentes).
const FAMILIAS = [
  { nombre: 'Archivo Black', query: 'Archivo+Black:wght@400' },
  { nombre: 'DM Sans', query: 'DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;0,9..40,900;1,9..40,700' },
  { nombre: 'DM Mono', query: 'DM+Mono:wght@400;500' },
];

async function bajar(url, binario = false) {
  const r = await fetch(url, { headers: { 'User-Agent': UA } });
  if (!r.ok) throw new Error(`HTTP ${r.status} en ${url}`);
  return binario ? Buffer.from(await r.arrayBuffer()) : r.text();
}

async function main() {
  await mkdir(DESTINO, { recursive: true });

  const partes = [
    '/* Tipografias de marca hospedadas localmente.',
    '   Generado por scripts/bajar-fuentes.mjs — no editar a mano.',
    '   Permite renderizar las placas sin depender de la red. */',
    '',
  ];
  const yaBajados = new Map();

  for (const fam of FAMILIAS) {
    const css = await bajar(`https://fonts.googleapis.com/css2?family=${fam.query}&display=swap`);
    const bloques = css.match(/@font-face\s*\{[^}]*\}/g) || [];
    if (!bloques.length) throw new Error(`Google Fonts no devolvio @font-face para ${fam.nombre}`);

    for (const bloque of bloques) {
      const m = bloque.match(/url\((https:\/\/fonts\.gstatic\.com[^)]+)\)/);
      if (!m) continue;
      const urlFuente = m[1];

      if (!yaBajados.has(urlFuente)) {
        const archivo = fam.nombre.replace(/\s+/g, '') + '-' + urlFuente.split('/').pop();
        const datos = await bajar(urlFuente, true);
        await writeFile(path.join(DESTINO, archivo), datos);
        yaBajados.set(urlFuente, archivo);
        console.log(`  ${archivo}  (${(datos.length / 1024).toFixed(0)} KB)`);
      }
      partes.push(bloque.replace(urlFuente, yaBajados.get(urlFuente)), '');
    }
  }

  await writeFile(path.join(DESTINO, 'fuentes.css'), partes.join('\n'), 'utf8');
  console.log(`\n  ${yaBajados.size} archivo(s) -> docs/assets/fonts/fuentes.css`);
}

main().catch((e) => {
  console.error('  ERROR:', e.message);
  process.exit(1);
});
