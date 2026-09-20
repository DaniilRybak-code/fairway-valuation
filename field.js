/* Fairway football field.
 *
 * Four columns: the method, the reference metric, the multiple, and the chart.
 * The chart takes roughly sixty per cent of the width because it is the product;
 * everything to its left is deliberately compact so the eye runs down the
 * multiples and across the bars.
 *
 * THE RULE THIS FILE EXISTS TO SERVE: every bar must be reproducible from the
 * two columns beside it. Metric times multiple equals bar. If a row cannot show
 * its own arithmetic, it does not belong here, and since 20-Sep-2026 it is not
 * drawn at all: what is missing is named in one line under the field.
 *
 * The axis is scaled from the method rows only. The stage benchmark sits under
 * the axis and never sets the scale.
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
function ffNum(m) {
  if (m >= 10) return Math.round(m).toString();
  const t = Math.round(m * 10) / 10;
  return Number.isInteger(t) ? String(t) : t.toFixed(1);
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

/* THE ENGINE'S ANSWER, HELD HERE SO THE FIELD CAN READ IT.
 *
 * Until 7-Sep-2026 this file drew nine method rows from figures typed into the HTML and printed
 * "in build" where a multiple belonged. From 7-Sep it read the engine's lanes. From 20-Sep-2026 it
 * is the landing's field, drawn from the live payload: the same rows in the same order, the same
 * bar colours, the peers behind each multiple on hover, four group rules and no line per row.
 * Daniil, 20-Sep, on his first live run: "look at the way the football field looks on the landing
 * page... that's how it should look."
 *
 * THE RULES THIS FILE SERVES.
 *   1. Every bar is the metric beside it times the multiple beside it. A row that cannot show its
 *      own arithmetic is not drawn.
 *   2. A row with no number is not drawn at all. Not hatched, not "in build", not "locked". What
 *      was not drawn and why is said once, in one line under the field, so a missing method reads
 *      as a method we could not run for this company rather than one we do not have.
 *   3. The stage benchmark never sets the scale. The axis is scaled from the method rows only. If
 *      the benchmark falls inside that range it is a marker; if it falls outside, it is a note at
 *      the edge of the axis with the figure, and the bars keep their width (Daniil, 20-Sep: "it
 *      should not impact the perception of the rest of the football field").
 *   4. The listed lane is priced on the founder's NEXT twelve months, because the listed multiples
 *      are enterprise value over next-twelve-months revenue. The private lane is priced on the
 *      founder's ARR TODAY, because the private multiples were computed on ARR or last-twelve-months
 *      revenue at the round (of 219 priced rounds, 93 on ARR or run-rate, 120 on LTM or annual
 *      revenue, none forward). Daniil, 20-Sep: "would generally apply those multiples to current ARR
 *      given by the founder". Until 20-Sep both rows multiplied the NTM figure and the private row
 *      overstated by the forward growth.
 *
 * NULL IS THE NORMAL STATE BEFORE THE ENGINE ANSWERS. With no payload the field shows the rows the
 * page can draw on its own (the last round and the unrefined range) and nothing else.
 */
var FF_PAYLOAD = null;
var FF_LAST_R = null;
var FF_PROFILER = null;
var FF_FIGURES = null;

/* The lane a row prices on, and null when the engine has not produced one or the lane carries no
   figures (a locked lane on the free tier keeps its names and loses its numbers, rule E8). */
function ffLane(lane, basis) {
  if (!FF_PAYLOAD || !FF_PAYLOAD.ranges) return null;
  const l = FF_PAYLOAD.ranges[lane];
  if (!l) return null;
  const r = basis ? l[basis] : l[Object.keys(l)[0]];
  if (!r || r.low === null || r.low === undefined) return null;
  return r;
}

/* THE PEERS BEHIND A MULTIPLE, as the landing shows them: name and the multiple applied, one per
   line, on hover. Rounds carry their date beside the name, because a 2022 multiple is a 2022 price. */
