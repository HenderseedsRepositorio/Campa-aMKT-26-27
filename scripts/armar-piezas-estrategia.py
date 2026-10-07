#!/usr/bin/env python3
"""
Placas de la estrategia (docs/estrategia/piezas/): genera el HTML de cada opción y la galería.

Cada opción sale en dos formatos dentro del mismo HTML:
  - feed     1080x1350 (4:5)   -> Instagram / Facebook
  - historia 1080x1920 (9:16)  -> historias de Instagram y Estados de WhatsApp (diseño propio, no la placa achicada)

Los textos están UNA sola vez acá arriba (PASOS, HIBRIDOS, COPYS): si cambia una condición, se cambia acá
y se regeneran todas.

Uso:
  python3 scripts/armar-piezas-estrategia.py          # escribe HTML + piezas.css + index.html
  node scripts/render-piezas-estrategia.mjs            # HTML -> JPG (docs/estrategia/piezas/img/)

Reglas que respeta (CLAUDE.md): sin precios ni plazos de financiación, sin números de ensayo en maíz,
el drone solo como paso 5 de la oferta, nadie en cámara, CTA a la conversación privada.
"""
from pathlib import Path
import html

RAIZ = Path(__file__).resolve().parent.parent
DIR = RAIZ / "docs/estrategia/piezas"

# --------------------------------------------------------------------------------------------------
# Contenido (fuente única)
# --------------------------------------------------------------------------------------------------
PASOS = [
    ("Diagnóstico", "Tu lote y tu planteo."),
    ("Recomendación Asista", "Híbrido por ambiente; siembra variable, opcional."),
    ("Financiación", "A cosecha o de contado; tarjetas agro en pesos o dólares."),
    ("Seguro de resiembra", "De Nidera, ante granizo o encharcamiento."),
    ("Vuelo de drone", "La calidad de siembra, vista desde arriba."),
    ("Informe de visita", "Lo que vimos y recomendamos, por escrito."),
]
MOMENTOS = [("Antes de sembrar", [0, 1, 2]), ("Al sembrar", [3, 4]), ("Después", [5])]

H7624 = dict(nm="NS 7624", ciclo="Corto · MR 117", fecha="Siembras tardías", san="Quebrado 2 · Roya 2")
H7921 = dict(nm="NS 7921", ciclo="MR 118", fecha="Temprana y tardía", san="Quebrado 2")
HERB = ["Glifosato", "Glufosinato", "Imidazolinonas"]
FUENTE_CL = "Marbetes Nidera 26/27. Usá solo herbicidas identificados como CLEARFIELD® (marca registrada de BASF)."

CTA_PLAN = "¿Armamos el tuyo? Mandanos un DM."
CTA_CL = "¿Tenés un lote así? Mandanos un DM."

COPY_PLAN = """Tu campaña, con un plan. 📋

Así trabajamos cada campaña con los productores de Henderson, Daireaux y Bolívar:

1. Diagnóstico de tu lote y tu planteo.
2. Recomendación Asista: híbrido Nidera por ambiente y, si querés, siembra variable.
3. Financiación a cosecha o de contado, con tarjetas agro en pesos o en dólares.
4. Seguro de resiembra de Nidera, ante granizo o encharcamiento.
5. Vuelo de drone para ver la calidad de siembra.
6. Informe de visita: lo que vimos y lo que recomendamos, por escrito.

Es el Plan de Campaña HenderSeeds.
📩 ¿Armamos el tuyo? Mandanos un DM.

#Henderseeds #PlanDeCampaña #Nidera #REDIN #Henderson #Daireaux #Bolivar #Agro"""

COPY_CL = """¿Tu lote tardío viene con malezas complicadas? 🌽

Los dos VIPTERA3 CL del portafolio Nidera traen control de lepidópteros y tres herramientas herbicidas: glifosato, glufosinato e imidazolinonas.

→ NS 7624 VIPTERA3 CL: ciclo corto (MR 117), pensado para siembras tardías.
→ NS 7921 VIPTERA3 CL: MR 118, va en temprana y en tardía.

Recordá: con Clearfield, solo herbicidas identificados como CLEARFIELD®.
📩 ¿Tenés un lote así? Mandanos un DM y lo vemos.

#Henderseeds #Nidera #Maiz2627 #MaizTardio #Clearfield #Malezas #Henderson #Bolivar"""

