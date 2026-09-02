#!/usr/bin/env python3
"""Glovo lives in the software/fintech file, not the consumer one. Note only, no numbers change."""
import csv, io, sys
P = 'data/private-rounds.csv'
NOTE = ("STILL RECORD ONLY, BUT FOR A NARROWER REASON AFTER DANIIL'S 02-Sep-2026 RULING. The ruling that "
        "all-stock deals price at ANNOUNCEMENT removes the objection that had killed Wolt's press number, "
        "so the announced EUR 2.3bn 100% fully-diluted valuation is usable here too. What is still missing "
        "is a SOURCED denominator. Daniil's database carries roughly EUR 360m of 2020 revenue giving 6.39x, "
        "and 2300/360 reproduces CB Insights' published 6.4x exactly, which is why our own header note "
        "flagged that pair as read off a comps blog rather than sourced. One source for Glovo's 2020 "
        "revenue turns this row on.")
raw = open(P).read().split('\n')
head = [l for l in raw if l.startswith('#')]
body = '\n'.join([l for l in raw if not l.startswith('#') and l.strip()])
rows = list(csv.DictReader(io.StringIO(body)))
cols = list(rows[0].keys())
hit = 0
for r in rows:
    if r.get('company_name') == 'Glovo' and (r.get('date_iso') or '').startswith('2021-12'):
        r['notes'] = NOTE + ' || ' + (r.get('notes') or ''); hit += 1
if hit != 1:
    print('ERROR: matched %d Glovo rows' % hit); sys.exit(1)
out = io.StringIO(); w = csv.DictWriter(out, fieldnames=cols); w.writeheader()
for r in rows: w.writerow({c: r.get(c, '') for c in cols})
open(P, 'w').write('\n'.join(head) + '\n' + out.getvalue())
print('Glovo note added, %d rows' % len(rows))
