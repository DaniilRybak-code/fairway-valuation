# -*- coding: utf-8 -*-
"""Snapshot and check the selector's output for the frozen profiles.

  python selector/golden.py --write    regenerate the fixtures (do this deliberately)
  python selector/golden.py            check, exit 1 and print a diff if anything moved
  python selector/golden.py --peers    report coverage against the frozen human peer sets
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import match_reference as M
from golden_profiles import PROFILES, EXPECTED_PEERS, peer_hit
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

def peer_coverage():
    """How much of the human peer set the engine actually surfaced, fixture by fixture.

    Reports. Does not assert. A peer we do not hold in the file cannot be surfaced, so a low number
    is usually a data gap rather than a matcher defect: read it next to the sourcing list before
    touching weights. See the note above EXPECTED_PEERS in golden_profiles.py for why this is a
    frozen input and not a live search.
    """
    have = [(k, l, p) for k, l, p in PROFILES if EXPECTED_PEERS.get(k)]
    if not have:
        print('No expected peer sets recorded yet. Run the two searches for a fixture and add it')
        print('to EXPECTED_PEERS in golden_profiles.py.')
        return 0
    tot_hit = tot_held = tot_exp = 0
    universe = ([r['company_name'] for r in M.listed]
                + [r['company_name'] for r in M.private])
    for key, label, prof in have:
        spec = EXPECTED_PEERS[key]
        got = snap(prof)
        names = ([x['company'] for x in got.get('core', [])]
                 + [x['company'] for x in got.get('secondary', [])]
                 + [x['company'] for x in got.get('private', [])])
        hits = [e for e in spec['peers'] if peer_hit(e, names)]
        held = [e for e in spec['peers'] if peer_hit(e, universe)]
        # A peer we do not hold in the file cannot be surfaced. Separating the two is the whole
        # point: the first column is a matcher question, the third is a sourcing question.
        held_missed = [e for e in held if e not in hits]
        absent = [e for e in spec['peers'] if e not in held]
        tot_hit += len(hits); tot_held += len(held); tot_exp += len(spec['peers'])
        print('%-16s surfaced %d  held %d  human set %d   %s'
              % (key, len(hits), len(held), len(spec['peers']), spec.get('confidence', '')))
        if hits: print('    surfaced       ', ', '.join(hits))
        if held_missed: print('    HELD, NOT SHOWN', ', '.join(held_missed))
        if absent: print('    not in our data', ', '.join(absent))
    print('\n%d fixtures, %d human-verified peers between them.' % (len(have), tot_exp))
    print('  %3d of those peers exist anywhere in our data (%.0f%%)   <- SOURCING'
          % (tot_held, 100.0 * tot_held / tot_exp if tot_exp else 0))
    print('  %3d of the %d we hold were actually surfaced          <- MATCHER'
          % (tot_hit, tot_held))
    print('%d of %d fixtures have a human peer set recorded' % (len(have), len(PROFILES)))
    return 0


def main():
    if '--peers' in sys.argv: return peer_coverage()
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
