# -*- coding: utf-8 -*-
"""Apply the UNAMBIGUOUS verdicts from Fable's 1-Sep basis audit.

Only the flips with no open question are applied here. Zepz is held back because it needs Daniil's
denominator ruling, and Scale AI / Invisible are held because they need his staffing-equivalence
ruling. Each change records its own reason in the notes column so nothing moves silently.

  python3 tools/apply_basis_verdicts_1sep.py          # dry run
  python3 tools/apply_basis_verdicts_1sep.py --write
"""
import csv, io, os, sys

WRITE = '--write' in sys.argv
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# company, date -> (new basis, new in_medians or None to leave, why)
VERDICTS = {
 ('Delhivery', 'May-21'): ('NET_REVENUE', '1',
   'BASIS FLIPPED 1-Sep-2026 on Fable audit, verified. Delhivery OPERATES its own network and sells '
   'its own delivery service; fleet partners and line-haul are its COSTS, not other people\'s money '
   'inside the line. The old note described a freight BROKER. The test is ownership: a carrier keeps '
   'the fee it charges. Compare Shiprocket, which resells other couriers and stays GROSS.'),
 ('Xpressbees', 'Feb-22'): ('NET_REVENUE', '1',
   'BASIS FLIPPED 1-Sep-2026 on Fable audit, verified. Same reasoning as Delhivery: operator, not '
   'broker. COD cash it collects belongs to merchants but is a balance-sheet item and never touches '
   'the revenue line.'),
 ('OLIPOP', 'Feb-25'): ('NET_REVENUE', None,
   'BASIS FLIPPED 1-Sep-2026 on Fable audit. These are OLIPOP\'s own wholesale sales, not retail '
   'scanner sell-through, so the company keeps the whole price. A first-party brand is NET in our '
   'sense however large the number looks. No value change; it was already in medians.'),
}

def load(path):
    raw = open(path).read().splitlines(True)
    head = [l for l in raw if l.lstrip().lstrip('"').startswith('#')]
    body = [l for l in raw if not l.lstrip().lstrip('"').startswith('#')]
    rdr = csv.DictReader(io.StringIO(''.join(body)))
    return head, rdr.fieldnames, list(rdr)

changed = 0
for path in ('data/private-rounds.csv', 'data/private-rounds-consumer.csv'):
    p = os.path.join(HERE, path)
    head, cols, rows = load(p)
    touched = False
    for r in rows:
        key = ((r.get('company_name') or '').strip(), (r.get('date') or '').strip())
        if key not in VERDICTS:
            continue
        basis, medians, why = VERDICTS[key]
        print('%-12s %-7s  basis %s -> %s' % (key[0], key[1], r.get('revenue_basis'), basis), end='')
        r['revenue_basis'] = basis
        if medians is not None and 'in_medians' in r:
            print('   in_medians %s -> %s' % (r.get('in_medians'), medians), end='')
            r['in_medians'] = medians
        print()
        if 'notes' in r:
            r['notes'] = ((r.get('notes') or '').strip() + '  ' + why).strip()
        touched = True; changed += 1
    if touched and WRITE:
        with open(p, 'w', newline='') as f:
            f.writelines(head)
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, '') for k in cols})
print()
print('%d rows %s' % (changed, 'WRITTEN' if WRITE else 'would change (dry run)'))
