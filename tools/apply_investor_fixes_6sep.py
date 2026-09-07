#!/usr/bin/env python3
"""Investor table fixes on Daniil's rulings of 6 September 2026 (late), idempotent, count in and out.

1. THE STALE deal_note TAILS. deal_note is the evidence sentence printed on a founder's investor
   card (a cited recent deal: "Canaan's own post, 30-Jan-2026: led OpenArt's $30M Series A"). Six
   rows still ended with a sentence beginning "STAGE BAND LEFT EMPTY", written when those houses
   had no band and never removed when the bands were filled on 6 Sep. Daniil: "If it is stale and
   empty we should delete." Only the stale sentence is removed; the cited deal stays.
2. Y COMBINATOR's stage band read "Growth; Late stage; Crossover", which contradicts the row's own
   deal_note ("$125,000 on a post-money SAFE", ycombinator.com/deal) and the stale tail's own
   source ("companies arrive at YC at all different stages", ycombinator.com/about). Set to
   "All stages", the phrase Daniil ruled acceptable on 6 Sep and the phrase YC's page supports.

  python3 tools/apply_investor_fixes_6sep.py
"""
import csv, io, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE)
PATH = 'data/investors.csv'
TAIL = 'STAGE BAND LEFT EMPTY'
head = [l for l in open(PATH, encoding='utf-8') if l.lstrip('"').startswith('#')]
body = [l for l in open(PATH, encoding='utf-8') if not l.lstrip('"').startswith('#')]
rows = list(csv.DictReader(io.StringIO(''.join(body)))); fields = list(rows[0].keys()); n_in = len(rows)
changed = 0
for r in rows:
    n = r.get('deal_note') or ''
    if TAIL in n:
        i = n.find(TAIL)
        r['deal_note'] = n[:i].rstrip()
        changed += 1
        print('STRIPPED %-20s deal_note tail removed; band now %r' % (r['investor_name'], r.get('stage_bands')))
    if r['investor_name'] == 'Y Combinator' and r.get('stage_bands') != 'All stages':
        print('CHANGED  Y Combinator stage_bands %r -> %r (source already in the row: ycombinator.com/deal and /about)' % (r.get('stage_bands'), 'All stages'))
        r['stage_bands'] = 'All stages'
        changed += 1
if not changed:
    print('ALREADY APPLIED: no stale tails, Y Combinator reads All stages. Nothing changed.'); sys.exit(0)
out = io.StringIO(); w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(rows)
open(PATH, 'w', encoding='utf-8').write(''.join(head) + out.getvalue())
n_out = len(list(csv.DictReader(io.StringIO(''.join(l for l in open(PATH, encoding='utf-8') if not l.lstrip('"').startswith('#'))))))
print('COUNT IN %d rows, COUNT OUT %d rows, %d edits, dropped %d.' % (n_in, n_out, changed, n_in - n_out))
sys.exit(0 if n_in == n_out else 1)
