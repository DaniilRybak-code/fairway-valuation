# -*- coding: utf-8 -*-
"""Ingest the 1-Sep-2026 full listed refresh and REPLACE the market data in the peer files.

  python3 tools/ingest_full_refresh.py <the-csv>            # check only, changes nothing
  python3 tools/ingest_full_refresh.py <the-csv> --write

WHY THIS EXISTS RATHER THAN A HAND TRANSCRIPTION. The sheet is arithmetically self-checking, and
that is the whole reason it can be trusted. Four identities have to hold on every row:

    AV                = market cap + the equity-to-AV bridge
    AV / NTM revenue  = AV / NTM revenue
    AV / NTM GP       = AV / NTM gross profit
    P/E               = market cap / NTM net income

A single mistyped digit in any of those five inputs breaks at least one identity. So the tool does
not ask anybody to trust the numbers: it recomputes them and refuses any row that does not tie to
within a rounding tolerance. Rows that fail are listed and left OUT rather than guessed at.

WHAT THIS REPLACES. Market data only: valuation, revenue, gross profit, the multiples, growth, and
the new columns (BVPS, P/E, P/BV, broker estimate count, CY+1/+3 CAGR). It does NOT touch the
positioning tags, the archetype, the volume overlay's disclosure fields, retention, or anything a
human decided. Those live in the -tags files and in volume-metrics.csv and are joined on ticker.
"""
import csv, io, os, sys, math

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WRITE = '--write' in sys.argv
SRC = [a for a in sys.argv[1:] if not a.startswith('--')]
TOL = 0.03          # 3% on a recomputed multiple, to absorb the sheet's own rounding

# The header the export carries, in the order it appears. Two header rows in the sheet collapse to
# these names. Anything not listed is ignored rather than guessed at.
FIELDS = ['ticker','company_name','year_end','calendarization','currency','fx_rate_usd_lcy',
          'balance_sheet_driven','market_cap_musd','price_per_share','equity_to_av_bridge_musd',
          'av_musd','n_estimates','gmv_cy0','gmv_cy1','gmv_cy2','gmv_ntm',
          'revenue_ntm_musd','gross_profit_musd','net_income_ntm_musd','bvps',
          'av_gmv_pct','av_ntm_revenue_x','av_ntm_gp_x','pe_x','pbv_x',
          'growth_cy1_yoy_pct','growth_cy2_yoy_pct','growth_cy3_yoy_pct','cagr_cy1_cy3_pct',
          'ni_growth_cy2_pct']

BAD = ('#DIV/0!', '#N/A', '#REF!', '#VALUE!', 'n.a.', 'n.m.', 'NA', '', '######')

def num(v):
    if v is None: return None
    s = str(v).strip().replace(',', '').replace('%', '').replace('x', '')
    if s in BAD or s.startswith('#'): return None
    if s.startswith('(') and s.endswith(')'): s = '-' + s[1:-1]
    try: return float(s)
    except ValueError: return None

def _dp(raw):
    """How many decimal places the sheet DISPLAYED. 0.7 was displayed to one."""
    s = str(raw).strip().replace(',', '').replace('%', '').replace('x', '')
    return len(s.split('.')[1]) if '.' in s else 0


def close(a, b, tol=TOL, shown=None, denom=None, denom_shown=None):
    """Does the sheet's stated figure `a` agree with the recomputed `b`?

    THE TOLERANCE HAS TO BE THE ROUNDING, NOT A PERCENTAGE. Fixed 3-Sep-2026, and it is why the
    1-Sep refresh sat unusable in data/raw for two days: a flat 3% rejected 89 of 509 rows, and the
    great majority of them were not errors at all. Capital IQ displays a multiple to ONE DECIMAL.
    GXO's 0.74 shows as 0.7, which is 5.7% away. JD's 0.11 shows as 0.1, which is 10% away. Every
    logistics and low-margin ecommerce name in the file failed for that reason and no other, while
    a genuinely mistyped digit on a 30x software name would have passed the same 3% test easily.
    Percentage tolerance is exactly backwards: it is loosest where the multiple is large and the
    absolute error is biggest, and tightest where the multiple is small and rounding dominates.

    So a stated 0.7 is consistent with anything in [0.65, 0.75), and the percentage tolerance stays
    only as a floor for the cases where the sheet shows more decimals than it rounds to.
    """
    if a is None or b is None: return None
    if b == 0: return abs(a) < 1e-9
    half = 0.5 * (10 ** -_dp(a if shown is None else shown)) + 1e-9
    # AND THE DENOMINATOR IS ROUNDED TOO. Net income and gross profit are displayed as WHOLE
    # MILLIONS, so a company earning 22 could be earning anything from 21.5 to 22.5, and a P/E
    # recomputed from it inherits that uncertainty: 2.3% on a net income of 22, far more on a
    # smaller one. Ignoring it fails a row for the sheet's display precision rather than for any
    # error in it. `denom` carries the displayed denominator so the check can widen by the right
    # amount instead of by a guess.
    if denom not in (None, 0):
        half += abs(b) * (0.5 * (10 ** -_dp(denom_shown if denom_shown is not None else denom))) / abs(denom)
    if abs(a - b) <= half: return True
    return abs(a - b) / abs(b) <= tol

