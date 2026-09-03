# -*- coding: utf-8 -*-
"""Apply a listed refresh to the peer files. ONE dataset, updated for market movements.

Daniil, 3-Sep-2026: "There was one pull I provided on 1st of Sep, it was supposed to supersede /
update numbers we had before. I will be providing these update on public comps on weekly /
bi-weekly basis, we cannot get confused and start referring to different data sets. All of that is
one set, simply updated for market movements."

That is the correct model and the repo was not built for it. `tools/ingest_full_refresh.py` CHECKED
the refresh and never had a write path at all, so the 1-Sep pull sat in data/raw for two days while
the engine ran on 30-Aug numbers, and I spent an evening describing a single dataset as two pulls
that disagreed. They did not disagree. One was simply stale.

WHAT THIS REPLACES: market data only. Valuation, revenue, gross profit, the multiples, book value
per share, net income, growth. It does NOT touch a tag, an archetype, a family, the volume overlay's
disclosure fields or anything a human decided; those live in the -tags files and are joined on
ticker.

MATCHING, AND WHY IT IS NOT JUST THE TICKER. Capital IQ writes the same company as NASDAQ:ETSY on
one pull and NYSE:ETSY on the next, and CCC Intelligent Solutions as CCC and CCCS. Twelve of the
1-Sep rows looked new and twenty-three existing rows looked dropped, and almost all of them were the
same companies wearing a different exchange prefix. So the match runs in three passes, most exact
first, and a symbol match is refused when the two names are not recognisably the same company,
because NYSE:ZIP is ZipRecruiter and ASX:ZIP is Zip Co.

EVERY ROW IS ACCOUNTED FOR by name, in both directions, per Daniil's standing rule.
"""
import csv
import difflib
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
WRITE = '--write' in sys.argv
SRC = [a for a in sys.argv[1:] if not a.startswith('--')] or \
      ['data/raw/2026-09-01_listed-full-refresh.csv']

FIELDS = ['ticker', 'company_name', 'year_end', 'calendarization', 'currency', 'fx_rate_usd_lcy',
          'balance_sheet_driven', 'market_cap_musd', 'price_per_share', 'equity_to_av_bridge_musd',
          'av_musd', 'n_estimates', 'gmv_cy0', 'gmv_cy1', 'gmv_cy2', 'gmv_ntm',
          'revenue_ntm_musd', 'gross_profit_musd', 'net_income_ntm_musd', 'bvps',
          'av_gmv_pct', 'av_ntm_revenue_x', 'av_ntm_gp_x', 'pe_x', 'pbv_x',
          'rev_cagr_a', 'rev_cagr_b', 'rev_cagr_c', 'rev_cagr_d', 'gross_margin_pct']

PEERS = ['data/peers-software.csv', 'data/peers-ecommerce.csv', 'data/peers-fintech.csv',
         'data/peers-logistics-services.csv', 'data/peers-lending.csv']

# refresh column -> the column name each peers file uses for the same measure. The five pulls do
# not agree on their own column names, which is how 123 logistics rows lost their growth, so the
# mapping is explicit per target column and anything unmapped is simply not written.
MAP = {
    'market_cap_musd':        ['market_cap_musd'],
    'equity_to_av_bridge_musd': ['equity_to_av_bridge_musd', 'eqv_ev_bridge_musd'],
    'av_musd':                ['enterprise_value_musd'],
    'revenue_ntm_musd':       ['revenue_ntm_musd'],
    'gross_profit_musd':      ['gross_profit_musd'],
    'av_ntm_revenue_x':       ['ev_ntm_revenue_x'],
    'av_ntm_gp_x':            ['ev_ntm_gp_x'],
    'pe_x':                   ['p_e_x'],
    'pbv_x':                  ['p_bv_x'],
    'bvps':                   ['bvps_ntm'],
    'net_income_ntm_musd':    ['ni_ntm_musd'],
    'price_per_share':        ['price_per_share'],
}

# The last five columns of the refresh are unnamed. The check tool never named them either: its
# FIELDS list stops at pbv_x. On MercadoLibre they read 44.3, 27.9, 24.7, 26.3, 43.3 and on nCino
# 8.7, 8.5, 8.7, 8.6, 29.5, so the first four are plainly growth rates and a CAGR, and the fifth is
# something else again. NOTHING IS WRITTEN FROM THEM until Daniil says what they are. A column
# guessed at is worse than a column left alone: the growth ladder already carries three different
# definitions and a fourth one guessed would be undetectable.
UNNAMED = ['rev_cagr_a', 'rev_cagr_b', 'rev_cagr_c', 'rev_cagr_d', 'gross_margin_pct']


