# Reel — Un día de siembra en 30 segundos

- **Semana:** 2026-W44 (sábado 31/10, o apenas estén las tomas) · **Pilar:** institucional / técnica
- **Objetivo:** alcance en la zona + seguidores nuevos; mostrar que estamos en el lote. Base para pauta de Alcance con tope de frecuencia si se quiere reactivar la cuenta.
- **Duración objetivo:** 30–34 s · **Formato:** 1080×1920 (9:16)
- **Quién aparece / qué se filma:** tomas de la [guía de tomas](../produccion/guia-foto-video-siembra.md) (códigos A1–A8, B2/B3, B6). Celular alcanza. Vertical.

> 🎬 **Alternativa lista sin filmar (19/10):** versión 100 % animada (motion graphics, sin fotos),
> 28 s, mismo mensaje con los datos de marbete y de conteo →
> [`produccion/sintetico/reel-siembra-motion.html`](../produccion/sintetico/reel-siembra-motion.html)
> (MP4: `node scripts/render-reel.mjs produccion/sintetico/reel-siembra-motion.html`).
> Publicable tal cual: no muestra nada "real" que no lo sea. Agregar música desde Instagram.
> Versión con fotos (reales o IA): `produccion/sintetico/reel-siembra.html` + `produccion/sintetico/img/`.

