/* Public-market comparables, browser side.
 *
 * Every figure here comes from one place and is citable by name. This is the file
 * the reviewers refresh, and nothing may enter it that we cannot attribute.
 *
 * Source: Aswath Damodaran, NYU Stern, "Revenue Multiples by Industry Sector",
 * data as of January 2026, 5,994 US firms. Free, public, and the standard
 * reference for exactly this purpose.
 *
 * `industry` is the Damodaran industry we map our sector onto, and it is shown
 * to the founder on the row. Where the mapping is a judgement rather than an
 * obvious match, `note` says so, because a mapping the founder cannot see is a
 * mapping they cannot argue with.
 */

const PUBLIC_COMPS = {
  source: 'Damodaran, NYU Stern, revenue multiples by industry',
  vintage: 'January 2026',
  universe: '5,994 US listed firms',
  url: 'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/psdata.html',

  /* There was an illiquidity discount here. It has been removed.

     It was a judgement of ours, invented to bridge a listed industry aggregate
     to a private company, and it was doing the work that a properly selected
     peer set should do. Nothing on this page may be a number we made up, so it
     is gone rather than re-tuned. The listed multiple below is now shown as
     market context only, and is not converted into a valuation of anybody. */

  sectors: {
    'SaaS / B2B software':            { industry: 'Software (System & Application)', ev_sales: 11.41, n: 309 },
    'AI / ML':                        { industry: 'Software (System & Application)', ev_sales: 11.41, n: 309 },
    'Fintech':                        { industry: 'Software (System & Application)', ev_sales: 11.41, n: 309, note: 'Mapped to software rather than financial services: revenue is defined differently for banks and insurers, so their reported multiples are not comparable.' },
    'Insurtech':                      { industry: 'Insurance (Prop/Cas.)', ev_sales: 1.49, n: 57, note: 'Mapped to insurance because carrying or sharing underwriting risk is what the market prices. A pure software MGA platform belongs closer to software.' },
    'Healthtech / Digital health':    { industry: 'Healthcare Information and Technology', ev_sales: 5.31, n: 115 },
    'Biotech / Life sciences':        { industry: 'Drugs (Biotechnology)', ev_sales: 7.92, n: 496, note: 'Shown for reference only. Pre-commercial biotech is priced on programme value and precedent rounds, not on a revenue multiple.' },
    'Medtech / Devices':              { industry: 'Healthcare Products', ev_sales: 4.76, n: 204 },
    'Consumer / D2C':                 { industry: 'Retail (Special Lines)', ev_sales: 1.63, n: 94 },
    'E-commerce / Retail':            { industry: 'Retail (General)', ev_sales: 2.11, n: 23 },
    'Marketplaces':                   { industry: 'Software (Internet)', ev_sales: 9.56, n: 29, note: 'Applied to net revenue. If you quote GMV, this multiple does not apply to it.' },
    'Climate / Energy':               { industry: 'Green & Renewable Energy', ev_sales: 7.87, n: 15 },
    'Deeptech / Hardware':            { industry: 'Electronics (General)', ev_sales: 3.21, n: 114 },
    'Cybersecurity':                  { industry: 'Software (System & Application)', ev_sales: 11.41, n: 309 },
    'Logistics / Supply chain':       { industry: 'Transportation', ev_sales: 1.64, n: 19, note: 'If your revenue is a software or data fee rather than freight, the applicable set is software at 11.41x. Separating the two is worth more than any other change here.' },
    'Proptech':                       { industry: 'Real Estate (Operations & Services)', ev_sales: 1.46, n: 54 },
    'Edtech':                         { industry: 'Education', ev_sales: 1.99, n: 32 },
    'Legaltech / Regtech':            { industry: 'Software (System & Application)', ev_sales: 11.41, n: 309 },
    'HR tech / Future of work':       { industry: 'Software (System & Application)', ev_sales: 11.41, n: 309 },
    'Adtech / Martech':               { industry: 'Advertising', ev_sales: 2.12, n: 52, note: 'Applied to net revenue. Gross billings are restated before any multiple is applied.' },
    'Media / Content':                { industry: 'Entertainment', ev_sales: 4.33, n: 92 },
    'Gaming':                         { industry: 'Software (Entertainment)', ev_sales: 9.13, n: 77 },
    'Travel / Hospitality':           { industry: 'Hotel/Gaming', ev_sales: 4.33, n: 63 },
    'Food / Beverage':                { industry: 'Food Processing', ev_sales: 1.47, n: 78 },
    'Agritech':                       { industry: 'Farming/Agriculture', ev_sales: 1.34, n: 35 },
    'Web3 / Digital assets':          { industry: 'Software (Internet)', ev_sales: 9.56, n: 29, note: 'Mapped to internet software. Fee revenue only: token-driven activity is excluded before the multiple is applied.' },
    'Defence / Gov tech':             { industry: 'Aerospace/Defense', ev_sales: 3.57, n: 79 },
    'Telecoms / Connectivity':        { industry: 'Telecom. Services', ev_sales: 2.61, n: 39 },
    'Mobility / Automotive':          { industry: 'Auto & Truck', ev_sales: 3.88, n: 33 },
    'Agencies / Professional services': { industry: 'Business & Consumer Services', ev_sales: 2.53, n: 155 },
    'Other':                          { industry: 'Total Market', ev_sales: 3.97, n: 5994 }
  }
};

/* Stage anchors. Source: Carta, Record-setting early-stage valuations, Q4 2025.
   A median is a point, not a range, and it is drawn as a point for that reason. */
const STAGE_ANCHOR = {
  'Pre-seed': { post_median_m: null, source: null },
  'Seed': { post_median_m: 24.0, currency: 'USD', source: 'Carta, Record-setting early-stage valuations, Q4 2025', note: 'US-weighted, all sectors. Median post-money.' },
  'Series A': { post_median_m: 78.7, currency: 'USD', source: 'Carta, Record-setting early-stage valuations, Q4 2025', note: 'US-weighted, all sectors. Median post-money.' }
};

/* Euro foreign exchange reference rates. Free, public, published daily, and
 * citable to the day, which is the only reason we are willing to convert at all.
 * Rates are units of the currency per one euro, exactly as the ECB publishes them.
 * Currencies the ECB does not publish are absent on purpose: a row we cannot
 * convert with a sourced rate is left unplotted rather than converted anyway.
 * Refresh by pasting a later day's table and moving the date.
 */
const FX = {
  source: 'European Central Bank, euro foreign exchange reference rates',
  date: '20 August 2026',
  perEur: {
    EUR: 1, USD: 1.1681, JPY: 185.45, CZK: 24.153, DKK: 7.4758, GBP: 0.85725,
    HUF: 365.10, PLN: 4.3188, RON: 5.2515, SEK: 11.0875, CHF: 0.9333,
    ISK: 142.00, NOK: 10.9025, TRY: 56.0145, AUD: 1.6438, BRL: 6.0666,
    CAD: 1.6085, CNY: 7.8538, HKD: 9.1624, IDR: 20788.62, ILS: 3.4950,
    INR: 111.7985, KRW: 1631.08, MXN: 19.8467, MYR: 4.7238, NZD: 1.9657,
    PHP: 72.104, SGD: 1.4860, THB: 38.448, ZAR: 18.8929
  }
};

/* Returns null rather than guessing when either side is missing. */
function fxConvert(amount, from, to) {
  const a = FX.perEur[from], b = FX.perEur[to];
  if (!a || !b || typeof amount !== 'number') return null;
  return amount / a * b;
}
