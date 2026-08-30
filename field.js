/* Fairway football field.
 *
 * Four columns: the method, the reference metric, the multiple, and the chart.
 * The chart takes roughly sixty per cent of the width because it is the product;
 * everything to its left is deliberately compact so the eye runs down the
 * multiples and across the bars.
 *
 * THE RULE THIS FILE EXISTS TO SERVE: every bar must be reproducible from the
 * two columns beside it. Metric times multiple equals bar. If a row cannot show
 * its own arithmetic, it does not belong here.
 *
 * Locked rows are drawn at a fixed decorative position, never their true one,
 * and the axis is scaled from visible rows only, so the hidden answer cannot be
 * read off the screen with a ruler.
 *
 * Loaded after app.js and data-public-comps.js.
 */

function ffMoney(m) {
  const c = (typeof curSymbol === 'function') ? curSymbol() : '$';
  if (!m) return c + '0';
  if (m >= 1) return c + (m < 10 ? m.toFixed(1) : Math.round(m)) + 'm';
  return c + Math.round(m * 1000) + 'k';
}

/* Bare number for the chart, where the currency is already stated on the axis. */
function ffNum(m) { return m >= 10 ? Math.round(m).toString() : m.toFixed(1); }

/* A cell value that carries a source becomes a button. */
function ffCell(v, id, cls) {
  if (!v) return '<div class="' + cls + '"><span class="ff-dash">&mdash;</span></div>';
  const inner = v.source
    ? '<button type="button" class="ffm-src" aria-expanded="false" aria-controls="' + id + '" ' +
      'onclick="ffToggleSource(this)">' + escapeHtml(v.value) + '</button>'
    : escapeHtml(v.value);
  return '<div class="' + cls + '">' + inner +
    (v.sub ? '<span class="sub">' + escapeHtml(v.sub) + '</span>' : '') + '</div>';
}

function ffToggleSource(btn) {
  const box = document.getElementById(btn.getAttribute('aria-controls'));
  if (!box) return;
  const open = box.style.display !== 'none';
  box.style.display = open ? 'none' : 'block';
  btn.setAttribute('aria-expanded', open ? 'false' : 'true');
  if (typeof track === 'function' && !open) track('ff_source_opened', { metric: btn.textContent.slice(0, 40) });
}

/* Round tick values across the axis, so the scale reads like a printed exhibit
   rather than whatever the data happened to produce. */
function ffTicks(lo, hi) {
  const span = hi - lo;
  const raw = span / 6;
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const step = [1, 2, 2.5, 5, 10].map(s => s * mag).find(s => s >= raw) || mag * 10;
  const out = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) out.push(Math.round(v * 100) / 100);
  return out;
}

/* ---------------- the rows ---------------- */

