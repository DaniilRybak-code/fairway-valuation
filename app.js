/* Fairway landing funnel. Config first, then data, then flow.
 * The valuation content layer lives in drivers.js and the football field in field.js,
 * both of which load after this file. */

const CONFIG = {
  stripeLink: 'https://buy.stripe.com/bJe6oG3Xf5Tp1Sf1n1cjS00',
  price: 750,
  spotsPerWeek: 5,
  spotsLeft: 2,
  leadEndpoint: '/api/lead',
  /* Prior employers of the reviewing team. Text only, no logos: see notes in the repo.
     Every name here must be true of someone who actually reviews reports. */
  teamFirms: ['Morgan Stanley', 'Goldman Sachs', 'J.P. Morgan', 'Deutsche Bank', 'Barclays', 'PJT Partners'],
  /* Illustrative growth assumption used on the result screen. */
  valuationGrowth12m: 2
};

const SECTORS = [
  'SaaS / B2B software', 'AI / ML', 'Fintech', 'Insurtech',
  'Healthtech / Digital health', 'Biotech / Life sciences', 'Medtech / Devices',
  'Consumer / D2C', 'E-commerce / Retail', 'Marketplaces',
  'Climate / Energy', 'Deeptech / Hardware', 'Cybersecurity',
  'Logistics / Supply chain', 'Proptech', 'Edtech',
  'Legaltech / Regtech', 'HR tech / Future of work', 'Adtech / Martech',
  'Media / Content', 'Gaming', 'Travel / Hospitality', 'Food / Beverage',
  'Agritech', 'Web3 / Digital assets', 'Defence / Gov tech',
  'Telecoms / Connectivity', 'Mobility / Automotive',
  'Agencies / Professional services', 'Other'
];

/* How the revenue is earned. Single select. This changes which multiple set applies
   more than sector does in several cases, which is why it is asked separately. */
const REVENUE_MODELS = [
  'Subscription / SaaS', 'Usage or consumption', 'Transaction fee / take rate',
  'Marketplace commission', 'One-off sales or licences', 'Services / retainer',
  'Advertising', 'Hardware plus software', 'Interest / spread', 'Other'
];

/* Display only. All maths runs in the founder's own currency, because a multiple is a
   ratio and does not need converting. The one place a rate is used is the US dollar
   stage anchor on the field, and that is converted at a published ECB rate with a date. */
const CURRENCY_SYMBOL = {
  USD: '$', GBP: '£', EUR: '€', CAD: 'C$', AUD: 'A$', CHF: 'CHF ',
  SEK: 'kr', NOK: 'kr', DKK: 'kr', SGD: 'S$', HKD: 'HK$', JPY: '¥',
  INR: '₹', AED: 'AED ', SAR: 'SAR ', ILS: '₪', ZAR: 'R',
  BRL: 'R$', MXN: 'MX$', PLN: 'zł'
};

const CONCERNS = [
  'Valuation looks high', 'Market size', 'Traction is early', 'Unit economics',
  'Churn or retention', 'Competition', 'Team gaps', 'Regulatory risk',
  'Concentration in a few customers', 'Nothing specific yet'
];