function ffPeerTip(rng, unit, header, note) {
  const peers = (rng.peers || []).slice().sort(function (a, b) {
    return (Number(b.multiple) || 0) - (Number(a.multiple) || 0);
  });
  if (!peers.length) return '';
  const rows = peers.slice(0, 12).map(function (p) {
    /* The small print beside a name is the round's date on a private row and the peer's forecast
       growth on the regression row (`sub`). */
    const small = p.date || p.sub;
    const name = '<span>' + escapeHtml(p.company || p.ticker || '') + (small ? '<small>' + escapeHtml(small) + '</small>' : '') + '</span>';
    const m = (typeof p.multiple === 'number') ? (unit === 'x' ? ffNum(p.multiple) + 'x' : ffPerUnit(p.multiple)) : '';
    return '<i>' + name + '<em>' + m + '</em></i>';
  }).join('');
  const more = peers.length > 12 ? '<u>and ' + (peers.length - 12) + ' more</u>' : '';
  return '<div class="peer-tip"><b>' + (header || 'Peer &middot; applied multiple') + '</b>' + rows + more
    + (note ? '<u>' + note + '</u>' : '') + '</div>';
}

/* HOW THE RANGE IS CUT FROM THE NAMES, said under the list, because a founder who sees a peer at
   8.2x above a range that stops at 6.3x deserves the reason. The listed lane runs from the lower
   to the upper quartile of its peers (match_reference.py, the listed summary), the private lane
   from its lowest to its highest round. */
function ffCutNote(rng, lane) {
  const n = (rng.peers || []).length;
  if (n < 2) return '';
  if (lane === 'listed') return 'The range is the middle of these ' + n + ': the top and the bottom are set aside.';
  return 'The range is the full spread of these ' + n + ' rounds.';
}

function ffPerUnit(v) {
  if (v >= 1e6) return '$' + (v / 1e6).toFixed(1) + 'm';
  if (v >= 1e3) return '$' + (v / 1e3).toFixed(1) + 'k';
  return '$' + Math.round(v);
}

/* The multiple cell: the range, how many names, and the hover table. */
function ffMultCell(rng, subLabel, unit, header, lane) {
  const u = unit || 'x';
  const one = ffOneName(rng);
  const fmt = function (v) { return u === 'x' ? ffNum(v) + 'x' : ffPerUnit(v); };
  const value = one ? fmt(rng.low) : fmt(rng.low) + ' &ndash; ' + fmt(rng.high);
  /* A round whose revenue was disclosed as "more than" gives a multiple that is a ceiling, so the
     top of the range is "at most" (the engine's `bounded`). */
  const sub = subLabel + (rng.bounded ? ', top is a ceiling' : '') + (rng.display === 'SCATTER' ? ', they disagree' : '');
  return { html: value, sub: sub, tip: ffPeerTip(rng, u, header, ffCutNote(rng, lane)) };
}

/* ONE NAME IS NEVER A RANGE (rule A7). The engine says so with display DIAMOND; the field draws
   the row as a point and says whose. */
function ffOneName(rng) { return rng.display === 'DIAMOND' || rng.n < 2; }
/* The words for a range in a hover: "10x to 46x", or "10x" when it is one name. */
function ffMults(rng) { return ffOneName(rng) ? ffNum(rng.low) + 'x' : ffNum(rng.low) + 'x to ' + ffNum(rng.high) + 'x'; }
function ffMoneys(m, rng) { return ffOneName(rng) ? ffMoney(m * rng.low) : ffMoney(m * rng.low) + ' to ' + ffMoney(m * rng.high); }

/* THE BAR FOR A METRIC TIMES A RANGE: a bar, a point when the range is one name, and a bar marked
   `scatter` when the engine says the names disagree too much for a band (display SCATTER). */
function ffSpan(rng, metric, bar) {
  if (ffOneName(rng)) return { point: metric * rng.low, pointBar: true, bar: bar };
  return { low: metric * rng.low, high: metric * rng.high, bar: bar + (rng.display === 'SCATTER' ? ' scatter' : '') };
}

/* One method row. `low`/`high` in $m draw a bar; `point` draws a marker; neither means the row is
   not drawn and its `why` goes into the footnote. */
function ffRow(o) { if (o.span) { Object.assign(o, o.span); delete o.span; } return o; }

