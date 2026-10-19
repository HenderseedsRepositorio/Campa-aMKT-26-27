"""Más videos para el kit de publicación (scripts/armar-kit.py): alternativas y reels ya hechos que
siguen vigentes en la semana del 20 al 31/10. Los videos viven en docs/placas/video/."""

_R1 = '''{primera} 🌽🌻
Con Experiencia Nidera, el equipo HenderSeeds te acompaña en cada etapa:
— Antes de sembrar: híbrido y densidad para cada zona del lote, con la base de ensayos de Nidera.
— Al sembrar: mapa de siembra variable para tu sembradora, con la recomendación Nidera o a medida.
— Con el cultivo nacido: control de calidad de siembra con dron (Nidera Vuela).
— Hasta la cosecha: recorridas e informe de cada visita.
¿Querés que recorramos tu lote? Mandanos un DM o escribinos por WhatsApp 📲 wa.me/5492314530691

#Henderseeds #Nidera #ExperienciaNidera #Maiz #Girasol #Henderson #Daireaux #Bolivar'''

BANCO = [
 dict(grupo='El video 1 con otro título', desc='Mismo video y mismo cierre ("Pedí tu recorrida por DM"), con otra pregunta de arranque. Sirven para pauta (probar cuál engancha más) o para volver a publicarlo más adelante.', items=[
   dict(id='b-v1', fmt='Reel · 31 s', video='2026-W43-video1-alt-te-acompana.mp4', portada='2026-W43-video1-alt-te-acompana-portada.jpg',
        titulo='¿Quién te acompaña toda la campaña?', obj='Arranca con los 4 pasos que se ordenan en la línea de tiempo.',
        cap=_R1.format(primera='¿Quién te acompaña toda la campaña?')),
   dict(id='b-v2', fmt='Reel · 31 s', video='2026-W43-video1-alt-conoce-tu-lote.mp4', portada='2026-W43-video1-alt-conoce-tu-lote-portada.jpg',
        titulo='¿Quién conoce tu lote tanto como vos?', obj='Pregunta y respuesta: "Nosotros. Antes, durante y después de sembrar."',
        cap=_R1.format(primera='¿Quién conoce tu lote tanto como vos?')),
   dict(id='b-v4', fmt='Reel corto · 23 s', video='2026-W43-video1-alt-corto.mp4', portada='2026-W43-video1-alt-corto-portada.jpg',
        titulo='¿Sembrás solo o con equipo?', obj='Versión corta, la más ágil para pauta.',
        cap=_R1.format(primera='¿Sembrás solo o con equipo?')),
   dict(id='b-h1', fmt='Historia · 26 s', video='2026-W43-video1-historia.mp4', portada='2026-W43-video1-historia-portada.jpg',
        titulo='¿Quién sigue de cerca tu lote? (historia)', obj='Versión para historias y Estados de WhatsApp, con lugar abajo para el sticker de enlace o de encuesta.',
        nota='Subila como historia y poné un sticker de enlace a WhatsApp (wa.me/5492314530691) donde dice "Tocá el enlace".'),
 ]),
 dict(grupo='Reels ya hechos que siguen vigentes', desc='Se armaron para el plan de septiembre y nunca se publicaron. Revisados el 19/10: datos del marbete correctos y sin precios. Ninguno repite lo de los 4 de la semana.', items=[
   dict(id='b-calc', fmt='Reel · 16 s', video='2026-W41-reel-calculadora.mp4', portada='2026-W41-reel-calculadora-portada.jpg',
        titulo='¿Qué te queda de cada hectárea?', obj='Herramientas: la barra de la calculadora de márgenes, sin números. Buen candidato para el sábado 31/10.',
        nota='El mismo día, historia con sticker de enlace a margen.henderseeds.com.',
        cap='''¿Qué te queda de cada hectárea? 🌽🌻

Alquiler, semilla e insumos, labores, cosecha, flete y comercialización: cada uno se lleva su parte y lo que sobra es tu margen. Si sube el alquiler o baja el precio, el reparto cambia.

Cargá tus números en la calculadora de márgenes y mirá cómo se compone tu hectárea, cultivo por cultivo.

📲 margen.henderseeds.com (link en la bio) · gratis y sin registro
📩 ¿La hacemos juntos? Mandanos tus números por DM o al WhatsApp 2314 53-0691.

#Henderseeds #MargenesAgricolas #Maiz2627 #Girasol2627 #Herramientas #Henderson #Daireaux #Bolivar'''),
   dict(id='b-calc-h', fmt='Historia · 9,5 s', video='2026-W41-calculadora-maiz-girasol-historia.mp4', portada='2026-W41-calculadora-maiz-girasol-historia-portada.jpg',
        titulo='¿Maíz o girasol? (historia)', obj='Historia con la pregunta del margen. El plan de 9 semanas la ponía el lunes 26/10.',
        nota='Sticker de enlace a margen.henderseeds.com.'),
   dict(id='b-wa', fmt='Reel · 14 s', video='2026-W40-reel-whatsapp-lote.mp4', portada='2026-W40-reel-whatsapp-lote-portada.jpg',
        titulo='¿Qué híbrido de girasol va en tu lote?', obj='Un chat de ejemplo y los 3 datos que hay que mandar. Sirve mientras quede girasol por sembrar (hasta el 15/11).',
        cap='''¿Qué híbrido de girasol va en tu lote? 🌻 Te lo decimos por WhatsApp.

Mandanos 3 datos:
1. Dónde está el lote
2. Qué tuvo antes
3. Qué problemas tuvo (enfermedades, malezas)

Te respondemos con qué híbrido va y por qué, con el marbete Nidera en la mano. Y si querés, la cotización en menos de 24 h.

📲 WhatsApp 2314 53-0691 · o por DM.

(El chat del video es un ejemplo.)

#Henderseeds #Nidera #Girasol2627 #GirasolCL #Siembra2627 #Henderson #Daireaux #Bolivar'''),
   dict(id='b-ph', fmt='Reel · 16 s', video='2026-W41-reel-girasol-phomopsis.mp4', portada='2026-W41-reel-girasol-phomopsis-portada.jpg',
        titulo='¿Rinde o sanidad?', obj='Girasol: NS 1113 CL para techo de rinde o NS 1115 / 1117 CL (Phomopsis 2) para el lote con historia de enfermedad. Para quien todavía no sembró.',
        nota='El mismo día, historia con encuesta: "¿Qué priorizás en tu girasol?" Rinde / Sanidad. Respondé por DM a cada voto.',
        cap='''¿Rinde o sanidad? Así se elige el girasol para cada lote. 🌻

Si buscás techo de rinde: NS 1113 CL, +2,11 qq/ha sobre el promedio de cada sitio de ensayo (74% de éxito, 225 comparaciones, Sur+Oeste).

Si el lote tiene historia de Phomopsis: priorizá sanidad. NS 1115 CL y NS 1117 CL tienen Phomopsis 2 en el marbete (escala 1 a 9, 1 = excelente): el mejor puntaje del portafolio.

📩 Contanos cómo es tu lote por DM o al WhatsApp 2314 53-0691 y te decimos cuál va.

#Henderseeds #Nidera #Girasol2627 #Phomopsis #GirasolCL #Henderson #Daireaux #Bolivar'''),
   dict(id='b-1113', fmt='Reel · 16 s', video='2026-W40-reel-ns1113.mp4', portada='2026-W40-reel-ns1113-portada.jpg',
        titulo='NS 1113 CL: ¿cuánto es en tu campo?', obj='Girasol: el dato del marbete llevado a la cuenta del productor (en girasol sí se muestran números de ensayo).',
        cap='''NS 1113 CL: +2,11 qq/ha por encima del promedio de cada ensayo. ¿Cuánto es en tu campo? 🌻

Es la diferencia de rinde contra el promedio de cada sitio de ensayo en la región Sur+Oeste: 225 comparaciones, 74% de éxito, diferencia significativa (marbete Nidera 26/27).

Hacé la cuenta: en 100 ha son 211 qq más, si se repite el promedio de los ensayos. No es promesa de rinde: el ambiente y el manejo mandan.

📩 ¿Te queda girasol por sembrar? Escribinos por DM o al WhatsApp 2314 53-0691. Cotización en menos de 24 h.

#Henderseeds #Nidera #NS1113CL #Girasol2627 #GirasolCL #Henderson #Daireaux #Bolivar'''),
   dict(id='b-7925', fmt='Reel · 14,5 s', video='2026-W41-reel-ns7925.mp4', portada='2026-W41-reel-ns7925-portada.jpg',
        titulo='Maíz para diciembre: NS 7925 VIPTERA3', obj='Tardío: la planta crece y aparecen sus fichas del marbete, sin números de ensayo. Se superpone con el video 4: usalo en otra semana o como anuncio.',
        cap='''Maíz para diciembre: NS 7925 VIPTERA3. 🌽

Lanzamiento Nidera 26/27, posicionado para siembras tardías:
• Viptera 3: control de lepidópteros.
• Spiroplasma 3: el mejor puntaje del portafolio de maíz (escala del marbete: 1 excelente, 9 deficiente).
• Roya 2 · Green Snap 2 · Quebrado 2.
• Madurez relativa 119, grano semidentado.

El híbrido suma; el monitoreo y el manejo siguen siendo la base.

📩 ¿Lo sembrás en diciembre? Escribinos por DM o al WhatsApp 2314 53-0691.

#Henderseeds #Nidera #Maiz2627 #MaizTardio #VIPTERA3 #NS7925 #Henderson #Daireaux'''),
   dict(id='b-aca', fmt='Reel corto · 10 s', video='2026-W40-somos-de-aca-reel.mp4', portada='2026-W40-somos-de-aca-reel-portada.jpg',
        titulo='Somos de acá', obj='Institucional: el mapa de Henderson, Daireaux y Bolívar. Sirve para historias o para presentarnos en la pauta.',
        cap='''Somos de acá. 📍

Henderson, Daireaux y Bolívar: recorremos los lotes de la zona, posicionamos cada híbrido según el ambiente y después de la siembra volvemos a ver cómo quedó la implantación.

Distribuidor oficial RED.IN de Nidera Semillas. Más de 100 productores y más de 30.000 hectáreas bajo plan en la 25/26. Cotización en menos de 24 horas.

📩 Pasá por la oficina en Henderson o mandanos un DM.

#Henderseeds #Nidera #REDIN #Henderson #Daireaux #Bolivar #OesteBonaerense #Agro'''),
 ]),
]
