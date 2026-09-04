#!/usr/bin/env python3
"""How many houses a founder actually gets, and how thin the thinnest lists are.

The compliance check answers "is anything on a card that should not be". This answers the
question underneath it: DOES A FOUNDER GET A LIST AT ALL. Those are different failures and only
one of them was being counted. On 3-Sep the table held 140 CALLABLE rows and 62 of them could
render; the other 78 were in the database and invisible to every founder, which nothing reported.

Run it after every change to data/investors.csv:  python3 tools/investor_coverage.py
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import match_reference as M                      # noqa: E402
import investors as I                            # noqa: E402
from golden_profiles import PROFILES             # noqa: E402

THIN = 3          # fewer than this and the list is not worth showing as a list


def main():
    callable_rows = [d for d in I.INVESTORS if 'CALLABLE' in (d.get('layer') or '')]
    rend = [d for d in callable_rows if I.renderable(d)[0]]
    # THE VOCABULARY REPORT. A sector name that matches no archetype matches no founder, and it
    # fails silently: the house simply never appears and nothing says why. Nine houses tagged
    # "Insurance" were invisible to every insurance founder until 4-Sep. The aliases in
    # investors.SECTOR_ALIASES translate what can be translated; what is printed below is what
    # cannot, and each one is either a missing alias or an industry our taxonomy does not carry.
    arch = {r[f].strip() for r in M.listed + M.private
            for f in ('archetype', 'archetype_secondary') if r.get(f)}
    reach, dead = I.sector_vocabulary(arch)
    print('SECTORS %d category names in the file | %d reach a founder | %d reach nobody'
          % (len(reach) + len(dead), len(reach), len(dead)))
    for c, (n, _h) in sorted(dead.items(), key=lambda x: -x[1][0]):
        print('        %-40s %3d houses carry it and no founder can match it' % (c, n))

    print('TABLE   %d houses | %d carry a CALLABLE layer | %d of those can render'
          % (len(I.INVESTORS), len(callable_rows), len(rend)))

    # WHY EACH BLOCKED ROW IS BLOCKED, because "78 incomplete" is not an instruction and
    # "31 need a cheque range, 13 need a dated deal" is.
    miss = {}
    for d in callable_rows:
        ok, m = I.renderable(d)
        if not ok:
            miss.setdefault(' + '.join(m), []).append(d['investor_name'])
    for why in sorted(miss, key=lambda k: -len(miss[k])):
        print('        %3d blocked on %s' % (len(miss[why]), why))

    # DOES GEOGRAPHY ACTUALLY DO ANYTHING? Nothing tested this, and that is why it took a
    # rebuild to notice it was doing nothing. The country is resolved from the edge header rather
    # than asked (docs/lead-capture.md), so no golden fixture carries one and the whole facet was
    # dead in every test we run. Two synthetic founders, identical but for the country, must get
    # different lists and must carry the exact-fit label. If this stops being true, geography has
    # silently stopped being scored again.
    base = dict(PROFILES[0][2])
    uk = dict(base, country='United Kingdom')
    us = dict(base, country='United States')
    picked, _mo, _pt = M.select_private(base, M.private)
    l_uk = I.match_callable(uk, raise_musd=1.0, want=12)
    l_us = I.match_callable(us, raise_musd=1.0, want=12)
    l_none = I.match_callable(base, raise_musd=1.0, want=12)
    names = lambda L: [c['investor'] for c in L]
    exact = lambda L: [c for c in L if c['tier'] == 0]
    print('GEOGRAPHY  UK %d houses (%d exact) | US %d (%d exact) | no country %d'
          % (len(l_uk), len(exact(l_uk)), len(l_us), len(exact(l_us)), len(l_none)))
    problems = []
    if names(l_uk) == names(l_us):
        problems.append('a UK founder and a US founder get the identical list: '
                        'geography is not being scored')
    if not exact(l_uk) and not exact(l_us):
        problems.append('no house reaches tier 0 for either country, so the exact-fit label '
                        'is unreachable')
    if any('location was not resolved' in (c.get('why') or '') for c in l_uk + l_us):
        problems.append('a founder WITH a country is being labelled as unresolved')
    if not all('location was not resolved' in (c.get('why') or '') for c in l_none):
        problems.append('a founder with no country is not being labelled as unresolved')
    for m in problems:
        print('        FAIL %s' % m)

    thin, tot = [], 0
    for k, _label, p in PROFILES:
        picked, _mo, _pt = M.select_private(p, M.private)
        pay = I.reveal_payload(p, picked, raise_musd=3.0)
        n = pay['callable']['count']
        tot += n
        if n < THIN:
            thin.append((k, n))
    print('FOUNDER %d fixtures | %d callable cards | %.1f a founder on average'
          % (len(PROFILES), tot, tot / float(len(PROFILES))))
    print('        %d fixtures get fewer than %d houses' % (len(thin), THIN))
    for k, n in thin:
        print('            %-24s %d' % (k, n))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
