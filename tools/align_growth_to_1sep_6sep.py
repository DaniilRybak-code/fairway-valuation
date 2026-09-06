#!/usr/bin/env python3
"""ONE SOURCE OF TRUTH FOR LISTED GROWTH: Daniil's 1-September database, on his ruling of 6-Sep.

HIS WORDS: "ALL peers in the dataset I provided measure CY+1 to CY+3 CAGR... If you have CY+1 to
CY+3 CAGR for everything, align all data to that."

He is right, and what was actually wrong is worse than the naming argument I had been having with
myself. The five listed peers files carry growth in three different columns:

    revenue_growth_cagr_cy0_cy2_pct   software 170, fintech 87
    revenue_growth_cagr_cy1_cy3_pct   ecommerce 74
    revenue_growth_pct                logistics and services 123, no horizon stated at all
    ni_growth_pct                     lending 79, an earnings growth rate

and NONE of them matches the database he supplied on 1 September. Checked row by row before writing
this script: of 166 testable software rows, 5 match his figure; of 82 fintech rows, 0; of 73
ecommerce rows, 22. Ours are rounded to whole percentages (Visa 12.0, Alibaba 18.0, FedEx 4.0) and
his carry a decimal (10.9, 12.8, 1.8), and the gaps are often material rather than rounding.

So the 1-September refresh updated the market data and never touched the growth columns. The engine
has been ranking peers on stale, rounded numbers from the 30-August pulls, under a column name that
described a window nobody had verified, while 500 rows of his authoritative CY+1/+3 CAGR sat unused
in data/raw/2026-09-01_listed-full-refresh.csv.

WHAT THIS SCRIPT DOES, and it does nothing else:

  1. Reads data/raw/2026-09-01_listed-full-refresh.csv, which is his database as transcribed on the
     day it arrived. 500 rows, one CAGR column, `cagr_cy1_cy3_pct`.
  2. For every row of every listed peers file, matches on the ticker SYMBOL (the part after the
     exchange prefix, because the two files spell the exchange differently: NASDAQ vs NASDAQGS).
  3. Writes his figures into the row: the CAGR into `revenue_growth_cagr_cy1_cy3_pct`, the three
     year-on-year rates, and `n_estimates`, the broker count the engine has been asking for since
     August to turn the micro-cap exclusion list into a rule.
  4. BLANKS `revenue_growth_cagr_cy0_cy2_pct` on any row it filled, because the whole point is one
     source of truth and leaving a stale second column is how this happened in the first place. The
     column stays in the header so nothing that reads it breaks; it is simply empty.
  5. Leaves `revenue_growth_pct` and `ni_growth_pct` untouched. They are different measures (an
     unstated horizon and an earnings rate) and overwriting them would be inventing.

NOTHING IS DROPPED AND NOTHING IS INVENTED. Every figure written comes from his file. A row not
found in his database keeps exactly what it had and is NAMED in the output, so the 17 of them are
visible rather than silently stale. Count in and count out is printed for every file.

Idempotent: run it twice and the second run reports 0 changed.

  python3 tools/align_growth_to_1sep_6sep.py
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)

SOURCE = 'data/raw/2026-09-01_listed-full-refresh.csv'
FILES = ('data/peers-software.csv', 'data/peers-fintech.csv', 'data/peers-ecommerce.csv',
         'data/peers-logistics-services.csv', 'data/peers-lending.csv')

# his column -> our column
MAP = (('cagr_cy1_cy3_pct', 'revenue_growth_cagr_cy1_cy3_pct'),
       ('growth_cy1_pct',   'revenue_growth_cy1_pct'),
       ('growth_cy2_pct',   'revenue_growth_cy2_pct'),
       ('growth_cy3_pct',   'revenue_growth_cy3_pct'),
       ('n_estimates',      'n_estimates'))

STALE = 'revenue_growth_cagr_cy0_cy2_pct'
BAD = ('', 'na', 'n.a.', 'nm', 'n.m.', 'HIDDEN', 'BROKEN', '-')


def norm(t):
    return (t or '').strip().upper().split(':')[-1]


def clean(v):
    v = (v or '').strip()
    return '' if v in BAD else v


def read(path):
    head = [l for l in open(path) if l.lstrip('"').startswith('#')]
    body = [l for l in open(path) if not l.lstrip('"').startswith('#')]
    return head, list(csv.DictReader(io.StringIO(''.join(body))))


def main():
    _h, src = read(SOURCE)
    D = {}
    for x in src:
        D.setdefault(norm(x.get('ticker')), x)
    print('SOURCE  %s: %d rows, keyed on %d distinct ticker symbols.\n' % (SOURCE, len(src), len(D)))

    grand_in = grand_out = grand_hit = grand_changed = 0
    unmatched = []
    for path in FILES:
        head, rows = read(path)
        n_in = len(rows)
        fields = list(rows[0].keys())
        for _his, ours in MAP:
            if ours not in fields:
                fields.append(ours)
        hit = changed = 0
        for r in rows:
            his = D.get(norm(r.get('exchange_ticker')))
            if not his:
                unmatched.append((path.split('/')[-1], r.get('exchange_ticker'), r.get('company_name')))
                continue
            hit += 1
            touched = False
            for hcol, ocol in MAP:
                v = clean(his.get(hcol))
                if v and (r.get(ocol) or '').strip() != v:
                    r[ocol] = v
                    touched = True
                elif ocol not in r:
                    r[ocol] = r.get(ocol, '')
            # THE STALE COLUMN GOES EMPTY ON ANY ROW WE FILLED. One source of truth means one.
            if STALE in fields and (r.get(STALE) or '').strip() and clean(his.get('cagr_cy1_cy3_pct')):
                r[STALE] = ''
                touched = True
            if touched:
                changed += 1

        out = io.StringIO()
        w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in fields})
        open(path, 'w').write(''.join(head) + out.getvalue())

        _h2, back = read(path)
        n_out = len(back)
        grand_in += n_in; grand_out += n_out; grand_hit += hit; grand_changed += changed
        print('%-34s IN %3d  OUT %3d  matched %3d  changed %3d  dropped %d'
              % (path.split('/')[-1], n_in, n_out, hit, changed, n_in - n_out))

    print('\nTOTAL   IN %d  OUT %d  matched %d  changed %d  DROPPED %d'
          % (grand_in, grand_out, grand_hit, grand_changed, grand_in - grand_out))
    print('\nNOT IN THE 1-SEP DATABASE, so left exactly as they were (%d):' % len(unmatched))
    for f, t, n in unmatched:
        print('   %-30s %-22s %s' % (f, t, n))
    print('\nThese %d keep whatever growth figure they already carried. They are the only rows in'
          % len(unmatched))
    print('the listed universe not now on Daniil\'s single source, and they are named here so that')
    print('stays visible rather than becoming another silent mix.')
    return 0 if grand_in == grand_out else 1


if __name__ == '__main__':
    sys.exit(main())
