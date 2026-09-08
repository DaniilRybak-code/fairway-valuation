/* THE FIGURES, AND THE MULTIPLICATION. Both live in this browser and neither one leaves it.
 *
 * The engine sends multiples. This file holds the founder's own figures and multiplies. That split
 * is the whole privacy architecture: a multiple is a fact about other companies and a figure is a
 * fact about this one, so the first can travel and the second does not have to.
 *
 * THE SPECIFICATION IS tools/check_reveal_payload.py, assertion 4:
 *
 *     founder_low  = round(founder_metric * low,  2)
 *     founder_high = round(founder_metric * high, 2)
 *
 * That is what the engine recomputes server-side for the 102 fixtures, and check 15 runs the
 * functions below against real payloads built from the real engine and asserts they agree. Two
 * implementations of one sum drift; a check that compares them is how you find out on the day.
 *
 * NO BROWSER STORAGE. Not localStorage, not sessionStorage, not IndexedDB, not a cookie. The
 * figures live in one variable for as long as the tab is open and are gone when it closes. A
 * figure written to disk is a figure that survives the promise made on the page.
 */

/* ---------------------------------------------------------------------------
 * WHICH BASIS THE PAGE CAN PRICE, AND WHAT IT PRICES IT FROM.
 *
 * The keys must be keys of BASIS_FOUNDER_FIELD in selector/match_reference.py. Check 15 asserts
 * that, so a basis renamed on one side fails loudly rather than silently pricing nothing.
 *
 * THE LIVE QUIZ COLLECTS ONE FIGURE. Step 3 asks for current monthly revenue and that is the only
 * amount on the page that any basis can use. Everything else the engine can price on (a trailing
 * revenue figure, a gross revenue figure, book value, net income, originations, volume, and every
 * user count) is asked by a fork in selector/quiz_fork.py that is not on the live page yet.
 *
 * A BASIS WITH NO FIGURE IS NOT AN ERROR. Daniil, 6-Sep-2026: a founder who gives no numbers at
 * all still gets the peer charts, because a range counts the comparable rounds that exist and only
 * the PRICE needs a founder figure. `priced: false` is the normal case and the chart is still the
 * argument.
 * ------------------------------------------------------------------------- */

/* Monthly revenue times twelve, in USD millions. This is the page's own long-standing convention:
   computeResult() calls it runRateM and field.js prints it as ARR. It is carried across here
   unchanged rather than reinvented, and it is a RUN RATE, which is why it prices the ARR basis and
   not the trailing REVENUE one. */
function figureArrMusd(responses) {
  var r = responses || {};
  var monthly = Number(r.revenue_exact);
  if (!isFinite(monthly) || monthly <= 0) return null;
  var annual = monthly * 12;
  var cur = r.currency || 'USD';
  if (cur === 'USD') return annual / 1e6;
  /* fxConvert lives in data-public-comps.js and returns null rather than guessing when the ECB
     does not publish the rate. A figure we cannot convert with a sourced rate is left unpriced. */
  if (typeof fxConvert !== 'function') return null;
  var usd = fxConvert(annual, cur, 'USD');
  return (typeof usd === 'number' && isFinite(usd)) ? usd / 1e6 : null;
}

/* THE COUNT BASES, mirrored from COUNT_BASES in selector/match_reference.py. Check 15 asserts the
   two lists are the same, because they are one fact written in two languages.

   THE PAGE NEEDS THEM FOR THE AXIS. A revenue multiple is "times" and a per-user reading is
   "dollars of enterprise value per user". Drawing 3.0x to 4.4x on the same axis as $2,700 a
   subscriber makes the first one a dot at the left edge and says nothing true about either. The
   charts are grouped by unit and each group is scaled on its own. */
var COUNT_BASES = ['PAYING_SUBSCRIBERS', 'BORROWERS', 'MEMBERS', 'CUSTOMERS', 'BUSINESS_CUSTOMERS',
                   'MERCHANTS', 'ACTIVE_USERS', 'REGISTERED_USERS'];

function unitOf(basis) {
  return COUNT_BASES.indexOf(basis) >= 0 ? 'per-user' : 'multiple';
}

