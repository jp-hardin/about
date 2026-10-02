(function () {
  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { nav.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  }

  // Reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('is-in'); });
  }

  // YouTube click-to-play (keeps pages fast)
  document.querySelectorAll('.yt[data-id]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + btn.dataset.id + '?autoplay=1&rel=0';
      f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen = true;
      f.title = btn.getAttribute('aria-label') || 'Video';
      btn.replaceWith(f);
    });
  });

  // Transaction filters
  var grid = document.querySelector('[data-tomb-filter]');
  if (grid) {
    var chips = document.querySelectorAll('.chip[data-sector]');
    var search = document.querySelector('.search');
    var count = document.querySelector('.result-count');
    var items = grid.querySelectorAll('.tomb');
    var active = 'all';
    var hash = location.hash.replace('#', '');
    if (hash && document.querySelector('.chip[data-sector="' + hash + '"]')) active = hash;

    function apply() {
      var q = (search && search.value || '').trim().toLowerCase();
      var shown = 0;
      items.forEach(function (el) {
        var ok = (active === 'all' || el.dataset.sector === active) && (!q || el.dataset.text.indexOf(q) !== -1);
        el.hidden = !ok;
        if (ok) shown++;
      });
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.sector === active ? 'true' : 'false'); });
      if (count) count.textContent = shown + (shown === 1 ? ' transaction' : ' transactions');
    }
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        active = c.dataset.sector;
        history.replaceState(null, '', active === 'all' ? location.pathname : '#' + active);
        apply();
      });
    });
    if (search) search.addEventListener('input', apply);
    apply();
  }
})();
