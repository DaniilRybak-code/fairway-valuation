# -*- coding: utf-8 -*-
"""Does every FIGURE in a source file reach the engine, not just every row?

WHY THIS EXISTS. Three bugs were found on 3-Sep-2026, all by Daniil looking at an output and
saying that cannot be right, and not one of them by a check:

  * twelve neobanks lost their price-to-book and price-earnings, because the loader skipped any
    ticker it had already seen in another peers file
  * sixteen volume multiples reached nothing, because the two private files spell the column
    ev_gmv_x and ev_volume_x and only the first was read
  * a valuation over 121.5 MEGATONNES OF CO2 sat in a column called volume_musd and produced a
    tidy 11.52x

They share a shape, and it is the shape our checks were blind to. **Every existing check counts
ROWS. All three of these bugs lose a FIELD while the row arrives intact.**

  check_raw_coverage   is every supplied ROW accounted for              passes on a blank field
  check_engine_reach   does every ROW reach the engine                  passes on a blank field
  golden.py            did the output MOVE                              a field that was always
                       empty never moves, so a bug present when the
                       baseline was written is invisible forever
  honesty_check        is the output caveated                           a missing multiple gives
                                                                        fewer names, not a wrong
                                                                        caveat

Rule D8 already says a figure in the file but not in the engine is ABSENT, not pending. Nothing
enforced D8 below the row.

HOW IT WORKS, and it is deliberately dumb so it cannot go stale. For every numeric column in every
source file it takes the rows that HAVE a value, and asks whether that value appears anywhere at
all on the loaded row. No column-to-field map is maintained, so a new column cannot be forgotten
and a renamed field cannot silently stop being checked. A column at 0% is a column the engine has
never seen. Anything below 100% names the rows that fell out.
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import match_reference as M                      # noqa: E402

# Columns that are identifiers, dates or flags rather than measures. A value here reaching or not
# reaching the engine says nothing, so they are skipped rather than reported as noise.
SKIP = {'row', 'sheet_row', 'transaction_id', 'date_iso', 'in_medians', 'in_stats', 'in_gmv_medians',
        'target_was_listed', 'fx_date', 'book_value_date', 'as_of', 'tags_as_of'}
FILES = [
    ('data/peers-software.csv', 'exchange_ticker', 'listed'),
    ('data/peers-ecommerce.csv', 'exchange_ticker', 'listed'),
    ('data/peers-fintech.csv', 'exchange_ticker', 'listed'),
    ('data/peers-logistics-services.csv', 'exchange_ticker', 'listed'),
    ('data/peers-lending.csv', 'exchange_ticker', 'listed'),
    ('data/private-rounds.csv', 'transaction_id', 'private'),
    ('data/private-rounds-consumer.csv', 'transaction_id', 'private'),
]


def safe_norm(k):
    try:
        return M.norm(k)
    except Exception:
        return k


def num(v):
    try:
        return round(float(str(v).strip().replace(',', '')), 4)
    except (TypeError, ValueError):
        return None


def rows_of(path):
    # peers-software.csv opens with a QUOTED comment line, so the plain startswith('#') test that
    # every other tool uses lets it through and it becomes the header. Strip the quote first.
    lines = [l for l in io.open(path, encoding='utf-8')
             if l.strip() and not l.lstrip('"').startswith('#')]
    return list(csv.DictReader(lines))


def loaded_index(kind):
    """Every loaded row, keyed by BOTH its id and its normalised ticker, with the set of every
    numeric value it holds. Two keys because the listed loader stores rows under a normalised
    ticker and the file carries the raw one."""
    out = {}
    pool = M.listed if kind == 'listed' else {i: r for i, r in enumerate(M.private)}
    for _k, r in (pool.items() if isinstance(pool, dict) else enumerate(pool)):
        vals = set()
        for v in r.values():
            n = num(v)
            if n is not None:
                vals.add(n)
        for key in (r.get('transaction_id'), r.get('exchange_ticker'),
                    safe_norm(r.get('exchange_ticker') or '')):
            if key:
                out.setdefault(key, set()).update(vals)
    return out


# ---------------------------------------------------------------------------
# THE SECOND HALF, AND IT IS THE HALF THAT CATCHES THE HARDER BUG.
#
# The value test above catches a column lost because the whole ROW was dropped. It CANNOT catch a
# column the loader never reads, because both loaders build their row with {**raw, **tags}, so the
# raw string is sitting on the row whether anything interprets it or not. I found this by planting
# the ev_volume_x fault and watching the check pass, which is the only reason to plant a fault.
#
# So: does any line of the loader MENTION this column name? A numeric column that appears in a data
# file and nowhere in the loader source is a column the engine cannot possibly be using, however
# many rows carry it. That is exactly the shape of the ev_volume_x bug, and it is a static test, so
# no amount of raw passthrough can fool it.
# A column the loader does not read ON PURPOSE, with the reason written down. This dict is the
# only permitted way to silence the static test, and an entry without a reason is not an entry.
# Adding to it is a decision; leaving a column out of it is a bug waiting to be found.
REASONED_UNREAD = {
 ('peers-logistics-services.csv', 'nci_musd'):
   'a component of the enterprise value the same file already computes in enterprise_value_musd',
 ('peers-logistics-services.csv', 'invest_assoc_musd'):
   'same, a bridge component behind enterprise_value_musd',
 ('peers-logistics-services.csv', 'eqv_ev_bridge_musd'):
   'same, the bridge total behind enterprise_value_musd',
 ('peers-logistics-services.csv', 'revenue_fy0_musd'):
   'per-year revenue. The engine prices on revenue_ntm_musd and ranks on a CAGR; the yearly series '
   'is kept in the file for the volume forecast and is not an engine input',
 ('peers-logistics-services.csv', 'revenue_fy1_musd'): 'same as revenue_fy0_musd',
 ('peers-logistics-services.csv', 'revenue_fy2_musd'): 'same as revenue_fy0_musd',
 ('peers-logistics-services.csv', 'gross_margin_pct'):
   'gross margin is COMPUTED from gross_profit_musd over revenue_ntm_musd rather than read, so the '
   'engine cannot hold a margin that disagrees with the two numbers behind it',
 ('peers-lending.csv', 'market_cap_musd'):
   'an input to p_bv_x and p_e_x, which the same file already computes and the loader does read',
}


# Whole CLASSES of column the loader does not read, with the reason written once rather than once
# per file. These are the same three shapes in every peers pull.
REASONED_UNREAD_COLS = {
 'market_cap_musd': 'an input to the enterprise value and to p_bv_x / p_e_x, all of which the same file computes',
 'net_debt_musd': 'a bridge component behind enterprise_value_musd, which the file computes',
 'minority_interest_musd': 'a bridge component behind enterprise_value_musd',
 'associates_musd': 'a bridge component behind enterprise_value_musd',
 'equity_to_av_bridge_musd': 'the bridge total behind enterprise_value_musd',
 'nci_musd': 'a bridge component behind enterprise_value_musd',
 'invest_assoc_musd': 'a bridge component behind enterprise_value_musd',
 'eqv_ev_bridge_musd': 'the bridge total behind enterprise_value_musd',
 'gross_margin_pct': 'COMPUTED from gross_profit_musd over revenue, never read, so the engine cannot '
                     'hold a margin that disagrees with the two numbers behind it',
 'revenue_local_cy0': 'local-currency series behind the CAGR the file already computes',
 'revenue_local_cy1': 'same', 'revenue_local_cy2': 'same', 'revenue_local_cy3': 'same',
 'revenue_cy1_musd': 'per-year revenue series, kept for the volume forecast, not an engine input',
 'revenue_cy2_musd': 'same', 'revenue_fy0_musd': 'same', 'revenue_fy1_musd': 'same',
 'revenue_fy2_musd': 'same',
 'gmv_cy1_musd': 'per-year GMV series behind gmv_ntm_musd, which the loader does read',
 'gmv_cy2_musd': 'same',
 'revenue_growth_cy1_pct': 'a single forward year. Daniil, 31-Aug: only a multi-year rate may rank '
                           'a peer, so this is deliberately not an engine input',
 'revenue_growth_cy2_pct': 'same, a single forward year',
 # THESE TWO ARE A REAL FINDING, NOT A DISMISSAL. We hold net revenue retention for 83 listed
 # software companies and the percentage of revenue that is recurring for 80, and the engine reads
 # neither. Whether retention enters the quiz is an open decision from the 29-Aug review ("keep as
 # optional, or cut"). If it is kept, THIS is the peer field it has to join, and the data is
 # already here. Recorded so the check stays green and the fact stays visible.
 'nrr_pct': 'held and not read: retention is an open quiz decision (29-Aug review). 83 listed '
            'software rows carry it and it is the peer field a retention question would join',
 'nrr_pct_low': 'same, the low end of a stated NRR range',
 'nrr_pct_high': 'same, the high end of a stated NRR range',
 'recurring_revenue_pct': 'held and not read, same open decision. 80 listed software rows carry it',
}


def unread_columns():
    src = io.open(os.path.join('selector', 'match_reference.py'), encoding='utf-8').read()
    out = []
    for path, _idcol, _kind in FILES:
        if not os.path.exists(path):
            continue
        rows = rows_of(path)
        if not rows:
            continue
        for c in rows[0].keys():
            if not c or c in SKIP or c.startswith('#'):
                continue
            populated = sum(1 for r in rows if num(r.get(c)) not in (None, 0))
            if not populated:
                continue
            if ("'%s'" % c) in src or ('"%s"' % c) in src:
                continue
            if (os.path.basename(path), c) in REASONED_UNREAD or c in REASONED_UNREAD_COLS:
                continue
            out.append((os.path.basename(path), c, populated))
    return out


_COLS = {}


def main():
    bad, warn = [], []
    for path, idcol, kind in FILES:
        if not os.path.exists(path):
            print('MISSING FILE %s' % path)
            bad.append(path)
            continue
        idx = loaded_index(kind)
        rows = rows_of(path)
        by_key = {}
        # WHICH ROWS ARE SHADOWED. A ticker present in an earlier peers file is loaded from that
        # file, so this file's version of the same company is not the row in the engine. That is a
        # DIFFERENT finding from a column the engine never reads, and it is where the 3-Sep bug
        # lived, so it gets its own line rather than being averaged into a percentage.
        # A ROW KILLED ON PURPOSE IS NOT A ROW LOST. LISTED_NOT_PRICING is Daniil's own kill list,
        # each entry carrying the reason it was killed, and this check must not report those as
        # missing data or nobody will read its output twice. EML Payments and OFX Group are there.
        killed = {M.__dict__.get('_norm_t', lambda x: x)(k) for k in
                  getattr(M, 'LISTED_NOT_PRICING', {})}
        shadowed = set()
        if kind == 'listed':
            for lr in M.listed:
                by_key[safe_norm(lr.get('exchange_ticker') or '')] = lr
            for r in rows:
                key = safe_norm((r.get(idcol) or '').strip())
                if (r.get(idcol) or '').strip().upper().replace(' ', '') in killed:
                    shadowed.add(key)          # deliberately excluded, reason on the kill list
                    continue
                got = by_key.get(key)
                if got is not None and os.path.basename(got.get('_src_file') or '') != os.path.basename(path):
                    shadowed.add(key)
        cols = [c for c in (rows[0].keys() if rows else []) if c not in SKIP]
        shadow_cols = []

        def cols_of(fpath):
            if fpath not in _COLS:
                r = rows_of(fpath)
                _COLS[fpath] = set(r[0].keys()) if r else set()
            return _COLS[fpath]

        def winners_for(keys):
            out = set()
            for k in keys:
                w = (by_key.get(k) or {}).get('_src_file') if kind == 'listed' else None
                if w:
                    out.add(w if os.path.exists(w) else os.path.join('data', os.path.basename(w)))
            return out

        print('=== %s (%d rows) ===' % (path, len(rows)))
        for c in cols:
            # A column already declared unread-with-a-reason cannot fail the VALUE test either.
            # The two halves must agree about what the engine is expected to carry, or the check
            # contradicts itself and gets ignored, which is how a check dies.
            if c in REASONED_UNREAD_COLS or (os.path.basename(path), c) in REASONED_UNREAD:
                continue
            have, reach, missing, missing_keys = 0, 0, [], set()
            for r in rows:
                v = num(r.get(c))
                if v is None or v == 0:
                    continue        # a zero is not evidence either way, it collides with everything
                have += 1
                key = (r.get(idcol) or '').strip()
                vals = idx.get(key) or idx.get(safe_norm(key)) or set()
                if v in vals:
                    reach += 1
                else:
                    missing_keys.add(safe_norm(key))
                    if len(missing) < 6:
                        missing.append('%s=%s' % (r.get('company_name', key)[:22], r.get(c)))
            if not have:
                continue
            pct = 100.0 * reach / have
            # SHADOWING ONLY EXPLAINS A MISSING VALUE IF THE WINNING FILE CARRIES THAT COLUMN AT
            # ALL. Without this the rule would suppress the exact bug the check was built for:
            # peers-fintech.csv has no p_bv_x column, so when a neobank loads from there the book
            # multiple is not "the other file's version", it is GONE. A column the winner cannot
            # carry is a real loss on every shadowed row and is reported as one.
            winner_has_col = all(c in cols_of(w) for w in winners_for(missing_keys))
            if reach and missing_keys and missing_keys <= shadowed and winner_has_col:
                shadow_cols.append(c)
                continue
            if pct >= 99.5:
                continue
            line = '   %-26s %3d values in file, %3d reach the engine (%.0f%%)' % (c, have, reach, pct)
            print(line + ('   NONE REACH' if reach == 0 else ''))
            print('        e.g. %s' % ', '.join(missing))
            (bad if reach == 0 else warn).append('%s : %s' % (os.path.basename(path), c))
        if shadow_cols:
            print('   %d columns miss only on tickers that are SHADOWED by an earlier peers file or'
                  % len(shadow_cols))
            print('   deliberately on the LISTED_NOT_PRICING kill list,')
            print('   so the engine holds the other file\'s version of those companies: %s'
                  % ', '.join(sorted(shadowed)[:8]))
            print('   columns: %s' % ', '.join(shadow_cols[:8]))
    print()
    if bad:
        print('FAIL: %d columns exist in a file and reach the engine ZERO times.' % len(bad))
        for b in bad:
            print('   %s' % b)
    if warn:
        print('%d columns reach the engine for some rows and not others. Read them, then either fix'
              % len(warn))
        print('the loader or write down why those rows are different:')
        for w in warn:
            print('   %s' % w)
    unread = unread_columns()
    if unread:
        print()
        print('COLUMNS THE LOADER NEVER MENTIONS, though the file populates them:')
        for f, c, n in unread:
            print('   %-30s %-28s %d rows carry a value' % (f, c, n))
        print('Each is either a column the engine should be reading and is not, or a column that')
        print('belongs in SKIP with a line saying why. It cannot be neither.')
    if not bad and not warn and not unread:
        print('PASS: every numeric value in every source file reaches the engine, and every')
        print('populated numeric column is at least read by the loader.')
    return 1 if (bad or unread) else 0


if __name__ == '__main__':
    sys.exit(main())


