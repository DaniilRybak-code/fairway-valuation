#!/usr/bin/env python3
"""
PHASE 2 OF THE 5-SEP-2026 PULL: load the committed raw files into the working files.

    python3 tools/load_claude_pull_5sep.py            # in your own terminal, after commit 1 is in
    FAIRWAY_NO_GIT=1 python3 tools/load_claude_pull_5sep.py   # only through the bridge (skips the git guard)

Rule D14 (raw first): the raw files are committed before anything is built on them, so this script
refuses to run until git says data/raw/2026-09-05_private-rounds-claude.csv is in a commit. It then:

  1. appends the 24 rounds to data/private-rounds.csv and the 21 tag rows to
     data/private-companies-tags.csv, skipping any transaction_id or company_key already present,
     and prints count in, count out, and what was skipped by name (rule D12);
  2. registers the raw file in tools/check_raw_coverage.py SOURCES so check 2 accounts for every row;
  3. rebuilds data/investors.csv from its sources, which now include the 5-Sep investor pull
     (tools/load_investor_pull_5sep.py, hooked into tools/build_investors_table.py);
  4. regenerates the golden snapshots (the 24 rounds move eight fixtures from FAIL to PASS, 81 to 89
     of 102 on the dry run of 5-Sep) and prints the gate.

Then run FAIRWAY_NO_GIT=1 sh tools/check_all.sh (or without the flag in your own terminal) and commit.
Idempotent: running it twice loads nothing twice.
"""
import csv, io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.chdir(ROOT)

RAW_ROUNDS = 'data/raw/2026-09-05_private-rounds-claude.csv'
RAW_TAGS = 'data/raw/2026-09-05_private-companies-tags-claude.csv'
RAW_INV = 'data/raw/2026-09-05_investor-pull-claude.csv'
WORK_ROUNDS = 'data/private-rounds.csv'
WORK_TAGS = 'data/private-companies-tags.csv'


def header_line(path):
    for line in open(path, encoding='utf-8'):
        if not line.startswith('#'):
            return line.rstrip('\n')


def rows_of(path):
    lines = [l for l in open(path, encoding='utf-8') if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(lines))))


def guard():
    if os.environ.get('FAIRWAY_NO_GIT') == '1':
        print('git guard skipped (FAIRWAY_NO_GIT=1): make sure the raw files are committed first')
        return
    for f in (RAW_ROUNDS, RAW_TAGS, RAW_INV):
        out = subprocess.run(['git', 'log', '--oneline', '-1', '--', f], capture_output=True, text=True).stdout.strip()
        if not out:
            sys.exit('REFUSING TO LOAD: %s is not in any commit yet. Commit the raw files first (rule D14).' % f)
        print('raw committed: %s  (%s)' % (f, out))


def append(raw, work, key):
    cols = next(csv.reader([header_line(work)]))
    have = {r[key] for r in rows_of(work)}
    new = rows_of(raw)
    rawcols = next(csv.reader([header_line(raw)]))
    if rawcols != cols:
        sys.exit('HEADER MISMATCH between %s and %s, refusing (rule D11)' % (raw, work))
    kept, skipped = [], []
    for r in new:
        (skipped if r[key] in have else kept).append(r)
    with open(work, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writerows(kept)
    print('%s: %d rows in, %d loaded, %d already present%s'
          % (raw, len(new), len(kept), len(skipped), (': ' + ', '.join(r[key] for r in skipped)) if skipped else ''))
    return len(kept)


def register_source():
    p = 'tools/check_raw_coverage.py'
    s = open(p, encoding='utf-8').read()
    if RAW_ROUNDS in s:
        print('check_raw_coverage.py already lists %s' % RAW_ROUNDS)
        return
    entry = ("    '%s': (\n        'company_name', 'date_iso',\n"
             "        ['data/private-rounds.csv', 'data/private-rounds-consumer.csv']),\n" % RAW_ROUNDS)
    anchor = "SOURCES = {\n"
    assert anchor in s
    s = s.replace(anchor, anchor + entry, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('check_raw_coverage.py: registered %s in SOURCES' % RAW_ROUNDS)


def main():
    guard()
    n1 = append(RAW_ROUNDS, WORK_ROUNDS, 'transaction_id')
    n2 = append(RAW_TAGS, WORK_TAGS, 'company_key')
    register_source()
    print('\n--- rebuilding data/investors.csv from its sources')
    subprocess.run([sys.executable, 'tools/build_investors_table.py'], check=True)
    print('\n--- regenerating golden snapshots (deliberate rebaseline: %d rounds and %d tag rows landed)' % (n1, n2))
    subprocess.run([sys.executable, 'selector/golden.py', '--write'], check=True, stdout=subprocess.DEVNULL)
    print('\n--- the gate')
    out = subprocess.run([sys.executable, 'tools/peer_universe_check.py'], capture_output=True, text=True).stdout
    print('\n'.join(l for l in out.splitlines() if 'fixtures |' in l or l.startswith('Currently')))
    print('\nNow run: FAIRWAY_NO_GIT=1 sh tools/check_all.sh   (drop the flag in your own terminal), then commit.')


if __name__ == '__main__':
    main()