/* A FORK ANSWER, IN US DOLLAR MILLIONS. The fork questions ask for a figure in the founder's own
   currency, the one they picked at step 3, exactly like the revenue question does. This is the same
   conversion figureArrMusd does, factored out so the two cannot drift. Returns null rather than
   guessing when the ECB publishes no rate for the currency. */
function figureForkMusd(responses, key) {
  var r = responses || {};
  var v = Number(r[key]);
  if (!isFinite(v) || v <= 0) return null;
  var cur = r.currency || 'USD';
  if (cur === 'USD') return v / 1e6;
  if (typeof fxConvert !== 'function') return null;
  var usd = fxConvert(v, cur, 'USD');
  return (typeof usd === 'number' && isFinite(usd)) ? usd / 1e6 : null;
}

/* A COUNT IS NOT AN AMOUNT. Subscribers, borrowers and merchants are numbers of things, so they
   are never converted and never divided by a million: the engine's per-unit readings are dollars of
   enterprise value per ONE of them. */
function figureForkCount(responses, key) {
  var v = Number((responses || {})[key]);
  return (isFinite(v) && v > 0) ? v : null;
}

function forkMoney(key, label, note) {
  return { label: label, from: key, note: note,
           value: function (r) { return figureForkMusd(r, key); } };
}
function forkCount(key, label, note) {
  return { label: label, from: key, note: note,
           value: function (r) { return figureForkCount(r, key); } };
}

var FIGURE_SOURCES = {
  ARR: {
    label: 'run-rate revenue',
    from: 'revenue_exact',
    note: 'your monthly revenue times twelve, in US dollar millions',
    /* THE FORK'S OWN ARR WINS WHERE THERE IS ONE. The software fork asks for ARR directly, which is
       a better answer than twelve times a month, so it is used when the founder gave it and the
       monthly figure stands in when they did not. */
    value: function (r) {
      var own = figureForkMusd(r, 'arr');
      return own !== null ? own : figureArrMusd(r);
    }
  },

  /* ---------------------------------------------------------------------------
   * EVERY BASIS BELOW REACHED NOTHING UNTIL 7 SEPTEMBER, because the nine forks in
   * selector/quiz_fork.py had never been rendered on the page. Check 15 printed
   * "PRICEABLE 1 of 15 bases" on every run and it was right.
   *
   * The forks are on the page now (quiz-fork.js), so their answers arrive on `responses` under the
   * keys quiz_fork.apply_answers reads, and each one prices the basis the engine matches it to.
   * BASIS_FOUNDER_FIELD in selector/match_reference.py is the other half of this map, and check 15
   * asserts the two agree, so a basis renamed on one side fails loudly.
   *
   * EVERY ONE OF THESE IS AN AMOUNT AND NONE OF THEM LEAVE (rule E9). They are multiplied here,
   * beside the founder, and reveal-request.js has never carried one of these keys.
   * ------------------------------------------------------------------------- */
  REVENUE: forkMoney('net_revenue', 'net revenue',
      'your net revenue over the last twelve months, in US dollar millions'),
  REVENUE_GROSS: forkMoney('gross_revenue', 'gross revenue',
      'your gross revenue over the same period, in US dollar millions'),
  BOOK: forkMoney('book_value', 'book value',
      'the book value of the business, in US dollar millions'),
  ORIGINATIONS: forkMoney('originations', 'originations',
      'what you lent over the last twelve months, in US dollar millions'),
  THROUGHPUT: forkMoney('throughput_volume', 'throughput',
      'what moved across your platform over the last twelve months'),
  PAYING_SUBSCRIBERS: forkCount('paying_subscribers', 'paying subscribers',
      'how many people pay you today'),
  BORROWERS: forkCount('borrowers', 'borrowers',
      'how many borrowers you have today')
};

/* WHY EVERY OTHER BASIS IS UNPRICED TODAY, said in the code so that nobody has to guess whether it
   is a bug. Printed by check 15 so the list stays honest as the forks reach the page. */
/* WHAT IS STILL UNPRICED, AND WHY, said in the code so nobody has to guess whether it is a bug.
   Printed by check 15 on every run. This list was fourteen entries long until 7 September, when the
   forks reached the page; every one that came off did so because a fork now asks the question. */
