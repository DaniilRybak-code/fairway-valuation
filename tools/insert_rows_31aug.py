# -*- coding: utf-8 -*-
"""Insert the rounds Daniil supplied with source URLs on 31-Aug-2026.

READS data/raw/2026-08-31_private-rounds-with-sources.csv rather than repeating the numbers here,
so there is exactly one place the figures live and the raw file stays the record.

THE SILENT DROP THIS ALSO FIXES. A private round whose company_key has no row in the tags file is
skipped by the loader with `if not t: continue`. Creditas, Fundbox, Gorillas, Jobandtalent and
Loadsmart were all in that state, so inserting rounds alone would have changed nothing at all.
"""
import csv, io, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
RAW = os.path.join(D, 'raw', '2026-08-31_private-rounds-with-sources.csv')

def split(p):
    L = open(p).readlines(); head, body, started = [], [], False
    for l in L:
        if not started and (l.lstrip('"').startswith('#') or not l.strip()): head.append(l); continue
        started = True; body.append(l)
    return head, list(csv.DictReader(io.StringIO(''.join(body))))

def write(p, head, rows):
    w = io.StringIO(); o = csv.DictWriter(w, fieldnames=list(rows[0].keys()))
    o.writeheader(); o.writerows(rows); open(p, 'w').write(''.join(head) + w.getvalue())

KEY = {'AG1': 'ag1', 'Airwallex': 'airwallex', 'Creditas': 'creditas', 'Fundbox': 'fundbox',
       'Gopuff': 'gopuff', 'Gorillas': 'gorillas', 'Jobandtalent': 'jobandtalent',
       'Loadsmart': 'loadsmart', 'Marqeta': 'marqeta', 'Patreon': 'patreon',
       'Savage X Fenty': 'savage-x-fenty', 'Zepz': 'zepz', 'Zopa': 'zopa', 'dLocal': 'dlocal'}
CONSUMER = {'gopuff', 'patreon', 'ag1', 'savage-x-fenty', 'gorillas'}
# Rows already in the files under their own ruling, or not a revenue multiple. Skipped here.
SKIP = {'Marqeta|2020-05-28', 'Zepz|2021-08', 'dLocal|2021-04-02|TPV', 'Zopa|2021-10-19',
        'Creditas|2025-12-01', 'Creditas|2022-07-08', 'AG1|2022-01-01', 'Gopuff|2021-07-30',
        'Patreon|2021-04-07', 'Savage X Fenty|2021-02-01', 'dLocal|2021-04-02|Revenue'}
# revenue_basis by metric_type wording. A staffing or freight line carries the pass-through.
GROSS = {'jobandtalent', 'loadsmart'}
MON = dict(zip(range(1, 13), 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()))

def main():
    _, raw = split(RAW)
    sw, con = [], []
    for r in raw:
        co = r['company']; k = KEY.get(co)
        tag = '%s|%s' % (co, r['transaction_date'][:7] if co in ('Zepz', 'Creditas', 'AG1') else r['transaction_date'])
        if tag in SKIP or ('%s|%s|%s' % (co, r['transaction_date'], r['metric_type'])) in SKIP:
            continue
        y, m = int(r['transaction_date'][:4]), int(r['transaction_date'][5:7])
        tid = '%s-%04d-%02d' % (k, y, m)
        mult = r['numeric_multiple']
        bound = '<=' if r['comparator'].strip().startswith('<') else ''
        core = r['quality_classification'] == 'CORE'
        basis = 'GROSS_REVENUE' if k in GROSS else ('ARR_RUNRATE' if 'run-rate' in r['metric_type'] or 'Annualized' in r['metric_type'] else 'NET_REVENUE')
        row = dict(transaction_id=tid, company_key=k, company_name=co, date='%s-%s' % (MON[m], str(y)[2:]),
                   date_iso='%04d-%02d' % (y, m), round_type=r['round_type'],
                   capital_raised_musd=r['capital_raised_musd'],
                   post_money_musd=(r['implied_post_musd'] or r['valuation_musd']),
                   valuation_status=r['valuation_basis'], revenue_metric=r['exact_metric_wording'][:220],
                   revenue_musd=r['metric_value'], revenue_status=r['basis_classification'][:60],
                   ev_revenue_x=('%.2f' % float(mult)) if mult else '', bound=bound,
                   denominator_basis=r['publication_timing'][:60], revenue_basis=basis,
                   revenue_period='RUN_RATE' if basis == 'ARR_RUNRATE' else 'LTM',
                   transaction_type='PRIMARY', in_medians='1' if core else '0',
                   verification='SOURCED_31AUG', valuation_basis='REVENUE',
                   round_source_url=r['round_source_url'], revenue_source_url=r['metric_source_url'],
                   notes=('%s. %s' % (r['quality_classification'], r['methodology']))[:900],
                   subsector_as_supplied='', screening_category_as_supplied='',
                   lead_key_investors=r['investors'][:200], currency='USD',
                   lead_investor=r['investors'].split(';')[0].strip(),
                   lead_confidence='named in source',
                   other_named_investors=';'.join(r['investors'].split(';')[1:])[:200],
                   category_as_supplied='', fx_ccy=(r['metric_ccy'] if r['metric_ccy'] != 'USD' else ''))
        (con if k in CONSUMER else sw).append(row)
    for fname, rows in (('private-rounds.csv', sw), ('private-rounds-consumer.csv', con)):
        if not rows: continue
        p = os.path.join(D, fname); head, cur = split(p); flds = list(cur[0].keys())
        by = {r['transaction_id']: r for r in cur}; a = u = 0
        for n in rows:
            clean = {kk: vv for kk, vv in n.items() if kk in flds}
            if n['transaction_id'] in by: by[n['transaction_id']].update(clean); u += 1
            else:
                base = {kk: '' for kk in flds}; base.update(clean); cur.append(base); a += 1
        write(p, head, cur)
        print('  %-30s %d added, %d updated, %d rows now' % (fname, a, u, len(cur)))

if __name__ == '__main__':
    main()
