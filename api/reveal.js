/* The reveal engine.
 *
 * Every request goes through a model with fixed macro-settings (config/) and a
 * verified data pack (data/comps.js). The model positions the range inside a
 * corridor the code computes, writes the basis sentence, and produces the four
 * reference points and three concerns. The code then enforces the guard rails
 * and falls back to a deterministic range if anything about the output is off.
 *
 * The model never decides the corridor and never gets to state a figure that
 * has no source. Those two constraints are what make this defensible.
 *
 * Env: ANTHROPIC_API_KEY (required), ANTHROPIC_MODEL (optional)
 */

import { SETTINGS } from '../config/reveal-settings.js';
import { buildSystem } from '../config/reveal-prompt.js';
import { COMPS } from '../data/comps.js';

export const config = { maxDuration: 60 };

/* PLACEHOLDER. Dispersion around the stage median, used to build the corridor.
   These are assumptions, not data, and the basis sentence says so. Replace the
   moment real p25 and p75 figures are in data/comps.js. */
const ASSUMED_DISPERSION = { low: 0.65, high: 1.55 };

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
    basis = `no published anchor for ${a.stage || 'this stage'} in the current pack, so the range is derived from stage patterns rather than a comp set and is correspondingly wide`;
  }

  if (preAnchor && sectorRow && sectorRow.stage_multiple) {
    preAnchor = preAnchor * sectorRow.stage_multiple;
    basis += `, adjusted for ${a.sector} (${sectorRow.source})`;
  }
  if (preAnchor && regionRow && regionRow.multiple) {
    preAnchor = preAnchor * regionRow.multiple;
    basis += `, adjusted for ${a.country} (${regionRow.source})`;
  }

  const heuristic = heuristicBase(a);
  const centre = preAnchor || heuristic;
  const anchorLow = centre * ASSUMED_DISPERSION.low;
  const anchorHigh = centre * ASSUMED_DISPERSION.high;

  return {
    raise, centre, anchorLow, anchorHigh,
    hasVerifiedAnchor: !!preAnchor,
    basis: basis,
    corridorLow: round1(anchorLow * SETTINGS.corridor.lowMultiple),
    corridorHigh: round1(anchorHigh * SETTINGS.corridor.highMultiple),
    vintage: COMPS.vintage
  };
}

/* Same shape as the client-side first pass, used as the safety net. */
function heuristicBase(a) {
  const stageBase = { 'Pre-seed': 1.5, 'Seed': 3.5, 'Series A': 9 }[a.stage] || 2;
  const revenueBump = { 'Pre-revenue': 0, 'Under $10k/mo': 0.4, '$10k–$50k/mo': 1.2, '$50k–$150k/mo': 3, '$150k+/mo': 6 }[a.revenue] || 0;
  const growthMult = { 'Early / pre-traction': 1, 'Steady, under 15%/mo': 1.15, 'Fast, 15%+/mo': 1.4 }[a.growth] || 1;
  const profitMult = { 'Profitable': 1.15, 'Around break-even': 1.05, 'Burning, 12+ months runway': 1, 'Burning, under 12 months runway': 0.9 }[a.profit] || 1;
  return (stageBase + revenueBump) * growthMult * profitMult;
}

function deterministic(a, anchor) {
  return {
    range_low_m: round1(anchor.centre * 0.85),
    range_high_m: round1(anchor.centre * 1.55),
    basis_sentence: `First-pass range from ${anchor.basis}. Reviewed by a person within 24 hours.`,
    confidence: anchor.hasVerifiedAnchor ? 'medium' : 'low',
    reference_points: [],
    concerns: [],
    vintage: anchor.vintage,
    verified_anchor: anchor.hasVerifiedAnchor,
    source: 'deterministic'
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
    corridorLow: anchor.corridorLow,
    corridorHigh: anchor.corridorHigh,
    anchorBasis: anchor.basis
  });

  const tool = {
    name: 'emit_reveal',
    description: 'Return the reveal for this founder.',
    input_schema: {
      type: 'object',
      properties: {
        range_low_m: { type: 'number' },
        range_high_m: { type: 'number' },
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
      required: ['range_low_m', 'range_high_m', 'basis_sentence', 'confidence', 'reference_points', 'concerns']
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
  let low = Number(out.range_low_m);
  let high = Number(out.range_high_m);
  const notes = [];

  if (!isFinite(low) || !isFinite(high) || low <= 0 || high <= low) {
    return { ...fallback, source: 'fallback', reason: 'bad_range' };
  }

  if (low < anchor.corridorLow) { low = anchor.corridorLow; notes.push('clamped_low'); }
  if (high > anchor.corridorHigh) { high = anchor.corridorHigh; notes.push('clamped_high'); }

  const width = high / low;
  if (width < SETTINGS.width.min) { high = low * SETTINGS.width.min; notes.push('widened'); }
  if (width > SETTINGS.width.max) { high = low * SETTINGS.width.max; notes.push('narrowed'); }

  /* A reference point without a source never reaches a founder. */
  let refs = Array.isArray(out.reference_points) ? out.reference_points : [];
  if (SETTINGS.referencePoints.requireSource) {
    refs = refs.filter(p => p && p.source && String(p.source).trim().length > 3);
  }
  if (refs.length < SETTINGS.referencePoints.minSurviving) {
    return { ...fallback, source: 'fallback', reason: 'insufficient_sourced_reference_points' };
  }
  refs = refs.slice(0, SETTINGS.referencePoints.total).map(p => ({
    label: t(p.label, 90), kind: t(p.kind, 20), detail: t(p.detail, 400), source: t(p.source, 160)
  }));

  const concerns = (Array.isArray(out.concerns) ? out.concerns : [])
    .slice(0, 3)
    .map(c => ({ title: t(c.title, 120), body: t(c.body, 500) }));

  const mid = (low + high) / 2;
  const dilMid = anchor.raise / (mid + anchor.raise) * 100;
  const dilutionFlag = dilMid < SETTINGS.dilutionFlag.min || dilMid > SETTINGS.dilutionFlag.max;

  return {
    range_low_m: round1(low),
    range_high_m: round1(high),
    basis_sentence: t(out.basis_sentence, 400),
    confidence: ['low', 'medium', 'high'].includes(out.confidence) ? out.confidence : 'low',
    reference_points: refs,
    visible_reference_points: SETTINGS.referencePoints.visible,
    concerns,
    dilution_flag: dilutionFlag,
    vintage: anchor.vintage,
    verified_anchor: anchor.hasVerifiedAnchor,
    adjustments: notes,
    source: 'model'
  };
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
