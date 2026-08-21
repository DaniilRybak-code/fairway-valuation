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
  const arrM = (responses.revenue_exact || 0) * 12 / 1e6;
  const cur = responses.currency || 'USD';
  const raiseM = r.raise;

  /* 1. Stage benchmark. A median is a point, so it is drawn as a point, and it is
     labelled market context rather than a valuation: half the companies in a
     median sit below it. */
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
      locked: false,
      context: true
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

  /* 2. Public market comparable. Real, sourced, and computable today. */
  const pc = PUBLIC_COMPS.sectors[sector];
  if (pc && arrM > 0) {
    const gross = arrM * pc.ev_sales;
    const lo = gross * (1 - PUBLIC_COMPS.illiquidity.high);
    const hi = gross * (1 - PUBLIC_COMPS.illiquidity.low);
    const metrics = [
      { label: 'Your ARR', value: ffMoney(arrM) },
      { label: pc.industry + ', ' + pc.n + ' firms', value: pc.ev_sales.toFixed(2) + 'x EV/Sales',
        source: PUBLIC_COMPS.source + ', ' + PUBLIC_COMPS.vintage + '. ' + PUBLIC_COMPS.universe + '.' +
          (pc.note ? ' ' + pc.note : '') },
      { label: 'Less illiquidity discount', value: Math.round(PUBLIC_COMPS.illiquidity.low * 100) + '% to ' + Math.round(PUBLIC_COMPS.illiquidity.high * 100) + '%',
        source: PUBLIC_COMPS.illiquidity.note + '. It is a judgement, not a market observation, which is why it is shown as a range and shown at all.' }
    ];
    rows.push({
      parameter: 'Public market comparable',
      basis: 'Listed sector EV/Revenue applied to your ARR',
      metrics: metrics, low: lo, high: hi, locked: false
    });
  } else if (pc) {
    rows.push({
      parameter: 'Public market comparable',
      basis: 'Listed sector EV/Revenue applied to your ARR',
      metrics: [
        { label: pc.industry + ', ' + pc.n + ' firms', value: pc.ev_sales.toFixed(2) + 'x EV/Sales',
          source: PUBLIC_COMPS.source + ', ' + PUBLIC_COMPS.vintage + '. ' + PUBLIC_COMPS.universe + '.' },
        { label: 'Your ARR', value: 'none yet' }
      ],
      unplotted: 'Nothing to apply the multiple to until there is revenue.',
      locked: false
    });
  }

  /* 3. Growth adjusted. The anchor row, and the one still in build. It says so
     rather than pretending to be a paywall. */
  const g = responses.growth_exact;
  rows.push({
    parameter: 'Growth-adjusted multiple',
    basis: 'Fitted EV/Revenue at your growth rate, from a listed peer regression',
    metrics: [
      { label: 'Your growth', value: (g === null || g === undefined)
        ? (responses.growth || 'not given')
        : g + '% a month, ' + Math.round((Math.pow(1 + g / 100, 12) - 1) * 100) + '% a year' },
      { label: 'Fitted multiple at that rate', value: 'in the report' }
    ],
    locked: true, pending: true
  });

  /* 4. EBITDA. Only when the founder gave a positive figure. */
  if (responses.ebitda_ltm > 0) {
    rows.push({
      parameter: 'EBITDA multiple',
      basis: 'Sector EV/EBITDA applied to your last twelve months',
      metrics: [
        { label: 'Your LTM EBITDA', value: ffMoney(responses.ebitda_ltm / 1e6) },
        { label: 'Sector EV/EBITDA', value: 'in the report' }
      ],
      locked: true
    });
  }

  /* 5. Comparable private rounds. The filter is the interesting part, so it shows. */
  const revLabel = responses.revenue_exact > 0
    ? ffMoney((responses.revenue_exact * 0.8) / 1e6) + ' to ' + ffMoney((responses.revenue_exact * 1.25) / 1e6) + ' MRR'
    : (responses.revenue || 'pre-revenue');
  rows.push({
    parameter: 'Comparable private rounds',
    basis: 'Real rounds filtered to companies like yours',
    metrics: [
      { label: 'Filter', value: [responses.stage, sector, revLabel, responses.country || 'your market', 'last 12 months'].join(' · ') },
      { label: 'Rounds matching', value: 'in the report' }
    ],
    locked: true
  });

  /* 6. Ownership target. Arithmetic on the founder's own answer. */
  rows.push({
    parameter: 'Ownership-target implied',
    basis: 'What the round size implies at a lead fund ownership target',
    metrics: [
      { label: 'Your raise', value: ffMoney(raiseM) },
      { label: 'Divided by target ownership', value: 'in the report' }
    ],
    locked: true
  });

  /* 7. The conclusion, not a method. */
  rows.push({
    parameter: 'Reviewer band',
    basis: 'The banker’s view after reading everything you sent',
    metrics: [{ label: 'Reviewed by hand', value: 'in the report' }],
    locked: true
  });

  return rows;
}

