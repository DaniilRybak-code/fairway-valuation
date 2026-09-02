#!/usr/bin/env python3
"""
Repairs four rows of data/private-rounds.csv where `revenue_musd` holds a figure in the LOCAL
currency while the stored multiple was computed off a USD figure that was never written down.

THIS IS THE SAME CLASS OF ERROR AS THE DROPPED AA/AB COLUMNS. In three of the four cases Daniil's
own sheet already carried the correct USD number and we loaded the local-currency one instead. In
the fourth our own note carries it. Nothing here is derived by us; every replacement value is
quoted from a file already in the repo.

  Creditas Dec-25   592.1 BRL -> 445.4 USD   his sheet: "Q3 2025 annualized x4 to USD", 445.4
  Creditas Jul-22   846.1 BRL -> 304.0 USD   our note: "Multiple = US$4,800m / (~US$152m x 2)"
  Creditas Dec-20    78.8 BRL ->  56.0 USD   his sheet: "Q3 2020 revenue annualized x4 from BRL 78.8", 56.0
  Jobandtalent      1000.0 EUR -> 1130.0 USD our note: "CB Insights translated >EUR1.0bn as >US$1.13bn"

Each replacement reconciles the row exactly: post_money_musd / new revenue == the stored multiple,
to the second decimal. That reconciliation is the test, and it is asserted below.

Jobandtalent also gains the FX rate and date. Daniil's sheet cites the rate source itself,
https://www.xrates.eu/exchange-rate-1-december-2021, so the rate is recorded rather than assumed.
"""
import csv, io, sys

PATH = 'data/private-rounds.csv'

FIX = {
    ('Creditas', 'Dec-25'): dict(revenue_musd='445.400', expect=7.41,
        note_add=' FX REPAIR 02-Sep-2026: revenue_musd held the BRL figure 592.1 while the multiple '
                 'used the USD figure. Daniil\'s sheet row carries 445.4 USD, "Q3 2025 annualized x4 '
                 'to USD". Restated to 445.4.'),
    ('Creditas', 'Jul-22'): dict(revenue_musd='304.000', expect=15.79,
        note_add=' FX REPAIR 02-Sep-2026: revenue_musd held the BRL figure 846.1 while the multiple '
                 'used the USD figure named in this row\'s own note, ~US$152m x 2 = US$304m. '
                 'Restated to 304.0.'),
    ('Creditas', 'Dec-20'): dict(revenue_musd='56.000', expect=31.25,
        note_add=' FX REPAIR 02-Sep-2026: revenue_musd held the BRL QUARTERLY figure 78.8 while the '
                 'multiple used the USD annualised figure. Daniil\'s sheet row carries 56.0 USD, '
                 '"Q3 2020 revenue annualized x4 from BRL 78.8". Restated to 56.0.'),
    ('Jobandtalent', 'Dec-21'): dict(revenue_musd='1130.000', expect=2.08,
        fx_rate='1.1300', fx_date='2021-12-01',
        note_add=' FX REPAIR 02-Sep-2026: revenue_musd held the EUR figure 1,000.0 while the multiple '
                 'used US$1,130m, as this row\'s own note already said. Restated to 1130.0 and the '
                 'rate recorded. Rate source cited in Daniil\'s sheet: '
                 'https://www.xrates.eu/exchange-rate-1-december-2021'),
}


def main():
    raw = open(PATH).read()
    head = ''.join(l for l in raw.splitlines(True) if l.startswith('#'))
    body = ''.join(l for l in raw.splitlines(True) if not l.startswith('#'))
    rd = csv.DictReader(io.StringIO(body))
    cols = rd.fieldnames
    rows = list(rd)

    done = 0
    for r in rows:
        k = (r['company_name'], r['date'])
        if k not in FIX:
            continue
        f = FIX[k]
        before = r['revenue_musd']
        r['revenue_musd'] = f['revenue_musd']
        if 'fx_rate' in f:
            r['fx_rate'] = f['fx_rate']
            r['fx_date'] = f['fx_date']
        r['notes'] = (r['notes'] or '') + f['note_add']
        calc = float(r['post_money_musd']) / float(r['revenue_musd'])
        assert abs(calc - f['expect']) < 0.01, (k, calc, f['expect'])
        print('  %-14s %-8s revenue_musd %-10s -> %-10s  post/rev %.2fx == stored %s' %
              (k[0], k[1], before, r['revenue_musd'], calc, r['ev_revenue_x']))
        done += 1

    if done != len(FIX):
        sys.exit('expected %d rows, repaired %d' % (len(FIX), done))

    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=cols, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    open(PATH, 'w').write(head + out.getvalue())
    print('%s rewritten, %d rows repaired, %d rows total' % (PATH, done, len(rows)))


if __name__ == '__main__':
    main()
