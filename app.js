/* Fairway landing funnel. Config first, then flow.
 * Content tables live in data-content.js and growth in app-growth.js, both of
 * which load before this file. The drivers layer is drivers.js, the football
 * field is field.js, and the result-screen metrics are app-result.js, all of
 * which load after it. */

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

/* SECTORS, REVENUE_MODELS, CURRENCY_SYMBOL, CONCERNS, INVESTORS, FIX_BY_* and
   the hook copy live in data-content.js, which loads before this file. */

/* Keys must match the button values in index.html exactly, or the band falls
   through to the 1.0 default and the dilution arithmetic runs on the wrong raise. */
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
const params = new URLSearchParams(window.location.search);
const variant = hooks[params.get('hook')] ? params.get('hook') : 'frustration';

(function initHero() {
  const h = hooks[variant];
  const k = document.getElementById('hook-kicker');
  if (!k) return;
  k.textContent = h.kicker;
  k.style.display = h.kicker ? '' : 'none';
  /* Headlines carry two-tone <span> markup written by us in data-content.js;
     nothing user-supplied ever reaches this string. */
  document.getElementById('hook-headline').innerHTML = h.headline;
  document.getElementById('hook-sub').innerHTML = h.sub;   // our own strings; carries <br> line breaks
  document.getElementById('hook-cta').textContent = h.cta;
})();

/* marquee: repeat the list six times so the -50% loop never shows a gap on any
   viewport width. With an even repeat count, translateX(-50%) lands on an
   identical arrangement, so the loop point is invisible. */
function renderMarquee(id) {
  const el = document.getElementById(id);
  if (!el) return;
  let firms = [];
  for (let i = 0; i < 6; i++) firms = firms.concat(CONFIG.teamFirms);
  el.innerHTML = firms.map(f => '<span>' + f + '</span>').join('');
}
renderMarquee('marquee-track');
renderMarquee('marquee-track-2');

/* ---------------- quiz ---------------- */
let currentStep = 1;
const totalSteps = 6;   /* six since 20-Sep-2026; the step table is in docs/STATUS-2026-09.md */
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
  /* STEP 3 CARRIES THE FORK'S EXTRAS, when we have them. qfShowIfReady draws the founder's own
     questions under the ARR box (or one line saying the website is being read); with no fork it
     hides itself and the step is ARR and margin, which every founder can answer. */
  if (currentStep === 3 && typeof qfShowIfReady === 'function') qfShowIfReady();
  else { const qf = document.getElementById('qf-block'); if (qf) qf.style.display = 'none'; }
  document.getElementById('step-label').textContent = 'Step ' + currentStep + ' of ' + totalSteps;
  document.getElementById('progress-fill').style.width = (currentStep / totalSteps * 100) + '%';
  document.getElementById('back-link').textContent = currentStep === 1 ? '← Back to start' : '← Back';
  /* THE PRIVACY PARAGRAPH IS PRINTED ONCE, on step 1, and is one tap away on every other step.
     Daniil, 20-Sep-2026: the same paragraph on every step was most of what made the quiz crowded. */
  const priv = document.getElementById('privacy-line-quiz');
  const privShort = document.getElementById('privacy-short');
  if (priv && privShort) {
    priv.style.display = currentStep === 1 ? '' : 'none';
    privShort.style.display = currentStep === 1 ? 'none' : '';
    const b = privShort.querySelector('.info-btn');
    if (b) b.setAttribute('aria-expanded', 'false');
  }
  track('quiz_step_view', { step: currentStep });
}

/* THE "i". Every explanation that used to sit under a question as a paragraph is behind one of
   these now: the question, the input and one line are what a founder sees; the reasoning is a tap
   away. One function, used by every step. */
