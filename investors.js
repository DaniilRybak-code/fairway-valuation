/* Fairway investor blocks on the reveal. Draws the two layers the selector produces.
 *
 * THE CONTRACT IS selector/investors.py reveal_payload(). Every field this file reads is on the
 * CARD_FIELDS whitelist there, and nothing else is passed through, so a column added to
 * data/investors.csv later cannot arrive on the page by accident. If this file starts reading a
 * field the whitelist does not carry, it renders nothing rather than a blank, and
 * tools/check_investor_compliance.py is the check that keeps the two in step.
 *
 * TWO LAYERS AND THEY ARE NEVER BLENDED.
 *   callable  houses writing a first cheque this size in this sector, each with a dated round we
 *             read and the label saying how far we reached to find it.
 *   evidence  the houses behind the founder's own comparables. Honestly labelled as a map, and
 *             never as a call list, because it is mostly growth stage and mostly US.
 *
 * COMPLIANCE TRAVELS WITH THE MARKUP, not with whoever remembers it: no contact details, no
 * logos (styled text wordmarks only), and the footer line on every rendering of both layers.
 *
 * Everything degrades. No payload, a payload with no callable houses, or a fetch that never
 * lands, and the founder simply does not see the block. They never see an error and they never
 * see an empty heading with nothing under it.
 *
 * Loaded after app.js.
 */

