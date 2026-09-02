#!/usr/bin/env python3
"""
THE ROW-ACCOUNTING CHECK. Run it after every load, and before every commit.

    python3 tools/check_raw_coverage.py          exits 1 if any supplied row is unaccounted for

WHY IT EXISTS. Daniil spends hours building a sheet and sending it through as photographs. Twice
now his work has been silently lost after arriving safely:

  02-Sep-2026  the loader deduplicated on COMPANY rather than on company AND round, so six rounds
               belonging to companies we already held were skipped without a word
  01/02-Sep    two screenshot batches carried source URLs in columns AA and AB and the target
               schema had no field for them, so they landed nowhere and nothing counted their
               absence

Durability rule 11 fixed the second by requiring the schema to carry every column. This tool fixes
the first, and it is the general answer: **EVERY ROW HE SUPPLIES MUST BE ACCOUNTED FOR BY NAME,
either loaded or listed in EXCLUSIONS below with a written reason.** Silence is not an outcome.

The check is deliberately dumb. It matches on company plus year-month, never on company alone,
because company-alone matching is the exact bug it was written to catch.

HOW TO ADD A NEW SUPPLIED FILE. Add one entry to SOURCES. If a row genuinely should not be loaded,
add it to EXCLUSIONS with a reason a stranger could audit. Never make this pass by deleting a row
from a raw file: raw files are the record of what Daniil sent and are append-only.
"""
import csv, io, os, re, sys

# supplied file -> (company column, date column, the loaded files it may land in)
SOURCES = {
    'data/raw/2026-09-01_private-transactions-daniil.csv': (
        'company', 'txn_date',
        ['data/private-rounds.csv', 'data/private-rounds-consumer.csv']),
}

# (supplied file, company, YYYY-MM) -> the reason it is not loaded. Auditable, or it does not count.
EXCLUSIONS = {
    ('data/raw/2026-09-01_private-transactions-daniil.csv', 'Figma', '2024-05'):
        'Same round as our Figma Jul-24 row, same Axios URL. We re-dated it from tender LAUNCH to '
        'tender CLOSE, which is the honest date for a tender. Same $12.5bn, $700m ARR, 17.9x.',
    ('data/raw/2026-09-01_private-transactions-daniil.csv', 'Canva', '2024-05'):
        'Same round as our Canva Apr-24 row, same Forbes URL. The $26bn secondary completed in '
        'early April 2024 and there is no May-2024 Canva share sale. Priced 02-Sep-2026 on Daniil\'s '
        'ruling off Canva\'s own published figure of more than US$2.2bn annualised revenue.',
}


def rows_of(path):
    lines = [l for l in open(path) if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(lines))))


def key(name):
    return re.sub(r'[^a-z0-9]', '', (name or '').lower())


def ym(value):
    m = re.match(r'^(\d{4})-(\d{2})', (value or '').strip())
    return '%s-%s' % (m.group(1), m.group(2)) if m else ''


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    failures = 0

    for src, (ccol, dcol, targets) in SOURCES.items():
        if not os.path.exists(src):
            print('MISSING SUPPLIED FILE %s' % src)
            failures += 1
            continue
        supplied = rows_of(src)

        loaded = set()
        for t in targets:
            if not os.path.exists(t):
                continue
            for r in rows_of(t):
                loaded.add((key(r.get('company_name')), ym(r.get('date_iso'))))

        unaccounted = []
        excused = 0
        for r in supplied:
            k = (key(r[ccol]), ym(r[dcol]))
            if k in loaded:
                continue
            if (src, r[ccol], ym(r[dcol])) in EXCLUSIONS:
                excused += 1
                continue
            unaccounted.append(r)

        print('%s' % src)
        print('   supplied %d | loaded %d | excluded with a written reason %d | UNACCOUNTED %d'
              % (len(supplied), len(supplied) - len(unaccounted) - excused, excused,
                 len(unaccounted)))
        for r in unaccounted:
            print('   UNACCOUNTED  %-24s %s' % (r[ccol], r[dcol]))
        failures += len(unaccounted)

    print()
    if failures:
        print('FAIL: %d supplied rows are neither loaded nor excluded with a reason.' % failures)
        print('Load them, or add them to EXCLUSIONS in this file with a reason. Do not delete them '
              'from the raw file: raw files are the record of what was sent and are append-only.')
        sys.exit(1)
    print('PASS: every supplied row is accounted for.')


if __name__ == '__main__':
    main()
