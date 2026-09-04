# -*- coding: utf-8 -*-
"""Two checks, both written after the fault they catch had already happened.

CHECK 1, FILE VERSUS ENGINE. D8 says a figure that is in the file but not in the engine is ABSENT,
not pending. Nothing computed that comparison, so on 2 September fifty-eight priced rounds sat in
data/private-rounds.csv and reached no founder for days. The cause was a silent join: the engine
joins the rounds to data/private-companies-tags.csv on company_key and drops any round whose company
has no tag row. It was found by hand while writing a handover. This check computes it every run.

CHECK 2, CROSS-FILE DUPLICATES. AG1's January 2022 round was in the engine twice under two keys and
a third copy was one load away. The three spellings were "AG1", "AG1 (Athletic Greens)" and
"Athletic Greens (AG1)", so NO NAME MATCH FINDS IT. Match on the round: company tokens plus month
plus post-money. It was found by reading a golden diff, which is not a check.

Exit 1 on any finding. Run before any commit that touches a data file, next to check_raw_coverage.
"""
import csv, io, os, re, sys

ROUND_FILES = ['data/private-rounds.csv', 'data/private-rounds-consumer.csv']
TAG_FOR = {'data/private-rounds.csv': 'data/private-companies-tags.csv',
           'data/private-rounds-consumer.csv': 'data/private-companies-consumer-tags.csv'}
STOP = {'the', 'group', 'inc', 'ltd', 'bank', 'com', 'then', 'holdings', 'technologies'}
MON = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}


def rows_of(path):
    lines = [l for l in open(path) if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(lines))))


def toks(name):
    n = re.sub(r'[^a-z0-9 ]', ' ', (name or '').lower())
    return frozenset(t for t in n.split() if t and t not in STOP)


def ym(value):
    v = (value or '').strip()
    m = re.match(r'^(\d{4})-(\d{2})', v)
    if m:
        return '%s-%s' % (m.group(1), m.group(2))
    m = re.match(r'^(\d{1,2})-([A-Za-z]{3})[a-z]*-(\d{4})$', v)
    if m:
        return '%s-%02d' % (m.group(3), MON[m.group(2).lower()])
    m = re.match(r'^([A-Za-z]{3})[a-z]*-(\d{2})$', v)
    if m:
        return '20%s-%02d' % (m.group(2), MON[m.group(1).lower()])
    return ''


def num(v):
    v = (v or '').strip().replace(',', '')
    try:
        return float(v)
    except ValueError:
        return None


def engine_rows():
    """What match_reference actually loads. Imported, not reimplemented, so the check cannot drift
    from the loader it is checking."""
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(here, 'selector'))
    sys.path.insert(0, here)
    import match_reference as M
    return M.private


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    failures = 0
    loaded = engine_rows()
    in_engine = {(toks(r['company_name']), ym(str(r.get('date_iso') or r.get('date')))) for r in loaded}

    print('CHECK 1 -- every row in the file reaches the engine')
    total_file = 0
    for path in ROUND_FILES:
        rows = rows_of(path)
        total_file += len(rows)
        missing = [r for r in rows
                   if (toks(r['company_name']), ym(r.get('date_iso') or r.get('date'))) not in in_engine]
        tags = {t['company_key'] for t in rows_of(TAG_FOR[path])}
        print('   %-36s file %3d | engine %3d | ABSENT %d'
              % (path.split('/')[-1], len(rows), len(rows) - len(missing), len(missing)))
        for r in missing:
            why = 'no tag row for company_key %r' % r['company_key'] if r['company_key'] not in tags else 'reason unknown'
            print('      ABSENT  %-26s %-8s in_medians=%s  %s'
                  % (r['company_name'], r['date'], r['in_medians'], why))
            failures += 1
    print('   files hold %d rows | the engine loads %d' % (total_file, len(loaded)))

    print('\nCHECK 2 -- no round counted twice, matched on the ROUND and not the name')
    # Bucket on month + post-money first, then group inside the bucket by NAME TOKEN OVERLAP.
    # Exact token-set equality is not enough and this check failed its own planted fault by using it:
    # "AG1" gives {ag1} while "AG1 (Athletic Greens)" gives {ag1, athletic, greens}, so the two sets
    # are unequal and the duplicate walks straight through. Overlap is the test that works.
    buckets = {}
    total = 0
    for path in ROUND_FILES:
        for r in rows_of(path):
            pm = num(r.get('post_money_musd'))
            total += 1
            if pm is None:
                continue
            buckets.setdefault((ym(r.get('date_iso') or r.get('date')), round(pm, 1)), []).append((path.split('/')[-1], r))
    groups = []
    for (month, pm), members in buckets.items():
        unassigned = list(members)
        while unassigned:
            fname, seed = unassigned.pop(0)
            grp = [(fname, seed)]
            keep = []
            for f2, other in unassigned:
                if toks(seed['company_name']) & toks(other['company_name']):
                    grp.append((f2, other))
                else:
                    keep.append((f2, other))
            unassigned = keep
            if len(grp) > 1:
                groups.append((month, pm, grp))
    print('   rounds examined %d | duplicate groups %d' % (total, len(groups)))
    for month, pm, grp in sorted(groups):
        med = [x for _f, x in grp if str(x.get('in_medians')).strip() == '1']
        # A duplicate that is deliberately held out of the medians is managed, not a fault: the round
        # still votes once. Only more than one copy IN the medians is a silent double vote, and only
        # that fails the build. Managed duplicates are still printed, because an unexplained one is a
        # fault waiting to happen the next time somebody flips a flag.
        bad = len(med) > 1
        print('      %s  %s  post %s  [%d of %d in the medians]'
              % ('DOUBLE VOTE' if bad else 'duplicate, managed', month, pm, len(med), len(grp)))
        for fname, x in grp:
            print('         %-32s %-26s key=%-22s in_medians=%s' % (fname, x['company_name'], x['company_key'], x['in_medians']))
        if bad:
            failures += 1

    # CHECK 3, A ROW THAT REACHES THE ENGINE AND CARRIES NO PRICE.
    #
    # Daniil, 4-Sep-2026: "Negative multiples are not allowed, they should be marked as n.m."
    # The loader applies that rule, and this is the count in, count out, name what fell. These
    # companies are NOT dropped: they keep their name, their tags and their revenue and can be
    # shown as context. They cannot enter a range, a median or a quartile, which is what n.m.
    # means, and a silent version of that would be exactly the class of loss D-rules exist to stop.
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(here, 'selector'))
    import match_reference as M
    print('\nCHECK 3 -- multiples that are not meaningful, marked n.m. rather than dropped')
    priced = len([r for r in M.listed if r.get('mult') is not None])
    print('   listed rows %d | carry a revenue multiple %d | marked n.m. %d'
          % (len(M.listed), priced, len(M.not_meaningful)))
    for where, tk, name, field, value in M.not_meaningful:
        print('      n.m.  %-8s %-30s %-9s was %s' % (where, name[:30], field, value))
    if not M.not_meaningful:
        print('      none')

    print('\n%s' % ('PASS: every row reaches the engine and no round votes twice.' if not failures
                    else 'FAIL: %d finding(s) above. A row in the file and not in the engine is ABSENT, '
                         'not pending (D8); a round counted twice is a silent double vote.' % failures))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
