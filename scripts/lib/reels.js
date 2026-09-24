/* Página "Reels para arrancar": copiar textos, repetir, ver la interfaz de Instagram
   encima y marcar cada reel (aprobar / cambiar / descartar). Sin JS se lee completa.
   Las marcas se guardan en este navegador. */
(function () {
  'use strict';

  function avisar(boton, texto) {
    var original = boton.getAttribute('data-original') || boton.textContent;
    boton.setAttribute('data-original', original);
    boton.textContent = texto || 'Copiado ✓';
    boton.classList.add('is-ok');
    setTimeout(function () { boton.textContent = original; boton.classList.remove('is-ok'); }, 1800);
  }
  function copiar(texto, boton, el) {
    var alternativa = function () {
      if (el) {
        var r = document.createRange(); r.selectNodeContents(el);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      }
      try { if (document.execCommand('copy')) avisar(boton); } catch (_) { /* queda seleccionado */ }
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(texto).then(function () { avisar(boton); }, alternativa);
    else alternativa();
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-copiar]');
    if (b) { var el = document.getElementById(b.getAttribute('data-copiar')); if (el) copiar(el.textContent, b, el); return; }
    var r = e.target.closest('[data-repetir]');
    if (r && window.HS) { var s = document.getElementById(r.getAttribute('data-repetir')); if (s) window.HS.restart(s); return; }
    var ig = e.target.closest('[data-ig]');
    if (ig) {
      var cel = document.getElementById(ig.getAttribute('data-ig'));
      var on = !cel.classList.contains('con-ig');
      cel.classList.toggle('con-ig', on);
      ig.setAttribute('aria-pressed', on ? 'true' : 'false');
    }
  });

  /* ── marcas ─────────────────────────────────────────────────────── */
  var CLAVE = 'hs-reels-2627';
  var estado = {};
  try { estado = JSON.parse(localStorage.getItem(CLAVE) || '{}') || {}; } catch (_) { estado = {}; }
  function guardar() { try { localStorage.setItem(CLAVE, JSON.stringify(estado)); } catch (_) { /* vale para esta visita */ } }
  var reels = Array.prototype.slice.call(document.querySelectorAll('.rp-reel'));

  function pintar() {
    var n = { ok: 0, cambiar: 0, no: 0, pend: 0 };
    reels.forEach(function (r) {
      var id = r.getAttribute('data-id');
      var e = estado[id] && estado[id].estado;
      if (e) { r.setAttribute('data-estado', e); n[e]++; } else { r.removeAttribute('data-estado'); n.pend++; }
      Array.prototype.forEach.call(r.querySelectorAll('.rp-ap'), function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-estado') === e ? 'true' : 'false');
      });
      var nota = r.querySelector('.rp-nota');
      if (nota) {
        nota.hidden = e !== 'cambiar';
        var ta = nota.querySelector('textarea');
        if (ta && document.activeElement !== ta) ta.value = (estado[id] && estado[id].nota) || '';
      }
      var link = document.querySelector('.rp-orden a[href="#' + r.id + '"]');
      if (link) { if (e) link.setAttribute('data-estado', e); else link.removeAttribute('data-estado'); }
    });
    ['ok', 'cambiar', 'no', 'pend'].forEach(function (k) { var el = document.getElementById('n-' + k); if (el) el.textContent = n[k]; });
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('.rp-ap');
    if (!b) return;
    var id = b.closest('.rp-reel').getAttribute('data-id');
    var nuevo = b.getAttribute('data-estado');
    if (estado[id] && estado[id].estado === nuevo) delete estado[id];
    else estado[id] = { estado: nuevo, nota: (estado[id] && estado[id].nota) || '' };
    guardar(); pintar();
    if (nuevo === 'cambiar' && estado[id]) { var ta = document.getElementById('nota-' + id); if (ta) ta.focus(); }
  });
  document.addEventListener('input', function (e) {
    if (!e.target.matches || !e.target.matches('.rp-nota textarea')) return;
    var id = e.target.id.replace(/^nota-/, '');
    if (!estado[id]) estado[id] = { estado: 'cambiar', nota: '' };
    estado[id].nota = e.target.value;
    guardar();
  });

  function resumen() {
    var g = { ok: [], cambiar: [], no: [], pend: [] };
    reels.forEach(function (r) {
      var nombre = r.getAttribute('data-nombre');
      var e = estado[r.getAttribute('data-id')];
      if (!e) g.pend.push(nombre);
      else if (e.estado === 'cambiar') g.cambiar.push(nombre + (e.nota && e.nota.trim() ? ' — ' + e.nota.trim() : ''));
      else g[e.estado].push(nombre);
    });
    var t = ['Reels Siembra 26/27 — revisión del ' + new Date().toLocaleDateString('es-AR'), ''];
    [['✓ Aprobados', g.ok], ['✎ Para cambiar', g.cambiar], ['✕ Descartados', g.no], ['○ Sin revisar', g.pend]].forEach(function (b) {
      t.push(b[0] + ' (' + b[1].length + ')'); b[1].forEach(function (x) { t.push('• ' + x); }); t.push('');
    });
    return t.join('\n').trim();
  }
  var btn = document.getElementById('rp-resumen');
  var pre = document.getElementById('rp-resumen-txt');
  if (btn) btn.addEventListener('click', function () { var txt = resumen(); pre.textContent = txt; copiar(txt, btn, pre); });

  var barra = document.getElementById('rp-barra');
  if (barra) barra.hidden = false;
  pintar();
})();