function toggleInfo(btn) {
  const id = btn.getAttribute('aria-controls');
  const box = id ? document.getElementById(id) : null;
  if (!box) return;
  const open = box.hasAttribute('hidden') ? false : (box.style.display !== 'none');
  if (open) { box.setAttribute('hidden', ''); box.style.display = 'none'; }
  else { box.removeAttribute('hidden'); box.style.display = ''; }
  btn.setAttribute('aria-expanded', open ? 'false' : 'true');
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

/* ---------------- sector, one dropdown ----------------
   Daniil, 20-Sep-2026: thirty chips cannot be scanned, so the sector is one dropdown. It still
   leads the listed set and the investor list; what the company actually sells is read from the
   website by the profiler. `sectors` stays a list of one so nothing downstream changes shape. */

const sectorSelect = document.getElementById('sector-select');
if (sectorSelect) {
  SECTORS.forEach(function (s) {
    const o = document.createElement('option');
    o.value = s; o.textContent = s;
    sectorSelect.appendChild(o);
  });
}

/* `suggested` is true when quiz-fork.js filled the dropdown from the website read; a founder's own
   pick marks the sector as touched so a later read never overwrites it. */
function onSectorPick(el, suggested) {
  const v = el.value || '';
  if (!suggested && typeof QF_SECTOR_TOUCHED !== 'undefined') QF_SECTOR_TOUCHED = true;
  const other = document.getElementById('sector-other-wrap');
  if (other) other.style.display = v === 'Other' ? 'block' : 'none';
  if (typeof qfSectorState === 'function') qfSectorState();
  else { const btn = document.getElementById('sector-continue'); if (btn) btn.disabled = !v; }
  /* A founder's own change of sector asks the profiler again with the new hint (quiz-fork.js). */
  if (!suggested && typeof qfMaybeAsk === 'function') qfMaybeAsk();
}

function submitSector() {
  const sel = document.getElementById('sector-select');
  const v = sel ? sel.value : '';
  if (!v) return;
  responses.sectors = [v];
  responses.sector = v;
  const own = document.getElementById('sector-other');
  responses.sector_detail = (own && own.value.trim()) || null;
  const site = document.getElementById('site-url');
  responses.website = (site && site.value.trim()) || null;
  track('quiz_answer', {
    step: 2, key: 'sector', value: responses.sector,
    all: responses.sectors, detail: responses.sector_detail, has_website: !!responses.website
  });
  /* ASK WHO THIS FOUNDER IS, NOW. The fork is chosen from their archetype, the archetype comes
     from the profiler, and the profiler needs what they do and their website, which is exactly
     what step 2 just collected. The call is started here and NOT waited on: the founder moves to
     step 3 immediately; step 3 shows a one-line "reading your website" until the answer lands, and
     the fork's extra questions appear under the revenue box when it does. */
  if (typeof qfAsk === 'function') qfAsk();
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

/* growthBand, forwardAnnualGrowth and forwardRevenue live in app-growth.js,
   which loads before this file. */

function fmtPlain(n) {
  return curSymbol() + Math.round(n).toLocaleString('en-GB');
}

/* THE FIGURE IS ARR, TYPED ONCE. Daniil, 20-Sep-2026: ask for ARR and show the monthly figure as
   a memo. Everything downstream (the bands, the run-rate, the "matched on" label, the ARR basis
   in reveal-figures.js) reads `revenue_exact` as a MONTHLY figure, and it still does: ARR divided
   by twelve lands there, and `arr` carries the annual figure the founder typed. Neither leaves
   the browser (rule E9). */
function paintRevenue(v, source) {
  responses.revenue_exact = v;
  responses.arr = v > 0 ? v * 12 : null;
  responses.revenue = revenueBand(v);
  const read = document.getElementById('rev-read');
  if (source !== 'type') {
    const box = document.getElementById('arr-exact');
    if (box) box.value = v > 0 ? Math.round(v * 12) : '';
  }
  if (!read) return;
  if (v > 0) {
    read.innerHTML = '<strong>' + fmtPlain(v * 12) + ' a year, about ' + fmtPlain(v) + ' a month.</strong> ' +
      '<button type="button" class="link-btn" onclick="setPreRevenue()">We are pre-revenue</button>';
  } else {
    read.innerHTML = 'Type the figure. <button type="button" class="link-btn" onclick="setPreRevenue()">We are pre-revenue</button>';
  }
}

function onArrType() {
  const v = parseFloat(document.getElementById('arr-exact').value);
  paintRevenue(isNaN(v) || v < 0 ? 0 : v / 12, 'type');
}
function setPreRevenue() {
  const box = document.getElementById('arr-exact');
  if (box) box.value = '';
  paintRevenue(0, null);
  responses.recurring_pct = null;
  responses.revenue_model = null;
  track('quiz_answer', { step: 3, key: 'revenue', value: 'Pre-revenue' });
  currentStep = 4; renderStep();
}

/* Currency is guessed from the edge and then shown, at the revenue question and
   again beside the field, because nobody converts their own revenue into a
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
  /* Every box that carries the sign follows: the fork's money boxes and the plan's target. */
  if (typeof qfRefreshCurrency === 'function') qfRefreshCurrency();
  if (typeof paintNtm === 'function') paintNtm();
  if (lastResult) renderResult(lastResult);
}
/* Kept so an older cached page does not break on the selector. */
function onCurrency() {
  const el = document.getElementById('range-currency');
  if (el) onCurrencyChange(el);
}

(function bootCurrency() {
  /* USD BY DEFAULT. Daniil, 20-Sep-2026: the page guessed the currency from the browser and the
     visitor's country, and a London founder got GBP. The selector stays, one tap to change. */
  setCurrency('USD', 'boot');
  /* THE COUNTRY STILL COMES FROM THE EDGE. When the currency guess went (above), the country
     lookup went with it by mistake, and from 13:19 to 22:00 UK on 20-Sep-2026 every investor card
     said "your location was not resolved". /api/geo returns a country code and nothing else that
     identifies the visitor (no IP is read, stored or returned; docs/lead-capture.md). The
     currency it guesses is ignored on purpose. */
  fetch('/api/geo')
    .then(function (r) { return r.json(); })
    .then(function (g) { if (g && g.country) responses.country = g.country; })
    .catch(function () {});
})();

/* The recurring-share and revenue-model questions left the quiz on 20-Sep-2026: neither reached
   the engine (the profiler reads the revenue model from the website), and the page has one line per
   step now. The fields stay on `responses` as null so nothing downstream has to change shape. */

function showGrowthBands() {
  /* the band fallback left the page on 20-Sep-2026; kept null-safe for an older cached page */
  const g = document.getElementById('growth-bands'); if (g) g.style.display = 'grid';
  const t = document.getElementById('growth-band-toggle'); if (t) t.style.display = 'none';
}
function pickGrowthBand(band) {
  responses.growth = band;
  responses.growth_yoy = null;
  responses.growth_exact = null;
  if (typeof paintNtm === 'function') paintNtm();
  track('quiz_answer', { step: 4, key: 'growth', value: band, exact: null, fallback: true });
}

function submitRevenue() {
  if (!responses.currency) responses.currency = 'USD';
  if (responses.revenue_exact === undefined) paintRevenue(0, null);
  if (responses.gross_margin === undefined) onGrossMargin();
  /* The fork's extra figures, when the read landed and the founder filled any in. */
  if (typeof qfSubmit === 'function') qfSubmit();
  track('quiz_answer', {
    step: 3, key: 'revenue', value: responses.revenue,
    has_exact: responses.revenue_exact > 0, currency: responses.currency,
    gross_margin: responses.gross_margin
  });
  currentStep = 4; renderStep();
}

/* ---------------- growth, year on year ---------------- */

function paintGrowth(pct, source) {
  responses.growth_yoy = pct;
  responses.growth_exact = pct;
  responses.growth = growthBand(pct);
  if (source !== 'type') document.getElementById('growth-exact').value = pct;
  if (source !== 'slide') document.getElementById('growth-slider').value = pct;
  document.getElementById('growth-read').innerHTML =
    '<strong>' + pct + '% over the last twelve months.</strong> <button type="button" class="link-btn" onclick="setPreTraction()">Too early to measure</button>';
  document.getElementById('growth-annual').textContent = pct < 0
    ? 'Revenue is contracting. That is priced, and the report is where it gets explained rather than hidden.'
    : '';
  const pw = document.getElementById('plan-wrap');
  if (pw) pw.style.display = responses.revenue_exact > 0 ? '' : 'none';
  paintPlanFallback();
}

function onGrowthType() {
  const v = parseFloat(document.getElementById('growth-exact').value);
  if (isNaN(v)) return;
  paintGrowth(Math.max(-90, Math.min(1000, v)), 'type');
}
function onGrowthSlide() {
  paintGrowth(parseFloat(document.getElementById('growth-slider').value), 'slide');
}
function setPreTraction() {
  responses.growth_yoy = null;
  responses.growth_exact = null;
  responses.growth = 'Too early to measure';
  document.getElementById('growth-exact').value = '';
  document.getElementById('growth-annual').textContent = '';
  document.getElementById('growth-read').innerHTML =
    '<strong>Too early to measure.</strong> <button type="button" class="link-btn" onclick="onGrowthSlide()">Enter a rate instead</button>';
  const pw = document.getElementById('plan-wrap');
  if (pw) pw.style.display = responses.revenue_exact > 0 ? '' : 'none';
  paintPlanFallback();
}

/* ---------------- planned growth, the founder's own forecast ----------------
   This is the number the forward revenue figures are built from. We use it as
   given: no haircut, no persistence factor, no coefficient of ours anywhere in
   it. If the plan is not credible that is a conversation for the reviewer, not
   something to silently correct on the founder's behalf. */

/* THE PLAN, TWO WAYS. Daniil, 20-Sep-2026: the founder gives EITHER a growth rate for the next
   twelve months OR a money target for the next twelve months, and the page fills in the other one.
   Whichever box was typed last wins. Both are the founder's own figure, used exactly as given, with
   no haircut and no coefficient of ours. The money figure never leaves the browser (rule E9):
   `ntm_revenue_exact` is named in tools/check_request_boundary.py as a refused figure. */

function paintPlan(pct) {
  responses.growth_plan = pct;
  responses.ntm_revenue_exact = null;            /* the rate was typed last, so the sum follows it */
  const box = document.getElementById('plan-exact');
  if (box && document.activeElement !== box) box.value = pct;
  /* The slider follows the box (Daniil, 20-Sep-2026: the plan should have a slider like the
     trailing rate does). Its range is the trailing slider's; a typed rate beyond it sits at the end. */
  const sl = document.getElementById('plan-slider');
  if (sl && document.activeElement !== sl) sl.value = Math.max(-50, Math.min(400, pct));
  paintNtm();
}

function onPlanType() {
  const el = document.getElementById('plan-exact');
  const v = parseFloat(el.value);
  if (el.value.trim() === '' || isNaN(v)) { clearPlan(); return; }
  paintPlan(Math.max(-90, Math.min(1000, v)));
}
function onPlanSlide() {
  const sl = document.getElementById('plan-slider');
  if (!sl) return;
  const box = document.getElementById('plan-exact');
  if (box) box.value = sl.value;
  paintPlan(parseFloat(sl.value));
}

function clearPlan() {
  responses.growth_plan = null;
  responses.ntm_revenue_exact = null;
  const box = document.getElementById('plan-exact');
  if (box && document.activeElement !== box) box.value = '';
  paintNtm();
}

/* The twelve-month sum from the monthly figure and one annual rate: the plan if given, else the
   trailing rate, else flat. Whole units of the founder's currency, or null without revenue. */
function ntmComputed() {
  const monthly = responses.revenue_exact || 0;
  if (!(monthly > 0)) return null;
  const f = (typeof forwardAnnualGrowth === 'function') ? forwardAnnualGrowth() : null;
  const r = forwardRevenue(monthly, f);
  return (r && r.ntmM !== null) ? r.ntmM * 1e6 : null;
}

/* What the page prices on: the founder's own target if they typed one, otherwise our sum. */
function ntmForPricing() {
  const o = responses.ntm_revenue_exact;
  if (o !== null && o !== undefined && o > 0) return o;
  return ntmComputed();
}

/* The target typed by the founder: keep it, and back-calculate the annual rate that produces it
   as a twelve-month sum from today's monthly figure, so the growth box shows what the target
   implies. Solved numerically because the sum is a geometric series in the monthly step. */
function onNtmType() {
  const el = document.getElementById('ntm-exact');
  const v = parseFloat(el.value);
  if (el.value.trim() === '' || !isFinite(v) || v <= 0) {
    responses.ntm_revenue_exact = null;
    paintNtm();
    return;
  }
  responses.ntm_revenue_exact = v;
  const monthly = responses.revenue_exact || 0;
  if (monthly > 0) {
    const g = impliedAnnualGrowth(monthly, v);
    responses.growth_plan = g === null ? null : Math.round(g * 10) / 10;
    const box = document.getElementById('plan-exact');
    if (box) box.value = g === null ? '' : Math.round(g);
  }
  paintNtm();
}

/* The annual rate g such that twelve months from `monthly`, compounding at (1+g)^(1/12) a month,
   add up to `target`. Bisection on g in [-90%, +10,000%]; null when the target cannot be reached
   (below twelve months at minus 90 per cent, or above a hundred times today's figure). */
function impliedAnnualGrowth(monthly, target) {
  const sumAt = function (g) { return forwardRevenue(monthly, g / 100).ntmM * 1e6; };
  let lo = -90, hi = 10000;
  if (target < sumAt(lo) || target > sumAt(hi)) return null;
  for (let i = 0; i < 60; i++) {
    const mid = (lo + hi) / 2;
    if (sumAt(mid) < target) lo = mid; else hi = mid;
  }
  return (lo + hi) / 2;
}

function paintNtm() {
  const wrap = document.getElementById('plan-wrap');
  const box = document.getElementById('ntm-exact');
  const note = document.getElementById('ntm-note');
  if (!wrap || !box || !note) return;
  const monthly = responses.revenue_exact || 0;
  if (!(monthly > 0)) { wrap.style.display = 'none'; return; }
  wrap.style.display = '';
  const curEl = document.getElementById('ntm-cur');
  if (curEl && typeof curSymbol === 'function') curEl.textContent = curSymbol();

  const own = responses.ntm_revenue_exact;
  const overridden = own !== null && own !== undefined && own > 0;
  const sum = ntmComputed();
  if (!overridden && document.activeElement !== box) box.value = sum === null ? '' : Math.round(sum);

  const f = (typeof forwardAnnualGrowth === 'function') ? forwardAnnualGrowth() : null;
  const basis = (typeof forwardGrowthBasis === 'function') ? forwardGrowthBasis() : '';
  /* forwardAnnualGrowth() is a fraction (0.6 for 60%); the note speaks in per cent. */
  const pct = (f === null) ? null : Math.round(f * 1000) / 10;
  /* ANNUAL FIRST. Daniil, 20-Sep: step 3 asks for a yearly figure, so this line leads with the
     yearly figure and names it; the monthly number is the working, not the headline. */
  const annual = fmtPlain(monthly * 12);
  /* The twelve-month SUM is what the listed multiples apply to (they are EV over the next twelve
     months of revenue); the month-twelve run-rate is said beside it so a founder who expects
     "$90,000 times 1.47" sees where that figure went. */
  const exit = (f === null) ? null : fmtPlain(Math.round(monthly * 12 * (1 + f)));
  const runrate = exit ? ' (a run-rate of ' + exit + ' by month twelve)' : '';
  if (overridden) {
    /* The growth beside a typed target is the back-calculated one, never the trailing rate. */
    const gp = responses.growth_plan;
    const implied = (gp === null || gp === undefined) ? null : Math.round(gp * 10) / 10;
    note.textContent = fmtPlain(own) + ' over the next twelve months is your target and is what we price'
      + (implied === null
        ? ', which is beyond any growth rate we can put beside the ' + annual + ' of revenue you gave at step 3.'
        : ', which is ' + implied + '% growth on the ' + annual + ' of revenue you gave at step 3.');
  } else if (basis === 'plan') {
    note.textContent = 'Your ' + annual + ' of revenue today, growing at ' + pct + '% a year, gives '
      + fmtPlain(Math.round(sum)) + ' over the next twelve months' + runrate + '. Your plan, used as given.';
  } else if (basis === 'trailing') {
    note.textContent = 'Without a plan, your last twelve months carried forward: ' + annual
      + ' today at ' + pct + '% a year gives ' + fmtPlain(Math.round(sum)) + ' over the next twelve months' + runrate + '. Type either box to change it.';
  } else {
    note.textContent = 'Your ' + annual + ' of revenue today, carried forward flat, gives '
      + fmtPlain(Math.round(sum)) + ' over the next twelve months. Type either box to change it.';
  }
}

/* Painted whenever step 4 is shown, so a founder who typed revenue and a trailing rate sees their
   next twelve months without touching the plan. */
function paintPlanFallback() {
  if (typeof paintNtm === 'function') setTimeout(paintNtm, 0);
}

function submitRaise() {
  onLastRound();
  track('quiz_answer', {
    step: 5, key: 'raise', value: responses.raise,
    has_last_round: responses.last_round_value != null
  });
  currentStep = 6; renderStep();
}

function pickRaise(v, btn) {
  responses.raise = v;
  const grid = btn && btn.parentNode;
  if (grid) grid.querySelectorAll('.opt').forEach(o => o.classList.remove('on'));
  if (btn) btn.classList.add('on');
  const c = document.getElementById('raise-continue');
  if (c) c.disabled = false;
}

function submitGrowth() {
  if (!responses.growth) responses.growth = 'Too early to measure';
  if (responses.growth_plan === undefined) responses.growth_plan = null;
  /* The fork's growth question (three-month rate, AI-native companies) sits on this step. */
  if (typeof qfSubmitGrowth === 'function') qfSubmitGrowth();
  track('quiz_answer', {
    step: 4, key: 'growth', value: responses.growth,
    yoy: responses.growth_yoy, plan: responses.growth_plan,
    has_target: !!responses.ntm_revenue_exact
  });
  currentStep = 5; renderStep();
}

/* The investor-pushback step (chips, notes, link) left the quiz on 20-Sep-2026: the chips fed one
   echo sentence and nothing in the engine. A note and a deck link are asked for beside the consent
   button on the reveal (reveal-client.js), which is the only moment free text leaves the browser.
   `concerns` stays an empty list so the result page's echo logic needs no change. */
responses.concerns = [];

/* contact */
function validEmail(v) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v); }

