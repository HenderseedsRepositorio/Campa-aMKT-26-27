/* Página de propuesta: copiar textos, repetir animaciones y filtrar piezas.
   Sin JS la página se lee completa: esto solo agrega comodidad. */
(function () {
  'use strict';

  function avisar(boton) {
    var original = boton.textContent;
    boton.textContent = 'Copiado ✓';
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

  document.addEventListener('click', function (e) {
    var copiar = e.target.closest('.pp-copy');
    if (copiar) {
      var el = document.getElementById(copiar.getAttribute('data-target'));
      if (!el) return;
      var texto = el.textContent;
      var alternativa = function () {
        seleccionar(el);
        try { if (document.execCommand('copy')) avisar(copiar); } catch (_) { /* queda seleccionado para copiar a mano */ }
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(texto).then(function () { avisar(copiar); }, alternativa);
      } else {
        alternativa();
      }
      return;
    }

    var repetir = e.target.closest('.pp-replay');
    if (repetir && window.HS) {
      var slide = document.getElementById(repetir.getAttribute('data-slide'));
      if (slide) window.HS.restart(slide);
    }
  });

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
})();
