# Prompts de IA — tomas sintéticas de siembra

> Para generar imágenes y videos "de relleno" mientras no hay material real, o para piezas
> ilustrativas. Complementa a la [guía de tomas](guia-foto-video-siembra.md) (mismos códigos).

## Reglas de uso (leer antes de publicar algo generado)
1. **Nunca como "foto real".** No usar imágenes/videos de IA en el **Parte de siembra**, en
   testimonios ni en nada que diga "este lote", "esta semana" o nombre una localidad o un productor.
   Ahí va solo material real.
2. **Sí sirven para:** fondos de placas técnicas, reels ilustrativos (conceptos: emergencia,
   conteo, ventana de siembra), portadas, historias genéricas.
3. **Etiquetar.** En la pieza, chico: "Imagen generada con IA" o "Ilustrativa". Instagram/Meta
   además puede ponerle la etiqueta "Info de IA" sola; no la saques.
4. **Sin marcas en la imagen.** Nada de logos de Nidera, de maquinaria ni de otras semilleras
   generados por IA (salen deformes y es usar marcas sin control). Los logos reales se ponen
   encima, en el diseño.
5. **Revisar a ojo:** plantas con forma rara, máquinas imposibles, surcos que no cierran.
   Si algo "no es del oeste", descartar.

## Dónde generarlas
| Qué | Herramienta | Notas |
|-----|-------------|-------|
| Fotos | **Canva** (Magic Media / "Generar imagen") o **Gemini** (Imagen) | Canva: ya hay 5 generadas en tu cuenta (ver abajo). |
| Videos realistas de 5–8 s | **Gemini → Veo** (o Google Flow) | Lo más realista hoy para clips cortos. Pedí vertical 9:16. |
| Reel animado con datos | **Claude Code (este repo)** | `produccion/sintetico/reel-siembra-motion.html` → `node scripts/render-reel.mjs …` |

## Imágenes ya generadas en Canva (19/10/2026)
| Toma | Canva |
|------|-------|
| A1 · sembradora, plano general, atardecer | https://www.canva.com/M/MAHYaHLW1qA |
| A6 · plántulas de maíz a contraluz | https://www.canva.com/M/MAHYaC30cJg |
| A7 · cinta métrica en el surco de maíz | https://www.canva.com/M/MAHYaAC_9Jw |
| A6 · girasol en cotiledones | https://www.canva.com/M/MAHYaGq2p_4 |
| B3 · atardecer con sembradora en el horizonte | https://www.canva.com/M/MAHYaLxIsIM |

Para usarlas en el reel con fotos (`produccion/sintetico/reel-siembra.html`): bajarlas de Canva y
guardarlas en `produccion/sintetico/img/` como `a1-sembradora.jpg`, `a6-maiz.jpg`, `a6-girasol.jpg`,
`a7-cinta.jpg`, `b3-atardecer.jpg` (o pasarlas en el chat de Claude y lo hace él).

## Prompts de imagen (copiar y pegar)
Funcionan mejor en inglés. Todos piden vertical, sin marcas y estilo documental.

**A1 · Sembradora, plano general**
> Photorealistic vertical photo, documentary agricultural style. A no-till corn planter pulled by a tractor working across a wide flat field in the western Pampas of Buenos Aires, Argentina, seen from the side at about 40 meters. Dry wheat/soybean stubble on the ground, light dust trailing behind the planter. Golden hour, low warm sun from the side, long shadows, huge open sky with a few clouds, horizon in the upper third. Completely unbranded machinery: no logos, no text, no brand colors, neutral grey and red paint. Shot on a full-frame camera, 85mm, natural colors.

**A6 · Plántulas de maíz**
> Photorealistic vertical macro photo at ground level: young corn seedlings at V2-V3 stage emerging in a straight row through dry no-till crop stubble, Pampas of Buenos Aires, Argentina. Early morning backlight, sun low behind the plants making the leaves glow translucent green, dew drops, shallow depth of field with the row receding into soft bokeh. Natural colors, documentary style, no text, no people.

**A6 · Girasol en cotiledones**
> Photorealistic vertical macro photo at ground level: tiny sunflower seedlings with two round cotyledon leaves just emerging in a straight row through dark soil and dry no-till stubble, western Buenos Aires province, Argentina. Warm early morning side light, shallow depth of field, row fading into soft focus. Natural colors, documentary agronomy style, no text, no people.

**A7 · Conteo con cinta**
> Photorealistic vertical photo, close perspective low angle: a yellow measuring tape stretched along a straight row of young corn seedlings (V2 stage) in a no-till field with dry stubble, the tape running from the foreground into the distance along the row. Soft morning light, natural colors, documentary agronomy style, Pampas of Buenos Aires, Argentina. No people, no logos, no readable brand text.

**B3 · Atardecer de cierre**
> Photorealistic vertical cinematic photo: sunset over the flat endless Pampas of western Buenos Aires, Argentina. A tractor with a planter far away on the horizon as a small dark silhouette, a thin line of dust glowing in the backlight. Dramatic orange and deep blue sky, freshly sown field lines leading toward the horizon in the foreground. Unbranded machinery, no logos, no text, no people. Natural color grading.

## Prompts de video para Veo (Gemini) — clips de 8 s, vertical 9:16
Pedir siempre: *vertical 9:16, sin texto en pantalla, sin logos, sin música* (la música se
pone en Instagram). Generar 2–3 versiones de cada uno y quedarse con la más creíble.

**V1 · La pasada (A2) — hook del reel**
> Vertical 9:16 video, 8 seconds, photorealistic documentary style. Low camera at the edge of a flat no-till field in the western Pampas of Argentina at golden hour. An unbranded tractor pulling a wide corn planter approaches from the distance along the field and passes the camera from left to right at a safe distance, light dust in the backlight, stubble on the ground. Camera static on a tripod, slight natural handheld feel. No text, no logos, no people visible up close, ambient field sound only.

**V2 · Tren de siembra de costado (A1)**
> Vertical 9:16 video, 8 seconds, photorealistic. Side tracking shot at walking pace following a no-till planter's row units as they cut through dry wheat stubble, closing wheels pressing the soil, fine dust, warm late-afternoon light, western Buenos Aires province. Unbranded machinery, no logos, no text.

**V3 · Plántulas a contraluz (A6)**
> Vertical 9:16 video, 8 seconds, photorealistic macro. Very slow lateral slider movement at ground level along a row of young corn seedlings (V2-V3) emerging through no-till stubble at sunrise, backlit translucent green leaves, dew, shallow depth of field. No text, no people.

**V4 · Conteo de plantas (A7)**
> Vertical 9:16 video, 8 seconds, photorealistic. A person's hands (no face visible) stretch a yellow measuring tape along a row of young corn seedlings in a no-till field, then a finger moves along the row touching each plant as if counting. Soft morning light, documentary agronomy style, Pampas of Argentina. No text, no logos.

**V5 · Cierre atardecer (B3)**
> Vertical 9:16 video, 8 seconds, photorealistic cinematic timelapse feel. Sunset over the flat Pampas, an unbranded tractor and planter as a small silhouette on the horizon moving slowly, dust glowing, clouds drifting, freshly sown lines in the foreground leading to the horizon. No text, no logos.

Con V1 → V2 → V3 → V4 → V5 (8 s c/u, recortados a 3–5 s) se arma el reel
"[Un día de siembra](../reels/2026-W44-reel-un-dia-de-siembra.md)": los textos y el cierre de marca
se suman en CapCut o en el editor de Reels, siguiendo el guion.
