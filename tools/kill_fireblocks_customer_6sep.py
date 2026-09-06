#!/usr/bin/env python3
"""Fireblocks' per-customer reading killed, on Daniil's ruling of 6 September 2026.

HIS WORDS: "Let's kill Fireblocks user multiple, looks to be a B2B business, they do not price on
number of customers."

WHY IT SURFACED. He asked what the 20,588x per-user comparable was. It is unifold's chart, holding
Fireblocks at $10,000,000 of enterprise value per customer next to MoonPay at $486. Fireblocks had
roughly 800 institutional clients against an $8bn post-money; MoonPay had roughly 7 million retail
consumers against $3.4bn. Both arithmetic is right and the comparison is meaningless.

TWO SEPARATE FIXES CAME OUT OF THAT QUESTION AND THIS IS THE SECOND.

The first was general: a round whose buyer is CONSUMER now counts consumers and every other round
counts businesses, using the `buyer` field the data already carried. That split the CUSTOMERS basis
in two and took the median spread on the per-user charts from 33x to 12.6x.

This script is the specific one, and it goes further than the split. The split would still show
Fireblocks against other business-customer rounds. Daniil's ruling is that Fireblocks should not
carry a per-customer multiple AT ALL: an institutional custody and settlement business is not
bought for its client count, so the figure is not a valuation measure for this company however it is
banded. That is a judgement about the business, which is his to make and not something a spread
threshold would ever have caught.

WHAT IS REMOVED, AND WHAT IS NOT. Only the count reading goes: `vol_metric`, `vol_value` and the
per-unit multiple. The revenue multiple, the post-money, the denominator, the dates and every source
URL are untouched, so Fireblocks stays a comparable on the lane it belongs on and stops being one on
the lane it does not. Nothing is deleted from the file; the rows stay, with a note saying why the
count reading is gone.

Both Fireblocks rows are treated the same way (Jul-21 and Jan-22), because the ruling is about the
business and not about one round.

COUNT IN, COUNT OUT, and the note names what changed. Idempotent.

  python3 tools/kill_fireblocks_customer_6sep.py
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)

PATH = 'data/private-rounds.csv'
COMPANY = 'fireblocks'
MARK = 'PER-CUSTOMER READING KILLED 6-Sep-2026 ON DANIIL RULING'
NOTE = (' ' + MARK + ': "looks to be a B2B business, they do not price on number of customers". '
        'The row carried a count of institutional clients, which produced $10m of enterprise value '
        'per customer beside MoonPay at $486 for 7 million retail consumers. An institutional '
        'custody and settlement business is not bought for its client count, so the reading is not '
        'a valuation measure here at any band. The count fields are cleared; the revenue multiple, '
        'the post-money, the denominator and every source URL are untouched.')

# The count reading and nothing else.
CLEAR = ('vol_metric', 'vol_value', 'volume_metric', 'volume_value', 'gmv_mult', 'vol_periodic',
         'vol_unit', 'volume_basis')


def main():
    head = [l for l in open(PATH) if l.startswith('#')]
    body = [l for l in open(PATH) if not l.startswith('#')]
    rows = list(csv.DictReader(io.StringIO(''.join(body))))
    fields = list(rows[0].keys())
    n_in = len(rows)

    targets = [r for r in rows if (r.get('company_key') or '').strip().lower() == COMPANY]
    if not targets:
        print('REFUSED: no rows with company_key %r. Nothing changed.' % COMPANY)
        return 1
    if all(MARK in (r.get('notes') or '') for r in targets):
        print('ALREADY APPLIED: all %d Fireblocks rows carry the note. Nothing changed.' % len(targets))
        return 0

    changed = 0
    for r in targets:
        if MARK in (r.get('notes') or ''):
            continue
        before = {k: r.get(k) for k in CLEAR if (r.get(k) or '').strip()}
        for k in CLEAR:
            if k in r:
                r[k] = ''
        r['notes'] = ((r.get('notes') or '').strip() + NOTE).strip()
        changed += 1
        print('CHANGED  %s %s' % (r.get('company_name'), r.get('date')))
        for k, v in sorted(before.items()):
            print('   cleared  %-16s was %s' % (k, v))
        print('   kept     mult %s | post-money %s | revenue %s'
              % (r.get('mult'), r.get('post_money_musd'), r.get('revenue_musd')))

    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    open(PATH, 'w').write(''.join(head) + out.getvalue())

    back = list(csv.DictReader(io.StringIO(''.join(
        l for l in open(PATH) if not l.startswith('#')))))
    print('\nCOUNT IN %d rows, COUNT OUT %d rows, changed %d, dropped %d.'
          % (n_in, len(back), changed, n_in - len(back)))
    return 0 if len(back) == n_in else 1


if __name__ == '__main__':
    sys.exit(main())
