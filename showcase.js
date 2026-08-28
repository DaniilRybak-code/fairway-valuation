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

/* v8.2: the genie, on the hero itself. The hero pins for two extra viewports;
   the first scroll expands the hero's own field card across the page while the
   copy gives way and the metric and multiple columns spawn on. Reversible.
   Skipped on small screens and under prefers-reduced-motion. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var wrap = document.querySelector('#screen-hero .snap.first');
  var hero = wrap && wrap.querySelector('.hero');
  var card = wrap && wrap.querySelector('.ffcard');
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
