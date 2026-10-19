# Video 1 — Voz en off y clip real ("¿Quién sigue de cerca tu lote?")

Las dos mejoras que más impacto suman al video 1 y que necesitan material del equipo.
El video ya funciona sin ellas: si llegan antes del martes salen en la versión orgánica;
si llegan después, se usa la versión mejorada para la pauta.

## 1. Voz en off (≈ 25 s, la lee alguien del equipo)

Guion medido al tiempo de cada etapa del video (unas 2,5 palabras por segundo, ritmo de charla).
Tono: como cuando le explicás a un productor en la camioneta, sin "voz de locutor".

| Tiempo | En pantalla | Texto a leer |
|--------|-------------|--------------|
| 0,3 – 3,5 s | ¿Quién sigue de cerca tu lote? | **¿Quién sigue de cerca tu lote?** |
| 3,9 – 9,0 s | 01 · Antes de sembrar | **Antes de sembrar, elegimos híbrido y densidad para cada ambiente del lote.** |
| 9,3 – 14,2 s | 02 · Al sembrar | **Al sembrar, armamos el mapa de siembra variable para tu sembradora.** |
| 14,5 – 21,0 s | 03 · Con el cultivo nacido | **Con el cultivo nacido, volamos el lote con dron y medimos cómo quedó la siembra.** |
| 21,3 – 26,6 s | 04 · Hasta la cosecha | **Y hasta la cosecha, recorremos el lote y te mandamos un informe de cada visita.** |
| 26,9 – 30,5 s | Cierre | **Equipo HenderSeeds, Experiencia Nidera. Pedí tu recorrida por DM.** |

**Cómo grabarla (5 minutos):**
- Lugar callado y sin eco: la camioneta parada, con el motor apagado y las ventanillas
  cerradas, es una cabina de grabación muy buena.
- Celular a un palmo de la boca, con la app de grabadora de voz (no nota de voz de WhatsApp:
  comprime mucho).
- Leer cada frase **por separado**, con 2 segundos de silencio entre una y otra. Hacer 2 tomas completas.
- Mandar el archivo por WhatsApp **como documento** o por Drive.

Con el audio, se reacomodan los tiempos de cada etapa a la voz (el video se genera por código,
así que se ajusta exacto) y se mezcla con música baja. En Instagram se sube igual que ahora.

## 2. Clip real en el cierre (3–8 s de video)

**Ojo, regla del equipo (07/10): "nadie aparece en cámara".** Por eso las tomas van sin caras ni
personas de cuerpo entero. Si esa regla cambió, la mejor toma sigue siendo alguien del equipo
caminando el surco de espaldas (toma A8).

**Tomas que respetan la regla (con 1 alcanza):**
1. **Manos contando plantas** con la cinta estirada en el surco, celular al ras del suelo (toma A7).
2. **El dron despegando** en la cabecera del lote, o una pasada en vuelo (B2).
3. **La sembradora trabajando**, de costado, cruzando el cuadro (A1).

Detalle de cada toma en [produccion/guia-foto-video-siembra.md](../produccion/guia-foto-video-siembra.md).
Celular **vertical**, 30 cuadros por segundo, sol a la espalda de quien filma. Sin marcas de la competencia.

**Qué hace el video con el clip:** al terminar la etapa 04, la toma real ocupa toda la pantalla
2,4 s con el rótulo "Equipo HenderSeeds · a campo" (se puede cambiar según la toma); después el cierre (logos, "Lo seguimos de
cerca.", botón de DM) aparece encima del clip oscurecido. El video pasa de 31 a 33 s.

**Pasos (cuando llegue el archivo):**
```bash
# 1) cortar y pasar a cuadros (inicio y duración en segundos; recorta al centro si vino horizontal)
scripts/preparar-clip.sh ruta/al/clip.mp4 1.5 6
# 2) render con el clip (el comando exacto lo imprime el paso 1)
node scripts/render-reel.mjs produccion/sintetico/reel-experiencia-v5.html \
  produccion/sintetico/out/video1-con-clip.mp4 --v 3 --q "clip=img/clip&clipn=180"
```
Probado con un clip de prueba armado con la foto de dron (no se publica).

## Estado
- [ ] Voz en off grabada → `[COMPLETAR: quién la graba]`
- [ ] Clip filmado (A7, B2 o A1) → `[COMPLETAR: quién lo filma y en qué lote]`
- [ ] Versión con voz y clip renderizada