def num(v):
    s = str(v).strip().replace(',', '').replace('%', '').replace('x', '')
    if s.lower() in ('', 'na', 'nm', 'n.a.', 'n.m.', 'hidden', 'broken', '-'):
        return None
    if s.startswith('(') and s.endswith(')'):
        s = '-' + s[1:-1]
    try:
        float(s)
    except ValueError:
        return None
    return s


def sym(t):
    t = (t or '').strip()
    return (t.split(':', 1)[1] if ':' in t else t).strip().upper()


# A COMPANY THAT RENAMES ITSELF IS STILL THE SAME COMPANY. LendingClub became Happen and kept the
# ticker NYSE:LC, so the refresh calls it Happen, Inc. under NASDAQGS:HAPN while two of our peers
# files still say LendingClub Corporation. Neither the ticker, the symbol nor the name matches, and
# without this the row silently goes stale under its old name while a second row for the same
# company updates under the new one.
RENAMES = {
    'lendingclub corporation': 'happen, inc.',
}


def same_company(a, b):
    """Are these two names the same company? Used only to allow a symbol match."""
    def clean(n):
        n = (n or '').lower()
        for junk in (' inc.', ' inc', ' corporation', ' corp.', ' corp', ' ltd.', ' ltd', ' plc',
                     ' limited', ' n.v.', ' nv', ' s.a.', ' sa', ' ab', ' oyj', ' a/s', ' group',
                     ' holdings', ' holding', ' co.', ' company', ' (publ)', ',', '.'):
            n = n.replace(junk, ' ')
        return ' '.join(n.split())
    a = RENAMES.get((a or '').strip().lower(), a)
    b = RENAMES.get((b or '').strip().lower(), b)
    x, y = clean(a), clean(b)
    if not x or not y:
        return False
    return x == y or x.startswith(y) or y.startswith(x) or \
        difflib.SequenceMatcher(None, x, y).ratio() >= 0.85


def read_refresh(path):
    lines = [l for l in io.open(path, encoding='utf-8') if not l.lstrip('"').startswith('#')]
    out = []
    for cells in csv.reader(lines):
        if not cells:
            continue
        ti = next((i for i, c in enumerate(cells) if ':' in str(c) and len(str(c)) < 24), None)
        if ti is None:
            continue
        vals = cells[ti:]
        out.append(dict(zip(FIELDS, vals + [''] * (len(FIELDS) - len(vals)))))
    return out


def read_peers(path):
    raw = io.open(path, encoding='utf-8').read()
    head = ''.join(l for l in raw.splitlines(True) if l.lstrip('"').startswith('#'))
    body = [l for l in raw.splitlines(True) if l.strip() and not l.lstrip('"').startswith('#')]
    rd = csv.DictReader(body)
    return head, rd.fieldnames, list(rd)


