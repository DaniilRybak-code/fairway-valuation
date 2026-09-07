/* THE BOUNDARY. What leaves the browser, and what does not.
 *
 * Daniil, 6-Sep-2026: "Is there a way to do all the same for the founder WITHOUT storing his
 * financials? So we say transparently, we only take a record of the company data (profile,
 * website), without storing the numbers. Then he gets the reveal based on the numbers he put in
 * (we still do not see any financials at that point). Then if the user wants to have his numbers
 * and ff reviewed, he presses a button and it comes through to us, in which case he would
 * specifically agree for us to see it."
 *
 * THIS FILE IS THE ONLY PLACE A REQUEST BODY IS BUILT. Nothing else in the page may hand an object
 * to fetch(). That is the whole design: a boundary spread across three call sites is a boundary
 * that moves the first time somebody adds a field in a hurry, which is what happened to the
 * honesty strings and to the gross rounds.
 *
 * WHY THE ENGINE DOES NOT NEED THE FIGURES, measured on 6-Sep-2026 rather than assumed:
 *
 *   SELECTION needs two ratios and a handful of labels. The growth rate decides which private
 *   rounds a founder is compared against (band_compatible) and how the peers are ranked (g_rank).
 *   The gross margin decides whether the reveal leads on revenue or on gross profit (denominator).
 *   Both are percentages. Neither says anything about the size of the business.
 *
 *   PRICING needs the figures, and pricing is one multiplication. Revenue, ARR, book value, net
 *   income, originations and every user count are used for exactly one thing: to multiply a peer
 *   multiple. That multiplication happens in reveal-figures.js, in this browser, on a value that
 *   never enters one of these request bodies.
 *
 *   The proof that this works is the gate. All 102 test fixtures carry no revenue, no growth rate
 *   and no margin, and 95 of them pass the peer-universe gate. The engine has been running on the
 *   private architecture since before anyone asked for it.
 *
 * TWO THINGS STILL CROSS AND THE PAGE MUST NOT PRETEND OTHERWISE. The growth rate and the gross
 * margin are needed for selection and they do reach us. They are ratios, not amounts. The copy in
 * index.html says exactly that and must keep saying exactly that.
 */

/* ---------------------------------------------------------------------------
 * THE ALLOWLIST. Three groups, and every entry is either a LABEL or a PERCENTAGE.
 * Adding anything here is changing the promise on the page, and check 15 fails until the same
 * field is added to tools/check_request_boundary.py with a reason written beside it.
 * ------------------------------------------------------------------------- */

/* Company data. Daniil's own words: "we only take a record of the company data (profile,
   website)". These are what the profiler reads to produce the tags the selector matches on. */
var REVEAL_PROFILE_FIELDS = [
  'stage',            /* Pre-seed, Seed, Series A. The founder's own answer, step 1. */
  'sector',           /* the leading sector chip */
  'sectors',          /* up to three, in the order picked */
  'sector_detail',    /* "in your own words", when the sector is Other */
  'website',          /* the heaviest input the matcher has, see docs/engine-architecture.md */
  'company',          /* the company name, which is company data and not a figure */
  'country',          /* resolved from the edge header at boot, never asked */
  'revenue_model'     /* HOW they charge (subscription, transaction fee), never HOW MUCH */
];

/* Labels the forks already read. The lending fork asks how the book is funded, the exchange fork
   asks what unit the volume is in, and the revenue fork asks which measure the figure is on. Each
   one is a word, not an amount: "marketplace", "tonnes", "gross". None of them says anything about
   the size of the business.

   NOT ALL OF THESE ARE ON THE LIVE PAGE YET. The forks live in selector/quiz_fork.py and the live
   quiz is still the nine-step one, so today these arrive undefined and are skipped. They are named
   here rather than added later so that the boundary does not have to be reopened on the day the
   forks reach the page. */
var REVEAL_FORK_LABELS = [
  'funding_model',    /* balance sheet, marketplace, forward-flow */
  'volume_unit',      /* tonnes, transactions, USD */
  'revenue_basis'     /* net, gross, both. WHICH measure, never how much of it */
];

