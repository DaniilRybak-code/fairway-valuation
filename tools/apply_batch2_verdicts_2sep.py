#!/usr/bin/env python3
"""
Applies what the second private batch (rows 123-195, 12 screenshots, 02-Sep-2026) changed, after
each disagreement was checked against live sources.

Only four rows move. Everything else in the overlap either agreed or was checked and ours held.
"""
import csv, io, sys

MAIN, CONS = 'data/private-rounds.csv', 'data/private-rounds-consumer.csv'

MAIN_EDITS = {
  ('Salesloft', '2019-04'): {
    'fields': {
      'post_money_musd': '600.0',
      'valuation_status': 'Reported (press sourcing, company declined to confirm)',
      'revenue_metric': 'ARR',
      'revenue_musd': '50.0',
      'revenue_status': 'Reported (CEO on the record)',
      'ev_revenue_x': '12.0',
      'in_medians': '0',
      'revenue_period': 'RUN_RATE',
      'revenue_basis': 'ARR',
      'denominator_basis': 'REPORTED_CONTEMPORANEOUS',
      'valuation_basis': 'REVENUE',
      'round_source_url': 'https://techcrunch.com/2019/04/25/salesloft-funding/',
      'revenue_source_url': 'https://getlatka.com/blog/salesloft-revenue-hits-50m-will-be-ipo-ready-in-2020-with-140m-raised/',
    },
    'note': ("PRICED 02-Sep-2026, PREVIOUSLY A ROUND WITH NO VALUATION AND NO DENOMINATOR. Neither "
             "number is company-confirmed and the row is DISPLAY ONLY, out of medians. Valuation: "
             "TechCrunch of 25-Apr-2019, 'This round gives it a valuation of $600 million, according "
             "to TechCrunch, although the company is declining to comment on that'; the CEO would say "
             "only that it was more than double the previous round and less than $1bn. Denominator: "
             "CEO Kyle Porter on the record, 'we're sitting around the 50 million mark', recorded "
             "25-Jul-2019, three months after the round, and a March-2019 post seven weeks BEFORE the "
             "round already reported Salesloft crossing $50m ARR, so the figure brackets the pricing "
             "date on both sides. 600/50 gives 12.0x, which is what Daniil's sheet carries."),
  },
}

CONS_EDITS = {
  ('GOAT Group', '2021-06'): {
    'fields': {'ev_gmv_x': '1.85'},
    'note': ("ROUNDING CORRECTED 02-Sep-2026, from 1.9x to 1.85x. 3700 over 2000 is 1.85 exactly. "
             "Daniil's sheet carries 1.85x and it is right; ours was carrying a rounded 1.9x."),
  },
  ('Trendyol', '2021-08'): {
    'fields': {'ev_gmv_x': '1.65'},
    'note': ("VOLUME MULTIPLE FILLED 02-Sep-2026 FROM NUMBERS WE ALREADY HELD. The row carried a "
             "$16.5bn post-money and $10bn of FY2021E GMV and no multiple, so it displayed nothing. "
             "16500 over 10000 is 1.65x, which is what Daniil's sheet carries. Revenue was never "
             "published, so this row prices on volume or not at all."),
  },
}

