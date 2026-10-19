# Análisis rápido de las fotos de dron (19/10/2026)

> Prueba hecha por Claude sobre 2 fotos cenitales de maíz (V2–V3 aprox.) que mandó Henderseeds
> (`produccion/sintetico/img/dron/dron-01.jpg` y `dron-02.jpg`). **No reemplaza al informe de
> Nidera Vuela**: sirve para ver hasta dónde se puede llegar y para los anillos del reel v3.

## Método (reproducible, solo numpy + PIL)
1. Índice de exceso de verde (ExG = 2g − r − b) → máscara de pixeles de planta.
2. Dilatación chica + componentes conexas → una mancha por planta → centroides.
3. Surcos: picos del perfil horizontal de la máscara. Distancia entre surcos ≈ **47 px** (zona central).
4. Plantas asignadas al surco más cercano → distancias entre plantas vecinas en cada surco.
5. Densidad: `pl/ha = 10.000 / (distancia entre surcos [m] × distancia media entre plantas [m])`.
   La escala sale del propio surco, así que **solo hay que saber a qué distancia se sembró**.

## Resultados (franja central de cada foto)
| | Foto 1 | Foto 2 |
|---|---|---|
| Plantas detectadas en la franja | 351 | 288 |
| Distancia entre surcos | 47 px | 47 px |
| CV de distancia entre plantas | 45 % | 58 % |
| Huecos > 1,8 × la mediana ("fallas") | 9,5 % | 16,5 % |
| **Densidad si el surco es a 52,5 cm** | **≈ 46.600 pl/ha** | **≈ 44.200 pl/ha** |
| Densidad si el surco es a 70 cm | ≈ 26.200 pl/ha | ≈ 24.900 pl/ha |

## Por qué NO publicar estos números
- **Sombras:** en las franjas sombreadas el verde se apaga y se pierden plantas → la densidad
  sale **más baja** y el CV y las "fallas" **más altos** que la realidad.
- **Dobles:** dos plantas muy pegadas se funden en una mancha (da 0 % de dobles, poco creíble).
- **Perspectiva:** arriba de la foto los surcos se ven más juntos (34 px vs 47 px): la foto no es
  100 % cenital. Por eso se midió solo la franja central.
- Falta confirmar la **distancia entre surcos** real del lote.

## Para que sirva de verdad
- `[COMPLETAR: distancia entre surcos del lote de las fotos]`
- `[COMPLETAR: plantas/ha, CV y fallas/dobles del informe Nidera Vuela de ese lote]` → comparar
  con esta estimación y, con números reales, cargarlos en `METRICAS` del reel v3.
- Fotos ideales para medir: dron bien cenital, mediodía (sin sombras largas), misma altura en todos
  los puntos, una foto por ambiente.
