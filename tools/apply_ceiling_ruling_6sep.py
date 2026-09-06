#!/usr/bin/env python3
"""The ceiling ruling applied throughout, on Daniil's word of 6 September 2026 (evening).

THE RULING: "The ceiling ruling should not be applicable to StockX only, should be applicable
throughout." A multiple built on a "more than", "over", "crossed", "surpassed" or "almost" figure is
a CEILING or a FLOOR (rule B5), displayed as "at most" or "at least". It is never a reason to hold
the row out of the medians. Thresholds are a customary way of disclosing metrics in financing
rounds.

THE SWEEP. Of 320 private rounds, 84 are held out of the medians. Twelve carry a printed multiple
with a bound mark. Ten of those are held for the bound and nothing else, and are released here.
Two are held for a second reason that the ruling does not touch, and stay held, named:

  perplexity-2024-01   the $520m post-money is press-reported (Reuters), not company-disclosed;
                       the row is RECORD ONLY on the valuation, not on the threshold.
  marqeta-2020-05      the revenue basis is unstated ("probably gross"); rule B3 has no lane for
                       a figure whose basis is unknown when the row itself says it is unknown.

ONE FLAG, NOT RESOLVED HERE: factorial-2022-10 carries revenue_basis GROSS_REVENUE in the field and
"revenue_basis is corrected to NET_REVENUE" in its own note. Released on the label the field
carries (gross); the contradiction goes to the B3 audit.

The remaining 72 held rows carry no multiple at all, or are held as duplicates, estimates,
secondary-only rounds, originations multiples, or rows with an entity or period problem. None of
them is a threshold case and none is touched.

COUNT IN, COUNT OUT, per file. Only in_medians changes, plus a note. Idempotent.

  python3 tools/apply_ceiling_ruling_6sep.py
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)

MARK = 'RELEASED 6-Sep-2026 ON THE CEILING RULING'
NOTE = (MARK + ' (Daniil, evening: the ceiling ruling applies throughout, a "more than" figure is '
        'a bound, never an exclusion; rule B5 displays it as at most or at least).')
RELEASE = ['anthropic-2026-05', 'anthropic-2025-09', 'vercel-2024-05', 'databricks-2023-09',
           'docker-2022-03', 'miro-2022-01', 'notion-2026-01', 'payfit-2022-01',
           'decagon-2026-01', 'factorial-2022-10']
FILES = ['data/private-rounds.csv', 'data/private-rounds-consumer.csv']


def main():
    seen, changed_total, already = set(), 0, []
    for path in FILES:
        head = [l for l in open(path, encoding='utf-8') if l.startswith('#')]
        body = [l for l in open(path, encoding='utf-8') if not l.startswith('#')]
        rows = list(csv.DictReader(io.StringIO(''.join(body))))
        fields = list(rows[0].keys())
        n_in = len(rows)
        changed = 0
        for r in rows:
            k = (r.get('transaction_id') or '').strip()
            if k not in RELEASE:
                continue
            seen.add(k)
            if MARK in (r.get('notes') or ''):
                already.append(k)
                continue
            before = r.get('in_medians')
            r['in_medians'] = '1'
            r['notes'] = ((r.get('notes') or '').strip() + ' ' + NOTE).strip()
            changed += 1
            print('RELEASED %-22s in_medians %s -> 1   mult %s bound %s basis %s'
                  % (k, before, r.get('ev_revenue_x') or r.get('mult'), r.get('bound'), r.get('revenue_basis')))
        if changed:
            out = io.StringIO()
            w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
            w.writeheader()
            w.writerows(rows)
            open(path, 'w', encoding='utf-8').write(''.join(head) + out.getvalue())
        n_out = len(list(csv.DictReader(io.StringIO(''.join(
            l for l in open(path, encoding='utf-8') if not l.startswith('#'))))))
        print('%s: %d rows in, %d out, %d changed, %d dropped' % (path, n_in, n_out, changed, n_in - n_out))
        if n_in != n_out:
            return 1
        changed_total += changed
    missing = sorted(set(RELEASE) - seen)
    if missing:
        print('REFUSED TO CLAIM: %d listed rows were not found: %s' % (len(missing), ', '.join(missing)))
        return 1
    if already:
        print('ALREADY APPLIED on %d rows: %s' % (len(already), ', '.join(already)))
    print('%d of %d rows released this run; still held with a named reason: perplexity-2024-01, marqeta-2020-05'
          % (changed_total, len(RELEASE)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
