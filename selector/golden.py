# -*- coding: utf-8 -*-
"""Snapshot and check the selector's output for the frozen profiles.

  python selector/golden.py --write    regenerate the fixtures (do this deliberately)
  python selector/golden.py            check, exit 1 and print a diff if anything moved
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import match_reference as M
from golden_profiles import PROFILES
FIX = os.path.join(HERE, 'golden')

def snap(prof):
    core, sec, listed_tier = M.peer_groups(prof, M.listed)
    out = {}
    for name, grp in (('core', core), ('secondary', sec)):
        out[name] = [{'company': r['company_name'], 'ticker': r['exchange_ticker'],
                      'family': r['family'], 'score': round(s, 1),
                      'in_medians': r['in_medians'],
                      'reason': M.why_text(prof, r, _w)} for (s, _w), r in grp]
        which, _reason = M.denominator(prof, grp)
        rng = M.group_range(prof, grp, which, listed_tier)
        out[name + '_range'] = {'denominator': which, **({k: round(v, 2) if isinstance(v, float) else v
                                                          for k, v in rng.items()} if rng else {})}
    # private comparables: business nature selects, recency only orders
    picked, months, priv_tier = M.select_private(prof, M.private)
    out['private'] = [{'company': r['company_name'], 'date': r['date'],
                       'type': r['transaction_type'], 'mult': r.get('mult'),
                       'basis': r.get('denominator_basis',''), 'bound': r.get('bound',''),
                       'in_medians': r['in_medians'], 'score': round(s, 1),
                       'reason': M.why_text(prof, r, _w)}
                      for (s, _w), r in picked]
    out['private_window_months'] = months
    out['listed_proximity'] = listed_tier
    out['private_proximity'] = priv_tier
    out['private_range'] = M.private_range(prof, picked, priv_tier)
    return out

def main():
    write = '--write' in sys.argv
    os.makedirs(FIX, exist_ok=True)
    bad = 0
    for key, label, prof in PROFILES:
        got = snap(prof)
        path = os.path.join(FIX, key + '.json')
        if write:
            json.dump({'label': label, 'expected': got}, open(path, 'w'), indent=1, sort_keys=True)
            print('wrote', key); continue
        if not os.path.exists(path):
            print('MISSING FIXTURE', key); bad += 1; continue
        want = json.load(open(path))['expected']
        if want == got: print('ok   ', key); continue
        names_moved = any([x['company'] for x in want.get(g,[])] != [x['company'] for x in got.get(g,[])]
                          or want.get(g+'_range') != got.get(g+'_range') for g in ('core','secondary','private'))
        bad += 1; print('DIFF ' if names_moved else 'SCORE', key, '-', label)
        for grp in ('core', 'secondary', 'private'):
            a = [x['company'] for x in want.get(grp, [])]
            b = [x['company'] for x in got.get(grp, [])]
            if a != b:
                print('   %-9s was: %s' % (grp, ', '.join(a) or '(none)'))
                print('   %-9s now: %s' % ('', ', '.join(b) or '(none)'))
            if want.get(grp+'_range') != got.get(grp+'_range'):
                print('   %-9s range was %s now %s' % (grp, want.get(grp+'_range'), got.get(grp+'_range')))
    if not write:
        print('\n%d of %d profiles moved' % (bad, len(PROFILES)))
    return 1 if bad and not write else 0

if __name__ == '__main__':
    sys.exit(main())
