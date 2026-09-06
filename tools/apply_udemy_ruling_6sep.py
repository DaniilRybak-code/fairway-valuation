#!/usr/bin/env python3
"""Udemy released into the medians, on Daniil's ruling of 6 September 2026.

THE RULING, in his words: "Why Udemy is held back? If this was an all-share transaction, calculate
the value based on the acquirer's share price at transaction and then the implied multiples."

WHY IT WAS HELD. The row was written on 5-Sep with in_medians=0 and the reason "no standalone price
exists in the release, only an exchange ratio, a combined implied equity value and an ownership
split". That reason was wrong, and reading the release again is what shows it.

WHAT THE RELEASE ACTUALLY SAYS, quoted from the 8-K exhibit already cited in the row
(https://www.sec.gov/Archives/edgar/data/1651562/000114036125045770/ef20061429_ex99-1.htm):

  "Udemy stockholders will receive 0.800 shares of Coursera common stock for each share of Udemy
   common stock"

  "Based on the closing prices of Coursera and Udemy common stock on December 16, 2025, the implied
   equity value of the combined company is approximately $2.5 billion."

  "Upon the closing of the transaction, existing Coursera stockholders are expected to own
   approximately 59% and existing Udemy stockholders are expected to own approximately 41% of the
   combined company, on a fully diluted basis."

SO THE FIGURE WE ALREADY HOLD IS DANIIL'S METHOD, WRITTEN THE OTHER WAY ROUND. The $2.5bn is struck
on the acquirer's own market price on the transaction date, in the release's own words. 41 per cent
of it, $1,025m, is therefore the market value of the stock consideration Udemy holders receive,
priced off Coursera's share price at the transaction, which is exactly what he asked for. It is not
a modelled or negotiated number; it is arithmetic on two figures the company published together.

THE ONE THING TO BE HONEST ABOUT, and it is written into the row rather than smoothed over. The
purest form of the calculation is (0.800 x Udemy fully diluted shares) x Coursera's 16-Dec-2025
closing price. The release states neither the share count nor the closing price, so that form cannot
be computed from it. The two constructions should agree closely, because the $2.5bn was struck on
those same closing prices, but they are not identical: the 41 per cent is a fully diluted ownership
split of the COMBINED company. Anyone who later finds the share count and the closing price should
recompute and compare; if the two disagree materially, this row is the one that is wrong.

IT PRICES ON THE GROSS LANE AND ONLY THERE. Udemy books marketplace revenue gross of instructor
payouts, so revenue_basis is GROSS_REVENUE and rule B3a puts it in the gross range, never the net
one. Released, it is evidence for a founder who gives a gross figure and invisible to one who does
not, which is the whole point of the 5-Sep change.

COUNT IN, COUNT OUT. One row examined, one row changed, nothing dropped. The multiple, the
denominator and every source URL are untouched: this ruling changes in_medians and adds a note, and
nothing else.

Idempotent: a row already carrying the note is skipped and says so.

  python3 tools/apply_udemy_ruling_6sep.py
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)

PATH = 'data/private-rounds.csv'
KEY = 'udemy-2025-12'
MARK = 'RELEASED 6-Sep-2026 ON DANIIL RULING'

NOTE = (
    'HELD 5-Sep, ' + MARK + ': "if this was an all-share transaction, calculate the value based on '
    'the acquirer\'s share price at transaction and then the implied multiples". THE NOTE, and it '
    'is the whole reason this row was held: the release states no standalone price for Udemy. It '
    'states an exchange ratio of 0.800 Coursera shares per Udemy share, a combined implied equity '
    'value of approximately $2.5bn "based on the closing prices of Coursera and Udemy common stock '
    'on December 16, 2025", and a 41 per cent fully diluted ownership share for Udemy holders. '
    '41 per cent of $2.5bn is $1,025m, and because the $2.5bn is struck on the acquirer\'s own '
    'market price at the transaction date, that IS the value of the stock consideration measured '
    'the way Daniil asked for. The purest form of the same calculation, 0.800 x Udemy fully diluted '
    'shares x Coursera\'s 16-Dec-2025 close, cannot be computed from the release, which states '
    'neither figure; the two should agree closely and this row is the one that is wrong if they do '
    'not. Prices on the GROSS lane only (marketplace revenue is booked gross of instructor '
    'payouts), so under rule B3a it reaches a founder who gives a gross figure and no other.'
)


def main():
    lines = open(PATH).read().split('\n')
    hits = 0
    for i, line in enumerate(lines):
        if KEY not in line:
            continue
        hits += 1
        if MARK in line:
            print('ALREADY APPLIED: %s already carries the 6-Sep note. Nothing changed.' % KEY)
            return 0
    if hits != 1:
        print('REFUSED: expected exactly one row for %s, found %d. Nothing changed.' % (KEY, hits))
        return 1

    import csv
    import io
    head = [l for l in open(PATH) if l.startswith('#')]
    body = [l for l in open(PATH) if not l.startswith('#')]
    rows = list(csv.DictReader(io.StringIO(''.join(body))))
    fields = list(rows[0].keys())
    n_in = len(rows)

    changed = 0
    for r in rows:
        if (r.get('transaction_id') or '').strip() != KEY:
            continue
        before = (r.get('in_medians'), r.get('mult'), r.get('revenue_musd'), r.get('post_money_musd'))
        r['in_medians'] = '1'
        r['notes'] = ((r.get('notes') or '').strip() + ' ' + NOTE).strip()
        after = (r.get('in_medians'), r.get('mult'), r.get('revenue_musd'), r.get('post_money_musd'))
        changed += 1
        print('CHANGED  %s' % KEY)
        print('   in_medians   %s -> %s' % (before[0], after[0]))
        print('   mult         %s (unchanged)' % after[1])
        print('   revenue      %s (unchanged)' % after[2])
        print('   post-money   %s (unchanged)' % after[3])

    if changed != 1:
        print('REFUSED: matched %d rows on transaction_id, expected 1. Nothing written.' % changed)
        return 1

    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    open(PATH, 'w').write(''.join(head) + out.getvalue())

    check = list(csv.DictReader(io.StringIO(''.join(
        l for l in open(PATH) if not l.startswith('#')))))
    print()
    print('COUNT IN %d rows, COUNT OUT %d rows, changed %d, dropped %d.'
          % (n_in, len(check), changed, n_in - len(check)))
    return 0 if len(check) == n_in else 1


if __name__ == '__main__':
    sys.exit(main())
