#!/usr/bin/env python3
"""GROWTH ENRICHMENT, 9 September 2026: three columns filled on the private rounds, nothing else touched.

The work order (docs/prompts/growth-enrichment-9sep.md) is an enrichment, not an edit. 163 private
rounds that price a founder's range carried no growth figure. The raw file
data/raw/2026-09-09_private-growth-enrichment.csv records, for every one of the 163, either a
year-on-year revenue growth rate with the page it came from and the sentence quoted, or a reason in
plain words why none could be found. This script moves the figures that were found into the three
columns that already exist on data/private-rounds.csv and data/private-rounds-consumer.csv:

    growth_pct_at_round     the number, a plain percentage (140 means 140 per cent)
    growth_band             MATURE / GROWING / HYPER, computed by selector/match_reference.band_of,
                            never judged (BAND_LOW and BAND_HIGH are read from the code, 77 and 206
                            on the day this was written)
    growth_band_basis       DISCLOSED / DERIVED / THIRD_PARTY_DATED / STATED

THE FENCE, enforced here rather than promised:

  1. Only those three columns are ever written, and only on a row where all three are empty. A row
     that already carries a growth figure is REFUSED and named, even if the raw file has a figure
     for it. Nothing is overwritten.
  2. Every other column on every row, and every row that is not a target, is byte-identical after
     the run. The script re-reads both files and compares them line by line, and exits 1 if
     anything else moved. The comment header at the top of each file is written back unchanged.
  3. No row is added and no row is removed. Count in equals count out, per file, or the run fails.
  4. The band written is recomputed from the code and must equal the band in the raw file.
  5. Every raw row is accounted for by name (rule D12): loaded, already loaded, refused, or not
     found. A raw row whose transaction_id is not in the named file is a FAILURE, not a skip.

Matching is on transaction_id, which is company plus year and month, and the script also checks
that company_key and date_iso agree with the target row, so a wrong row can never be written by a
name collision.

Idempotent: run it twice and the second run reports 0 changed and the same refusals.

    python3 tools/load_growth_enrichment_9sep.py
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, 'selector'))
import match_reference as M  # noqa: E402

RAW = 'data/raw/2026-09-09_private-growth-enrichment.csv'
FILES = {'private-rounds.csv': 'data/private-rounds.csv',
         'private-rounds-consumer.csv': 'data/private-rounds-consumer.csv'}
COLS = ('growth_pct_at_round', 'growth_band', 'growth_band_basis')
BASES = ('DISCLOSED', 'DERIVED', 'THIRD_PARTY_DATED', 'STATED')


def read(path):
    """Raw text, the comment header, the header-line index, the column list and the rows."""
    raw = open(path, newline='').read()
    lines = raw.split('\n')
    n = 0
    while n < len(lines) and lines[n].lstrip('"').startswith('#'):
        n += 1
    head = '\n'.join(lines[:n]) + ('\n' if n else '')
    rows = list(csv.DictReader(io.StringIO('\n'.join(lines[n:]))))
    fields = list(rows[0].keys())
    return raw, head, n, fields, rows


def write(path, head, fields, rows):
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, '') for k in fields})
    open(path, 'w', newline='').write(head + out.getvalue())


def parse_line(header_line, line):
    return next(csv.DictReader(io.StringIO(header_line + '\n' + line)))


def check_fence(path, before, after, n_comment, fields, n_in, changed_idx):
    """Every line that differs must be a loaded row, and on it only the three columns may differ."""
    a, b = before.split('\n'), after.split('\n')
    ok = True
    if len(a) != len(b):
        print('FAIL: %s has %d lines before and %d after' % (path, len(a), len(b)))
        return False
    header_line = a[n_comment]
    for i, (la, lb) in enumerate(zip(a, b)):
        if la == lb:
            continue
        ri = i - n_comment - 1                      # data-row index; the header sits at n_comment
        if ri < 0 or ri >= n_in or ri not in changed_idx:
            print('FAIL: %s line %d differs and is not a row this run loaded' % (path, i + 1))
            ok = False
            continue
        ra, rb = parse_line(header_line, la), parse_line(header_line, lb)
        diff = [k for k in fields if ra.get(k, '') != rb.get(k, '')]
        outside = [k for k in diff if k not in COLS]
        if outside:
            print('FAIL: %s line %d (%s) changed columns outside the three: %s'
                  % (path, i + 1, rb.get('transaction_id'), outside))
            ok = False
    return ok


def main():
    raw_rows = list(csv.DictReader(open(RAW, newline='')))
    print('RAW  %s: %d rows' % (RAW, len(raw_rows)))
    by_file = {}
    for x in raw_rows:
        by_file.setdefault(x['source_file'], []).append(x)
    unknown = sorted(set(by_file) - set(FILES))
    if unknown:
        print('FAIL: raw rows name a file this script does not know: %s' % unknown)
        return 1
    print('BANDS from selector/match_reference.py: MATURE below %s, GROWING to %s, HYPER above.\n'
          % (M.BAND_LOW, M.BAND_HIGH))

    failed = False
    tot = dict(n_in=0, n_out=0, loaded=0, already=0, refused=0, not_found=0, raw=0)
    for name, path in FILES.items():
        before, head, n_comment, fields, rows = read(path)
        n_in = len(rows)
        missing = [c for c in COLS if c not in fields]
        if missing:
            print('FAIL: %s has no column %s' % (path, missing))
            return 1
        index = {}
        for i, r in enumerate(rows):
            index.setdefault(r['transaction_id'], []).append(i)

        loaded, already, refused, not_found, unmatched, band_bad = [], [], [], [], [], []
        changed_idx = set()
        for x in by_file.get(name, []):
            tid = x['transaction_id']
            hits = index.get(tid, [])
            if len(hits) != 1:
                unmatched.append((tid, '%d rows match in %s' % (len(hits), name)))
                continue
            r = rows[hits[0]]
            if r['company_key'] != x['company_key'] or r['date_iso'] != x['date_iso']:
                unmatched.append((tid, 'company_key or date_iso disagree: file %s %s, raw %s %s'
                                  % (r['company_key'], r['date_iso'], x['company_key'], x['date_iso'])))
                continue
            pct = (x['growth_pct_at_round'] or '').strip()
            if not pct:
                not_found.append((tid, x['not_found_reason']))
                continue
            band = M.band_of(pct)
            basis = (x['growth_band_basis'] or '').strip()
            if not band or band != x['growth_band'] or basis not in BASES:
                band_bad.append((tid, pct, x['growth_band'], band, basis))
                continue
            had = tuple((r.get(c) or '').strip() for c in COLS)
            if any(had):
                if had == (pct, band, basis):
                    already.append(tid)              # a second run: nothing to do
                else:
                    refused.append((tid, had))
                continue
            r['growth_pct_at_round'], r['growth_band'], r['growth_band_basis'] = pct, band, basis
            changed_idx.add(hits[0])
            loaded.append(tid)

        if changed_idx:
            write(path, head, fields, rows)

        after, head2, n_comment2, fields2, rows2 = read(path)
        n_out = len(rows2)
        if head != head2 or n_comment != n_comment2 or fields != fields2:
            print('FAIL: %s header or columns changed' % path)
            failed = True
        if n_in != n_out:
            print('FAIL: %s rows in %d, rows out %d' % (path, n_in, n_out))
            failed = True
        if not check_fence(path, before, after, n_comment, fields, n_in, changed_idx):
            failed = True

        n_raw = len(by_file.get(name, []))
        tot['n_in'] += n_in; tot['n_out'] += n_out; tot['raw'] += n_raw
        tot['loaded'] += len(loaded); tot['already'] += len(already)
        tot['refused'] += len(refused); tot['not_found'] += len(not_found)
        print('%-28s IN %3d  OUT %3d  changed %3d  |  raw rows %3d: loaded %3d, already loaded %3d, '
              'refused %2d, not found %2d, unmatched %d, band mismatch %d'
              % (name, n_in, n_out, len(changed_idx), n_raw, len(loaded), len(already),
                 len(refused), len(not_found), len(unmatched), len(band_bad)))
        if loaded:
            print('  LOADED (%d): %s' % (len(loaded), ', '.join(loaded)))
        if already:
            print('  ALREADY LOADED with the same figure, untouched (%d): %s' % (len(already), ', '.join(already)))
        if refused:
            print('  REFUSED, already carry a different growth figure and are left exactly as they were (%d):' % len(refused))
            for tid, had in refused:
                print('    %-32s has %s' % (tid, had))
        if not_found:
            print('  NOT FOUND in the raw file, nothing written (%d):' % len(not_found))
            for tid, why in not_found:
                print('    %-32s %s' % (tid, (why or '')[:120]))
        if unmatched:
            print('  UNMATCHED, and that is a failure (%d):' % len(unmatched))
            for tid, why in unmatched:
                print('    %-32s %s' % (tid, why))
            failed = True
        if band_bad:
            print('  BAND OR BASIS MISMATCH between the raw file and the code, nothing written, and that is a failure (%d):' % len(band_bad))
            for tid, pct, raw_band, code_band, basis in band_bad:
                print('    %-32s pct %s raw band %s code band %s basis %s' % (tid, pct, raw_band, code_band, basis))
            failed = True
        if len(loaded) + len(already) + len(refused) + len(not_found) + len(unmatched) + len(band_bad) != n_raw:
            print('FAIL: %s raw rows not all accounted for' % name)
            failed = True
        print()

    print('TOTAL  IN %d  OUT %d  |  raw rows %d: loaded %d, already loaded %d, refused %d, not found %d'
          % (tot['n_in'], tot['n_out'], tot['raw'], tot['loaded'], tot['already'], tot['refused'], tot['not_found']))
    if tot['n_in'] != tot['n_out']:
        print('FAIL: a row was added or dropped.')
        failed = True
    if tot['raw'] != len(raw_rows):
        print('FAIL: %d raw rows, %d routed to a file.' % (len(raw_rows), tot['raw']))
        failed = True
    print('FAIL: the fence was crossed, see above.' if failed else 'OK: only the three growth columns changed, and only on rows that were empty.')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