const INVESTORS = {
  'SaaS / B2B software': [
    { name: 'Playfair Capital', note: 'AI, enterprise software and developer tools. First cheques £100k to £1.5M.' },
    { name: 'Episode 1 Ventures', note: 'UK-only B2B software. £250k to £3M.' },
    { name: 'Concept Ventures', note: 'AI, deep tech and infrastructure software. Around £1M average first cheque.' }
  ],
  'AI / ML': [
    { name: 'Concept Ventures', note: 'AI, deep tech and infrastructure software. Around £1M average first cheque.' },
    { name: 'MMC Ventures', note: 'AI-first companies. Around $3.2M average seed cheque.' },
    { name: 'Playfair Capital', note: 'AI, enterprise software and developer tools. £100k to £1.5M.' }
  ],
  'Fintech': [
    { name: 'Seedcamp', note: 'Fintech, AI, developer tools and marketplaces. First cheques $350k to $1M.' },
    { name: 'Passion Capital', note: 'Fintech, insurtech and marketplaces. £1M to £2M.' },
    { name: 'LocalGlobe / Latitude', note: 'Fintech, health, climate and marketplaces. £500k to £2M at seed.' }
  ],
  'Insurtech': [
    { name: 'Passion Capital', note: 'Fintech, insurtech and marketplaces. £1M to £2M.' },
    { name: 'Octopus Ventures', note: 'Fintech, B2B SaaS, health and climate. Active seed through Series A.' },
    { name: 'Seedcamp', note: 'Fintech, AI, developer tools and marketplaces. $350k to $1M.' }
  ],
  'Healthtech / Digital health': [
    { name: 'Octopus Ventures', note: 'Healthtech and biotech alongside B2B SaaS. Active seed through Series A.' },
    { name: 'Ada Ventures', note: 'Healthy ageing and economic empowerment theses. £250k to £1.5M.' },
    { name: 'Mercia Ventures', note: 'Life sciences, software and deeptech. Among the most active UK early-stage funds by deal count.' }
  ],
  'Biotech / Life sciences': [
    { name: 'Mercia Ventures', note: 'Life sciences, software and deeptech. Among the most active UK early-stage funds by deal count.' },
    { name: 'Future Planet Capital', note: 'Deeptech, health and engineering biology out of the university ecosystem.' },
    { name: 'Backed VC', note: 'AI therapeutics and frontier science. $500k to $5M.' }
  ],
  'Consumer / D2C': [
    { name: 'Hoxton Ventures', note: 'Broad tech with a consumer and fintech lean. $500k to $5M.' },
    { name: 'Fuel Ventures', note: 'B2C and B2B via SEIS/EIS. High early-stage deal volume. £100k to £1M.' },
    { name: 'Cherry Ventures', note: 'Europe-wide, sector-agnostic at seed. €2M to €7M.' }
  ],
  'Marketplaces': [
    { name: 'Seedcamp', note: 'Marketplaces, fintech, AI and developer tools. First cheques $350k to $1M.' },
    { name: 'Fuel Ventures', note: 'B2B SaaS and marketplaces via SEIS/EIS. £100k to £1M.' },
    { name: 'Passion Capital', note: 'Marketplaces, fintech and insurtech. £1M to £2M.' }
  ],
  'Climate / Energy': [
    { name: 'Octopus Ventures', note: 'Climate tech alongside B2B SaaS and deeptech. Active seed through Series A.' },
    { name: 'Ada Ventures', note: 'Climate equity thesis. £250k to £1.5M.' },
    { name: 'Future Planet Capital', note: 'Climate, deeptech and engineering biology. High early-stage deal volume.' }
  ],
  'Deeptech / Hardware': [
    { name: 'Concept Ventures', note: 'Deep tech, AI and infrastructure software. Around £1M average first cheque.' },
    { name: 'Mercia Ventures', note: 'Deeptech, life sciences and software. Among the most active UK early-stage funds.' },
    { name: 'Future Planet Capital', note: 'Deeptech, space, defence and engineering biology.' }
  ],
  'Cybersecurity': [
    { name: 'Playfair Capital', note: 'Enterprise software, AI and developer tools. £100k to £1.5M.' },
    { name: 'Episode 1 Ventures', note: 'UK-only B2B software including infrastructure and security. £250k to £3M.' },
    { name: 'Octopus Ventures', note: 'B2B SaaS and deeptech. Active seed through Series A.' }
  ],
  'Logistics / Supply chain': [
    { name: 'Maven Capital Partners', note: 'SaaS, transport and energy. Among the most active UK early-stage investors by deal count.' },
    { name: 'Fuel Ventures', note: 'B2B SaaS and marketplaces via SEIS/EIS. £100k to £1M.' },
    { name: 'Backed VC', note: 'Manufacturing and automation alongside frontier tech. $500k to $5M.' }
  ],
  'Proptech': [
    { name: 'Fuel Ventures', note: 'B2B SaaS and marketplaces via SEIS/EIS. £100k to £1M.' },
    { name: 'Concept Ventures', note: 'Infrastructure software and AI. Around £1M average first cheque.' },
    { name: 'SFC Capital', note: 'The most active UK early-stage investor by deal count. SEIS-led, £100k to £300k.' }
  ],
  'Edtech': [
    { name: 'Founders Factory', note: 'Multi-sector early-stage via corporate partners. £30k to £250k.' },
    { name: 'SFC Capital', note: 'The most active UK early-stage investor by deal count. SEIS-led, £100k to £300k.' },
    { name: 'Mercia Ventures', note: 'Software and consumer alongside deeptech. High early-stage deal volume.' }
  ],
  'Other': [
    { name: 'SFC Capital', note: 'The most active UK early-stage investor by deal count. SEIS-led, £100k to £300k.' },
    { name: 'SyndicateRoom', note: 'Sector-agnostic, high-volume early-stage syndicate.' },
    { name: 'Fuel Ventures', note: 'B2B SaaS, marketplaces and fintech via SEIS/EIS. £100k to £1M.' }
  ]
};

const FIX_BY_REVENUE = {
  'Pre-revenue': { title: 'Turn your pipeline into signed evidence.', body: 'Three named design partners with a start date and a price does more for a pre-revenue range than any traction slide. At this stage the range is priced on proof of demand, not on product.' },
  'Under $10k/mo': { title: 'Show retention before you show growth.', body: 'At this revenue the first question is whether the early customers stay. A three-month cohort chart pre-empts it and defends the top of your range. A cumulative revenue line invites it.' },
  '$10k–$50k/mo': { title: 'Lead with gross margin and net revenue retention, not top line.', body: 'At this level the range is set by the quality of the revenue rather than the size of it. Gross margin, NRR and payback are the three numbers that move it.' },
  '$50k–$150k/mo': { title: 'Bring CAC payback by channel.', body: 'At this revenue the objection is efficiency, not demand. Payback in months, split by channel, moves the range further than another month of growth does.' },
  '$150k+/mo': { title: 'Expect the range to be argued on multiples, not story.', body: 'Above this level the conversation moves to ARR multiples against recent comparable rounds. The defensible argument is why your growth and margin profile sits above the median for that comp set.' }
};

const FIX_BY_GROWTH = {
  'Early / pre-traction': { title: 'The team is currently the only asset being priced.', body: 'Pre-traction ranges are argued on founder-market fit and on what the first 90 days after close will prove. Both need to be explicit and dated, or the range defaults to the bottom of the band.' },
  'Steady, under 15%/mo': { title: 'This growth rate will be read as a market-size problem.', body: 'Steady growth invites the question of whether the ceiling is low. The answer is a segment-level breakdown showing where growth is constrained by your capacity rather than by demand.' },
  'Fast, 15%+/mo': { title: 'This growth is probably being attributed to one channel.', body: 'Fast growth gets discounted when it looks like a single acquisition channel that will saturate. Two channels with independent payback curves removes the discount.' }
};

