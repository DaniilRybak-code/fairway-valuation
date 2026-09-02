# -*- coding: utf-8 -*-
"""Compare Daniil's realigned private-transactions database against what the engine holds.

Neither side is assumed right. The output is three lists: rows where the multiple disagrees, rows
he has that we do not, and rows we have that he does not. Matching is on company plus month, since
his dates are full and ours are month-year.
"""
import csv, io, os, sys, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
import match_reference as M

MON = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
       '07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
def key(name, date):
    n = re.sub(r'[^a-z0-9]', '', (name or '').lower())
    n = n.replace('athleticgreens','').replace('luminati','').replace('cursor','')
    return n, (date or '').strip()

def his_date(d):
    d = (d or '').strip()
    m = re.match(r'^(\d{4})-(\d{2})', d)
    return '%s-%s' % (MON[m.group(2)], m.group(1)[2:]) if m else d

body = [l for l in open(os.path.join(HERE, 'data/raw/2026-09-01_private-transactions-daniil.csv')) if not l.lstrip().startswith('#')]
HIS = list(csv.DictReader(io.StringIO(''.join(body))))
his = {}
for r in HIS:
    his[key(r['company'], his_date(r['txn_date']))] = r
ours = {}
for r in M.private:
    ours[key(r.get('company_name'), r.get('date'))] = r

def f(v):
    try: return float(str(v).replace('x','').strip())
    except (ValueError, TypeError): return None

both = sorted(set(his) & set(ours))
print('rows in his file (transcribed) : %d' % len(HIS))
print('rows in ours                   : %d' % len(M.private))
print('matched on company + month     : %d' % len(both))
print()
print('=== 1. MATCHED BUT THE MULTIPLE DISAGREES ===')
dis = 0
for k in both:
    h, o = f(his[k]['mult_reported']), f(ours[k].get('mult'))
    if h is None or o is None:
        if (h is None) != (o is None):
            dis += 1
            print('  %-24s %-8s his %-9s ours %-9s  ONE SIDE HAS NO MULTIPLE' % (
                his[k]['company'][:23], his[k]['txn_date'], h if h is not None else 'none', o if o is not None else 'none'))
        continue
    if abs(h - o) / max(abs(h), abs(o)) > 0.02:
        dis += 1
        print('  %-24s %-8s his %-9.2f ours %-9.2f  %s' % (
            his[k]['company'][:23], his[k]['txn_date'], h, o, his[k]['denominator_basis'][:38]))
print('  %d disagreements' % dis)
print()
print('=== 2. HE HAS, WE DO NOT ===')
missing = sorted(set(his) - set(ours), key=lambda k: his[k]['txn_date'], reverse=True)
for k in missing:
    r = his[k]
    print('  %-24s %-11s %-9s %-16s %s' % (r['company'][:23], r['txn_date'], r['mult_reported'], r['metric_type'], r['denominator_basis'][:34]))
print('  %d rows' % len(missing))
print()
print('=== 3. WE HAVE, HE DOES NOT (within the dates his screenshots cover) ===')
extra = [k for k in set(ours) - set(his)]
print('  %d rows, listing only those with a priced multiple:' % len(extra))
for k in sorted(extra, key=lambda k: (ours[k].get('company_name') or '')):
    o = ours[k]
    if o.get('mult') is not None:
        print('  %-24s %-8s %-8s %s' % ((o.get('company_name') or '')[:23], o.get('date'), o.get('mult'), (o.get('revenue_basis') or '')))
