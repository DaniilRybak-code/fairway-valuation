#!/usr/bin/env python3
"""BVNK's archetypes, on Daniil's word of 6 September 2026. Afternoon: "BVNK is an infrastructure
company (connecting tradfi to stablecoins)". Evening, sharpening it: "not simply infrastructure
(should not be compared to ports or airports), this is payments / market / DeFi infrastructure".
Claude tagged it on 5-Sep with Card Issuing & BaaS first and Crypto & Digital Assets second. The
end state is Crypto & Digital Assets first and Cross-Border & FX second: the rails are the business,
they settle payments across borders, and the card is one product on them. Measured before applying:
2 of 102 fixtures change peers (trolley and dots, both payouts businesses, gain BVNK in place of
dLocal and Rapyd). Idempotent from either earlier state; count in and count out.

  python3 tools/apply_bvnk_swap_6sep.py
"""
import csv, io, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE)
PATH = 'data/private-companies-tags.csv'
head = [l for l in open(PATH, encoding='utf-8') if l.startswith('#')]
body = [l for l in open(PATH, encoding='utf-8') if not l.startswith('#')]
rows = list(csv.DictReader(io.StringIO(''.join(body)))); fields = list(rows[0].keys()); n_in = len(rows)
hits = [r for r in rows if r['company_key'] == 'bvnk']
if len(hits) != 1:
    print('REFUSED: expected one bvnk row, found %d' % len(hits)); sys.exit(1)
r = hits[0]
END = ('Crypto & Digital Assets', 'Cross-Border & FX')
if (r['archetype'], r['archetype_secondary']) == END:
    print('ALREADY APPLIED: bvnk is Crypto & Digital Assets | Cross-Border & FX. Nothing changed.'); sys.exit(0)
if (r['archetype'], r['archetype_secondary']) not in (('Card Issuing & BaaS', 'Crypto & Digital Assets'),
                                                       ('Crypto & Digital Assets', 'Card Issuing & BaaS')):
    print('REFUSED: unexpected archetypes %r / %r' % (r['archetype'], r['archetype_secondary'])); sys.exit(1)
was = (r['archetype'], r['archetype_secondary'])
r['archetype'], r['archetype_secondary'] = END
if 'SWAPPED 6-Sep-2026' not in (r.get('taxonomy_note') or ''):
    r['taxonomy_note'] = (r.get('taxonomy_note') or '') + ' SWAPPED 6-Sep-2026 on Daniil: "payments / market / DeFi infrastructure (connecting tradfi to stablecoins)"; the rails are the business and they settle across borders, the card is one product on them.'
out = io.StringIO(); w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(rows)
open(PATH, 'w', encoding='utf-8').write(''.join(head) + out.getvalue())
n_out = len(list(csv.DictReader(io.StringIO(''.join(l for l in open(PATH, encoding='utf-8') if not l.startswith('#'))))))
print('CHANGED bvnk: %s | %s -> %s | %s' % (was + END))
print('COUNT IN %d rows, COUNT OUT %d rows, changed 1, dropped %d.' % (n_in, n_out, n_in - n_out))
sys.exit(0 if n_in == n_out else 1)