const FIX_BY_PROFIT = {
  'Profitable': { title: 'Profitability at this stage invites a growth-ceiling question.', body: 'Investors read early profitability either as discipline or as under-investment. The defence is showing what happens to growth once the round is deployed, modelled rather than asserted.' },
  'Around break-even': { title: 'Break-even makes the raise itself the question.', body: 'If you do not need the money to survive, the round has to be justified by what it accelerates. Tie the raise to a specific milestone and to the timeline for reaching it without the money.' },
  'Burning, 12+ months runway': { title: 'Your burn multiple will be checked before your growth rate.', body: 'Net new revenue divided by net burn is the number that decides whether growth is being bought or earned. Bring it before you are asked for it.' },
  'Burning, under 12 months runway': { title: 'Your runway is shorter than the raise will take.', body: 'Under twelve months, the round gets priced against your deadline rather than your business. Either extend runway before opening the process or arrive with a bridge already committed. This is the single largest downward pressure on your range.' }
};

const RAISE_MIDPOINT = {
  'Under $500k': 0.35, '$500k–$1M': 0.75, '$1M–$2.5M': 1.75,
  '$2.5M–$5M': 3.75, '$5M–$10M': 7.5, 'Over $10M': 12
};

/* ---------------- analytics ---------------- */
function track(event, props) {
  const payload = Object.assign({ hook_variant: variant }, props || {});
  if (window.posthog && typeof window.posthog.capture === 'function') { window.posthog.capture(event, payload); }
  if (window.dataLayer) { window.dataLayer.push(Object.assign({ event: event }, payload)); }
  console.log('[fairway]', event, payload);
}

/* ---------------- hooks ---------------- */
const hooks = {
  frustration: {
    kicker: 'For founders raising in the next 90 days',
    headline: 'You know what your company is worth. The hard part is proving it in the room.',
    sub: 'Every investor pushes back on the number. Answer nine quick questions and get an indicative pre-money range, the specific concerns that will be raised against it, and the funds actively backing this profile. Checked by hand before it reaches you.',
    cta: 'Start the quiz'
  },
  readiness: {
    kicker: 'Before your next raise',
    headline: 'Are you actually ready to defend your valuation?',
    sub: 'Nine questions, four minutes. You get an indicative pre-money range, the three concerns investors will raise against it, and the funds writing cheques into your sector right now. Reviewed by former bulge bracket bankers.',
    cta: 'Find out in four minutes'
  },
  reveal: {
    kicker: 'The number problem',
    headline: 'Two founders with the same metrics raise at $2M and $4M.',
    sub: 'The difference is rarely the business. It is whether the number survives being pushed on. Nine questions gets you the range, the concerns coming at it, and a banker review of both.',
    cta: 'Show me my range'
  }
};

const params = new URLSearchParams(window.location.search);
const variant = hooks[params.get('hook')] ? params.get('hook') : 'frustration';

(function initHero() {
  const h = hooks[variant];
  const k = document.getElementById('hook-kicker');
  if (!k) return;
  k.textContent = h.kicker;
  document.getElementById('hook-headline').textContent = h.headline;
  document.getElementById('hook-sub').textContent = h.sub;
  document.getElementById('hook-cta').textContent = h.cta;
})();

/* marquee: duplicate the list so the loop is seamless */
function renderMarquee(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const firms = CONFIG.teamFirms.concat(CONFIG.teamFirms);
  el.innerHTML = firms.map(f => '<span>' + f + '</span>').join('');
}
renderMarquee('marquee-track');
renderMarquee('marquee-track-2');

/* ---------------- quiz ---------------- */
let currentStep = 1;
const totalSteps = 9;
const responses = { variant: variant, started_at: new Date().toISOString() };

function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  window.scrollTo(0, 0);
}

function startQuiz() { track('quiz_start', {}); showScreen('screen-quiz'); renderStep(); }
function backToStart() { track('back_to_start', { from_step: currentStep }); showScreen('screen-hero'); }

function renderStep() {
  document.querySelectorAll('.q-block').forEach(b => {
    b.style.display = (parseInt(b.dataset.step) === currentStep ? 'block' : 'none');
  });
  document.getElementById('step-label').textContent = 'Step ' + currentStep + ' of ' + totalSteps;
  document.getElementById('progress-fill').style.width = (currentStep / totalSteps * 100) + '%';
  document.getElementById('back-link').textContent = currentStep === 1 ? '← Back to start' : '← Back';
  track('quiz_step_view', { step: currentStep });
}

function answer(key, value) {
  responses[key] = value;
  track('quiz_answer', { step: currentStep, key: key, value: value });
  if (currentStep < totalSteps) { currentStep++; renderStep(); }
}

function goBack() {
  if (currentStep > 1) { currentStep--; renderStep(); }
  else { backToStart(); }
}

/* sector */
const sectorGrid = document.getElementById('sector-grid');
if (sectorGrid) {
  SECTORS.forEach(function (s) {
    const b = document.createElement('button');
    b.className = 'opt';
    b.textContent = s;
    b.onclick = function () {
      if (s === 'Other') {
        document.getElementById('sector-other-wrap').style.display = 'block';
        document.getElementById('sector-other').focus();
        track('sector_other_opened', {});
        return;
      }
      answer('sector', s);
    };
    sectorGrid.appendChild(b);
  });
}

