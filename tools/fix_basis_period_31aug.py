# -*- coding: utf-8 -*-
"""Fix the period labels the audit caught, and record HOW WE KNOW each basis.

TWO DIFFERENT PROBLEMS CAME OUT OF tools/audit_basis_period.py AND THEY NEED DIFFERENT ANSWERS.

TEN ROWS ARE SIMPLY MISLABELLED ON PERIOD and the row's own words say so. A denominator described
as "annualized" or "run rate" is not a trailing year, and one described as "expected", "forecast" or
"projection" is forward looking. Those are corrected here.

FORTY-TWO ROWS CARRY A BASIS THE SOURCE NEVER STATED. "FY2021 revenue" does not say gross or net;
somebody read the business model and wrote NET_REVENUE. Usually that is right and occasionally it
is badly wrong, and until now the file could not tell the two apart. So a new column records how we
know: STATED means the source says it in words, INFERRED means we read it off the business model.

THE TEST FOR GROSS IS NOT "IS IT A BIG NUMBER". It is whether the line contains money that belongs
to somebody else. A freight broker's revenue holds the carrier's money; a staffing platform's holds
the worker's wage; a marketplace's commission does not. A first-party retailer keeps the whole sale
price, so its revenue is NET in our sense even though it looks gross next to a commission.
"""
import csv, io, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

def split(p):
    L = open(p).readlines(); head, body, st = [], [], False
    for l in L:
        if not st and (l.lstrip('"').startswith('#') or not l.strip()): head.append(l); continue
        st = True; body.append(l)
    return head, list(csv.DictReader(io.StringIO(''.join(body))))

def write(p, head, rows):
    w = io.StringIO(); o = csv.DictWriter(w, fieldnames=list(rows[0].keys()))
    o.writeheader(); o.writerows(rows); open(p, 'w').write(''.join(head) + w.getvalue())

PERIOD = {
 'loadsmart-2022-02': ('LTM', 'The closed FY2021 floor is what we use; the projected doubling is excluded, so this IS trailing. Audit false positive, label confirmed.'),
 'loadsmart-2020-11': ('NTM', 'The denominator is an EXPECTED 2020 figure published at pricing. Forward, not trailing.'),
 'skims-2025-11':     ('NTM', 'FY2025E net sales is an estimate for a year not yet closed. Forward.'),
 'skims-2023-07':     ('NTM', 'FY2023 FORECAST net sales. Forward.'),
 'liquid-death-2022-10': ('NTM', 'FY2022 company projection. Forward.'),
 'mews-2024-03':      ('RUN_RATE', 'Annualized net revenue, not a trailing year.'),
 'creditas-2025-12':  ('RUN_RATE', 'A single quarter multiplied by four. Not a trailing year.'),
 'creditas-2022-07':  ('RUN_RATE', 'A half year multiplied by two. Not a trailing year.'),
 'creditas-2020-12':  ('RUN_RATE', 'A single quarter multiplied by four. Not a trailing year.'),
 'jobandtalent-2021-12': ('RUN_RATE', 'The source says annual revenue RUN RATE in those words.'),
}

# How we know the basis. Anything not listed keeps whatever it has and is marked INFERRED.
STATED = {
 'loadsmart-2022-02', 'loadsmart-2020-11', 'marqeta-2020-05', 'zepz-2021-08', 'jobandtalent-2021-12',
 'delhivery-2021-05', 'xpressbees-2022-02', 'shiprocket-2022-08', 'olipop-2025-02', 'gorillas-2021-10',
 'guesty-2024-04', 'klarna-2021-06', 'klarna-2022-07',
}
# Rows where the inference could be an order of magnitude wrong and a human must read the filing.
HIGH_RISK = {
 'flipkart-2021-07': 'Flipkart India Pvt Ltd is the WHOLESALE entity, not the marketplace entity. Its revenue is gross B2B sales, not commission. If so this is a gross multiple sitting in net ranges.',
 'flipkart-2023-07': 'Same entity question as the 2021 row.',
 'pinelabs-2021-05': 'Revenue from operations on an Indian payments company may include pass-through interchange. If it does, the line is gross.',
 'stockx-2021-04': 'StockX takes possession of goods for authentication, which can push it into gross revenue recognition rather than a marketplace commission.',
 'dlocal-2021-04': 'dLocal reports Total revenues before cost of services. Whether that is gross of network and processing costs decides the basis.',
}

def main():
    n_per = n_conf = n_risk = 0
    for f in ('private-rounds.csv', 'private-rounds-consumer.csv'):
        p = os.path.join(D, f); head, rows = split(p)
        flds = list(rows[0].keys())
        for c in ('revenue_basis_source', 'basis_risk_note'):
            if c not in flds: flds.append(c)
        for r in rows:
            for c in ('revenue_basis_source', 'basis_risk_note'): r.setdefault(c, '')
            tid = r['transaction_id']
            if tid in PERIOD:
                new, why = PERIOD[tid]
                if r.get('revenue_period') != new:
                    r['revenue_period'] = new; n_per += 1
                r['basis_risk_note'] = (r.get('basis_risk_note') or '') + ' PERIOD: ' + why
            if (r.get('revenue_basis') or '').strip().upper() in ('', 'NONE'):
                r['revenue_basis_source'] = ''
            elif tid in STATED:
                r['revenue_basis_source'] = 'STATED'; n_conf += 1
            else:
                r['revenue_basis_source'] = 'INFERRED'; n_conf += 1
            if tid in HIGH_RISK:
                r['basis_risk_note'] = (r.get('basis_risk_note') or '') + ' BASIS RISK: ' + HIGH_RISK[tid]
                r['revenue_basis_source'] = 'INFERRED_HIGH_RISK'; n_risk += 1
        rows = [{k: r.get(k, '') for k in flds} for r in rows]
        write(p, head, rows)
        print('  %-30s written' % f)
    print('%d period labels corrected, %d rows given a basis source, %d flagged high risk'
          % (n_per, n_conf, n_risk))

if __name__ == '__main__':
    main()
