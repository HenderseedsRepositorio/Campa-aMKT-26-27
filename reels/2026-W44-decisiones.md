# Decisiones 26/27 — sesión 3 (21/10/2026)

Pedido de Henderseeds (21/10): una sesión nueva de placas y videos que **le deje al productor algo para
decidir**, no piezas para que responda ("¿cuántos mm te cayeron?"). Página para verlo todo:
[docs/decisiones/](https://henderseedsrepositorio.github.io/Campa-aMKT-26-27/decisiones/)
(`python3 scripts/armar-decisiones.py`).

## Versión simple (la que va al feed) — devolución del 21/10
"Te pasaste para el otro lado": las fichas tenían demasiada información. El mensaje se queda (cada pieza
ayuda a decidir algo), pero con el formato de los reels anteriores: **una idea por pantalla, letra grande,
pocas palabras** (máximo ~15 grandes por pantalla; las fichas llegaban a 47).

| # | Reel (18 s) | Escenas | Archivo |
|---|-------------|---------|---------|
| 01 | ¿Te alcanza la sembradora? | 15/11 → hectáreas ÷ días hábiles = ha por día → ejemplo 40 ha por día → regla | `produccion/decisiones/s1-sembradora.html` |
| 02 | ¿Qué girasol va? Empezá por tu lote | ¿Phomopsis? NS 1115/1117 → ¿no? NS 1113 CL → ¿alto oleico? NS 1227 CL HO → regla | `produccion/decisiones/s2-girasol.html` |
| 03 | ¿Qué te preocupa más del tardío? | chicharrita NS 7925 → viento NS 7765 → malezas NS 7921 CL → regla | `produccion/decisiones/s3-maiz-tardio.html` |
| 04 | ¿En qué ambiente está tu lote? | escala del girasol → promedio, no la mejor → híbrido, plantas, inversión → "mandanos tus rindes" | `produccion/decisiones/s4-ambiente.html` |
| 05 | ¿Girasol o maíz tardío en ese lote? | rinde · precio · costo · flete → límite 20/11 y chicharrita → calculadora → regla | `produccion/decisiones/s5-girasol-o-maiz.html` |

- Reels: `docs/placas/video/2026-W44-decision-0N-*.mp4` (+ portada al segundo 1,2).
- Placas 4:5 de resumen (pregunta, 3 respuestas y la regla): `node scripts/render-fichas.mjs s` → `docs/decisiones/img/decision-0N-feed.jpg`.
- Captions cortas en `scripts/armar-decisiones.py`. Cierre de todas: "Mandanos un DM" + WhatsApp.
- La ficha 04 simple usa solo la escala del girasol (sin cortes de maíz en kg/ha).
- Las fichas completas de abajo (`dN-*.html`) quedan solo para el PDF que se manda a quien pide más detalle.

## 06–10 · otra onda: "charla de lote" (21/10)
Fondo noche, la frase entra palabra por palabra (como dicha en el lote), palabras clave en ámbar, línea de avance
y cierre en tarjeta crema. Cada reel es solo datos sobre `produccion/decisiones/charla.js`.

| # | Gancho | Escenas | Fuente | Archivo |
|---|--------|---------|--------|---------|
| 06 | Todo lote tiene un rinde de indiferencia. | costos por ha ÷ precio neto → si apenas lo superás, revisá el planteo → margen.henderseeds.com | sin cifras; herramientas.md | `c6-indiferencia.html` |
| 07 | Alto oleico: la bonificación la paga el comprador. | NS 1227 CL HO → Downy Mildew R → óptima 15/11, límite 20/11 | marbete NS 1227 CL HO | `c7-alto-oleico.html` |
| 08 | Un lote. Dos ambientes. | cada ambiente, su híbrido y su densidad → Recomendación Asista por ambiente → siembra variable opcional | Plan de Campaña, paso 2 | `c8-lomas-y-bajos.html` |
| 09 | Maíz: no todo híbrido va en tardía. | NS 7621 mejor en temprana → tardía: 7925, 7624 CL, 7818 → las dos: 7765, 7852, 7921 CL | posicionamiento de los marbetes; sin ensayos | `c9-maiz-fecha.html` |
| 10 | Lote encharcado después de sembrar: hay seguro. | seguro de resiembra de Nidera (granizo o encharcamiento) → contá las plantas que quedaron → si te pasa, escribinos | Plan de Campaña, paso 4; sin condiciones | `c10-encharcado.html` |

## Tono (revisión del 21/10)
Un agente de marca revisó los 10 contra `brand/tono-voz.md`. Cambios: ganchos afirmativos (01 "Girasol: la ventana
cierra el 15/11.", 02 "Girasol: el híbrido depende del lote.", 03 "Tardío: tres riesgos, tres híbridos.", 04 "Girasol:
cuatro ambientes según el rinde.", 05 "Girasol o maíz tardío: misma cuenta."), "Si el lote tuvo Phomopsis" en vez de
preguntas, cierre común "Pasamos por tu lote. Mandanos un DM.". En 08 la siembra variable es **opcional** (no "incluida");
en 10 se sacaron los pasos del seguro (podían ser condiciones): queda "contá las plantas" y "si te pasa, escribinos".
En girasol, en pantalla solo "% de éxito en N comparaciones": el marbete no dice contra qué se comparan los qq/ha.

## Las fichas completas (solo PDF)

## La idea
Cada pieza responde **una decisión que el productor tiene que tomar en las próximas semanas**, con el
dato del marbete, la cuenta o el criterio, y **una regla** que se lleva. El video arma la ficha delante de
él; la placa del feed es la ficha terminada; las cinco juntas forman el *Cuaderno de decisiones 26/27*
(PDF) que se manda a quien comenta **FICHAS**. Si su lote no encaja, el cierre es "Lo vemos juntos".

| # | Decisión | Herramienta en pantalla | Pilar | Archivo |
|---|----------|-------------------------|-------|---------|
| 01 | ¿Te alcanza la sembradora para el girasol? | Calendario de días hábiles + cuenta ha/día | Técnica (girasol) | `produccion/decisiones/d1-sembradora.html` |
| 02 | ¿Qué girasol va? Empezá por tu lote | Árbol de decisión con datos de ensayo Sur + Oeste | Producto (girasol) | `produccion/decisiones/d2-girasol.html` |
| 03 | Maíz tardío: elegí por tu mayor riesgo | Mapa de calor del perfil sanitario (6 híbridos) | Producto (maíz tardío) | `produccion/decisiones/d3-maiz-tardio.html` |
| 04 | ¿En qué ambiente está tu lote? | Escala de ambientes del marbete + promedio de campañas | Diagnóstico (paso 1 del Plan) | `produccion/decisiones/d4-ambiente.html` |
| 05 | ¿Girasol o maíz tardío en ese lote? | Misma cuenta para los dos + calculadora de márgenes | Márgenes / herramientas | `produccion/decisiones/d5-girasol-o-maiz.html` |

Motor común: `produccion/decisiones/ficha.css` + `ficha.js` (gancho legible en el cuadro 0, herramienta
que se arma, LA REGLA a los 13,6 s, sello GUARDALA, cortina y cierre "Comentá FICHAS" a los 18,4 s).
Tapa del cuaderno: `produccion/decisiones/d0-tapa.html`.

- Reels (22 s): `node scripts/render-reel.mjs produccion/decisiones/dN-*.html` → `docs/placas/video/2026-W44-ficha-0N-*.mp4`
- Placas 4:5: `node scripts/render-fichas.mjs` → `docs/decisiones/img/ficha-0N-feed.jpg` (controla que nada se salga)
- Estados 9:16: cuadro de los 17 s del reel → `docs/decisiones/img/ficha-0N-estado.jpg`
- Cuaderno PDF (tapa + 5): `docs/decisiones/cuaderno-de-decisiones-26-27.pdf`
- Revisión automática: `node scripts/revisar-reel.mjs produccion/decisiones/dN-*.html` (las 5 en verde)

## Fuentes de cada dato
- **01.** Ventana del girasol, Oeste de Buenos Aires: óptima 15/10–15/11, límite 20/11 (marbetes oficiales
  Nidera 26/27 de los 4 girasoles). Cuenta del ejemplo, rotulada: 21 días − 7 perdidos (1 de cada 3, supuesto)
  = 14 días hábiles; 560 ha ÷ 14 = 40 ha por día.
- **02.** Posicionamiento, ensayos a campo Sur + Oeste (diferencia de rinde, % de éxito, n.º de comparaciones)
  y perfil sanitario de NS 1113 CL, NS 1115 CL, NS 1117 CL y NS 1227 CL HO: marbetes Nidera
  (`contexto/productos-26-27.md`). En girasol se muestran datos de ensayo.
- **03.** Perfil sanitario y agronómico (1 excelente – 9 deficiente) de NS 7925, NS 7765, NS 7921 CL,
  NS 7624 CL, NS 7818 y NS 7852: marbetes Nidera. **Sin números de ensayo de maíz** (regla del 25/09).
- **04.** Escala de ambientes de los marbetes Nidera (texto de los PDF): girasol < 1.500 / 1.500–2.500 /
  2.500–3.500 / > 3.500 kg/ha; maíz < 6.000 / 6.001–9.000 / 9.001–12.000 / > 12.000 kg/ha. Es la
  definición del ambiente, no un resultado de ensayo. Ejemplo: (2.100 + 2.600 + 1.900) ÷ 3 = 2.200.
- **05.** Sin cifras: la ficha pide los datos del lote. Límite del girasol 20/11 (marbete). Calculadora:
  margen.henderseeds.com (`contexto/herramientas.md`).

## Captions
Están en `scripts/armar-decisiones.py` (botón "Copiar texto" en la página). Todas: voseo, máximo 8
hashtags, "Comentá FICHAS" + WhatsApp wa.me/5492314530691, sin precios ni condiciones.

## Cuando comenten FICHAS
Responder por DM (no en el comentario):
> ¡Hola! Acá tenés las 5 fichas: https://henderseedsrepositorio.github.io/Campa-aMKT-26-27/decisiones/cuaderno-de-decisiones-26-27.pdf
> ¿Qué estás por decidir, girasol o maíz tardío? Si querés, lo vemos para tu lote.

Cada respuesta va al mapa de cuentas en Salesforce.

## Para revisar antes de publicar (Santi)
- Ficha 04 muestra en kg/ha los cortes de ambiente del maíz. No es un dato de ensayo, pero es un número de
  maíz: confirmar que entra en la regla del 25/09.
- Ficha 03 incluye NS 7852 (lanzamiento, temprana y tardía) aunque no gana en ninguna columna.
