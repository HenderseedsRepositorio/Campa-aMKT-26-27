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

> 🎬 **v2 educativa (19/10) — recomendada:** 5 escenas + cierre, ritmo tranquilo, 40 s →
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