function submitSectorOther() {
  const v = document.getElementById('sector-other').value.trim();
  responses.sector = 'Other';
  responses.sector_detail = v || null;
  track('quiz_answer', { step: 2, key: 'sector', value: 'Other', detail: v });
  currentStep = 3; renderStep();
}

/* ---------------- revenue, exact ----------------
   Bands are kept alongside the exact figure so the existing copy tables, investor lists
   and the reveal engine keep working unchanged. The exact number is what the football
   field runs on. */

function curSymbol() { return CURRENCY_SYMBOL[responses.currency || 'USD'] || ''; }

/* Log-ish slider so the bottom of the range, where most founders sit, has real resolution. */
function sliderToRevenue(s) {
  if (s <= 0) return 0;
  const raw = (Math.pow(1.0715, s) - 1) * 1000;
  if (raw < 10000) return Math.round(raw / 100) * 100;
  if (raw < 100000) return Math.round(raw / 500) * 500;
  return Math.round(raw / 1000) * 1000;
}
function revenueToSlider(v) {
  if (!v || v <= 0) return 0;
  return Math.max(0, Math.min(100, Math.round(Math.log(v / 1000 + 1) / Math.log(1.0715))));
}

function revenueBand(monthly) {
  if (!monthly || monthly <= 0) return 'Pre-revenue';
  if (monthly < 10000) return 'Under $10k/mo';
  if (monthly < 50000) return '$10k–$50k/mo';
  if (monthly < 150000) return '$50k–$150k/mo';
  return '$150k+/mo';
}

function growthBand(pct) {
  if (pct === null || pct === undefined) return 'Early / pre-traction';
  if (pct < 15) return 'Steady, under 15%/mo';
  return 'Fast, 15%+/mo';
}

function fmtPlain(n) {
  return curSymbol() + Math.round(n).toLocaleString('en-GB');
}

function paintRevenue(v, source) {
  responses.revenue_exact = v;
  responses.revenue = revenueBand(v);
  const read = document.getElementById('rev-read');
  const follow = document.getElementById('rev-followups');
  if (source !== 'type') document.getElementById('rev-exact').value = v || '';
  if (source !== 'slide') document.getElementById('rev-slider').value = revenueToSlider(v);
  if (v > 0) {
    read.innerHTML = '<strong>' + fmtPlain(v) + ' a month, about ' + fmtPlain(v * 12) +
      ' of ARR.</strong> <button type="button" class="link-btn" onclick="setPreRevenue()">We are pre-revenue</button>';
    follow.style.display = 'block';
  } else {
    read.innerHTML = 'Type the number or drag the slider. <button type="button" class="link-btn" onclick="setPreRevenue()">We are pre-revenue</button>';
    follow.style.display = 'none';
  }
}

function onRevType() {
  const v = parseFloat(document.getElementById('rev-exact').value);
  paintRevenue(isNaN(v) || v < 0 ? 0 : v, 'type');
}
function onRevSlide() {
  paintRevenue(sliderToRevenue(parseInt(document.getElementById('rev-slider').value, 10)), 'slide');
}
function setPreRevenue() {
  document.getElementById('rev-exact').value = '';
  paintRevenue(0, null);
  responses.recurring_pct = null;
  responses.revenue_model = null;
  track('quiz_answer', { step: 3, key: 'revenue', value: 'Pre-revenue' });
  currentStep = 4; renderStep();
}

/* Currency is guessed from the edge and then shown, at the revenue question and
   again beside the range, because nobody converts their own revenue into a
   currency the page picked for them. Both selectors stay in step. */
function setCurrency(code, source) {
  responses.currency = CURRENCY_SYMBOL[code] ? code : 'USD';
  ['rev-currency', 'range-currency'].forEach(function (id) {
    const el = document.getElementById(id);
    if (el) el.value = responses.currency;
  });
  const pfx = document.getElementById('ebitda-cur-prefix');
  if (pfx) pfx.textContent = curSymbol().trim() || responses.currency;
  if (source !== 'boot') track('currency_set', { currency: responses.currency, source: source });
}

function onCurrencyChange(el) {
  setCurrency(el.value, 'user');
  paintRevenue(responses.revenue_exact || 0, null);
  if (lastResult) renderResult(lastResult);
}
/* Kept so an older cached page does not break on the range selector. */
function onCurrency() {
  const el = document.getElementById('range-currency');
  if (el) onCurrencyChange(el);
}

(function bootCurrency() {
  /* Best guess from the browser first, so nothing is ever blank, then the edge
     header refines it. Falls back to USD and stays silent on failure. */
  const lang = (navigator.language || '').toUpperCase();
  const byLang = { GB: 'GBP', IE: 'EUR', DE: 'EUR', FR: 'EUR', ES: 'EUR', IT: 'EUR', NL: 'EUR',
    CH: 'CHF', SE: 'SEK', NO: 'NOK', DK: 'DKK', PL: 'PLN', CA: 'CAD', AU: 'AUD',
    SG: 'SGD', HK: 'HKD', JP: 'JPY', IN: 'INR', AE: 'AED', IL: 'ILS', ZA: 'ZAR', BR: 'BRL', MX: 'MXN' };
  setCurrency(byLang[lang.split('-')[1]] || 'USD', 'boot');
  fetch('/api/geo')
    .then(r => r.json())
    .then(function (g) {
      if (g && g.currency) { responses.country = g.country || null; setCurrency(g.currency, 'boot'); }
    })
    .catch(function () { /* keep the browser guess */ });
})();