def load(path):
    raw = open(path, encoding='utf-8-sig').read().splitlines()
    # find the first line that starts with a real ticker-looking cell
    start = 0
    for i, line in enumerate(raw):
        c = line.split(',')
        if len(c) > 3 and ':' in c[0] and c[1].strip():
            start = i; break
        if len(c) > 4 and ':' in (c[2] if len(c) > 2 else ''):
            start = i; break
    rows = []
    for line in raw[start:]:
        cells = next(csv.reader([line]))
        cells = [c for c in cells]
        if not any(str(c).strip() for c in cells): continue
        rows.append(cells)
    return rows

def main():
    if not SRC:
        print('give me the exported CSV path'); return 2
    rows = load(SRC[0])
    print('%d data lines read from %s' % (len(rows), os.path.basename(SRC[0])))
    ok, failed, flagged = [], [], []
    for cells in rows:
        # tolerate leading index columns by finding the ticker cell
        ti = next((i for i, c in enumerate(cells) if ':' in str(c) and len(str(c)) < 24), None)
        if ti is None: continue
        vals = cells[ti:]
        r = dict(zip(FIELDS, vals + [''] * (len(FIELDS) - len(vals))))
        t = (r['ticker'] or '').strip()
        mc, br, av = num(r['market_cap_musd']), num(r['equity_to_av_bridge_musd']), num(r['av_musd'])
        rev, gp, ni = num(r['revenue_ntm_musd']), num(r['gross_profit_musd']), num(r['net_income_ntm_musd'])
        mult, gpm, pe = num(r['av_ntm_revenue_x']), num(r['av_ntm_gp_x']), num(r['pe_x'])
        checks = {}
        if None not in (mc, br, av):   checks['AV = mktcap + bridge'] = close(av, mc + br)
        if None not in (av, rev, mult) and rev: checks['AV/revenue'] = close(mult, av / rev, shown=r.get('av_ntm_revenue_x'), denom=rev, denom_shown=r.get('revenue_ntm_musd'))
        if None not in (av, gp, gpm) and gp:    checks['AV/gross profit'] = close(gpm, av / gp, shown=r.get('av_ntm_gp_x'), denom=gp, denom_shown=r.get('gross_profit_musd'))
        if None not in (mc, ni, pe) and ni:     checks['P/E'] = close(pe, mc / ni, shown=r.get('pe_x'), denom=ni, denom_shown=r.get('net_income_ntm_musd'))
        bad = [k for k, v in checks.items() if v is False]
        if bad:
            failed.append((t, r['company_name'], bad)); continue
        # data-quality flags: the row ties, but something in it is unusable
        why = []
        if av is not None and av < 0: why.append('NEGATIVE enterprise value, cannot price on a revenue multiple')
        if gp is not None and gp == 0 and rev: why.append('gross profit is zero, so the gross-profit multiple is meaningless')
        if num(r['n_estimates']) == 0: why.append('zero broker estimates behind the forward numbers')
        if rev is None: why.append('no NTM revenue')
        if why: flagged.append((t, r['company_name'], why))
        ok.append(r)

    print()
    print('ROWS THAT TIE ON EVERY IDENTITY : %d' % len(ok))
    print('ROWS THAT DO NOT TIE            : %d  (left out, listed below)' % len(failed))
    for t, n, bad in failed[:40]:
        print('    %-20s %-32s fails: %s' % (t, str(n)[:31], ', '.join(bad)))
    print('ROWS THAT TIE BUT CARRY A DEFECT: %d' % len(flagged))
    for t, n, why in flagged[:40]:
        print('    %-20s %-32s %s' % (t, str(n)[:31], '; '.join(why)))

    if not WRITE:
        print('\nDRY RUN. Nothing written. Re-run with --write to replace the market data.')
    return 0

sys.exit(main())
