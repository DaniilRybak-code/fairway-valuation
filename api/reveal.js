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
 * Env: ANTHROPIC_API_KEY (required), ANTHROPIC_MODEL (optional)
 */

import { SETTINGS } from '../config/reveal-settings.js';
import { buildSystem } from '../config/reveal-prompt.js';
import { COMPS } from '../data/comps.js';

export const config = { maxDuration: 60 };

const RAISE_MIDPOINT = {
  'Under $500k': 0.35, '$500k–$1M': 0.75, '$1M–$2.5M': 1.75,
  '$2.5M–$5M': 3.75, '$5M–$10M': 7.5, 'Over $10M': 12
};

const cache = new Map();
const hits = new Map();

export default async function handler(req, res) {
  if (req.method !== 'POST') { res.status(405).json({ error: 'method_not_allowed' }); return; }

  const ip = String(req.headers['x-forwarded-for'] || 'unknown').split(',')[0].trim();
  if (rateLimited(ip)) { res.status(429).json({ error: 'rate_limited' }); return; }

  const a = typeof req.body === 'string' ? safeParse(req.body) : (req.body || {});
  /* Contact details are never sent to the model. Nothing here identifies a person. */
  const answers = {
    stage: s(a.stage), sector: s(a.sector), sector_detail: s(a.sector_detail),
    revenue: s(a.revenue), growth: s(a.growth), growth_detail: s(a.growth_detail),
    profit: s(a.profit), raise: s(a.raise), timing: s(a.timing),
    concerns: Array.isArray(a.concerns) ? a.concerns.map(s) : [],
    concern_notes: s(a.concern_notes),
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
    res.status(200).json({ ...fallback, source: 'fallback', reason: 'no_api_key' });
    return;
  }

  try {
    const out = await callModel(answers, anchor);
    const clean = enforce(out, anchor, fallback);
    cache.set(key, { at: Date.now(), payload: clean });
    res.status(200).json(clean);
  } catch (err) {
    console.error('[fairway-reveal] model call failed:', err && err.message);
    res.status(200).json({ ...fallback, source: 'fallback', reason: 'model_error' });
  }
}

/* ---------- anchors ---------- */

function buildAnchor(a) {
  const raise = RAISE_MIDPOINT[a.raise] || 1.0;
  const stageRow = COMPS.stages[a.stage] || {};
  const sectorRow = COMPS.sectors[a.sector] || null;
  const regionRow = COMPS.regions[a.country] || null;

  let preAnchor = null;
  let basis = '';

  if (stageRow.post_median_m) {
    preAnchor = Math.max(stageRow.post_median_m - raise, 0.3);
    basis = `${a.stage} median post-money of $${stageRow.post_median_m}M (${stageRow.source}), less the midpoint of the stated raise`;
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
    raise,
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
