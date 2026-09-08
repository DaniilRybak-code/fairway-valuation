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
  out.push('</label>');
  if (q.why) out.push('<p class="q-help" style="margin:2px 0 8px;">' + qfEsc(q.why) + '</p>');

  if (q.kind === 'choice' && q.options && q.options.length) {
    out.push('<div class="opt-grid">');
    q.options.forEach(function (o) {
      var val = qfEsc(typeof o === 'string' ? o : (o.value || o.label));
      var lab = qfEsc(typeof o === 'string' ? o : (o.label || o.value));
      out.push('<button type="button" class="opt" data-q="' + qfEsc(q.key) + '" data-v="' + val
             + '" onclick="qfPickChoice(this)">' + lab + '</button>');
    });
    out.push('</div>');
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
    out.push('<input class="field field-num" id="' + id + '" type="number" step="1" min="0"'
           + ' inputmode="numeric" placeholder="' + qfEsc(q.placeholder || '') + '"'
           + ' oninput="qfChanged()" aria-label="' + qfEsc(q.label) + '">');
    if (q.unit) out.push('<span class="unit">' + qfEsc(q.unit) + '</span>');
    out.push('</div>');
  }
  out.push('</div>');
  return out.join('');
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
  var sells = (r.sells || '').split('|').filter(Boolean).slice(0, 4).join(', ');
  var bits = [];
  if (sells) bits.push('you sell ' + sells.toLowerCase());
  if (r.industry && r.industry !== 'Horizontal') bits.push('into ' + r.industry.toLowerCase());
  if (!bits.length) return '';
  var out = '<p class="q-help" style="margin:-6px 0 16px;">We read your site as: <b>' + qfEsc(bits.join(', '))
          + '</b>. That decides what we ask and who you are compared against. '
          + '<button type="button" class="link-btn" onclick="qfWrongRead()">That is not right</button></p>';
  if (!spec.site_read && spec.site_note) {
    out += '<p class="q-help" style="margin:-10px 0 16px;">We could not read your website ('
         + qfEsc(spec.site_note) + '), so this is from your answers alone.</p>';
  }
  return out;
}

/* If the read is wrong, we do not argue and we do not guess again. They get the plain revenue
   question, which is what every founder got before today, and the reviewer sees the note. */
function qfWrongRead() {
  responses.profile_disputed = true;
  track('quiz_profile_disputed', { fork: FORK_SPEC && FORK_SPEC.fork });
  FORK_SPEC = null;
  var mount = document.getElementById('qf-block');
  if (mount) mount.style.display = 'none';
  var plain = document.querySelector('.q-block[data-step="3"]');
  if (plain) plain.setAttribute('data-qf-fallback', '1');
  currentStep = 3;
  renderStep();
}

/* Required questions gate the Continue button, optional ones never do. */
function qfChanged() {
  var btn = document.getElementById('qf-continue');
  if (!btn || !FORK_SPEC) return;
  var missing = FORK_SPEC.questions.filter(function (q) {
    if (!q.required) return false;
    if (q.kind === 'choice') return !responses[q.key];
    return qfNum('qf-' + q.key) === null;
  });
  btn.disabled = missing.length > 0;
  btn.textContent = missing.length ? 'Answer the questions above to continue' : 'Continue';
}

function qfRender(spec) {
  FORK_SPEC = spec;
  var mount = document.getElementById('qf-block');
  if (!mount || !spec || !spec.questions || !spec.questions.length) return false;
  var html = ['<h2 class="q-title">' + qfEsc(qfTitleFor(spec.fork)) + '</h2>'];
  html.push(qfReadBack(spec));
  spec.questions.forEach(function (q) { html.push(qfQuestion(q)); });
  html.push('<button class="btn" id="qf-continue" style="width:100%; margin-top:16px;"'
          + ' onclick="qfSubmit()">Continue</button>');
  mount.innerHTML = html.join('');
  mount.style.display = 'block';
  /* Money questions are in the founder's own currency, the one they already picked. */
  var cur = (typeof curSymbol === 'function') ? curSymbol() : '$';
  mount.querySelectorAll('[id$="-cur"]').forEach(function (e) { e.textContent = cur; });
  qfChanged();
  track('quiz_fork_shown', { fork: spec.fork, questions: spec.questions.length });
  return true;
}

/* The heading. One line per fork, in the founder's language rather than ours: a lender should not
   be greeted with the word "fork". */
function qfTitleFor(fork) {
  return {
    software: 'Your revenue, the way software is priced',
    marketplace: 'What goes through your marketplace, and what you keep',
    consumer_subscription: 'Your subscribers, and what they pay',
    exchange: 'What you move, and what you earn on it',
    ecommerce: 'Your sales, and what you keep after cost',
    payments: 'What you keep after interchange',
    lending: 'Your book, and how it is funded',
    media: 'Your revenue and your audience',
    delivery: 'The basket, and your share of it'
  }[fork] || 'Your numbers';
}

function qfSubmit() {
  if (!FORK_SPEC) return;
  var answered = 0;
  FORK_SPEC.questions.forEach(function (q) {
    if (q.kind === 'choice') { if (responses[q.key]) answered++; return; }
    var v = qfNum('qf-' + q.key);
    if (v !== null) { responses[q.key] = v; answered++; }
  });
  responses.fork = FORK_SPEC.fork;
  /* ANSWERED, NEVER THE ANSWERS. The event carries how many questions were filled in and which
     fork, because that is what tells us whether a fork is too long. It carries no figure. */
  track('quiz_answer', { step: 3, key: 'fork_answers', fork: FORK_SPEC.fork, answered: answered });
  currentStep = 4;
  renderStep();
}

/* ASKED ONCE, AFTER STEP 2, AND THE FOUNDER NEVER WAITS ON IT. The call is started as soon as the
   sector and website are in, and the page carries on. If it lands before they reach step 3 they get
   their fork; if it does not, they get the plain revenue question and the quiz is exactly what it
   was yesterday. Nothing about this is allowed to hold a founder up. */
function qfAsk() {
  if (FORK_ASKED) return;
  FORK_ASKED = true;
  var body = (typeof buildRevealRequest === 'function') ? buildRevealRequest(responses) : null;
  if (!body) return;
  fetch('/api/profile', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body)
  })
    .then(function (r) { return r.json(); })
    .then(function (spec) {
      if (!spec || !spec.questions || !spec.questions.length) return;
      if (responses.profile_disputed) return;
      FORK_SPEC = spec;
      if (currentStep === 3) qfShowIfReady();
    })
    .catch(function (e) { console.warn('[fairway] fork unavailable', e); });
}

/* Called by renderStep when step 3 comes up: draw the fork if we have one, otherwise leave the
   page's own revenue question exactly where it is. */
function qfShowIfReady() {
  var plain = document.querySelector('.q-block[data-step="3"]');
  var mount = document.getElementById('qf-block');
  if (!FORK_SPEC || responses.profile_disputed) {
    if (mount) mount.style.display = 'none';
    return false;
  }
  if (!qfRender(FORK_SPEC)) return false;
  if (plain) plain.style.display = 'none';
  return true;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { qfQuestion: qfQuestion, qfTitleFor: qfTitleFor };
}
