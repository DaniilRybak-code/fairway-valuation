# -*- coding: utf-8 -*-
"""Has every file Daniil supplied actually been ingested?

THE ONE CHECK NOTHING HAD. Daniil, 3-Sep-2026: "I will be providing data updates on regular basis,
so we need to make sure the updated numbers go into the database and start reaching the user as soon
as received, without creating any conflicts."

The 1-Sep listed refresh, 509 rows he recalculated and calendarised by hand, sat in data/raw for two
days while the engine ran on 30-August numbers. Every check passed the whole time, because every
check we had starts by reading data/, and this file had never got that far. A dataset that is not
ingested is invisible to a check that looks at what was ingested.

So this check starts at the other end: it walks data/raw, and for each supplied file asks whether
its contents are in the engine. It does that by sampling identifying values out of the raw file and
looking for them in the loaded universe, which needs no per-file configuration and therefore cannot
go stale when a new kind of file arrives.

A file is one of:
  INGESTED     its rows are in the engine
  PARTIAL      some are, some are not. Usually correct (rows excluded with a written reason) but
               always worth reading
  NOT INGESTED nothing from it reached the engine. THIS IS THE LOUD ONE
  SUPERSEDED   listed here on purpose, in SUPERSEDED below, with the file that replaced it
  REFERENCE    not data to ingest: a prompt, a note, a screenshot
"""
import csv
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import match_reference as M                      # noqa: E402

RAW = 'data/raw'
# A file that is deliberately not the current one, with the file that replaced it. An entry here is
# a decision and it carries its reason, which is the difference between superseded and forgotten.
SUPERSEDED = {
    '2026-09-02_lending-screen.csv':
        'superseded by 2026-09-03_lending-screen-v2.csv, which removed every '
        'cumulative-since-inception denominator',
    '2026-09-02_sector-screen.csv':
        'superseded by 2026-09-02_sector-screen-fixed.csv',
    '2026-08-31_capiq-tpv-block.csv': 'superseded by v4',
    '2026-08-31_capiq-tpv-block-v2.csv': 'superseded by v4',
    '2026-08-31_capiq-tpv-block-v3.csv': 'superseded by v4',
}
# Files that are not a dataset to ingest.
REFERENCE = ('-targets.csv', '-sourcing.csv', 'pull-list', 'prompt', 'needed')


def names_in(path):
    """Identifying strings from a raw file: company names and tickers."""
    out = set()
    try:
        lines = [l for l in io.open(path, encoding='utf-8', errors='replace')
                 if l.strip() and not l.lstrip('"').startswith('#')]
    except OSError:
        return out
    for row in csv.reader(lines):
        for cell in row[:4]:
            c = (cell or '').strip().strip('"')
            if len(c) < 3 or len(c) > 60:
                continue
            if re.match(r'^[-\d.,%$ ]+$', c):
                continue
            out.add(c.lower())
    return out


def main():
    have = set()
    for r in M.listed:
        have.add((r.get('company_name') or '').strip().lower())
        have.add((r.get('exchange_ticker') or '').strip().lower())
    for r in M.private:
        have.add((r.get('company_name') or '').strip().lower())
        have.add((r.get('company_key') or '').strip().lower())
    # The investor table is a THIRD destination and the first version of this check did not know
    # about it, so it reported the two seed investor screens as unused when they are the source of
    # data/investors.csv. A check that cries wolf is a check nobody runs.
    try:
        for d in csv.DictReader([l for l in io.open('data/investors.csv', encoding='utf-8')
                                 if not l.startswith('#')]):
            have.add((d.get('investor_name') or '').strip().lower())
            have.add((d.get('investor_key') or '').strip().lower())
    except OSError:
        pass
    bad, rows = [], []
    for f in sorted(os.listdir(RAW)):
        if not f.endswith('.csv'):
            continue
        if any(k in f for k in REFERENCE):
            rows.append((f, 'REFERENCE', '', 0, 0))
            continue
        if f in SUPERSEDED:
            rows.append((f, 'SUPERSEDED', SUPERSEDED[f], 0, 0))
            continue
        names = names_in(os.path.join(RAW, f))
        if not names:
            rows.append((f, 'EMPTY', 'no identifying values found', 0, 0))
            continue
        hit = len(names & have)
        pct = 100.0 * hit / len(names)
        if pct < 5:
            state, note = 'NOT INGESTED', 'nothing from this file is in the engine'
            bad.append(f)
        elif pct < 80:
            state, note = 'PARTIAL', 'some rows are not in the engine, check they were excluded on purpose'
        else:
            state, note = 'INGESTED', ''
        rows.append((f, state, note, hit, len(names)))
    print('SUPPLIED FILES AND WHETHER THEY REACHED THE ENGINE\n')
    for f, state, note, hit, tot in rows:
        extra = (' %d of %d names found' % (hit, tot)) if tot else ''
        print('%-14s %-46s%s' % (state, f[:46], extra))
        if note:
            print('               %s' % note)
    print()
    if bad:
        print('FAIL: %d supplied file(s) reached nothing.' % len(bad))
        for f in bad:
            print('   %s' % f)
        print('A dataset sitting unused in data/raw is the most expensive failure in this repo:')
        print('somebody spent real time producing it and the founder never sees it. Either ingest')
        print('it, or record it in SUPERSEDED above with the file that replaced it.')
        return 1
    print('PASS: every supplied dataset has reached the engine, or is recorded as superseded.')
    return 0


sys.exit(main())