function ffBuildRows(r) {
  const rows = [];
  const sector = responses.sector === 'Other' ? 'Other' : (responses.sector || 'Other');
  const cur = responses.currency || 'USD';
  const raiseM = r.raise;

  const IN_BUILD = 'Being wired to live comparable-company data. Until it is, this row shows the metric it will price rather than a number we invented.';

  /* ---- 1. Last round. A marker, feeding nothing. */
  if (r.markerM) {
    const when = responses.last_round_date ? prettyMonth(responses.last_round_date) : 'date not given';
    const kind = responses.last_round_type === 'SAFE or note cap' ? 'cap' : 'pre-money';
    rows.push({
      group: 'Where you are today',
      parameter: 'Last round',
      basis: 'Marker only, feeds nothing',
      metric: { value: ffMoney(r.markerM), sub: kind },
      mult: null,
      point: r.markerM, marker: true,
      pointNote: when,
      locked: false
    });
  }

  /* ---- 2. Stage benchmark, market context. */
  const anchor = STAGE_ANCHOR[responses.stage];
  if (anchor && anchor.post_median_m) {
    const medianLocal = cur === 'USD' ? anchor.post_median_m : fxConvert(anchor.post_median_m, 'USD', cur);
    rows.push({
      group: 'Where you are today',
      parameter: 'Stage benchmark',
      basis: 'Market context, not a valuation of you',
      metric: { value: '$' + anchor.post_median_m.toFixed(1) + 'm', sub: responses.stage + ' median',
        source: anchor.source + '. ' + anchor.note + ' A cross-sector median is market context, not a valuation of your company: half the companies in it sit below this line.' +
          (cur !== 'USD' && medianLocal ? ' Converted at ' + (FX.perEur[cur] / FX.perEur.USD).toFixed(4) + ' ' + cur + ' per USD, ' + FX.source + ', ' + FX.date + '.' : '') },
      mult: { value: 'less ' + ffMoney(raiseM), sub: 'your raise' },
      point: medianLocal ? medianLocal - raiseM : null,
      unplotted: medianLocal ? null : 'No published ECB rate for ' + cur + ', so this is left unconverted rather than converted at a rate we cannot source.',
      locked: false, context: true
    });
  }

  /* ---- 3. The unrefined range. Kept, plotted, and labelled for what it is. */
  const pc = PUBLIC_COMPS.sectors[sector];
  const runRateM = r.runRateM;
  if (pc && runRateM > 0 && r.ntmM) {
    const a = runRateM * pc.ev_sales, b = r.ntmM * pc.ev_sales;
    rows.push({
      group: 'Public trading multiples',
      parameter: 'Unrefined range',
      basis: 'Before any comparable set is chosen',
      metric: { value: ffMoney(runRateM) + ' · ' + ffMoney(r.ntmM), sub: 'ARR · NTM revenue' },
      mult: { value: pc.ev_sales.toFixed(1) + 'x', sub: pc.n + ' listed firms',
        source: PUBLIC_COMPS.source + ', ' + PUBLIC_COMPS.vintage + '. ' + PUBLIC_COMPS.universe + '.' +
          (pc.note ? ' ' + pc.note : '') +
          ' The low end is ' + pc.ev_sales.toFixed(1) + 'x on your ARR today, the high end is the same multiple on your next twelve months. This is every listed company in the industry, from the largest in the world down, with no adjustment for the fact that you are private and small. The rows below narrow it to companies actually like yours, which is the whole point.' },
      low: Math.min(a, b), high: Math.max(a, b),
      locked: false, unrefined: true
    });
  } else if (pc) {
    rows.push({
      group: 'Public trading multiples',
      parameter: 'Unrefined range',
      basis: 'Before any comparable set is chosen',
      metric: { value: 'no revenue yet' },
      mult: { value: pc.ev_sales.toFixed(1) + 'x', sub: pc.n + ' listed firms',
        source: PUBLIC_COMPS.source + ', ' + PUBLIC_COMPS.vintage + '. ' + PUBLIC_COMPS.universe + '.' },
      unplotted: 'Nothing to apply the multiple to until there is a revenue figure.',
      locked: false, unrefined: true
    });
  }

  /* ---- 4. NTM revenue. */
  rows.push({
    group: 'Public trading multiples',
    parameter: 'NTM revenue',
    basis: 'Median of your core peer set',
    metric: { value: r.ntmM === null ? 'needs revenue' : ffMoney(r.ntmM), sub: 'next twelve months',
      source: r.ntmM === null ? 'Give an exact monthly revenue figure and this becomes a number.'
        : 'The sum of your next twelve months, built from ' + fmtPlain(responses.revenue_exact || 0) + ' a month growing at ' +
          (r.forwardGrowth === null ? 'no assumed growth' : Math.round(r.forwardGrowth) + '% a year') + '. ' +
          (r.forwardBasis === 'plan'
            ? 'That is the growth you told us you plan, used exactly as you gave it. We apply no haircut and no coefficient of our own to it.'
            : (r.forwardBasis === 'trailing'
              ? 'You did not give a plan, so that is your last twelve months carried forward unchanged.'
              : 'Derived from the growth band you chose. An exact figure replaces it.')) +
          ' Forward consensus revenue is a sum, so ours is a sum.' },
    mult: { value: 'in build', source: IN_BUILD },
    locked: true, pending: true
  });

  /* ---- 5. Month-twelve ARR, same peers. */
  rows.push({
    group: 'Public trading multiples',
    parameter: 'ARR, month 12',
    basis: 'Same peers, forward run-rate',
    metric: { value: r.exitArrM === null ? 'needs revenue' : ffMoney(r.exitArrM), sub: 'run-rate in a year',
      source: r.exitArrM === null ? 'Give an exact monthly revenue figure and this becomes a number.'
        : 'Your run-rate a year from now at the growth you gave us, not the twelve-month sum, which is why it is the larger of the two. This row values you at a future date. The more of your revenue that recurs, the better that basis holds.' },
    mult: { value: 'in build', source: IN_BUILD },
    locked: true, pending: true
  });

  /* ---- 6. Private rounds. A multiple, never a valuation. */
  const revLabel = responses.revenue_exact > 0
    ? ffMoney((responses.revenue_exact * 0.8) / 1e6) + ' to ' + ffMoney((responses.revenue_exact * 1.25) / 1e6)
    : (responses.revenue || 'pre-revenue');
  rows.push({
    group: 'Private rounds',
    parameter: 'Comparable private rounds',
    basis: [responses.stage, sector].filter(Boolean).join(' · '),
    metric: { value: r.ntmM === null ? 'needs revenue' : ffMoney(r.ntmM), sub: 'matched on ' + revLabel + ' MRR' },
    mult: { value: 'in build',
      source: 'The multiple, never the valuation. Another company’s post-money tells you nothing without the revenue underneath it, so every round in this set carries a revenue figure and a link to where it came from, or it is not in the set.' },
    locked: true, pending: true
  });

  /* ---- 7 to 10. The paid rows. These stay locked after launch. */
  rows.push({
    group: 'Public trading multiples',
    parameter: 'Growth-adjusted',
    basis: 'Fitted on the peer regression',
    metric: { value: r.ntmM === null ? 'needs revenue' : ffMoney(r.ntmM), sub: 'NTM revenue' },
    mult: null, locked: true, paid: true
  });

  rows.push({
    group: 'Discounted cash flow',
    parameter: 'Discounted cash flow',
    basis: 'Cost of capital from peer beta',
    metric: { value: 'your plan', sub: 'send a link and it opens',
      source: 'Unlevered beta for each company in your peer set at its own capital structure, median taken, relevered. Risk-free rate from the government curve, equity risk premium from Damodaran, who publishes it monthly. The size and stage premium is the reviewer’s judgement, and it is the part you cannot get anywhere else.' },
    mult: null, locked: true, paid: true
  });

  if (r.ebitdaM) {
    rows.push({
      group: 'Public trading multiples',
      parameter: 'NTM EBITDA',
      basis: 'Peer median, forward',
      metric: { value: ffMoney(r.ebitdaM), sub: 'last twelve months' },
      mult: { value: 'in build', source: IN_BUILD },
      locked: true, pending: true
    });
  }

  rows.push({
    group: 'Private rounds',
    parameter: 'Precedents, growth-adjusted',
    basis: 'Fitted across the matched rounds',
    metric: { value: r.ntmM === null ? 'needs revenue' : ffMoney(r.ntmM), sub: 'NTM revenue' },
    mult: null, locked: true, paid: true
  });

  rows.push({
    group: "The reviewer's conclusion",
    parameter: 'Reviewer band',
    basis: 'Where inside these you actually sit',
    metric: { value: 'all rows', sub: 'read by a banker' },
    mult: null, locked: true, paid: true, conclusion: true
  });

  /* THE FIELD IS ORGANISED BY METHOD, and this is the part the landing page always showed and
     the reveal did not. Daniil, 29-Aug: the reveal field "does not really look like the one we have
     on first page, no split into public trading multiples vs private rounds vs DCF". A banker reads
     a football field by method, because the question is never "what is the number" but "which
     approaches agree and which do not". Four rows in a flat list do not answer that. Four rows
     under three headings do.

     THE DISCOUNTED CASH FLOW ROW STAYS IN THE FIELD EVEN THOUGH IT IS NOT DISPLAYED. It sits under
     its own heading with a redacted bar, so a founder can see that the method is run and held back,
     rather than concluding we cannot do it. A method missing from the exhibit reads as a method we
     do not have. */
  const order = ffGroupOrder();
  return rows
    .map(function (row, i) { return [order.indexOf(row.group || ''), i, row]; })
    .sort(function (x, y) { return (x[0] - y[0]) || (x[1] - y[1]); })
    .map(function (t) { return t[2]; });
}

