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
  document.querySelectorAll('[data-dialog]').forEach(function (c) {
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
  // Report pages: the contents sidebar marks the section being read
  var toc = document.querySelector('.rtoc');
  if (toc && 'IntersectionObserver' in window) {
    var links = {};
    toc.querySelectorAll('a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var a = links[e.target.id];
        if (!e.isIntersecting || !a) return;
        var ch = e.target.closest('.wchap');
        toc.querySelectorAll('a.is-current').forEach(function (x) { x.classList.remove('is-current'); });
        a.classList.add('is-current');
        if (ch && links[ch.id]) links[ch.id].classList.add('is-current');
        if (getComputedStyle(toc).position === 'sticky') {
          var t = a.offsetTop - toc.clientHeight / 2;
          toc.scrollTop = Math.max(0, t);
        }
      });
    }, { rootMargin: '-30% 0px -65% 0px' });
    document.querySelectorAll('.wchap, .wpart[id]').forEach(function (c) { spy.observe(c); });
  }
  // Report downloads: a short form (name, email, optional email opt-ins, agreement to the report terms) before the PDF.
  // The answers go to the report downloads sheet; this browser then skips the form for later downloads.
  var gate = document.getElementById('report-gate');
  function send(endpoint, data) {
    if (!endpoint) return Promise.resolve();
    return fetch(endpoint, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(data) }).catch(function () {});
  }
  function remembered() { try { return localStorage.getItem('mmtReportForm') === '1'; } catch (err) { return false; } }
  function startDownload(href) {
    var a = document.createElement('a');
    a.href = href; a.setAttribute('download', ''); document.body.appendChild(a); a.click(); a.remove();
  }
  if (gate && typeof gate.showModal === 'function') {
    var form = gate.querySelector('.gate-form'), done = gate.querySelector('.gate-done'), err = gate.querySelector('.gate-error');
    var current = null;
    document.addEventListener('click', function (ev) {
      var link = ev.target.closest('[data-gate]');
      if (!link) return;
      ev.preventDefault();
      current = { pdf: link.getAttribute('data-gate'), report: link.getAttribute('data-report') || 'Industry report' };
      if (remembered()) {
        send(gate.getAttribute('data-endpoint'), { action: 'download', report: current.report, page: location.pathname,
          terms_version: gate.getAttribute('data-terms'), returning: 'yes', email: localStorage.getItem('mmtReportEmail') || '' });
        startDownload(current.pdf);
        return;
      }
      gate.querySelector('.gate-report').textContent = current.report;
      form.hidden = false; done.hidden = true; err.hidden = true;
      gate.showModal();
      var first = form.querySelector('input[name="first_name"]');
      if (first) first.focus();
    });
    gate.querySelector('.gate-close').addEventListener('click', function () { gate.close(); });
    gate.addEventListener('click', function (ev) { if (ev.target === gate) gate.close(); });
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var f = form.elements, problem = '';
      if (!f.first_name.value.trim() || !f.last_name.value.trim()) problem = 'Please enter your first and last name.';
      else if (!f.email.checkValidity() || !f.email.value.trim()) problem = 'Please enter a valid email address.';
      else if (!f.terms.checked) problem = 'Please agree to the Report Terms and Conditions to download the report.';
      if (problem) { err.textContent = problem; err.hidden = false; return; }
      var data = { action: 'download', first_name: f.first_name.value.trim(), last_name: f.last_name.value.trim(),
        email: f.email.value.trim(), reports: f.reports.checked ? 'yes' : 'no', newsletter: f.newsletter.checked ? 'yes' : 'no',
        terms: 'yes', terms_version: gate.getAttribute('data-terms'), report: current.report, page: location.pathname,
        company_website: f.company_website.value };
      var btn = form.querySelector('.gate-submit');
      btn.disabled = true;
      send(gate.getAttribute('data-endpoint'), data).then(function () {
        try { localStorage.setItem('mmtReportForm', '1'); localStorage.setItem('mmtReportEmail', data.email); } catch (err2) {}
        btn.disabled = false;
        form.hidden = true; done.hidden = false;
        done.querySelector('.gate-file').href = current.pdf;
        startDownload(current.pdf);
      });
    });
  }
  // Email preferences: unsubscribe requests go to the same sheet.
  var prefs = document.querySelector('.prefs-form');
  if (prefs) {
    prefs.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var f = prefs.elements, perr = prefs.querySelector('.gate-error');
      if (!f.email.checkValidity() || !f.email.value.trim()) { perr.textContent = 'Please enter a valid email address.'; perr.hidden = false; return; }
      perr.hidden = true;
      send(prefs.getAttribute('data-endpoint'), { action: 'unsubscribe', email: f.email.value.trim(),
        reports: f.reports.checked ? 'yes' : 'no', newsletter: f.newsletter.checked ? 'yes' : 'no', company_website: f.company_website.value })
        .then(function () { prefs.querySelector('.prefs-done').hidden = false; });
    });
  }
  // The github.io sandbox says so, and links to the live preview (what "merge live" would publish).
  if (/\/about\/mid-market-practice\//.test(location.pathname) && /github\.io$/.test(location.hostname)) {
    var note = document.createElement('div');
    note.setAttribute('role', 'note');
    note.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:9999;display:flex;gap:16px;justify-content:center;align-items:center;flex-wrap:wrap;padding:9px 16px;background:#2b2725;color:#fff;font:600 12px/1.4 Arial,sans-serif;letter-spacing:.06em;text-transform:uppercase';
    note.innerHTML = '<span>Sandbox &middot; working copy, not live</span><a style="color:#d4b48c" href="' +
      location.pathname.replace(/\/about\/mid-market-practice\/.*/, '/about/live-preview/index.html') + '">Live preview &rarr;</a>';
    document.body.appendChild(note);
  }
})();
