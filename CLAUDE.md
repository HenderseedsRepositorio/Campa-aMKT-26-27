# Henderseeds — Campaña Digital 26/27

## Qué es este repo
Centro de producción de contenido y marketing digital de **HenderSeeds**
([henderseeds.com](https://henderseeds.com)), distribuidor y asesor técnico de la red
**RED.IN de Nidera Semillas** para **Henderson, Daireaux y Bolívar**
(oeste de la provincia de Buenos Aires, Argentina).

**Foco actual:** precampaña de **maíz y girasol 26/27**. La precampaña sigue abierta
hasta agosto/septiembre 2026 aproximadamente (las fechas y condiciones las define Nidera).
También difundimos las **herramientas Henderseeds**: calculadora de márgenes para el
productor y herramientas financieras para la reventa.

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
