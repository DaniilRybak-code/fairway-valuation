/* THE REVEAL, DRAWN FROM ONE PAYLOAD, WITH THE FOUNDER'S FIGURES NEVER LEAVING THIS BROWSER.
 *
 * Loaded after app.js, field.js, reveal-request.js and reveal-figures.js.
 *
 * WHAT THIS FILE DOES NOW THAT IT DID NOT BEFORE.
 *
 *   1. It sends the profile and two ratios, and no amount. The body is built by
 *      buildRevealRequest in reveal-request.js, which loops over an allowlist and contains no
 *      field name of its own. Check 15 fails if a figure ever appears in it.
 *   2. It holds the founder's figures in one variable in this file and multiplies here. The
 *      arithmetic is priceBand in reveal-figures.js and it is the same sum check 14 recomputes
 *      server-side for the fixtures.
 *   3. It reads the engine payload: the peer charts, the honesty caveats, the fix list and both
 *      investor layers, all from ONE selection run. Before today renderRecommendations and
 *      renderInvestors existed and nothing called them.
 *   4. It offers the consent button. Nothing sends a figure until the founder presses it.
 *
 * WHAT IT DELIBERATELY DOES NOT DO. It does not redraw the football field. field.js draws nine
 * METHOD rows (the last round marker, the stage anchor, the unrefined range, NTM, DCF and the paid
 * rows) and the payload carries PEER EVIDENCE per lane per basis. They are different objects, and
 * deciding which of the nine method rows survives contact with the engine is a product decision
 * rather than a privacy one. The peer charts are rendered in their own block under the field, and
 * merging the two is the named next piece of work.
 *
 * Everything degrades. If the endpoint is missing, slow or unhappy, the founder keeps the field
 * that is already on screen and never sees an error.
 */
