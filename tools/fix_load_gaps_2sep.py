#!/usr/bin/env python3
"""
Two fixes to the load of Daniil's 191-row sheet.

FIX 1, MY BUG. tools/load_daniil_sheet_2sep.py deduplicated on COMPANY, not on company AND round.
So any round belonging to a company we already held was silently skipped. Six rounds were lost:

    Airwallex  2021-11-18  Series E1, $100m at $5.5bn, run-rate 100, 55.0x
    Deel       2022-05-11  Series D extension, $12bn, ARR 295, 40.68x
    Perplexity 2025-07     $18bn, run-rate 150, 120.0x
    Ramp       2025-07-30  $22.5bn, run-rate 700, 32.14x
    Ramp       2021-08-24  Series C, $3.9bn, run-rate 100, 39.0x
    Whatnot    2025-01-08  Series E, $4.97bn, GMV 3,000, 1.66x  -> the CONSUMER file

Two more looked missing and are not. Figma 16-May-2024 is the round we hold as Jul-24: same Axios
URL, re-dated from tender launch to tender close, and the note says so. Canva 23-May-2024 is the
round we hold as Apr-24, same Forbes URL, where WE withdrew the multiple over two recorded defects.
Neither is inserted. Canva is reported to Daniil instead, because his sheet supplies the run-rate
of 2,300 that our row lacks and he may want the withdrawal revisited.

FIX 2, DANIIL'S RULING OF 02-Sep-2026: "even if this is a finance company, if the revenue or ARR
was cited for it in the press release, this is how the round was priced and this is what our data
needs to reflect."

I had held 31 of the 63 loaded rows out of the medians. Most of those holds were mine, not the
data's, and the ruling reverses them. Fourteen rows go back in:

    the ten deposit-taking banks and neobanks   Revolut x4, Monzo, Chime x2, N26, Atom Bank,
                                                Mercury, Qonto
    two entity-proxy denominators               SumUp Dec-23, Checkout.com Dec-23
    one stated ARR proxy                        Cohere Jun-23
    one basis doubt the sheet states itself     Rapyd Jan-21

NOTHING IS LOST BY DOING THIS, because the engine already separates the lanes properly.
`is_balance_sheet` in selector/match_reference.py decides the pricing basis from the FOUNDER'S
archetype, not from the comparable's. A lender founder is still priced on book. Revolut's revenue
multiple simply becomes available to the payments and fintech founders who are priced on revenue,
which is what the round itself was priced on.

WHAT STAYS OUT, and it is arithmetic rather than judgement:

    13 volume-only rows      LOANS_ORIGINATED, PAYMENT_VOLUME, OTHER_VOLUME. There is no revenue
                             denominator on these rows, so no revenue multiple can exist. Their
                             volume multiple is recorded in ev_volume_x and is used by the volume
                             lane.
    2 subscriber counts      Calm, Flo Health. A count of people is not a revenue figure.
    1 Coalition Jul-22       RECLASSIFIED by this script. Its denominator is annualised GROSS
                             WRITTEN PREMIUM. For an insurer GWP is the volume that flows through,
                             the analogue of GMV, not the insurer's own revenue. It moves from the
                             revenue fields to the volume fields, where it is usable.
    1 Kriya Oct-25           Post-money 7.5 against revenue 12.6 gives 0.60x. Held pending Daniil.

That leaves 17 of the 63 out of the revenue medians and 46 in, from 32.
"""
import csv, io, re, sys

DST = 'data/private-rounds.csv'
CONS = 'data/private-rounds-consumer.csv'