function onRecurring() {
  const v = parseInt(document.getElementById('rec-slider').value, 10);
  responses.recurring_pct = v;
  document.getElementById('rec-read').textContent = v + '% recurring';
}

/* Revenue model is asked before the recurring share, because the model decides
   whether the recurring question is worth asking at all and what it should default to. */
const RECURRING_DEFAULT = {
  'Subscription / SaaS': 90, 'Usage or consumption': 70, 'Transaction fee / take rate': 20,
  'Marketplace commission': 20, 'One-off sales or licences': null, 'Services / retainer': 30,
  'Advertising': 30, 'Hardware plus software': 30, 'Interest / spread': 60, 'Other': 50
};

const modelWrap = document.getElementById('model-chips');
if (modelWrap) {
  REVENUE_MODELS.forEach(function (m) {
    const b = document.createElement('button');
    b.className = 'chip'; b.type = 'button'; b.textContent = m;
    b.onclick = function () {
      responses.revenue_model = m;
      modelWrap.querySelectorAll('.chip').forEach(c => c.classList.remove('on'));
      b.classList.add('on');
      applyModel(m);
    };
    modelWrap.appendChild(b);
  });
}

function applyModel(m) {
  const wrap = document.getElementById('rec-wrap');
  const def = RECURRING_DEFAULT[m];
  if (def === null) {
    /* One-off revenue has no meaningful recurring share, so we do not ask. */
    responses.recurring_pct = 0;
    wrap.style.display = 'none';
    return;
  }
  responses.recurring_pct = def;
  document.getElementById('rec-slider').value = def;
  document.getElementById('rec-read').textContent = def + '% recurring';
  wrap.style.display = 'block';
}

/* Band fallbacks, for anyone who would rather not give a figure. */
function showRevBands() {
  document.getElementById('rev-bands').style.display = 'grid';
  document.getElementById('rev-band-toggle').style.display = 'none';
}
function pickRevBand(band) {
  responses.revenue = band;
  responses.revenue_exact = null;
  document.getElementById('rev-followups').style.display = 'block';
  track('quiz_answer', { step: 3, key: 'revenue', value: band, exact: null, fallback: true });
}
function showGrowthBands() {
  document.getElementById('growth-bands').style.display = 'grid';
  document.getElementById('growth-band-toggle').style.display = 'none';
}
function pickGrowthBand(band) {
  responses.growth = band;
  responses.growth_exact = null;
  document.getElementById('growth-detail-wrap').style.display = 'block';
  track('quiz_answer', { step: 4, key: 'growth', value: band, exact: null, fallback: true });
}

function submitRevenue() {
  if (!responses.currency) responses.currency = 'USD';
  if (responses.revenue_exact === undefined) paintRevenue(0, null);
  if (responses.revenue_exact > 0 && responses.recurring_pct === undefined) responses.recurring_pct = 50;
  track('quiz_answer', {
    step: 3, key: 'revenue', value: responses.revenue,
    exact: responses.revenue_exact, currency: responses.currency,
    recurring_pct: responses.recurring_pct, revenue_model: responses.revenue_model || null
  });
  currentStep = 4; renderStep();
}

/* ---------------- growth, exact ---------------- */

function paintGrowth(pct, source) {
  responses.growth_exact = pct;
  responses.growth = growthBand(pct);
  if (source !== 'type') document.getElementById('growth-exact').value = pct;
  if (source !== 'slide') document.getElementById('growth-slider').value = pct;
  const annual = (Math.pow(1 + pct / 100, 12) - 1) * 100;
  document.getElementById('growth-read').innerHTML =
    '<strong>' + pct + '% a month.</strong> <button type="button" class="link-btn" onclick="setPreTraction()">Too early to measure</button>';
  document.getElementById('growth-annual').textContent = pct > 0
    ? 'Held for twelve months that compounds to about ' + Math.round(annual) + '% a year, which is the figure the multiple is read against.'
    : (pct < 0 ? 'Revenue is contracting. That is priced, and the report is where it gets explained rather than hidden.' : '');
  document.getElementById('growth-detail-wrap').style.display = 'block';
}

function onGrowthType() {
  const v = parseFloat(document.getElementById('growth-exact').value);
  if (isNaN(v)) return;
  paintGrowth(Math.max(-50, Math.min(100, v)), 'type');
}
function onGrowthSlide() {
  paintGrowth(parseFloat(document.getElementById('growth-slider').value), 'slide');
}
function setPreTraction() {
  responses.growth_exact = null;
  responses.growth = 'Early / pre-traction';
  document.getElementById('growth-exact').value = '';
  document.getElementById('growth-annual').textContent = '';
  document.getElementById('growth-read').innerHTML =
    '<strong>Too early to measure.</strong> <button type="button" class="link-btn" onclick="onGrowthSlide()">Enter a rate instead</button>';
  document.getElementById('growth-detail-wrap').style.display = 'block';
}

function submitGrowth() {
  if (!responses.growth) responses.growth = 'Early / pre-traction';
  responses.growth_detail = document.getElementById('growth-detail').value.trim() || null;
  track('quiz_answer', {
    step: 4, key: 'growth', value: responses.growth,
    exact: responses.growth_exact, has_detail: !!responses.growth_detail
  });
  currentStep = 5; renderStep();
}

