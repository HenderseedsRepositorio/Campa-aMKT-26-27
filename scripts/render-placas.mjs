#!/usr/bin/env node
/**
 * Render de placas: HTML -> imagen lista para publicar.
 *
 * Toma cada archivo de docs/placas/*.html y genera:
 *   - feed     1080x1350 (4:5)  -> lo que se sube al feed de Instagram/Facebook
 *   - historia 1080x1920 (9:16) -> la placa centrada sobre lienzo de marca
 *
 * Por qué existe: hasta ahora las placas se bajaban a mano con el boton
 * "Descargar" de cada HTML, que usa html2canvas. Esa libreria NO soporta
 * filter ni box-shadow, asi que el resplandor del sol de mayo (y cualquier
 * glow de marca) desaparecia del PNG. Playwright hace una captura real del
 * navegador: sale identico a lo que se ve en pantalla.
 *
 * Uso:
 *   npm run placas              # renderiza todas
 *   npm run placas -- amigo     # solo las que matcheen "amigo"
 *
 * La salida va a docs/placas/img/ y NO se commitea (ver .gitignore): es un
 * artefacto derivado del HTML, que es la fuente de verdad.
 */

import { chromium } from 'playwright';
import { readdir, mkdir, writeFile, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR_PLACAS = path.join(RAIZ, 'docs/placas');
const DIR_SALIDA = path.join(DIR_PLACAS, 'img');
const CSS_FUENTES = path.join(RAIZ, 'docs/assets/fonts/fuentes.css');

const FEED = { width: 1080, height: 1350 };
const HISTORIA = { width: 1080, height: 1920 };
const FONDO_HISTORIA = '#05070d';
const CALIDAD_JPG = 95;

// Tipografias de marca (brand/identidad.md). Si alguna no carga, la placa sale
// con letra generica y nadie se da cuenta hasta verla publicada -> se aborta.
const FUENTES_MARCA = ['Archivo Black', 'DM Sans', 'DM Mono'];

const filtro = process.argv.slice(2).filter((a) => !a.startsWith('-'));
const avisos = [];

async function main() {
  const archivos = (await readdir(DIR_PLACAS))
    .filter((f) => f.endsWith('.html'))
    .filter((f) => !filtro.length || filtro.some((t) => f.includes(t)))
    .sort();

  if (!archivos.length) {
    console.error('No se encontro ninguna placa' + (filtro.length ? ` que matchee "${filtro.join(' ')}"` : ''));
    process.exit(1);
  }

  await mkdir(DIR_SALIDA, { recursive: true });

  // El CSS de fuentes referencia los .woff2 con rutas relativas a su carpeta.
  // Al inyectarlo en la pagina, el navegador las resolveria contra la URL de la
  // placa (docs/placas/) y no las encontraria: por eso se absolutizan aca.
  const cssFuentes = (await readFile(CSS_FUENTES, 'utf8')).replace(
    /url\((?!['"]?(?:data:|file:|https?:))['"]?([^)'"]+)['"]?\)/g,
    (_, f) => `url("file://${path.join(path.dirname(CSS_FUENTES), f)}")`
  );

  const navegador = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  const generados = [];

  for (const archivo of archivos) {
    const base = archivo.replace(/\.html$/, '');
    const pagina = await navegador.newPage({
      viewport: { width: FEED.width + 80, height: FEED.height },
      deviceScaleFactor: 1,
    });

    await pagina.goto('file://' + path.join(DIR_PLACAS, archivo), { waitUntil: 'load' });

    // 1. Tipografias de marca desde el repo, no desde internet: el render es
    //    hermetico (no depende de que fonts.googleapis.com este accesible desde
    //    el navegador, que es justo lo que falla dentro de un contenedor).
    await pagina.addStyleTag({ content: cssFuentes });
    await pagina.evaluate(() => document.fonts.ready);

    // 2. Verificar que cargaron DE VERDAD.
    //    Ojo: document.fonts.check() no sirve para esto — si el CSS de fuentes
    //    nunca cargo, no hay ninguna @font-face pendiente y check() devuelve
    //    true igual, aunque el texto se dibuje con la tipografia del sistema.
    //    Lo que hay que mirar es el registro real de FontFace cargadas.
    const faltantes = await pagina.evaluate((fuentes) => {
      const cargadas = new Set();
      document.fonts.forEach((f) => {
        if (f.status === 'loaded') cargadas.add(f.family.replace(/["']/g, ''));
      });
      return fuentes.filter((f) => !cargadas.has(f));
    }, FUENTES_MARCA);

    if (faltantes.length) {
      console.error(`\n  ABORTADO en ${archivo}`);
      console.error(`  No cargaron las tipografias de marca: ${faltantes.join(', ')}`);
      console.error(`  Sin ellas la placa sale con letra generica y no se nota hasta verla publicada.`);
      console.error(`  Corre: node scripts/bajar-fuentes.mjs`);
      await navegador.close();
      process.exit(1);
    }

    // 2. Ocultar la barra de descarga, que el propio HTML muestra por JS.
    await pagina.addStyleTag({ content: '.dlbar{display:none !important}' });

    const slides = pagina.locator('.slide');
    const total = await slides.count();

    for (let i = 0; i < total; i++) {
      const slide = slides.nth(i);
      const sufijo = total > 1 ? `-slide-${String(i + 1).padStart(2, '0')}` : '';
      const nombre = base + sufijo;

      // 3. Las placas tienen overflow:hidden. Si el contenido no entra, se
      //    recorta en silencio: avisamos con cuanto se pasa.
      const medida = await slide.evaluate((el) => ({
        alto: el.scrollHeight,
        visible: el.clientHeight,
        ancho: el.scrollWidth,
      }));
      if (medida.alto > medida.visible + 2) {
        avisos.push(`${nombre}: el contenido se pasa ${medida.alto - medida.visible}px del alto (se recorta)`);
      }

      const rutaFeed = path.join(DIR_SALIDA, `${nombre}-feed-1080x1350.jpg`);
      await slide.screenshot({ path: rutaFeed, type: 'jpeg', quality: CALIDAD_JPG });

      const rutaHistoria = path.join(DIR_SALIDA, `${nombre}-historia-1080x1920.jpg`);
      await componerHistoria(navegador, rutaFeed, rutaHistoria);

      generados.push(nombre);
      console.log(`  ${nombre}  ->  feed + historia`);
    }

    await pagina.close();
  }

  await escribirIndice(generados);
  await navegador.close();

  console.log(`\n  ${generados.length} placa(s) renderizada(s) -> docs/placas/img/`);
  if (avisos.length) {
    console.log('\n  AVISOS (revisar a ojo antes de publicar):');
    avisos.forEach((a) => console.log(`   - ${a}`));
  }
}

/**
 * Historia 9:16: la placa 4:5 centrada sobre un lienzo de marca.
 * Se compone en una pagina aparte a partir del JPG del feed, asi la historia
 * es siempre identica al feed (no se vuelve a renderizar el CSS).
 */
async function componerHistoria(navegador, rutaFeed, rutaSalida) {
  const pagina = await navegador.newPage({
    viewport: HISTORIA,
    deviceScaleFactor: 1,
  });

  // La imagen va embebida en base64: una pagina creada con setContent corre
  // sobre about:blank y no tiene permiso para leer file://, asi que un
  // <img src="file://..."> sale roto (y el screenshot igual "funciona").
  const b64 = (await readFile(rutaFeed)).toString('base64');

  await pagina.setContent(`
    <style>
      html,body{margin:0;padding:0;background:${FONDO_HISTORIA};}
      body{width:${HISTORIA.width}px;height:${HISTORIA.height}px;
           display:flex;align-items:center;justify-content:center;overflow:hidden}
      img{width:${FEED.width}px;height:${FEED.height}px;display:block;
          box-shadow:0 0 0 2px rgba(245,166,35,0.25)}
    </style>
    <img src="data:image/jpeg;base64,${b64}">
  `);

  // Una <img> rota tambien cuenta como "visible": lo que hay que verificar es
  // que el navegador haya decodificado la imagen de verdad.
  await pagina.waitForFunction(() => {
    const img = document.querySelector('img');
    return img && img.complete && img.naturalWidth > 0;
  }, null, { timeout: 15000 });

  await pagina.screenshot({ path: rutaSalida, type: 'jpeg', quality: CALIDAD_JPG });
  await pagina.close();
}

/** Indice navegable: una sola URL para abrir del celular y guardar todo. */
async function escribirIndice(nombres) {
  // Ojo: la tarjeta es un <div>, no un <a>. Un <a> con otros <a> adentro es
  // HTML invalido y el navegador lo "repara" duplicando el elemento.
  const tarjetas = nombres
    .map(
      (n) => `  <div class="card">
    <a class="foto" href="${n}-feed-1080x1350.jpg" target="_blank">
      <img src="${n}-feed-1080x1350.jpg" alt="${n}" loading="lazy">
    </a>
    <div class="pie">
      <span class="nombre">${n}</span>
      <span class="links">
        <a href="${n}-feed-1080x1350.jpg" download>feed 4:5</a>
        <a href="${n}-historia-1080x1920.jpg" download>historia 9:16</a>
      </span>
    </div>
  </div>`
    )
    .join('\n');

  const html = `<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HenderSeeds — Placas listas para publicar</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0A0F1B;color:#E8EEF7;font-family:system-ui,sans-serif;padding:24px}
h1{font-size:20px;margin-bottom:6px}
p{color:#8FA0BE;font-size:14px;margin-bottom:22px}
a{color:#F5A623}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
      border-radius:12px;overflow:hidden}
.card .foto{display:block}
.card img{width:100%;display:block}
.pie{padding:10px 12px}
.nombre{display:block;font-size:12px;font-family:ui-monospace,monospace;color:#E8EEF7;word-break:break-all}
.links{display:flex;gap:12px;margin-top:6px;font-size:12px}
</style></head><body>
<h1>Placas listas para publicar</h1>
<p>Tocá una imagen para abrirla en grande y guardarla, o usá los links de descarga.
Generado automáticamente desde <code>docs/placas/*.html</code>.</p>
<div class="grid">
${tarjetas}
</div>
</body></html>`;

  await writeFile(path.join(DIR_SALIDA, 'index.html'), html, 'utf8');
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
