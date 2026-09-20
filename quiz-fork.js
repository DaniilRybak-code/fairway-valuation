/* The fork step: the questions this founder actually gets.
 *
 * WHAT WAS WRONG UNTIL NOW. selector/quiz_fork.py has held nine forks since 31 August. The page has
 * never rendered any of them: index.html asks the same nine fixed steps of everyone and collects
 * one figure, current monthly revenue. Measured on the 102 test companies, 45 of them would be
 * asked a different set of questions by their own fork, and 5 are priced on something the live quiz
 * never asks for at all. A lender is asked for revenue while the engine prices them on their book,
 * which is the exact failure fork_for() was written to prevent. And the gross-revenue question
 * Daniil ruled on 5 September, which unlocked 105 rounds, reaches nobody.
 *
 * Nothing had to be rebuilt. The whole specification was already in the source, in code, walked by
 * check 10 on every run. This file is the half that was missing: it draws it.
 *
 * HOW IT WORKS. After step 2 the page asks /api/profile who this founder is. That endpoint runs the
 * profiler over their answers and their website, picks the fork, and sends back the fork's
 * questions. This renders them, collects the answers, and puts them on `responses` under the keys
 * selector/quiz_fork.apply_answers() reads.
 *
 * EVERY ANSWER HERE IS AN AMOUNT AND NONE OF THEM LEAVE (rule E9). The endpoint sends QUESTIONS and
 * gets back nothing: the answers live in `responses`, the browser prices with them, and
 * reveal-request.js has never carried a single one of these keys.
 *
 * IT DEGRADES TO WHAT THE PAGE DID YESTERDAY. If the endpoint is slow, refused or missing, the
 * founder gets the plain revenue question and the quiz runs exactly as it did before this file
 * existed. A founder never waits on us and never sees an error.
 *
 * Loaded after app.js.
 */

var FORK_SPEC = null;          /* what /api/profile returned, or null */
var FORK_ASKED = false;        /* asked once per quiz run, never twice */

