/* Fairway landing funnel. Config first, then data, then flow. */

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
  'Telecoms / Connectivity', 'Professional services', 'Other'
];

/* How the revenue is earned. Single select. This changes which multiple set applies
   more than sector does in several cases, which is why it is asked separately. */
const REVENUE_MODELS = [
  'Subscription / SaaS', 'Usage or consumption', 'Transaction fee / take rate',
  'Marketplace commission', 'One-off sales or licences', 'Services / retainer',
  'Advertising', 'Hardware plus software', 'Interest / spread', 'Other'
];

/* Display only. All maths runs in the founder's own currency, because a multiple is a
   ratio and does not need converting. The only cross-currency comparison is against the
   US market anchors, and that is stated in the copy rather than silently converted. */
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

/* ---------------- what actually moves the multiple, by sector ----------------
   One entry per sector. `pays` is what that market rewards, `cuts` is what compresses
   the multiple there, `metric` is the number investors index on before anything else.
   Written to be specific enough that a founder in the sector recognises it. */
const SECTOR_DRIVERS = {
  'SaaS / B2B software': { metric: 'Net revenue retention', pays: 'Net revenue retention above 110% is what separates a software multiple from a services one, because it means the installed base grows without new sales.', cuts: 'Logo churn above 2% a month caps the multiple regardless of new business, since it implies the revenue has to be re-won every three years.' },
  'AI / ML': { metric: 'Gross margin after inference cost', pays: 'Proprietary data or a workflow the model is embedded in, rather than the model itself, because the model is the part that commoditises fastest.', cuts: 'Inference cost inside cost of sales. AI companies routinely report 40% to 60% gross margins where buyers price 75%+, and that gap is applied straight to the multiple.' },
  'Fintech': { metric: 'Revenue net of interchange and funding cost', pays: 'Net revenue after partner and interchange costs, plus a regulatory permission that takes a competitor two years to obtain.', cuts: 'Gross transaction value quoted as revenue. Investors restate it, and the restated multiple is what gets discussed.' },
  'Insurtech': { metric: 'Loss ratio and commission share', pays: 'Distribution economics with a stable loss ratio, or an MGA model where you keep commission without carrying underwriting risk.', cuts: 'Any balance sheet risk. Carrying underwriting moves you from a software multiple to an insurance one, which is a different order of magnitude.' },
  'Healthtech / Digital health': { metric: 'Contracted lives or sites, and reimbursement route', pays: 'A live reimbursement pathway and multi-year contracts with providers or payers, because both make the revenue predictable through a long sales cycle.', cuts: 'Pilot revenue counted as recurring. Pilots that have not converted are valued as pipeline, not as ARR.' },
  'Biotech / Life sciences': { metric: 'Programme stage and IP position', pays: 'Programmes past a de-risking milestone, with composition of matter protection and a credible route to partnering.', cuts: 'Revenue multiples do not apply here at all. Value is priced on risk-adjusted programme value, so the football field is built on precedent rounds and licensing deals instead.' },
  'Medtech / Devices': { metric: 'Regulatory clearance and reimbursement code', pays: 'Clearance already in hand and a reimbursement code, since together they convert a science risk into a commercial one.', cuts: 'Hardware gross margin. Device margins sit well below software and the multiple follows the margin.' },
  'Consumer / D2C': { metric: 'Contribution margin after CAC, and repeat rate', pays: 'Repeat purchase inside 90 days and contribution margin that survives paid acquisition, because that is what makes growth self-funding.', cuts: 'Revenue bought with paid media. Consumer businesses are priced on contribution margin, and a large paid mix pulls the multiple towards retail rather than tech.' },
  'E-commerce / Retail': { metric: 'Contribution margin and inventory turns', pays: 'Own brand with pricing power, high repeat rate and inventory that turns quickly enough not to consume the raise.', cuts: 'Reselling third-party product. Thin gross margin puts you on a retail multiple, typically well under 2x revenue.' },
  'Marketplaces': { metric: 'Net revenue, take rate and liquidity', pays: 'Take rate holding as volume grows, plus repeat activity on both sides, which is the evidence that the marketplace and not the subsidy is doing the work.', cuts: 'Quoting GMV. Investors price net revenue, and a founder who leads with GMV usually gets a lower number than one who leads with take rate.' },
  'Climate / Energy': { metric: 'Contracted offtake and unit economics without subsidy', pays: 'Signed offtake agreements and economics that work at unsubsidised prices, because subsidy risk is what buyers discount hardest.', cuts: 'Project-heavy capital intensity, which shifts pricing towards infrastructure returns rather than software multiples.' },
  'Deeptech / Hardware': { metric: 'Technology readiness level and first commercial contract', pays: 'A first paid commercial deployment and defensible IP, since together they mark the transition from grant funding to a priced business.', cuts: 'Time to revenue. Long development timelines are discounted for the capital needed to reach the next milestone.' },
  'Cybersecurity': { metric: 'Net revenue retention and displacement rate', pays: 'Displacing an incumbent tool rather than adding to the stack, plus expansion inside existing accounts.', cuts: 'A crowded category with a large incumbent. Buyers assume the incumbent ships a good-enough feature and discount accordingly.' },
  'Logistics / Supply chain': { metric: 'Revenue quality: software fee versus freight margin', pays: 'A software or data fee separated cleanly from freight, since that part earns a software multiple and the rest does not.', cuts: 'Blended revenue. Mixing freight and software gets you the lower multiple applied to everything until it is separated.' },
  'Proptech': { metric: 'Recurring share and transaction dependence', pays: 'Revenue tied to a recurring service or a software fee rather than to transaction volume in a cyclical market.', cuts: 'Dependence on transaction volumes, which are priced with a cycle discount because the market can halve.' },
  'Edtech': { metric: 'Retention past the first cohort and B2B mix', pays: 'Institutional or employer contracts that renew, which is what moves you off consumer churn rates.', cuts: 'Consumer subscription churn. High first-90-day churn caps the multiple whatever the growth rate is.' },
  'Legaltech / Regtech': { metric: 'Seats or matters under contract, and renewal rate', pays: 'Multi-year enterprise contracts and a compliance mandate that makes the spend non-discretionary.', cuts: 'Long procurement cycles at law firms and banks, which lengthen payback and are discounted for it.' },
  'HR tech / Future of work': { metric: 'Net revenue retention against headcount changes', pays: 'Pricing that is not purely per-seat, so that revenue does not fall when a customer freezes hiring.', cuts: 'Seat-based pricing in a soft hiring market, where net retention drops below 100% without a single logo lost.' },
  'Adtech / Martech': { metric: 'Net revenue and platform dependence', pays: 'Direct relationships with advertisers and revenue that does not sit inside one platform.', cuts: 'Gross billings quoted as revenue, and dependence on a single platform whose policy change can remove the business.' },
  'Media / Content': { metric: 'Owned audience and revenue per user', pays: 'A first-party audience and diversified revenue, since owned distribution is the asset being bought.', cuts: 'Advertising cyclicality and algorithm dependence, both of which are discounted heavily at seed.' },
  'Gaming': { metric: 'D30 retention and lifetime value against CAC', pays: 'Retention curves that flatten, plus a live-ops cadence that lifts revenue per user over time.', cuts: 'Hit-driven revenue concentration in one title, which is priced as a single-product risk.' },
  'Travel / Hospitality': { metric: 'Net revenue and repeat booking rate', pays: 'Repeat bookings and direct relationships rather than paid intermediated demand.', cuts: 'Seasonality and cyclicality, which widen the range and pull the mid-point down.' },
  'Food / Beverage': { metric: 'Gross margin and velocity per point of distribution', pays: 'Rate of sale in existing doors, which is what a retailer and an investor both look at first.', cuts: 'Physical gross margin and working capital. This is priced on consumer packaged goods multiples, usually a small multiple of revenue.' },
  'Agritech': { metric: 'Contracted acreage or output, and season-over-season retention', pays: 'Multi-season contracts and measurable yield or cost improvement per hectare.', cuts: 'Single-season sales cycles, which mean one bad season resets the growth rate.' },
  'Web3 / Digital assets': { metric: 'Protocol or platform revenue excluding token effects', pays: 'Real fee revenue that would exist without token incentives.', cuts: 'Token-driven activity and regulatory uncertainty, which together produce the widest ranges of any sector we see.' },
  'Defence / Gov tech': { metric: 'Contract vehicle and framework position', pays: 'A place on a framework or an incumbent programme, since that is what converts a long sales cycle into predictable revenue.', cuts: 'Budget cycle timing and procurement length, which stretch payback well beyond commercial norms.' },
  'Telecoms / Connectivity': { metric: 'ARPU, churn and capital intensity', pays: 'Low churn on a contracted base, and asset-light delivery.', cuts: 'Network capital expenditure, which moves the pricing towards infrastructure multiples on EBITDA rather than revenue.' },
  'Professional services': { metric: 'Utilisation, and revenue per head', pays: 'Productised delivery or a recurring retainer, which is the only route to a multiple above the services range.', cuts: 'Revenue that scales with headcount. This is priced on a small multiple of profit, not of revenue, and no growth rate changes that.' },
  'Other': { metric: 'Recurring share and gross margin', pays: 'Contracted, repeatable revenue at software-like gross margin.', cuts: 'Revenue that has to be re-won each period, which is priced on profit rather than on revenue.' }
};

