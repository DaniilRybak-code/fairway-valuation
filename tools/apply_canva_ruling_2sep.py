#!/usr/bin/env python3
"""
Daniil's ruling of 02-Sep-2026 on Canva Apr-24: "price it off the number that was published by
the company".

Canva's own number, published 24-May-2024, is "more than US$2.2 billion in annualised revenue".
That is the company's figure, not a press estimate and not the phantom 2,300 or 3,300 that came
from the AUD translation A$3.3bn sitting in the same sentence.

  post-money 26,000 / 2,200 = 11.8x

TWO THINGS TRAVEL WITH IT, because both are true and neither is a reason to withhold the number.

  The denominator is a FLOOR. "More than US$2.2 billion" is not a point, so 11.8x is a CEILING and
  the row carries bound '<='.

  The figure was published on 24-May-2024, about six weeks AFTER the secondary closed in early
  April 2024. It is recorded in denominator_basis and in the note so nobody later mistakes it for
  a figure that was public at pricing.
"""
import csv, io, sys

PATH = 'data/private-rounds.csv'


def main():
    raw = open(PATH).read()
    head = ''.join(l for l in raw.splitlines(True) if l.startswith('#'))
    body = ''.join(l for l in raw.splitlines(True) if not l.startswith('#'))
    rd = csv.DictReader(io.StringIO(body))
    cols = rd.fieldnames
    rows = list(rd)

    hit = 0
    for r in rows:
        if not (r['company_name'] == 'Canva' and r['date'] == 'Apr-24'):
            continue
        r['revenue_metric'] = 'annualised revenue (> threshold), company-published'
        r['revenue_musd'] = '2200.0'
        r['revenue_status'] = 'Disclosed'
        r['ev_revenue_x'] = '11.8'
        r['revenue_basis'] = 'NET_REVENUE'
        r['revenue_period'] = 'RUN_RATE'
        r['denominator_basis'] = 'Company-published annualised revenue, 24-May-2024'
        r['bound'] = '<='
        r['in_medians'] = '1'
        r['revenue_source_url'] = 'https://www.canva.com/newsroom/news/canva-create-2024/'
        r['notes'] = (r['notes'] or '') + (
            ' PRICED 02-Sep-2026 ON DANIIL\'S RULING: use the number the company itself published. '
            'Canva said "more than US$2.2 billion in annualised revenue" on 24-May-2024, so the '
            'denominator is 2,200 and the multiple is 26,000/2,200 = 11.8x. Two qualifications '
            'travel with it and neither withholds the number: "more than" makes the denominator a '
            'FLOOR, so 11.8x is a ceiling and bound is set to <=; and the figure was published '
            'about six weeks AFTER the secondary closed in early April 2024, which is recorded in '
            'denominator_basis. The earlier withdrawal stands corrected: the objection was to the '
            'phantom 2,300, which came from the AUD translation A$3.3bn in the same sentence, not '
            'to Canva\'s own US$2.2bn.')
        calc = float(r['post_money_musd']) / float(r['revenue_musd'])
        assert abs(calc - 11.8) < 0.05, calc
        print('  Canva Apr-24  post %s / revenue %s = %.1fx  bound %s  in_medians %s'
              % (r['post_money_musd'], r['revenue_musd'], calc, r['bound'], r['in_medians']))
        hit += 1

    if hit != 1:
        sys.exit('expected one Canva Apr-24 row, found %d' % hit)

    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=cols, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    open(PATH, 'w').write(head + out.getvalue())
    print('%s rewritten, %d rows' % (PATH, len(rows)))


if __name__ == '__main__':
    main()
