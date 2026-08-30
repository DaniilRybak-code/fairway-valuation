# -*- coding: utf-8 -*-
"""Merge a fresh listed market-data pull into a peers file, without losing the analysis on it.

    python3 tools/refresh_listed_pull.py data/raw/2026-08-30_capiq-listed-software.csv data/peers-software.csv

WHY A MERGE AND NOT AN OVERWRITE. Daniil, 30-Aug-2026: "public comps will be updated regularly due
to share price movements." A market-data file therefore has two kinds of column in it and they must
be treated differently:

  MARKET COLUMNS   market cap, enterprise value, revenue, gross profit, the multiples. These change
                   every time the market moves and are REPLACED wholesale on every refresh.
  ANALYSIS COLUMNS net revenue retention and its period, scope, source and status; paying users.
                   These were researched by hand, they do not move with the share price, and
                   overwriting the file would silently destroy them. They are PRESERVED.

The join key is `exchange_ticker`. Company name is never a key: it changes spelling between pulls
and produces silent duplicates.

WHAT THE SCRIPT WILL NOT DO SILENTLY. It reports, and does not guess, on three things:
  - names in the old file that the new pull does not contain, which keep their old figures and are
    stamped with their old as_of so a stale row is visible rather than assumed fresh;
  - names in the new pull that are not in the old file, which are added and will need a tags row
    before the engine can match them;
  - names with no tags row at all, which the engine cannot use however good the market data is.
"""
import csv, io, os, re, sys, datetime

MARKET = ['market_cap_musd', 'enterprise_value_musd', 'revenue_ntm_musd', 'gross_profit_musd',
          'ev_ntm_revenue_x', 'ev_ntm_gp_x', 'revenue_local_cy0', 'revenue_local_cy2',
          'revenue_growth_cagr_cy0_cy2_pct', 'recurring_revenue_pct', 'gross_margin_pct', 'as_of']


def read(path):
    lines = open(path, encoding='utf-8').read().splitlines()
    head = [l for l in lines if l.lstrip('"').startswith('#')]
    body = '\n'.join(l for l in lines if not l.lstrip('"').startswith('#'))
    rd = csv.DictReader(io.StringIO(body))
    return head, rd.fieldnames, list(rd)


def as_of_from(path, head):
    m = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(path))
    if m:
        return m.group(1)
    for h in head:
        m = re.search(r'as_of=(\d{4}-\d{2}-\d{2})', h)
        if m:
            return m.group(1)
    return datetime.date.today().isoformat()


def num(s):
    try:
        return float(str(s).replace(',', ''))
    except (TypeError, ValueError):
        return None


def main(raw_path, target_path):
    rhead, rcols, rrows = read(raw_path)
    thead, tcols, trows = read(target_path)
    stamp = as_of_from(raw_path, rhead)
    old_stamp = as_of_from(target_path, thead)

    cols = list(tcols)
    for c in MARKET:
        if c not in cols:
            cols.append(c)

    by_ticker = {r['exchange_ticker']: r for r in trows}
    updated, added = [], []

    for n in rrows:
        t = n['exchange_ticker']
        gp, rev = num(n.get('gross_profit_musd')), num(n.get('revenue_ntm_musd'))
        # DERIVED, and the only derived figure in the file: gross margin is gross profit over
        # revenue, both of which the screen supplied. Blank when either side is missing.
        gm = round(100.0 * gp / rev, 1) if (gp is not None and rev) else ''
        patch = {c: n.get(c, '') for c in MARKET if c in n}
        patch['gross_margin_pct'] = gm
        patch['as_of'] = stamp
        if t in by_ticker:
            by_ticker[t].update(patch)
            updated.append(t)
        else:
            row = {c: '' for c in cols}
            row['company_name'] = n.get('company_name', '')
            row['exchange_ticker'] = t
            row['country'] = n.get('country', '')
            row.update(patch)
            by_ticker[t] = row
            trows.append(row)
            added.append(t)

    fresh = set(updated) | set(added)
    stale = [r['exchange_ticker'] for r in trows if r['exchange_ticker'] not in fresh]
    for r in trows:
        if r['exchange_ticker'] in stale and not r.get('as_of'):
            r['as_of'] = old_stamp

    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=cols, lineterminator='\n', extrasaction='ignore')
    w.writeheader()
    for r in trows:
        w.writerow({c: r.get(c, '') for c in cols})

    head = [h for h in thead if 'as_of=' not in h]
    head.insert(1, '# as_of=%s  refreshed from %s. Market columns replaced, analysis columns kept.'
                % (stamp, os.path.basename(raw_path)))
    open(target_path, 'w', encoding='utf-8').write('\n'.join(head) + '\n' + out.getvalue())

    print('refreshed %s at as_of=%s' % (os.path.basename(target_path), stamp))
    print('  updated in place %d' % len(updated))
    print('  added new        %d  %s' % (len(added), ', '.join(added) or ''))
    print('  NOT IN NEW PULL  %d  %s' % (len(stale), ', '.join(stale) or ''))
    print('  rows now         %d' % len(trows))

    tags_path = target_path.replace('.csv', '-tags.csv')
    if os.path.exists(tags_path):
        _, _, tag_rows = read(tags_path)
        have = {r['exchange_ticker'] for r in tag_rows}
        missing = [r['exchange_ticker'] for r in trows if r['exchange_ticker'] not in have]
        print('\n  WITHOUT A TAGS ROW, so the engine cannot match them: %d' % len(missing))
        for t in missing:
            print('    %-24s %s' % (t, by_ticker[t].get('company_name', '')))
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
