/**
 * Fairway lead sink. Google Apps Script, bound to the leads spreadsheet.
 *
 * Setup is in docs/lead-capture.md. Short version:
 *   1. New Google Sheet, call it "Fairway leads"
 *   2. Extensions > Apps Script, paste this file over Code.gs
 *   3. Set NOTIFY_EMAIL and SHARED_SECRET below
 *   4. Deploy > New deployment > Web app
 *      Execute as: Me.  Who has access: Anyone.
 *   5. Copy the /exec URL into Vercel as LEAD_WEBHOOK_URL
 *      and the same secret as LEAD_SHARED_SECRET
 *
 * "Anyone" sounds alarming but the URL is unguessable and the secret check
 * below rejects anything that does not carry it. Rotate by redeploying.
 */

const SHEET_NAME = 'Leads';
const NOTIFY_EMAIL = 'daniil.rybak@gmail.com';   // where the alert goes
const SHARED_SECRET = 'change-me';               // must match LEAD_SHARED_SECRET in Vercel
const CREATE_DRAFT = true;                       // pre-draft the reviewer reply in Gmail

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);

    if (SHARED_SECRET && body.secret !== SHARED_SECRET) {
      return json({ ok: false, error: 'bad_secret' });
    }

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) sheet = ss.insertSheet(SHEET_NAME);

    // Header-aware write. The field list grows over time (exact revenue, currency,
    // recurring share and so on were added after the first leads landed), so we map each
    // field onto the column that already holds it and append genuinely new fields on the
    // right. Existing rows keep their meaning and nothing shifts underneath them.
    const fields = body.fields || [];
    const width = Math.max(sheet.getLastColumn(), 1);
    let header = sheet.getLastRow() === 0
      ? []
      : sheet.getRange(1, 1, 1, width).getValues()[0].filter(function (h) { return h !== ''; });

    if (!header.length) {
      header = fields.slice();
      sheet.getRange(1, 1, 1, header.length).setValues([header]).setFontWeight('bold');
      sheet.setFrozenRows(1);
    } else {
      const added = fields.filter(function (f) { return header.indexOf(f) === -1; });
      if (added.length) {
        sheet.getRange(1, header.length + 1, 1, added.length)
          .setValues([added]).setFontWeight('bold');
        header = header.concat(added);
      }
    }

    const row = sheet.getLastRow() + 1;
    const out = new Array(header.length).fill('');
    fields.forEach(function (f, i) {
      const col = header.indexOf(f);
      if (col > -1) out[col] = body.values[i];
    });
    sheet.getRange(row, 1, 1, out.length).setValues([out]);

    // Phone is written last, as plain text, so Sheets does not strip the leading plus.
    const phoneCol = header.indexOf('phone') + 1;
    if (phoneCol > 0) {
      sheet.getRange(row, phoneCol).setNumberFormat('@').setValue(String(out[phoneCol - 1] || ''));
    }

    const r = body.record || {};
    if (r.type === 'lead') {
      if (NOTIFY_EMAIL) notify(r);
      if (CREATE_DRAFT && r.email) createDraft(r);
    }

    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  }
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function notify(r) {
  const subject = 'Fairway lead: ' + (r.company || r.email) + ' (' + r.stage + ', ' + r.sector + ')';
  const lines = [
    'New check completed. Reply is due within 24 hours.',
    '',
    'Company:      ' + (r.company || 'not given'),
    'Email:        ' + r.email,
    'Phone:        ' + (r.phone || 'not given'),
    'Stage:        ' + r.stage,
    'Sector:       ' + r.sector + (r.sector_detail ? ' (' + r.sector_detail + ')' : ''),
    'Revenue:      ' + (r.revenue_exact_monthly ? (r.currency || 'USD') + ' ' + r.revenue_exact_monthly + '/mo (ARR ' + r.arr_exact + ')' : r.revenue),
    'Recurring:    ' + (r.recurring_pct !== '' && r.recurring_pct != null ? r.recurring_pct + '%' : 'not given'),
    'Model:        ' + (r.revenue_model || 'not given'),
    'Growth:       ' + (r.growth_pct_monthly !== '' && r.growth_pct_monthly != null ? r.growth_pct_monthly + '%/mo' : r.growth),
    'Growth notes: ' + (r.growth_detail || 'none'),
    'Profitability:' + r.profitability,
    'Raise:        ' + r.raise_band,
    'Timing:       ' + r.timing,
    'Location:     ' + [r.city, r.region, r.country].filter(Boolean).join(', '),
    '',
    'Concerns heard: ' + (r.concerns || 'none selected'),
    'Their words:    ' + (r.concern_notes || 'none'),
    'Link shared:    ' + (r.context_link || 'none'),
    '',
    'First-pass range: $' + r.range_low_m + 'M to $' + r.range_high_m + 'M',
    'Dilution spread:  ' + r.dilution_points + ' points'
  ];
  MailApp.sendEmail(NOTIFY_EMAIL, subject, lines.join('\n'));
}

/**
 * Pre-drafts the 24 hour reply so review is an edit, not a blank page.
 * The draft deliberately leaves the judgement blanks marked with [ ].
 */
function createDraft(r) {
  const subject = 'Your valuation range, reviewed';
  const body = [
    'Hi' + (r.company ? '' : '') + ',',
    '',
    'I looked at what you sent through for ' + (r.company || 'your company') + '.',
    '',
    'The first-pass range on screen was $' + r.range_low_m + 'M to $' + r.range_high_m + 'M pre-money.',
    'Having gone through it: [confirmed / I would move this to $X to $Y], because [one specific reason',
    'tied to their stage, sector, growth or margin profile].',
    '',
    (r.concerns
      ? 'You said investors have been pushing on ' + r.concerns + '. On that: [one concrete thing they can do before the next meeting].'
      : 'On the concerns you are most likely to face: [one concrete thing they can do before the next meeting].'),
    '',
    'If it is useful, the full report works through all four valuation methods, the three concerns with the',
    'evidence that answers each, and a ranked investor list with a named contact for each fund. Happy to',
    'do that under NDA if you would rather share numbers privately.',
    '',
    '[name]',
    'Fairway'
  ].join('\n');

  GmailApp.createDraft(r.email, subject, body);
}
