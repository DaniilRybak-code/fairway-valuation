#!/usr/bin/env python3
"""
Daniil, 02-Sep-2026: "Let's add some run rate for Zopa and Upgrade. If these runrates were quoted
in the announcement, they were used for pricing, so we should be making note of them."
And: "Loft - let's price it off the 150m that appeared a month later, close enough."

The test he set is the right one and it changes the answer for Zopa. Every figure below was read
off the round coverage itself, not off a later filing.
"""
import csv, io, sys
P = 'data/private-rounds.csv'

EDITS = {
  ('Zopa', '2021-10'): {
    'fields': {
      'revenue_metric': 'Revenue run-rate at the round',
      'revenue_musd': '116.0',
      'revenue_status': 'Reported (TechCrunch, day of round)',
      'ev_revenue_x': '8.9',
      'revenue_period': 'RUN_RATE',
      'revenue_basis': 'ARR_RUNRATE',
      'denominator_basis': 'REPORTED_CONTEMPORANEOUS',
      'in_medians': '0',
      'fx_ccy': 'GBP',
      'revenue_source_url': 'https://techcrunch.com/2021/10/18/zopa-raises-300m-at-a-1b-valuation-to-expand-its-p2p-lending-and-savings-neobank-in-the-uk/',
    },
    'note': ("RUN-RATE ADDED 02-Sep-2026 ON DANIIL'S TEST: if a run-rate was quoted at the round it "
             "was part of the pricing and must be recorded. It was. TechCrunch of 18-Oct-2021, the "
             "day of the round: Zopa has a 'run rate of GBP 85 million ($116 million)' and expects "
             "'GBP 170 million ($233 million) by 2022', at '$1 billion (GBP 750 million) post-money'. "
             "In sterling on both legs, 750 over 85 is 8.8x; in dollars on both legs, 1,030 over 116 "
             "is 8.9x, and the row carries 8.9x so it ties to its own cells. "
             "THIS IS WHY THE TEST MATTERS: Daniil's sheet prices Zopa at 25.16x on FY2020 statutory "
             "revenue of GBP 29.8m. The run-rate at the round was GBP 85m, nearly three times that, "
             "because a bank growing this fast leaves its last filed year far behind. 25.16x is not "
             "a Zopa multiple, it is a stale-denominator artefact. "
             "BOOK REMAINS THE PRICING BASIS. valuation_basis stays BOOK at 5.6x and in_medians stays "
             "0 on the revenue leg, because our standing rule is that lenders price on book: their "
             "revenue contains interest earned on borrowed money, so two lenders with the same book "
             "and different leverage read identically on book and differently on revenue. The "
             "run-rate is recorded, not priced off. Zopa's own release adds GBP 675m of fixed-savings "
             "deposits, over GBP 6bn of loans disbursed and profitability expected within ten weeks."),
  },
  ('Upgrade', '2021-08'): {
    'fields': {
      'revenue_metric': 'Annual revenue run-rate',
      'revenue_musd': '160.0',
      'revenue_status': 'Reported (trade press, day of round)',
      'ev_revenue_x': '21.4',
      'revenue_period': 'RUN_RATE',
      'revenue_basis': 'ARR_RUNRATE',
      'denominator_basis': 'REPORTED_CONTEMPORANEOUS',
      'in_medians': '0',
      'originations_musd': '7000.0',
      'originations_period': 'CY2021, on track at announcement',
      'revenue_source_url': 'https://www.pymnts.com/digital-first-banking/2021/upgrade-valued-3-billion-dollars-series-e-fundraising-round/',
    },
    'note': ("RUN-RATE ADDED 02-Sep-2026. PYMNTS on the day of the round: 'The company grew by 75 "
             "percent in 2020 as it achieved profitability with a $160 million annual revenue run "
             "rate.' 3,430 over 160 gives 21.4x. Upgrade's OWN release gives no revenue figure at "
             "all; what it gives is credit volume, 'over $7 billion in affordable credit to consumers "
             "through cards and loans since inception in 2017' and 'on track to deliver $7 billion in "
             "2021 alone', and that CY2021 originations figure is now recorded too. Valuation is "
             "Upgrade's own: '$105 million Series E round at a $3.325 billion pre-money valuation', "
             "so the $3,430m here is the derived post-money. BOOK OR ORIGINATIONS REMAINS THE PRICING "
             "BASIS for a consumer lender; in_medians stays 0 on the revenue leg."),
  },
  ('Upgrade', '2021-11'): {
    'fields': {
      'originations_musd': '8000.0',
      'originations_period': 'CY2021, on track at announcement',
      'round_source_url': 'https://techcrunch.com/2021/11/16/credit-focused-company-upgrade-raises-280-million-at-6-billion-valuation/',
    },
    'note': ("NO RUN-RATE EXISTS FOR THIS ROUND, AND THAT IS THE FINDING. Checked 02-Sep-2026 against "
             "Upgrade's own release and TechCrunch, both of 16-Nov-2021: neither states any revenue or "
             "run-rate figure. The only metric either gives is credit volume, 'over $10 billion in "
             "affordable credit to consumers' since 2017 and 'on track to deliver $8 billion in 2021 "
             "alone', and that CY2021 originations figure is now recorded. "
             "Daniil's sheet prices this round at 62.80x on a $100m run-rate. That $100m is Upgrade's "
             "JUNE-2020 Series D figure, seventeen months earlier: TechCrunch of 17-Jun-2020, 'the "
             "company told TechCrunch it is currently on a $100 million run rate'. No Q3-2021 figure "
             "of $100m exists anywhere. The monotonicity check built today catches it: the run-rate "
             "cannot fall from 160 in August to 100 in November. Valuation is Upgrade's own, $6.0bn "
             "pre-money, so $6,280m is the derived post-money."),
  },
  ('Loft', '2021-03'): {
    'fields': {
      'revenue_metric': 'Annualised revenue, first full year of operation',
      'revenue_musd': '150.0',
      'revenue_status': 'Reported (TechCrunch, one month after the round)',
      'ev_revenue_x': '14.7',
      'revenue_period': 'RUN_RATE',
      'revenue_basis': 'ARR_RUNRATE',
      'denominator_basis': 'REPORTED_NEAR_CONTEMPORANEOUS',
      'in_medians': '1',
      'valuation_basis': 'REVENUE',
      'revenue_source_url': 'https://techcrunch.com/2021/04/22/brazils-loft-adds-100m-to-its-accounts-700m-to-its-valuation-in-a-single-month/',
    },
    'note': ("PRICED 02-Sep-2026 ON DANIIL'S RULING, 'let's price it off the 150m that appeared a "
             "month later, close enough'. TechCrunch of 22-Apr-2021, one month after this round: Loft "
             "'told me last year that it had notched over $150 million in annualized revenues in its "
             "first full year of operation'. 2,200 over 150 gives 14.7x. "
             "THE CAVEAT, RECORDED RATHER THAN ARGUED: on the day of the round itself the co-founder "
             "said only that revenue and GMV 'increased significantly' in 2020 and declined to give a "
             "figure, and the $150m is Loft quoting its own prior-year milestone rather than a "
             "figure struck at pricing. It is therefore a floor on a growing company, which makes "
             "14.7x a CEILING on the true multiple. Daniil's sheet carries the same 14.67x."),
  },
}

raw = open(P).read().split('\n')
head = [l for l in raw if l.startswith('#')]
body = '\n'.join([l for l in raw if not l.startswith('#') and l.strip()])
rows = list(csv.DictReader(io.StringIO(body)))
cols = list(rows[0].keys())
hit = 0
for r in rows:
    key = (r.get('company_name'), (r.get('date_iso') or '')[:7])
    if key in EDITS:
        e = EDITS[key]
        for k, v in e['fields'].items():
            if k not in cols: print('ERROR: unknown column %r' % k); sys.exit(1)
            print('  %-9s %-8s %-22s %r -> %r' % (key[0], key[1], k, r.get(k), v))
        r.update(e['fields'])
        r['notes'] = e['note'] + ' || ' + (r.get('notes') or '')
        hit += 1
if hit != len(EDITS):
    print('ERROR: matched %d of %d' % (hit, len(EDITS))); sys.exit(1)
out = io.StringIO(); w = csv.DictWriter(out, fieldnames=cols); w.writeheader()
for r in rows: w.writerow({c: r.get(c, '') for c in cols})
open(P, 'w').write('\n'.join(head) + '\n' + out.getvalue())
print('\n%d rows updated in %s' % (hit, P))
