/* Landing page 3, "Under the hood": two small jobs, both presentation.
 *
 * 1. Motion. The section is armed on load (its blocks hidden) and switched on when it
 *    scrolls into view, so the rail draws and the cards arrive in order in front of the
 *    reader rather than while the page is still off screen. If this file never loads, or
 *    the visitor prefers reduced motion, nothing is armed and the section simply shows.
 *
 * 2. Counts. The four pool figures on the funnels (listed companies tracked, private rounds
 *    tracked, and how many of each share the example's business model) come from
 *    landing-counts.js, which tools/check_landing_page3.py writes from the data files.
 *    The HTML carries the same figures as text, kept in step by the same tool, so the
 *    page is right with or without this script. Nothing here is typed by hand.
 */
(function () {
  var sec = document.getElementById('read');
  if (!sec || !sec.classList.contains('p3')) return;

  var counts = window.FAIRWAY_COUNTS;
  if (counts) {
    Array.prototype.slice.call(sec.querySelectorAll('[data-count]')).forEach(function (el) {
      var key = el.getAttribute('data-count');
      if (Object.prototype.hasOwnProperty.call(counts, key) && counts[key] != null) {
        el.textContent = String(counts[key]);
      }
    });
  }

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;

  sec.classList.add('p3-armed');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      sec.classList.add('p3-on');
      io.disconnect();
    });
  }, { threshold: 0.02 });   /* a low threshold: on a phone the section is several screens tall,
                                so a quarter of it can never be in view at once */
  io.observe(sec);
})();
