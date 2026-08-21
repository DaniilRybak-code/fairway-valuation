/* Resolves the visitor's country from the Vercel edge header and maps it to a
 * reporting currency, so the funnel does not have to ask.
 *
 * Coarse only: country code, and a currency guess. No IP is read, stored or
 * returned. The founder can override the currency next to the range.
 */

const CURRENCY_BY_COUNTRY = {
  US: 'USD', GB: 'GBP', IE: 'EUR', CA: 'CAD', AU: 'AUD', NZ: 'AUD',
  DE: 'EUR', FR: 'EUR', ES: 'EUR', IT: 'EUR', NL: 'EUR', BE: 'EUR', AT: 'EUR',
  PT: 'EUR', FI: 'EUR', GR: 'EUR', LU: 'EUR', EE: 'EUR', LV: 'EUR', LT: 'EUR',
  SI: 'EUR', SK: 'EUR', CY: 'EUR', MT: 'EUR', HR: 'EUR',
  CH: 'CHF', SE: 'SEK', NO: 'NOK', DK: 'DKK', PL: 'PLN',
  SG: 'SGD', HK: 'HKD', JP: 'JPY', IN: 'INR',
  AE: 'AED', SA: 'SAR', IL: 'ILS', ZA: 'ZAR', BR: 'BRL', MX: 'MXN'
};

export default function handler(req, res) {
  const country = header(req, 'x-vercel-ip-country');
  const currency = CURRENCY_BY_COUNTRY[country] || 'USD';
  /* Short cache: the answer only changes if the visitor moves country. */
  res.setHeader('cache-control', 'public, max-age=3600');
  res.status(200).json({ country: country || null, currency: currency });
}

function header(req, k) {
  return (req.headers && req.headers[k]) ? String(req.headers[k]).toUpperCase() : '';
}
