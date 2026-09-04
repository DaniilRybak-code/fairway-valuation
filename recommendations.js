/* Fairway's read: the fix list, drawn from the selector's own payload.
 *
 * THE CONTRACT IS selector/recommendations.py reveal_payload(). Every field this file reads is on
 * the BLOCK_FIELDS whitelist there and nothing else is passed through, so the read objects, the
 * peer values and the figure provenance stay on the engine's side of the wall and cannot arrive on
 * the page by accident. tools/recommendations_check.py is the check that keeps the two in step.
 *
 * WHAT THIS BLOCK IS. Five dimensions, each rendered as three sentences in one order and no other:
 * where the founder stands against their own named peer set, the one action to take, and the
 * valuation consequence named as a row on their own field. The third sentence is the whole reason
 * the block exists: a deck analyser can score a deck, it cannot say which fix moves which bar.
 *
 * ORDERED BY RANGE IMPACT, NOT BY RUBRIC ORDER, and the ordering is visible: each card carries the
 * turns of forward revenue that dimension moves the founder between. A founder reading top to
 * bottom is reading in the order that matters to their number, and can see why.
 *
 * A DIMENSION WITH NO EVIDENCE BEHIND IT IS ABSENT, NOT EMPTY. Retention nobody in the set
 * discloses, a margin the founder did not give: the dimension does not render, and the note says
 * how many of the five could be answered rather than letting a short list read as a thin product.
 *
 * Everything degrades. No payload, no blocks, or a fetch that never lands, and the founder simply
 * does not see the block: never an error, never a heading with nothing under it.
 *
 * Loaded after app.js, alongside investors.js.
 */

function recEsc(v) {
  return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

/* The three sentences are one paragraph each and they are never reordered or merged: the founder
   reads standing, then action, then consequence, in that order, on every dimension. */
function recCard(b) {
  const lines = (b.lines || []).slice(0, 3);
  if (lines.length !== 3) return '';
  const out = ['<div class="fxc">'];
  out.push('<div class="fxc-h"><span class="fxc-n">' + recEsc(b.rank) + '</span>'
         + '<b class="fxc-d">' + recEsc(b.dimension) + '</b>'
         /* THE IMPACT IS ON THE CARD BECAUSE IT IS THE ORDERING. Without it the list looks like a
            rubric read out in rubric order, which is the thing it deliberately is not. */
         + (b.impact ? '<span class="fxc-i">moves ' + recEsc(b.impact) + 'x of revenue</span>' : '')
         + '</div>');
  out.push('<p class="fxc-s">' + recEsc(lines[0]) + '</p>');
  out.push('<p class="fxc-a">' + recEsc(lines[1]) + '</p>');
  out.push('<p class="fxc-c">' + recEsc(lines[2]) + '</p>');
  out.push('</div>');
  return out.join('');
}

/* payload is exactly what selector/recommendations.py reveal_payload() returns. */
function renderRecommendations(payload, mountId) {
  const mount = document.getElementById(mountId || 'recommendation-blocks');
  if (!mount || !payload) return false;
  const blocks = (payload.blocks || []).filter(function (b) { return (b.lines || []).length === 3; });
  if (!blocks.length) { mount.innerHTML = ''; return false; }

  const html = ['<div class="rd wide"><b class="rd-t">' + recEsc(payload.heading) + '</b>'];
  html.push('<div class="fix-list">' + blocks.map(recCard).join('') + '</div>');
  /* HOW MANY OF THE FIVE COULD BE ANSWERED. Said before the footer, because a founder who sees
     three cards should know whether that is the product or their own missing answers. */
  if (payload.note) {
    html.push('<p class="microcopy" style="margin-top:10px;">' + recEsc(payload.note) + '</p>');
  }
  /* ON EVERY RENDERING, not as a page-level footer somebody can move. */
  html.push('<p class="microcopy fix-footer">' + recEsc(payload.footer) + '</p>');
  html.push('</div>');
  mount.innerHTML = html.join('');
  return true;
}

if (typeof window !== 'undefined') { window.renderRecommendations = renderRecommendations; }
