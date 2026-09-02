#!/usr/bin/env python3
"""
Applies the verdicts from the independent check of the 19 private-round disagreements
(2 September 2026). Only rows where OUR number was found to be wrong, or our source URL
did not contain the figure we cite, are touched. Every change carries its reason in notes.

Run from the repo root:  python3 tools/apply_reconciliation_verdicts_2sep.py
"""
import csv, io, sys

PATH = 'data/private-rounds.csv'

CHANGES = {
    # (company_name, date_iso) -> dict of column -> new value, plus a note to prepend
    ('Replit', '2025-09'): {
        'fields': {
            'revenue_musd': '150.0',
            'ev_revenue_x': '20.0',
            'revenue_metric': 'annualised revenue at pricing',
            'revenue_status': 'Disclosed',
        },
        'note': ("CORRECTED 02-Sep-2026 FROM 100 TO 150 ON OUR OWN CITED SOURCE. Replit's Series C "
                 "announcement, replit.com/news/funding-announcement-series-c, says in its own words "
                 "'growing annualized revenue from $2.8 million to $150 million in less than a year, "
                 "a more than 50x increase'. We had 100, which is Replit's June-2025 milestone "
                 "('crossed $100M in ARR' earlier that month), three months before pricing. TechCrunch "
                 "of 10-Sep-2025 carries the same $150m. This was a misreading of a primary source we "
                 "were already citing, not a sourcing gap. 3000/150 gives 20.0x, was 30.0x."),
    },
    ('Notion', '2026-01'): {
        'fields': {
            'revenue_musd': '600.0',
            'ev_revenue_x': '18.3',
            'revenue_metric': 'ARR (> threshold)',
            'revenue_status': 'Reported estimate',
            'revenue_source_url': 'https://www.forbes.com/sites/annatong/2025/12/15/notion-kicks-off-employee-share-sale-at-11-billion-valuation-as-ai-accelerates-its-growth/',
        },
        'note': ("CORRECTED 02-Sep-2026 FROM 500 TO 600. Our 500 was CNBC of 18-Sep-2025, four months "
                 "before this tender. Forbes of 15-Dec-2025, the day Notion told employees it was doing "
                 "the tender at $11bn, reports Notion 'passed $600M in ARR, half of it from AI products'. "
                 "That is the figure current when the price was set. Corroborated by itiger.com of "
                 "16-Dec-2025, 'Notion's ARR has crossed the $600 million threshold, with 50% originating "
                 "from AI products', and by Sacra's independent $610m at end-2025. 'Passed' makes the "
                 "denominator a floor, so 18.3x is a CEILING. Daniil's database carries 865, which is "
                 "Sacra's July-2026 figure, six months AFTER this tender: hindsight, excluded by our own "
                 "rule. Notion's own blog on the tender gives no dollar ARR."),
    },
    ('AlphaSense', '2023-09'): {
        'fields': {
            'revenue_source_url': 'https://www.cnbc.com/2023/04/11/alphabets-capitalg-leads-100-million-round-in-ai-startup-alphasense-.html',
        },
        'note': ("SOURCE URL CORRECTED 02-Sep-2026, FIGURE UNCHANGED. We were citing the TechCrunch piece "
                 "of 28-Sep-2023 for the $100m. That article was read in full on 02-Sep-2026 and contains "
                 "NO AlphaSense revenue or ARR figure of any kind; its only business numbers are 4,000 "
                 "enterprise customers and 10,000 sources. The $100m actually comes from CNBC of "
                 "11-Apr-2023: 'AlphaSense is much further along, having already surpassed $100 million in "
                 "annual recurring revenue in 2022.' The number stands, the citation did not. The $200m "
                 "Daniil's database carries is Fortune of 09-Apr-2024 describing END-2023, six months "
                 "after this pricing, which is what our existing note already said."),
    },
    ('Clay', '2026-01'): {
        'fields': {
            'revenue_source_url': 'https://www.businesswire.com/news/home/20260128514638/en/Clay-Announces-Second-Employee-Tender-Offer-in-Nine-Months-at-a-$5B-Valuation',
        },
        'note': ("SOURCE UPGRADED 02-Sep-2026, FIGURE UNCHANGED. We were citing Clay's $100m ARR milestone "
                 "post of 08-Dec-2025. Clay's own tender announcement of 28-Jan-2026 restates the same "
                 "figure as the basis for this price: 'Clay's revenue grew more than 3.5x, reaching $100M "
                 "in ARR in December.' The round announcement is the stronger source and now carries the "
                 "row. Daniil's 150 is Sacra's May-2026 figure, four months after this tender."),
    },
}

lines = open(PATH).read().split('\n')
head = [l for l in lines if l.startswith('#')]
body = '\n'.join([l for l in lines if not l.startswith('#') and l.strip()])
rows = list(csv.DictReader(io.StringIO(body)))
cols = list(rows[0].keys())

applied = []
for r in rows:
    key = (r.get('company_name'), (r.get('date_iso') or '')[:7])
    if key not in CHANGES:
        continue
    ch = CHANGES[key]
    before = {k: r.get(k) for k in ch['fields']}
    r.update(ch['fields'])
    r['notes'] = ch['note'] + ' || ' + (r.get('notes') or '')
    applied.append((key, before, ch['fields']))

if len(applied) != len(CHANGES):
    print('ERROR: matched %d of %d rows. Nothing written.' % (len(applied), len(CHANGES)))
    sys.exit(1)

out = io.StringIO()
w = csv.DictWriter(out, fieldnames=cols)
w.writeheader()
for r in rows:
    w.writerow(r)

with open(PATH, 'w') as f:
    f.write('\n'.join(head) + '\n' + out.getvalue())

for key, before, after in applied:
    print('%s %s' % key)
    for k in after:
        print('    %-20s %r -> %r' % (k, before[k], after[k]))
print('\n%d rows changed in %s' % (len(applied), PATH))
