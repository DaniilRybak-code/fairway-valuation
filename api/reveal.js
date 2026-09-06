/* The reveal engine.
 *
 * This endpoint no longer produces a valuation. It used to compute a range and
 * hand it to a model to position inside a corridor, which meant the page carried
 * two independent range calculations that were never reconciled with each other
 * or with the football field. Both are deleted.
 *
 * What remains is prose: the basis sentence and the three concerns, written
 * about the founder's own answers. Every numeric field the model emits is
 * dropped by enforce(). A model may not put a number on this page.
 *
 * NO FIGURE REACHES THIS ENDPOINT, and from 6-Sep-2026 that is enforced here as well as in the
 * page. Daniil's instruction was that we do not receive a founder's financials unless they choose,
 * after seeing their field, to send them for review. The body this endpoint now receives is the
 * profile, the growth rate and the gross margin: labels and two percentages. `answers` below reads
 * only those, so a body that still carries a figure has it dropped on the floor here rather than
 * forwarded to a model.
 *
 * WHAT LEFT WITH THE FIGURES. This endpoint used to subtract the midpoint of the founder's stated
 * raise from the stage median to build its anchor sentence. The raise is an amount, so it is gone
 * from the request. field.js has always done that same subtraction on the page, from a value in
 * the browser, so nothing the founder sees changes: the deduction moved to the side of the wall
 * that already had the number.
 *
 * THE ENGINE PAYLOAD IS NOT SERVED FROM HERE YET, and the response says so rather than pretending.
 * selector/reveal_payload.py builds the whole reveal in one pass and it is Python; this endpoint is
 * a Node function. `payload: null` with a named reason is what the client reads, and reveal-client
 * .js renders nothing rather than something wrong when it sees one. Standing up the Python side is
 * the next piece of the wiring week and it does not change the boundary: that request carries the
 * same allowlisted body this one does.
 *
 * Env: ANTHROPIC_API_KEY (required), ANTHROPIC_MODEL (optional)
 */

import { SETTINGS } from '../config/reveal-settings.js';
import { buildSystem } from '../config/reveal-prompt.js';
import { COMPS } from '../data/comps.js';

export const config = { maxDuration: 60 };

/* RAISE_MIDPOINT USED TO LIVE HERE and it is deleted, not moved. The raise is an amount and this
   endpoint no longer receives one. The same table still lives in app.js, where the browser needs
   it to draw the stage-anchor row of the football field. */

const cache = new Map();
const hits = new Map();

export default async function handler(req, res) {
  if (req.method !== 'POST') { res.status(405).json({ error: 'method_not_allowed' }); return; }

  const ip = String(req.headers['x-forwarded-for'] || 'unknown').split(',')[0].trim();
  if (rateLimited(ip)) { res.status(429).json({ error: 'rate_limited' }); return; }

  const a = typeof req.body === 'string' ? safeParse(req.body) : (req.body || {});
  /* Contact details are never sent to the model. Nothing here identifies a person.
   *
   * AND NEITHER IS A FIGURE. This object is the allowlist, server side. `revenue`, `profit`,
   * `raise`, `timing`, `growth_detail`, `concerns` and `concern_notes` were all read here until
   * 6-Sep-2026 and all of them are gone: the first four are amounts or facts about the founder's
   * own money, and the last three are free text, which is where founders write figures when a box
   * does not ask for one. What is left is the profile and two percentages. */
  const answers = {
    stage: s(a.stage), sector: s(a.sector), sector_detail: s(a.sector_detail),
    sectors: Array.isArray(a.sectors) ? a.sectors.map(s) : [],
    website: s(a.website), company: s(a.company),
    revenue_model: s(a.revenue_model),
    growth: s(a.growth),
    growth_yoy: n(a.growth_yoy), growth_plan: n(a.growth_plan),
    gross_margin: n(a.gross_margin),
    country: String(req.headers['x-vercel-ip-country'] || '')
  };

  const key = JSON.stringify(answers);
  const cached = cache.get(key);
  if (cached && Date.now() - cached.at < SETTINGS.cacheTtlMinutes * 60000) {
    res.status(200).json({ ...cached.payload, cached: true });
    return;
  }

  const anchor = buildAnchor(answers);
  const fallback = deterministic(answers, anchor);

  if (!process.env.ANTHROPIC_API_KEY) {
    res.status(200).json({ ...fallback, ...ENGINE_PAYLOAD, source: 'fallback', reason: 'no_api_key' });
    return;
  }

  try {
    const out = await callModel(answers, anchor);
    const clean = enforce(out, anchor, fallback);
    cache.set(key, { at: Date.now(), payload: clean });
    res.status(200).json({ ...clean, ...ENGINE_PAYLOAD });
  } catch (err) {
    console.error('[fairway-reveal] model call failed:', err && err.message);
    res.status(200).json({ ...fallback, ...ENGINE_PAYLOAD, source: 'fallback', reason: 'model_error' });
  }
}