(function () {
  let started = false;

  /* THE FIGURES. One variable, this closure, this tab. Never written to localStorage,
     sessionStorage, IndexedDB or a cookie, and never placed in a request body except by the
     consent handler at the foot of this file. */
  let figures = {};
  let payload = null;

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
    if (typeof responses === 'undefined') return;

    /* Held here, sent nowhere. */
    figures = (typeof founderFigures === 'function') ? founderFigures(responses) : {};

    /* THE ONLY BODY THIS FILE POSTS ON THE FREE PATH, and it is built from the allowlist. */
    const body = (typeof buildRevealRequest === 'function') ? buildRevealRequest(responses) : {};

    /* TWO ENDPOINTS, ONE BODY, AND THE SAME BODY. /api/reveal writes the prose and /api/payload
       serves the engine, because the engine is Python and the prose endpoint is Node. They are
       fetched in parallel rather than chained: neither needs the other's answer, and chaining
       would make the whole reveal wait for the slower of the two.

       THE BODY IS BUILT ONCE, above, by the one function in the product allowed to build one. Both
       posts send that same object, so there is one boundary to check and not two, and
       tools/check_request_boundary.py asserts the Python endpoint's allowlist is the same set of
       names as this page's. */
    const post = function (url) {
      return fetch(url, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body)
      }).then(r => r.json());
    };

    post('/api/reveal')
      .then(apply)
      .catch(function (e) {
        console.warn('[fairway] reveal unavailable', e);
      });

    /* THE ENGINE. Its own promise, so a failure here leaves the prose standing and a failure there
       leaves the numbers standing. Before 7-Sep-2026 /api/reveal answered payload:null with a
       reason and this was the block that never ran. */
    post('/api/payload')
      .then(applyPayload)
      .catch(function (e) {
        console.warn('[fairway] engine unavailable', e);
      });

    /* The consent button does not wait for the engine. The 24-hour banker read is offered whether
       or not the payload arrives, so the button is mounted from what the page already knows. */
    mountConsent();
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

    /* THE ENGINE PAYLOAD MOVED TO ITS OWN RESPONSE ON 7-SEP-2026. /api/reveal still carries the
       key, so a deployment where only the Node function has been updated keeps working; when it is
       null, which is what it always was, applyPayload simply gets nothing and renders nothing. */
    if (data.payload) applyPayload(data);
  }

  /* WHAT THE ENGINE'S ANSWER DOES TO THE PAGE. One function, called from whichever response
     carries a payload, so there is exactly one place that decides what a reveal looks like.

     RENDERS NOTHING RATHER THAN SOMETHING WRONG. A missing payload leaves the blocks empty, which
     is the same failure mode the two renderers already have: empty rather than a heading with
     nothing under it. A half-drawn reveal reads as a finished one, and that is the failure this
     guard exists to prevent. */
  function applyPayload(data) {
    payload = (data && data.payload) || null;
    if (!payload) return;

    renderPeerCharts(payload, figures);
    renderHonesty(payload);
    if (typeof renderRecommendations === 'function') {
      renderRecommendations(payload.recommendations, 'recommendation-blocks');
    }
    if (typeof renderInvestors === 'function') {
      renderInvestors(payload.investors, 'investor-blocks');
    }
    /* THE FOOTBALL FIELD, DRAWN FROM THE PAYLOAD. field.js has drawn its own nine method rows from
       figures typed into the HTML since the page was built; renderField() replaces them with the
       lanes the engine actually produced, when field.js offers it. Guarded so that an older
       field.js on a cached deploy leaves the existing field alone rather than blanking it. */
    /* NO FIGURES, NO FOOTBALL FIELD. Daniil, 7-Sep-2026: "If they give nothing, we only show the
       bar charts with multiples, not football fields." A field whose every row says "needs revenue"
       is a page telling a founder what they did not do, nine times. The charts say what their peers
       trade at, which is the argument they can actually use. */
    var gaveSomething = figures && Object.keys(figures).length > 0;
    if (!gaveSomething) {
      hideField();
    } else if (typeof renderFieldFromPayload === 'function') {
      renderFieldFromPayload(payload, figures);
    }
    mountConsent();
  }

  /* THE FIELD, HIDDEN. Everything from the football field's own heading down goes, rather than the
     rows alone, so there is no orphan title over an empty space. The charts and the honesty block
     are untouched and are what the founder reads instead. */
  function hideField() {
    ['ff', 'ff-context', 'ff-legend', 'ff-head'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.style.display = 'none';
    });
  }

  /* ---------------- the peer charts ----------------
     Daniil, 6-Sep-2026: "what if the user does not want to give us the numbers at all? Then we
     should be able just to show the peers and how they trade." The payload carries `charts` in his
     own reading order: public multiples, then private net, then private gross, then per user. */

  function renderPeerCharts(p, figs) {
    const mount = document.getElementById('peer-charts');
    if (!mount) return false;
    const rows = (typeof priceCharts === 'function') ? priceCharts(p.charts, figs) : (p.charts || []);
    /* THE NAMES LIVE IN `ranges`, NOT IN `charts`. A chart entry carries what a bar needs and
       nothing else, which is right, but a range whose names are not visible is an assertion rather
       than an argument, so each bar is joined back to its own lane and basis for them. `sole` comes
       across at the same time: it is the one name behind a reading that is not a range. */
    rows.forEach(function (c) {
      const rng = ((p.ranges || {})[c.lane] || {})[c.basis] || {};
      c.peers = rng.peers || [];
      c.sole = rng.sole || null;
    });
    const drawable = rows.filter(function (c) { return c.n; });
    if (!drawable.length) { mount.innerHTML = ''; return false; }

    /* THE AXIS IS PER UNIT, NOT PER BLOCK. A revenue multiple and a dollars-per-subscriber reading
       are not the same measure and putting them on one scale makes the smaller one a dot at the
       left edge. Each unit group is scaled on its own.

       Inside a group the scale is shared on purpose: listed at 3.0x beside private rounds at 120x
       is the finding, not a drawing problem.

       ONLY VISIBLE ROWS SET THE SCALE. A locked lane carries no low, mid or high at all on the
       free tier, so there is nothing of it in the axis and nothing to read off the screen with a
       ruler. */
    const unit = function (c) {
      return (typeof unitOf === 'function') ? unitOf(c.basis) : 'multiple';
    };
    const tops = {};
    drawable.forEach(function (c) {
      if (typeof c.high !== 'number') return;
      const u = unit(c);
      tops[u] = Math.max(tops[u] || 0, c.high);
    });

    const html = ['<div class="rd wide"><b class="rd-t">How companies like yours have been priced</b>'];
    html.push('<p class="microcopy" style="margin:-2px 0 14px;">Each bar is the range of multiples paid '
      + 'for the comparable companies behind it, not a valuation of you. Where you gave us a figure, '
      + 'the value beside the bar is that figure times the multiple, worked out in your browser.</p>');
    html.push('<div class="pc-list">' + drawable.map(function (c) {
      return chartRow(c, tops[unit(c)] || 1);
    }).join('') + '</div>');
    html.push('</div>');
    mount.innerHTML = html.join('');
    return true;
  }

  function chartRow(c, hi) {
    const names = (c.peers || []).map(function (x) {
      return esc(x.company || x.ticker || '') + (x.date ? ', ' + esc(x.date) : '');
    }).filter(Boolean);
    const title = esc(c.label || c.basis) + ' <span class="pc-lane">' + esc(c.lane) + '</span>';
    const count = c.n + (c.n === 1 ? ' comparable' : ' comparables');

    if (c.locked || typeof c.low !== 'number') {
      /* NOTHING BEHIND THE BLUR. Rule E8 as amended: the names and the count are here and the
         figures were never sent, so there is no element to inspect. */
      return '<div class="pc-row pc-locked" title="' + esc(names.join(' | ')) + '">'
        + '<div class="pc-head">' + title + '<span class="pc-n">' + count + '</span></div>'
        + '<div class="pc-bar"><span class="pc-blur"></span></div>'
        + '<div class="pc-foot">' + (names.length
          ? 'Hover for the names. ' + esc(names.slice(0, 6).join(' | '))
          : 'The multiples open with the full field.') + '</div></div>';
    }

    const left = Math.max(0, (c.low / hi) * 100);
    const width = Math.max(1.5, ((c.high - c.low) / hi) * 100);

    /* HONOUR `display`. The engine has always said whether a reading is a band, a scatter or a
       single point, and until today nothing read it, which is the same shape of problem as the
       honesty strings. A DIAMOND is one name and rule A7 says one name is never a range, so it is
       drawn as a point and labelled as one rather than as a bar of no width. */
    const kind = c.display === 'DIAMOND' || c.n < 2 ? 'point'
      : (c.display === 'SCATTER' ? 'scatter' : 'band');
    const bar = kind === 'point'
      ? '<span class="pc-point" style="left:' + left.toFixed(1) + '%;"></span>'
      : '<span class="pc-fill' + (kind === 'scatter' ? ' pc-scatter' : '') + '" style="left:'
        + left.toFixed(1) + '%;width:' + width.toFixed(1) + '%;"></span>';

    const mult = kind === 'point'
      ? fx(c.low) + 'x, one comparable' + (c.sole ? ' (' + esc(c.sole) + ')' : '')
      : fx(c.low) + 'x to ' + fx(c.high) + 'x' + (kind === 'scatter' ? ', and they disagree' : '');

    const price = (c.priced && c.founder_low != null)
      ? '<span class="pc-price">' + money(c.founder_low) + ' to ' + money(c.founder_high) + '</span>'
      : '<span class="pc-nop" title="' + esc(c.unpriced_reason || '') + '">'
        + (c.unpriced_reason ? 'we do not have a figure of yours on this measure'
          : 'give us this figure and the bar carries a value') + '</span>';

    const note = kind === 'point'
      ? '<div class="pc-names">One name is not a range, so this is a point of reference rather than '
        + 'a band.</div>'
      : (names.length ? '<div class="pc-names">' + esc(names.slice(0, 8).join(' | ')) + '</div>' : '');

    return '<div class="pc-row">'
      + '<div class="pc-head">' + title + '<span class="pc-n">' + count + '</span></div>'
      + '<div class="pc-bar">' + bar + '</div>'
      + '<div class="pc-foot"><span class="pc-mult">' + mult + '</span>' + price + '</div>'
      + note
      + '</div>';
  }

  /* ---------------- the honesty caveats ----------------
     honesty.py has produced these since 26 August and no founder has ever seen one. Two lists,
     because inline and behind-the-disclosure are two different places on the page and the split is
     already decided by severity in the engine. */

  function renderHonesty(p) {
    const mount = document.getElementById('honesty-block');
    if (!mount) return false;
    const h = p.honesty || {};
    const inline = h.inline || [];
    const behind = h.disclosure || [];
    if (!inline.length && !behind.length) { mount.innerHTML = ''; return false; }
    const html = [];
    inline.forEach(function (c) {
      html.push('<p class="hon-inline">' + esc(c.text) + '</p>');
    });
    if (behind.length) {
      html.push('<details class="hon-more"><summary>What else we would want you to know about this set</summary>');
      behind.forEach(function (c) { html.push('<p>' + esc(c.text) + '</p>'); });
      html.push('</details>');
    }
    mount.innerHTML = html.join('');
    return true;
  }

  /* ---------------- the consent button ----------------
     Daniil, 6-Sep-2026: "if the user wants to have his numbers and ff reviewed, he presses a
     button and it comes through to us, in which case he would specifically agree for us to see it."

     IT SITS BESIDE THE 24-HOUR PROMISE because that read is what it buys. The wording says what is
     being sent and to whom, and the exact wording clicked is stored beside the figures so that
     what the founder agreed to is a matter of record. */

  const CONSENT_WORDING = 'Send the figures I typed on this page to the Fairway reviewer, so a '
    + 'person can check my football field and email me their read within 24 hours.';

  function figureList() {
    /* What is actually in the founder's answers right now, named one by one. A consent notice that
       says "your data" is not consent to anything. */
    const named = [];
    if (responses.revenue_exact) named.push('your monthly revenue');
    if (responses.gross_margin != null) named.push('your gross margin');
    if (responses.ebitda_ltm) named.push('your last twelve months of EBITDA');
    if (responses.last_round_value || responses.last_round_amount) named.push('your last round');
    if (responses.raise) named.push('the size of the round you are raising');
    if (responses.profit) named.push('whether you are profitable');
    if (responses.growth_detail || responses.concern_notes) named.push('the notes you wrote');
    if (responses.context_link) named.push('the link you gave us');
    return named;
  }

  function mountConsent() {
    const mount = document.getElementById('consent-block');
    if (!mount) return false;
    if (mount.getAttribute('data-sent') === '1') return false;
    const named = figureList();
    if (!named.length) {
      mount.innerHTML = '<p class="microcopy">You have not given us any figures, so there is '
        + 'nothing to send. The peer sets above were chosen on your growth rate and your margin.</p>';
      return false;
    }
    mount.innerHTML =
      '<div class="consent-card">'
      + '<b>Nothing above has been sent to us.</b>'
      + '<p>' + esc(CONSENT_WORDING) + '</p>'
      + '<p class="consent-what">What goes with it: ' + esc(named.join(', ')) + '. '
      + 'It goes to the Fairway reviewer and to nobody else. It is not sent to any model, it is '
      + 'not sold, and it is not shared with investors.</p>'
      + '<button type="button" class="btn" id="consent-send">Send my figures for the banker review</button>'
      + '<p class="consent-note" id="consent-note"></p>'
      + '</div>';
    const btn = document.getElementById('consent-send');
    if (btn) btn.onclick = sendForReview;
    return true;
  }

  function sendForReview() {
    const btn = document.getElementById('consent-send');
    const note = document.getElementById('consent-note');
    if (btn) { btn.disabled = true; btn.textContent = 'Sending'; }

    /* THE ONE REQUEST IN THIS PRODUCT THAT CARRIES A FIGURE, and the founder pressed the button
       that made it. */
    const body = buildReviewRequest(responses, figuresForReview(), window.__fairwayLeadId || null,
                                   CONSENT_WORDING);

    fetch('/api/lead', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body)
    })
      .then(function () {
        const mount = document.getElementById('consent-block');
        if (mount) mount.setAttribute('data-sent', '1');
        if (note) note.textContent = 'Sent. A reviewer reads it by hand and emails you within 24 hours.';
        if (btn) btn.textContent = 'Sent for review';
        if (typeof track === 'function') track('figures_consented', {});
      })
      .catch(function (e) {
        console.warn('[fairway] review send failed', e);
        if (note) note.textContent = 'That did not go through. Try again, or reply to the email we sent you.';
        if (btn) { btn.disabled = false; btn.textContent = 'Send my figures for the banker review'; }
      });
  }

  /* WHAT THE CONSENT REQUEST CARRIES. The founder's own answers, not the derived figures: the
     reviewer wants what was typed, and every derived number on this page is reproducible from it. */
  function figuresForReview() {
    return {
      currency: responses.currency || 'USD',
      revenue: responses.revenue,
      revenue_exact: responses.revenue_exact,
      arr_exact: responses.revenue_exact != null ? responses.revenue_exact * 12 : null,
      recurring_pct: responses.recurring_pct,
      ebitda_ltm: responses.ebitda_ltm,
      last_round_amount: responses.last_round_amount,
      last_round_value: responses.last_round_value,
      last_round_type: responses.last_round_type,
      last_round_date: responses.last_round_date,
      profit: responses.profit,
      raise: responses.raise,
      timing: responses.timing,
      growth_detail: responses.growth_detail,
      concern_notes: responses.concern_notes,
      context_link: responses.context_link
    };
  }

  /* ---------------- small helpers ---------------- */

  function injectStyles() {
    const css =
      '.range-refined{animation:revealfade .5s ease;}' +
      '@keyframes revealfade{from{opacity:.35}to{opacity:1}}' +
      '@media (prefers-reduced-motion: reduce){.range-refined{animation:none;}}' +
      '.pc-row{padding:12px 0;border-top:1px solid rgba(0,0,0,.07);}' +
      '.pc-row:first-child{border-top:0;}' +
      '.pc-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;font-weight:600;}' +
      '.pc-lane{font-weight:400;opacity:.55;font-size:.85em;text-transform:uppercase;letter-spacing:.04em;}' +
      '.pc-n{font-weight:400;opacity:.6;font-size:.85em;white-space:nowrap;}' +
      '.pc-bar{position:relative;height:12px;margin:8px 0 6px;background:rgba(0,0,0,.05);border-radius:6px;}' +
      '.pc-fill{position:absolute;top:0;bottom:0;background:currentColor;opacity:.55;border-radius:6px;}' +
      '.pc-scatter{background:repeating-linear-gradient(90deg,currentColor 0 3px,transparent 3px 8px);opacity:.7;}' +
      '.pc-point{position:absolute;top:-2px;width:16px;height:16px;margin-left:-8px;' +
        'background:currentColor;opacity:.75;transform:rotate(45deg);border-radius:3px;}' +
      '.pc-blur{position:absolute;top:0;bottom:0;left:22%;width:34%;border-radius:6px;' +
        'background:repeating-linear-gradient(90deg,rgba(0,0,0,.16) 0 6px,rgba(0,0,0,.06) 6px 12px);}' +
      '.pc-foot{display:flex;justify-content:space-between;gap:12px;font-size:.9em;}' +
      '.pc-mult{font-variant-numeric:tabular-nums;}' +
      '.pc-price{font-weight:600;font-variant-numeric:tabular-nums;}' +
      '.pc-nop{opacity:.55;}' +
      '.pc-names{margin-top:6px;font-size:.85em;opacity:.6;}' +
      '.hon-inline{margin:10px 0;opacity:.85;}' +
      '.hon-more{margin-top:10px;}.hon-more summary{cursor:pointer;opacity:.7;}' +
      '.consent-card{border:1px solid rgba(0,0,0,.12);border-radius:12px;padding:18px;margin:18px 0;}' +
      '.consent-card b{display:block;margin-bottom:6px;}' +
      '.consent-what{font-size:.9em;opacity:.7;}' +
      '.consent-note{font-size:.9em;margin-top:10px;}';
    const tag = document.createElement('style');
    tag.textContent = css;
    document.head.appendChild(tag);
  }

  function money(m) {
    /* curSymbol lives in app.js, which loads first. Falls back to $ if it is ever absent. */
    const c = (typeof curSymbol === 'function') ? curSymbol() : '$';
    return m >= 1 ? c + m.toFixed(1) + 'M' : c + Math.round(m * 1000) + 'k';
  }

  function fx(n) { return (typeof n === 'number') ? (n >= 10 ? Math.round(n).toString() : n.toFixed(1)) : ''; }

  function esc(v) {
    return String(v === undefined || v === null ? '' : v)
      .replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }
})();