function ffBuildRows(r) {
  const rows = [];
  const sector = responses.sector === 'Other' ? 'Other' : (responses.sector || 'Other');
  const cur = responses.currency || 'USD';
  const stage = responses.stage || '';
  const notDrawn = [];

  /* THE FOUNDER'S THREE FIGURES, and which row each one prices. */
  const arrM = r.runRateM;                      /* ARR today: the private lane */
  const ntmM = r.ntmM;                          /* next twelve months: the listed lane */
  const gm = (responses.gross_margin === null || responses.gross_margin === undefined) ? null : responses.gross_margin / 100;
  const ntmGpM = (ntmM !== null && gm !== null) ? ntmM * gm : null;

  /* ---- Last round. A marker, feeding nothing. */
  if (r.markerM) {
    const when = responses.last_round_date ? prettyMonth(responses.last_round_date) : 'date not given';
    const kind = responses.last_round_type === 'SAFE or note cap' ? 'cap' : 'pre-money';
    rows.push(ffRow({
      group: '', cls: 'lr-row', parameter: 'Last round', basis: 'Marker only, feeds nothing',
      metric: { value: ffMoney(r.markerM), sub: kind + ', ' + when },
      mult: null, point: r.markerM, marker: true, bar: ''
    }));
  }

  /* ---- Public trading multiples. */
  const pc = PUBLIC_COMPS.sectors[sector];
  if (pc && arrM > 0 && ntmM) {
    const a = arrM * pc.ev_sales, b = ntmM * pc.ev_sales;
    rows.push(ffRow({
      group: 'Public trading multiples', cls: 'unref',
      parameter: 'Unrefined range', tag: 'Unrefined', basis: 'Before any comparable set is chosen',
      metric: { value: ffMoney(arrM) + ' &middot; ' + ffMoney(ntmM), sub: 'ARR &middot; NTM revenue',
        source: PUBLIC_COMPS.source + ', ' + PUBLIC_COMPS.vintage + '. ' + PUBLIC_COMPS.universe + '.' + (pc.note ? ' ' + pc.note : '') },
      mult: { html: pc.ev_sales.toFixed(1) + 'x', sub: pc.n + ' listed firms',
        tipText: pc.industry + ': every listed company in the industry, from the largest in the world down, with no adjustment for the fact that you are private and small. The low end is ' + pc.ev_sales.toFixed(1) + 'x on your ARR today, the high end the same multiple on your next twelve months.' },
      low: Math.min(a, b), high: Math.max(a, b), bar: 'unrefined',
      barTip: ffMoney(arrM) + ' of ARR and ' + ffMoney(ntmM) + ' of NTM revenue, each times ' + pc.ev_sales.toFixed(1) + 'x: ' + ffMoney(Math.min(a, b)) + ' to ' + ffMoney(Math.max(a, b)) + '.'
    }));
  }

  const listedRev = ffLane('listed', 'REVENUE');
  if (listedRev && ntmM) {
    const m = ffMultCell(listedRev, listedRev.n + ' core peer' + (listedRev.n === 1 ? '' : 's'), 'x', 'Peer &middot; EV / NTM revenue', 'listed');
    rows.push(ffRow({
      group: 'Public trading multiples',
      parameter: 'Core peer set', basis: 'EV / NTM revenue &middot; ' + listedRev.n + ' named peer' + (listedRev.n === 1 ? '' : 's'),
      metric: { value: ffMoney(ntmM), sub: 'next twelve months', source: ffNtmSource(r) },
      mult: m, span: ffSpan(listedRev, ntmM, 'grey'),
      barTip: ffMoney(ntmM) + ' of your NTM revenue, multiplied by the ' + ffMults(listedRev) + (ffOneName(listedRev) ? ' of your one core peer: ' : ' range implied by your ' + listedRev.n + ' core peers: ') + ffMoneys(ntmM, listedRev) + '.'
    }));
  } else if (FF_PAYLOAD) {
    notDrawn.push('the core peer set on revenue (' + (ntmM ? 'no listed peer with a usable multiple' : 'no revenue given') + ')');
  }

  const listedGp = ffLane('listed', 'GROSS_PROFIT');
  if (listedGp && ntmGpM) {
    const m = ffMultCell(listedGp, 'same peers', 'x', 'Peer &middot; EV / gross profit', 'listed');
    rows.push(ffRow({
      group: 'Public trading multiples',
      parameter: 'Core peer set', basis: 'EV / gross profit &middot; same peers',
      metric: { value: ffMoney(ntmGpM), sub: 'NTM gross profit', source: 'Your next twelve months of revenue at your ' + Math.round(gm * 100) + '% gross margin.' },
      mult: m, span: ffSpan(listedGp, ntmGpM, 'grey2'),
      barTip: ffMoney(ntmGpM) + ' of NTM gross profit, multiplied by the ' + ffMults(listedGp) + ' implied by the same peers on gross profit: ' + ffMoneys(ntmGpM, listedGp) + '.'
    }));
  }

  /* ---- The growth regression. Daniil, 20-Sep-2026: read at the founder's FORWARD growth (the plan
     from step 4; the trailing rate only stands in when no plan was given), drawn with a callout
     when growth explains less than 40% of the spread (R-squared below 0.40), and named under the
     field with the numbers when it cannot be read at all. selector/regression.py is the other half. */
  const reg = FF_PAYLOAD && FF_PAYLOAD.regression;
  const regBasis = reg && reg.growth_basis === 'plan' ? 'planned' : 'trailing';
  const regAt = reg ? 'your ' + Math.round(reg.growth) + '% ' + regBasis + ' growth' : '';
  const regStandIn = reg && reg.growth_basis !== 'plan'
    ? ' No plan was given at step 4, so your last twelve months stand in; your peers’ rates are forecasts, so a plan is the better match.'
    : '';
  if (reg && typeof reg.low === 'number' && ntmM) {
    /* The points the line was fitted through, shown the way the peer sets are: name and multiple.
       The engine calls the multiple `mult` here and `multiple` in the lanes. */
    const regPeers = (reg.peers || []).map(function (p) { return { company: p.company, ticker: p.ticker, multiple: p.mult, sub: (typeof p.growth === 'number' ? Math.round(p.growth) + '%' : '') }; });
    const r2Text = 'R² ' + reg.r2.toFixed(2);
    const weak = !!reg.weak_fit;
    rows.push(ffRow({
      group: 'Public trading multiples', cls: weak ? 'weak' : '',
      parameter: 'Regression analysis', basis: 'Multiple vs forward growth, read at ' + escapeHtml(regAt),
      metric: { value: ffMoney(ntmM), sub: 'NTM revenue', source: ffNtmSource(r) },
      mult: { html: ffNum(reg.low) + 'x &ndash; ' + ffNum(reg.high) + 'x', sub: reg.n + ' peers, ' + r2Text + (weak ? ', weak fit' : ''),
        tip: ffPeerTip({ peers: regPeers }, 'x', 'Fitted through &middot; forecast growth &middot; own multiple. Read at ' + escapeHtml(regAt) + ', a tenth either side: ' + ffNum(reg.low) + 'x to ' + ffNum(reg.high) + 'x.',
          'Their growth is a forecast, ' + reg.peer_growth_low + '% to ' + reg.peer_growth_high + '% a year.' + escapeHtml(regStandIn)) },
      low: ntmM * reg.low, high: ntmM * reg.high, bar: 'reg',
      barTip: ffMoney(ntmM) + ' of NTM revenue at ' + ffNum(reg.low) + 'x to ' + ffNum(reg.high) + 'x off the regression: ' + ffMoney(ntmM * reg.low) + ' to ' + ffMoney(ntmM * reg.high) + '.',
      callout: weak
        ? 'Weak fit: growth explains only ' + Math.round(reg.r2 * 100) + '% of the spread in these ' + reg.n + ' peers’ multiples (' + r2Text + '). Read this range as a rough guide, not a price.'
        : null
    }));
  } else if (reg && reg.refused) {
    /* Every reason that applies, with the numbers: a founder who asks "why not?" gets a sentence,
       not an adjective. A weak fit alone no longer refuses; it draws with the callout above. */
    const why = [];
    if (reg.refused === 'OUT_OF_RANGE') why.push(regAt + ' sits outside the ' + reg.peer_growth_low + '% to ' + reg.peer_growth_high + '% your ' + reg.n + ' listed peers are expected to grow at, so reading the line there would be a guess' + (reg.weak_fit ? ' (and growth explains only ' + Math.round((reg.r2 || 0) * 100) + '% of the spread in their multiples, R² ' + (typeof reg.r2 === 'number' ? reg.r2.toFixed(2) : '?') + ')' : ''));
    if (reg.refused === 'TOO_FEW') why.push('only ' + reg.n + ' listed peers carry both a growth rate and a multiple, and a line needs six');
    if (reg.refused === 'NEGATIVE') why.push('the line through your ' + reg.n + ' listed peers implies a multiple at or below zero at ' + regAt);
    if (!why.length) why.push('the fitted line could not be published for this set');
    notDrawn.push('the growth regression: ' + why.join('; and ') + (reg.growth_basis !== 'plan' ? '. No plan was given at step 4, so your last twelve months stood in' : ''));
  } else if (FF_PAYLOAD && r.trailingGrowth === null && r.plannedGrowth === null) {
    notDrawn.push('the growth regression (no growth rate given)');
  } else if (FF_PAYLOAD) {
    notDrawn.push('the growth regression (too few listed peers carry both a growth rate and a multiple to fit a line)');
  }

  /* ---- Private rounds. */
  const priv = ffLane('private', 'REVENUE');
  if (priv && arrM > 0) {
    const m = ffMultCell(priv, priv.n + ' matched round' + (priv.n === 1 ? '' : 's'), 'x', 'Round &middot; revenue multiple', 'private');
    rows.push(ffRow({
      group: 'Private rounds',
      parameter: 'Precedent transactions', basis: 'Revenue multiple at pricing',
      metric: { value: ffMoney(arrM), sub: 'ARR today', source: 'Your ARR today, because these rounds were priced on the revenue the company had at the time of the round, not on a forecast.' },
      mult: m, span: ffSpan(priv, arrM, 'priv'),
      barTip: ffMoney(arrM) + ' of your ARR today, multiplied by the ' + ffMults(priv) + ' that investors paid in the ' + priv.n + ' matched round' + (priv.n === 1 ? '' : 's') + ': ' + ffMoneys(arrM, priv) + '.'
    }));
  } else if (FF_PAYLOAD) {
    notDrawn.push('the precedent transactions (' + (arrM > 0 ? 'no matched round with a usable multiple' : 'no revenue given') + ')');
  }

  /* Per-user and other private readings, wherever the browser holds the founder's own count. The
     arithmetic is priceCharts() in reveal-figures.js, the same one check 15 recomputes. */
  /* priceCharts works in US dollar millions (the figures are converted before they are multiplied);
     the axis is in the founder's currency, so a per-unit row is brought back at the same ECB rate,
     and left undrawn rather than mis-scaled when there is no rate. */
  const usdToLocal = cur === 'USD' ? 1 : ((typeof fxConvert === 'function') ? fxConvert(1, 'USD', cur) : null);
  if (FF_PAYLOAD && FF_FIGURES && typeof priceCharts === 'function' && usdToLocal) {
    priceCharts(FF_PAYLOAD.charts, FF_FIGURES).forEach(function (c) {
      if (c.lane !== 'private' || c.basis === 'REVENUE' || !c.priced) return;
      const rng = ffLane('private', c.basis);
      if (!rng) return;
      const perUnit = (typeof unitOf === 'function' && unitOf(c.basis) !== 'multiple');
      /* The metric in the founder's currency, in millions, so metric times multiple is the bar in
         the axis unit: a count times dollars per unit is dollars, hence the million for per-unit. */
      const metricM = c.founder_metric * usdToLocal / (perUnit ? 1e6 : 1);
      /* The engine's label is "dollars of enterprise value per paying subscriber" or "enterprise
         value to gross revenue"; the row says the same in the landing's shorthand. A brand's or
         retailer's gross figure is called GMV, as the question that asked for it is (Daniil,
         20-Sep-2026: "gross sales is a misleading term, let's use GMV"). */
      let noun = String(c.label || '').replace(/^dollars of enterprise value per /, '').replace(/^enterprise value to /, '');
      if (c.basis === 'REVENUE_GROSS' && responses.fork === 'ecommerce') noun = 'GMV';
      const basisText = perUnit ? 'EV per ' + noun : 'EV / ' + noun;
      const count = Math.round(c.founder_metric).toLocaleString('en-GB');
      const m = ffMultCell(rng, perUnit ? 'per ' + noun : 'same rounds', perUnit ? '$' : 'x', 'Round &middot; ' + (perUnit ? 'paid per ' + noun : 'multiple'), 'private');
      rows.push(ffRow({
        group: 'Private rounds',
        parameter: 'Precedent transactions', basis: escapeHtml(basisText) + ' &middot; same rounds',
        metric: { value: perUnit ? count : ffMoney(c.founder_metric * usdToLocal), sub: escapeHtml(perUnit ? noun + 's today' : noun + ', same period as your ARR') },
        mult: m, span: ffSpan(rng, metricM, 'priv2'),
        barTip: (perUnit ? count + ' ' + noun + 's' : ffMoney(c.founder_metric * usdToLocal) + ' of ' + noun) + ', times what the same rounds paid: ' + ffMoneys(metricM, rng) + '.'
      }));
    });
  }

  if (FF_PAYLOAD) {
    notDrawn.push('the discounted cash flow and the reviewer band (both come with the banker read, once you share your figures)');
  }

  return { rows: rows, notDrawn: notDrawn, stage: stage };
}