/* The two ratios, and the growth rate in the three shapes the quiz collects it in. */
var REVEAL_RATIOS = [
  'growth',           /* the band label, e.g. "Under 50%" */
  'growth_yoy',       /* the trailing rate the founder typed, a percentage */
  'growth_plan',      /* the rate they plan, a percentage */
  'gross_margin'      /* a percentage */
];

var REVEAL_FIELDS = REVEAL_PROFILE_FIELDS.concat(REVEAL_FORK_LABELS).concat(REVEAL_RATIOS);

/* ---------------------------------------------------------------------------
 * THE RAISE: DANIIL'S OPEN RULING, WRITTEN DOWN SO THE ANSWER IS SMALL AND THE QUESTION IS CLEAR.
 *
 * The question from the status document: the amount the founder is raising left the browser until
 * rule E9 on 6 September, and it did one job. `_cheque_fits` in selector/investors.py drops an
 * investor whose published first cheque cannot fund the round, so a fund writing $10m cheques stays
 * off a pre-seed founder's call list. Without the raise that filter never excludes anyone, and
 * those houses appear with their published cheque range printed on the card for the founder to
 * judge for themselves.
 *
 * NO FLAG IS PROVIDED HERE ON PURPOSE. Putting the raise back is changing the sentence on the page
 * that says no figure leaves the browser, and a promise should not be reversible by a boolean
 * somebody can flip without reading it. The change, if Daniil says yes, is three named edits:
 *
 *   1. add 'raise' to REVEAL_PROFILE_FIELDS above, with a comment saying it is the ONE amount that
 *      leaves, and that it is the ask rather than a figure from the accounts
 *   2. add 'raise' to ALLOWED in tools/check_request_boundary.py with the same reason, and remove
 *      it from FIGURE_NAMES, or the check fails by design
 *   3. add 'raise' to ALLOWED in api/payload.py and pass it to RP.build as raise_musd
 *
 * Plus the consent copy on the page, which currently names the founder's answers one by one.
 *
 * WHAT IT BUYS, MEASURED 7-SEP-2026 ACROSS ALL 102 FIXTURES, with the stated stage doing the work
 * it now does:
 *
 *     raise $0.5m   812 call-list cards without it, 13 fewer with it   (1.6%)
 *     raise $1m     812 cards, 0 fewer
 *     raise $3m     812 cards, 0 fewer
 *     raise $10m    812 cards, 0 fewer
 *
 * So at every raise except the smallest it currently changes NOTHING, and at $500k it removes 13
 * cards out of 812. The earlier figure of "3 of 156 houses" was counted before stage bands were
 * filled in on 6 September; the stage gate now does almost all of this filter's work, and the
 * cheque range is printed on the card either way.
 *
 * On those numbers the honest recommendation is NO: it is the largest promise on the page bought
 * back for 1.6 per cent of one founder's list. The ruling is still Daniil's.
 * ------------------------------------------------------------------------- */

/* ---------------------------------------------------------------------------
 * WHAT NEVER LEAVES WITHOUT A CLICK. Named here so that the check has something to assert
 * against and so that a reader can see the promise as a list rather than as prose.
 * ------------------------------------------------------------------------- */
var FIGURE_FIELDS = [
  'revenue',            /* the band, which is an amount written as a range */
  'revenue_exact',      /* monthly revenue */
  'arr_exact',
  'recurring_pct',      /* a ratio, but it is a ratio OF the revenue and nothing reads it */
  'ebitda_ltm',
  'last_round_amount',
  'last_round_value',
  'profit',             /* profitable or burning, which is a fact about their own money */
  'raise',              /* the size of the round. See the note below. */
  'timing',
  'growth_detail',      /* free text about growth, and founders write figures into free text */
  'concern_notes',      /* the same, and it is where a deck link and a number usually land */
  'context_link',       /* a link to a deck is a link to every figure in it */
  'ntmM', 'exitArrM', 'runRateM', 'markerM', 'ebitdaM'   /* computeResult's own arithmetic */
];

