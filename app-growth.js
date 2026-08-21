/* Growth, and the bridge from MRR to the two forward revenue figures.
 *
 * Loaded BEFORE app.js. Kept separate because it is the part of the funnel most
 * likely to be argued about, and it should be readable without scrolling past
 * three hundred lines of investor lists to find it.
 */

/* Growth persistence: the observed ratio of next year's growth rate to this
   year's. Point Nine measured a median of 75% across 29 early-stage SaaS
   companies and 96 data pairs, against 89% for public SaaS (75 companies, 218
   data pairs, regression slope 0.775) and Scale Venture Partners' 80 to 85%.
   Our users are the early-stage sample.

   It is applied to a TRAILING twelve-month growth rate, which is what the
   research measured. It is not applied to a spot monthly rate: that is a
   different claim, and it is the reason the quiz question changed.
   https://medium.com/point-nine-news/persistence-and-predictability-of-saas-growth-bd7b90ee20d3 */
const GROWTH_PERSISTENCE = 0.75;

const GROWTH_BAND_PROXY = {
  'Roughly flat': 0,
  'Growing, under 100% a year': 50,
  'Growing, 100% or more a year': 150
};

function growthBand(pct) {
  if (pct === null || pct === undefined) return 'Too early to measure';
  if (pct < 100) return 'Growing, under 100% a year';
  return 'Growing, 100% or more a year';
}

/* Forward twelve-month growth, as a decimal. Null when we have nothing to go on,
   which is a state the field draws rather than papers over. */
function forwardAnnualGrowth() {
  const y = responses.growth_yoy;
  if (y === null || y === undefined) {
    const proxy = GROWTH_BAND_PROXY[responses.growth];
    if (proxy === undefined) return null;
    return (proxy / 100) * GROWTH_PERSISTENCE;
  }
  return Math.max(-0.5, (y / 100) * GROWTH_PERSISTENCE);
}

/* NTM revenue is the SUM of the next twelve months, because consensus forward
   revenue is a sum and the two have to be on the same basis to be divided by the
   same multiple. Month-twelve ARR is an exit run-rate and is a different, larger
   number: at 8% monthly growth the two differ by about 47%, at 15% by 93%.
   Using one where the other belongs moves a valuation by more than half. */
function forwardRevenue(monthlyRevenue, forwardGrowth) {
  if (!(monthlyRevenue > 0)) return { ntmM: null, exitArrM: null };
  const f = (forwardGrowth === null || forwardGrowth === undefined) ? 0 : forwardGrowth;
  const m = Math.pow(1 + f, 1 / 12) - 1;
  let sum = 0;
  for (let t = 1; t <= 12; t++) sum += monthlyRevenue * Math.pow(1 + m, t);
  return {
    ntmM: sum / 1e6,
    exitArrM: monthlyRevenue * (1 + f) * 12 / 1e6
  };
}