function ffNtmSource(r) {
  const monthly = responses.revenue_exact || 0;
  if (!(monthly > 0) || r.ntmM === null) return 'Give a revenue figure and this becomes a number.';
  const own = responses.ntm_revenue_exact;
  if (own !== null && own !== undefined && own > 0) {
    return 'Your own target for the next twelve months, ' + fmtPlain(own) + ', used as you gave it.';
  }
  return 'The sum of your next twelve months, built from ' + fmtPlain(monthly) + ' a month growing at '
    + (r.forwardGrowth === null ? 'no assumed growth' : Math.round(r.forwardGrowth) + '% a year') + '. '
    + (r.forwardBasis === 'plan' ? 'That is the growth you plan, used exactly as you gave it.'
      : (r.forwardBasis === 'trailing' ? 'You gave no plan, so that is your last twelve months carried forward.'
        : 'Derived from the growth band you chose.'))
    + ' Forward consensus revenue is a sum, so ours is a sum.';
}

/* ---------------- the stage benchmark: a marker inside the scale, a note outside it ---------------- */
function ffBenchmark(r) {
  const anchor = STAGE_ANCHOR[responses.stage];
  if (!anchor || !anchor.post_median_m) return null;
  const cur = responses.currency || 'USD';
  const medianLocal = cur === 'USD' ? anchor.post_median_m : fxConvert(anchor.post_median_m, 'USD', cur);
  if (!medianLocal) return null;
  return {
    value: medianLocal - r.raise,
    label: responses.stage + ' median, less your raise',
    text: 'Median ' + responses.stage + ' post-money of $' + anchor.post_median_m.toFixed(1) + 'm (' + anchor.source + '), less the ' + ffMoney(r.raise) + ' you are raising: ' + ffMoney(medianLocal - r.raise) + '. A cross-sector median, market context and not a valuation of you.'
  };
}