/* concerns, multi-select */
const chipWrap = document.getElementById('concern-chips');
const chosenConcerns = new Set();
if (chipWrap) {
  CONCERNS.forEach(function (c) {
    const b = document.createElement('button');
    b.className = 'chip';
    b.type = 'button';
    b.textContent = c;
    b.onclick = function () {
      if (chosenConcerns.has(c)) { chosenConcerns.delete(c); b.classList.remove('on'); }
      else { chosenConcerns.add(c); b.classList.add('on'); }
    };
    chipWrap.appendChild(b);
  });
}

function submitConcerns(skipped) {
  responses.concerns = skipped ? [] : Array.from(chosenConcerns);
  responses.concern_notes = skipped ? null : (document.getElementById('concern-notes').value.trim() || null);
  responses.context_link = skipped ? null : (document.getElementById('ctx-link').value.trim() || null);
  track('concerns_step', {
    skipped: !!skipped, count: responses.concerns.length,
    has_notes: !!responses.concern_notes, has_link: !!responses.context_link
  });
  currentStep = 9; renderStep();
}

/* contact */
function validEmail(v) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v); }

async function submitLead() {
  const email = document.getElementById('lead-email').value.trim();
  const err = document.getElementById('submit-error');
  if (!validEmail(email)) { err.style.display = 'block'; return; }
  err.style.display = 'none';

  responses.email = email;
  responses.company = document.getElementById('lead-company').value.trim() || null;
  responses.phone = document.getElementById('lead-phone').value.trim() || null;

  const btn = document.getElementById('final-submit');
  btn.disabled = true; btn.textContent = 'Saving';

  const result = computeResult();
  try {
    await fetch(CONFIG.leadEndpoint, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(Object.assign({}, responses, { computed: result }))
    });
    track('lead_captured', {});
  } catch (e) {
    console.error('[fairway] lead post failed', e);
    track('lead_post_failed', {});
  }
  renderResult(result);
  btn.disabled = false; btn.textContent = 'Show me my range';
}

/* ---------------- optional enrichment on the result screen ----------------
   Everything here is optional, free and ungated. Each field removes a reason the
   range is wide, and the narrowing happens in front of the founder rather than
   being promised in an email. */

let lastResult = null;

function onGrossMargin() {
  const v = parseInt(document.getElementById('gm-slider').value, 10);
  responses.gross_margin = v;
  document.getElementById('gm-read').textContent = v + '%';
}

function onLastRound() {
  const amount = parseFloat(document.getElementById('lr-amount').value);
  const value = parseFloat(document.getElementById('lr-value').value);
  responses.last_round_amount = isNaN(amount) ? null : amount;
  responses.last_round_value = isNaN(value) ? null : value;
  responses.last_round_type = document.getElementById('lr-type').value || null;
  responses.last_round_date = document.getElementById('lr-date').value || null;
}

/* Months between a YYYY-MM string and today. Returns null if unusable. */
function monthsSince(ym) {
  if (!ym || !/^\d{4}-\d{2}$/.test(ym)) return null;
  const parts = ym.split('-');
  const then = new Date(Number(parts[0]), Number(parts[1]) - 1, 1);
  const now = new Date();
  const m = (now.getFullYear() - then.getFullYear()) * 12 + (now.getMonth() - then.getMonth());
  return m >= 0 && m < 120 ? m : null;
}

async function applyNarrowing() {
  /* The margin slider always has a value, so it must only count once the founder has
     actually moved it. onGrossMargin fires on input and nowhere else, deliberately.
     The other two read empty fields as null, so they are safe to call here. */
  onLastRound(); onEbitda();
  const btn = document.getElementById('narrow-btn');
  btn.disabled = true; btn.textContent = 'Recalculating';

  const before = lastResult;
  const after = computeResult();
  lastResult = after;

  const foot = document.getElementById('narrow-foot');
  /* Width measured relative to the mid-point, because that is what precision means
     here. An absolute spread can widen while the answer gets more precise, simply
     because the mid-point moved. */
  const relBefore = before ? (before.high - before.low) / before.mid : null;
  const relAfter = (after.high - after.low) / after.mid;
  const tighter = relBefore ? Math.round((1 - relAfter / relBefore) * 100) : 0;
  if (before) {
    foot.textContent = 'Was ' + money(before.low) + ' to ' + money(before.high) +
      '. Now ' + money(after.low) + ' to ' + money(after.high) +
      (tighter > 0 ? ', and the range is ' + tighter + '% tighter relative to its mid-point.' : '.') +
      ' What you added goes to the reviewer, so the email you get back is built on it too.';
  } else {
    foot.textContent = 'Added and sent to the reviewer.';
  }

  try {
    await fetch(CONFIG.leadEndpoint, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(Object.assign({}, responses, { type: 'enrichment', computed: after }))
    });
    track('narrowing_applied', {
      has_margin: responses.gross_margin != null,
      has_last_round: responses.last_round_value != null,
      has_ebitda: responses.ebitda_ltm != null,
      narrowed: tighter > 0
    });
  } catch (e) {
    console.error('[fairway] enrichment post failed', e);
  }

  renderResult(after);
  btn.disabled = false; btn.textContent = 'Update my range';
  document.getElementById('narrow-card').scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function onEbitda() {
  const v = parseFloat(document.getElementById('ebitda-ltm').value);
  responses.ebitda_ltm = isNaN(v) ? null : v;
  const help = document.getElementById('ebitda-help');
  if (!help) return;
  if (responses.ebitda_ltm !== null && responses.ebitda_ltm <= 0) {
    help.textContent = 'Negative or zero EBITDA means an EBITDA multiple does not apply, and no honest field would draw the line. It still goes to the reviewer, because burn against growth is its own argument.';
  } else if (responses.ebitda_ltm > 0) {
    help.textContent = 'Positive EBITDA gives you a second independent lens, and investors will run it whether or not you do. It does not change the free range above. The line and its peer set are in the report.';
  }
}

