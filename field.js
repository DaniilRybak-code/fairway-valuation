/* Fairway football field.
 *
 * The visual layer for the range. Kept separate from the funnel because this is the
 * component that grows: today it draws the last-round marker, the indicative range
 * and a locked EBITDA line, and it will grow to the full two-block field.
 *
 * Loaded after app.js, which declares `responses`, `money` and `escapeHtml`.
 */

/* ---------------- the football field, first two lines ----------------
   Line one is the last round, plotted as a diamond. It is a marker and nothing more:
   no calculation reads it, which is the point. A field that lets the last price set
   the next price is not a field, it is an echo.

   Locked rows render at a fixed decorative position, never their true one, so a
   founder with a ruler cannot read the answer off the screen. The axis is scaled from
   the visible rows only, for the same reason. */

function ffScale(vals) {
  const lo = Math.min.apply(null, vals);
  const hi = Math.max.apply(null, vals);
  const span = Math.max(hi - lo, hi * 0.2, 0.1);
  return { lo: Math.max(0, lo - span * 0.22), hi: hi + span * 0.22 };
}

function ffRow(label, inner, locked) {
  return '<div class="ff-row' + (locked ? ' locked' : '') + '">' +
    '<div class="ff-label">' + escapeHtml(label) + (locked ? '<span class="lock-tag">Locked</span>' : '') + '</div>' +
    '<div class="ff-track">' + inner + '</div></div>';
}

function renderField(r) {
  const wrap = document.getElementById('ff');
  if (!wrap) return;

  const plotted = [r.low, r.high];
  if (r.markerM) plotted.push(r.markerM);
  const s = ffScale(plotted);
  const pct = v => ((v - s.lo) / (s.hi - s.lo)) * 100;

  let html = '';

  if (r.markerM) {
    const at = pct(r.markerM);
    const when = responses.last_round_date ? ', ' + prettyMonth(responses.last_round_date) : '';
    const kind = responses.last_round_type === 'SAFE or note cap' ? 'cap' : 'pre-money';
    html += ffRow('Last round',
      '<div class="ff-line"></div>' +
      '<div class="ff-diamond" style="left:' + at.toFixed(2) + '%" ' +
      'title="' + escapeHtml(money(r.markerM) + ' ' + kind + when) + '"></div>' +
      '<div class="ff-point-label" style="left:' + at.toFixed(2) + '%">' +
      escapeHtml(money(r.markerM)) + '</div>', false);
  }

  html += ffRow('Indicative range',
    '<div class="ff-line"></div>' +
    '<div class="ff-bar" style="left:' + pct(r.low).toFixed(2) + '%;width:' +
    (pct(r.high) - pct(r.low)).toFixed(2) + '%"></div>', false);

  if (r.ebitdaM) {
    /* Decorative position. Deliberately not where the answer is. */
    html += ffRow('EBITDA multiple',
      '<div class="ff-line"></div><div class="ff-bar redacted" style="left:28%;width:34%"></div>', true);
  }

  document.getElementById('ff-rows').innerHTML = html;
  document.getElementById('ff-lo').textContent = money(s.lo);
  document.getElementById('ff-hi').textContent = money(s.hi);

  const foot = [];
  if (r.markerM) foot.push('The diamond is your last round, plotted for comparison. It is not an input to the range.');
  if (r.ebitdaM) foot.push('You are profitable, so an EBITDA multiple applies as a second independent lens. That line and its peer set are in the report.');
  document.getElementById('ff-foot').textContent = foot.join(' ');

  wrap.style.display = (r.markerM || r.ebitdaM) ? 'block' : 'none';
}

function prettyMonth(ym) {
  if (!/^\d{4}-\d{2}$/.test(ym)) return ym;
  const months = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'];
  const p = ym.split('-');
  return months[Number(p[1]) - 1] + ' ' + p[0];
}