/* ---------------- render ---------------- */

/* CALLED BY reveal-client.js WHEN THE ENGINE ANSWERS. */
function renderFieldFromPayload(payload, figures, profiler) {
  FF_PAYLOAD = payload || null;
  FF_FIGURES = figures || null;
  FF_PROFILER = profiler || null;
  if (FF_LAST_R) renderField(FF_LAST_R);
}

function renderField(r) {
  FF_LAST_R = r;
  const wrap = document.getElementById('ff');
  if (!wrap) return;

  const built = ffBuildRows(r);
  const rows = built.rows;

  /* AXIS FROM THE METHOD ROWS ONLY. The benchmark never contributes (rule 3 above). */
  const plotted = [];
  rows.forEach(function (row) {
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
  const cur = (typeof curSymbol === 'function') ? curSymbol().trim() : '$';

  /* The card's head names the unit, as the landing's does. */
  const cap = document.querySelector('#ff-card .cap');
  if (cap) cap.innerHTML = 'Implied pre-money, ' + escapeHtml(cur) + 'm<span class="hover-hint">hover a figure, multiple or bar for the working</span>';
  wrap.classList.add('ffx');

  let html = '';

  /* READ AS. The engine's read of the company, in one line, because the peers follow from it and
     the founder is the person best placed to say it is wrong. */
  if (FF_PROFILER && FF_PROFILER.archetype) {
    const sells = String(FF_PROFILER.product_tags || '').split('|').filter(Boolean).slice(0, 3).join(', ');
    html += '<p class="ff-readas">Compared as <b>' + escapeHtml(FF_PROFILER.archetype) + '</b>'
      + (sells ? ', selling ' + escapeHtml(sells.toLowerCase()) : '') + '. '
      + '<button type="button" class="link-btn" onclick="backToStart()">Not right? Start again</button></p>';
  }

  /* THE SAFE SENTENCE. Daniil, 20-Sep-2026: a founder at pre-seed or seed should be told that the
     round is most likely a SAFE, so the bars are read as reference and not as a price. */
  if (built.stage === 'Pre-seed' || built.stage === 'Seed') {
    html += '<p class="ff-safe">At ' + escapeHtml(built.stage.toLowerCase()) + ', the round is most likely a SAFE with a cap: the cap is set by the round size and the ownership investors expect, not by comparables. Read the bars as what the market pays for revenue like yours, not as your price.</p>';
  }

  let lastGroup = null;
  rows.forEach(function (row, i) {
    if (row.group && row.group !== lastGroup) {
      lastGroup = row.group;
      html += '<div class="ff-group">' + escapeHtml(lastGroup) + '</div>';
    }
    let cell;
    if (typeof row.low === 'number') {
      const l = pct(row.low), h = pct(row.high);
      const narrow = (h - l) < 16;
      const labels = narrow
        ? '<div class="ff-point-label' + (l < 12 ? ' anchor-l' : (h > 88 ? ' anchor-r' : '')) + '" style="left:' + ((l + h) / 2).toFixed(2) + '%">' + escapeHtml(ffNum(row.low) + ' – ' + ffNum(row.high)) + '</div>'
        : '<div class="ff-end lo" style="left:' + l.toFixed(2) + '%">' + escapeHtml(ffNum(row.low)) + '</div>'
          + '<div class="ff-end hi" style="left:' + h.toFixed(2) + '%">' + escapeHtml(ffNum(row.high)) + '</div>';
      cell = '<div class="ff-track' + (row.barTip ? ' has-tip' : '') + '"' + (row.barTip ? ' data-tip="' + escapeHtml(row.barTip) + '"' : '') + '><div class="ff-line"></div>'
        + '<div class="ff-bar ' + (row.bar || '') + '" style="left:' + l.toFixed(2) + '%;width:' + Math.max(1.5, h - l).toFixed(2) + '%"></div>' + labels + '</div>';
    } else if (typeof row.point === 'number' && row.pointBar) {
      /* One name: a point on the scale, never a bar of no width. */
      const at = pct(row.point);
      const cls = at < 12 ? ' anchor-l' : (at > 88 ? ' anchor-r' : '');
      cell = '<div class="ff-track' + (row.barTip ? ' has-tip' : '') + '"' + (row.barTip ? ' data-tip="' + escapeHtml(row.barTip) + '"' : '') + '><div class="ff-line"></div>'
        + '<div class="ff-bar ' + (row.bar || '') + ' one" style="left:' + at.toFixed(2) + '%;width:4px"></div>'
        + '<div class="ff-point-label' + cls + '" style="left:' + at.toFixed(2) + '%">' + escapeHtml(ffNum(row.point)) + ', one name</div></div>';
    } else if (typeof row.point === 'number') {
      const at = pct(row.point);
      const cls = at < 12 ? ' anchor-l' : (at > 88 ? ' anchor-r' : '');
      cell = '<div class="ff-track"><div class="ff-line"></div>'
        + '<div class="ff-diamond" style="left:' + at.toFixed(2) + '%"></div>'
        + '<div class="ff-point-label marker' + cls + '" style="left:' + at.toFixed(2) + '%">' + escapeHtml(ffNum(row.point)) + '</div></div>';
    } else {
      return;
    }

    const tag = row.tag ? '<span class="lock-tag unrefined-tag">' + escapeHtml(row.tag) + '</span>' : '';
    const metric = row.metric
      ? '<div class="ff-metric' + (row.metric.source ? ' has-tip' : '') + '"' + (row.metric.source ? ' data-tip="' + escapeHtml(row.metric.source) + '"' : '') + '>' + row.metric.value
        + (row.metric.sub ? '<span class="sub">' + row.metric.sub + '</span>' : '') + '</div>'
      : '<div class="ff-metric"></div>';
    let mult;
    if (!row.mult) {
      mult = '<div class="ff-mult">&mdash;</div>';
    } else if (row.mult.tip) {
      mult = '<div class="ff-mult has-peers">' + row.mult.html + '<span class="sub">' + row.mult.sub + '</span>' + row.mult.tip + '</div>';
    } else {
      mult = '<div class="ff-mult' + (row.mult.tipText ? ' has-tip' : '') + '"' + (row.mult.tipText ? ' data-tip="' + escapeHtml(row.mult.tipText) + '"' : '') + '>' + row.mult.html + '<span class="sub">' + row.mult.sub + '</span></div>';
    }

    html += '<div class="ff-row ' + (row.cls || '') + '">'
      + '<div class="ff-param"><strong>' + escapeHtml(row.parameter) + tag + '</strong><span>' + row.basis + '</span></div>'
      + metric + mult
      + '<div class="ff-cell">' + cell + '</div>'
      + '</div>';
    /* THE CALLOUT, under the row it disclaims (Daniil, 20-Sep-2026: a weak regression is drawn
       and disclaimed "with a callout to that range on FF", not hidden). */
    if (row.callout) html += '<p class="ff-callout">' + escapeHtml(row.callout) + '</p>';
  });

  html += '<div class="ffx-axis"><div></div><div></div><div></div><div class="ff-cell">'
    + ticks.map(t => '<b style="left:' + pct(t).toFixed(2) + '%">' + ffNum(t) + '</b>').join('')
    + '</div></div>';

  /* THE STAGE BENCHMARK, in a row of its own under the axis: a marker where it falls inside the
     scale, a note at the edge where it falls outside. Either way the bars above keep their width. */
  const bench = ffBenchmark(r);
  if (bench) {
    let mark;
    if (bench.value >= aLo && bench.value <= aHi) {
      const at = pct(bench.value);
      const cls = at < 14 ? ' anchor-l' : (at > 86 ? ' anchor-r' : '');
      mark = '<div class="ff-bench has-tip' + cls + '" data-tip="' + escapeHtml(bench.text) + '" style="left:' + at.toFixed(2) + '%"><i></i><span>' + escapeHtml(bench.label) + ' ' + ffNum(bench.value) + '</span></div>';
    } else {
      const side = bench.value > aHi ? 'right' : 'left';
      mark = '<div class="ff-bench-note ' + side + ' has-tip" data-tip="' + escapeHtml(bench.text) + '">' + (side === 'left' ? '&larr; ' : '') + escapeHtml(bench.label) + ': ' + escapeHtml(ffMoney(bench.value)) + ', off this scale' + (side === 'right' ? ' &rarr;' : '') + '</div>';
    }
    html += '<div class="ff-bench-row"><div></div><div></div><div></div><div class="ff-cell">' + mark + '</div></div>';
  }

  if (built.notDrawn.length) {
    html += '<p class="ff-foot">Not drawn: ' + escapeHtml(built.notDrawn.join('; ')) + '.</p>';
  }

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
