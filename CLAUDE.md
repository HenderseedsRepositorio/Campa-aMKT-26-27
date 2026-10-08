# Henderseeds — Campaña Digital 26/27

## Qué es este repo
Centro de producción de contenido y marketing digital de **HenderSeeds**
([henderseeds.com](https://henderseeds.com)), distribuidor y asesor técnico de la red
**RED.IN de Nidera Semillas** para **Henderson, Daireaux y Bolívar**
(oeste de la provincia de Buenos Aires, Argentina).

**Estrategia vigente (07/10/2026): `docs/estrategia/index.html`** — publicada en
https://henderseedsrepositorio.github.io/Campa-aMKT-26-27/estrategia/ . Manda sobre el resto de
este archivo. Idea central: el motor es la venta directa planificada (mapa de cuentas en
Salesforce, visitas con algo de valor, referidos, jornada a campo); la marca digital es chica pero
constante (1 publicación por semana, Estados de WhatsApp, pauta solo por zona y concentrada en la
precampaña). El drone va solo dentro de la oferta (paso 5), nunca como pieza suelta. Nadie aparece en cámara.
Tres páginas, en este orden: **estrategia** (`docs/estrategia/index.html`, v3: situación, objetivos,
segmentos, oferta, recorrido del productor, canales, presupuesto, medición, roles, reglas, riesgos),
**guía de 10 pasos** (`guia.html`) y **plan de 9 semanas** (`plan.html`: publicaciones listas,
mensajes, pauta A + B, checklist de Santi). Planillas: `mapa-de-cuentas.csv`, `tablero-mensual.csv`.
Piezas nuevas en `docs/estrategia/piezas/` (HTML + JPG; usan `../../assets/hs2627.css` del sitio).
Galería de descarga: `docs/estrategia/piezas/index.html` (Plan de Campaña: 8 diseños × colores = 16; Clearfield: 7 diseños = 14;
cada una en feed 4:5 e historia 9:16 propia). Recomendadas: Plan C navy (2ª vuelta: F ámbar) y Clearfield D navy.
Textos y diseños en UN archivo: `python3 scripts/armar-piezas-estrategia.py` → HTML; `node scripts/render-piezas-estrategia.mjs`
→ JPG (se commitean; el robot del sitio solo renderiza `docs/placas/`).
Panel de gusto (08/10): `docs/estrategia/gusto/` — 13 estilos de placa con el mismo mensaje + colores, letras,
titulares y tono para votar (`python3 scripts/armar-panel-gusto.py` + `PIEZAS_DIR=docs/estrategia/gusto/estilos node
scripts/render-piezas-estrategia.mjs`). Tipografías extra en `docs/assets/fonts/extra/`. Lo que Alvaro elija define el estilo nuevo.
**Roles (07/10):** Alvaro publica; Santi revisa cada pieza antes con la checklist.
**Oferta (definida por Alvaro el 07/10): "Plan de Campaña HenderSeeds"**, seis pasos:
1. Diagnóstico · 2. Recomendación Asista (híbrido por ambiente; siembra variable incluida, opcional) ·
3. Financiación (en público solo "a cosecha o de contado, con tarjetas agro en pesos o dólares"; el plazo
exacto va solo en privado, NUNCA en el repo) · 4. Seguro de resiembra (de Nidera, ante granizo o encharcamiento) · 5. Vuelo de drone (calidad de siembra) ·
6. Informe de visita. El drone aparece solo como paso 5 de la oferta, nunca como pieza suelta.
La hoja de visita y el modelo de informe (PDF) NO se suben al repo: tienen condiciones comerciales.
**Regla del equipo (25/09): en maíz NO se muestran números de ensayo** (kg/ha vs. promedio): se
muestra el híbrido y su tecnología. En girasol sí.
**Nunca subir información comercial interna al repo (es público).** El archivo con precios
(`brand/referencias/hibridos-nidera.md`) se borró de las 8 ramas el 07/10; sigue en el historial.
GitHub: Alvaro decidió no pagar Pro (07/10).

**Rama única: `main` (desde el 07/10/2026).** Se juntaron las 8 ramas de trabajo (septiembre como base,
más la estrategia y lo útil de julio/agosto). Cada sesión nueva trabaja sobre `main` y vuelve a `main`.
El sitio lo publica solo `.github/workflows/pages.yml` desde `main` (renderiza `docs/placas/` y copia `docs/`
entero a gh-pages con `keep_files`). Las ramas viejas `claude/*` quedan como historial: no trabajar en ellas.

Acá se generan: posteos para Instagram/Facebook, carruseles, guiones de reels y briefs
de pauta para Meta Business Suite. Ritmo objetivo: **2–3 posteos por semana**.

## Skill maestra de generación de contenido
Leer **`.claude/skills/generar-contenido.md`** — contiene el flujo completo
paso a paso (7 pasos), checklist, reglas duras y tabla de híbridos prioritarios.
Seguirla al pie de la letra para generar cualquier lote semanal o post suelto.

## Antes de generar cualquier contenido (obligatorio)
1. Leé `.claude/skills/generar-contenido.md` (skill maestra).
2. Leé `brand/identidad.md` y `brand/tono-voz.md`.
3. Leé los archivos de `contexto/` que toquen el tema del posteo
   (productos, herramientas, zona, calendario comercial).
4. Revisá `calendario.md`: qué toca esta semana y qué ya se publicó.
   No repetir tema de las últimas 2 semanas.
5. Si falta un dato (rinde, fecha), **no lo inventes**:
   dejá `[COMPLETAR: qué falta]` en el texto y listalo en tu resumen final.

## Pilares de contenido (rotarlos)
| # | Pilar | Qué incluye |
|---|-------|-------------|
| 1 | Precampaña maíz | Híbridos Nidera, posicionamiento por ambiente/zona, condiciones de precampaña |
| 2 | Precampaña girasol | Híbridos (CL, alto oleico), argumentos para el oeste bonaerense, fechas |
| 3 | Herramientas | Calculadora de márgenes (productor), herramientas financieras (reventa) |
| 4 | Técnica & tecnología | Manejo, densidades, fechas de siembra, traits, dato agronómico útil |
| 5 | Márgenes & finanzas | Números de campaña, financiación, canje, costo/beneficio de sembrar |
| 6 | Institucional / cercanía | Equipo, zona, RED.IN Nidera, historias con productores |

Mix semanal sugerido: 1 post de cultivo (maíz o girasol, alternando) +
1 de herramientas o márgenes + 1 técnico o institucional.

## Estructura del repo
```
CLAUDE.md                  ← este archivo (leerlo siempre primero)
prompt-opus-master.md      ← prompt para copiar/pegar en sesión con Opus
calendario.md              ← grilla semanal: qué sale, cuándo, estado
.claude/
  skills/
    generar-contenido.md   ← SKILL MAESTRA: flujo paso a paso para generar contenido
brand/
  identidad.md             ← paleta, tipografías, logo, formatos de pieza
  tono-voz.md              ← voz de marca, ejemplos, checklist de calidad
  referencias/             ← logos, carrusel HTML de referencia, capturas
contexto/
  empresa.md               ← quiénes somos, contacto, redes
  productos-26-27.md       ← 13 híbridos con fichas completas de marbete oficial
  herramientas.md          ← calculadora de márgenes y herramientas financieras
  zona-y-audiencia.md      ← perfil del productor y audiencias para Meta
  calendario-comercial.md  ← hitos de precampaña y fechas Nidera
  marbetes/                ← PDFs oficiales Nidera (fuente de verdad de producto)
posts/
  _plantilla-post.md       ← formato obligatorio de cada post
  AAAA-Www/                ← una carpeta por semana (ej: 2026-W25/)
carruseles/
  _plantilla-carrusel.html ← HTML single-file 1080×1350, 1 sección = 1 slide
reels/
  _plantilla-reel.md       ← guion: hook, escenas, texto en pantalla, audio
meta-ads/
  _plantilla-brief.md      ← formato de brief de pauta
  como-promocionar.md      ← cómo promocionar un reel ya publicado (sin republicarlo)
  briefs/                  ← un brief por campaña pautada
```

## Flujo de trabajo semanal
1. Cada lote semanal vive en `posts/AAAA-Www/` (ej: `posts/2026-W25/`).
   Nombrar archivos `post-01-tema.md`, `post-02-tema.md`, etc.
2. Cada post sigue `posts/_plantilla-post.md`: objetivo, copy final, descripción
   precisa de la pieza visual, hashtags (máx 8), CTA y nota de pauta.
3. Si un post va con pauta → crear brief en `meta-ads/briefs/AAAA-Www-tema.md`
   según la plantilla.
4. Placas, carruseles e historias → HTML en `docs/placas/AAAA-Www-tema.html` con el sistema
   visual **Siembra 26/27** (`docs/assets/hs2627.css` + `hs-anim.js`). Cada archivo lleva su texto,
   hashtags, horario, pauta y fuentes en `<script type="application/json" class="hs-meta">`.
   `npm run placas` → JPG · `npm run videos` → MP4 de las animadas · `npm run propuesta` → página
   `docs/propuesta/`. Mínimo legible: nada por debajo de 19 px en el canvas; lectura desde 30 px.
5. Reels → guion en `reels/` según plantilla.
6. **Siempre actualizá `calendario.md`** con lo generado (tema + estado).

## Reglas duras
- Voseo rioplatense, técnico pero cercano: hablamos de productor a productor.
- Nunca prometer rindes ni resultados sin fuente (ensayo, dato Nidera, REM). Citarla.
- **NUNCA publicar % de descuento, precios ni condiciones comerciales específicas
  en redes ni en la web.** Hablamos de "precampaña" en general. La venta se cierra
  cara a cara o por WhatsApp. El CTA siempre lleva a la conversación privada.
- CTA siempre a la conversación privada. En orgánico: primario "Mandanos un DM" + WhatsApp
  wa.me/5492314530691 visible en la placa y en la bio. En pauta: botón "Enviar mensaje de WhatsApp".
- Máximo 8 hashtags por post.
- Prohibido el marketing genérico: "¡imperdible!", "¡no te lo pierdas!", "¡calidad premium!".
- Paleta y tipografías según `brand/identidad.md`.
- Todo el contenido en español rioplatense.

## Checklist antes de dar por terminado un lote
- [ ] ¿Leíste `brand/` y `contexto/`?
- [ ] ¿Cada post tiene copy final, pieza visual descripta, hashtags y CTA?
- [ ] ¿Ningún dato comercial inventado? ¿Los `[COMPLETAR]` quedaron listados en el resumen?
- [ ] ¿Actualizaste `calendario.md`?
- [ ] ¿Creaste el brief de pauta si corresponde?
- [ ] ¿Pasa el checklist de `brand/tono-voz.md`?

## Estado del proyecto (mantener al día)
- ⏸️ Jul–sep 2026 (W29–W39): no se publicó nada. Último posteo: reel de márgenes (26/06).
- ✅ 24/09/2026: revisión completa + **relanzamiento W40–W46** → `docs/propuesta/index.html`
  (16 conceptos, 35 placas, 6 animaciones MP4 en `docs/placas/video/`). Posts en `posts/2026-W40…W46/`.
- ✅ Fecha de siembra del girasol en el oeste corregida según marbete: **15/10 → 15/11, límite 20/11**.
- ✅ Segunda vuelta (24/09): hooks de reels visibles desde el cuadro 0 + tapas para la grilla 3:4,
  modo aprobación en la propuesta, grilla del perfil, versiones crema, carrusel de maíz tardío,
  Estados de WhatsApp y generador de placas con foto (`docs/foto/`).
- ✅ Tercera vuelta (24/09): **arranque con 6 reels** directos y con cierre a WhatsApp →
  `docs/reels-siembra/index.html` (`node scripts/armar-reels.mjs`). Girasol realista
  (`scripts/lib/girasol.py`: semillas en filotaxis, pétalos, tallo que se mece, lote a contraluz) y
  plantas de maíz (`scripts/lib/maiz.py`); se meten en las piezas con `scripts/lib/inyectar-girasol.py`.
  Afuera por pedido del usuario: almanaque, refugio, "cómo leer un marbete" y teasers ("mirá este número").
  **Regla:** nada introductorio (el productor ya sabe leer un marbete): dato directo + pedido de contacto.
- ✅ Cuarta vuelta (25/09): girasol dibujado en serio (`flor2` en `scripts/lib/girasol.py`), R1 "la siembra
  arranca el 15/10", R2 "¿qué híbrido va en tu lote?", R4 "¿rinde o sanidad?" (el girasol todavía no se
  sembró), R5 nuevo `2026-W41-reel-ns7925.html` y R6 con la barra de cómo se compone el margen.
  **Regla:** en maíz no comparamos ensayos (no somos líderes): mostramos el híbrido y su tecnología.
- ✅ 07/10/2026: `brand/referencias/hibridos-nidera.md` (precios) borrado; el repo sigue público.
- ✅ 07/10/2026: estrategia v3 + plan de 9 semanas + galería de placas; las 8 ramas juntas en `main`.
- ✅ Estructura inicial creada (junio 2026, semana W24).
- ✅ Primer post de lanzamiento de precampaña 26/27 ya publicado por Henderseeds,
  previo a este repo. `[COMPLETAR: link o texto del post para mantener coherencia]`
- ⏳ Datos pendientes de carga: ver los `[COMPLETAR]` en `contexto/` y `brand/`.
