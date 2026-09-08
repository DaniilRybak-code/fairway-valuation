#!/usr/bin/env python3
"""Fold the near-duplicate end-market labels (TAKEOVER item 7), on Daniil's approval of 8 September
2026 ("1: Agree, proceed"). Idempotent; count in and count out; a row count that moves fails it.

WHY IT MATTERS. The end market is a hard test in two places: a name with no shared product word
is relevant only if it shares the founder's SPECIFIC end market, and a name reaches the pricing set
only if its end market is the founder's or Horizontal. A label spelled two ways is two end markets
that never meet. Measured on 8-Sep: alloovium (Real Estate) could not reach Procore (Construction &
Infrastructure); florin (Financial Services) was shown PayPoint and SS&C while Guidewire, FINEOS,
Crawford and Trupanion sat under "Insurance"; princeps failed the gate for the same reason.

THE FOLDS, each one row-level and named:
  Real Estate & Construction  -> Real Estate            (Better.com, a mortgage lender)
  Retail & Commerce           -> Retail & E-commerce    (Pine Labs, Shiprocket, ElasticRun)
  Retail & Commerce           -> Automotive             (Spinny, a used-car retailer: the truer label)
  Transportation & Logistics  -> Logistics & Mobility   (Loadsmart)
  Financial Services          -> Insurance              (Wefox, Coalition, The Zebra, Sapiens: the
                                                         insurers and the insurance-software vendor,
                                                         so that "Insurance" is one end market on
                                                         both sides of the pool; Alan and Devoted
                                                         stay Healthcare, which is their market)
The two insurance FIXTURES that carried Financial Services (florin, princeps) are moved in
selector/golden_profiles.py in the same commit. Measured: florin's listed set becomes Guidewire,
FINEOS, Crawford, ZhongAn, Trupanion (5 priced) instead of ZhongAn, PayPoint, SS&C; princeps passes
the gate on Crawford, Trupanion and CCC (3 priced) instead of failing on wealth platforms, and still
needs a listed specialty P&C carrier from the bulk pass to be a set a banker would sign.

  python3 tools/apply_industry_folds_8sep.py
"""
import csv, io, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE)
PATH = 'data/private-companies-tags.csv'
PLAN = [
    ('better', 'Real Estate', 'a mortgage lender sells into the housing market; "& Construction" was a spelling, not a market'),
    ('pinelabs', 'Retail & E-commerce', 'the label the other 54 retail rows carry'),
    ('shiprocket', 'Retail & E-commerce', 'the label the other 54 retail rows carry'),
    ('elasticrun', 'Retail & E-commerce', 'the label the other 54 retail rows carry'),
    ('spinny', 'Automotive', 'a used-car retailer; the pool\'s car names carry Automotive'),
    ('loadsmart', 'Logistics & Mobility', 'the label Delhivery, Xpressbees and Moove carry'),
    ('wefox', 'Insurance', 'an insurer; Insurance is the end market the listed insurance rows carry'),
    ('coalition', 'Insurance', 'an insurer; Insurance is the end market the listed insurance rows carry'),
    ('the-zebra', 'Insurance', 'an insurance marketplace; same'),
    ('sapiens', 'Insurance', 'insurance software; same'),
]
MARK = 'END MARKET FOLDED 8-Sep-2026 (TAKEOVER 7)'


def _split(path):
    lines = open(path, encoding='utf-8').read().splitlines(keepends=True)
    return ([l for l in lines if l.lstrip('"').startswith('#')],
            [l for l in lines if not l.lstrip('"').startswith('#')])


def main():
    head, body = _split(PATH)
    rows = list(csv.DictReader(io.StringIO(''.join(body))))
    fields = list(rows[0].keys()); n_in = len(rows); changed = 0
    for key, industry, why in PLAN:
        hits = [r for r in rows if (r.get('company_key') or '').strip() == key]
        if len(hits) < 1:
            print('REFUSED: %s matched no row' % key); return 1
        for r in hits:
            if (r.get('industry') or '') == industry:
                print('ALREADY APPLIED: %-12s %s' % (key, r['company_name'])); continue
            before = r.get('industry')
            r['industry'] = industry
            if 'taxonomy_note' in r:
                r['taxonomy_note'] = ((r.get('taxonomy_note') or '').strip() + ' ' + MARK + ': ' + before + ' to ' + industry + ', ' + why).strip()
            changed += 1
            print('CHANGED %-12s %-24s %s -> %s' % (key, r['company_name'][:24], before, industry))
    if changed:
        out = io.StringIO()
        w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(rows)
        open(PATH, 'w', encoding='utf-8').write(''.join(head) + out.getvalue())
    n_out = len(list(csv.DictReader(io.StringIO(''.join(_split(PATH)[1])))))
    print('%s: %d rows in, %d out, %d changed, %d dropped' % (PATH, n_in, n_out, changed, n_in - n_out))
    return 0 if n_in == n_out else 1


if __name__ == '__main__':
    sys.exit(main())
