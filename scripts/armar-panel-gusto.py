#!/usr/bin/env python3
"""
Panel de gusto (docs/estrategia/gusto/): 12 estilos de placa con el MISMO mensaje (Plan de Campaña),
más paletas, tipografías, titulares y tono, para votar y elegir el rumbo visual.

  python3 scripts/armar-panel-gusto.py                         # HTML de cada estilo + index.html
  PIEZAS_DIR=docs/estrategia/gusto/estilos node scripts/render-piezas-estrategia.mjs   # -> JPG

Los votos se guardan en el navegador de quien vota y se copian con un botón para pasárselos a Claude.
"""
from pathlib import Path
import html, sys

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts/lib"))
import maiz  # noqa: E402

DIR = RAIZ / "docs/estrategia/gusto"
EST = DIR / "estilos"
A = "../../../assets"  # desde docs/estrategia/gusto/estilos/

PASOS = [
    ("Diagnóstico", "Tu lote y tu planteo."),
    ("Recomendación Asista", "Híbrido por ambiente; siembra variable, opcional."),
    ("Financiación", "A cosecha o de contado; tarjetas agro."),
    ("Seguro de resiembra", "De Nidera, ante granizo o encharcamiento."),
    ("Vuelo de drone", "La calidad de siembra, vista desde arriba."),
    ("Informe de visita", "Lo que vimos y recomendamos, por escrito."),
]
CTA = "¿Armamos el tuyo? Mandanos un DM."
e = lambda s: html.escape(s, quote=False)

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="hs-dm" viewBox="0 0 24 24"><path d="M22 2 11 13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 2 15 22l-4-9-9-4 20-7z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="hs-wa" viewBox="0 0 32 32"><path d="M16 .4C7.4.4.5 7.3.5 15.9c0 2.8.7 5.4 2 7.8L.4 31.6l8.1-2.1c2.3 1.2 4.8 1.9 7.5 1.9 8.6 0 15.5-7 15.5-15.5S24.6.4 16 .4zm0 28.3c-2.4 0-4.7-.6-6.7-1.8l-.5-.3-4.8 1.3 1.3-4.7-.3-.5c-1.3-2.1-2-4.5-2-7 0-7.2 5.9-13.1 13.1-13.1 3.5 0 6.8 1.4 9.3 3.8 2.5 2.5 3.8 5.8 3.8 9.3 0 7.2-5.9 13-13.2 13zm7.2-9.8c-.4-.2-2.3-1.1-2.7-1.3-.4-.1-.6-.2-.9.2-.3.4-1 1.3-1.2 1.5-.2.2-.4.3-.8.1-.4-.2-1.7-.6-3.2-2-1.2-1.1-2-2.4-2.2-2.8-.2-.4 0-.6.2-.8.2-.2.4-.4.6-.7.2-.2.3-.4.4-.7.1-.3.1-.5 0-.7-.1-.2-.9-2.2-1.3-3-.3-.8-.7-.7-.9-.7h-.8c-.3 0-.7.1-1.1.5-.4.4-1.4 1.4-1.4 3.4s1.5 3.9 1.7 4.2c.2.3 2.9 4.4 7 6.2 1 .4 1.8.7 2.4.9 1 .3 1.9.3 2.6.2.8-.1 2.3-.9 2.7-1.9.3-.9.3-1.7.2-1.9-.1-.2-.4-.3-.8-.5z"/></symbol>
</svg>"""

def pie(nidera="logo-nidera-negativo.png", cta=CTA):
    return f'''<footer class="ft">
      <div class="cta"><svg><use href="#hs-dm"/></svg><span>{e(cta)}</span></div>
      <div class="base"><div class="sello"><img src="{A}/{nidera}" alt="Nidera Semillas"><span>Red.in · Distribuidor oficial</span></div>
      <div class="wa"><svg><use href="#hs-wa"/></svg>2314 53-0691</div></div>
    </footer>'''

def logo(color="blanco"):
    return f'<img class="logo-hs" src="{A}/logo-hs-{color}-hd.png" alt="HenderSeeds">'

# ------------------------------------------------------------------------------------------------
# Los 12 estilos. Cada uno: (clave, nombre, idea, css, cuerpo)
# ------------------------------------------------------------------------------------------------
E = []

# 02 · Editorial (revista)
E.append(("02", "Editorial", "Papel crema, serif grande, filetes finos. Como una nota de revista agropecuaria.", r"""
.e02 { --txt:#1B1A17; --txt-2:#4A463D; --txt-3:#7C766A; --line:rgba(27,26,23,.18); --line-2:rgba(27,26,23,.3); --amber:#B5651D; background:#F3EEE3; }
.e02 .frame { padding:70px 80px 56px; }
.e02 .mast { display:flex; justify-content:space-between; align-items:center; border-bottom:3px double #1B1A17; padding-bottom:20px; }
.e02 .mast span { font:500 22px/1 'DM Mono'; letter-spacing:.18em; text-transform:uppercase; color:#1B1A17; }
.e02 .logo-hs { height:62px; }
.e02 h1 { font-family:'Fraunces'; font-weight:800; font-size:128px; line-height:.92; letter-spacing:-.03em; color:#1B1A17; margin-top:46px; }
.e02 h1 i { font-family:'Instrument Serif'; font-style:italic; font-weight:400; color:#B5651D; letter-spacing:-.01em; }
.e02 .dek { font:400 32px/1.35 'Fraunces'; color:#4A463D; margin-top:24px; max-width:860px; }
.e02 .cols { display:grid; grid-template-columns:1fr 1fr; gap:0 56px; margin-top:40px; border-top:1.5px solid rgba(27,26,23,.3); }
.e02 .it { padding:20px 0; border-bottom:1.5px solid rgba(27,26,23,.18); display:grid; grid-template-columns:52px 1fr; }
.e02 .it b { font:italic 400 44px/1 'Instrument Serif'; color:#B5651D; }
.e02 .it span { font:600 30px/1.15 'DM Sans'; color:#1B1A17; } .e02 .it small { display:block; font:400 22px/1.3 'DM Sans'; color:#7C766A; margin-top:4px; }
""", lambda: f'''<div class="mast"><span>Plan de Campaña · 26/27</span>{logo("navy")}</div>
    <h1>Tu campaña, <i>con un plan.</i></h1>
    <p class="dek">Seis pasos que hacemos con cada productor de Henderson, Daireaux y Bolívar.</p>
    <div class="cols">{"".join(f'<div class="it"><b>{i+1}</b><span>{e(t)}<small>{e(d)}</small></span></div>' for i,(t,d) in enumerate(PASOS))}</div>
    <div class="grow"></div>{pie("logo-nidera-positivo.png")}'''))

# 03 · Minimal suizo
E.append(("03", "Minimal", "Blanco, negro y un solo punto ámbar. Mucho aire, tipografía grande y prolija.", r"""
.e03 { --txt:#0B0B0C; --txt-2:#3D3F44; --txt-3:#8A8D93; --line:#E4E4E6; --line-2:#CFCFD3; background:#FFFFFF; }
.e03 .frame { padding:76px 80px 56px; }
.e03 .top { display:flex; justify-content:space-between; align-items:center; }
.e03 .top span { font:500 24px/1 'Inter Tight'; color:#0B0B0C; display:flex; gap:14px; align-items:center; }
.e03 .top span i { width:18px; height:18px; border-radius:50%; background:#F5A623; display:inline-block; }
.e03 .logo-hs { height:58px; }
.e03 .n { font:800 470px/.8 'Inter Tight'; letter-spacing:-.07em; color:#0B0B0C; margin-top:60px; margin-left:-18px; }
.e03 h1 { font:800 96px/1 'Inter Tight'; letter-spacing:-.045em; color:#0B0B0C; margin-top:20px; }
.e03 h1 span { color:#9A9CA1; }
.e03 .list { display:grid; grid-template-columns:1fr 1fr; gap:30px 40px; margin-top:64px; border-top:2px solid #0B0B0C; padding-top:26px; }
.e03 .list div { font:600 34px/1.15 'Inter Tight'; color:#0B0B0C; letter-spacing:-.01em; }
.e03 .list b { display:block; font:500 20px/1 'DM Mono'; color:#F5A623; margin-bottom:10px; }
""", lambda: f'''<div class="top"><span><i></i>Plan de Campaña</span>{logo("navy")}</div>
    <div class="n">6</div>
    <h1>pasos. <span>Una campaña.</span></h1>
    <div class="list">{"".join(f'<div><b>0{i+1}</b>{e(t)}</div>' for i,(t,d) in enumerate(PASOS))}</div>
    <div class="grow"></div>{pie("logo-nidera-positivo.png")}'''))

# 04 · Afiche
E.append(("04", "Afiche", "Letra condensada gigante en mayúsculas, como un cartel de ruta. Se lee a 50 metros.", r"""
.e04 { --txt:#0A0F1B; --txt-2:#1F1A10; --txt-3:#3A2E12; --line:rgba(10,15,27,.25); background:#F5A623; }
.e04 .frame { padding:60px 70px 54px; }
.e04 .hd2 { display:flex; justify-content:space-between; align-items:center; }
.e04 .hd2 span { font:400 34px/1 'Bebas Neue'; letter-spacing:.12em; color:#0A0F1B; }
.e04 .logo-hs { height:62px; }
.e04 h1 { font:400 232px/.84 'Bebas Neue'; color:#0A0F1B; margin-top:30px; letter-spacing:.005em; }
.e04 h1 span { display:block; color:#fff; -webkit-text-stroke:0; background:#0A0F1B; padding:6px 18px 0; margin-left:-18px; width:max-content; }
.e04 .rows { margin-top:44px; display:grid; grid-template-columns:1fr; gap:6px; }
.e04 .rows div { font:400 58px/1.05 'Bebas Neue'; letter-spacing:.03em; color:#0A0F1B; border-top:3px solid #0A0F1B; padding-top:10px; }
.e04 .rows b { font-weight:400; color:#fff; -webkit-text-stroke:1.5px #0A0F1B; margin-right:10px; }
.e04 .cta svg { color:#0A0F1B; } .e04 .wa svg { fill:#0A0F1B; } .e04 .wa { color:#0A0F1B; }
.e04 .sello img { background:#0A0F1B; padding:8px 12px; border-radius:10px; height:64px; }
""", lambda: f'''<div class="hd2"><span>Plan de Campaña · HenderSeeds</span>{logo("navy")}</div>
    <h1>Tu campaña<span>con un plan</span></h1>
    <div class="rows">{"".join(f'<div><b>{i+1}</b>{e(t)}</div>' for i,(t,d) in enumerate(PASOS))}</div>
    <div class="grow"></div>{pie("logo-nidera-negativo.png")}'''))

# 05 · Etiqueta de bolsa de semilla
E.append(("05", "Etiqueta de bolsa", "Papel kraft, marco doble y sello, como la etiqueta de una bolsa de semilla. Rural y con oficio.", r"""
.e05 { --txt:#2B1D10; --txt-2:#4E3820; --txt-3:#7A5B36; --line:rgba(43,29,16,.3); background:#CDAA78; }
.e05 .bg2 { position:absolute; inset:0; background: radial-gradient(800px 600px at 30% 20%, rgba(255,255,255,.18), transparent 60%), repeating-linear-gradient(45deg, rgba(0,0,0,.025) 0 2px, transparent 2px 6px); }
.e05 .frame { padding:56px; }
.e05 .box { position:relative; flex:1; border:4px solid #2B1D10; outline:2px solid #2B1D10; outline-offset:-14px; padding:50px 50px 40px; display:flex; flex-direction:column; }
.e05 .t1 { display:flex; justify-content:space-between; align-items:flex-start; }
.e05 .t1 span { font:500 26px/1.2 'Oswald'; letter-spacing:.2em; text-transform:uppercase; color:#2B1D10; }
.e05 .logo-hs { height:60px; }
.e05 h1 { font:700 118px/.95 'Oswald'; text-transform:uppercase; color:#2B1D10; letter-spacing:-.005em; margin-top:30px; }
.e05 h1 span { color:#8A2E12; }
.e05 .stamp { position:absolute; right:48px; top:190px; width:200px; height:200px; border-radius:50%; border:5px solid #8A2E12; color:#8A2E12; display:flex; flex-direction:column; align-items:center; justify-content:center; transform:rotate(-12deg); font:700 30px/1.05 'Oswald'; text-transform:uppercase; text-align:center; letter-spacing:.05em; }
.e05 .stamp small { font:500 20px/1 'Oswald'; letter-spacing:.2em; }
.e05 table { width:100%; border-collapse:collapse; margin-top:34px; }
.e05 td { border-top:2px solid rgba(43,29,16,.45); padding:13px 0; font:500 30px/1.1 'Oswald'; color:#2B1D10; text-transform:uppercase; letter-spacing:.03em; }
.e05 td:first-child { width:100px; font:400 24px/1 'Courier Prime'; color:#7A5B36; }
.e05 td small { display:block; font:400 21px/1.2 'Courier Prime'; color:#4E3820; text-transform:none; letter-spacing:0; margin-top:2px; }
.e05 .ft { margin-top:20px; } .e05 .cta svg { color:#8A2E12; } .e05 .wa svg { fill:#2B1D10; } .e05 .wa { color:#2B1D10; }
""", lambda: f'''<div class="bg2"></div><div class="box">
    <div class="t1"><span>Lote N.º ___ · Campaña 26/27</span>{logo("navy")}</div>
    <h1>Plan de<br><span>campaña</span></h1>
    <div class="stamp"><small>Incluye</small>6 pasos<small>HenderSeeds</small></div>
    <table>{"".join(f'<tr><td>Paso {i+1}</td><td>{e(t)}<small>{e(d)}</small></td></tr>' for i,(t,d) in enumerate(PASOS))}</table>
    <div class="grow"></div>{pie("logo-nidera-positivo.png")}</div>'''))

# 06 · Pizarra
E.append(("06", "Pizarra de campo", "Pizarra verde con letra a mano en tiza. Humano y cercano, como lo que se anota en el galpón.", r"""
.e06 { --txt:#F4F1E6; --txt-2:#D5D9CC; --txt-3:#A5B0A0; --line:rgba(244,241,230,.25); background:#1E3A2F; }
.e06 .bg2 { position:absolute; inset:0; background: radial-gradient(900px 700px at 50% 30%, rgba(255,255,255,.07), transparent 65%), radial-gradient(600px 400px at 80% 90%, rgba(0,0,0,.25), transparent 70%); }
.e06 .frame { padding:64px 76px 54px; }
.e06 .t1 { display:flex; justify-content:space-between; align-items:center; }
.e06 .t1 span { font:700 40px/1 'Caveat'; color:#F5C451; }
.e06 .logo-hs { height:60px; }
.e06 h1 { font:700 132px/.9 'Caveat'; color:#F4F1E6; margin-top:30px; transform:rotate(-2deg); }
.e06 h1 u { text-decoration:none; background:linear-gradient(transparent 70%, rgba(245,196,81,.55) 70% 88%, transparent 88%); }
.e06 ul { list-style:none; margin-top:36px; display:grid; gap:8px; }
.e06 li { font:600 58px/1.12 'Caveat'; color:#F4F1E6; display:flex; gap:20px; align-items:baseline; }
.e06 li i { font-style:normal; color:#F5C451; font-weight:700; }
.e06 li small { font:600 32px/1 'Caveat'; color:#A5B0A0; }
.e06 .cta { font-family:'Caveat'; font-size:48px; } .e06 .cta svg { color:#F5C451; }
""", lambda: f'''<div class="bg2"></div>
    <div class="t1"><span>Plan de Campaña 26/27</span>{logo("blanco")}</div>
    <h1>Tu campaña,<br><u>con un plan.</u></h1>
    <ul>{"".join(f'<li><i>✓</i>{e(t)}<small>— {e(d.rstrip("."))}</small></li>' if i == 0 else f'<li><i>✓</i>{e(t)}</li>' for i,(t,d) in enumerate(PASOS))}</ul>
    <div class="grow"></div>{pie()}'''))

# 07 · Informe técnico
E.append(("07", "Informe técnico", "Hoja blanca, máquina de escribir, casilleros y sello. Serio, profesional, de agrónomo.", r"""
.e07 { --txt:#14171C; --txt-2:#3A3F48; --txt-3:#7B818C; --line:#D7D9DD; --line-2:#B9BDC4; background:#FBFBF8; }
.e07 .frame { padding:64px 72px 54px; }
.e07 .t1 { display:flex; justify-content:space-between; align-items:flex-start; border-bottom:2px solid #14171C; padding-bottom:20px; }
.e07 .t1 div { font:400 22px/1.4 'Courier Prime'; color:#3A3F48; } .e07 .t1 b { display:block; font:700 30px/1.1 'Courier Prime'; color:#14171C; }
.e07 .logo-hs { height:58px; }
.e07 h1 { font:700 92px/1 'Courier Prime'; letter-spacing:-.03em; color:#14171C; margin-top:40px; }
.e07 h1 mark { background:#F5A623; color:#14171C; padding:0 8px; }
.e07 .grid { margin-top:36px; border:2px solid #14171C; }
.e07 .row { display:grid; grid-template-columns:70px 1fr 56px; border-top:1.5px solid #B9BDC4; align-items:center; }
.e07 .row:first-child { border-top:0; }
.e07 .row div { padding:16px 18px; font:400 26px/1.2 'Courier Prime'; color:#14171C; }
.e07 .row div:first-child { border-right:1.5px solid #B9BDC4; color:#7B818C; }
.e07 .row b { font-weight:700; } .e07 .row small { display:block; font-size:20px; color:#7B818C; }
.e07 .row .ok { width:34px; height:34px; border:2.5px solid #14171C; margin:auto; padding:0; display:flex; align-items:center; justify-content:center; font:700 26px/1 'Courier Prime'; }
.e07 .sello2 { position:absolute; right:84px; top:330px; border:5px solid #C0392B; color:#C0392B; font:700 34px/1 'Courier Prime'; padding:12px 20px; transform:rotate(8deg); letter-spacing:.06em; }
.e07 .cta svg { color:#C0392B; }
""", lambda: f'''<div class="t1"><div><b>INFORME · PLAN DE CAMPAÑA</b>Campaña 26/27 · Henderson · Daireaux · Bolívar</div>{logo("navy")}</div>
    <h1>Tu campaña,<br><mark>con un plan.</mark></h1>
    <div class="sello2">INCLUIDO</div>
    <div class="grid">{"".join(f'<div class="row"><div>{i+1:02d}</div><div><b>{e(t)}</b><small>{e(d)}</small></div><div><span class="ok">✓</span></div></div>' for i,(t,d) in enumerate(PASOS))}</div>
    <div class="grow"></div>{pie("logo-nidera-positivo.png")}'''))

# 08 · Amanecer ilustrado
E.append(("08", "Amanecer en el lote", "Cielo al amanecer y un maíz dibujado en el horizonte. Emoción y campo, sin fotos ni caras.", r"""
.e08 { --txt:#FFF6E8; --txt-2:#F1D9B8; --txt-3:#D7B48C; --line:rgba(255,246,232,.22); background:#0A0F1B; }
.e08 .sky { position:absolute; inset:0; background: linear-gradient(180deg, #0A0F1B 0%, #12223F 30%, #3A2A45 50%, #A4502A 64%, #F2A23A 72%, #FFD27A 76%); }
.e08 .sun { position:absolute; left:50%; top:1000px; width:300px; height:300px; margin-left:-150px; border-radius:50%; background:radial-gradient(circle, #FFF3C4, #FFC45A 55%, rgba(255,180,70,0) 72%); }
.e08 .lote { position:absolute; left:0; right:0; bottom:0; height:420px; }
.e08 .frame { z-index:3; padding:66px 76px 54px; }
.e08 .logo-hs { height:64px; }
.e08 h1 { font-family:'Archivo Black'; font-size:110px; line-height:.95; letter-spacing:-.035em; color:#FFF6E8; margin-top:40px; }
.e08 h1 span { color:#FFC45A; }
.e08 .chips2 { display:flex; flex-wrap:wrap; gap:12px; margin-top:36px; max-width:900px; }
.e08 .chips2 span { font:600 27px/1 'DM Sans'; color:#FFF6E8; padding:15px 20px; border-radius:999px; background:rgba(10,15,27,.45); border:1.5px solid rgba(255,246,232,.3); backdrop-filter:blur(4px); }
.e08 .chips2 b { color:#FFC45A; font:500 22px/1 'DM Mono'; margin-right:8px; }
.e08 .ft { position:relative; } .e08 .cta { text-shadow:0 2px 12px rgba(0,0,0,.6); } .e08 .base { border-top-color:rgba(255,246,232,.25); }
""", lambda: f'''<div class="hd"><div class="kicker" style="color:#FFC45A"><span class="led"></span>Plan de Campaña</div>{logo("blanco")}</div>
    <h1>Tu campaña,<br><span>con un plan.</span></h1>
    <div class="chips2">{"".join(f'<span><b>0{i+1}</b>{e(t)}</span>' for i,(t,d) in enumerate(PASOS))}</div>
    <div class="grow"></div>{pie()}''', ))

# 09 · Chat de WhatsApp
E.append(("09", "Chat de WhatsApp", "La placa es una conversación: el productor pregunta y HenderSeeds responde. Nativo del celular.", r"""
.e09 { --txt:#E9EDEF; --txt-2:#AEBAC1; --txt-3:#8696A0; --line:rgba(255,255,255,.12); background:#0B141A; }
.e09 .bg2 { position:absolute; inset:0; background: radial-gradient(800px 600px at 80% 0%, rgba(37,211,102,.08), transparent 60%); }
.e09 .frame { padding:0 0 54px; }
.e09 .tb { display:flex; align-items:center; gap:20px; padding:56px 60px 26px; background:#1F2C34; }
.e09 .av { width:84px; height:84px; border-radius:50%; background:#F5A623; display:flex; align-items:center; justify-content:center; }
.e09 .av img { height:44px; }
.e09 .tb b { font:700 34px/1.1 'DM Sans'; color:#E9EDEF; display:block; } .e09 .tb small { font:400 24px/1 'DM Sans'; color:#25D366; }
.e09 .conv { padding:44px 60px 0; display:flex; flex-direction:column; gap:22px; }
.e09 .bb { max-width:820px; padding:16px 24px 12px; border-radius:22px; font:400 36px/1.3 'DM Sans'; color:#E9EDEF; position:relative; }
.e09 .bb time { display:block; text-align:right; font:400 20px/1 'DM Sans'; color:#8696A0; margin-top:8px; }
.e09 .yo { align-self:flex-start; background:#202C33; border-top-left-radius:6px; }
.e09 .hs2 { align-self:flex-end; background:#005C4B; border-top-right-radius:6px; }
.e09 .hs2 ol { margin:10px 0 0 34px; } .e09 .hs2 li { margin:4px 0; } .e09 .hs2 li b { color:#FFD27A; font-weight:700; }
.e09 .px { padding:0 60px; } .e09 .ft { padding:0 60px; }
""", lambda: f'''<div class="bg2"></div>
    <div class="tb"><div class="av"><img src="{A}/logo-hs-navy-hd.png" alt=""></div><div><b>HenderSeeds</b><small>en línea</small></div></div>
    <div class="conv">
      <div class="bb yo">Hola, ¿qué incluye el plan de campaña?<time>08:12</time></div>
      <div class="bb hs2">Seis pasos, de la visita a la cosecha:<ol>{"".join(f'<li><b>{e(t)}</b></li>' for t,d in PASOS)}</ol><time>08:13 ✓✓</time></div>
      <div class="bb yo">¿Y cuándo pasan por el campo?<time>08:14</time></div>
      <div class="bb hs2">Cuando quieras. ¿Te va esta semana?<time>08:14 ✓✓</time></div>
    </div>
    <div class="grow"></div>{pie(cta="Escribinos y lo armamos con vos.")}'''))

# 10 · Bloques de color
E.append(("10", "Bloques de color", "Cada paso es un bloque de color con su número. Moderno, alegre, muy de Instagram.", r"""
.e10 { --txt:#0A0F1B; --txt-2:#2C3342; --txt-3:#5B6475; --line:rgba(10,15,27,.15); background:#F6F4EE; }
.e10 .frame { padding:62px 64px 54px; }
.e10 .t1 { display:flex; justify-content:space-between; align-items:center; }
.e10 .t1 span { font:700 28px/1 'Space Grotesk'; color:#0A0F1B; letter-spacing:-.01em; }
.e10 .logo-hs { height:60px; }
.e10 h1 { font:700 104px/.95 'Space Grotesk'; letter-spacing:-.05em; color:#0A0F1B; margin-top:34px; }
.e10 .tiles { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:38px; }
.e10 .tile { aspect-ratio:1/1.02; border-radius:26px; padding:24px; display:flex; flex-direction:column; justify-content:space-between; }
.e10 .tile b { font:700 74px/1 'Space Grotesk'; letter-spacing:-.04em; }
.e10 .tile span { font:700 29px/1.08 'Space Grotesk'; letter-spacing:-.02em; }
.e10 .c1 { background:#0D2D5E; color:#fff; } .e10 .c2 { background:#F5A623; color:#0A0F1B; } .e10 .c3 { background:#2F6B3A; color:#fff; }
.e10 .c4 { background:#C65A2E; color:#fff; } .e10 .c5 { background:#9CC3E6; color:#0A0F1B; } .e10 .c6 { background:#0A0F1B; color:#F5A623; }
""", lambda: f'''<div class="t1"><span>● Plan de Campaña</span>{logo("navy")}</div>
    <h1>Tu campaña,<br>con un plan.</h1>
    <div class="tiles">{"".join(f'<div class="tile c{i+1}"><b>{i+1}</b><span>{e(t)}</span></div>' for i,(t,d) in enumerate(PASOS))}</div>
    <div class="grow"></div>{pie("logo-nidera-positivo.png")}'''))

# 11 · Foto protagonista
E.append(("11", "Foto protagonista", "La foto del lote ocupa todo, con una frase y un sticker. Poco texto: ideal para anuncio.", r"""
.e11 { --txt:#fff; --txt-2:#E6E9EE; --txt-3:#C3C9D3; --line:rgba(255,255,255,.3); background:#222; }
.e11 .ph { position:absolute; inset:0; background:url(../../../assets/fotos/drone-maiz-implantacion-01.jpg) center/cover; filter:saturate(1.15) contrast(1.1); }
.e11 .ph::after { content:''; position:absolute; inset:0; background:linear-gradient(180deg, rgba(10,15,27,.55) 0%, rgba(10,15,27,.05) 35%, rgba(10,15,27,.2) 60%, rgba(10,15,27,.92) 100%); }
.e11 .frame { z-index:3; }
.e11 .logo-hs { height:66px; }
.e11 h1 { font-family:'Archivo Black'; font-size:120px; line-height:.92; letter-spacing:-.04em; color:#fff; margin-top:34px; text-shadow:0 4px 30px rgba(0,0,0,.45); }
.e11 .stk { position:absolute; right:70px; top:560px; width:280px; height:280px; border-radius:50%; background:#F5A623; color:#0A0F1B; display:flex; flex-direction:column; align-items:center; justify-content:center; transform:rotate(10deg); box-shadow:0 12px 40px rgba(0,0,0,.35); text-align:center; }
.e11 .stk b { font:400 150px/.8 'Archivo Black'; letter-spacing:-.05em; } .e11 .stk span { font:700 30px/1.05 'DM Sans'; margin-top:8px; }
.e11 .line { font:500 32px/1.35 'DM Sans'; color:#fff; max-width:760px; text-shadow:0 2px 12px rgba(0,0,0,.6); margin-bottom:26px; }
""", lambda: f'''<div class="ph"></div>
    <div class="hd"><div class="kicker"><span class="led"></span>Plan de Campaña</div>{logo("blanco")}</div>
    <h1>Tu lote<br>tiene un plan.</h1>
    <div class="stk"><b>6</b><span>pasos<br>incluidos</span></div>
    <div class="grow"></div>
    <p class="line">Diagnóstico, Recomendación Asista, financiación, seguro de resiembra, vuelo de drone e informe.</p>{pie()}'''))

# 12 · Línea de tiempo
E.append(("12", "Línea de tiempo", "Los pasos ubicados en el calendario real de la campaña, de la visita a la cosecha.", r"""
.e12 { --txt:#F2F5FA; --txt-2:#B4C1D6; --txt-3:#7F8DA6; --line:rgba(255,255,255,.14); background:#0D2D5E; }
.e12 .bg2 { position:absolute; inset:0; background: radial-gradient(900px 700px at 100% 0%, rgba(245,166,35,.16), transparent 60%), linear-gradient(180deg, #0D2D5E, #091E3E); }
.e12 .frame { padding:66px 70px 54px; }
.e12 .logo-hs { height:62px; }
.e12 h1 { font:700 110px/.95 'Space Grotesk'; letter-spacing:-.05em; color:#fff; margin-top:36px; } .e12 h1 span { color:#F5A623; }
.e12 .tl { position:relative; margin-top:80px; padding:0 6px; display:grid; grid-template-columns:repeat(6,1fr); }
.e12 .tl::before { content:''; position:absolute; left:0; right:0; top:58px; height:6px; border-radius:3px; background:linear-gradient(90deg, #F5A623, #F5A623 60%, rgba(245,166,35,.35)); }
.e12 .ev { position:relative; display:flex; flex-direction:column; align-items:center; text-align:center; padding:0 4px; }
.e12 .ev .mo { font:500 22px/1 'DM Mono'; color:#B4C1D6; letter-spacing:.08em; text-transform:uppercase; height:36px; }
.e12 .ev .dot { width:34px; height:34px; border-radius:50%; background:#0D2D5E; border:6px solid #F5A623; margin-top:4px; }
.e12 .ev .nm { font:700 28px/1.1 'Space Grotesk'; color:#fff; margin-top:20px; letter-spacing:-.02em; }
.e12 .ev:nth-child(even) .nm { margin-top:140px; }
.e12 .note { margin-top:90px; font:500 36px/1.35 'DM Sans'; color:#B4C1D6; border-left:5px solid #F5A623; padding-left:24px; }
.e12 .note b { color:#fff; }
""", lambda: f'''<div class="bg2"></div>
    <div class="hd"><div class="kicker"><span class="led"></span>Plan de Campaña</div>{logo("blanco")}</div>
    <h1>De la visita<br><span>a la cosecha.</span></h1>
    <div class="tl">{"".join(f'<div class="ev"><div class="mo">{m}</div><div class="dot"></div><div class="nm">{e(t)}</div></div>' for m,(t,d) in zip(["Visita","Elección","Compra","Siembra","Emergencia","Cierre"], PASOS))}</div>
    <p class="note"><b>Un solo interlocutor</b> durante toda la campaña: el mismo que te visitó es el que te entrega el informe.</p>
    <div class="grow"></div>{pie()}'''))

# 13 · Datos grandes / ficha
E.append(("13", "Tarjeta de producto", "Como la ficha de un producto premium: la oferta es el producto, con nombre, versión y lo que trae.", r"""
.e13 { --txt:#0A0F1B; --txt-2:#3E4A60; --txt-3:#6B7488; --line:rgba(13,45,94,.14); background:#E9EEF5; }
.e13 .frame { padding:60px 60px 54px; }
.e13 .card2 { background:#fff; border-radius:40px; padding:56px 50px 50px; box-shadow:0 30px 60px rgba(13,45,94,.14); margin-top:10px; }
.e13 .r1 { display:flex; justify-content:space-between; align-items:center; }
.e13 .r1 span { font:500 22px/1 'DM Mono'; color:#6B7488; letter-spacing:.12em; text-transform:uppercase; }
.e13 .logo-hs { height:56px; }
.e13 h1 { font:800 108px/.95 'Inter Tight'; letter-spacing:-.05em; color:#0A0F1B; margin-top:30px; }
.e13 .ver { display:inline-flex; gap:10px; margin-top:20px; }
.e13 .ver span { font:600 24px/1 'Inter Tight'; padding:12px 18px; border-radius:999px; background:#0A0F1B; color:#fff; }
.e13 .ver span:last-child { background:#F5A623; color:#0A0F1B; }
.e13 .inc { margin-top:30px; display:grid; grid-template-columns:1fr 1fr; gap:4px 30px; }
.e13 .inc div { display:flex; gap:14px; align-items:center; font:600 32px/1.15 'Inter Tight'; color:#0A0F1B; padding:30px 0; border-bottom:1.5px solid #E2E7EF; letter-spacing:-.01em; }
.e13 .inc i { width:30px; height:30px; flex-shrink:0; border-radius:50%; background:#E6F4EA; color:#1E8E3E; font:700 18px/30px 'DM Sans'; text-align:center; font-style:normal; }
.e13 .ft { margin-top:30px; }
""", lambda: f'''<div class="card2"><div class="r1"><span>Oferta · Campaña 26/27</span>{logo("navy")}</div>
    <h1>Plan de Campaña<br>HenderSeeds</h1>
    <div class="ver"><span>Maíz y girasol</span><span>6 pasos incluidos</span></div>
    <div class="inc">{"".join(f'<div><i>✓</i>{e(t)}</div>' for t,d in PASOS)}</div></div>
    <div class="grow"></div>{pie("logo-nidera-positivo.png")}'''))

ESTILOS = E

# ------------------------------------------------------------------------------------------------
BASE_CSS = r"""
body { margin:0; background:#05070d; display:flex; flex-direction:column; align-items:center; gap:40px; padding:40px 16px; }
.slide .grow { flex:1 1 auto; }
.slide .frame > * { position:relative; z-index:1; }
.slide .frame > .bg2, .slide .frame > .ph { position:absolute; z-index:0; }
"""

def pagina(k, nombre, css, cuerpo):
    lote = ""
    if k == "08":
        lote = (f'<div class="sky"></div><div class="sun"></div>'
                f'<svg class="lote" viewBox="0 0 1080 420" preserveAspectRatio="xMidYMax slice">{maiz.defs()}{maiz.lote(1080, 420, semilla=5)}</svg>')
    return f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Estilo {k} · {e(nombre)}</title>
<link rel="stylesheet" href="{A}/fonts/fuentes.css"><link rel="stylesheet" href="{A}/fonts/extra/fuentes-extra.css"><link rel="stylesheet" href="{A}/hs2627.css">
<style>{BASE_CSS}{css}</style></head><body>
{SPRITE}
<section class="slide hs e{k}" data-name="estilo-{k}" data-fmt="feed">
  {lote}<div class="frame">
    {cuerpo()}
  </div>
</section>
</body></html>
'''

# ------------------------------------------------------------------------------------------------
# Las otras preguntas del panel
# ------------------------------------------------------------------------------------------------
PALETAS = [
    ("p1", "Navy + ámbar (la actual)", ["#0A0F1B", "#0D2D5E", "#F5A623", "#F2F5FA"]),
    ("p2", "Crema + navy", ["#F6F4EE", "#0D2D5E", "#D98B00", "#121826"]),
    ("p3", "Ámbar pleno", ["#F5A623", "#0A0F1B", "#FFFFFF", "#FFD27A"]),
    ("p4", "Verde campo", ["#1E3A2F", "#2F6B3A", "#F5C451", "#F4F1E6"]),
    ("p5", "Tierra y kraft", ["#CDAA78", "#2B1D10", "#8A2E12", "#F3EEE3"]),
    ("p6", "Blanco minimal", ["#FFFFFF", "#0B0B0C", "#9A9CA1", "#F5A623"]),
    ("p7", "Cielo y tierra", ["#9CC3E6", "#0D2D5E", "#C65A2E", "#F6F4EE"]),
    ("p8", "Amanecer", ["#12223F", "#A4502A", "#FFC45A", "#FFF6E8"]),
]
TIPOS = [
    ("t1", "Archivo Black + DM Sans (la actual)", "'Archivo Black'", "400", "'DM Sans'"),
    ("t2", "Fraunces (serif de revista)", "'Fraunces'", "800", "'DM Sans'"),
    ("t3", "Instrument Serif (elegante)", "'Instrument Serif'", "400", "'DM Sans'"),
    ("t4", "Bebas Neue (afiche)", "'Bebas Neue'", "400", "'DM Sans'"),
    ("t5", "Oswald (etiqueta rural)", "'Oswald'", "700", "'Courier Prime'"),
    ("t6", "Inter Tight (moderna y limpia)", "'Inter Tight'", "800", "'Inter Tight'"),
    ("t7", "Space Grotesk (técnica, joven)", "'Space Grotesk'", "700", "'DM Sans'"),
    ("t8", "Caveat (a mano)", "'Caveat'", "700", "'DM Sans'"),
]
TITULARES = [
    ("h1", "Tu campaña, con un plan."),
    ("h2", "6 pasos para tu campaña."),
    ("h3", "De la visita a la cosecha."),
    ("h4", "Un plan. Seis pasos. Un solo equipo."),
    ("h5", "Tu lote tiene un plan."),
    ("h6", "No te vendemos la bolsa y desaparecemos."),
    ("h7", "¿Quién te acompaña después de la siembra?"),
    ("h8", "Sembrá con plan, no a ojo."),
]
TONOS = [
    ("o1", "Técnico", "Recomendación Asista: posicionamos el híbrido según el ambiente de cada lote, con prescripción de siembra variable si la querés."),
    ("o2", "Cercano", "Pasamos por tu campo, vemos el lote con vos y armamos juntos la campaña. Después volvemos a ver cómo quedó."),
    ("o3", "Directo comercial", "Plan de Campaña HenderSeeds: híbrido, financiación a cosecha y seguro de resiembra en una sola propuesta. Pedí la tuya."),
    ("o4", "Con humor de campo", "El pronóstico no lo manejamos. Todo lo demás, sí: híbrido, financiación, seguro y un drone que no se olvida de nada."),
]

def tarjeta_voto(qid, titulo, cuerpo, sub=""):
    return f'''<article class="q" data-id="{qid}">
  {cuerpo}
  <div class="qt"><b>{e(titulo)}</b>{f"<span>{e(sub)}</span>" if sub else ""}</div>
  <div class="vote" role="group" aria-label="Votar {e(titulo)}">
    <button data-v="2" title="Me encanta">❤️</button><button data-v="1" title="Va">👍</button><button data-v="-1" title="No">👎</button>
  </div>
  <input class="nota" type="text" placeholder="Nota (opcional)">
</article>'''

def index():
    est = "".join(tarjeta_voto(f"estilo-{k}", f"{k} · {n}",
                               f'<a class="img" href="estilos/img/estilo-{k}-feed-1080x1350.jpg"><img src="estilos/img/estilo-{k}-feed-1080x1350.jpg" alt="Estilo {e(n)}" loading="lazy"></a>', d)
                  for k, n, d, _c, _b in ESTILOS)
    est = tarjeta_voto("estilo-01", "01 · Siembra 26/27 (la actual)",
                       '<a class="img" href="../piezas/img/plan-de-campana-C-feed-1080x1350.jpg"><img src="../piezas/img/plan-de-campana-C-feed-1080x1350.jpg" alt="Estilo actual" loading="lazy"></a>',
                       "Navy, grilla y ámbar. Es la base de todo lo que hicimos hasta ahora.") + est
    pal = "".join(tarjeta_voto(pid, n, '<div class="sw">' + "".join(f'<i style="background:{c}"></i>' for c in cs) + "</div>") for pid, n, cs in PALETAS)
    tip = "".join(tarjeta_voto(tid, n, f'<div class="ty"><div style="font-family:{f};font-weight:{w}">Tu campaña, con un plan.</div><p style="font-family:{f2}">Seis pasos, de la visita a la cosecha.</p></div>') for tid, n, f, w, f2 in TIPOS)
    tit = "".join(tarjeta_voto(hid, t, f'<div class="hl2">{e(t)}</div>') for hid, t in TITULARES)
    ton = "".join(tarjeta_voto(oid, n, f'<div class="tn">“{e(t)}”</div>') for oid, n, t in TONOS)
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Panel de gusto</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="../../assets/fonts/fuentes.css">
<link rel="stylesheet" href="../../assets/fonts/extra/fuentes-extra.css">
<link rel="stylesheet" href="../estilo.css">
<style>
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:14px; }}
@media (min-width:900px) {{ .grid {{ grid-template-columns:repeat(4,1fr); }} .grid.wide {{ grid-template-columns:repeat(2,1fr); }} }}
.grid > * {{ min-width:0; }}
.toc {{ min-width:0; }}
.q {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:8px; display:flex; flex-direction:column; gap:8px; transition:border-color .15s; }}
.q.v2 {{ border-color:var(--amber); box-shadow:0 0 0 1px var(--amber); }} .q.v1 {{ border-color:#4f8a5b; }} .q.vn {{ opacity:.45; }}
.q .img img {{ width:100%; aspect-ratio:4/5; display:block; border-radius:8px; object-fit:cover; background:#05070d; }}
.qt {{ display:flex; flex-direction:column; gap:3px; padding:0 4px; }} .qt b {{ font-size:14.5px; color:var(--txt); }} .qt span {{ font-size:13px; color:var(--txt-2); line-height:1.4; }}
.vote {{ display:flex; gap:6px; padding:0 4px; margin-top:auto; }}
.vote button {{ flex:1; font-size:18px; padding:7px 0; border-radius:8px; border:1px solid var(--line-2); background:transparent; cursor:pointer; }}
.vote button.on {{ background:rgba(245,166,35,.18); border-color:var(--amber); }}
.nota {{ min-width:0; width:auto; margin:0 4px 4px; padding:7px 9px; border-radius:7px; border:1px solid var(--line); background:rgba(0,0,0,.25); color:var(--txt); font:14px var(--f-sans); }}
.sw {{ display:grid; grid-template-columns:2fr 1fr 1fr 1fr; height:110px; border-radius:8px; overflow:hidden; }} .sw i {{ display:block; }}
.ty {{ background:#F6F4EE; color:#121826; border-radius:8px; padding:18px 14px; min-height:150px; }} .ty {{ overflow:hidden; }} .ty div {{ font-size:25px; line-height:1.05; overflow-wrap:anywhere; }} .ty p {{ font-size:14px; margin-top:10px; color:#3E4A60; }}
.hl2 {{ overflow-wrap:anywhere; hyphens:auto; font-family:'Archivo Black'; font-size:19px; line-height:1.1; color:var(--txt); padding:18px 12px; min-height:110px; background:var(--navy-2, #0d2d5e); border-radius:8px; }}
.tn {{ font-size:15px; line-height:1.5; color:var(--txt); padding:14px 12px; background:rgba(255,255,255,.03); border-radius:8px; border:1px dashed var(--line-2); }}
.res {{ margin-top:16px; }} .res textarea {{ width:100%; min-height:200px; border-radius:10px; padding:12px; background:var(--navy-2,#0d2d5e); color:var(--txt); border:1px solid var(--line); font:14px/1.5 var(--f-mono); }}
.who {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:12px; align-items:center; }} .who input {{ padding:8px 10px; border-radius:8px; border:1px solid var(--line-2); background:transparent; color:var(--txt); font:15px var(--f-sans); }}
.btns {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:10px; }}
.btns button, .btns a {{ font-family:var(--f-mono); font-size:13px; border-radius:8px; padding:9px 13px; cursor:pointer; border:1px solid var(--amber); background:var(--amber); color:#0a0a0a; text-decoration:none; }}
.btns .sec {{ background:transparent; color:var(--txt); border-color:var(--line-2); }}
.count {{ font-family:var(--f-mono); font-size:12px; color:var(--amber); }}
</style>
</head>
<body>
<div class="topbar">
  <div class="wrap">
    <a href="../" aria-label="Volver a la estrategia"><img src="../../assets/logo-henderseeds-white.png" alt="HenderSeeds"></a>
    <nav class="toc" aria-label="Secciones">
      <a href="../">← Estrategia</a><a href="../piezas/">Piezas</a>
      <a href="#estilos">Estilos</a><a href="#paletas">Colores</a><a href="#tipos">Letras</a><a href="#titulares">Titulares</a><a href="#tono">Tono</a><a href="#enviar">Enviar</a>
    </nav>
  </div>
</div>
<div class="wrap">
<header class="hero">
  <div class="kicker"><span class="led"></span>Panel de gusto · 08/10</div>
  <h1>¿Qué te<br><em>gusta?</em></h1>
  <p class="lead">Trece estilos de placa con <b>el mismo mensaje</b>, para que compares solo el estilo. Después, colores, letras, titulares y tono. Votá con <b>❤️ me encanta</b>, <b>👍 va</b> o <b>👎 no</b>, y si querés dejá una nota ("me gusta la letra pero no el color"). Al final tocá <b>Copiar</b> y pegámelo en el chat: con eso armo el estilo de HenderSeeds para todo lo que viene. Santi puede votar en su celular y mandar el suyo.</p>
  <p class="count" id="cnt"></p>
</header>

<section id="estilos"><div class="sec-k">01 · Estilos de placa</div><h2>El mismo mensaje, trece maneras.</h2>
  <p class="body">Tocá la imagen para verla grande. No hace falta que te guste toda: anotá qué parte sí.</p>
  <div class="grid">{est}</div></section>

<section id="paletas"><div class="sec-k">02 · Colores</div><h2>¿Con qué colores?</h2><div class="grid">{pal}</div></section>
<section id="tipos"><div class="sec-k">03 · Letras</div><h2>¿Con qué letra?</h2><div class="grid">{tip}</div></section>
<section id="titulares"><div class="sec-k">04 · Titulares</div><h2>¿Cómo lo decimos?</h2><div class="grid">{tit}</div></section>
<section id="tono"><div class="sec-k">05 · Tono</div><h2>¿Con qué voz?</h2><div class="grid wide">{ton}</div></section>

<section id="enviar"><div class="sec-k">06 · Enviar</div><h2>Mandame tu elección.</h2>
  <div class="who"><label for="quien">¿Quién vota?</label><input id="quien" placeholder="Alvaro, Santi…"></div>
  <div class="res"><textarea id="res" readonly></textarea></div>
  <div class="btns"><button id="copiar">Copiar para Claude</button><a id="wa" class="sec" href="#" target="_blank" rel="noopener">Mandar por WhatsApp</a><button id="borrar" class="sec">Borrar mis votos</button></div>
</section>

<footer><a href="../">Estrategia</a> · <a href="../piezas/">Piezas</a> · <a href="../plan.html">Plan</a></footer>
</div>
<script>
(function () {{
  var KEY = 'hs-gusto-0810', st = {{}};
  try {{ st = JSON.parse(localStorage.getItem(KEY) || '{{}}') || {{}}; }} catch (e) {{ st = {{}}; }}
  function save() {{ try {{ localStorage.setItem(KEY, JSON.stringify(st)); }} catch (e) {{}} resumen(); }}
  var qs = document.querySelectorAll('.q');
  function pinta(q) {{
    var r = st[q.dataset.id] || {{}};
    q.classList.toggle('v2', r.v === 2); q.classList.toggle('v1', r.v === 1); q.classList.toggle('vn', r.v === -1);
    q.querySelectorAll('.vote button').forEach(function (b) {{ b.classList.toggle('on', +b.dataset.v === r.v); }});
    q.querySelector('.nota').value = r.n || '';
  }}
  qs.forEach(function (q) {{
    pinta(q);
    q.querySelector('.vote').addEventListener('click', function (ev) {{
      var b = ev.target.closest('button'); if (!b) return;
      var r = st[q.dataset.id] || {{}}; var v = +b.dataset.v; r.v = (r.v === v) ? undefined : v; st[q.dataset.id] = r; pinta(q); save();
    }});
    q.querySelector('.nota').addEventListener('input', function (ev) {{ var r = st[q.dataset.id] || {{}}; r.n = ev.target.value; st[q.dataset.id] = r; save(); }});
  }});
  var quien = document.getElementById('quien'); quien.value = st._quien || '';
  quien.addEventListener('input', function () {{ st._quien = quien.value; save(); }});
  function nombre(id) {{ var q = document.querySelector('.q[data-id="' + id + '"] .qt b'); return q ? q.textContent : id; }}
  function resumen() {{
    var lin = ['Panel de gusto HenderSeeds · vota: ' + (st._quien || '(sin nombre)')], sec = {{ '❤️': [], '👍': [], '👎': [], '📝': [] }}, n = 0;
    qs.forEach(function (q) {{
      var r = st[q.dataset.id]; if (!r || (r.v === undefined && !r.n)) return; n++;
      var k = r.v === 2 ? '❤️' : r.v === 1 ? '👍' : r.v === -1 ? '👎' : '📝';
      sec[k].push('- [' + q.dataset.id + '] ' + nombre(q.dataset.id) + (r.n ? ' — ' + r.n : ''));
    }});
    ['❤️', '👍', '👎', '📝'].forEach(function (k) {{ if (sec[k].length) {{ lin.push('', k); lin = lin.concat(sec[k]); }} }});
    var t = lin.join('\\n'); document.getElementById('res').value = t;
    document.getElementById('wa').href = 'https://wa.me/?text=' + encodeURIComponent(t);
    document.getElementById('cnt').textContent = n ? n + ' de ' + qs.length + ' votadas' : '';
  }}
  resumen();
  document.getElementById('copiar').addEventListener('click', function () {{
    var b = this, t = document.getElementById('res').value;
    var ok = function () {{ b.textContent = 'Copiado ✓'; setTimeout(function () {{ b.textContent = 'Copiar para Claude'; }}, 1600); }};
    try {{ navigator.clipboard.writeText(t).then(ok, function () {{ document.getElementById('res').select(); document.execCommand('copy'); ok(); }}); }}
    catch (e) {{ document.getElementById('res').select(); document.execCommand('copy'); ok(); }}
  }});
  document.getElementById('borrar').addEventListener('click', function () {{ if (confirm('¿Borrar tus votos?')) {{ st = {{}}; qs.forEach(pinta); quien.value = ''; save(); }} }});
}})();
</script>
</body>
</html>
'''

def main():
    EST.mkdir(parents=True, exist_ok=True)
    for f in EST.glob("*.html"):
        f.unlink()
    for k, n, _d, css, cuerpo in ESTILOS:
        (EST / f"estilo-{k}.html").write_text(pagina(k, n, css, cuerpo), encoding="utf-8")
    (DIR / "index.html").write_text(index(), encoding="utf-8")
    print(f"{len(ESTILOS)} estilos + panel en {DIR.relative_to(RAIZ)}")

if __name__ == "__main__":
    main()
