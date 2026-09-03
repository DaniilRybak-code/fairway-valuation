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
function renderInvestors(payload, mountId) {
  const mount = document.getElementById(mountId || 'investor-blocks');
  if (!mount || !payload) return false;
  const cal = payload.callable || {};
  const ev = payload.evidence || {};
  const cards = cal.cards || [];
  const chips = ev.chips || [];
  if (!cards.length && !chips.length) { mount.innerHTML = ''; return false; }

  const html = [];
  if (cards.length) {
    html.push('<div class="rd wide"><b class="rd-t">' + invEsc(cal.heading) + '</b>');
    html.push('<div class="inv-call">' + cards.map(invCallableCard).join('') + '</div>');
    /* NEVER PADDED, and the page says so rather than looking thin by accident. */
    if (cal.note) html.push('<p class="microcopy" style="margin-top:10px;">'
                            + invEsc(cal.note) + '</p>');
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
