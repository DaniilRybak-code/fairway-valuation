# -*- coding: utf-8 -*-
"""Check MY TRANSCRIPTION of the 1-Sep listed refresh. Not Daniil's arithmetic, which was already
verified where it came from. This asks only: did I copy the digits correctly?

Four identities, tested the way the SHEET rounds rather than on a flat percentage, because a
multiple displayed to one decimal place cannot tie to better than that:

    AV            = market cap + equity-to-AV bridge      (to within 1 unit of component rounding)
    AV / NTM rev  rounds to the displayed multiple
    AV / NTM GP   rounds to the displayed multiple
    P/E           lies inside the range the rounded net income allows

  python3 tools/check_listed_refresh.py         full file
  python3 tools/check_listed_refresh.py 0.15    a reproducible 15% sample
"""
import csv, io, os, sys, random
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAC = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
body = [l for l in open(os.path.join(HERE, 'data/raw/2026-09-01_listed-full-refresh.csv')) if not l.lstrip().startswith('#')]
R = list(csv.DictReader(io.StringIO(''.join(body))))

def n(v):
    v = (v or '').strip()
    if v in ('', 'na', 'nm', 'BROKEN', 'HIDDEN'): return None
    try: return float(v)
    except ValueError: return None

rows = R
if FRAC < 1.0:
    random.seed(1); rows = random.sample(R, max(1, int(len(R) * FRAC)))

fails, checks = [], 0
for r in rows:
    mc, br, av = n(r['market_cap_musd']), n(r['eqv_av_bridge_musd']), n(r['av_musd'])
    rev, gp, ni = n(r['revenue_ntm_musd']), n(r['gross_profit_musd']), n(r['net_income_musd'])
    mult, gpm, pe = n(r['av_ntm_revenue_x']), n(r['av_ntm_gp_x']), n(r['pe_x'])
    def fail(w, d): fails.append((r['ticker'], r['company_name'][:30], w, d))
    if None not in (mc, br, av):
        checks += 1
        if abs(mc + br - av) > 1.5: fail('AV = mktcap + bridge', '%g + %g = %g, transcribed %g' % (mc, br, mc + br, av))
    if None not in (av, rev, mult) and rev:
        checks += 1
        if round(av / rev, 1) != mult: fail('AV/revenue', '%g/%g = %.3f -> %.1f, transcribed %.1f' % (av, rev, av/rev, round(av/rev,1), mult))
    if None not in (av, gp, gpm) and gp:
        checks += 1
        if round(av / gp, 1) != gpm: fail('AV/gross profit', '%g/%g = %.3f -> %.1f, transcribed %.1f' % (av, gp, av/gp, round(av/gp,1), gpm))
    if None not in (mc, ni, pe) and ni and abs(ni) > 0.5:
        checks += 1
        lo, hi = sorted((mc / (ni + 0.5), mc / (ni - 0.5)))
        if not (lo * 0.99 <= pe <= hi * 1.01): fail('P/E', 'mktcap %g / NI %g gives %.1f to %.1f, transcribed %.1f' % (mc, ni, lo, hi, pe))

print('rows checked              : %d of %d' % (len(rows), len(R)))
print('identity checks performed : %d' % checks)
print('checks failed             : %d' % len(fails))
for t, c, w, d in fails: print('    %-18s %-30s %-22s %s' % (t, c, w, d))
