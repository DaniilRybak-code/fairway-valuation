# -*- coding: utf-8 -*-
"""WHY a thin lane is thin, for every fixture the peer-universe gate fails.

Daniil, 3-Sep-2026: "we have enough peers in our dataset to be able to find something relevant for
the companies that we can test. If you believe that next best peer does not exist in our database
at all, then flag it to me and we will try to source."

That is the question this answers, and it separates three causes that look identical on a report and
need completely different work:

  MULTIPLE ON THE WRONG BASIS   we hold the company AND a multiple, but on a denominator this
                                founder is not priced on. Gross revenue where net is needed, or
                                revenue where book is needed. Cost to fix: one figure per company.
  COMPANY HELD, NO MULTIPLE     we hold the company and it matched, but no multiple at all.
                                Cost to fix: a valuation and a denominator for a name we already
                                decided is relevant.
  NOTHING ELSE IN THE FAMILY    the pool this founder can draw from is genuinely exhausted.
                                This is the only one that is a SOURCING request.

Prints the fixture, the lane, the basis the lane needs, and the named rows behind each cause.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import match_reference as M                      # noqa: E402
from golden_profiles import PROFILES             # noqa: E402

LANES = ('core', 'secondary', 'private')


def f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main():
    fixdir = 'selector/golden'
    profs = {k: p for k, l, p in PROFILES}
    thin = []
    for k in sorted(profs):
        fp = os.path.join(fixdir, k + '.json')
        if not os.path.exists(fp):
            continue
        e = json.load(open(fp))['expected']
        for lane in LANES:
            rng = e.get(lane + '_range') or {}
            n = rng.get('n')
            if isinstance(n, int) and n < 2:
                thin.append((k, lane, rng, e))
    print('THIN LANES AND WHY. A lane is thin when fewer than two comparables actually price it.\n')
    sourcing = []
    for key, lane, rng, e in thin:
        prof = profs[key]
        need_basis = M.basis_for(prof)
        need_key = M.BASIS_KEYS[need_basis][0]
        print('=== %s / %s lane | needs %s | has %d ===' % (key, lane, need_basis, rng.get('n') or 0))
        wrong, nomult = [], []
        if lane == 'private':
            picked, _m, _t = M.select_private(prof, M.private)
            for _s, r in picked:
                if f(r.get(need_key)):
                    continue
                other = [(bk, r.get(v[0])) for bk, v in M.BASIS_KEYS.items()
                         if bk != need_basis and f(r.get(v[0]))]
                if other:
                    wrong.append('%s (%s, has %s %s)' % (r['company_name'], r.get('date'),
                                                         other[0][0].lower(), other[0][1]))
                else:
                    nomult.append('%s (%s)' % (r['company_name'], r.get('date')))
            shown = set(r['company_key'] for _s, r in picked)
            cut = min([s for (s, _w), _r in picked] or [0.0])
            # THE SPARE LIST HAS TO CLEAR THE SAME RELEVANCE BAR AS THE LANE ITSELF, or it is not
            # an answer to "is the next best peer in our data", it is a list of everything we hold.
            # The first version used the family gate alone and told me goldfish had 175 spare
            # comparables, which is the whole software universe and no help to anybody.
            spare = []
            for r in M.same_family(prof, M.private):
                if r.get('company_key') in shown or not f(r.get(need_key)):
                    continue
                sc, why = M.score(prof, r, M.WP, use_fin=False)
                if M._relevant(prof, r, why):
                    t = M._tier(prof, r, why)
                    if t != 'BROAD' and sc < cut:
                        t = 'UNDER_CUT'
                    spare.append((sc, '%s [%s]' % (r['company_name'], t)))
            spare = [n for _s, n in sorted(set(spare), reverse=True)]
        else:
            core, sec, _t = M.peer_groups(prof, M.listed)
            grp = core if lane == 'core' else sec
            lkey = M.BASIS_KEYS[need_basis][1]
            for _s, r in grp:
                if f(r.get(lkey)):
                    continue
                nomult.append(r['company_name'])
            shown = set(r['company_name'] for _s, r in core + sec)
            cut = min([s for (s, _w), _r in (core + sec)] or [0.0])
            spare = []
            for r in M.same_family(prof, M.listed):
                if r['company_name'] in shown or not f(r.get(lkey)):
                    continue
                sc, why = M.score(prof, r)
                if M._relevant(prof, r, why):
                    t = M._tier(prof, r, why)
                    if t != 'BROAD' and sc < cut:
                        t = 'UNDER_CUT'
                    spare.append((sc, '%s [%s]' % (r['company_name'], t)))
            spare = [n for _s, n in sorted(set(spare), reverse=True)]
        if wrong:
            print('   MULTIPLE ON THE WRONG BASIS, one figure each away from usable:')
            for x in wrong:
                print('      %s' % x)
        if nomult:
            print('   HELD AND MATCHED BUT CARRIES NO MULTIPLE AT ALL:')
            for x in nomult:
                print('      %s' % x)
        # A SPARE AT BROAD TIER IS NOT A SPARE. Daniil's rule is that nothing unrelated may be
        # shown, and BROAD is the tier for names that share no archetype with the founder. Finn is
        # the case that makes it concrete: Savage X Fenty, Huel and Harry's all score ABOVE its
        # shown names and all price on net revenue, and all three are BROAD. Putting Huel next to a
        # car subscription business with an owned fleet would fill the lane and break the rule the
        # lane exists to keep. So they are listed, and they are not counted as an answer.
        # AND A SPARE BELOW THE LANE'S OWN SCORE CUT IS NOT A SPARE EITHER. The cut is relative to
        # the best name in the lane, so a name can be related, priced, in the right tier and still
        # rank too far behind the leader to belong. DeHaat against Priori Legal is the case: it is
        # ADJACENT and priced on net, and it sits under the cut the lane's own top name sets.
        near = [x for x in spare if '[BROAD]' not in x and '[UNDER_CUT]' not in x]
        if near:
            print('   ALSO RELATED AND PRICED ON THE RIGHT BASIS, NOT SHOWN (%d): %s'
                  % (len(near), ', '.join(near[:8]) + (' ...' if len(near) > 8 else '')))
        else:
            print('   NOTHING RELATED LEFT THAT CARRIES THIS BASIS. This one is a sourcing request.')
            sourcing.append('%s / %s (%s)' % (key, lane, need_basis))
        far = [x for x in spare if '[BROAD]' in x]
        if far and not near:
            print('   (only BROAD-tier names remain, which the no-unrelated-comparable rule bars: %s)'
                  % ', '.join(far[:6]))
        print()
    print('----')
    print('%d thin lanes. %d of them are genuine sourcing requests:' % (len(thin), len(sourcing)))
    for x in sourcing:
        print('   %s' % x)
    return 0


if __name__ == '__main__':
    sys.exit(main())
