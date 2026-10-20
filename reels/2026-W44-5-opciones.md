# 5 opciones de reel para elegir (W44 en adelante)

Pedido de Henderseeds (20/10): reels **distintos de verdad** para elegir, no el mismo video con otro
título. Cada opción tiene su propio mensaje, formato y dibujo. Se miran y se eligen en el
[kit](https://henderseedsrepositorio.github.io/Campa-aMKT-26-27/kit/) (casilla "Me la quedo" y botón
"Copiar mi elección"). Las captions están en `scripts/kit_banco.py`.

| # | Reel | Formato y estilo | Pilar | Dur. | Archivo |
|---|------|------------------|-------|------|---------|
| 1 | ¿Verdadero o falso? | Juego: tarjeta, botones V/F y sello que golpea; fondo crema con rayos | Técnica | 24 s | `produccion/sintetico/reel-op1-verdadero-falso.html` |
| 2 | ¿Sembrás maíz tardío? Mirá la chicharrita | Lupa sobre una chicharrita dibujada, trampa amarilla y escala 1–9 del marbete; navy | Maíz tardío | 24 s | `produccion/sintetico/reel-op2-chicharrita.html` |
| 3 | ¿Cuántas semillas por metro? | Sembradora de costado: caen semillas sobre una regla de 1 m y se arma la cuenta; lámina técnica | Técnica (para guardar) | 24 s | `produccion/sintetico/reel-op3-semillas-por-metro.html` |
| 4 | ¿Pesos o dólares? | Balanza de grabado que se inclina con tasa, plazo y devaluación; crema | Finanzas / herramientas | 22 s | `produccion/sintetico/reel-op4-pesos-o-dolares.html` |
| 5 | ¿Y si graniza después de sembrar? | Tormenta con granizo sobre las plantitas, se abre el cielo y 3 pasos | Oferta (seguro de resiembra) | 25 s | `produccion/sintetico/reel-op5-granizo.html` |

Render: `node scripts/render-reel.mjs <archivo>` → `produccion/sintetico/out/`. Los MP4 finales (CRF 21)
están en `docs/placas/video/2026-W44-opcion-*.mp4`.

## Fuentes de cada dato
- **Opción 1.** Planta atrasada: Nafziger, Carter y Graham (1991), *Crop Science* 31: 811–815, citado
  por INTA (6–9 % menos de rinde con ~10 días de atraso de parte de las plantas). Girasol en el oeste:
  marbetes Nidera 26/27, óptima 15/10–15/11, límite 20/11. Densidad por ambiente: criterio de
  recomendación por ambiente (sin cifras).
- **Opción 2.** NS 7925 VIPTERA3, Spiroplasma 3, el mejor del portafolio (el resto, 4 a 6), escala 1
  excelente – 9 deficiente, lanzamiento 26/27 para tardía: marbete oficial Nidera (`contexto/productos-26-27.md`).
  La chicharrita (*Dalbulus maidis*) como vector del Spiroplasma (achaparramiento): dato agronómico general.
  Sin números de ensayo de maíz (regla del 25/09).
- **Opción 3.** Aritmética: semillas/m = plantas/ha ÷ logro × distancia (m) ÷ 10.000.
  50.000 ÷ 0,9 × 0,525 ÷ 10.000 = 2,92; 70.000 ÷ 0,9 × 0,525 ÷ 10.000 = 4,08. Ejemplos rotulados, no recomendación.
- **Opción 4.** Herramienta pesos vs. dólares (`contexto/herramientas.md`, punto 2). Sin tasas, plazos,
  montos ni condiciones de financiación.
- **Opción 5.** Punto de crecimiento del maíz bajo tierra hasta ~V5–V6: R. L. Nielsen, Purdue University
  (Corny News, daño por granizo en maíz joven). Seguro de resiembra de Nidera ante granizo o
  encharcamiento: paso 4 del Plan de Campaña (CLAUDE.md), sin condiciones.

## Notas
- Ninguna muestra personas ni el dron como pieza suelta. Cierre de todas: "Mandanos un DM" + WhatsApp.
- La opción 4 lleva el mismo día una historia con enlace a la herramienta.
- Cuando elijas, la sumo al calendario con fecha y la paso al kit como publicación de la semana.