async function submitLead() {
  const email = document.getElementById('lead-email').value.trim();
  const err = document.getElementById('submit-error');
  if (!validEmail(email)) { err.style.display = 'block'; return; }
  err.style.display = 'none';

  responses.email = email;
  responses.company = document.getElementById('lead-company').value.trim() || null;
  responses.phone = null;   /* the phone box left the quiz on 20-Sep-2026 */

  const btn = document.getElementById('final-submit');
  btn.disabled = true; btn.textContent = 'Saving';

  const result = computeResult();
  try {
    /* THE LEAD CARRIES NO FIGURE. Until 6-Sep-2026 this line posted the whole `responses` object
       plus every number computeResult had just worked out, so a founder's revenue, ARR, EBITDA and
       last round landed in the sheet at the moment they typed their email, before they had seen
       anything. buildLeadRecord in reveal-request.js loops over an allowlist of profile fields and
       two ratios, and api/lead.js blanks every figure column unless it sees a consent block, so
       the boundary is held at both ends. The figures go later, once, when the founder presses the
       button on the result screen. */
    const res = await fetch(CONFIG.leadEndpoint, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(buildLeadRecord(responses))
    });
    const out = await res.json().catch(function () { return {}; });
    /* Kept so the consent post can be joined to this row rather than arriving as an orphan. */
    if (out && out.lead_id) window.__fairwayLeadId = out.lead_id;
    track('lead_captured', {});
  } catch (e) {
    console.error('[fairway] lead post failed', e);
    track('lead_post_failed', {});
  }
  renderResult(result);
  btn.disabled = false; btn.textContent = 'Show me the Football Field';
}

