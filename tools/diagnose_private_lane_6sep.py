# -*- coding: utf-8 -*-
"""Why does a fixture's private lane not price? Every held round in its archetype, one line each.

Fable, 6-Sep-2026, task (1) of the matching-refinement brief. Reads the engine as it is; changes
nothing. For a fixture, this lists EVERY private round that shares an archetype slot with the
founder (the widest pool the archetype fallback could ever reach) and says, for each, which fence
stops it and whether it could price on the founder's net or gross reading.

    python3 tools/diagnose_private_lane_6sep.py levelten manifold-robotics tash
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
import match_reference as M                      # noqa: E402
from golden_profiles import PROFILES             # noqa: E402

ASOF = (2026, 8)


def months_old(iso):
    y, m = int(iso[:4]), int(iso[5:7])
    return (ASOF[0] - y) * 12 + (ASOF[1] - m)


def diagnose(key):
    prof = next(p for k, _l, p in PROFILES if k == key)
    mine = {prof.get('archetype'), prof.get('archetype_secondary')} - {None, ''}
    picked, months, tier = M.select_private(prof, M.private)
    picked_ids = {r['transaction_id'] for _sw, r in picked}
    fam = set(id(r) for r in M.same_family(prof, M.private))
    bs = set(id(r) for r in M.balance_sheet_compatible(prof, M.private))
    pband = (prof.get('growth_band') or M.band_of(prof.get('growth')) or '').upper()
    print('=' * 100)
    print('%s   archetypes %s   industry %s   founder basis %s' % (
        key, sorted(mine), prof.get('industry'), M.basis_for(prof)))
    print('picked today: %s   tier %s   oldest %d months' % (
        [r['company_name'] for _sw, r in picked], tier, months))
    pool = [r for r in M.private if ({r.get('archetype'), r.get('archetype_secondary')} & mine)]
    print('%d private rounds share an archetype slot with this founder\n' % len(pool))
    hdr = '%-24s %-7s %-4s %6s %-24s %-15s %6s %6s %-5s %-9s %s'
    print(hdr % ('company', 'date', 'age', 'score', 'route', 'tier', 'net', 'gross', 'inmed',
                 'gate', 'verdict'))
    counts = {}
    for r in sorted(pool, key=lambda r: -M.score(prof, r, M.WP, use_fin=False)[0]):
        sc, why = M.score(prof, r, M.WP, use_fin=False)
        route = M.relevance_route(prof, r, why) or 'NO ROUTE'
        t = M._tier(prof, r, why)
        net = M.basis_mult(prof, r, 'mult', basis='REVENUE')
        gross = M.basis_mult(prof, r, 'mult', basis='REVENUE_GROSS')
        inmed = r.get('in_medians', True)
        age = months_old(r['date_iso'])
        gate = r.get('display_gate') or '-'
        # THE ORDER OF THE FENCES, as _select_private_strict applies them.
        if id(r) not in fam:
            v = 'family gate'
        elif id(r) not in bs:
            v = 'lender fence'
        elif pband and not M.band_compatible(pband, r.get('growth_band')):
            v = 'growth band'
        elif gate == 'NO_FIELD':
            v = 'display gate NO_FIELD'
        elif gate == 'CLOSE_MATCH_ONLY' and M._tag_points(why) < M.FLOOR_TAG_EVIDENCE:
            v = 'display gate CLOSE_MATCH_ONLY'
        elif route == 'NO ROUTE':
            v = 'RELEVANCE GATE (no shared word, no shared end market)'
        elif route == 'ARCHETYPE FALLBACK':
            v = 'RELEVANCE GATE (archetype only; fallback territory)'
        elif sc < M.FLOOR_ABS:
            v = 'score floor %.1f' % M.FLOOR_ABS
        elif t == 'DIRECT' and sc < M.FLOOR_ADEQUATE:
            v = 'adequacy floor %.1f (DIRECT)' % M.FLOOR_ADEQUATE
        elif r['transaction_id'] not in picked_ids:
            v = 'passes gates, not picked (trim / one round per company)'
        else:
            v = 'PICKED'
        if v == 'PICKED' or v.startswith('passes'):
            if net is None and gross is None:
                v += '; NO REVENUE MULTIPLE'
            elif not inmed:
                v += '; in_medians=0'
        counts[v.split(';')[0]] = counts.get(v.split(';')[0], 0) + 1
        print(hdr % (r['company_name'][:24], r['date'], '%dm' % age, '%.1f' % sc, route[:24],
                     t, '-' if net is None else '%.2f' % net,
                     '-' if gross is None else '%.2f' % gross,
                     'Y' if inmed else 'N', gate, v))
    print()
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print('   %3d  %s' % (v, k))
    print()


if __name__ == '__main__':
    for k in sys.argv[1:] or ('levelten', 'manifold-robotics', 'tash'):
        diagnose(k)