# company_key -> (screening category, subsector), reusing the mapping from the first load
MISSING = [
    dict(company='Airwallex', iso='2021-11', date='Nov-21', post=5500.0, metric='RUN_RATE',
         val=100.0, mult='55.00', basis='Q3 2021 annualized', rt='Series E1',
         cat='Cross-Border & FX', sub='Cross-border payments for businesses',
         url='https://www.airwallex.com/global/newsroom/airwallex-raises-additional-usd100-million-in-series-e1-led-by-lone-pine'),
    dict(company='Deel', iso='2022-05', date='May-22', post=12000.0, metric='ARR',
         val=295.0, mult='40.68', basis='ARR', rt='Series D extension',
         cat='Enterprise Applications', sub='HR, payroll and global workforce',
         url='https://www.deel.com/blog/series-d-extension/'),
    dict(company='Perplexity', iso='2025-07', date='Jul-25', post=18000.0, metric='RUN_RATE',
         val=150.0, mult='120.00', basis='Jul-2025', rt='Growth financing',
         cat='Data, AI & Developer Tools', sub='AI search / answer engine',
         url='https://news.bloomberglaw.com/private-equity/ai-startup-perplexity-valued-at-18-billion-with-new-funding'),
    dict(company='Ramp', iso='2025-07', date='Jul-25', post=22500.0, metric='RUN_RATE',
         val=700.0, mult='32.14', basis='Annualized revenue', rt='Growth financing',
         cat='Vertical Software', sub='Spend management / corporate cards',
         url='https://techcrunch.com/2025/07/30/ramp-raises-500m-at-22-5b-valuation/',
         revurl='https://techcrunch.com/2025/09/09/ramp-says-it-has-hit-1b-in-annualized-revenue/'),
    dict(company='Ramp', iso='2021-08', date='Aug-21', post=3900.0, metric='RUN_RATE',
         val=100.0, mult='39.00', basis='Annualized revenue', rt='Series C',
         cat='Vertical Software', sub='Spend management / corporate cards',
         url='https://ramp.com/blog/series-c'),
]

# rows whose in_medians I set to 0 on my own judgement, reversed by Daniil's ruling
REINSTATE = [('Revolut', 'Nov-25'), ('Revolut', 'Aug-24'), ('Revolut', 'Nov-23'),
             ('Revolut', 'Jul-21'), ('Monzo', 'May-24'), ('Chime', 'Apr-24'), ('Chime', 'Aug-21'),
             ('N26', 'Oct-21'), ('Atom Bank', 'Nov-23'), ('Mercury', 'Mar-25'), ('Qonto', 'Jan-22'),
             ('SumUp', 'Dec-23'), ('Checkout.com', 'Dec-23'), ('Cohere', 'Jun-23'),
             ('Rapyd', 'Jan-21')]

RULING = (' IN THE MEDIANS by Daniil\'s ruling of 02-Sep-2026: if revenue or ARR was cited in the '
          'press release, that is how the round was priced and our data must reflect it. The hold '
          'was my judgement, not a defect in the row. Nothing is lost: the engine picks the pricing '
          'basis from the FOUNDER\'S archetype, so a lender founder is still priced on book.')


def rd(p):
    lines = [l for l in open(p) if not l.startswith('#')]
    return csv.DictReader(io.StringIO(''.join(lines)))


