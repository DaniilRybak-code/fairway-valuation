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
    'data/raw/2026-09-02_sector-screen-fixed.csv': (
        'company_name', 'transaction_date',
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
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Ninjacart', '2021-12'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Vegrow', '2023-12'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'ElasticRun', '2022-02'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'DeHaat', '2022-10'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'eFishery', '2023-07'):
        'Not loaded. Reported figures were later found to be fabricated; the sheet marks it excluded with no usable denominator.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'WayCool Foods', '2022-06'):
        'HELD FOR A RULING. Denominator INR 9,306m is total revenue including interest and other operating income; operating revenue was INR 926.9 crore. The multiple stays 5.9x either way, so this is a basis label, not a value. See finding 1.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Octopus Energy Group', '2021-12'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Octopus Energy Group', '2023-12'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Fuse Energy', '2025-12'):
        'Not loaded. No public valuation: the cited sources do not state one, so there is no numerator. NOT FOUND, not an estimate.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Octopus Energy Group', '2022-07'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Octopus Energy Group', '2021-09'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Octopus Energy Group', '2024-05'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Enpal', '2023-01'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Blockworks', '2023-05'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'BlockFi', '2021-03'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Celsius Network', '2021-10'):
        'Not loaded. Bankruptcy and fraud findings; the sheet calculates the 25.8x but marks the row excluded.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'MoonPay', '2021-11'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Fireblocks', '2022-01'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'ConsenSys', '2022-03'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Thirty Madison', '2021-06'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Cityblock Health', '2021-09'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Alan', '2022-05'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Devoted Health', '2021-10'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Doctolib', '2022-03'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Virta Health', '2021-04'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Aledade', '2023-06'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Ro', '2021-03'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'upGrad', '2021-08'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'LEAD School', '2022-01'):
        'HELD FOR A RULING. Denominator INR 600m looks like total income; entrackr reads operating revenue of Rs 57.1 crore (INR 571m) from the RoC filings, giving 142.2x not 135.3x. The cited Forbes India source returns 403 and cannot be checked. See finding 1.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'MasterClass', '2021-05'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Vedantu', '2021-09'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'BetterUp', '2021-10'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Guild Education', '2022-06'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'EGYM', '2023-07'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Restore Hyper Wellness', '2021-12'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Oura', '2024-12'):
        'HELD FOR A RULING. The $225m denominator rests on Sacra alone, which is tier 4, and the cited TechCrunch article carries no revenue figure. Denominator basis also says FY2024 expected while the metric period says FY2023 estimate. See findings 2 and 3.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Athletic Greens (AG1)', '2022-01'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Noom', '2021-05'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'wefox', '2022-07'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'The Zebra', '2021-04'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Alan', '2024-09'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Alan', '2026-06'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'wefox', '2021-05'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Roblox', '2021-01'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Epic Games', '2021-04'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Voodoo', '2021-08'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Discord', '2021-09'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Epic Games', '2022-04'):
        "Transcribed and arithmetically verified 2 Sep 2026 from Daniil's screenshots. Not yet wired into the engine: the sector screen is pending Daniil's ruling on the gross-versus-net rows in docs/sector-screen-fixed-verdicts-2sep.md. Remove this entry when the row is loaded.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Dream Sports', '2021-11'):
        'HELD FOR A RULING. Denominator INR 27,060m is TOTAL INCOME (Rs 2,705.56 crore). Revenue from operations was Rs 2,551.59 crore. On revenue from operations the multiple is 23.4x, not 22.1x. See docs/sector-screen-fixed-verdicts-2sep.md finding 1.',
}


def rows_of(path):
    lines = [l for l in open(path) if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(lines))))


def key(name):
    return re.sub(r'[^a-z0-9]', '', (name or '').lower())


_MON = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}


def ym(value):
    # The sheets arrive in three date shapes. All three must parse, or a row that IS
    # loaded looks unaccounted for and the check cries wolf until somebody stops reading it.
    v = (value or '').strip()
    m = re.match(r'^(\d{4})-(\d{2})', v)
    if m:
        return '%s-%s' % (m.group(1), m.group(2))
    m = re.match(r'^(\d{1,2})-([A-Za-z]{3})[a-z]*-(\d{4})$', v)
    if m:
        return '%s-%02d' % (m.group(3), _MON[m.group(2).lower()])
    m = re.match(r'^([A-Za-z]{3})[a-z]*-(\d{4})$', v)
    if m:
        return '%s-%02d' % (m.group(2), _MON[m.group(1).lower()])
    return ''


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
