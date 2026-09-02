#!/usr/bin/env python3
"""
Part two of the 2-Sep-2026 rulings: the consumer file.

Also fixes a SCHEMA GAP found while doing it. data/private-rounds-consumer.csv has a
round_source_url column but NO revenue_source_url, so not one of its 51 rows can say where
its revenue figure came from. The column is added here, empty everywhere except Gorillas.
Filling the other 50 is a job for the sourcing list.
"""
import csv, io, sys

CONS = 'data/private-rounds-consumer.csv'

EDITS = {
  ('Gorillas', '2021-10'): {
    'fields': {
      'round_source_url': 'https://www.cnbc.com/2021/10/19/delivery-hero-leads-1-billion-investment-in-grocery-start-up-gorillas.html',
      'revenue_source_url': 'https://www.cnbc.com/2021/10/19/delivery-hero-leads-1-billion-investment-in-grocery-start-up-gorillas.html',
    },
    'note': ("SOURCES ADDED 02-Sep-2026, NUMBERS UNCHANGED AND CONFIRMED. This was the one row of the "
             "nineteen disagreements carrying no revenue source, and the reason turned out to be "
             "structural: this file had no revenue_source_url column at all. Both figures come from CNBC "
             "of 19-Oct-2021, the day of the round: 'Gorillas is now valued at $3.1 billion following the "
             "cash injection' and 'Gorillas says it now has a run rate of $300 million, meaning it expects "
             "to make that much revenue on an annual basis.' TechCrunch the same day carries the OTHER "
             "number: 'It's now being valued at $2.1 billion, pre-money.' Pre-money plus the close-to-$1bn "
             "raise reconciles to the $3.1bn post-money, so the two reports agree rather than conflict. "
             "Daniil's database shows post-money 3,100 in its valuation cell but a 7.0x multiple, which is "
             "2,100 over 300, so that multiple was computed off the pre-money. Ours is 3,100 over 300 and "
             "stands at 10.3x, a ceiling because Gorillas said MORE than $300m."),
  },
}

raw = open(CONS).read().split('\n')
head = [l for l in raw if l.startswith('#')]
body = '\n'.join([l for l in raw if not l.startswith('#') and l.strip()])
rows = list(csv.DictReader(io.StringIO(body)))
cols = list(rows[0].keys())

if 'revenue_source_url' not in cols:
    cols.insert(cols.index('round_source_url') + 1, 'revenue_source_url')
    for r in rows:
        r['revenue_source_url'] = ''
    print('ADDED COLUMN revenue_source_url, empty on all %d rows' % len(rows))

hit = 0
for r in rows:
    key = (r.get('company_name'), (r.get('date_iso') or '')[:7])
    if key in EDITS:
        e = EDITS[key]
        for k, v in e['fields'].items():
            if k not in cols:
                print('ERROR: unknown column %r' % k); sys.exit(1)
            print('  %-10s %-8s %-20s %r -> %r' % (key[0], key[1], k, r.get(k), v))
        r.update(e['fields'])
        r['notes'] = e['note'] + ' || ' + (r.get('notes') or '')
        hit += 1

if hit != len(EDITS):
    print('ERROR: matched %d of %d' % (hit, len(EDITS))); sys.exit(1)

out = io.StringIO()
w = csv.DictWriter(out, fieldnames=cols)
w.writeheader()
for r in rows:
    w.writerow({c: r.get(c, '') for c in cols})
open(CONS, 'w').write('\n'.join(head) + '\n' + out.getvalue())
print('\n%s rewritten, %d rows, %d columns' % (CONS, len(rows), len(cols)))
