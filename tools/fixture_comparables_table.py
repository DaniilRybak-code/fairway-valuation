# -*- coding: utf-8 -*-
"""One table: every test company beside the comparables the engine chose for it.

Daniil, 8-Sep-2026, after march 1 showed three aerospace companies passing the gate on restaurant
and hospitality rounds: "give me a table with the whole set that we have, with one column for the
companies and a second column for the comparables that our engine chose. I now want to check it
one by one."

The gate (tools/peer_universe_check.py) counts names found and prices held. It cannot tell whether
a name makes sense. This table is the instrument for the person who can. It reads the golden
snapshots, so it shows exactly what a founder with that profile would be shown today, and writes
two files: a markdown table for reading, and a CSV with an empty VERDICT column for marking up in a
spreadsheet. A struck fixture (rule 5 of the gate) carries its reason in the last column.

  python3 tools/fixture_comparables_table.py            writes docs/fixture-comparables-<date>.md and .csv
"""
import csv
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
from golden_profiles import PROFILES, OUT_OF_MARKET   # noqa: E402

CLOSE = {'STRONG_OVERLAP': 'strong', 'PARTIAL_OVERLAP': 'partial', 'SHARED_PRODUCT': 'shared product',
         'THIN_OVERLAP': 'thin', None: '-', '': '-'}


def lane(e, name):
    rows = e.get(name) or []
    rng = e.get(name + '_range') or {}
    names = [r['company'] for r in rows]
    tag = CLOSE.get(rng.get('closeness'), rng.get('closeness') or '-')
    n = rng.get('n')
    head = '%s, %s priced' % (tag, n if isinstance(n, int) else 0)
    return head, names


def main():
    stamp = datetime.date.today().strftime('%-d%b').lower()
    out_md = os.path.join(HERE, 'docs', 'fixture-comparables-%s.md' % stamp)
    out_csv = os.path.join(HERE, 'docs', 'fixture-comparables-%s.csv' % stamp)
    rows = []
    for key, label, prof in PROFILES:
        path = os.path.join(HERE, 'selector', 'golden', key + '.json')
        if not os.path.exists(path):
            rows.append((key, label, '(no golden snapshot yet)', '', '', prof.get('struck', '')))
            continue
        e = json.load(open(path))['expected']
        lh, ln = lane(e, 'core')
        ph, pn = lane(e, 'private')
        listed = '%s: %s' % (lh, ', '.join(ln) or '(none)')
        private = '%s: %s' % (ph, ', '.join(pn) or '(none)')
        flags = []
        if key in OUT_OF_MARKET:
            flags.append('out of market')
        if prof.get('struck'):
            flags.append('STRUCK: ' + prof['struck'])
        rows.append((key, label, listed, private, prof.get('archetype', ''), '; '.join(flags)))

    with open(out_md, 'w', encoding='utf-8') as f:
        f.write('# Every test company beside the comparables the engine chose, %s\n\n'
                % datetime.date.today().strftime('%-d %B %Y'))
        f.write('Read from the golden snapshots (`selector/golden/*.json`), so this is exactly what a\n'
                'founder with that profile is shown today. "Listed" is the core listed lane, "private"\n'
                'the private-round lane; the word before the colon is how close the engine judged the\n'
                'lane (strong, partial, shared product, thin) and how many names in it carry a price.\n'
                'STRUCK means a person read the set and judged the names irrelevant (gate rule 5).\n'
                'The CSV beside this file has an empty VERDICT column for marking up one by one.\n\n')
        f.write('%d fixtures.\n\n' % len(rows))
        f.write('| # | fixture | what it says it is | archetype | listed comparables | private comparables | flags |\n')
        f.write('|---|---|---|---|---|---|---|\n')
        for i, (key, label, listed, private, arch, flags) in enumerate(rows, 1):
            cell = lambda s: str(s).replace('|', '/')
            f.write('| %d | %s | %s | %s | %s | %s | %s |\n'
                    % (i, key, cell(label), cell(arch), cell(listed), cell(private), cell(flags)))
    with open(out_csv, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['#', 'fixture', 'what it says it is', 'archetype', 'listed comparables',
                    'private comparables', 'flags', 'VERDICT (Daniil)'])
        for i, (key, label, listed, private, arch, flags) in enumerate(rows, 1):
            w.writerow([i, key, label, arch, listed, private, flags, ''])
    print('wrote %s and %s: %d fixtures, %d struck, %d out of market'
          % (os.path.relpath(out_md, HERE), os.path.relpath(out_csv, HERE), len(rows),
             sum(1 for r in rows if 'STRUCK' in r[5]), sum(1 for r in rows if 'out of market' in r[5])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
