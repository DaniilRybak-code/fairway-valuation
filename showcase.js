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
  /* 7-Sep-2026: the genie plays on phones too (Daniil: keep the same three pages, sized for an
     iPhone). Tablets between 641 and 899px keep the older continuous layout. On a phone the copy
     and the card stack, so the card rises from under the copy to the top of the screen while the
     copy fades; once the genie is done the pinned content is shifted up by the scroll so the
     field scrolls through like normal text. landing-mobile.css carries the geometry. */
  var phone = window.innerWidth <= 640;
  if (!wrap || !hero || !card || reduce || (window.innerWidth < 900 && !phone)) return;
  wrap.classList.add('hero-genie-on');
  if (phone) wrap.classList.add('hero-genie-phone');
  var ticking = false;
  var travelPx = 0, travelW = 0;
  function phoneTravel() {
    /* a phone's toolbar shrinks and grows the viewport as the reader scrolls; the distance the
       genie plays over is fixed at the first measurement so it does not jump mid-scroll, and
       only measured again when the width changes (the phone was turned) */
    if (!travelPx || travelW !== window.innerWidth) {
      travelPx = Math.round(window.innerHeight * 1.15); travelW = window.innerWidth;
      wrap.style.setProperty('--travel', travelPx + 'px');
    }
    return travelPx;
  }
  function update() {
    ticking = false;
    var top = wrap.getBoundingClientRect().top;
    var travel = phone ? phoneTravel() : wrap.offsetHeight - hero.offsetHeight;
    if (travel < 120) travel = 120;
    var p = Math.min(1, Math.max(0, -top / travel));
    wrap.style.setProperty('--exp', p.toFixed(3));
    wrap.classList.toggle('hero-genie-mid', p > 0.55);
    wrap.classList.toggle('genie-done', p > 0.97);
    if (phone) {
      /* the shift stops growing where the hero stops sticking (the section's end), or the
         content would move twice, with the scroll and with the shift, and leave a gap */
      var most = Math.max(0, wrap.offsetHeight - hero.offsetHeight - travel);
      var shift = Math.min(most, Math.max(0, -top - travel));
      wrap.style.setProperty('--card-shift', (-shift) + 'px');
    }
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
  var phone = wrap.classList.contains('hero-genie-phone');
  var vis = wrap.querySelector('.hero-vis');
  var copy = wrap.querySelector('.hero-copy');
  var read = wrap.querySelector('.our-read');
  function phoneHeight(exp) {
    /* the section is the genie's travel plus everything that has to scroll through afterwards:
       the story block, then the expanded card. At rest the card is measured with the "Our read"
       block still folded, so its unfolded height is added; once the genie is done the card is
       measured as it stands. */
    var travel = parseFloat(wrap.style.getPropertyValue('--travel')) || Math.round(window.innerHeight * 1.15);
    var storyH = story ? story.offsetHeight + 24 : 0;
    var visH = vis ? vis.offsetHeight : card.offsetHeight;
    if (exp < 0.97 && read) visH += read.scrollHeight;
    wrap.style.height = (travel + storyH + visH + 32) + 'px';
  }
  function measure() {
    var exp = parseFloat(wrap.style.getPropertyValue('--exp') || '0');
    if (phone) {
      if (story) wrap.style.setProperty('--story-h', (story.offsetHeight + 24) + 'px');
      if (exp <= 0.02 && copy) wrap.style.setProperty('--card-top', (copy.offsetHeight + 28) + 'px');
      phoneHeight(exp);
      return;
    }
    /* the story block's height decides where the expanded card starts */
    if (story) wrap.style.setProperty('--story-h', (story.offsetHeight + 40) + 'px');
    if (exp > 0.02) return;
    var top = Math.max(24, Math.round((grid.clientHeight - card.offsetHeight) / 2) + 8);
    wrap.style.setProperty('--card-top', top + 'px');
  }
  if (phone) {
    /* re-measure once the genie has finished, when the card stands at its full height */
    var done = false;
    window.addEventListener('scroll', function () {
      if (done || !wrap.classList.contains('genie-done')) return;
      done = true; phoneHeight(1);
    }, { passive: true });
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