/* The reading order of the exhibit. Context first, then the two market-observed methods, then the
   intrinsic one, then the human. A group not listed here sorts to the front, which is loud enough
   to notice. */
function ffGroupOrder() {
  return ['Where you are today', 'Public trading multiples', 'Private rounds',
          'Discounted cash flow', "The reviewer's conclusion"];
}

/* ---------------- render ---------------- */

function renderField(r) {
  const wrap = document.getElementById('ff');
  if (!wrap) return;

  const rows = ffBuildRows(r);

  /* Axis from visible values only. Locked rows never contribute. */
  const plotted = [];
  rows.forEach(function (row) {
    if (row.locked) return;
    if (typeof row.low === 'number') plotted.push(row.low, row.high);
    if (typeof row.point === 'number') plotted.push(row.point);
  });
  if (!plotted.length) plotted.push(0, Math.max(1, r.raise * 4));
  let lo = Math.min.apply(null, plotted);
  let hi = Math.max.apply(null, plotted);
  if (hi - lo < hi * 0.05) { lo = 0; hi = hi * 1.6; }
  const span = Math.max(hi - lo, hi * 0.2, 0.1);
  const aLo = Math.max(0, lo - span * 0.14);
  const aHi = hi + span * 0.14;
  const pct = v => Math.max(0, Math.min(100, ((v - aLo) / (aHi - aLo)) * 100));

  const ticks = ffTicks(aLo, aHi);
  const grid = ticks.map(t => '<i style="left:' + pct(t).toFixed(2) + '%"></i>').join('');

  const cur = (typeof curSymbol === 'function') ? curSymbol().trim() : '$';
  let html = '<div class="ffx-head"><div>Method</div><div>Metric</div><div>Multiple</div>' +
    '<div>Implied pre-money, ' + escapeHtml(cur) + 'm</div></div>';

  let lastGroup = null;
  rows.forEach(function (row, i) {
    if ((row.group || '') !== lastGroup) {
      lastGroup = row.group || '';
      html += '<div class="ff-group"><span>' + escapeHtml(lastGroup) + '</span></div>';
    }
    let cell;
    if (row.locked) {
      /* Neutral position, never the real one. */
      const l = row.conclusion ? 34 : (24 + (i * 7) % 22);
      const w = row.conclusion ? 24 : 30;
      cell = '<div class="ff-track"><div class="ff-line"></div>' +
        '<div class="ff-bar redacted" style="left:' + l + '%;width:' + w + '%"></div></div>';
    } else if (typeof row.low === 'number') {
      const l = pct(row.low), h = pct(row.high);
      const labels = (h - l) < 16
        ? '<div class="ff-point-label' + (l < 12 ? ' anchor-l' : (h > 88 ? ' anchor-r' : '')) + '" style="left:' +
          ((l + h) / 2).toFixed(2) + '%">' + escapeHtml(ffNum(row.low) + ' – ' + ffNum(row.high)) + '</div>'
        : '<div class="ff-end lo" style="left:' + l.toFixed(2) + '%">' + escapeHtml(ffNum(row.low)) + '</div>' +
          '<div class="ff-end hi" style="left:' + h.toFixed(2) + '%">' + escapeHtml(ffNum(row.high)) + '</div>';
      cell = '<div class="ff-track"><div class="ff-line"></div>' +
        '<div class="ff-bar' + (row.unrefined ? ' unrefined' : '') + '" style="left:' + l.toFixed(2) +
        '%;width:' + Math.max(1.5, h - l).toFixed(2) + '%"></div>' + labels + '</div>';
    } else if (typeof row.point === 'number') {
      const at = pct(row.point);
      const cls = at < 12 ? ' anchor-l' : (at > 88 ? ' anchor-r' : '');
      cell = '<div class="ff-track"><div class="ff-line"></div>' +
        (row.marker
          ? '<div class="ff-diamond" style="left:' + at.toFixed(2) + '%"></div>'
          : '<div class="ff-bar" style="left:' + at.toFixed(2) + '%;width:3px"></div>') +
        '<div class="ff-point-label' + (row.marker ? ' marker' : '') + cls + '" style="left:' + at.toFixed(2) + '%">' +
        escapeHtml(ffNum(row.point)) + '</div></div>';
    } else {
      cell = '<div class="ff-track empty"><span>' + escapeHtml(row.unplotted || 'Not drawn') + '</span></div>';
    }

    const tag = row.paid ? '<span class="lock-tag paid-tag">Locked</span>'
      : (row.pending ? '<span class="lock-tag">In build</span>'
      : (row.unrefined ? '<span class="lock-tag unrefined-tag">Unrefined</span>' : ''));

    html += '<div class="ff-row' + (row.locked ? ' locked' : '') + (row.conclusion ? ' conclusion' : '') + '">' +
      '<div class="ff-param"><strong>' + escapeHtml(row.parameter) + tag + '</strong>' +
        '<span>' + escapeHtml(row.basis) + '</span></div>' +
      ffCell(row.metric, 'ffs-m-' + i, 'ff-metric') +
      ffCell(row.mult, 'ffs-x-' + i, 'ff-mult') +
      '<div class="ff-cell">' + grid + cell + '</div>' +
      (row.metric && row.metric.source ? '<div class="ffm-source" id="ffs-m-' + i + '" style="display:none">' + escapeHtml(row.metric.source) + '</div>' : '') +
      (row.mult && row.mult.source ? '<div class="ffm-source" id="ffs-x-' + i + '" style="display:none">' + escapeHtml(row.mult.source) + '</div>' : '') +
      '</div>';
  });

  html += '<div class="ffx-axis"><div></div><div></div><div></div><div class="ff-cell">' +
    ticks.map(t => '<b style="left:' + pct(t).toFixed(2) + '%">' + ffNum(t) + '</b>').join('') +
    '</div></div>';

  const drawn = rows.filter(x => !x.locked && (typeof x.low === 'number' || typeof x.point === 'number')).length;
  const build = rows.filter(x => x.pending).length;
  const paid = rows.filter(x => x.paid).length;
  html += '<p class="ff-foot">Every drawn bar is the reference metric multiplied by the range beside it. ' +
    'Tap any figure to see the publication it came from and its date. ' +
    drawn + ' drawn, ' + build + ' being wired to live peer data, ' + paid +
    ' in the reviewed report. Locked bars sit in a neutral position, never their real one.</p>';

  wrap.innerHTML = html;
  wrap.style.display = 'block';
}

function prettyMonth(ym) {
  if (!/^\d{4}-\d{2}$/.test(ym)) return ym;
  const months = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'];
  const p = ym.split('-');
  return months[Number(p[1]) - 1] + ' ' + p[0];
}
