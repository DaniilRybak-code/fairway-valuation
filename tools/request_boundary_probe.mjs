/* The half of check 15 that has to RUN the code rather than read it.
 *
 * Called by tools/check_request_boundary.py, which owns the assertions. This file only produces
 * evidence and prints it as one JSON object on stdout. It asserts nothing itself, so that there is
 * one place to read to find out what check 15 believes.
 *
 * Four probes:
 *   requests   the three request builders, run against a responses object holding every field the
 *              live quiz collects, with distinctive sentinel values in every figure.
 *   lead       api/lead.js handled twice, without a consent block and with one, so the server-side
 *              gate is tested rather than described.
 *   model      api/reveal.js handled with a figure-laden body and the outbound call intercepted, so
 *              that what actually reaches the model is inspected rather than assumed.
 *   arithmetic reveal-figures.js priceBand run over real payload rows handed in by the Python side.
 */
import { createRequire } from 'module';
import { readFileSync } from 'fs';

const require = createRequire(import.meta.url);
const ROOT = new URL('..', import.meta.url).pathname.replace(/\/$/, '');

const RQ = require(ROOT + '/reveal-request.js');
const FG = require(ROOT + '/reveal-figures.js');
const IV = require(ROOT + '/investors.js');

/* SENTINELS. Every figure in this object is a value that appears nowhere else in the repo, so if
   one of them turns up in a request body or a model prompt there is no argument about where it
   came from. */
const SENTINEL = {
  revenue: 'BAND_SENTINEL_9111',
  revenue_exact: 913371,
  arr_exact: 10960452,
  /* A PERCENTAGE STILL HAS TO BE DISTINCTIVE. This was 91, and 91 is two digits: it appears in
     timestamps, durations and byte counts, and the Python side looks for a sentinel by plain
     substring. On 7-Sep-2026 check 15 passed on its own and failed inside the suite, reporting that
     api/lead.js had logged recurring_pct, because that run's log happened to contain "91". A check
     that is sometimes red is worse than one that is always red: it teaches whoever runs it to re-run
     rather than to look. Six significant figures, still a valid percentage. */
  recurring_pct: 90.9137,
  ebitda_ltm: -917731,
  last_round_amount: 9155000,
  last_round_value: 9188000,
  last_round_type: 'SAFE or note cap',
  last_round_date: '2025-04',
  profit: 'PROFIT_SENTINEL_9122',
  raise: 'RAISE_SENTINEL_9133',
  timing: 'TIMING_SENTINEL_9144',
  growth_detail: 'DETAIL_SENTINEL_9155 we went from 40k to 90k',
  concern_notes: 'NOTES_SENTINEL_9166 we did 1.2m last year',
  context_link: 'https://LINK_SENTINEL_9177.example/deck'
};

const RESPONSES = Object.assign({
  stage: 'Seed', sector: 'B2B software', sectors: ['B2B software', 'Fintech'],
  sector_detail: 'carbon accounting for shipping', website: 'example.com',
  company: 'Acme Ltd', country: 'GB', revenue_model: 'Subscription',
  funding_model: 'Balance sheet', volume_unit: 'tonnes', revenue_basis: 'net',
  growth: '50% to 100%', growth_yoy: 74, growth_plan: 60, gross_margin: 78,
  growth_exact: 74, currency: 'USD', email: 'founder@example.com', phone: '+44 7000 000000',
  concerns: ['Investors say we are too early'], variant: 'frustration', utm_source: 'x'
}, SENTINEL);

const out = { sentinels: SENTINEL };

/* THE CHEQUE FILTER, BOTH SIDES. Added 7-Sep-2026 with the browser-side investor filter. The rule
   that drops a fund whose first cheque cannot fund the round now exists twice: in
   selector/investors._cheque_fits, and in investors.invChequeFits, because the raise stays in the
   browser and the filter has to run where the raise is. Two copies of one rule is exactly the
   shape that drifts, so the Python side sends real cards and real raises through here and compares
   the answers one by one. The cases come from the spec file, not from this file. */
out.chequeCases = null;

/* ---- 1. the three request builders ---- */
const reveal = RQ.buildRevealRequest(RESPONSES);
const lead = RQ.buildLeadRecord(RESPONSES);
const review = RQ.buildReviewRequest(RESPONSES, {
  revenue_exact: SENTINEL.revenue_exact, raise: SENTINEL.raise
}, 'fw_test123', 'the wording the founder clicked');

out.requests = {
  allowlist: RQ.REVEAL_FIELDS,
  figure_fields: RQ.FIGURE_FIELDS,
  reveal_keys: Object.keys(reveal),
  reveal_json: JSON.stringify(reveal),
  lead_keys: Object.keys(lead),
  lead_json: JSON.stringify(lead),
  review_keys: Object.keys(review),
  review_json: JSON.stringify(review)
};

