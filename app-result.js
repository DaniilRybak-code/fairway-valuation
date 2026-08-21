/* Result-screen metrics and the price-worth card.
 *
 * Loaded after app.js. Everything here exists because the indicative range was
 * deleted: what the founder now sees first is their own revenue restated on the
 * basis a forward multiple is quoted on, not our opinion of what the company is
 * worth.
 */

/* The median post-money for the stage, in the founder's currency. Real, sourced
   and dated, which is why it is the only valuation-scale anchor the free page is
   allowed to use until the peer engine ships. */
function stageAnchorLocal() {
  const anchor = (typeof STAGE_ANCHOR !== 'undefined') ? STAGE_ANCHOR[responses.stage] : null;
  if (!anchor || !anchor.post_median_m) return null;
  const cur = responses.currency || 'USD';
  const v = cur === 'USD' ? anchor.post_median_m : fxConvert(anchor.post_median_m, 'USD', cur);
  return (typeof v === 'number' && isFinite(v)) ? v : null;
}

function metricTile(value, caption, hint) {
  return '<div class="metric">' +
    '<div class="metric-val">' + escapeHtml(value) + '</div>' +
    '<div class="metric-cap">' + escapeHtml(caption) + '</div>' +
    (hint ? '<div class="metric-hint">' + escapeHtml(hint) + '</div>' : '') +
    '</div>';
}

/* Your revenue restated the way an investor reads it. These are the founder's own
   numbers made precise, not a valuation. */
function paintMetrics(r) {
  const el = document.getElementById('metric-row');
  if (!el) return;
  const tiles = [];

  if (r.ntmM !== null && r.ntmM !== undefined) {
    tiles.push(metricTile(money(r.ntmM), 'Next twelve months’ revenue',
      'The sum of the next twelve months, which is what a forward multiple multiplies.'));
    tiles.push(metricTile(money(r.exitArrM), 'ARR at month twelve',
      'Your run-rate a year from now. A larger number than the one on its left, and a different question.'));
  } else {
    tiles.push(metricTile(responses.revenue || 'Pre-revenue', 'Revenue today',
      'Give an exact figure and we can put a forward number here instead of a band.'));
  }

  if (r.trailingGrowth !== null && r.trailingGrowth !== undefined) {
    tiles.push(metricTile(Math.round(r.trailingGrowth) + '%', 'Growth, last twelve months',
      'Carried forward at ' + Math.round(r.forwardGrowth) + '%, after the 0.75 persistence haircut.'));
  }

  el.innerHTML = tiles.join('');

  /* The one caveat the month-twelve tile has to carry, in the copy rather than a
     footnote. Two rows that disagree is a feature only if the page says why. */
  const cav = document.getElementById('metric-caveat');
  if (!cav) return;
  if (r.exitArrM === null || r.exitArrM === undefined) { cav.style.display = 'none'; return; }
  cav.style.display = 'block';
  const rec = r.recurringPct;
  cav.innerHTML = (rec !== null && rec !== undefined && rec >= 70)
    ? '<strong>Two dates, not two opinions.</strong> The first figure values you today. The second values you in twelve months, if you hold this growth. With ' + Math.round(rec) + '% of your revenue recurring there is a real case for pricing off the month-twelve run-rate, because recurring revenue is the part a buyer can actually count on repeating. That case is exactly what the reviewed report argues.'
    : '<strong>Two dates, not two opinions.</strong> The first figure values you today. The second values you in twelve months, if you hold this growth. The more of your revenue that recurs, the stronger the case for pricing off the month-twelve run-rate rather than the twelve-month sum.';
}

/* What the price is worth, keyed to a published median rather than to a range we
   invented. The old card priced the width of our own made-up spread, which had
   the perverse property that the less certain we were, the more urgent we
   claimed the problem was. */
function paintGapCard(r) {
  const card = document.querySelector('.gap-card');
  if (!card) return;
  const anchorM = stageAnchorLocal();
  if (!anchorM) { card.style.display = 'none'; return; }
  card.style.display = '';

  const raise = r.raise;
  const preA = Math.max(0.1, anchorM - raise);
  const preB = preA * 1.1;
  const dilA = raise / (preA + raise) * 100;
  const dilB = raise / (preB + raise) * 100;
  const pts = dilA - dilB;
  const worthNow = (pts / 100) * (preB + raise);

  document.getElementById('gap-headline').textContent =
    'Pricing 10% higher is worth about ' + money(worthNow) + ' to you.';
  document.getElementById('gap-body').textContent =
    'On a ' + money(raise) + ' raise against the ' + (responses.stage || 'stage') + ' median post-money of ' +
    money(anchorM) + ', published by Carta, you give away ' + dilA.toFixed(1) + '% of the company. Price 10% higher and you give away ' +
    dilB.toFixed(1) + '%. Nothing about the business changes between those two numbers, only whether you can defend the higher one.';
  document.getElementById('gap-future').innerHTML =
    '<strong>Those ' + pts.toFixed(1) + ' points are worth about ' + money(worthNow) +
    ' today, and about ' + money(worthNow * CONFIG.valuationGrowth12m) + ' if the company is worth ' +
    CONFIG.valuationGrowth12m + ' times as much in twelve months.</strong> That is an illustration on an assumed multiple, not a forecast, and it is the reason the price is worth an argument.';
}
