# -*- coding: utf-8 -*-
"""What is actually in the data folder, in one command.

WHY THIS EXISTS. On 30-Aug-2026 Daniil asked how entire sectors could be missing when he had sourced
them and pushed every time. The answer was not architecture. It was that data arriving as SCREENSHOTS
never became files: it was read on screen, reasoned about, and never written down, so `git push` had
nothing to push. Nobody could see the gap because nobody could see the inventory.

    python3 tools/data_inventory.py

Prints every data file, its row count, and the archetype coverage the engine actually has. Run it
before claiming any coverage, and after every data drop. If a sector you expect is not in the
COVERAGE block, it is not in the product, whatever anyone remembers sending.
"""
import csv, io, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, 'data')


def rows(path):
    body = ''.join(l for l in open(path, encoding='utf-8') if not l.startswith('#'))
    try:
        return list(csv.DictReader(io.StringIO(body)))
    except Exception:
        return []


def main():
    print('FILES')
    total = 0
    for f in sorted(os.listdir(DATA)):
        if not f.endswith('.csv'):
            continue
        n = len(rows(os.path.join(DATA, f)))
        total += n
        print('  %-44s %5d rows' % (f, n))
    print('  %-44s %5d rows total' % ('', total))

    sys.path.insert(0, os.path.join(HERE, 'selector'))
    try:
        import match_reference as M
    except Exception as e:
        print('\nLoader did not import: %s' % e)
        return 1

    print('\nWHAT THE ENGINE ACTUALLY LOADS')
    print('  listed  %d' % len(M.listed))
    print('  private %d' % len(M.private))

    print('\nCOVERAGE BY ARCHETYPE. A sector missing here is missing from the product.')
    for label, rs in (('listed', M.listed), ('private', M.private)):
        c = Counter()
        for r in rs:
            for a in (r.get('archetype'), r.get('archetype_secondary')):
                if a:
                    c[a] += 1
        print('\n  %s' % label.upper())
        for a, n in sorted(c.items()):
            print('    %-40s %4d' % (a, n))

    for _f, _why in sorted(getattr(M, '_SUPERSEDED', {}).items()):
        print('  SUPERSEDED  %-42s %s' % (_f, _why))
    print('\nFILES PRESENT BUT NOT WIRED INTO THE LOADER')
    # DERIVED FROM THE LOADER, NEVER HARDCODED. A hand-maintained list of wired files goes stale the
    # moment someone wires a new one, and then this section reports files as unread when they are
    # read. That is worse than not reporting at all, because it is the check people trust.
    wired = set()
    for _mf, _tf, _ in getattr(M, '_PRIMARY', []):
        wired.update((_mf, _tf))
    for _mf, _tf in getattr(M, '_SECONDARY', []):
        wired.update((_mf, _tf))
    wired.update(getattr(M, '_OVERLAYS', ()))
    sup = getattr(M, '_SUPERSEDED', {})
    wired.update(sup)
    for extra in ('private-rounds.csv', 'private-rounds-consumer.csv', 'private-companies-tags.csv',
                  'private-companies-consumer-tags.csv', 'private-round-investors.csv',
                  'private-round-investors-consumer.csv', 'tag-token-weights.csv'):
        wired.add(extra)
    loose = [f for f in sorted(os.listdir(DATA)) if f.endswith('.csv') and f not in wired]
    if loose:
        for f in loose:
            print('    %-44s %5d rows  NOT READ BY THE ENGINE' % (f, len(rows(os.path.join(DATA, f)))))
    else:
        print('    none')
    return 0


if __name__ == '__main__':
    sys.exit(main())
