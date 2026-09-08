/* Scroll behaviour for the landing page.
 *
 * One job: a visitor opens the page and sees the hero and nothing else. Scroll
 * once and the football field is there, with the highlights arriving one at a
 * time rather than all at once. Scroll again and the third section follows.
 *
 * Everything here is presentation. If this file never loads, or the visitor
 * prefers reduced motion, every section is still on the page and still reads.
 */
(function () {
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const items = Array.prototype.slice.call(document.querySelectorAll('.rv'));
  if (!items.length) return;

  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }

  /* Stagger is per-group, not per-page: each section's items count from zero, so
     the fourth highlight in section two does not inherit a delay from section
     one and arrive after the reader has already moved on. */
  const io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      const el = e.target;
      const group = el.closest('.snap') || document.body;
      const peers = Array.prototype.slice.call(group.querySelectorAll('.rv'));
      const i = Math.max(0, peers.indexOf(el));
      el.style.transitionDelay = Math.min(i * 110, 660) + 'ms';
      el.classList.add('in');
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

  items.forEach(function (el) { io.observe(el); });

  /* The cue under the hero is only useful before the first scroll. */
  const cue = document.querySelector('.scroll-cue');
  if (cue) {
    window.addEventListener('scroll', function () {
      cue.style.opacity = window.scrollY > 60 ? '0' : '1';
    }, { passive: true });
    cue.style.transition = 'opacity .3s ease';
  }
})();


/* Hero field opening animation: bars grow from their midpoint, numbers fade in
   behind them, staggered top to bottom. Skipped under prefers-reduced-motion. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var field = document.querySelector('.hero-field');
  if (!field || reduce || !('IntersectionObserver' in window)) return;
  field.classList.add('hf-animate');
  field.querySelectorAll('.hf-row').forEach(function (row, i) {
    row.querySelectorAll('.hf-bar, .hf-track > b').forEach(function (el) {
      el.style.setProperty('--d', (i * 90) + 'ms');
    });
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      requestAnimationFrame(function () { field.classList.add('hf-play'); });
      io.disconnect();
    });
  }, { threshold: 0.3 });
  io.observe(field);
})();

/* Phones, 8-Sep-2026 (fourth phone pass): the moves in the DOM that make the four snapping pages of
   landing-mobile.css out of the desktop's markup. Nothing runs above 640px, nothing changes in
   index.html, and without this script the page still reads top to bottom in the desktop's order.
     page 2  the story block (eyebrow, title, lede) moves above the field card and its five steps
             move below it, so a phone reads title, picture, explanation, button
     page 1  the privacy sentence under the button folds behind an "i" (Daniil, 8 Sep: it should
             not be there by default); the quiz screen still shows it in full before question one
     page 4  page 3's button, the reviewing-team strip and the footer gather into one last page,
             and the two paragraphs of small print fold behind "Your data" and "About this service" */