/* ---- 2. api/lead.js, the server-side gate ---- */
function fakeRes() {
  const r = { code: null, body: null };
  r.status = function (c) { r.code = c; return r; };
  r.json = function (b) { r.body = b; return r; };
  return r;
}

async function runLead(body) {
  const mod = await import(ROOT + '/api/lead.js');
  const req = { method: 'POST', body: body, headers: { 'user-agent': 'probe' } };
  const res = fakeRes();
  const logs = [];
  const realLog = console.log, realWarn = console.warn;
  console.log = function () { logs.push(Array.from(arguments).join(' ')); };
  console.warn = function () { logs.push(Array.from(arguments).join(' ')); };
  try { await mod.default(req, res); } finally { console.log = realLog; console.warn = realWarn; }
  return { response: res.body, log: logs.join('\n') };
}

/* The page's own lead body, and then the same body with every figure forced back in, which is the
   case that matters: it is what a future edit to the page would send. */
const leakedLead = Object.assign({}, lead, {
  revenue: SENTINEL.revenue, revenue_exact: SENTINEL.revenue_exact,
  ebitda_ltm: SENTINEL.ebitda_ltm, last_round_value: SENTINEL.last_round_value,
  profit: SENTINEL.profit, raise: SENTINEL.raise, timing: SENTINEL.timing,
  growth_detail: SENTINEL.growth_detail, concern_notes: SENTINEL.concern_notes,
  context_link: SENTINEL.context_link,
  computed: { ntmM: 9.1234, exitArrM: 9.5678, runRateM: 9.9012 }
});

out.lead = {
  clean: await runLead(lead),
  leaked: await runLead(leakedLead),
  consented: await runLead(review)
};

/* ---- 3. api/reveal.js, and what actually reaches the model ---- */
process.env.ANTHROPIC_API_KEY = 'probe-key-not-a-real-one';
const captured = [];
const realFetch = globalThis.fetch;
globalThis.fetch = async function (url, opts) {
  captured.push({ url: String(url), body: (opts && opts.body) || '' });
  throw new Error('probe: outbound call intercepted, nothing was sent');
};
let revealBody = null;
try {
  const mod = await import(ROOT + '/api/reveal.js');
  const req = {
    method: 'POST',
    /* Everything, including every figure, as if the page had been changed to send it all again. */
    body: Object.assign({}, RESPONSES),
    headers: { 'x-forwarded-for': '127.0.0.1', 'x-vercel-ip-country': 'GB' }
  };
  const res = fakeRes();
  const realErr = console.error;
  console.error = function () {};
  try { await mod.default(req, res); } finally { console.error = realErr; }
  revealBody = res.body;
} finally {
  globalThis.fetch = realFetch;
  delete process.env.ANTHROPIC_API_KEY;
}
out.model = {
  outbound: captured.map(c => ({ url: c.url, body: c.body })),
  response_keys: revealBody ? Object.keys(revealBody) : [],
  payload_is_null: !!(revealBody && revealBody.payload === null)
};

/* ---- 4. the arithmetic, over real payload rows ---- */
/* The Python side writes {rows: [{basis, low, mid, high}], probes: [numbers]} to this file. The
   probe values are inputs to a multiplication, not data about any company: they test that two
   implementations of one sum agree, which is the same thing check_period_conversion.py does with
   known inputs and known answers. */
const arg = process.argv[2];
if (arg) {
  const spec = JSON.parse(readFileSync(arg, 'utf8'));
  out.arithmetic = spec.rows.map(function (row) {
    return spec.probes.map(function (v) {
      const priced = FG.priceBand(row, { [row.basis]: v });
      return { basis: row.basis, metric: v,
               low: priced ? priced.low : null, high: priced ? priced.high : null };
    });
  }).flat();

  /* The cheque cases, answered by the PAGE's copy of the rule. */
  if (spec.cheque_cases) {
    out.chequeCases = spec.cheque_cases.map(function (c) {
      return IV.invChequeFits({ cheque_low_m: c.lo, cheque_high_m: c.hi },
                              c.raise,
                              { low_multiple: c.low_multiple, high_multiple: c.high_multiple });
    });
  }
}

/* ---- 5. what the page can price at all ---- */
out.figures = {
  sources: Object.keys(FG.FIGURE_SOURCES),
  not_priced: Object.keys(FG.BASIS_NOT_PRICED),
  arr_from_50k_usd: FG.figureArrMusd({ revenue_exact: 50000, currency: 'USD' }),
  arr_from_nothing: FG.figureArrMusd({})
};

process.stdout.write(JSON.stringify(out));
