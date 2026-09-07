# -*- coding: utf-8 -*-
"""Load the 5-September public pull of 16 names into data/peers-mixed.csv.

Opus, 7-Sep-2026. This is the last red check in the suite: check 1 has reported
`2026-09-04_public-pull-16-names.csv` as NOT INGESTED since 5 September, because the load was
blocked first on three open questions and then on nobody doing the work. Two of the three questions
closed on 5 September (the two Euronext rows are USD at a derived rate; no customer-float
adjustment, Daniil's figures stand) and the third closed on 6 September (CY+1 is the current year,
so the pull's CAGR goes into revenue_growth_cagr_cy1_cy3_pct, tested on 16 of 16 rows). Nothing is
open. This is the work.

NOT ONE FIGURE IN THE OUTPUT IS RETYPED. Every number in data/peers-mixed.csv is copied cell by cell
out of the raw transcription by the MAP below, which is a pure rename from the screen's column names
to the engine's. That is the whole point of doing this with a script instead of by hand: the raw
file was itself transcribed from a screenshot once, and a second hand-transcription would be a
second chance to fluff a digit with nothing to catch it.

THE TWO EXCLUSIONS ARE NAMED, COUNTED AND WRITTEN INTO THE OUTPUT, never silent. Both are
docs/public-pull-verdicts-4sep.md verdicts:

  NASDAQ:LPSN  LivePerson      EXCLUDED. Under a Nasdaq delisting notice, market cap $37m, net
                               income -$40m, revenue forecast to shrink 17.8% then 35.9%. A company
                               shrinking a third a year cannot price a founder.
  NYSE:GDOT    Green Dot       HELD OUT. Gross profit reads 0 against $2,491m of revenue, which is
                               missing rather than zero, so no gross-profit multiple can be built;
                               BVPS and P/BV are absent, so no book multiple can be built either.
                               And it is a bank holding company, so 0.3x on revenue is a market cap
                               against gross interest and fee income, which is not a price. It
                               belongs in data/peers-lending.csv once BVPS and P/BV arrive.

The difference between the two words matters and is kept: LivePerson is excluded on its business,
Green Dot is held pending two fields. Whoever pulls a lending screen next should pick Green Dot up.

ONE DERIVED COLUMN, AND IT SAYS SO. leverage_debt_share_pct is the equity-to-enterprise-value bridge
divided by enterprise value, both from the screen, expressed as a percentage. It exists because
verdicts issue 4 says Claritev and Skillsoft are leverage rather than price and asks for a flag, and
there was no flag in the repo. It is COMPUTED for every row rather than hand-set on two, so the
threshold that turns it into a rule is a single number Daniil can name later rather than a list
somebody has to maintain.

    python3 tools/load_public_pull_16_7sep.py             writes the file
    python3 tools/load_public_pull_16_7sep.py --dry-run   prints the counts, writes nothing

Idempotent: it reads the raw file and rewrites the output from scratch every time, so running it
twice gives the same file.
"""
import csv
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'data', 'raw', '2026-09-04_public-pull-16-names.csv')
OUT = os.path.join(ROOT, 'data', 'peers-mixed.csv')

# EXCLUSIONS, with the verdict that produced each. A ticker here is not loaded and the reason is
# printed on every run and written into the output header.
EXCLUDE = {
    'NASDAQ:LPSN': ('EXCLUDED',
                    'Nasdaq delisting notice; market cap $37m, net income -$40m, revenue forecast '
                    'to shrink 17.8% then 35.9%. Verdicts issue 1.'),
    'NYSE:GDOT': ('HELD OUT',
                  'gross profit reads 0 against $2,491m of revenue (missing, not zero) and there '
                  'is no BVPS or P/BV, so neither a gross-profit nor a book multiple can be built; '
                  'it is a bank holding company and belongs in data/peers-lending.csv. '
                  'Verdicts issue 2.'),
}

# THE SCREEN'S COLUMN NAME -> THE ENGINE'S COLUMN NAME. A pure rename. Anything not in here is not
# carried, and the two columns that ARE deliberately dropped are named under it so the omission is a
# decision rather than an oversight.
MAP = [
    ('ticker',                   'exchange_ticker'),
    ('company_name',             'company_name'),
    ('market_cap_musd',          'market_cap_musd'),
    ('price_per_share',          'price_per_share'),
    ('eq_to_av_bridge_musd',     'equity_to_av_bridge_musd'),
    ('av_musd',                  'enterprise_value_musd'),
    ('n_estimates',              'n_estimates'),
    ('revenue_ntm_musd',         'revenue_ntm_musd'),
    ('gross_profit_ntm_musd',    'gross_profit_musd'),
    ('net_income_ntm_musd',      'ni_ntm_musd'),
    ('bvps_ntm',                 'bvps_ntm'),
    ('av_ntm_revenue_x',         'ev_ntm_revenue_x'),
    ('av_ntm_gp_x',              'ev_ntm_gp_x'),
    ('pe_ntm_x',                 'p_e_x'),
    ('pbv_ntm_x',                'p_bv_x'),
    ('rev_growth_cy1_yoy_pct',   'revenue_growth_cy1_pct'),
    ('rev_growth_cy2_yoy_pct',   'revenue_growth_cy2_pct'),
    ('rev_growth_cy3_yoy_pct',   'revenue_growth_cy3_pct'),
    ('rev_cagr_cy1_cy3_pct',     'revenue_growth_cagr_cy1_cy3_pct'),
    ('ni_growth_cy2_reported_pct', 'ni_growth_pct'),
]
# DELIBERATELY NOT CARRIED, and why:
#   net_float_eur_m_NOT_APPLIED, av_adj_*_NOT_APPLIED   the float adjustment Daniil ruled out on
#       5-Sep. Kept in the raw file as the audit trail for the ruling; carrying it into the engine
#       would put a number nobody may use one column away from a number everybody reads.
#   unused_a, unused_b, float_source_url                empty or a source link, not measures.
#   country                                             THE SCREEN DOES NOT SUPPLY IT. Rule D11: a
#       column the source does not have does not exist here rather than being guessed at. The
#       listing venue is not the country of operation, and monday.com on Nasdaq is the case that
#       proves it.

