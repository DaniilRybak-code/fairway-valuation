# -*- coding: utf-8 -*-
"""Check MY TRANSCRIPTION, not Daniil's arithmetic.

Daniil's numbers were already verified in the sandbox they came from. What has NOT been checked is
whether I copied them off a screenshot correctly. usd = local x fx catches that: a mistyped digit in
any of the three columns breaks the identity, which is the whole reason this file is trustworthy.
It costs one second to run, so there is no reason not to.
"""
import csv, io, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(HERE, 'data/raw/2026-09-01_gmv-tpv-combined.csv')
body = [l for l in open(p) if not l.lstrip().startswith('#')]
R = list(csv.DictReader(io.StringIO(''.join(body))))
bad, ok = [], 0
for r in R:
    try:
        loc, fx, usd = float(r['local_value']), float(r['fx_usd_per_local']), float(r['usd_musd'])
    except (ValueError, TypeError):
        bad.append((r['exchange_ticker'], 'unparsable number')); continue
    calc = loc * fx
    # tolerance is generous on the FX rate only, which the sheet shows to 6dp but stores deeper
    tol = 0.0005 if fx != 1.0 else 1e-9
    if abs(calc - usd) > max(abs(usd) * tol, 0.15):
        bad.append((r['exchange_ticker'], 'local %s x fx %s = %.1f, transcribed %.1f'
                    % (r['local_value'], r['fx_usd_per_local'], calc, usd)))
    else:
        ok += 1
print('%d rows transcribed' % len(R))
print('%d tie on usd = local x fx' % ok)
print('%d do NOT tie' % len(bad))
for t, why in bad: print('    %-22s %s' % (t, why))
from collections import Counter
print()
print('by disclosure status:', dict(Counter(r['disclosure_status'] for r in R)))
print('by currency        :', dict(Counter(r['local_ccy'] for r in R)))
dups = [k for k, v in Counter((r['company_name'] or '').lower() for r in R).items() if v > 1]
print('company names appearing more than once:', dups)