(function () {
  if (!(window.matchMedia && window.matchMedia('(max-width: 640px)').matches)) return;
  var vis = document.querySelector('#screen-hero .hero-vis');
  var story = document.querySelector('#screen-hero .hero-story');
  var card = vis && vis.querySelector('.ffcard');
  var cta = vis && vis.querySelector('.story-cta');
  if (vis && story && card) {
    var steps = story.querySelector('.steps');
    vis.insertBefore(story, card);
    if (steps) { if (cta) vis.insertBefore(steps, cta); else vis.appendChild(steps); }
    vis.classList.add('ph-page');
  }
  var read = document.getElementById('read');
  if (read) read.classList.add('ph-page');

  /* the "i" after "About four minutes · no card" */
  var privacy = document.getElementById('privacy-line-hero');
  var note = privacy && privacy.parentElement && privacy.parentElement.querySelector('.cta-note');
  if (privacy && note) {
    var info = document.createElement('button');
    info.type = 'button'; info.className = 'ph-info'; info.textContent = 'i';
    info.setAttribute('aria-expanded', 'false');
    info.setAttribute('aria-controls', 'privacy-line-hero');
    info.setAttribute('aria-label', 'What we receive and what stays in your browser');
    info.addEventListener('click', function () {
      var open = privacy.classList.toggle('open');
      info.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    note.appendChild(info);
  }

  /* the last page: page 3's button, the strip, the footer */
  var marquee = document.querySelector('#screen-hero .marquee');
  var footer = document.querySelector('#screen-hero footer');
  var p3cta = document.querySelector('#read .p3-cta');
  if (marquee && footer) {
    var last = document.createElement('div');
    last.className = 'ph-page ph-last';
    marquee.parentNode.insertBefore(last, marquee);
    last.appendChild(marquee);
    if (p3cta) last.appendChild(p3cta);
    last.appendChild(footer);
    var labels = ['Your data', 'About this service'];
    Array.prototype.slice.call(footer.querySelectorAll('.disclaimer')).forEach(function (p, i) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'ph-fold';
      var strong = p.querySelector('strong');
      b.textContent = (strong ? strong.textContent.replace(/[.\s]+$/, '') : labels[i]) || labels[i];
      b.setAttribute('aria-expanded', 'false');
      b.addEventListener('click', function () {
        var open = p.classList.toggle('open');
        b.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      p.parentNode.insertBefore(b, p);
    });
  }
})();

/* v8.2: the genie, on the hero itself. The hero pins for two extra viewports;
   the first scroll expands the hero's own field card across the page while the
   copy gives way and the metric and multiple columns spawn on. Reversible.
   Skipped below 900px (phones and tablets) and under prefers-reduced-motion. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var wrap = document.querySelector('#screen-hero .snap.first');
  var hero = wrap && wrap.querySelector('.hero');
  var card = wrap && wrap.querySelector('.ffcard');
  /* Below 900px there is no genie: phones and tablets get the stacked page, with the field as
     one chart (landing-mobile.css). The second phone pass of 7-Sep-2026 played the genie on
     phones and pinned the card through three screens; Daniil could not read it, so it is out. */
  if (!wrap || !hero || !card || reduce || window.innerWidth < 900) return;
  wrap.classList.add('hero-genie-on');
  var ticking = false;
  function update() {
    ticking = false;
    var top = wrap.getBoundingClientRect().top;
    var travel = wrap.offsetHeight - hero.offsetHeight;
    if (travel < 120) travel = 120;
    var p = Math.min(1, Math.max(0, -top / travel));
    wrap.style.setProperty('--exp', p.toFixed(3));
    wrap.classList.toggle('hero-genie-mid', p > 0.55);
    wrap.classList.toggle('genie-done', p > 0.97);
  }
  function onScroll() {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();
})();

/* v9: the card starts at its rest position (measured once, re-measured on
   resize while still at rest) and settles under the story block as it
   expands; the story's height is measured so the two never overlap. */
(function () {
  var wrap = document.querySelector('#screen-hero .snap.first.hero-genie-on');
  if (!wrap) return;
  var grid = wrap.querySelector('.hero-grid');
  var card = wrap.querySelector('.ffcard');
  if (!grid || !card) return;
  var story = wrap.querySelector('.hero-story');
  function measure() {
    var exp = parseFloat(wrap.style.getPropertyValue('--exp') || '0');
    /* the story block's height decides where the expanded card starts */
    if (story) wrap.style.setProperty('--story-h', (story.offsetHeight + 40) + 'px');
    if (exp > 0.02) return;
    var top = Math.max(24, Math.round((grid.clientHeight - card.offsetHeight) / 2) + 8);
    wrap.style.setProperty('--card-top', top + 'px');
  }
  measure();
  window.addEventListener('resize', measure, { passive: true });
  /* fonts arriving late change the card's height; measure again once they have */
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
  window.addEventListener('load', measure);
})();

/* v9: the opening. The headline arrives word by word (a soft blur-and-rise,
   one word every 75ms); the copy under it and the card follow once the last
   word has landed. Runs once per visit, never on the way back up the page, and
   not at all under prefers-reduced-motion. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var wrap = document.querySelector('#screen-hero .snap.first');
  var h1 = document.getElementById('hook-headline');
  if (!wrap || !h1 || reduce) return;
  var i = 0;
  Array.prototype.slice.call(h1.childNodes).forEach(function (node) {
    var host = node.nodeType === 1 ? node : null;
    var text = node.textContent;
    if (!text.trim()) return;
    var html = text.split(/\s+/).filter(Boolean).map(function (w) {
      return '<span class="w" style="--wi:' + (i++) + '">' + w + '</span>';
    }).join(' ');
    if (host) host.innerHTML = html;
    else { var s = document.createElement('span'); s.innerHTML = html; h1.replaceChild(s, node); }
  });
  wrap.classList.add('hero-intro');
  /* once played, hand every element back to its static styles so the genie
     and hover rules own them again */
  setTimeout(function () { wrap.classList.add('intro-done'); }, 120 + i * 75 + 1600);
})();
