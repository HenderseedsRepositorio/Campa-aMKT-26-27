# Reels de la semana — W43/W44 (siembra 26/27)

> 4 videos con **estilos y mensajes distintos** para no repetir formato. Todos 1080×1920, H.264,
> color BT.709, pista de audio muda (agregar música desde Instagram). Se renderizan con
> `node scripts/render-reel.mjs <archivo>` → `produccion/sintetico/out/`.

| # | Video | Estilo | Mensaje | Duración | Publicar |
|---|-------|--------|---------|----------|----------|
| 1 | [`reel-experiencia-v5.html?v=3`](../produccion/sintetico/reel-experiencia-v5.html) | Agro-tech oscuro, línea de tiempo + 4 etapas | Acompañamiento Experiencia Nidera (institucional) | 31 s | **mar 20/10** |
| 2 | [`reel-girasol-tolva.html`](../produccion/sintetico/reel-girasol-tolva.html) | Claro/editorial (crema): tolva que se llena, calendario real, 4 girasoles | Arranca el girasol: ventana del oeste + qué girasol va en cada lote | 24 s | **jue 22/10** |
| 3 | [`reel-conteo-plantas.html`](../produccion/sintetico/reel-conteo-plantas.html) | Tutorial con números gigantes, 3 pasos | Cómo contar plantas + planilla para el lote (imán de contactos) | 24 s | **sáb 24/10** (+ pauta) |
| 4 | [`reel-maiz-tardio.html`](../produccion/sintetico/reel-maiz-tardio.html) | Fichas de producto que se deslizan | 3 híbridos para tardío (producto) | 22 s | **mar 27/10** |

## Video 1 — ¿Quién sigue de cerca tu lote?
Elegido por Henderseeds (19/10, opción 2). Cierre: "Lo seguimos de cerca. Equipo HenderSeeds · etapa por etapa."
Botón: "Pedí tu recorrida por DM" + línea de WhatsApp. Render: `node scripts/render-reel.mjs
produccion/sintetico/reel-experiencia-v5.html --v 3` (31 s; la línea de tiempo aparece en el segundo 0,3).
**Otras variantes del título** (`?g=línea1|línea2`): ¿Quién le sigue el pulso a tu lote? ·
¿Quién está encima de tu lote? · ¿Quién no le saca los ojos a tu lote?

**Cómo publicarlo:**
- **Reel** 9:16, subido a Instagram con "compartir también en Facebook". Portada: cuadro del segundo
  ~2,9 (título completo + línea de tiempo; entra en el recorte 3:4 de la grilla).
- Música: el MP4 va mudo → elegir un tema instrumental tranquilo de la biblioteca de IG, volumen bajo.
- Ubicación: Henderson. Fijarlo en el perfil la primera semana.
- Mismo día, **compartirlo en historia** con sticker de encuesta: "¿Ya medís la calidad de siembra?
  Sí / Todavía no" → a los que voten "Todavía no", responderles por DM.
- Horario: mar 20/10, 7–9 h o 20–22 h. Si en 48 h tiene buena retención, pautarlo (ver brief W43).
- Colaboración con la cuenta de Nidera (Collab de IG) **solo con su OK**.
- **Voz en off y clip real:** guion y pasos en [2026-W43-video1-voz-y-clip.md](2026-W43-video1-voz-y-clip.md).

**Caption:**
> ¿Quién sigue de cerca tu lote? 🌽🌻
> Con Experiencia Nidera, el equipo HenderSeeds te acompaña en cada etapa:
> — Antes de sembrar: híbrido y densidad para cada zona del lote, con la base de ensayos de Nidera.
> — Al sembrar: mapa de siembra variable para tu sembradora, con la recomendación Nidera o a medida.
> — Con el cultivo nacido: control de calidad de siembra con dron (Nidera Vuela).
> — Hasta la cosecha: recorridas e informe de cada visita.
> ¿Querés que recorramos tu lote? Mandanos un DM o escribinos por WhatsApp 📲 wa.me/5492314530691
>
> #Henderseeds #Nidera #ExperienciaNidera #Maiz #Girasol #Henderson #Daireaux #Bolivar

