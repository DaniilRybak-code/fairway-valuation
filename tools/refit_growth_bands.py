#!/usr/bin/env python3
"""Refit the private growth bands from the distribution, and print the boundaries.

Run this whenever growth coverage on the private rounds grows materially. The boundaries in
selector/match_reference.py are OUTPUTS of this script, not choices, and they should be updated
from it rather than by taste.

Method. Growth rates are strictly positive and heavily right-skewed, so a Gaussian on the raw rate
is the wrong model: on our data it has a skew of +3.2 and an excess kurtosis of +11.8. Taking
ln(1+g) pulls that to +1.2 and +1.7, and a Kolmogorov-Smirnov test does not reject log-normality.
Band boundaries are then plus and minus half a standard deviation in log space, which splits a
normal into roughly 31 / 38 / 31 per cent.
"""
import csv, io, math, os, sys, statistics as st, collections
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def load(p):
    lines = open(p, encoding='utf-8').read().split('\n')
    raw = [l for l in lines if not l.lstrip('"').startswith('#') and l.strip()]
    return list(csv.DictReader(io.StringIO('\n'.join(raw))))

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None

g = []
for f in ('private-rounds.csv', 'private-rounds-consumer.csv'):
    for r in load(os.path.join(D, f)):
        v = num(r.get('growth_pct_at_round'))
        if v is not None and 1 + v/100.0 > 0: g.append(v)
if len(g) < 12:
    sys.exit('only %d growth points, too few to refit' % len(g))

lv = [math.log(1 + x/100.0) for x in g]
mu, sd = st.mean(lv), st.pstdev(lv)
n = len(lv)
def mom(v, m, s): return (sum(((x-m)/s)**3 for x in v)/len(v), sum(((x-m)/s)**4 for x in v)/len(v) - 3)
rm, rs = st.mean(g), st.pstdev(g)
sk_raw, ku_raw = mom(g, rm, rs)
sk_log, ku_log = mom(lv, mu, sd)
cdf = lambda z: 0.5*(1+math.erf(z/math.sqrt(2)))
sv = sorted(lv)
ks = max(max(abs((i+1)/n - cdf((x-mu)/sd)), abs(i/n - cdf((x-mu)/sd))) for i, x in enumerate(sv))
crit = 1.36/math.sqrt(n)
back = lambda z: (math.exp(mu + z*sd) - 1) * 100
lo, hi = back(-0.5), back(0.5)

print('n = %d private rounds carrying a growth rate' % n)
print('raw scale      skew %+.2f  excess kurtosis %+.2f' % (sk_raw, ku_raw))
print('ln(1+g) scale  skew %+.2f  excess kurtosis %+.2f   mu %.3f  sd %.3f' % (sk_log, ku_log, mu, sd))
print('KS D = %.3f against 5%% critical %.3f  ->  %s' % (ks, crit, 'log-normal not rejected' if ks < crit else 'LOG-NORMAL REJECTED, do not use these boundaries'))
print('typical private round (geometric mean) = %.0f%%' % back(0))
print('BOUNDARIES:  MATURE below %.0f%%   GROWING %.0f%% to %.0f%%   HYPER above %.0f%%' % (lo, lo, hi, hi))
c = collections.Counter('MATURE' if x < lo else ('GROWING' if x <= hi else 'HYPER') for x in g)
print('split: %s' % dict(c))
