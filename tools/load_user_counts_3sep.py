# -*- coding: utf-8 -*-
"""Load the swept counts onto the rounds and compute the per-unit figure.

Daniil, 3-Sep-2026: "check thoroughly the existing database of 290 private rounds, checking for each
if the number of users / subscribers / members was quoted at the announcement and calculating the
respective EV / subscribers multiple for each row where available."

The counts come from data/raw/2026-09-03_user-counts-sweep-wave1.csv, -wave2.csv and -wave3.csv,
each figure read off the round's own announcement by an agent told to quote it verbatim.

BOTH PRIVATE ROUND FILES, from wave 3 on. Until then this tool wrote only to private-rounds.csv, so
the 52 rounds in private-rounds-consumer.csv could never receive a count however well it was
sourced, and waves 1 and 2 lost 19 of them without saying so. Daniil, 3-Sep: "Why are there two
separate CSVs for private rounds? We should have 1 CSV with all data combined." The merge is its own
job. Until it happens this tool treats the two files as one universe, and it adds the five volume
columns to the consumer file if they are missing, which moves the two schemas toward each other
rather than further apart. selector/match_reference.py already reads volume_musd, ev_volume_x and
volume_metric from BOTH files, so nothing on the engine side had to change.

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
# A FLOW IS NOT A STOCK, AND A SINCE-INCEPTION TOTAL IS NOT A DENOMINATOR.
#
# Added 3-Sep-2026 after Daniil asked whether Decagon's count could price where its revenue could
# not. It cannot, and checking why found three more of the same shape, two of them loaded from
# waves 1 and 2 this afternoon. The raw files are append-only, so the exclusion lives here with a
# reason a stranger could audit, per D12.
#
# Two different objections, both fatal to a denominator:
#   a PERIOD ADDITION  "100 new customers joined", "introducing 1 million new customers". That is
#                      customers ADDED, and EV over customers added is not a price per customer.
#   SINCE INCEPTION    "over 325,000 businesses since its founding", "signed up since its public
#                      launch in June 2020". Daniil, 2-Sep: "multiples cannot be calculated over
#                      all time origination volumes." A price divided by everything a company has
#                      ever done falls as the company ages and says nothing about what it is worth.
#                      match_reference already bars this for money volumes by testing vol_period
#                      for INCEPTION, but this loader writes 'At the round' for every count, so the
#                      guard could never fire on the count lane. These are barred here instead.
#
# Keyed on company, round, kind and count so it can only ever match the figure it names.
EXCLUSIONS = {
    ('Decagon', 'Jan-26', 'BUSINESS_CUSTOMERS', 100.0):
        'PERIOD ADDITION. "more than 100 new global enterprise customers ... joined the Decagon '
        'family" is customers added, not the installed base.',
    ('Glossier', 'Mar-19', 'CUSTOMERS', 1000000.0):
        'PERIOD ADDITION. "introducing more than 1 million new customers" is customers added over '
        'the period, not the base at the round.',
    ('Fundbox', 'Nov-21', 'BUSINESS_CUSTOMERS', 325000.0):
        'SINCE INCEPTION. "connected with over 325,000 businesses since its founding" is a '
        'cumulative total that grows with age.',
    ('Pipe', 'May-21', 'BUSINESS_CUSTOMERS', 4000.0):
        'SINCE INCEPTION. "have signed up on the Pipe trading platform since its public launch in '
        'June 2020" is cumulative signups, not an active base.',
}
SRC = ['data/raw/2026-09-03_user-counts-sweep-wave1.csv',
       'data/raw/2026-09-03_user-counts-sweep-wave2.csv',
       'data/raw/2026-09-03_user-counts-sweep-wave3.csv']
# The two private round files, treated as one universe until they are merged.
ROUND_FILES = ['data/private-rounds.csv', 'data/private-rounds-consumer.csv']
# The volume lane, as private-rounds.csv spells it. A file missing these gets them, empty, so that
# a count has somewhere to land. D11: a column with no field has nowhere to go and nothing counts
# its absence.
VOL_COLS = ['volume_metric', 'volume_musd', 'volume_period', 'volume_basis', 'ev_volume_x']
# RESIDUE OF THE in_medians BUG, corrected by name against commit 02836c8.
#
# The promotion described below ran once before it was found, in commit cc85d3a of 17:52 on 3-Sep,
# over the 56 rows waves 1 and 2 loaded. Restoring the data files to e9ab546 did not undo it,
# because e9ab546 is AFTER cc85d3a and carries other real work that must not be lost. The reset
# pass takes this tool's volume columns back out but cannot know what in_medians was before the
# tool first ran.
#
# So these four are named against 02836c8, the last commit before any count was loaded, where all
# four read in_medians=0. Each carries a revenue multiple that somebody excluded on purpose, and
# under the rule below each must stay excluded and be reported as BLOCKED instead. Verified by
# reading 02836c8 through the GitHub MCP rather than by running git on Daniil's machine.
IN_MEDIANS_WAS_ZERO_AT_02836C8 = {
    ('Anthropic', 'Sep-25'), ('OpenAI', 'Mar-25'),
    ('Perplexity', 'Jan-24'), ('Shiprocket', 'Aug-22'),
}
# The stamp this tool leaves in notes, and the handle it uses to take its own work back out.
MARKER = 'COUNT LOADED 3-Sep-2026'


def read(path):
    return list(csv.DictReader([l for l in io.open(path, encoding='utf-8')
                                if not l.startswith('#')]))


def main():
    counts = {}
    skipped = []
    excluded = []
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
            if (key[0], key[1], kind, n) in EXCLUSIONS:
                excluded.append((key, kind, n, EXCLUSIONS[(key[0], key[1], kind, n)]))
                continue
            # PREFER THE MOST MONETISED KIND when a page gives several. A paying count beats a
            # member count beats a customer count beats an active count beats a registered one,
            # because the further down that list you go the looser the relationship to revenue.
            rank = {'PAYING_SUBSCRIBERS': 0, 'BORROWERS': 1, 'MERCHANTS': 2, 'BUSINESS_CUSTOMERS': 3,
                    'MEMBERS': 4, 'CUSTOMERS': 5, 'ACTIVE_USERS': 6, 'REGISTERED_USERS': 7}[kind]
            cur = counts.get(key)
            if cur is None or rank < cur[0]:
                counts[key] = (rank, kind, n, d['is_paying'], d['as_worded_on_the_page'])

    total_hit, total_before, all_clash, added_cols, blocked, reset = 0, 0, [], [], [], 0
    for path in ROUND_FILES:
        raw = io.open(path, encoding='utf-8').read()
        head = ''.join(l for l in raw.splitlines(True) if l.startswith('#'))
        body = [l for l in raw.splitlines(True) if not l.startswith('#')]
        rd = csv.DictReader(body)
        cols, rows = list(rd.fieldnames), list(rd)

        # RESET WHAT THIS TOOL WROTE LAST TIME, so a run is a clean rebuild and not a patch on top
        # of its own output. Added 3-Sep-2026 with the EXCLUSIONS above, because without it an
        # excluded figure could not be taken back out: Fundbox's since-inception 325,000 had been
        # loaded by wave 2 and the exclusion only stopped it being loaded AGAIN, leaving the stale
        # $3,385 per business customer in the file. Only rows this tool stamped are touched, so a
        # volume written by any other tool is left exactly alone.
        for r in rows:
            if MARKER not in (r.get('notes') or ''):
                continue
            cleared_kind = (r.get('volume_metric') or '').strip()
            for c in VOL_COLS:
                r[c] = ''
            if (r.get('valuation_basis') or '').strip() == cleared_kind:
                r['valuation_basis'] = ''
            r['notes'] = (r['notes'].split(' || ' + MARKER)[0]).rstrip()
            reset += 1
        before = len(rows)
        total_before += before
        missing = [c for c in VOL_COLS if c not in cols]
        if missing:
            cols += missing
            for r in rows:
                for c in missing:
                    r.setdefault(c, '')
            added_cols.append((path, missing))
        hit, clash = 0, []
        print('\n%s' % path)
        for r in rows:
            key = (r['company_name'].strip(), (r.get('date') or '').strip())
            got = counts.pop(key, None)
            if not got:
                continue
            _rank, kind, n, paying, quote = got
            if (r.get('volume_metric') or '').strip() or (r.get('gmv_metric') or '').strip():
                # ALREADY CARRIES A VOLUME. Never overwritten: an originations, GMV or payment
                # volume figure is a different and usually better denominator, and the count stays
                # in the raw file. gmv_metric is checked too because the consumer file spells the
                # lane that way and a count must not quietly displace a GMV multiple.
                clash.append((key, r.get('volume_metric') or r.get('gmv_metric'), kind))
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
            # A COUNT LOAD MAY NEVER READMIT A REVENUE MULTIPLE. Added 3-Sep-2026, wave 3.
            #
            # This tool used to set in_medians = '1' on every row it touched. There is only ONE
            # in_medians gate in selector/match_reference.py and it governs whether a row may price
            # AT ALL, on any basis. So loading a user count also switched that row's REVENUE
            # multiple back on, and 12 rows that had been excluded by hand came back into revenue
            # ranges without anyone deciding it. Decagon at "at most 150x" was one of them, and it
            # lifted the top of two founders' ranges from 105.3 to 150.0. Factorial was another,
            # and its denominator is GROSS_REVENUE, which is the exact case match_reference warns
            # about at line 1205: "That is how Razorpay's 67.6x on a gross denominator sat in the
            # fintech file for four days."
            #
            # So the gate is raised only where there is no revenue multiple to readmit. Where a row
            # carries one and was excluded, the count is still written and still visible, and the
            # row is named below as BLOCKED. D8: a figure in the file but not in the engine is
            # reported as absent, not as pending. The real fix is to split the gate so a row can be
            # barred from revenue ranges and still price on a count, and that is Daniil's decision,
            # not something to slip in inside a sweep.
            was_in = (r.get('in_medians') or '').strip()
            if key in IN_MEDIANS_WAS_ZERO_AT_02836C8:
                was_in = '0'
                r['in_medians'] = '0'
            has_rev = (r.get('ev_revenue_x') or '').strip()
            if has_rev and was_in in ('0', ''):
                blocked.append((key, kind, r.get('ev_revenue_x'), r.get('revenue_basis'),
                                r.get('bound')))
            else:
                r['in_medians'] = '1'
            r['notes'] = ((r.get('notes') or '').rstrip() +
                          ' || ' + MARKER + ' from the round announcement itself: "%s". '
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
        total_hit += hit
        all_clash += clash
        if WRITE:
            buf = io.StringIO()
            w = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
            w.writeheader()
            for r in rows:
                w.writerow({c: r.get(c, '') for c in cols})
            io.open(path, 'w', encoding='utf-8').write(head + buf.getvalue())
        print('   rows in %d, rows out %d, counts loaded %d' % (before, len(rows), hit))

    print()
    for path, missing in added_cols:
        print('ADDED the volume lane to %s: %s' % (path, ', '.join(missing)))
    print('rows reset from this tool\'s own previous run: %d' % reset)
    print('rows in %d, counts loaded %d' % (total_before, total_hit))
    print('kinds not loadable as a denominator (recorded in raw only): %d' % len(skipped))
    print('figures EXCLUDED as a flow or a since-inception total, in writing: %d' % len(excluded))
    for k, kind, n, why in excluded:
        print('   %-22s %-8s %-20s %14s  %s' % (k[0][:22], k[1], kind, '{:,.0f}'.format(n), why))
    print('rounds that already carry a money volume, count NOT overwritten: %d' % len(all_clash))
    for k, have, kind in all_clash:
        print('   %-24s %-8s keeps %-30s instead of %s' % (k[0][:24], k[1], have, kind))
    print('counts loaded but BLOCKED from pricing, because the row carries a revenue multiple that\n'
          'was excluded by hand and one in_medians gate governs both lanes: %d' % len(blocked))
    for k, kind, rev, basis, bound in blocked:
        print('   %-24s %-8s %-20s blocked behind ev_revenue_x=%-8s %s %s'
              % (k[0][:24], k[1], kind, rev or '-', (basis or '-'), (bound or '')))
    print('counts with no matching round in either file: %d' % len(counts))
    for k in sorted(counts):
        print('   %s %s' % k)
    if not WRITE:
        print('\nDRY RUN. Re-run with --write.')
    return 0


sys.exit(main())
