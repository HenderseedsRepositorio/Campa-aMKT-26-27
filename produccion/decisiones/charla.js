/* Motor de la onda "charla de lote" (decisiones 06–10). Cada reel es solo datos:
   C.init({ num, tema, escenas: [{ a, b, txt, fs, obj }], cierre: { a, b, regla, humana, src }, placa: {...} })
   txt: palabras separadas por espacio; *palabra* va en ámbar; | corta la línea.
   La escena 1 se lee entera desde el cuadro 0; de la 2 en adelante la frase entra palabra por palabra.
   ?formato=placa → la placa 4:5 (placa.titulo, placa.filas [[pregunta, respuesta]], placa.regla). */
var C = (function () {
  function clamp(v) { return Math.max(0, Math.min(1, v)); }
  function seg(t, a, b) { return clamp((t - a) / (b - a)); }
  function eio(v) { v = clamp(v); return v < 0.5 ? 4 * v * v * v : 1 - Math.pow(-2 * v + 2, 3) / 2; }
  // Resorte amortiguado: sobrepaso leve y asentamiento rápido. u = segundos desde que arranca.
  function resorte(u, z, w) { if (u <= 0) return 0; z = z || 0.65; w = w || 13; var wd = w * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w * u) * (Math.cos(wd * u) + z * w / wd * Math.sin(wd * u)); }
  function h(tag, cls, html, p) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (p) p.appendChild(e); return e; }
  var PLACA = new URLSearchParams(location.search).get('formato') === 'placa';
  var ICONO_DM = '<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="#0A0A0A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20.5l1.6-5.3A8.4 8.4 0 1 1 21 11.5z"/></svg>';
  var ICONO_WA = '<svg viewBox="0 0 32 32" width="34" height="34" fill="#25D366"><path d="M16 .4C7.4.4.5 7.3.5 15.9c0 2.8.7 5.4 2 7.8L.4 31.6l8.1-2.1c2.3 1.2 4.8 1.9 7.5 1.9 8.6 0 15.5-7 15.5-15.5S24.6.4 16 .4zm0 28.3c-2.4 0-4.7-.6-6.7-1.8l-.5-.3-4.8 1.3 1.3-4.7-.3-.5c-1.3-2.1-2-4.5-2-7 0-7.2 5.9-13.1 13.1-13.1 3.5 0 6.8 1.4 9.3 3.8 2.5 2.5 3.8 5.8 3.8 9.3 0 7.2-5.9 13-13.2 13zm7.2-9.8c-.4-.2-2.3-1.1-2.7-1.3-.4-.1-.6-.2-.9.2-.3.4-1 1.3-1.2 1.5-.2.2-.4.3-.8.1-.4-.2-1.7-.6-3.2-2-1.2-1.1-2-2.4-2.2-2.8-.2-.4 0-.6.2-.8.2-.2.4-.4.6-.7.2-.2.3-.4.4-.7.1-.3.1-.5 0-.7-.1-.2-.9-2.2-1.3-3-.3-.8-.7-.7-.9-.7h-.8c-.3 0-.7.1-1.1.5-.4.4-1.4 1.4-1.4 3.4s1.5 3.9 1.7 4.2c.2.3 2.9 4.4 7 6.2 1 .4 1.8.7 2.4.9 1 .3 1.9.3 2.6.2.8-.1 2.3-.9 2.7-1.9.3-.9.3-1.7.2-1.9-.1-.2-.4-.3-.8-.5z"/></svg>';

  // "¿Cuántos *qq/ha* necesitás?" → spans (una por palabra) y <br> en cada |
  function frase(txt) {
    return txt.split(' ').map(function (w) {
      if (w === '|') return '<br>';
      var a = /^\*.*\*[.,:?]?$/.test(w), limpio = w.replace(/\*/g, '');
      return '<span' + (a ? ' class="a"' : '') + '>' + limpio + '</span>';
    }).join(' ');
  }

  function init(o) {
    var st = document.getElementById('stage');
    if (PLACA) st.classList.add('placa');
    h('div', 'kick', 'HenderSeeds · <b>' + o.num + '</b> · ' + o.tema, st);
    var av = h('div', 'avance', '<i></i>', st).firstChild;
    var esc = o.escenas.map(function (e, i) {
      var n = h('div', 'esc', null, st), f = h('div', 'frase', frase(e.txt), n);
      if (e.fs) f.style.setProperty('--fs', e.fs + 'px');
      var obj = e.obj ? h('div', 'obj', e.obj, n) : null;
      return { e: e, i: i, n: n, ws: Array.prototype.slice.call(f.querySelectorAll('span')), obj: obj };
    });
    var c = o.cierre;
    var tar = h('div', 'tarjeta', '<img src="../../docs/assets/logo-hs-navy-hd.png" alt="HenderSeeds">' +
      '<div class="r">' + c.regla + '</div>' + (c.humana ? '<div class="h">' + c.humana + '</div>' : '') +
      '<div class="dm">' + ICONO_DM + 'Mandanos un DM</div><div class="wa">' + ICONO_WA + ' WhatsApp 2314 53-0691</div>' +
      (c.src ? '<div class="src">' + c.src + '</div>' : ''), st);
    var hijos = Array.prototype.slice.call(tar.children);
    var p = o.placa;
    h('div', 'placa-c ficha', '<div class="pk">Decisión ' + o.num + ' · ' + o.tema + '</div><div class="pt"' + (p.fs ? ' style="font-size:' + p.fs + 'px"' : '') + '>' + p.titulo + '</div>' +
      '<div class="filas">' + p.filas.map(function (f) { return '<div class="fila"><span class="p">' + f[0] + '</span><span class="x">' + f[1] + '</span></div>'; }).join('') + '</div>' +
      '<div class="regla"><span class="rt">LA REGLA</span><p>' + p.regla + '</p></div>' +
      '<div class="pcta">' + (p.cta || 'Pasamos por tu lote. <b>Mandanos un DM</b> · WA 2314 53-0691') + '</div>' +
      (p.src ? '<div class="psrc">' + p.src + '</div>' : ''), st);

    window.REEL_DURACION = c.b;
    window.render = function (t) {
      if (PLACA) return;
      av.style.transform = 'scaleX(' + clamp(t / c.a) + ')';
      esc.forEach(function (s) {
        var a = s.e.a, b = s.e.b, on = (s.i === 0 ? t < b : t >= a && t < b);
        s.n.style.visibility = on ? '' : 'hidden';
        if (!on) return;
        var ke = s.i === esc.length - 1 ? 0 : eio(seg(t, b - 0.28, b));   // la frase se va hacia arriba
        s.n.style.opacity = 1 - ke; s.n.style.transform = 'translateY(' + (-50 * ke) + 'px)';
        s.ws.forEach(function (w, j) {
          if (s.i === 0) { var k0 = resorte(t + 0.22 - j * 0.05, 0.5, 14); w.style.opacity = 1; w.style.transform = 'translateY(' + (1 - k0) * 16 + 'px)'; return; }
          var k = resorte(t - a - 0.12 - j * 0.11, 0.6, 13);
          w.style.opacity = clamp(k * 1.8); w.style.transform = 'translateY(' + (1 - k) * 50 + 'px)';
        });
        if (s.obj) {
          var t0 = s.i === 0 ? 0.5 : a + 0.27 + s.ws.length * 0.11, ko = resorte(t - t0, 0.55, 12);
          s.obj.style.opacity = clamp(ko * 1.8); s.obj.style.transform = 'translateY(' + (1 - ko) * 40 + 'px)';
        }
        if (s.e.anima) s.e.anima(t, s);
      });
      var kt = eio(seg(t, c.a - 0.1, c.a + 0.45));
      tar.style.transform = 'translateY(' + (1 - kt) * 100 + '%)';
      hijos.forEach(function (n, i) { var k = resorte(t - c.a - 0.3 - i * 0.12, 0.62, 12); n.style.opacity = clamp(k * 1.6); n.style.transform = 'translateY(' + (1 - k) * 24 + 'px)'; });
    };
    var imgs = Array.prototype.map.call(document.images, function (im) { return im.complete ? 1 : new Promise(function (r) { im.onload = im.onerror = r; }); });
    window.LISTO = Promise.all([document.fonts ? document.fonts.ready : 1].concat(imgs)).then(function () { window.render(0); });
    if (!window.__RENDER_MODE__ && !PLACA) { var t0 = null; (function loop(ts) { if (t0 === null) t0 = ts; window.render(((ts - t0) / 1000) % c.b); requestAnimationFrame(loop); })(performance.now()); }
    else window.render(0);
  }
  return { PLACA: PLACA, clamp: clamp, seg: seg, eio: eio, resorte: resorte, h: h, init: init };
})();
