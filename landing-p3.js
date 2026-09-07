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
 *
 * 3. Phones (7 Sep 2026, third phone pass). Below 640px the four cards would run four screens,
 *    so each of the rail's four numbered stops is moved into its card and becomes the row you
 *    tap to open it; card 1 keeps its two funnels in view while folded, because they are the
 *    picture of the page. Nothing is removed from the HTML: every word is one tap away. Without
 *    this script the rail stays a wrapped row and the cards stand open, as before.
 */
(function () {
  var sec = document.getElementById('read');
  if (!sec || !sec.classList.contains('p3')) return;

  var phone = window.matchMedia && window.matchMedia('(max-width: 640px)').matches;
  if (phone) {
    var stops = Array.prototype.slice.call(sec.querySelectorAll('.p3-stop'));
    var cards = Array.prototype.slice.call(sec.querySelectorAll('.p3-card'));
    var rail = sec.querySelector('.p3-rail');
    if (stops.length === cards.length && rail) {
      stops.forEach(function (stop, i) {
        var card = cards[i];
        card.classList.add('p3-fold');
        card.insertBefore(stop, card.firstChild);
        stop.setAttribute('role', 'button');
        stop.setAttribute('tabindex', '0');
        stop.setAttribute('aria-expanded', 'false');
        function toggle() {
          var open = card.classList.toggle('open');
          stop.setAttribute('aria-expanded', open ? 'true' : 'false');
        }
        stop.addEventListener('click', toggle);
        stop.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
        });
      });
      rail.hidden = true;
    }
    /* the button closes the page rather than opening it: the one under Our read is a screen above */
    var cta = sec.querySelector('.p3-cta');
    var wrap = sec.querySelector('.wrap-wide');
    if (cta && wrap) wrap.appendChild(cta);
  }

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
