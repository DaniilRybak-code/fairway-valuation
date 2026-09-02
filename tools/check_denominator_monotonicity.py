#!/usr/bin/env python3
"""
THE MONOTONICITY CHECK, built 02-Sep-2026.

The Upgrade defect: two figures from ONE article were attached to two different rounds in the
wrong order, so a consumer lender printed 62.8x on the later round off the smaller, earlier
number. The header of private-rounds.csv called for this check on 31-Aug and it did not exist.

Rule: across sequential priced rounds of the SAME company on the SAME denominator basis, the
denominator should not fall. A company can shrink, so a fall is a FLAG, not a verdict. What it
catches is a figure attached to the wrong round.

Usage:
    python3 tools/check_denominator_monotonicity.py                 # our files
    python3 tools/check_denominator_monotonicity.py <a csv> ...     # any file with the same shape
"""
import csv, io, sys, re
from collections import defaultdict

OURS = ['data/private-rounds.csv', 'data/private-rounds-consumer.csv']

def rows_from(path):
    lines = [l for l in open(path) if not l.startswith('#')]
    rd = list(csv.DictReader(io.StringIO(''.join(lines))))
    out = []
    for r in rd:
        if 'company_name' in r:            # our shape
            out.append(dict(company=r.get('company_name'), date=(r.get('date_iso') or '')[:7],
                            rev=r.get('revenue_musd'), basis=(r.get('revenue_basis') or '').upper(),
                            mult=r.get('ev_revenue_x')))
        else:                              # the transcribed sheet shape
            out.append(dict(company=r.get('company'), date=(r.get('txn_date') or '')[:7],
                            rev=r.get('metric_value_m'), basis=(r.get('metric_type') or '').upper(),
                            mult=r.get('mult_reported')))
    return out

def f(x):
    try: return float(x)
    except: return None

# ARR, run-rate and annualised revenue are the same kind of forward number and are compared
# together. A GMV or loans-originated series is compared only against itself.
FAMILY = {'ARR': 'FWD', 'ARR_RUNRATE': 'FWD', 'RUN_RATE': 'FWD',
          'NET_REVENUE': 'REV', 'GROSS_REVENUE': 'REV', 'REVENUE': 'REV'}

def check(paths):
    seq = defaultdict(list)
    for p in paths:
        for r in rows_from(p):
            rev = f(r['rev'])
            if not rev or not r['company'] or not r['date']:
                continue
            fam = FAMILY.get(r['basis'], r['basis'])
            seq[(r['company'], fam)].append((r['date'], rev, f(r['mult']), r['basis']))
    flags = 0
    checked = 0
    for (co, fam), obs in sorted(seq.items()):
        if len(obs) < 2:
            continue
        obs.sort()
        checked += 1
        for (d0, v0, m0, b0), (d1, v1, m1, b1) in zip(obs, obs[1:]):
            if v1 < v0 * 0.999:
                flags += 1
                print(f"  {co:<20} {fam:<5} {d0} {v0:>10,.1f} ({b0})  ->  {d1} {v1:>10,.1f} ({b1})"
                      f"   DENOMINATOR FALLS {100*(1-v1/v0):.0f}%"
                      + (f"   multiples {m0}x -> {m1}x" if m0 and m1 else ""))
    print(f"\n{checked} company/basis series with two or more dated denominators. {flags} fall.")
    return flags

if __name__ == '__main__':
    paths = sys.argv[1:] or OURS
    print("DENOMINATOR MONOTONICITY, %s" % ', '.join(paths))
    print("A fall is a flag, not a verdict: a company can shrink. What it catches is a figure")
    print("attached to the wrong round.\n")
    sys.exit(0 if check(paths) == 0 else 0)
