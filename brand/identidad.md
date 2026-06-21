# Identidad visual — HenderSeeds

> Paleta y tipografías extraídas del sitio web (henderseeds.com) y del
> carrusel de precampaña 26/27. Logos originales en `brand/referencias/`.

## Paleta
| Uso | Color | Hex |
|-----|-------|-----|
| Fondo oscuro (modo dark, placas) | Navy profundo | `#0A0F1B` |
| Navy principal (logo, títulos) | Navy | `#0D2D5E` |
| Navy oscuro (gradientes, paneles) | Navy dark | `#091E3E` |
| Navy medio (acentos secundarios) | Navy mid | `#1A4A8A` |
| Acento (CTA, datos clave, highlights) | Naranja/ámbar | `#F5A623` |
| Amarillo alternativo (subtítulos) | Yellow | `#F59E0B` |
| Fondo claro (modo light) | Crema | `#F6F4EE` |
| Panel claro (modo light) | Blanco | `#FFFFFF` |
| Panel claro secundario (light) | Arena | `#EFEAE0` |
| Texto principal (modo light) | Casi negro | `#15181E` |
| Texto secundario (light) | Gris | `#4A5264` |
| Texto secundario (dark) | Gris claro | `#8FA0BE` |
| Texto principal (dark) | Blanco azulado | `#E8EEF7` |
| WhatsApp (botón flotante) | Verde WA | `#25D366` |

Reglas:
- Navy + naranja/ámbar es la combinación principal en TODA la comunicación.
- El naranja `#F5A623` se usa para UNA cosa por pieza: el dato clave O el CTA, no ambos.
- Nunca texto naranja sobre navy en cuerpos largos (solo títulos cortos o cifras grandes).
- El fondo por defecto es **oscuro** (`#0A0F1B`), estilo agro-tech. Las placas para
  Instagram siguen esa línea: fondo navy, textos blancos, acentos naranja.
- Para variantes claras: fondo crema `#F6F4EE`, textos casi negro, acentos naranja.

## Tipografías (confirmadas desde web y carrusel)
| Uso | Fuente | Fallback |
|-----|--------|----------|
| Títulos principales (hero, slides) | **Archivo Black** | sans-serif |
| Títulos web (secciones, cards) | **Space Grotesk** 600/700 | sans-serif |
| Cuerpo de texto | **DM Sans** 400/500/600/700 | sans-serif |
| Etiquetas, datos, código | **DM Mono** 400/500 | monospace |

Reglas:
- Títulos en Archivo Black o Space Grotesk, siempre BOLD, tracking apretado (-1px a -2px).
- Cuerpo en DM Sans, limpio y legible.
- Cifras grandes: el número siempre más grande que su unidad (ej: **+392** kg/ha).
- Etiquetas y tags en DM Mono, uppercase, letter-spacing amplio.

## Logo
- **Isotipo:** espiga dorada/ámbar a la izquierda.
- **Logotipo:** "Hender" + "Seeds" en navy (`#0D2D5E`) sobre fondo claro,
  o blanco sobre fondo oscuro.
- Versiones disponibles en `brand/referencias/`:
  - `00-LOGO HENDERSEEDS TRANSPARENTE.png` — blanco sobre transparente (para fondos oscuros)
  - `LogoPowerBI.png` — navy sobre fondo blanco (alta resolución)
  - `logo black fondo.png` — blanco sobre fondo negro
- Logo Nidera: `LogoNideraSemillas.png` — "N" amarilla + texto "NIDERA SEMILLAS"
- Isotipo Nidera solo: `logo-n.png` — la "N" amarilla
- Siempre con aire alrededor; nunca deformado ni con sombras.
- En piezas con foto: logo en esquina superior o inferior derecha.
- Acompañar con sello Nidera + "RED.IN" cuando sea pertinente.

## Formatos de pieza
| Pieza | Tamaño | Notas |
|-------|--------|-------|
| Post feed (placa simple) | 1080×1350 (4:5) | Un mensaje por placa |
| Carrusel | 1080×1350 por slide, 5 slides típico | Un dato por slide, numerador "01 / 05" |
| Historia | 1080×1920 (9:16) | Texto en zona segura central |
| Reel | 1080×1920 (9:16) | Subtítulos siempre (se mira sin audio) |

## Estilo visual (extraído del carrusel y la web)
- **Fondo navy oscuro** con grilla sutil de líneas naranjas tenues (`rgba(245,166,35,0.05)`).
- **Estilo "agro-tech"**: mezcla de lenguaje visual tecnológico (monospace, etiquetas tipo terminal) con contenido agronómico.
- Foto real de lotes/campo de la zona > foto de stock. Si es stock, que parezca oeste bonaerense.
- Placas limpias: máximo un titular + un dato + un CTA.
- Los datos numéricos van GRANDES con DM Mono o Space Grotesk bold.
- Cards con borde sutil (`rgba(255,255,255,0.09)`), border-radius 12-14px.
- Indicadores tipo "led" naranja animado para mostrar estado activo (ej: "PRECAMPAÑA 26/27").
- Gráficos simples: barras horizontales con gradiente naranja, nunca tortas con 6 categorías.
- Botones primarios: fondo naranja `#F5A623`, texto negro `#0a0a0a`, border-radius 8px.
- Bordes con líneas dashed `var(--border-strong)` para separar secciones.
