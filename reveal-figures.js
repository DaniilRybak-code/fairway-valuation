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

var FIGURE_SOURCES = {
  ARR: {
    label: 'run-rate revenue',
    from: 'revenue_exact',
    note: 'your monthly revenue times twelve, in US dollar millions',
    value: figureArrMusd
  }
};

/* WHY EVERY OTHER BASIS IS UNPRICED TODAY, said in the code so that nobody has to guess whether it
   is a bug. Printed by check 15 so the list stays honest as the forks reach the page. */
var BASIS_NOT_PRICED = {
  REVENUE: 'the engine prices this on a trailing twelve-month figure and the live quiz asks for '
         + 'current monthly revenue only. A run rate is a forward figure, so using it here would '
         + 'overstate the founder against a trailing multiple. Needs a quiz question or a ruling.',
  REVENUE_GROSS: 'the quiz asks for one revenue figure. The net and gross split ruled on 5-Sep is '
         + 'in the engine and in quiz_fork.py, and it is not on the live page yet.',
  BOOK: 'the lending fork asks for book value and is not on the live page yet.',
  EARNINGS: 'this basis prices on net income. The page collects LTM EBITDA, which is a different '
         + 'line, so it is not substituted for it.',
  ORIGINATIONS: 'the lending fork asks for originations and is not on the live page yet.',
  THROUGHPUT: 'the exchange fork asks for volume and is not on the live page yet.',
  PAYING_SUBSCRIBERS: 'no count question on the live page yet.',
  BORROWERS: 'no count question on the live page yet.',
  MEMBERS: 'no count question on the live page yet.',
  CUSTOMERS: 'no count question on the live page yet.',
  BUSINESS_CUSTOMERS: 'no count question on the live page yet.',
  MERCHANTS: 'no count question on the live page yet.',
  ACTIVE_USERS: 'no count question on the live page yet.',
  REGISTERED_USERS: 'no count question on the live page yet.'
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
