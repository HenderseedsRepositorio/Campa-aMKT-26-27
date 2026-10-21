/* Motor de la versión simple de Decisiones 26/27.
   Cada reel trae sus escenas: <div class="esc" data-a="0" data-b="3.4"> … </div> (segundos).
   Dentro, todo lo que lleva data-t="1.2" entra con resorte a ese segundo (data-t negativo = visible
   desde el cuadro 0); data-fx="pop" entra creciendo. Un .mk con data-mk="0.2" pinta el marcador.
   Entre escena y escena cruza la cortina navy. S.cierre({...}) agrega la escena final navy.
   ?formato=placa → muestra .placa-c (el resumen 4:5) y nada más. */
var S = (function () {
  var NS = 'http://www.w3.org/2000/svg';
  function clamp(v) { return Math.max(0, Math.min(1, v)); }
  function seg(t, a, b) { return clamp((t - a) / (b - a)); }
  function eio(v) { v = clamp(v); return v < 0.5 ? 4 * v * v * v : 1 - Math.pow(-2 * v + 2, 3) / 2; }
  function eout(v) { v = clamp(v); return 1 - Math.pow(1 - v, 3); }
  // Resorte amortiguado: sobrepaso leve y asentamiento rápido. u = segundos desde que arranca.
  function resorte(u, z, w) { if (u <= 0) return 0; z = z || 0.65; w = w || 13; var wd = w * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w * u) * (Math.cos(wd * u) + z * w / wd * Math.sin(wd * u)); }
  function el(tag, a, p) { var e = document.createElementNS(NS, tag); for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; }
  function h(tag, cls, html, p) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (p) p.appendChild(e); return e; }
  var PLACA = new URLSearchParams(location.search).get('formato') === 'placa';
  var ICONO_DM = '<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="#0A0A0A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>';
  var ICONO_WA = '<svg viewBox="0 0 32 32" width="34" height="34" fill="#25D366"><path d="M16 .4C7.4.4.5 7.3.5 15.9c0 2.8.7 5.4 2 7.8L.4 31.6l8.1-2.1c2.3 1.2 4.8 1.9 7.5 1.9 8.6 0 15.5-7 15.5-15.5S24.6.4 16 .4zm0 28.3c-2.4 0-4.7-.6-6.7-1.8l-.5-.3-4.8 1.3 1.3-4.7-.3-.5c-1.3-2.1-2-4.5-2-7 0-7.2 5.9-13.1 13.1-13.1 3.5 0 6.8 1.4 9.3 3.8 2.5 2.5 3.8 5.8 3.8 9.3 0 7.2-5.9 13-13.2 13zm7.2-9.8c-.4-.2-2.3-1.1-2.7-1.3-.4-.1-.6-.2-.9.2-.3.4-1 1.3-1.2 1.5-.2.2-.4.3-.8.1-.4-.2-1.7-.6-3.2-2-1.2-1.1-2-2.4-2.2-2.8-.2-.4 0-.6.2-.8.2-.2.4-.4.6-.7.2-.2.3-.4.4-.7.1-.3.1-.5 0-.7-.1-.2-.9-2.2-1.3-3-.3-.8-.7-.7-.9-.7h-.8c-.3 0-.7.1-1.1.5-.4.4-1.4 1.4-1.4 3.4s1.5 3.9 1.7 4.2c.2.3 2.9 4.4 7 6.2 1 .4 1.8.7 2.4.9 1 .3 1.9.3 2.6.2.8-.1 2.3-.9 2.7-1.9.3-.9.3-1.7.2-1.9-.1-.2-.4-.3-.8-.5z"/></svg>';

  // escena final: la regla, el botón y el WhatsApp
  function cierre(o) {
    var e = h('div', 'esc navy', '<div class="caja">' +
      '<img class="hs" src="../../docs/assets/logo-hs-blanco-hd.png" alt="HenderSeeds" data-t="' + (o.a + 0.15) + '">' +
      '<div class="r" data-t="' + (o.a + 0.3) + '">' + o.regla + '</div>' +
      '<div class="dm" data-t="' + (o.a + 0.8) + '" data-fx="pop">' + ICONO_DM + (o.boton || 'Mandanos un DM') + '</div>' +
      '<div class="wa" data-t="' + (o.a + 1.0) + '">' + ICONO_WA + ' WhatsApp 2314 53-0691</div>' +
      (o.src ? '<div class="src" data-t="' + (o.a + 1.2) + '">' + o.src + '</div>' : '') + '</div>', document.getElementById('stage'));
    e.dataset.a = o.a; e.dataset.b = o.b;
  }

  function init(o) {
    o = o || {};
    var st = document.getElementById('stage');
    if (PLACA) st.classList.add('placa');
    var esc = Array.prototype.map.call(document.querySelectorAll('.esc'), function (n) { return { n: n, a: +n.dataset.a, b: +n.dataset.b }; });
    var TOTAL = esc.length ? esc[esc.length - 1].b : 1;
    window.REEL_DURACION = TOTAL;
    var cortes = esc.slice(0, -1).map(function (e) { return e.b; });
    var cortina = null; if (!PLACA) { cortina = h('div', null, null, st); cortina.id = 'cortina'; }
    var entran = Array.prototype.slice.call(document.querySelectorAll('.esc [data-t]'));
    var marcas = Array.prototype.slice.call(document.querySelectorAll('.esc .mk'));
    window.render = function (t) {
      if (PLACA) { document.querySelectorAll('.placa-c .mk').forEach(function (m) { m.style.setProperty('--k', 1); }); if (o.placa) o.placa(); return; }
      esc.forEach(function (e) { var on = t >= e.a && t < e.b; e.n.style.opacity = on ? 1 : 0; e.n.style.visibility = on ? '' : 'hidden'; });
      var cx = -1500;
      cortes.forEach(function (b) { if (t > b - 0.36 && t < b + 0.36) cx = -1500 + eio(seg(t, b - 0.36, b + 0.36)) * (1500 + 1400); });
      cortina.style.transform = 'translateX(' + cx + 'px) skewX(-8deg)';
      entran.forEach(function (n) {
        var t0 = +n.dataset.t, k = t0 < 0 ? 1 : resorte(t - t0, 0.62, 12);
        n.style.opacity = clamp(k * 1.6);
        n.style.transform = n.dataset.fx === 'pop' ? 'scale(' + (0.6 + 0.4 * k) + ')' : 'translateY(' + (1 - k) * 36 + 'px)';
      });
      marcas.forEach(function (m) { var t0 = +(m.dataset.mk || 0); m.style.setProperty('--k', eio(seg(t, t0, t0 + 0.6))); });
      if (o.escena) o.escena(t);
    };
    var imgs = Array.prototype.map.call(document.images, function (im) { return im.complete ? 1 : new Promise(function (r) { im.onload = im.onerror = r; }); });
    window.LISTO = Promise.all([document.fonts ? document.fonts.ready : 1].concat(imgs)).then(function () { window.render(0); });
    if (!window.__RENDER_MODE__ && !PLACA) { var t0 = null; (function loop(ts) { if (t0 === null) t0 = ts; window.render(((ts - t0) / 1000) % TOTAL); requestAnimationFrame(loop); })(performance.now()); }
    else window.render(0);
  }
  return { PLACA: PLACA, clamp: clamp, seg: seg, eio: eio, eout: eout, resorte: resorte, el: el, h: h, cierre: cierre, init: init };
})();