> 🔀 **4 versiones para elegir (19/10)** — mismo archivo, `?v=1..4` (`node scripts/render-reel.mjs
> produccion/sintetico/reel-experiencia-v5.html --v N`). Se descartó "de la bolsa a la cosecha".
> | Versión | Gancho | Apertura | Cierre | Duración |
> |---|---|---|---|---|
> | V1 | ¿Quién te acompaña toda la campaña? | 4 pasos que vuelan al seguidor | Toda la campaña, en tu lote. | 36 s |
> | V2 | ¿Quién conoce tu lote tanto como vos? | Pregunta + respuesta "Nosotros. Antes, durante y después de sembrar." | Antes, durante y después. | 36 s |
> | V3 | ¿Quién recorre tu lote con vos? | Línea de tiempo de la campaña que sube y se vuelve el seguidor | Recorremos tu lote con vos. | 36 s |
> | V4 | ¿Sembrás solo o con equipo? | 4 pasos (corte corto, sin bajadas) | Sembrá con equipo. | 23,5 s |
> Los ganchos son intercambiables entre versiones (variable `VARIANTES` del HTML).
>
> ✅ **v5 "Experiencia Nidera" (19/10) — revisada por 4 agentes (diseño, formatos, ritmo, texto/marca)** →
> [`produccion/sintetico/reel-experiencia-v5.html`](../produccion/sintetico/reel-experiencia-v5.html)
> - **Reel** (36 s): `node scripts/render-reel.mjs produccion/sintetico/reel-experiencia-v5.html`
> - **Historia** (26 s, sin bajadas, lugar para stickers): `… --modo historia`, cortada en 3 archivos:
>   H1 gancho (5 s) · H2 etapas (15 s) · H3 cierre (6 s).
> - Gancho: "¿Quién te acompaña de la bolsa a la cosecha?" (se descartó "¿Comprás semilla o comprás un
>   plan?": en el campo "plan" se lee como plan de pagos/canje, roza condición comercial).
> - Grilla dentro de la zona libre de IG (x 80–930, y 250–1540); la foto del lote aparece **solo** en el
>   conteo; el gancho muestra los 4 pasos y vuelan al seguidor de etapas; naranja = resaltado + 1 dato.
> - Exportación BT.709, H.264 High, pista de audio muda (la música se agrega en Instagram).
>
> **Plan de publicación**
> 1. **Día 1 — Reel.** Portada: `produccion/sintetico/out/portada-reel-1080x1920.png` (o el cuadro de 3 s).
>    Subir mudo y agregar música desde la biblioteca de Instagram (acústica, ~120 BPM, cortes en 4,4 ·
>    10,8 · 16,8 · 24,6 · 31,4 s). Compartirlo a la historia ese mismo día.
> 2. **Días 2–3 — Historia propia (3 partes).** H1 + sticker de encuesta en y 1380–1560: "¿Ya medís la
>    calidad de siembra? Sí / Todavía no" (a los que respondan, DM). H2 tal cual. H3 + sticker de enlace a
>    wa.me/5492314530691 en el espacio libre debajo de "Tocá el enlace y escribinos".
> 3. **Pauta (si se hace):** pide una versión con los gráficos ~250 px más arriba (el botón del anuncio
>    tapa y 1248–1540) y música de Meta Sound Collection incrustada.
>
> **Caption (v5):**
> ¿Quién te acompaña de la bolsa a la cosecha? 🌽🌻
> Con Experiencia Nidera, el equipo HenderSeeds está en tu lote en cada etapa:
> — Antes de sembrar: híbrido y densidad para cada zona del lote, con la base de ensayos de Nidera.
> — Al sembrar: mapa de siembra variable para tu sembradora, con la recomendación Nidera o a medida.
> — Con el cultivo nacido: control con dron (Nidera Vuela): plantas logradas, distribución, fallas y dobles.
> — Hasta la cosecha: recorridas e informe de visita con qué hacer.
> ¿Lo vemos para tu campo? Mandanos un DM o escribinos por WhatsApp 📲 wa.me/5492314530691
> #Henderseeds #Nidera #ExperienciaNidera #Maiz #Girasol #Henderson #Daireaux #Bolivar
>
> **Confirmado 19/10:** OK de Nidera para el logo y los nombres "Experiencia Nidera" y "Nidera Vuela";
> los 4 servicios valen para todos los clientes. · El "106 plantas detectadas" es el conteo de nuestra prueba (coincide con
> los anillos que se ven), no un dato de Nidera Vuela.
>
> 🎬 **v4 "Experiencia Nidera" (19/10):** reel general del acompañamiento, 37 s →
> [`produccion/sintetico/reel-experiencia-v4.html`](../produccion/sintetico/reel-experiencia-v4.html)
> Gancho en pregunta sobre foto real de dron (horizontal) + 4 etapas con seguidor de pasos:
> **Antes** (híbrido y densidad por ambiente, base de ensayos Nidera) · **Siembra** (siembra variable,
> mapa de prescripción; recomendación Nidera o plan a medida) · **Post-siembra** (calidad de siembra
> con dron: escena de detección sobre foto real, sin números) · **Ciclo** (informe de visita) ·
> Cierre "Experiencia Nidera · Con el equipo HenderSeeds en tu lote".
> Ganchos (variable `GANCHO`): ¿Comprás semilla o comprás un plan? · ¿Quién te acompaña después de
> la bolsa? · ¿Qué hay detrás de una buena siembra? · ¿Tu semilla viene con equipo? · ¿Sembrar y
> esperar? Hay otra forma. · ¿Cuánto conocés tu lote?
> `[COMPLETAR: confirmar el nombre exacto de la herramienta de recomendación ("Asista" / Asistente
> Dinámico Nidera) si se quiere nombrar en el video o el caption]`
>
> 🎬 **v3 con fotos REALES de dron (19/10), foco en conteo:** 37 s, 5 escenas + cierre →
> [`produccion/sintetico/reel-siembra-v3.html`](../produccion/sintetico/reel-siembra-v3.html)
> 1. **Gancho sobre foto real** (texto desde el cuadro 0, sirve de portada): "La sembradora dice
> una cosa. / El lote, otra." · 2. Cuándo medir: V3–V4 · 3. Cómo: Nidera Vuela (dron por ambientes) ·
> 4. Qué medimos: foto real con las plantas detectadas + plantas/ha, CV, fallas/dobles · 5. Para qué
> sirve: resembrar o no, ajustar la sembradora, densidad por ambiente · Cierre co-brand.
> ⚠️ Tarjetas de la escena 4 = EJEMPLO hasta tener el informe real (ver `produccion/analisis-dron-ejemplo.md`).
>
> **Ganchos alternativos** (variable `GANCHO`): "Lo que no ves desde la camioneta, / lo ve el dron." ·
> "¿Cuántas plantas nacieron / de verdad?" · "Antes de decidir si resembrás, / mirá esto." ·
> "Así se ve tu maíz / desde el dron." · "¿Nació parejo? / Desde arriba no hay dudas."
>
> **Caption sugerido (v3):**
> La sembradora dice una cosa. El lote, otra. 🌽
> En V3–V4 volamos el lote con dron (Nidera Vuela), sacamos fotos por ambiente y contamos planta por planta: cuántas hay, cómo quedaron distribuidas y dónde hubo fallas.
> Con ese dato decidís si resembrás, qué ajustar en la sembradora y qué densidad usar en cada ambiente la próxima.
> ¿Lo medimos en tu lote? Mandanos un DM. 📲 wa.me/5492314530691
> #Henderseeds #Nidera #NideraVuela #Maiz #Siembra2627 #Henderson #Daireaux #Bolivar
>
> 🎬 **v2 educativa (19/10), ilustrada:** 5 escenas + cierre, ritmo tranquilo, 40 s →
> [`produccion/sintetico/reel-siembra-motion-v2.html`](../produccion/sintetico/reel-siembra-motion-v2.html)
> 1. Título (configurable) · 2. En V3–V4 el lote ya muestra cómo nació · 3. **Nidera Vuela**: volamos
> el lote con dron, fotos en loma/media loma/bajo · 4. Qué medimos: plantas/ha, CV de distancia entre
> plantas, fallas/dobles · 5. Por qué importa (6–9 %, Nafziger 1991/INTA) · Cierre co-brand
> "Tecnología Nidera Vuela · El ojo de HenderSeeds en tu lote".
> ⚠️ Los números de la escena 4 son **EJEMPLO ILUSTRATIVO**: `[COMPLETAR: plantas/ha, CV y
> fallas/dobles de un informe real de Nidera Vuela]` (variable `METRICAS` del HTML).
>
> **Opciones de título** (variable `TITULO` del HTML):
> La 26/27 ya se está sembrando. · La siembra no termina en la sembradora. · Sembrar es la mitad.
> La otra, medirlo. · ¿Cómo nació tu maíz? Lo vemos desde arriba. · Tu lote, planta por planta. ·
> Del surco al dron. · Sembramos. Ahora, a contar. · Lo que dejó la sembradora, el dron lo cuenta. ·
> Ya está sembrado. ¿Nació parejo?

## Hook (segundos 0–3)
Toma **A2**: la sembradora viene de frente desde la cabecera y pasa de largo.
Texto en pantalla (grande, Archivo Black blanco con sombra suave): **"Un día de siembra en el oeste, en 30 segundos."**

## Escenas
| # | Seg | Toma / imagen | Texto en pantalla | Audio |
|---|-----|---------------|-------------------|-------|
| 1 | 0–3 | **A2** sembradora de frente | Un día de siembra en el oeste, en 30 segundos. | Sonido ambiente (B6) + entra música |
| 2 | 3–7 | **A3** carga de tolva, cámara lenta | La semilla: Nidera, elegida lote por lote. | música |
| 3 | 7–12 | **A1** plano general de costado | Maíz temprano: adentro. Girasol: arrancando. | música + motor bajo |
| 4 | 12–17 | **A5** semilla en el surco con la regla | Profundidad pareja = nacimiento parejo. | música |
| 5 | 17–22 | **A7** cinta en el surco, alguien contando | Después, contamos plantas: 19,05 m × 1.000. | música |
| 6 | 22–26 | **A6** plántulas a contraluz | Para saber cómo arrancó cada lote. | música |
| 7 | 26–30 | **A8** equipo HenderSeeds con el productor | De la bolsa a la cosecha, en el lote con vos. | música |
| 8 | 30–34 | **B3** atardecer o **B2** dron → placa final | ¿Cómo viene tu siembra? Mandanos un DM. | música baja, cierre |

## Cierre + CTA (últimos 4 s)
Placa final navy `#0A0F1B` 9:16: logo HenderSeeds blanco al centro, debajo "¿Cómo viene tu siembra?
Mandanos un DM" (DM Sans 700) y abajo chico `RED.IN · Nidera Semillas` + WhatsApp 2314 53-0691.
Se puede usar la historia 9:16 de la placa del martes 20/10 como último frame.

## Edición
- Cortes al ritmo de la música, cada toma 3–5 s. Sin transiciones raras: corte seco.
- **Subtítulos siempre** (texto en pantalla de la tabla), zona segura central, nada en el tercio inferior (lo tapa la UI de IG).
- Corrección de color suave, cálida. Nada de filtros.
- Si falta alguna toma: A5 y A7 se pueden reemplazar por A4 (semilla en la mano) y A1 de otro ángulo. El hook (A2) y el cierre son obligatorios.
- Herramienta sugerida: CapCut o el editor de Reels de Instagram (plantilla "texto + corte").

## Audio sugerido
Sonido ambiente de la sembradora los primeros 2 s (B6) y después música instrumental suave con
pulso (de la biblioteca de audio de Instagram, sin letra). Volumen del ambiente al 20 % por debajo.

## Caption para publicar
> Así viene la siembra 26/27 en el oeste: maíz temprano adentro y el girasol arrancando. 🚜🌻
>
> De la tolva al conteo de plantas, en el lote con vos.
>
> ¿Cómo viene tu siembra? Mandanos un DM.
>
> #Henderseeds #Nidera #Siembra2627 #Maiz #Girasol #Henderson #Daireaux #Bolivar

## Estado
- [x] ✍️ Guion listo
- [ ] 🎥 Filmado (faltan tomas: A1, A2, A3, A5, A6, A7, A8, B2/B3, B6)
- [ ] 📤 Publicado → link:
