/* Fairway football field.
 *
 * Three columns, exactly like a banker's page: the parameter, the reference
 * metrics that went into it, and the implied value. The middle column is the
 * product. Every competitor prints a number with a pre-fixed multiple and no
 * sourcing, so a field without a reference-metrics column is just a calculator
 * with bars on it. Every metric that has a source carries one, revealed on tap
 * or hover, and a row we cannot source honestly is drawn locked rather than
 * filled with something plausible.
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
  if (m >= 1) return c + (m < 10 ? m.toFixed(1) : Math.round(m)) + 'M';
  return c + Math.round(m * 1000) + 'k';
}

/* Each metric is {label, value, source}. A source turns the value into a button. */
function ffMetric(m, id) {
  const val = '<span class="ffm-v">' + escapeHtml(m.value) + '</span>';
  if (!m.source) {
    return '<div class="ffm"><span class="ffm-l">' + escapeHtml(m.label) + '</span> ' + val + '</div>';
  }
  return '<div class="ffm"><span class="ffm-l">' + escapeHtml(m.label) + '</span> ' +
    '<button type="button" class="ffm-src" aria-expanded="false" aria-controls="' + id + '" ' +
    'onclick="ffToggleSource(this)">' + val + '</button>' +
    '<div class="ffm-source" id="' + id + '" hidden>' + escapeHtml(m.source) + '</div></div>';
}

function ffToggleSource(btn) {
  const box = document.getElementById(btn.getAttribute('aria-controls'));
  if (!box) return;
  const open = !box.hasAttribute('hidden');
  if (open) { box.setAttribute('hidden', ''); btn.setAttribute('aria-expanded', 'false'); }
  else { box.removeAttribute('hidden'); btn.setAttribute('aria-expanded', 'true'); }
  if (typeof track === 'function' && !open) track('ff_source_opened', { metric: btn.textContent.slice(0, 40) });
}

/* A label centred on a point runs off the track when the point is near either
   end, so it anchors to whichever side keeps it inside. */
function ffLabel(posPct, text, extraClass) {
  const cls = posPct < 14 ? ' anchor-l' : (posPct > 86 ? ' anchor-r' : '');
  return '<div class="ff-point-label' + (extraClass ? ' ' + extraClass : '') + cls +
    '" style="left:' + posPct.toFixed(2) + '%">' + escapeHtml(text) + '</div>';
}

/* ---------------- the rows ---------------- */

function ffBuildRows(r) {
  const rows = [];
  const sector = responses.sector === 'Other' ? 'Other' : (responses.sector || 'Other');
  const cur = responses.currency || 'USD';
  const raiseM = r.raise;

  const IN_BUILD = 'Being wired to live comparable-company data. Until it is, this row shows the metric it will price rather than a number we invented.';

  /* ---- 1. Stage benchmark. A median is a point, so it is drawn as a point, and
     it is labelled market context rather than a valuation: half the companies in
     a median sit below it. */
  const anchor = STAGE_ANCHOR[responses.stage];
  if (anchor && anchor.post_median_m) {
    const medianLocal = cur === 'USD' ? anchor.post_median_m : fxConvert(anchor.post_median_m, 'USD', cur);
    const metrics = [
      { label: responses.stage + ' median post-money', value: '$' + anchor.post_median_m.toFixed(1) + 'M',
        source: anchor.source + '. ' + anchor.note + ' A cross-sector median is market context, not a valuation of your company: half the companies in it sit below this line.' }
    ];
    if (cur !== 'USD' && medianLocal) {
      metrics.push({ label: 'Converted at', value: (FX.perEur[cur] / FX.perEur.USD).toFixed(4) + ' ' + cur + ' per USD',
        source: FX.source + ', ' + FX.date + '. We convert only at a rate we can point you at.' });
    }
    metrics.push({ label: 'Less midpoint of your raise', value: ffMoney(raiseM) });
    rows.push({
      parameter: 'Stage benchmark',
      basis: 'Market context. Median post-money for the stage, less the round',
      metrics: metrics,
      point: medianLocal ? medianLocal - raiseM : null,
      unplotted: medianLocal ? null : 'The ECB does not publish a reference rate for ' + cur + ', so this is left unconverted rather than converted at a rate we cannot source.',
      locked: false, context: true
    });
  } else {
    rows.push({
      parameter: 'Stage benchmark',
      basis: 'Median post-money for the stage, less the round',
      metrics: [{ label: 'Pre-seed median', value: 'not published', source: 'The cited Carta release covers Seed and Series A only. We would rather draw nothing than guess a pre-seed median.' }],
      unplotted: 'No published anchor at this stage, which is why pre-seed ranges are wide.',
      locked: false, context: true
    });
  }

  /* ---- 2. Where listed multiples currently sit. Shown as context and never
     converted into a valuation of this company. An industry aggregate on a
     trailing basis cannot be applied to a private company without a discount
     somebody invented, and we removed ours rather than keep using it. */
  const pc = PUBLIC_COMPS.sectors[sector];
  if (pc) {
    rows.push({
      parameter: 'Where listed multiples sit',
      basis: 'Market context. The listed sector aggregate, not applied to you',
      metrics: [
        { label: pc.industry + ', ' + pc.n + ' firms', value: pc.ev_sales.toFixed(1) + 'x EV/Sales',
          source: PUBLIC_COMPS.source + ', ' + PUBLIC_COMPS.vintage + '. ' + PUBLIC_COMPS.universe + '.' +
            (pc.note ? ' ' + pc.note : '') +
            ' This is a trailing industry aggregate across every size of company, so it is context rather than a comparable. The rows below replace it with a peer set chosen for your business.' }
      ],
      unplotted: 'An industry aggregate is not a comparable set, and turning one into a valuation needs a discount we would have to invent. We used to. We stopped.',
      locked: false, context: true
    });
  }

  /* ---- 3. NTM revenue multiple. The reference metric is real and computed from
     the founder's own answers today. The multiple is what is still being built. */
  rows.push({
    parameter: 'NTM revenue multiple',
    basis: 'Peer median EV / next twelve months’ revenue, plus or minus 1.5 turns',
    metrics: [
      { label: 'Your NTM revenue', value: r.ntmM === null ? 'needs an exact revenue figure' : ffMoney(r.ntmM),
        source: r.ntmM === null ? 'Give an exact monthly revenue figure and this becomes a number.'
          : 'The sum of your next twelve months, built from ' + fmtPlain(responses.revenue_exact || 0) + ' a month carried forward at ' +
            (r.forwardGrowth === null ? 'no assumed growth' : Math.round(r.forwardGrowth) + '% a year') +
            '. That forward rate is your trailing ' + (r.trailingGrowth === null ? 'growth' : Math.round(r.trailingGrowth) + '%') +
            ' multiplied by a growth persistence factor of 0.75, the median Point Nine measured across 29 early-stage SaaS companies and 96 data pairs. Consensus forward revenue is a sum, so ours is a sum, which is a different and smaller number than your run-rate a year out.' },
      { label: 'Peer median multiple', value: 'in build', source: IN_BUILD }
    ],
    locked: true, pending: true
  });

  /* ---- 4. The same peers, read against the run-rate the company exits on. */
  rows.push({
    parameter: 'ARR multiple, month twelve',
    basis: 'The same peers, applied to your run-rate in twelve months',
    metrics: [
      { label: 'Your ARR at month twelve', value: r.exitArrM === null ? 'needs an exact revenue figure' : ffMoney(r.exitArrM),
        source: r.exitArrM === null ? 'Give an exact monthly revenue figure and this becomes a number.'
          : 'Your run-rate a year from now, not the twelve-month sum, which is why it is the larger of the two. This row values you at a future date, so it reads high against the row above by design. The more of your revenue that recurs, the better that basis holds.' },
      { label: 'Peer median multiple', value: 'in build', source: IN_BUILD }
    ],
    locked: true, pending: true
  });

  /* ---- 5. Growth-adjusted. */
  rows.push({
    parameter: 'Growth-adjusted multiple',
    basis: 'Fitted EV/revenue at your growth rate, from a regression across the peer set',
    metrics: [
      { label: 'Your growth, trailing', value: r.trailingGrowth === null ? (responses.growth || 'not given') : Math.round(r.trailingGrowth) + '% year on year' },
      { label: 'Fitted multiple at that rate', value: 'in the report' }
    ],
    locked: true
  });

  /* ---- 6. DCF. The unlock is the plan, which is a better qualifier than an
     email address, and the blur has a stated reason. */
  rows.push({
    parameter: 'Discounted cash flow',
    basis: 'Cost of capital built from your peer set’s beta',
    metrics: [
      { label: 'Cost of equity', value: 'from peer beta, relevered',
        source: 'Unlevered beta for each company in your peer set at its own capital structure, median taken, relevered. Risk-free rate from the government curve, equity risk premium from Damodaran, who publishes it monthly. The size and stage premium is the reviewer’s judgement, and it is the part you cannot get anywhere else.' },
      { label: 'Needs', value: 'your plan or model', source: 'A DCF needs forecast cash flows, and at this stage the terminal value assumption does most of the work, which is exactly why a person should be behind it. Send a link to your plan or model and the reviewer builds it.' }
    ],
    locked: true, pending: true
  });

  /* ---- 7. EBITDA, forward, only when the founder gave a positive figure. */
  if (r.ebitdaM) {
    rows.push({
      parameter: 'NTM EBITDA multiple',
      basis: 'Peer median EV / next twelve months’ EBITDA',
      metrics: [
        { label: 'Your EBITDA, last twelve months', value: ffMoney(r.ebitdaM) },
        { label: 'Peer median multiple', value: 'in the report', source: 'Forward, like the revenue rows, because that is the basis listed companies trade on.' }
      ],
      locked: true
    });
  }

  /* ---- 8. Private rounds. A valuation cannot be handed to a company with
     different metrics, so this row is a multiple or it is nothing. */
  const revLabel = responses.revenue_exact > 0
    ? ffMoney((responses.revenue_exact * 0.8) / 1e6) + ' to ' + ffMoney((responses.revenue_exact * 1.25) / 1e6) + ' MRR'
    : (responses.revenue || 'pre-revenue');
  rows.push({
    parameter: 'Comparable private rounds',
    basis: 'Revenue multiples paid in recent rounds by companies like yours',
    metrics: [
      { label: 'Filter', value: [responses.stage, sector, revLabel, responses.country || 'your market', 'last 12 months'].join(' · ') },
      { label: 'Multiples paid', value: 'in build',
        source: 'The multiple, never the valuation. Another company’s post-money tells you nothing without the revenue underneath it, so every round in this set carries a revenue figure and a link to where it came from, or it is not in the set.' }
    ],
    locked: true, pending: true
  });

  /* ---- 9. The same precedents, read against growth. */
  rows.push({
    parameter: 'Precedents, growth-adjusted',
    basis: 'Fitted across the matched rounds at your growth rate',
    metrics: [{ label: 'Fitted multiple', value: 'in the report' }],
    locked: true
  });

  /* ---- 10. The conclusion, not a method. */
  rows.push({
    parameter: 'Reviewer band',
    basis: 'The banker’s read on where inside all of the above you actually sit',
    metrics: [{ label: 'Reviewed by hand', value: 'in the report' }],
    locked: true
  });

  return rows;
}

/* ffTotalMetrics used to build the reference metrics for a concluding
   "Indicative range" row at the foot of the field. That row was the headline
   range in another costume: it was positioned from our own coefficients rather
   than derived from anything above it, and it quietly became the number every
   founder read. It is gone, along with the function that fed it. The field ends
   with the reviewer row, because the reviewer is the conclusion. */

/* ---------------- render ---------------- */

function renderField(r) {
  const wrap = document.getElementById('ff');
  if (!wrap) return;

  const rows = ffBuildRows(r);

  /* Axis from visible values only. Locked rows never contribute, and there is no
     headline range feeding it any more, so it can legitimately be near empty. */
  const plotted = [];
  if (r.markerM) plotted.push(r.markerM);
  rows.forEach(function (row) {
    if (row.locked) return;
    if (typeof row.low === 'number') plotted.push(row.low, row.high);
    if (typeof row.point === 'number') plotted.push(row.point);
  });
  if (!plotted.length) plotted.push(0, Math.max(1, r.raise * 4));
  let lo = Math.min.apply(null, plotted);
  let hi = Math.max.apply(null, plotted);
  /* One plotted point on its own gives a degenerate axis, a couple of hundred
     thousand wide, which makes a single tick look like a precise reading. Show
     it against zero instead, which is honest about how little is on the chart. */
  if (hi - lo < hi * 0.05) { lo = 0; hi = hi * 1.6; }
  const span = Math.max(hi - lo, hi * 0.2, 0.1);
  const aLo = Math.max(0, lo - span * 0.12);
  const aHi = hi + span * 0.12;
  const pct = v => Math.max(0, Math.min(100, ((v - aLo) / (aHi - aLo)) * 100));

  let html = '<div class="ff-head"><div>Parameter</div><div>Reference metrics</div><div>Implied pre-money</div></div>';

  /* Marker line first: a point, on its own row, feeding nothing. */
  if (r.markerM) {
    const at = pct(r.markerM);
    const when = responses.last_round_date ? prettyMonth(responses.last_round_date) : 'date not given';
    const kind = responses.last_round_type === 'SAFE or note cap' ? 'cap' : 'pre-money';
    html += '<div class="ff-row marker">' +
      '<div class="ff-param"><strong>Last round</strong><span>Where you were priced, for comparison</span></div>' +
      '<div class="ff-metrics">' +
        ffMetric({ label: 'Priced at', value: ffMoney(r.markerM) + ' ' + kind }, 'ffs-marker-a') +
        ffMetric({ label: 'When', value: when }, 'ffs-marker-b') +
      '</div>' +
      '<div class="ff-cell"><div class="ff-track"><div class="ff-line"></div>' +
        '<div class="ff-diamond" style="left:' + at.toFixed(2) + '%"></div>' +
        ffLabel(at, ffMoney(r.markerM)) +
      '</div></div></div>';
  }

  rows.forEach(function (row, i) {
    let cell;
    if (row.locked) {
      cell = '<div class="ff-track"><div class="ff-line"></div>' +
        '<div class="ff-bar redacted" style="left:26%;width:36%"></div></div>';
    } else if (typeof row.low === 'number') {
      const l = pct(row.low), h = pct(row.high);
      /* A narrow bar cannot carry a label at each end without them colliding, so
         it gets one centred label instead. Two numbers printed on top of each
         other is worse than one printed clearly. */
      const labels = (h - l) < 14
        ? ffLabel((l + h) / 2, ffMoney(row.low) + ' to ' + ffMoney(row.high), 'muted')
        : '<div class="ff-end lo" style="left:' + l.toFixed(2) + '%">' + escapeHtml(ffMoney(row.low)) + '</div>' +
          '<div class="ff-end hi" style="left:' + h.toFixed(2) + '%">' + escapeHtml(ffMoney(row.high)) + '</div>';
      cell = '<div class="ff-track"><div class="ff-line"></div>' +
        '<div class="ff-bar" style="left:' + l.toFixed(2) + '%;width:' + Math.max(1.5, h - l).toFixed(2) + '%"></div>' +
        labels + '</div>';
    } else if (typeof row.point === 'number') {
      const at = pct(row.point);
      cell = '<div class="ff-track"><div class="ff-line"></div>' +
        '<div class="ff-tick" style="left:' + at.toFixed(2) + '%"></div>' +
        ffLabel(at, ffMoney(row.point), 'muted') + '</div>';
    } else {
      cell = '<div class="ff-track empty"><span>' + escapeHtml(row.unplotted || 'Not drawn') + '</span></div>';
    }

    html += '<div class="ff-row' + (row.locked ? ' locked' : '') + (row.context ? ' context' : '') + '">' +
      '<div class="ff-param"><strong>' + escapeHtml(row.parameter) +
        (row.locked ? '<span class="lock-tag">' + (row.pending ? 'In build' : 'Locked') + '</span>' : '') +
        '</strong><span>' + escapeHtml(row.basis) + '</span></div>' +
      '<div class="ff-metrics">' +
        row.metrics.map(function (m, j) { return ffMetric(m, 'ffs-' + i + '-' + j); }).join('') +
      '</div>' +
      '<div class="ff-cell">' + cell + '</div></div>';
  });

  html += '<div class="ff-axis"><span>' + escapeHtml(ffMoney(aLo)) + '</span><span>' + escapeHtml(ffMoney(aHi)) + '</span></div>';

  const contextRows = rows.filter(function (x) { return !x.locked && x.context; }).length;
  const openRows = rows.filter(function (x) { return !x.locked && !x.context; }).length;
  const buildRows = rows.filter(function (x) { return x.locked && x.pending; }).length;
  const lockedRows = rows.filter(function (x) { return x.locked && !x.pending; }).length;
  const bits = [];
  if (openRows) bits.push(openRows + ' method' + (openRows === 1 ? '' : 's') + ' priced');
  if (contextRows) bits.push(contextRows + ' market context');
  if (buildRows) bits.push(buildRows + ' being wired to live peer data');
  if (lockedRows) bits.push(lockedRows + ' in the report');
  html += '<p class="ff-foot">Tap any reference metric to see where it came from. ' +
    bits.join(', ') + '. Locked bars are drawn in a neutral position, not their real one, ' +
    'and nothing on this page is a multiple we typed in ourselves.</p>';

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
