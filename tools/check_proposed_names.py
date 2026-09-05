#!/usr/bin/env python3
"""Is this company already in our data? Run before any name goes on a ticker request.

Daniil, 4-Sep-2026, on being asked to pull Wix, JFrog and GitLab: "we ALREADY had these in our
database. WHY DID YOU ASK FOR THESE COMPS?"

Because nothing checked. The list was written from memory and the duplicate check was run
afterwards, as a separate thought. This makes it a command, so it cannot be a habit that lapses.

  python3 tools/check_proposed_names.py "Wix" "JFrog" "Green Dot"
  python3 tools/check_proposed_names.py --file docs/prompts/ticker-request-4sep.md

Exit 1 if any proposed name is already held.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import match_reference as M                      # noqa: E402


def held(name):
    n = name.strip().lower()
    if not n:
        return []
    out = []
    for r in M.listed:
        c = (r.get('company_name') or '').lower()
        if n in c or c.split(',')[0].split(' inc')[0].strip() == n:
            out.append(('listed', r.get('company_name'), r.get('exchange_ticker'),
                        'priced' if r.get('mult') is not None else 'HELD BUT NOT PRICED'))
    for r in M.private:
        c = (r.get('company_name') or '').lower()
        if n in c:
            out.append(('private', r.get('company_name'), r.get('date', ''),
                        'priced' if r.get('mult') is not None else 'no multiple'))
    return out


def main(argv):
    names = []
    if argv[:1] == ['--file']:
        txt = open(argv[1], encoding='utf-8').read()
        # every markdown table row's first cell, which is where a name sits in a ticker request
        for line in txt.splitlines():
            m = re.match(r'^\|\s*([A-Za-z][^|]{2,40}?)\s*\|', line)
            if m and m.group(1).lower() not in ('company', 'name', 'lane', 'target'):
                names.append(m.group(1))
    else:
        names = argv
    if not names:
        print(__doc__)
        return 2
    bad = 0
    for n in names:
        hits = held(n)
        if hits:
            bad += 1
            for where, nm, tk, note in hits[:3]:
                print('ALREADY HELD   %-28s -> %s %s (%s) [%s]' % (n, where, nm, tk, note))
        else:
            print('not held       %s' % n)
    print('\n%d proposed, %d already in the data.' % (len(names), bad))
    if bad:
        print('A name already in the file is not a pull. If the engine is not using it, that is a')
        print('matcher or tagging question: run tools/thin_lane_diagnosis.py and read the list, not')
        print('the headline.')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
