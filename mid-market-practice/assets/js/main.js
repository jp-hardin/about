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

  // Transaction filters (sector chips on the transactions page, segment chips on sector pages)
  var grid = document.querySelector('[data-tomb-filter]');
  if (grid) {
    var key = grid.dataset.filterKey || 'sector';
    var limit = parseInt(grid.dataset.limit || '0', 10);
    var chips = document.querySelectorAll('.chip[data-filter]');
    var search = document.querySelector('.search');
    var count = document.querySelector('.result-count');
    var more = document.querySelector('.show-more');
    var items = grid.querySelectorAll('[data-sector]');
    var active = 'all';
    var expanded = !limit;
    var hash = decodeURIComponent(location.hash.replace('#', ''));
    chips.forEach(function (c) { if (hash && c.dataset.filter === hash) active = hash; });

    function apply() {
      var q = (search && search.value || '').trim().toLowerCase();
      var matched = 0, shown = 0;
      items.forEach(function (el) {
        var ok = (active === 'all' || (key === 'sector' ? el.dataset.sector.split(' ').indexOf(active) !== -1 : el.dataset[key] === active)) && (!q || el.dataset.text.indexOf(q) !== -1);
        if (ok) matched++;
        var visible = ok && (expanded || active !== 'all' || q || matched <= limit);
        el.hidden = !visible;
        if (visible) shown++;
      });
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.filter === active ? 'true' : 'false'); });
      if (count) count.textContent = shown < matched ? ('Showing ' + shown + ' of ' + matched + ' transactions') : (matched + (matched === 1 ? ' transaction' : ' transactions'));
      if (more) more.hidden = shown >= matched;
    }
    function select(v, scroll) {
      active = v;
      if (key === 'sector') history.replaceState(null, '', v === 'all' ? location.pathname : '#' + v);
      apply();
      if (scroll) grid.parentElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { select(c.dataset.filter); }); });
    document.querySelectorAll('.seg-jump').forEach(function (b) {
      b.addEventListener('click', function () { select(b.dataset.segment, true); });
    });
    if (more) more.addEventListener('click', function () { expanded = true; apply(); });
    if (search) search.addEventListener('input', apply);
    apply();
  }

  // Team: filter tabs and profile windows
  var teamTabs = document.querySelectorAll('.team-filter');
  teamTabs.forEach(function (t) {
    t.addEventListener('click', function () {
      var g = t.dataset.teamFilter;
      teamTabs.forEach(function (x) { x.setAttribute('aria-pressed', x === t ? 'true' : 'false'); });
      document.querySelectorAll('.team-card').forEach(function (c) { c.hidden = g !== 'all' && c.dataset.group !== g; });
    });
  });
  document.querySelectorAll('.team-card[data-dialog]').forEach(function (c) {
    c.addEventListener('click', function () {
      var d = document.getElementById(c.dataset.dialog);
      if (d && d.showModal) { d.showModal(); }
    });
  });
  document.querySelectorAll('.team-dialog').forEach(function (d) {
    d.querySelector('.team-close').addEventListener('click', function () { d.close(); });
    d.addEventListener('click', function (ev) {
      if (ev.target !== d) return;
      var r = d.getBoundingClientRect();
      if (ev.clientX < r.left || ev.clientX > r.right || ev.clientY < r.top || ev.clientY > r.bottom) d.close();
    });
  });
})();