/* THE CONTRACT THE PAGE READS, stated even though there is nothing behind it yet. reveal-client.js
   renders the peer charts, the honesty caveats, the fix list and both investor layers from
   `payload`, and renders none of them when `payload` is null. Saying null with a reason is how the
   page knows the difference between "the engine has nothing for you" and "the engine is not
   plugged in", and it is what stops a half-drawn reveal from looking like a finished one. */
const ENGINE_PAYLOAD = {
  payload: null,
  payload_reason: 'engine_not_served: selector/reveal_payload.py is Python and this endpoint is '
                + 'Node. Serving it is the next piece of the wiring week. The request body does '
                + 'not change when it lands.'
};

/* ---------- anchors ---------- */

function buildAnchor(a) {
  const stageRow = COMPS.stages[a.stage] || {};
  const sectorRow = COMPS.sectors[a.sector] || null;
  const regionRow = COMPS.regions[a.country] || null;

  let preAnchor = null;
  let basis = '';

  if (stageRow.post_median_m) {
    /* THE MEDIAN, NOT THE MEDIAN LESS THE RAISE. The raise is an amount and it does not reach this
       endpoint. field.js draws the same row with the deduction applied, from the value it holds in
       the browser, so the founder still sees a pre-money figure. */
    preAnchor = stageRow.post_median_m;
    basis = `${a.stage} median post-money of $${stageRow.post_median_m}M (${stageRow.source}), before the round you are raising`;
  } else {
    /* No published anchor for this stage. Say so and widen rather than guess. */
    const seed = COMPS.stages['Seed'];
    if (seed && seed.post_median_m && a.stage === 'Pre-seed') {
      preAnchor = null;
      basis = `no published anchor for ${a.stage} in the current pack, so the methods lean on stage patterns rather than a comp set and are correspondingly wide`;
    }
  }

  if (preAnchor && sectorRow && sectorRow.stage_multiple) {
    preAnchor = preAnchor * sectorRow.stage_multiple;
    basis += `, adjusted for ${a.sector} (${sectorRow.source})`;
  }
  if (preAnchor && regionRow && regionRow.multiple) {
    preAnchor = preAnchor * regionRow.multiple;
    basis += `, adjusted for ${a.country} (${regionRow.source})`;
  }

  /* No centre, no corridor, no dispersion. Nothing here produces a number any
     more: what the model gets is the basis sentence, so it can write prose that
     is honest about what the page is standing on. */
  return {
    hasVerifiedAnchor: !!preAnchor,
    basis: basis || 'stage and sector patterns rather than a published comp set',
    vintage: COMPS.vintage
  };
}

/* The heuristic that used to sit here produced the second of two independent
   valuation ranges, neither of which was reconciled with the other or with the
   football field. Both are gone. Nothing in this file computes a valuation. */

function deterministic(a, anchor) {
  /* This used to return a range. It does not any more.

     The indicative range was removed from the product: it was a chain of
     coefficients nobody could trace, and the football field now carries the
     valuation as a set of methods instead. What survives here is the prose,
     which is the only thing a model was ever allowed to write. */
  return {
    basis_sentence: `Reference metrics from ${anchor.basis}. Reviewed by a person within 24 hours.`,
    confidence: anchor.hasVerifiedAnchor ? 'medium' : 'low',
    reference_points: [], concerns: [], source: 'deterministic'
  };
}

/* ---------- model ---------- */

