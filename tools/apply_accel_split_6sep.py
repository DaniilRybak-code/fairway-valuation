#!/usr/bin/env python3
"""Accel split into Accel (evidence) and Accel Atoms (callable), on Daniil's ruling of 6 Sep 2026.

Daniil: "Accel should not be above funds that specialize on seed and Series A in my view."

WHAT THE ROW WAS. One row, layer CALLABLE|EVIDENCE. The callable half (cheque $1m to $2m, band
Pre-seed; Seed, geography India and Indian-origin founders) is the Accel Atoms pre-seed programme,
per its own source atoms.accel.com/faqs, and the row's dormant_note said so: "Cheque and geography
are the Accel Atoms programme only. Accel's core funds publish no cheque range and no investing
geography." The evidence half (20 rounds in our set, median round $300m, median post-money $5bn,
Legora and Decagon Series D) is Accel's core funds. The card was ranked on the core funds' deal
count while offering the programme's cheque. That is why it sat above Seedcamp and Playfair.

WHAT IT IS NOW. Two rows. `accel-atoms`, CALLABLE, named "Accel Atoms", with the programme's own
cheque, band, geography and sources, and NO deal evidence (it has none of its own in our set).
`accel`, EVIDENCE only, keeps every deal field and no cheque, band or geography, which is what
Accel's core funds publish. Nothing is invented: every value comes from the original row.

COUNT: 532 rows in, 533 out, 1 split, 0 dropped. Idempotent.

  python3 tools/apply_accel_split_6sep.py
"""
import csv, io, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE)
PATH = 'data/investors.csv'
head = [l for l in open(PATH, encoding='utf-8') if l.lstrip('"').startswith('#')]
body = [l for l in open(PATH, encoding='utf-8') if not l.lstrip('"').startswith('#')]
rows = list(csv.DictReader(io.StringIO(''.join(body)))); fields = list(rows[0].keys()); n_in = len(rows)
if any(r['investor_key'] == 'accel-atoms' for r in rows):
    print('ALREADY APPLIED: accel-atoms exists. Nothing changed.'); sys.exit(0)
acc = [r for r in rows if r['investor_key'] == 'accel']
if len(acc) != 1 or acc[0].get('layer') != 'CALLABLE|EVIDENCE':
    print('REFUSED: expected one accel row with layer CALLABLE|EVIDENCE'); sys.exit(1)
a = acc[0]
atoms = dict(a)
atoms.update({'investor_key': 'accel-atoms', 'investor_name': 'Accel Atoms', 'layer': 'CALLABLE',
              'screening_categories': '', 'subsectors': '', 'recent_deal_1_company': '', 'recent_deal_1_date': '',
              'recent_deal_1_source_url': '', 'recent_deal_2_company': '', 'recent_deal_2_date': '',
              'recent_deal_2_source_url': '', 'rounds_in_set': '', 'companies_in_set': '', 'companies_backed': '',
              'first_round': '', 'last_round': '', 'median_round_size_m': '', 'median_postmoney_m': '',
              'round_size_low_m': '', 'round_size_high_m': '',
              'provenance': 'SPLIT 6-Sep-2026 from the accel row on Daniil\'s ruling; every value is the programme\'s own, from atoms.accel.com/faqs',
              'dormant_note': 'The Accel Atoms pre-seed programme for Indian and Indian-origin founders. Not Accel\'s core funds, which publish no cheque range and no investing geography and sit in the evidence layer under Accel.'})
a.update({'layer': 'EVIDENCE', 'stage_bands': '', 'first_cheque_low_m': '', 'first_cheque_high_m': '',
          'cheque_currency': '', 'geographies': '', 'geographies_source': '', 'cheque_range_source': '',
          'thesis_one_liner': 'Accel core funds: seed to growth, publish no cheque range and no investing geography. Evidence layer only; the callable pre-seed programme is Accel Atoms.',
          'dormant_note': 'SPLIT 6-Sep-2026 on Daniil\'s ruling (Accel should not rank above seed and Series A specialists): the callable card was the Accel Atoms programme ranking on the core funds\' deal count. The programme is now its own row, accel-atoms.'})
i = rows.index(a)
rows.insert(i + 1, atoms)
out = io.StringIO(); w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(rows)
open(PATH, 'w', encoding='utf-8').write(''.join(head) + out.getvalue())
n_out = len(list(csv.DictReader(io.StringIO(''.join(l for l in open(PATH, encoding='utf-8') if not l.lstrip('"').startswith('#'))))))
print('SPLIT accel -> accel (EVIDENCE) + accel-atoms (CALLABLE, Accel Atoms)')
print('COUNT IN %d rows, COUNT OUT %d rows, 1 split, dropped %d.' % (n_in, n_out, n_in + 1 - n_out))
sys.exit(0 if n_out == n_in + 1 else 1)
