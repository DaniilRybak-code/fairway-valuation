#!/usr/bin/env python3
"""Three re-tags on Daniil's rulings of 6 September 2026, one idempotent script, count in and out.

1. WIX (listed, data/peers-software-tags.csv). Daniil, 6 Sep late: "Wix is a website builder, no?
   Nothing to do with payments, nothing to do with engineering really. This is just software." It
   carried Cloud & Infrastructure first, Commerce & Payments Software second, function IT &
   Integration. Now Consumer & Prosumer Software first (the same label Framer carries for the same
   kind of business), Business Applications second (the SMB business apps), function Productivity
   (Framer's). Product tags untouched.
2. OWNER (private, data/private-companies-tags.csv). Daniil, 6 Sep afternoon: "Broadly makes sense
   what you did for Owner." The Marketing & Customer Engagement secondary is dropped: measured on
   the morning, it only ever served non-restaurant founders (fundraisly, elentaria, pazi, clarify,
   lightfield, akkari) on the words "ai" and "operations"; Owner stays with marble on real tags.
3. AUDITBOARD (private). "Vertical Software" with industry "Horizontal" contradicts itself; audit
   and compliance workflow sells across industries. Business Applications first, Vertical Software
   second. Measured on the morning: 0 fixtures move.

  python3 tools/apply_retags_6sep.py
"""
import csv, io, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE)
MARK = 'RETAGGED 6-Sep-2026 on Daniil'
PLAN = [
    ('data/peers-software-tags.csv', 'exchange_ticker', 'NASDAQGS:WIX',
     {'archetype': 'Consumer & Prosumer Software', 'archetype_secondary': 'Business Applications', 'function': 'Productivity'},
     'a website builder is software sold to prosumers and small businesses, not cloud infrastructure and not payments (his words, 6 Sep)'),
    ('data/private-companies-tags.csv', 'company_key', 'owner',
     {'archetype_secondary': ''},
     'the Marketing secondary only ever reached non-restaurant founders on generic words; Owner stays with the restaurant back-office founders on real tags'),
    ('data/private-companies-tags.csv', 'company_key', 'auditboard',
     {'archetype': 'Business Applications', 'archetype_secondary': 'Vertical Software'},
     'Vertical Software with a Horizontal end market contradicts itself; compliance workflow sells across industries'),
]
def main():
    rc = 0
    for path in sorted({p for p, *_ in PLAN}):
        head = [l for l in open(path, encoding='utf-8') if l.lstrip('"').startswith('#')]
        body = [l for l in open(path, encoding='utf-8') if not l.lstrip('"').startswith('#')]
        rows = list(csv.DictReader(io.StringIO(''.join(body)))); fields = list(rows[0].keys()); n_in = len(rows)
        changed = 0
        for p, keyf, key, fields_new, why in PLAN:
            if p != path: continue
            hits = [r for r in rows if (r.get(keyf) or '').strip() == key]
            if len(hits) != 1:
                print('REFUSED: %s %s matched %d rows' % (path, key, len(hits))); return 1
            r = hits[0]
            notef = 'taxonomy_note' if 'taxonomy_note' in r else ('notes' if 'notes' in r else None)
            if notef and (MARK + ': ' + key) in (r.get(notef) or ''):
                print('ALREADY APPLIED: %s' % key); continue
            before = {k: r.get(k) for k in fields_new}
            r.update(fields_new)
            if notef:
                r[notef] = ((r.get(notef) or '').strip() + ' ' + MARK + ': ' + key + ', ' + why).strip()
            changed += 1
            print('CHANGED %-14s %s -> %s' % (key, before, fields_new))
        if changed:
            out = io.StringIO(); w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(rows)
            open(path, 'w', encoding='utf-8').write(''.join(head) + out.getvalue())
        n_out = len(list(csv.DictReader(io.StringIO(''.join(l for l in open(path, encoding='utf-8') if not l.lstrip('"').startswith('#'))))))
        print('%s: %d rows in, %d out, %d changed, %d dropped' % (path, n_in, n_out, changed, n_in - n_out))
        if n_in != n_out: rc = 1
    return rc
if __name__ == '__main__':
    sys.exit(main())
