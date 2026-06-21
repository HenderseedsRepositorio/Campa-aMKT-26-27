# Skill: Generar contenido semanal Henderseeds

## Qué es esta skill
Guía maestra paso a paso para generar lotes de contenido de marketing digital
para Henderseeds (Instagram/Facebook). Cubre desde la lectura de contexto hasta
la entrega del lote completo con posts, carruseles, reels y briefs de pauta.

---

## PASO 1 — Leer antes de escribir (obligatorio, no saltear)

Leer en este orden:
1. `CLAUDE.md` — reglas duras, estructura, checklist
2. `brand/identidad.md` — paleta, tipografías, estilo visual
3. `brand/tono-voz.md` — voz de marca, ejemplos, qué no decir
4. `contexto/productos-26-27.md` — fichas de los 13 híbridos + los 6 prioritarios
5. `contexto/herramientas.md` — calculadora de márgenes, suite financiera
6. `contexto/zona-y-audiencia.md` — perfil del productor, audiencias Meta
7. `contexto/calendario-comercial.md` — hitos y regla de no publicar precios
8. `contexto/empresa.md` — quiénes somos, contacto, cifras
9. `calendario.md` — qué se publicó, qué toca esta semana

## PASO 2 — Determinar la semana y qué toca

1. Identificar la semana ISO actual (formato `AAAA-Www`).
2. Revisar `calendario.md`:
   - ¿Qué se publicó en las últimas 2 semanas? No repetir pilar.
   - ¿Qué está propuesto (💡) para esta semana?
   - ¿Hay hito de `calendario-comercial.md` que pise la rotación?
3. Definir el lote: **3 posts por semana** siguiendo la rotación:
   - **Post 1 — Cultivo:** maíz o girasol (alternar semana a semana).
     Rotar entre los 6 prioritarios: NS 7765, NS 7621, NS 7921 (maíz) /
     NS 1113, NS 1115, NS 1117 (girasol).
   - **Post 2 — Negocio:** herramientas (calculadora, suite financiera) o
     márgenes/finanzas de campaña.
   - **Post 3 — Comunidad:** técnico (manejo, densidades, dato agronómico) o
     institucional (equipo, zona, RED.IN, historia con productor).

## PASO 3 — Generar cada post

Para cada post, seguir `posts/_plantilla-post.md`. Producir:

### A) Copy (Instagram/Facebook)
- **Línea 1 = gancho** (pregunta, dato fuerte o afirmación que frena el scroll).
- **Cuerpo:** UNA idea en 2-4 líneas. Aire entre párrafos. Voseo rioplatense.
- **CTA:** siempre cerrar con acción concreta a WhatsApp (wa.me/5492314530691).
- **Hashtags:** máximo 8, al final. Mezclar marca + cultivo + zona.
  Base: #Henderseeds #Nidera + cultivo + zona (Henderson/Daireaux/Bolivar).

### B) Pieza visual (descripción precisa)
- Describir composición, textos que van EN la pieza, dato destacado,
  foto de referencia, colores exactos de `brand/identidad.md`.
- Fondo navy oscuro (`#0A0F1B`) por defecto, estilo agro-tech.
- Logo Henderseeds arriba derecha + sello RED.IN Nidera abajo.
- Cifras grandes en DM Mono o Space Grotesk bold.
- Un solo mensaje por placa. Limpio.

### C) Validación de datos
- Todo dato numérico (rinde, kg/ha, qq/ha, % éxito) DEBE venir de
  `contexto/productos-26-27.md` con fuente "marbete oficial Nidera".
- Si falta un dato: poner `[COMPLETAR: qué falta]` y listarlo al final.
- **NUNCA inventar rindes, precios, descuentos ni condiciones comerciales.**
- **NUNCA publicar % de descuento ni precios.** Hablar de "precampaña" en general.

## PASO 4 — Formatos especiales (si corresponden)

### Carrusel
- HTML single-file 1080x1350 en `carruseles/`.
- Usar como referencia: `brand/referencias/Primer post precampaña...html`.
- Variables CSS del carrusel de referencia: `--navy`, `--orange`, `--mono`, `--sans`, `--arch`.
- Una sección por slide. Numerador "01 / 05".
- Screenshoteable sin scroll.
- Si hay MCP de Canva conectado, armar directo en Canva y poner el link.

