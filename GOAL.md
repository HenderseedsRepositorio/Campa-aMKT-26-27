# Goal — Loop de auto-mejora

> Cada vez que arranca una sesión de Claude Code, leer este archivo PRIMERO
> (después de CLAUDE.md) y avanzar hacia el goal activo.

## Goal activo

**W28: PUBLICAR (no redactar) — 2 piezas en la calle y el sistema de medición arrancado, antes del 12/07.**

> Cambio de doctrina tras la crítica de estrategia (08/07): el cuello de botella
> no es producir, es publicar. En 5 semanas se redactaron ~12 piezas y se
> publicaron 3. Regla nueva: **publicado o no existe.**

### Criterios de "hecho"
- [ ] 📤 Publicar NS 1113 CL (post + placa **ya listos**) en feed + Estados de WhatsApp
- [ ] 📤 Publicar 2ª pieza: "Precampaña vs. esperar" (borrador W27, [placa ya hecha](docs/placas/w27-post-02-finanzas.html))
- [ ] Cargar métricas reales de W27 en `metricas.md` (post maíz + reel pautado)
- [ ] Conseguir de Nidera fechas de escalones/cierre → cargar en `contexto/calendario-comercial.md`
- [ ] Subir las primeras fotos reales a `docs/assets/fotos/` (mínimo 5)
- [x] Post NS 1113 CL redactado con fuentes independientes (CREA)
- [x] `calendario.md` sincerado (♻️/🗄️) y pasado al modelo "1 idea semanal"

### Congelamiento de infraestructura (hasta septiembre)
No crear páginas, sistemas ni artefactos nuevos. La infraestructura ya alcanza:
las sesiones producen contenido, marcas de publicado y métricas cargadas.

---

## Loop de auto-mejora (correr en cada sesión)

Cada vez que entro al proyecto, sigo este ciclo:

### 1. Diagnosticar
- ¿Qué semana es hoy? ¿Qué debería estar listo y no lo está?
- ¿Hay posts en borrador que se pueden mejorar?
- ¿El calendario tiene huecos sin cubrir en las próximas 2 semanas?

### 2. Producir
- Avanzar el goal activo (generar lo que falta).
- Si el goal ya está cumplido → pasar al siguiente de la cola.

### 3. Revisar (self-review)
- [ ] ¿El tono es rioplatense, técnico pero cercano? (no marketing genérico)
- [ ] ¿Hay variedad? No repetir pilar ni enfoque de las últimas 2 semanas.
- [ ] ¿Los datos de producto vienen de `contexto/productos-26-27.md` o marbetes?
- [ ] ¿El CTA lleva a WhatsApp (wa.me/5492314530691)?
- [ ] ¿Se respeta la regla de NO publicar precios/descuentos/condiciones?
- [ ] ¿Los hashtags son <= 8 y relevantes?
- [ ] ¿La pieza visual está descripta con suficiente detalle para diseñar?

### 4. Corregir
- Si algo no pasa el review → corregirlo en el mismo ciclo.
- Si falta un dato real → dejarlo como `[COMPLETAR: qué falta]`.

### 5. Registrar
- Actualizar `calendario.md`.
- Commitear con mensaje descriptivo.
- Actualizar este archivo: marcar checks del goal, mover goals cumplidos al historial.

---

## Cola de goals (próximos)

1. **W29 según modelo nuevo** — idea "hacé tus números": placa calculadora (♻️ W25) + pieza humana equipo (♻️ W27-03 con foto real)
2. **Banco de fotos reales** — 10+ fotos en `docs/assets/fotos/` (lotes, recorridas, equipo)
3. **Definir el número norte en `metricas.md`** — X conversaciones nuevas/semana (decidirlo con datos de W27–W28)
4. **Brief de pauta para NS 1113 v2** — si el orgánico funciona, pautarlo (reutilizar base del brief W26)
5. **Primer caso real con productor** — pedir permiso + foto a un cliente para historia (1/mes)

---

## Historial de goals cumplidos

| Goal | Fecha | Notas |
|------|-------|-------|
| Estructura del repo creada | W24 (junio 2026) | CLAUDE.md, plantillas, carpetas |
| GitHub Pages activo | W24 | Dashboard + infografía "cómo funciona" |
| W25 completa (4 posts) | W25 | 3 rotación + extra Día de la Bandera |
| W26 completa (3 posts) | W26 | Foco girasol + brief de pauta NS 1113 |
| W27 completa (3 posts + reel) | W27 | Maíz NS 7765 publicado 25/06 · reel pautado 26/06 |
| Página Portafolio Nidera co-brand | W28 | `docs/nidera/` — 13 híbridos + marbetes + links oficiales |
| Sistema de métricas creado | W28 | `metricas.md` — carga semanal, pendiente primer registro |

---

## Estándar visual (IMPORTANTE — seguir siempre)

Las piezas se hacen en **HTML single-file**, NO en Canva (Canva no respeta logo ni estilo).

- **Ubicación:** `docs/placas/AAAA-WXX-tema.html` (dentro de `docs/` para que GitHub Pages las sirva).
- **Estilo:** calcar el carrusel `carruseles/2026-W26-elegir-girasol-por-ambiente.html`:
  fondo navy `#0A0F1B`, grilla naranja sutil, barra naranja superior 8px, Archivo Black
  para títulos, DM Mono para datos/etiquetas, dato hero grande en naranja/amarillo.
- **Logos REALES** (no recreados con texto): están en `docs/assets/`
  - `logo-henderseeds-white.png` → placas navy (fondo oscuro)
  - `logo-henderseeds-navy.png` → placas crema (fondo claro)
  - `logo-nidera.png` → sello RED.IN en el footer
- **Linkear** cada placa desde el dashboard (`docs/index.html`) con "Ver placa".
- El productor las ve online en GitHub Pages y las screenshotea a 1080×1350.

**Regla de contacto (Instagram):** el CTA primario es **"Mandanos un DM"** (ícono
avioncito) — es la acción nativa sin fricción. El **WhatsApp va como info de última**,
chico y abajo, con el ícono SVG real verde (`#25D366`). Nunca el número grande/protagonista.

## Cómo usar esto

**Vos (usuario):** abrís sesión y decís "seguí", "avanzá", o algo más específico.
**Claude:** lee GOAL.md → diagnostica → produce → revisa → corrige → registra → reporta qué hizo y qué queda.

Si querés cambiar el goal: editá la sección "Goal activo" o decime y lo actualizo.