def main():
    r = rd(DST)
    cols = r.fieldnames
    rows = list(r)
    key = lambda n: re.sub(r'[^a-z0-9]', '', (n or '').lower())

    # ---- FIX 1, the five missing software rounds -------------------------------------------
    have = set((x['company_name'], x['date_iso']) for x in rows)
    added = 0
    for m in MISSING:
        if (m['company'], m['iso']) in have:
            print('  already present, skipped: %s %s' % (m['company'], m['iso']))
            continue
        row = {c: '' for c in cols}
        row.update(
            transaction_id='%s-%s' % (key(m['company']), m['iso']),
            company_key=key(m['company']), company_name=m['company'],
            date=m['date'], date_iso=m['iso'], round_type=m['rt'],
            post_money_musd='%.1f' % m['post'], valuation_status='Disclosed',
            revenue_metric=m['basis'], revenue_musd='%.3f' % m['val'],
            revenue_status='Disclosed', ev_revenue_x=m['mult'],
            revenue_basis='ARR' if m['metric'] == 'ARR' else 'ARR_RUNRATE',
            revenue_period='RUN_RATE', denominator_basis=m['basis'],
            subsector_as_supplied=m['sub'], screening_category_as_supplied=m['cat'],
            round_source_url=m['url'], revenue_source_url=m.get('revurl', m['url']),
            transaction_type='PRIMARY', verification='SHEET_02SEP', in_medians='1',
            bound='<=' if '>' in m['basis'] or 'threshold' in m['basis'].lower() else '',
            notes=('LOADED 02-Sep-2026. MISSED BY THE FIRST PASS: '
                   'tools/load_daniil_sheet_2sep.py deduplicated on company rather than on company '
                   'and round, so this round was skipped because we already held a different round '
                   'for the same company. Figures, basis and URLs are Daniil\'s.'),
        )
        rows.append(row)
        added += 1
        print('  inserted %-12s %-8s post %-9s %s %s -> %sx' %
              (m['company'], m['date'], m['post'], m['metric'], m['val'], m['mult']))

    # ---- FIX 2, Daniil's ruling ------------------------------------------------------------
    back = 0
    for x in rows:
        if (x['company_name'], x['date']) in REINSTATE and x['in_medians'] == '0':
            x['in_medians'] = '1'
            x['notes'] = (x['notes'] or '') + RULING
            back += 1

    # Coalition: GWP is volume, not revenue. Move it rather than delete it.
    for x in rows:
        if x['company_name'] == 'Coalition' and x['date'] == 'Jul-22':
            x['volume_metric'] = 'GROSS_WRITTEN_PREMIUM'
            x['volume_musd'] = x['revenue_musd']
            x['volume_period'] = x['denominator_basis']
            x['volume_basis'] = 'GROSS_WRITTEN_PREMIUM'
            x['ev_volume_x'] = x['ev_revenue_x']
            x['revenue_musd'] = x['ev_revenue_x'] = x['revenue_metric'] = ''
            x['revenue_basis'] = 'NONE'
            x['revenue_period'] = ''
            x['notes'] = (x['notes'] or '') + (
                ' RECLASSIFIED 02-Sep-2026: the denominator is annualised GROSS WRITTEN PREMIUM. '
                'For an insurer GWP is the volume flowing through the book, the analogue of GMV, '
                'not the insurer\'s own revenue. Moved from the revenue fields to the volume '
                'fields, where 6.76x is usable as a volume multiple.')
            print('  reclassified Coalition Jul-22 to a volume multiple')

    rows.sort(key=lambda x: x['date_iso'], reverse=True)
    head = ''.join(l for l in open(DST).read().splitlines(True) if l.startswith('#'))
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=cols, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    open(DST, 'w').write(head + out.getvalue())
    print('%s: %d rounds inserted, %d rows put back in the medians, %d rows total'
          % (DST, added, back, len(rows)))

    # ---- Whatnot into the consumer file ----------------------------------------------------
    cr = rd(CONS)
    ccols = cr.fieldnames
    crows = list(cr)
    if not any(x['company_name'] == 'Whatnot' and x['date_iso'] == '2025-01' for x in crows):
        row = {c: '' for c in ccols}
        row.update(
            transaction_id='whatnot-2025-01', company_key='whatnot', company_name='Whatnot',
            date='Jan-25', date_iso='2025-01', round_type='Series E',
            transaction_type='PRIMARY', post_money_musd='4970.0', currency='USD',
            gmv_metric='GMV', gmv_musd='3000.0', gmv_period='FY2024', gmv_basis='GMV',
            ev_gmv_x='1.66', verification='SHEET_02SEP', in_medians='1',
            round_source_url='https://techcrunch.com/2025/01/08/livestream-shopping-app-whatnot-raises-265m-pinning-valuation-at-nearly-5b/',
            revenue_source_url='https://www.greycroft.com/perspectives/reimagining-commerce-leading-whatnots-series-e/',
            notes=('LOADED 02-Sep-2026 from Daniil\'s 191-row sheet. Missed by the first pass, which '
                   'deduplicated on company rather than on company and round.'),
        )
        crows.append(row)
        crows.sort(key=lambda x: x['date_iso'], reverse=True)
        chead = ''.join(l for l in open(CONS).read().splitlines(True) if l.startswith('#'))
        out = io.StringIO()
        w = csv.DictWriter(out, fieldnames=ccols, lineterminator='\n')
        w.writeheader()
        w.writerows(crows)
        open(CONS, 'w').write(chead + out.getvalue())
        print('%s: Whatnot Jan-25 inserted, %d rows total' % (CONS, len(crows)))
    else:
        print('%s: Whatnot Jan-25 already present' % CONS)


if __name__ == '__main__':
    main()
