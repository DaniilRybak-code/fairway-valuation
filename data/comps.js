/* Verified market anchors. Everything here must be traceable to a named source
 * with a vintage. Nothing in this file may be estimated, rounded from memory,
 * or produced by a model. If we cannot cite it, it does not belong here.
 *
 * Geography: Carta's dataset is predominantly US, which is deliberate. The US
 * generates most of the data points, so it is the spine. Non-US companies are
 * handled by the regional adjustment below rather than by a separate table.
 *
 * Figures are POST-money medians. Pre-money is derived as post minus the round,
 * using the founder's own raise band, which is arithmetic rather than assumption.
 */

export const COMPS = {
  vintage: '2025-Q4',
  updated: '2026-08-19',

  /* Stage anchors. Source: Carta, "Record-setting early-stage valuations",
     covering Q4 2025. Seed and Series A are the two figures Carta published
     directly; the others are marked null rather than guessed. */
  stages: {
    'Pre-seed': {
      post_median_m: null,
      source: null,
      note: 'Not published in the cited Carta release. Engine falls back to a wider band and says so.'
    },
    'Seed': {
      post_median_m: 24.0,
      post_median_prior_year_m: 18.0,
      source: 'Carta, Record-setting early-stage valuations, Q4 2025',
      note: 'US-weighted. Median post-money across all sectors.'
    },
    'Series A': {
      post_median_m: 78.7,
      post_median_prior_year_m: 57.5,
      source: 'Carta, Record-setting early-stage valuations, Q4 2025',
      note: 'US-weighted. Median post-money across all sectors. Up 37% year on year.'
    }
  },

  /* Market context the model may cite. Each entry carries its own source. */
  context: [
    {
      claim: 'The down-round rate fell to 11.4% of priced rounds in Q1 2026.',
      source: 'Carta, State of Private Markets, Q1 2026'
    },
    {
      claim: 'Median seed post-money rose from $18M in Q4 2024 to $24M in Q4 2025, and Series A from $57.5M to $78.7M over the same period.',
      source: 'Carta, Record-setting early-stage valuations, Q4 2025'
    },
    {
      claim: 'Of 431 VC-backed startups that shut down since 2023, 70% ran out of capital and 43% cited poor product-market fit.',
      source: 'CB Insights, why startups fail'
    }
  ],

  /* Sector overlay. EMPTY ON PURPOSE.
   *
   * This is where the reviewing team's own knowledge goes, and it is the part
   * no competitor can copy. Each row is a multiplier applied to the stage
   * anchor, plus an optional ARR multiple for revenue-stage companies.
   * Fill these in a session with the reviewers, put a name against each, and
   * the engine will start using them automatically.
   *
   * Shape:
   *   'Fintech': { stage_multiple: 1.05, arr_multiple_median: 12, n: 40,
   *                source: 'Reviewer panel, Aug 2026', confidence: 'medium' }
   */
  sectors: {},

  /* Regional adjustment to the US-weighted anchors. Also empty on purpose:
   * these numbers should come from the reviewers, not from a guess.
   * Shape: 'GB': { multiple: 0.7, source: '...', confidence: 'low' }
   */
  regions: {}
};

export default COMPS;