NEW_MAIN = [
 {
  'transaction_id': 'anthropic-2024-01', 'company_key': 'anthropic', 'company_name': 'Anthropic',
  'date': 'Jan-24', 'date_iso': '2024-01', 'round_type': 'Series D (Menlo Ventures SPV)',
  'capital_raised_musd': '750.0', 'post_money_musd': '18400.0',
  'valuation_status': 'Reported (never announced by Anthropic)',
  'revenue_metric': 'Run-rate revenue', 'revenue_musd': '87.0',
  'revenue_status': 'Disclosed (company, retrospective, describes this date)',
  'ev_revenue_x': '211.5',
  'subsector_as_supplied': 'Foundation models / generative AI',
  'screening_category_as_supplied': 'Data, AI & Developer Tools',
  'lead_key_investors': 'Menlo Ventures (lead, via SPV); Lightspeed; Alkeon Capital; Manhattan Venture Partners',
  'round_source_url': 'https://www.forbes.com/sites/alexkonrad/2024/01/11/anthropic-750million-funding-round-menlo-ventures/',
  'revenue_source_url': 'https://www.anthropic.com/news/anthropic-expands-global-leadership-in-enterprise-ai-naming-chris-ciauri-as-managing-director-of',
  'transaction_type': 'PRIMARY', 'denominator_basis': 'DISCLOSED_ACTUAL', 'bound': '',
  'in_medians': '1', 'verification': 'VERIFIED', 'revenue_basis': 'ARR_RUNRATE',
  'revenue_period': 'RUN_RATE', 'valuation_basis': 'REVENUE', 'revenue_basis_source': 'STATED',
  'growth_band': 'HYPER', 'growth_band_basis': 'STATED',
  'notes': ("INSERTED 02-Sep-2026 at Daniil's instruction: 'earlier stages (where there is a "
            "denominator) could be used for earlier stage companies, not necessarily Series F'. This "
            "is the EARLIEST Anthropic round that can be priced at all, and it is the one an "
            "early-stage founder should meet. Valuation: Forbes of 11-Jan-2024, '$750 million in new "
            "funding that would nearly quadruple its valuation to $18.4 billion'. Forbes says the "
            "round 'remains in progress' on that date; TechCrunch of 23-Jun-2026, writing up Menlo's "
            "next fund, confirms it closed: Menlo 'preemptively' led Anthropic's Series D and 'that "
            "round quadrupled the startup's valuation to $18 billion'. Denominator: Anthropic's own "
            "newsroom, 'our run-rate revenue has grown from $87 million at the start of 2024 to over "
            "$5 billion in August 2025'. That figure is published later but DESCRIBES this moment, "
            "which is what our hindsight rule asks for; it is the same shape as a filed account. "
            "18400/87 gives 211.5x. NOT priced, and correctly so: the Series B of Apr-2022 and the "
            "Google investment of Feb-2023 have no disclosed valuation, and the Series C of May-2023 "
            "has no revenue figure describing it. Amazon's 2023 and 2024 money went in as convertible "
            "notes with no stated valuation, per Amazon's own 10-Q, so none of it is a priced round."),
 },
]


def load(path):
    raw = open(path).read().split('\n')
    head = [l for l in raw if l.startswith('#')]
    body = '\n'.join([l for l in raw if not l.startswith('#') and l.strip()])
    rows = list(csv.DictReader(io.StringIO(body)))
    return head, rows, list(rows[0].keys())


def save(path, head, rows, cols):
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow({c: r.get(c, '') for c in cols})
    open(path, 'w').write('\n'.join(head) + '\n' + out.getvalue())


def apply_to(path, edits, new_rows=None):
    head, rows, cols = load(path)
    hit = 0
    for r in rows:
        key = (r.get('company_name'), (r.get('date_iso') or '')[:7])
        if key in edits:
            e = edits[key]
            for k, v in e['fields'].items():
                if k not in cols: print('ERROR: unknown column %r in %s' % (k, path)); sys.exit(1)
                print('  %-12s %-8s %-22s %r -> %r' % (key[0], key[1], k, r.get(k), v))
            r.update(e['fields'])
            r['notes'] = e['note'] + ' || ' + (r.get('notes') or '')
            hit += 1
    if hit != len(edits):
        print('ERROR: matched %d of %d in %s' % (hit, len(edits), path)); sys.exit(1)
    for nr in (new_rows or []):
        if nr['transaction_id'] in {r['transaction_id'] for r in rows}:
            print('ERROR: %s exists' % nr['transaction_id']); sys.exit(1)
        for k in nr:
            if k not in cols: print('ERROR: unknown column %r' % k); sys.exit(1)
        rows.append({c: nr.get(c, '') for c in cols})
        print('  INSERTED %s  %s at %s post-money on %s, %sx'
              % (nr['transaction_id'], nr['round_type'], nr['post_money_musd'],
                 nr['revenue_musd'], nr['ev_revenue_x']))
    save(path, head, rows, cols)
    return len(rows)

print('--- %s' % MAIN); n1 = apply_to(MAIN, MAIN_EDITS, NEW_MAIN)
print('--- %s' % CONS); n2 = apply_to(CONS, CONS_EDITS)
print('\n%s %d rows, %s %d rows' % (MAIN, n1, CONS, n2))
