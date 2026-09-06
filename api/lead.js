/* Receives what the funnel collects and writes it somewhere durable.
 *
 * Flow: browser POSTs JSON -> this function flattens it into a fixed column
 * order -> POSTs to LEAD_WEBHOOK_URL (a Google Apps Script web app bound to a
 * spreadsheet, see docs/lead-capture.md) -> one row per entry.
 *
 * The function sends `fields` alongside `values` so the sheet can write its own
 * header row on first use. Column order lives here and nowhere else.
 *
 * THE FIGURE COLUMNS ARE EMPTY UNLESS THE FOUNDER PRESSED THE BUTTON.
 *
 * Daniil, 6-Sep-2026: "we only take a record of the company data (profile, website), without
 * storing the numbers... if the user wants to have his numbers and ff reviewed, he presses a
 * button and it comes through to us, in which case he would specifically agree for us to see it."
 *
 * The page holds up its end: buildLeadRecord in reveal-request.js sends no figure. This function
 * holds up the other end. Every column in FIGURE_COLUMNS below is written as an empty string
 * unless the body carries `consent.figures === true`, so a future change to the page that starts
 * sending figures again still writes nothing to the sheet. A boundary enforced at one end only is
 * a boundary that lasts until the next hurried edit.
 *
 * IT NEVER DROPS SILENTLY. The log line names how many figure fields arrived and were refused, so
 * a page that starts leaking shows up in the logs on the first request rather than in the sheet a
 * month later.
 *
 * Env vars:
 *   LEAD_WEBHOOK_URL  the Apps Script /exec URL. Without it nothing persists.
 *   LEAD_SHARED_SECRET  optional, echoed to the script so it can reject noise.
 */

const FIELDS = [
  'timestamp_utc', 'lead_id', 'type',
  'email', 'company', 'phone',
  'stage', 'sector', 'sector_detail', 'website',
  'currency', 'revenue', 'revenue_exact_monthly', 'arr_exact', 'recurring_pct', 'revenue_model',
  'growth', 'growth_pct_yoy', 'growth_fwd_pct', 'growth_detail', 'gross_margin_pct', 'profitability', 'raise_band', 'timing',
  'ebitda_ltm', 'last_round_amount', 'last_round_value', 'last_round_type', 'last_round_date',
  'concerns', 'concern_notes', 'context_link',
  'ntm_revenue_m', 'exit_arr_m', 'run_rate_arr_m',
  'hook_variant', 'utm_source', 'country', 'region', 'city',
  'user_agent', 'status', 'reviewer_notes', 'sent_at',
  /* ADDED 6-Sep-2026, AT THE END, so an existing sheet keeps every column it already has in the
     position it already has it. `figures_consent` is the column a reviewer sorts on to find the
     rows they are allowed to read numbers in. */
  'figures_consent', 'consent_at', 'consent_wording'
];

/* THE COLUMNS THAT HOLD A FIGURE. Blank unless consent. Growth and margin are NOT on this list
   and that is deliberate: they are ratios, the engine needs them to choose the comparables, and
   the page says so in as many words rather than claiming we receive nothing. */
const FIGURE_COLUMNS = [
  'revenue', 'revenue_exact_monthly', 'arr_exact', 'recurring_pct',
  'profitability', 'raise_band', 'timing',
  'ebitda_ltm', 'last_round_amount', 'last_round_value', 'last_round_type', 'last_round_date',
  'growth_detail', 'concern_notes', 'context_link',
  'ntm_revenue_m', 'exit_arr_m', 'run_rate_arr_m'
];

/* Consent is a positive act and nothing else counts as one. A missing block, a string "true", a
   truthy object: none of them open the figure columns. */