function qfEsc(v) {
  return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

/* A number the founder typed, or null. Never a string, never NaN, never zero-as-empty. */
function qfNum(id) {
  var el = document.getElementById(id);
  if (!el) return null;
  var v = parseFloat(el.value);
  return (isFinite(v) && v >= 0 && String(el.value).trim() !== '') ? v : null;
}

/* ONE QUESTION, DRAWN IN THE PAGE'S OWN CLASSES so a fork question is indistinguishable from a
   hand-written one. The kinds come from the fork spec: money and quantity are numbers, percent is a
   number with a unit, choice is a row of buttons. */
function qfQuestion(q) {
  var id = 'qf-' + q.key;
  var out = [];
  out.push('<div class="qf-q" data-key="' + qfEsc(q.key) + '">');
  out.push('<label class="field-label" for="' + id + '">' + qfEsc(q.label));
  if (!q.required) out.push(' <span class="optional">Optional.</span>');
  /* THE WHY SITS BEHIND AN "i", as every explanation in the quiz does since 20-Sep-2026 (Daniil:
     one line per question, the rest one tap away). The text is the engine's own, unchanged. */
  if (q.why) out.push(' <button type="button" class="info-btn" aria-expanded="false" aria-controls="' + id + '-why" onclick="toggleInfo(this)">i</button>');
  out.push('</label>');
  if (q.why) out.push('<p class="q-info" id="' + id + '-why" hidden>' + (qfUsedFor(q.key) ? '<b>Used for:</b> ' + qfEsc(qfUsedFor(q.key)) + ' ' : '') + qfEsc(q.why) + '</p>');

  if (q.kind === 'choice' && q.options && q.options.length) {
    out.push('<div class="opt-grid">');
    q.options.forEach(function (o) {
      var val = qfEsc(typeof o === 'string' ? o : (o.value || o.label));
      var lab = qfEsc(typeof o === 'string' ? o : (o.label || o.value));
      out.push('<button type="button" class="opt" data-q="' + qfEsc(q.key) + '" data-v="' + val
             + '" onclick="qfPickChoice(this)">' + lab + '</button>');
    });
    out.push('</div>');
  } else if (q.kind === 'percent' && q.key === 'nrr_pct') {
    /* RETENTION AS A SLIDER (Daniil, 20-Sep-2026, Elentaria run: "why is revenue retention asked
       as a window, not as a slider? ... and the user to disregard it if it is not available").
       The box and the slider are the same value; the slider starts unset, so a founder who does
       not measure it leaves it blank, and the link clears it if they moved it by mistake. */
    out.push('<div class="num-row">');
    out.push('<input class="field field-num" id="' + id + '" type="number" step="1" min="0" max="300"'
           + ' inputmode="numeric" placeholder="e.g. 110" oninput="qfSyncSlider(\'' + qfEsc(q.key) + '\', \'box\')" aria-label="' + qfEsc(q.label) + '">');
    out.push('<span class="unit">%</span></div>');
    out.push('<input class="slider" id="' + id + '-slider" type="range" min="50" max="200" value="100" step="1"'
           + ' oninput="qfSyncSlider(\'' + qfEsc(q.key) + '\', \'slider\')" aria-label="' + qfEsc(q.label) + ' slider">');
    out.push('<p class="slider-read" id="' + id + '-read">Drag the slider or type the number. '
           + '<button type="button" class="link-btn" onclick="qfClearPercent(\'' + qfEsc(q.key) + '\')">We do not measure it</button></p>');
  } else if (q.kind === 'percent') {
    out.push('<div class="num-row">');
    out.push('<input class="field field-num" id="' + id + '" type="number" step="1" min="-100" max="1000"'
           + ' inputmode="numeric" oninput="qfChanged()" aria-label="' + qfEsc(q.label) + '">');
    out.push('<span class="unit">%</span></div>');
  } else {
    /* money, quantity and count all draw as a plain number. The unit sits beside it when the spec
       names one, because "tonnes" and "dollars" are not interchangeable and the founder should not
       have to guess which we meant. */
    out.push('<div class="num-row">');
    if (q.kind === 'money') out.push('<span class="unit" id="' + id + '-cur">$</span>');
    /* The arrows step by something a founder would type: ten thousand on money, a hundred on a
       count (Daniil, 20-Sep: a net revenue box stepping by single dollars "is weird"). */
    out.push('<input class="field field-num" id="' + id + '" type="number" step="' + (q.kind === 'money' ? '10000' : '100') + '" min="0"'
           + ' inputmode="numeric" placeholder="' + qfEsc(q.placeholder || '') + '"'
           + ' oninput="qfChanged()" aria-label="' + qfEsc(q.label) + '">');
    if (q.unit) out.push('<span class="unit">' + qfEsc(q.unit) + '</span>');
    out.push('</div>');
  }
  out.push('</div>');
  return out.join('');
}

/* The retention slider and its box stay in step; the read-out says what is set. */
function qfSyncSlider(key, from) {
  var box = document.getElementById('qf-' + key);
  var sl = document.getElementById('qf-' + key + '-slider');
  var read = document.getElementById('qf-' + key + '-read');
  if (!box || !sl) return;
  if (from === 'slider') box.value = sl.value;
  else if (box.value !== '' && isFinite(parseFloat(box.value))) sl.value = Math.max(50, Math.min(200, parseFloat(box.value)));
  if (read) read.innerHTML = (box.value === '' ? 'Drag the slider or type the number. ' : '<strong>' + qfEsc(box.value) + '% net revenue retention.</strong> ')
    + '<button type="button" class="link-btn" onclick="qfClearPercent(\'' + qfEsc(key) + '\')">We do not measure it</button>';
  qfChanged();
}
function qfClearPercent(key) {
  var box = document.getElementById('qf-' + key);
  var sl = document.getElementById('qf-' + key + '-slider');
  if (box) box.value = '';
  if (sl) sl.value = 100;
  responses[key] = null;
  qfSyncSlider(key, 'box');
}

/* THE CURRENCY SIGN ON EVERY FORK MONEY BOX, refreshed when the founder changes currency after
   the questions were drawn (Daniil, 20-Sep-2026: the gross box stayed in $ after EUR was picked). */
function qfRefreshCurrency() {
  var cur = (typeof curSymbol === 'function') ? curSymbol() : '$';
  document.querySelectorAll('#qf-block [id$="-cur"], #qf-growth-block [id$="-cur"]').forEach(function (e) { e.textContent = cur; });
}

function qfPickChoice(btn) {
  var key = btn.getAttribute('data-q');
  document.querySelectorAll('.opt[data-q="' + key + '"]').forEach(function (b) {
    b.classList.remove('sel');
  });
  btn.classList.add('sel');
  responses[key] = btn.getAttribute('data-v');
  qfChanged();
}

/* WHAT THEY WERE READ AS, SHOWN BACK TO THEM. The profiler decides which questions a founder gets,
   and it can be wrong. The person best placed to catch that is the founder, before they answer four
   questions on the wrong basis, so the read is printed above the questions in their own words. */
function qfReadBack(spec) {
  var r = spec.read_as || {};
  var sells = (r.sells || '').split('|').filter(Boolean).slice(0, 3).join(', ');
  var bits = [];
  if (sells) bits.push('you sell ' + sells.toLowerCase());
  if (r.industry && r.industry !== 'Horizontal') bits.push('into ' + r.industry.toLowerCase());
  if (!bits.length) return '';
  return '<p class="q-help" style="margin:0 0 10px;">We read your site as: <b>' + qfEsc(bits.join(', '))
       + '</b>. <button type="button" class="link-btn" onclick="qfWrongRead()">Not right</button></p>';
}

/* If the read is wrong, we do not argue and we do not guess again. They get the plain revenue
   question, which is what every founder got before today, and the reviewer sees the note. */
function qfWrongRead() {
  responses.profile_disputed = true;
  track('quiz_profile_disputed', { fork: FORK_SPEC && FORK_SPEC.fork });
  FORK_SPEC = null;
  ['qf-block', 'qf-read2', 'qf-growth-block'].forEach(function (id) {
    var mount = document.getElementById(id);
    if (mount) { mount.innerHTML = ''; mount.style.display = 'none'; }
  });
  qfRelabelRevenue('software');
  qfSectorState();
}

/* NO FIGURE EVER BLOCKS THE BUTTON. Daniil, 7-Sep-2026: a founder who gives nothing still gets the
   peer charts, so a figure they choose not to give cannot be a wall.
   THIS WAS A REGRESSION I SHIPPED EARLIER THE SAME DAY. Every fork had a required money question,
   and drawing the forks turned that flag into a disabled button. The fork step was stricter than
   the plain revenue question it replaced, which has always had a "We are pre-revenue" escape. The
   flags are off in selector/quiz_fork.py now and this is the belt to that braces: even if one comes
   back, a number never gates the page.
   THE TWO CHOICE QUESTIONS STILL DO, and they are the only ones. The lending fork's funding model
   and the exchange fork's unit are labels, one tap each, and each one changes how the founder is
   priced rather than saying anything about their size. */
function qfChanged() {
  /* THE STEP'S OWN CONTINUE IS THE BUTTON, since 20-Sep-2026 the extras sit under the ARR box
     rather than replacing the step. A missing figure never gates it; the two choice questions do,
     because they are labels that change how the founder is priced. */
  var btn = document.querySelector('.q-block[data-step="3"] .btn');
  if (!btn || !FORK_SPEC) return;
  var missingChoice = FORK_SPEC.questions.filter(function (q) {
    return q.required && q.kind === 'choice' && !responses[q.key];
  });
  btn.disabled = missingChoice.length > 0;
  btn.textContent = missingChoice.length ? 'Pick one above to continue' : 'Continue';
}

/* THE EXTRAS, DRAWN UNDER THE ARR BOX. Until 20-Sep-2026 the fork REPLACED step 3, which dropped
   the gross margin question (only the e-commerce fork asks it) and asked ARR a second way. Now the
   step is ARR and margin for everyone, and the fork adds only the figures its business is priced
   on beyond ARR: net revenue for a marketplace, the book for a lender, subscribers for a consumer
   app. `arr` is skipped because the step already asked it. */
var QF_ALREADY_ASKED = { arr: true, net_revenue: true, gross_margin: true };

/* WHAT THE REVENUE BOX MEANS FOR THIS FORK, said in the fork's own words once the read has landed.
   Daniil, 20-Sep, on the D2C run: four figures asked at step 3, two of them the same thing twice
   (the fork's "net revenue" beside the revenue box, the fork's "gross margin" beside the slider).
   The box is the one revenue figure; it prices every revenue row; the fork adds only the figures
   that add a row of their own. */
var QF_REVENUE_LABEL = {
  software: 'Annual recurring revenue today, or your revenue run-rate if it does not recur.',
  lending: 'Annual recurring revenue today, or your revenue run-rate if it does not recur.',
  ecommerce: 'Your revenue over the last twelve months, net of returns and discounts.',
  consumer: 'Your revenue over the last twelve months, net of refunds and app-store fees.',
  consumer_subscription: 'Your revenue over the last twelve months, net of refunds and app-store fees.',
  marketplace: 'Your own revenue over the last twelve months: your commission and fees, not what buyers paid in total.',
  delivery: 'Your own revenue over the last twelve months: your fees and commission, not the basket.',
  payments: 'Your net revenue over the last twelve months, after interchange and scheme fees.',
  exchange: 'Your net revenue over the last twelve months.',
  media: 'Your revenue over the last twelve months.'
};

/* WHAT EACH EXTRA FIGURE IS USED FOR, in one line, ahead of the engine's own explanation. Keyed
   by the question, written here rather than sent by /api/profile: how an answer is used is the
   engine's business (check 15), but a founder deciding whether to type a figure deserves to know
   what it changes. */
var QF_USED_FOR = {
  gross_revenue: 'one row of its own, EV to gross revenue, on private rounds priced that way. It changes nothing else.',
  gmv: 'the rounds and listed names that are priced on what passes through the platform. It changes nothing else.',
  paying_subscribers: 'one row of its own, dollars of enterprise value per paying subscriber, from rounds that disclosed the count. It changes nothing else.',
  nrr_pct: 'the reviewer, with your figures. It prices no row today.',
  free_users: 'the reviewer, with your figures. It prices no row today.',
  book_value: 'the book-value rows, which is how listed lenders are priced.',
  net_loan_book: 'the reviewer, with your figures. It prices no row.',
  net_income: 'the price-to-earnings row, where listed lenders carry one.',
  originations: 'the EV-to-originations row, from rounds priced on what was lent.',
  borrowers: 'one row of its own, dollars of enterprise value per borrower.',
  funding_model: 'whether a lender may be priced on revenue at all.',
  throughput_volume: 'the EV-per-unit-of-throughput row, in the unit you pick.',
  throughput_unit: 'the unit the throughput row is priced in.',
  growth_3m_pct: 'your growth band. For an AI-native company a three-month rate, annualised, replaces the last twelve months, because an annual rate means little for a company doubling every two months.'
};

/* THE SAME LINE IN THE FORK'S OWN WORD. A brand or retailer calls its gross figure GMV (Daniil,
   20-Sep-2026: "gross sales is a misleading term, let's use GMV"), and the row it feeds is named
   the same way on the field. Keyed by fork, then by question; falls back to QF_USED_FOR. */
var QF_USED_FOR_BY_FORK = {
  ecommerce: {
    gross_revenue: 'one row of its own, EV to GMV, from private rounds priced on GMV. It changes nothing else.'
  }
};
function qfUsedFor(key) {
  var fork = (FORK_SPEC && FORK_SPEC.fork) || '';
  var byFork = QF_USED_FOR_BY_FORK[fork] || {};
  return byFork[key] || QF_USED_FOR[key] || '';
}

/* The read-back and the one-line "what these are for", drawn above the extras. */
function qfIntro(qs) {
  if (!qs.length) return '';
  return '<p class="q-help" style="margin:8px 0 6px;">The revenue above prices every revenue row. Each figure below adds a row of its own, and only if you give it. Tap an "i" to see what it feeds.</p>';
}

/* QUESTIONS THAT BELONG ON STEP 4, not under the revenue box: a growth question sits with the
   growth question (Daniil, 20-Sep-2026: "And over the last three months? -> what are we asking
   for?"; it was the AI-native growth question drawn under revenue with no context). */
var QF_ON_GROWTH_STEP = { growth_3m_pct: true };

function qfRender(spec) {
  FORK_SPEC = spec;
  var mount = document.getElementById('qf-block');
  if (!mount || !spec || !spec.questions) return false;
  var all = spec.questions.filter(function (q) { return !QF_ALREADY_ASKED[q.key]; });
  var qs = all.filter(function (q) { return !QF_ON_GROWTH_STEP[q.key]; });
  var gqs = all.filter(function (q) { return QF_ON_GROWTH_STEP[q.key]; });
  /* The read is shown on step 2 when it landed in time (qfShowRead2); on step 3 it is repeated
     only if the founder never saw it there. */
  var html = [QF_READ_SHOWN_ON_2 ? '' : qfReadBack(spec)];
  qfRelabelRevenue(spec.fork);
  if (qs.length) {
    html.push('<p class="field-label" style="margin:6px 0 2px;">' + qfEsc(qfTitleFor(spec.fork))
            + ' <span class="optional">Optional.</span></p>');
    html.push(qfIntro(qs));
    qs.forEach(function (q) { html.push(qfQuestion(q)); });
  }
  mount.innerHTML = html.join('');
  mount.style.display = html.join('').trim() ? 'block' : 'none';
  var gm = document.getElementById('qf-growth-block');
  if (gm) {
    gm.innerHTML = gqs.map(qfQuestion).join('');
    gm.style.display = gqs.length ? 'block' : 'none';
  }
  qfRefreshCurrency();
  qfChanged();
  track('quiz_fork_shown', { fork: spec.fork, questions: all.length });
  return true;
}

/* The step-4 fork answers, read when step 4 is submitted (qfSubmit runs at step 3, before they
   are typed). */
function qfSubmitGrowth() {
  if (!FORK_SPEC) return;
  FORK_SPEC.questions.forEach(function (q) {
    if (!QF_ON_GROWTH_STEP[q.key]) return;
    var v = qfNum('qf-' + q.key);
    if (v !== null) responses[q.key] = v;
  });
}

/* The heading. One line per fork, in the founder's language rather than ours: a lender should not
   be greeted with the word "fork". */
function qfTitleFor(fork) {
  return {
    software: 'Also priced on, if you have it',
    marketplace: 'What goes through your marketplace',
    consumer: 'Your subscribers and users',
    consumer_subscription: 'Your subscribers and users',
    exchange: 'What you move, and what you earn on it',
    ecommerce: 'Your GMV, if you track it',
    payments: 'Before interchange, if you report it',
    lending: 'Your book, and how it is funded',
    media: 'Your audience',
    delivery: 'The basket, if you book it'
  }[fork] || 'More figures';
}

/* The revenue box's own line, in the fork's words. Falls back to the generic line for a fork not
   in the map, and never touches the figure already typed. */
function qfRelabelRevenue(fork) {
  var el = document.getElementById('rev-help-text');
  if (!el) return;
  el.textContent = QF_REVENUE_LABEL[fork] || QF_REVENUE_LABEL.software;
}

function qfSubmit() {
  if (!FORK_SPEC) return;
  var answered = 0;
  FORK_SPEC.questions.forEach(function (q) {
    if (QF_ALREADY_ASKED[q.key] || QF_ON_GROWTH_STEP[q.key]) return;
    if (q.kind === 'choice') { if (responses[q.key]) answered++; return; }
    var v = qfNum('qf-' + q.key);
    if (v !== null) { responses[q.key] = v; answered++; }
  });
  responses.fork = FORK_SPEC.fork;
  /* ANSWERED, NEVER THE ANSWERS. The event carries how many questions were filled in and which
     fork, because that is what tells us whether a fork is too long. It carries no figure. */
  track('quiz_answer', { step: 3, key: 'fork_answers', fork: FORK_SPEC.fork, answered: answered });
}

/* ASKED ONCE, AFTER STEP 2, AND THE FOUNDER NEVER WAITS ON IT. The call is started as soon as the
   sector and website are in, and the page carries on. If it lands before they reach step 3 they get
   their fork; if it does not, they get the plain revenue question and the quiz is exactly what it
   was yesterday. Nothing about this is allowed to hold a founder up. */
var QF_STATE = 'idle';         /* idle | asking | ready | failed */
var QF_ASKED_FOR = '';         /* the sector and website the last read was asked for */
var QF_READ_SHOWN_ON_2 = false;
var QF_TIMER = null;

/* THE READ STARTS ON STEP 2, the moment a website is typed (Daniil, 20-Sep, second ruling of the
   day: "ask for the website straight away ... the description should pop up in step 2, and then
   step 2 could automatically suggest the vertical, and then the user could change it"). Typing
   pauses for three quarters of a second before the call goes, so a founder still typing is not
   asked about "fyl" and then "fyle.i". A changed website or sector asks again; the same pair does
   not. The sector, when the founder has already picked one, goes with the ask as a hint. */
function qfMaybeAsk() {
  var sel = document.getElementById('sector-select');
  var site = document.getElementById('site-url');
  var sector = sel ? sel.value : '';
  var url = site ? site.value.trim() : '';
  if (!url || url.indexOf('.') < 0) { qfSectorState(); return; }
  clearTimeout(QF_TIMER);
  QF_TIMER = setTimeout(function () {
    responses.sector = sector || null; responses.sectors = sector ? [sector] : []; responses.website = url;
    qfAsk();
  }, 750);
}

/* WHICH SECTOR THE READ SUGGESTS. A judgement table, in the page where the founder can see the
   result and change it: the profiler returns an archetype (what the company is) and an industry
   (who it sells to), and the sector dropdown is coarser than both. A software archetype takes its
   sector from the industry it sells into; everything else maps straight. Unknown maps to nothing,
   and the founder picks. */
var QF_SECTOR_BY_INDUSTRY = {
  'Healthcare & Life Sciences': 'Healthtech / Digital health', 'Financial Services': 'Fintech',
  'Insurance': 'Insurtech', 'Real Estate': 'Proptech', 'Construction & Infrastructure': 'Proptech',
  'Education': 'Edtech', 'Legal & Professional Services': 'Legaltech / Regtech',
  'Recruitment & Work': 'HR tech / Future of work', 'Logistics & Mobility': 'Logistics / Supply chain',
  'Hospitality': 'Travel / Hospitality', 'Travel': 'Travel / Hospitality', 'Government': 'Defence / Gov tech',
  'Energy & Utilities': 'Climate / Energy', 'Automotive': 'Mobility / Automotive',
  'Retail & E-commerce': 'E-commerce / Retail', 'Media & Gaming': 'Media / Content',
  'Food & Grocery': 'Food / Beverage', 'Telecom': 'Telecoms / Connectivity',
  'Security & Property': 'Cybersecurity', 'Semiconductors': 'Deeptech / Hardware',
  'Manufacturing': 'Deeptech / Hardware'
};
var QF_SOFTWARE_ARCHETYPES = {
  'Business Applications': 1, 'Vertical Software': 1, 'Communications & Collaboration': 1,
  'Software Consolidator': 1, 'Design & Engineering': 1, 'Cloud & Infrastructure': 1
};
var QF_SECTOR_BY_ARCHETYPE = {
  'Data, AI & Developer Tools': 'AI / ML', 'Cybersecurity': 'Cybersecurity',
  'Marketing & Customer Engagement': 'Adtech / Martech',
  'Consumer & Prosumer Software': 'Consumer / D2C', 'Consumer Brand': 'Consumer / D2C',
  'Owned-Inventory Retail': 'E-commerce / Retail', 'Commerce Enablement & Fulfilment': 'E-commerce / Retail',
  'Third-Party Marketplace': 'Marketplaces', 'Classifieds & Listings': 'Marketplaces',
  'Freelance & Services Marketplace': 'Marketplaces', 'Travel Booking & OTA': 'Travel / Hospitality',
  'Gaming & Virtual Economy': 'Gaming',
  'Merchant Acquiring & PSP': 'Fintech', 'Payment Network': 'Fintech', 'Cross-Border & FX': 'Fintech',
  'Commerce & Payments Software': 'Fintech', 'Card Issuing & BaaS': 'Fintech', 'Lending & Credit': 'Fintech',
  'Digital Bank & Deposits': 'Fintech', 'Wealth & Capital Markets Platform': 'Fintech',
  'Market Infrastructure & Exchange': 'Fintech', 'Financial Data & Index': 'Fintech',
  'Crypto & Digital Assets': 'Web3 / Digital assets', 'Insurance Technology': 'Insurtech',
  'Local Delivery & On-Demand': 'Logistics / Supply chain', 'Supply Chain & Logistics Software': 'Logistics / Supply chain',
  'Online Learning': 'Edtech', 'Streaming & Digital Media': 'Media / Content',
  'Dating & Social Network': 'Consumer / D2C'
};
function qfSectorFor(readAs) {
  var a = (readAs && readAs.archetype) || '', i = (readAs && readAs.industry) || '';
  if (QF_SOFTWARE_ARCHETYPES[a]) return QF_SECTOR_BY_INDUSTRY[i] || 'SaaS / B2B software';
  return QF_SECTOR_BY_ARCHETYPE[a] || '';
}

/* The founder's own pick always wins over the suggestion. Set by onSectorPick (app.js). */
var QF_SECTOR_TOUCHED = false;
var QF_WAIT_MS = 15000;          /* how long Continue waits for the read; Daniil, 20-Sep: fine, as long as the user knows */
var QF_WAIT_TIMER = null;
var QF_WAIT_OVER = false;

function qfSuggestSector(spec) {
  var sel = document.getElementById('sector-select');
  if (!sel) return;
  var want = qfSectorFor(spec && spec.read_as);
  var opts = Array.prototype.map.call(sel.options, function (o) { return o.value; });
  if (!want || opts.indexOf(want) < 0) return;
  if (QF_SECTOR_TOUCHED && sel.value) return;
  sel.value = want;
  responses.sector = want; responses.sectors = [want];
  QF_ASKED_FOR = want + '|' + (responses.website || '');   /* the suggestion is not a change that re-asks */
  if (typeof onSectorPick === 'function') onSectorPick(sel, true);
}

/* CONTINUE ON STEP 2: enabled once a sector is set (suggested or picked). While the read is in
   flight and nothing is set, the button says what it is waiting for; after QF_WAIT_MS it stops
   waiting and asks the founder to pick, and the read catches up on step 3 if it lands later. */
function qfSectorState() {
  var btn = document.getElementById('sector-continue');
  var sel = document.getElementById('sector-select');
  var note = document.getElementById('sector-note');
  if (!btn || !sel) return;
  var has = !!sel.value;
  var reading = QF_STATE === 'asking' && !QF_WAIT_OVER;
  btn.disabled = !has;
  btn.textContent = (reading && !has) ? 'Reading your website\u2026' : 'Continue';
  if (note) {
    note.textContent = has && !QF_SECTOR_TOUCHED && QF_STATE === 'ready' ? 'Suggested from your website. Change it if it is wrong.'
      : (reading && !has ? 'Filled in from your website in a few seconds, or pick it yourself.'
      : (QF_WAIT_OVER && !has && QF_STATE === 'asking' ? 'The read is taking longer than usual. Pick your sector and continue; the read catches up on the next step.'
      : 'Pick the closest.'));
  }
}

function qfAsk() {
  var key = (responses.sector || '') + '|' + (responses.website || '');
  if (QF_ASKED_FOR === key && QF_STATE !== 'failed') return;
  QF_ASKED_FOR = key;
  FORK_ASKED = true;
  var body = (typeof buildRevealRequest === 'function') ? buildRevealRequest(responses) : null;
  if (!body) return;
  QF_STATE = 'asking';
  FORK_SPEC = null;
  QF_READ_SHOWN_ON_2 = false;
  responses.profile_disputed = false;
  QF_WAIT_OVER = false;
  clearTimeout(QF_WAIT_TIMER);
  QF_WAIT_TIMER = setTimeout(function () { QF_WAIT_OVER = true; qfSectorState(); qfShowRead2(); }, QF_WAIT_MS);
  qfShowRead2();
  qfSectorState();
  fetch('/api/profile', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body)
  })
    .then(function (r) { return r.json(); })
    .then(function (spec) {
      if (QF_ASKED_FOR !== key) return;          /* a later ask superseded this one */
      if (!spec || !spec.questions) { QF_STATE = 'failed'; clearTimeout(QF_WAIT_TIMER); qfShowRead2(); qfSectorState(); qfShowIfReady(); return; }
      if (responses.profile_disputed) return;
      FORK_SPEC = spec;
      QF_STATE = 'ready';
      clearTimeout(QF_WAIT_TIMER);
      if (currentStep === 2) { qfShowRead2(); qfSuggestSector(spec); }
      qfSectorState();
      if (currentStep === 3) qfShowIfReady();
    })
    .catch(function (e) {
      console.warn('[fairway] fork unavailable', e);
      QF_STATE = 'failed';
      clearTimeout(QF_WAIT_TIMER);
      qfShowRead2();
      qfSectorState();
      qfShowIfReady();
    });
}

