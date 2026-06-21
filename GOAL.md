# Goal — Loop de auto-mejora

> Cada vez que arranca una sesión de Claude Code, leer este archivo PRIMERO
> (después de CLAUDE.md) y avanzar hacia el goal activo.

## Goal activo

**Tener la semana W27 completa (3 posts listos para publicar) antes del 27/06.**

### Criterios de "hecho"
- [ ] 3 posts en `posts/2026-W27/` según plantilla
- [ ] Cada post tiene: copy final, visual descripta, hashtags (max 8), CTA a WhatsApp
- [ ] Pasa el checklist de `brand/tono-voz.md`
- [ ] Ningún dato inventado — los `[COMPLETAR]` están listados
- [ ] `calendario.md` actualizado (💡 → ✍️ con links)
- [ ] Brief de pauta creado si algún post lo amerita
- [ ] Variedad de pilares respetada (cultivo + negocio + comunidad)

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

1. **W28 completa** (3 posts para la semana del 06/07)
2. **Primer reel** — guion según plantilla para uno de los posts existentes
3. **Carrusel maíz** — HTML single-file comparando los 3 maíces VIP3
4. **Brief de pauta consolidado** — al menos 2 posts pautados con brief en `meta-ads/`
5. **Revisar W25 y W26** — subir calidad de borradores existentes (self-review)
6. **Actualizar página web** — reflejar el contenido nuevo en `docs/index.html`

---

## Historial de goals cumplidos

| Goal | Fecha | Notas |
|------|-------|-------|
| Estructura del repo creada | W24 (junio 2026) | CLAUDE.md, plantillas, carpetas |
| GitHub Pages activo | W24 | Dashboard + infografía "cómo funciona" |
| W25 completa (4 posts) | W25 | 3 rotación + extra Día de la Bandera |
| W26 completa (3 posts) | W26 | Foco girasol + brief de pauta NS 1113 |

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
