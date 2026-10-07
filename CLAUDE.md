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
Galería de descarga: `docs/estrategia/piezas/index.html` (4 opciones por placa; recomendadas: Plan C y Clearfield D).
Los JPG se renderizan local con Playwright y se commitean (el robot de esta rama no renderiza).
**Roles (07/10):** Alvaro publica; Santi revisa cada pieza antes con la checklist.
**Oferta (definida por Alvaro el 07/10): "Plan de Campaña HenderSeeds"**, seis pasos:
1. Diagnóstico · 2. Recomendación Asista (híbrido por ambiente; siembra variable incluida, opcional) ·
3. Financiación (en público solo "a cosecha y con tarjetas agro, en pesos o dólares"; el plazo
exacto va solo en privado) · 4. Seguro de resiembra · 5. Vuelo de drone (calidad de siembra) ·
6. Informe de visita. El drone aparece solo como paso 5 de la oferta, nunca como pieza suelta.
La hoja de visita y el modelo de informe (PDF) NO se suben al repo: tienen condiciones comerciales.
**Regla del equipo (25/09): en maíz NO se muestran números de ensayo** (kg/ha vs. promedio): se
muestra el híbrido y su tecnología. En girasol sí.
**Nunca subir información comercial interna al repo (es público).** El archivo con precios
(`brand/referencias/hibridos-nidera.md`) se borró de las 8 ramas el 07/10; sigue en el historial.
GitHub: Alvaro decidió no pagar Pro (07/10).

**Ramas (leer antes de trabajar):** la versión más completa del contenido está en
`claude/gallant-hawking-qbdjlf` (relanzamiento de septiembre, la que publica el sitio). Esta rama
(`claude/loving-edison-byfwnx`) arrancó de la de agosto y solo publica `docs/estrategia/`. Falta
consolidar todo en una rama `main` (pendiente de autorización de Alvaro).

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
  briefs/                  ← un brief por campaña pautada
```

## Flujo de trabajo semanal
1. Cada lote semanal vive en `posts/AAAA-Www/` (ej: `posts/2026-W25/`).
   Nombrar archivos `post-01-tema.md`, `post-02-tema.md`, etc.
2. Cada post sigue `posts/_plantilla-post.md`: objetivo, copy final, descripción
   precisa de la pieza visual, hashtags (máx 8), CTA y nota de pauta.
3. Si un post va con pauta → crear brief en `meta-ads/briefs/AAAA-Www-tema.md`
   según la plantilla.
4. Carruseles → HTML single-file 1080×1350 en `carruseles/`, una sección por slide,
   screenshoteable sin scroll. Si la sesión tiene conectado el MCP de Canva,
   también se puede armar la pieza directo en Canva (avisar en el resumen con el link).
5. Reels → guion en `reels/` según plantilla.
6. **Siempre actualizá `calendario.md`** con lo generado (tema + estado).

## Reglas duras
- Voseo rioplatense, técnico pero cercano: hablamos de productor a productor.
- Nunca prometer rindes ni resultados sin fuente (ensayo, dato Nidera, REM). Citarla.
- **NUNCA publicar % de descuento, precios ni condiciones comerciales específicas
  en redes ni en la web.** Hablamos de "precampaña" en general. La venta se cierra
  cara a cara o por WhatsApp. El CTA siempre lleva a la conversación privada.
- CTA siempre a WhatsApp comercial: wa.me/5492314530691
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
- ✅ Estructura inicial creada (junio 2026, semana W24).
- ✅ Primer post de lanzamiento de precampaña 26/27 ya publicado por Henderseeds,
  previo a este repo. `[COMPLETAR: link o texto del post para mantener coherencia]`
- ⏳ Datos pendientes de carga: ver los `[COMPLETAR]` en `contexto/` y `brand/`.