/* The read-back on step 2, under the website box. One line while the site is being read, the
   read when it lands, nothing when it failed (the founder is not told about our plumbing). */
function qfShowRead2() {
  var mount = document.getElementById('qf-read2');
  if (!mount) return;
  if (responses.profile_disputed) { mount.style.display = 'none'; return; }
  if (FORK_SPEC && QF_STATE === 'ready') {
    var rb = qfReadBack(FORK_SPEC);
    mount.innerHTML = rb;
    mount.style.display = rb ? 'block' : 'none';
    QF_READ_SHOWN_ON_2 = !!rb && currentStep === 2;
    return;
  }
  if (QF_STATE === 'asking') {
    mount.innerHTML = '<p class="q-help qf-wait" style="margin:0 0 6px;">' + (QF_WAIT_OVER
      ? 'Still reading your website. You can carry on; what we read shows on the next step.'
      : 'Reading your website to see what you sell and who buys it. This takes up to fifteen seconds.') + '</p>';
    mount.style.display = 'block';
    return;
  }
  if (QF_STATE === 'failed') {
    mount.innerHTML = '<p class="q-help" style="margin:0 0 6px;">We could not read that website. Pick your sector below and carry on; your comparables are chosen from the sector and your answers.</p>';
    mount.style.display = 'block';
    return;
  }
  mount.innerHTML = '';
  mount.style.display = 'none';
}

/* Called by renderStep when step 3 comes up, and again when the read lands. While the read is in
   flight the step shows one line saying so (Daniil, 20-Sep-2026: he reached step 3 before the
   profiler answered and never saw its read, so the reveal priced him on a set he was never shown).
   Nothing waits: ARR and margin are answerable immediately, and if the read never lands the step
   is exactly those two questions. */
function qfShowIfReady() {
  var mount = document.getElementById('qf-block');
  if (!mount) return false;
  if (responses.profile_disputed) { mount.style.display = 'none'; return false; }
  if (FORK_SPEC) return qfRender(FORK_SPEC);
  if (QF_STATE === 'asking') {
    mount.innerHTML = '<p class="q-help qf-wait" style="margin:0 0 8px;">Reading your website for the figures your business is priced on&hellip;</p>';
    mount.style.display = 'block';
    return false;
  }
  mount.innerHTML = '';
  mount.style.display = 'none';
  return false;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { qfQuestion: qfQuestion, qfTitleFor: qfTitleFor };
}