/* ---------------- result ---------------- */
/* First-pass range only. Deliberately coarse, and replaced on screen by the engine
   when it returns a sourced range. Continuous in ARR so that two founders £1 apart do
   not get different answers, which is what the old bands did. */
function firstPassRevenueValue(arrM) {
  if (arrM <= 0) return 0;
  const pts = [[0, 0], [0.06, 0.4], [0.36, 1.2], [1.2, 3], [2.4, 6], [6, 13]];
  for (let i = 1; i < pts.length; i++) {
    if (arrM <= pts[i][0]) {
      const a = pts[i - 1], b = pts[i];
      return a[1] + (b[1] - a[1]) * (arrM - a[0]) / (b[0] - a[0]);
    }
  }
  return arrM * 2.2;
}

function computeResult() {
  const stageBase = { 'Pre-seed': 1.5, 'Seed': 3.5, 'Series A': 9 }[responses.stage] || 2;

  const monthly = responses.revenue_exact || 0;
  const arrM = monthly * 12 / 1e6;
  const revenueBump = monthly > 0
    ? firstPassRevenueValue(arrM)
    : ({ 'Pre-revenue': 0, 'Under $10k/mo': 0.4, '$10k–$50k/mo': 1.2, '$50k–$150k/mo': 3, '$150k+/mo': 6 }[responses.revenue] || 0);

  const g = responses.growth_exact;
  const growthMult = (g === null || g === undefined)
    ? ({ 'Early / pre-traction': 1, 'Steady, under 15%/mo': 1.15, 'Fast, 15%+/mo': 1.4 }[responses.growth] || 1)
    : 1 + Math.min(0.55, Math.max(-0.15, g / 100 * 1.6));

  /* Recurring share is applied once, here, rather than also inside the revenue model,
     so the two do not compound into a discount nobody can trace. */
  const rec = responses.recurring_pct;
  const recurringMult = (monthly > 0 && rec !== null && rec !== undefined)
    ? 0.7 + 0.4 * (rec / 100)
    : 1;

  const profitMult = { 'Profitable': 1.15, 'Around break-even': 1.05, 'Burning, 12+ months runway': 1, 'Burning, under 12 months runway': 0.9 }[responses.profit] || 1;

  /* Gross margin decides which multiple set you belong to at all. Combined with the
     recurring share it is floored, so two related discounts cannot compound into a
     haircut nobody can trace back to a cause. */
  const gm = responses.gross_margin;
  const marginMult = (gm === null || gm === undefined) ? 1
    : (gm < 50 ? 0.75 + 0.005 * gm : Math.min(1.18, 1 + 0.004 * (gm - 50)));
  const qualityMult = Math.max(0.6, recurringMult * marginMult);

  const base = (stageBase + revenueBump) * growthMult * qualityMult * profitMult;

  /* Each thing we know removes a reason to be wide. Stated here rather than tuned
     invisibly, because the width is the number founders actually complain about. */
  let spreadLow = 0.85, spreadHigh = 1.55;
  if (gm !== null && gm !== undefined) { spreadLow = 0.88; spreadHigh = 1.45; }

  let mid = base;

  /* The last round is a MARKER, not an input. It is plotted as a point on the field so
     the founder can see where they were priced against where the methods land, and it
     touches no calculation anywhere. Carrying it forward and blending it would be us
     deciding the answer from the last answer, which is the thing a football field
     exists to avoid. */
  const lrValue = responses.last_round_value;
  const markerM = lrValue > 0 ? lrValue / 1e6 : null;
  const months = monthsSince(responses.last_round_date);

  const low = mid * spreadLow;
  const high = mid * spreadHigh;
  const raise = RAISE_MIDPOINT[responses.raise] || 1.0;
  mid = (low + high) / 2;
  const dilLow = raise / (low + raise) * 100;
  const dilHigh = raise / (high + raise) * 100;

  return {
    low: low, high: high, mid: mid, raise: raise,
    dilLow: dilLow, dilHigh: dilHigh,
    dilMid: raise / (mid + raise) * 100,
    /* Computed here rather than in renderResult so that it reaches the leads sheet.
       Illustration on a doubling assumption, not a forecast. */
    futureValue: ((dilLow - dilHigh) / 100) * CONFIG.valuationGrowth12m * (mid + raise),
    /* Surfaced so the copy can say what the range is standing on. */
    usedMargin: gm !== null && gm !== undefined,
    /* Marker only. Never read by any calculation above. */
    markerM: markerM,
    monthsSinceRound: months,
    /* EBITDA multiple is a locked row, and only exists when the founder gave a
       positive figure. It does not touch the free ranges. */
    ebitdaM: (responses.ebitda_ltm > 0) ? responses.ebitda_ltm / 1e6 : null
  };
}

