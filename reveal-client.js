/* Calls the reveal engine once the result screen appears, then fills in the
 * basis sentence and the reference points, and updates the range if the engine
 * moved it. Loaded after app.js, which is where `responses` is declared.
 *
 * Everything degrades: if the endpoint is missing, slow or unhappy, the founder
 * keeps the first-pass range that is already on screen and never sees an error.
 */
(function () {
  const VISIBLE_DEFAULT = 2;
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
    const card = buildCard();
    const rangeCard = document.querySelector('#screen-result .result-card');
    if (rangeCard && rangeCard.parentNode) {
      rangeCard.parentNode.insertBefore(card, rangeCard.nextSibling);
    }

    const payload = typeof responses !== 'undefined' ? {
      stage: responses.stage, sector: responses.sector, sector_detail: responses.sector_detail,
      revenue: responses.revenue, growth: responses.growth, growth_detail: responses.growth_detail,
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
        card.remove();
      });
  }

  function apply(data) {
    const card = document.getElementById('reveal-card');
    if (!card) return;

    if (!data || !Array.isArray(data.reference_points) || !data.reference_points.length) {
      card.remove();
      if (data && data.basis_sentence) setBasis(data.basis_sentence, data);
      return;
    }

    if (typeof data.range_low_m === 'number' && typeof data.range_high_m === 'number') {
      const el = document.getElementById('range-output');
      if (el) {
        el.textContent = money(data.range_low_m) + ' – ' + money(data.range_high_m);
        el.classList.add('range-refined');
      }
    }

    setBasis(data.basis_sentence, data);

    const visible = typeof data.visible_reference_points === 'number'
      ? data.visible_reference_points : VISIBLE_DEFAULT;

    document.getElementById('reveal-lead').textContent =
      'The anchors this number rests on. Sources shown so you can check them.';

    const list = document.getElementById('reveal-list');
    list.innerHTML = '';
    data.reference_points.forEach(function (p, i) {
      const locked = i >= visible;
      const row = document.createElement('div');
      row.className = 'item' + (locked ? ' locked' : '');
      row.innerHTML =
        '<div class="num">' + (i + 1) + '</div><div>' +
        '<h3>' + esc(p.label) + (locked ? '<span class="lock-tag">Locked</span>' : '') + '</h3>' +
        '<p' + (locked ? ' class="body-lock"' : '') + '>' + esc(p.detail) + '</p>' +
        (locked ? '' : '<p class="reveal-src">' + esc(p.source) + '</p>') +
        '</div>';
      list.appendChild(row);
    });

    document.getElementById('reveal-foot').textContent =
      (data.reference_points.length - visible) + ' of the ' + data.reference_points.length +
      ' anchors behind this range are in the full report, with the working shown for each.';

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

  function setBasis(text, data) {
    if (!text) return;
    const note = document.getElementById('range-note');
    if (!note) return;
    const bits = [text];
    if (data && data.vintage) bits.push('Market data vintage ' + data.vintage + '.');
    if (data && data.verified_anchor === false) {
      bits.push('No published anchor exists for this stage yet, so the range is wider than it will be.');
    }
    note.textContent = bits.join(' ');
  }

  function buildCard() {
    const card = document.createElement('div');
    card.className = 'list-card';
    card.id = 'reveal-card';
    card.innerHTML =
      '<h2>What the range is built on</h2>' +
      '<p class="lead" id="reveal-lead">Working through the comparables and the methods. A few seconds.</p>' +
      '<div id="reveal-list"><div class="reveal-skel"></div><div class="reveal-skel"></div>' +
      '<div class="reveal-skel"></div><div class="reveal-skel"></div></div>' +
      '<p class="list-foot" id="reveal-foot"></p>';
    return card;
  }

  function injectStyles() {
    const css =
      '.reveal-skel{height:46px;border-radius:10px;margin:10px 0;' +
      'background:linear-gradient(90deg,#eef0f3 25%,#f7f8fa 50%,#eef0f3 75%);' +
      'background-size:400% 100%;animation:revealpulse 1.4s ease infinite;}' +
      '@keyframes revealpulse{0%{background-position:100% 0}100%{background-position:0 0}}' +
      '.reveal-src{font-size:12px;color:var(--lock);margin-top:5px;}' +
      '.range-refined{animation:revealfade .5s ease;}' +
      '@keyframes revealfade{from{opacity:.35}to{opacity:1}}' +
      '@media (prefers-reduced-motion: reduce){.reveal-skel,.range-refined{animation:none;}}';
    const tag = document.createElement('style');
    tag.textContent = css;
    document.head.appendChild(tag);
  }

  function money(m) {
    return m >= 1 ? '$' + m.toFixed(1) + 'M' : '$' + Math.round(m * 1000) + 'k';
  }

  function esc(v) {
    return String(v === undefined || v === null ? '' : v)
      .replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }
})();