HEADER = '''"# Fairway peer set: the MIXED listed names from the 5-September public pull."
# GENERATED by tools/load_public_pull_16_7sep.py from data/raw/2026-09-04_public-pull-16-names.csv.
# Never hand-edit: re-run the script. Tags for these names are in data/peers-mixed-tags.csv, which
# also carries the reasoning and the two places the archetype vocabulary does not reach.
#
# as_of=2026-09-05. The pull was run and transcribed on 5 September; the file NAME says 4 September
# and is deliberately unchanged, because the MANIFEST, check 1, the verdicts document and the status
# document all point at it by that name. The correction lives inside the record.
#
# 16 ROWS SUPPLIED, 14 LOADED, 2 NOT LOADED, both named:
#   NASDAQ:LPSN  LivePerson  EXCLUDED  Nasdaq delisting notice, shrinking a third a year.
#   NYSE:GDOT    Green Dot   HELD OUT  no gross profit, no BVPS or P/BV, and it is a bank holding
#                                      company. Belongs in data/peers-lending.csv once those arrive.
#
# CURRENCY IS USD ON EVERY ROW INCLUDING THE TWO EURONEXT LISTINGS. Derived, not assumed: Pluxee
# reports net cash excluding restricted cash of EUR 1,270m against a screen bridge of -1,365, which
# gives USD/EUR 1.0748. docs/public-pull-verdicts-4sep.md issue 3.
#
# NO CUSTOMER-FLOAT ADJUSTMENT. Ruled by Daniil 5-Sep-2026 21:50 UK: his figures stand. The
# enterprise values below are the screen's own.
#
# GROWTH: rev_cagr_cy1_cy3_pct goes into revenue_growth_cagr_cy1_cy3_pct, the column the loader
# already reads first and 72 ecommerce rows already use. Settled 6-Sep and tested: compounding the
# CY+2 and CY+3 yearly rates reproduces the printed CAGR on 16 of 16 rows.
#
# leverage_debt_share_pct IS THE ONE DERIVED COLUMN: equity_to_av_bridge_musd divided by
# enterprise_value_musd, as a percentage, both from the screen. Verdicts issue 4 asks for a flag on
# Claritev (87.5%) and Skillsoft (89.0%) because their multiples describe balance sheets rather than
# businesses. It is computed on every row so a threshold can be set once instead of a list being
# maintained. NOTHING FILTERS ON IT TODAY: it reaches the founder as a caveat and does not move a
# number. Evolent Health at 63.9% is the third name a threshold would catch.
'''


def main():
    dry = '--dry-run' in sys.argv
    lines = [l for l in io.open(RAW, encoding='utf-8')
             if l.strip() and not l.lstrip('"').startswith('#')]
    rows = list(csv.DictReader(lines))
    n_in = len(rows)
    kept, dropped = [], []
    for r in rows:
        tk = (r.get('ticker') or '').strip()
        if tk in EXCLUDE:
            dropped.append((tk, r.get('company_name', ''), EXCLUDE[tk][0], EXCLUDE[tk][1]))
            continue
        out = {}
        for src, dst in MAP:
            out[dst] = (r.get(src) or '').strip()
        # The one derived column. Blank rather than 0 when either input is missing, because a blank
        # says "not computed" and a 0 says "no debt".
        try:
            br = float(out['equity_to_av_bridge_musd'])
            ev = float(out['enterprise_value_musd'])
            out['leverage_debt_share_pct'] = ('%.1f' % (100.0 * br / ev)) if ev else ''
        except (TypeError, ValueError):
            out['leverage_debt_share_pct'] = ''
        out['as_of'] = '2026-09-05'
        kept.append(out)

    cols = ['row'] + [d for _s, d in MAP] + ['leverage_debt_share_pct', 'as_of']
    for i, k in enumerate(kept, 1):
        k['row'] = str(i)

    print('PUBLIC PULL OF 16 NAMES -> data/peers-mixed.csv')
    print('  rows in the raw file      %d' % n_in)
    print('  rows written              %d' % len(kept))
    print('  rows not written          %d' % len(dropped))
    for tk, nm, kind, why in dropped:
        print('     %-12s %-26s %-9s %s' % (tk, nm, kind, why))
    assert len(kept) + len(dropped) == n_in, 'a row fell out unaccounted for'
    print('  %d in, %d out, %d named. Nothing fell between.' % (n_in, len(kept), len(dropped)))

    if dry:
        print('\n--dry-run: nothing written.')
        return 0
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
    w.writeheader()
    for k in kept:
        w.writerow(k)
    io.open(OUT, 'w', encoding='utf-8').write(HEADER + buf.getvalue())
    print('\nwritten: data/peers-mixed.csv (%d rows, %d columns)' % (len(kept), len(cols)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