function money(m) {
  const c = curSymbol();
  if (m >= 1) return c + m.toFixed(1) + 'M';
  return c + Math.round(m * 1000) + 'k';
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

function setItem(prefix, title, body, locked) {
  document.getElementById(prefix + '-title').innerHTML =
    locked ? escapeHtml(title) + '<span class="lock-tag">Locked</span>' : escapeHtml(title);
  document.getElementById(prefix + '-body').textContent = body;
}

function renderResult(r) {
  lastResult = r;
  const sectorLabel = responses.sector === 'Other'
    ? (responses.sector_detail || 'your sector')
    : (responses.sector || 'your sector');

  document.getElementById('range-output').textContent = money(r.low) + ' – ' + money(r.high);
  document.getElementById('range-stage-sector').textContent = (responses.stage || 'your stage') + ' · ' + sectorLabel;

  const note = document.getElementById('range-note');
  if (note) {
    const bits = [];
    if (r.usedMargin) bits.push('Gross margin is in this range.');
    if (r.markerM) {
      /* The marker is a comparison, never an input, so the copy compares rather than
         explains. What it says is the whole point of plotting it. */
      bits.push(r.high < r.markerM
        ? 'Your last round sits above the whole of this range, so on these inputs you would be pricing a down round. Better to know now than in the meeting.'
        : (r.low > r.markerM
          ? 'Your last round sits below this range, which is the up round you are arguing for. The report is where that argument gets evidenced.'
          : 'Your last round sits inside this range, so you are arguing for a flat to modest up round unless something has changed that these inputs cannot see.'));
    }
    if (!bits.length) bits.push('First pass. Every method behind it is set out below, with its sources.');
    note.textContent = bits.join(' ');
  }

  renderField(r);

  const points = r.dilLow - r.dilHigh;
  const spread = r.high - r.low;
  const futureValue = r.futureValue;

  document.getElementById('gap-headline').textContent =
    'That spread is about ' + points.toFixed(0) + ' points of your company.';
  document.getElementById('gap-body').textContent =
    'On a ' + money(r.raise) + ' raise, the bottom of that range costs you ' + r.dilLow.toFixed(1) +
    '% of the company and the top costs ' + r.dilHigh.toFixed(1) +
    '%. Nothing about the business changes between those two numbers, only whether you can defend the higher one.';
  document.getElementById('gap-future').innerHTML =
    '<strong>In cash terms: if the company is worth twice this valuation in twelve months, those ' +
    points.toFixed(0) + ' points are worth about ' + money(futureValue) +
    '.</strong> That is an illustration on a doubling assumption, not a forecast, and it is the reason the number is worth an argument.';

  renderDrivers();

  const f1 = FIX_BY_REVENUE[responses.revenue] || FIX_BY_REVENUE['Pre-revenue'];
  const f2 = FIX_BY_GROWTH[responses.growth] || FIX_BY_GROWTH['Early / pre-traction'];
  const f3 = FIX_BY_PROFIT[responses.profit] || FIX_BY_PROFIT['Burning, 12+ months runway'];
  setItem('fix-1', f1.title, f1.body, false);
  setItem('fix-2', f2.title, f2.body, true);
  setItem('fix-3', f3.title, f3.body, true);

  const named = (responses.concerns || []).filter(c => c !== 'Nothing specific yet');
  if (named.length || responses.concern_notes || responses.context_link) {
    const el = document.getElementById('concern-echo');
    el.style.display = 'block';
    el.textContent = named.length
      ? 'You told us investors are pushing on ' + named.join(', ').toLowerCase() + '. That goes to the reviewer with your range, and the report answers those directly alongside the three below.'
      : 'Your notes are with the reviewer and will shape the range you get back by email.';
    document.getElementById('fix-foot').textContent =
      'These are pattern-level. The report replaces them with concerns drawn from your own numbers.';
  }

  const list = INVESTORS[responses.sector] || INVESTORS['Other'];
  document.getElementById('inv-heading').textContent =
    'Three funds active in ' + sectorLabel + ' at ' + (responses.stage || 'your stage');
  document.getElementById('inv-1-name').textContent = list[0].name;
  document.getElementById('inv-1-body').textContent = list[0].note;

  document.getElementById('price-anchor').textContent =
    'One point of a ' + money(r.mid) + ' company is worth about ' + curSymbol() + Math.round(r.mid * 10000).toLocaleString() + '.';

  track('result_view', {
    low: +r.low.toFixed(2), high: +r.high.toFixed(2), spread: +spread.toFixed(2),
    dilution_points: +points.toFixed(1), future_value_m: +futureValue.toFixed(2),
    sector: responses.sector || null, profit: responses.profit || null,
    timing: responses.timing || null, concerns: (responses.concerns || []).length
  });
  showScreen('screen-result');
}

/* ---------------- price and CTA wiring ---------------- */
(function initOffer() {
  const cap = document.getElementById('capacity-line');
  if (!cap) return;
  cap.textContent = 'Every report is reviewed by hand. ' + CONFIG.spotsPerWeek + ' a week, ' + CONFIG.spotsLeft + ' left this week.';
  document.getElementById('price-figure').innerHTML = '$' + CONFIG.price + '<span> one-time</span>';

  const unlockCta = document.getElementById('unlock-cta');
  unlockCta.textContent = 'Unlock my full report, $' + CONFIG.price;
  unlockCta.addEventListener('click', function (e) {
    track('unlock_click', { price: CONFIG.price, placement: 'box' });
    if (!CONFIG.stripeLink) { e.preventDefault(); console.warn('[fairway] CONFIG.stripeLink is not set'); return; }
    unlockCta.href = CONFIG.stripeLink;
  });

  const bar = document.getElementById('cta-bar-link');
  bar.textContent = 'Full report, $' + CONFIG.price;
  bar.addEventListener('click', function () { track('unlock_click', { price: CONFIG.price, placement: 'bar' }); });
})();

track('page_view', { utm_source: params.get('utm_source') || null });