/* ---------------- inputs that used to sit on the result screen ----------------
   Gross margin, EBITDA and the last round are quiz questions now. Asking them
   after the founder has already seen the field means building the field with
   less than we could have had. */

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

function onEbitda() {
  const el = document.getElementById('ebitda-ltm');
  const v = el ? parseFloat(el.value) : NaN;
  responses.ebitda_ltm = isNaN(v) ? null : v;
  const help = document.getElementById('ebitda-help');
  if (!help) return;
  if (responses.ebitda_ltm !== null && responses.ebitda_ltm <= 0) {
    help.textContent = 'Negative or zero EBITDA means an EBITDA multiple does not apply, and no honest field would draw the line. It still goes to the reviewer, because burn against growth is its own argument.';
  } else if (responses.ebitda_ltm > 0) {
    help.textContent = 'Positive EBITDA gives you a second independent lens, and investors will run it whether or not you do. The line and its peer set are in the report, and it is priced forward like the revenue rows because that is the basis listed companies trade on.';
  }
}

/* ---------------- result ---------------- */

function money(m) {
  const c = curSymbol();
  if (!m) return c + '0';
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

function computeResult() {
  /* This function does not produce a valuation. It produces the reference
     metrics that the football field prices, and nothing else.

     There is no coefficient of ours anywhere in it. Every number it returns is
     either something the founder typed or plain arithmetic on two things they
     typed, which is what makes every bar on the field reproducible by hand from
     what is printed beside it. */

  const monthly = responses.revenue_exact || 0;
  const runRateM = monthly * 12 / 1e6;
  const fwd = forwardAnnualGrowth();

  const fwdRev = forwardRevenue(monthly, fwd);

  /* THE FOUNDER'S OWN TARGET WINS. If they typed a next-twelve-months figure, that figure is what
     every forward row prices on. The month-twelve run-rate is monthly times (1 + g) times twelve
     on the rate that stands (the plan, else the trailing rate), which is what app-growth.js
     already returned.
     BUG FIXED 20-Sep-2026: this block used to rebuild the run-rate from the twelve-month SUM
     whenever a sum existed, override or not, so it grew the sum by a further year: at $10k a month
     and 145% growth it printed $494k where $294k is right. Daniil's live run showed $49m for $29m.
     The run-rate now comes from the rate alone; a typed target changes the sum and, through the
     back-calculated rate, the run-rate with it. */
  const ntmOwn = responses.ntm_revenue_exact;
  if (ntmOwn !== null && ntmOwn !== undefined && ntmOwn > 0) {
    fwdRev.ntmM = ntmOwn / 1e6;
  }

  /* The last round is a MARKER. It is plotted so the founder can see where they
     were priced against where the methods land, and it touches no calculation. */
  const lrValue = responses.last_round_value;

  return {
    raise: RAISE_MIDPOINT[responses.raise] || 1.0,
    runRateM: runRateM,
    ntmM: fwdRev.ntmM,
    exitArrM: fwdRev.exitArrM,
    trailingGrowth: (responses.growth_yoy === null || responses.growth_yoy === undefined) ? null : responses.growth_yoy,
    plannedGrowth: (responses.growth_plan === null || responses.growth_plan === undefined) ? null : responses.growth_plan,
    forwardGrowth: (fwd === null) ? null : fwd * 100,
    forwardBasis: forwardGrowthBasis(),
    recurringPct: (responses.recurring_pct === null || responses.recurring_pct === undefined) ? null : responses.recurring_pct,
    usedMargin: responses.gross_margin !== null && responses.gross_margin !== undefined,
    markerM: lrValue > 0 ? lrValue / 1e6 : null,
    monthsSinceRound: monthsSince(responses.last_round_date),
    ebitdaM: (responses.ebitda_ltm > 0) ? responses.ebitda_ltm / 1e6 : null
  };
}

/* stageAnchorLocal and paintCostCard live in app-result.js, which loads after
   this file. */

function renderResult(r) {
  lastResult = r;
  const sectorLabel = responses.sector === 'Other'
    ? (responses.sector_detail || 'your sector')
    : (responses.sector || 'your sector');

  const ctx = document.getElementById('ff-context');
  if (ctx) {
    const bits = [responses.stage || 'your stage', sectorLabel];
    if (r.runRateM > 0) bits.push(ffMoney(r.runRateM) + ' ARR');
    if (r.trailingGrowth !== null) bits.push('grew ' + Math.round(r.trailingGrowth) + '%');
    if (r.plannedGrowth !== null) bits.push('plans ' + Math.round(r.plannedGrowth) + '%');
    ctx.textContent = bits.join(' · ');
  }

  renderField(r);

  paintCostCard(r);

  renderDrivers();

  const f1 = FIX_BY_REVENUE[responses.revenue] || FIX_BY_REVENUE['Pre-revenue'];
  const f2 = FIX_BY_GROWTH[responses.growth] || FIX_BY_GROWTH['Too early to measure'];
  const f3 = FIX_BY_PROFIT[responses.profit] || FIX_BY_PROFIT['Burning, 12+ months runway'];
  setItem('fix-1', f1.title, f1.body, false);
  setItem('fix-2', f2.title, f2.body, true);
  setItem('fix-3', f3.title, f3.body, true);
  void f2; void f3;

  const named = (responses.concerns || []).filter(c => c !== 'Nothing specific yet');
  if (named.length || responses.concern_notes || responses.context_link) {
    const el = document.getElementById('concern-echo');
    el.style.display = 'block';
    el.textContent = named.length
      ? 'You told us investors are pushing on ' + named.join(', ').toLowerCase() + '. That goes to the reviewer with your answers, and the report answers those directly alongside the three below.'
      : 'Your notes are with the reviewer and will shape what comes back by email.';
    document.getElementById('fix-foot').textContent =
      'These are pattern-level. The report replaces them with concerns drawn from your own numbers.';
  }

  const list = INVESTORS[responses.sector] || INVESTORS['Other'];
  document.getElementById('inv-heading').textContent =
    'Three funds active in ' + sectorLabel + ' at ' + (responses.stage || 'your stage');
  document.getElementById('inv-1-name').textContent = list[0].name;
  document.getElementById('inv-1-body').textContent = list[0].note;

  const anchorM = stageAnchorLocal();
  document.getElementById('price-anchor').textContent = anchorM
    ? 'One point of a ' + money(anchorM) + ' company, the median post-money at your stage, is worth about ' + curSymbol() + Math.round(anchorM * 10000).toLocaleString() + '.'
    : 'A single point of the company is usually worth many times what this report costs.';

  track('result_view', {
    ntm_revenue_m: (r.ntmM === null || r.ntmM === undefined) ? null : +r.ntmM.toFixed(3),
    exit_arr_m: (r.exitArrM === null || r.exitArrM === undefined) ? null : +r.exitArrM.toFixed(3),
    trailing_growth: r.trailingGrowth,
    planned_growth: r.plannedGrowth,
    forward_growth: r.forwardGrowth === null ? null : Math.round(r.forwardGrowth),
    forward_basis: r.forwardBasis,
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
