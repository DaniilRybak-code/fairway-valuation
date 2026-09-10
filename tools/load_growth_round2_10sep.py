#!/usr/bin/env python3
"""GROWTH ENRICHMENT ROUND TWO, 10 September 2026: the rows the 9 September pass could not close
with search, plus Daniil's rulings of 10 September. Three columns filled, nothing else touched.

The 9 September pass ran out of web-search allowance mid-run, so about twenty-five of its 66
not-found rows rested on direct page reads only. Those were researched again with search. The raw
file data/raw/2026-09-10_private-growth-round2.csv records, for every one of the 28 rows in this
pass, either a year-on-year revenue growth rate with the page it came from and the sentence quoted,
or a reason in plain words why none exists. 11 close, 17 do not.

Daniil's rulings of 10 September, and what each did:
  1. "Sacra accepted in the absence of a better source." Applied to all five held-out rows. Only
     one changed: skims-2023-07 closes, and not on Sacra, because a better source turned out to
     exist (Retail Dive, round week, same two figures, named as net sales). suno-2025-11 and
     mercury-2025-03 stay open because the Sacra figures do not hold up when read: Suno's sentence
     contradicts itself and Mercury's rate rests on a 2023 denominator that has never been
     published. betterup-2021-10 and oura-2024-12 keep the company floors they already carry, and
     Oura's own later release contradicts the Sacra figure outright.
  2. "If there is no matching data on ARR, take revenue growth." Applied. sumup-2022-06 and
     zopa-2021-10 are loaded on revenue and on bank operating income against rows that price on a
     run rate. The 17 rows the 9 September pass loaded on the same reading stand unchanged.
  3. "Rerun the growth bands." Done separately, see docs/growth-round2-10sep.md. NOT applied to
     this load: the bands written here are still the 77 and 206 in selector/match_reference.py,
     because refitting is a change to every row in the file and the refit script's own
     goodness-of-fit test now fails.

THE FENCE, enforced here rather than promised, and identical to the 9 September loader:

  1. Only growth_pct_at_round, growth_band and growth_band_basis are ever written, and only on a
     row where all three are empty. A row that already carries a growth figure is REFUSED and
     named. Nothing is overwritten, including everything the 9 September pass loaded.
  2. Every other column on every row, and every row that is not a target, is byte-identical after
     the run. The script re-reads both files and compares them line by line, and exits 1 if
     anything else moved.
  3. No row is added and no row is removed. Count in equals count out, per file, or the run fails.
  4. The band written is recomputed from selector/match_reference.py and must equal the band in the
     raw file.
  5. Every raw row is accounted for by name: loaded, already loaded, refused, or not found.

Idempotent: run it twice and the second run reports 0 loaded and 11 already loaded.

    python3 tools/load_growth_round2_10sep.py
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, 'selector'))
import match_reference as M  # noqa: E402

RAW = 'data/raw/2026-09-10_private-growth-round2.csv'
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
