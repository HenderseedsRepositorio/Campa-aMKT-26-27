# Campaña Digital Henderseeds 26/27

Repo de marketing de **HenderSeeds** (distribuidor RED.IN de Nidera Semillas —
Henderson, Daireaux y Bolívar). Acá se produce todo el contenido de la
precampaña maíz/girasol 26/27: posts, carruseles, reels y pauta de Meta.

> 🧠 Las reglas del juego están en [`CLAUDE.md`](CLAUDE.md). Claude las lee
> automáticamente en cada sesión.

**🌐 Página demo online:** <https://henderseedsrepositorio.github.io/Campa-aMKT-26-27/>
(se publica sola desde `docs/` con cada push, vía GitHub Pages + Actions).

**🌱 Relanzamiento Siembra 26/27 (24/09/2026):** diagnóstico, plan W40–W46 y todas las piezas
con su texto → `docs/propuesta/index.html` (online en `/propuesta/` cuando se mergea).

**🎬 Reels para arrancar (W40–W41):** los 6 reels con MP4, tapa, texto y audio sugerido →
`docs/reels-siembra/index.html` (`node scripts/armar-reels.mjs`; `--autocontenida archivo.html` arma
un solo archivo para mandar).

| Comando | Qué hace |
|---------|----------|
| `npm run placas` | Renderiza cada `docs/placas/*.html` a JPG (feed 4:5 + historia 9:16) en `docs/placas/img/` |
| `npm run videos` | Graba las placas animadas a MP4 (1080×1920, H.264) en `docs/placas/video/` — necesita `ffmpeg` |
| `npm run propuesta` | Rearma `docs/propuesta/index.html` desde las placas (`--posts` escribe los `.md` del plan, `--miniaturas` regenera la grilla del perfil) |

**📷 Placa con foto:** `docs/foto/index.html` — subís una foto del celular y sale la placa con marca
(plantillas titular / dato / frase, feed o historia). Funciona sin internet y la foto no sale del teléfono.

## Cómo se usa (desde la web o el celular)

Abrí una sesión de Claude Code sobre este repo y tirá uno de estos prompts:

**Lote semanal (el recurrente, lunes a la mañana):**
> Generá los 3 posts de la semana 2026-WXX en posts/2026-WXX/. Seguí la rotación
> de calendario.md. Para cada post: copy IG/FB, pieza visual, hashtags, CTA.
> El post que va con pauta: agregá el brief en meta-ads/briefs/.

**Carrusel:**
> Creá en carruseles/ un carrusel de 6 slides (1080×1350) sobre [tema], estilo
> según brand/identidad.md. Un dato por slide, screenshoteable sin scroll.

**Reel:**
> Armá en reels/ el guion de un reel de 20–30 segundos sobre [tema]: hook,
> escenas, texto en pantalla, audio sugerido y caption.

**Cargar datos comerciales:**
> Te pego datos de [híbridos / condiciones / herramientas]: actualizá los
> archivos de contexto/ que correspondan y resolvé los [COMPLETAR].

## Estructura

| Carpeta | Qué hay |
|---------|---------|
| `brand/` | Identidad visual y tono de voz |
| `contexto/` | Productos, herramientas, zona, calendario comercial |
| `posts/` | Lotes semanales de posteos (una carpeta por semana) |
| `carruseles/` | Carruseles HTML listos para screenshotear |
| `reels/` | Guiones de reels |
| `meta-ads/` | Briefs de pauta para Meta Business Suite |
| `calendario.md` | Grilla: qué sale cada semana y en qué estado está |