var BASIS_NOT_PRICED = {
  EARNINGS: 'this basis prices on net income. The lending fork asks for net income and the engine '
         + 'reads it, but EARNINGS is a LISTED-lane multiple on price to earnings, which needs a '
         + 'share count we do not ask a private company for. Ruling, not a wiring job.',
  MEMBERS: 'no fork asks for a member count. The consumer subscription fork asks for paying '
         + 'subscribers, which is a different thing and is priced separately.',
  CUSTOMERS: 'no fork asks a consumer business for a customer count distinct from subscribers.',
  BUSINESS_CUSTOMERS: 'no fork asks for a business customer count. Worth adding to the software '
         + 'fork, and it is a question rather than a wiring job.',
  MERCHANTS: 'the payments fork does not ask how many merchants. Same shape as the above.',
  ACTIVE_USERS: 'no fork asks for an active user count.',
  REGISTERED_USERS: 'no fork asks for a registered user count.'
};

/* ---------------------------------------------------------------------------
 * THE STORE. One variable, one tab, no disk.
 * ------------------------------------------------------------------------- */

function founderFigures(responses) {
  var out = {};
  Object.keys(FIGURE_SOURCES).forEach(function (basis) {
    var v = FIGURE_SOURCES[basis].value(responses);
    if (typeof v === 'number' && isFinite(v)) out[basis] = v;
  });
  return out;
}

/* ---------------------------------------------------------------------------
 * THE MULTIPLICATION. One function, used by every bar on the field.
 * ------------------------------------------------------------------------- */

function ffRound2(n) {
  return Math.round(n * 100) / 100;
}

/* `band` is a range or a chart entry from the payload: it carries low, mid and high, or it does
   not, in which case there is nothing to multiply and this says so by returning null.

   A LOCKED BAND HAS NO NUMBERS IN IT AT ALL and that is rule E8 working, not a failure. The free
   payload strips low, mid and high from every non-public lane before it leaves the engine, so the
   blur on the page is drawn over nothing. This function finds nothing to multiply and returns
   null, exactly as it does for a founder who typed no figure. */
function priceBand(band, figures) {
  if (!band || !figures) return null;
  var v = figures[band.basis];
  if (typeof v !== 'number' || !isFinite(v)) return null;
  if (typeof band.low !== 'number' || typeof band.high !== 'number') return null;
  var out = {
    metric: v,
    low: ffRound2(v * band.low),
    high: ffRound2(v * band.high)
  };
  if (typeof band.mid === 'number') out.mid = ffRound2(v * band.mid);
  return out;
}

/* Every chart in the payload, priced where the browser holds the figure for it. The payload's own
   `priced` flag says whether the ENGINE had a figure, which on the free path it never does, so the
   page recomputes the flag from what it holds itself. */
function priceCharts(charts, figures) {
  return (charts || []).map(function (c) {
    var p = priceBand(c, figures);
    var row = {};
    Object.keys(c).forEach(function (k) { row[k] = c[k]; });
    row.priced = !!p;
    row.founder_low = p ? p.low : null;
    row.founder_high = p ? p.high : null;
    row.founder_metric = p ? p.metric : null;
    row.unpriced_reason = p ? null : (BASIS_NOT_PRICED[c.basis] || null);
    return row;
  });
}

if (typeof window !== 'undefined') {
  window.FIGURE_SOURCES = FIGURE_SOURCES;
  window.COUNT_BASES = COUNT_BASES;
  window.unitOf = unitOf;
  window.BASIS_NOT_PRICED = BASIS_NOT_PRICED;
  window.founderFigures = founderFigures;
  window.priceBand = priceBand;
  window.priceCharts = priceCharts;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    FIGURE_SOURCES: FIGURE_SOURCES,
    COUNT_BASES: COUNT_BASES,
    unitOf: unitOf,
    BASIS_NOT_PRICED: BASIS_NOT_PRICED,
    founderFigures: founderFigures,
    priceBand: priceBand,
    priceCharts: priceCharts,
    figureArrMusd: figureArrMusd
  };
}