## Video 2 — ¿Ya tenés el girasol en la tolva?
Reemplaza a la versión "¿Cuándo se siembra el girasol?" (`reel-girasol-ventana.html`, queda de archivo).
Arco: tolva que se llena de semilla (arranca el girasol, sin decirlo) → ventana óptima en el calendario →
¿cuál va en tu lote? (NS 1113 CL techo de rinde y aceite · NS 1115 CL la sanidad más completa ·
NS 1117 CL máximo rinde con Phomopsis 2 · NS 1227 CL HO alto oleico) → 20/11 + consejo → contacto.
**Títulos alternativos** (`?g=`): El girasol ya está en la tolva. · ¿Ya cargaste la tolva? · Se viene el
amarillo. · ¿Llegás con el girasol?
**Caption:**
> ¿Ya tenés el girasol en la tolva? 🌻
> En el oeste bonaerense la ventana óptima va del 15/10 al 15/11 (fecha límite 20/11), según los marbetes Nidera. Igual para los cuatro: NS 1113 CL, NS 1115 CL, NS 1117 CL y NS 1227 CL HO.
> Cada uno tiene su lugar: techo de rinde y aceite, la sanidad más completa, máximo rinde con Phomopsis 2 o alto oleico.
> Hay tiempo para sembrar bien. ¿Dudas de densidad o de qué girasol va en tu lote? Pedí tu recomendación por DM o escribinos 📲 wa.me/5492314530691
>
> #Henderseeds #Nidera #Girasol #NS1113CL #Siembra2627 #Henderson #Daireaux #Bolivar
Fuente: marbetes Nidera 26/27, Oeste de Buenos Aires: óptima 15/10–15/11, límite 20/11.
⚠️ El calendario marca "hoy" el 22/10 (variable `HOY` del HTML): cambiarlo si se publica otro día.

## Video 3 — ¿Cuántas plantas lograste?
Tutorial de 3 pasos que cierra con un **imán de contactos**: la
[planilla de conteo de plantas](../docs/recursos/planilla-conteo-plantas.html) (A4 para imprimir; se
genera con `node scripts/render-pdf.mjs docs/recursos/planilla-conteo-plantas.html` → PDF + JPG).
- **Orgánico:** cierre "Comentá PLANILLA" (`reel-conteo-plantas.mp4`). Los comentarios empujan el alcance
  y cada uno abre una conversación privada.
- **Pauta:** cierre "Mandanos PLANILLA por DM" (`--v pauta`), ver
  [brief](../meta-ads/briefs/2026-W43-maiz-conta-plantas.md). El carrusel queda en el feed para guardar.
- 63 plantas / 63.000 pl/ha = EJEMPLO rotulado.

**Caption:**
> ¿Cuántas plantas lograste? 🌽
> Con una cinta y 15 minutos lo sabés: medís 19,05 m de surco (si sembraste a 52,5 cm; 14,29 m a 70), contás las plantas y multiplicás por 1.000. Eso son tus plantas por hectárea.
> Repetilo en 4 o 5 puntos, lomas y bajos por separado, y fijate si nacieron parejas: cuando parte de las plantas nace unos 10 días tarde, el maíz pierde entre 6 y 9 % de rinde (Nafziger y col., 1991, citado por INTA).
> 📋 Armamos una planilla para llevar al lote, con el logro de implantación, dobles y fallas. Comentá PLANILLA y te la mandamos por DM.
> ¿Preferís que lo contemos juntos en tu lote? Escribinos 📲 wa.me/5492314530691
>
> #Henderseeds #Nidera #Maiz #Siembra2627 #Implantacion #Henderson #Daireaux #Bolivar

**Cuando alguien comenta PLANILLA** (responder en el día, idealmente en la primera hora):
1. Respuesta pública al comentario (ir rotando, para que no parezca automático):
   "¡Te la mandamos por DM! 📩" · "¡Listo, revisá tus mensajes!" · "¡Va por privado! 🌽"
2. Mensaje directo con la imagen `docs/recursos/out/planilla-conteo-plantas.jpg` (Instagram no acepta PDF):
   > ¡Hola, [nombre]! Acá va la planilla de conteo 📋 Si la querés en PDF para imprimir, escribinos al
   > WhatsApp 2314 53-0691 y te la pasamos. ¿Qué sembraste y a qué distancia entre surcos?
3. Según la respuesta: si tiene dudas con el número o el lote vino desparejo → ofrecer la recorrida
   ("¿Querés que pasemos y lo contamos juntos?"). Anotar cada pedido en `metricas.md`.
   Si los comentarios son muchos, se puede automatizar el DM con ManyChat (revisar plan y costo antes).

## Video 4 — ¿Te queda maíz tardío por definir?
Usa el copy de [posts/2026-W44/post-01-maiz-tardio.md](../posts/2026-W44/post-01-maiz-tardio.md).
Datos: marbetes Nidera 26/27, siembra tardía templada vs. índice ambiental (NS 7765 +324 kg/ha, 71 %,
165 comp. · NS 7925 +228, 59 %, 120 · NS 7921 CL +179, 60 %, 364). No se comparan entre sí.
Cierre del video y última línea del caption: "Pedí tu recomendación por DM".

## Pendientes comunes
- `[COMPLETAR: OK de Nidera para usar su logo y los nombres "Experiencia Nidera" / "Nidera Vuela"]`
- `[COMPLETAR: confirmar que los servicios del video 1 valen para todos los clientes]`