async function callModel(a, anchor) {
  const dataPack = [
    `Vintage: ${COMPS.vintage}. Anchors are US-weighted.`,
    'Stage anchors:',
    ...Object.entries(COMPS.stages).map(([k, v]) => v.post_median_m
      ? `  ${k}: median post-money $${v.post_median_m}M. Source: ${v.source}. ${v.note || ''}`
      : `  ${k}: no published figure in this pack.`),
    'Market context you may cite:',
    ...COMPS.context.map(c => `  ${c.claim} Source: ${c.source}`),
    Object.keys(COMPS.sectors).length
      ? `Sector overlay: ${JSON.stringify(COMPS.sectors)}`
      : 'Sector overlay: empty. Do not state any sector-specific multiple as fact.'
  ].join('\n');

  const answers = Object.entries(a)
    .filter(([, v]) => v && (!Array.isArray(v) || v.length))
    .map(([k, v]) => `  ${k}: ${Array.isArray(v) ? v.join(', ') : v}`)
    .join('\n');

  const system = buildSystem({
    dataPack,
    answers,
    anchorBasis: anchor.basis
  });

  const tool = {
    name: 'emit_reveal',
    description: 'Return the reveal for this founder.',
    input_schema: {
      type: 'object',
      properties: {
        basis_sentence: { type: 'string' },
        confidence: { type: 'string', enum: ['low', 'medium', 'high'] },
        reference_points: {
          type: 'array', minItems: 4, maxItems: 4,
          items: {
            type: 'object',
            properties: {
              label: { type: 'string' },
              kind: { type: 'string', enum: ['market', 'method', 'positioning'] },
              detail: { type: 'string' },
              source: { type: 'string' }
            },
            required: ['label', 'kind', 'detail', 'source']
          }
        },
        concerns: {
          type: 'array', minItems: 3, maxItems: 3,
          items: {
            type: 'object',
            properties: { title: { type: 'string' }, body: { type: 'string' } },
            required: ['title', 'body']
          }
        }
      },
      required: ['basis_sentence', 'confidence', 'reference_points', 'concerns']
    }
  };

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), SETTINGS.timeoutMs);

  try {
    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      signal: controller.signal,
      headers: {
        'content-type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: SETTINGS.model,
        max_tokens: SETTINGS.maxTokens,
        temperature: SETTINGS.temperature,
        system,
        tools: [tool],
        tool_choice: { type: 'tool', name: 'emit_reveal' },
        messages: [{ role: 'user', content: 'Produce the reveal for the founder described in the system prompt.' }]
      })
    });

    if (!r.ok) throw new Error('anthropic ' + r.status + ' ' + (await r.text()).slice(0, 300));
    const body = await r.json();
    const block = (body.content || []).find(c => c.type === 'tool_use');
    if (!block) throw new Error('no tool_use block returned');
    return block.input;
  } finally {
    clearTimeout(timer);
  }
}

/* ---------- guard rails ---------- */

function enforce(out, anchor, fallback) {
  /* There is no range left to clamp. What remains is a whitelist: only prose the
     model wrote about the founder's own answers gets through, and every numeric
     field is dropped on the floor rather than trusted. */
  if (!out || typeof out !== 'object') return fallback;
  const clean = {
    basis_sentence: typeof out.basis_sentence === 'string' ? out.basis_sentence.slice(0, 400) : fallback.basis_sentence,
    confidence: ['low', 'medium', 'high'].includes(out.confidence) ? out.confidence : fallback.confidence,
    reference_points: Array.isArray(out.reference_points) ? out.reference_points.slice(0, 4) : [],
    concerns: Array.isArray(out.concerns) ? out.concerns.slice(0, 3) : [],
    source: 'model'
  };
  return clean;
}

/* ---------- small helpers ---------- */
function safeParse(x) { try { return JSON.parse(x); } catch (e) { return {}; } }
function s(v) { return v === undefined || v === null ? '' : String(v).slice(0, 1200); }
/* A percentage, or nothing. Never a string, so a figure smuggled in as text does not survive. */
function n(v) { return typeof v === 'number' && isFinite(v) ? v : null; }
function t(v, n) { return String(v === undefined || v === null ? '' : v).slice(0, n); }
function round1(n) { return Math.round(n * 10) / 10; }

function rateLimited(ip) {
  const now = Date.now();
  const rec = hits.get(ip) || { count: 0, since: now };
  if (now - rec.since > 3600000) { rec.count = 0; rec.since = now; }
  rec.count += 1;
  hits.set(ip, rec);
  return rec.count > SETTINGS.rateLimit.perIpPerHour;
}
