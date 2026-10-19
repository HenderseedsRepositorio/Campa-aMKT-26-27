/* ==========================================================================
   HenderSeeds · runtime de animación de placas (Siembra 26/27)

   - En el navegador: cada .hs.anim corre en loop (dura data-dur segundos,
     queda quieta data-hold segundos y vuelve a empezar).
   - Con ?capture en la URL: no corre solo. Expone HS.seek(t) para que el
     script de video (scripts/render-videos.mjs) congele cualquier instante
     y saque cuadro por cuadro. Así el MP4 sale idéntico a lo que se ve.
   - Contadores: <span data-count="324" data-t0="2.1" data-d="1.2" data-dec="0"
     data-pre="+"> cuentan de data-from (0) a data-count con formato es-AR.
   - Sin JS o con "reducir movimiento": la placa se ve en su estado final.
   ========================================================================== */
(function () {
  'use strict';
  var params = new URLSearchParams(location.search);
  var CAPTURE = params.has('capture');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  function fmt(v, dec) {
    return v.toLocaleString('es-AR', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }
  function easeOut(p) { return 1 - Math.pow(1 - p, 3); }

  function counters(root, t) {
    var els = root.querySelectorAll('[data-count]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i], ds = el.dataset;
      var to = parseFloat(ds.count), from = parseFloat(ds.from || '0');
      var t0 = parseFloat(ds.t0 || '0'), d = parseFloat(ds.d || '1');
      var dec = parseInt(ds.dec || '0', 10);
      var p = Math.min(1, Math.max(0, (t - t0) / d));
      el.textContent = (ds.pre || '') + fmt(from + (to - from) * easeOut(p), dec) + (ds.post || '');
    }
  }

  function slides() { return Array.prototype.slice.call(document.querySelectorAll('.hs.anim')); }

  /* Congela todas las animaciones CSS del documento en el segundo t. */
  function seek(t) {
    document.getAnimations().forEach(function (a) { a.pause(); a.currentTime = t * 1000; });
    slides().forEach(function (s) { counters(s, t); });
  }

  function restart(s) {
    s.classList.remove('play');
    void s.offsetWidth;            // fuerza el reflow para reiniciar las animaciones
    s.classList.add('play');
    s._t0 = performance.now();
  }

  window.HS = {
    seek: seek,
    restart: restart,
    duration: function (s) { return parseFloat(s.dataset.dur || '10'); }
  };

  function boot() {
    if (CAPTURE) {
      document.documentElement.classList.add('capture');
      slides().forEach(function (s) { s.classList.add('play'); });
      seek(0);
      window.HS.ready = true;
      return;
    }
    if (reduce) return;              // queda el estado final, sin movimiento

    var visibles = new Set();
    var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { if (!visibles.has(e.target)) { visibles.add(e.target); restart(e.target); } }
        else { visibles.delete(e.target); }
      });
    }, { threshold: 0.25 }) : null;

    slides().forEach(function (s) { if (io) io.observe(s); else { visibles.add(s); restart(s); } });

    function loop(now) {
      visibles.forEach(function (s) {
        var dur = parseFloat(s.dataset.dur || '10'), hold = parseFloat(s.dataset.hold || '2.5');
        var t = (now - (s._t0 || now)) / 1000;
        if (t > dur + hold) { restart(s); t = 0; }
        counters(s, Math.min(t, dur));
      });
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
