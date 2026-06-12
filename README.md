# Campaña Digital Henderseeds 26/27

Repo de marketing de **HenderSeeds** (distribuidor RED.IN de Nidera Semillas —
Henderson, Daireaux y Bolívar). Acá se produce todo el contenido de la
precampaña maíz/girasol 26/27: posts, carruseles, reels y pauta de Meta.

> 🧠 Las reglas del juego están en [`CLAUDE.md`](CLAUDE.md). Claude las lee
> automáticamente en cada sesión.

**🌐 Página demo online:** <https://henderseedsrepositorio.github.io/Campa-aMKT-26-27/>
(se publica sola desde `docs/` con cada push, vía GitHub Pages + Actions).

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
