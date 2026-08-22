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

/* ---------------- sector, multi-select ----------------
   A company is rarely one box. Picking several is more informative than forcing
   a single choice, and the first one picked leads: it decides which peer set and
   which investor list we start from, and the rest sharpen the peer selection.
   Nothing advances the step, so the website field below can actually be typed in. */

const chosenSectors = [];

const sectorGrid = document.getElementById('sector-grid');
if (sectorGrid) {
  SECTORS.forEach(function (s) {
    const b = document.createElement('button');
    b.className = 'opt';
    b.type = 'button';
    b.textContent = s;
    b.onclick = function () { toggleSector(s, b); };
    sectorGrid.appendChild(b);
  });
}

function toggleSector(s, btn) {
  const i = chosenSectors.indexOf(s);
  if (i === -1) {
    if (chosenSectors.length >= 3) return;
    chosenSectors.push(s); btn.classList.add('on');
  } else {
    chosenSectors.splice(i, 1); btn.classList.remove('on');
  }
  const other = document.getElementById('sector-other-wrap');
  if (other) other.style.display = chosenSectors.indexOf('Other') !== -1 ? 'block' : 'none';
  paintSectorState();
}

function paintSectorState() {
  const read = document.getElementById('sector-read');
  const btn = document.getElementById('sector-continue');
  const n = chosenSectors.length;
  if (read) {
    read.textContent = n === 0
      ? 'Pick the closest. You can pick up to three, and the first one leads.'
      : (n === 1 ? chosenSectors[0] + '. Add a second if you straddle two.'
        : chosenSectors.join(' · ') + '. The first one leads.');
  }
  if (btn) btn.disabled = n === 0;
}

function submitSector() {
  if (!chosenSectors.length) return;
  responses.sectors = chosenSectors.slice();
  /* The first pick is the primary: peer set, investor list and copy tables all
     key off it. The others go to the reviewer and to the peer selection. */
  responses.sector = chosenSectors[0];
  const v = document.getElementById('sector-other').value.trim();
  responses.sector_detail = (chosenSectors.indexOf('Other') !== -1 ? (v || null) : (v || null));
  track('quiz_answer', {
    step: 2, key: 'sector', value: responses.sector,
    all: responses.sectors, detail: responses.sector_detail, has_website: !!responses.website
  });
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
  if (lastResult) renderResult(lastResult);
}
/* Kept so an older cached page does not break on the selector. */
function onCurrency() {
  const el = document.getElementById('range-currency');
  if (el) onCurrencyChange(el);
}

(function bootCurrency() {
  /* Best guess from the browser first, so nothing is ever blank, then the edge
     header refines it. Anything outside the four we support falls back to USD. */
  const lang = (navigator.language || '').toUpperCase();
  const byLang = { GB: 'GBP', CA: 'CAD',
    IE: 'EUR', DE: 'EUR', FR: 'EUR', ES: 'EUR', IT: 'EUR', NL: 'EUR',
    BE: 'EUR', AT: 'EUR', PT: 'EUR', FI: 'EUR', GR: 'EUR', EE: 'EUR', LT: 'EUR', LV: 'EUR' };
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
  responses.growth_yoy = null;
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
    recurring_pct: responses.recurring_pct, revenue_model: responses.revenue_model || null,
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
  document.getElementById('growth-detail-wrap').style.display = 'block';
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
  document.getElementById('growth-detail-wrap').style.display = 'block';
}

/* ---------------- planned growth, the founder's own forecast ----------------
   This is the number the forward revenue figures are built from. We use it as
   given: no haircut, no persistence factor, no coefficient of ours anywhere in
   it. If the plan is not credible that is a conversation for the reviewer, not
   something to silently correct on the founder's behalf. */

function paintPlan(pct) {
  responses.growth_plan = pct;
  document.getElementById('plan-exact').value = pct;
  document.getElementById('plan-slider').value = pct;
  document.getElementById('plan-read').innerHTML =
    '<strong>' + pct + '% planned for the next twelve months.</strong> ' +
    '<button type="button" class="link-btn" onclick="clearPlan()">Use my last twelve months instead</button>';
  paintPlanNote();
}

/* Says out loud what the two numbers imply about each other. A plan far above
   the trailing rate is the single most common thing an investor pushes on, so
   the page raises it here rather than letting it surface in the meeting. */
function paintPlanNote() {
  const el = document.getElementById('plan-note');
  if (!el) return;
  const p = responses.growth_plan, y = responses.growth_yoy;
  if (p === null || p === undefined) { el.textContent = ''; return; }
  if (y === null || y === undefined) { el.textContent = 'Everything forward on the next screen is built from this number, exactly as you gave it.'; return; }
  if (y > 0 && p > y * 1.25) {
    el.textContent = 'That is an acceleration on the ' + Math.round(y) + '% you just did. It is the first thing an investor will test, so bring what changes to make it happen: a channel, a hire, a price move.';
  } else if (y > 0 && p < y * 0.6) {
    el.textContent = 'That is a deceleration on the ' + Math.round(y) + '% you just did. Planning conservatively is fine, but say why, or the multiple gets read against the lower number without the reason attached.';
  } else {
    el.textContent = 'Broadly in line with the ' + Math.round(y) + '% you just did, which is the easiest version of this to defend.';
  }
}

/* Prefill the plan with the trailing rate the first time, so the founder edits a
   sensible starting point rather than facing an empty box. Never overwrites a
   number they have already typed. */
function paintPlanFallback() {
  if (responses.growth_plan !== null && responses.growth_plan !== undefined) { paintPlanNote(); return; }
  const y = responses.growth_yoy;
  const el = document.getElementById('plan-exact');
  if (!el || y === null || y === undefined) return;
  if (el.value === '') { el.value = Math.round(y); document.getElementById('plan-slider').value = Math.round(y); }
}

function onPlanType() {
  const v = parseFloat(document.getElementById('plan-exact').value);
  if (isNaN(v)) return;
  paintPlan(Math.max(-90, Math.min(1000, v)));
}
function onPlanSlide() { paintPlan(parseFloat(document.getElementById('plan-slider').value)); }

function clearPlan() {
  responses.growth_plan = null;
  document.getElementById('plan-exact').value = '';
  document.getElementById('plan-read').innerHTML =
    'Type the number or drag the slider. <button type="button" class="link-btn" onclick="onPlanSlide()">Enter a plan</button>';
  document.getElementById('plan-note').textContent =
    'Without a plan we carry your last twelve months forward unchanged, and the row says that is what we did.';
}

function submitProfit(v) {
  responses.profit = v;
  onEbitda();
  track('quiz_answer', { step: 5, key: 'profit', value: v, ebitda: responses.ebitda_ltm });
  currentStep = 6; renderStep();
}

function submitRaise() {
  onLastRound();
  track('quiz_answer', {
    step: 6, key: 'raise', value: responses.raise,
    has_last_round: responses.last_round_value != null
  });
  currentStep = 7; renderStep();
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
  responses.growth_detail = document.getElementById('growth-detail').value.trim() || null;
  track('quiz_answer', {
    step: 4, key: 'growth', value: responses.growth,
    yoy: responses.growth_yoy, plan: responses.growth_plan, has_detail: !!responses.growth_detail
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
  const v = parseFloat(document.getElementById('ebitda-ltm').value);
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