/* Where the multiple set is not revenue-based at all. Used to change the copy honestly
   rather than showing a revenue multiple that no investor in that sector would use. */
const NON_REVENUE_SECTORS = ['Biotech / Life sciences', 'Medtech / Devices'];

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
function onCurrency() {
  responses.currency = document.getElementById('rev-currency').value;
  paintRevenue(responses.revenue_exact || 0, null);
  track('currency_set', { currency: responses.currency });
}
function onRecurring() {
  const v = parseInt(document.getElementById('rec-slider').value, 10);
  responses.recurring_pct = v;
  document.getElementById('rec-read').textContent = v + '% recurring';
}

/* revenue model chips, single select */
const modelWrap = document.getElementById('model-chips');
if (modelWrap) {
  REVENUE_MODELS.forEach(function (m) {
    const b = document.createElement('button');
    b.className = 'chip'; b.type = 'button'; b.textContent = m;
    b.onclick = function () {
      responses.revenue_model = m;
      modelWrap.querySelectorAll('.chip').forEach(c => c.classList.remove('on'));
      b.classList.add('on');
    };
    modelWrap.appendChild(b);
  });
}

function submitRevenue() {
  if (!responses.currency) responses.currency = document.getElementById('rev-currency').value || 'USD';
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

  const base = (stageBase + revenueBump) * growthMult * recurringMult * profitMult;
  const low = base * 0.85;
  const high = base * 1.55;
  const raise = RAISE_MIDPOINT[responses.raise] || 1.0;
  const mid = (low + high) / 2;
  const dilLow = raise / (low + raise) * 100;
  const dilHigh = raise / (high + raise) * 100;

  return {
    low: low, high: high, mid: mid, raise: raise,
    dilLow: dilLow, dilHigh: dilHigh,
    dilMid: raise / (mid + raise) * 100,
    /* Computed here rather than in renderResult so that it reaches the leads sheet.
       Illustration on a doubling assumption, not a forecast. */
    futureValue: ((dilLow - dilHigh) / 100) * CONFIG.valuationGrowth12m * (mid + raise)
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


/* ---------------- what moves your valuation, tailored ----------------
   Built from sector, stage, size, growth, recurring share and revenue model. Nothing in
   here is a fixed paragraph: every driver either quotes the founder's own number back or
   is drawn from the sector table. If we cannot tailor a driver, we do not show it. */

const MODEL_NOTE = {
  'Subscription / SaaS': 'On a subscription model the argument is won on net revenue retention. Gross retention tells an investor whether the base holds; net tells them whether it grows on its own.',
  'Usage or consumption': 'Usage pricing has no floor, so investors discount for the month a large customer runs less. A committed minimum on your largest accounts removes most of that discount.',
  'Transaction fee / take rate': 'Transaction revenue is priced on whether the take rate holds as volume grows. If it has compressed, show why, before someone assumes it will keep compressing.',
  'Marketplace commission': 'Lead with net revenue, not GMV. Investors restate GMV to net revenue in their own model anyway, and the founder who quotes GMV usually ends up defending a lower number than the one who quoted take rate.',
  'One-off sales or licences': 'One-off revenue has to be re-won every period, so it is valued closer to a services multiple. Any maintenance, support or renewal component should be separated out and shown on its own line.',
  'Services / retainer': 'Services revenue scales with headcount, which is why it is priced on a multiple of profit rather than of revenue. The route to a higher multiple is productising a repeatable part of the delivery.',
  'Advertising': 'Advertising revenue is cyclical and usually concentrated. Show the share coming from your largest three advertisers before you are asked for it.',
  'Hardware plus software': 'Split hardware from software revenue explicitly. Blended, the whole thing gets the hardware multiple; split, the software line can carry its own.',
  'Interest / spread': 'Spread revenue is rate sensitive, so investors will want to see the range at a lower rate environment. Model it rather than waiting for the question.',
  'Other': 'The first thing an investor will do is work out how much of this revenue repeats without a new sale. Answer it before they ask.'
};

function stageNote(stage, arrM) {
  if (stage === 'Series A') {
    return 'At Series A the range is argued on multiples against recent comparable rounds, and the burden of proof sits on why your growth and margin profile deserves to sit above the median of that comp set.';
  }
  if (stage === 'Seed') {
    return arrM >= 0.5
      ? 'At seed with real revenue you are in the narrow band where a multiple can actually be applied. That is an advantage, because a sourced multiple is far easier to defend than a story.'
      : 'At seed with limited revenue, price is usually set by the intersection of the round size and the lead fund ownership target rather than by any multiple. Knowing that target before the meeting is worth more than another slide.';
  }
  return 'At pre-seed there is no published median to anchor against, which is why ranges at this stage are wide. What narrows them is evidence of demand with a date and a price attached to it.';
}

function sizeNote(arrM) {
  if (arrM <= 0) return null;
  if (arrM < 0.25) {
    return { title: 'Size, and why the discount is large here', body: 'At roughly ' + Math.round(arrM * 1000) + 'k of ARR, a listed peer multiple cannot be applied without a substantial size and illiquidity discount. The report states that discount as a number with a reason, rather than burying it inside the range.' };
  }
  if (arrM < 1) {
    return { title: 'Size, and the discount that comes with it', body: 'At about ' + arrM.toFixed(2).replace(/0$/, '') + 'M of ARR you are below the level where a comparable round set gets dense, so the range stays wider than it will be at 1M. The discount to listed peers is still material and should be shown, not assumed.' };
  }
  return { title: 'Size, and where the argument moves next', body: 'Above 1M of ARR the conversation stops being about the story and starts being about which comparable set you belong in. Getting into the right comp set is worth more than any single metric, because it resets the multiple before anything else is discussed.' };
}

function buildDrivers() {
  const out = [];
  const sector = responses.sector === 'Other' ? 'Other' : (responses.sector || 'Other');
  const sd = SECTOR_DRIVERS[sector] || SECTOR_DRIVERS['Other'];
  const monthly = responses.revenue_exact || 0;
  const arrM = monthly * 12 / 1e6;
  const g = responses.growth_exact;
  const rec = responses.recurring_pct;
  const nonRev = NON_REVENUE_SECTORS.indexOf(sector) !== -1;

  /* 1. growth, or proof of demand when there is nothing to multiply */
  if (monthly > 0 && g !== null && g !== undefined && g !== 0) {
    const annual = Math.round((Math.pow(1 + g / 100, 12) - 1) * 100);
    out.push({
      title: 'Growth at ' + g + '% a month is the largest single lever you have',
      body: 'That compounds to roughly ' + annual + '% a year. Revenue multiples are not flat, they are fitted against growth, so this is the input the range is most sensitive to. ' +
        (g >= 15
          ? 'At this rate the risk is not the number, it is that a single acquisition channel is doing all of it. Two channels with independent payback curves removes the discount that assumption creates.'
          : 'At this rate expect the market-size question. The answer is a segment-level view showing growth constrained by your own capacity rather than by demand.')
    });
  } else {
    out.push({
      title: 'With no revenue to multiply, demand evidence is the range',
      body: 'Pre-revenue ranges are argued on proof that someone will pay, not on product. Three named design partners with a start date and a price moves the number further than any traction slide, because it converts an opinion into a dated commitment.'
    });
  }

  /* 2. revenue quality, from the recurring share and the model */
  if (monthly > 0 && rec !== null && rec !== undefined) {
    let lead;
    if (rec >= 80) {
      lead = rec + '% of your revenue recurs without a new sale. That is what puts you in the software multiple set rather than the services one, and the gap between those two sets is usually wider than any other single factor on this page.';
    } else if (rec >= 40) {
      lead = rec + '% of your revenue recurs and the rest has to be re-won each period. Investors will value the two parts separately, so present them separately. Blended, the lower multiple tends to get applied to the whole.';
    } else {
      lead = 'Only ' + rec + '% of your revenue recurs. Expect the non-recurring part to be priced closer to a services multiple, which is typically a small multiple of revenue rather than a software one. Moving this number is the highest-value change available to you.';
    }
    const note = MODEL_NOTE[responses.revenue_model] || MODEL_NOTE['Other'];
    out.push({ title: 'Revenue quality, not revenue size', body: lead + ' ' + note });
  }

  /* 3. the sector, from the table */
  out.push({
    title: 'In ' + (responses.sector === 'Other' ? (responses.sector_detail || 'your sector') : sector) + ', the number they index on is ' + sd.metric.toLowerCase(),
    body: sd.pays + ' The other side of it: ' + sd.cuts.charAt(0).toLowerCase() + sd.cuts.slice(1)
  });

  /* 4. size and stage */
  const sz = sizeNote(arrM);
  if (sz && !nonRev) out.push(sz);
  out.push({ title: 'Your stage sets how wide the range starts', body: stageNote(responses.stage, arrM) });

  /* 5. runway, only when it is the binding constraint */
  if (responses.profit === 'Burning, under 12 months runway') {
    out.push({
      title: 'Under twelve months of runway is priced before anything else',
      body: 'A round takes longer than the runway you have, so the price gets set against your deadline rather than against the business. Nothing else in this list outweighs it. Either extend runway before opening the process or arrive with a bridge already committed.'
    });
  }

  if (nonRev) {
    out.splice(1, 0, {
      title: 'Revenue multiples do not apply in this sector',
      body: 'Companies here are priced on programme stage, regulatory position and precedent transactions, not on a multiple of revenue. The football field in your report is built from those instead, which is why it looks different from the software version.'
    });
  }

  return out;
}

function renderDrivers() {
  const list = document.getElementById('drivers-list');
  if (!list) return;
  const drivers = buildDrivers();
  list.innerHTML = '';
  drivers.forEach(function (d, i) {
    const row = document.createElement('div');
    row.className = 'item';
    row.innerHTML = '<div class="num">' + (i + 1) + '</div><div><h3>' +
      escapeHtml(d.title) + '</h3><p>' + escapeHtml(d.body) + '</p></div>';
    list.appendChild(row);
  });
  document.getElementById('drivers-foot').textContent =
    'These are selected for your sector, stage, size and revenue model. They are the levers, not the arithmetic. The report shows which of them your range is actually sitting on, and what each one is worth in points.';
  track('drivers_view', { count: drivers.length, sector: responses.sector || null });
}

function renderResult(r) {
  const sectorLabel = responses.sector === 'Other'
    ? (responses.sector_detail || 'your sector')
    : (responses.sector || 'your sector');

  document.getElementById('range-output').textContent = money(r.low) + ' – ' + money(r.high);
  document.getElementById('range-stage-sector').textContent = (responses.stage || 'your stage') + ' · ' + sectorLabel;

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
