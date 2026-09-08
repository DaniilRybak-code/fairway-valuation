#!/usr/bin/env python3
"""A home for supply-chain and logistics SOFTWARE, split out of the operators. Daniil, 8 September
2026 ("Route A"), on the evaluator's verdicts for ekho-labs, bizmark, derya and manifold-robotics.

THE PROBLEM, in numbers. "Commerce Enablement & Fulfilment" holds 28 listed rows: 20 carriers,
forwarders, 3PLs and freight fleets, 3 cold-chain operators, 3 warehouse REITs (Americold, Lineage,
Tritax Big Box) and only 2 software rows (Baozun, BASE). The family map is learned from those rows
by majority, so the archetype is filed in the consumer (asset-heavy) family, and a supply-chain
SOFTWARE company tagged with it was walled off from Kinaxis, Manhattan, Tecsys and Samsara by the
family gate before a single word was scored. Kinaxis shares 3.9 product points with bizmark and
never reached it. E2open (software) reached the same fixtures only because it wore the same wrong
label, and a "world model for freight" was priced off seven parcel carriers.

THE FIX. A new archetype, "Supply Chain & Logistics Software", carried first by the software rows
(Kinaxis, Manhattan, Tecsys; E2open) so that the family map learns it as software, and second
by the platforms that straddle (Samsara's fleet telematics, Freightos's and Full Truck Alliance's
freight marketplaces, Loadsmart, Shiprocket's courier aggregation, which stays with the operators
first so the parcel networks keep it). The operators keep "Commerce Enablement & Fulfilment"
and nothing about them moves. Tecsys keeps its Healthcare end market on purpose (hospital supply
chain is its business, and scheduling-wizard reaches it that way); its archetype was the wrong half.

WHAT ELSE KNOWS ABOUT THE NEW LABEL, all done in the same commit: the software fork routes it
(selector/quiz_fork.py); the investor sector aliases offer the supply-chain funds to it
(selector/investors.py); the profiler's menu picks it up from the tag files by itself; the family
map learns it from the listed rows by itself. Idempotent: run it twice and the second run changes
nothing. Count in and count out on every file; a row count that moves fails the script.

  python3 tools/apply_supply_chain_software_8sep.py
"""
import csv, io, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE)
NEW = 'Supply Chain & Logistics Software'
PLAN = [
    # listed, software file: the archetype moves, the secondary and end market stay
    ('data/peers-software-tags.csv', 'exchange_ticker', 'TSX:KXS',
     {'archetype': NEW, 'archetype_secondary': 'Business Applications'},
     'supply-chain planning software, not a logistics operator'),
    ('data/peers-software-tags.csv', 'exchange_ticker', 'NASDAQGS:MANH',
     {'archetype': NEW, 'archetype_secondary': 'Business Applications'},
     'warehouse and transport management software, not a logistics operator'),
    ('data/peers-software-tags.csv', 'exchange_ticker', 'TSX:TCS',
     {'archetype': NEW, 'archetype_secondary': 'Vertical Software'},
     'supply-chain execution software; keeps its Healthcare end market, which is its market'),
    ('data/peers-software-tags.csv', 'exchange_ticker', 'NYSE:IOT',
     {'archetype_secondary': NEW},
     'fleet telematics is the software side of logistics; Vertical Software stays first'),
    # listed, logistics file: two freight marketplaces gain the software label second
    ('data/peers-logistics-services-tags.csv', 'exchange_ticker', 'NASDAQGM:CRGO',
     {'archetype_secondary': NEW},
     'a digital freight booking platform straddles marketplace and logistics software'),
    ('data/peers-logistics-services-tags.csv', 'exchange_ticker', 'NYSE:YMM',
     {'archetype_secondary': NEW},
     'a freight-matching platform is software, not a carrier; was Commerce Enablement second'),
    # private
    ('data/private-companies-tags.csv', 'company_key', 'e2open',
     {'archetype': NEW, 'archetype_secondary': 'Business Applications'},
     'supply-chain software; was filed with the carriers and reached founders only on that error'),
    ('data/private-companies-tags.csv', 'company_key', 'shiprocket',
     {'archetype': 'Commerce Enablement & Fulfilment', 'archetype_secondary': NEW},
     'a courier-aggregation platform gains the software label SECOND; it stays with the operators first so the parcel networks (byrd, hived, 99minutos) keep it'),
    ('data/private-companies-tags.csv', 'company_key', 'loadsmart',
     {'archetype_secondary': NEW},
     'digital freight brokerage with its own TMS software; marketplace first, software second'),
]
MARK = 'RETAGGED 8-Sep-2026 (Route A, supply-chain software)'


def _split(path):
    lines = open(path, encoding='utf-8').read().splitlines(keepends=True)
    head = [l for l in lines if l.lstrip('"').startswith('#')]
    body = [l for l in lines if not l.lstrip('"').startswith('#')]
    return head, body


def main():
    rc = 0
    for path in sorted({p for p, *_ in PLAN}):
        head, body = _split(path)
        rows = list(csv.DictReader(io.StringIO(''.join(body))))
        fields = list(rows[0].keys()); n_in = len(rows); changed = 0
        for p, keyf, key, new, why in PLAN:
            if p != path: continue
            hits = [r for r in rows if (r.get(keyf) or '').strip() == key]
            if len(hits) != 1:
                print('REFUSED: %s %s matched %d rows' % (path, key, len(hits))); return 1
            r = hits[0]
            if all((r.get(k) or '') == v for k, v in new.items()):
                print('ALREADY APPLIED: %-16s %s' % (key, r['company_name'])); continue
            before = {k: r.get(k) for k in new}
            r.update(new)
            notef = 'taxonomy_note' if 'taxonomy_note' in r else None
            if notef:
                r[notef] = ((r.get(notef) or '').strip() + ' ' + MARK + ': ' + why).strip()
            changed += 1
            print('CHANGED %-16s %-28s %s -> %s' % (key, r['company_name'][:28], before, new))
        if changed:
            out = io.StringIO()
            w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(rows)
            open(path, 'w', encoding='utf-8').write(''.join(head) + out.getvalue())
        n_out = len(list(csv.DictReader(io.StringIO(''.join(_split(path)[1])))))
        print('%s: %d rows in, %d out, %d changed, %d dropped' % (path, n_in, n_out, changed, n_in - n_out))
        if n_in != n_out: rc = 1
    return rc


if __name__ == '__main__':
    sys.exit(main())
