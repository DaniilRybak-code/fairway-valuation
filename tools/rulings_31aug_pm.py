# -*- coding: utf-8 -*-
"""Daniil's rulings and the four basis investigations, 31-Aug-2026 evening."""
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

E = {
 # dLocal. RESOLVED, and Daniil's expectation was right. The F-1 says revenue is "fees charged to
 # our merchants... a fixed fee per transaction or fixed percentage per transaction". $104.1m
 # against $2,064.8m of TPV is a 5.0% take rate. The merchant's money is NOT in the line, so it is
 # net by the only test that matters. It is gross of dLocal's own processing COSTS, but a cost is
 # an expense, not somebody else's money passing through. Risk flag removed.
 'dlocal-2021-04': dict(revenue_basis='NET_REVENUE', revenue_basis_source='STATED',
   basis_risk_note='RESOLVED 31-Aug-2026. F-1: revenue is fees charged to merchants, a fixed fee or '
     'fixed percentage per transaction. US$104.1m against US$2,064.8m of TPV is a 5.0 per cent take '
     'rate, so the merchant transaction value is not in the line. Net of volume, gross of dLocal own '
     'processing cost, and a cost is an expense rather than a pass-through. NET confirmed.'),

 # Pine Labs. RESOLVED as net. FY2021 revenue from operations of Rs 726.16 crore breaks down as PoS
 # terminal service charges 61 per cent, gift card and voucher PROCESSING FEES 29.2 per cent, and
 # Fave commissions of Rs 70.7 crore. Every one of those is a fee line. The gross value of the
 # vouchers and the card transactions is not in it.
 'pinelabs-2021-05': dict(revenue_basis='NET_REVENUE', revenue_basis_source='INFERRED',
   basis_risk_note='RESOLVED 31-Aug-2026. The FY2021 revenue of Rs 726.16 crore is composed of PoS '
     'terminal service charges (61 per cent), gift card and voucher processing FEES (29.2 per cent) '
     'and Fave commissions of Rs 70.7 crore. All three are fee lines; the gross value of the '
     'transactions and vouchers is not in the number. No interchange pass-through found. NET, '
     'inferred from the composition rather than from an explicit statement. Source: Entrackr, '
     '5-Jul-2022, on the filed FY21 accounts.'),

 # StockX. NOT RESOLVED, and it cannot be from public sources: StockX is private and files nothing.
 # It stays flagged and it stays out of the ranges until somebody has the accounts.
 'stockx-2021-04': dict(revenue_basis_source='INFERRED_HIGH_RISK', in_medians='0',
   basis_risk_note='UNRESOLVED 31-Aug-2026 AND NOW OUT OF RANGES BECAUSE OF IT. $400m of FY2020 GAAP '
     'revenue against roughly $1.8bn of GMV is a 22 per cent implied take rate, which is far above '
     'the roughly 12.5 per cent StockX charges in seller and processing fees. Either the GMV figure '
     'is understated or part of the revenue is recognised GROSS because StockX takes possession of '
     'goods for authentication. StockX is private and publishes no accounts, so this cannot be '
     'settled from public sources. Until it is, the row is context and does not price anybody.'),

 # FLIPKART. THE WORST ONE, AND THE NOTES ALREADY SAID SO WITHOUT ANYONE ACTING ON IT.
 # The denominator is Flipkart India Private Limited, the B2B WHOLESALE entity, whose revenue is the
 # gross sale of goods to sellers. The MARKETPLACE entity, Flipkart Internet Private Limited, earned
 # Rs 8,115 crore in FY2021 against the wholesale entity's Rs 43,357 crore. Same group, five times
 # apart, and the multiple moves from 6.4x to 34.2x depending which you divide by.
 # A marketplace founder shown 5.2x was being told something wrong by a factor of about six.
 'flipkart-2021-07': dict(revenue_basis='GROSS_REVENUE', revenue_basis_source='STATED', in_medians='0',
   basis_risk_note='RESOLVED 31-Aug-2026 AND REMOVED FROM RANGES. The denominator is Flipkart India '
     'Private Limited, the B2B WHOLESALE entity, whose revenue is the gross sale of goods to sellers '
     'and therefore GROSS by any reading. The MARKETPLACE entity, Flipkart Internet Private Limited, '
     'earned Rs 8,115 crore in FY2021 against the wholesale entity Rs 43,357 crore, which would give '
     '34.2x rather than 6.4x. Neither entity alone is the right denominator for a group valuation and '
     'no group revenue is public, so the row is context with the entity named and prices nobody.'),
 'flipkart-2023-07': dict(revenue_basis='GROSS_REVENUE', revenue_basis_source='STATED', in_medians='0',
   basis_risk_note='RESOLVED 31-Aug-2026 AND REMOVED FROM RANGES. Same entity problem as the 2021 '
     'row: the denominator is the B2B wholesale entity at Rs 56,013 crore, which is gross sale of '
     'goods. Context only.'),
}

def main():
    n = 0
    for f in ('private-rounds.csv', 'private-rounds-consumer.csv'):
        p = os.path.join(D, f); head, rows = split(p)
        for r in rows:
            e = E.get(r['transaction_id'])
            if not e: continue
            for k, v in e.items():
                if k in r: r[k] = v
                else: print('  WARNING: %s missing column %s' % (f, k))
            n += 1; print('  %-24s ruled' % r['transaction_id'])
        write(p, head, rows)
    print('%d rows ruled' % n)

if __name__ == '__main__':
    main()
