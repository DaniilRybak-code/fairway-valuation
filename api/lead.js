/* Receives everything the funnel collects and writes it somewhere durable.
 *
 * Flow: browser POSTs JSON -> this function flattens it into a fixed column
 * order -> POSTs to LEAD_WEBHOOK_URL (a Google Apps Script web app bound to a
 * spreadsheet, see docs/lead-capture.md) -> one row per entry.
 *
 * The function sends `fields` alongside `values` so the sheet can write its own
 * header row on first use. Column order lives here and nowhere else.
 *
 * Env vars:
 *   LEAD_WEBHOOK_URL  the Apps Script /exec URL. Without it nothing persists.
 *   LEAD_SHARED_SECRET  optional, echoed to the script so it can reject noise.
 */

const FIELDS = [
  'timestamp_utc', 'lead_id', 'type',
  'email', 'company', 'phone',
  'stage', 'sector', 'sector_detail',
  'currency', 'revenue', 'revenue_exact_monthly', 'arr_exact', 'recurring_pct', 'revenue_model',
  'growth', 'growth_pct_monthly', 'growth_detail', 'gross_margin_pct', 'profitability', 'raise_band', 'timing',
  'last_round_amount', 'last_round_value', 'last_round_type', 'last_round_date',
  'concerns', 'concern_notes', 'context_link',
  'range_low_m', 'range_high_m', 'range_mid_m',
  'dilution_low_pct', 'dilution_high_pct', 'dilution_points', 'future_value_m',
  'hook_variant', 'utm_source', 'country', 'region', 'city',
  'user_agent', 'status', 'reviewer_notes', 'sent_at'
];

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'method_not_allowed' });
    return;
  }

  const body = typeof req.body === 'string' ? safeParse(req.body) : (req.body || {});
  const c = body.computed || {};

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

    currency: str(body.currency) || 'USD',
    revenue: str(body.revenue),
    revenue_exact_monthly: num(body.revenue_exact),
    arr_exact: num(body.revenue_exact != null ? body.revenue_exact * 12 : null),
    recurring_pct: num(body.recurring_pct),
    revenue_model: str(body.revenue_model),

    growth: str(body.growth),
    growth_pct_monthly: num(body.growth_exact),
    growth_detail: str(body.growth_detail),
    gross_margin_pct: num(body.gross_margin),
    profitability: str(body.profit),
    raise_band: str(body.raise),
    timing: str(body.timing),

    last_round_amount: num(body.last_round_amount),
    last_round_value: num(body.last_round_value),
    last_round_type: str(body.last_round_type),
    last_round_date: str(body.last_round_date),

    concerns: Array.isArray(body.concerns) ? body.concerns.join('; ') : str(body.concerns),
    concern_notes: str(body.concern_notes || body.notes),
    context_link: str(body.context_link || body.link),

    range_low_m: num(c.low),
    range_high_m: num(c.high),
    range_mid_m: num(c.mid),
    dilution_low_pct: num(c.dilLow),
    dilution_high_pct: num(c.dilHigh),
    dilution_points: num(c.dilLow != null && c.dilHigh != null ? c.dilLow - c.dilHigh : null),
    future_value_m: num(c.futureValue),

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
    sent_at: ''
  };

  const values = FIELDS.map(f => (record[f] === undefined || record[f] === null ? '' : record[f]));

  console.log('[fairway-lead]', JSON.stringify(record));

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
  res.status(200).json({ ok: true, forwarded, lead_id: record.lead_id });
}

function safeParse(s) { try { return JSON.parse(s); } catch (e) { return { raw: s }; } }
function str(v) { return v === undefined || v === null ? '' : String(v).slice(0, 2000); }
function num(v) { return typeof v === 'number' && isFinite(v) ? Math.round(v * 100) / 100 : ''; }
function header(req, k) { return (req.headers && req.headers[k]) ? String(req.headers[k]) : ''; }
function decodeSafe(v) { try { return decodeURIComponent(v); } catch (e) { return v; } }
function newId() {
  return 'fw_' + Math.random().toString(36).slice(2, 8) + Date.now().toString(36).slice(-5);
}