function hasFigureConsent(body) {
  const c = body && body.consent;
  return !!(c && c.figures === true);
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'method_not_allowed' });
    return;
  }

  const body = typeof req.body === 'string' ? safeParse(req.body) : (req.body || {});
  const c = body.computed || {};
  const consented = hasFigureConsent(body);

  const record = {
    timestamp_utc: new Date().toISOString(),
    lead_id: body.lead_id || newId(),
    type: body.type || 'lead',

    email: str(body.email),
    company: str(body.company),
    phone: str(body.phone),

    stage: str(body.stage),
    sector: str(body.sector),
    sector_detail: str(body.sector_detail),
    website: str(body.website),

    currency: str(body.currency) || 'USD',
    revenue: str(body.revenue),
    revenue_exact_monthly: num(body.revenue_exact),
    arr_exact: num(body.revenue_exact != null ? body.revenue_exact * 12 : null),
    recurring_pct: num(body.recurring_pct),
    revenue_model: str(body.revenue_model),

    growth: str(body.growth),
    growth_pct_yoy: num(body.growth_yoy != null ? body.growth_yoy : body.growth_exact),
    growth_fwd_pct: num(c.forwardGrowth),
    growth_detail: str(body.growth_detail),
    gross_margin_pct: num(body.gross_margin),
    profitability: str(body.profit),
    raise_band: str(body.raise),
    timing: str(body.timing),

    ebitda_ltm: num(body.ebitda_ltm),
    last_round_amount: num(body.last_round_amount),
    last_round_value: num(body.last_round_value),
    last_round_type: str(body.last_round_type),
    last_round_date: str(body.last_round_date),

    concerns: Array.isArray(body.concerns) ? body.concerns.join('; ') : str(body.concerns),
    concern_notes: str(body.concern_notes || body.notes),
    context_link: str(body.context_link || body.link),

    /* The indicative range was removed from the product, so there is no range to
       log. What the reviewer needs is the metrics the field prices. */
    ntm_revenue_m: num(c.ntmM),
    exit_arr_m: num(c.exitArrM),
    run_rate_arr_m: num(c.runRateM),

    hook_variant: str(body.variant),
    utm_source: str(body.utm_source),

    /* Vercel resolves these from the request IP at the edge. Coarse only:
       country, region, city. Never an IP address, never stored client side. */
    country: header(req, 'x-vercel-ip-country'),
    region: header(req, 'x-vercel-ip-country-region'),
    city: decodeSafe(header(req, 'x-vercel-ip-city')),

    user_agent: header(req, 'user-agent').slice(0, 180),

    /* Reviewer workflow columns, filled in by a human in the sheet. */
    status: body.type === 'partial' ? 'abandoned' : (body.type === 'enrichment' ? 'enriched' : 'new'),
    reviewer_notes: '',
    sent_at: '',

    figures_consent: consented ? 'yes' : '',
    consent_at: consented ? str((body.consent || {}).at) : '',
    consent_wording: consented ? str((body.consent || {}).wording) : ''
  };

  /* THE GATE. Count what arrived, name it in the log, and blank it. */
  let refused = [];
  if (!consented) {
    refused = FIGURE_COLUMNS.filter(f => record[f] !== '' && record[f] !== undefined && record[f] !== null);
    FIGURE_COLUMNS.forEach(f => { record[f] = ''; });
  }

  const values = FIELDS.map(f => (record[f] === undefined || record[f] === null ? '' : record[f]));

  /* The log carries the record AFTER the gate, so a figure the founder has not consented to is
     not written to a log line either. */
  console.log('[fairway-lead]', JSON.stringify(record));
  if (refused.length) {
    console.warn('[fairway-lead] refused %d figure field(s) with no consent block: %s',
                 refused.length, refused.join(', '));
  }

  let forwarded = false;
  const hook = process.env.LEAD_WEBHOOK_URL;
  if (hook) {
    try {
      const r = await fetch(hook, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          secret: process.env.LEAD_SHARED_SECRET || '',
          fields: FIELDS,
          values: values,
          record: record
        })
      });
      forwarded = r.ok;
      if (!r.ok) console.error('[fairway-lead] webhook returned', r.status);
    } catch (err) {
      console.error('[fairway-lead] forward failed:', err && err.message);
    }
  } else {
    console.warn('[fairway-lead] LEAD_WEBHOOK_URL is not set, this lead exists only in the logs');
  }

  /* Always 200. A storage failure must never cost the founder their result. */
  res.status(200).json({ ok: true, forwarded, lead_id: record.lead_id,
                        figures_stored: consented, figures_refused: refused.length });
}

function safeParse(s) { try { return JSON.parse(s); } catch (e) { return { raw: s }; } }
function str(v) { return v === undefined || v === null ? '' : String(v).slice(0, 2000); }
function num(v) { return typeof v === 'number' && isFinite(v) ? Math.round(v * 100) / 100 : ''; }
function header(req, k) { return (req.headers && req.headers[k]) ? String(req.headers[k]) : ''; }
function decodeSafe(v) { try { return decodeURIComponent(v); } catch (e) { return v; } }
function newId() {
  return 'fw_' + Math.random().toString(36).slice(2, 8) + Date.now().toString(36).slice(-5);
}