/* WHY THE RAISE IS ON THE LIST, AND WHAT IT COST TO PUT IT THERE.
 *
 * The raise band is an amount, so under the strict reading of Daniil's instruction it does not go
 * on the free path. Removing it looked expensive: investors._stage_for derived the founder's stage
 * from the raise, and with no raise the call list collapsed from 813 cards across the 102 fixtures
 * to 44, with 92 fixtures getting no houses at all.
 *
 * That turned out to be a bug rather than a price. The founder tells us their stage in step 1 of
 * the quiz and the engine was deriving it from an amount instead of reading the answer. With
 * _stage_for reading the stated stage, the same 102 fixtures give 813 cards at Seed, 724 at
 * Pre-seed and 797 at Series A, and no fixture is left without a house.
 *
 * WHAT IS ACTUALLY LOST is investors._cheque_fits, which drops a house whose published first
 * cheque cannot fund the round. At a $3m raise it excluded 3 of 156 callable houses. Those 3 are
 * now shown, with their published cheque range printed on the card, which is the thing the founder
 * can check for themselves.
 */

/* ---------------------------------------------------------------------------
 * THE BUILDERS. All three are loops over a named list. None of them contains a field name of its
 * own, which is what makes the allowlist above the only way in.
 * ------------------------------------------------------------------------- */

function pickFields(source, fields) {
  var out = {};
  var src = source || {};
  fields.forEach(function (f) {
    var v = src[f];
    if (v === undefined || v === null || v === '') return;
    out[f] = v;
  });
  return out;
}

/* THE DEFAULT REQUEST. Everything the engine needs to choose the comparables, and nothing that
   says how big the business is. This is the body check 15 asserts against. */
function buildRevealRequest(responses) {
  return pickFields(responses, REVEAL_FIELDS);
}

/* THE LEAD. The same allowlist plus the contact details, because the whole point of the lead is a
   person emailing the founder back within 24 hours.

   The contact fields are a separate list and a separate argument on purpose. They are personal
   data, they are not company data, and they are the one thing on this page that a founder types
   knowing exactly where it is going. */
var LEAD_CONTACT_FIELDS = ['email', 'phone'];
var LEAD_CONTEXT_FIELDS = ['concerns', 'variant', 'utm_source', 'currency'];

function buildLeadRecord(responses) {
  var body = pickFields(responses, REVEAL_FIELDS);
  var contact = pickFields(responses, LEAD_CONTACT_FIELDS);
  var context = pickFields(responses, LEAD_CONTEXT_FIELDS);
  Object.keys(contact).forEach(function (k) { body[k] = contact[k]; });
  Object.keys(context).forEach(function (k) { body[k] = context[k]; });
  body.type = 'lead';
  /* SAID OUT LOUD IN THE BODY ITSELF. api/lead.js blanks every figure column unless it sees a
     consent block, so a future page change that starts sending figures on this path still writes
     nothing to the sheet. The boundary is enforced at both ends or it is enforced at neither. */
  body.consent = { figures: false };
  return body;
}

/* THE CONSENT REQUEST. The only body in this file that carries a figure, and the only one that is
   built from an explicit act by the founder.

   `figures` is the object reveal-figures.js has been holding in memory. `leadId` ties this row to
   the lead row already in the sheet. `agreedText` is the exact wording the founder clicked, stored
   beside their figures so that what they agreed to is a matter of record rather than of memory. */
function buildReviewRequest(responses, figures, leadId, agreedText) {
  var body = buildLeadRecord(responses);
  body.type = 'figures';
  body.lead_id = leadId || null;
  Object.keys(figures || {}).forEach(function (k) { body[k] = figures[k]; });
  body.consent = {
    figures: true,
    at: new Date().toISOString(),
    wording: agreedText || ''
  };
  return body;
}

if (typeof window !== 'undefined') {
  window.REVEAL_FIELDS = REVEAL_FIELDS;
  window.FIGURE_FIELDS = FIGURE_FIELDS;
  window.buildRevealRequest = buildRevealRequest;
  window.buildLeadRecord = buildLeadRecord;
  window.buildReviewRequest = buildReviewRequest;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    REVEAL_PROFILE_FIELDS: REVEAL_PROFILE_FIELDS,
    REVEAL_FORK_LABELS: REVEAL_FORK_LABELS,
    REVEAL_RATIOS: REVEAL_RATIOS,
    REVEAL_FIELDS: REVEAL_FIELDS,
    FIGURE_FIELDS: FIGURE_FIELDS,
    buildRevealRequest: buildRevealRequest,
    buildLeadRecord: buildLeadRecord,
    buildReviewRequest: buildReviewRequest
  };
}
