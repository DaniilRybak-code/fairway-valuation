# -*- coding: utf-8 -*-
"""Load the swept counts onto the rounds and compute the per-unit figure.

Daniil, 3-Sep-2026: "check thoroughly the existing database of 290 private rounds, checking for each
if the number of users / subscribers / members was quoted at the announcement and calculating the
respective EV / subscribers multiple for each row where available."

The counts come from data/raw/2026-09-03_user-counts-sweep-wave1.csv and -wave2.csv, each figure
read off the round's own announcement by an agent told to quote it verbatim.

WHAT IS LOADED AND WHAT IS NOT. Only a count whose KIND is unambiguous and whose subject is the
company itself. Downloads, sessions, visits, locations, listings, terminals, trucks and units sold
are recorded in the raw file and NOT loaded: they are not counts of customers and a price per
download would be a number with no meaning behind it.

THE KIND IS THE WHOLE POINT. A range may only ever be built inside one kind, so a merchant count
never meets a subscriber count. is_paying is carried as a note on the label, per Daniil's
correction of the same day: the count does not have to be of payers, but if it is, say so.
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
WRITE = '--write' in sys.argv

LOADABLE = {'PAYING_SUBSCRIBERS', 'MEMBERS', 'CUSTOMERS', 'BUSINESS_CUSTOMERS', 'MERCHANTS',
            'BORROWERS', 'ACTIVE_USERS', 'REGISTERED_USERS'}
SRC = ['data/raw/2026-09-03_user-counts-sweep-wave1.csv',
       'data/raw/2026-09-03_user-counts-sweep-wave2.csv']


def read(path):
    return list(csv.DictReader([l for l in io.open(path, encoding='utf-8')
                                if not l.startswith('#')]))


def main():
    counts = {}
    skipped = []
    for p in SRC:
        for d in read(p):
            kind = (d['metric_kind'] or '').strip().upper()
            key = (d['company'].strip(), d['round'].strip())
            if kind not in LOADABLE:
                skipped.append((key, kind))
                continue
            try:
                n = float(d['count'])
            except ValueError:
                continue
            if n <= 0:
                continue
            # PREFER THE MOST MONETISED KIND when a page gives several. A paying count beats a
            # member count beats a customer count beats an active count beats a registered one,
            # because the further down that list you go the looser the relationship to revenue.
            rank = {'PAYING_SUBSCRIBERS': 0, 'BORROWERS': 1, 'MERCHANTS': 2, 'BUSINESS_CUSTOMERS': 3,
                    'MEMBERS': 4, 'CUSTOMERS': 5, 'ACTIVE_USERS': 6, 'REGISTERED_USERS': 7}[kind]
            cur = counts.get(key)
            if cur is None or rank < cur[0]:
                counts[key] = (rank, kind, n, d['is_paying'], d['as_worded_on_the_page'])

    raw = io.open('data/private-rounds.csv', encoding='utf-8').read()
    head = ''.join(l for l in raw.splitlines(True) if l.startswith('#'))
    body = [l for l in raw.splitlines(True) if not l.startswith('#')]
    rd = csv.DictReader(body)
    cols, rows = rd.fieldnames, list(rd)
    before = len(rows)
    hit, clash = 0, []
    for r in rows:
        key = (r['company_name'].strip(), (r.get('date') or '').strip())
        got = counts.pop(key, None)
        if not got:
            continue
        _rank, kind, n, paying, quote = got
        if (r.get('volume_metric') or '').strip():
            # ALREADY CARRIES A VOLUME. Never overwritten: an originations or GMV figure is a
            # different and usually better denominator, and the count stays in the raw file.
            clash.append((key, r['volume_metric'], kind))
            continue
        try:
            post = float(r['post_money_musd'])
        except (ValueError, TypeError):
            continue
        per = post * 1e6 / n
        r['volume_metric'] = kind
        r['volume_musd'] = '%.6f' % (n / 1e6)      # the count, in millions, as the column expects
        r['volume_period'] = 'At the round'
        r['volume_basis'] = kind
        r['ev_volume_x'] = '%.2f' % per
        if not (r.get('valuation_basis') or '').strip():
            r['valuation_basis'] = kind
        r['in_medians'] = '1'
        r['notes'] = (r['notes'].rstrip() +
                      ' || COUNT LOADED 3-Sep-2026 from the round announcement itself: "%s". '
                      '%s of %s at the round against a $%.0fm post-money is $%s of enterprise '
                      'value per unit. is_paying=%s. A range may only be built against the same '
                      'KIND: this figure never meets a count of a different kind.'
                      % (quote.strip('"'), '{:,.0f}'.format(n), kind, post,
                         '{:,.0f}'.format(per), paying))
        hit += 1
        print('   %-24s %-8s %-20s %14s  ->  $%s per unit  (paying=%s)'
              % (r['company_name'][:24], r['date'], kind, '{:,.0f}'.format(n),
                 '{:,.0f}'.format(per), paying))
    assert len(rows) == before
    if WRITE:
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, '') for c in cols})
        io.open('data/private-rounds.csv', 'w', encoding='utf-8').write(head + buf.getvalue())
    print()
    print('rows in %d, rows out %d, counts loaded %d' % (before, len(rows), hit))
    print('kinds not loadable as a denominator (recorded in raw only): %d' % len(skipped))
    print('rounds that already carry a money volume, count NOT overwritten: %d' % len(clash))
    for k, have, kind in clash:
        print('   %-24s keeps %-22s instead of %s' % (k[0][:24], have, kind))
    print('counts with no matching round in the file: %d' % len(counts))
    for k in list(counts)[:12]:
        print('   %s %s' % k)
    if not WRITE:
        print('\nDRY RUN. Re-run with --write.')
    return 0


sys.exit(main())
