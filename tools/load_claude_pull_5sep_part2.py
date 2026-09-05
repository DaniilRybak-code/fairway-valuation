#!/usr/bin/env python3
"""
PART 2 OF THE 5-SEP-2026 PULL, second phase: Daniil's evening rulings and the additions.

    python3 tools/load_claude_pull_5sep_part2.py            # in your own terminal, after the raw files are committed
    FAIRWAY_NO_GIT=1 python3 tools/load_claude_pull_5sep_part2.py   # only through the bridge (skips the git guard)

What it does, in order, and each step prints count in, count out (rule D12):

  1. DANIIL'S RULING, 5-Sep-2026 (his words): "I never ruled to hold anything out of median because
     something is stated as floor. It is customary to say 'more than' in such announcements, which
     just take that figure for the valuation purposes." Moss (Aug-26), Restaurant365 (May-23) and
     AuditBoard (May-24) had been held out of the medians because valuation and revenue were both
     stated as floors; they go back in at the stated figures, bound left empty, note prepended.
     Udemy (Dec-25) is NOT released here: it was held for a different reason (no standalone price is
     stated, the value is 41% of a combined implied equity value) and Daniil listed it as "value to
     confirm".
  2. Loads the three control transactions from data/raw/2026-09-05_control-transactions-claude.csv
     (Confluent, Verint, Learning Technologies Group) and their tag rows, skipping any already present.
  3. Registers that raw file in tools/check_raw_coverage.py SOURCES.
  4. Rebuilds data/investors.csv, which now reads round two of the investor pull
     (data/raw/2026-09-05_investor-pull-claude-round2.csv, 14 CALLABLE and 10 EVIDENCE) through
     tools/load_investor_pull_5sep.py.
  5. Regenerates the golden snapshots (deliberate rebaseline) and prints the gate.

Idempotent. Refuses to run until git says the two new raw files are in a commit (rule D14), unless
FAIRWAY_NO_GIT=1.
"""
import csv, io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.chdir(ROOT)

RAW_ROUNDS = 'data/raw/2026-09-05_control-transactions-claude.csv'
RAW_TAGS = 'data/raw/2026-09-05_control-transactions-tags-claude.csv'
RAW_INV2 = 'data/raw/2026-09-05_investor-pull-claude-round2.csv'
WORK_ROUNDS = 'data/private-rounds.csv'
WORK_TAGS = 'data/private-companies-tags.csv'

RELEASE = ('moss-2026-08', 'restaurant365-2023-05', 'auditboard-2024-05')
RULING = ("RELEASED INTO THE MEDIANS 05-Sep-2026 ON DANIIL'S RULING: 'I never ruled to hold anything out of "
          "median because something is stated as floor. It is customary to say more than in such announcements, "
          "which just take that figure for the valuation purposes.' Stated figures taken as the figures; the "
          "earlier hold-out was Claude's own reading and is withdrawn. || ")


def header_line(path):
    for line in open(path, encoding='utf-8'):
        if not line.startswith('#'):
            return line.rstrip('\n')


def read_all(path):
    head = [l for l in open(path, encoding='utf-8') if l.startswith('#')]
    body = [l for l in open(path, encoding='utf-8') if not l.startswith('#')]
    cols = next(csv.reader([body[0].rstrip('\n')]))
    return head, cols, list(csv.DictReader(io.StringIO(''.join(body))))


def write_all(path, head, cols, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        f.write(''.join(head))
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def guard():
    if os.environ.get('FAIRWAY_NO_GIT') == '1':
        print('git guard skipped (FAIRWAY_NO_GIT=1): make sure the raw files are committed first')
        return
    for f in (RAW_ROUNDS, RAW_TAGS, RAW_INV2):
        out = subprocess.run(['git', 'log', '--oneline', '-1', '--', f], capture_output=True, text=True).stdout.strip()
        if not out:
            sys.exit('REFUSING TO LOAD: %s is not in any commit yet. Commit the raw files first (rule D14).' % f)
        print('raw committed: %s  (%s)' % (f, out))


def release_floors():
    head, cols, rows = read_all(WORK_ROUNDS)
    changed = []
    for r in rows:
        if r['transaction_id'] in RELEASE:
            if r['in_medians'] == '1' and r['notes'].startswith('RELEASED INTO THE MEDIANS'):
                continue
            r['in_medians'] = '1'
            r['bound'] = ''
            r['notes'] = RULING + r['notes']
            changed.append(r['transaction_id'])
    write_all(WORK_ROUNDS, head, cols, rows)
    print('floor ruling: %d of %d target rows released into the medians%s' % (len(changed), len(RELEASE), (': ' + ', '.join(changed)) if changed else ' (already done)'))


def append(raw, work, key):
    head, cols, have_rows = read_all(work)
    have = {r[key] for r in have_rows}
    new = list(csv.DictReader(open(raw, encoding='utf-8')))
    rawcols = next(csv.reader([header_line(raw)]))
    if rawcols != cols:
        sys.exit('HEADER MISMATCH between %s and %s, refusing (rule D11)' % (raw, work))
    kept = [r for r in new if r[key] not in have]
    skipped = [r[key] for r in new if r[key] in have]
    with open(work, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n'); w.writerows(kept)
    print('%s: %d rows in, %d loaded, %d already present%s' % (raw, len(new), len(kept), len(skipped), (': ' + ', '.join(skipped)) if skipped else ''))


def register_source():
    p = 'tools/check_raw_coverage.py'
    s = open(p, encoding='utf-8').read()
    if RAW_ROUNDS in s:
        print('check_raw_coverage.py already lists %s' % RAW_ROUNDS); return
    entry = ("    '%s': (\n        'company_name', 'date_iso',\n"
             "        ['data/private-rounds.csv', 'data/private-rounds-consumer.csv']),\n" % RAW_ROUNDS)
    anchor = "SOURCES = {\n"
    assert anchor in s
    open(p, 'w', encoding='utf-8').write(s.replace(anchor, anchor + entry, 1))
    print('check_raw_coverage.py: registered %s in SOURCES' % RAW_ROUNDS)


def main():
    guard()
    release_floors()
    append(RAW_ROUNDS, WORK_ROUNDS, 'transaction_id')
    append(RAW_TAGS, WORK_TAGS, 'company_key')
    register_source()
    print('\n--- rebuilding data/investors.csv from its sources (now including round two of the pull)')
    subprocess.run([sys.executable, 'tools/build_investors_table.py'], check=True)
    print('\n--- regenerating golden snapshots (deliberate rebaseline)')
    subprocess.run([sys.executable, 'selector/golden.py', '--write'], check=True, stdout=subprocess.DEVNULL)
    out = subprocess.run([sys.executable, 'tools/peer_universe_check.py'], capture_output=True, text=True).stdout
    print('\n'.join(l for l in out.splitlines() if 'fixtures |' in l))
    print('\nNow run sh tools/check_all.sh (FAIRWAY_NO_GIT=1 through the bridge), then commit.')


if __name__ == '__main__':
    main()