# --------------------------------------------------------------------------------------------------
# Temas
# --------------------------------------------------------------------------------------------------
TEMAS = {
    "navy": dict(cls="", logo="logo-hs-blanco-hd.png", nidera="logo-nidera-negativo.png", nombre="Navy"),
    "crema": dict(cls="light", logo="logo-hs-navy-hd.png", nidera="logo-nidera-positivo.png", nombre="Crema"),
    "ambar": dict(cls="amb", logo="logo-hs-navy-hd.png", nidera="logo-nidera-negativo.png", nombre="Ámbar"),
}

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="hs-dm" viewBox="0 0 24 24"><path d="M22 2 11 13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 2 15 22l-4-9-9-4 20-7z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="hs-wa" viewBox="0 0 32 32"><path d="M16 .4C7.4.4.5 7.3.5 15.9c0 2.8.7 5.4 2 7.8L.4 31.6l8.1-2.1c2.3 1.2 4.8 1.9 7.5 1.9 8.6 0 15.5-7 15.5-15.5S24.6.4 16 .4zm0 28.3c-2.4 0-4.7-.6-6.7-1.8l-.5-.3-4.8 1.3 1.3-4.7-.3-.5c-1.3-2.1-2-4.5-2-7 0-7.2 5.9-13.1 13.1-13.1 3.5 0 6.8 1.4 9.3 3.8 2.5 2.5 3.8 5.8 3.8 9.3 0 7.2-5.9 13-13.2 13zm7.2-9.8c-.4-.2-2.3-1.1-2.7-1.3-.4-.1-.6-.2-.9.2-.3.4-1 1.3-1.2 1.5-.2.2-.4.3-.8.1-.4-.2-1.7-.6-3.2-2-1.2-1.1-2-2.4-2.2-2.8-.2-.4 0-.6.2-.8.2-.2.4-.4.6-.7.2-.2.3-.4.4-.7.1-.3.1-.5 0-.7-.1-.2-.9-2.2-1.3-3-.3-.8-.7-.7-.9-.7h-.8c-.3 0-.7.1-1.1.5-.4.4-1.4 1.4-1.4 3.4s1.5 3.9 1.7 4.2c.2.3 2.9 4.4 7 6.2 1 .4 1.8.7 2.4.9 1 .3 1.9.3 2.6.2.8-.1 2.3-.9 2.7-1.9.3-.9.3-1.7.2-1.9-.1-.2-.4-.3-.8-.5z"/></symbol>
</svg>"""

# --------------------------------------------------------------------------------------------------
# CSS compartido (temas + cada diseño). Lo de .story ajusta el formato 9:16.
# --------------------------------------------------------------------------------------------------
CSS = r"""
body { margin:0; background:#05070d; display:flex; flex-direction:column; align-items:center; gap:40px; padding:40px 16px; }
.hs { --acc: var(--amber); --card: var(--panel); --card-b: var(--line-2); }
.hs.light { --acc: #D98B00; --card: #fff; --card-b: rgba(13,45,94,.16); }
.hs.amb { --navy-bg:#F5A623; --txt:#0A0F1B; --txt-2:#2B2414; --txt-3:#5C4613; --line:rgba(10,15,27,.18); --line-2:rgba(10,15,27,.30);
  --panel:rgba(255,255,255,.26); --acc:#0A0F1B; --card:rgba(255,255,255,.30); --card-b:rgba(10,15,27,.22); background:#F5A623; }
.hs.amb .bg { background: radial-gradient(900px 700px at 100% -10%, rgba(255,255,255,.30), transparent 60%); }
.hs.amb .bg::after { background-image: linear-gradient(rgba(10,15,27,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(10,15,27,.06) 1px, transparent 1px); }
.hs.amb .topbar { background:#0A0F1B; }
.hs.amb .kicker { color:#0A0F1B; } .hs.amb .led { background:#0A0F1B; box-shadow:none; }
.hs.amb .hl { color:#F5A623; background:#0A0F1B; padding:0 .14em; -webkit-box-decoration-break:clone; box-decoration-break:clone; }
.hs.amb .sello img { background:#0A0F1B; padding:8px 12px; border-radius:10px; height:66px; } .hs.amb .cta svg { color:#0A0F1B; } .hs.amb .wa svg { fill:#0A0F1B; } .hs.amb .wa { color:#0A0F1B; }
.hs.light .card-sh { box-shadow: 0 6px 18px rgba(13,45,94,.06); }
.hs .sgrow { display:none; } .hs.story .sgrow { display:block; flex: 1 1 auto; }
.hs .h1 { margin-top: 34px; }
.hs.story .h1 { margin-top: 0; }
.hs .src { margin-top: 22px; }
/* foto de lote como textura (sin caras) */
.hs .foto { position:absolute; inset:0; z-index:1; background: var(--img) center/cover; filter: grayscale(.35) contrast(1.05); }
.hs .foto::after { content:''; position:absolute; inset:0; background: linear-gradient(180deg, rgba(10,15,27,.80) 0%, rgba(10,15,27,.90) 45%, rgba(10,15,27,.97) 100%); }

/* ===== PLAN ===== */
/* A · lista */
.pA .steps { display:grid; gap:12px; margin-top:34px; }
.pA .st { display:grid; grid-template-columns:78px 1fr; align-items:center; gap:18px; padding:16px 24px; border-radius:18px; background:var(--card); border:1.5px solid var(--card-b); }
.pA .st .i { font-family:var(--f-arch); font-size:50px; color:var(--acc); line-height:1; text-align:center; }
.pA .st .t { font:700 34px/1.08 var(--f-sans); color:var(--txt); letter-spacing:-.01em; }
.pA .st .d { font:400 25px/1.25 var(--f-sans); color:var(--txt-2); margin-top:4px; }
.story.pA .h1 { font-size:116px; } .story.pA .steps { gap:16px; margin-top:48px; } .story.pA .st { padding:22px 26px; } .story.pA .st .t { font-size:38px; } .story.pA .st .d { font-size:28px; }
/* B · grilla */
.pB .h1 { font-size:100px; } .pB .grid { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:40px; }
.pB .c { background:var(--card); border:1.5px solid var(--card-b); border-radius:20px; padding:24px 26px; }
.pB .c .i { font-family:var(--f-arch); font-size:48px; color:var(--acc); line-height:1; }
.pB .c .t { font:700 34px/1.1 var(--f-sans); color:var(--txt); margin-top:10px; letter-spacing:-.01em; }
.pB .c .d { font:400 24px/1.3 var(--f-sans); color:var(--txt-2); margin-top:8px; }
.story.pB .h1 { font-size:112px; } .story.pB .grid { grid-template-columns:1fr; gap:14px; margin-top:44px; }
.story.pB .c { display:grid; grid-template-columns:90px 1fr; align-items:center; padding:20px 26px; } .story.pB .c .t { margin-top:0; font-size:36px; } .story.pB .c .d { grid-column:2; margin-top:4px; font-size:26px; }
/* C · el 6 grande */
.pC .big { display:flex; align-items:flex-end; gap:26px; margin-top:30px; }
.pC .big .n { font-family:var(--f-arch); font-size:360px; line-height:.78; color:var(--acc); letter-spacing:-.04em; }
.pC .big .w { font-family:var(--f-arch); font-size:100px; line-height:.95; color:var(--txt); letter-spacing:-.02em; padding-bottom:6px; }
.pC .sub { font:500 36px/1.3 var(--f-sans); color:var(--txt-2); margin-top:34px; }
.pC .pills { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:44px; }
.pC .pill { font:600 34px/1.05 var(--f-sans); color:var(--txt); padding:38px 30px; border-radius:24px; background:var(--card); border:1.5px solid var(--card-b); display:flex; align-items:center; gap:14px; }
.pC .pill b { font-family:var(--f-mono); font-weight:500; font-size:28px; color:var(--acc); }
.story.pC .big { flex-direction:column; align-items:flex-start; gap:10px; margin-top:0; } .story.pC .big .n { font-size:360px; } .story.pC .big .w { font-size:112px; }
.story.pC .pills { grid-template-columns:1fr; gap:14px; } .story.pC .pill { padding:22px 30px; font-size:36px; } .story.pC .pills { margin-top:40px; }
/* D · recorrido */
.pD .h1 { font-size:100px; }
.pD .route { position:relative; margin-top:44px; padding-left:64px; display:grid; gap:30px; }
.pD .route::before { content:''; position:absolute; left:21px; top:18px; bottom:18px; width:4px; background:linear-gradient(var(--acc), transparent); border-radius:2px; opacity:.9; }
.pD .p { position:relative; }
.pD .p::before { content:''; position:absolute; left:-54px; top:12px; width:26px; height:26px; border-radius:50%; background:var(--navy); border:5px solid var(--acc); }
.hs.light.pD .p::before { background:var(--cream); } .hs.amb.pD .p::before { background:#F5A623; }
.pD .p .t { font:700 42px/1.05 var(--f-sans); color:var(--txt); letter-spacing:-.01em; }
.pD .p .t small { font:500 25px/1 var(--f-mono); color:var(--acc); margin-right:12px; letter-spacing:.06em; }
.pD .p .d { font:400 29px/1.25 var(--f-sans); color:var(--txt-2); margin-top:6px; }
.story.pD .h1 { font-size:120px; } .story.pD .route { gap:40px; margin-top:60px; } .story.pD .p .t { font-size:46px; } .story.pD .p .d { font-size:31px; }
/* E · antes / al sembrar / después */
.pE .h1 { font-size:96px; }
.pE .mom { display:grid; gap:16px; margin-top:38px; }
.pE .m { display:grid; grid-template-columns:230px 1fr; gap:22px; padding:24px 26px; border-radius:20px; background:var(--card); border:1.5px solid var(--card-b); align-items:start; }
.pE .m .k { font:500 23px/1.25 var(--f-mono); color:var(--acc); text-transform:uppercase; letter-spacing:.1em; padding-top:8px; }
.pE .m ul { list-style:none; display:grid; gap:10px; }
.pE .m li { font:700 34px/1.1 var(--f-sans); color:var(--txt); letter-spacing:-.01em; }
.pE .m li small { display:block; font:400 24px/1.25 var(--f-sans); color:var(--txt-2); margin-top:3px; letter-spacing:0; }
.story.pE .h1 { font-size:112px; } .story.pE .m { grid-template-columns:1fr; gap:14px; padding:28px; } .story.pE .m .k { padding-top:0; font-size:25px; } .story.pE .m li { font-size:38px; } .story.pE .m li small { font-size:27px; } .story.pE .mom { gap:20px; margin-top:50px; }
/* F · lista compacta grande (pensada para ámbar) */
.pF .h1 { font-size:116px; }
.pF ol { list-style:none; margin-top:44px; display:grid; gap:0; border-top:2px solid var(--line-2); }
.pF li { display:flex; align-items:baseline; gap:22px; padding:30px 0; border-bottom:2px solid var(--line-2); font:700 42px/1.05 var(--f-sans); color:var(--txt); letter-spacing:-.015em; }
.pF li b { font-family:var(--f-arch); font-weight:400; font-size:40px; color:var(--acc); width:52px; flex-shrink:0; }
.hs.amb.pF li b { color:#fff; -webkit-text-stroke:2px #0A0F1B; }
.story.pF .h1 { font-size:128px; } .story.pF ol { margin-top:60px; } .story.pF li { padding:26px 0; font-size:46px; }
/* G · tipográfica */
.pG .lines { margin-top:46px; display:grid; gap:4px; }
.pG .lines div { font-family:var(--f-arch); font-size:140px; line-height:.98; letter-spacing:-.04em; color:var(--txt); }
.pG .lines div:nth-child(2) { color:var(--acc); }
.pG .strip { margin-top:80px; display:flex; flex-wrap:wrap; gap:16px 14px; }
.pG .strip span { font:500 29px/1 var(--f-mono); color:var(--txt-2); padding:20px 22px; border:1.5px solid var(--card-b); border-radius:999px; letter-spacing:.02em; }
.pG .strip span b { color:var(--acc); font-weight:500; margin-right:8px; }
.story.pG .lines div { font-size:150px; } .story.pG .strip { margin-top:70px; gap:14px; } .story.pG .strip span { font-size:28px; padding:18px 22px; }
/* H · checklist sobre foto de lote */
.pH .h1 { font-size:98px; }
.pH .lab { font:500 26px/1.2 var(--f-mono); color:var(--txt-3); text-transform:uppercase; letter-spacing:.12em; margin-top:38px; }
.pH ul { list-style:none; margin-top:20px; display:grid; gap:18px; }
.pH li { display:grid; grid-template-columns:52px 1fr; gap:16px; align-items:start; }
.pH li i { width:46px; height:46px; border-radius:50%; background:var(--acc); color:#0A0F1B; font:400 26px/46px var(--f-arch); text-align:center; font-style:normal; margin-top:2px; }
.pH li .t { font:700 38px/1.1 var(--f-sans); color:var(--txt); letter-spacing:-.01em; }
.pH li .d { font:400 26px/1.25 var(--f-sans); color:var(--txt-2); margin-top:3px; }
.story.pH .h1 { font-size:112px; } .story.pH ul { gap:28px; } .story.pH li .t { font-size:42px; } .story.pH li .d { font-size:29px; }

/* ===== CLEARFIELD ===== */
.cA .h1, .cB .h1 { font-size:106px; }
.cA .sub { font:500 32px/1.3 var(--f-mono); color:var(--txt-2); margin-top:24px; }
.cA .hibs { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:40px; }
.cA .hb { padding:34px 30px; border-radius:20px; background:var(--card); border:1.5px solid var(--card-b); }
.cA .hb .nm { font:700 48px/1 var(--f-sans); color:var(--txt); } .cA .hb .nm b { color:var(--acc); }
.cA .hb .tg { font:500 24px/1.3 var(--f-mono); color:var(--acc); margin-top:16px; text-transform:uppercase; letter-spacing:.06em; }
.cA .hb .ds { font:400 30px/1.32 var(--f-sans); color:var(--txt-2); margin-top:16px; }
.cA .tl { font:500 24px/1 var(--f-mono); color:var(--txt-3); text-transform:uppercase; letter-spacing:.1em; margin-top:40px; }
.cA .tools { display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; margin-top:16px; }
.cA .tool { font:700 32px/1 var(--f-sans); color:var(--txt); padding:28px 16px; border-radius:16px; background:var(--card); border:1.5px solid var(--card-b); text-align:center; }
.cA .tool b { font-family:var(--f-arch); color:var(--acc); margin-right:12px; font-weight:400; }
.story.cA .h1 { font-size:110px; } .story.cA .hibs { grid-template-columns:1fr; margin-top:36px; } .story.cA .hb { padding:28px 30px; } .story.cA .tool { font-size:28px; padding:26px 10px; }
/* C · el 3 grande */
.cC .h1 { font-size:92px; }
.cC .big { display:flex; align-items:center; gap:44px; margin-top:40px; }
.cC .big .n { font-family:var(--f-arch); font-size:360px; line-height:.8; color:var(--acc); }
.cC .big ul { list-style:none; display:grid; gap:16px; }
.cC .big li { font:700 50px/1.1 var(--f-sans); color:var(--txt); } .cC .big li::before { content:'✓ '; color:var(--acc); }
.cC .cap { font:500 32px/1.3 var(--f-sans); color:var(--txt-2); margin-top:34px; }
.cC .row2 { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:36px; }
.cC .hb { padding:30px 28px; border-radius:18px; background:var(--card); border:1.5px solid var(--card-b); }
.cC .hb .nm { font:700 42px/1 var(--f-sans); color:var(--txt); } .cC .hb .nm b { color:var(--acc); }
.cC .hb .ds { font:400 28px/1.3 var(--f-sans); color:var(--txt-2); margin-top:12px; }
.story.cC .h1 { font-size:104px; } .story.cC .big { flex-direction:column; align-items:flex-start; gap:30px; } .story.cC .big .n { font-size:330px; } .story.cC .big li { font-size:52px; } .story.cC .big { gap:24px; margin-top:30px; }
/* D · cara a cara */
.cD .h1 { font-size:104px; }
.cD .vs { display:grid; grid-template-columns:1fr 70px 1fr; align-items:stretch; margin-top:44px; }
.cD .col { padding:36px 30px; border-radius:20px; background:var(--card); border:1.5px solid var(--card-b); }
.cD .col.on { border-color:var(--acc); }
.hs:not(.light):not(.amb).cD .col.on { background:rgba(245,166,35,.08); }
.cD .col .nm { font:700 50px/1 var(--f-sans); color:var(--txt); } .cD .col .nm b { color:var(--acc); }
.cD .col dl { display:grid; gap:22px; margin-top:28px; }
.cD .col dt { font:500 21px/1 var(--f-mono); color:var(--txt-3); text-transform:uppercase; letter-spacing:.1em; }
.cD .col dd { font:600 32px/1.2 var(--f-sans); color:var(--txt); margin-top:8px; }
.cD .mid { display:flex; align-items:center; justify-content:center; font-family:var(--f-arch); font-size:34px; color:var(--txt-3); }
.cD .both { margin-top:28px; font:600 32px/1.3 var(--f-sans); color:var(--txt); padding:26px 28px; border-radius:16px; border:1.5px dashed var(--line-2); }
.cD .both b { color:var(--acc); } .hs.amb.cD .both b { color:#fff; }
.story.cD .h1 { font-size:120px; } .story.cD .vs { grid-template-columns:1fr; grid-template-rows:auto 80px auto; } .story.cD .col { padding:30px; }
.story.cD .col dl { grid-template-columns:1fr 1fr; gap:18px 24px; } .story.cD .col dl div:last-child { grid-column:1 / -1; }
/* E · ámbar pregunta / respuesta */
.cE .q { font-family:var(--f-arch); font-size:118px; line-height:.97; letter-spacing:-.035em; color:var(--txt); margin-top:40px; }
.cE .a { font-family:var(--f-arch); font-size:84px; line-height:1; letter-spacing:-.03em; color:var(--acc); margin-top:30px; }
.cE .a .hl { padding:0 .1em; }
.cE .tags { display:grid; gap:16px; margin-top:44px; }
.cE .tag { display:flex; justify-content:space-between; align-items:center; gap:20px; padding:26px 30px; border-radius:20px; background:var(--card); border:1.5px solid var(--card-b); }
.cE .tag .nm { font:700 46px/1 var(--f-sans); color:var(--txt); } .cE .tag .ds { font:500 26px/1.2 var(--f-mono); color:var(--txt-2); text-align:right; }
.cE .herb { font:600 30px/1.35 var(--f-sans); color:var(--txt); margin-top:26px; }
.story.cE .q { font-size:132px; } .story.cE .a { font-size:96px; } .story.cE .tag { flex-direction:column; align-items:flex-start; gap:12px; } .story.cE .tag .ds { text-align:left; font-size:28px; }
/* F · checklist */
.cF .h1 { font-size:96px; }
.cF .lab { font:500 26px/1.2 var(--f-mono); color:var(--txt-3); text-transform:uppercase; letter-spacing:.12em; margin-top:40px; }
.cF ul { list-style:none; margin-top:20px; display:grid; gap:16px; }
.cF li { display:flex; gap:20px; align-items:center; font:700 40px/1.12 var(--f-sans); color:var(--txt); padding:24px 28px; border-radius:18px; background:var(--card); border:1.5px solid var(--card-b); }
.cF li i { font-style:normal; width:50px; height:50px; flex-shrink:0; border-radius:50%; background:var(--acc); color:#0A0F1B; font:400 28px/50px var(--f-arch); text-align:center; }
.cF .ans { margin-top:34px; font-family:var(--f-arch); font-size:56px; line-height:1.05; letter-spacing:-.02em; color:var(--txt); }
.cF .ans span { color:var(--acc); }
.story.cF .h1 { font-size:110px; } .story.cF ul { gap:20px; } .story.cF li { font-size:42px; padding:30px; } .story.cF .ans { font-size:64px; margin-top:50px; }
/* G · CL gigante */
.cG .cl { font-family:var(--f-arch); font-size:430px; line-height:.8; letter-spacing:-.06em; color:transparent; -webkit-text-stroke:5px var(--acc); margin-top:30px; }
.cG .t { font-family:var(--f-arch); font-size:80px; line-height:1; letter-spacing:-.03em; color:var(--txt); margin-top:26px; }
.cG .t span { color:var(--acc); }
.cG .two { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:40px; }
.cG .two div { padding:24px 26px; border-radius:18px; border:1.5px solid var(--card-b); background:var(--card); }
.cG .two b { display:block; font:700 42px/1 var(--f-sans); color:var(--txt); } .cG .two small { display:block; font:400 27px/1.3 var(--f-sans); color:var(--txt-2); margin-top:10px; }
.story.cG .cl { font-size:520px; } .story.cG .t { font-size:92px; } .story.cG .two { grid-template-columns:1fr; }
/* H · dato técnico sobre foto */
.cH .h1 { font-size:104px; }
.cH .rule { margin-top:50px; padding:38px 34px; border-left:8px solid var(--acc); background:rgba(10,15,27,.55); border-radius:0 18px 18px 0; }
.cH .rule .k { font:500 24px/1 var(--f-mono); color:var(--acc); text-transform:uppercase; letter-spacing:.12em; }
.cH .rule .v { font:700 50px/1.18 var(--f-sans); color:var(--txt); margin-top:14px; letter-spacing:-.01em; }
.cH .two { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:40px; }
.cH .two div { padding:30px 28px !important; }
.cH .two div { padding:24px 26px; border-radius:18px; border:1.5px solid var(--line-2); background:rgba(10,15,27,.6); }
.cH .two b { display:block; font:700 42px/1 var(--f-sans); color:var(--txt); } .cH .two b span { color:var(--acc); }
.cH .two small { display:block; font:400 27px/1.3 var(--f-sans); color:var(--txt-2); margin-top:10px; }
.story.cH .h1 { font-size:108px; } .story.cH .rule .v { font-size:50px; } .story.cH .two { grid-template-columns:1fr; }
"""

# --------------------------------------------------------------------------------------------------
# Cuerpos de cada diseño (devuelven el HTML entre el encabezado y el pie)
# --------------------------------------------------------------------------------------------------
def e(s):
    return html.escape(s, quote=False)

def plan_A(_):
    st = "".join(f'<div class="st"><div class="i">{i+1}</div><div><div class="t">{e(t)}</div><div class="d">{e(d)}</div></div></div>' for i, (t, d) in enumerate(PASOS))
    return f'<h1 class="h1">Tu campaña, <span class="hl">con un plan.</span></h1><div class="steps">{st}</div>'

def plan_B(_):
    c = "".join(f'<div class="c card-sh"><div class="i">0{i+1}</div><div class="t">{e(t)}</div><div class="d">{e(d)}</div></div>' for i, (t, d) in enumerate(PASOS))
    return f'<h1 class="h1">Tu campaña, <span class="hl">con un plan.</span></h1><div class="grid">{c}</div>'

def plan_C(_):
    p = "".join(f'<div class="pill card-sh"><b>0{i+1}</b>{e(t)}</div>' for i, (t, _d) in enumerate(PASOS))
    return ('<div class="big"><div class="n">6</div><div class="w">pasos para<br>tu campaña.</div></div>'
            '<div class="sub">De la visita a la cosecha, con un solo interlocutor.</div>'
            f'<div class="pills">{p}</div>')

def plan_D(_):
    p = "".join(f'<div class="p"><div class="t"><small>0{i+1}</small>{e(t)}</div><div class="d">{e(d)}</div></div>' for i, (t, d) in enumerate(PASOS))
    return f'<h1 class="h1">De la visita <span class="hl">a la cosecha.</span></h1><div class="route">{p}</div>'

def plan_E(_):
    bloques = ""
    for k, idx in MOMENTOS:
        li = "".join(f'<li>{e(PASOS[i][0])}<small>{e(PASOS[i][1])}</small></li>' for i in idx)
        bloques += f'<div class="m card-sh"><div class="k">{e(k)}</div><ul>{li}</ul></div>'
    return f'<h1 class="h1">Antes, durante <span class="hl">y después.</span></h1><div class="mom">{bloques}</div>'

def plan_F(_):
    li = "".join(f'<li><b>{i+1}</b>{e(t)}</li>' for i, (t, _d) in enumerate(PASOS))
    return f'<h1 class="h1">Tu campaña, <span class="hl">con un plan.</span></h1><ol>{li}</ol>'

def plan_G(_):
    s = "".join(f'<span><b>0{i+1}</b>{e(t)}</span>' for i, (t, _d) in enumerate(PASOS))
    return f'<div class="lines"><div>Un plan.</div><div>Seis pasos.</div><div>Un solo equipo.</div></div><div class="strip">{s}</div>'

def plan_H(_):
    li = "".join(f'<li><i>✓</i><div><div class="t">{e(t)}</div><div class="d">{e(d)}</div></div></li>' for t, d in PASOS)
    return f'<h1 class="h1">Hecho para <span class="hl">tu lote.</span></h1><div class="lab">Lo que incluye tu Plan de Campaña</div><ul>{li}</ul>'

def hib(h):
    return f'{h["nm"]} <b>CL</b>'

def cl_A(_):
    hb = lambda h, tg, ds: f'<div class="hb card-sh"><div class="nm">{hib(h)}</div><div class="tg">{tg}</div><div class="ds">{ds}</div></div>'
    tools = "".join(f'<div class="tool card-sh"><b>{i+1}</b>{t}</div>' for i, t in enumerate(HERB))
    return ('<h1 class="h1">Tardío con malezas <span class="hl">difíciles.</span></h1>'
            '<div class="sub">Los dos VIPTERA3 CL del portafolio</div>'
            '<div class="hibs">' + hb(H7624, "Ciclo corto · MR 117", "Pensado para siembras tardías. Quebrado 2 y Roya 2.")
            + hb(H7921, "MR 118", "Va en temprana y en tardía. Quebrado 2.") + '</div>'
            f'<div class="tl">Tres herbicidas, el mismo lote</div><div class="tools">{tools}</div><p class="src">{FUENTE_CL}</p>')

def cl_C(_):
    li = "".join(f"<li>{t}</li>" for t in HERB)
    return ('<h1 class="h1">¿Tardío con malezas <span class="hl">difíciles?</span></h1>'
            f'<div class="big"><div class="n">3</div><ul>{li}</ul></div>'
            '<div class="cap">Tres herramientas herbicidas y control de lepidópteros VIPTERA3.</div>'
            f'<div class="row2"><div class="hb card-sh"><div class="nm">{hib(H7624)}</div><div class="ds">Ciclo corto · MR 117. Para siembras tardías.</div></div>'
            f'<div class="hb card-sh"><div class="nm">{hib(H7921)}</div><div class="ds">MR 118. Temprana y tardía.</div></div></div>'
            f'<p class="src">{FUENTE_CL}</p>')

def cl_D(_):
    col = lambda h, on: (f'<div class="col card-sh{" on" if on else ""}"><div class="nm">{hib(h)}</div><dl>'
                         f'<div><dt>Ciclo</dt><dd>{h["ciclo"]}</dd></div><div><dt>Fecha</dt><dd>{h["fecha"]}</dd></div>'
                         f'<div><dt>Sanidad</dt><dd>{h["san"]}</dd></div></dl></div>')
    return ('<h1 class="h1">Lote sucio: <span class="hl">¿cuál va?</span></h1>'
            f'<div class="vs">{col(H7624, True)}<div class="mid">o</div>{col(H7921, False)}</div>'
            '<div class="both">Los dos: <b>glifosato, glufosinato e imidazolinonas</b>, y lepidópteros VIPTERA3.</div>'
            f'<p class="src">{FUENTE_CL}</p>')

def cl_E(_):
    return ('<div class="q">¿Lote sucio para el tardío?</div><div class="a"><span class="hl">Hay dos Clearfield.</span></div>'
            f'<div class="tags"><div class="tag card-sh"><div class="nm">{hib(H7624)}</div><div class="ds">Ciclo corto · siembras tardías</div></div>'
            f'<div class="tag card-sh"><div class="nm">{hib(H7921)}</div><div class="ds">MR 118 · temprana y tardía</div></div></div>'
            '<div class="herb">Glifosato, glufosinato e imidazolinonas en el mismo lote.</div>'
            f'<p class="src">{FUENTE_CL}</p>')

def cl_F(_):
    items = ["Un ciclo que llegue en fecha tardía", "Tres herbicidas en el mismo lote", "Control de lepidópteros"]
    li = "".join(f"<li class='card-sh'><i>✓</i>{t}</li>" for t in items)
    return ('<h1 class="h1">Tardío con malezas: <span class="hl">qué pedirle.</span></h1>'
            f'<div class="lab">El híbrido tiene que traer</div><ul>{li}</ul>'
            '<div class="ans">NS 7624 CL y NS 7921 CL: <span>los dos lo traen.</span></div>'
            f'<p class="src">{FUENTE_CL}</p>')

def cl_G(_):
    return ('<div class="cl">CL</div><div class="t">Clearfield <span>en maíz tardío.</span></div>'
            f'<div class="two"><div class="card-sh"><b>NS 7624</b><small>Ciclo corto · MR 117. Para siembras tardías.</small></div>'
            f'<div class="card-sh"><b>NS 7921</b><small>MR 118. Temprana y tardía.</small></div></div>'
            f'<p class="src">VIPTERA3 CL: glifosato, glufosinato e imidazolinonas. {FUENTE_CL}</p>')

def cl_H(_):
    return ('<h1 class="h1">En lote sucio, <span class="hl">primero el híbrido.</span></h1>'
            '<div class="rule"><div class="k">Dato técnico</div><div class="v">Las imidazolinonas van solo sobre híbridos Clearfield (CL).</div></div>'
            f'<div class="two"><div><b>NS 7624 <span>CL</span></b><small>Ciclo corto · siembras tardías.</small></div>'
            f'<div><b>NS 7921 <span>CL</span></b><small>MR 118 · temprana y tardía.</small></div></div>'
            f'<p class="src">{FUENTE_CL}</p>')

FOTO = "../../assets/fotos/drone-maiz-implantacion-02.jpg"

# clave, nombre, descripción, función, temas, foto
PLAN = [
    ("A", "Lista", "Los 6 pasos con su explicación. La más completa; se lee mejor abierta que en el scroll.", plan_A, ["navy", "crema"], False),
    ("B", "Grilla", "Seis tarjetas. En crema corta la grilla oscura del perfil.", plan_B, ["crema", "navy"], False),
    ("C", "El número grande", "Un “6” que se ve desde lejos y pocas palabras. La que mejor funciona chica, en el scroll y como anuncio.", plan_C, ["navy", "crema", "ambar"], False),
    ("D", "Recorrido", "La línea de la visita a la cosecha. Buena para fijar en el perfil.", plan_D, ["navy", "crema"], False),
    ("E", "Antes, durante y después", "Agrupa los pasos en tres momentos: se entiende que acompañás toda la campaña.", plan_E, ["navy", "crema"], False),
    ("F", "Lista grande", "Solo los nombres, bien grandes. En ámbar es la que más resalta en el feed.", plan_F, ["ambar", "navy"], False),
    ("G", "Tipográfica", "“Un plan. Seis pasos. Un solo equipo.” Tres frases y los pasos abajo. Para anuncio.", plan_G, ["navy", "ambar"], False),
    ("H", "Sobre foto de lote", "Checklist de lo que incluye, con una foto de lote propia de fondo.", plan_H, ["navy"], True),
]
CL = [
    ("A", "Lista", "Los dos híbridos y las tres herramientas, ordenado.", cl_A, ["navy", "crema"], False),
    ("C", "El número grande", "Un “3” con los tres herbicidas. Muy legible, pero repite la pregunta sin ayudar a elegir.", cl_C, ["navy", "crema"], False),
    ("D", "¿Cuál va?", "Cara a cara NS 7624 vs. NS 7921. Ayuda a decidir y abre la conversación: “¿cuál va en mi lote?”.", cl_D, ["navy", "crema", "ambar"], False),
    ("E", "Pregunta y respuesta", "“¿Lote sucio para el tardío? Hay dos Clearfield.” Directa, para anuncio.", cl_E, ["ambar", "navy"], False),
    ("F", "Qué pedirle al híbrido", "Tres condiciones y la respuesta. Educa antes de vender.", cl_F, ["navy", "crema"], False),
    ("G", "CL gigante", "Las letras CL como imagen. La más llamativa, la que menos explica.", cl_G, ["navy", "ambar"], False),
    ("H", "Dato técnico sobre foto", "“En lote sucio, primero el híbrido”: un dato útil que se guarda y se comparte.", cl_H, ["navy"], True),
]

GRUPOS = [
    dict(id="plan", base="plan-de-campana", titulo="Plan de Campaña HenderSeeds", kicker="Plan de Campaña HenderSeeds",
         cuando="jue 22/10 · 8–10 h (y segunda vuelta lun 09/11 con otra opción)", cta=CTA_PLAN, copy=COPY_PLAN,
         opciones=PLAN, rec=("C", "navy"), rec2=("F", "ambar")),
    dict(id="clearfield", base="clearfield", titulo="Tardío con malezas: los dos Clearfield", kicker="Maíz tardío · lotes sucios",
         cuando="lun 02/11 · 20–22 h", cta=CTA_CL, copy=COPY_CL, opciones=CL, rec=("D", "navy"), rec2=("H", "navy")),
]

# --------------------------------------------------------------------------------------------------
def nombre(g, k, tema):
    return f'{g["base"]}-{k}' + ("" if tema == "navy" else f"-{tema}")

def seccion(g, k, fn, tema, story, foto):
    t = TEMAS[tema]
    cls = " ".join(x for x in ["slide", "hs", t["cls"], "story" if story else "", f'{g["id"][0]}{k}'] if x)
    cls = cls.replace(f'{g["id"][0]}{k}', ("p" if g["id"] == "plan" else "c") + k)
    capa = f'<div class="foto" style="--img:url({FOTO})"></div>' if foto else '<div class="bg"></div>'
    fmt = "historia" if story else "feed"
    return f'''<section class="{cls}" data-name="{nombre(g, k, tema)}" data-fmt="{fmt}">
  {capa}<div class="topbar"></div>
  <div class="frame">
    <header class="hd">
      <div class="kicker"><span class="led"></span>{e(g["kicker"])}</div>
      <img class="logo-hs" src="../../assets/{t["logo"]}" alt="HenderSeeds">
    </header>
    <div class="sgrow"></div>
    {fn(story)}
    <div class="grow"></div>
    <footer class="ft">
      <div class="cta"><svg><use href="#hs-dm"/></svg><span>{e(g["cta"])}</span></div>
      <div class="base">
        <div class="sello"><img src="../../assets/{t["nidera"] if not foto else "logo-nidera-negativo.png"}" alt="Nidera Semillas"><span>Red.in · Distribuidor oficial</span></div>
        <div class="wa"><svg><use href="#hs-wa"/></svg>2314 53-0691</div>
      </div>
    </footer>
  </div>
</section>'''

def pagina(g, k, fn, tema, foto):
    return f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HenderSeeds · {e(g["titulo"])} {k} {TEMAS[tema]["nombre"]}</title>
<link rel="stylesheet" href="../../assets/fonts/fuentes.css"><link rel="stylesheet" href="../../assets/hs2627.css"><link rel="stylesheet" href="piezas.css">
</head><body>
{SPRITE}
{seccion(g, k, fn, tema, False, foto)}
{seccion(g, k, fn, tema, True, foto)}
</body></html>
'''

def galeria():
    secciones = ""
    for g in GRUPOS:
        cards = ""
        for k, n, d, fn, temas, foto in g["opciones"]:
            for tema in temas:
                nm = nombre(g, k, tema)
                feed, hist = f"img/{nm}-feed-1080x1350.jpg", f"img/{nm}-historia-1080x1920.jpg"
                rec = (k, tema) == g["rec"]
                rec2 = (k, tema) == g["rec2"]
                badge = ('<span class="badge">★ Recomendada para promocionar</span>' if rec else
                         '<span class="badge b2">Segunda opción</span>' if rec2 else "")
                cls = "op rec" if rec else "op"
                cards += f'''    <figure class="{cls}" data-k="{k}" data-tema="{tema}">
      <a class="ph" href="{feed}" data-feed="{feed}" data-hist="{hist}"><img src="{feed}" data-feed="{feed}" data-hist="{hist}" alt="{e(g["titulo"])}, opción {k} {TEMAS[tema]["nombre"]}" loading="lazy"></a>
      <figcaption>{badge}<b>Opción {k} · {e(n)} <i class="tema t-{tema}">{TEMAS[tema]["nombre"]}</i></b><span>{e(d)}</span>
        <span class="dls"><a href="{feed}" download>Feed 4:5</a><a href="{hist}" download>Historia 9:16</a></span></figcaption>
    </figure>
'''
        secciones += f'''<section id="{g["id"]}">
  <div class="sec-k">{e(g["cuando"])}</div>
  <h2>{e(g["titulo"])}</h2>
  <div class="gal">
{cards}  </div>
  <div class="links-row"><button class="copy" data-c="t-{g["id"]}">Copiar texto del posteo</button></div>
  <details class="cap"><summary>Ver texto</summary><pre class="txt" id="t-{g["id"]}">{e(g["copy"])}</pre></details>
</section>
'''
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Placas para descargar</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="../../assets/fonts/fuentes.css">
<link rel="stylesheet" href="../estilo.css">
<style>
.bar {{ position:sticky; top:0; z-index:5; background:var(--navy, #0a0f1b); padding:10px 0; display:flex; flex-wrap:wrap; gap:8px; align-items:center; border-bottom:1px solid var(--line); }}
.bar span {{ font-family:var(--f-mono); font-size:12px; color:var(--txt-3); margin-right:4px; }}
.bar button {{ font-family:var(--f-mono); font-size:12px; color:var(--txt); background:transparent; border:1px solid var(--line-2); border-radius:999px; padding:6px 12px; cursor:pointer; }}
.bar button.on {{ background:var(--amber); color:#0a0a0a; border-color:var(--amber); }}
.gal {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:14px; }}
@media (min-width:900px) {{ .gal {{ grid-template-columns:repeat(4,1fr); }} }}
.op {{ margin:0; background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:8px; display:flex; flex-direction:column; }}
.op.rec {{ border-color:var(--amber); box-shadow:0 0 0 1px var(--amber); }}
.op .ph img {{ width:100%; aspect-ratio:4/5; object-fit:cover; display:block; border-radius:8px; background:#05070d; }}
body.hist .op .ph img {{ aspect-ratio:9/16; }}
.op figcaption {{ display:flex; flex-direction:column; gap:4px; padding:8px 4px 4px; font-size:13.5px; color:var(--txt-2); flex:1; }}
.op figcaption b {{ color:var(--txt); font-size:14.5px; }}
.tema {{ font-style:normal; font-family:var(--f-mono); font-size:11px; font-weight:400; padding:2px 6px; border-radius:4px; margin-left:4px; vertical-align:1px; }}
.t-navy {{ background:#0D2D5E; color:#fff; }} .t-crema {{ background:#F6F4EE; color:#121826; }} .t-ambar {{ background:#F5A623; color:#0A0F1B; }}
.dls {{ margin-top:auto; padding-top:8px; display:flex; gap:12px; flex-wrap:wrap; }}
.dls a {{ font-family:var(--f-mono); font-size:12px; color:var(--amber); text-decoration:none; }}
.badge {{ align-self:flex-start; background:var(--amber); color:#0a0a0a; font-family:var(--f-mono); font-size:11px; font-weight:500; padding:4px 8px; border-radius:6px; }}
.badge.b2 {{ background:transparent; color:var(--amber); border:1px solid var(--amber); }}
.op.hide {{ display:none; }}
.links-row {{ margin-top:12px; }}
.copy {{ font-family:var(--f-mono); font-size:12px; border-radius:6px; padding:7px 11px; cursor:pointer; border:1px solid var(--amber); }}
</style>
</head>
<body>
<div class="topbar">
  <div class="wrap">
    <a href="../" aria-label="Volver a la estrategia"><img src="../../assets/logo-henderseeds-white.png" alt="HenderSeeds"></a>
    <nav class="toc" aria-label="Secciones">
      <a href="../">← Estrategia</a>
      <a href="../plan.html">Plan</a>
      <a href="#plan">Plan de Campaña</a>
      <a href="#clearfield">Clearfield</a>
    </nav>
  </div>
</div>
<div class="wrap">
<header class="hero">
  <div class="kicker"><span class="led"></span>Piezas · listas para subir</div>
  <h1>Placas para<br><em>descargar.</em></h1>
  <p class="lead">Varias opciones de cada placa, en colores distintos y en dos formatos: <b>feed 4:5</b> (Instagram y Facebook) e <b>historia 9:16</b> (historias y Estados de WhatsApp, con diseño propio). La marcada en amarillo es la que conviene publicar y promocionar. Santi revisa la elegida con la checklist del plan antes de subirla.</p>
</header>
<div class="bar" role="toolbar" aria-label="Filtros">
  <span>Ver</span><button data-f="feed" class="on">Feed 4:5</button><button data-f="hist">Historia 9:16</button>
  <span style="margin-left:10px">Color</span><button data-t="todos" class="on">Todos</button><button data-t="navy">Navy</button><button data-t="crema">Crema</button><button data-t="ambar">Ámbar</button>
</div>
{secciones}
<footer>
  <a href="../">Estrategia</a> · <a href="../guia.html">Guía</a> · <a href="../plan.html">Plan</a>
</footer>
</div>
<script>
(function () {{
  var bar = document.querySelector('.bar');
  bar.addEventListener('click', function (ev) {{
    var b = ev.target.closest('button'); if (!b) return;
    if (b.dataset.f) {{
      bar.querySelectorAll('[data-f]').forEach(function (x) {{ x.classList.toggle('on', x === b); }});
      var h = b.dataset.f === 'hist'; document.body.classList.toggle('hist', h);
      document.querySelectorAll('.op .ph').forEach(function (a) {{ var u = h ? a.dataset.hist : a.dataset.feed; a.href = u; a.querySelector('img').src = u; }});
    }}
    if (b.dataset.t) {{
      bar.querySelectorAll('[data-t]').forEach(function (x) {{ x.classList.toggle('on', x === b); }});
      document.querySelectorAll('.op').forEach(function (o) {{ o.classList.toggle('hide', b.dataset.t !== 'todos' && o.dataset.tema !== b.dataset.t); }});
    }}
  }});
  function respaldo(t) {{ var ta=document.createElement('textarea'); ta.value=t; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); try {{ document.execCommand('copy'); }} catch (e) {{}} document.body.removeChild(ta); }}
  document.querySelectorAll('button.copy').forEach(function (b) {{
    b.addEventListener('click', function () {{
      var t = document.getElementById(b.getAttribute('data-c')).textContent;
      var ok = function () {{ var a=b.textContent; b.textContent='Copiado ✓'; b.classList.add('ok'); setTimeout(function () {{ b.textContent=a; b.classList.remove('ok'); }}, 1600); }};
      try {{ if (navigator.clipboard && navigator.clipboard.writeText) {{ navigator.clipboard.writeText(t).then(ok, function () {{ respaldo(t); ok(); }}); return; }} }} catch (e) {{}}
      respaldo(t); ok();
    }});
  }});
}})();
</script>
</body>
</html>
'''

def main():
    DIR.mkdir(parents=True, exist_ok=True)
    for viejo in DIR.glob("*.html"):
        viejo.unlink()
    (DIR / "piezas.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    n = 0
    for g in GRUPOS:
        for k, _n, _d, fn, temas, foto in g["opciones"]:
            for tema in temas:
                (DIR / f"{nombre(g, k, tema)}.html").write_text(pagina(g, k, fn, tema, foto), encoding="utf-8")
                n += 1
    (DIR / "index.html").write_text(galeria(), encoding="utf-8")
    print(f"{n} placas (x2 formatos) + galería en {DIR.relative_to(RAIZ)}")

if __name__ == "__main__":
    main()
