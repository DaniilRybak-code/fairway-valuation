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
    return 0


if __name__ == '__main__':
    sys.exit(main())
