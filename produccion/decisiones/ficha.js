/* Motor común de la serie "Decisiones 26/27".
   Cada ficha define su herramienta (window.render la arma) y llama a F.init({ escena }).
   ?formato=placa → 1080×1350, sin sello ni cierre, la ficha terminada (para la placa del feed).
   Línea de tiempo del reel (22 s): 0 gancho legible · 0,8–13 la herramienta se arma · 13,6 la regla ·
   15,2 sello GUARDALA · 18,4 cortina y cierre "Comentá FICHAS". */
var F = (function () {
  var P = new URLSearchParams(location.search);
  var PLACA = P.get('formato') === 'placa';
  var NS = 'http://www.w3.org/2000/svg';
  function clamp(v) { return Math.max(0, Math.min(1, v)); }
  function seg(t, a, b) { return clamp((t - a) / (b - a)); }
  function eio(v) { v = clamp(v); return v < 0.5 ? 4 * v * v * v : 1 - Math.pow(-2 * v + 2, 3) / 2; }
  function eout(v) { v = clamp(v); return 1 - Math.pow(1 - v, 3); }
  // Resorte amortiguado: sobrepaso leve y asentamiento rápido. u = segundos desde que arranca.
  function resorte(u, z, w) { if (u <= 0) return 0; z = z || 0.65; w = w || 13; var wd = w * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w * u) * (Math.cos(wd * u) + z * w / wd * Math.sin(wd * u)); }
  function el(tag, a, p) { var e = document.createElementNS(NS, tag); for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; }
  function h(tag, cls, html, p) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (p) p.appendChild(e); return e; }
  // entra con resorte desde abajo (dy px); devuelve k
  function entra(n, t, t0, dy) { var k = resorte(t - t0, 0.62, 12); n.style.opacity = clamp(k * 1.6); n.style.transform = 'translateY(' + (1 - k) * (dy == null ? 26 : dy) + 'px)'; return k; }

  var ICONO_DM = '<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="#0A0A0A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20.5l1.6-5.3A8.4 8.4 0 1 1 21 11.5z"/></svg>';
  var ICONO_WA = '<svg viewBox="0 0 32 32" width="34" height="34" fill="#25D366"><path d="M16 .4C7.4.4.5 7.3.5 15.9c0 2.8.7 5.4 2 7.8L.4 31.6l8.1-2.1c2.3 1.2 4.8 1.9 7.5 1.9 8.6 0 15.5-7 15.5-15.5S24.6.4 16 .4zm0 28.3c-2.4 0-4.7-.6-6.7-1.8l-.5-.3-4.8 1.3 1.3-4.7-.3-.5c-1.3-2.1-2-4.5-2-7 0-7.2 5.9-13.1 13.1-13.1 3.5 0 6.8 1.4 9.3 3.8 2.5 2.5 3.8 5.8 3.8 9.3 0 7.2-5.9 13-13.2 13zm7.2-9.8c-.4-.2-2.3-1.1-2.7-1.3-.4-.1-.6-.2-.9.2-.3.4-1 1.3-1.2 1.5-.2.2-.4.3-.8.1-.4-.2-1.7-.6-3.2-2-1.2-1.1-2-2.4-2.2-2.8-.2-.4 0-.6.2-.8.2-.2.4-.4.6-.7.2-.2.3-.4.4-.7.1-.3.1-.5 0-.7-.1-.2-.9-2.2-1.3-3-.3-.8-.7-.7-.9-.7h-.8c-.3 0-.7.1-1.1.5-.4.4-1.4 1.4-1.4 3.4s1.5 3.9 1.7 4.2c.2.3 2.9 4.4 7 6.2 1 .4 1.8.7 2.4.9 1 .3 1.9.3 2.6.2.8-.1 2.3-.9 2.7-1.9.3-.9.3-1.7.2-1.9-.1-.2-.4-.3-.8-.5z"/></svg>';

  function init(o) {
    var st = document.getElementById('stage');
    if (PLACA) st.classList.add('placa');
    var TOTAL = o.total || 22, TR = o.tRegla || 13.6, TS = TR + 1.6, TO = o.tOut || 18.4;
    var T_FICHA = TO - 0.6;   // la ficha terminada: lo que muestra la placa
    window.REEL_DURACION = TOTAL;
    var ficha = document.querySelector('.ficha'), marca = document.querySelector('.q .mk'), regla = document.querySelector('.regla'), pie = document.querySelector('.pie');
    var sello = null, cortina = null, outro = null;
    if (!PLACA) {
      sello = h('div', 'sello', 'GUARDALA', st);
      cortina = h('div', null, null, st); cortina.id = 'cortina';
      outro = h('div', 'outro', '<img src="../../docs/assets/logo-hs-blanco-hd.png" alt="HenderSeeds">' +
        '<div class="o1">¿Tu lote no encaja<br>en la ficha?<br><span>Lo vemos juntos.</span></div>' +
        '<div class="dm">' + ICONO_DM + 'Comentá FICHAS</div>' +
        '<div class="o2">y te mandamos las 5 por DM.</div>' +
        '<div class="wa">' + ICONO_WA + ' WhatsApp 2314 53-0691</div>', st);
    }
    var hijos = outro ? Array.prototype.slice.call(outro.children) : [];

    window.render = function (t) {
      if (PLACA) t = T_FICHA;
      if (marca) marca.style.setProperty('--k', eio(seg(t, 0.1, 0.8)));
      o.escena(t);
      entra(regla, t, TR, 40);
      entra(pie, t, TR + 0.5, 16);
      if (sello) { var ks = resorte(t - TS, 0.45, 14); sello.style.opacity = clamp(ks * 2); sello.style.transform = 'rotate(-9deg) scale(' + (1.6 - 0.6 * ks) + ')'; }
      if (cortina) {
        var cx = -1500; if (t > TO - 0.38 && t < TO + 0.38) cx = -1500 + eio(seg(t, TO - 0.38, TO + 0.38)) * (1500 + 1400);
        cortina.style.transform = 'translateX(' + cx + 'px) skewX(-8deg)';
        outro.style.opacity = t >= TO ? 1 : 0;
        ficha.style.visibility = sello.style.visibility = t >= TO ? 'hidden' : '';   // tapada por el cierre: que no cuente
        hijos.forEach(function (c, i) { var k = resorte(t - TO - 0.1 - i * 0.12, 0.62, 12); c.style.opacity = clamp(k * 1.6); c.style.transform = 'translateY(' + (1 - k) * 24 + 'px)'; });
      }
    };
    var imgs = Array.prototype.slice.call(document.images).map(function (im) { return im.complete ? Promise.resolve() : new Promise(function (r) { im.onload = im.onerror = r; }); });
    window.LISTO = Promise.all([document.fonts ? document.fonts.ready : Promise.resolve()].concat(imgs)).then(function () { if (o.alListo) o.alListo(); window.render(PLACA ? 0 : (window.__T || 0)); });
    if (!window.__RENDER_MODE__ && !PLACA) { var t0 = null; (function loop(ts) { if (t0 === null) t0 = ts; window.render(((ts - t0) / 1000) % TOTAL); requestAnimationFrame(loop); })(performance.now()); }
    else window.render(0);
  }
  return { PLACA: PLACA, clamp: clamp, seg: seg, eio: eio, eout: eout, resorte: resorte, el: el, h: h, entra: entra, init: init };
})();
