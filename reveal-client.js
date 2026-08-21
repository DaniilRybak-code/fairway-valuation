/* Calls the reveal engine once the result screen appears and refines what is
 * already there. Loaded after app.js and field.js.
 *
 * Everything degrades: if the endpoint is missing, slow or unhappy, the founder
 * keeps the field that is already on screen, and never sees an error.
 */
(function () {
  let started = false;

  injectStyles();

  const result = document.getElementById('screen-result');
  if (!result) return;

  new MutationObserver(function () {
    if (result.classList.contains('active') && !started) {
      started = true;
      run();
    }
  }).observe(result, { attributes: true, attributeFilter: ['class'] });

  function run() {
    /* No card of its own any more. The football field is the single place the
       working is shown, so a second list of reference points beside it would be
       the same information twice, in two formats, disagreeing at the edges. */
    const payload = typeof responses !== 'undefined' ? {
      stage: responses.stage, sector: responses.sector, sector_detail: responses.sector_detail,
      /* The website is what lets the model read the business rather than the box
         it ticked. It is the input the peer selection will lean on hardest. */
      website: responses.website || null,
      /* Exact figures where the founder gave them. The bands are still sent so the
         engine keeps working for pre-revenue and for anyone who skipped the numbers. */
      currency: responses.currency || 'USD',
      revenue: responses.revenue,
      revenue_exact: responses.revenue_exact != null ? responses.revenue_exact : null,
      arr_exact: responses.revenue_exact != null ? responses.revenue_exact * 12 : null,
      recurring_pct: responses.recurring_pct != null ? responses.recurring_pct : null,
      revenue_model: responses.revenue_model || null,
      growth: responses.growth,
      growth_yoy: responses.growth_yoy != null ? responses.growth_yoy : null,
      growth_detail: responses.growth_detail,
      profit: responses.profit, raise: responses.raise, timing: responses.timing,
      concerns: responses.concerns || [], concern_notes: responses.concern_notes
    } : {};

    fetch('/api/reveal', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(r => r.json())
      .then(apply)
      .catch(function (e) {
        console.warn('[fairway] reveal unavailable', e);
      });
  }

  function apply(data) {
    if (!data) return;

    /* The engine no longer returns a range and this client no longer applies one.
       A model may never move a number on this page. It writes the concerns below,
       which are prose about the founder's own answers, and nothing else. */

    /* Replace the pattern-level concerns when the engine produced better ones. */
    if (Array.isArray(data.concerns) && data.concerns.length === 3) {
      ['fix-1', 'fix-2', 'fix-3'].forEach(function (id, i) {
        const title = document.getElementById(id + '-title');
        const body = document.getElementById(id + '-body');
        if (!title || !body) return;
        const locked = i > 0;
        title.innerHTML = esc(data.concerns[i].title) + (locked ? '<span class="lock-tag">Locked</span>' : '');
        body.textContent = data.concerns[i].body;
      });
    }
  }

  function injectStyles() {
    const css =
      '.range-refined{animation:revealfade .5s ease;}' +
      '@keyframes revealfade{from{opacity:.35}to{opacity:1}}' +
      '@media (prefers-reduced-motion: reduce){.range-refined{animation:none;}}';
    const tag = document.createElement('style');
    tag.textContent = css;
    document.head.appendChild(tag);
  }

  function money(m) {
    /* curSymbol lives in app.js, which loads first. Falls back to $ if it is ever absent. */
    const c = (typeof curSymbol === 'function') ? curSymbol() : '$';
    return m >= 1 ? c + m.toFixed(1) + 'M' : c + Math.round(m * 1000) + 'k';
  }

  function esc(v) {
    return String(v === undefined || v === null ? '' : v)
      .replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }
})();