def main():
    ref = read_refresh(SRC[0])
    print('%s: %d rows' % (os.path.basename(SRC[0]), len(ref)))
    by_ticker = {}
    by_symbol = {}
    for r in ref:
        by_ticker.setdefault((r['ticker'] or '').strip().upper(), r)
        by_symbol.setdefault(sym(r['ticker']), []).append(r)

    used, updated, unmatched_peer, changed_cells = set(), [], [], 0
    for path in PEERS:
        head, cols, rows = read_peers(path)
        # EVERY FILE NEEDS AN as_of, or a row cannot be told apart from a refreshed one. The
        # logistics and lending pulls had no such column, so 188 rows carried no date at all and
        # nothing could tell that they had been left behind by a refresh. Added rather than assumed.
        if 'as_of' not in cols:
            cols = list(cols) + ['as_of']
        targets = {c for c in cols}
        n_file = 0
        for d in rows:
            t = (d.get('exchange_ticker') or '').strip()
            r = by_ticker.get(t.upper())
            how = 'ticker'
            if r is None:
                # PASS 2, the symbol with a name guard. NASDAQ:ETSY and NYSE:ETSY are the same
                # company; NYSE:ZIP is ZipRecruiter and ASX:ZIP is Zip Co, so the names must agree.
                # The refresh's own repeated tickers are collapsed first, otherwise a company that
                # appears twice in the refresh looks like a collision with itself: that is what was
                # dropping Freightos, GigaCloud, Kanzhun, LegalZoom, Copart and Xometry.
                cand = [c for c in by_symbol.get(sym(t), [])
                        if same_company(c['company_name'], d.get('company_name'))]
                seen_t = set()
                cand = [c for c in cand if not (c['ticker'] in seen_t or seen_t.add(c['ticker']))]
                if len({sym(c['ticker']) for c in cand}) == 1 and cand:
                    r, how = cand[0], 'symbol+name'
            if r is None:
                # PASS 3, the NAME alone, when it is unique on both sides. Capital IQ changed CCC
                # Intelligent Solutions from CCCS to CCC between pulls. A company that renames its
                # ticker is still the same company and must not go stale for it.
                cand = [c for c in ref if same_company(c['company_name'], d.get('company_name'))]
                peers_same = [x for x in rows if same_company(x.get('company_name'), d.get('company_name'))]
                if len(cand) == 1 and len(peers_same) == 1:
                    r, how = cand[0], 'name'
            if r is None:
                unmatched_peer.append((os.path.basename(path), d.get('company_name'), t))
                continue
            used.add((r['ticker'] or '').strip().upper())
            for src, dsts in MAP.items():
                v = num(r.get(src))
                if v is None:
                    continue
                for dst in dsts:
                    if dst in targets and (d.get(dst) or '').strip() != v:
                        d[dst] = v
                        changed_cells += 1
            # GROSS MARGIN IS RECOMPUTED, NOT COPIED. The refresh's last five columns are unnamed
            # so nothing is written from them, but the peers files carry a stored gross_margin_pct
            # that would otherwise stay at its 30-Aug value beside a refreshed gross profit and
            # revenue. MercadoLibre was the case: 42.1 in one file, 44.3 in the other, and 42.7 on
            # the refreshed figures. Derived from the two numbers just written, never guessed.
            gp, rv = num(r.get('gross_profit_musd')), num(r.get('revenue_ntm_musd'))
            if 'gross_margin_pct' in targets and gp is not None and rv not in (None, '0'):
                try:
                    d['gross_margin_pct'] = '%.1f' % (100.0 * float(gp) / float(rv))
                    changed_cells += 1
                except (ValueError, ZeroDivisionError):
                    pass
            if 'as_of' in targets:
                d['as_of'] = REFRESH_DATE
            n_file += 1
            updated.append((os.path.basename(path), d.get('company_name'), how))
        if WRITE:
            buf = io.StringIO()
            w = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
            w.writeheader()
            for d in rows:
                w.writerow({c: d.get(c, '') for c in cols})
            io.open(path, 'w', encoding='utf-8').write(head + buf.getvalue())
        print('   %-38s %d of %d rows refreshed' % (os.path.basename(path), n_file, len(rows)))

    unmatched_ref = [r for r in ref if (r['ticker'] or '').strip().upper() not in used]
    print()
    print('ROW ACCOUNTING, both directions')
    print('   refresh rows                 %d' % len(ref))
    print('   matched into a peers file    %d' % len(used))
    print('   peers rows refreshed         %d' % len(updated))
    print('   cells changed                %d' % changed_cells)
    print()
    print('   IN THE REFRESH, NOT MATCHED TO ANY PEERS ROW: %d' % len(unmatched_ref))
    for r in unmatched_ref:
        print('      %-22s %s' % (r['ticker'], r['company_name'][:44]))
    print()
    print('   IN A PEERS FILE, NOT IN THE REFRESH (now stale): %d' % len(unmatched_peer))
    for f, n, t in unmatched_peer:
        print('      %-30s %-22s %s' % (str(n)[:30], t, f))
    print()
    print('   COLUMNS IN THE REFRESH THAT NOTHING IS WRITTEN FROM: %s' % ', '.join(UNNAMED))
    print('   The last five columns are unnamed in the source and are NOT guessed at.')
    if not WRITE:
        print('\nDRY RUN. Nothing written. Re-run with --write.')
    return 0


REFRESH_DATE = '2026-09-01'

if __name__ == '__main__':
    sys.exit(main())
