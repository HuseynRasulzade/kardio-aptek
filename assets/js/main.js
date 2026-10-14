(function () {
  // scroll progress + header state
  var bar = document.querySelector('.progress'), hdr = document.querySelector('header.site');
  var onScroll = function () {
    var h = document.documentElement, max = h.scrollHeight - h.clientHeight;
    if (bar) bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    if (hdr) hdr.classList.toggle('scrolled', h.scrollTop > 20);
  };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // cursor spotlight on cards
  document.addEventListener('pointermove', function (e) {
    var c = e.target.closest && e.target.closest('.card');
    if (!c) return;
    var r = c.getBoundingClientRect();
    c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    c.style.setProperty('--my', (e.clientY - r.top) + 'px');
  });

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // mobile menu
  var btn = $('.menu-btn'), nav = $('nav.main');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
  }

  // reveal on scroll
  var items = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .12 });
    items.forEach(function (i) { io.observe(i); });
  } else { items.forEach(function (i) { i.classList.add('in'); }); }

  // product filter + search
  var cards = $$('[data-cat]'), chips = $$('.chip'), search = $('#q'), empty = $('.empty');
  if (cards.length && (chips.length || search)) {
    var cat = 'all';
    var apply = function () {
      var q = (search && search.value || '').trim().toLowerCase(), shown = 0;
      cards.forEach(function (c) {
        var ok = (cat === 'all' || c.dataset.cat.split(' ').indexOf(cat) > -1) &&
                 (!q || c.textContent.toLowerCase().indexOf(q) > -1);
        c.style.display = ok ? '' : 'none';
        if (ok) shown++;
      });
      if (empty) empty.style.display = shown ? 'none' : 'block';
    };
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        chips.forEach(function (x) { x.classList.remove('active'); });
        c.classList.add('active'); cat = c.dataset.filter; apply();
      });
    });
    if (search) search.addEventListener('input', apply);
  }

  // lightbox
  var shots = $$('.shot');
  if (shots.length) {
    var lb = document.createElement('div');
    lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
    var d = document.body.dataset;
    lb.innerHTML = '<button class="x" aria-label="' + d.close + '">×</button><button class="prev" aria-label="' + d.prev + '">‹</button><img alt=""><p></p><button class="next" aria-label="' + d.next + '">›</button>';
    document.body.appendChild(lb);
    var img = $('img', lb), cap = $('p', lb), idx = 0;
    var show = function (i) {
      idx = (i + shots.length) % shots.length;
      img.src = shots[idx].dataset.full; img.alt = shots[idx].dataset.cap; cap.textContent = shots[idx].dataset.cap;
      lb.classList.add('open'); document.body.style.overflow = 'hidden';
    };
    var close = function () { lb.classList.remove('open'); document.body.style.overflow = ''; };
    shots.forEach(function (s, i) { s.addEventListener('click', function () { show(i); }); });
    $('.x', lb).addEventListener('click', close);
    $('.prev', lb).addEventListener('click', function () { show(idx - 1); });
    $('.next', lb).addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  // contact form -> WhatsApp (no backend needed)
  var form = $('#contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form);
      var d = form.dataset;
      var text = d.t1 + f.get('name') + '.\n' + d.t2 + ': ' + f.get('phone') + '\n' + d.t3 + ': ' + f.get('topic') + '\n\n' + f.get('message');
      window.open('https://wa.me/' + form.dataset.wa + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
    });
  }
})();
