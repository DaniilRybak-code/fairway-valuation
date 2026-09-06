#!/usr/bin/env python3
"""StockX's gross-revenue ceiling released into the medians, on Daniil's ruling of 6 September 2026.

THE RULING, in his words (6 Sep, afternoon): "Why is StockX kept out of median? I think we ruled
many times in the last 2 days that just because the multiple is calculated of metrics that are
framed as 'more than' it cannot be excluded as it is a customary way of disclosing metrics in
financing rounds."

WHY IT WAS HELD. The row was resolved on 31-Aug-2026 from the company release of 8-Apr-2021: 2020
GAAP revenue "of over $400 million" against a $3,800m post-money, so 9.5x is a CEILING (bound <=),
and the note reasoned that part of the revenue is recognised GROSS because StockX takes possession
of goods to authenticate them. On 31 August there was no gross range for a gross ceiling to sit in,
so the row was marked in_medians=0 and the GMV reading (2.11x) was left to price. Since 5 September
(rule B3a) the engine builds a separate GROSS range, and a bounded row in it is displayed as "at
most", exactly as Owner's 23.0x ceiling already is. The reason for holding StockX out no longer
exists.

WHAT THIS CHANGES AND WHAT IT DOES NOT. in_medians 0 to 1 on one row, and a note. The multiple
(9.5), the bound (<=), the basis (GROSS_REVENUE), the GMV figures and every source URL are
untouched. Under rule B3 it prices ONLY a founder who gives a gross figure; it stays silent in every
net range. Under rule B5 the page must say "at most 9.5x".

COUNT IN, COUNT OUT. One row examined, one row changed, nothing dropped. Idempotent: a row already
carrying the note is skipped and says so.

  python3 tools/apply_stockx_release_6sep.py
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)

PATH = 'data/private-rounds-consumer.csv'
KEY = 'stockx-2021-04'
MARK = 'RELEASED 6-Sep-2026 ON DANIIL RULING'
NOTE = (
    MARK + ' (afternoon): a multiple built on a "more than" figure is a ceiling, not an exclusion; '
    'thresholds are a customary way of disclosing metrics in financing rounds. The 31-Aug hold-out '
    'existed because no gross range existed for a gross ceiling to sit in; rule B3a (5-Sep) built '
    'one. Prices the GROSS lane only, displayed as at most 9.5x (B5); silent in every net range (B3).'
)


def main():
    head = [l for l in open(PATH, encoding='utf-8') if l.startswith('#')]
    body = [l for l in open(PATH, encoding='utf-8') if not l.startswith('#')]
    rows = list(csv.DictReader(io.StringIO(''.join(body))))
    fields = list(rows[0].keys())
    n_in = len(rows)
    hits = [r for r in rows if (r.get('transaction_id') or '').strip() == KEY]
    if len(hits) != 1:
        print('REFUSED: expected exactly one row for %s, found %d. Nothing changed.' % (KEY, len(hits)))
        return 1
    r = hits[0]
    if MARK in (r.get('notes') or ''):
        print('ALREADY APPLIED: %s already carries the 6-Sep note. Nothing changed.' % KEY)
        return 0
    before = (r.get('in_medians'), r.get('mult'), r.get('bound'), r.get('revenue_basis'), r.get('gmv_mult') or r.get('ev_gmv_x'))
    r['in_medians'] = '1'
    r['notes'] = ((r.get('notes') or '').strip() + ' ' + NOTE).strip()
    print('CHANGED  %s' % KEY)
    print('   in_medians    %s -> %s' % (before[0], r['in_medians']))
    print('   mult          %s (unchanged), bound %s (unchanged), basis %s (unchanged)'
          % (before[1], before[2], before[3]))
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    open(PATH, 'w', encoding='utf-8').write(''.join(head) + out.getvalue())
    check = list(csv.DictReader(io.StringIO(''.join(
        l for l in open(PATH, encoding='utf-8') if not l.startswith('#')))))
    print('COUNT IN %d rows, COUNT OUT %d rows, changed 1, dropped %d.' % (n_in, len(check), n_in - len(check)))
    return 0 if len(check) == n_in else 1


if __name__ == '__main__':
    sys.exit(main())
