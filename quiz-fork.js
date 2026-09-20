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
  if (q.why) out.push('<p class="q-info" id="' + id + '-why" hidden>' + qfEsc(q.why) + '</p>');

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
  var mount = document.getElementById('qf-block');
  if (mount) { mount.innerHTML = ''; mount.style.display = 'none'; }
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
var QF_ALREADY_ASKED = { arr: true };

function qfRender(spec) {
  FORK_SPEC = spec;
  var mount = document.getElementById('qf-block');
  if (!mount || !spec || !spec.questions) return false;
  var qs = spec.questions.filter(function (q) { return !QF_ALREADY_ASKED[q.key]; });
  var html = [qfReadBack(spec)];
  if (qs.length) {
    html.push('<p class="field-label" style="margin:6px 0 8px;">' + qfEsc(qfTitleFor(spec.fork))
            + ' <span class="optional">Optional. Give what you have.</span></p>');
    qs.forEach(function (q) { html.push(qfQuestion(q)); });
  }
  mount.innerHTML = html.join('');
  mount.style.display = html.join('').trim() ? 'block' : 'none';
  var cur = (typeof curSymbol === 'function') ? curSymbol() : '$';
  mount.querySelectorAll('[id$="-cur"]').forEach(function (e) { e.textContent = cur; });
  qfChanged();
  track('quiz_fork_shown', { fork: spec.fork, questions: qs.length });
  return true;
}

/* The heading. One line per fork, in the founder's language rather than ours: a lender should not
   be greeted with the word "fork". */
function qfTitleFor(fork) {
  return {
    software: 'More on how software is priced',
    marketplace: 'What goes through your marketplace',
    consumer: 'Your subscribers and users',
    consumer_subscription: 'Your subscribers and users',
    exchange: 'What you move, and what you earn on it',
    ecommerce: 'Your sales and what you keep',
    payments: 'What you keep after interchange',
    lending: 'Your book, and how it is funded',
    media: 'Your revenue and your audience',
    delivery: 'The basket, and your share of it'
  }[fork] || 'More figures';
}

function qfSubmit() {
  if (!FORK_SPEC) return;
  var answered = 0;
  FORK_SPEC.questions.forEach(function (q) {
    if (QF_ALREADY_ASKED[q.key]) return;
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

function qfAsk() {
  if (FORK_ASKED) return;
  FORK_ASKED = true;
  var body = (typeof buildRevealRequest === 'function') ? buildRevealRequest(responses) : null;
  if (!body) return;
  QF_STATE = 'asking';
  fetch('/api/profile', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body)
  })
    .then(function (r) { return r.json(); })
    .then(function (spec) {
      if (!spec || !spec.questions) { QF_STATE = 'failed'; qfShowIfReady(); return; }
      if (responses.profile_disputed) return;
      FORK_SPEC = spec;
      QF_STATE = 'ready';
      if (currentStep === 3) qfShowIfReady();
    })
    .catch(function (e) {
      console.warn('[fairway] fork unavailable', e);
      QF_STATE = 'failed';
      qfShowIfReady();
    });
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
