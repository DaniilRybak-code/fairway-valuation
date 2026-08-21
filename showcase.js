/* Motion for the landing-page showcase.
 *
 * Two effects, both optional to the meaning of the section: a slow parallax
 * drift on the example panel, and a rise-in on each row as it enters. If this
 * file never loads, or the visitor prefers reduced motion, the section still
 * reads correctly and every number is still on screen.
 */
(function () {
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const panel = document.getElementById('showcase-panel');
  const rows = Array.prototype.slice.call(document.querySelectorAll('.ex-row'));

  if (reduce) {
    rows.forEach(function (r) { r.classList.add('in'); });
    return;
  }

  /* Rows rise in once, staggered, so the field assembles rather than appearing. */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        const i = rows.indexOf(e.target);
        e.target.style.transitionDelay = Math.max(0, i) * 65 + 'ms';
        e.target.classList.add('in');
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
    rows.forEach(function (r) { io.observe(r); });
  } else {
    rows.forEach(function (r) { r.classList.add('in'); });
  }

  /* Parallax. The panel drifts against the scroll by a small fraction of how far
     the section has travelled through the viewport. Capped so it never detaches
     from the copy beside it, and skipped entirely on narrow screens where the
     two columns are stacked and the effect would just look like a jitter. */
  if (!panel) return;
  const section = panel.closest('.showcase');
  if (!section) return;

  let ticking = false;
  const MAX = 34;

  function apply() {
    ticking = false;
    if (window.innerWidth < 900) { panel.style.setProperty('--drift', '0px'); return; }
    const box = section.getBoundingClientRect();
    const vh = window.innerHeight || 800;
    if (box.bottom < 0 || box.top > vh) return;
    /* -1 when the section is entering from below, +1 when it is leaving above. */
    const progress = 1 - (box.top + box.height / 2) / (vh / 2 + box.height / 2);
    const drift = Math.max(-MAX, Math.min(MAX, progress * MAX));
    panel.style.setProperty('--drift', drift.toFixed(1) + 'px');
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(apply);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  apply();
})();
