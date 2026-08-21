/* Growth, and the bridge from MRR to the two forward revenue figures.
 *
 * Loaded BEFORE app.js.
 *
 * There are no coefficients in this file, deliberately. An earlier build applied
 * a growth persistence factor to haircut the founder's own rate. It was removed:
 * a number the founder cannot see the reason for is a number they cannot argue
 * with, and a haircut we impose is our forecast wearing their clothes.
 *
 * Instead we ask two questions and use the answers as given. The founder owns
 * the forward number. Our job is to price it, and to show the reviewer both
 * figures so they can say whether the plan is credible.
 */

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

/* Forward twelve-month growth, as a decimal.
 *
 * The founder's plan if they gave one. Their trailing rate if they did not, and
 * the page says so on the row rather than passing it off as a forecast. Null
 * when we have neither, which is a state the field draws rather than papers over. */
function forwardAnnualGrowth() {
  const plan = responses.growth_plan;
  if (plan !== null && plan !== undefined) return Math.max(-0.9, plan / 100);

  const y = responses.growth_yoy;
  if (y !== null && y !== undefined) return Math.max(-0.9, y / 100);

  const proxy = GROWTH_BAND_PROXY[responses.growth];
  if (proxy === undefined) return null;
  return proxy / 100;
}

/* Which of the two the forward figure actually came from, so the row can say it. */
function forwardGrowthBasis() {
  if (responses.growth_plan !== null && responses.growth_plan !== undefined) return 'plan';
  if (responses.growth_yoy !== null && responses.growth_yoy !== undefined) return 'trailing';
  if (GROWTH_BAND_PROXY[responses.growth] !== undefined) return 'band';
  return null;
}

/* NTM revenue is the SUM of the next twelve months, because consensus forward
   revenue is a sum and the two have to be on the same basis to be divided by the
   same multiple. Month-twelve ARR is an exit run-rate and is a different, larger
   number: at 100% annual growth the two differ by about 40%.

   Both are plain arithmetic on the founder's own two numbers. Either can be
   reproduced by hand from what the page shows. */
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
