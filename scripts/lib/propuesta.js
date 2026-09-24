/* Página de propuesta: copiar textos, repetir animaciones, filtrar piezas y
   revisarlas (aprobar / cambiar / descartar). Sin JS la página se lee completa:
   esto solo agrega comodidad. Las marcas se guardan en este navegador. */
(function () {
  'use strict';

  function avisar(boton, texto) {
    var original = boton.getAttribute('data-original') || boton.textContent;
    boton.setAttribute('data-original', original);
    boton.textContent = texto || 'Copiado ✓';
    boton.classList.add('is-ok');
    setTimeout(function () { boton.textContent = original; boton.classList.remove('is-ok'); }, 1800);
  }

  function seleccionar(el) {
    var rango = document.createRange();
    rango.selectNodeContents(el);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(rango);
  }

  function copiar(texto, boton, elParaSeleccionar) {
    var alternativa = function () {
      if (elParaSeleccionar) { elParaSeleccionar.hidden = false; seleccionar(elParaSeleccionar); }
      try { if (document.execCommand('copy')) avisar(boton); } catch (_) { /* queda seleccionado para copiar a mano */ }
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(texto).then(function () { avisar(boton); }, alternativa);
    } else {
      alternativa();
    }
  }

  /* ── copiar textos y repetir animaciones ─────────────────────── */
  document.addEventListener('click', function (e) {
    var boton = e.target.closest('.pp-copy[data-target]');
    if (boton) {
      var el = document.getElementById(boton.getAttribute('data-target'));
      if (el) copiar(el.textContent, boton, el);
      return;
    }
    var repetir = e.target.closest('.pp-replay');
    if (repetir && window.HS) {
      var slide = document.getElementById(repetir.getAttribute('data-slide'));
      if (slide) window.HS.restart(slide);
    }
  });

  /* ── filtros ─────────────────────────────────────────────────── */
  var filtros = document.querySelectorAll('.pp-filtro');
  Array.prototype.forEach.call(filtros, function (boton) {
    boton.addEventListener('click', function () {
      var f = boton.getAttribute('data-f');
      Array.prototype.forEach.call(filtros, function (b) { b.setAttribute('aria-pressed', b === boton ? 'true' : 'false'); });
      Array.prototype.forEach.call(document.querySelectorAll('.pp-pieza'), function (p) {
        p.hidden = !(f === 'todos' || p.getAttribute('data-grupo') === f);
      });
    });
  });

  /* ── modo aprobación ─────────────────────────────────────────── */
  var CLAVE = 'hs-aprobacion-2627';
  var estado = {};
  try { estado = JSON.parse(localStorage.getItem(CLAVE) || '{}') || {}; } catch (_) { estado = {}; }
  function guardar() { try { localStorage.setItem(CLAVE, JSON.stringify(estado)); } catch (_) { /* sin almacenamiento: vale para esta visita */ } }

  var piezas = Array.prototype.slice.call(document.querySelectorAll('.pp-pieza'));
  var barra = document.getElementById('pp-barra');
  var preRes = document.getElementById('pp-resumen-txt');
  var idDe = function (p) { return p.id.replace(/^p-/, ''); };

  function pintar() {
    var n = { ok: 0, cambiar: 0, no: 0, pend: 0 };
    piezas.forEach(function (p) {
      var id = idDe(p);
      var e = estado[id] && estado[id].estado;
      if (e) { p.setAttribute('data-estado', e); n[e]++; } else { p.removeAttribute('data-estado'); n.pend++; }
      Array.prototype.forEach.call(p.querySelectorAll('.pp-ap'), function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-estado') === e ? 'true' : 'false');
      });
      var nota = p.querySelector('.pp-nota-ap');
      if (nota) {
        nota.hidden = e !== 'cambiar';
        var ta = nota.querySelector('textarea');
        if (ta && document.activeElement !== ta) ta.value = (estado[id] && estado[id].nota) || '';
      }
      Array.prototype.forEach.call(document.querySelectorAll('.pp-sem-items li[data-pieza="' + id + '"]'), function (li) {
        if (e) li.setAttribute('data-estado', e); else li.removeAttribute('data-estado');
      });
    });
    ['ok', 'cambiar', 'no', 'pend'].forEach(function (k) {
      var el = document.getElementById('n-' + k);
      if (el) el.textContent = n[k];
    });
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('.pp-ap');
    if (!b) return;
    var id = b.closest('.pp-aprob').getAttribute('data-id');
    var nuevo = b.getAttribute('data-estado');
    var actual = estado[id] && estado[id].estado;
    if (actual === nuevo) delete estado[id];
    else estado[id] = { estado: nuevo, nota: (estado[id] && estado[id].nota) || '' };
    guardar();
    pintar();
    if (nuevo === 'cambiar' && estado[id]) {
      var ta = document.getElementById('nota-' + id);
      if (ta) ta.focus();
    }
  });

  document.addEventListener('input', function (e) {
    if (!e.target.matches || !e.target.matches('.pp-nota-ap textarea')) return;
    var id = e.target.id.replace(/^nota-/, '');
    if (!estado[id]) estado[id] = { estado: 'cambiar', nota: '' };
    estado[id].nota = e.target.value;
    guardar();
  });

  function resumen() {
    var g = { ok: [], cambiar: [], no: [], pend: [] };
    piezas.forEach(function (p) {
      var nombre = p.getAttribute('data-nombre');
      var e = estado[idDe(p)];
      if (!e) g.pend.push(nombre);
      else if (e.estado === 'cambiar') g.cambiar.push(nombre + (e.nota && e.nota.trim() ? ' — ' + e.nota.trim() : ''));
      else g[e.estado].push(nombre);
    });
    var t = ['Relanzamiento Siembra 26/27 — revisión del ' + new Date().toLocaleDateString('es-AR'), ''];
    function bloque(titulo, lista) {
      t.push(titulo + ' (' + lista.length + ')');
      lista.forEach(function (x) { t.push('• ' + x); });
      t.push('');
    }
    bloque('✓ Aprobadas', g.ok);
    bloque('✎ Para cambiar', g.cambiar);
    bloque('✕ Descartadas', g.no);
    bloque('○ Sin revisar', g.pend);
    return t.join('\n').trim();
  }

  var btnRes = document.getElementById('pp-resumen');
  if (btnRes) btnRes.addEventListener('click', function () {
    var txt = resumen();
    preRes.textContent = txt;
    copiar(txt, btnRes, preRes);
  });

  var btnLimpiar = document.getElementById('pp-limpiar');
  var armado = false;
  if (btnLimpiar) btnLimpiar.addEventListener('click', function () {
    if (!armado) {           // doble toque: evita borrar todo por error
      armado = true;
      btnLimpiar.textContent = '¿Seguro? Tocá de nuevo';
      setTimeout(function () { armado = false; btnLimpiar.textContent = 'Borrar marcas'; }, 3000);
      return;
    }
    armado = false;
    btnLimpiar.textContent = 'Borrar marcas';
    estado = {};
    guardar();
    pintar();
    preRes.hidden = true;
  });

  if (barra && piezas.length) { barra.hidden = false; document.body.classList.add('con-barra'); }
  pintar();
})();
