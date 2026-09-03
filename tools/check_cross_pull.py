# -*- coding: utf-8 -*-
"""Where two of Daniil's own screens disagree about the same company.

Fifteen tickers appear in more than one peers pull, because a neobank is both a fintech and a
lender and MercadoLibre is both a marketplace and a payments business. The loader keeps ONE row per
ticker, so when two pulls carry different figures for the same measure, the engine silently uses
whichever file loaded first and nothing anywhere says the other exists.

MercadoLibre, 3-Sep-2026, is the case that prompted this. Both pulls are dated 2026-08-30 and both
carry an identical enterprise value of $104,938m. They differ on NTM revenue:

    ecommerce pull   49,038  ->  2.1x
    fintech pull     46,874  ->  2.2x

The ecommerce figure is the one that reconciles. Both pulls agree CY2027 revenue is 53,210, and the
ecommerce pull gives CY2026 as 41,673. Next twelve months from 30-Aug-2026 is four months of 2026
and eight of 2027: 0.333 x 41,673 + 0.667 x 53,210 = 49,364, which is 0.7% from the ecommerce
figure and 5% from the fintech one. So 2.1x stands and the fintech row's NTM is the outlier.

This check exists because the peers files are REFRESHED from the screens, so a note written into one
would be overwritten by the next pull. A check re-fires every time.
"""
import csv
import io
import os
import sys
import collections

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import match_reference as M                      # noqa: E402

FILES = ['data/peers-software.csv', 'data/peers-ecommerce.csv', 'data/peers-fintech.csv',
         'data/peers-logistics-services.csv', 'data/peers-lending.csv']
# A measure worth comparing. Identifiers, row numbers and dates are not.
SKIP = {'row', 'as_of', 'country', 'exchange_ticker', 'company_name', 'sector_block',
        'in_medians', 'in_stats', 'paying_users_basis', 'mix_note'}
TOLERANCE = 0.02          # two per cent. Below that it is rounding, not disagreement.
# Growth measured over different windows is NOT a disagreement, and the loader already records
# which window each row carries. Comparing them would report a fact as a fault.
DIFFERENT_BY_DESIGN = {'revenue_growth_ntm_pct', 'revenue_growth_cagr_cy0_cy2_pct',
                       'revenue_growth_cagr_cy1_cy3_pct', 'revenue_growth_pct',
                       'revenue_growth_cy1_pct', 'revenue_growth_cy2_pct',
                       'revenue_local_cy0', 'revenue_local_cy1', 'revenue_local_cy2',
                       'revenue_local_cy3'}


def num(v):
    try:
        return float(str(v).strip().replace(',', ''))
    except (TypeError, ValueError):
        return None


def rows_of(path):
    lines = [l for l in io.open(path, encoding='utf-8')
             if l.strip() and not l.lstrip('"').startswith('#')]
    return list(csv.DictReader(lines))


def main():
    by = collections.defaultdict(dict)
    for path in FILES:
        if not os.path.exists(path):
            continue
        for d in rows_of(path):
            t = (d.get('exchange_ticker') or '').strip()
            if not t:
                continue
            try:
                k = M.norm(t)
            except Exception:
                k = t
            by[k][os.path.basename(path)] = d
    shared = {k: v for k, v in by.items() if len(v) > 1}
    print('%d tickers appear in more than one peers pull.\n' % len(shared))
    found = 0
    for k, files in sorted(shared.items()):
        names = sorted(files)
        rows = [files[n] for n in names]
        cols = set(rows[0].keys())
        for r in rows[1:]:
            cols &= set(r.keys())
        bad = []
        for c in sorted(cols):
            if c in SKIP or c in DIFFERENT_BY_DESIGN or not c or c.startswith('#'):
                continue
            vals = [(n, num(files[n].get(c))) for n in names]
            vals = [(n, v) for n, v in vals if v is not None]
            if len(vals) < 2:
                continue
            lo, hi = min(v for _n, v in vals), max(v for _n, v in vals)
            if abs(hi) < 1e-9:
                continue
            if abs(hi - lo) / max(abs(hi), abs(lo)) > TOLERANCE:
                bad.append((c, vals))
        if bad:
            found += 1
            print('=== %s  %s ===' % (rows[0].get('company_name', k), k))
            for c, vals in bad:
                print('   %-26s %s' % (c, '   '.join('%s %s' % (n.replace('peers-', '').replace('.csv', ''), v)
                                                     for n, v in vals)))
            # WHICH PULL RECONCILES. An enterprise value should equal market capitalisation plus
            # the equity-to-EV bridge the same row carries. A pull that shows its working and adds
            # up is better evidence than one that states a number with no components, and this is
            # objective rather than a preference. nCino is the case: the fintech pull gives net debt
            # 224 and minority interest 14, so 2,259 + 238 = 2,497, and it ties. The software pull
            # gives 2,630 with no bridge at all, which is 371 above market capitalisation with
            # nothing shown to explain it.
            for n in names:
                d = files[n]
                mc, br, ev = num(d.get('market_cap_musd')), num(d.get('equity_to_av_bridge_musd') or d.get('eqv_ev_bridge_musd')), num(d.get('enterprise_value_musd'))
                if mc is None or ev is None:
                    continue
                if br is None:
                    print('   %-14s EV %s stated with NO bridge components' % (n.replace('peers-', '').replace('.csv', ''), ev))
                elif abs((mc + br) - ev) <= max(1.0, 0.005 * abs(ev)):
                    print('   %-14s EV RECONCILES: %s market cap + %s bridge = %s' % (n.replace('peers-', '').replace('.csv', ''), mc, br, ev))
                else:
                    print('   %-14s EV DOES NOT RECONCILE: %s + %s is not %s' % (n.replace('peers-', '').replace('.csv', ''), mc, br, ev))
            loaded = [r for r in M.listed if (r.get('exchange_ticker') or '') == k
                      or M.norm(r.get('exchange_ticker') or '') == k]
            if loaded:
                print('   THE ENGINE USES %s' % os.path.basename(loaded[0].get('_src_file') or '?'))
            print()
    if not found:
        print('PASS: where a company sits in two pulls, the pulls agree to within %.0f%%.' % (100 * TOLERANCE))
    else:
        print('%d companies where two of your own pulls disagree by more than %.0f%% on a measure.'
              % (found, 100 * TOLERANCE))
        print('The engine uses one row and shows nothing about the other. Each needs a ruling on')
        print('which pull is right, or a note saying why they differ.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
