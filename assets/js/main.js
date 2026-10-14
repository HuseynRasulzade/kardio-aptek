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
        if (ok) { c.dataset.pos = shown % 5; shown++; }
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


/* ======================= v3 interactions ======================= */
(function () {
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;

  // theme toggle
  var tb = $('.theme-btn');
  if (tb) tb.addEventListener('click', function () {
    var t = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem('theme', t); } catch (e) {}
  });

  // section tone shifting
  var tones = $$('[data-tone]');
  if (tones.length && 'IntersectionObserver' in window) {
    var to = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) document.body.dataset.tone = e.target.dataset.tone; });
    }, { rootMargin: '-45% 0px -45% 0px' });
    tones.forEach(function (t) { to.observe(t); });
  }

  // 3D hero scene
  var scene = $('#scene'), hero = $('.hero');
  if (scene && hero && !reduce) {
    var setLight = function (x, y) { scene.style.setProperty('--lx', x + '%'); scene.style.setProperty('--ly', y + '%'); };
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect(), nx = (e.clientX - r.left) / r.width - .5, ny = (e.clientY - r.top) / r.height - .5;
      scene.classList.remove('settle');
      scene.style.setProperty('--ry', (nx * 22).toFixed(2) + 'deg');
      scene.style.setProperty('--rx', (-ny * 16).toFixed(2) + 'deg');
      setLight(50 + nx * 80, 40 + ny * 80);
    });
    hero.addEventListener('pointerleave', function () {
      scene.classList.add('settle'); scene.style.setProperty('--ry', '0deg'); scene.style.setProperty('--rx', '0deg'); setLight(30, 20);
    });
    window.addEventListener('deviceorientation', function (e) {
      if (e.gamma == null) return;
      scene.style.setProperty('--ry', Math.max(-18, Math.min(18, e.gamma / 2.5)) + 'deg');
      scene.style.setProperty('--rx', Math.max(-14, Math.min(14, -(e.beta - 45) / 4)) + 'deg');
    });
    // gentle idle sway so it never looks static
    var t0 = performance.now();
    (function sway(now) {
      if (scene.classList.contains('settle')) {
        var t = (now - t0) / 1000;
        scene.style.setProperty('--ry', (Math.sin(t * .6) * 6).toFixed(2) + 'deg');
        scene.style.setProperty('--rx', (Math.cos(t * .5) * 3).toFixed(2) + 'deg');
      }
      requestAnimationFrame(sway);
    })(t0);
  }

  // parallax + scroll ECG + counters on scroll
  var giant = $('.hero-giant'), ecgs = $$('.scroll-ecg');
  ecgs.forEach(function (el) {
    var live = $('.live', el), len = live.getTotalLength();
    live.style.setProperty('--len', len); live.style.setProperty('--off', len); el._len = len; el._live = live;
  });
  var tick = function () {
    var y = window.scrollY, vh = window.innerHeight;
    if (giant && !reduce) giant.style.setProperty('--py', (y * -.12).toFixed(1) + 'px');
    ecgs.forEach(function (el) {
      var r = el.getBoundingClientRect(), p = 1 - Math.max(0, Math.min(1, (r.top - vh * .25) / (vh * .7)));
      el._live.style.setProperty('--off', (el._len * (1 - p)).toFixed(0));
    });
  };
  window.addEventListener('scroll', tick, { passive: true }); tick();

  // counters
  var counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; co.unobserve(e.target);
        var el = e.target, end = parseInt(el.dataset.count, 10), start = end > 1000 ? end - 40 : 0, t0 = performance.now();
        (function step(now) {
          var k = Math.min(1, (now - t0) / 1400), v = Math.round(start + (end - start) * (1 - Math.pow(1 - k, 3)));
          el.textContent = v; if (k < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, { threshold: .6 });
    counters.forEach(function (c) { co.observe(c); });
  }

  // calculator
  var calc = $('.calc');
  if (calc) {
    var sel = $('select', calc), out = $('.calc-days', calc), total = parseFloat(calc.dataset.total);
    var run = function () { var d = parseFloat(sel.value); out.textContent = d > 0 ? Math.floor(total / d) : '–'; };
    sel.addEventListener('change', run); run();
  }

  // quiz
  var qd = $('#quiz-data');
  if (qd) {
    var D = JSON.parse(qd.textContent), app = $('#quiz-app'), ans = {}, step = 0;
    var dots = function (n) { return '<div class="q-dots">' + [0, 1, 2].map(function (i) { return '<i class="' + (i <= n ? 'on' : '') + '"></i>'; }).join('') + '</div>'; };
    var render = function () {
      var h = '';
      if (step < 3) {
        var title = [D.goal, D.who, D.care][step], opts = [D.goals, D.whos, [['yes', D.yes], ['no', D.no]]][step];
        h = '<div class="q-slide">' + dots(step) + '<div class="q-step">' + D.step + ' ' + (step + 1) + ' / 3</div><h3 class="q-title">' + title + '</h3><div class="q-opts">' +
          opts.map(function (o) { return '<button class="q-opt" type="button" data-v="' + o[0] + '">' + o[1] + '</button>'; }).join('') + '</div>' +
          (step ? '<button class="q-back" type="button">← ' + D.back + '</button>' : '') + '</div>';
      } else {
        var list = D.products.filter(function (p) {
          if (p.cat !== ans.goal) return false;
          if (ans.who === 'adult') return true;
          if (p.kids == null) return false;
          return ans.who === 'teen' ? p.kids <= 12 : p.kids <= 11;
        });
        h = '<div class="q-slide"><div class="q-step">' + D.title + '</div>' + (ans.care === 'yes' ? '<div class="q-note"><b>!</b> ' + D.doctor + '</div>' : '') + '<div class="q-res">' +
          (list.length ? list.map(function (p) {
            return '<div class="q-card"><img src="' + p.img + '" alt=""><div><b>' + p.name + '</b><small>' + p.short + (p.kids != null && p.kids > 0 ? ' · ' + D.age + ' ' + p.kids + '+' : '') + '</small></div><a href="' + p.url + '">' + D.more + '</a></div>';
          }).join('') : '<div class="q-note">' + D.none + '</div>') +
          '</div><p class="q-disc">' + D.disc + '</p><button class="q-back" type="button" data-reset="1">↺ ' + D.again + '</button></div>';
      }
      app.innerHTML = h;
    };
    app.addEventListener('click', function (e) {
      var o = e.target.closest('.q-opt'), b = e.target.closest('.q-back');
      if (o) { ans[['goal', 'who', 'care'][step]] = o.dataset.v; step++; render(); }
      else if (b) { if (b.dataset.reset) { ans = {}; step = 0; } else step = Math.max(0, step - 1); render(); }
    });
    render();
  }

  // compare
  var cd = $('#cmp-data');
  if (cd) {
    var C = JSON.parse(cd.textContent), L = C.labels, picked = [];
    var bar = document.createElement('div'); bar.className = 'cmp-bar';
    bar.innerHTML = '<span></span><button class="go" type="button">' + L.compare + '</button><button class="clr" type="button">' + L.clear + '</button>';
    var modal = document.createElement('div'); modal.className = 'cmp-modal';
    modal.innerHTML = '<div class="cmp-box"><button class="cmp-x" type="button" aria-label="' + L.close + '">×</button><h2>' + L.title + '</h2><div class="cmp-body"></div></div>';
    document.body.appendChild(bar); document.body.appendChild(modal);
    var upd = function () {
      $('span', bar).textContent = picked.length + ' ' + L.bar;
      bar.classList.toggle('on', picked.length > 0);
      $('.go', bar).disabled = picked.length < 2; $('.go', bar).style.opacity = picked.length < 2 ? .5 : 1;
    };
    document.addEventListener('change', function (e) {
      var k = e.target.closest && e.target.closest('.cmp-chk'); if (!k) return;
      var s = k.dataset.slug;
      if (k.checked) { if (picked.length >= 3) { k.checked = false; alert(L.max); return; } picked.push(s); }
      else picked = picked.filter(function (x) { return x !== s; });
      upd();
    });
    $('.clr', bar).addEventListener('click', function () { picked = []; $$('.cmp-chk').forEach(function (c) { c.checked = false; }); upd(); });
    $('.go', bar).addEventListener('click', function () {
      if (picked.length < 2) return;
      var items = picked.map(function (s) { return C.items.filter(function (i) { return i.slug === s; })[0]; });
      var rows = ['kind', 'form', 'pack', 'use', 'ing', 'dose', 'storage', 'shelf'];
      var html = '<table class="cmp-tbl"><thead><tr><th></th>' + items.map(function (i) { return '<th>' + i.name + '</th>'; }).join('') + '</tr></thead><tbody>' +
        rows.map(function (r) { return '<tr><th>' + L[r] + '</th>' + items.map(function (i) { return '<td>' + i[r] + '</td>'; }).join('') + '</tr>'; }).join('') +
        '<tr><th></th>' + items.map(function (i) { return '<td><a class="btn btn-green btn-sm" href="' + i.url + '">' + L.open + '</a></td>'; }).join('') + '</tr></tbody></table>';
      $('.cmp-body', modal).innerHTML = html; modal.classList.add('open'); document.body.style.overflow = 'hidden';
    });
    var closeM = function () { modal.classList.remove('open'); document.body.style.overflow = ''; };
    $('.cmp-x', modal).addEventListener('click', closeM);
    modal.addEventListener('click', function (e) { if (e.target === modal) closeM(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeM(); });
    upd();
  }

  // custom cursor + magnetic buttons
  if (fine && !reduce) {
    var cur = document.createElement('div'); cur.className = 'cursor'; document.body.appendChild(cur);
    var cx = 0, cy = 0, tx = 0, ty = 0;
    document.addEventListener('pointermove', function (e) {
      tx = e.clientX; ty = e.clientY; cur.classList.add('on');
      cur.classList.toggle('big', !!e.target.closest('a,button,.chip,.shot,summary,select,label'));
    });
    document.addEventListener('pointerleave', function () { cur.classList.remove('on'); });
    (function loop() { cx += (tx - cx) * .2; cy += (ty - cy) * .2; cur.style.transform = 'translate(' + cx + 'px,' + cy + 'px)'; requestAnimationFrame(loop); })();
    $$('.btn,.fab a,.theme-btn').forEach(function (b) {
      b.classList.add('mag');
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * .22).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * .3).toFixed(1) + 'px)';
      });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });
  }
})();