function invEsc(v) {
  return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

/* Jan-26 rather than 2026-01. The whole page dates rounds this way. */
function invMonth(iso) {
  const m = /^(\d{4})-(\d{2})/.exec(String(iso || ''));
  if (!m) return '';
  const names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  return names[parseInt(m[2], 10) - 1] + '-' + m[1].slice(2);
}

/* A LINE THAT SAYS NOTHING IS PUBLISHED IS NOT A BLANK LINE. An empty row reads as our
   omission. "First cheque not published" reads as a fact about the fund, which is what it is,
   and it is the reason Benchmark and Thrive can be on this list at all. */
function invLine(text, isNone) {
  return '<span class="ivk-line' + (isNone ? ' ivk-none' : '') + '">' + invEsc(text) + '</span>';
}

function invCallableCard(c) {
  const none = (c.not_published || []);
  const out = ['<div class="ivk">'];
  out.push('<span class="ivn-logo">' + invEsc(c.investor) + '</span>');
  out.push(invLine(c.cheque_line, none.indexOf('cheque') > -1));
  out.push(invLine(c.geography_line, none.indexOf('geography') > -1));
  if (c.recent_deal) {
    /* The round is a link to the page it was read on, because the whole promise of this block is
       that every name carries evidence a founder can check in one click. */
    const label = 'Backed <b>' + invEsc(c.recent_deal) + '</b> <em>'
                + invEsc(invMonth(c.recent_deal_date)) + '</em>';
    out.push(c.recent_deal_url
      ? '<a class="ivk-deal" rel="nofollow noopener" target="_blank" href="'
        + invEsc(c.recent_deal_url) + '">' + label + '</a>'
      : '<span class="ivk-deal">' + label + '</span>');
  }
  /* THE CAVEATS, ON THE CARD RATHER THAN IN THE FILE BEING TRUE. A cheque figure that is four
     years old and a deal that is a regional fund deployment both change what the line above
     means to the person reading it. */
  if (c.deal_note) out.push('<span class="ivk-note">' + invEsc(c.deal_note) + '</span>');
  out.push('<span class="ivk-why">' + invEsc(c.reach || '') + '</span>');
  out.push('</div>');
  return out.join('');
}

function invEvidenceChip(e) {
  return '<div class="ivc"><span class="ivn-logo">' + invEsc(e.investor) + '</span>'
       + '<span class="ivn-rounds">'
       + (e.backed ? '<i>' + invEsc(e.backed) + '</i>' : '')
       + (e.n > 1 ? '<u>+' + (e.n - 1) + ' more on your field</u>' : '')
       + '</span></div>';
}

/* payload is exactly what selector/investors.py reveal_payload() returns. */
/* ---------------------------------------------------------------------------
 * THE CHEQUE FILTER, DONE HERE BECAUSE THE RAISE IS HERE.
 *
 * Daniil, 7-Sep-2026: "can we not do the work of refining the universe of potential investors
 * without me actually seeing what amount they are raising?" Yes, and this is how.
 *
 * It is the football field's own trick. The field works because the server sends MULTIPLES and
 * this page multiplies them by a revenue figure that never leaves it. The same shape works here:
 * the server sends the candidate houses WITH THEIR PUBLISHED CHEQUE RANGES, which are our data
 * about funds and not the founder's data about themselves, and this function drops the ones that
 * cannot fund the round. The raise never leaves the browser and the filter still runs.
 *
 * THIS IS A COPY OF selector/investors._cheque_fits AND IT MUST STAY ONE. The rule and both
 * multiples arrive in the payload rather than being written here, so the server owns the rule and
 * this owns only the arithmetic. tools/check_request_boundary.py runs both sides over every
 * fixture and fails if they ever disagree.
 *
 * AN UNKNOWN CHEQUE NEVER EXCLUDES. A house that has not published a range keeps its place and
 * says "First cheque not published" on its card, exactly as it does on the paid path. Excluding on
 * an absence would quietly punish the funds that publish least.
 * ------------------------------------------------------------------------- */
function invChequeFits(card, raiseM, rule) {
  const lo = card.cheque_low_m, hi = card.cheque_high_m;
  if (!(raiseM > 0) || lo === null || lo === undefined) return true;
  return lo <= raiseM * rule.low_multiple
      && (hi === null || hi === undefined || hi >= raiseM * rule.high_multiple);
}

/* The raise as a number of millions, from the value the quiz already holds. RAISE_MIDPOINT is
   app.js's own table and is what the football field's stage row already uses, so there is one
   reading of "how much are you raising" on the page and not two. */
function invRaiseMusd() {
  if (typeof responses === 'undefined' || !responses) return null;
  if (typeof RAISE_MIDPOINT !== 'undefined' && RAISE_MIDPOINT && responses.raise) {
    const v = RAISE_MIDPOINT[responses.raise];
    if (typeof v === 'number' && isFinite(v) && v > 0) return v;
  }
  return null;
}

function renderInvestors(payload, mountId) {
  const mount = document.getElementById(mountId || 'investor-blocks');
  if (!mount || !payload) return false;
  const cal = payload.callable || {};
  const ev = payload.evidence || {};
  let cards = cal.cards || [];

  /* THE FILTER, WHEN THE SERVER ASKS FOR IT. It sends more candidates than the founder will see
     and this cuts them down. If the founder has not said what they are raising, nothing is cut and
     they simply see the top of the list, which is what they saw before this existed. */
  const rule = cal.cheque_filter;
  if (rule && rule.apply) {
    const raiseM = invRaiseMusd();
    if (raiseM > 0) {
      cards = cards.filter(function (c) { return invChequeFits(c, raiseM, rule); });
    }
    cards = cards.slice(0, rule.show || 8);
  }
  const chips = ev.chips || [];
  if (!cards.length && !chips.length) { mount.innerHTML = ''; return false; }

  const html = [];
  if (cards.length) {
    html.push('<div class="rd wide"><b class="rd-t">' + invEsc(cal.heading) + '</b>');
    html.push('<div class="inv-call">' + cards.map(invCallableCard).join('') + '</div>');
    /* NEVER PADDED, and the page says so rather than looking thin by accident.

       THE SERVER'S NOTE COUNTS WHAT IT SENT, NOT WHAT IS SHOWN. When the browser has done the
       cheque filter the two differ, and printing "14 houses match" above eight cards would be a
       plain untruth, so the note is rewritten here from the number actually on the screen. */
    const shown = cards.length;
    let note = cal.note;
    if (rule && rule.apply) {
      note = (shown < (rule.show || 8))
        ? shown + ' houses write a cheque the size of your round. We do not pad the list: a shorter '
          + 'list of houses that write your cheque is worth more than a longer one that does not.'
        : rule.note;
    }
    if (note) html.push('<p class="microcopy" style="margin-top:10px;">' + invEsc(note) + '</p>');
    html.push('</div>');
  }
  if (chips.length) {
    html.push('<div class="rd wide"><b class="rd-t">' + invEsc(ev.heading) + '</b>');
    /* THE HONEST LABEL, and it is the difference between our failure mode and vcconf's. It is
       printed before the names, not after them, because a founder reads the heading and the
       first row and then decides what this block is. */
    html.push('<p class="microcopy" style="margin:-2px 0 12px;">' + invEsc(ev.note) + '</p>');
    html.push('<div class="inv-cols">' + chips.slice(0, 9).map(invEvidenceChip).join('') + '</div>');
    html.push('</div>');
  }
  /* ON EVERY RENDERING OF BOTH LAYERS. Not a page-level footer somebody can move. */
  html.push('<p class="microcopy inv-footer">' + invEsc(payload.footer) + '</p>');
  mount.innerHTML = html.join('');
  return true;
}

if (typeof window !== 'undefined') { window.renderInvestors = renderInvestors; }

/* THE ONE EXPORT, AND IT IS FOR A CHECK. tools/request_boundary_probe.mjs requires this file so
   that tools/check_request_boundary.py can run invChequeFits beside selector/investors._cheque_fits
   over real cards and real raises, and fail if the two ever disagree. The rule lives in two places
   because the raise stays in the browser; this is what stops the two copies drifting apart.
   In the page, `module` is undefined and this block does nothing. */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { invChequeFits: invChequeFits };
}
