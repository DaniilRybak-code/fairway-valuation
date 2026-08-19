/* Macro-settings for the reveal engine.
 *
 * This file is the dial panel. Change behaviour here rather than in api/reveal.js.
 * Anything that constrains what the model is allowed to say lives here, so the
 * guard rails are reviewable in one place.
 */

export const SETTINGS = {
  /* ---- model ---- */
  /* Set ANTHROPIC_MODEL in Vercel to pin a specific version. Check the current
     model list before pinning; do not assume an identifier still exists. */
  model: process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-5',
  maxTokens: 1600,
  /* Zero, because two founders with identical answers must see the same range. */
  temperature: 0,

  /* Let the model search the web for fresh sector multiples and recent rounds.
     Off by default: it adds latency and cost, and every returned figure still
     has to carry a source before we will print it. Turn on once you are happy
     with the tool version string for the current API. */
  allowWebSearch: false,

  /* ---- what the model is allowed to move ---- */
  /* The deterministic engine produces an anchor band from data/comps.js. The
     model may move within this corridor and no further. Outside it, the code
     clamps and flags the output as adjusted. */
  corridor: {
    lowMultiple: 0.70,   // model may go down to 70% of the anchor low
    highMultiple: 1.40   // and up to 140% of the anchor high
  },

  /* Range width, low to high. Narrower is a false claim of precision on nine
     multiple-choice answers. Wider is useless to the founder. */
  width: { min: 1.35, max: 2.30 },

  /* Sanity check on the round itself. Outside this, we say so rather than
     quietly printing a number that implies a strange cap table. */
  dilutionFlag: { min: 8, max: 40 },

  /* ---- reference points ---- */
  referencePoints: {
    total: 4,
    visible: 2,          // the rest render locked
    /* A reference point with no source is dropped before rendering. This is the
       single most important rule in the file: an invented comparable round is
       worse than no reveal at all. */
    requireSource: true,
    minSurviving: 2      // below this, fall back to the deterministic reveal
  },

  /* ---- operational ---- */
  cacheTtlMinutes: 1440,
  rateLimit: { perIpPerHour: 12 },
  timeoutMs: 25000
};

export default SETTINGS;
