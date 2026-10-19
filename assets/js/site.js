/* Bruxa do Piercing · comportamento do site */
window.CONFIG = {
  instagram: 'bruxadopiercing',
  whatsapp: '5547991017599'
};

(function () {
  var doc = document.documentElement;
  var reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* abertura */
  requestAnimationFrame(function () { setTimeout(function () { doc.classList.add('pronto'); }, 60); });
  document.querySelectorAll('[data-ano]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* gaveta do menu (celular) */
  var nav = document.querySelector('.nav');
  var abrir = document.querySelector('.nav-abrir');
  var gaveta = document.querySelector('.nav-menu');
  if (abrir && gaveta) {
    function alternar(a) {
      abrir.setAttribute('aria-expanded', a);
      abrir.querySelector('span').textContent = a ? 'Fechar' : 'Menu';
      gaveta.classList.toggle('aberta', a);
      nav.classList.toggle('menu-aberto', a);
      document.body.style.overflow = a ? 'hidden' : '';
    }
    abrir.addEventListener('click', function () { alternar(abrir.getAttribute('aria-expanded') !== 'true'); });
    gaveta.addEventListener('click', function (e) { if (e.target.closest('a') && abrir.getAttribute('aria-expanded') === 'true') alternar(false); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape' && abrir.getAttribute('aria-expanded') === 'true') { alternar(false); abrir.focus(); } });
    matchMedia('(min-width: 1100px)').addEventListener('change', function (m) { if (m.matches) alternar(false); });
  }

  /* progresso e botão fixo */
  var prog = document.querySelectorAll('[data-prog]');
  var fixo = document.querySelector('.fixo');
  function aoRolar() {
    var t = Math.max(1, doc.scrollHeight - innerHeight);
    var p = Math.min(1, scrollY / t).toFixed(4);
    prog.forEach(function (el) { el.style.setProperty('--p', p); });
    if (fixo) fixo.classList.toggle('vis', scrollY > innerHeight * .7 && scrollY < t - 200);
  }
  addEventListener('scroll', aoRolar, { passive: true });
  aoRolar();

  /* abertura: luz de vela tremulando e poeira dourada subindo, bem devagar */
  var tela = document.querySelector('[data-luz]');
  if (tela && tela.getContext) {
    var cx = tela.getContext('2d');
    var W = 0, H = 0, dpr = 1, motes = [], ativo = true, t0 = performance.now();
    function medir() {
      var r = tela.getBoundingClientRect();
      dpr = Math.min(devicePixelRatio || 1, 2);
      W = r.width; H = r.height;
      tela.width = Math.round(W * dpr); tela.height = Math.round(H * dpr);
      cx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(80, W * H / 16000));
      motes = [];
      for (var k = 0; k < n; k++) motes.push(novo(true));
    }
    function novo(qualquerAltura) {
      var grande = Math.random() < .12;
      return {
        x: Math.random() * W, y: qualquerAltura ? Math.random() * H : H + 10,
        r: grande ? 2.2 + Math.random() * 2 : .5 + Math.random() * 1.3,
        v: 5 + Math.random() * 14, fase: Math.random() * 6.28, amp: 6 + Math.random() * 16,
        a: grande ? .08 + Math.random() * .08 : .25 + Math.random() * .5, pisca: .6 + Math.random() * 1.6
      };
    }
    function luz(x, y, raio, a) {
      var g = cx.createRadialGradient(x, y, 0, x, y, raio);
      g.addColorStop(0, 'rgba(201,140,78,' + a + ')');
      g.addColorStop(.45, 'rgba(160,100,52,' + a * .45 + ')');
      g.addColorStop(1, 'rgba(22,16,13,0)');
      cx.fillStyle = g;
      cx.fillRect(0, 0, W, H);
    }
    var ultimo = t0;
    function quadro(agora) {
      var t = (agora - t0) / 1000, dt = Math.min(.05, (agora - ultimo) / 1000);
      ultimo = agora;
      cx.clearRect(0, 0, W, H);
      cx.globalCompositeOperation = 'source-over';
      // tremor de vela: soma de senos lentos e um rápido bem fraco
      var tremor = .02 * Math.sin(t * 1.7) + .012 * Math.sin(t * 4.3 + 1) + .008 * Math.sin(t * 9.1);
      var grandeR = Math.max(W, H);
      luz(W * (.74 + .03 * Math.sin(t * .13)), H * (.32 + .04 * Math.cos(t * .11)), grandeR * .6, .2 + tremor);
      luz(W * (.1 + .03 * Math.cos(t * .09)), H * (.95 + .03 * Math.sin(t * .17)), grandeR * .45, .1 + tremor * .6);
      cx.globalCompositeOperation = 'lighter';
      for (var k = 0; k < motes.length; k++) {
        var m = motes[k];
        m.y -= m.v * dt;
        if (m.y < -10) { motes[k] = novo(false); continue; }
        var x = m.x + Math.sin(t * .4 + m.fase) * m.amp;
        var a = m.a * (.55 + .45 * Math.sin(t * m.pisca + m.fase));
        // some perto do topo, como poeira saindo da luz
        a *= Math.min(1, m.y / (H * .25));
        cx.fillStyle = 'rgba(240,200,150,' + Math.max(0, a).toFixed(3) + ')';
        cx.beginPath(); cx.arc(x, m.y, m.r, 0, 6.283); cx.fill();
      }
      if (ativo && !reduz) requestAnimationFrame(quadro);
    }
    medir();
    addEventListener('resize', function () { medir(); if (reduz) quadro(performance.now()); });
    if (reduz) quadro(performance.now());
    else {
      // só anima com a abertura visível e a aba aberta
      new IntersectionObserver(function (es) {
        var v = es[0].isIntersecting && !document.hidden;
        if (v && !ativo) { ativo = true; ultimo = performance.now(); requestAnimationFrame(quadro); }
        ativo = v;
      }).observe(tela);
      document.addEventListener('visibilitychange', function () {
        if (!document.hidden && !ativo && tela.getBoundingClientRect().bottom > 0) { ativo = true; ultimo = performance.now(); requestAnimationFrame(quadro); }
        else if (document.hidden) ativo = false;
      });
      requestAnimationFrame(quadro);
    }
  }

  /* revelar ao rolar */
  var io = 'IntersectionObserver' in window && !reduz ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' }) : null;
  function revelar(els) {
    els.forEach(function (el, i) {
      el.classList.add('rv');
      if (!io) { el.classList.add('vis'); return; }
      el.style.transitionDelay = (i % 4) * 70 + 'ms';
      io.observe(el);
    });
  }
  revelar(document.querySelectorAll('[data-rv]'));

  /* fotos */
  var OBRAS = window.OBRAS || [];
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }
  function src(o, w) { return 'assets/obras/' + o.id + '-' + w + '.webp'; }
  function fig(o, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'obra';
    b.dataset.i = i;
    b.innerHTML = '<img src="' + src(o, 640) + '" alt="' + esc(o.d) + '" loading="lazy" decoding="async" width="640" height="' + Math.round(640 / o.r) + '">' +
      '<span class="leg">' + esc(o.d) + '</span>';
    return b;
  }
  var lista = OBRAS;
  var grade = document.querySelector('[data-grade]');
  if (grade) {
    var limite = +grade.dataset.limite || 0;
    var filtros = document.querySelectorAll('.filtros button');
    var ordem = grade.dataset.ordem ? grade.dataset.ordem.split(',').map(function (n) {
      return OBRAS.filter(function (o) { return o.id === 'bp-' + n; })[0];
    }).filter(Boolean) : null;
    function aplicar(e, empurrar) {
      lista = ordem || (e && e !== 'todos' ? OBRAS.filter(function (o) { return o.e === e; }) : OBRAS);
      grade.innerHTML = '';
      (limite ? lista.slice(0, limite) : lista).forEach(function (o) { grade.appendChild(fig(o, OBRAS.indexOf(o))); });
      revelar(grade.querySelectorAll('.obra'));
      filtros.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.f === (e || 'todos')); });
      if (empurrar && history.replaceState) history.replaceState(null, '', e && e !== 'todos' ? '?cat=' + e : location.pathname);
    }
    filtros.forEach(function (b) {
      var n = b.dataset.f === 'todos' ? OBRAS.length : OBRAS.filter(function (o) { return o.e === b.dataset.f; }).length;
      var s = b.querySelector('sup'); if (s) s.textContent = n;
      b.addEventListener('click', function () { aplicar(b.dataset.f, true); });
    });
    var q = new URLSearchParams(location.search).get('cat');
    aplicar(['orelha', 'rosto', 'corpo', 'ensaios'].indexOf(q) > -1 ? q : 'todos');
  }

  /* lightbox */
  var lb = document.querySelector('.lb');
  if (lb) {
    var img = lb.querySelector('img');
    var leg = lb.querySelector('[data-leg]');
    var cont = lb.querySelector('[data-cont]');
    var atual = 0, origem = null;
    function mostrar(k) {
      var n = lista.length;
      atual = (k + n) % n;
      var o = lista[atual];
      img.style.opacity = 0;
      var novo = new Image();
      novo.onload = function () { img.src = novo.src; img.alt = o.d; img.style.opacity = 1; };
      novo.src = src(o, 1200);
      leg.textContent = o.d;
      cont.textContent = String(atual + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0');
    }
    function abrirLb(o) {
      origem = document.activeElement;
      mostrar(lista.indexOf(o));
      lb.classList.add('aberto');
      lb.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      lb.querySelector('[data-fechar]').focus();
    }
    function fechar() {
      lb.classList.remove('aberto');
      lb.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (origem) origem.focus();
    }
    document.addEventListener('click', function (e) {
      var b = e.target.closest('.obra');
      if (!b) return;
      if (b.dataset.id) {
        lista = OBRAS.filter(function (o) { return o.e === 'ensaios'; });
        abrirLb(lista.filter(function (o) { return o.id === b.dataset.id; })[0]);
      } else abrirLb(OBRAS[+b.dataset.i]);
    });
    lb.querySelector('[data-fechar]').addEventListener('click', fechar);
    lb.querySelector('[data-ant]').addEventListener('click', function () { mostrar(atual - 1); });
    lb.querySelector('[data-prox]').addEventListener('click', function () { mostrar(atual + 1); });
    lb.querySelector('.lb-palco').addEventListener('click', function (e) { if (e.target === e.currentTarget) fechar(); });
    addEventListener('keydown', function (e) {
      if (!lb.classList.contains('aberto')) return;
      if (e.key === 'Escape') fechar();
      if (e.key === 'ArrowLeft') mostrar(atual - 1);
      if (e.key === 'ArrowRight') mostrar(atual + 1);
    });
    var x0 = null;
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) mostrar(atual + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  /* agendamento: monta a mensagem e abre o WhatsApp */
  var form = document.querySelector('[data-agendar]');
  if (form) {
    var previa = form.querySelector('.previa');
    var soPerf = form.querySelectorAll('[data-so-perf]');
    var q = new URLSearchParams(location.search);
    var c = q.get('cidade') && form.querySelector('[data-c="' + q.get('cidade') + '"]');
    if (c) c.checked = true;
    var t = q.get('tipo') && form.querySelector('[data-t="' + q.get('tipo') + '"]');
    if (t) t.checked = true;
    function perf() {
      var s = form.querySelector('input[name=tipo]:checked');
      return !s || s.hasAttribute('data-perf');
    }
    function texto() {
      var f = new FormData(form);
      var l = ['Oi, Moni! Vim pelo site e queria agendar.', ''];
      if (f.get('nome')) l.push('Nome: ' + f.get('nome'));
      if (f.get('cidade')) l.push('Onde: ' + f.get('cidade'));
      if (f.get('tipo')) l.push('Quero: ' + f.get('tipo'));
      if (perf() && f.get('local')) l.push('Perfuração: ' + f.get('local'));
      if (perf() && f.get('primeira')) l.push(f.get('primeira'));
      var per = f.getAll('periodo');
      if (per.length) l.push('Período: ' + per.join(', '));
      if (f.get('obs')) { l.push(''); l.push('Observações: ' + f.get('obs')); }
      return l.join('\n');
    }
    function atualizar() {
      var p = perf();
      soPerf.forEach(function (el) { el.hidden = !p; });
      previa.textContent = texto();
    }
    form.addEventListener('input', atualizar);
    form.addEventListener('change', atualizar);
    atualizar();
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var erro = form.querySelector('.erro');
      if (erro) erro.remove();
      var faltando = !form.nome.value.trim() ? form.nome
        : !form.querySelector('input[name=cidade]:checked') ? form.querySelector('input[name=cidade]')
        : !form.querySelector('input[name=tipo]:checked') ? form.querySelector('input[name=tipo]') : null;
      if (faltando) {
        var p = document.createElement('p');
        p.className = 'erro';
        p.setAttribute('role', 'alert');
        p.textContent = faltando.name === 'nome' ? 'Escreva seu nome para a Moni saber com quem está falando.' : faltando.name === 'cidade' ? 'Escolha a cidade.' : 'Escolha o que você quer.';
        faltando.closest('.campo').after(p);
        faltando.focus();
        return;
      }
      window.open('https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(texto()), '_blank', 'noopener');
    });
  }
})();