### Reel
- Guion en `reels/` según `reels/_plantilla-reel.md`.
- Hook en los primeros 3 segundos.
- Subtítulos siempre (se mira sin audio).
- Duración ideal: 30-60 segundos.

### Brief de pauta
- Si el post va con pauta → crear brief en `meta-ads/briefs/AAAA-Www-tema.md`.
- Seguir `meta-ads/_plantilla-brief.md`.
- Audiencia base: geo Henderson+Daireaux+Bolívar 40-60km, 25-60 años,
  intereses agro. Objetivo según tipo de post (ver `contexto/zona-y-audiencia.md`).

## PASO 5 — Guardar y actualizar calendario

1. Crear carpeta `posts/AAAA-Www/` si no existe.
2. Nombrar archivos: `post-01-tema.md`, `post-02-tema.md`, `post-03-tema.md`.
3. **Actualizar `calendario.md`**: cambiar 💡 a ✍️, linkear archivo del post.
4. Si hay carrusel o reel, linkear desde el post.
5. Si hay brief de pauta, linkear desde el post.

## PASO 6 — Checklist final (no entregar sin pasar esto)

- [ ] ¿Leí todos los archivos de `brand/` y `contexto/`?
- [ ] ¿Cada post tiene copy final, pieza visual descripta, hashtags (max 8) y CTA a WhatsApp?
- [ ] ¿Ningún dato inventado? ¿Los `[COMPLETAR]` están listados?
- [ ] ¿No publiqué precios, descuentos ni condiciones comerciales?
- [ ] ¿Actualicé `calendario.md`?
- [ ] ¿Creé el brief de pauta si corresponde?
- [ ] ¿Pasa el checklist de `brand/tono-voz.md`? (gancho, una idea, voseo, fuente, CTA)
- [ ] ¿No repetí pilar de las últimas 2 semanas?
- [ ] ¿Los híbridos mencionados son de los 6 prioritarios?

## PASO 7 — Resumen de entrega

Al terminar, dar un resumen con:
1. Qué posts se generaron (título + pilar + formato).
2. Lista de `[COMPLETAR]` pendientes (si los hay).
3. Sugerencia para la semana siguiente (qué pilar toca, qué híbrido rotar).
4. Commit y push al branch.

---

## Reglas que NUNCA se rompen

1. **Voseo rioplatense.** "Sembrás", "calculá", "escribinos". Nunca tuteo ni ustedeo.
2. **Nunca prometer rindes sin fuente.** Citar marbete Nidera o ensayo con localidad/año.
3. **Nunca publicar precios/descuentos/condiciones.** La venta se cierra por WhatsApp o cara a cara.
4. **Nunca marketing genérico.** Prohibido: "imperdible", "no te lo pierdas", "calidad premium", "líder", "revolucionario".
5. **Máximo 8 hashtags.**
6. **Paleta navy + naranja.** Fondo oscuro por defecto. Naranja para UN acento por pieza.
7. **CTA siempre a WhatsApp** (wa.me/5492314530691).
8. **Datos > adjetivos.** "+392 kg/ha en 191 comparaciones" vence a "excelente rendimiento".

---

## Híbridos prioritarios (referencia rápida)

### Maíz
| Híbrido | Para qué | Dato top |
|---------|----------|----------|
| NS 7765 VIP3 | Top del portafolio, temprana y tardía | +392 kg/ha** (74% éxito) |
| NS 7621 VIP3 | Performance pura en temprana | +290 kg/ha** (67% éxito) |
| NS 7921 VIP3 CL | Versátil + 3 herbicidas, toda fecha | +179 kg/ha** tardía |

### Girasol
| Híbrido | Para qué | Dato top Sur+Oeste |
|---------|----------|--------------------|
| NS 1113 CL | Techo de rinde y aceite | +2,11 qq/ha** (74% éxito) |
| NS 1115 CL | Mejor sanidad (Phomopsis 2) | +1,64 qq/ha** (69% éxito) |
| NS 1117 CL | Máximo rinde + Phomopsis | +1,75 qq/ha** (67% éxito) |