/* The conclusion row states plainly what it is and is not. It is a first pass
   positioned from the answers, not an average of the rows above, and saying so is
   cheaper than being caught implying otherwise. The implied multiple is the
   cross-check a banker would run on it, so it is shown rather than left to the
   founder to work out. */
function ffTotalMetrics(r) {
  const arrM = (responses.revenue_exact || 0) * 12 / 1e6;
  const sector = responses.sector === 'Other' ? 'Other' : (responses.sector || 'Other');
  const pc = PUBLIC_COMPS.sectors[sector];
  const out = [ffMetric({
    label: 'First pass, positioned from your answers',
    value: ffMoney(r.low) + ' to ' + ffMoney(r.high),
    source: 'Not an average of the rows above. It is positioned from your stage, sector, revenue, growth, recurring share and margin, and it is wider than any single method because the two strongest methods are not built yet. A person replaces it within 24 hours.'
  }, 'ffs-total-a')];
  if (arrM > 0 && pc) {
    const impliedMult = r.mid / arrM;
    out.push(ffMetric({
      label: 'Implied EV/Revenue at the mid-point',
      value: impliedMult.toFixed(1) + 'x, against ' + pc.ev_sales.toFixed(2) + 'x listed',
      source: impliedMult > pc.ev_sales
        ? 'This range prices your revenue above the listed sector, which is normal at your stage: the venture market pays a premium to public fundamentals for growth. The size of that premium is what the report has to defend.'
        : 'This range prices your revenue at or below the listed sector. That is unusual at seed and worth understanding before you open a round, because it usually points at revenue quality rather than at the market.'
    }, 'ffs-total-b'));
  }
  return out.join('');
}

/* ---------------- render ---------------- */

function renderField(r) {
  const wrap = document.getElementById('ff');
  if (!wrap) return;

  const rows = ffBuildRows(r);

  /* Axis from visible values only. Locked rows never contribute. */
  const plotted = [r.low, r.high];
  if (r.markerM) plotted.push(r.markerM);
  rows.forEach(function (row) {
    if (row.locked) return;
    if (typeof row.low === 'number') plotted.push(row.low, row.high);
    if (typeof row.point === 'number') plotted.push(row.point);
  });
  const lo = Math.min.apply(null, plotted);
  const hi = Math.max.apply(null, plotted);
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

  /* The conclusion row. Emphasised, because it is the answer. */
  const cl = pct(r.low), ch = pct(r.high);
  html += '<div class="ff-row total">' +
    '<div class="ff-param"><strong>Indicative range</strong><span>Where the reviewer starts from</span></div>' +
    '<div class="ff-metrics">' + ffTotalMetrics(r) + '</div>' +
    '<div class="ff-cell"><div class="ff-track"><div class="ff-line"></div>' +
      '<div class="ff-bar total" style="left:' + cl.toFixed(2) + '%;width:' + Math.max(1.5, ch - cl).toFixed(2) + '%"></div>' +
    '</div></div></div>';

  html += '<div class="ff-axis"><span>' + escapeHtml(ffMoney(aLo)) + '</span><span>' + escapeHtml(ffMoney(aHi)) + '</span></div>';

  const openRows = rows.filter(function (x) { return !x.locked; }).length;
  const lockedRows = rows.length - openRows;
  html += '<p class="ff-foot">Tap any reference metric to see where it came from. ' +
    openRows + ' method' + (openRows === 1 ? '' : 's') + ' open, ' + lockedRows +
    ' in the report. Locked bars are drawn in a neutral position, not their real one.</p>';

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
